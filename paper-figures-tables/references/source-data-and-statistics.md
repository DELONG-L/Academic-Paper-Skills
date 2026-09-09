# Source Data And Statistics

Use this when an artifact depends on experiment data, statistical summaries, or actual-vs-placeholder status.

## Data Status

Classify the source before making artifacts:

- `ACTUAL_RUN`: source data exists and represents real experiment output.
- `USER_SUPPLIED_VALUES`: user supplied values directly, but raw output may not exist.
- `PLACEHOLDER`: values are illustrative or missing.

An executed simulation is actual research output when simulation is the study
method; record it as `ACTUAL_RUN` with its simulation setting and disclose that
setting where scientifically relevant. It is not a layout placeholder merely
because its data are synthetic. Supplied numerical prose is also a usable input
when its values, units and provenance are explicit.

Do not present `PLACEHOLDER` values as actual results.

## Multiple Runs and Aggregation

When combining runs, derive the displayed summary reproducibly from identified
sources. Reuse the project's aggregation artifact or script if it captures the
following information; no particular schema or additional ledger is required:

- Run/sample identity and the actual unit being aggregated.
- Source status, input revision/hash, analysis command and output locator.
- Inclusion/exclusion decisions and their reasons; retain invalid/missing counts
  in the analysis record. Unfavorable valid measurements are not exclusions.
- Fields that must match for the comparison: data/split, protocol, metric
  definition, model/configuration and budget as applicable.
- Grouping, weighting, missing-data handling, summary and uncertainty definition.

If configurations differ, stratify the summary or report the material difference
with the comparison. Do not silently average different protocols into one number.
Avoid duplicate runs, paired/unpaired confusion, or counting samples as independent
runs. Recompute dependent text/tables when source data or inclusion decisions change.

The aggregation record should make any incompatibility visible at the top level,
not hide it among nested details. Such a record supports a judgment; it is not
itself formal policy PASS. For supplied aggregate values, report them faithfully
with their provenance and do not imply raw-run verification.

## Basic Summary

When source data supports it, compute or report:

- mean and standard deviation
- number of runs or seeds
- confidence intervals when appropriate
- paired or unpaired test choice when comparisons require it
- missing values or outliers

If statistical testing is requested, choose tests based on the data shape and assumptions. If the data is too thin, say so.

Follow a prespecified analysis when one exists. Consider the estimand, sampling
unit, dependence/pairing, uncertainty and multiple comparisons before selecting a
test. Do not use a preliminary normality-test p-value as an automatic switch
between all parametric and nonparametric methods. Never choose a test or exclude
data because it produces a preferred result. A single descriptive measurement
can be reported as such without invented variation or an automatic extra-run gate.

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
