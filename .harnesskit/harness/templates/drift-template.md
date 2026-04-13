# Harness Drift Report: {{date}}

| Field | Value |
| --- | --- |
| Project | {{project_name}} |
| Date | {{date}} |
| Agent | {{agent}} |
| Scope | {{scope}} |

## Drift Signals

{{#each drift_signals}}
- **{{type}}:** {{description}}
  Evidence: {{evidence}}
  Suggested sensor/rule: {{suggested_control}}
{{/each}}

## Recommended Cleanup

{{#each cleanup_items}}
- {{this}}
{{/each}}

## Follow-Up Contracts

{{#each follow_up_contracts}}
- {{this}}
{{/each}}
