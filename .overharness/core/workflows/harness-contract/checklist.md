# Validation Checklist: Harness Contract

Validate each item below before handing the contract to Howard or Amy.

## Required Items

- [ ] **Scope is bounded** — In-scope and out-of-scope sections are both filled.
  - Criterion: the contract prevents obvious scope creep.

- [ ] **Source artifacts are referenced** — The contract points to relevant spec, design, planning, or analysis artifacts.
  - Criterion: at least one source artifact is listed, or the contract explicitly says this is a new quick/surgical change.

- [ ] **Must-haves are observable** — Each must-have can be checked through files, behavior, commands, or user acceptance.
  - Criterion: no must-have uses vague language like "improve", "clean up", or "make better" without an observable target.

- [ ] **Expected files or areas are listed** — The builder knows where work is expected.
  - Criterion: at least one file, directory, or code area is listed, or the contract explains why this cannot be known yet.

- [ ] **Sensors are selected** — Required and recommended sensors from `harness/sensors.yaml` are considered.
  - Criterion: required sensors are listed and missing sensors are documented as feedback gaps.

- [ ] **Risk routing is explicit** — Amy/human review policy follows risk.
  - Criterion: medium/high/critical contracts route to Amy; critical routes to human approval.

- [ ] **Contract is self-contained** — A fresh agent can use it without reading chat history.
  - Criterion: the contract includes enough context, scope, must-haves, sensors, and next handoff.

## Optional Items

- [ ] **Baseline failures are known** — If sensors have known failures, they are listed.
- [ ] **Progress artifact planned** — Long-running work references a progress file path.

## Validation Result

- **All required items approved?** -> Save contract and hand off.
- **Any required item failed?** -> Revise before implementation.
