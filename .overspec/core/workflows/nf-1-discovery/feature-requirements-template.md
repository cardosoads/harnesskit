# Feature Requirements: {{project_name}}

| Field    | Value                      |
|----------|----------------------------|
| Project  | {{project_name}}           |
| Date     | {{date}}                   |
| Version  | {{version}}                |
| Agent    | penny                      |
| Phase    | Discovery (New Features)   |
| Based on | Impact Analysis by raj     |

---

## Executive Summary

{{executive_summary}}

---

## Features

{{#each features}}
### {{id}} — {{name}}

**Description:** {{description}}

**User/Persona:** {{user_persona}}

**Impact Summary (from Raj):** {{impact_summary}}

#### Functional Requirements

{{#each functional_requirements}}
- **{{id}}:** {{description}}
{{/each}}

#### Non-Functional Requirements

{{#each non_functional_requirements}}
- **{{id}}:** {{description}}
{{/each}}

#### Acceptance Criteria

{{#each acceptance_criteria}}
- **{{id}}:** Given {{given}}, When {{when}}, Then {{then}}
{{/each}}

#### Business Rules

{{business_rules}}

---
{{/each}}

## Summary Matrix

| Feature | Priority | Effort | Risk | Functional Reqs | Acceptance Criteria |
|---------|----------|--------|------|-----------------|---------------------|
{{#each features}}
| {{name}} | {{priority}} | {{effort}} | {{risk}} | {{func_count}} | {{ac_count}} |
{{/each}}

---

## Scope Decisions

{{#if scope_changes}}
### Changes from Original Proposal
{{scope_changes}}
{{/if}}

### In Scope
{{in_scope}}

### Out of Scope
{{out_of_scope}}

---

## Next Steps

> Section automatically filled by the system.

- [ ] Requirements reviewed and approved by the user
- [ ] Handoff created for specification phase (penny)
- [ ] State.json updated with status `completed`
