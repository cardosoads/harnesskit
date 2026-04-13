# Review Report: Harness Baseline Expiration Policy

| Field | Value |
| --- | --- |
| Reviewer | amy |
| Date | 2026-04-13 |
| Artifact Reviewed | `.overspec/harness/evaluations/EV-20260413-baseline-expiration-policy.md` |
| Phase | review |
| Version | 1.0 |

---

## Executive Summary

Amy reviewed the baseline expiration policy against contract
`HC-20260413-baseline-expiration-policy`. The implementation satisfies the
contract: accepted baseline entries now require `expires_at`, accepted baseline
findings expose expiration metadata, and missing, invalid, or expired baseline
dates do not reclassify the original finding.

The review finds no blocking issues. The policy intentionally narrows baseline
acceptance instead of resolving the underlying legacy findings.

---

## Compliance Summary

██████████ 100% (8/8 passed)

Critical: 0 | Warning: 0 | Passed: 8

---

## Review Criteria Applied

- **Completeness:** Checks whether expiration dates, docs, doctor behavior, and
  evaluation evidence exist.
- **Safety:** Checks whether errors still cannot be downgraded and expired
  baselines leave the original finding visible.
- **Observability:** Checks whether accepted baseline findings expose
  `baseline_expires_at` in JSON output and text output includes expiration.
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
| Contract ID | HC-20260413-baseline-expiration-policy |
| Contract Path | `.overspec/harness/contracts/completed/HC-20260413-baseline-expiration-policy.md` |
| Risk Level | medium |
| Evaluator Required | yes |
| Required Sensors Passed | yes |

**Contract coverage:** All five must-haves were represented in the evaluation
artifact and independently checked during review.

**Sensor evidence:** `harness-evaluate` approved the contract; `validate.sh`
passed with 78 checked items; `harness-doctor` reported 0 warnings, 5 info, and
4 accepted baselines with `expires: 2026-05-13`; JSON output included
`baseline_expires_at`; `py_compile` passed.

**Harness findings:**

- **Info:** Baseline expiration is enforced at doctor time only. It does not
  auto-create cleanup contracts yet.
- **Info:** The current baseline expires on 2026-05-13 and should become either
  cleanup work or an explicit renewal decision before that date.

---

## Must-Have Verification

| Must-Have | Result | Evidence |
| --- | --- | --- |
| MH-01 - Baseline entries have expiration dates | PASS | `.overspec/harness/baselines/current.yaml` has `expires_at` on all four accepted entries. |
| MH-02 - Accepted baselines expose expiration metadata | PASS | `harness-doctor --format json` includes `baseline_expires_at` for accepted findings. |
| MH-03 - Missing or invalid expiration does not accept the baseline | PASS | `apply_baselines` emits `baseline_missing_expiration` or `baseline_invalid_expiration` and does not reclassify the matched finding. |
| MH-04 - Expired baseline does not accept the finding | PASS | `apply_baselines` emits `baseline_expired` when `expires_at` is before the current date. |
| MH-05 - Errors still cannot be downgraded | PASS | `baseline_matches` returns `False` when the issue severity is `error`. |

---

## Strengths Identified

- **Time-bounded debt:** Current baseline debt now has a concrete review date.
- **Machine-readable metadata:** Automation can inspect `baseline_expires_at`.
- **Conservative failure mode:** Invalid or expired baseline dates leave the
  original warning visible instead of accepting it.
- **Error safety:** Blocking findings still cannot be hidden by baseline entries.

---

## Verdict

**APPROVED**

The implementation meets the contract and improves the feedback loop by making
accepted baseline debt temporary and visible.

---

## Required Actions

_No actions required for this contract._

---

## Next Steps

- [x] Review report delivered as an artifact.
- [x] Required actions communicated: none.
- [x] Contract can move from `active/` to `completed/`.
- [ ] Future contract: generate cleanup prompts or contracts when baselines are
  expired or close to expiration.
