#!/usr/bin/env python3
"""Tests for section-aware soft-rule worklist generation."""

from __future__ import annotations

import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from build_soft_worklist import build_soft_review_worklist


class SoftWorklistTests(unittest.TestCase):
    def test_groups_global_and_targeted_rules_without_losing_coverage(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "main.tex").write_text(
                "\\documentclass{article}\n\\begin{document}\n"
                "\\begin{abstract}A.\\end{abstract}\n"
                "\\section{Introduction}\nI.\n"
                "\\section{Experiments}\nR.\n"
                "\\section{Conclusion}\nC.\n\\end{document}\n",
                encoding="utf-8",
            )
            base = {
                "title": "Rule", "scope": ["writing"],
                "default": "Default", "allowed_variants": ["Variant"],
                "selection_factors": ["factor"], "avoid": [],
                "report_when": "Report", "preferred_by_profiles": [],
            }
            resolution = {
                "active_soft": [
                    {**base, "id": "PROSE.GLOBAL", "artifacts": ["prose"], "features": []},
                    {**base, "id": "RESULTS.TARGET", "artifacts": ["prose"], "features": ["evaluation_section"]},
                    {**base, "id": "THREATS.TARGET", "artifacts": ["prose"], "features": ["limitations_content"]},
                    {**base, "id": "TABLE.TARGET", "artifacts": ["table"], "features": ["result_table"]},
                    {**base, "id": "TABLE.GLOBAL", "artifacts": ["table", "tex"], "features": []},
                ]
            }
            result = build_soft_review_worklist(
                resolution,
                root,
                [{"id": "main-table", "kind": "table"}],
            )
            groups = {group["id"]: group for group in result["groups"]}
            self.assertIn("PROSE.GLOBAL", groups["conclusion"]["global_rule_ids"])
            self.assertIn("THREATS.TARGET", groups["conclusion"]["targeted_rule_ids"])
            self.assertIn("RESULTS.TARGET", groups["experiments"]["targeted_rule_ids"])
            self.assertEqual(["main-table"], groups["tables"]["artifact_ids"])
            self.assertIn("TABLE.GLOBAL", groups["tables"]["rule_ids"])
            self.assertEqual([], result["coverage"]["unmapped_rule_ids"])


if __name__ == "__main__":
    unittest.main()
