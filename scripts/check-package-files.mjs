#!/usr/bin/env node
import { spawnSync } from "node:child_process";

const requiredFiles = [
  "bin/overharness.mjs",
  ".overharness/overharness.yaml",
  ".overharness/harness/HARNESS.md",
  ".overharness/harness/feedforward.yaml",
  ".overharness/harness/sensors.yaml",
  ".overharness/harness/contracts/README.md",
  ".overharness/harness/templates/contract-template.md",
  ".overharness/schemas/spec-schema.json",
  ".overharness/scripts/validate.sh",
  ".overharness/scripts/harness-doctor.sh",
  ".overharness/scripts/harness-evaluate.sh",
  ".overharness/scripts/harness-selftest.sh",
  ".overharness/specs/software/spec.yaml",
  ".overharness/teams/team-newfeatures.yaml",
  ".claude/commands/overharness-status.md",
  ".claude/commands/overharness-contract.md",
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
