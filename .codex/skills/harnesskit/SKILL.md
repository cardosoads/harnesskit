---
name: harnesskit
description: Use when working in a project that has `.harnesskit`, when the user mentions Harnesskit, Harness contracts, Sheldon, Leslie, Howard, Amy, feedforward, feedback, sensors, project status, next Harness step, feature-work, new-product, or existing-system. This skill makes Harnesskit an internal Codex workflow rather than a shell-only command flow.
---

# Harnesskit

Use this skill to run the Harnesskit workflow inside Codex. The CLI remains the
sensor runner, but the workflow decisions should happen in the agent, not as a
set of commands the user has to remember.

## Start

1. If `.harnesskit/` is missing, tell the user to initialize the project with:
   `npx @cardosoads/harnesskit@latest init --type feature-work --name <project-name>`.
2. Read `AGENTS.md` if present.
3. Read `.harnesskit/harnesskit.yaml`, `.harnesskit/state.json`, and
   `.harnesskit/core/agents/sheldon.agent.yaml`.
4. Follow Sheldon first. Use `state.json` to determine the current phase,
   then load the responsible agent file from `.harnesskit/core/agents/`.

## Work Loop

For non-trivial implementation work, use this route:

```text
Sheldon -> Leslie contract -> Howard implementation -> sensors -> Amy review
```

- Sheldon decides the next phase and responsible agent.
- Leslie defines or completes the Harness contract before implementation.
- Howard implements within the contract scope.
- Sensors verify feedforward and feedback conditions.
- Amy reviews medium, high, or critical risk work before the contract is closed.

## Codex Behavior

- Do not ask the user to run `npx` just to know where the project is. Read the
  Harnesskit files and use the CLI yourself when a sensor or status check is
  useful.
- Use `npx @cardosoads/harnesskit@latest status` and
  `npx @cardosoads/harnesskit@latest next` as supporting signals, not as a
  replacement for agent routing.
- If there is no active contract and the requested work is implementation,
  create one with `npx @cardosoads/harnesskit@latest contract "<work unit>"`
  or write it from `.harnesskit/harness/templates/contract-template.md`.
- Make must-haves observable and sensors executable. If a spec, contract field,
  test, or sensor is missing, stop and make that gap explicit before coding.
- Record review artifacts under `.harnesskit/artifacts/review/` and complete
  contracts under `.harnesskit/harness/contracts/completed/`.

## Useful User Phrases

Treat these as Harnesskit triggers:

- "Use Harnesskit"
- "Harnesskit status"
- "What's next in Harnesskit?"
- "Create a Harness contract"
- "Implement this feature with Harnesskit"
- "Run the sensors"
- "Ask Amy to review"

## Required Sensors

Use the relevant subset for the change:

```bash
npx @cardosoads/harnesskit@latest status
npx @cardosoads/harnesskit@latest next
npx @cardosoads/harnesskit@latest doctor
npx @cardosoads/harnesskit@latest validate
```

For Harnesskit itself, also run:

```bash
npm test
npm run pack:check
```
