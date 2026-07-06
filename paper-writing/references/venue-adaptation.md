# Venue Adaptation

Use this only when the user asks for venue-aware writing or the target venue is known.

## Scope

Venue adaptation affects structure, required statements, checklists, anonymity, page budget, and section emphasis. It does not override the house style unless the venue requires a specific format.

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
- Include at least one comparison table aligned with the taxonomy.
- End with concrete research agenda items.

## Anonymity and Submission

For double-blind submissions:

- Remove acknowledgments.
- Avoid identifying repository URLs.
- Cite prior work in third person if it identifies the authors.
- Avoid paper-body meta language such as `our previous work` unless anonymized correctly.

## Page Budget

When space is tight:

- Keep section names traditional.
- Merge Background and Related Work.
- Move exhaustive tables, examples, or proofs to the appendix.
- Keep the main Related Work comparison table if it carries the gap argument.
