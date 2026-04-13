# Validation Checklist: System Architecture

Validate each item below against the generated architecture document. Items marked as **required** must pass for the document to be approved. Optional items are recommended but do not block approval.

---

## Required Items

- [ ] **System type clearly defined** — Is the type of system (web app, mobile, API, CLI, etc.) explicitly stated with a brief justification?
  - Criterion: a reader can identify in one sentence what kind of system is being built.

- [ ] **Architecture style justified** — Is the chosen architecture style (monolith, microservices, serverless, etc.) stated with a clear justification for why it was chosen over alternatives?
  - Criterion: the justification references project constraints, team capabilities, or requirements.

- [ ] **At least 3 components identified** — Are there at least three components/modules listed with their responsibilities clearly defined?
  - Criterion: each component has a name, a responsibility description, and its interfaces or dependencies.

- [ ] **Data model covers main entities** — Does the data model include the key entities of the system with their attributes and relationships?
  - Criterion: at least the core entities are described with their key attributes and how they relate to each other.

- [ ] **Non-functional requirements addressed** — Are the key non-functional requirements (performance, scalability, security) listed with corresponding architectural solutions?
  - Criterion: each non-functional requirement has a target metric and an architectural approach to meet it.

- [ ] **No technology choices without justification** — Is every technology choice accompanied by a reason for selection?
  - Criterion: the tech stack table has a justification column filled for every entry.

---

## Optional Items (recommended)

- [ ] **Integration points documented** — Are external systems and APIs listed with their type, purpose, and protocol?
  - Criterion: each integration has at least a name, purpose, and communication method.

- [ ] **ADRs present** — Are there Architecture Decision Records for significant decisions made during the design?
  - Criterion: at least one ADR with context, options considered, decision, and consequences.

- [ ] **Diagrams included** — Are there visual diagrams (component diagram, data model diagram, or similar) to aid understanding?
  - Criterion: at least one diagram or structured text representation of the system structure.

- [ ] **Risks identified** — Are architectural risks listed with impact assessment and mitigation strategies?
  - Criterion: at least one risk with impact, probability, and mitigation described.

---

## Validation Result

- **All required items approved?** -> Architecture document approved. Proceed to handoff.
- **Any required item failed?** -> Inform the user which item failed and go back to the corresponding step to fix it.
- **Optional items failed?** -> Inform the user, suggest filling them in, but do not block progress.
