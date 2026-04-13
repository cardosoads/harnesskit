# Project Brief: {{project_name}}

| Field    | Value                |
|----------|----------------------|
| Project  | {{project_name}}     |
| Date     | {{date}}             |
| Version  | {{version}}          |
| Agent    | {{agent}}            |
| Phase    | Discovery            |

---

## Overview

{{description}}

---

## Problem & Opportunity

**Problem:** {{problem}}

**Opportunity:** {{opportunity}}

---

## Target Users

{{#each user_profiles}}
### Profile: {{name}}

- **Description:** {{description}}
- **Needs:** {{needs}}
- **Pain Points:** {{pain_points}}
{{/each}}

---

## Scope

### In Scope

{{in_scope}}

### Out of Scope

{{out_of_scope}}

---

## Success Metrics

{{#if success_metrics}}
{{success_metrics}}
{{else}}
_Not defined in this version._

> 💡 **Tip:** Success metrics can be added here or revisited during the Specification phase.
{{/if}}

---

## Constraints & Assumptions

{{#if constraints}}
**Constraints:**
{{constraints}}
{{else}}
_No constraints identified at this time._
{{/if}}

**Assumptions:**
- The user has validated all information in this brief
- The scope may be refined in subsequent phases

---

## References & Inspirations

{{#if references}}
{{references}}
{{else}}
_No references provided._
{{/if}}

---

## Next Steps

> 📌 **Note:** Section automatically filled by the system.

- [ ] Brief reviewed and approved by the user
- [ ] Handoff created for the next agent ({{handoff_to}})
- [ ] State.json updated with status `completed`
