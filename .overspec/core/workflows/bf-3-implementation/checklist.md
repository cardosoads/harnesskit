# Validation Checklist: Brownfield Setup Report

Validate each item below against the generated report. Items marked as **required** must pass for the report to be approved. Optional items are recommended but do not block approval.

---

## Required Items

- [ ] **Plan reviewed** — Were the improvement plan priorities confirmed with the user?
  - Criterion: the report references the improvement plan and confirms the selected priorities.

- [ ] **Safety net in place** — Is there a documented backup strategy, rollback plan, and pre-change verification?
  - Criterion: the safety net section is filled in with a specific rollback plan and at least one pre-change verification item is checked or addressed.

- [ ] **First change identified** — Is a specific epic/story selected with clear acceptance criteria?
  - Criterion: a selected epic and story are named with at least one acceptance criterion listed.

- [ ] **Approach validated** — Is the implementation approach described with ordered, incremental steps?
  - Criterion: at least two implementation steps are listed, each with an action and a verification method.

- [ ] **Rollback possible** — Can the proposed changes be reverted if something goes wrong?
  - Criterion: a rollback plan is documented and each implementation step has a rollback note.

---

## Optional Items (recommended)

- [ ] **Tests written before changes** — Are tests planned or written before modifying existing code?
  - Criterion: at least one mention of writing or verifying tests before making changes.

- [ ] **Impact on other components assessed** — Is the impact on other parts of the codebase documented?
  - Criterion: affected components are listed with their expected impact.

---

## Validation Result

- **All required items approved?** -> Report approved. Proceed to handoff.
- **Any required item failed?** -> Inform the user which item failed and go back to the corresponding step to fix it.
- **Optional items failed?** -> Inform the user, suggest filling them in, but do not block progress.
