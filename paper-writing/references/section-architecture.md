# Section Architecture

Use this for outlines, section naming, and paper structure.

For post-draft paragraph decisions and cross-section relocation, use
`../../paper-review/references/argument-structure.md`. This reference covers
writing-time organization; that workflow checks an existing draft's structure
and provides a located edit plan at the requested scope.

## Top-Level Section Names

Use concise names that make the section function clear. Adapt them when a precise topic-specific heading improves navigation or
follows a venue requirement. The following names are useful defaults:

- Introduction
- Background
- Related Work
- Background and Related Work
- Preliminaries
- Problem Formulation
- System Model
- Threat Model
- Method
- Methodology
- Approach
- Design
- Implementation
- Experiments
- Evaluation
- Results
- Discussion
- Limitations
- Conclusion

The following title forms need a clear navigational purpose; their wording alone is not a violation:

- `Towards ...`
- `Rethinking ...`
- `A Unified Journey ...`
- `Why Does X Matter?`
- `From X to Y`
- long colon titles
- metaphorical titles

Retain a precise topic-specific or question heading when it clarifies the section function. Revise decorative
headings that obscure that function or violate a sourced project requirement.

## Default Structure

For ML, systems, and security papers, the following is a starting example. Adapt order and grouping to the argument, evidence, reader navigation, paper type, and applicable venue requirements:

```text
1 Introduction
2 Background and Related Work
3 System Model
4 Method
5 Experiments
6 Discussion
7 Conclusion
```

For SoK or survey papers:

```text
1 Introduction
2 Background and Scope
3 Methodology
4 Taxonomy
5 Comparative Analysis
6 Research Agenda
7 Conclusion
```

For measurement papers:

```text
1 Introduction
2 Background and Related Work
3 Dataset and Methodology
4 Measurement Results
5 Discussion
6 Conclusion
```

## Section Discipline

- Keep top-level sections few and predictable.
- Follow explicit project and sourced venue sectioning requirements. Choose section count and hierarchy from the explanatory dependencies and navigation needs.
- Merge thin `Preliminaries` into Background when this improves navigation; retain a distinct section when definitions or the template give it a clear role.
- Retain a short subsection for a distinct formal artifact or a venue requirement; paragraph count alone is not a failure criterion.
- Prefer a short paragraph heading for a local distinction when it improves navigation, following the manuscript formatting convention.
- Place material limitation analysis where the venue and argument support it. A compact Conclusion can finish with a supported finding or implication when its scope is clear. Separate Limitations sections and multiple conclusion paragraphs are valid.
- Keep section numbering consistent with the template. Do not mix numbered and unnumbered main sections unless the venue template requires it.
- For venues requiring Ethics, Broader Impact, Limitations, or Reproducibility statements, use the names and placement required by the verified venue or template.

## Roadmaps

Keep end-of-introduction roadmaps short. Remove them when the Introduction already contains the gap, RQs, method overview, contribution list, and a clear section order.

## Argumentative Spine

Choose one central distinction, mechanism, or inferential chain that explains
why the sections appear in their order. Carry it from the Introduction through
the method and evidence organization into Results, Discussion, and Conclusion.

For dependent RQs, order them by what each RQ establishes for the next and
state that dependency in a short Results transition. For independent RQs, keep
them as parallel branches under one contribution claim; do not invent a causal
or logical dependency merely to make the outline look linear.

## Special Paper Types

For SoK or survey papers:

Choose a structure that explains how knowledge is organized and what the synthesis
establishes. Taxonomies, comparison frameworks, corpus selection methods and a
research agenda can help, but no particular combination is universally required.
Make the evidence-selection basis clear enough to assess the stated synthesis;
retain selection facts needed to interpret conclusions. Apply a mandated section
or content item only when an explicit project or verified venue source requires it.

For security or protocol papers:

- Separate threat model, system model, and method when the distinction affects claims.
- Present constructions with explicit primitives, assumptions, and procedures.
- Do not imply cryptographic guarantees for empirical or interface-level mechanisms.
