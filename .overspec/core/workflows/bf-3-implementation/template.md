# Brownfield Setup Report: {{project_name}}

| Field    | Value                |
|----------|----------------------|
| Project  | {{project_name}}     |
| Date     | {{date}}             |
| Version  | {{version}}          |
| Agent    | howard               |
| Phase    | Implementation (Brownfield) |

---

## Improvement Plan Summary

> 📌 **Note:** Extracted automatically from the improvement plan artifact.

**Total Epics:** {{total_epics}}

**Total Stories:** {{total_stories}}

**Top Priority:** {{top_priority}}

**Risk Tolerance:** {{risk_tolerance}}

---

## Selected Epic / Story

**Epic:** {{selected_epic}}

**Story:** {{selected_story}}

**Priority:** {{story_priority}}

**Effort:** {{story_effort}}

**Risk:** {{story_risk}}

**Acceptance Criteria:**

{{#each acceptance_criteria}}
- [ ] {{this}}
{{/each}}

---

## Current State

> 📌 **Note:** Current state of the area being changed, based on the codebase analysis.

{{current_state_description}}

**Affected Files:**

{{#each affected_files}}
- `{{path}}` — {{description}}
{{/each}}

**Affected Components:**

{{#each affected_components}}
- **{{name}}** ({{health}}) — {{impact}}
{{/each}}

---

## Proposed Changes

| File / Area              | What Changes           | Why                          |
|--------------------------|------------------------|------------------------------|
{{#each proposed_changes}}
| `{{file}}`               | {{what}}               | {{why}}                      |
{{/each}}

---

## Safety Net

**Test Coverage (before):** {{test_coverage_before}}

**Backup Strategy:** {{backup_strategy}}

**Rollback Plan:** {{rollback_plan}}

**Pre-change Verification:**

- [ ] All existing tests pass
- [ ] Feature branch created
- [ ] Backup/snapshot taken (if applicable)
- [ ] Team notified (if applicable)

---

## Implementation Steps

{{#each implementation_steps}}
### Step {{number}}: {{title}}

**Action:** {{action}}

**Verification:** {{verification}}

**Rollback:** {{rollback}}
{{/each}}

---

## Verification Plan

**After implementation, verify:**

{{#each verification_items}}
- [ ] {{this}}
{{/each}}

---

## Next Steps

> 📌 **Note:** Section automatically filled by the system.

- [ ] Setup report reviewed and approved by the user
- [ ] Handoff created for the next agent ({{handoff_to}})
- [ ] State.json updated with status `completed`
