# Harness Contract: HC-20260413-npx-init-package-template

| Field | Value |
| --- | --- |
| Project | overharness-dev |
| Contract | HC-20260413-npx-init-package-template |
| Date | 2026-04-13 |
| Builder | howard |
| Evaluator | amy |
| Risk | high |
| Source Spec | User request: create a test project and use OverHarness via npx |
| Source Design | `package.json`, `scripts/check-package-files.mjs`, `bin/overharness.mjs` |
| Source Review | `.overharness/artifacts/review/npx-init-package-template-review.md` |
| Status | blocked-on-npm-auth |

## Work Unit

Fix the published package so `npx overharness@latest init` can scaffold a fresh
project from the npm tarball.

## Scope

### In Scope

- Include `.overharness/overharness.yaml` in the package tarball.
- Add a package contents check that fails when required scaffold templates are
  missing from the tarball.
- Make fresh-project validation target generated command files instead of
  package-development files that only exist in this repository.
- Avoid feedforward errors for future pending step artifacts that have not been
  produced yet.
- Copy agent entrypoint docs into fresh projects when those docs do not already
  exist.
- Bump and publish a patch version.
- Create a disposable test project with `npx overharness@latest init`.
- Run `status`, `doctor`, and `validate` from that test project via `npx`.

### Out of Scope

- Reworking the full scaffold layout.
- Changing project track semantics.
- Removing accepted baseline findings.

## Must-Haves

### MH-01 - Tarball contains init config template

**Observable truth:** package dry-run includes `.overharness/overharness.yaml`.

**Verification:**
- `npm run pack:check`

---

### MH-02 - Published npx init works in a fresh directory

**Observable truth:** `npx overharness@latest init --type feature-work --name overharness-npx-test --yes` creates `.overharness/overharness.yaml` and `.overharness/state.json`.

**Verification:**
- Run the command in a disposable test directory.
- Check for the generated files.

---

### MH-03 - Fresh project commands work through npx

**Observable truth:** `status`, `doctor`, and `validate` pass from the fresh
test project when invoked through `npx overharness@latest`.

**Verification:**
- `npx --yes overharness@latest status`
- `npx --yes overharness@latest doctor`
- `npx --yes overharness@latest validate`

## Sensors

### Required

- **package-test**: `npm run test`
- **package-pack-check**: `npm run pack:check`
- **publish-dry-run**: `npm publish --dry-run --access public`
- **test-project-npx-init**: create a disposable test project and run `npx --yes overharness@latest init --type feature-work --name overharness-npx-test --yes`
- **test-project-npx-status**: run `npx --yes overharness@latest status` in the disposable test project
- **test-project-npx-doctor**: run `npx --yes overharness@latest doctor` in the disposable test project
- **test-project-npx-validate**: run `npx --yes overharness@latest validate` in the disposable test project

## Risk and Routing

**Risk level:** high

**Why:** The published CLI install path is currently broken for fresh users.

**Amy review:** Required.

**Human approval:** Captured by user request to use the package via npx.

## Exit Criteria

- [x] All required must-haves are satisfied locally with the packaged tarball
- [x] Required sensors pass or blockers are documented
- [ ] Patch version is published to npm
- [x] Amy review is recorded

## Current Blocker

The local package tarball for `overharness@0.1.1` fixes the `npx init` failure
and passes the disposable-project smoke test. Publishing `0.1.1` to npm is
blocked because the current token is not accepted for this package update.

The next required action is to publish with an authenticated npm session using a
valid OTP or a granular token with publish rights for `overharness`.
