# Harness Contract: {{contract_id}}

| Field | Value |
| --- | --- |
| Project | {{project_name}} |
| Contract | {{contract_id}} |
| Date | {{date}} |
| Builder | {{builder_agent}} |
| Evaluator | {{evaluator_agent}} |
| Risk | {{risk_level}} |
| Source Spec | {{source_spec}} |
| Source Design | {{source_design}} |
| Source Planning/Analysis | {{source_planning}} |
| Status | active |

## Work Unit

{{work_unit_summary}}

## Scope

### In Scope

{{#each in_scope}}
- {{this}}
{{/each}}

### Out of Scope

{{#each out_of_scope}}
- {{this}}
{{/each}}

## Assumptions

{{#each assumptions}}
- {{this}}
{{/each}}

## Expected Files or Areas

{{#each expected_files}}
- `{{path}}` — {{reason}}
{{/each}}

## Must-Haves

{{#each must_haves}}
### {{id}} — {{truth}}

**Observable truth:** {{truth}}

**Verification:**
{{#each verification}}
- `{{this}}`
{{/each}}

**Failure mode this catches:** {{failure_mode}}

---
{{/each}}

## Sensors

### Required

{{#each required_sensors}}
- **{{id}}**: `{{command}}` — {{why}}
{{/each}}

### Recommended

{{#each recommended_sensors}}
- **{{id}}**: `{{command}}` — {{why}}
{{/each}}

### Feedback Gaps

{{#each feedback_gaps}}
- {{this}}
{{/each}}

## Risk and Routing

**Risk level:** {{risk_level}}

**Why:** {{risk_reason}}

**Amy review:** {{amy_review_policy}}

**Human approval:** {{human_approval_policy}}

## Blockers and Open Questions

{{#each blockers}}
- {{this}}
{{/each}}

## Exit Criteria

- [ ] All required must-haves are satisfied
- [ ] All required sensors passed or have documented baseline exceptions approved by the user
- [ ] Deviations are documented with reason and impact
- [ ] Amy reviewed the result if risk is `medium`, `high`, or `critical`
- [ ] Human approval captured if risk is `critical`

## Next Handoff

{{next_handoff}}
