# Validation Checklist: Design System

---

## Required Items

- [ ] **Art direction defined** — Is there an explicit, named aesthetic direction with rationale?
  - Criterion: direction has a name, 1-2 sentence rationale, and 3 signature motifs.

- [ ] **Design tokens exist** — Are CSS custom properties defined for colors, typography, spacing?
  - Criterion: at least colors (5+), typography (2 fonts, type scale), and spacing (4+ steps).

- [ ] **Atomic hierarchy complete** — Does the design cover atoms, molecules, organisms?
  - Criterion: at least 3 atoms, 2 molecules, and 1 organism defined.

- [ ] **Component states defined** — Are interaction states documented?
  - Criterion: at least hover, focus-visible, and disabled states for interactive components.

- [ ] **Accessibility gates passed** — Are a11y requirements addressed?
  - Criterion: semantic HTML mentioned, contrast considered, keyboard nav addressed, responsive behavior defined.

---

## Optional Items (recommended)

- [ ] **Motion specification included** — Is motion behavior documented?
  - Criterion: at least one motion pattern defined with prefers-reduced-motion handling.

- [ ] **Production code examples** — Are runnable code snippets included?
  - Criterion: at least one component with production-grade HTML/CSS/JS.

- [ ] **Memorability hook identified** — Is there a distinctive design detail?
  - Criterion: at least one unique visual element explicitly called out.

---

## Validation Result

- **All required items approved?** -> Proceed to implementation.
- **Any required item failed?** -> Fix before proceeding.
