# Amy Review: Harnesskit Publish Prep

Date: 2026-04-13
Contract: `.harnesskit/harness/contracts/completed/HC-20260413-harnesskit-publish.md`
Verdict: approved; GitHub push and npm publish complete

## Scope Reviewed

- `package.json`
- `package-lock.json`
- `README.md`
- `bin/harnesskit.mjs`
- `.claude/commands/harnesskit-*.md`
- `.harnesskit/scripts/validate.sh`
- `.harnesskit/harness/sensors.yaml`
- `.harnesskit/scripts/harness_doctor.py`

## Findings

No blocking code/package findings for GitHub push.

The public package name is now `harnesskit`, with `harnesskit` as the only CLI
binary.

The main CLI file is now `bin/harnesskit.mjs`. User-facing README commands,
CLI help, generated slash command names, and validation checks use the
Harnesskit name. The internal project structure uses `.harnesskit/`.

`ajv-cli` remains pinned to `5.0.0`. The known `npm audit` findings are still
accepted as a temporary package-choice risk until the upstream dependency chain
is fixed or the validator implementation is replaced.

## Publish State

`npm view @cardosoads/harnesskit` returned 404, so the package name appears available on
the public npm registry.

`npm publish --dry-run --access public` passed for `harnesskit@0.1.0` and no
longer reports the prior `bin` autocorrection warning.

Real npm publish completed after authentication was restored and a granular npm
token was supplied via a temporary user config outside the repository.

Registry confirmation:

```json
{
  "version": "0.1.0",
  "dist-tags.latest": "0.1.0"
}
```

## GitHub State

The GitHub remote is configured as:

```text
origin git@github.com:cardosoads/harnesskit.git
```

`git ls-remote git@github.com:cardosoads/harnesskit.git HEAD` exits
successfully and returns no HEAD, consistent with an empty remote repository.

## Sensor Evidence

- `node --check bin/harnesskit.mjs` passed.
- `node bin/harnesskit.mjs --help` passed and prints Harnesskit commands.
- `node bin/harnesskit.mjs validate` passed: 97 checked, 97 passed.
- `npm run test` passed.
- `bash .harnesskit/scripts/harness-doctor.sh` passed with 0 errors and 0
  warnings after the sensor id rename.
- `npm run pack:check` passed for `harnesskit@0.1.0`.
- `npm publish --dry-run --access public` passed for `harnesskit@0.1.0`.
- Real `npm publish --access public` completed for `harnesskit@0.1.0`.
- Temporary init test generated `.claude/commands/harnesskit-*.md` and
  reported the expected next step.
- `git diff --check` passed.

## Decision

Approved and complete.
