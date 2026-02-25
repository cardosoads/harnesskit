# Validation Checklist: Tech Debt Report

Validate each item below against the generated report. Items marked as **required** must pass for the report to be approved. Optional items are recommended but do not block approval.

---

## Required Items

- [ ] **At least 3 findings documented** — Are there at least three tech debt findings with complete classification?
  - Criterion: the findings section has at least 3 entries, each with severity, effort, impact, and recommended action.

- [ ] **Evidence-based findings** — Is every finding backed by evidence from the codebase?
  - Criterion: each finding references specific files, configurations, or observable patterns. No finding is based purely on assumption.

- [ ] **Severity classification applied** — Are all findings classified by severity (critical/high/medium/low)?
  - Criterion: every finding has a severity level assigned.

- [ ] **Actionable recommendations** — Does every finding have a clear recommended action?
  - Criterion: every finding has an action (fix now / plan fix / accept / monitor) with a brief recommendation.

- [ ] **Summary matrix present** — Is there a summary table showing all findings at a glance?
  - Criterion: the summary matrix table is populated with all findings.

---

## Optional Items (recommended)

- [ ] **Prioritization provided** — Are findings organized into prioritized groups (quick wins, short-term, medium-term)?
  - Criterion: at least one prioritization group is populated.

- [ ] **Multiple categories covered** — Does the audit cover at least 3 different categories (dependencies, testing, security, etc.)?
  - Criterion: findings span at least 3 of the 7 audit categories.

- [ ] **Executive summary present** — Is there a concise summary at the top?
  - Criterion: executive summary exists with total finding counts by severity.

---

## Validation Result

- **All required items approved?** -> Report approved. Proceed to handoff.
- **Any required item failed?** -> Inform the user which item failed and go back to the corresponding step to fix it.
- **Optional items failed?** -> Inform the user, suggest filling them in, but do not block progress.
