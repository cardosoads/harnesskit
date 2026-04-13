# OverHarness — AI Agent Orchestration Framework

You are operating inside a project powered by **OverHarness**, a framework that orchestrates specialized AI agents to build complete systems through structured phases.

## How to Start

**ALWAYS start by loading Sheldon** (the orchestrator agent).

1. Read `.overspec/core/agents/sheldon.agent.yaml` — this is Sheldon's complete definition
2. Read `.overspec/overspec.yaml` — global configuration
3. Read `.overspec/state.json` — current project state
4. Follow Sheldon's `activation` sequence exactly

Sheldon is the GPS of this project. He reads the state, determines the current phase, and directs you to the correct specialist agent. **Never skip Sheldon.**

## CLI Entrypoints

```bash
npx overharness init --type feature-work --name my-project
node bin/overharness.mjs status
node bin/overharness.mjs next
node bin/overharness.mjs doctor
node bin/overharness.mjs validate
```

User-facing track names are `new-product`, `existing-system`, and
`feature-work`. Internal IDs remain `greenfield`, `brownfield`, and
`new-features` for compatibility with existing workflows and config.

## Core Principles (Constitution)

1. **SHELDON FIRST** — Sheldon is always the entry point
2. **STATE IS TRUTH** — `state.json` is the single source of truth
3. **NO PHASE SKIP** — Phases cannot be skipped
4. **ARTIFACT DRIVEN** — Agents communicate through artifacts
5. **ASK DONT ASSUME** — When in doubt, ask the user
6. **GUIDED ALWAYS** — The user should never be lost

## Framework Structure

```
.overspec/
  overspec.yaml          — Global configuration
  state.json             — Project state (source of truth)
  core/
    constitution.md      — Non-negotiable principles
    agents/              — Agent definitions (sheldon, penny, leonard, leslie, howard, amy, raj, bernadette)
    engine/              — Workflow engine, state machine, spec loader
    workflows/           — Phase workflows with instructions, templates, checklists
  specs/                 — Domain specs (software is built-in)
  teams/                 — Team presets (fullstack, brownfield, quick)
  schemas/               — JSON schemas for validation
  artifacts/             — Generated artifacts (briefs, requirements, architecture, etc.)
  harness/               — Harness policies, sensors, contracts, evaluations, progress, drift
  handoffs/              — Agent-to-agent handoff records
```

## Agent Roster

| Agent | Role | Phases |
|-------|------|--------|
| Sheldon | GPS Orchestrator | All |
| Penny | Requirements Analyst | Discovery, Specification |
| Leonard | Software Architect | Architecture |
| Leslie | Harness Contract Designer | All |
| Howard | Developer | Implementation |
| Amy | Quality Reviewer | Review |
| Raj | Brownfield Analyst | Analysis, Planning |
| Bernadette | Spec Designer | All (on demand) |

## Key Rules

- Read `state.json` BEFORE any action — it determines what happens next
- Update `state.json` AFTER completing any step — follow `core/engine/state-machine.md`
- Execute workflows following `core/engine/workflow-engine.md`
- For non-trivial implementation work, route contract creation through Leslie using `core/workflows/harness-contract/`
- For every new OverHarness feature from 2026-04-13 onward, treat Harness as the default implementation gate: Leslie contract, Howard implementation, sensors, then Amy review when risk requires
- Save artifacts to `.overspec/artifacts/` using the templates
- Create handoffs when transitioning between agents
- Respond in the language configured in `overspec.yaml > user_preferences.response_language`
- If `response_language` is null, ask the user first (Sheldon handles this)
