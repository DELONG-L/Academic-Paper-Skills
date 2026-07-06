# Section Architecture

Use this for outlines, section naming, and paper structure.

## Top-Level Section Names

Top-level section names must be traditional and concise. Prefer:

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

These phrases may appear in prose if they carry real meaning, but not as top-level section names.

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
- Do not exceed the venue's sectioning convention. If no venue-specific convention is supplied, keep the main paper around 5--7 top-level sections plus Abstract and References.
- Merge thin `Preliminaries` into `Background and Related Work`.
- Do not create a subsection for one paragraph.
- Use inline bold paragraph heads for short local distinctions.
- Put limitations in `Discussion` or a dedicated `Limitations` section, not as a vague ending to the conclusion.
- Keep section numbering consistent with the template. Do not mix numbered and unnumbered main sections unless the venue template requires it.
- For venues requiring Ethics, Broader Impact, Limitations, or Reproducibility statements, include them with traditional concise headings.

## Roadmaps

Keep end-of-introduction roadmaps short. Remove them when the Introduction already contains the gap, RQs, method overview, contribution list, and a clear section order.

## Special Paper Types

For SoK or survey papers:

- State the corpus, search boundary, or screening method when the paper claims coverage.
- Use a taxonomy or comparison axes that can be audited by the reader.
- End with concrete research directions rather than a generic future-work list.

For security or protocol papers:

- Separate threat model, system model, and method when the distinction affects claims.
- Present constructions with explicit primitives, assumptions, and procedures.
- Do not imply cryptographic guarantees for empirical or interface-level mechanisms.
