# Harnesskit State Machine

This document defines the rules of the Harnesskit state machine. Every agent that reads or updates `state.json` must follow these rules.

---

## Phase States

| State         | Description                                            |
|---------------|--------------------------------------------------------|
| `locked`      | Phase is blocked. Prerequisites have not been met.     |
| `unlocked`    | Phase is unblocked but not yet started.                |
| `in_progress` | At least one step in the phase has been started.       |
| `completed`   | All required steps in the phase have been completed.   |

## Step States

| State         | Description                                            |
|---------------|--------------------------------------------------------|
| `pending`     | Step is awaiting execution.                            |
| `in_progress` | Step is being executed by the agent.                   |
| `completed`   | Step finished successfully. Artifact generated.        |
| `skipped`     | Optional step that the user decided to skip.           |

---

## Phase Transition Rules

### locked -> unlocked

A phase changes from `locked` to `unlocked` when **all steps with `required: true` in the previous phase** have status `completed`.

Exception: the first phase (`discovery`) starts as `unlocked`.

### unlocked -> in_progress

A phase changes from `unlocked` to `in_progress` when the **first step** in the phase has its status changed to `in_progress`.

### in_progress -> completed

A phase changes from `in_progress` to `completed` when **all steps with `required: true`** in the phase have status `completed`.

Optional steps (`required: false`) can be `pending`, `completed`, or `skipped` — they do not block the transition.

---

## Step Transition Rules

### pending -> in_progress

The responsible agent begins executing the step.

### in_progress -> completed

The agent completes the step successfully. It must record:
- `status: "completed"`
- `artifact`: path of the generated artifact (if applicable)
- `completed_at`: ISO 8601 timestamp

### in_progress -> skipped (optional steps only)

The user decided to skip an optional step. Record:
- `status: "skipped"`
- `skipped_at`: ISO 8601 timestamp

Required steps can **never** be `skipped`.

---

## current_phase

The `current_phase` field in `state.json` must always point to the **first phase that is not `completed`**.

After updating the status of any phase, recalculate `current_phase`:

```
# Read the phase order from harnesskit.yaml based on the active project_type:
#   - greenfield:    greenfield_phases (ordered by 'order' field)
#   - brownfield:    brownfield_phases (ordered by 'order' field)
#   - new-features:  newfeatures_phases (ordered by 'order' field)

phase_list = read harnesskit.yaml > {project_type}_phases, sorted by order

for each phase in phase_list:
  if phase.status != "completed":
    current_phase = this phase
    stop
```

### Optional Phases

Some phases have `required: false` in harnesskit.yaml (e.g., `discuss`, `design`). These phases are **optional** — they can be skipped without breaking the flow.

When the orchestrator (Sheldon) encounters an optional phase:

1. **Ask the user** whether they want to execute the phase or skip it
2. If the user wants to **execute**: set the phase status to `unlocked` and proceed normally
3. If the user wants to **skip**: set the phase status to `completed` with a skip marker and advance to the next phase

```
# When transitioning to the next phase:
next_phase = next phase in phase_list

if next_phase has required: false:
  ask user: "Do you want to execute the [phase_name] phase? (optional)"
  if user says skip:
    next_phase.status = "completed"
    add skip_reason to the phase: "Skipped by user (optional phase)"
    advance to the phase after next_phase
  else:
    next_phase.status = "unlocked"
    proceed normally
```

Optional phases currently defined:
- **discuss** (greenfield, order 2.5) — Multi-agent discussion
- **design** (all tracks, order 2.5 or 3.5) — UI/UX design with Emily

---

## Handoffs

Handoffs are automatically created when:
1. A step is marked as `completed`
2. That step's workflow has `output.handoff_to` defined

The agent must:
1. Add an entry to the `handoffs` array in `state.json`:
   ```json
   {
     "from": "penny",
     "to": "leonard",
     "artifact": "artifacts/discovery/brief.md",
     "created_at": "2026-02-25T10:30:00Z",
     "consumed": false
   }
   ```
2. Create a handoff file in `.harnesskit/handoffs/` with details

The destination agent (`to`) consumes the handoff by setting `consumed: true` when it begins working.

---

## How to Read state.json

Every agent, upon activation, must:

1. Open `.harnesskit/state.json`
2. Read `current_phase` to determine the current phase
3. Read `phases[current_phase].steps` to determine the steps
4. Identify the first step with status `pending` or `in_progress`
5. Check if there are unconsumed handoffs addressed to it

---

## How to Update state.json

Upon completing a step:

1. Update the step: `status`, `artifact`, `completed_at`
2. Check if all required steps in the phase are completed
3. If so, update `phases[phase].status` to `completed`
4. Check if the next phase should be unlocked (`locked` -> `unlocked`)
5. Recalculate `current_phase`
6. Create handoffs if applicable
7. Save `state.json`

**Important:** always read `state.json` before updating to avoid overwriting changes made by another agent.

---

## Transition Examples

### Example 1: Completing the first step of discovery

**Before:**
```json
{
  "current_phase": "discovery",
  "phases": {
    "discovery": {
      "status": "in_progress",
      "steps": [
        { "id": "project-brief", "status": "in_progress", "artifact": null, "agent": "penny" },
        { "id": "requirements", "status": "pending", "artifact": null, "agent": "penny" }
      ]
    },
    "specification": { "status": "locked", "steps": [...] }
  },
  "handoffs": []
}
```

**After:**
```json
{
  "current_phase": "discovery",
  "phases": {
    "discovery": {
      "status": "in_progress",
      "steps": [
        { "id": "project-brief", "status": "completed", "artifact": "artifacts/discovery/brief.md", "agent": "penny", "completed_at": "2026-02-25T10:30:00Z" },
        { "id": "requirements", "status": "pending", "artifact": null, "agent": "penny" }
      ]
    },
    "specification": { "status": "locked", "steps": [...] }
  },
  "handoffs": [
    { "from": "penny", "to": "leonard", "artifact": "artifacts/discovery/brief.md", "created_at": "2026-02-25T10:30:00Z", "consumed": false }
  ]
}
```

The phase remains `in_progress` because `requirements` (if required) is still `pending`.

### Example 2: Completing the discovery phase and unlocking specification

**Before:**
```json
{
  "current_phase": "discovery",
  "phases": {
    "discovery": {
      "status": "in_progress",
      "steps": [
        { "id": "project-brief", "status": "completed", "artifact": "artifacts/discovery/brief.md", "agent": "penny", "completed_at": "..." },
        { "id": "requirements", "status": "completed", "artifact": "artifacts/discovery/requirements.md", "agent": "penny", "completed_at": "..." }
      ]
    },
    "specification": { "status": "locked", "steps": [...] }
  }
}
```

**After:**
```json
{
  "current_phase": "specification",
  "phases": {
    "discovery": {
      "status": "completed",
      "steps": [...]
    },
    "specification": { "status": "unlocked", "steps": [...] }
  }
}
```

`discovery` moves to `completed`, `specification` is unlocked, and `current_phase` advances.
