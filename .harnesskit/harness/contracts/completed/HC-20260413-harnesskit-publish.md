# Harness Contract: HC-20260413-harnesskit-publish

| Field | Value |
| --- | --- |
| Project | harnesskit-dev |
| Contract | HC-20260413-harnesskit-publish |
| Date | 2026-04-13 |
| Builder | howard |
| Evaluator | amy |
| Risk | medium |
| Source Spec | User request: rename to Harnesskit and publish to GitHub/npm |
| Source Design | `package.json`, `README.md`, `bin/` |
| Source Review | `.harnesskit/artifacts/review/harnesskit-publish-review.md` |
| Status | completed |

## Work Unit

Prepare the public product/package surface for Harnesskit, use the
`.harnesskit/` project structure, prepare the npm package for `harnesskit`,
and push the repository to
`git@github.com:cardosoads/harnesskit.git`.

## Scope

### In Scope

- Change the npm package name to `harnesskit`.
- Add the `harnesskit` CLI binary.
- Rename the main CLI file to `bin/harnesskit.mjs`.
- Update user-facing README, CLI help, generated slash command names, and
  validation checks to the Harnesskit name.
- Keep `ajv-cli` pinned to `5.0.0` until the upstream vulnerability is resolved.
- Add the GitHub remote and push the repository.
- Run npm publish preflight checks.

### Out of Scope

- Changing the `.harnesskit/` project structure further.
- Rewriting historical completed contracts or evaluations.
- Publishing to npm without an authenticated npm session.
- Changing `.harnesskit/state.json`.

## Must-Haves

### MH-01 - npm package is renamed

**Observable truth:** `package.json` uses `name: harnesskit` and exposes
`harnesskit` as the primary CLI binary.

**Verification:**
- Static review of `package.json`.

---

### MH-02 - CLI user-facing copy is renamed

**Observable truth:** `node bin/harnesskit.mjs --help` shows Harnesskit and
documents `harnesskit` commands.

**Verification:**
- `node bin/harnesskit.mjs --help`

---

### MH-03 - Fresh scaffold writes Harnesskit slash commands

**Observable truth:** new scaffold command files use the Harnesskit name.

**Verification:**
- Static review of `bin/harnesskit.mjs`.
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
`git@github.com:cardosoads/harnesskit.git`.

**Verification:**
- `git remote -v`

## Sensors

### Required

- **harnesskit-help**: `node bin/harnesskit.mjs --help`
- **harnesskit-validate**: `node bin/harnesskit.mjs validate`
- **harness-doctor**: `bash .harnesskit/scripts/harness-doctor.sh`
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
`.harnesskit/harness/evaluations/EV-20260413-harnesskit-publish.md`

Amy review artifact:
`.harnesskit/artifacts/review/harnesskit-publish-review.md`

npm publish completed with:

```bash
npm publish --access public
```

Registry confirmation:

```bash
npm view @cardosoads/harnesskit version dist-tags.latest --json
```

```json
{
  "version": "0.1.0",
  "dist-tags.latest": "0.1.0"
}
```
