# Section Architecture

Use this for outlines, section naming, and paper structure.

## Top-Level Section Names

When `STRUCT.TRADITIONAL_HEADINGS` is active, top-level section names must be
traditional and concise. Otherwise use the following names as safe defaults:

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

Avoid rhetorical or decorative top-level titles:

- `Towards ...`
- `Rethinking ...`
- `A Unified Journey ...`
- `Why Does X Matter?`
- `From X to Y`
- long colon titles
- metaphorical titles

When the strict heading rule is disabled, use these phrases only when they
improve navigation rather than as automatic novelty signals.

## Default Structure

For ML, systems, and security papers, start from this structure and adapt only when the venue or paper type requires it:

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
- Do not exceed the venue's sectioning convention. Apply the 5--7 section range only when `STRUCT.SECTION_COUNT_PROFILE` or `STRUCT.SECTION_COUNT` is enabled.
- Merge thin `Preliminaries` into `Background and Related Work`.
- Do not create a subsection for one paragraph.
- Use inline bold paragraph heads for short local distinctions.
- Place limitation analysis where the venue and argument support it. Require the key boundary in Conclusion only when `STRUCT.CONCLUSION_INTEGRATES_LIMITATIONS` is active, and require one paragraph only when `STRUCT.CONCLUSION_SINGLE_PARAGRAPH` is active.
- Keep section numbering consistent with the template. Do not mix numbered and unnumbered main sections unless the venue template requires it.
- For venues requiring Ethics, Broader Impact, Limitations, or Reproducibility statements, include them with traditional concise headings.

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

- State the corpus, search boundary, or screening method when the paper claims coverage.
- Use a taxonomy or comparison axes that can be audited by the reader.
- End with concrete research directions rather than a generic future-work list.

For security or protocol papers:

- Separate threat model, system model, and method when the distinction affects claims.
- Present constructions with explicit primitives, assumptions, and procedures.
- Do not imply cryptographic guarantees for empirical or interface-level mechanisms.
