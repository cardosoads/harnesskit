# Amy Review: Npx Init Package Template

| Field | Value |
| --- | --- |
| Date | 2026-04-13 |
| Reviewer | amy |
| Contract | `.overharness/harness/contracts/active/HC-20260413-npx-init-package-template.md` |
| Verdict | approved locally; npm publish blocked by auth |

## Scope Reviewed

- `package.json`
- `package-lock.json`
- `scripts/check-package-files.mjs`
- `bin/overharness.mjs`
- `.overharness/scripts/validate.sh`
- `.overharness/scripts/harness_doctor.py`

## Findings

No blocking implementation findings for the patch.

The published `0.1.0` tarball did not include `.overharness/overharness.yaml`,
which made `npx overharness@latest init` fail with:

```text
Missing packaged .overharness/overharness.yaml template.
```

The patch adds `.overharness/overharness.yaml` to the npm file list and replaces
`pack:check` with a package-contents smoke check so this class of omission is
detected before publish.

The fresh-project smoke test also found two consumer-flow issues:

- `validate` required package-development files that should not exist in a
  consumer project.
- `doctor` treated future pending step artifacts as missing required files.

Both are corrected in the patch. Fresh projects now receive `CLAUDE.md` and
`AGENTS.md` when those files do not already exist.

## Sensor Evidence

- `node --check bin/overharness.mjs` passed.
- `node --check scripts/check-package-files.mjs` passed.
- `npm run pack:check` passed and confirms the tarball includes the required
  scaffold files.
- `npm run test` passed.
- `npm publish --dry-run --access public` passed for `overharness@0.1.1`.
- Disposable test project created at
  `/Users/wesleycardoso/Wesley/Harness/overharness-npx-test`.
- `npx --yes --package /tmp/overharness-0.1.1.tgz overharness init --type feature-work --name overharness-npx-test --yes` passed.
- `npx --yes --package /tmp/overharness-0.1.1.tgz overharness status` passed.
- `npx --yes --package /tmp/overharness-0.1.1.tgz overharness doctor` passed with
  one expected baseline-content warning and one informational no-runner finding.
- `npx --yes --package /tmp/overharness-0.1.1.tgz overharness validate` passed.

## Publish State

Publishing `overharness@0.1.1` with the current token is blocked. `npm whoami`
using that token returns unauthorized, and publish returns a package access
error. Complete the publish with a valid OTP on the authenticated npm session or
with a new token that has publish rights for `overharness`.
