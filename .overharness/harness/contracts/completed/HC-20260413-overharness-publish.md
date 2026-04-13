# Harness Contract: HC-20260413-overharness-publish

| Field | Value |
| --- | --- |
| Project | overharness-dev |
| Contract | HC-20260413-overharness-publish |
| Date | 2026-04-13 |
| Builder | howard |
| Evaluator | amy |
| Risk | medium |
| Source Spec | User request: rename to OverHarness and publish to GitHub/npm |
| Source Design | `package.json`, `README.md`, `bin/` |
| Source Review | `.overharness/artifacts/review/overharness-publish-review.md` |
| Status | completed |

## Work Unit

Prepare the public product/package surface for OverHarness, use the
`.overharness/` project structure, prepare the npm package for `overharness`,
and push the repository to
`git@github.com:cardosoads/overharness.git`.

## Scope

### In Scope

- Change the npm package name to `overharness`.
- Add the `overharness` CLI binary.
- Rename the main CLI file to `bin/overharness.mjs`.
- Update user-facing README, CLI help, generated slash command names, and
  validation checks to the OverHarness name.
- Keep `ajv-cli` pinned to `5.0.0` until the upstream vulnerability is resolved.
- Add the GitHub remote and push the repository.
- Run npm publish preflight checks.

### Out of Scope

- Changing the `.overharness/` project structure further.
- Rewriting historical completed contracts or evaluations.
- Publishing to npm without an authenticated npm session.
- Changing `.overharness/state.json`.

## Must-Haves

### MH-01 - npm package is renamed

**Observable truth:** `package.json` uses `name: overharness` and exposes
`overharness` as the primary CLI binary.

**Verification:**
- Static review of `package.json`.

---

### MH-02 - CLI user-facing copy is renamed

**Observable truth:** `node bin/overharness.mjs --help` shows OverHarness and
documents `overharness` commands.

**Verification:**
- `node bin/overharness.mjs --help`

---

### MH-03 - Fresh scaffold writes OverHarness slash commands

**Observable truth:** new scaffold command files use the OverHarness name.

**Verification:**
- Static review of `bin/overharness.mjs`.
- Validation script checks the new command files.

---

### MH-04 - Validation and package checks pass

**Observable truth:** sensors pass after the rename.

**Verification:**
- `npm run test`
- `npm run pack:check`
- `npm publish --dry-run --access public`

---

### MH-05 - GitHub remote is configured

**Observable truth:** `origin` points to
`git@github.com:cardosoads/overharness.git`.

**Verification:**
- `git remote -v`

## Sensors

### Required

- **overharness-help**: `node bin/overharness.mjs --help`
- **overharness-validate**: `node bin/overharness.mjs validate`
- **harness-doctor**: `bash .overharness/scripts/harness-doctor.sh`
- **package-test**: `npm run test`
- **package-pack-check**: `npm run pack:check`
- **package-publish-dry-run**: `npm publish --dry-run --access public`
- **git-remote-check**: `git remote -v`

## Risk and Routing

**Risk level:** medium

**Why:** This changes the public package and CLI name before first publish.

**Amy review:** Required.

**Human approval:** Not required; the user explicitly requested GitHub publish.

## Exit Criteria

- [x] All required must-haves are satisfied
- [x] Required sensors pass or blockers are documented
- [x] npm publish completed
- [x] Amy review is recorded

## Next Handoff

GitHub push and npm publish are complete.

Evaluation artifact:
`.overharness/harness/evaluations/EV-20260413-overharness-publish.md`

Amy review artifact:
`.overharness/artifacts/review/overharness-publish-review.md`

npm publish completed with:

```bash
npm publish --access public
```

Registry confirmation:

```bash
npm view overharness version dist-tags.latest --json
```

```json
{
  "version": "0.1.0",
  "dist-tags.latest": "0.1.0"
}
```
