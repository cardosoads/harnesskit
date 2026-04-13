# Harness Evaluation: EV-20260413-remove-legacy-name

| Field | Value |
| --- | --- |
| Project | harnesskit-dev |
| Evaluation | EV-20260413-remove-legacy-name |
| Contract | HC-20260413-remove-legacy-name |
| Contract Path | `/Users/wesleycardoso/Wesley/Harness/harnesskit-dev/.harnesskit/harness/contracts/completed/HC-20260413-remove-legacy-name.md` |
| Date | 2026-04-13 |
| Evaluator | harness-evaluate |
| Risk | high |
| Verdict | APPROVED |
| Score | 1.00 |

## Contract Coverage

### MH-01 - RECORDED

**Expected truth:** No tracked current-source legacy references

**Evidence:** Sensor evidence is recorded below. Semantic verification remains with Amy when the contract risk requires evaluator review.

**Finding:** Not failed by the mechanical runner.

**Required follow-up:** Amy should review this must-have against the implementation artifact when risk routing requires it.

---

### MH-02 - RECORDED

**Expected truth:** CLI uses Harnesskit-only paths

**Evidence:** Sensor evidence is recorded below. Semantic verification remains with Amy when the contract risk requires evaluator review.

**Finding:** Not failed by the mechanical runner.

**Required follow-up:** Amy should review this must-have against the implementation artifact when risk routing requires it.

---

### MH-03 - RECORDED

**Expected truth:** Package exposes no legacy alias

**Evidence:** Sensor evidence is recorded below. Semantic verification remains with Amy when the contract risk requires evaluator review.

**Finding:** Not failed by the mechanical runner.

**Required follow-up:** Amy should review this must-have against the implementation artifact when risk routing requires it.

---

### MH-04 - RECORDED

**Expected truth:** Sensors pass after rename

**Evidence:** Sensor evidence is recorded below. Semantic verification remains with Amy when the contract risk requires evaluator review.

**Finding:** Not failed by the mechanical runner.

**Required follow-up:** Amy should review this must-have against the implementation artifact when risk routing requires it.

---

## Sensor Results

### harnesskit-validate - PASS

**Command:** `bash .harnesskit/scripts/validate.sh`

**Required:** yes

**Exit status:** 0

**Output summary:**

```text
Validating JSON files...
  ✓ state.json
  ✓ core/agents/_schema.json
  ✓ schemas/spec-schema.json
  ✓ schemas/team-schema.json

Validating YAML files...
  ✓ core/agents/amy.agent.yaml
  ✓ core/agents/bernadette.agent.yaml
  ✓ core/agents/design-specialist.agent.yaml
  ✓ core/agents/howard.agent.yaml
  ✓ core/agents/leonard.agent.yaml
  ✓ core/agents/leslie.agent.yaml
  ✓ core/agents/penny.agent.yaml
  ✓ core/agents/raj.agent.yaml
  ✓ core/agents/sheldon.agent.yaml
  ✓ core/workflows/1-discovery/requirements-workflow.yaml
  ✓ core/workflows/1-discovery/workflow.yaml
... output truncated (96 more lines)
```

**Blocks completion:** no

---

### harness-doctor - PASS

**Command:** `bash .harnesskit/scripts/harness-doctor.sh`

**Required:** yes

**Exit status:** 0

**Output summary:**

```text
Harnesskit Doctor
Errors: 0  Warnings: 0  Info: 4
Baseline accepted: 4
[BASELINE] feedforward/phase_missing_in_state: Configured phase 'design' is missing in state.json [baseline: baseline-design-phase-state, expires: 2026-05-13] (state.json)
[BASELINE] feedforward/artifact_placeholder: .harnesskit/artifacts/architecture/feature-design.md has unresolved template/TODO markers at lines 239, 303, 304, 305, 319 [baseline: baseline-feature-design-template-markers, expires: 2026-05-13] (.harnesskit/artifacts/architecture/feature-design.md)
[BASELINE] feedforward/completed_step_without_artifact: Completed step 'implementation/feature-implementation' has no artifact recorded [baseline: baseline-feature-implementation-artifact, expires: 2026-05-13] (state.json)
[BASELINE] feedforward/implementation_report_missing_harness: .harnesskit/artifacts/implementation/bf-setup-report.md has no Harness Contract section [baseline: baseline-bf-report-no-harness-section, expires: 2026-05-13] (.harnesskit/artifacts/implementation/bf-setup-report.md)
```

**Blocks completion:** no

---

### harness-selftest - PASS

**Command:** `bash .harnesskit/scripts/harness-selftest.sh`

**Required:** yes

**Exit status:** 0

**Output summary:**

```text
test_errors_are_never_downgraded (__main__.BaselineExpirationTests.test_errors_are_never_downgraded) ... ok
test_expired_baseline_leaves_warning_visible (__main__.BaselineExpirationTests.test_expired_baseline_leaves_warning_visible) ... ok
test_future_expiration_accepts_matching_warning (__main__.BaselineExpirationTests.test_future_expiration_accepts_matching_warning) ... ok
test_invalid_expiration_leaves_warning_visible (__main__.BaselineExpirationTests.test_invalid_expiration_leaves_warning_visible) ... ok
test_missing_expiration_leaves_warning_visible (__main__.BaselineExpirationTests.test_missing_expiration_leaves_warning_visible) ... ok

----------------------------------------------------------------------
Ran 5 tests in 0.006s

OK
```

**Blocks completion:** no

---

### harnesskit-cli-status - PASS

**Command:** `node bin/harnesskit.mjs status`

**Required:** yes

**Exit status:** 0

**Output summary:**

```text
Project: harnesskit-dev
Track: Feature work (feature-work; internal: new-features)
Current phase: completed
Progress: ########## 100% (5/5 phases)
Active contracts: 2

Phase map:
  [x] discovery - completed
  [x] specification - completed
  [x] architecture - completed
  [x] implementation - completed
  [x] review - completed

Next step: no pending state step. Start a new work unit with a Harness contract.
```

**Blocks completion:** no

---

### harnesskit-cli-next - PASS

**Command:** `node bin/harnesskit.mjs next`

**Required:** yes

**Exit status:** 0

**Output summary:**

```text
Project: harnesskit-dev
Track: Feature work (feature-work; internal: new-features)
Current phase: completed
Progress: ########## 100% (5/5 phases)
Active contracts: 2

Phase map:
  [x] discovery - completed
  [x] specification - completed
  [x] architecture - completed
  [x] implementation - completed
  [x] review - completed

Next step: no pending state step. Start a new work unit with a Harness contract.

Recommended action:
  Continue the active Harness contract: .harnesskit/harness/contracts/active/HC-20260413-harnesskit-publish.md
  Run: harnesskit doctor
... output truncated (1 more lines)
```

**Blocks completion:** no

---

### package-test - PASS

**Command:** `npm run test`

**Required:** yes

**Exit status:** 0

**Output summary:**

```text
> harnesskit@0.1.0 test
> bash .harnesskit/scripts/validate.sh && bash .harnesskit/scripts/harness-selftest.sh

Validating JSON files...
  ✓ state.json
  ✓ core/agents/_schema.json
  ✓ schemas/spec-schema.json
  ✓ schemas/team-schema.json

Validating YAML files...
  ✓ core/agents/amy.agent.yaml
  ✓ core/agents/bernadette.agent.yaml
  ✓ core/agents/design-specialist.agent.yaml
  ✓ core/agents/howard.agent.yaml
  ✓ core/agents/leonard.agent.yaml
  ✓ core/agents/leslie.agent.yaml
  ✓ core/agents/penny.agent.yaml
  ✓ core/agents/raj.agent.yaml
... output truncated (110 more lines)
```

**Blocks completion:** no

---

### package-pack-check - PASS

**Command:** `npm run pack:check`

**Required:** yes

**Exit status:** 0

**Output summary:**

```text
> harnesskit@0.1.0 pack:check
> npm pack --dry-run --json

[
  {
    "id": "harnesskit@0.1.0",
    "name": "@cardosoads/harnesskit",
    "version": "0.1.0",
    "size": 155124,
    "unpackedSize": 571616,
    "shasum": "b43bb7b056047aeae4f076ad2724b7b55d1460b4",
    "integrity": "sha512-WDNhftbRKWVu5uBHdGYG9kWiuYmgvDthD3NbARWu5HgB3q60doFoEz/njF117XHmmMRSxuAFfVEldtlUv7X9wA==",
    "filename": "harnesskit-0.1.0.tgz",
    "files": [
      {
        "path": ".claude/commands/harnesskit-contract.md",
        "size": 294,
        "mode": 420
... output truncated (671 more lines)
```

**Blocks completion:** no

---

### package-lint - SKIPPED

**Command:** `npm run lint`

**Required:** no

**Exit status:** n/a

**Output summary:**

```text
Condition not met: package.json has a lint script
```

**Blocks completion:** no

---

### package-typecheck - SKIPPED

**Command:** `npm run typecheck`

**Required:** no

**Exit status:** n/a

**Output summary:**

```text
Condition not met: package.json has a typecheck script
```

**Blocks completion:** no

---

### python-tests - SKIPPED

**Command:** `pytest`

**Required:** no

**Exit status:** n/a

**Output summary:**

```text
Condition not met: pyproject.toml, pytest.ini, or tests/ indicates pytest
```

**Blocks completion:** no

---

### ui-e2e - SKIPPED

**Command:** `npx playwright test`

**Required:** no

**Exit status:** n/a

**Output summary:**

```text
Condition not met: playwright config exists and the change is UI-visible
```

**Blocks completion:** no

---

## Deviations

- None recorded by the mechanical runner.

## Verdict Rules

- `APPROVED`: all required sensors passed.
- `NEEDS_FIX`: one or more required checks are incomplete but fixable within current scope.
- `BLOCKED`: required sensor failed, timed out, was unavailable, or the scope needs a decision.
- `ESCALATE`: human decision required.

## Final Recommendation

All required sensors passed. Semantic review is still required when the contract risk level routes to Amy.
