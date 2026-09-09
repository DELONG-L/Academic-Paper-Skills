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


SOFT_STRUCTURE = {
    'STRUCT.TRADITIONAL_HEADINGS', 'STRUCT.CONCLUSION_SINGLE_PARAGRAPH',
    'STRUCT.CONCLUSION_INTEGRATES_LIMITATIONS', 'RELATED.COMPARISON_REQUIRED',
}


class StructurePreferenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        baseline.ComplianceAssessmentTests.setUpClass()
        cls.base = baseline.ComplianceAssessmentTests()
        cls.local_sets = load_yaml(baseline.REFS / 'policy-sets.yaml')

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
        self.context.pop('policy_sets')  # Exercise actual personal defaults.
        self.context['primary_tex'] = 'main.tex'

    def resolve(self):
        return resolve_policy(self.context, self.base.hard, self.base.soft,
                              self.base.profiles, self.local_sets)

    def evidence(self, resolution):
        evidence = self.base.complete_evidence(resolution)
        evidence['soft_results'] = [
            {'rule_id': rid, 'status': 'ADAPTED',
             'rationale': 'Explicit comparisons in prose, distinct conclusion ideas, and standalone limitations improve clarity.'}
            for rid in sorted(SOFT_STRUCTURE)
        ]
        return evidence

    def run_project(self, evidence):
        context_path = self.root / 'context.yaml'
        evidence_path = self.root / 'evidence.yaml'
        context_path.write_text(yaml.safe_dump(self.context))
        evidence_path.write_text(yaml.safe_dump(evidence))
        return run_validation(context_path, self.root, self.root / 'validation', evidence_path)

    def test_local_default_preserves_preferences_without_hard_membership(self):
        resolution = self.resolve()
        self.assertEqual(['integrity-core', 'academic-defaults'], resolution['active_policy_sets'])
        self.assertTrue(SOFT_STRUCTURE.isdisjoint(x['id'] for x in resolution['active_hard']))
        self.assertTrue(SOFT_STRUCTURE.issubset(x['id'] for x in resolution['active_soft']))
        self.assertIn('FACT.NO_FABRICATION', {x['id'] for x in resolution['active_hard']})

    def test_adapted_structure_is_ready_when_other_requirements_have_evidence(self):
        # Supplied hard judgments are fixture evidence, not a real paper review.
        manifest = self.run_project(self.evidence(self.resolve()))
        self.assertEqual('READY', manifest['readiness_status'])
        self.assertEqual(0, manifest['finding_instance_count'])
        self.assertEqual(0, manifest['total_failing_rule_count'])
        worklist = load_yaml(self.root / 'validation/soft-review-worklist.yaml')
        self.assertEqual([], worklist['coverage']['unmapped_rule_ids'])
        result = load_yaml(self.root / 'validation/initial-assessment.yaml')
        self.assertEqual(SOFT_STRUCTURE, {x['rule_id'] for x in result['soft_results']})
        self.assertTrue(SOFT_STRUCTURE.isdisjoint(x['rule_id'] for x in result['hard_results']))

    def test_unassessed_style_does_not_block_otherwise_complete_readiness(self):
        resolution = self.resolve()
        evidence = self.base.complete_evidence(resolution)
        result = assess_compliance(resolution, self.base.hard, evidence)
        self.assertEqual('READY', result['readiness']['status'])
        self.assertTrue(SOFT_STRUCTURE.issubset(result['unassessed_soft']))

    def test_unregistered_section_count_profile_is_rejected(self):
        self.context['structure_profile'] = 'standard_conference'
        with self.assertRaisesRegex(ValueError, 'unknown fields'):
            self.resolve()

    def test_conference_venue_does_not_promote_section_preference(self):
        resolution = self.resolve()
        self.assertNotIn('STRUCT.SECTION_COUNT_PROFILE', {x['id'] for x in resolution['active_hard']})
        self.assertIn('STRUCT.SECTION_COUNT', {x['id'] for x in resolution['active_soft']})
        self.assertEqual('READY', self.run_project(self.evidence(resolution))['readiness_status'])

    def test_style_adaptation_cannot_clear_integrity_or_venue_failure(self):
        resolution = self.resolve()
        for rule_id in ['CLAIM.EVIDENCE_BOUND', 'VENUE.CONSTRAINT_PROVENANCE']:
            with self.subTest(rule=rule_id):
                evidence = self.evidence(resolution)
                target = next(x for x in evidence['hard_results'] if x['rule_id'] == rule_id)
                target['status'] = 'FAIL'
                target['evidence'] = 'Required supporting evidence is contradicted by the inspected source.'
                result = assess_compliance(resolution, self.base.hard, evidence)
                self.assertEqual('BLOCKED', result['readiness']['status'])
                self.assertIn(rule_id, result['readiness']['hard_blockers'])

    def test_old_hard_style_records_require_explicit_soft_reassessment(self):
        resolution = self.resolve()
        for rid in SOFT_STRUCTURE:
            with self.subTest(rule=rid):
                evidence = self.evidence(resolution)
                evidence['hard_results'].append(self.base.pass_record(rid))
                with self.assertRaisesRegex(ValueError, 'soft rule; reassess'):
                    assess_compliance(resolution, self.base.hard, evidence)

    def test_shared_defaults_retain_adaptable_structure_guidance(self):
        self.context['policy_sets'] = ['integrity-core', 'academic-defaults']
        resolution = self.resolve()
        self.assertNotIn('strict-house-style', resolution['active_policy_sets'])
        self.assertTrue(SOFT_STRUCTURE.issubset(x['id'] for x in resolution['active_soft']))
        self.assertTrue(SOFT_STRUCTURE.isdisjoint(x['id'] for x in resolution['active_hard']))


if __name__ == '__main__':
    unittest.main()
