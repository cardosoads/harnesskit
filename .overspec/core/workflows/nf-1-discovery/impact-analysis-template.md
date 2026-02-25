# Impact Analysis: {{project_name}}

| Field    | Value                |
|----------|----------------------|
| Project  | {{project_name}}     |
| Date     | {{date}}             |
| Version  | {{version}}          |
| Agent    | raj                  |
| Phase    | Discovery (New Features) |

---

## Feature Overview

{{feature_description}}

---

## Current Architecture Summary

{{architecture_summary}}

---

## Impact Assessment

{{#each features}}
### {{name}}

| Field | Value |
|-------|-------|
| **Effort** | {{effort}} |
| **Risk** | {{risk}} |
| **Priority** | {{priority}} |

**Affected Components:**
{{#each affected_components}}
- `{{path}}` — {{description}}
{{/each}}

**New Components:**
{{#each new_components}}
- `{{path}}` — {{description}}
{{/each}}

**Dependencies:**
{{dependencies}}

**Integration Points:**
{{integration_points}}

**Risk Details:**
{{risk_details}}

**Recommended Approach:**
{{approach}}

---
{{/each}}

## Summary Matrix

| Feature | Effort | Risk | Affected Files | New Files |
|---------|--------|------|----------------|-----------|
{{#each features}}
| {{name}} | {{effort}} | {{risk}} | {{affected_count}} | {{new_count}} |
{{/each}}

---

## Recommendations

{{recommendations}}

---

## Next Steps

> Section automatically filled by the system.

- [ ] Impact analysis reviewed and approved by the user
- [ ] Handoff created for Penny (feature requirements)
- [ ] State.json updated with status `completed`
