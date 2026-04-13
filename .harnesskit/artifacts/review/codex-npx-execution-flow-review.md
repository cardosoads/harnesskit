# Amy Review: HC-20260413-codex-npx-execution-flow

| Field | Value |
| --- | --- |
| Contract | HC-20260413-codex-npx-execution-flow |
| Date | 2026-04-13 |
| Reviewer | amy |
| Verdict | approved |

## Review Summary

The change satisfies the contract. Codex now has an explicit CLI route through
`harnesskit codex`, project docs explain the distinction between Codex shell
usage and Claude Code slash commands, and generated slash-command files no
longer point at development-only `node bin/harnesskit.mjs` paths.

## Evidence Reviewed

- `node --check bin/harnesskit.mjs` passed.
- `npm run test` passed; validation checked 94 items and Harness selftest ran 5
  tests.
- `npm run pack:check` passed; package dry-run included 136 files.
- `npm publish --dry-run --access public` passed for `harnesskit@0.1.2`.
- Disposable local tarball flow passed with `harnesskit init`, `codex`,
  `status`, `doctor`, and `validate`.
- `npm publish --access public` completed for `harnesskit@0.1.2`.
- `npm view @cardosoads/harnesskit version dist-tags.latest --json` confirmed `0.1.2` as
  latest.
- Registry `npx @cardosoads/harnesskit@latest` flow passed with `init`, `codex`, `status`,
  `doctor`, and `validate`.
- Static scan of generated `.claude/commands/` in disposable projects produced
  no `node bin/harnesskit` matches.

## Findings

No blocking findings.

## Residual Risk

Codex does not have a verified repo-local slash-command file format in this
project. The implementation intentionally avoids claiming Codex slash commands
exist and routes Codex usage through natural language plus `npx` shell commands.

## Approval

Approved for commit and push.
