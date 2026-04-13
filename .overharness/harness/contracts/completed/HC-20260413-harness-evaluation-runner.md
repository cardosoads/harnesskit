# Harness Contract: HC-20260413-harness-evaluation-runner

| Field | Value |
| --- | --- |
| Project | overharness-dev |
| Contract | HC-20260413-harness-evaluation-runner |
| Date | 2026-04-13 |
| Builder | howard |
| Evaluator | amy |
| Risk | medium |
| Source Spec | `.overharness/artifacts/analysis/current-harness-readiness-2026-04-13.md` |
| Source Design | `.overharness/harness/HARNESS.md` |
| Source Planning/Analysis | `.overharness/artifacts/planning/harness-engineering-plan.md` |
| Status | completed |

## Work Unit

Implement the first executable Harness evaluation runner for OverHarness. The
runner must read an active Harness contract, execute or document applicable
sensors from `.overharness/harness/sensors.yaml`, and write a durable evaluation
artifact under `.overharness/harness/evaluations/`.

## Scope

### In Scope

- Add a Python runner script for Harness evaluations.
- Add a shell wrapper for running the evaluation from the repository root.
- Support selecting a contract explicitly, or defaulting to the newest active contract.
- Execute enabled required command sensors that are safe and available.
- Mark unavailable recommended sensors as skipped with a reason.
- Write a Markdown evaluation artifact with contract ID, verdict, sensor results, and recommendation.
- Register the runner as a required Harness file in validation.
- Document the runner in the Harness guide.

### Out of Scope

- Moving contracts from `active/` to `completed/` automatically.
- Editing `state.json`.
- Implementing automatic Howard -> Amy retry loops.
- Adding project-specific application tests where no runtime exists yet.
- Installing external tools such as `ajv-cli`, `semgrep`, Playwright, npm dependencies, or pytest.

## Assumptions

- The current repository has no application runtime markers such as `package.json`, `pyproject.toml`, or `pytest.ini`.
- The first runner can focus on OverHarness structural sensors.
- A Markdown evaluation artifact is enough for Amy to review in the next step.
- Required sensor failures block approval unless explicitly recorded as baseline exceptions.

## Expected Files or Areas

- `.overharness/scripts/harness_evaluate.py` - main evaluation runner.
- `.overharness/scripts/harness-evaluate.sh` - executable wrapper.
- `.overharness/harness/HARNESS.md` - usage documentation.
- `.overharness/harness/sensors.yaml` - optional runner sensor registration.
- `.overharness/scripts/validate.sh` - required file registration.
- `.overharness/harness/evaluations/EV-20260413-harness-evaluation-runner.md` - generated evaluation evidence.

## Must-Haves

### MH-01 - Runner script exists and is executable through wrapper

**Observable truth:** Running `bash .overharness/scripts/harness-evaluate.sh --help` exits successfully and prints usage.

**Verification:**
- `bash .overharness/scripts/harness-evaluate.sh --help`

**Failure mode this catches:** The runner was documented but cannot be invoked.

---

### MH-02 - Runner creates a durable evaluation artifact

**Observable truth:** Running the wrapper with this contract writes a Markdown evaluation under `.overharness/harness/evaluations/`.

**Verification:**
- `bash .overharness/scripts/harness-evaluate.sh --contract .overharness/harness/contracts/active/HC-20260413-harness-evaluation-runner.md`
- `test -f .overharness/harness/evaluations/EV-20260413-harness-evaluation-runner.md`

**Failure mode this catches:** The runner only prints transient output and does not persist review evidence.

---

### MH-03 - Required sensors are reflected in the evaluation

**Observable truth:** The evaluation artifact lists `overharness-validate` and `harness-doctor` with command, exit status, and blocking status.

**Verification:**
- `rg "overharness-validate|harness-doctor|Exit status|Blocks completion" .overharness/harness/evaluations/EV-20260413-harness-evaluation-runner.md`

**Failure mode this catches:** The evaluation is subjective and does not show sensor evidence.

---

### MH-04 - Completion is blocked on required sensor failures

**Observable truth:** The runner uses a non-APPROVED verdict when any required sensor exits non-zero, unless baseline exception behavior is explicitly added in a future contract.

**Verification:**
- Static review of `.overharness/scripts/harness_evaluate.py` verdict logic.

**Failure mode this catches:** Required sensors become advisory and the Harness gate is weakened.

---

### MH-05 - Core validation knows about the runner

**Observable truth:** `validate.sh` requires the runner and wrapper files.

**Verification:**
- `rg "harness_evaluate.py|harness-evaluate.sh" .overharness/scripts/validate.sh`

**Failure mode this catches:** The runner can be deleted without core validation noticing.

---

## Sensors

### Required

- **overharness-validate**: `bash .overharness/scripts/validate.sh` - checks YAML/JSON and required Harness files.
- **harness-doctor**: `bash .overharness/scripts/harness-doctor.sh` - reports Harness feedforward and feedback readiness.
- **harness-evaluate-help**: `bash .overharness/scripts/harness-evaluate.sh --help` - verifies the runner is invokable.
- **harness-evaluate-contract**: `bash .overharness/scripts/harness-evaluate.sh --contract .overharness/harness/contracts/active/HC-20260413-harness-evaluation-runner.md` - verifies the runner can generate evaluation evidence.

### Recommended

- **template-marker-scan**: static scan from `artifact_quality` sensors - useful for generated artifacts; known template files may produce intentional matches.

### Feedback Gaps

- No code-level application tests are available because this repository currently has no detected runtime test runner.
- No automatic contract promotion from active to completed exists yet.
- No automatic retry loop exists yet.

## Risk and Routing

**Risk level:** medium

**Why:** This changes the Harness control loop and introduces a new gate runner, but it is limited to scripts and documentation and does not mutate project state.

**Amy review:** Required after implementation. Amy should review the generated evaluation artifact against this contract.

**Human approval:** Not required unless the runner starts mutating `state.json` or moving contracts automatically.

## Blockers and Open Questions

- No blocker for the runner MVP.
- Follow-up decision needed: whether the runner should treat existing doctor warnings as blocking or advisory.
- Follow-up decision needed: whether to add baseline exception files.

## Exit Criteria

- [x] All required must-haves are satisfied
- [x] All required sensors passed or have documented baseline exceptions approved by the user
- [x] Deviations are documented with reason and impact
- [x] Amy reviewed the result if risk is `medium`, `high`, or `critical`
- [x] Human approval captured if risk is `critical` or documented as not applicable

## Next Handoff

Amy approved the generated evaluation artifact in
`.overharness/artifacts/review/harness-evaluation-runner-review.md`. The contract
is complete and available for future Harness work as the first runner-backed
evaluation example.
