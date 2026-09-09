# Rebuttal Strategy

Use this reference after reviewer comments have been atomized into issue cards.

## Core Principle

Evidence beats rhetoric. If the reviewer asks for support that is central to the paper's claim, prefer a concrete result, derivation, limitation, or manuscript change over a long argumentative defense.

## Reviewer Intent Step

Before writing a response, infer:

- What is the reviewer actually worried about?
- What evidence would change their mind?
- Is this reviewer likely pivotal: low or borderline score, addressable concerns, or high confidence?
- Is the issue a real flaw, a misread-risk caused by unclear writing, or a preference that should be downgraded?

Do not overfit to psychology. The response must still be grounded in paper evidence and user-confirmed facts.

## Response Modes

### Accept

Use when the reviewer is right and the fix is feasible.

Pattern:
- Acknowledge the point.
- State the concrete revision or already-completed result.
- Identify manuscript location.

### Clarify

Use when the paper already contains the answer but it was too hidden or unclear.

Pattern:
- Thank the reviewer.
- Clarify without blaming them.
- Point to existing evidence.
- Promise a visibility or wording improvement.

### Defend

Use sparingly when the current choice is correct and changing it would be inappropriate.

Pattern:
- Acknowledge the concern.
- Explain the design constraint or research-question alignment.
- Provide evidence or a concrete mechanism.
- Add a manuscript clarification if possible.

### Experiment

Use when new empirical evidence is central and feasible.

Rules:
- Cite completed results only after inspecting supplied or already accessible
  evidence within the task's scope.
- If evidence is missing, identify the required result and draft supported parts.
  A proposed experiment needs the applicable authorization before execution or a
  commitment in the response; do not automatically ask the user to run it.
- Do not invent expected gains, p-values, runtime, or table entries.

### Narrow Concession

Use when part of the reviewer concern is correct, but the main claim survives.

Pattern:
- Concede the local point.
- State what remains true.
- Narrow the claim or scope.
- Add a limitation or revised wording.

### Scope Boundary

Use when a requested experiment or comparison is outside the paper's research question.

Rules:
- Explain the boundary technically, not defensively.
- If useful, add it to limitations or future work.
- Do not use "out of scope" as a way to dodge a central claim.

### Citation Support Needed

Follow `citation-and-evidence-policy.md`: resolve public sources when literature completion or citation verification is in scope, and use a manual-source request only for an inaccessible source or a closed corpus. Keep unsupported promises out of the rebuttal.

## Feasibility Filter

Do not promise:

- New large-scale training from scratch.
- New data collection.
- Major architectural redesign.
- New theorem or proof not already derived or user-approved.
- New numerical claims without results.
- New citation claims before source identity and relevant support are verified. Add verified BibTeX within an authorized citation-completion task; unresolved sources remain explicit gaps.

Feasible actions often include:

- Re-running an existing script on an additional metric.
- Adding an already available baseline result supplied by the user.
- Adding a small ablation the user confirms is possible.
- Reframing claims and limitations.
- Moving clarification from appendix to main text.
- Adding a related-work comparison row from verified sources within the
  authorized citation workflow.

## Strategy Plan Template

```markdown
## Rebuttal Strategy

### Global Themes
1. <theme that resolves shared concerns>
2. ...

### Pivotal Reviewers
- <reviewer>: <why pivotal> and <what must be answered>.

### Issue Strategies
- <issue_id>: mode=<mode>; evidence=<source>; action=<action>; blocker=<none|user input needed>.

### Evidence Gaps
- <issue_id>: <needed evidence>; status=<source verification|needs user input|experiment result>.

### Compression Plan
- Must keep: <items>
- Cut first if over limit: <items>
```
