# Reduce Over-Defensive Writing

Use when manuscript prose repeatedly apologizes, disclaims ambitions, or weakens
supported findings. The aim is confident, bounded reporting. These are editorial
judgments, not new policy violations or a quota for negative sentences.

## Default: State the Finding

In ordinary manuscript prose, report what the evidence establishes and state
the relevant experimental conditions as part of that report. Do not volunteer
what the result cannot establish in anticipation of an unasked objection.
A logically true disclaimer is not automatically useful writing. The possibility
that someone could demand a broader claim does not justify preemptive defense.

If a claim is too broad, narrow the claim itself instead of following it with
an excuse. Report actual adverse findings and conditions needed for the claim
to hold. Discuss material validity issues in the appropriate scientific context;
answer specific objections in author responses when they arise. Explicit venue
disclosures still apply. None of these calls for cataloguing every untested
setting next to an otherwise accurate result.

## Decide What the Sentence Does

Read the claim and its local context before changing a caveat.

| Function | Editorial action |
|---|---|
| Reports a negative finding, material uncertainty, or a limitation relevant to the stated contribution | Retain the scientific content in its appropriate context |
| Lists broader conclusions the result cannot support, without a specific question or an actual overclaim | Remove the anticipatory defense; let the accurate, scoped claim stand |
| Reveals that the current claim is false or too broad without a condition | Correct the claim directly and include the condition it requires |
| Explains an actual design choice or names excluded conditions | Preserve the reason and the exact conditions |
| Repeats a boundary already clear to this reader | Merge or shorten if no information or necessary emphasis is lost |
| Apologizes for not solving an unspecified larger problem | Remove the apology; state the supported contribution and its actual scope |

An author's negative phrasing is a candidate for review, not evidence that the
sentence is unnecessary. Conversely, a positive sentence can still be empty
self-justification. Judge what the reader learns.

## Calibrate Confidence at the Claim Level

Separate what was measured from what it might mean. Report an observed value
directly in its measured setting; qualify the uncertain explanation, comparison,
or extrapolation. Having data does not remove sampling uncertainty or establish
causality. Avoid stacking several hedges around the same uncertainty.

For example, given a single split with B at 74% and A at 71%:

> On the evaluated split, B achieved 74% accuracy, compared with 71% for A.

Stop there when this is the result being reported. Do not append “This result
does not establish performance across datasets or variability across runs”
without a concrete reason to address that question. A direct reviewer question
about generalization warrants a direct answer; an ordinary result sentence does
not need to rehearse that exchange. Do not expand the observation into a general
superiority claim either.

Remove unsupported self-assessments such as “merely a small step” when they add
no scientific information. Retain limitations that materially affect validity
or usefulness, even when they are unfavorable. A request for more confident
writing never licenses suppressing those limitations.

## Place Boundaries Where Readers Need Them

Prefer a concise condition attached to the relevant claim when it is sufficient.
Use an explicit negative statement to report a relevant negative fact, not to
anticipate every possible inference. “We evaluate static attacks” describes the
evaluation. An established inability to support adaptive attacks is a different
fact: retain it where it materially describes the method, but do not invent it
or append it simply because adaptive attacks were not evaluated.

Repeated wording can be shortened; repeated information can be necessary.
An abstract must stand alone, a result may need its own scope condition, and
separate reviewer responses may each need a complete answer. There is no fixed
number of allowed homes, and caveats may lead or end a paragraph when their
function warrants it. Do not add a limitation sentence just to complete a template.

For cross-section removal, inspect the proposed surviving location and confirm
that it retains the full information and remains accessible to the reader.
With only one passage available, edit locally; do not assume an unseen section
contains the missing qualification. A forward reference cannot replace a
condition needed to interpret the current result correctly.

## Author Responses

Answer the actual concern, give the evidence, and identify any supported action.
Remove repetitive apologies and arguments about the authors' intentions. Keep
courtesy, substantive disagreement, acknowledged limits, and honest revision
status. Directness does not require a clipped “No.” or deletion of a reasoned
response. Do not invent a reviewer concern to justify manuscript disclaimers.

## Final Comparison

Check whether the revision changed the population, conditions, exclusions,
uncertainty, causal status, or commitment. A shorter positive statement is not
automatically equivalent to the negative original. Return the revised prose;
explain only substantive changes or an unresolved boundary.

Related guidance: [prose-pattern-audit.md](prose-pattern-audit.md) for broader
formulaic-prose cleanup. This reference selectively adapts the semantic
distinctions in claude-scholar's [over-defensive writing](https://github.com/OniReimu/claude-scholar/blob/d5eb9fc2e46128fccaf0a198519035c752f358b7/policy/rules/prose-over-defensive.md)
and [hedging discipline](https://github.com/OniReimu/claude-scholar/blob/d5eb9fc2e46128fccaf0a198519035c752f358b7/policy/rules/prose-hedging-discipline.md),
with contextual placement and evidence calibration rather than fixed style limits.
