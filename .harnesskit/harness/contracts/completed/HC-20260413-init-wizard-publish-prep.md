# Harness Contract: HC-20260413-init-wizard-publish-prep

| Field | Value |
| --- | --- |
| Project | harnesskit-dev |
| Contract | HC-20260413-init-wizard-publish-prep |
| Date | 2026-04-13 |
| Builder | howard |
| Evaluator | amy |
| Risk | medium |
| Source Spec | `.harnesskit/harness/contracts/completed/HC-20260413-execution-flow-cli.md` |
| Source Design | `.harnesskit/core/engine/flow-guide.md` |
| Source Planning/Analysis | `.harnesskit/artifacts/review/execution-flow-cli-review.md` |
| Status | active |

## Work Unit

Make `harnesskit init` easier for first-time use by adding an interactive wizard
when required inputs are missing, and prepare the package for npm publishing
with user-facing README guidance and pack checks.

## Scope

### In Scope

- Add interactive prompts to `harnesskit init` for project name and track.
- Preserve non-interactive usage with `--type`, `--name`, and `--yes`.
- Add a root `README.md` for npm/install usage.
- Add npm metadata/scripts for pack checking.
- Document the wizard and publishing checklist in the flow guide.
- Register the README in validation.

### Out of Scope

- Publishing to npm.
- Adding third-party prompt dependencies.
- Renaming internal workflow directories.
- Mutating `.harnesskit/state.json` for this development project.

## Assumptions

- Node's built-in `readline/promises` is enough for the wizard.
- Non-interactive environments should still work through explicit flags or
  `--yes`.
- The package should remain dependency-free for this increment.

## Expected Files or Areas

- `bin/harnesskit.mjs` - init wizard and non-interactive behavior.
- `package.json` - npm scripts/metadata for pack checks.
- `README.md` - user-facing npm usage.
- `.harnesskit/core/engine/flow-guide.md` - wizard and publishing notes.
- `.harnesskit/scripts/validate.sh` - README required-file check.
- `.harnesskit/harness/evaluations/EV-20260413-init-wizard-publish-prep.md` -
  evaluation evidence.

## Must-Haves

### MH-01 - Explicit init remains non-interactive

**Observable truth:** `node bin/harnesskit.mjs init --type feature-work --name sample`
still initializes without prompts.

**Verification:**
- Temporary directory init test.

**Failure mode this catches:** The wizard breaks CI or scripted install paths.

---

### MH-02 - Yes mode works without TTY prompts

**Observable truth:** `node bin/harnesskit.mjs init --yes --name sample` uses a
safe default track and initializes without prompts.

**Verification:**
- Temporary directory init test.

**Failure mode this catches:** Non-interactive npx usage hangs waiting for input.

---

### MH-03 - Interactive code path exists without dependencies

**Observable truth:** `bin/harnesskit.mjs` uses Node built-ins for prompting and
does not add runtime dependencies.

**Verification:**
- Static review of `bin/harnesskit.mjs` and `package.json`.

**Failure mode this catches:** First-run usability depends on extra packages.

---

### MH-04 - npm usage is documented

**Observable truth:** `README.md` documents `npx @cardosoads/harnesskit@latest init`, track names,
and next-step commands.

**Verification:**
- Static review of `README.md`.

**Failure mode this catches:** Package installation exists but is not
self-explanatory.

---

### MH-05 - Package dry run remains clean

**Observable truth:** `npm pack --dry-run --json` excludes development
artifacts, completed contracts, evaluations, and `__pycache__`.

**Verification:**
- `npm run pack:check`
- package content grep.

**Failure mode this catches:** Publishing leaks local development history.

---

### MH-06 - Validation protects README/publish prep

**Observable truth:** `validate.sh` requires the root `README.md`.

**Verification:**
- `bash .harnesskit/scripts/validate.sh`

**Failure mode this catches:** Publishing docs can disappear silently.

---

## Sensors

### Required

- **harnesskit-validate**: `bash .harnesskit/scripts/validate.sh`
- **harness-doctor**: `bash .harnesskit/scripts/harness-doctor.sh`
- **harness-selftest**: `bash .harnesskit/scripts/harness-selftest.sh`
- **harnesskit-cli-status**: `node bin/harnesskit.mjs status`
- **harnesskit-cli-next**: `node bin/harnesskit.mjs next`
- **package-test**: `npm run test`
- **pack-check**: `npm run pack:check`

### Recommended

- **init-explicit-tempdir**: temporary directory init with `--type feature-work --name sample`.
- **init-yes-tempdir**: temporary directory init with `--yes --name sample`.

## Risk and Routing

**Risk level:** medium

**Why:** This changes the first-run path and npm package contents, but keeps
existing explicit CLI usage compatible.

**Amy review:** Required after implementation.

**Human approval:** Not required.

## Blockers and Open Questions

- No blocker for MVP.
- Follow-up decision: final npm package namespace and publish ownership.

## Exit Criteria

- [x] All required must-haves are satisfied
- [x] All required sensors passed or have documented baseline exceptions approved by the user
- [x] Deviations are documented with reason and impact
- [x] Amy reviewed the result if risk is `medium`, `high`, or `critical`
- [x] Human approval captured if risk is `critical` - not applicable

## Next Handoff

Evaluation artifact:
`.harnesskit/harness/evaluations/EV-20260413-init-wizard-publish-prep.md`

Amy review artifact:
`.harnesskit/artifacts/review/init-wizard-publish-prep-review.md`

Approved for completion and moved to
`.harnesskit/harness/contracts/completed/`.
