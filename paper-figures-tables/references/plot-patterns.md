# Plot Patterns

Use this file to choose the simplest figure that supports the paper claim.

| Pattern | Use For | Encoding |
| --- | --- | --- |
| Grouped bar | Method comparisons over 2-5 metrics; ablations; robustness summaries. | Methods as colors/hatches, metrics as x categories. |
| Interval bar | Paired margins, confidence intervals, or seed means. | One bar/dot per condition with CI whiskers. |
| Line/scaling curve | Runtime, sample size, budget, training/evaluation progression. | x is scale or budget; y is metric; limited to 2-4 methods. |
| Pareto/frontier | Utility-vs-cost, attack-vs-defense, edit-vs-preservation tradeoffs. | Scatter or step frontier; highlight focal method and key baselines. |
| Ladder/boundary bar | Observability regimes, threat model tiers, attack stages, deployment ceilings. | Ordered regimes on x; prevention/gap/cost as bars or aligned panels. |
| Heatmap | Policy x channel matrices, attack x defense coverage, ablation activation. | Rows and columns must be meaningful categories; annotate only small matrices. |
| Small multiples | Per-domain or per-family comparisons with repeated axes. | Shared y-axis and consistent method order. |
| Diagram | Evidence-flow graph, attack graph, protocol pipeline, threat model. | Use graph/layout tooling; keep the same figure contract and caption rules. |

## AI Evaluation Figures

- Main comparison: grouped bar or compact table-like plot.
- Robustness across seeds/generators: interval bar or small multiple.
- Scaling: line plot with throughput or time per case, not both on one axis unless necessary.
- Pareto audit: plot utility loss versus edit/action count and label frontier points.

## Security And System Figures

- Attack/defense matrix: heatmap when both axes are categorical and complete.
- Threat model: diagram with assets, trust boundaries, adversary capabilities, and policy boundary.
- Observability or deployment boundary: ladder bar ordered from strongest information to weakest information.
- Privacy/utility tradeoff: Pareto or paired bars with the privacy constraint stated in caption and axis labels.

## Avoid

- Radar plots unless the metrics are normalized, few, and genuinely comparable.
- 3D plots for quantitative comparisons.
- Mixed units on a single axis.
- Figures that rely on color alone to distinguish safety-critical states.
