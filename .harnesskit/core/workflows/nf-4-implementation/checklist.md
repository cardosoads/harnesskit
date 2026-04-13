# Validation Checklist: Feature Implementation

---

## Required Items

- [ ] **All stories implemented** — Has every story from the specification been addressed?
  - Criterion: each story has a corresponding commit or documented deviation.

- [ ] **Atomic commits** — Is there one commit per story with proper format?
  - Criterion: commits follow `feat(<story-id>): <description>` format.

- [ ] **Design followed** — Does the implementation match Leonard's architecture design?
  - Criterion: proposed changes and new components match the design document.

- [ ] **No breaking changes** — Does existing functionality remain intact?
  - Criterion: no unplanned modifications to existing behavior.

- [ ] **Deviations documented** — Are all deviations from the plan explained?
  - Criterion: each deviation has a reason and impact assessment.

- [ ] **Harness contract created** — Was an active harness contract created before implementation?
  - Criterion: the implementation report includes a contract ID, contract path, risk level, must-haves, sensors, and exit criteria.

- [ ] **Required sensors passed or baseline approved** — Did required sensors from `harness/sensors.yaml` pass, or is there an explicitly approved baseline exception?
  - Criterion: each required sensor has command, exit status, output summary, and pass/fail/baseline decision.

- [ ] **Evaluator routing applied** — Was Amy review queued when the contract risk is `medium`, `high`, or `critical`?
  - Criterion: the report states whether evaluator review is required and includes the evaluation path or handoff expectation.

---

## Optional Items (recommended)

- [ ] **Verification results included** — Were manual or automated checks performed?
  - Criterion: at least one verification method documented in the report.

- [ ] **Files changed listed** — Is each story's file change set documented?
  - Criterion: implementation report lists files changed per story.

- [ ] **Progress artifact created** — Was short-session memory recorded for continuation?
  - Criterion: a progress file exists under `.harnesskit/harness/progress/` or the report explains why the task was small enough not to need one.

---

## Validation Result

- **All required items approved?** -> Proceed to review.
- **Any required item failed?** -> Fix before proceeding.
