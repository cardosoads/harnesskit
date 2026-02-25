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

---

## Optional Items (recommended)

- [ ] **Verification results included** — Were manual or automated checks performed?
  - Criterion: at least one verification method documented in the report.

- [ ] **Files changed listed** — Is each story's file change set documented?
  - Criterion: implementation report lists files changed per story.

---

## Validation Result

- **All required items approved?** -> Proceed to review.
- **Any required item failed?** -> Fix before proceeding.
