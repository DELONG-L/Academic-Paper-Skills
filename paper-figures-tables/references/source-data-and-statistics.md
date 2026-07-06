# Source Data And Statistics

Use this when an artifact depends on experiment data, statistical summaries, or actual-vs-placeholder status.

## Data Status

Classify the source before making artifacts:

- `ACTUAL_RUN`: source data exists and represents real experiment output.
- `USER_SUPPLIED_VALUES`: user supplied values directly, but raw output may not exist.
- `PLACEHOLDER`: values are illustrative or missing.

Do not present `PLACEHOLDER` values as actual results.

## Basic Summary

When source data supports it, compute or report:

- mean and standard deviation
- number of runs or seeds
- confidence intervals when appropriate
- paired or unpaired test choice when comparisons require it
- missing values or outliers

If statistical testing is requested, choose tests based on the data shape and assumptions. If the data is too thin, say so.

Do not add p-values, confidence intervals, or significance marks unless the source data and test choice support them. If the user supplies only aggregate values, state which statistical claims cannot be computed.

## Artifact Disclosure

If an artifact contains placeholder or synthetic values, mark it visibly in the caption or artifact note. Do not let placeholder values enter final paper-ready artifacts silently.

Use placeholder artifacts only for planning, layout review, or user-visible drafts. They are not final paper evidence.

## Traceability

Every table or data figure should have a trace:

- source file path or user-supplied table
- transformation script or manual transformation note
- output artifact path
- caption draft

If traceability is missing, produce a spec and request the missing data.

## Route Split

- Exact values and dense comparisons normally become tables.
- Trends, uncertainty, distributions, and tradeoff geometry normally become precise data figures.
- Mechanism explanations with no exact numeric encoding become conceptual figures, not Python plots.
