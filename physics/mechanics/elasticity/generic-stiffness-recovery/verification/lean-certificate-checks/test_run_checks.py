"""Protect source integrity and ensure failed or bounded-out jobs cannot pass."""

import json
import os
from pathlib import Path
import shutil
import sys
import tempfile
import time
import unittest
from unittest.mock import patch

import run_checks


class RunnerChecks(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory(prefix="elasticity-runner-test-")
        self.addCleanup(self.directory.cleanup)
        self.output = Path(self.directory.name)
        (self.output / "diagnostics").mkdir()

    def run_child(self, name, program, deadline):
        return run_checks.run_step(
            name,
            [sys.executable, "-B", "-u", "-c", program],
            self.output,
            self.output,
            dict(os.environ),
            deadline,
        )

    def test_changed_proof_source_is_rejected(self):
        """A modified Lean input must fail even if its certificate name is unchanged."""
        source = self.output / "source"
        source.mkdir()
        manifest = json.loads((run_checks.ROOT / "source-manifest.json").read_text())
        for relative in ["source-manifest.json"] + [
            item["path"] for item in manifest["files"]
        ]:
            target = source / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(run_checks.ROOT / relative, target)
        changed = source / "lean/MinorBatch16.lean"
        changed.write_text(
            changed.read_text().replace("certificate_3_213", "certificate_3_212", 1)
        )
        with patch.object(run_checks, "ROOT", source):
            with self.assertRaisesRegex(ValueError, "Source hash mismatch"):
                run_checks.verify_sources()

    def test_failed_child_preserves_nonzero_exit(self):
        """A compiler-like failure must remain a failure and retain its diagnostic."""
        with self.assertRaisesRegex(RuntimeError, "exited 7"):
            self.run_child(
                "nonzero",
                "print('deliberate failure', flush=True); raise SystemExit(7)",
                time.monotonic() + 30,
            )
        record = json.loads((self.output / "diagnostics/nonzero.json").read_text())
        self.assertEqual((record["status"], record["exit_code"]), ("FAIL", 7))
        self.assertIn(
            "deliberate failure", (self.output / "diagnostics/nonzero.log").read_text()
        )

    def test_expired_budget_stops_child(self):
        """A time-limited job must terminate its process and record failure."""
        with self.assertRaisesRegex(RuntimeError, "compilation budget expired"):
            self.run_child(
                "deadline", "import time; time.sleep(30)", time.monotonic() + 0.2
            )
        record = json.loads((self.output / "diagnostics/deadline.json").read_text())
        self.assertEqual(record["status"], "FAIL")
        self.assertIsInstance(record["exit_code"], int)
        self.assertLess(record["exit_code"], 0)

    def test_disk_and_memory_guards_stop_real_children(self):
        """Both resource limits must fail a running child without allocating large data."""
        limits = [
            (
                "MIN_FREE_BYTES",
                shutil.disk_usage(self.output).free + 1_000_000_000,
                "free disk",
            ),
            ("MAX_RSS_BYTES", 1, "process RSS"),
        ]
        for setting, limit, message in limits:
            with self.subTest(setting=setting), patch.object(
                run_checks, setting, limit
            ):
                with self.assertRaisesRegex(RuntimeError, message):
                    self.run_child(
                        setting, "import time; time.sleep(30)", time.monotonic() + 30
                    )
            record = json.loads(
                (self.output / f"diagnostics/{setting}.json").read_text()
            )
            self.assertEqual(record["status"], "FAIL")
            self.assertIsInstance(record["exit_code"], int)
            self.assertLess(record["exit_code"], 0)


if __name__ == "__main__":
    unittest.main(verbosity=2, buffer=True)
