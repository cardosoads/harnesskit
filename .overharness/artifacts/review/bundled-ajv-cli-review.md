# Amy Review: Bundled ajv-cli

Date: 2026-04-13
Contract: `.overharness/harness/contracts/active/HC-20260413-bundled-ajv-cli.md`
Verdict: approved with documented dependency risk

## Scope Reviewed

- `package.json`
- `package-lock.json`
- `bin/overharness.mjs`
- `.overharness/scripts/validate.sh`
- `.overharness/harness/evaluations/EV-20260413-bundled-ajv-cli.md`

## Findings

No blocking implementation findings.

`ajv-cli@5.0.0` is now a runtime dependency, so an npm install of OverHarness
will install the validator dependency without requiring a separate global
`ajv` install.

`overharness validate` now passes the packaged validator through
`OVERHARNESS_AJV_BIN` when the package-local binary exists. Direct script usage
still works because `validate.sh` resolves validators in this order:

1. `OVERHARNESS_AJV_BIN`
2. `$PROJECT_ROOT/node_modules/.bin/ajv`
3. global `ajv`

The validation script writes temporary agent JSON to an `agent.json` filename
inside a temporary directory. This keeps `ajv-cli` from failing on extensionless
temporary files while preserving cleanup after each file.

## Dependency Risk

`npm audit --omit=dev --json` reports 2 high severity findings:

- `ajv-cli` via `fast-json-patch`
- `fast-json-patch` prototype pollution, advisory `GHSA-8gh8-hqwg-xf34`

The npm suggested fix is a semver-major downgrade to `ajv-cli@0.6.0`. That is
not applied here because the user asked to install the current npm tool, and a
downgrade could change validation behavior. Recommended follow-up: decide
whether to keep `ajv-cli`, pin/override the transitive dependency if viable, or
replace CLI-based validation with direct `ajv` library usage in a Node script.

## Sensor Evidence

- `bash .overharness/scripts/validate.sh` passed: 97 checked, 97 passed.
- `node bin/overharness.mjs validate` passed: 97 checked, 97 passed.
- `bash .overharness/scripts/harness-doctor.sh` passed with 0 errors, 0 warnings,
  and 4 accepted baseline findings.
- `npm run test` passed.
- `npm run pack:check` passed and did not include `node_modules/` or Harness
  development history outside the packaged public scaffold files.
- `git diff --check` passed.
- `harness-evaluate` approved the active contract.

## Decision

Approved for completion. The dependency audit finding is non-blocking for this
contract because it is inherent to the requested `ajv-cli` package choice and is
documented for the next hardening decision.
