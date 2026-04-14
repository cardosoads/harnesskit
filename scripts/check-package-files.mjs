#!/usr/bin/env node
import { spawnSync } from "node:child_process";

const requiredFiles = [
  "bin/harnesskit.mjs",
  ".codex/skills/harnesskit/SKILL.md",
  ".harnesskit/harnesskit.yaml",
  ".harnesskit/harness/HARNESS.md",
  ".harnesskit/harness/feedforward.yaml",
  ".harnesskit/harness/sensors.yaml",
  ".harnesskit/harness/contracts/README.md",
  ".harnesskit/harness/templates/contract-template.md",
  ".harnesskit/schemas/spec-schema.json",
  ".harnesskit/scripts/validate.sh",
  ".harnesskit/scripts/harness-doctor.sh",
  ".harnesskit/scripts/harness-evaluate.sh",
  ".harnesskit/scripts/harness-selftest.sh",
  ".harnesskit/specs/software/spec.yaml",
  ".harnesskit/teams/team-newfeatures.yaml",
  ".claude/commands/harnesskit-status.md",
  ".claude/commands/harnesskit-contract.md",
  "README.md",
  "package.json",
];

const result = spawnSync("npm", ["pack", "--dry-run", "--json"], {
  encoding: "utf8",
  shell: false,
});

if (result.status !== 0) {
  process.stdout.write(result.stdout || "");
  process.stderr.write(result.stderr || "");
  process.exit(result.status ?? 1);
}

let pack;
try {
  pack = JSON.parse(result.stdout);
} catch (error) {
  console.error("Could not parse npm pack output as JSON.");
  console.error(error instanceof Error ? error.message : String(error));
  process.stdout.write(result.stdout || "");
  process.stderr.write(result.stderr || "");
  process.exit(1);
}

const files = new Set((pack[0]?.files || []).map((file) => file.path));
const missing = requiredFiles.filter((file) => !files.has(file));

if (missing.length) {
  console.error("Package dry-run is missing required files:");
  for (const file of missing) console.error(`  - ${file}`);
  process.exit(1);
}

console.log(`Package dry-run passed: ${pack[0]?.filename || "tarball"} includes ${files.size} files.`);
