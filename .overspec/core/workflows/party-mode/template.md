# Party Mode Discussion Summary

| Field | Value |
|-------|-------|
| Date | {{date}} |
| Topic | {{topic}} |
| Agents | {{agents}} |
| Rounds | {{round_count}} |
| Duration | {{duration}} |

---

## Topic

{{topic_description}}

---

## Agents Involved

{{#each agents}}
- **{{name}}** ({{title}}) — {{role_in_discussion}}
{{/each}}

---

## Key Perspectives

{{#each perspectives}}
### {{agent_name}} {{agent_icon}}
{{perspective_summary}}
{{/each}}

---

## Points of Agreement

{{agreements}}

---

## Points of Disagreement

{{disagreements}}

---

## Decisions Made

{{#if decisions}}
{{decisions}}
{{else}}
_No formal decisions were made during this discussion._
{{/if}}

---

## Open Questions

{{#if open_questions}}
{{open_questions}}
{{else}}
_All questions were addressed during the discussion._
{{/if}}

---

## Impact on Project

{{#if impact}}
{{impact}}
{{else}}
_To be determined based on next steps._
{{/if}}
