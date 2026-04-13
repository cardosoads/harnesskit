# Review Report

| Field             | Value                          |
|-------------------|--------------------------------|
| Reviewer          | {{reviewer}}                   |
| Date              | {{date}}                       |
| Artifact Reviewed | {{artifact_path}}              |
| Phase             | {{artifact_phase}}             |
| Version           | {{version}}                    |

---

## Executive Summary

{{executive_summary}}

---

## Compliance Summary

{{compliance_bar}}

{{#if severity_breakdown}}
🔴 Critical: {{critical_count}} | 🟡 Warning: {{warning_count}} | 🟢 Passed: {{passed_count}}
{{/if}}

> 📌 **Note:** Compliance bar uses the format `████████░░ 80% (N/M passed)`.
> See `core/style-guide.md` for progress bar specification.

---

## Review Criteria Applied

{{#each criteria}}
- **{{name}}**: {{description}}
{{/each}}

---

## Issues Found

| ID  | Severity | Description | Location | Recommendation |
|-----|----------|-------------|----------|----------------|
{{#each issues}}
| {{id}} | {{severity}} | {{description}} | {{location}} | {{recommendation}} |
{{/each}}

{{#if no_issues}}
_No issues found. All criteria passed._
{{/if}}

---

## Harness Review

{{#if harness_review_applicable}}
| Field | Value |
|-------|-------|
| Contract ID | {{harness_contract_id}} |
| Contract Path | `{{harness_contract_path}}` |
| Risk Level | {{harness_risk_level}} |
| Evaluator Required | {{harness_evaluator_required}} |
| Required Sensors Passed | {{harness_required_sensors_passed}} |

**Contract coverage:** {{harness_contract_coverage}}

**Sensor evidence:** {{harness_sensor_evidence_summary}}

**Harness findings:**

{{#each harness_findings}}
- **{{severity}}:** {{description}} — {{recommendation}}
{{/each}}
{{else}}
_Harness review not applicable to this artifact._
{{/if}}

---

## Strengths Identified

{{#each strengths}}
- **{{title}}**: {{description}}
{{/each}}

{{#if no_strengths}}
_No notable strengths identified._
{{/if}}

---

## Verdict

**{{verdict}}**

{{verdict_justification}}

---

## Required Actions

{{#if actions}}
{{#each actions}}
1. {{description}} — _Severity: {{severity}}_
{{/each}}
{{else}}
_No actions required. Artifact is approved._
{{/if}}

---

## Next Steps

> 📌 **Note:** Section automatically filled by the system.

- [ ] Review report delivered to the user
- [ ] Required actions communicated to the responsible agent
- [ ] State.json updated with review result
- [ ] Return to Sheldon for next phase routing
