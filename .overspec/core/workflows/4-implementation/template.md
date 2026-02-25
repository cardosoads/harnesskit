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
_No specific dev environment configuration defined. Standard local setup assumed._
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

## Next Steps

> Section automatically filled by the system.

- [ ] Project structure created on disk
- [ ] Dependencies installed successfully
- [ ] Dev environment verified (builds and runs)
- [ ] First user story ready for implementation
- [ ] Handoff created for the next agent ({{handoff_to}})
- [ ] State.json updated with status `completed`
