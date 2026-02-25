# Codebase Analysis: overspec-dev

| Field    | Value                |
|----------|----------------------|
| Project  | overspec-dev         |
| Date     | 2026-02-25           |
| Version  | 1.0                  |
| Agent    | raj                  |
| Phase    | Analysis             |

---

## Project Overview

**Description:** OverSpec is an AI agent orchestration framework that coordinates specialized AI agents to build complete software systems through structured phases. It operates entirely through YAML-based agent definitions, Markdown workflows, and a JSON state machine — there is no runtime code (no JavaScript, Python, etc.). The framework is consumed by AI coding assistants (like Claude Code) that interpret the configuration files as instructions.

**Age:** Early-stage project, recently bootstrapped as a brownfield improvement project.

**Team Size:** Solo developer (Wesley Cardoso).

**Additional Context:** The project is self-referential — OverSpec is being used to improve itself. The framework draws its persona system from The Big Bang Theory characters, giving each agent a distinct personality that shapes how it communicates with users.

---

## Tech Stack

| Layer          | Technology        | Version    | Notes                                    |
|----------------|-------------------|------------|------------------------------------------|
| Language       | YAML + Markdown   | N/A        | Configuration-as-code, no runtime lang   |
| Framework      | OverSpec (self)    | 1.5.0      | Self-referential framework               |
| Database       | JSON (state.json) | N/A        | Flat-file state management               |
| ORM/ODM        | N/A               | N/A        | No database layer                        |
| Testing        | N/A               | N/A        | No automated tests — manual validation via checklists |
| Build Tool     | N/A               | N/A        | No build step — pure config files        |
| Containerization | N/A             | N/A        | Not containerized                        |
| CI/CD          | N/A               | N/A        | No CI/CD pipeline                        |
| VCS            | Git               | N/A        | Single branch (main), 1 commit          |
| Schemas        | JSON Schema       | draft-07   | Validation schemas for specs, teams, agents |

---

## Project Structure

```
overspec-dev/
├── .gitignore
├── CLAUDE.md                          # Entry point — instructs AI to load Sheldon
├── .overspec/
│   ├── overspec.yaml                  # Global configuration (project, language, specs, teams, model profiles)
│   ├── state.json                     # Single source of truth — project state machine
│   ├── core/
│   │   ├── constitution.md            # 6 non-negotiable principles
│   │   ├── agents/
│   │   │   ├── _schema.json           # JSON Schema for agent definitions
│   │   │   ├── sheldon.agent.yaml     # GPS Orchestrator (entry point)
│   │   │   ├── penny.agent.yaml       # Requirements Analyst
│   │   │   ├── leonard.agent.yaml     # Software Architect
│   │   │   ├── howard.agent.yaml      # Developer
│   │   │   ├── amy.agent.yaml         # Quality Reviewer
│   │   │   ├── raj.agent.yaml         # Brownfield Analyst
│   │   │   └── bernadette.agent.yaml  # Spec Designer
│   │   ├── engine/
│   │   │   ├── state-machine.md       # Phase/step transition rules
│   │   │   ├── workflow-engine.md     # Workflow execution engine (waves, checkpoints)
│   │   │   ├── spec-loader.md         # Spec discovery, validation, multi-spec support
│   │   │   ├── spec-designer-guide.md # Guide for Bernadette's spec design process
│   │   │   └── hooks/
│   │   │       └── context-monitor.md # Context window monitoring and auto-checkpoint
│   │   ├── tasks/                     # Empty — no task definitions yet
│   │   └── workflows/
│   │       ├── 1-discovery/           # Greenfield phase 1 (workflow, instructions, template, checklist)
│   │       ├── 2-specification/       # Greenfield phase 2
│   │       ├── 2.5-discuss/           # Greenfield optional discuss phase
│   │       ├── 3-architecture/        # Greenfield phase 3
│   │       ├── 4-implementation/      # Greenfield phase 4 (+ quick-fix-workflow.yaml)
│   │       ├── 5-review/              # Shared review phase (greenfield + brownfield)
│   │       ├── bf-1-analysis/         # Brownfield phase 1
│   │       ├── bf-2-planning/         # Brownfield phase 2
│   │       ├── bf-3-implementation/   # Brownfield phase 3
│   │       └── party-mode/            # Multi-agent discussion mode
│   ├── specs/
│   │   └── software/
│   │       └── spec.yaml              # Built-in software development spec
│   ├── teams/
│   │   ├── team-fullstack.yaml        # Full team: penny, leonard, howard, amy
│   │   ├── team-brownfield.yaml       # Brownfield team: raj, howard, amy
│   │   └── team-quick.yaml            # Quick fix team: howard only
│   ├── schemas/
│   │   ├── spec-schema.json           # JSON Schema for spec.yaml files
│   │   └── team-schema.json           # JSON Schema for team definition files
│   ├── artifacts/
│   │   ├── discovery/.gitkeep
│   │   ├── specification/.gitkeep
│   │   ├── architecture/.gitkeep
│   │   └── implementation/.gitkeep
│   └── handoffs/
│       └── .gitkeep
```

---

## Architecture Pattern

**Pattern:** Configuration-Driven Agent Orchestration (no runtime code)

**Description:** OverSpec is a pure configuration framework — there is no executable code. The entire system is composed of YAML agent definitions, Markdown instruction/template/checklist files, JSON state and schemas, and a single entry point (`CLAUDE.md`) that instructs an AI coding assistant to load and follow the framework.

The architecture follows a **state machine pattern** with:
- **Orchestrator** (Sheldon) as the single entry point and phase controller
- **Specialist agents** that execute workflows within their designated phases
- **Artifacts** as the communication mechanism between agents (no direct agent-to-agent calls)
- **Handoffs** that track artifact transitions between agents
- **State.json** as the single source of truth for all progress

```
User ─→ CLAUDE.md ─→ Sheldon (Orchestrator)
                         │
                         ├── reads state.json
                         ├── determines current phase
                         └── directs to specialist agent
                              │
                              ├── Penny (Discovery/Spec)
                              ├── Leonard (Architecture)
                              ├── Howard (Implementation)
                              ├── Amy (Review)
                              ├── Raj (Brownfield Analysis/Planning)
                              └── Bernadette (Spec Design)

Agents communicate via:
  artifacts/ ──handoffs/──→ next agent
```

---

## Key Components

| Component           | Purpose                                          | Location                          | Health         |
|---------------------|--------------------------------------------------|-----------------------------------|----------------|
| Constitution        | 6 non-negotiable framework principles            | `core/constitution.md`            | Healthy        |
| Sheldon Orchestrator| Central GPS — entry point, phase routing, menus  | `core/agents/sheldon.agent.yaml`  | Healthy        |
| State Machine       | Phase/step transition rules and handoff protocol | `core/engine/state-machine.md`    | Healthy        |
| Workflow Engine     | Execution engine (waves, checkpoints, validation)| `core/engine/workflow-engine.md`  | Healthy        |
| Spec Loader         | Spec discovery, validation, multi-spec support   | `core/engine/spec-loader.md`      | Needs Attention|
| Context Monitor     | Context window monitoring and auto-checkpoint    | `core/engine/hooks/context-monitor.md` | Needs Attention|
| Agent Definitions   | 7 agents with personas, menus, behaviors         | `core/agents/*.agent.yaml`        | Healthy        |
| Workflows           | 10 workflow directories with full artifact set   | `core/workflows/*/`               | Healthy        |
| Schemas             | JSON Schema validation for specs, teams, agents  | `schemas/`                        | Needs Attention|
| Teams               | 3 team presets (fullstack, brownfield, quick)     | `teams/`                          | Healthy        |
| Software Spec       | Built-in spec for software development           | `specs/software/spec.yaml`        | Healthy        |

**Health Legend:** Healthy | Needs Attention | Critical | Unknown

---

## Data Layer

**Database:** JSON flat file (`state.json`)

**ORM/ODM:** N/A — direct JSON read/write by AI agents

**Models/Entities:**

- **State** — Project state with current phase, phase statuses, step statuses, artifacts, handoffs (`state.json`)
- **Agent** — Agent definition with persona, phases, menu, behaviors, outputs, consumes (`core/agents/*.agent.yaml`)
- **Workflow** — Workflow definition with steps, inputs, output, handoff_to (`core/workflows/*/workflow.yaml`)
- **Spec** — Domain spec package with components, config, dependencies (`specs/*/spec.yaml`)
- **Team** — Agent grouping with purpose and party_mode config (`teams/team-*.yaml`)
- **Handoff** — Agent-to-agent artifact transition record (`handoffs/`)

**Migrations:** N/A

---

## API / Endpoints

_No API endpoints — this is a configuration framework consumed by AI coding assistants, not a server._

---

## Testing Status

**Framework:** N/A — No automated testing framework

**Coverage Estimate:** 0% automated coverage

**Types of Tests:**

- [ ] Unit tests
- [ ] Integration tests
- [ ] End-to-end tests
- [ ] Performance tests
- [ ] Security tests

**Test Health:** N/A

**Notes:** Validation is done through Markdown checklists (`checklist.md`) within each workflow. These are evaluated by the AI agent during artifact generation, not by automated test runners. This is by design for a configuration-as-code framework, but means there's no automated way to validate that agent definitions conform to schemas or that workflow references are correct.

---

## Dependencies Summary

**Total Dependencies:** 0 (no package manager, no runtime dependencies)

**Outdated:** N/A

**Security Concerns:** None identified — the framework has no runtime code, no network access, no dependency chain. Security depends entirely on the AI coding assistant's behavior.

**Notable Dependencies:**

- `JSON Schema draft-07` — Used for validation schemas (spec, team, agent)
- `Git` — Version control (single commit on main branch)

---

## Initial Observations

### Strengths

- **Extremely well-designed architecture**: The separation between orchestrator, specialist agents, state machine, and workflow engine is clean and coherent. Each component has a clear single responsibility.
- **Constitution-driven design**: The 6 principles provide a strong guiding framework that ensures consistency across all agents and workflows.
- **Rich persona system**: Each agent has a fully developed persona with identity, style, catchphrase, and principles. This makes the framework engaging and the agents distinguishable.
- **Dual-track support**: Both greenfield (6 phases) and brownfield (4 phases) workflows are fully mapped with distinct flows, agents, and artifacts.
- **Comprehensive workflow engine**: The engine supports parallel waves, checkpoints (auto, human-verify, decision), error handling, and progress display — sophisticated for a v1 framework.
- **Self-documenting**: Engine docs (state-machine.md, workflow-engine.md) are clear, with examples and transition rules that any AI agent can follow.
- **Extensibility via specs**: The spec system (with spec-loader, spec-schema, Bernadette as designer) allows the framework to be extended to non-software domains.
- **Team presets**: The team system allows different agent configurations for different project types, adding flexibility without complexity.
- **Context monitoring**: The context-monitor hook addresses a real problem (context rot in long AI conversations) with clear alert levels and checkpoint integration.
- **Party Mode**: Creative feature for multi-agent discussions that brings diverse perspectives to decision-making.

### Concerns

- **Agent schema doesn't match actual agent files**: The `_schema.json` for agents defines `phases` as an enum restricted to `["discovery", "specification", "architecture", "implementation", "review"]` — but actual agents use values like `"all"`, `"analysis"`, and `"planning"` (brownfield phases). Sheldon and Bernadette use `[all]` which isn't in the enum. This means schema validation would fail for most agents.
- **Spec schema `components.workflows` structure mismatch**: The schema defines `workflows` as a flat array of strings, but the actual `spec.yaml` uses a nested object with `greenfield` and `brownfield` keys. Schema validation would fail.
- **Agent schema doesn't cover all actual fields**: Actual agent files include `language_protocol`, `activation` (as array of objects, not strings), `behaviors`, `atomic_commits`, `deviation_rules`, `verification_protocol`, and `first_run_behavior` — none of which are in the schema. The schema's `additionalProperties: false` would reject these.
- **Empty `core/tasks/` directory**: Referenced in the structure but contains no files. The spec schema references `tasks` as a component type, but no tasks exist in the software spec or anywhere else. Unclear if this is planned or abandoned.
- **Missing `artifacts/analysis/` and `artifacts/planning/` directories**: The brownfield flow expects these directories but only greenfield artifact directories exist with `.gitkeep` files. [Fixed during this analysis]
- **State.json doesn't have a `tech-debt-audit` workflow**: The state has a `tech-debt-audit` step, but there's no separate workflow YAML for it — it's referenced in Raj's agent behavior but there's no `bf-1-analysis/tech-debt-audit/` workflow directory. It appears to share the analysis workflow.
- **No `bf-4-review/` workflow**: The brownfield flow uses the same `5-review/` as greenfield. This works but the naming is inconsistent (`bf-1-`, `bf-2-`, `bf-3-` but then `5-review`).
- **Context monitor is conceptual**: The hook describes what should happen but there's no actual hook implementation (no `.claude/settings.json` or hooks config file). It's documentation-only.
- **Model profiles not consumed**: `overspec.yaml` defines `model_profiles` with quality/balanced/budget tiers, but no agent or workflow references these profiles. The configuration exists but isn't wired into the system.
- **Spec `components.workflows` inconsistency**: The spec.yaml uses nested keys (`greenfield`, `brownfield`) while the schema expects a flat list. Also, the `templates` list in spec.yaml references paths like `discovery/template.md` but actual templates are at `core/workflows/1-discovery/template.md`.

### Opportunities

- **Align schemas with reality**: Update `_schema.json`, `spec-schema.json`, and `team-schema.json` to match the actual structure of the YAML files. This would enable real validation.
- **Wire model profiles**: Connect `model_profiles` to the agent system so that the active profile actually influences which model each agent uses. This is already configured but not consumed.
- **Implement context monitor hook**: Create the actual `.claude/settings.json` or hooks configuration to make context monitoring functional.
- **Create brownfield-specific artifact directories**: Add `artifacts/analysis/`, `artifacts/planning/`, and `artifacts/review/` to the directory structure.
- **Add tech-debt-audit workflow**: Create a dedicated `bf-1-analysis/tech-debt-audit/` workflow directory with its own instructions, template, and checklist — or explicitly document that it shares the codebase-analysis workflow.
- **Standardize brownfield review naming**: Either create `bf-4-review/` or document that `5-review/` is shared across both flows.
- **Define tasks system**: The `core/tasks/` directory and spec schema support tasks, but no tasks exist. Either implement the task system or remove it from the schema to avoid confusion.
- **Add automated validation**: Create a simple script (shell or Node) that validates all YAML/JSON files against their schemas — would catch structural issues early.

---

## Next Steps

> Section automatically filled by the system.

- [x] Analysis reviewed and approved by the user
- [ ] Handoff created for the next agent (raj — tech-debt-audit)
- [ ] State.json updated with status `completed`
