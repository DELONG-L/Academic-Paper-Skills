# Rebuttal Drafting

Use this reference only after an issue board and strategy plan exist, even if they are lightweight.

## Venue Shape

Confirm:

- Single shared author-response box or per-reviewer threads.
- Character or word limit.
- Whether Markdown, LaTeX, tables, or figures are allowed.
- Whether revised manuscript content can be referenced.

If venue shape or limit is unknown, draft a strategy first and ask before final paste-ready drafting.

## Single-Document Structure

```markdown
We thank the reviewers for their constructive feedback. We address the main concerns by <global theme 1>, <global theme 2>, and <global theme 3>.

R1. <short concern label>. <answer -> evidence -> manuscript change>.

R2. <short concern label>. <answer -> evidence -> manuscript change>.

...

We will incorporate these changes in the revised manuscript, with the main edits summarized in <locations>.
```

Keep the opener short. Do not spend scarce length on generic gratitude.

## Per-Reviewer Thread Structure

Each reviewer response must stand alone.

```markdown
We thank Reviewer <id> for <specific positive/constructive framing>.

Q1/W1: <concern label>.  
Response: <direct answer>. <evidence>. <change>.

Q2/W2: ...
```

Do not write "see response to Reviewer 2" unless the platform clearly shares all responses and the user approves.

## Response Unit

Each response should usually contain:

1. Direct stance: accept, clarify, defend, concede narrowly, or provide evidence.
2. Grounded support: local paper evidence, user-confirmed result, or approved planned change.
3. Manuscript action: section, table, figure, appendix, limitation, or no-change reason.

## Tone Rules

Use:

- "We thank the reviewer for..."
- "We agree that..."
- "We clarify that..."
- "We respectfully note that..."
- "We have revised..." only when already done or user confirmed.
- "We will revise..." only when user approved the commitment.

Avoid:

- "The reviewer is wrong."
- "The reviewer misunderstood."
- "Obviously", "clearly", "trivially".
- Long defensive arguments.
- Vague promises such as "we will improve the paper" without location.
- Flattery aimed at the area chair.

## Missing Results

If a result is needed but not provided:

- Use `[TBD: user-provided result]` in a draft only when the user asked for a fill-in draft.
- Otherwise stop at strategy and ask the user for the result.
- Never fabricate a plausible number.

## Tables in Rebuttals

Use compact tables only for numeric results or issue coverage. Do not put prose Q/A pairs into a large table.

If a LaTeX table or figure artifact is needed, hand off to `paper-figures-tables`.

## Length Control

Use `scripts/count_rebuttal_limit.py` when a limit exists.

Compression order:

1. Remove generic gratitude.
2. Merge duplicate setup explanations.
3. Shorten background.
4. Keep answers to pivotal reviewers and critical issues.
5. Do not drop a reviewer concern silently.

## Draft Quality Checklist

- Every issue card is answered, deferred, or marked needs-user-input.
- Every factual statement is sourced.
- Every promise appears in the revision plan.
- Tone is respectful but not submissive.
- No invented citations, numbers, experiments, or links.
- Limit is satisfied or overage is explicitly reported.
