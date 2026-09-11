"""Requirements assess manuscripts; editorial and execution choices stay outside gates."""
from copy import deepcopy
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
import yaml

from assess_compliance import assess_compliance
from lint_project import lint_project
from resolve_policy import resolve_policy
from run_project_validation import run_validation
from validate_registry import load_yaml, validate_hard_document

REFS = Path(__file__).resolve().parent.parent / 'references'


class RequirementScopeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.hard = load_yaml(REFS / 'hard-rules.yaml')
        cls.profiles = load_yaml(REFS / 'profiles.yaml')

    def resolve(self, **changes):
        context = {'version': 1, 'submission_stage': 'submission',
                   'scopes': ['writing', 'review'], 'artifacts': ['prose', 'tex'],
                   'features': ['latex_manuscript', 'paper_prose', 'introduction', 'conclusion'],
                   'provenance': {'submission_stage': 'user'}}
        context.update(changes)
        return resolve_policy(context, self.hard, self.profiles)

    def test_execution_only_scope_cannot_claim_manuscript_readiness(self):
        resolution = self.resolve(scopes=['workflow'], artifacts=['policy'], features=[])
        self.assertEqual([], resolution['active_hard'])
        result = assess_compliance(resolution, self.hard)
        self.assertEqual('NOT_EVALUATED', result['readiness']['status'])

    def test_unmandated_sok_structure_and_author_workflow_do_not_add_blockers(self):
        resolution = self.resolve(paper_type='sok', task_mode='architecture_review')
        result = assess_compliance(resolution, self.hard)
        blockers = result['readiness']['hard_blockers']
        for retired in ['SOK.REQUIRED_CONTENT', 'STRUCT.INTRO_CONCRETE_GAP',
                        'PROSE.ABBREVIATION_FIRST_USE', 'REVIEW.ARCHITECTURE_SAFETY',
                        'ROUTE.SKILL_BOUNDARY', 'AUTOFIX.SEMANTIC_APPROVAL']:
            self.assertNotIn(retired, blockers)
        self.assertIn('CLAIM.EVIDENCE_BOUND', blockers)
        self.assertIn('FACT.NO_FABRICATION', blockers)

    def test_retired_evidence_is_rejected_instead_of_silently_reused(self):
        record = {'rule_id': 'PROSE.ABBREVIATION_FIRST_USE', 'status': 'PASS',
                  'artifact': 'main.tex', 'locator': 'paragraph 1',
                  'evidence': 'Synthetic former requirement record.', 'evaluator': 'human'}
        with self.assertRaisesRegex(ValueError, 'rule is not active'):
            assess_compliance(self.resolve(), self.hard, {'version': 1, 'hard_results': [record]})

    def test_editorial_variation_survives_while_missing_citation_still_fails(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            tex = root / 'main.tex'
            text = '\n'.join(r'\section{Part ' + str(i) + '}' for i in range(1, 9))
            text += '\n' + r'\begin{itemize}' + '\n'
            text += '\n'.join(r'\item Contribution ' + str(i) for i in range(1, 7))
            text += '\n' + r'\end{itemize}' + '\n'
            text += 'The GPU renderer executes reference.py. On Atlas-v1, B reaches 74% accuracy.\n'
            tex.write_text(text)
            active = {r['id'] for r in self.resolve()['active_hard']}
            findings, _ = lint_project(root, 'submission', active)
            self.assertEqual([], findings)
            tex.write_text(text + r'\cite{missing}' + '\n')
            findings, _ = lint_project(root, 'submission', active)
            self.assertEqual(['CITE.APPROVED_SOURCE_ONLY'], [f.rule_id for f in findings])

    def test_unused_keys_remain_located_maintenance_notes_outside_assessment(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'main.tex').write_text(r'\cite{used}\bibliography{references}' + '\n')
            (root / 'references.bib').write_text('@article{used,title={Used}}\n@article{unused,title={Unused}}\n')
            context = self.resolve()['context']
            (root / 'context.yaml').write_text(yaml.safe_dump(context))
            output = root / 'validation'
            manifest = run_validation(root / 'context.yaml', root, output)
            note = load_yaml(output / 'unused-bibtex-keys.yaml')
            self.assertTrue(note['active'])
            self.assertEqual(['unused'], note['keys'])
            self.assertEqual(2, note['entries'][0]['line'])
            self.assertEqual(0, manifest['deterministic_failing_rule_count'])
            results = load_yaml(output / 'initial-assessment.yaml')['hard_results']
            self.assertNotIn('CITE.UNUSED_KEYS_REPORTED', [r['rule_id'] for r in results])

    def test_review_hint_is_not_counted_as_a_deterministic_failure(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'main.tex').write_text(r'\eqref{custom-label}' + '\n')
            (root / 'context.yaml').write_text(yaml.safe_dump(self.resolve()['context']))
            manifest = run_validation(root / 'context.yaml', root, root / 'validation')
            self.assertEqual(1, manifest['review_hint_count'])
            self.assertEqual(0, manifest['deterministic_failing_rule_count'])
            self.assertEqual(0, manifest['total_failing_rule_count'])

    def test_current_schema_has_source_attribution_without_ballot_codes(self):
        self.assertTrue(all(r.get('source', {}).get('origin') for r in self.hard['rules']))
        doc = deepcopy(self.hard)
        doc['rules'][0]['decision_refs'] = ['A01']
        errors, _ = validate_hard_document(doc)
        self.assertTrue(any('unknown fields decision_refs' in e for e in errors))


if __name__ == '__main__':
    unittest.main()
