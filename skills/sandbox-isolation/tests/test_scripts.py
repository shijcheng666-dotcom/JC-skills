import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "scripts" / "audit_memory.py"
LINT = ROOT / "scripts" / "lint_daily_logs.py"
SCAN = ROOT / "scripts" / "scan_publication.py"
FIXTURES = ROOT / "tests" / "fixtures"


class ScriptTests(unittest.TestCase):
    def run_json(self, script, *args, expected=0):
        result = subprocess.run([sys.executable, str(script), *map(str, args)], capture_output=True, text=True)
        self.assertEqual(result.returncode, expected, result.stderr)
        return json.loads(result.stdout)

    def test_audit_is_read_only_and_detects_layout_conflict(self):
        root = FIXTURES / "dirty" / "memory"
        before = {p: p.stat().st_mtime_ns for p in root.rglob("*") if p.is_file()}
        report = self.run_json(AUDIT, root)
        after = {p: p.stat().st_mtime_ns for p in root.rglob("*") if p.is_file()}
        self.assertEqual(before, after)
        self.assertEqual(report["governance"], "present")
        self.assertTrue(any(item["status"] == "conflict" for item in report["files"]))
        self.assertFalse(report["writes_performed"])

    def test_audit_reports_missing_governance(self):
        report = self.run_json(AUDIT, FIXTURES / "missing" / "memory")
        self.assertEqual(report["governance"], "missing")
        self.assertEqual(report["files"], [])

    def test_lint_honors_historical_date_and_20_char_limit(self):
        report = self.run_json(LINT, FIXTURES / "dirty" / "memory", "--governance-date", "2026-07-28")
        by_name = {item["path"]: item for item in report["files"]}
        self.assertEqual(by_name["2026-07-20.md"]["status"], "historical")
        self.assertEqual(by_name["2026-07-30.md"]["status"], "violation")
        self.assertTrue(by_name["2026-07-30.md"]["violations"])

    def test_publication_scan_passes_package(self):
        report = self.run_json(SCAN, ROOT)
        self.assertEqual(report["status"], "pass")


if __name__ == "__main__":
    unittest.main()
