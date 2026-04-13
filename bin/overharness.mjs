#!/usr/bin/env node
import { spawnSync } from "node:child_process";
import { stdin as input, stdout as output } from "node:process";
import { createInterface } from "node:readline/promises";
import {
  cpSync,
  existsSync,
  mkdirSync,
  readdirSync,
  readFileSync,
  statSync,
  writeFileSync,
} from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const packageRoot = path.resolve(path.dirname(__filename), "..");

const TRACKS = {
  greenfield: {
    id: "greenfield",
    alias: "new-product",
    label: "New product",
    team: "team-fullstack",
    phases: ["discovery", "specification", "discuss", "architecture", "design", "implementation", "review"],
  },
  brownfield: {
    id: "brownfield",
    alias: "existing-system",
    label: "Existing system",
    team: "team-brownfield",
    phases: ["analysis", "planning", "design", "implementation", "review"],
  },
  "new-features": {
    id: "new-features",
    alias: "feature-work",
    label: "Feature work",
    team: "team-newfeatures",
    phases: ["discovery", "specification", "architecture", "design", "implementation", "review"],
  },
};

const TYPE_ALIASES = {
  new: "greenfield",
  "new-product": "greenfield",
  product: "greenfield",
  greenfield: "greenfield",
  existing: "brownfield",
  "existing-system": "brownfield",
  improve: "brownfield",
  brownfield: "brownfield",
  feature: "new-features",
  "feature-work": "new-features",
  extend: "new-features",
  "new-features": "new-features",
  newfeatures: "new-features",
};

const PHASE_STEPS = {
  greenfield: {
    discovery: [
      ["project-brief", "penny", "artifacts/discovery/project-brief.md"],
      ["requirements", "penny", "artifacts/discovery/requirements.md"],
    ],
    specification: [["user-stories", "penny", "artifacts/specification/user-stories.md"]],
    discuss: [["discuss-implementation", "sheldon", "artifacts/discuss/implementation-discussion.md"]],
    architecture: [["system-architecture", "leonard", "artifacts/architecture/system-architecture.md"]],
    design: [["ui-design", "design-specialist", "artifacts/design/ui-design.md"]],
    implementation: [["project-setup", "howard", "artifacts/implementation/setup-report.md"]],
    review: [["review-artifact", "amy", "artifacts/review/review-report.md"]],
  },
  brownfield: {
    analysis: [
      ["codebase-analysis", "raj", "artifacts/analysis/codebase-analysis.md"],
      ["tech-debt-audit", "raj", "artifacts/analysis/tech-debt-report.md"],
    ],
    planning: [["improvement-plan", "raj", "artifacts/planning/improvement-plan.md"]],
    design: [["design-audit", "design-specialist", "artifacts/design/design-audit.md"]],
    implementation: [["brownfield-setup", "howard", "artifacts/implementation/bf-setup-report.md"]],
    review: [["review-artifact", "amy", "artifacts/review/review-report.md"]],
  },
  "new-features": {
    discovery: [
      ["impact-analysis", "raj", "artifacts/discovery/impact-analysis.md"],
      ["feature-requirements", "penny", "artifacts/discovery/feature-requirements.md"],
    ],
    specification: [["feature-specification", "penny", "artifacts/specification/feature-stories.md"]],
    architecture: [["feature-design", "leonard", "artifacts/architecture/feature-design.md"]],
    design: [["feature-ui-design", "design-specialist", "artifacts/design/feature-ui-design.md"]],
    implementation: [["feature-implementation", "howard", "artifacts/implementation/feature-implementation.md"]],
    review: [["review-artifact", "amy", "artifacts/review/review-report.md"]],
  },
};

function help(exitCode = 0) {
  console.log(`OverHarness CLI

Usage:
  overharness init [--type <new-product|existing-system|feature-work>] [--name <name>] [--yes]
  overharness status
  overharness next
  overharness doctor
  overharness validate
  overharness contract "<work unit>"

User-facing tracks:
  new-product      Internal id: greenfield
  existing-system  Internal id: brownfield
  feature-work     Internal id: new-features
`);
  process.exit(exitCode);
}

function argValue(args, name) {
  const index = args.indexOf(name);
  if (index === -1 || index + 1 >= args.length) return "";
  return args[index + 1];
}

function hasFlag(args, name) {
  return args.includes(name);
}

function isInteractive() {
  return Boolean(input.isTTY && output.isTTY);
}

function formatTrackOptions() {
  return Object.values(TRACKS)
    .map((track, index) => `${index + 1}. ${track.alias} - ${track.label} (internal: ${track.id})`)
    .join("\n");
}

async function promptForInit(args, targetRoot) {
  let name = argValue(args, "--name");
  let track = normalizeType(argValue(args, "--type") || "");
  const assumeDefaults = hasFlag(args, "--yes") || hasFlag(args, "-y");

  if (!TRACKS[track]) track = "";
  if (assumeDefaults) {
    return {
      name: name || path.basename(targetRoot),
      track: track || "new-features",
    };
  }
  if (name && track) return { name, track };
  if (!isInteractive()) {
    if (!name || !track) {
      console.error("Missing init inputs in a non-interactive environment.");
      console.error("Use: overharness init --type feature-work --name <project-name>");
      console.error("Or:  overharness init --yes --name <project-name>");
      process.exit(1);
    }
    return { name, track };
  }

  const rl = createInterface({ input, output });
  try {
    console.log("OverHarness init wizard");
    if (!name) {
      const answer = await rl.question(`Project name (${path.basename(targetRoot)}): `);
      name = answer.trim() || path.basename(targetRoot);
    }
    while (!track) {
      console.log("\nChoose the project track:");
      console.log(formatTrackOptions());
      const answer = await rl.question("Track (feature-work): ");
      const selected = answer.trim() || "feature-work";
      const byNumber = Number(selected);
      if (Number.isInteger(byNumber) && byNumber >= 1 && byNumber <= Object.keys(TRACKS).length) {
        track = Object.values(TRACKS)[byNumber - 1].id;
      } else {
        track = normalizeType(selected);
      }
      if (!TRACKS[track]) {
        console.log(`Unknown track: ${selected}`);
        track = "";
      }
    }
    return { name, track };
  } finally {
    rl.close();
  }
}

function readText(file) {
  return readFileSync(file, "utf8");
}

function writeText(file, text) {
  mkdirSync(path.dirname(file), { recursive: true });
  writeFileSync(file, text, "utf8");
}

function findProjectRoot(start = process.cwd()) {
  let current = path.resolve(start);
  while (true) {
    if (existsSync(path.join(current, ".overspec"))) return current;
    const parent = path.dirname(current);
    if (parent === current) return "";
    current = parent;
  }
}

function loadState(root) {
  const statePath = path.join(root, ".overspec", "state.json");
  if (!existsSync(statePath)) return null;
  return JSON.parse(readText(statePath));
}

function normalizeType(value) {
  const key = String(value || "").trim().toLowerCase();
  if (!key) return "";
  return TYPE_ALIASES[key] || key;
}

function readProjectType(root, state) {
  if (state?.project_type) return normalizeType(state.project_type);
  const config = path.join(root, ".overspec", "overspec.yaml");
  if (!existsSync(config)) return "new-features";
  const text = readText(config);
  const match = text.match(/project_type:\s*["']?([^"'\n]+)["']?/);
  return normalizeType(match?.[1]?.trim() || "new-features");
}

function projectName(root, state) {
  if (state?.project) return state.project;
  const config = path.join(root, ".overspec", "overspec.yaml");
  if (!existsSync(config)) return path.basename(root);
  const match = readText(config).match(/name:\s*["']?([^"'\n]+)["']?/);
  return match?.[1]?.trim() || path.basename(root);
}

function orderedPhases(track, state) {
  const known = TRACKS[track]?.phases || Object.keys(state?.phases || {});
  const actual = Object.keys(state?.phases || {});
  const ordered = known.filter((phase) => actual.includes(phase));
  return [...ordered, ...actual.filter((phase) => !ordered.includes(phase))];
}

function progressFor(phases) {
  const total = phases.length;
  const completed = phases.filter(([, data]) => data?.status === "completed").length;
  const percent = total ? Math.round((completed / total) * 100) : 0;
  const filled = Math.round(percent / 10);
  return { total, completed, percent, bar: "#".repeat(filled) + "-".repeat(10 - filled) };
}

function phaseLine(name, data, current) {
  const marker = data?.status === "completed" ? "[x]" : name === current ? "[>]" : "[ ]";
  return `${marker} ${name} - ${data?.status || "unknown"}`;
}

function nextStep(state, ordered) {
  for (const phase of ordered) {
    const data = state.phases?.[phase];
    if (!data || data.status === "completed") continue;
    const steps = Array.isArray(data.steps) ? data.steps : [];
    const active = steps.find((step) => ["in_progress", "pending"].includes(step.status));
    if (active) return { phase, step: active };
    return { phase, step: null };
  }
  return null;
}

function activeContracts(root) {
  const activeDir = path.join(root, ".overspec", "harness", "contracts", "active");
  if (!existsSync(activeDir)) return [];
  return readdirSync(activeDir)
    .filter((file) => file.endsWith(".md"))
    .map((file) => path.join(activeDir, file))
    .filter((file) => statSync(file).isFile());
}

function printStatus(root) {
  const state = loadState(root);
  if (!state) {
    console.log("OverHarness is not initialized here.");
    console.log("Run: npx overharness init --type feature-work --name <project-name>");
    return;
  }
  const track = readProjectType(root, state);
  const trackInfo = TRACKS[track] || { label: track, alias: track };
  const ordered = orderedPhases(track, state);
  const entries = ordered.map((phase) => [phase, state.phases?.[phase] || {}]);
  const progress = progressFor(entries);
  const current = state.current_phase;
  const contracts = activeContracts(root);

  console.log(`Project: ${projectName(root, state)}`);
  console.log(`Track: ${trackInfo.label} (${trackInfo.alias}; internal: ${track})`);
  console.log(`Current phase: ${current}`);
  console.log(`Progress: ${progress.bar} ${progress.percent}% (${progress.completed}/${progress.total} phases)`);
  console.log(`Active contracts: ${contracts.length}`);
  console.log("");
  console.log("Phase map:");
  for (const [phase, data] of entries) console.log(`  ${phaseLine(phase, data, current)}`);
  const next = nextStep(state, ordered);
  console.log("");
  if (next?.step) {
    console.log(`Next step: ${next.phase}/${next.step.id} by ${next.step.agent || "unknown"}`);
    if (next.step.artifact) console.log(`Expected artifact: ${next.step.artifact}`);
  } else if (current === "completed" || !next) {
    console.log("Next step: no pending state step. Start a new work unit with a Harness contract.");
  } else {
    console.log(`Next step: review phase '${next.phase}' because no pending step was found.`);
  }
}

function printNext(root) {
  printStatus(root);
  const state = loadState(root);
  if (!state) return;
  const track = readProjectType(root, state);
  const ordered = orderedPhases(track, state);
  const next = nextStep(state, ordered);
  const contracts = activeContracts(root);

  console.log("");
  console.log("Recommended action:");
  if (contracts.length) {
    console.log(`  Continue the active Harness contract: ${path.relative(root, contracts[0])}`);
    console.log("  Run: overharness doctor");
    console.log("  Then route implementation through Leslie -> Howard -> sensors -> Amy.");
    return;
  }
  if (next?.step) {
    console.log(`  Ask Sheldon to route ${next.phase}/${next.step.id} to ${next.step.agent || "the responsible agent"}.`);
    console.log("  Slash command: /overharness-next");
    return;
  }
  console.log("  Create the next Harness contract for the feature or improvement you want.");
  console.log('  Run: overharness contract "describe the work unit"');
  console.log("  Slash command: /overharness-contract");
}

function packageAjvBin() {
  const executable = process.platform === "win32" ? "ajv.cmd" : "ajv";
  return path.join(packageRoot, "node_modules", ".bin", executable);
}

function runProjectCommand(root, command, extraEnv = {}) {
  const result = spawnSync(command[0], command.slice(1), {
    cwd: root,
    stdio: "inherit",
    shell: false,
    env: { ...process.env, ...extraEnv },
  });
  process.exit(result.status ?? 1);
}

function copyDirectory(source, target) {
  if (!existsSync(source)) return;
  cpSync(source, target, {
    recursive: true,
    filter: (file) => {
      const rel = path.relative(source, file);
      if (!rel) return true;
      return !rel.includes(`${path.sep}__pycache__`) && !rel.endsWith(".pyc");
    },
  });
}

function ensureCleanDirs(root) {
  const dirs = [
    "artifacts/analysis",
    "artifacts/architecture",
    "artifacts/design",
    "artifacts/discovery",
    "artifacts/discuss",
    "artifacts/discussions",
    "artifacts/implementation",
    "artifacts/planning",
    "artifacts/review",
    "artifacts/specification",
    "handoffs",
    "harness/contracts/active",
    "harness/contracts/completed",
    "harness/evaluations",
    "harness/progress",
    "harness/drift",
  ];
  for (const dir of dirs) writeText(path.join(root, ".overspec", dir, ".gitkeep"), "");
}

function freshState(name, track) {
  const phases = {};
  for (const phase of TRACKS[track].phases) {
    const required = !["design", "discuss"].includes(phase);
    phases[phase] = {
      status: phase === TRACKS[track].phases[0] ? "unlocked" : "locked",
      required,
      steps: (PHASE_STEPS[track][phase] || []).map(([id, agent, artifact]) => ({
        id,
        status: "pending",
        artifact,
        agent,
      })),
    };
  }
  return {
    project: name,
    spec: "software",
    project_type: track,
    created_at: new Date().toISOString(),
    cycle: 1,
    current_phase: TRACKS[track].phases[0],
    phases,
    previous_cycles: [],
    handoffs: [],
  };
}

function writeConfig(targetRoot, name, track) {
  const templatePath = path.join(packageRoot, ".overspec", "overspec.yaml");
  let text = existsSync(templatePath) ? readText(templatePath) : "";
  if (!text) throw new Error("Missing packaged .overspec/overspec.yaml template.");
  text = text.replace(/name:\s*"[^"]*"/, `name: "${name}"`);
  text = text.replace(/description:\s*"[^"]*"/, 'description: "OverHarness project scaffold"');
  text = text.replace(/project_type:\s*"[^"]*"/, `project_type: "${track}"`);
  text = text.replace(/active:\s*"team-[^"]*"/, `active: "${TRACKS[track].team}"`);
  writeText(path.join(targetRoot, ".overspec", "overspec.yaml"), text);
}

function writeEmptyBaselines(targetRoot) {
  writeText(
    path.join(targetRoot, ".overspec", "harness", "baselines", "current.yaml"),
    'version: 1\nupdated_at: ""\ndescription: "Accepted Harness findings for this project."\n\naccepted_issues: []\n',
  );
}

function writeSlashCommands(targetRoot) {
  const commands = {
    "overharness-status.md": "Read `.overspec/state.json`, run `node bin/overharness.mjs status` if available, and explain where the project is in the OverHarness process. Respond in the configured user language.\n",
    "overharness-next.md": "Run or emulate `node bin/overharness.mjs next`, then recommend the next OverHarness action. If work is non-trivial, route through Sheldon -> Leslie contract -> Howard -> sensors -> Amy.\n",
    "overharness-doctor.md": "Run `bash .overspec/scripts/harness-doctor.sh` and summarize feedforward/feedback findings. Do not hide baseline debt.\n",
    "overharness-contract.md": "Guide the user through Leslie's Harness contract workflow for the requested work unit. Create or revise a contract in `.overspec/harness/contracts/active/` before implementation.\n",
  };
  for (const [name, body] of Object.entries(commands)) {
    writeText(path.join(targetRoot, ".claude", "commands", name), body);
  }
}

async function initProject(args) {
  if (hasFlag(args, "--help") || hasFlag(args, "-h")) {
    console.log("Usage: overharness init [--type <new-product|existing-system|feature-work>] [--name <name>] [--yes] [--force]");
    return;
  }
  const targetRoot = process.cwd();
  if (existsSync(path.join(targetRoot, ".overspec")) && !hasFlag(args, "--force")) {
    console.error("OverHarness already exists here. Use --force only when you intend to replace the scaffold.");
    process.exit(1);
  }
  const { name, track } = await promptForInit(args, targetRoot);
  if (!TRACKS[track]) {
    console.error(`Unknown project type: ${argValue(args, "--type")}`);
    help(1);
  }
  const templateRoot = path.join(packageRoot, ".overspec");

  for (const dir of ["core", "schemas", "scripts", "specs", "teams"]) {
    copyDirectory(path.join(templateRoot, dir), path.join(targetRoot, ".overspec", dir));
  }
  copyDirectory(path.join(templateRoot, "harness", "templates"), path.join(targetRoot, ".overspec", "harness", "templates"));
  copyDirectory(path.join(templateRoot, "harness", "baselines"), path.join(targetRoot, ".overspec", "harness", "baselines"));
  for (const file of ["HARNESS.md", "feedforward.yaml", "sensors.yaml"]) {
    cpSync(path.join(templateRoot, "harness", file), path.join(targetRoot, ".overspec", "harness", file));
  }
  if (existsSync(path.join(templateRoot, "harness", "contracts", "README.md"))) {
    mkdirSync(path.join(targetRoot, ".overspec", "harness", "contracts"), { recursive: true });
    cpSync(path.join(templateRoot, "harness", "contracts", "README.md"), path.join(targetRoot, ".overspec", "harness", "contracts", "README.md"));
  }
  writeConfig(targetRoot, name, track);
  writeText(path.join(targetRoot, ".overspec", "state.json"), `${JSON.stringify(freshState(name, track), null, 2)}\n`);
  writeEmptyBaselines(targetRoot);
  ensureCleanDirs(targetRoot);
  writeSlashCommands(targetRoot);
  console.log(`OverHarness initialized for ${name}.`);
  console.log(`Track: ${TRACKS[track].label} (${TRACKS[track].alias}; internal: ${track})`);
  console.log("Next: overharness status");
}

function createContract(root, args) {
  const workUnit = args.join(" ").trim();
  if (!workUnit || hasFlag(args, "--help") || hasFlag(args, "-h")) {
    console.log('Usage: overharness contract "describe the work unit"');
    return;
  }
  const slug = workUnit.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "").slice(0, 60) || "work-unit";
  const today = new Date().toISOString().slice(0, 10).replaceAll("-", "");
  const contractId = `HC-${today}-${slug}`;
  const file = path.join(root, ".overspec", "harness", "contracts", "active", `${contractId}.md`);
  if (existsSync(file)) {
    console.log(`Contract already exists: ${path.relative(root, file)}`);
    return;
  }
  const body = `# Harness Contract: ${contractId}

| Field | Value |
| --- | --- |
| Project | ${projectName(root, loadState(root))} |
| Contract | ${contractId} |
| Date | ${new Date().toISOString().slice(0, 10)} |
| Builder | howard |
| Evaluator | amy |
| Risk | medium |
| Source Spec | CLI contract draft |
| Source Design | .overspec/harness/HARNESS.md |
| Status | active |

## Work Unit

${workUnit}

## Scope

### In Scope

- Define the exact change before implementation.
- Identify files, artifacts, and sensors required for completion.

### Out of Scope

- Unrelated refactors.
- Mutating state.json unless explicitly required by the approved contract.

## Must-Haves

### MH-01 - Contract must be completed by Leslie

**Observable truth:** Leslie replaces this draft with observable must-haves,
expected files, sensors, risk, and exit criteria before Howard implements.

**Verification:**
- Static review of this contract.

## Sensors

### Required

- **overharness-validate**: \`bash .overspec/scripts/validate.sh\`
- **harness-doctor**: \`bash .overspec/scripts/harness-doctor.sh\`
- **harness-selftest**: \`bash .overspec/scripts/harness-selftest.sh\`

## Exit Criteria

- [ ] Leslie completed the contract details.
- [ ] Required sensors are listed and runnable.
- [ ] Amy review is planned when risk is medium or higher.
`;
  writeText(file, body);
  console.log(`Draft contract created: ${path.relative(root, file)}`);
  console.log("Next: route this draft to Leslie before implementation.");
}

async function main() {
  const [command = "help", ...args] = process.argv.slice(2);
  if (["help", "--help", "-h"].includes(command)) help(0);
  if (command === "init") return await initProject(args);

  const root = findProjectRoot();
  if (!root) {
    console.error("No .overspec directory found. Run: npx overharness init --type feature-work");
    process.exit(1);
  }

  if (command === "status") return printStatus(root);
  if (command === "next") return printNext(root);
  if (command === "doctor") return runProjectCommand(root, ["bash", ".overspec/scripts/harness-doctor.sh"]);
  if (command === "validate") {
    const ajvBin = packageAjvBin();
    const env = existsSync(ajvBin) ? { OVERSPEC_AJV_BIN: ajvBin } : {};
    return runProjectCommand(root, ["bash", ".overspec/scripts/validate.sh"], env);
  }
  if (command === "contract") return createContract(root, args);
  help(1);
}

main().catch((error) => {
  console.error(error instanceof Error ? error.message : String(error));
  process.exit(1);
});
