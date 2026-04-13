# Harness Contract: HC-20260413-harness-doctor-selftest

| Field | Value |
| --- | --- |
| Project | overharness-dev |
| Contract | HC-20260413-harness-doctor-selftest |
| Date | 2026-04-13 |
| Builder | howard |
| Evaluator | amy |
| Risk | medium |
| Source Spec | `.overharness/harness/contracts/completed/HC-20260413-baseline-expiration-policy.md` |
| Source Design | `.overharness/harness/HARNESS.md` |
| Source Planning/Analysis | `.overharness/artifacts/planning/harness-engineering-plan.md` |
| Status | completed |

## Work Unit

Add a dedicated self-test sensor for Harness doctor baseline behavior.

## Scope

### In Scope

- Add a Python self-test script for `harness_doctor.apply_baselines`.
- Cover valid, missing, invalid, expired, and error-severity baseline cases.
- Add a shell wrapper for consistent invocation.
- Register the self-test in `validate.sh`.
- Register the self-test as a required implementation sensor.

### Out of Scope

- Building a full pytest suite.
- Testing unrelated doctor feedforward and feedback scans.
- Mutating `state.json`.
- Changing current baseline decisions.

## Assumptions

- A standard-library `unittest` script is enough for this first executable
  feedback sensor.
- The self-test may import `harness_doctor.py` directly because it lives in the
  same scripts directory.
- PyYAML remains a prerequisite for doctor baseline parsing.

## Expected Files or Areas

- `.overharness/scripts/harness_selftest.py` - self-test implementation.
- `.overharness/scripts/harness-selftest.sh` - wrapper script.
- `.overharness/scripts/validate.sh` - required-file registration.
- `.overharness/harness/sensors.yaml` - required sensor registration.
- `.overharness/harness/evaluations/EV-20260413-harness-doctor-selftest.md` -
  evaluation evidence.

## Must-Haves

### MH-01 - Self-test script exists

**Observable truth:** `.overharness/scripts/harness_selftest.py` exists and can be
executed with Python.

**Verification:**
- `python3 .overharness/scripts/harness_selftest.py`

**Failure mode this catches:** Baseline logic has no direct regression check.

---

### MH-02 - Wrapper exists

**Observable truth:** `.overharness/scripts/harness-selftest.sh` exists and invokes
the Python self-test.

**Verification:**
- `bash .overharness/scripts/harness-selftest.sh`

**Failure mode this catches:** Sensors cannot call the self-test consistently.

---

### MH-03 - Baseline expiration edge cases are covered

**Observable truth:** The self-test covers valid future expiration, missing
expiration, invalid expiration, expired baseline, and error-severity findings.

**Verification:**
- Static review of `.overharness/scripts/harness_selftest.py`.

**Failure mode this catches:** A future doctor change can silently weaken
baseline expiration enforcement.

---

### MH-04 - Core validation knows about the self-test

**Observable truth:** `validate.sh` requires both self-test files.

**Verification:**
- `bash .overharness/scripts/validate.sh`

**Failure mode this catches:** The self-test files can be removed without
structural validation noticing.

---

### MH-05 - Harness evaluation runs the self-test

**Observable truth:** `sensors.yaml` lists `harness-selftest` as a required
implementation sensor, and `harness-evaluate` records its result.

**Verification:**
- `bash .overharness/scripts/harness-evaluate.sh --contract .overharness/harness/contracts/completed/HC-20260413-harness-doctor-selftest.md`

**Failure mode this catches:** The direct doctor regression test exists but is
not part of the feedback loop.

---

## Sensors

### Required

- **overharness-validate**: `bash .overharness/scripts/validate.sh`
- **harness-doctor**: `bash .overharness/scripts/harness-doctor.sh`
- **harness-selftest**: `bash .overharness/scripts/harness-selftest.sh`
- **harness-evaluate-contract**: `bash .overharness/scripts/harness-evaluate.sh --contract .overharness/harness/contracts/completed/HC-20260413-harness-doctor-selftest.md`

### Recommended

- **python-compile**: `python3 -m py_compile .overharness/scripts/harness_doctor.py .overharness/scripts/harness_evaluate.py .overharness/scripts/harness_selftest.py`

### Feedback Gaps

- No broader unit coverage for all doctor feedforward and feedback checks yet.

## Risk and Routing

**Risk level:** medium

**Why:** This changes the required implementation sensor set, so it can block
future Harness evaluations if the self-test regresses.

**Amy review:** Required after implementation.

**Human approval:** Not required.

## Blockers and Open Questions

- No blocker for MVP.
- Follow-up decision: whether to split self-tests into a standard test package.

## Exit Criteria

- [x] All required must-haves are satisfied
- [x] All required sensors passed or have documented baseline exceptions approved by the user
- [x] Deviations are documented with reason and impact
- [x] Amy reviewed the result if risk is `medium`, `high`, or `critical`
- [x] Human approval captured if risk is `critical` - not applicable

## Next Handoff

Evaluation artifact:
`.overharness/harness/evaluations/EV-20260413-harness-doctor-selftest.md`

Amy review artifact:
`.overharness/artifacts/review/harness-doctor-selftest-review.md`

Approved for completion and moved to
`.overharness/harness/contracts/completed/`.
