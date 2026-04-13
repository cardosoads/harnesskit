# Harnesskit Execution Flow Guide

This guide defines the first user-facing execution layer for Harnesskit.

## Entry Points

```bash
npx @cardosoads/harnesskit@latest init --type feature-work --name my-project
npx @cardosoads/harnesskit@latest init
npx @cardosoads/harnesskit@latest init --yes --name my-project
npx @cardosoads/harnesskit@latest status
npx @cardosoads/harnesskit@latest next
npx @cardosoads/harnesskit@latest codex
npx @cardosoads/harnesskit@latest doctor
npx @cardosoads/harnesskit@latest validate
npx @cardosoads/harnesskit@latest contract "describe the work unit"
```

The CLI is intentionally small. Its job is to make the process visible, point to
the next action, and keep Harness contracts in front of implementation work.

`harnesskit init` opens a small interactive wizard when `--type` or `--name` are
missing in a terminal session. In non-interactive environments, pass both flags
or use `--yes` to accept the default `feature-work` track.

## User-Facing Track Names

Internal IDs remain stable for compatibility with existing workflows and
artifacts.

| User-facing name | Internal ID | Use when |
| --- | --- | --- |
| `new-product` | `greenfield` | The project starts from zero. |
| `existing-system` | `brownfield` | The project exists and needs analysis, cleanup, refactor, or improvement. |
| `feature-work` | `new-features` | The project exists and the goal is a new feature. |

Use user-facing names in installation, slash commands, and onboarding. Use
internal IDs only in config files, workflow keys, and compatibility-sensitive
paths.

## Slash Commands

The default slash commands live in `.claude/commands/`:

- `/harnesskit-status` - show current state and active contracts.
- `/harnesskit-next` - suggest the next process action.
- `/harnesskit-doctor` - run Harness feedforward/feedback checks.
- `/harnesskit-contract` - guide Leslie's contract creation workflow.

These are Claude Code slash commands. Codex should use `AGENTS.md` plus shell
commands instead:

```bash
npx @cardosoads/harnesskit@latest codex
```

`harnesskit codex` prints the current project route, the shell commands to run,
and the prompt to give Codex. It treats agents as instruction files under
`.harnesskit/core/agents/`, not as separate executable processes.

## Process Intelligence

`harnesskit status` and `harnesskit next` read:

- `.harnesskit/state.json`
- `.harnesskit/harnesskit.yaml`
- `.harnesskit/harness/contracts/active/`

The CLI does not mutate `state.json` during status or next checks.

## Harness Rule

For non-trivial work, the expected flow is:

```text
Sheldon -> Leslie contract -> Howard implementation -> sensors -> Amy review
```

Quick fixes can still use a smaller path, but any work with unclear scope,
multiple files, architecture impact, or user-visible behavior should begin with
a Harness contract.

## Publishing Checklist

Before publishing the npm package:

```bash
npm test
npm run pack:check
```

The dry-run package must include the CLI, commands, core workflows, Harness
templates, schemas, scripts, specs, teams, `README.md`, `CLAUDE.md`, and
`AGENTS.md`. It must not include local development artifacts, completed
contracts, evaluations, or `__pycache__`.
