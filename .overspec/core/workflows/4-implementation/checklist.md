# Validation Checklist: Project Setup

Validate each item below against the generated setup report. Items marked as **required** must pass for the report to be approved. Optional items are recommended but do not block approval.

---

## Required Items

- [ ] **Tech stack matches architecture** — Does the tech stack in the setup report match what was defined in the architecture document?
  - Criterion: every technology listed in the architecture (languages, frameworks, databases) is present in the setup report with a corresponding version.

- [ ] **Project structure covers all components** — Does the folder structure cover all architectural components (layers, modules, services)?
  - Criterion: each component from the architecture's component diagram has a corresponding directory in the project structure.

- [ ] **Core dependencies listed with versions** — Are all core dependencies listed with their specific versions?
  - Criterion: every dependency has a name, version number, and stated purpose. No unversioned dependencies.

- [ ] **Build instructions documented** — Are there clear instructions for how to install, run, and test the project?
  - Criterion: a developer can follow the instructions from scratch and get a running dev environment.

- [ ] **No conflicting or redundant dependencies** — Are there any dependencies that conflict with each other or serve the same purpose?
  - Criterion: no two dependencies solve the same problem; no known version conflicts exist.

- [ ] **Harness contract created** — Was an active harness contract created and referenced in the setup report?
  - Criterion: the report includes a contract ID, contract path, risk level, must-haves, and exit criteria.

- [ ] **Harness sensor evidence recorded** — Were required and applicable recommended sensors from `harness/sensors.yaml` considered?
  - Criterion: the report lists each applicable sensor with status, evidence, and any approved baseline or reason it could not run.

---

## Optional Items (recommended)

- [ ] **Docker setup documented** — Is there a Docker or Docker Compose configuration for the dev environment?
  - Criterion: a Dockerfile or docker-compose.yml is described or referenced with instructions for use.

- [ ] **CI/CD configuration** — Is there a plan or configuration for continuous integration and deployment?
  - Criterion: at least a mention of the CI/CD tool and the basic pipeline steps (build, test, deploy).

- [ ] **Linting and formatting rules** — Are linting and code formatting rules defined and documented?
  - Criterion: the linter and formatter are listed as dev dependencies with their configuration files referenced.

- [ ] **Environment variables documented** — Are required environment variables listed with descriptions?
  - Criterion: a table or list of env vars with name, description, and example values.

- [ ] **Evaluator policy documented** — Does the report state whether Amy review is required by risk level?
  - Criterion: the harness section includes `Evaluator Required` and explains the decision.

---

## Validation Result

- **All required items approved?** -> Setup report approved. Proceed to handoff.
- **Any required item failed?** -> Inform the user which item failed and go back to the corresponding step to fix it.
- **Optional items failed?** -> Inform the user, suggest filling them in, but do not block progress.
