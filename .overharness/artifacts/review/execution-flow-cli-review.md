# Review Report: Execution Flow CLI

| Field | Value |
| --- | --- |
| Reviewer | amy |
| Date | 2026-04-13 |
| Artifact Reviewed | `.overharness/harness/evaluations/EV-20260413-execution-flow-cli.md` |
| Phase | review |
| Version | 1.0 |

---

## Executive Summary

Amy reviewed the execution flow CLI against contract
`HC-20260413-execution-flow-cli`. The implementation satisfies the contract: it
adds an npm `bin` entry, a dependency-free CLI, clean scaffold initialization,
process-aware `status` and `next` commands, slash command prompts, user-facing
track names, and validation coverage for the new entrypoints.

The review finds no blocking issues. Internal IDs remain stable, which avoids a
large compatibility rename while making the user-facing flow clearer.

---

## Compliance Summary

██████████ 100% (9/9 passed)

Critical: 0 | Warning: 0 | Passed: 9

---

## Review Criteria Applied

- **Usability:** Checks whether a user can ask where they are and what to do
  next without reading raw state files.
- **Installability:** Checks whether `package.json` exposes a `bin` entry and
  package contents exclude development artifacts.
- **Compatibility:** Checks whether better names are aliases over existing
  internal IDs, not breaking workflow keys.
- **Harness evidence:** Checks contract ID, risk level, required sensor status,
  and evaluator routing.

---

## Issues Found

| ID | Severity | Description | Location | Recommendation |
| --- | --- | --- | --- | --- |
| None | n/a | No blocking issues found. | n/a | No action required for this contract. |

---

## Harness Review

| Field | Value |
| --- | --- |
| Contract ID | HC-20260413-execution-flow-cli |
| Contract Path | `.overharness/harness/contracts/completed/HC-20260413-execution-flow-cli.md` |
| Risk Level | medium |
| Evaluator Required | yes |
| Required Sensors Passed | yes |

**Contract coverage:** All six must-haves were represented in the evaluation
artifact and independently checked during review.

**Sensor evidence:** `harness-evaluate` approved the contract with 5 required
sensors; `validate.sh` passed with 87 checked items; `harness-doctor` passed
with only accepted baseline debt; `harness-selftest` passed; `node
bin/overharness.mjs status` and `node bin/overharness.mjs next` passed; `npm test`
passed as a recommended sensor; `npm pack --dry-run --json` did not include
development contracts, evaluations, artifacts, or `__pycache__`.

**Harness findings:**

- **Info:** The CLI is intentionally deterministic and non-interactive for this
  increment. A richer interactive wizard remains future work.
- **Info:** The npm package name and publishing scope still need a human
  publishing decision before release.

---

## Must-Have Verification

| Must-Have | Result | Evidence |
| --- | --- | --- |
| MH-01 - CLI status is executable | PASS | `node bin/overharness.mjs status` exits 0 and prints project, track, phase map, active contracts, and next step. |
| MH-02 - CLI next recommends what to do | PASS | `node bin/overharness.mjs next` recommends the next process action from current state and active contracts. |
| MH-03 - npx entrypoint exists | PASS | `package.json` defines `bin.overharness` as `./bin/overharness.mjs`, and the CLI has a Node shebang. |
| MH-04 - Slash commands exist | PASS | `.claude/commands/` contains status, next, doctor, and contract command prompts. |
| MH-05 - Better track names are documented without breaking internals | PASS | `.overharness/core/engine/flow-guide.md` maps `new-product`, `existing-system`, and `feature-work` to the stable internal IDs. |
| MH-06 - Validation protects the new entrypoints | PASS | `validate.sh` requires package, CLI, flow guide, and slash command files. |

---

## Additional Verification

| Check | Result | Evidence |
| --- | --- | --- |
| Clean scaffold init | PASS | Temporary `existing-system` and `new-product` projects initialized with clean state and without dev artifacts. |
| Package dry run | PASS | `npm pack --dry-run --json` did not include development contracts, evaluations, artifacts, or `__pycache__`. |
| npm test | PASS | `npm test` runs validation and Harness self-tests successfully. |

---

## Verdict

**APPROVED**

The implementation meets the contract and materially improves the execution
flow: users can now install, initialize, inspect status, ask for the next step,
run doctor checks, and use slash commands without manually navigating the
OverHarness internals.

---

## Required Actions

_No actions required for this contract._

---

## Next Steps

- [x] Review report delivered as an artifact.
- [x] Required actions communicated: none.
- [x] Contract can move from `active/` to `completed/`.
- [ ] Future contract: interactive `overharness init` wizard and npm publishing
  preparation.
