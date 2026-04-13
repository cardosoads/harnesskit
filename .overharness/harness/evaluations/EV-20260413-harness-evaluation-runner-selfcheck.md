# Harness Evaluation: EV-20260413-harness-evaluation-runner

| Field | Value |
| --- | --- |
| Project | overharness-dev |
| Evaluation | EV-20260413-harness-evaluation-runner |
| Contract | HC-20260413-harness-evaluation-runner |
| Contract Path | `/Users/wesleycardoso/Wesley/Harness/overharness-dev/.overharness/harness/contracts/completed/HC-20260413-harness-evaluation-runner.md` |
| Date | 2026-04-13 |
| Evaluator | harness-evaluate |
| Risk | medium |
| Verdict | APPROVED |
| Score | 1.00 |

## Contract Coverage

### MH-01 - RECORDED

**Expected truth:** Runner script exists and is executable through wrapper

**Evidence:** Sensor evidence is recorded below. Semantic verification remains with Amy when the contract risk requires evaluator review.

**Finding:** Not failed by the mechanical runner.

**Required follow-up:** Amy should review this must-have against the implementation artifact when risk routing requires it.

---

### MH-02 - RECORDED

**Expected truth:** Runner creates a durable evaluation artifact

**Evidence:** Sensor evidence is recorded below. Semantic verification remains with Amy when the contract risk requires evaluator review.

**Finding:** Not failed by the mechanical runner.

**Required follow-up:** Amy should review this must-have against the implementation artifact when risk routing requires it.

---

### MH-03 - RECORDED

**Expected truth:** Required sensors are reflected in the evaluation

**Evidence:** Sensor evidence is recorded below. Semantic verification remains with Amy when the contract risk requires evaluator review.

**Finding:** Not failed by the mechanical runner.

**Required follow-up:** Amy should review this must-have against the implementation artifact when risk routing requires it.

---

### MH-04 - RECORDED

**Expected truth:** Completion is blocked on required sensor failures

**Evidence:** Sensor evidence is recorded below. Semantic verification remains with Amy when the contract risk requires evaluator review.

**Finding:** Not failed by the mechanical runner.

**Required follow-up:** Amy should review this must-have against the implementation artifact when risk routing requires it.

---

### MH-05 - RECORDED

**Expected truth:** Core validation knows about the runner

**Evidence:** Sensor evidence is recorded below. Semantic verification remains with Amy when the contract risk requires evaluator review.

**Finding:** Not failed by the mechanical runner.

**Required follow-up:** Amy should review this must-have against the implementation artifact when risk routing requires it.

---

## Sensor Results

### harness-evaluate-help - PASS

**Command:** `bash .overharness/scripts/harness-evaluate.sh --help`

**Required:** yes

**Exit status:** 0

**Output summary:**

```text
usage: harness_evaluate.py [-h] [--root ROOT] [--contract CONTRACT]
                           [--sensor-group SENSOR_GROUP] [--output OUTPUT]
                           [--include-recommended] [--timeout TIMEOUT]
                           [--format {text,json}]

Run Harness sensors and write an evaluation artifact.

options:
  -h, --help            show this help message and exit
  --root ROOT           Project root
  --contract CONTRACT   Path to an active Harness contract. Defaults to newest
                        active contract.
  --sensor-group SENSOR_GROUP
                        Sensor group from .overharness/harness/sensors.yaml
  --output OUTPUT       Evaluation output path. Defaults to
                        .overharness/harness/evaluations/<evaluation-id>.md
  --include-recommended
                        Run recommended sensors as well as required sensors
... output truncated (2 more lines)
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
