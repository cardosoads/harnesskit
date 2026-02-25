# Validation Checklist: Feature UI Design

---

## Required Items

- [ ] **Design context analyzed** — Was the existing design system (if any) reviewed?
  - Criterion: document states whether a design system exists and how the feature integrates.

- [ ] **Art direction defined** — Is the aesthetic direction clear (inherited or new)?
  - Criterion: direction has a name and rationale, even if inherited from existing system.

- [ ] **Components specified** — Are new components listed with Atomic Design classification?
  - Criterion: at least 1 new component defined with purpose, states, and code.

- [ ] **Integration plan clear** — Is it clear how the feature fits into existing UI?
  - Criterion: layout position, token usage (new vs inherited), and responsive behavior documented.

---

## Optional Items (recommended)

- [ ] **Design tokens documented** — Are new or extended tokens listed?
  - Criterion: any new CSS variables are documented with values and purpose.

- [ ] **Accessibility addressed** — Are a11y requirements for the feature covered?
  - Criterion: keyboard flow, ARIA roles, and contrast for new components.

- [ ] **Code examples included** — Is production-grade code provided?
  - Criterion: at least one component has runnable code.

---

## Validation Result

- **All required items approved?** -> Proceed to implementation.
- **Any required item failed?** -> Fix before proceeding.
