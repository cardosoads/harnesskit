# Design Audit: {{project_name}}

| Field    | Value                    |
|----------|--------------------------|
| Project  | {{project_name}}         |
| Date     | {{date}}                 |
| Version  | {{version}}              |
| Agent    | emily                    |
| Phase    | Design (Brownfield)      |

---

## Current Design State

### Colors in Use
{{colors_audit}}

### Typography
{{typography_audit}}

### Spacing Patterns
{{spacing_audit}}

### Component Inventory
{{component_inventory}}

### CSS Approach
{{css_approach}}

---

## Gaps & Inconsistencies

{{#each gaps}}
### {{category}}
- **Finding:** {{finding}}
- **Impact:** {{impact}}
- **Severity:** {{severity}}
{{/each}}

---

## Accessibility Assessment

{{accessibility_audit}}

---

## Proposed Design Tokens

### Token System
{{proposed_tokens}}

### Migration Strategy

> 💡 **Tip:** Define a gradual migration path so existing styles are replaced incrementally, not all at once.

{{migration_strategy}}

---

## Improvement Plan

| Priority | Change | Impact | Effort | Affected Files |
|----------|--------|--------|--------|----------------|
{{#each improvements}}
| {{priority}} | {{description}} | {{impact}} | {{effort}} | {{files}} |
{{/each}}

---

## Next Steps

> 📌 **Note:** Section automatically filled by the system.

- [ ] Design audit reviewed and approved by the user
- [ ] Handoff created for Howard (implementation)
- [ ] State.json updated with status `completed`
