# Feature Implementation Report: {{project_name}}

| Field    | Value                           |
|----------|---------------------------------|
| Project  | {{project_name}}                |
| Date     | {{date}}                        |
| Version  | {{version}}                     |
| Agent    | howard                          |
| Phase    | Implementation (New Features)   |

---

## Implementation Summary

{{implementation_summary}}

**Stories implemented:** {{stories_completed}} / {{stories_total}}
**Commits:** {{commit_count}}
**Branch:** {{branch_name}}

---

## Stories Implemented

{{#each stories}}
### {{id}} — {{title}}

| Field | Value |
|-------|-------|
| **Status** | {{status}} |
| **Commit** | {{commit_hash}} |
| **Files Changed** | {{files_changed}} |

**What was built:** {{description}}

**Deviations from plan:** {{deviations}}

---
{{/each}}

## Verification Results

{{verification_results}}

---

## Next Steps

> Section automatically filled by the system.

- [ ] Implementation reviewed by the user
- [ ] Handoff created for Amy (review)
- [ ] State.json updated with status `completed`
