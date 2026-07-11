#!/usr/bin/env python3
"""Regression tests for the preferred 24pt house source-font defaults."""

from __future__ import annotations

import re
import unittest
from pathlib import Path

from paperfig_style import FigureStyle, figure_size
from setup_style import JOURNAL_PRESETS, SOURCE_SCALE


SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
FONT_PATTERN = re.compile(
    r"(?:font\.size|axes\.labelsize|axes\.titlesize|xtick\.labelsize|"
    r"ytick\.labelsize|legend\.fontsize|font[-_]?size|fontsize|labelsize)"
    r"[\"']?\s*[:=]\s*[\"']?([0-9]+(?:\.[0-9]+)?)"
)


class SourceFontPolicyTests(unittest.TestCase):
    def test_journal_presets_have_no_font_below_24pt(self) -> None:
        font_keys = {
            "font.size", "axes.labelsize", "axes.titlesize",
            "xtick.labelsize", "ytick.labelsize", "legend.fontsize",
        }
        for name, preset in JOURNAL_PRESETS.items():
            values = [preset[key] for key in font_keys]
            self.assertGreaterEqual(min(values), 24, (name, values))

    def test_house_helper_defaults_have_no_font_below_24pt(self) -> None:
        style = FigureStyle()
        self.assertGreaterEqual(
            min(style.font_size, style.label_size, style.tick_size, style.legend_size),
            24,
        )
        self.assertEqual(3.0, SOURCE_SCALE)
        self.assertAlmostEqual(9.75, figure_size("single")[0])

    def test_shipped_source_examples_have_no_explicit_font_below_24pt(self) -> None:
        paths = list(SCRIPT_DIR.glob("*.py")) + [
            SKILL_DIR / "references" / "plot-recipes.md"
        ]
        violations: list[tuple[str, float]] = []
        for path in paths:
            text = path.read_text(encoding="utf-8")
            for value in FONT_PATTERN.findall(text):
                size = float(value)
                if size < 24:
                    violations.append((str(path.relative_to(SKILL_DIR)), size))
        self.assertEqual([], violations)


if __name__ == "__main__":
    unittest.main()
