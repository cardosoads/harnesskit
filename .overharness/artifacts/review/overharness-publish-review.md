# Amy Review: OverHarness Publish Prep

Date: 2026-04-13
Contract: `.overharness/harness/contracts/active/HC-20260413-overharness-publish.md`
Verdict: approved for GitHub push; npm publish blocked by authentication

## Scope Reviewed

- `package.json`
- `package-lock.json`
- `README.md`
- `bin/overharness.mjs`
- `.claude/commands/overharness-*.md`
- `.overharness/scripts/validate.sh`
- `.overharness/harness/sensors.yaml`
- `.overharness/scripts/harness_doctor.py`

## Findings

No blocking code/package findings for GitHub push.

The public package name is now `overharness`, with `overharness` as the primary
CLI binary. The old `overharness` bin remains as a compatibility alias pointing to
the same CLI entrypoint.

The main CLI file is now `bin/overharness.mjs`. User-facing README commands,
CLI help, generated slash command names, and validation checks use the
OverHarness name. The internal `.overharness/` directory remains unchanged for
compatibility.

`ajv-cli` remains pinned to `5.0.0`. The known `npm audit` findings are still
accepted as a temporary package-choice risk until the upstream dependency chain
is fixed or the validator implementation is replaced.

## Publish State

`npm view overharness` returned 404, so the package name appears available on
the public npm registry.

`npm publish --dry-run --access public` passed for `overharness@0.1.0` and no
longer reports the prior `bin` autocorrection warning.

Real npm publish is blocked in this environment. `npm whoami` returns
`E401 Unauthorized`, and the real `npm publish --access public` attempt returns
`E404 Not Found - PUT https://registry.npmjs.org/overharness`, which indicates
the current npm session does not have permission or authentication sufficient to
create/publish `overharness@0.1.0`.

The next npm step is authentication on this machine with an npm account that can
publish the package, followed by `npm publish --access public`.

## GitHub State

The GitHub remote is configured as:

```text
origin git@github.com:cardosoads/overharness.git
```

`git ls-remote git@github.com:cardosoads/overharness.git HEAD` exits
successfully and returns no HEAD, consistent with an empty remote repository.

## Sensor Evidence

- `node --check bin/overharness.mjs` passed.
- `node bin/overharness.mjs --help` passed and prints OverHarness commands.
- `node bin/overharness.mjs validate` passed: 97 checked, 97 passed.
- `npm run test` passed.
- `bash .overharness/scripts/harness-doctor.sh` passed with 0 errors and 0
  warnings after the sensor id rename.
- `npm run pack:check` passed for `overharness@0.1.0`.
- `npm publish --dry-run --access public` passed for `overharness@0.1.0`.
- Real `npm publish --access public` was attempted and blocked by npm registry
  auth/permission (`E404 Not Found - PUT .../overharness`).
- Temporary init test generated `.claude/commands/overharness-*.md` and
  reported the expected next step.
- `git diff --check` passed.

## Decision

Approved to commit and push to GitHub. npm publish should resume after npm auth
is configured.
