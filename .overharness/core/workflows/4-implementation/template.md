# Setup Report: {{project_name}}

| Field    | Value                |
|----------|----------------------|
| Project  | {{project_name}}     |
| Date     | {{date}}             |
| Version  | {{version}}          |
| Agent    | howard               |
| Phase    | Implementation       |

---

## Tech Stack Summary

| Layer      | Technology          | Version   |
|------------|---------------------|-----------|
{{#each tech_stack}}
| {{layer}}  | {{technology}}      | {{version}} |
{{/each}}

---

## Project Structure

```
{{project_structure}}
```

---

## Core Dependencies

### Production Dependencies

| Package         | Version   | Purpose                          |
|-----------------|-----------|----------------------------------|
{{#each prod_dependencies}}
| {{name}}        | {{version}} | {{purpose}}                    |
{{/each}}

### Development Dependencies

| Package         | Version   | Purpose                          |
|-----------------|-----------|----------------------------------|
{{#each dev_dependencies}}
| {{name}}        | {{version}} | {{purpose}}                    |
{{/each}}

---

## Dev Environment Setup

{{#if dev_environment}}
{{dev_environment}}
{{else}}
> 📌 **Note:** No specific dev environment configuration defined. Standard local setup assumed.
{{/if}}

---

## Coding Standards & Conventions

{{#if coding_standards}}
{{coding_standards}}
{{else}}
_No specific coding standards defined. Default language conventions apply._
{{/if}}

---

## Build & Run Instructions

### Prerequisites

{{prerequisites}}

### Installation

```bash
{{install_commands}}
```

### Running in Development

```bash
{{dev_commands}}
```

### Running Tests

```bash
{{test_commands}}
```

### Building for Production

```bash
{{build_commands}}
```

---

## Harness Contract

| Field | Value |
|-------|-------|
| Contract ID | {{harness_contract_id}} |
| Contract Path | `{{harness_contract_path}}` |
| Risk Level | {{harness_risk_level}} |
| Evaluator Required | {{harness_evaluator_required}} |

**Must-haves:**

{{#each harness_must_haves}}
- [ ] {{this}}
{{/each}}

**Out of scope:**

{{#each harness_out_of_scope}}
- {{this}}
{{/each}}

---

## Harness Sensor Evidence

{{#each harness_sensors}}
### {{id}} — {{status}}

**Command:** `{{command}}`

**Required:** {{required}}

**Evidence:** {{evidence}}

---
{{/each}}

---

## Next Steps

> 📌 **Note:** Section automatically filled by the system.

- [ ] Project structure created on disk
- [ ] Dependencies installed successfully
- [ ] Dev environment verified (builds and runs)
- [ ] First user story ready for implementation
- [ ] Harness contract created and referenced
- [ ] Harness sensor evidence recorded
- [ ] Handoff created for the next agent ({{handoff_to}})
- [ ] State.json updated with status `completed`
