"""Behavioral regressions for broken docs and unsafe or mismatched repo assets."""
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from check_repository import anchors, check_document, check_pair, check_skill, check_svg


class RepositoryChecks(unittest.TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def put(self, name, text):
        p = self.root / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text)
        return p

    def test_relative_html_and_unicode_anchor_resolve(self):
        self.put('docs/指南.md', '# 安装\n<a id="upgrade"></a>\n')
        p = self.put('README.md', '[Guide](docs/%E6%8C%87%E5%8D%97.md#安装)\n<a href="docs/指南.md#upgrade">Upgrade</a>')
        self.assertEqual([], check_document(p, self.root))

    def test_missing_target_and_anchor_are_reported(self):
        self.put('guide.md', '# Setup\n')
        p = self.put('README.md', '[One](missing.md)\n[Two](guide.md#absent)')
        errors = check_document(p, self.root)
        self.assertEqual(2, len(errors))
        self.assertTrue(any('missing anchor' in x for x in errors))

    def test_fenced_examples_and_remote_badges_are_not_local_links(self):
        p = self.put('README.md', '```md\n[x](not-real.md)\n```\n<img src="https://example.com/badge.svg">')
        self.assertEqual([], check_document(p, self.root))

    def test_escape_outside_repository_rejected(self):
        p = self.put('README.md', '[Outside](../private.md)')
        self.assertIn('escapes repository', check_document(p, self.root)[0])

    def test_duplicate_heading_anchors(self):
        self.assertEqual({'setup', 'setup-1'}, anchors('# Setup\n# Setup\n'))

    def test_language_pair_needs_both_switches_and_matching_navigation(self):
        a = self.put('README.md', '[中文](README.zh-CN.md)\n<a id="start"></a>')
        b = self.put('README.zh-CN.md', '<a id="different"></a>')
        self.assertEqual(2, len(check_pair(a, b, self.root)))

    def test_self_contained_vector_and_unsafe_raster_are_distinguished(self):
        a = self.put('logo.svg', '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 10 10"><title>Logo</title><path d="M0 0L1 1"/></svg>')
        self.assertEqual([], check_svg(a))
        a.write_text('<svg viewBox="0 0 10 10"><title>Logo</title><image href="https://example.com/x.png"/><script>bad()</script></svg>')
        self.assertGreaterEqual(len(check_svg(a)), 2)

    def test_skill_identity_mismatch_rejected(self):
        self.put('paper-example/SKILL.md', '---\nname: another-skill\ndescription: Example\n---\n')
        self.put('paper-example/agents/openai.yaml', 'interface:\n  display_name: Example\n  short_description: Example skill\n  default_prompt: Use $another-skill\n')
        self.assertEqual(2, len(check_skill(self.root / 'paper-example')))


if __name__ == '__main__':
    unittest.main()
