# Harness Baselines

Baselines document known Harness findings that are accepted as operational
debt for the current cycle.

They are not fixes and they are not a way to hide errors. The doctor only
reclassifies non-error findings when `plane`, `code`, and `file` match an
accepted entry. Use `message_contains` when a finding needs a narrower match.

## Rules

- Baseline entries must include an owner and reason.
- Baseline entries must include `expires_at` in `YYYY-MM-DD` format.
- Baseline entries should point to a follow-up contract or cleanup item when
  the issue should be resolved later.
- Errors are never downgraded by baseline matching.
- New warnings that do not match the baseline remain visible as warnings.
- Expired, missing, or invalid baseline dates do not reclassify matching
  findings.
