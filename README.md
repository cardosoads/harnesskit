# OverHarness

OverHarness is a Harness-first workflow scaffold for agentic software projects.
It gives a project a visible process, durable artifacts, verifiable contracts,
and feedback sensors so users can see where they are and what should happen
next.

## Install In A Project

```bash
npx overharness init
```

For scripted setup:

```bash
npx overharness init --type feature-work --name my-project
npx overharness init --type existing-system --name legacy-app
npx overharness init --type new-product --name new-app
```

For non-interactive defaults:

```bash
npx overharness init --yes --name my-project
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
overharness status
overharness next
overharness doctor
overharness validate
overharness contract "describe the work unit"
```

`overharness status` explains the current phase, progress, active Harness
contracts, and next pending step. `overharness next` recommends the next action.

For non-trivial implementation work, use the Harness loop:

```text
Sheldon -> Leslie contract -> Howard implementation -> sensors -> Amy review
```

## Slash Commands

When using an agent environment that reads `.claude/commands/`, the scaffold
adds:

- `/overharness-status`
- `/overharness-next`
- `/overharness-doctor`
- `/overharness-contract`

## Package Checks

```bash
npm test
npm run pack:check
```

`pack:check` should not include local development artifacts, completed
contracts, evaluations, or Python cache files.
