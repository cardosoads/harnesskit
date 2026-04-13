# Harness Progress: {{progress_id}}

| Field | Value |
| --- | --- |
| Project | {{project_name}} |
| Contract | {{contract_id}} |
| Date | {{date}} |
| Agent | {{agent}} |
| Status | {{status}} |

## Current State

{{current_state}}

## Completed

{{#each completed_items}}
- {{this}}
{{/each}}

## In Progress

{{#each in_progress_items}}
- {{this}}
{{/each}}

## Open Issues

{{#each open_issues}}
- {{this}}
{{/each}}

## Next Action

{{next_action}}

## Resume Notes

{{resume_notes}}
