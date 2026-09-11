from pathlib import Path
import tempfile
import unittest

from audit_skill_integration import SKILLS, audit


class IntegrationAuditTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        for skill in SKILLS:
            folder = self.root / skill
            (folder / "references").mkdir(parents=True)
            (folder / "SKILL.md").write_text("# Skill\n")
        for name in ("hard",):
            (self.root / "paper-policy/references" / (name + "-rules.yaml")).write_text(
                "rules:\n  - id: CLAIM." + name.upper() + "\n")

    def doc(self, text):
        (self.root / "paper-writing/SKILL.md").write_text(text)

    def test_valid_cross_skill_reference_and_rule_index(self):
        self.doc("Use `CLAIM.HARD` and [review](../paper-review/SKILL.md).\n")
        result = audit(self.root)
        self.assertEqual(result["errors"], [])
        self.assertEqual(result["rule_consumers"]["CLAIM.HARD"][0]["line"], 1)

    def test_missing_reference_fails(self):
        self.doc("Read `references/missing.md`.\n")
        self.assertEqual(audit(self.root)["errors"][0]["kind"], "missing_reference")

    def test_retired_rule_fails(self):
        self.doc("Follow `CLAIM.RETIRED`.\n")
        self.assertEqual(audit(self.root)["errors"][0]["kind"], "unknown_rule")

    def test_runtime_names_urls_and_examples_are_not_dependencies(self):
        self.doc("Use `PROJECT-WORKSPACE.md` and [source](https://example.org/a.md).\n"
                 "```text\n`references/example.md` `CLAIM.EXAMPLE`\n```\n")
        self.assertEqual(audit(self.root)["errors"], [])

    def test_valid_id_does_not_certify_semantics(self):
        self.doc("`CLAIM.HARD` means anything the writer wants.\n")
        result = audit(self.root)
        self.assertEqual(result["errors"], [])
        self.assertIn("Semantic consistency", result["coverage"]["not_checked"])

    def test_missing_skill_is_not_clean(self):
        (self.root / "paper-review/SKILL.md").unlink()
        self.assertEqual(audit(self.root)["errors"][0]["kind"], "missing_skill")

    def test_inline_skill_root_convention_and_relative_markdown_links(self):
        folder = self.root / "paper-writing"
        (folder / "scripts").mkdir()
        (folder / "scripts/check.py").write_text("pass\n")
        ref = folder / "references/workflow.md"
        ref.write_text("Use `scripts/check.py`.\n")
        self.assertEqual(audit(self.root)["errors"], [])
        ref.write_text("Use [checker](scripts/check.py).\n")
        self.assertEqual(audit(self.root)["errors"][0]["kind"], "missing_reference")


if __name__ == "__main__":
    unittest.main()
