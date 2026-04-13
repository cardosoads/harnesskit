# Validation Checklist: Requirements

Validate each item below against the generated requirements document. Items marked as **required** must pass for the document to be approved. Optional items are recommended but do not block approval.

---

## Required Items

- [ ] **At least 3 functional requirements** — Are there at least three functional requirements with IDs, descriptions, and acceptance criteria?
  - Criterion: the functional requirements table has at least 3 entries with all fields filled in.

- [ ] **At least 1 non-functional requirement** — Is there at least one non-functional requirement documented?
  - Criterion: the non-functional requirements table has at least 1 entry with category, description, and acceptance criteria.

- [ ] **MoSCoW prioritization applied** — Are requirements prioritized using Must/Should/Could/Won't?
  - Criterion: the prioritization summary section has at least the "Must Have" list populated.

- [ ] **Acceptance criteria for all Must-Have** — Do all Must-Have requirements have clear acceptance criteria?
  - Criterion: every requirement listed as Must-Have has a non-empty acceptance criteria field.

- [ ] **No contradictions with brief** — Are the requirements consistent with the project brief?
  - Criterion: no requirement contradicts the scope, constraints, or problem defined in the brief.

---

## Optional Items (recommended)

- [ ] **Business rules documented** — Are domain-specific rules captured?
  - Criterion: business rules section has at least one entry, or explicitly states "none identified."

- [ ] **Integrations identified** — Are external system dependencies documented?
  - Criterion: integrations section has at least one entry, or explicitly states "none required."

- [ ] **Each requirement has a source** — Can each requirement be traced back to the brief or a user statement?
  - Criterion: requirements feel grounded in the brief context, not invented.

---

## Validation Result

- **All required items approved?** -> Requirements approved. Proceed to handoff.
- **Any required item failed?** -> Inform the user which item failed and go back to the corresponding step to fix it.
- **Optional items failed?** -> Inform the user, suggest filling them in, but do not block progress.
