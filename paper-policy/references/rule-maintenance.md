# Maintain Rules and Their Consumers Together

Use when adding, changing, retiring, or auditing policy and writing guidance.
Keep YAML registries authoritative for policy IDs and activation. Editorial
workflows can live in references without becoming new rule IDs.

## Make the Decision Reviewable

For a nontrivial rule change, record the actual failure it addresses, its source,
applicability, hard/soft force, check type, allowed adaptations, and likely false
positives. Add an example requiring a fix and one that must survive unchanged.
Use an existing change record; do not require a new file for every preference.

Distinguish a verified venue requirement from an author preference or a source
repository's convention. Avoid introducing a numerical style threshold because
it is easy to count. Before adding a rule, check whether an existing rule or
reference already owns the decision.

## Trace the Impact

Search the exact rule ID and the old wording across the affected skills,
references, examples, policy sets, profiles, tests and output templates. Record
the relevant consumer locations. When semantics or force changes, update the
actual advice as well as the ID; a valid reference can still repeat an obsolete
prohibition. Remove contradictory examples rather than adding another exception.

Use `../scripts/audit_skill_integration.py` with the shared skills directory to
find unknown inline rule IDs and broken explicit local reference paths, and to
produce a rule-to-document index. This is structural maintenance, not a semantic
style checker or a manuscript readiness assessment. Inspect the report's coverage.

## Check at the Right Level

- Validate registry structure with `validate_registry.py` after registry changes.
- Validate changed entrypoints and explicit references after documentation changes.
- Run affected behavior tests when changing code or activation behavior.
- For an editing workflow, exercise realistic tasks with defects, required
  preservation cases and an ordering case. Compare actual outputs and reasons.
  Include an unchanged or deliberately incorrect control where a scorer is used.
- An independent run needs independent context and an authorized evaluator. Label
  same-agent demonstrations honestly; passing a reference output is a scorer
  check, not a successful model run.

Do not verify editing quality by matching the desired reasoning vocabulary.
Numeric preservation needs method/metric/condition associations, not just a bag
of numbers. A correct deletion with a wrong reason is a workflow concern.

## State Coverage and Residual Uncertainty

Every check report should distinguish what it inspected from what it cannot
decide. A regex locator finds candidates, not semantic violations. No hits can
mean the target text was omitted or a pattern missed the wording. Verify a known
positive and a legitimate negative before trusting a new scanner.

Check all three consumers of a decision: registry requirement/default, task
guidance and examples, and executable diagnostics. An entrypoint can be correct
while a deep checklist or CLI still enforces an obsolete preference. Do not
label the system consistent from path/ID validation alone. Keep uncertain
`review_hint` records separate from definite findings throughout assessment and
worklist generation; verify that hints neither force FAIL nor supply PASS.

For TeX, select the actual input tree with the existing `project_files.py` logic;
inspect unresolved macro-based includes rather than silently assuming coverage.
Preserve escaped percentages, line locations, and phrases split across lines.
Do not strip arbitrary dollar-delimited text with a regex that can swallow prose.
Captions, tables, supplements and macros may need explicit inspection; the source
projection is not a TeX interpreter. Compare with the rendered artifact when
source extraction cannot establish what the reader sees.

Keep deterministic failure precedence, manual-check authority and source-snapshot
invalidation intact. Reuse unchanged results only for unchanged dependencies.
Deliver the patch, relevant checks and precise remaining limits; stop adding
unrelated rules once the authorized change is complete.
