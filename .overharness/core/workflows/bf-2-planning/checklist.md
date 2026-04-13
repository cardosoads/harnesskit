# Validation Checklist: Improvement Plan

Validate each item below against the generated plan. Items marked as **required** must pass for the plan to be approved. Optional items are recommended but do not block approval.

---

## Required Items

- [ ] **Goals clearly defined** — Are the user's goals documented with priorities and success metrics?
  - Criterion: at least one goal is listed with a priority level and a measurable success metric.

- [ ] **Changes prioritized** — Are proposed changes listed with type, priority, effort, and risk?
  - Criterion: the changes table is populated and each entry has all fields filled in.

- [ ] **At least 1 epic with stories** — Is there at least one epic broken down into actionable stories with acceptance criteria?
  - Criterion: at least one epic exists with at least one story, and each story has at least one acceptance criterion.

- [ ] **Risk assessment present** — Are risks identified with probability, impact, and mitigation strategies?
  - Criterion: the risk table has at least one entry with all fields filled in.

- [ ] **No changes without justification** — Is every proposed change tied to a user goal or an analysis finding?
  - Criterion: no change appears without a clear reason; changes can be traced back to goals or concerns from the analysis.

---

## Optional Items (recommended)

- [ ] **Timeline estimated** — Is there a rough implementation roadmap with phases or sprints?
  - Criterion: at least one implementation phase is defined with a timeline estimate.

- [ ] **Dependencies mapped** — Are inter-change dependencies and external constraints documented?
  - Criterion: dependencies section is populated or explicitly states "no dependencies."

- [ ] **Rollback plan considered** — Is there consideration of how to revert changes if something goes wrong?
  - Criterion: at least one mention of rollback, revert, or backup strategy in the plan.

---

## Validation Result

- **All required items approved?** -> Plan approved. Proceed to handoff.
- **Any required item failed?** -> Inform the user which item failed and go back to the corresponding step to fix it.
- **Optional items failed?** -> Inform the user, suggest filling them in, but do not block progress.
