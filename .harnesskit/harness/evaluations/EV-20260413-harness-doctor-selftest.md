# Harness Evaluation: EV-20260413-harness-doctor-selftest

| Field | Value |
| --- | --- |
| Project | harnesskit-dev |
| Evaluation | EV-20260413-harness-doctor-selftest |
| Contract | HC-20260413-harness-doctor-selftest |
| Contract Path | `/Users/wesleycardoso/Wesley/Harness/harnesskit-dev/.harnesskit/harness/contracts/completed/HC-20260413-harness-doctor-selftest.md` |
| Date | 2026-04-13 |
| Evaluator | harness-evaluate |
| Risk | medium |
| Verdict | APPROVED |
| Score | 1.00 |

## Contract Coverage

### MH-01 - RECORDED

**Expected truth:** Self-test script exists

**Evidence:** Sensor evidence is recorded below. Semantic verification remains with Amy when the contract risk requires evaluator review.

**Finding:** Not failed by the mechanical runner.

**Required follow-up:** Amy should review this must-have against the implementation artifact when risk routing requires it.

---

### MH-02 - RECORDED

**Expected truth:** Wrapper exists

**Evidence:** Sensor evidence is recorded below. Semantic verification remains with Amy when the contract risk requires evaluator review.

**Finding:** Not failed by the mechanical runner.

**Required follow-up:** Amy should review this must-have against the implementation artifact when risk routing requires it.

---

### MH-03 - RECORDED

**Expected truth:** Baseline expiration edge cases are covered

**Evidence:** Sensor evidence is recorded below. Semantic verification remains with Amy when the contract risk requires evaluator review.

**Finding:** Not failed by the mechanical runner.

**Required follow-up:** Amy should review this must-have against the implementation artifact when risk routing requires it.

---

### MH-04 - RECORDED

**Expected truth:** Core validation knows about the self-test

**Evidence:** Sensor evidence is recorded below. Semantic verification remains with Amy when the contract risk requires evaluator review.

**Finding:** Not failed by the mechanical runner.

**Required follow-up:** Amy should review this must-have against the implementation artifact when risk routing requires it.

---

### MH-05 - RECORDED

**Expected truth:** Harness evaluation runs the self-test

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
... output truncated (79 more lines)
```

**Blocks completion:** no

---

### harness-doctor - PASS

**Command:** `bash .harnesskit/scripts/harness-doctor.sh`

**Required:** yes

**Exit status:** 0

**Output summary:**

```text
Harnesskit Harness Doctor
Errors: 0  Warnings: 0  Info: 5
Baseline accepted: 4
[BASELINE] feedforward/phase_missing_in_state: Configured phase 'design' is missing in state.json [baseline: baseline-design-phase-state, expires: 2026-05-13] (state.json)
[BASELINE] feedforward/artifact_placeholder: .harnesskit/artifacts/architecture/feature-design.md has unresolved template/TODO markers at lines 239, 303, 304, 305, 319 [baseline: baseline-feature-design-template-markers, expires: 2026-05-13] (.harnesskit/artifacts/architecture/feature-design.md)
[BASELINE] feedforward/completed_step_without_artifact: Completed step 'implementation/feature-implementation' has no artifact recorded [baseline: baseline-feature-implementation-artifact, expires: 2026-05-13] (state.json)
[BASELINE] feedforward/implementation_report_missing_harness: .harnesskit/artifacts/implementation/bf-setup-report.md has no Harness Contract section [baseline: baseline-bf-report-no-harness-section, expires: 2026-05-13] (.harnesskit/artifacts/implementation/bf-setup-report.md)
[INFO] feedback/no_code_test_runner_discovered: No package.json/pyproject/pytest test runner discovered; feedback is limited to Harnesskit structural sensors
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

### package-lint - SKIPPED

**Command:** `npm run lint`

**Required:** no

**Exit status:** n/a

**Output summary:**

```text
Recommended sensor not requested. Re-run with --include-recommended to execute it.
```

**Blocks completion:** no

---

### package-test - SKIPPED

**Command:** `npm run test`

**Required:** no

**Exit status:** n/a

**Output summary:**

```text
Recommended sensor not requested. Re-run with --include-recommended to execute it.
```

**Blocks completion:** no

---

### package-typecheck - SKIPPED

**Command:** `npm run typecheck`

**Required:** no

**Exit status:** n/a

**Output summary:**

```text
Recommended sensor not requested. Re-run with --include-recommended to execute it.
```

**Blocks completion:** no

---

### python-tests - SKIPPED

**Command:** `pytest`

**Required:** no

**Exit status:** n/a

**Output summary:**

```text
Recommended sensor not requested. Re-run with --include-recommended to execute it.
```

**Blocks completion:** no

---

### ui-e2e - SKIPPED

**Command:** `npx playwright test`

**Required:** no

**Exit status:** n/a

**Output summary:**

```text
Recommended sensor not requested. Re-run with --include-recommended to execute it.
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
