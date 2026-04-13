# Harness Contract: HC-20260413-execution-flow-cli

| Field | Value |
| --- | --- |
| Project | overharness-dev |
| Contract | HC-20260413-execution-flow-cli |
| Date | 2026-04-13 |
| Builder | howard |
| Evaluator | amy |
| Risk | medium |
| Source Spec | User request: make OverHarness easier to execute, install with npx, add slash commands, and show next steps |
| Source Design | `.overharness/harness/HARNESS.md` |
| Source Planning/Analysis | `.overharness/artifacts/analysis/current-harness-readiness-2026-04-13.md` |
| Status | active |

## Work Unit

Add a first executable CLI and slash-command layer so users can install and run
OverHarness without getting lost in greenfield, brownfield, or feature work.

## Scope

### In Scope

- Add an npm package manifest with a `bin` entry for `overharness`.
- Add a Node CLI with `init`, `status`, `next`, `doctor`, `validate`, and
  `contract` commands.
- Make `init` create a clean `.overharness` scaffold for a target project instead
  of copying old development artifacts.
- Add user-facing track aliases: `new-product`, `existing-system`, and
  `feature-work`.
- Add slash command prompt files for common OverHarness actions.
- Add a concise flow guide documenting the command flow and names.
- Register CLI and slash-command files in validation.

### Out of Scope

- Publishing the npm package.
- Renaming internal workflow directories in this cycle.
- Rewriting all existing historical artifacts from `greenfield`/`brownfield`.
- Mutating `.overharness/state.json` for this development project.
- Building an interactive TUI.

## Assumptions

- Internal IDs can stay stable while the CLI presents better names.
- A dependency-free Node CLI is preferable for the first npx path.
- Slash commands are implemented as `.claude/commands/*.md` prompt files.
- The initial CLI only needs deterministic process intelligence from
  `overharness.yaml`, `state.json`, active contracts, and harness doctor output.

## Expected Files or Areas

- `package.json` - npm metadata and bin entry.
- `bin/overharness.mjs` - CLI entrypoint.
- `.claude/commands/overharness-status.md` - slash command.
- `.claude/commands/overharness-next.md` - slash command.
- `.claude/commands/overharness-doctor.md` - slash command.
- `.claude/commands/overharness-contract.md` - slash command.
- `.overharness/core/engine/flow-guide.md` - flow guide and naming policy.
- `.overharness/scripts/validate.sh` - required file checks.
- `.overharness/core/agents/sheldon.agent.yaml` - user-facing naming update.
- `CLAUDE.md` and `AGENTS.md` - contributor entrypoint update.

## Must-Haves

### MH-01 - CLI status is executable

**Observable truth:** `node bin/overharness.mjs status` prints current process
state and exits 0 inside this repo.

**Verification:**
- `node bin/overharness.mjs status`

**Failure mode this catches:** Users still need to manually inspect
`.overharness/state.json`.

---

### MH-02 - CLI next recommends what to do

**Observable truth:** `node bin/overharness.mjs next` explains the next practical
step based on current state and active contracts.

**Verification:**
- `node bin/overharness.mjs next`

**Failure mode this catches:** The user still gets lost after status output.

---

### MH-03 - npx entrypoint exists

**Observable truth:** `package.json` exposes `overharness` under `bin` and the CLI
has an executable shebang.

**Verification:**
- Static review of `package.json` and `bin/overharness.mjs`.

**Failure mode this catches:** The package cannot be invoked through npx.

---

### MH-04 - Slash commands exist

**Observable truth:** `.claude/commands/` contains command files for status,
next, doctor, and contract flows.

**Verification:**
- `find .claude/commands -type f | sort`

**Failure mode this catches:** Users have no simple slash-command entrypoints.

---

### MH-05 - Better track names are documented without breaking internals

**Observable truth:** The flow guide documents `new-product`,
`existing-system`, and `feature-work` as user-facing names mapped to internal
IDs.

**Verification:**
- Static review of `.overharness/core/engine/flow-guide.md`.

**Failure mode this catches:** We rename concepts in prose without an explicit
compatibility policy.

---

### MH-06 - Validation protects the new entrypoints

**Observable truth:** `bash .overharness/scripts/validate.sh` checks the CLI,
package manifest, flow guide, and slash commands.

**Verification:**
- `bash .overharness/scripts/validate.sh`

**Failure mode this catches:** The easier execution path can regress silently.

---

## Sensors

### Required

- **overharness-validate**: `bash .overharness/scripts/validate.sh`
- **harness-doctor**: `bash .overharness/scripts/harness-doctor.sh`
- **harness-selftest**: `bash .overharness/scripts/harness-selftest.sh`
- **overharness-cli-status**: `node bin/overharness.mjs status`
- **overharness-cli-next**: `node bin/overharness.mjs next`
- **harness-evaluate-contract**: `bash .overharness/scripts/harness-evaluate.sh --contract .overharness/harness/contracts/completed/HC-20260413-execution-flow-cli.md`

### Recommended

- **cli-init-help**: `node bin/overharness.mjs init --help`
- **npm-test**: `npm test` when package scripts are available.

### Feedback Gaps

- The CLI does not yet include a fully interactive wizard.
- The package has not been published to npm yet.

## Risk and Routing

**Risk level:** medium

**Why:** This adds the user-facing entrypoint and installation scaffold, but it
does not rename internal workflows or mutate project state.

**Amy review:** Required after implementation.

**Human approval:** Not required.

## Blockers and Open Questions

- No blocker for MVP.
- Follow-up decision: npm package name and publishing scope.

## Exit Criteria

- [x] All required must-haves are satisfied
- [x] All required sensors passed or have documented baseline exceptions approved by the user
- [x] Deviations are documented with reason and impact
- [x] Amy reviewed the result if risk is `medium`, `high`, or `critical`
- [x] Human approval captured if risk is `critical` - not applicable

## Next Handoff

Evaluation artifact:
`.overharness/harness/evaluations/EV-20260413-execution-flow-cli.md`

Amy review artifact:
`.overharness/artifacts/review/execution-flow-cli-review.md`

Approved for completion and moved to
`.overharness/harness/contracts/completed/`.
