# Validation Checklist: Codebase Analysis

Validate each item below against the generated analysis. Items marked as **required** must pass for the analysis to be approved. Optional items are recommended but do not block approval.

---

## Required Items

- [ ] **Tech stack identified** — Is the tech stack documented with specific technologies and versions?
  - Criterion: at least the language, framework, and database (if applicable) are listed with versions.

- [ ] **Architecture pattern documented** — Is the architecture pattern identified and described?
  - Criterion: a pattern name is provided (e.g., MVC, layered, microservices) with a brief explanation of how it manifests in the codebase.

- [ ] **At least 3 components mapped** — Are at least three key components/modules identified with purpose and location?
  - Criterion: the components table has at least 3 entries with non-empty purpose and location fields.

- [ ] **Project structure documented** — Is the folder structure mapped and presented?
  - Criterion: a folder tree or structured overview of the project directories is included.

- [ ] **No assumptions without evidence** — Are all findings based on actual codebase observation?
  - Criterion: uncertain findings are marked with "[Needs Verification]"; no statements are presented as fact without evidence from the code.

---

## Optional Items (recommended)

- [ ] **Dependencies analyzed** — Are dependencies counted and notable ones highlighted?
  - Criterion: total dependency count is provided and at least one notable dependency is mentioned.

- [ ] **Test coverage assessed** — Is the testing infrastructure and coverage documented?
  - Criterion: test framework is identified and an estimate of coverage or test health is provided.

- [ ] **Security concerns noted** — Are any security-related observations documented?
  - Criterion: at least one statement about security posture, even if it is "no concerns identified."

---

## Validation Result

- **All required items approved?** -> Analysis approved. Proceed to handoff.
- **Any required item failed?** -> Inform the user which item failed and go back to the relevant step to fix it.
- **Optional items failed?** -> Inform the user, suggest filling them in, but do not block progress.
