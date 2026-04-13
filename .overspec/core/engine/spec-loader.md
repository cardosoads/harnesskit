# OverHarness Spec Loader

## Purpose

The Spec Loader discovers, validates, and activates domain specs. It resolves
spec dependencies, merges configurations, and makes agents/workflows available
to the orchestrator (Sheldon).

## Spec Resolution Order

Specs are discovered in the following order of precedence (later sources can
override earlier ones):

1. **Built-in**: `.overspec/specs/{name}/spec.yaml`
2. **Local**: `.overspec/custom-specs/{name}/spec.yaml`
3. **Installed**: `node_modules/@overspec-specs/{name}/spec.yaml` (future)

## Loading Process

1. Read `overspec.yaml` to determine which spec is active (`project.spec`)
2. Locate the spec directory using the resolution order above
3. Read and validate `spec.yaml` against `schemas/spec-schema.json`
4. Resolve dependencies (if spec depends on other specs, load them first)
5. Register all components (agents, workflows, tasks, templates)
6. Apply config (`extends` / `override` / `none`)
7. Update Sheldon's available agents and phase map

## Component Registration

When a spec is loaded, its components become available to the framework:

- **Agents** are added to Sheldon's known agents list
- **Workflows** are mapped to their respective phases
- **Templates** are available for artifact generation
- **Tasks** are available for execution

Each component is registered with its fully qualified ID (spec-name/component-id)
to prevent naming collisions across multiple specs.

## Multi-Spec Support

Multiple specs CAN be active simultaneously if they don't conflict:

- Agent IDs must be unique across all active specs
- Phase names can overlap (merged in order of spec loading)
- Conflicting configs resolved by `extends` / `override` / `none` setting
- If two specs define the same agent ID, the loader raises a conflict error

### Conflict Resolution

| Scenario | `extend` | `override` | `none` |
|---|---|---|---|
| Same agent ID | Error | Later spec wins | Error |
| Same phase name | Merged (both workflows available) | Later spec replaces | Isolated |
| Same template path | Error | Later spec wins | Isolated |

## Creating a Custom Spec

1. Create directory: `.overspec/custom-specs/my-spec/`
2. Create `spec.yaml` following the schema (`schemas/spec-schema.json`)
3. Add agents, tasks, workflows, templates in the spec directory
4. Validate: `overharness validate-spec my-spec`
5. Activate: set `project.spec` in `overspec.yaml`

### Minimal spec.yaml Example

```yaml
spec:
  name: my-custom-spec
  version: "1.0.0"
  description: "My custom domain spec"
  domain: "my-domain"
  author: "Your Name"

components:
  agents:
    - my-agent.agent.yaml
  workflows:
    default:
      - my-workflow/workflow.yaml
```

## Spec Validation Rules

The loader enforces these rules during validation:

- `spec.name` must be kebab-case (matching pattern `^[a-z][a-z0-9-]*$`)
- `spec.version` must be valid semver (matching pattern `^\d+\.\d+\.\d+$`)
- All referenced component files must exist on disk
- Agent IDs must not conflict with core agents (`sheldon` is reserved)
- Workflows must reference valid agents defined in the same spec or its dependencies
- If `dependencies.specs` lists other specs, those must be resolvable
- `config.extends` must be one of: `extend`, `override`, `none`

## Lifecycle Events

The loader emits events that other parts of the framework can hook into:

1. `spec:loading` — Before validation begins
2. `spec:validated` — After schema validation passes
3. `spec:dependencies-resolved` — After all dependencies are loaded
4. `spec:components-registered` — After agents/workflows/templates are registered
5. `spec:activated` — After the spec is fully active and available

## Error Handling

| Error | Cause | Resolution |
|---|---|---|
| `SPEC_NOT_FOUND` | Spec directory does not exist | Check spec name and resolution paths |
| `SCHEMA_VALIDATION_FAILED` | spec.yaml does not match schema | Fix the spec.yaml according to the schema |
| `MISSING_COMPONENT` | Referenced file does not exist | Create the missing file or remove the reference |
| `AGENT_CONFLICT` | Duplicate agent ID across specs | Rename one of the conflicting agents |
| `DEPENDENCY_NOT_FOUND` | Required spec is not available | Install or create the dependency spec |
| `VERSION_MISMATCH` | OverHarness version too old for spec | Update OverHarness to meet `overspec_min_version` |
