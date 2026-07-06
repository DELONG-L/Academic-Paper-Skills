# Reviewer Panel

Use this reference for simulated review, red-team review, or formal peer-review drafting.

## Evidence Anchors

Every criticism must include one of:

- Section, figure, table, equation, appendix, or line number.
- Short manuscript quote of at most 15 words.
- Reviewer quote if responding to external reviews.
- `MISSING: <expected content>` when the absence is the finding.
- `UNLOCATED: <concern>` only for a tentative concern that must not be treated as a hard finding.

No naked criticisms.

## Fairness Firewall

Before accepting a weakness as substantive, check whether it is an unfair or weak rejection reason.

Do not treat these as hard rejection grounds unless the paper's own claims require them:

- "Not state of the art."
- "Method is too simple."
- "The paper admits limitations."
- "The work is too narrow" without explaining why the stated claim needs broader scope.
- "The result is not surprising."
- "The authors should have used my preferred method."
- "The authors could run more experiments" without tying the experiment to a central unsupported claim.
- "Negative result" as a flaw by itself.
- "Not novel" without a concrete cited comparator.

Convert unfair items into optional suggestions or remove them.

## Simulated Reviewer Personas

### R1: Champion

Purpose: identify the strongest fair acceptance case and calibrate whether the paper has a real contribution.

Focus:
- Strongest contribution.
- Cleanest result.
- Best-positioned insight.
- What the community would learn if accepted.

Failure signal: if the champion cannot name a concrete strength, the manuscript likely has a positioning problem.

### R2: Methodological Skeptic

Purpose: stress-test soundness and evidence.

Focus:
- Missing or weak baselines.
- Ablation and mechanism attribution.
- Confounders: parameters, data, training time, tuning budget, seeds.
- Statistical support.
- Overclaims in abstract, introduction, and conclusion.
- Reproducibility gaps.

The skeptic may be blunt in Mode B for the user's own draft, but findings still need anchors and fairness checks.

### R3: Novelty/AC

Purpose: evaluate contribution delta and likely decision factors.

Focus:
- Closest prior work and novelty delta.
- Related Work completeness.
- Whether contributions are real or inflated.
- Scope, significance, and "so what".
- Consensus risks across reviewers.

## Review Report Schema

```markdown
### Reviewer: <Champion / Skeptic / Novelty-AC>

**Summary.**
<2-4 sentences proving the paper was understood.>

**Strengths.**
- <specific strength> [anchor].

**Weaknesses.**
1. [substance|misread-risk|polish] <issue> [anchor].  
   Reviewer risk: <why this could affect score>.  
   Fairness check: <passed or downgraded>.

**Questions to Authors.**
- <question likely to appear in rebuttal>.

**Indicative Scores.**
- Soundness: <score if requested>
- Clarity: <score if requested>
- Contribution: <score if requested>
- Overall: <score if requested>
- Confidence: <score if requested>
```

## AC Synthesis for Own-Draft Red Team

```markdown
## Area Chair Synthesis

**Consensus risks.**
- <issue raised by multiple personas> [anchor].

**Split opinions.**
- <where one reviewer might forgive and another might reject>.

**Decision factors.**
1. <factor most likely to decide the outcome>.
2. ...

**Predicted outcome.**
<Reject / Borderline / Accept> as simulation only, not a real decision.

**Fix list.**
- [ ] <action> [anchor] - impact: high|medium|low; cost: low|medium|high; route: paper-writing|paper-figures-tables|experiment|manual BibTeX.
```

## Formal Review Mode

When reviewing someone else's paper:

- Use one consolidated review, not adversarial personas in the final output.
- Keep tone professional, neutral, and constructive.
- Separate rejection-relevant weaknesses from suggestions.
- Make clear that the draft is for user review and final scoring responsibility stays with the user.
