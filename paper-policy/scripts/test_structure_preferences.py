"""Behavioral regressions for adaptable structure and retained hard boundaries."""
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
import yaml

from assess_compliance import assess_compliance
from resolve_policy import resolve_policy
from run_project_validation import run_validation
from validate_registry import load_yaml
import test_assess_compliance as baseline


RETIRED_STRUCTURE = {
    'STRUCT.TRADITIONAL_HEADINGS', 'STRUCT.CONCLUSION_SINGLE_PARAGRAPH',
    'STRUCT.CONCLUSION_INTEGRATES_LIMITATIONS', 'RELATED.COMPARISON_REQUIRED',
}


class StructurePreferenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        baseline.ComplianceAssessmentTests.setUpClass()
        cls.base = baseline.ComplianceAssessmentTests()

    def setUp(self):
        temp = TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name).resolve()
        # Eight sections, topic-specific headings, a prose-only comparison,
        # a separate Limitations section, and a two-paragraph Conclusion.
        (self.root / 'main.tex').write_text(
            '\\documentclass{article}\n\\begin{document}\n'
            '\\section{Introduction}\nA bounded comparison.\n'
            '\\section{Related Work}\nApproach A shares assumptions; B relaxes them.\n'
            '\\section{Problem Boundary}\nDefined scope.\n'
            '\\section{Method}\nProcedure.\n'
            '\\section{Results}\nObserved finding.\n'
            '\\section{Discussion}\nInterpretation.\n'
            '\\section{Limitations}\nOnly one setting was measured.\n'
            '\\section{Conclusion}\nThe finding applies in the measured setting.\n\n'
            'Other settings remain untested.\n\\end{document}\n'
        )
        self.context = load_yaml(baseline.CONTEXTS / 'submission.yaml')
        self.context['primary_tex'] = 'main.tex'

    def resolve(self):
        return resolve_policy(self.context, self.base.hard, self.base.profiles)

    def run_project(self, evidence):
        context_path = self.root / 'context.yaml'
        evidence_path = self.root / 'evidence.yaml'
        context_path.write_text(yaml.safe_dump(self.context))
        evidence_path.write_text(yaml.safe_dump(evidence))
        return run_validation(context_path, self.root, self.root / 'validation', evidence_path)

    def test_varied_structure_needs_no_editorial_registration(self):
        resolution = self.resolve()
        # Fixture judgments exercise aggregation; they are not a real paper review.
        manifest = self.run_project(self.base.complete_evidence(resolution))
        self.assertEqual('READY', manifest['readiness_status'])
        self.assertEqual(0, manifest['finding_instance_count'])
        result = load_yaml(self.root / 'validation/initial-assessment.yaml')
        self.assertNotIn('soft_results', result)
        self.assertNotIn('unassessed_soft', result)
        self.assertNotIn('active_soft', resolution)
        self.assertFalse((self.root / 'validation/soft-review-worklist.yaml').exists())
        self.assertTrue(RETIRED_STRUCTURE.isdisjoint(x['rule_id'] for x in result['hard_results']))

    def test_free_structure_does_not_clear_integrity_or_venue_failure(self):
        resolution = self.resolve()
        for rule_id in ['CLAIM.EVIDENCE_BOUND', 'VENUE.CONSTRAINT_PROVENANCE']:
            with self.subTest(rule=rule_id):
                evidence = self.base.complete_evidence(resolution)
                target = next(x for x in evidence['hard_results'] if x['rule_id'] == rule_id)
                target['status'] = 'FAIL'
                target['evidence'] = 'Supporting evidence contradicts the inspected source.'
                result = assess_compliance(resolution, self.base.hard, evidence)
                self.assertEqual('BLOCKED', result['readiness']['status'])
                self.assertIn(rule_id, result['readiness']['hard_blockers'])

    def test_retired_style_records_cannot_enter_requirement_results(self):
        resolution = self.resolve()
        for rid in RETIRED_STRUCTURE:
            with self.subTest(rule=rid):
                evidence = self.base.complete_evidence(resolution)
                evidence['hard_results'].append(self.base.pass_record(rid))
                with self.assertRaisesRegex(ValueError, 'rule is not active'):
                    assess_compliance(resolution, self.base.hard, evidence)

    def test_retired_evidence_and_context_fields_are_rejected(self):
        resolution = self.resolve()
        evidence = self.base.complete_evidence(resolution)
        evidence['soft_results'] = []
        with self.assertRaisesRegex(ValueError, 'unknown fields soft_results'):
            assess_compliance(resolution, self.base.hard, evidence)
        for field in ('policy_sets', 'table_profile'):
            with self.subTest(field=field):
                context = dict(self.context, **{field: 'unused'})
                with self.assertRaisesRegex(ValueError, 'unknown fields'):
                    resolve_policy(context, self.base.hard, self.base.profiles)


if __name__ == '__main__':
    unittest.main()
