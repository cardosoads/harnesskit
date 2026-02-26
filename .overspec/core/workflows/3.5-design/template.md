# Design System: {{project_name}}

| Field    | Value                    |
|----------|--------------------------|
| Project  | {{project_name}}         |
| Date     | {{date}}                 |
| Version  | {{version}}              |
| Agent    | emily                    |
| Phase    | Design (Greenfield)      |

---

## Art Direction

**Direction:** {{direction_name}}

**Rationale:** {{direction_rationale}}

**Signature Motifs:**
{{#each motifs}}
{{number}}. {{description}}
{{/each}}

**Memorability Hook:** {{memorability_hook}}

---

## Design Tokens

### Colors
{{#each colors}}
- `{{variable}}`: {{value}} — {{purpose}}
{{/each}}

### Typography
{{typography_spec}}

### Spacing Scale
{{spacing_spec}}

### Effects
{{effects_spec}}

---

## Atomic Design Hierarchy

### Atoms
{{atoms}}

### Molecules
{{molecules}}

### Organisms
{{organisms}}

### Templates
{{templates}}

### Pages
{{pages}}

---

## Component States

| Component | Hover | Active | Focus | Disabled | Loading | Empty |
|-----------|-------|--------|-------|----------|---------|-------|
{{#each components}}
| {{name}} | {{hover}} | {{active}} | {{focus}} | {{disabled}} | {{loading}} | {{empty}} |
{{/each}}

---

## Motion Specification

{{motion_spec}}

> 💡 **Tip:** Always specify `prefers-reduced-motion` behavior for accessibility compliance.

**prefers-reduced-motion behavior:** {{reduced_motion}}

---

## Accessibility

{{accessibility_spec}}

---

## Production Code Examples

{{code_examples}}

---

## Next Steps

> 📌 **Note:** Section automatically filled by the system.

- [ ] Design system reviewed and approved by the user
- [ ] Handoff created for Howard (implementation)
- [ ] State.json updated with status `completed`
