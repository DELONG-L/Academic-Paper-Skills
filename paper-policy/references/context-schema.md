# Paper Context And Resolution

## Context File

Use `paper_context.yaml` when running a reproducible policy audit or formal
submission-readiness assessment. Ordinary prose work can apply relevant
constraints from its supplied context without a YAML file. For substantial or
resumed work, persist context when it helps continuity; task size alone does not
make workflow files an acceptance criterion. CLI resolution still requires the
validated mapping described below.

```yaml
version: 1
paper_type: empirical
domain: machine_learning
venue: ExampleConf 2027
submission_stage: draft
language: en
double_blind: true
task_scope: multi_section
task_mode: writing
artifact_mode: [final_figure, final_table]
experiment_type: stochastic
measurement_bias_status: known_systematic
evidence_structure: multi_role
scopes: [writing]
artifacts: [prose, tex]
features: [paper_prose, latex_manuscript, threats_to_validity]
approved_citation_sources: [local_bib, user_notes]
primary_tex: paper.tex
additional_tex: [supplement/SupplementaryMaterial.tex]
venue_sources:
  - id: official-submission-rules
    kind: official
    locator: https://example.org/cfp
    as_of: 2026-07-11
    constraints: [page_limit, anonymity, appendix]
  - id: supplied-template
    kind: template
    locator: templates/exampleconf2027.sty
    as_of: 2026-07-11
    constraints: [formatting, section_numbering]
provenance:
  venue: official
  submission_stage: user
  double_blind: template
```

Unknown fields and unknown controlled values are rejected to catch
misspellings. Optional scalar fields may be omitted. `scopes` and `artifacts`
are required non-empty lists because they control applicability.
`approved_citation_sources` and `modes` are optional lists of non-empty strings.
Writing state, page pressure and layout choices can stay in the task context or
working notes; they require no policy profile.
`features` is optional only for genuinely short, untyped work; section,
artifact, multi-section, full-paper, polish, submission, and rebuttal scopes
must declare at least one semantic selector.

Use `primary_tex` to identify the authoritative main manuscript when the project
contains flattened submission copies, Overleaf mirrors, venue examples,
archived drafts, or multiple independent TeX documents. `additional_tex` may
list independent supplementary/checklist roots that should also be linted and
included in artifact discovery. Input/include descendants are followed
automatically, and only bibliographies referenced by the selected TeX trees are
audited. If `primary_tex` is omitted, the runner uses root-level `main.tex` or a
single unambiguous document root; multiple roots otherwise produce an error
instead of being merged silently.

Keep two inventories separate:

- `artifacts` contains generic kinds only: `policy`, `prose`, `tex`, `bibtex`,
  `figure`, `table`, or `paper_outline`.
- `features` contains semantic selectors: `abstract`, `introduction`,
  `conclusion`, `contribution_list`, `evaluation_section`, `related_work`,
  `related_work_table`, `result_table`, `data_table`, `latex_manuscript`,
  `paper_prose`, `paper_figure`, `data_figure`, `conceptual_figure`,
  `generated_conceptual_figure`, `threats_to_validity`, or
  `limitations_content`. Add `generated_conceptual_figure` together with
  `conceptual_figure` whenever a generative image model produces the final
  conceptual artifact; omit it for Graphviz, Mermaid, TikZ, or manually authored
  SVG figures.

Use `measurement_bias_status: known_systematic` when the manuscript identifies
a characterized systematic measurement, extraction, missingness, or labeling
error. Use `evidence_structure: multi_role` when substantive, validation,
calibration, control, case-study, or exploratory evidence coexist and must not
silently exchange claim roles. Add `threats_to_validity` or
`limitations_content` to `features` whenever the requested scope contains
load-bearing threat or limitation analysis.

## Controlled Task Modes

Canonical modes are:

`writing`, `figure_creation`, `related_work_full`,
`background_and_related_work_full`, `citation_audit`,
`final_citation_check`, `reproducibility_check`, `submission_readiness`,
`paper_run_final`, `architecture_review`, `cold_reader`,
`comprehension_test`, `anti_ai_cleanup`, `prose_cleanup`, `writing_anti_ai`,
`authorship_review`, `detector_review`, `self_review`, `formal_review`,
`external_review_analysis`, `rebuttal`, `revision_verification`,
`synthetic_results`, `placeholder_results`, `style_mining`,
`semantic_mutation`, `bibliography_rewrite`, and `autofix`.

Accepted aliases are normalized and reported in `context_warnings`:

- `anti-ai-cleanup` -> `anti_ai_cleanup`
- `writing-anti-ai` -> `writing_anti_ai`
- `prose-polish` or `prose_polish` -> `prose_cleanup`
- `pre_submission_audit` or `reviewer_panel` -> `self_review`
- `style-mining` -> `style_mining`

Registry files must use canonical values. Unknown modes fail context or
registry validation instead of silently suppressing activation.

## Provenance

Allowed provenance values are:

- `user`: directly stated by the user.
- `official`: read from an official venue source.
- `template`: read from the supplied venue template or checklist.
- `manuscript`: read from the manuscript project.
- `inferred`: a cautious model inference.

`venue`, `double_blind`, and `submission_stage` are hard-sensitive fields. They
activate profiles or venue hard rules only when their provenance is present and
is not `inferred`. Missing or inferred provenance is reported in
`unverified_context` and never silently activates those hard rules.

`venue_sources` is a non-empty list when present. Each record requires a stable
lowercase `id`, `kind: official | template | user`, a `locator`, an `as_of`
date, and one or more controlled `constraints`: `all`, `page_limit`,
`anonymity`, `mandatory_statements`, `section_numbering`, `appendix`,
`formatting`, or `submission_process`. Official locators must be HTTP(S) URLs;
template locators may be local project paths. Keep records separate when a
supplied template establishes formatting while an official page establishes
submission or page-limit rules.

The legacy singular mapping `venue_source: {url, as_of}` remains accepted and
is normalized to one `official` source with `constraints: [all]`. Do not provide
both forms.

If a trusted `venue` is specified, `VENUE.CONSTRAINT_PROVENANCE` activates even
when source coverage is incomplete. A template-only record is preserved but
does not silently stand in for a current official or explicit user-provided rule
source; the resolver reports that gap as a context warning.

## Resolution Semantics

1. Validate the requirement registry, activation profiles and context.
2. Match profiles by exact value; list-valued context intersects `any_of`.
3. Refuse provenance-sensitive matches from missing or inferred provenance.
4. Activate requirements from `always`, trusted profiles or exact conditional
   matches for stage, mode, paper type, venue and feature.
5. Filter by phase, scope and artifact applicability.

Resolver output lists active rules and activation reasons only. It does not
claim manuscript compliance, assign PASS, or apply fixes.

## Source Priority

Resolve context in this order:

1. Direct user statements.
2. Supplied manuscript, template, checklist, and official venue files.
3. Cautious inference.

Inference may guide editorial choices. It must not silently activate venue,
anonymity, or submission hard rules.
