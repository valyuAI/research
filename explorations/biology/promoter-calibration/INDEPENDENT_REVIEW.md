# Independent review of sparse promoter calibration

18 October 2026. **The independent-library prediction calculation is valid within its stated scope.** I found no target-response leakage in the frozen panel selection, no retained source/target promoter overlap, and no arithmetic error in the checked predictions or RMSE aggregation. Correctness confidence: high. Novelty and prospective assay usefulness remain unresolved.

This review inspected existing files and ran small read-only checks. It did not rerun the barcode-scale benchmark, choose a replacement panel, or download new data.

## What qualifies as held out

| Result | Classification |
| --- | --- |
| Published-responsiveness correlation and full-data response-model fit | In-sample reproduction/concordance. The response values contribute to the fit. |
| Original 203-by-78 pilot: locus excluded from enhancer-activity estimation, four pairs measured for each target promoter, other pairs evaluated on the opposite barcode half | Held-out locus plus technical nonpanel-pair prediction, conditional on calibration measurements. Barcode halves are not biological replicates. |
| Pilot sparse/full slope correlation around 0.97 | Descriptive parameter concordance, not independently measured responsiveness. Both slopes use the same calibration barcode half and share panel measurements. |
| Frozen 203-by-78 design transferred to nonoverlapping promoters in the 21-by-500 library, evaluating enhancer pairs absent from every compared calibration panel | Genuine independent-library, new-promoter, nonpanel-pair prediction. It still uses four measured calibration responses for each new promoter. |

The final row is the strongest new calculation. It is not zero-shot sequence prediction, validation across cell types, or prediction of endogenous expression. Both libraries come from the same published study and reporter context.

## Frozen design and leakage checks

The frozen file records `2026-10-18T12:32:08.720255+00:00`, seed `20261018`, primary CPM preprocessing, training promoter IDs, enhancer activities, candidate lists and panels. Its SHA256 is:

`27eaa79797267e616c5a8f2f8e57b2430f4427c2a47fce1281ee2987008111f7`

This matches both the value communicated before my result audit and `transfer_results.json`. The source and target compressed-data hashes also match their recorded values. This is a local freeze with an auditable hash, not a public preregistration. The frozen file does not contain the complete later cohort, evaluation and metric specification; describe the overall exercise as exploratory development followed by a frozen-panel transfer test.

I independently reconstructed all finite frozen CPM activity values from `pair_scores_cpm_all.tsv`: take the 43 source promoters with `clean_TSS==True`, subtract each promoter's mean over the 19 named/annotated negative controls, then average over source promoters. Maximum discrepancy: **zero**. The shared-enhancer candidates passing 80% source coverage and the four selected rank positions reproduce exactly. Thus the transfer script reads an already selected panel; it does not optimize the panel on target expression.

The four primary enhancers are:

- `chr19:12907390-12907654-enhancer_rc`
- `chr19:49395399-49395663-enhancer_rc`
- `tCMV-enhancer`
- `chr3:128134842-128135106-enhancer_rc`

Their training activity values are approximately `(-0.206, 0.054, 1.013, 2.492)`. These are evenly spaced **ranks**, not evenly spaced numeric activities.

The target cohort excludes every original-78 promoter ID, overlapping gene, edited derivative of an original promoter, and identical sequence, not merely the 43 source promoters used to estimate activities. I independently verified zero retained overlaps by those identities, and additionally zero reverse-complement sequence matches and zero genomic interval overlaps with the original 78. There are **282 eligible target promoters** after these exclusions and TSS QC.

The evaluation set is six fixed enhancer IDs excluded from the entire candidate-panel union and the alternative controls. Checking all **93,874 saved CPM prediction rows**, I found zero intersections between a row's calibration panel and its evaluated enhancer. Training measurements of these enhancers at source promoters are allowed: the generalization target is new promoter/enhancer pairs, not enhancers never measured anywhere.

## Preprocessing relative to the authors

The manuscript Methods specify DNA coverage at least 1 CPM, an RNA pseudocount of 0.1 CPM, median barcode log-ratios, and at least five barcodes per pair. The local CPM implementation matches those rules. The same manuscript specifies at least 1,000 aligned TSS reads for the larger libraries and uses a 90% promoter-start cutoff, matching the target QC. See the [primary manuscript](https://pmc.ncbi.nlm.nih.gov/articles/PMC13320843/), especially its Expression quantification and 5'-end quantification sections. The cached full text remains in the unpublished working archive.

The authors' reusable helper defaults differ: CPM filtering defaults to 0.5 when enabled, while the example normally uses raw-count filtering at 20 because CPM normalization is off. This does not invalidate the primary manuscript-based CPM route. Raw counts are an explicitly separate sensitivity analysis.

The baseline fit is still a near-reproduction rather than an exact reproduction of every author choice. For example, the transfer fits a free intercept and slope from the four calibration pairs; the published explanatory model estimates basal activity from controls and then fits a responsiveness slope. Global expression recentering is absorbed by a free intercept and by the source baseline subtraction, but QC and fitting choices should be documented.

Whole-library CPM normalization uses the target library's total reads, including evaluation-pair reads. This is conventional retrospective assay preprocessing, not selection using specific target responses. Nevertheless, a physically sparse follow-up assay would have a different library composition and read-depth allocation. Retrospective subset prediction does not demonstrate that its measurement noise and normalization would remain unchanged.

The target file has more distinct identifiers than its nominal library name. The analysis agent checked that outside-library identifiers are ambiguous dictionary assignments containing `__`; they account for under 0.05% of read mass. The evaluated matrix is restricted to exact frozen enhancer IDs and the annotated promoter cohort. I checked the restriction in the code; I did not independently repeat that read-mass calculation.

## Prediction and metric verification

For 11 target promoters selected at fixed intervals through the saved promoter order, I independently fitted the four-point regressions using `numpy.linalg.lstsq`, rather than the implementation's covariance formula. Sparse predictions agreed within `1.4e-15` and leave-one-enhancer-out full-profile predictions within `3.6e-15`.

The full-profile reference excludes the evaluated enhancer's own measured expression when predicting that enhancer. It is therefore a legitimate leave-one-enhancer-out reference, not an in-sample full fit. It uses other target evaluation responses, so it intentionally has more information than the four-pair method. Each reference prediction may come from a different leave-one-out fit; it should not be described as one independently measured true responsiveness parameter.

I independently recomputed the primary median per-promoter RMSE as **0.5038363172 log2 units**. On the same 202 promoters, the full-profile reference median is **0.5089028584**, and the random-four baseline median is **0.5396029345**. Equality with the full reference here means similar error against these observed pairs; it does not establish equality to biological truth.

The random baseline averages each promoter's RMSE over covered frozen panel draws, then summarizes promoters. This is correctly implemented, but it is the expected error of a random panel under that coverage conditioning, not the error of averaging predictions from an ensemble. There are 100 frozen draws containing 57 unique four-element subsets from the eight candidates. These are design repetitions, not biological sample size.

Matched-cohort comparisons independently recomputed from saved results:

| Comparator | Shared promoters | Median paired sparse/comparator RMSE | Promoters favoring sparse |
| --- | ---: | ---: | ---: |
| Random four | 202 | 0.94862 | 145 |
| Strongest four | 201 | 0.99022 | 112 |
| Strongest plus three controls | 177 | 0.96169 | 113 |
| Constant response | 202 | 0.91735 | 136 |
| Fixed slope of one | 202 | 0.91661 | 138 |

These are descriptive paired estimates. Do not compare different-cohort medians as if they were paired effects. The improvement over strongest-four is small; a general superiority claim needs uncertainty at the promoter-origin/gene cluster level. Related edited promoters are not independent experimental units. The later cluster-bootstrap implementation is audited separately in [BOOTSTRAP_REVIEW.md](BOOTSTRAP_REVIEW.md).

## Coverage and limits on the claim

The primary four-pair method covers **202/282 eligible promoters, 71.6%**. These are not 202 successes out of every promoter in the nominal 500-member library. There are 503 annotated entries; TSS QC, overlap exclusions and measurement coverage restrict the evaluated population. The 202 promoters supply 3–6 common evaluation pairs each: 44 have three, 63 have four, 55 have five and 40 have six.

The raw sensitivity now retains exactly the same primary frozen panels and evaluation IDs, changing only preprocessing and source activity values. It covers 270/282 promoters and gives median RMSE 0.41889 versus 0.39210 for the full reference and 0.43709 for random four. Raw and CPM RMSE are not directly comparable measures of scientific improvement because filtering, pseudocounts and the covered promoter cohort differ.

The defensible claim is:

> A four-enhancer panel chosen in one published reporter library predicts three to six additional enhancer responses for 202 nonoverlapping, QC-eligible promoters in a second library, with median log2 RMSE comparable to a leave-one-enhancer-out full-profile reference under the primary preprocessing.

Do not turn this into “four measurements replace 200” on independent promoters: that extrapolates beyond the independent-library evaluation set. The earlier larger-library pilot is useful supporting exploration but uses barcode splits from one library. Do not call the result a discovery of promoter responsiveness itself; that response model is the authors' established finding. The possible contribution is a specifically validated calibration strategy, and its novelty requires a focused comparison to previous sparse reporter designs.
