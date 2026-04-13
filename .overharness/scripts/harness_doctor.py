#!/usr/bin/env python3
"""
OverHarness Harness Doctor.

Checks feedforward and feedback readiness:
- feedforward: specs, state, artifacts, contracts, required context
- feedback: sensor policy, discovered checks, implementation evidence
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass, asdict
from datetime import date, datetime
from pathlib import Path
from typing import Any

try:
    import yaml  # type: ignore
except Exception:  # pragma: no cover - reported at runtime
    yaml = None


PLACEHOLDER_RE = re.compile(r"(\{\{[^}]+\}\}|\bTODO\b|\bTBD\b)", re.IGNORECASE)


@dataclass
class Issue:
    severity: str
    plane: str
    code: str
    message: str
    file: str = ""
    baseline: str = ""
    baseline_expires_at: str = ""


def rel(root: Path, path: Path | str) -> str:
    try:
        return str(Path(path).resolve().relative_to(root.resolve()))
    except Exception:
        return str(path)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def load_json(path: Path, issues: list[Issue], plane: str, code: str) -> dict[str, Any]:
    try:
        return json.loads(read_text(path))
    except Exception as exc:
        issues.append(Issue("error", plane, code, f"Invalid JSON: {exc}", str(path)))
        return {}


def load_yaml(path: Path, issues: list[Issue], plane: str, code: str) -> dict[str, Any]:
    if yaml is None:
        issues.append(Issue("error", plane, "missing_pyyaml", "PyYAML is required for harness doctor YAML checks", str(path)))
        return {}
    try:
        data = yaml.safe_load(read_text(path))
        return data if isinstance(data, dict) else {}
    except Exception as exc:
        issues.append(Issue("error", plane, code, f"Invalid YAML: {exc}", str(path)))
        return {}


def word_count(path: Path) -> int:
    if not path.exists() or path.name == ".gitkeep":
        return 0
    return len(re.findall(r"\S+", read_text(path)))


def add_missing_file(issues: list[Issue], root: Path, plane: str, path: Path, severity: str = "error") -> None:
    issues.append(Issue(severity, plane, "missing_file", f"Required file is missing: {rel(root, path)}", rel(root, path)))


def check_file_substance(
    root: Path,
    issues: list[Issue],
    plane: str,
    path: Path,
    min_words: int,
    code_prefix: str,
    allow_template_markers: bool = False,
) -> None:
    if not path.exists():
        add_missing_file(issues, root, plane, path)
        return
    if path.name == ".gitkeep":
        return
    wc = word_count(path)
    if wc < min_words:
        issues.append(Issue("warning", plane, f"{code_prefix}_thin_content", f"{rel(root, path)} has only {wc} words; expected at least {min_words}", rel(root, path)))
    text = read_text(path)
    placeholder_lines = []
    if not allow_template_markers:
        placeholder_lines = [
            str(index)
            for index, line in enumerate(text.splitlines(), start=1)
            if PLACEHOLDER_RE.search(line)
        ]
    if placeholder_lines:
        sample = ", ".join(placeholder_lines[:8])
        suffix = "..." if len(placeholder_lines) > 8 else ""
        issues.append(Issue("warning", plane, f"{code_prefix}_placeholder", f"{rel(root, path)} has unresolved template/TODO markers at lines {sample}{suffix}", rel(root, path)))


def collect_workflow_steps(workflow: dict[str, Any]) -> set[str]:
    steps = workflow.get("workflow", {}).get("steps", [])
    if not isinstance(steps, list):
        return set()
    return {str(step.get("id")) for step in steps if isinstance(step, dict) and step.get("id")}


def baseline_matches(issue: Issue, baseline: dict[str, Any]) -> bool:
    if issue.severity == "error":
        return False
    if str(baseline.get("plane", "")) != issue.plane:
        return False
    if str(baseline.get("code", "")) != issue.code:
        return False
    baseline_file = str(baseline.get("file", ""))
    if baseline_file and baseline_file != issue.file:
        return False
    message_contains = baseline.get("message_contains")
    if message_contains and str(message_contains) not in issue.message:
        return False
    return True


def parse_baseline_expiration(value: Any) -> tuple[str, date | None, str]:
    if value is None:
        return "", None, "missing"
    if isinstance(value, datetime):
        expires = value.date()
        return expires.isoformat(), expires, ""
    if isinstance(value, date):
        return value.isoformat(), value, ""
    try:
        expires = date.fromisoformat(str(value))
    except ValueError:
        return str(value), None, "invalid"
    return expires.isoformat(), expires, ""


def apply_baselines(root: Path, issues: list[Issue]) -> None:
    baseline_path = root / ".overharness" / "harness" / "baselines" / "current.yaml"
    if not baseline_path.exists():
        return
    baseline_doc = load_yaml(baseline_path, issues, "feedback", "invalid_baseline")
    entries = baseline_doc.get("accepted_issues", [])
    if not isinstance(entries, list):
        issues.append(Issue("warning", "feedback", "invalid_baseline_entries", "baselines/current.yaml accepted_issues must be a list", rel(root, baseline_path)))
        return

    for issue in issues:
        if issue.severity == "error":
            continue
        for entry in entries:
            if not isinstance(entry, dict):
                continue
            if baseline_matches(issue, entry):
                baseline_id = str(entry.get("id", "baseline"))
                expires_at, expires_on, expiration_error = parse_baseline_expiration(entry.get("expires_at"))
                if expiration_error == "missing":
                    issues.append(Issue("warning", "feedback", "baseline_missing_expiration", f"Baseline '{baseline_id}' matches a finding but has no expires_at date", rel(root, baseline_path)))
                    break
                if expiration_error == "invalid":
                    issues.append(Issue("warning", "feedback", "baseline_invalid_expiration", f"Baseline '{baseline_id}' has invalid expires_at: {expires_at}", rel(root, baseline_path)))
                    break
                if expires_on and expires_on < date.today():
                    issues.append(Issue("warning", "feedback", "baseline_expired", f"Baseline '{baseline_id}' expired on {expires_at}; finding is no longer accepted", rel(root, baseline_path)))
                    break
                issue.severity = "info"
                issue.baseline = baseline_id
                issue.baseline_expires_at = expires_at
                issue.message = f"{issue.message} [baseline: {issue.baseline}, expires: {expires_at}]"
                break


def check_feedforward(root: Path, issues: list[Issue]) -> None:
    overharness = root / ".overharness"
    feedforward_path = overharness / "harness" / "feedforward.yaml"
    if not feedforward_path.exists():
        add_missing_file(issues, root, "feedforward", feedforward_path)
        feedforward = {}
    else:
        feedforward = load_yaml(feedforward_path, issues, "feedforward", "invalid_feedforward")

    required_context = feedforward.get("required_context", [])
    if not required_context:
        required_context = [
            {"path": "CLAUDE.md", "min_words": 80, "severity": "error"},
            {"path": ".overharness/overharness.yaml", "min_words": 80, "severity": "error"},
            {"path": ".overharness/state.json", "min_words": 20, "severity": "error"},
            {"path": ".overharness/core/constitution.md", "min_words": 120, "severity": "error"},
            {"path": ".overharness/core/engine/workflow-engine.md", "min_words": 200, "severity": "error"},
            {"path": ".overharness/core/engine/state-machine.md", "min_words": 160, "severity": "error"},
            {"path": ".overharness/harness/HARNESS.md", "min_words": 150, "severity": "error"},
            {"path": ".overharness/harness/templates/contract-template.md", "min_words": 120, "severity": "error"},
        ]
    for item in required_context:
        if not isinstance(item, dict):
            continue
        path_value = item.get("path")
        if not path_value:
            continue
        path = root / str(path_value)
        severity = str(item.get("severity", "error"))
        if not path.exists():
            add_missing_file(issues, root, "feedforward", path, severity)
        else:
            check_file_substance(
                root,
                issues,
                "feedforward",
                path,
                int(item.get("min_words", 20)),
                "context",
                bool(item.get("allow_template_markers", False)),
            )

    config = load_yaml(overharness / "overharness.yaml", issues, "feedforward", "invalid_config") if (overharness / "overharness.yaml").exists() else {}
    state = load_json(overharness / "state.json", issues, "feedforward", "invalid_state") if (overharness / "state.json").exists() else {}

    project_type = state.get("project_type") or config.get("project", {}).get("project_type")
    if not project_type:
        issues.append(Issue("error", "feedforward", "missing_project_type", "No project_type found in state.json or overharness.yaml"))

    active_specs = config.get("specs", {}).get("active", [])
    if not active_specs:
        issues.append(Issue("warning", "feedforward", "missing_active_specs", "No active specs declared in overharness.yaml", "overharness.yaml"))
    for spec in active_specs:
        spec_path = overharness / "specs" / str(spec) / "spec.yaml"
        if not spec_path.exists():
            add_missing_file(issues, root, "feedforward", spec_path)
        else:
            check_file_substance(root, issues, "feedforward", spec_path, 80, "spec")

    active_team = config.get("teams", {}).get("active")
    if active_team:
        team_path = overharness / "teams" / f"{active_team}.yaml"
        if not team_path.exists():
            add_missing_file(issues, root, "feedforward", team_path)
    else:
        issues.append(Issue("warning", "feedforward", "missing_active_team", "No active team declared in overharness.yaml", "overharness.yaml"))

    phase_key = f"{project_type.replace('-', '')}_phases" if project_type else ""
    phases_config = config.get(phase_key, {}) if phase_key else {}
    state_phases = state.get("phases", {})
    if phases_config and isinstance(state_phases, dict):
        for phase in phases_config:
            if phase not in state_phases:
                issues.append(Issue("warning", "feedforward", "phase_missing_in_state", f"Configured phase '{phase}' is missing in state.json", "state.json"))

    if isinstance(state_phases, dict):
        for phase, pdata in state_phases.items():
            for step in pdata.get("steps", []) if isinstance(pdata, dict) else []:
                if not isinstance(step, dict):
                    continue
                artifact = step.get("artifact")
                status = step.get("status")
                step_id = step.get("id", "unknown-step")
                if status == "completed" and artifact is None:
                    issues.append(Issue("warning", "feedforward", "completed_step_without_artifact", f"Completed step '{phase}/{step_id}' has no artifact recorded", "state.json"))
                if artifact and status in {"completed", "in_progress"}:
                    artifact_path = overharness / str(artifact)
                    if not artifact_path.exists():
                        add_missing_file(issues, root, "feedforward", artifact_path)
                    else:
                        min_words = int(feedforward.get("artifact_quality", {}).get("state_artifact_min_words", 80))
                        check_file_substance(root, issues, "feedforward", artifact_path, min_words, "artifact")

    workflow_requirements = feedforward.get("workflow_requirements", {}).get("implementation_workflows", [])
    if not workflow_requirements:
        workflow_requirements = [
            {"path": ".overharness/core/workflows/4-implementation/workflow.yaml", "required_steps": ["create-harness-contract", "record-harness-sensors"]},
            {"path": ".overharness/core/workflows/bf-3-implementation/workflow.yaml", "required_steps": ["create-harness-contract", "record-harness-sensors"]},
            {"path": ".overharness/core/workflows/nf-4-implementation/workflow.yaml", "required_steps": ["create-harness-contract", "run-harness-sensors"]},
        ]
    for workflow_item in workflow_requirements:
        if not isinstance(workflow_item, dict):
            continue
        workflow_path = root / str(workflow_item.get("path", ""))
        data = load_yaml(workflow_path, issues, "feedforward", "invalid_workflow") if workflow_path.exists() else {}
        steps = collect_workflow_steps(data)
        for required_step in workflow_item.get("required_steps", []):
            if required_step not in steps:
                issues.append(Issue("error", "feedforward", "workflow_missing_required_step", f"{rel(root, workflow_path)} is missing required step '{required_step}'", rel(root, workflow_path)))

    for contract in (overharness / "harness" / "contracts" / "active").glob("*.md"):
        check_file_substance(root, issues, "feedforward", contract, 80, "contract")

    if feedforward.get("artifact_quality", {}).get("implementation_report_requires_harness", True):
        implementation_reports = list((overharness / "artifacts" / "implementation").glob("*.md"))
        for report in implementation_reports:
            text = read_text(report)
            if "## Harness Contract" not in text:
                issues.append(Issue("warning", "feedforward", "implementation_report_missing_harness", f"{rel(root, report)} has no Harness Contract section", rel(root, report)))


def package_scripts(package_json: Path) -> dict[str, str]:
    try:
        data = json.loads(read_text(package_json))
        scripts = data.get("scripts", {})
        return scripts if isinstance(scripts, dict) else {}
    except Exception:
        return {}


def check_feedback(root: Path, issues: list[Issue]) -> None:
    overharness = root / ".overharness"
    sensors_path = overharness / "harness" / "sensors.yaml"
    if not sensors_path.exists():
        add_missing_file(issues, root, "feedback", sensors_path)
        return

    sensors = load_yaml(sensors_path, issues, "feedback", "invalid_sensors")
    groups = sensors.get("sensor_groups", {})
    if not isinstance(groups, dict) or not groups:
        issues.append(Issue("error", "feedback", "missing_sensor_groups", "sensors.yaml has no sensor_groups", rel(root, sensors_path)))
        return

    implementation = groups.get("implementation", {})
    required_impl = implementation.get("required", []) if isinstance(implementation, dict) else []
    recommended_impl = implementation.get("recommended", []) if isinstance(implementation, dict) else []
    if not required_impl:
        issues.append(Issue("error", "feedback", "no_required_implementation_sensors", "Implementation has no required sensors; completion is not mechanically gated", rel(root, sensors_path)))

    required_ids = {str(sensor.get("id")) for sensor in required_impl if isinstance(sensor, dict)}
    if not ({"overharness-validate", "overharness-validate"} & required_ids):
        issues.append(Issue("warning", "feedback", "missing_overharness_validate_sensor", "overharness-validate is not required for implementation", rel(root, sensors_path)))

    for sensor in required_impl + recommended_impl:
        if not isinstance(sensor, dict):
            continue
        if not sensor.get("id") or not sensor.get("command") or not sensor.get("enabled_when"):
            issues.append(Issue("warning", "feedback", "incomplete_sensor_definition", f"Sensor definition is missing id, command, or enabled_when: {sensor}", rel(root, sensors_path)))

    project_markers = {
        "package.json": list(root.glob("**/package.json")),
        "pyproject.toml": list(root.glob("**/pyproject.toml")),
        "pytest.ini": list(root.glob("**/pytest.ini")),
    }
    project_markers["package.json"] = [p for p in project_markers["package.json"] if "node_modules" not in p.parts and ".git" not in p.parts]

    discovered_checks: list[str] = []
    sensor_commands = []
    for group in groups.values():
        if not isinstance(group, dict):
            continue
        for key in ("required", "recommended"):
            for sensor in group.get(key, []) or []:
                if isinstance(sensor, dict) and sensor.get("command"):
                    sensor_commands.append(str(sensor["command"]))

    for package in project_markers["package.json"]:
        scripts = package_scripts(package)
        for script_name in ("lint", "test", "typecheck"):
            if script_name in scripts:
                cmd = f"npm run {script_name}"
                discovered_checks.append(cmd)
                if not any(cmd in sensor_cmd for sensor_cmd in sensor_commands):
                    issues.append(Issue("warning", "feedback", "discovered_check_not_configured", f"Discovered {cmd} in {rel(root, package)} but no matching sensor is configured", rel(root, package)))

    if project_markers["pyproject.toml"] or project_markers["pytest.ini"]:
        discovered_checks.append("pytest")
        if not any("pytest" in sensor_cmd for sensor_cmd in sensor_commands):
            issues.append(Issue("warning", "feedback", "discovered_check_not_configured", "Discovered Python project markers but no pytest sensor is configured"))

    if not discovered_checks:
        issues.append(Issue("info", "feedback", "no_code_test_runner_discovered", "No package.json/pyproject/pytest test runner discovered; feedback is limited to OverHarness structural sensors"))

    evaluations = [p for p in (overharness / "harness" / "evaluations").glob("*.md") if p.name != ".gitkeep"]
    active_contracts = [p for p in (overharness / "harness" / "contracts" / "active").glob("*.md")]
    completed_contracts = [p for p in (overharness / "harness" / "contracts" / "completed").glob("*.md")]
    if active_contracts and not evaluations:
        issues.append(Issue("warning", "feedback", "active_contract_without_evaluation", "Active harness contracts exist but no evaluation artifact has been recorded", rel(root, overharness / "harness" / "evaluations")))
    if completed_contracts and not evaluations:
        issues.append(Issue("warning", "feedback", "completed_contract_without_evaluation", "Completed harness contracts exist but no evaluation artifact has been recorded", rel(root, overharness / "harness" / "evaluations")))


def print_text(issues: list[Issue]) -> None:
    counts = {level: sum(1 for issue in issues if issue.severity == level) for level in ("error", "warning", "info")}
    baseline_count = sum(1 for issue in issues if issue.baseline)
    print("OverHarness Doctor")
    print(f"Errors: {counts['error']}  Warnings: {counts['warning']}  Info: {counts['info']}")
    if baseline_count:
        print(f"Baseline accepted: {baseline_count}")
    if not issues:
        print("OK: feedforward and feedback checks passed.")
        return
    for issue in issues:
        location = f" ({issue.file})" if issue.file else ""
        label = "BASELINE" if issue.baseline else issue.severity.upper()
        print(f"[{label}] {issue.plane}/{issue.code}: {issue.message}{location}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Check OverHarness feedforward and feedback readiness.")
    parser.add_argument("--format", choices=["text", "json"], default="text")
    parser.add_argument("--plane", choices=["all", "feedforward", "feedback"], default="all")
    parser.add_argument("--root", default=".", help="Project root")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    issues: list[Issue] = []
    if not (root / ".overharness").exists():
        issues.append(Issue("error", "feedforward", "missing_overharness_dir", "No .overharness directory found", str(root)))
    else:
        if args.plane in ("all", "feedforward"):
            check_feedforward(root, issues)
        if args.plane in ("all", "feedback"):
            check_feedback(root, issues)
        apply_baselines(root, issues)

    if args.format == "json":
        print(json.dumps({"ok": not any(i.severity == "error" for i in issues), "issues": [asdict(i) for i in issues]}, indent=2))
    else:
        print_text(issues)
    return 1 if any(i.severity == "error" for i in issues) else 0


if __name__ == "__main__":
    sys.exit(main())
