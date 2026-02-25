# Feature Stories: {{project_name}}

| Field    | Value                      |
|----------|----------------------------|
| Project  | {{project_name}}           |
| Date     | {{date}}                   |
| Version  | {{version}}                |
| Agent    | penny                      |
| Phase    | Specification (New Features) |

---

## Executive Summary

{{executive_summary}}

**Total Stories:** {{total_stories}}
- Must Have: {{must_count}}
- Should Have: {{should_count}}
- Could Have: {{could_count}}

---

## User Stories by Feature

{{#each features}}
### Feature: {{name}}

{{#each stories}}
#### {{id}} — {{title}}

**As a** {{persona}},
**I want to** {{action}},
**So that** {{benefit}}.

**Acceptance Criteria:**
{{#each criteria}}
{{number}}. Given {{given}}, When {{when}}, Then {{then}}
{{/each}}

**Technical Notes:** {{technical_notes}}
**Priority:** {{priority}}
**Effort:** {{effort}}

---
{{/each}}
{{/each}}

## Story Summary

| ID | Story | Feature | Priority | Effort |
|----|-------|---------|----------|--------|
{{#each all_stories}}
| {{id}} | {{title}} | {{feature}} | {{priority}} | {{effort}} |
{{/each}}

---

## Next Steps

> Section automatically filled by the system.

- [ ] Stories reviewed and approved by the user
- [ ] Handoff created for Leonard (architecture)
- [ ] State.json updated with status `completed`
