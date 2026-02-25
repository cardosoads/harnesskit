# OverSpec Workflow Engine

This document defines how any AI agent must process and execute an OverSpec workflow. Follow these instructions exactly.

---

## Overview

The Workflow Engine is the execution engine that transforms a `workflow.yaml` into a sequence of actions. It ensures that each step is executed in the correct order, that the output artifact is generated and validated, and that `state.json` is updated at the end.

---

## Execution Flow

```
1. Load workflow
2. Validate inputs
3. Analyze step dependencies and build wave plan
4. Process steps (sequentially or in parallel waves)
5. Generate output artifact
6. Validate with checklist
7. Save artifact
8. Update state.json
9. Create handoff
```

---

## 1. Load the Workflow

1. Locate the `workflow.yaml` in the phase directory (e.g., `core/workflows/1-discovery/workflow.yaml`)
2. Parse the YAML and extract:
   - `id`, `name`, `phase`, `agent`, `required`
   - `instructions`, `template`, `checklist` — paths relative to the workflow directory
   - `inputs` — required artifacts
   - `output` — output path and handoff_to
   - `steps` — ordered list of steps with optional `depends_on` fields
3. Resolve the relative paths to absolute paths within `.overspec/`

## 2. Validate Inputs

1. Check the `inputs` array of the workflow
2. For each input, confirm that the artifact exists at the indicated path
3. If any input is missing, **stop** and inform the user:
   - "This workflow requires artifact X which has not been generated yet."
   - Suggest which workflow generates the missing artifact
4. If `inputs` is empty, proceed (no dependencies)

## 3. Process Steps

Process the steps in the order they appear in `workflow.yaml`. For each step, check the `action` field and follow the corresponding procedure. If steps declare `depends_on` fields, use the Parallel Wave Execution system described below to optimize execution.

### action: "ask"

Objective: collect information from the user.

1. Read the `prompt` field of the step
2. Present the question to the user clearly
3. If the step is `required: false`:
   - Before asking, offer: "Would you like to answer now or prefer to skip?"
   - If the user skips, mark the step as `skipped` and move to the next one
4. Wait for the user's response
5. Validate the response:
   - Do not accept empty responses for required steps
   - If the response is too short or vague, ask for elaboration
6. Store the response associated with the step's `id`
7. Mark the step as `completed`
8. Proceed to the next step

### action: "generate"

Objective: generate the output artifact using collected responses + template.

1. Load the template file defined in the workflow (`template` field)
2. Collect all responses stored from previous steps
3. Fill in the template by replacing placeholders with responses:
   - `{{field}}` — replace with the collected value
   - `{{#if field}}...{{/if}}` — include the block if the field was filled in
   - `{{#each list}}...{{/each}}` — repeat the block for each item
4. Expand short responses into well-structured text when necessary
5. Fill in metadata automatically (date, version, agent)
6. Keep the generated artifact in memory for the validation step

### action: "checklist"

Objective: validate the generated artifact against quality criteria.

1. Load the checklist file defined in the workflow (`checklist` field)
2. For each checklist item:
   - Evaluate whether the generated artifact meets the criterion
   - Mark as approved or failed
3. If any **required** item fails:
   - Inform the user which item failed and why
   - Identify which step needs to be redone
   - Go back to the corresponding step and repeat the process
   - After correction, re-execute the "generate" step and re-validate
4. If only **optional** items fail:
   - Inform the user
   - Ask if they want to fix it now or move forward
5. When all required items pass, the artifact is approved

### action: "auto"

Objective: execute an automated decision or computation without user input.

1. Read the `description` field of the step — it explains what the agent should do automatically
2. The agent uses its own judgment, context, and available data to complete the step
3. No user interaction is required — this is a machine-driven step
4. The agent should explain its reasoning after completing the step
5. Mark the step as `completed`
6. Proceed to the next step

Use cases:
- Agent selection in Party Mode (Sheldon selects agents based on topic)
- Automated classification or analysis
- Data-driven decisions that don't need human input

### action: "party"

Objective: run an iterative multi-agent discussion loop.

1. Read the `description` field for discussion rules
2. The orchestrator (Sheldon) moderates a multi-round discussion:
   a. Present the topic to selected agents
   b. Each agent responds in character (3-5 sentences per response)
   c. Agents reference and respond to each other's points
   d. Sheldon summarizes key points after each round
   e. Ask the user: continue, follow up, or wrap up?
3. The loop continues until the user ends the discussion
4. Exit conditions: user says "exit", "done", "end party", "wrap up"
5. After exit, generate a summary artifact
6. Mark the step as `completed`

This action is only used by Party Mode workflows. It combines elements of `ask` (user interaction between rounds) and `generate` (summary at the end).

---

## 4. Save the Artifact

1. Resolve the output path: `output.path` relative to the `.overspec/` root
2. Create intermediate directories if they do not exist
3. Save the generated artifact at the path
4. Confirm to the user: "Artifact saved to [path]"

## 5. Update state.json

Follow the rules defined in `state-machine.md`:

1. Read the current `state.json`
2. Find the step corresponding to the workflow in the current phase
3. Update:
   ```json
   {
     "status": "completed",
     "artifact": "artifacts/discovery/brief.md",
     "agent": "penny",
     "completed_at": "2026-02-25T10:30:00Z"
   }
   ```
4. Check if all `required` steps in the phase are `completed`
5. If so, update the phase status to `completed`
6. Unlock the next phase if applicable (`locked` -> `unlocked`)
7. Recalculate `current_phase`
8. Save `state.json`

## 6. Create Handoff

If the workflow has `output.handoff_to` defined:

1. For each agent in the `handoff_to` array:
   - Add to the `handoffs` array in `state.json`:
     ```json
     {
       "from": "penny",
       "to": "leonard",
       "artifact": "artifacts/discovery/brief.md",
       "created_at": "2026-02-25T10:30:00Z",
       "consumed": false
     }
     ```
2. Create a descriptive file in `.overspec/handoffs/` with handoff details

---

## Parallel Wave Execution

When a phase contains multiple independent steps, they can be grouped into "waves" for parallel execution. Steps within a wave run in parallel; waves run sequentially.

### How Waves Work

1. Analyze step dependencies within a phase by reading each step's `depends_on` field
2. Group steps with no unresolved dependencies into Wave 1
3. Steps that depend on Wave 1 outputs go into Wave 2
4. Continue until all steps are assigned to waves

### Wave Configuration in workflow.yaml

Steps can declare dependencies using the `depends_on` field:

```yaml
steps:
  - id: "step-a"
    action: "ask"
    depends_on: []          # No dependencies = Wave 1

  - id: "step-b"
    action: "ask"
    depends_on: []          # No dependencies = Wave 1 (parallel with step-a)

  - id: "step-c"
    action: "generate"
    depends_on: ["step-a", "step-b"]  # Depends on both = Wave 2
```

### Wave Resolution Algorithm

1. Build a dependency graph from all steps' `depends_on` fields
2. Assign Wave 1 to all steps with empty or missing `depends_on`
3. For each remaining step, find the highest wave number among its dependencies and assign it to that wave + 1
4. Validate: check for circular dependencies. If found, halt and report the error.

### Execution Rules

- Each parallel agent gets a fresh context window (no accumulated noise from other parallel steps)
- Wave N+1 only starts after ALL steps in Wave N complete successfully
- If any step in a wave fails, the entire wave pauses and the failure is reported
- Results from each wave are collected and made available to subsequent waves
- Steps with `action: "ask"` that run in parallel should present all questions to the user at once, then collect responses before moving to the next wave
- The wave plan should be displayed to the user before execution begins:

```
Wave Plan:
  Wave 1: step-a, step-b (parallel)
  Wave 2: step-c (depends on step-a, step-b)
  Wave 3: step-d (depends on step-c)
```

### Fallback to Sequential

If no `depends_on` fields are present in the workflow, fall back to sequential execution in the order steps appear in the YAML. This maintains backward compatibility with workflows that do not use the wave system.

---

## Checkpoint System

Checkpoints allow workflows to pause execution and resume with fresh context. This prevents context rot during long-running workflows.

### Checkpoint Types

1. **checkpoint:auto** — System automatically creates a checkpoint when context usage exceeds 70%. Saves current state and resumes in a fresh agent.

2. **checkpoint:human-verify** — Pauses execution and asks the user to manually verify something (e.g., "Open the app and confirm the login page looks correct").

3. **checkpoint:decision** — Pauses execution because a decision is needed that was not anticipated in the plan.

### When Checkpoints Are Triggered

- **Auto checkpoints**: The engine monitors context window usage. When usage exceeds 70%, it triggers an auto checkpoint at the end of the current step (never mid-step). This ensures long workflows do not degrade in quality due to context overflow.
- **Human-verify checkpoints**: Defined explicitly in the workflow.yaml as a step with `action: "checkpoint:human-verify"`.
- **Decision checkpoints**: Created dynamically by the agent when it encounters a situation that requires human judgment not covered by the workflow instructions.

### Checkpoint Data Format

When a checkpoint is created, save to `state.json`:

```json
{
  "checkpoint": {
    "type": "auto|human-verify|decision",
    "created_at": "2026-02-25T10:30:00Z",
    "phase": "current_phase",
    "step": "current_step_id",
    "context": "description of what was happening when the checkpoint was created",
    "resume_instructions": "what the next agent needs to know to continue from this exact point",
    "collected_data": {
      "step_responses": {},
      "partial_artifacts": {},
      "wave_results": {}
    }
  }
}
```

### Creating a Checkpoint

1. Complete the current step (never checkpoint mid-step)
2. Collect all data gathered so far: step responses, partial artifacts, wave results
3. Write a clear `resume_instructions` that describes:
   - What has been completed
   - What step comes next
   - Any context the next agent needs that is not in the collected data
4. Save the checkpoint to `state.json`
5. Inform the user:
   - For **auto**: "Context checkpoint created. Resuming in a fresh session to maintain quality."
   - For **human-verify**: "Checkpoint: [description of what to verify]. Please confirm when ready to continue."
   - For **decision**: "Checkpoint: A decision is needed — [description of the decision]. Please provide your choice to continue."

### Resuming from a Checkpoint

1. New agent reads `state.json` and detects the `checkpoint` field
2. Loads `resume_instructions` and `collected_data`
3. Restores all step responses and partial artifacts from collected_data
4. Continues execution from the paused step (identified by `checkpoint.step`)
5. Clears the `checkpoint` field from `state.json` once the step completes successfully
6. Informs the user: "Resumed from checkpoint. Continuing from step [step_id]."

### Checkpoint and Wave Interaction

- If a checkpoint is triggered during a parallel wave, all steps in the current wave must complete before the checkpoint is saved
- The checkpoint saves the complete wave results so the next agent can start the next wave cleanly
- Auto checkpoints between waves are the cleanest resume points — prefer them when context usage is near the threshold

---

## Error Handling

### Step "ask" failed (invalid response)

- Repeat the question with more context
- Offer examples to guide the user
- Maximum 3 attempts; after that, ask if they want to skip (if optional) or rephrase the question

### Step "generate" failed

- Check if all required responses are filled in
- If responses are missing, go back to the pending steps
- Try generating again

### Step "checklist" failed (required item failed)

- Identify exactly which step needs to be redone
- Go back to the step, collect a new response
- Re-execute "generate" and "checklist"
- Do not enter an infinite loop: after 2 correction cycles, present the result to the user and ask for a decision

### Unexpected error

- Do not lose progress: save responses collected so far
- Inform the user of the problem
- Suggest continuing from where it left off in the next execution
- If available, create an auto checkpoint to preserve state

---

## Displaying Progress

During execution, keep the user informed:

- Before each step: "Step 3 of 9: Project scope"
- After each step: visual completion marker
- When using waves: show the wave plan and current wave status
- At the end: summary of what was collected and generated

Suggested format for sequential execution:

```
[1/9] Project context ................. completed
[2/9] Problem and audience ............ completed
[3/9] Target users .................... completed
[4/9] Scope ........................... in progress
[5/9] Success metrics ................. pending
[6/9] Constraints ..................... pending
[7/9] References ...................... pending
[8/9] Generate brief .................. pending
[9/9] Validate brief .................. pending
```

Suggested format for parallel wave execution:

```
Wave 1 (parallel):
  [1a] Context questions .............. completed
  [1b] Audience questions ............. completed

Wave 2 (parallel):
  [2a] Scope definition ............... in progress
  [2b] Success metrics ................ in progress

Wave 3 (sequential):
  [3a] Generate brief ................. pending
  [3b] Validate brief ................. pending
```

---

## Artifact Output Format

The final artifact must be a valid Markdown file with:

1. Level 1 heading with the artifact name
2. Metadata table (project, date, version, agent, phase)
3. Sections organized according to the template
4. Unfilled placeholders removed (do not leave `{{field}}` in the output)
5. Unfilled optional sections with an explanatory note
6. No Markdown formatting errors
