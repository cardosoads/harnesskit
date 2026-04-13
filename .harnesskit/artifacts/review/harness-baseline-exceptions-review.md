# Review Report: Harness Baseline Exceptions

| Field | Value |
| --- | --- |
| Reviewer | amy |
| Date | 2026-04-13 |
| Artifact Reviewed | `.harnesskit/harness/evaluations/EV-20260413-harness-baseline-exceptions.md` |
| Phase | review |
| Version | 1.0 |

---

## Executive Summary

Amy reviewed the baseline exceptions feature against contract
`HC-20260413-harness-baseline-exceptions`. The implementation satisfies the
contract: known pre-Harness findings are now documented in a versioned baseline,
the doctor reclassifies only matching non-error findings as baseline info, JSON
output exposes baseline metadata, and validation requires the baseline files.

The review finds no blocking issues. This does not fix the underlying legacy
debt; it makes that debt explicit and prevents it from being confused with new
regressions.

---

## Compliance Summary

██████████ 100% (8/8 passed)

Critical: 0 | Warning: 0 | Passed: 8

---

## Review Criteria Applied

- **Completeness:** Checks whether the baseline file, doctor logic, JSON output, and validation registration all exist.
- **Consistency:** Checks whether baseline matching uses stable doctor fields rather than broad text suppression.
- **Safety:** Checks whether errors remain blocking and cannot be downgraded by baseline matching.
- **Harness evidence:** Checks contract ID, risk level, required sensor status, and evaluator routing.

---

## Issues Found

| ID | Severity | Description | Location | Recommendation |
| --- | --- | --- | --- | --- |
| None | n/a | No blocking issues found. | n/a | No action required for this contract. |

---

## Harness Review

| Field | Value |
| --- | --- |
| Contract ID | HC-20260413-harness-baseline-exceptions |
| Contract Path | `.harnesskit/harness/contracts/active/HC-20260413-harness-baseline-exceptions.md` |
| Risk Level | medium |
| Evaluator Required | yes |
| Required Sensors Passed | yes |

**Contract coverage:** All five must-haves were represented in the evaluation
artifact and independently checked during review.

**Sensor evidence:** `validate.sh` passed with 78 checked items; `harness-doctor`
reported 0 warnings, 5 info, and 4 baseline accepted findings; JSON output
included `baseline` fields; `py_compile` passed; `git diff --check` passed.

**Harness findings:**

- **Info:** Baseline entries are accepted debt, not fixes. They should eventually
  be resolved through small cleanup contracts.

---

## Must-Have Verification

| Must-Have | Result | Evidence |
| --- | --- | --- |
| MH-01 - Baseline file exists and documents current warnings | PASS | `.harnesskit/harness/baselines/current.yaml` exists and lists the four current warning codes. |
| MH-02 - Doctor reclassifies matched baseline warnings | PASS | `harness-doctor` reports `Warnings: 0`, `Info: 5`, `Baseline accepted: 4`. |
| MH-03 - JSON output exposes baseline status | PASS | `harness-doctor --format json` includes the `baseline` field for accepted issues. |
| MH-04 - Baselines do not suppress errors | PASS | `baseline_matches` returns `False` for issues with severity `error`. |
| MH-05 - Core validation requires baseline support files | PASS | `validate.sh` requires `harness/baselines/README.md` and `harness/baselines/current.yaml`. |

---

## Strengths Identified

- **Stable matching:** The baseline uses `plane`, `code`, `file`, and optional `message_contains` instead of broad text filtering.
- **Non-error only:** Errors cannot be downgraded by baseline matching.
- **Machine-readable state:** JSON output now exposes whether a finding came from a baseline.
- **Operational honesty:** The old warnings remain visible as `BASELINE`, so the debt is not hidden.

---

## Verdict

**APPROVED**

The implementation meets the contract and improves the feedback loop by
separating known baseline debt from new warnings.

---

## Required Actions

_No actions required for this contract._

---

## Next Steps

- [x] Review report delivered as an artifact.
- [x] Required actions communicated: none.
- [x] Contract can move from `active/` to `completed/`.
- [ ] Future contract: cleanup or expiration policy for baseline entries.
