# Improvement Plan: {{project_name}}

| Field    | Value                |
|----------|----------------------|
| Project  | {{project_name}}     |
| Date     | {{date}}             |
| Version  | {{version}}          |
| Agent    | raj                  |
| Phase    | Planning             |

---

## Executive Summary

{{executive_summary}}

---

## Goals & Objectives

| Goal                     | Priority   | Success Metric               |
|--------------------------|------------|------------------------------|
{{#each goals}}
| {{description}}          | {{priority}} | {{success_metric}}         |
{{/each}}

---

## Current State Summary

> Extracted from the codebase analysis artifact.

{{current_state_summary}}

---

## Proposed Changes

| ID   | Change                   | Type       | Priority | Effort | Risk   |
|------|--------------------------|------------|----------|--------|--------|
{{#each changes}}
| {{id}} | {{description}}        | {{type}}   | {{priority}} | {{effort}} | {{risk}} |
{{/each}}

**Type:** feature | refactor | fix | security | performance
**Effort:** XS | S | M | L | XL
**Risk:** Low | Medium | High

---

## Implementation Roadmap

{{#each phases}}
### Phase {{number}}: {{name}}

**Timeline:** {{timeline}}

**Focus:** {{focus}}

**Changes included:** {{change_ids}}
{{/each}}

---

## Epics & Stories

{{#each epics}}
### Epic: {{name}}

**Goal:** {{goal}}

{{#each stories}}
#### Story: {{title}}

- **Description:** {{description}}
- **Effort:** {{effort}}
- **Priority:** {{priority}}
- **Acceptance Criteria:**
{{#each acceptance_criteria}}
  - [ ] {{this}}
{{/each}}
{{/each}}
{{/each}}

---

## Risk Assessment

| Risk                     | Probability | Impact   | Mitigation                   |
|--------------------------|-------------|----------|------------------------------|
{{#each risks}}
| {{description}}          | {{probability}} | {{impact}} | {{mitigation}}          |
{{/each}}

---

## Dependencies & Constraints

**Dependencies:**

{{#each dependencies}}
- {{this}}
{{/each}}

**Constraints:**

{{#each constraints}}
- {{this}}
{{/each}}

---

## Success Metrics

{{#each success_metrics}}
- **{{name}}:** {{description}} (Target: {{target}})
{{/each}}

---

## Next Steps

> Section automatically filled by the system.

- [ ] Plan reviewed and approved by the user
- [ ] Handoff created for the next agent ({{handoff_to}})
- [ ] State.json updated with status `completed`
