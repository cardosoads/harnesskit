# Harness Contract: HC-20260414-codex-skill-integration

| Field | Value |
| --- | --- |
| Project | Harnesskit |
| Contract | HC-20260414-codex-skill-integration |
| Date | 2026-04-14 |
| Builder | howard |
| Evaluator | amy |
| Risk | medium |
| Source Spec | User request: Codex commands should work internally like a skill |
| Source Design | `.harnesskit/harness/HARNESS.md` |
| Source Planning/Analysis | `.harnesskit/artifacts/analysis/current-harness-readiness-2026-04-13.md` |
| Status | completed |

## Work Unit

Make Harnesskit usable inside Codex as an internal skill-driven workflow instead of forcing the user to leave Codex and run `npx` commands for guidance.

## Scope

### In Scope

- Add a packaged Codex skill for Harnesskit.
- Make `harnesskit init` install the project-local Codex skill.
- Make `harnesskit codex` verify or install the project-local skill and document optional user-scoped installation.
- Update package file checks and user-facing docs.
- Keep the CLI as the sensor runner for validation, doctor, and status.

### Out of Scope

- Changing Codex's native skill discovery runtime.
- Removing Claude Code slash commands.
- Replacing Harnesskit sensors with agent-only behavior.

## Expected Files or Areas

- `.codex/skills/harnesskit/SKILL.md` - Codex skill packaged with the npm module.
- `bin/harnesskit.mjs` - CLI installs and reports the Codex skill.
- `package.json` - package includes skill files and bumps patch version.
- `scripts/check-package-files.mjs` - package dry-run requires the Codex skill.
- `README.md` and `AGENTS.md` - explain the Codex skill workflow.

## Must-Haves

### MH-01 - Codex skill is packaged and discoverable

**Observable truth:** The npm package includes `.codex/skills/harnesskit/SKILL.md` with valid skill frontmatter.

**Verification:**
- `npm run pack:check`
- Static review of `.codex/skills/harnesskit/SKILL.md`

**Failure mode this catches:** Codex still has only shell guidance and no skill artifact to load.

### MH-02 - Init creates project-local skill

**Observable truth:** Running `harnesskit init` in a clean project creates `.codex/skills/harnesskit/SKILL.md`.

**Verification:**
- Temporary-project init smoke test.

**Failure mode this catches:** New projects remain dependent on manual skill setup.

### MH-03 - Codex command repairs missing skill

**Observable truth:** Running `harnesskit codex` in an initialized project creates the project-local skill if it is missing and prints how to trigger it in Codex.

**Verification:**
- Temporary-project smoke test after deleting `.codex/skills/harnesskit`.

**Failure mode this catches:** Existing Harnesskit projects cannot be upgraded into the skill workflow.

### MH-04 - Sensors remain executable from CLI

**Observable truth:** Harnesskit validation and selftest still pass after the Codex skill change.

**Verification:**
- `npm test`
- `node --check bin/harnesskit.mjs`

**Failure mode this catches:** Skill integration breaks the CLI sensors that still provide feedback.

## Sensors

### Required

- **node-check**: `node --check bin/harnesskit.mjs` - validates CLI syntax.
- **harnesskit-test**: `npm test` - validates harness schemas and selftests.
- **pack-check**: `npm run pack:check` - confirms npm tarball contents.
- **codex-skill-smoke**: clean temp project init and `codex` repair check - confirms runtime behavior.

### Recommended

- **doctor**: `node bin/harnesskit.mjs doctor` - confirms harness feedback stays clean.

### Feedback Gaps

- Codex native skill discovery may require a new session or user-scoped installation; the CLI can install artifacts but cannot force the already-running Codex app to refresh its skill catalog.

## Risk and Routing

**Risk level:** medium

**Why:** This changes package contents and the user-facing Codex workflow, but keeps CLI sensors and existing slash commands intact.

**Amy review:** Required before completing the contract.

**Human approval:** Not required.

## Exit Criteria

- [x] Packaged skill exists and is included in package dry-run.
- [x] `init` creates the skill in a clean project.
- [x] `codex` repairs missing skill in an existing project.
- [x] Required sensors pass.
- [x] Amy review records approval or blocking findings.

## Evidence

- `node --check bin/harnesskit.mjs` passed.
- `npm test` passed.
- `npm run pack:check` passed.
- `npm publish --dry-run --access public` passed.
- Temporary project smoke test verified `init` creates `.codex/skills/harnesskit/SKILL.md`.
- Temporary project repair test verified `codex` recreates the missing project-local skill.
- Temporary `CODEX_HOME` smoke test verified `codex --global` installs `skills/harnesskit/SKILL.md`.
- `node bin/harnesskit.mjs doctor` passed with 0 errors and 0 warnings.
- `git diff --check` passed.

## Amy Review

Approved in `.harnesskit/artifacts/review/codex-skill-integration-review.md`.
