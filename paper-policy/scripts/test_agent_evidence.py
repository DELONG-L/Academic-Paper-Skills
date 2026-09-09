"""Regression tests for evidence-backed agent judgments and stale dependencies."""
from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
import subprocess
import sys
import json
import yaml

from assess_compliance import assess_compliance
from evidence_sources import snapshot_sources
from lint_project import Finding, lint_tex_file
from run_project_validation import run_validation, build_evidence_worklist
import test_assess_compliance as baseline

FIXTURES = baseline.FIXTURES
SCRIPT_DIR = baseline.SCRIPT_DIR


class AgentEvidenceTests(unittest.TestCase):
    def test_unresolved_display_hint_does_not_become_deterministic_clean_pass(self):
        rid='LATEX.REFERENCEABLE_DISPLAY'
        self.assertTrue(any(x['id']==rid for x in self.resolution['active_hard']))
        result=assess_compliance(self.resolution,self.hard,
                                findings=[Finding(rid,'main.tex',1,'Unknown custom display',kind='review_hint')],
                                assessed_rules={rid},source_root=self.root)
        self.assertEqual('UNVERIFIED',self.base.result_by_id(result)[rid]['status'])

    def provenance_hint(self):
        path=self.root/'main.tex'
        path.write_text('The renderer is the method evaluated in this paper.\n')
        self.record.update(rule_id='PROSE.NO_INTERNAL_PROVENANCE',locator='main.tex line 1',
                           evidence='Renderer names the measured method, not irrelevant workflow bookkeeping.',
                           source_snapshots=snapshot_sources(self.root,['main.tex']))
        return lint_tex_file(path,self.root,'submission',{'PROSE.NO_INTERNAL_PROVENANCE'})

    def test_review_hint_without_semantic_evidence_is_unverified(self):
        hints=self.provenance_hint()
        result=assess_compliance(self.resolution,self.hard,findings=hints,
                                assessed_rules={self.record['rule_id']},source_root=self.root)
        target=self.base.result_by_id(result)[self.record['rule_id']]
        self.assertEqual('UNVERIFIED',target['status'])
        self.assertEqual([],target['findings'])
        self.assertEqual(1,len(target['review_hints']))

    def test_current_semantic_evidence_resolves_hint_but_stale_evidence_does_not(self):
        hints=self.provenance_hint()
        kwargs={'findings':hints,'assessed_rules':{self.record['rule_id']}}
        self.assertEqual('PASS',self.target(**kwargs)['status'])
        (self.root/'main.tex').write_text('Changed scientific context.\n')
        self.assertEqual('UNVERIFIED',self.target(**kwargs)['status'])

    def test_definite_failure_still_wins_when_hints_also_exist(self):
        hints=self.provenance_hint()
        findings=hints+[Finding(self.record['rule_id'],'main.tex',1,'Definite verified violation')]
        self.assertEqual('FAIL',self.target(findings=findings,assessed_rules={self.record['rule_id']})['status'])

    def test_evidence_worklist_retains_review_hint_locations(self):
        hints=self.provenance_hint()
        result=assess_compliance(self.resolution,self.hard,findings=hints,
                                assessed_rules={self.record['rule_id']},source_root=self.root)
        worklist=build_evidence_worklist(result,self.hard)
        row=next(x for x in worklist['items'] if x['rule_id']==self.record['rule_id'])
        self.assertEqual('main.tex',row['review_hints'][0]['path'])
        self.assertEqual([],row['deterministic_findings'])

    @classmethod
    def setUpClass(cls):
        baseline.ComplianceAssessmentTests.setUpClass()
        cls.base = baseline.ComplianceAssessmentTests()
        cls.hard = cls.base.hard

    def setUp(self):
        temp = TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        (self.root / 'main.tex').write_text('Observed mean: 2.\n')
        (self.root / 'results.csv').write_text('value\n1\n3\n')
        self.resolution = self.base.resolution('submission.yaml')
        self.record = {
            'rule_id': 'CLAIM.EVIDENCE_BOUND', 'status': 'PASS',
            'artifact': 'main.tex', 'locator': 'line 1; results.csv rows 2-3',
            'evidence': 'The reported mean 2 equals (1 + 3) / 2 in the supplied data.',
            'evaluator': 'agent',
            'source_snapshots': snapshot_sources(self.root, ['main.tex', 'results.csv']),
        }

    def assess(self, **kwargs):
        evidence = {'version': 1, 'hard_results': [self.record]}
        return assess_compliance(
            self.resolution, self.hard, evidence,
            source_root=self.root, **kwargs
        )

    def target(self, **kwargs):
        return self.base.result_by_id(self.assess(**kwargs))[self.record['rule_id']]

    def test_semantic_pass_is_current_and_contributes_to_readiness(self):
        self.resolution['active_hard'] = [x for x in self.resolution['active_hard']
                                          if x['id'] == self.record['rule_id']]
        result = self.assess()
        self.assertEqual('PASS', result['hard_results'][0]['status'])
        self.assertEqual('CURRENT', result['hard_results'][0]['source_verification']['status'])
        self.assertEqual('READY', result['readiness']['status'])
        self.assertIn('not human sign-off', result['readiness']['meaning'])

    def test_bare_pass_and_malformed_snapshots_are_rejected(self):
        original = deepcopy(self.record)
        for changes in [{'evidence': ''}, {'locator': ''}, {'artifact': ''},
                        {'source_snapshots': []},
                        {'source_snapshots': [{'path': 'main.tex', 'sha256': 'fake'}]}]:
            with self.subTest(changes=changes):
                self.record = {**deepcopy(original), **changes}
                with self.assertRaises(ValueError):
                    self.assess()

    def test_changed_manuscript_or_supporting_data_invalidates_pass(self):
        for name in ['main.tex', 'results.csv']:
            with self.subTest(name=name):
                path = self.root / name
                saved = path.read_bytes()
                path.write_bytes(saved + b'changed\n')
                result = self.target()
                self.assertEqual('UNVERIFIED', result['status'])
                self.assertEqual('source_evidence_unverified', result['basis'])
                self.assertIn('source changed: ' + name, result['source_verification']['issues'])
                path.write_bytes(saved)

    def test_missing_source_invalidates_pass(self):
        (self.root / 'results.csv').unlink()
        self.assertEqual('UNVERIFIED', self.target()['status'])

    def test_snapshot_must_cover_inspected_artifact(self):
        self.record['source_snapshots'] = snapshot_sources(self.root, ['results.csv'])
        self.assertEqual('UNVERIFIED', self.target()['status'])

    def test_all_referenced_artifact_files_need_snapshots(self):
        (self.root / 'plot.svg').write_text('<svg/>')
        self.record['artifact_refs'] = ['plot']
        evidence = {'version': 1, 'hard_results': [self.record], 'artifacts': [{
            'id': 'plot', 'kind': 'figure', 'artifact_types': ['data_figure'],
            'claim': 'Mean of 2', 'files': {'outputs': ['plot.svg'], 'source_data': ['results.csv']},
        }]}
        def run():
            return self.base.result_by_id(assess_compliance(
                self.resolution, self.hard, evidence, source_root=self.root
            ))[self.record['rule_id']]
        self.assertEqual('UNVERIFIED', run()['status'])
        self.record['source_snapshots'] += snapshot_sources(self.root, ['plot.svg'])
        self.assertEqual('PASS', run()['status'])
        (self.root / 'plot.svg').write_text('<svg>changed</svg>')
        self.assertEqual('UNVERIFIED', run()['status'])

    def test_unrelated_edit_does_not_invalidate_pass(self):
        (self.root / 'notes.txt').write_text('Unrelated planning notes')
        self.assertEqual('PASS', self.target()['status'])

    def test_manual_and_mixed_manual_rules_cannot_be_passed_by_agent(self):
        for rule_id in ['AUTH.INTEGRITY_PRECEDENCE', 'LATEX.PRESERVE_STRUCTURE',
                        'CITE.APPROVED_SOURCE_ONLY']:
            with self.subTest(rule=rule_id):
                self.record['rule_id'] = rule_id
                with self.assertRaisesRegex(ValueError, 'manual PASS requires'):
                    self.assess()

    def test_agent_cannot_waive_or_exclude_a_rule(self):
        for status in ['WAIVED', 'NOT_APPLICABLE']:
            self.record['status'] = status
            with self.assertRaisesRegex(ValueError, 'agent cannot assign'):
                self.assess()

    def test_agent_cannot_decide_deterministic_only_rule(self):
        self.record['rule_id'] = 'FINAL.NO_UNRESOLVED_MARKERS'
        with self.assertRaisesRegex(ValueError, 'deterministic-only'):
            self.assess()

    def test_mixed_deterministic_semantic_pass_requires_checks(self):
        self.record['rule_id'] = 'PROSE.NO_INTERNAL_PROVENANCE'
        self.assertEqual('UNVERIFIED', self.target()['status'])
        self.assertEqual('deterministic_checks_not_assessed', self.target()['basis'])
        self.assertEqual('PASS', self.target(assessed_rules={self.record['rule_id']})['status'])

    def test_deterministic_failure_wins_over_current_and_stale_pass(self):
        self.record['rule_id'] = 'PROSE.NO_INTERNAL_PROVENANCE'
        finding = Finding(self.record['rule_id'], 'main.tex', 1, 'Detected internal provenance')
        for stale in [False, True]:
            with self.subTest(stale=stale):
                if stale:
                    (self.root / 'main.tex').write_text('Changed')
                result = self.target(findings=[finding])
                self.assertEqual('FAIL', result['status'])
                self.assertEqual('deterministic_finding', result['basis'])

    def test_no_source_root_does_not_silently_use_current_directory(self):
        result = assess_compliance(self.resolution, self.hard,
                                  {'version': 1, 'hard_results': [self.record]})
        self.assertEqual('UNVERIFIED', self.base.result_by_id(result)[self.record['rule_id']]['status'])

    def test_absolute_external_source_is_supported(self):
        self.record['source_snapshots'] = snapshot_sources(
            self.root, [str(self.root / 'main.tex'), str(self.root / 'results.csv')])
        self.assertEqual('PASS', self.target()['status'])

    def test_legacy_human_record_is_explicitly_unbound(self):
        self.record['evaluator'] = 'human'
        del self.record['source_snapshots']
        self.assertEqual('PASS', self.target()['status'])
        self.assertEqual('UNBOUND', self.target()['source_verification']['status'])

    def test_optional_snapshots_also_invalidate_human_and_fail_records(self):
        for evaluator, status in [('human', 'PASS'), ('agent', 'FAIL')]:
            self.record.update(evaluator=evaluator, status=status)
            (self.root / 'main.tex').write_text('Changed')
            self.assertEqual('UNVERIFIED', self.target()['status'])

    def test_worklist_routes_semantic_and_manual_checks_separately(self):
        result = assess_compliance(self.resolution, self.hard)
        items = {x['rule_id']: x for x in build_evidence_worklist(result, self.hard)['items']}
        self.assertEqual('agent_or_human', items['CLAIM.EVIDENCE_BOUND']['suggested_evaluator'])
        self.assertEqual('human_or_user', items['AUTH.INTEGRITY_PRECEDENCE']['suggested_evaluator'])

    def test_runner_and_cli_recheck_sources_and_report_agent_passes(self):
        project = FIXTURES / 'project-submission-clean'
        self.record['source_snapshots'] = snapshot_sources(project, ['main.tex'])
        evidence_path = self.root / 'evidence.yaml'
        evidence_path.write_text(yaml.safe_dump({'version': 1, 'hard_results': [self.record]}))
        context = FIXTURES / 'context' / 'submission.yaml'
        manifest = run_validation(context, project, self.root / 'validation', evidence_path)
        self.assertEqual(1, manifest['agent_passing_rule_count'])
        self.assertIn(self.record['rule_id'], manifest['agent_passing_rule_ids'])
        self.assertEqual(0, manifest['unverified_source_rule_count'])
        # CLI uses the project root, not the evidence file's different directory.
        proc = subprocess.run([sys.executable, str(SCRIPT_DIR / 'assess_compliance.py'),
                               str(context), '--project', str(project), '--evidence',
                               str(evidence_path), '--format', 'json'], capture_output=True, text=True)
        self.assertEqual(1, proc.returncode, proc.stderr)  # Other rules still need evidence.
        assessed = self.base.result_by_id(json.loads(proc.stdout))
        self.assertEqual('PASS', assessed[self.record['rule_id']]['status'])
        self.record['source_snapshots'][0]['sha256'] = '0' * 64
        evidence_path.write_text(yaml.safe_dump({'version': 1, 'hard_results': [self.record]}))
        manifest = run_validation(context, project, self.root / 'stale-validation', evidence_path)
        self.assertEqual(0, manifest['agent_passing_rule_count'])
        self.assertEqual(1, manifest['unverified_source_rule_count'])


if __name__ == '__main__':
    unittest.main()
