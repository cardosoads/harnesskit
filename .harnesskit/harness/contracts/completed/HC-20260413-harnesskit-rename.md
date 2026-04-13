# Harness Contract: HC-20260413-harnesskit-rename

| Field | Value |
| --- | --- |
| Project | harnesskit-dev |
| Contract | HC-20260413-harnesskit-rename |
| Date | 2026-04-13 |
| Builder | howard |
| Evaluator | amy |
| Risk | high |
| Source Spec | User request: rename the project again to Harnesskit |
| Source Design | package metadata, CLI, scaffold paths, command docs |
| Status | completed |

## Work Unit

Rename the product, CLI, scaffold directory, config file, package metadata, and
user-facing docs to Harnesskit. Publishable npm package name is
`@cardosoads/harnesskit` because the unscoped package name is already owned by
another maintainer.

## Scope

### In Scope

- Use `Harnesskit` for product-facing text.
- Use `harnesskit` for CLI command, script names, filenames, and generated
  slash-command names.
- Use `.harnesskit/` as the scaffold directory and `harnesskit.yaml` as the
  config file.
- Publish package metadata as `@cardosoads/harnesskit`.
- Update validation, package checks, docs, harness artifacts, contracts, and
  generated project scaffolding to use the new name.
- Verify `npx @cardosoads/harnesskit@latest ...` after publish.

### Out of Scope

- Taking over or publishing the already-owned unscoped npm package.
- Rewriting git history.
- Deleting the previously published npm package.

## Assumptions

- The previous package can remain on npm as historical distribution, but the
  current codebase should move forward with the new package name.
- The GitHub repository may need to be created or renamed separately if the
  target remote does not yet exist.
- Breaking compatibility with the previous CLI name is acceptable for this
  rename.

## Expected Files or Areas

- `package.json` and `package-lock.json`.
- `bin/`.
- `.claude/commands/`.
- `.harnesskit/`.
- `README.md`, `AGENTS.md`, and `CLAUDE.md`.
- `scripts/check-package-files.mjs`.

## Must-Haves

### MH-01 - Package and CLI use Harnesskit

**Observable truth:** `package.json` is named `@cardosoads/harnesskit`, exposes
the `harnesskit` bin, and has no previous package-name command aliases.

**Verification:**

- Static review of `package.json`.
- `node bin/harnesskit.mjs --help`.

**Failure mode this catches:** Users install one name but receive commands or
docs for another.

---

### MH-02 - Scaffold uses `.harnesskit`

**Observable truth:** New projects initialize `.harnesskit/` and
`.harnesskit/harnesskit.yaml`, not the prior scaffold directory or config file.

**Verification:**

- Initialize a disposable project from a local tarball.
- Check for `.harnesskit/harnesskit.yaml`.

**Failure mode this catches:** The rename only changes npm metadata while the
generated project keeps the old filesystem contract.

---

### MH-03 - User-facing docs and commands use Harnesskit

**Observable truth:** `README.md`, `AGENTS.md`, `CLAUDE.md`, and
`.claude/commands/` show `npx @cardosoads/harnesskit@latest ...` and
`/harnesskit-*` commands.

**Verification:**

- Static review.
- Search current source for the previous product token after the rename.

**Failure mode this catches:** Codex or Claude users follow stale commands.

---

## Sensors

### Required

- **cli-check**: `node --check bin/harnesskit.mjs`.
- **cli-help**: `node bin/harnesskit.mjs --help`.
- **package-test**: `npm run test`.
- **package-pack-check**: `npm run pack:check`.
- **publish-dry-run**: `npm publish --dry-run --access public`.
- **local-npx-flow**: initialize a disposable project from a local tarball and
  run `harnesskit codex`, `status`, `doctor`, and `validate`.
- **name-scan**: search tracked current source for the previous product token,
  excluding third-party dependencies and git internals.

### Recommended

- **registry-npx-flow**: after publish, initialize a disposable project via
  `npx @cardosoads/harnesskit@latest` and run `codex`, `status`, `doctor`, and
  `validate`.

### Feedback Gaps

- GitHub repository rename or creation may require a separate authenticated
  operation if the target repository does not exist.

## Risk and Routing

**Risk level:** high

**Why:** This intentionally changes the public npm package name, CLI name,
generated filesystem paths, docs, and package contents.

**Amy review:** Required after all sensors.

**Human approval:** Captured by the user's confirmation to use
`@cardosoads/harnesskit`.

## Exit Criteria

- [x] All required must-haves are satisfied.
- [x] Required sensors pass or blockers are documented.
- [x] New package is published or publishing blocker is documented.
- [x] Amy review is recorded.
- [x] Contract moves to completed.

## Sensor Evidence

- `node --check bin/harnesskit.mjs` - passed.
- `node bin/harnesskit.mjs --help` - passed and prints Harnesskit commands.
- `node bin/harnesskit.mjs status` - passed against `.harnesskit/`.
- `node bin/harnesskit.mjs codex` - passed and prints
  `npx @cardosoads/harnesskit@latest ...` commands.
- `npm run test` - passed; validation checked 94 items and selftest ran 5
  tests.
- `npm run pack:check` - passed; dry-run package includes 136 files.
- `npm publish --dry-run --access public` - passed for
  `@cardosoads/harnesskit@0.1.3`.
- Local tarball `npx --package /tmp/cardosoads-harnesskit-0.1.3.tgz
  harnesskit ...` flow - passed for init, codex, status, doctor, and validate.
- Name scan for the previous product token and previous scaffold path returned
  no matches outside git internals and third-party dependencies.
- `npm publish --access public` - published `@cardosoads/harnesskit@0.1.3`.
- `npm view @cardosoads/harnesskit name version dist-tags.latest --json` -
  confirmed `0.1.3` as latest after registry propagation.
- Registry `npx @cardosoads/harnesskit@latest` flow - passed for init, codex,
  status, doctor, and validate.
- GitHub repository `https://github.com/cardosoads/harnesskit` was created.

## Next Handoff

Closed after Amy review. Next operational step is commit and push to the new
Harnesskit repository.
