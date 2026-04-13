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

> 💡 **Tip:** Document any deviations from the architecture plan and the rationale behind them.

**Deviations from plan:** {{deviations}}

---
{{/each}}

## Verification Results

{{verification_results}}

---

## Harness Contract

| Field | Value |
|-------|-------|
| Contract ID | {{harness_contract_id}} |
| Contract Path | `{{harness_contract_path}}` |
| Risk Level | {{harness_risk_level}} |
| Evaluator Required | {{harness_evaluator_required}} |
| Evaluation Path | `{{harness_evaluation_path}}` |

**Must-haves covered:**

{{#each harness_must_have_results}}
- [ ] {{id}} — {{status}} — {{evidence}}
{{/each}}

**Deviations:**

{{#each harness_deviations}}
- {{this}}
{{/each}}

---

## Harness Sensor Evidence

{{#each harness_sensors}}
### {{id}} — {{status}}

**Command:** `{{command}}`

**Required:** {{required}}

**Exit status:** {{exit_status}}

**Output summary:** {{output_summary}}

---
{{/each}}

---

## Next Steps

> 📌 **Note:** Section automatically filled by the system.

- [ ] Implementation reviewed by the user
- [ ] Harness contract created and referenced
- [ ] Required harness sensors passed or approved baseline documented
- [ ] Amy review queued if risk requires it
- [ ] Handoff created for Amy (review)
- [ ] State.json updated with status `completed`
