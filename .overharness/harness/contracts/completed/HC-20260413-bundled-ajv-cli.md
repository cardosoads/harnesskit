# Harness Contract: HC-20260413-bundled-ajv-cli

| Field | Value |
| --- | --- |
| Project | overharness-dev |
| Contract | HC-20260413-bundled-ajv-cli |
| Date | 2026-04-13 |
| Builder | howard |
| Evaluator | amy |
| Risk | low |
| Source Spec | User request: install ajv-cli when OverHarness is downloaded from npm |
| Source Design | `package.json`, `.overharness/scripts/validate.sh` |
| Source Review | `.overharness/artifacts/review/bundled-ajv-cli-review.md` |
| Status | completed |

## Work Unit

Bundle `ajv-cli` with the npm package and make OverHarness validation use the
packaged binary when available.

## Scope

### In Scope

- Add `ajv-cli` as an npm runtime dependency.
- Let `overharness validate` expose the packaged `ajv` binary to `validate.sh`.
- Let `validate.sh` prefer `OVERHARNESS_AJV_BIN`, then local project `node_modules`,
  then global `ajv`.
- Keep direct `bash .overharness/scripts/validate.sh` working.

### Out of Scope

- Publishing the package.
- Changing the agent schema.
- Making `ajv-cli` a peer dependency.

## Must-Haves

### MH-01 - npm package installs ajv-cli

**Observable truth:** `package.json` lists `ajv-cli` under `dependencies`.

**Verification:**
- Static review of `package.json`.

---

### MH-02 - CLI passes packaged ajv to validation

**Observable truth:** `overharness validate` sets `OVERHARNESS_AJV_BIN` when the
package-local `node_modules/.bin/ajv` exists.

**Verification:**
- Static review of `bin/overharness.mjs`.

---

### MH-03 - validate.sh can use local or global ajv

**Observable truth:** `validate.sh` checks `OVERHARNESS_AJV_BIN`,
`$PROJECT_ROOT/node_modules/.bin/ajv`, and global `ajv`.

**Verification:**
- `bash .overharness/scripts/validate.sh`

---

### MH-04 - Package and tests still pass

**Observable truth:** `npm run test` and `npm run pack:check` pass.

**Verification:**
- `npm run test`
- `npm run pack:check`

## Sensors

### Required

- **overharness-validate**: `bash .overharness/scripts/validate.sh`
- **harness-doctor**: `bash .overharness/scripts/harness-doctor.sh`
- **package-test**: `npm run test`
- **package-pack-check**: `npm run pack:check`

## Risk and Routing

**Risk level:** low

**Why:** Dependency and validation wiring only; no workflow semantics change.

**Amy review:** Optional.

**Human approval:** Not required.

## Exit Criteria

- [x] All required must-haves are satisfied
- [x] Required sensors pass
- [x] Deviations are documented

## Next Handoff

Evaluation artifact:
`.overharness/harness/evaluations/EV-20260413-bundled-ajv-cli.md`

Amy review artifact:
`.overharness/artifacts/review/bundled-ajv-cli-review.md`

Approved for completion and moved to
`.overharness/harness/contracts/completed/`.
