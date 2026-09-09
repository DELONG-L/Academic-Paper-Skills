# Prose Pattern Audit

Use this reference when revising academic prose that feels formulaic,
over-produced, generic, or recognizably model-shaped to a reader. Diagnose the
text, not its author. Do not use this audit to predict or evade automated
detectors.

Use the same functional criteria for English and Chinese. Phrases such as
“值得注意的是”, “具有重要意义”, or “不仅……而且……” invite inspection only when
they add no useful relation or information. A familiar phrase alone is no defect.

## Non-Negotiable Preservation

Before editing, identify and preserve:

- claim strength and causal status;
- evidence scope, population, setting, and evaluation boundary;
- citations and the claims each citation supports;
- numbers, units, equations, labels, references, and LaTeX macros;
- technical terms, method names, variable identities, and taxonomy labels;
- limitations, uncertainty, exceptions, and negative results.

Never add facts, citations, experiments, personal experiences, names, dates, or
other specifics merely to make prose seem less generic. Use a bracketed
placeholder when a concrete fact is necessary but unavailable.

Preserving meaning does not certify an unsupported original claim. If cleanup
reveals a factual or inferential problem, distinguish it from style: flag it in
a style-only task, or make an evidence-supported correction when revision is
in scope and disclose the substantive change. Never silently strengthen a claim
to make the writing sound confident.

## Diagnostic Families

Treat each item as a revision candidate, not a forbidden token. Revise it when
it obscures the claim, repeats across the passage, or adds presentation without
information.

### Paragraph Function and Empty Reasoning

Ask what the paragraph contributes: a definition, motivation, observation,
explanation, boundary, or needed navigation. If only generic importance remains,
remove the filler or use supplied evidence to make the point concrete. Do not
polish it into more fluent filler or invent a mechanism to rescue it.

Check whether a stated reason adds information beyond its conclusion: “the
framework is effective because it delivers effective outcomes” explains nothing.
Read setup sentences with the sentences that fulfill them; a topic sentence,
definition, transition, or required disclosure need not add a new empirical
finding of its own. Preserve useful navigation and necessary restatement.

When a paragraph needs merging, relocation, or deletion, use
`../../paper-review/references/argument-structure.md` at the smallest useful scope.
Complete the authorized structural change before polishing retained sentences;
do not make an empty paragraph more fluent and leave it in place.

### Inflated or Generic Framing

Flag stock framing such as `it is important to note`, `at its core`, `in
today's ... landscape`, `plays a crucial role`, `stands as a testament`, and
signposted conclusions that merely restate the section. Delete the frame or
replace it with the specific object, mechanism, measurement, or boundary.

Treat promotional adjectives and figurative nouns cautiously: `pivotal`,
`groundbreaking`, `transformative`, `seamless`, `robust`, `vibrant`,
`ecosystem`, `landscape`, `realm`, `journey`, and `tapestry`. Retain a term when
it has a defined technical meaning. Otherwise name the measurable property:
for example, replace `robust` with the tested perturbation range or failure
condition.

Prefer precise verbs over inflated substitutes: `uses`, `defines`, `measures`,
`compares`, `reduces`, `limits`, and `shows` are usually clearer than
`leverages`, `utilizes`, `showcases`, `underscores`, or `revolutionizes`.

### Formulaic Constructions

Check for clusters of:

- decorative negative parallelism (`not merely X, but Y`) where X is not a
  meaningful excluded alternative;
- repeated three-item lists chosen for cadence rather than completeness;
- rhetorical question-and-answer forms (`The result? ...`) and false suspense;
- copula avoidance (`serves as`, `stands as`, `functions as`) where `is` or
  `has` is exact;
- sentence-final participial clauses that append vague significance, especially
  `highlighting`, `underscoring`, and `ensuring`;
- false ranges (`from X to Y`) whose endpoints do not define a real spectrum;
- stacked hedges that blur the actual evidence boundary;
- vague authority (`studies show`, `experts argue`) without a named citation;
- analogies or newly coined labels that decorate a straightforward mechanism;
- grand claims about a field, era, or societal transformation unsupported by
  the reported evidence.

Keep a pattern when it performs technical work. A negative contrast may define
scope, a parallel list may support auditability, and repetition may be required
for terminology stability.

For a newly coined compound label, check whether it names a stable, defined
concept used by the argument. Remove disposable labels that add no distinction;
retain established technical compounds and explicit author-defined terminology.

### Structure and Rhythm

Audit paragraphs before polishing sentences:

- Shorten previews and recaps that add no navigation or interpretation. Preserve
  self-contained abstracts and restatements needed to follow a later argument.
- Delete assignment echoes such as `This section will discuss ...` unless the
  document genuinely needs a roadmap.
- Organize by objects, mechanisms, evidence, or boundaries. Retain numbered
  sequencing when the order or enumeration helps the reader.
- Merge repeated restatements of one point.
- Vary sentence length when the prose has a metronomic cadence, but do not add
  dramatic fragments or choppy slogans.
- Vary repeated sentence openings when doing so preserves the grammatical
  subject and technical identity.
- Give each paragraph one main job; do not force every paragraph into an
  identical topic-evidence-summary template.
- End on the paragraph's bounded result, mechanism, implication, or limitation
  rather than a generic uplift or recap.

### Evidence and Voice

- Avoid imaginary weak competitors or hypothetical readers invented to stage a
  contrast. Use the actual comparator and supported distinction.
- Resolve ambiguous pronouns and overloaded technical words from context. Keep
  established terms such as soundness, positive values, or fair bits when their
  definitions are clear; do not replace technical meaning with a superficially
  smoother but different term.
- Check subject-verb separation and old-to-new information flow when a sentence
  is hard to parse. Choose emphasis from the argument, without a fixed sentence
  length, topic-sentence position, or punctuation quota.

- Replace generic referents such as `prior studies`, `various datasets`, or
  `many approaches` with supported citations or scoped nouns already available
  in the manuscript.
- Separate descriptive observations from causal explanations.
- Remove automatic both-sides balancing and anticipatory disclaimers. State the
  supported finding directly with its relevant conditions; do not replace empty
  balancing with a list of broader claims the paper never made.
- Keep measured first-person statements when they identify an author decision,
  definition, or scope choice.
- Preserve deliberate terminology repetition. Do not introduce synonyms for a
  method, variable, class, or threat merely to create surface variety.

For repeated disclaimers or stacked hedges, read
[over-defensive-writing.md](over-defensive-writing.md). State measurements
directly; keep appropriate uncertainty on interpretations and extrapolations.

## Check the Revision, Not Just the Original

Compare changed spans with their source and neighboring prose:

- Retain the academic register and the specificity of technical objects. Plain
  language is welcome; replacing a precise mechanism with a conversational
  generality is not an improvement. Reuse established manuscript terms where
  they fit instead of manufacturing synonyms.
- Check connective meaning: a design motivation, logical consequence, empirical
  association, and causal finding are different relations. Changing `so` to
  `therefore`, or “因此” to another connector, does not repair an unsupported
  inference. Preserve the relation the evidence warrants.
- Check for newly uniform openings, transitions, positive scope formulas, or
  paragraph endings introduced by the cleanup itself. Do not replace one
  repeated template with another, or target sentence-length or punctuation quotas.
- Stop when no concrete reader-facing problem remains within the requested
  scope. Unchanged technical prose is an acceptable outcome; a flagged word or
  a remaining negative sentence does not justify another editing pass.

## Audit Workflow

1. State the passage's job in one line: claim, mechanism, comparison, result,
   limitation, or transition.
2. Record immutable content: claims, causal verbs, citations, numbers,
   technical terms, and caveats.
3. Mark repeated diagnostic families. A single ordinary occurrence usually
   needs no intervention; clusters deserve attention, not an automatic verdict.
4. Re-architect duplicate or generic paragraph structure before replacing
   individual words.
5. Replace vague language with evidence already present. If the needed detail
   is absent, retain a scoped statement or use a bracketed placeholder.
6. Compare source and revision for claim strength, causality, scope, citations,
   values, terminology, exclusions, limitations, and academic register.
7. Return the revision first. Add a short change note only when requested or
   when a preserved pattern or unresolved placeholder needs explanation.

## Completion Check

Confirm that the revision:

- reads as academic prose rather than a performance of informality;
- contains no invented evidence or humanizing detail;
- removes repeated filler, vague significance markers, and redundant summary;
- uses sentence and paragraph rhythm appropriate to the section;
- retains necessary hedges and technical repetition;
- preserves every load-bearing scientific claim and boundary;
- makes no claim about authorship or detector performance.
