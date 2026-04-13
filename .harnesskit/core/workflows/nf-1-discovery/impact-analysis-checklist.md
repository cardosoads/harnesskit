# Validation Checklist: Impact Analysis

Validate each item below against the generated report. Items marked as **required** must pass for the report to be approved.

---

## Required Items

- [ ] **Feature(s) clearly described** — Is every proposed feature described with its purpose and scope?
  - Criterion: each feature has a name, description, and clear scope.

- [ ] **Affected components identified** — Are all affected existing components listed with file paths?
  - Criterion: each feature has at least one affected component with a specific path.

- [ ] **Risk assessment present** — Does every feature have a risk assessment?
  - Criterion: each feature has risk level (low/medium/high) with explanation.

- [ ] **Recommended approach provided** — Does every feature have an implementation recommendation?
  - Criterion: each feature has a concrete approach, not just "implement it."

- [ ] **Summary matrix present** — Is there a summary table with all features at a glance?
  - Criterion: the matrix has effort, risk, and file counts for each feature.

---

## Optional Items (recommended)

- [ ] **New components identified** — Are new files/modules that need to be created listed?
  - Criterion: at least one feature lists new components to create.

- [ ] **Dependencies documented** — Are external or internal dependencies noted?
  - Criterion: dependency section is populated for features that have them.

- [ ] **Integration points mapped** — Are the connection points between new and existing code identified?
  - Criterion: at least one integration point is described per feature.

---

## Validation Result

- **All required items approved?** -> Report approved. Proceed to handoff to Penny.
- **Any required item failed?** -> Go back to the corresponding step to fix it.
- **Optional items failed?** -> Inform but do not block progress.
