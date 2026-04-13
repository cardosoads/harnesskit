# OverHarness

OverHarness is a Harness-first workflow scaffold for agentic software projects.
It gives a project a visible process, durable artifacts, verifiable contracts,
and feedback sensors so users can see where they are and what should happen
next.

## Install In A Project

```bash
npx overharness@latest init
```

For scripted setup:

```bash
npx overharness@latest init --type feature-work --name my-project
npx overharness@latest init --type existing-system --name legacy-app
npx overharness@latest init --type new-product --name new-app
```

For non-interactive defaults:

```bash
npx overharness@latest init --yes --name my-project
```

## Project Tracks

| User-facing name | Internal ID | Use when |
| --- | --- | --- |
| `new-product` | `greenfield` | You are starting a project from zero. |
| `existing-system` | `brownfield` | You are improving, refactoring, or analyzing an existing project. |
| `feature-work` | `new-features` | You are adding a feature to an existing project. |

Internal IDs are kept for compatibility with existing OverHarness workflows.

## Daily Commands

```bash
npx overharness@latest status
npx overharness@latest next
npx overharness@latest codex
npx overharness@latest doctor
npx overharness@latest validate
npx overharness@latest contract "describe the work unit"
```

`overharness status` explains the current phase, progress, active Harness
contracts, and next pending step. `overharness next` recommends the next action.
`overharness codex` prints a Codex-ready route with shell commands and the
prompt to give the agent.

For non-trivial implementation work, use the Harness loop:

```text
Sheldon -> Leslie contract -> Howard implementation -> sensors -> Amy review
```

## Slash Commands

Claude Code slash commands live in `.claude/commands/`. When using an agent
environment that reads those files, the scaffold adds:

- `/overharness-status`
- `/overharness-next`
- `/overharness-doctor`
- `/overharness-contract`

Codex does not use those Claude Code slash commands. In Codex, tell the agent to
read `AGENTS.md`, then run the shell flow:

```bash
npx overharness@latest codex
```

OverHarness agents are instruction files in `.overharness/core/agents/`; they
are not separate local processes that Codex has to execute.

## Package Checks

```bash
npm test
npm run pack:check
```

`pack:check` should not include local development artifacts, completed
contracts, evaluations, or Python cache files.
