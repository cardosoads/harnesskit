# Amy Review: HC-20260413-codex-npx-execution-flow

| Field | Value |
| --- | --- |
| Contract | HC-20260413-codex-npx-execution-flow |
| Date | 2026-04-13 |
| Reviewer | amy |
| Verdict | approved |

## Review Summary

The change satisfies the contract. Codex now has an explicit CLI route through
`overharness codex`, project docs explain the distinction between Codex shell
usage and Claude Code slash commands, and generated slash-command files no
longer point at development-only `node bin/overharness.mjs` paths.

## Evidence Reviewed

- `node --check bin/overharness.mjs` passed.
- `npm run test` passed; validation checked 94 items and Harness selftest ran 5
  tests.
- `npm run pack:check` passed; package dry-run included 136 files.
- `npm publish --dry-run --access public` passed for `overharness@0.1.2`.
- Disposable local tarball flow passed with `overharness init`, `codex`,
  `status`, `doctor`, and `validate`.
- `npm publish --access public` completed for `overharness@0.1.2`.
- `npm view overharness version dist-tags.latest --json` confirmed `0.1.2` as
  latest.
- Registry `npx overharness@latest` flow passed with `init`, `codex`, `status`,
  `doctor`, and `validate`.
- Static scan of generated `.claude/commands/` in disposable projects produced
  no `node bin/overharness` matches.

## Findings

No blocking findings.

## Residual Risk

Codex does not have a verified repo-local slash-command file format in this
project. The implementation intentionally avoids claiming Codex slash commands
exist and routes Codex usage through natural language plus `npx` shell commands.

## Approval

Approved for commit and push.
