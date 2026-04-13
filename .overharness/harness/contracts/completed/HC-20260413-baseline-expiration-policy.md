# Harness Contract: HC-20260413-baseline-expiration-policy

| Field | Value |
| --- | --- |
| Project | overharness-dev |
| Contract | HC-20260413-baseline-expiration-policy |
| Date | 2026-04-13 |
| Builder | howard |
| Evaluator | amy |
| Risk | medium |
| Source Spec | `.overharness/harness/contracts/completed/HC-20260413-harness-baseline-exceptions.md` |
| Source Design | `.overharness/harness/HARNESS.md` |
| Source Planning/Analysis | `.overharness/artifacts/planning/harness-engineering-plan.md` |
| Status | completed |

## Work Unit

Add expiration enforcement to Harness baseline exceptions so accepted warnings
cannot stay accepted indefinitely.

## Scope

### In Scope

- Require `expires_at` for baseline entries.
- Treat missing, invalid, or expired baseline dates as warnings.
- Keep matched findings as warnings when their baseline is expired or invalid.
- Include expiration metadata in doctor text and JSON output.
- Add expiration dates to the current accepted baseline entries.
- Document expiration behavior in Harness baseline docs.

### Out of Scope

- Automatically creating cleanup contracts from expired baselines.
- Automatically extending baseline dates.
- Mutating `state.json`.
- Changing the underlying legacy findings.

## Assumptions

- A 30-day expiration window is acceptable for the current pre-Harness baseline.
- Expiration is checked against the local current date.
- Errors remain impossible to downgrade through baseline matching.

## Expected Files or Areas

- `.overharness/scripts/harness_doctor.py` - expiration logic and output metadata.
- `.overharness/harness/baselines/current.yaml` - `expires_at` on each entry.
- `.overharness/harness/baselines/README.md` - expiration policy.
- `.overharness/harness/HARNESS.md` - user-facing rule summary.
- `.overharness/harness/evaluations/EV-20260413-baseline-expiration-policy.md` - evaluation evidence.

## Must-Haves

### MH-01 - Baseline entries have expiration dates

**Observable truth:** Every entry in `.overharness/harness/baselines/current.yaml` includes `expires_at`.

**Verification:**
- `rg "expires_at" .overharness/harness/baselines/current.yaml`

**Failure mode this catches:** Baseline debt becomes permanent.

---

### MH-02 - Accepted baselines expose expiration metadata

**Observable truth:** `bash .overharness/scripts/harness-doctor.sh --format json` includes `baseline_expires_at` for accepted baseline findings.

**Verification:**
- `bash .overharness/scripts/harness-doctor.sh --format json`

**Failure mode this catches:** Automation cannot see when a baseline needs review.

---

### MH-03 - Missing or invalid expiration does not accept the baseline

**Observable truth:** `harness_doctor.py` emits `baseline_missing_expiration` or `baseline_invalid_expiration` and leaves the matched finding as a warning.

**Verification:**
- Static review of `.overharness/scripts/harness_doctor.py`.

**Failure mode this catches:** Invalid baseline entries silently suppress findings.

---

### MH-04 - Expired baseline does not accept the finding

**Observable truth:** `harness_doctor.py` emits `baseline_expired` and leaves the matched finding as a warning when `expires_at` is before today.

**Verification:**
- Static review of `.overharness/scripts/harness_doctor.py`.

**Failure mode this catches:** Old baseline debt remains accepted after its review window.

---

### MH-05 - Errors still cannot be downgraded

**Observable truth:** `baseline_matches` rejects issues with severity `error`.

**Verification:**
- Static review of `.overharness/scripts/harness_doctor.py`.

**Failure mode this catches:** A baseline hides blocking feedforward or feedback failures.

---

## Sensors

### Required

- **overharness-validate**: `bash .overharness/scripts/validate.sh` - checks Harness files.
- **harness-doctor**: `bash .overharness/scripts/harness-doctor.sh` - verifies current baselines are accepted and not expired.
- **harness-evaluate-contract**: `bash .overharness/scripts/harness-evaluate.sh --contract .overharness/harness/contracts/completed/HC-20260413-baseline-expiration-policy.md` - writes evaluation evidence.

### Recommended

- **doctor-json**: `bash .overharness/scripts/harness-doctor.sh --format json` - confirms `baseline_expires_at` metadata.

### Feedback Gaps

- No automatic baseline cleanup contract generation yet.
- No dedicated unit test harness for doctor edge cases yet.

## Risk and Routing

**Risk level:** medium

**Why:** This changes how Harness warnings are classified, but only narrows acceptance by requiring expiration.

**Amy review:** Required after implementation.

**Human approval:** Not required.

## Blockers and Open Questions

- No blocker for MVP.
- Follow-up decision: whether expiration should be configurable per baseline category.

## Exit Criteria

- [x] All required must-haves are satisfied
- [x] All required sensors passed or have documented baseline exceptions approved by the user
- [x] Deviations are documented with reason and impact
- [x] Amy reviewed the result if risk is `medium`, `high`, or `critical`
- [x] Human approval captured if risk is `critical` - not applicable

## Next Handoff

Evaluation artifact:
`.overharness/harness/evaluations/EV-20260413-baseline-expiration-policy.md`

Amy review artifact:
`.overharness/artifacts/review/harness-baseline-expiration-policy-review.md`

Approved for completion and moved to
`.overharness/harness/contracts/completed/`.
