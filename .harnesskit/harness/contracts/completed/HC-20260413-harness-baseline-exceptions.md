# Harness Contract: HC-20260413-harness-baseline-exceptions

| Field | Value |
| --- | --- |
| Project | harnesskit-dev |
| Contract | HC-20260413-harness-baseline-exceptions |
| Date | 2026-04-13 |
| Builder | howard |
| Evaluator | amy |
| Risk | medium |
| Source Spec | `.harnesskit/artifacts/analysis/current-harness-readiness-2026-04-13.md` |
| Source Design | `.harnesskit/harness/HARNESS.md` |
| Source Planning/Analysis | `.harnesskit/artifacts/planning/harness-engineering-plan.md` |
| Status | completed |

## Work Unit

Implement baseline exceptions for `harness-doctor` so known pre-Harness warnings
are explicit, versioned, and distinguishable from new regressions.

## Scope

### In Scope

- Add `.harnesskit/harness/baselines/current.yaml` with documented baseline entries.
- Teach `harness_doctor.py` to read baseline entries and reclassify matching warnings as `info`.
- Preserve unmatched warnings and all errors as normal findings.
- Include baseline metadata in text and JSON doctor output.
- Register baseline files/directories in validation and documentation.

### Out of Scope

- Hiding errors.
- Changing `state.json`.
- Fixing the legacy warnings themselves.
- Building a full baseline approval workflow.
- Adding expiration enforcement.

## Assumptions

- Baseline entries match by `plane`, `code`, and `file`.
- Optional `message_contains` narrows the match when needed.
- Baselines are advisory debt records, not proof that the underlying issue is fixed.
- Amy review is required because this changes how feedback is classified.

## Expected Files or Areas

- `.harnesskit/scripts/harness_doctor.py` - baseline matching and output.
- `.harnesskit/harness/baselines/current.yaml` - current accepted baseline.
- `.harnesskit/harness/baselines/README.md` - baseline policy.
- `.harnesskit/harness/HARNESS.md` - user-facing documentation.
- `.harnesskit/harness/feedforward.yaml` - required context registration.
- `.harnesskit/scripts/validate.sh` - required file and directory registration.
- `.harnesskit/harness/evaluations/EV-20260413-harness-baseline-exceptions.md` - generated evaluation evidence.

## Must-Haves

### MH-01 - Baseline file exists and documents current warnings

**Observable truth:** `.harnesskit/harness/baselines/current.yaml` exists and includes the four current doctor warnings as baseline entries.

**Verification:**
- `test -f .harnesskit/harness/baselines/current.yaml`
- `rg "phase_missing_in_state|artifact_placeholder|completed_step_without_artifact|implementation_report_missing_harness" .harnesskit/harness/baselines/current.yaml`

**Failure mode this catches:** Known warnings remain implicit chat knowledge.

---

### MH-02 - Doctor reclassifies matched baseline warnings

**Observable truth:** Running `bash .harnesskit/scripts/harness-doctor.sh` reports 0 warnings for the four baseline entries and reports them as baseline info.

**Verification:**
- `bash .harnesskit/scripts/harness-doctor.sh`

**Failure mode this catches:** Baseline file exists but is not consumed by the sensor.

---

### MH-03 - JSON output exposes baseline status

**Observable truth:** `bash .harnesskit/scripts/harness-doctor.sh --format json` includes baseline metadata for matched issues.

**Verification:**
- `bash .harnesskit/scripts/harness-doctor.sh --format json`
- `rg "\"baseline\"" .harnesskit/harness/evaluations/EV-20260413-harness-baseline-exceptions.md`

**Failure mode this catches:** Automation cannot distinguish baseline debt from fresh issues.

---

### MH-04 - Baselines do not suppress errors

**Observable truth:** The implementation only reclassifies non-error issues and does not turn errors into info.

**Verification:**
- Static review of `.harnesskit/scripts/harness_doctor.py`.

**Failure mode this catches:** A baseline could hide a blocking Harness failure.

---

### MH-05 - Core validation requires baseline support files

**Observable truth:** `validate.sh` requires baseline files/directories.

**Verification:**
- `rg "harness/baselines" .harnesskit/scripts/validate.sh`

**Failure mode this catches:** Baseline support can be deleted without core validation noticing.

---

## Sensors

### Required

- **harnesskit-validate**: `bash .harnesskit/scripts/validate.sh` - checks required Harness files.
- **harness-doctor**: `bash .harnesskit/scripts/harness-doctor.sh` - verifies baseline reclassification.
- **harness-evaluate-contract**: `bash .harnesskit/scripts/harness-evaluate.sh --contract .harnesskit/harness/contracts/active/HC-20260413-harness-baseline-exceptions.md` - writes evaluation evidence.

### Recommended

- **doctor-json**: `bash .harnesskit/scripts/harness-doctor.sh --format json` - confirms machine-readable baseline metadata.

### Feedback Gaps

- No expiration enforcement for baseline entries yet.
- No command to create baseline entries automatically yet.

## Risk and Routing

**Risk level:** medium

**Why:** This changes feedback classification. The change is local to Harness scripts and docs, but incorrect matching could hide important warnings.

**Amy review:** Required after implementation.

**Human approval:** Not required.

## Blockers and Open Questions

- No blocker for MVP.
- Follow-up decision: whether baseline entries should expire automatically.
- Follow-up decision: whether some baseline warnings should stay visible as warnings even after acceptance.

## Exit Criteria

- [x] All required must-haves are satisfied
- [x] All required sensors passed or have documented baseline exceptions approved by the user
- [x] Deviations are documented with reason and impact
- [x] Amy reviewed the result if risk is `medium`, `high`, or `critical`
- [x] Human approval captured if risk is `critical` or documented as not applicable

## Next Handoff

Amy approved the generated evaluation artifact in
`.harnesskit/artifacts/review/harness-baseline-exceptions-review.md`. The
contract is complete and baseline debt is now tracked separately from fresh
warnings.
