# User Stories: {{project_name}}

| Field    | Value                |
|----------|----------------------|
| Project  | {{project_name}}     |
| Date     | {{date}}             |
| Version  | {{version}}          |
| Agent    | {{agent}}            |
| Phase    | Specification        |

---

## Epics Overview

| Epic ID | Epic Name       | Description                  | Stories Count |
|---------|-----------------|------------------------------|---------------|
{{#each epics}}
| {{id}}  | {{name}}        | {{description}}              | {{story_count}} |
{{/each}}

---

{{#each epics}}
## Epic: {{name}}

{{description}}

{{#each stories}}
### {{epic_id}}-{{story_id}}: {{title}}

**As a** {{persona}}, **I want** {{action}}, **so that** {{benefit}}.

**Acceptance Criteria:**

{{#each acceptance_criteria}}
- **Given** {{given}}
  **When** {{when}}
  **Then** {{then}}
{{/each}}

| Priority   | Complexity | Dependencies       |
|------------|------------|--------------------|
| {{priority}} | {{complexity}} | {{dependencies}} |

---

{{/each}}
{{/each}}

## Priority Summary

| Priority    | Count |
|-------------|-------|
| Must-Have   | {{must_have_count}}   |
| Should-Have | {{should_have_count}} |
| Could-Have  | {{could_have_count}}  |
| Won't-Have  | {{wont_have_count}}   |

---

## Dependencies Map

{{#if dependencies}}
{{#each dependencies}}
- {{from}} -> {{to}}: {{reason}}
{{/each}}
{{else}}
_No inter-story dependencies identified._
{{/if}}

---

## Next Steps

> Section automatically filled by the system.

- [ ] User stories reviewed and approved by the user
- [ ] Handoff created for the next agent ({{handoff_to}})
- [ ] State.json updated with status `completed`
