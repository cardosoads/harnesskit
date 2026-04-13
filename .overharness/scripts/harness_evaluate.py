#!/usr/bin/env python3
"""
OverHarness Harness Evaluation Runner.

Reads an active Harness contract, runs applicable sensors, and writes a
durable Markdown evaluation artifact for Amy or a future retry loop.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Any

try:
    import yaml  # type: ignore
except Exception:  # pragma: no cover - reported at runtime
    yaml = None


@dataclass
class SensorResult:
    sensor_id: str
    required: bool
    command: str
    status: str
    exit_status: int | None
    output_summary: str
    blocks_completion: bool


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def load_yaml(path: Path) -> dict[str, Any]:
    if yaml is None:
        raise RuntimeError("PyYAML is required to read sensors.yaml")
    data = yaml.safe_load(read_text(path))
    return data if isinstance(data, dict) else {}


def newest_contract(active_dir: Path) -> Path:
    contracts = sorted(
        [path for path in active_dir.glob("*.md") if path.is_file()],
        key=lambda path: path.stat().st_mtime,
        reverse=True,
    )
    if not contracts:
        raise FileNotFoundError(f"No active contracts found in {active_dir}")
    return contracts[0]


def resolve_cli_path(root: Path, value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else root / path


def contract_id_from_path(contract_path: Path) -> str:
    return contract_path.stem


def evaluation_id_for(contract_id: str) -> str:
    if contract_id.startswith("HC-"):
        return "EV-" + contract_id[3:]
    return "EV-" + contract_id


def extract_risk(contract_text: str) -> str:
    match = re.search(r"^\|\s*Risk\s*\|\s*([^|]+?)\s*\|$", contract_text, re.MULTILINE)
    if match:
        return match.group(1).strip().lower()
    match = re.search(r"^\*\*Risk level:\*\*\s*(.+)$", contract_text, re.MULTILINE)
    if match:
        return match.group(1).strip().lower()
    return "unknown"


def extract_must_haves(contract_text: str) -> list[tuple[str, str]]:
    results: list[tuple[str, str]] = []
    pattern = re.compile(r"^###\s+(MH-[0-9A-Za-z-]+)\s+[-—]\s+(.+)$", re.MULTILINE)
    for match in pattern.finditer(contract_text):
        results.append((match.group(1).strip(), match.group(2).strip()))
    return results


def package_scripts(root: Path) -> dict[str, str]:
    package_json = root / "package.json"
    if not package_json.exists():
        return {}
    try:
        data = json.loads(read_text(package_json))
    except Exception:
        return {}
    scripts = data.get("scripts", {})
    return scripts if isinstance(scripts, dict) else {}


def command_exists(root: Path, command: str) -> bool:
    script_match = re.match(r"^bash\s+(.+)$", command)
    if script_match:
        return (root / script_match.group(1).strip()).exists()
    if command == "pytest":
        return (root / "pyproject.toml").exists() or (root / "pytest.ini").exists() or (root / "tests").exists()
    npm_match = re.match(r"^npm\s+run\s+([A-Za-z0-9:_-]+)$", command)
    if npm_match:
        return npm_match.group(1) in package_scripts(root)
    if command == "npx playwright test":
        return any((root / name).exists() for name in ("playwright.config.ts", "playwright.config.js", "playwright.config.mjs"))
    return True


def enabled_by_condition(root: Path, condition: str, command: str) -> tuple[bool, str]:
    condition = condition.strip()
    if not condition:
        return True, "no enabled_when condition"
    if condition.endswith(" exists"):
        path_text = condition[: -len(" exists")].strip()
        return (root / path_text).exists(), condition
    if condition == "package.json has a lint script":
        return "lint" in package_scripts(root), condition
    if condition == "package.json has a test script":
        return "test" in package_scripts(root), condition
    if condition == "package.json has a typecheck script":
        return "typecheck" in package_scripts(root), condition
    if condition == "pyproject.toml, pytest.ini, or tests/ indicates pytest":
        return command_exists(root, "pytest"), condition
    if condition == "playwright config exists and the change is UI-visible":
        return command_exists(root, "npx playwright test"), condition
    if condition == "artifact was generated from a template":
        return True, condition
    return command_exists(root, command), f"fallback command availability for: {condition}"


def summarize_output(stdout: str, stderr: str, max_lines: int = 18) -> str:
    combined = (stdout + "\n" + stderr).strip()
    if not combined:
        return "_No output._"
    lines = combined.splitlines()
    if len(lines) > max_lines:
        clipped = lines[:max_lines]
        clipped.append(f"... output truncated ({len(lines) - max_lines} more lines)")
        lines = clipped
    return "\n".join(lines)


def run_sensor(root: Path, sensor: dict[str, Any], required: bool, timeout_seconds: int) -> SensorResult:
    sensor_id = str(sensor.get("id", "unknown-sensor"))
    command = str(sensor.get("command", "")).strip()
    condition = str(sensor.get("enabled_when", "")).strip()
    enabled, reason = enabled_by_condition(root, condition, command)
    if not command:
        return SensorResult(sensor_id, required, command, "INVALID", None, "Sensor has no command.", required)
    if not enabled:
        status = "UNAVAILABLE" if required else "SKIPPED"
        return SensorResult(sensor_id, required, command, status, None, f"Condition not met: {reason}", required)

    try:
        proc = subprocess.run(
            command,
            cwd=root,
            shell=True,
            text=True,
            capture_output=True,
            timeout=timeout_seconds,
        )
    except subprocess.TimeoutExpired as exc:
        output = summarize_output(exc.stdout or "", exc.stderr or "")
        return SensorResult(sensor_id, required, command, "TIMEOUT", None, output, required)

    status = "PASS" if proc.returncode == 0 else "FAIL"
    return SensorResult(
        sensor_id=sensor_id,
        required=required,
        command=command,
        status=status,
        exit_status=proc.returncode,
        output_summary=summarize_output(proc.stdout, proc.stderr),
        blocks_completion=required and proc.returncode != 0,
    )


def collect_sensor_results(
    root: Path,
    sensors: dict[str, Any],
    sensor_group: str,
    include_recommended: bool,
    timeout_seconds: int,
) -> list[SensorResult]:
    groups = sensors.get("sensor_groups", {})
    group = groups.get(sensor_group, {}) if isinstance(groups, dict) else {}
    if not isinstance(group, dict):
        raise KeyError(f"Sensor group not found: {sensor_group}")

    results: list[SensorResult] = []
    for sensor in group.get("required", []) or []:
        if isinstance(sensor, dict):
            results.append(run_sensor(root, sensor, True, timeout_seconds))
    for sensor in group.get("recommended", []) or []:
        if not isinstance(sensor, dict):
            continue
        if include_recommended:
            results.append(run_sensor(root, sensor, False, timeout_seconds))
        else:
            results.append(
                SensorResult(
                    sensor_id=str(sensor.get("id", "unknown-sensor")),
                    required=False,
                    command=str(sensor.get("command", "")).strip(),
                    status="SKIPPED",
                    exit_status=None,
                    output_summary="Recommended sensor not requested. Re-run with --include-recommended to execute it.",
                    blocks_completion=False,
                )
            )
    return results


def verdict(results: list[SensorResult]) -> tuple[str, str, str]:
    required = [result for result in results if result.required]
    blocking = [result for result in required if result.status in {"FAIL", "TIMEOUT", "INVALID", "UNAVAILABLE"}]
    if blocking:
        return (
            "BLOCKED",
            "0.00",
            "One or more required sensors failed or were unavailable. Fix the blocking sensors or document an approved baseline exception before completion.",
        )
    if required and all(result.status == "PASS" for result in required):
        return (
            "APPROVED",
            "1.00",
            "All required sensors passed. Semantic review is still required when the contract risk level routes to Amy.",
        )
    return (
        "NEEDS_FIX",
        "0.50",
        "The runner did not collect a complete required sensor set. Review the sensor policy and rerun.",
    )


def render_markdown(
    project_name: str,
    evaluation_id: str,
    contract_id: str,
    contract_path: Path,
    risk: str,
    must_haves: list[tuple[str, str]],
    results: list[SensorResult],
    final_verdict: str,
    score: str,
    recommendation: str,
) -> str:
    today = datetime.now().strftime("%Y-%m-%d")
    lines = [
        f"# Harness Evaluation: {evaluation_id}",
        "",
        "| Field | Value |",
        "| --- | --- |",
        f"| Project | {project_name} |",
        f"| Evaluation | {evaluation_id} |",
        f"| Contract | {contract_id} |",
        f"| Contract Path | `{contract_path}` |",
        f"| Date | {today} |",
        "| Evaluator | harness-evaluate |",
        f"| Risk | {risk} |",
        f"| Verdict | {final_verdict} |",
        f"| Score | {score} |",
        "",
        "## Contract Coverage",
        "",
    ]
    if must_haves:
        for must_id, truth in must_haves:
            lines.extend(
                [
                    f"### {must_id} - RECORDED",
                    "",
                    f"**Expected truth:** {truth}",
                    "",
                    "**Evidence:** Sensor evidence is recorded below. Semantic verification remains with Amy when the contract risk requires evaluator review.",
                    "",
                    "**Finding:** Not failed by the mechanical runner.",
                    "",
                    "**Required follow-up:** Amy should review this must-have against the implementation artifact when risk routing requires it.",
                    "",
                    "---",
                    "",
                ]
            )
    else:
        lines.extend(["No must-haves were parsed from the contract.", ""])

    lines.extend(["## Sensor Results", ""])
    for result in results:
        lines.extend(
            [
                f"### {result.sensor_id} - {result.status}",
                "",
                f"**Command:** `{result.command}`",
                "",
                f"**Required:** {'yes' if result.required else 'no'}",
                "",
                f"**Exit status:** {result.exit_status if result.exit_status is not None else 'n/a'}",
                "",
                "**Output summary:**",
                "",
                "```text",
                result.output_summary,
                "```",
                "",
                f"**Blocks completion:** {'yes' if result.blocks_completion else 'no'}",
                "",
                "---",
                "",
            ]
        )

    lines.extend(
        [
            "## Deviations",
            "",
            "- None recorded by the mechanical runner.",
            "",
            "## Verdict Rules",
            "",
            "- `APPROVED`: all required sensors passed.",
            "- `NEEDS_FIX`: one or more required checks are incomplete but fixable within current scope.",
            "- `BLOCKED`: required sensor failed, timed out, was unavailable, or the scope needs a decision.",
            "- `ESCALATE`: human decision required.",
            "",
            "## Final Recommendation",
            "",
            recommendation,
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Run Harness sensors and write an evaluation artifact.")
    parser.add_argument("--root", default=".", help="Project root")
    parser.add_argument("--contract", help="Path to an active Harness contract. Defaults to newest active contract.")
    parser.add_argument("--sensor-group", default="implementation", help="Sensor group from .overharness/harness/sensors.yaml")
    parser.add_argument("--output", help="Evaluation output path. Defaults to .overharness/harness/evaluations/<evaluation-id>.md")
    parser.add_argument("--include-recommended", action="store_true", help="Run recommended sensors as well as required sensors")
    parser.add_argument("--timeout", type=int, default=120, help="Timeout per sensor command in seconds")
    parser.add_argument("--format", choices=["text", "json"], default="text")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    overharness = root / ".overharness"
    if not overharness.exists():
        raise SystemExit(f"No .overharness directory found under {root}")

    if args.contract:
        contract_path = resolve_cli_path(root, args.contract).resolve()
    else:
        try:
            contract_path = newest_contract(overharness / "harness" / "contracts" / "active")
        except FileNotFoundError as exc:
            raise SystemExit(str(exc)) from None
    if not contract_path.exists():
        raise SystemExit(f"Contract does not exist: {contract_path}")

    sensors_path = overharness / "harness" / "sensors.yaml"
    if not sensors_path.exists():
        raise SystemExit(f"Sensor policy does not exist: {sensors_path}")

    config = load_yaml(overharness / "overharness.yaml") if (overharness / "overharness.yaml").exists() else {}
    project_name = str(config.get("project", {}).get("name", root.name))
    contract_text = read_text(contract_path)
    contract_id = contract_id_from_path(contract_path)
    evaluation_id = evaluation_id_for(contract_id)
    output_path = resolve_cli_path(root, args.output).resolve() if args.output else overharness / "harness" / "evaluations" / f"{evaluation_id}.md"

    sensors = load_yaml(sensors_path)
    results = collect_sensor_results(root, sensors, args.sensor_group, args.include_recommended, args.timeout)
    final_verdict, score, recommendation = verdict(results)
    markdown = render_markdown(
        project_name=project_name,
        evaluation_id=evaluation_id,
        contract_id=contract_id,
        contract_path=contract_path,
        risk=extract_risk(contract_text),
        must_haves=extract_must_haves(contract_text),
        results=results,
        final_verdict=final_verdict,
        score=score,
        recommendation=recommendation,
    )
    write_text(output_path, markdown)

    if args.format == "json":
        print(
            json.dumps(
                {
                    "verdict": final_verdict,
                    "score": score,
                    "contract": str(contract_path),
                    "evaluation": str(output_path),
                    "sensor_results": [asdict(result) for result in results],
                },
                indent=2,
            )
        )
    else:
        print(f"Harness evaluation written: {output_path}")
        print(f"Verdict: {final_verdict}")
        print(f"Required sensors: {sum(1 for result in results if result.required)}")
        print(f"Blocking sensors: {sum(1 for result in results if result.blocks_completion)}")

    return 1 if final_verdict == "BLOCKED" else 0


if __name__ == "__main__":
    sys.exit(main())
