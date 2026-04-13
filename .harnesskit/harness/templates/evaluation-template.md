# Harness Evaluation: {{evaluation_id}}

| Field | Value |
| --- | --- |
| Project | {{project_name}} |
| Evaluation | {{evaluation_id}} |
| Contract | {{contract_id}} |
| Date | {{date}} |
| Evaluator | {{evaluator_agent}} |
| Verdict | {{verdict}} |
| Score | {{score}} |

## Contract Coverage

{{#each must_have_results}}
### {{id}} - {{status}}

**Expected truth:** {{truth}}

**Evidence:** {{evidence}}

**Finding:** {{finding}}

**Required follow-up:** {{follow_up}}

---
{{/each}}

## Sensor Results

{{#each sensor_results}}
### {{id}} - {{status}}

**Command:** `{{command}}`

**Exit status:** {{exit_status}}

**Output summary:** {{output_summary}}

**Blocks completion:** {{blocks_completion}}

---
{{/each}}

## Deviations

{{#each deviations}}
- **{{id}}:** {{description}}
  Reason: {{reason}}
  Impact: {{impact}}
{{/each}}

## Verdict Rules

- `APPROVED`: all required must-haves and required sensors passed.
- `NEEDS_FIX`: one or more must-haves failed but are fixable within current scope.
- `BLOCKED`: missing decision, missing sensor baseline, or unsafe scope expansion.
- `ESCALATE`: human decision required.

## Final Recommendation

{{recommendation}}
