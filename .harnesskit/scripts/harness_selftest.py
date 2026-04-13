#!/usr/bin/env python3
"""Self-tests for focused Harnesskit Harness behavior."""

from __future__ import annotations

import json
import tempfile
import unittest
from datetime import date, timedelta
from pathlib import Path

import harness_doctor


class BaselineExpirationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tempdir.name)
        self.baseline_path = self.root / ".harnesskit" / "harness" / "baselines" / "current.yaml"
        self.baseline_path.parent.mkdir(parents=True)

    def tearDown(self) -> None:
        self.tempdir.cleanup()

    def issue(self, severity: str = "warning") -> harness_doctor.Issue:
        return harness_doctor.Issue(
            severity,
            "feedforward",
            "phase_missing_in_state",
            "Configured phase 'design' is missing in state.json",
            "state.json",
        )

    def baseline_entry(self, **overrides: object) -> dict[str, object]:
        entry: dict[str, object] = {
            "id": "baseline-design-phase-state",
            "plane": "feedforward",
            "code": "phase_missing_in_state",
            "file": "state.json",
            "message_contains": "Configured phase 'design' is missing in state.json",
            "expires_at": (date.today() + timedelta(days=30)).isoformat(),
        }
        entry.update(overrides)
        return entry

    def write_baseline(self, entry: dict[str, object]) -> None:
        self.baseline_path.write_text(
            json.dumps({"version": 1, "accepted_issues": [entry]}),
            encoding="utf-8",
        )

    def apply(self, issue: harness_doctor.Issue, entry: dict[str, object]) -> list[harness_doctor.Issue]:
        self.write_baseline(entry)
        issues = [issue]
        harness_doctor.apply_baselines(self.root, issues)
        return issues

    def test_future_expiration_accepts_matching_warning(self) -> None:
        issues = self.apply(self.issue(), self.baseline_entry())

        self.assertEqual(issues[0].severity, "info")
        self.assertEqual(issues[0].baseline, "baseline-design-phase-state")
        self.assertRegex(issues[0].baseline_expires_at, r"^\d{4}-\d{2}-\d{2}$")
        self.assertIn("expires:", issues[0].message)

    def test_missing_expiration_leaves_warning_visible(self) -> None:
        entry = self.baseline_entry()
        entry.pop("expires_at")
        issues = self.apply(self.issue(), entry)

        self.assertEqual(issues[0].severity, "warning")
        self.assertEqual(issues[0].baseline, "")
        self.assertTrue(any(issue.code == "baseline_missing_expiration" for issue in issues))

    def test_invalid_expiration_leaves_warning_visible(self) -> None:
        issues = self.apply(self.issue(), self.baseline_entry(expires_at="not-a-date"))

        self.assertEqual(issues[0].severity, "warning")
        self.assertEqual(issues[0].baseline, "")
        self.assertTrue(any(issue.code == "baseline_invalid_expiration" for issue in issues))

    def test_expired_baseline_leaves_warning_visible(self) -> None:
        expired = (date.today() - timedelta(days=1)).isoformat()
        issues = self.apply(self.issue(), self.baseline_entry(expires_at=expired))

        self.assertEqual(issues[0].severity, "warning")
        self.assertEqual(issues[0].baseline, "")
        self.assertTrue(any(issue.code == "baseline_expired" for issue in issues))

    def test_errors_are_never_downgraded(self) -> None:
        issues = self.apply(self.issue("error"), self.baseline_entry())

        self.assertEqual(issues[0].severity, "error")
        self.assertEqual(issues[0].baseline, "")
        self.assertFalse(any(issue.baseline for issue in issues))


if __name__ == "__main__":
    unittest.main(verbosity=2)
