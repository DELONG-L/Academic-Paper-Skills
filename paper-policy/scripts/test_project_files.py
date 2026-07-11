#!/usr/bin/env python3
"""Tests for authoritative paper-project file selection."""

from __future__ import annotations

import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from project_files import select_project_files


class ProjectFileSelectionTests(unittest.TestCase):
    def test_explicit_primary_excludes_flattened_template_and_unused_copies(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            (root / "sections").mkdir()
            (root / "archive").mkdir()
            (root / "paper.tex").write_text(
                "\\documentclass{article}\n\\input{sections/body}\n"
                "\\bibliography{references}\n",
                encoding="utf-8",
            )
            (root / "sections" / "body.tex").write_text("Primary.\n", encoding="utf-8")
            (root / "paper_flat.tex").write_text(
                "\\documentclass{article}\nDuplicate.\n", encoding="utf-8"
            )
            (root / "archive" / "template.tex").write_text(
                "\\documentclass{article}\nTemplate.\n", encoding="utf-8"
            )
            (root / "references.bib").write_text(
                "@article{primary, title={Primary}}\n", encoding="utf-8"
            )
            (root / "archive" / "template.bib").write_text(
                "@article{template, title={Template}}\n", encoding="utf-8"
            )
            selected = select_project_files(root, "paper.tex")
            self.assertEqual(
                {"paper.tex", "sections/body.tex"},
                {path.relative_to(root).as_posix() for path in selected.tex_paths},
            )
            self.assertEqual(
                {"references.bib"},
                {path.relative_to(root).as_posix() for path in selected.bib_paths},
            )

    def test_ambiguous_document_roots_require_explicit_primary(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            for name in ("paper.tex", "flattened.tex"):
                (root / name).write_text("\\documentclass{article}\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "ambiguous manuscript entrypoint"):
                select_project_files(root)


if __name__ == "__main__":
    unittest.main()
