# Validation Checklist: Review Report

Validate each item below against the generated review report. Items marked as **required** must pass for the review to be considered complete. Optional items are recommended but do not block completion.

---

## Required Items

- [ ] **Minimum review criteria applied** — Were at least 3 review criteria (completeness, consistency, clarity, actionability) applied during the review?
  - Criterion: the review report references at least 3 distinct evaluation dimensions.

- [ ] **Critical issues clearly described** — Do all critical issues have a clear description with specific location references?
  - Criterion: each critical issue has a non-vague description and points to a specific section or line in the artifact.

- [ ] **Recommendations are actionable** — Does every identified issue include a concrete recommendation for resolution?
  - Criterion: each issue row in the findings table has a non-empty recommendation that describes a specific action to take.

- [ ] **Verdict is justified** — Is the verdict (APPROVED/NEEDS_REVISION/REJECTED) supported by the evidence presented in the review?
  - Criterion: the verdict logically follows from the issues found. APPROVED means no critical/major issues. NEEDS_REVISION means major issues exist. REJECTED means critical issues exist.

- [ ] **No subjective opinions without backing** — Are all findings supported by specific references to the artifact content?
  - Criterion: there are no statements like "this feels incomplete" or "this seems wrong" without a concrete reference to what is incomplete or wrong.

- [ ] **Harness evidence checked when applicable** — If the reviewed artifact is an implementation artifact, did the review verify its contract and sensor evidence?
  - Criterion: the report references contract ID/path, risk level, required sensor status, and evaluator routing, or explicitly states why harness review is not applicable.

---

## Optional Items (recommended)

- [ ] **Strengths acknowledged** — Does the review identify at least one strength or positive aspect of the artifact?
  - Criterion: the strengths section is not empty and references specific elements done well.

- [ ] **Cross-artifact consistency checked** — If other artifacts exist, was consistency between them verified?
  - Criterion: the review mentions whether the artifact aligns with previously created artifacts.

- [ ] **Required actions prioritized** — If there are required actions, are they listed in priority order?
  - Criterion: actions are ordered from most critical to least critical.

---

## Validation Result

- **All required items approved?** -> Review is complete. Save the report and update state.
- **Any required item failed?** -> Revise the review report to address the gap before saving.
- **Optional items failed?** -> Note for improvement but do not block the review from being saved.
