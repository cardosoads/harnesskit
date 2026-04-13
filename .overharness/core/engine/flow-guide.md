# OverHarness Execution Flow Guide

This guide defines the first user-facing execution layer for OverHarness.

## Entry Points

```bash
npx overharness init --type feature-work --name my-project
npx overharness init
npx overharness init --yes --name my-project
overharness status
overharness next
overharness doctor
overharness validate
overharness contract "describe the work unit"
```

The CLI is intentionally small. Its job is to make the process visible, point to
the next action, and keep Harness contracts in front of implementation work.

`overharness init` opens a small interactive wizard when `--type` or `--name` are
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

- `/overharness-status` - show current state and active contracts.
- `/overharness-next` - suggest the next process action.
- `/overharness-doctor` - run Harness feedforward/feedback checks.
- `/overharness-contract` - guide Leslie's contract creation workflow.

## Process Intelligence

`overharness status` and `overharness next` read:

- `.overharness/state.json`
- `.overharness/overharness.yaml`
- `.overharness/harness/contracts/active/`

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
