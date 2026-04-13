# Harness Contract: HC-20260413-remove-legacy-name

| Field | Value |
| --- | --- |
| Project | overharness-dev |
| Contract | HC-20260413-remove-legacy-name |
| Date | 2026-04-13 |
| Builder | howard |
| Evaluator | amy |
| Risk | high |
| Source Spec | User request: remove the legacy product token from the project |
| Source Design | `package.json`, `bin/overharness.mjs`, `.overharness/` |
| Source Review | `.overharness/artifacts/review/remove-legacy-name-review.md` |
| Status | completed |

## Work Unit

Remove the previous product token from the current project surface and package by
using only OverHarness naming for internal paths, public aliases, docs, and
distribution metadata.

## Scope

### In Scope

- Use `.overharness/` as the only harness directory name.
- Use `.overharness/overharness.yaml` as the only project config path.
- Remove legacy npm bin and script aliases.
- Use `OVERHARNESS_AJV_BIN` as the only AJV override variable.
- Update code, docs, commands, artifacts, contracts, evaluations, and templates
  to avoid the legacy token in tracked source.
- Rename the local repo directory to `overharness-dev`.
- Keep npm publish blocked until npm auth exists.

### Out of Scope

- Rewriting git history.
- Editing ignored third-party `node_modules` package contents.
- Publishing to npm without auth.

## Must-Haves

### MH-01 - No tracked current-source legacy references

**Observable truth:** case-insensitive search for the legacy token in tracked
project files, excluding `.git` and `node_modules`, returns no matches.

**Verification:**
- Run a case-insensitive source search for the legacy token, excluding `.git`
  and `node_modules`.

---

### MH-02 - CLI uses OverHarness-only paths

**Observable truth:** `node bin/overharness.mjs --help`, `status`, and
`validate` work against `.overharness/`.

**Verification:**
- `node bin/overharness.mjs --help`
- `node bin/overharness.mjs status`
- `node bin/overharness.mjs validate`

---

### MH-03 - Package exposes no legacy alias

**Observable truth:** `package.json` has only the `overharness` bin/script and
packages `.overharness` files.

**Verification:**
- Static review of `package.json`.
- `npm run pack:check`

---

### MH-04 - Sensors pass after rename

**Observable truth:** validation, doctor, tests, and npm dry-run pass.

**Verification:**
- `npm run test`
- `bash .overharness/scripts/harness-doctor.sh`
- `npm publish --dry-run --access public`

## Sensors

### Required

- **overharness-help**: `node bin/overharness.mjs --help`
- **overharness-status**: `node bin/overharness.mjs status`
- **overharness-validate**: `node bin/overharness.mjs validate`
- **harness-doctor**: `bash .overharness/scripts/harness-doctor.sh`
- **package-test**: `npm run test`
- **package-pack-check**: `npm run pack:check`
- **publish-dry-run**: `npm publish --dry-run --access public`
- **no-legacy-current-source**: case-insensitive source search for the legacy
  token, excluding `.git` and `node_modules`

## Risk and Routing

**Risk level:** high

**Why:** This intentionally breaks legacy path and CLI compatibility to satisfy
the naming directive.

**Amy review:** Required.

**Human approval:** Captured by user directive.

## Exit Criteria

- [x] All required must-haves are satisfied
- [x] Required sensors pass or blockers are documented
- [x] Amy review is recorded
