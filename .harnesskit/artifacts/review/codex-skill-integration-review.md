# Amy Review: Codex Skill Integration

| Field | Value |
| --- | --- |
| Contract | HC-20260414-codex-skill-integration |
| Reviewer | amy |
| Date | 2026-04-14 |
| Verdict | approved |

## Review Summary

Harnesskit now has a packaged Codex skill at `.codex/skills/harnesskit/SKILL.md`.
The CLI installs it during `init`, repairs it during `codex`, and supports a
user-scoped install with `codex --global`.

## Evidence Reviewed

- `node --check bin/harnesskit.mjs` passed.
- `npm test` passed: validation checked 94 items and 5 selftests passed.
- `npm run pack:check` passed: `cardosoads-harnesskit-0.1.4.tgz` includes 137 files.
- `npm publish --dry-run --access public` passed and included `.codex/skills/harnesskit/SKILL.md`.
- Temporary project smoke test passed: `init` created `.codex/skills/harnesskit/SKILL.md`.
- Temporary project repair test passed: deleting the skill and running `codex` recreated it.
- Temporary `CODEX_HOME` smoke test passed: `codex --global` installed `skills/harnesskit/SKILL.md`.
- `node bin/harnesskit.mjs doctor` passed with 0 errors, 0 warnings, and 4 accepted baseline items.
- `git diff --check` passed.
- Legacy name scan passed with no `OverHarness`, `overharness`, or `.overharness` matches outside ignored paths.

## Findings

No blocking findings.

## Residual Risk

Codex may require a new session before a newly installed user-scoped skill is
listed in the runtime skill catalog. The CLI now prints this limitation and the
`codex --global` path explicitly.
