# Venue Adaptation

Use this only when the user asks for venue-aware writing or the target venue is known.

## Scope

Venue adaptation affects structure, required statements, checklists, anonymity, page budget, and section emphasis. Apply verified venue requirements and adapt presentation preferences to the paper; preferences do not require an exception procedure.

Record the official source, access date, year/track/article type, and applicable
submission stage for actual requirements. Check page/word counting, bibliography,
supplement and display-item rules individually. The topic notes below are writing
considerations, not a current venue checklist or a fixed page-limit table.

For template preparation or conversion, use `template-migration.md`. For journal
submissions, check whether the actual article type requires a significance
statement, end-positioned Methods, extended data, reporting checklist, cover
letter, or data/code availability statement. Draft only applicable materials and
use verified author facts for declarations. Conferences and journals both vary;
do not infer requirements from their names alone.

## Common Venue Adjustments

NeurIPS, ICML, and ICLR:

- Keep claims tied to evidence.
- Include limitations and reproducibility details.
- Report statistical variation where experiments are involved.
- Keep broad-impact or ethics material where required by the venue.

ACL and NLP venues:

- Keep dataset, annotation, evaluation, and error analysis explicit.
- Be careful with human-subject, data license, and model-use statements.

Security and systems venues:

- Make assumptions, threat model, deployment boundary, and attacker capability explicit.
- Separate mechanism, security analysis, and evaluation.
- Use comparison tables to clarify adjacent defenses and measurement scopes.

SoK or survey submissions:

- State corpus construction and screening criteria.
- Build an explicit taxonomy.
- Use a taxonomy-aligned comparison table when it adds value; axis-based prose
  can be sufficient under the shared soft comparison preference.
- End with concrete research agenda items.

## Anonymity and Submission

For double-blind submissions:

- Apply the verified anonymity requirements to acknowledgments and metadata.
- Avoid identifying repository URLs.
- Cite prior work in third person if it identifies the authors.
- Preserve correct bibliographic identity unless the venue specifically requires
  anonymization; do not blanket-replace self-citations with Anonymous entries.
- Avoid paper-body meta language such as `our previous work` unless anonymized correctly.

## Page Budget

When space is tight:

- Keep section names traditional.
- Merge Background and Related Work.
- Move exhaustive tables, examples, or proofs to the appendix.
- Keep the main Related Work comparison table if it carries the gap argument.
