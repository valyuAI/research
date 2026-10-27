# Independent bootstrap and simplification review

18 October 2026. **Pass: calculations reproduce; interpretation needs the qualifications below.** Confidence: high in implementation correctness. The intervals remain approximate exploratory uncertainty summaries, not a calibrated guarantee for arbitrary future biological experiments.

## Independent numerical verification

I recomputed all 12 comparisons from `transfer_per_promoter.tsv` and the promoter annotations. Instead of concatenating sampled cluster blocks as the implementation does, I converted cluster draws into multiplicities, assigned each promoter its cluster's multiplicity, and calculated weighted differences and repeated-value medians. With the recorded seed and 2,000 draws, every saved percentile endpoint agreed within **1.4e-17**.

The bootstrap samples promoter-origin clusters with replacement, keeping all available variants of each sampled origin together. A nonmissing `modification_of` supplies the parent ID; otherwise the promoter ID supplies it. I checked the annotation: there are no nontrivial nested parent chains requiring recursive resolution. Self-referential parent annotations correctly map to the same origin. The primary common cohort contains **202 promoters in 195 origin clusters**. Paired methods use the intersection of covered promoters, and each draw preserves pairing.

These are promoter-weighted statistics with cluster resampling: larger variant families contribute more promoters. They are not equal-weight-per-gene estimates, nor is the resampling unit a biological replicate or a barcode. That distinction is appropriate to the declared median over promoters, but should remain explicit.

## Verified wording and numbers

- **Versus the random-four baseline:** median paired RMSE ratio `0.9486217863`, percentile interval `[0.9365175349, 0.9571525821]`. Transforming both endpoints in reverse order gives a **5.1378% median per-promoter relative RMSE reduction**, with approximate 95% origin-cluster bootstrap interval **4.2847%–6.3482%**. “5.1% lower error, interval 4.3%–6.3%” is accurately rounded. This is not the ratio of the two cohort medians and not a five-percentage-point increase in prediction accuracy.
- **Versus full-profile leave-one-out prediction:** mean paired per-promoter RMSE difference is **+0.0172887670 log2 units**, with interval **[+0.0056315060, +0.0293620873]**. This is a penalty for the sparse panel. It is an arithmetic mean of per-promoter RMSE differences, not pooled RMSE, an expression fold change, or a percentage penalty.
- **Median comparison with the full reference:** paired ratio `0.9985428472`, interval `[0.9761090194, 1.0345873662]`. Similar medians coexist with the positive mean penalty. An interval containing one does not prove equivalence or noninferiority; neither was tested against a prespecified margin.
- **Versus strongest four:** the median paired ratio interval `[0.9599593422, 1.0024809838]` includes one. Avoid a general claim that activity-ranked selection beats strongest-only selection on the median endpoint.

The intervals condition on the frozen training design, its estimated enhancer activities, the observed target library, the coverage rules, the six evaluation enhancer identities and the frozen random-panel draws. They do not incorporate training-panel selection uncertainty, new biological replicate noise, resampling of enhancer identities, or prospective sparse-library effects. The random comparator averages RMSE over successfully covered frozen panels; its 100 draws are not independent biological observations. The multiple secondary comparisons have not been multiplicity-adjusted. Keep the random-four comparison primary and the others descriptive.

## Code-simplifier assessment

Reviewed `benchmark_library_transfer.py`, `summarize_transfer.py`, the original training-library `benchmark_sparse_panel.py` in the unpublished working archive, and the [detector script](../gene-switching/switching-prior-audit-20261018/forward-check/verify_detector.py).

**No mandatory change or correctness bug found.** The explicit scientific stages aid review, and extracting the short repeated loops into further abstractions would not improve this bounded analysis. `summarize_transfer.py` has one unused load of `FROZEN_TRANSFER_DESIGN.json`; removing that line would be a legitimate tiny cleanup if the file is otherwise edited, but does not warrant churn or rerunning the analysis. Do not simplify away the raw/CPM separation, coverage accounting, held-out-pair exclusion or full-reference leave-one-out calculation.

The detector script is already compact. Its retained output reports 217 traces, 286 timepoints and maximum ON-probability discrepancy `6.9e-15`; the scope is correctly restricted to reproducing the detector stage from supplied initiation posteriors. It does not validate deconvolution or infer the true promoter mechanism. I reviewed its code and saved result, without rerunning that separate detector calculation.

No existing source scripts or result artifacts were modified by this review.
