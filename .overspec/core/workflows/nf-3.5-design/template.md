# Feature UI Design: {{project_name}}

| Field    | Value                      |
|----------|----------------------------|
| Project  | {{project_name}}           |
| Date     | {{date}}                   |
| Version  | {{version}}                |
| Agent    | emily                      |
| Phase    | Design (New Features)      |

---

## Design Context

**Existing Design System:** {{has_design_system}}

{{design_context}}

---

## Art Direction

**Direction:** {{direction_name}} {{inherited_or_new}}

{{direction_details}}

---

## Design Tokens

### New / Extended Tokens
{{#each new_tokens}}
- `{{variable}}`: {{value}} — {{purpose}}
{{/each}}

### Inherited Tokens

> 📌 **Note:** Inherited tokens come from the existing design system. Only list new or overridden tokens above.

{{inherited_tokens}}

---

## Feature Components

{{#each components}}
### {{name}} ({{atomic_level}})

**Purpose:** {{purpose}}

**Variants:** {{variants}}

**States:**
| State | Description |
|-------|-------------|
{{#each states}}
| {{name}} | {{description}} |
{{/each}}

**Code:**
```{{language}}
{{code}}
```

---
{{/each}}

## Layout & Responsive

{{layout_spec}}

---

## Accessibility

{{accessibility_spec}}

---

## Integration Notes

{{integration_notes}}

---

## Next Steps

> 📌 **Note:** Section automatically filled by the system.

- [ ] Feature UI design reviewed and approved by the user
- [ ] Handoff created for Howard (implementation)
- [ ] State.json updated with status `completed`
