# Codebase Analysis: {{project_name}}

| Field    | Value                |
|----------|----------------------|
| Project  | {{project_name}}     |
| Date     | {{date}}             |
| Version  | {{version}}          |
| Agent    | raj                  |
| Phase    | Analysis             |

---

## Project Overview

**Description:** {{description}}

**Age:** {{project_age}}

**Team Size:** {{team_size}}

**Additional Context:** {{additional_context}}

---

## Tech Stack

| Layer          | Technology     | Version    | Notes              |
|----------------|----------------|------------|--------------------|
| Language       | {{language}}   | {{ver}}    | {{notes}}          |
| Framework      | {{framework}}  | {{ver}}    | {{notes}}          |
| Database       | {{database}}   | {{ver}}    | {{notes}}          |
| ORM/ODM        | {{orm}}        | {{ver}}    | {{notes}}          |
| Testing        | {{test_fw}}    | {{ver}}    | {{notes}}          |
| Build Tool     | {{build}}      | {{ver}}    | {{notes}}          |
| Containerization | {{container}}| {{ver}}    | {{notes}}          |
| CI/CD          | {{cicd}}       | {{ver}}    | {{notes}}          |

---

## Project Structure

```
{{folder_tree}}
```

---

## Architecture Pattern

**Pattern:** {{architecture_pattern}}

**Description:** {{architecture_description}}

**Diagram (if applicable):**

```
{{architecture_diagram}}
```

---

## Key Components

| Component        | Purpose                  | Location           | Health     |
|------------------|--------------------------|--------------------|------------|
{{#each components}}
| {{name}}         | {{purpose}}              | {{location}}       | {{health}} |
{{/each}}

> 💡 **Tip:** Use Health Legend values: `Healthy`, `Needs Attention`, `Critical`, `Unknown`.

---

## Data Layer

**Database:** {{database_type}}

**ORM/ODM:** {{orm_name}}

**Models/Entities:**

{{#each models}}
- **{{name}}** — {{description}} (`{{location}}`)
{{/each}}

**Migrations:** {{migrations_status}}

---

## API / Endpoints

{{#if has_api}}
| Method | Route              | Purpose            | Auth Required |
|--------|--------------------|--------------------|---------------|
{{#each endpoints}}
| {{method}} | {{route}}      | {{purpose}}        | {{auth}}      |
{{/each}}
{{else}}
_No API endpoints detected or not applicable._
{{/if}}

---

## Testing Status

**Framework:** {{test_framework}}

**Coverage Estimate:** {{coverage_estimate}}

**Types of Tests:**

- [ ] Unit tests
- [ ] Integration tests
- [ ] End-to-end tests
- [ ] Performance tests
- [ ] Security tests

**Test Health:** {{test_health}}

**Notes:** {{test_notes}}

---

## Dependencies Summary

**Total Dependencies:** {{total_deps}}

**Outdated:** {{outdated_count}}

**Security Concerns:** {{security_concerns}}

**Notable Dependencies:**

{{#each notable_deps}}
- `{{name}}` ({{version}}) — {{note}}
{{/each}}

---

## Initial Observations

### Strengths

{{#each strengths}}
- {{this}}
{{/each}}

### Concerns

{{#each concerns}}
- {{this}}
{{/each}}

### Opportunities

{{#each opportunities}}
- {{this}}
{{/each}}

---

## Next Steps

> 📌 **Note:** Section automatically filled by the system.

- [ ] Analysis reviewed and approved by the user
- [ ] Handoff created for the next agent ({{handoff_to}})
- [ ] State.json updated with status `completed`
