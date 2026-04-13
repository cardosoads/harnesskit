# Harness Contract: HC-20260413-bundled-ajv-cli

| Field | Value |
| --- | --- |
| Project | harnesskit-dev |
| Contract | HC-20260413-bundled-ajv-cli |
| Date | 2026-04-13 |
| Builder | howard |
| Evaluator | amy |
| Risk | low |
| Source Spec | User request: install ajv-cli when Harnesskit is downloaded from npm |
| Source Design | `package.json`, `.harnesskit/scripts/validate.sh` |
| Source Review | `.harnesskit/artifacts/review/bundled-ajv-cli-review.md` |
| Status | completed |

## Work Unit

Bundle `ajv-cli` with the npm package and make Harnesskit validation use the
packaged binary when available.

## Scope

### In Scope

- Add `ajv-cli` as an npm runtime dependency.
- Let `harnesskit validate` expose the packaged `ajv` binary to `validate.sh`.
- Let `validate.sh` prefer `HARNESSKIT_AJV_BIN`, then local project `node_modules`,
  then global `ajv`.
- Keep direct `bash .harnesskit/scripts/validate.sh` working.

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

**Observable truth:** `harnesskit validate` sets `HARNESSKIT_AJV_BIN` when the
package-local `node_modules/.bin/ajv` exists.

**Verification:**
- Static review of `bin/harnesskit.mjs`.

---

### MH-03 - validate.sh can use local or global ajv

**Observable truth:** `validate.sh` checks `HARNESSKIT_AJV_BIN`,
`$PROJECT_ROOT/node_modules/.bin/ajv`, and global `ajv`.

**Verification:**
- `bash .harnesskit/scripts/validate.sh`

---

### MH-04 - Package and tests still pass

**Observable truth:** `npm run test` and `npm run pack:check` pass.

**Verification:**
- `npm run test`
- `npm run pack:check`

## Sensors

### Required

- **harnesskit-validate**: `bash .harnesskit/scripts/validate.sh`
- **harness-doctor**: `bash .harnesskit/scripts/harness-doctor.sh`
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
`.harnesskit/harness/evaluations/EV-20260413-bundled-ajv-cli.md`

Amy review artifact:
`.harnesskit/artifacts/review/bundled-ajv-cli-review.md`

Approved for completion and moved to
`.harnesskit/harness/contracts/completed/`.
