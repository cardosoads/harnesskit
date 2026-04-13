# Tech Debt Report: {{project_name}}

| Field    | Value                |
|----------|----------------------|
| Project  | {{project_name}}     |
| Date     | {{date}}             |
| Version  | {{version}}          |
| Agent    | raj                  |
| Phase    | Analysis             |

---

## Executive Summary

{{executive_summary}}

**Findings totais:** {{total_findings}}
- Critical: {{critical_count}}
- High: {{high_count}}
- Medium: {{medium_count}}
- Low: {{low_count}}

---

## Findings

{{#each findings}}
### {{id}} — {{title}}

| Field | Value |
|-------|-------|
| **Severidade** | {{severity}} |
| **Esforço** | {{effort}} |
| **Impacto** | {{impact}} |
| **Ação** | {{action}} |

**Descrição:** {{description}}

**Evidência:** {{evidence}}

**Recomendação:** {{recommendation}}

---
{{/each}}

## Summary Matrix

| ID | Finding | Severidade | Esforço | Ação |
|----|---------|------------|---------|------|
{{#each findings}}
| {{id}} | {{title}} | {{severity}} | {{effort}} | {{action}} |
{{/each}}

---

## Priorização Recomendada

> 💡 **Tip:** Group findings by action urgency. Quick Wins are low-effort, high-impact items to tackle first.

### Quick Wins (Fix Now — esforço S)
{{#each quick_wins}}
- {{id}} — {{title}}
{{/each}}

### Short-term (Fix Now — esforço M)
{{#each short_term}}
- {{id}} — {{title}}
{{/each}}

### Medium-term (Plan Fix)
{{#each medium_term}}
- {{id}} — {{title}}
{{/each}}

### Accept / Monitor
{{#each accept_monitor}}
- {{id}} — {{title}}
{{/each}}

---

## Next Steps

> 📌 **Note:** Section automatically filled by the system.

- [ ] Report reviewed and approved by the user
- [ ] Handoff created for the next phase (planning)
- [ ] State.json updated with status `completed`
