# Harnesskit

Harnesskit is a Harness-first workflow scaffold for agentic software projects.
It gives a project a visible process, durable artifacts, verifiable contracts,
and feedback sensors so users can see where they are and what should happen
next.

## Install In A Project

```bash
npx @cardosoads/harnesskit@latest init
```

For scripted setup:

```bash
npx @cardosoads/harnesskit@latest init --type feature-work --name my-project
npx @cardosoads/harnesskit@latest init --type existing-system --name legacy-app
npx @cardosoads/harnesskit@latest init --type new-product --name new-app
```

For non-interactive defaults:

```bash
npx @cardosoads/harnesskit@latest init --yes --name my-project
```

## Project Tracks

| User-facing name | Internal ID | Use when |
| --- | --- | --- |
| `new-product` | `greenfield` | You are starting a project from zero. |
| `existing-system` | `brownfield` | You are improving, refactoring, or analyzing an existing project. |
| `feature-work` | `new-features` | You are adding a feature to an existing project. |

Internal IDs are kept for compatibility with existing Harnesskit workflows.

## Daily Commands

```bash
npx @cardosoads/harnesskit@latest status
npx @cardosoads/harnesskit@latest next
npx @cardosoads/harnesskit@latest codex
npx @cardosoads/harnesskit@latest doctor
npx @cardosoads/harnesskit@latest validate
npx @cardosoads/harnesskit@latest contract "describe the work unit"
```

`harnesskit status` explains the current phase, progress, active Harness
contracts, and next pending step. `harnesskit next` recommends the next action.
`harnesskit codex` installs or repairs the project-local Codex skill at
`.codex/skills/harnesskit/SKILL.md` and prints the current route.

For non-trivial implementation work, use the Harness loop:

```text
Sheldon -> Leslie contract -> Howard implementation -> sensors -> Amy review
```

## Codex Skill

Codex should use Harnesskit as a skill, not as a list of slash commands to run
manually. After `init`, the project includes:

```text
.codex/skills/harnesskit/SKILL.md
```

Use it from Codex with natural language:

```text
Use Harnesskit to implement this feature.
Harnesskit status.
What's next in Harnesskit?
Create a Harness contract for this change.
```

For user-scoped discovery in new Codex sessions, run:

```bash
npx @cardosoads/harnesskit@latest codex --global
```

Harnesskit agents are instruction files in `.harnesskit/core/agents/`; they
are not separate local processes that Codex has to execute. The CLI remains the
sensor runner for `status`, `next`, `doctor`, `validate`, and `contract`.

## Claude Code Slash Commands

Claude Code slash commands live in `.claude/commands/`. When using an agent
environment that reads those files, the scaffold adds:

- `/harnesskit-status`
- `/harnesskit-next`
- `/harnesskit-doctor`
- `/harnesskit-contract`

## Package Checks

```bash
npm test
npm run pack:check
```

`pack:check` should not include local development artifacts, completed
contracts, evaluations, or Python cache files.
