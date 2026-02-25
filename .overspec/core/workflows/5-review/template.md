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

> Section automatically filled by the system.

- [ ] Review report delivered to the user
- [ ] Required actions communicated to the responsible agent
- [ ] State.json updated with review result
- [ ] Return to Sheldon for next phase routing
