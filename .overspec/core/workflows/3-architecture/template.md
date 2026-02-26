# System Architecture: {{project_name}}

| Field    | Value                |
|----------|----------------------|
| Project  | {{project_name}}     |
| Date     | {{date}}             |
| Version  | {{version}}          |
| Agent    | {{agent}}            |
| Phase    | Architecture         |

---

## System Overview

{{system_overview}}

---

## Architecture Style

{{architecture_style}}

> **Justification:** {{architecture_style_justification}}

---

## Component Diagram

{{#if component_diagram}}
{{component_diagram}}
{{else}}
```
┌─────────────────────────────────────────────────┐
│                   [Client Layer]                 │
│  ┌─────────────┐  ┌─────────────┐               │
│  │  Component A │  │  Component B │              │
│  └──────┬──────┘  └──────┬──────┘               │
│         │                │                       │
│         └───────┬────────┘                       │
│                 ▼                                 │
│         ┌──────────────┐                         │
│         │   API Layer   │                        │
│         └──────┬───────┘                         │
│                ▼                                  │
│         ┌──────────────┐                         │
│         │  Data Layer   │                        │
│         └──────────────┘                         │
└─────────────────────────────────────────────────┘
```
> 💡 **Tip:** Replace this placeholder with the actual component diagram for the project.
{{/if}}

---

## Components

{{#each components}}
### {{name}}

- **Responsibility:** {{responsibility}}
- **Interfaces:** {{interfaces}}
- **Dependencies:** {{dependencies}}

{{/each}}

---

## Data Model

### Entities

{{#each entities}}
#### {{name}}

- **Description:** {{description}}
- **Key Attributes:** {{attributes}}
- **Relationships:** {{relationships}}

{{/each}}

### Entity Relationship Summary

{{entity_relationship_summary}}

---

## API Design

{{#if api_design}}
{{api_design}}
{{else}}
_Not applicable or to be defined in a subsequent workflow._
{{/if}}

---

## Technology Stack

| Layer        | Technology        | Justification                |
|--------------|-------------------|------------------------------|
{{#each tech_stack}}
| {{layer}}    | {{technology}}    | {{justification}}            |
{{/each}}

---

## Non-Functional Requirements & Solutions

| Requirement       | Target                  | Architectural Solution          |
|-------------------|-------------------------|---------------------------------|
{{#each non_functional}}
| {{requirement}}   | {{target}}              | {{solution}}                    |
{{/each}}

---

## Integration Points

{{#if integrations}}
{{#each integrations}}
### {{name}}

- **Type:** {{type}}
- **Purpose:** {{purpose}}
- **Protocol:** {{protocol}}
- **Notes:** {{notes}}

{{/each}}
{{else}}
_No external integrations identified at this time._
{{/if}}

---

## Architecture Decision Records (ADRs)

{{#if adrs}}
{{#each adrs}}
### ADR-{{number}}: {{title}}

- **Status:** {{status}}
- **Context:** {{context}}
- **Options Considered:**
{{#each options}}
  - **{{name}}:** {{description}} _(Pros: {{pros}} | Cons: {{cons}})_
{{/each}}
- **Decision:** {{decision}}
- **Consequences:** {{consequences}}

{{/each}}
{{else}}
_No ADRs recorded yet. ADRs will be added as architectural decisions are made._
{{/if}}

---

## Risks & Mitigations

{{#if risks}}
| Risk                  | Impact   | Probability | Mitigation                     |
|-----------------------|----------|-------------|--------------------------------|
{{#each risks}}
| {{risk}}              | {{impact}} | {{probability}} | {{mitigation}}           |
{{/each}}
{{else}}
_No significant architectural risks identified at this time._
{{/if}}

---

## Next Steps

> 📌 **Note:** Section automatically filled by the system.

- [ ] Architecture reviewed and approved by the user
- [ ] Technology stack validated against team capabilities
- [ ] Handoff created for the next agent ({{handoff_to}})
- [ ] State.json updated with status `completed`
