# Requirements: {{project_name}}

| Field    | Value                |
|----------|----------------------|
| Project  | {{project_name}}     |
| Date     | {{date}}             |
| Version  | {{version}}          |
| Agent    | penny                |
| Phase    | Discovery            |

---

## Brief Summary

> Key context extracted from the project brief.

{{brief_summary}}

---

## Functional Requirements

| ID    | Requirement              | Acceptance Criteria          | Priority |
|-------|--------------------------|------------------------------|----------|
{{#each functional_requirements}}
| {{id}} | {{description}}         | {{acceptance_criteria}}      | {{priority}} |
{{/each}}

---

## Non-Functional Requirements

| ID     | Category       | Requirement              | Acceptance Criteria          | Priority |
|--------|----------------|--------------------------|------------------------------|----------|
{{#each non_functional_requirements}}
| {{id}} | {{category}}   | {{description}}          | {{acceptance_criteria}}      | {{priority}} |
{{/each}}

**Categories:** Performance | Security | Scalability | Accessibility | Reliability | Usability

---

## Business Rules

{{#if business_rules}}
| ID     | Rule                     | Rationale                    |
|--------|--------------------------|------------------------------|
{{#each business_rules}}
| {{id}} | {{description}}          | {{rationale}}                |
{{/each}}
{{else}}
_No business rules identified at this time._
{{/if}}

---

## Integrations

{{#if integrations}}
| ID     | System / API             | Purpose                      | Priority |
|--------|--------------------------|------------------------------|----------|
{{#each integrations}}
| {{id}} | {{system}}               | {{purpose}}                  | {{priority}} |
{{/each}}
{{else}}
_No external integrations required at this time._
{{/if}}

---

## Prioritization Summary (MoSCoW)

### Must Have
{{#each must_have}}
- {{id}}: {{description}}
{{/each}}

### Should Have
{{#each should_have}}
- {{id}}: {{description}}
{{/each}}

### Could Have
{{#each could_have}}
- {{id}}: {{description}}
{{/each}}

### Won't Have (this version)
{{#each wont_have}}
- {{id}}: {{description}}
{{/each}}

---

## Next Steps

> Section automatically filled by the system.

- [ ] Requirements reviewed and approved by the user
- [ ] Handoff created for the next agent ({{handoff_to}})
- [ ] State.json updated with status `completed`
