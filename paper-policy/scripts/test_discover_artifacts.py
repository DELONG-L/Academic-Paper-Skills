#!/usr/bin/env python3
"""Tests for guarded LaTeX artifact discovery."""

from __future__ import annotations

import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from check_artifacts import validate_artifact_records
from discover_artifacts import compare_discovery, discover_artifacts


class ArtifactDiscoveryTests(unittest.TestCase):
    def test_discovers_figure_and_table_as_unconfirmed_skeleton(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "plot.pdf").write_bytes(b"%PDF")
            (root / "main.tex").write_text(
                r"""
\begin{figure}
\includegraphics{plot}
\caption{Overview of the evidence pipeline.}
\label{fig:overview}
\end{figure}
\begin{table*}
\caption{Main result audit.}
\label{tab:main-results}
\begin{tabular}{ll}\toprule A & B \\\midrule 1 & 2 \\\bottomrule\end{tabular}
\end{table*}
\begin{table}
\caption{Audited condition families in the experimental setup.}
\label{tab:condition-families}
\begin{tabular}{ll}\toprule A & B \\\midrule 1 & 2 \\\bottomrule\end{tabular}
\end{table}
""",
                encoding="utf-8",
            )
            result = discover_artifacts(root)
            self.assertEqual(3, len(result["artifacts"]))
            figure, table, setup_table = result["artifacts"]
            self.assertEqual(["paper_figure", "conceptual_figure"], figure["artifact_types"])
            self.assertEqual(["plot.pdf"], figure["files"]["outputs"])
            self.assertEqual("tab:main-results", table["latex_label"])
            self.assertEqual("needs_confirmation", table["discovery_status"])
            self.assertEqual(
                ["paper_table", "data_table"], setup_table["artifact_types"]
            )
            errors = validate_artifact_records(result["artifacts"])
            self.assertTrue(any("must be reviewed" in item for item in errors))

    def test_confirmed_evidence_comparison_uses_label_and_output(self) -> None:
        discovered = [
            {
                "id": "one", "kind": "figure",
                "files": {"outputs": ["figures/one.pdf"]},
            },
            {
                "id": "two", "kind": "table", "latex_label": "tab:two",
                "files": {"outputs": []},
            },
        ]
        confirmed = [
            {
                "id": "one", "kind": "figure",
                "files": {"outputs": ["figures/one.pdf"]},
            }
        ]
        result = compare_discovery(discovered, confirmed)
        self.assertEqual(1, result["missing_from_confirmed_evidence_count"])
        self.assertEqual("two", result["missing_from_confirmed_evidence"][0]["id"])
        self.assertEqual(0, result["confirmed_not_discovered_count"])


if __name__ == "__main__":
    unittest.main()
