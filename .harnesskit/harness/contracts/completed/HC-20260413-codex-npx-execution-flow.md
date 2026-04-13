# Harness Contract: HC-20260413-codex-npx-execution-flow

| Field | Value |
| --- | --- |
| Project | harnesskit-dev |
| Contract | HC-20260413-codex-npx-execution-flow |
| Date | 2026-04-13 |
| Builder | howard |
| Evaluator | amy |
| Risk | medium |
| Source Spec | User report: Codex cannot execute agent commands; npx works in bash |
| Source Design | .harnesskit/harness/HARNESS.md |
| Source Planning/Analysis | .harnesskit/core/engine/flow-guide.md |
| Status | completed |

## Work Unit

Make the Harnesskit execution flow clear for Codex users who can run `npx`
commands in the shell but cannot rely on Claude Code slash commands or
separate executable agent processes.

## Scope

### In Scope

- Add a Codex-oriented CLI entrypoint that prints the current route, shell
  commands, and an agent prompt for using Harnesskit from Codex.
- Replace generated consumer-project command guidance that references
  development-only `node bin/harnesskit.mjs` commands with `npx
  harnesskit@latest ...` guidance.
- Update project-facing docs so the difference between Claude Code slash
  commands and Codex shell-driven use is explicit.
- Verify the packaged CLI can initialize a disposable project and print the
  Codex route through `npx`.

### Out of Scope

- Creating a real Codex slash-command subsystem, because no repo-local Codex
  slash-command interface has been verified.
- Changing the agent definitions or workflow state machine.
- Publishing to npm until the local package checks and disposable-project
  checks pass.

## Assumptions

- In Codex, Harnesskit agents should be treated as instruction files and
  routing roles, not as independently executable processes.
- `npx @cardosoads/harnesskit@latest ...` is the reliable consumer-project path after the
  package is published.
- Claude Code users can keep using `.claude/commands/` when that environment
  reads project slash commands.

## Expected Files or Areas

- `bin/harnesskit.mjs` - CLI command list, generated command text, and Codex
  route output.
- `README.md` - user-facing execution instructions for Codex and Claude Code.
- `AGENTS.md` - agent-facing guidance that consumer projects receive during
  init.
- `CLAUDE.md` - Claude-facing guidance that consumer projects receive during
  init.
- `.claude/commands/` - Claude Code slash-command guidance bundled in the
  package and generated for new projects.
- `package.json` and `package-lock.json` - version bump if this is prepared
  for npm publication.

## Must-Haves

### MH-01 - Codex route is explicit

**Observable truth:** Running `harnesskit codex` in an initialized project
prints that Codex uses Harnesskit through instruction files plus shell
commands, and includes `npx @cardosoads/harnesskit@latest status`, `next`, `doctor`, and
`validate`.

**Verification:**

- `node bin/harnesskit.mjs codex`
- Disposable-project `npx --package <tarball> harnesskit codex`

**Failure mode this catches:** Codex users are told to use slash commands or
development-only paths that are not available in their project.

---

### MH-02 - Generated project commands do not reference development-only paths

**Observable truth:** New projects initialized from the package contain
`.claude/commands/harnesskit-*.md` files that use `npx @cardosoads/harnesskit@latest ...`
or the project-local harness scripts, not `node bin/harnesskit.mjs`.

**Verification:**

- Initialize a disposable project from the packed tarball.
- `rg "node bin/harnesskit" <disposable-project>/.claude/commands` returns no
  matches.

**Failure mode this catches:** Published scaffolds keep pointing at files that
exist only in the Harnesskit development repo.

---

### MH-03 - Docs answer "where are the slash commands?"

**Observable truth:** `README.md`, `AGENTS.md`, and `CLAUDE.md` state that
Claude Code slash commands live in `.claude/commands/`, while Codex should use
natural-language instructions plus `npx @cardosoads/harnesskit@latest ...` shell commands.

**Verification:**

- Static review of `README.md`, `AGENTS.md`, and `CLAUDE.md`.

**Failure mode this catches:** The user cannot tell which commands belong to
Codex, Claude Code, or the shell.

---

## Sensors

### Required

- **node-check**: `node --check bin/harnesskit.mjs` - verifies CLI syntax.
- **package-test**: `npm run test` - verifies harness validation and selftest.
- **package-pack-check**: `npm run pack:check` - verifies required package
  files are included.
- **pack-dry-run**: `npm publish --dry-run --access public` - verifies npm
  publication shape before any real publish.
- **disposable-npx-flow**: initialize a disposable project from a local tarball
  and run `harnesskit codex`, `status`, `doctor`, and `validate`.

### Recommended

- **registry-npx-flow**: after publish, initialize a disposable project from
  `npx @cardosoads/harnesskit@latest` and run `codex`, `status`, `doctor`, and `validate`.

### Feedback Gaps

- There is no verified repo-local Codex slash-command file format. The current
  feedback loop should therefore avoid claiming Codex slash commands exist.

## Risk and Routing

**Risk level:** medium

**Why:** This changes user-visible CLI behavior, generated scaffold guidance,
and publishable package docs.

**Amy review:** Amy reviews the result after required sensors pass.

**Human approval:** Not required before implementation.

## Blockers and Open Questions

- No blocker for implementation.
- Publishing to npm may require a valid auth token or OTP, separate from local
  verification.

## Sensor Evidence

- `node --check bin/harnesskit.mjs` - passed.
- `npm run test` - passed; validation checked 94 items and selftest ran 5 tests.
- `npm run pack:check` - passed; dry-run package includes 136 files.
- `npm publish --dry-run --access public` - passed for `harnesskit@0.1.2`.
- Disposable local tarball flow - passed for init, `codex`, `status`, `doctor`,
  `validate`, and no `node bin/harnesskit` matches in generated commands.
- `npm publish --access public` - passed for `harnesskit@0.1.2`.
- `npm view @cardosoads/harnesskit version dist-tags.latest --json` - confirmed
  `0.1.2`.
- Registry `npx @cardosoads/harnesskit@latest` flow - passed for init, `codex`, `status`,
  `doctor`, `validate`, and no `node bin/harnesskit` matches in generated
  commands.

## Exit Criteria

- [x] All required must-haves are satisfied.
- [x] All required sensors passed or have documented baseline exceptions
  approved by the user.
- [x] Deviations are documented with reason and impact.
- [x] Amy reviewed the result if risk is `medium`, `high`, or `critical`.
- [x] Contract moved to `contracts/completed/` after acceptance.

## Next Handoff

Closed after Amy review. Next operational step is commit and push.
