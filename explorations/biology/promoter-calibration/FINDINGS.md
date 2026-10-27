# Four measurements can calibrate much of a new promoter’s response profile

**Status: a reproducible exploratory result, not a new biological discovery or a manuscript-ready contribution.** Primary analysis uses manuscript CPM preprocessing. Confidence is high in the arithmetic and frozen transfer protocol; confidence in generalization beyond this study is low. Novelty is unresolved and ordinary two-parameter calibration is not new.

## What was actually tested

A four-pair calibration panel was selected using only Tan et al.’s 203-enhancer × 78-promoter library, then frozen before the 21-enhancer × 500-promoter count table was analyzed. No expression values from the target library selected those four enhancers. For each new target promoter, the four measured expression values fit an intercept and a slope against the frozen training-library enhancer activities. That fitted line predicts different enhancer-promoter pairs in the target library.

**Four means four total pair measurements. No additional basal controls are required by the primary panel.** The original 21-enhancer library already includes the three negative controls. The frozen panel is:

- `chr19:12907390-12907654-enhancer_rc`
- `chr19:49395399-49395663-enhancer_rc`
- `tCMV-enhancer`
- `chr3:128134842-128135106-enhancer_rc`

The design SHA-256 is `27eaa79797267e616c5a8f2f8e57b2430f4427c2a47fce1281ee2987008111f7`. The complete activity vector, candidate set, 100 random control panels, and timestamp are in `FROZEN_TRANSFER_DESIGN.json`. The random draws comprise 57 distinct four-element subsets of the eight eligible candidates; duplicates are retained as originally sampled.

## Primary result, with the relevant limits

On 202 new promoters and 899 common held-out enhancer-promoter pairs:

| Calibration method | Median per-promoter RMSE, log2 expression | Evaluated promoters |
| --- | ---: | ---: |
| Frozen four strengths across the training range | 0.503836 | 202 |
| Random four-pair panels, 100 frozen draws | 0.539603 | 202 |
| Four strongest training enhancers | 0.516378 | 201 |
| One strongest enhancer plus three negative controls | 0.531770 | 177 |
| Constant expression estimated from the same four pairs | 0.596437 | 202 |
| Fixed slope 1, intercept estimated from the same four pairs | 0.598209 | 202 |
| Leave-one-enhancer-out full-profile reference | 0.508903 | 202 |

This is a useful small-panel feasibility result. It is **not** evidence that the four-point method dominates full calibration. Median RMSE is similar, but the mean RMSE is worse: 0.574340 versus 0.557051, a paired difference of 0.017289 log2. A few worse predictions matter.

For fair comparisons, pairwise analyses use the same promoters and the same evaluated enhancer rows. Uncertainty resamples parent-promoter clusters, grouping edited variants with their original promoter (2,000 seeded bootstrap samples):

| Comparator | Shared promoters | Median paired RMSE ratio, four-panel/comparator | 95% cluster bootstrap interval |
| --- | ---: | ---: | --- |
| random | 202 | 0.9486 | 0.9365-0.9572 |
| strongest_only | 201 | 0.9902 | 0.9600-1.0025 |
| strongest_plus_controls | 177 | 0.9617 | 0.9315-0.9825 |
| mean_only | 202 | 0.9173 | 0.8858-0.9620 |
| equal_compatibility | 202 | 0.9166 | 0.8839-0.9560 |
| full_reference | 202 | 0.9985 | 0.9761-1.0346 |

The primary random-panel comparison is therefore a modest approximately 5% median paired error reduction. The strongest-only panel is a close competitor; its median-ratio interval includes 1. The mean paired RMSE difference versus full calibration has a 95% interval of +0.0056 to +0.0294 log2, so the four-panel tail performance is worse. These intervals describe resampling this study’s promoter cohort; they do not establish between-laboratory reproducibility.

The full reference fits each evaluated point using all other measured enhancers for that promoter, excluding the point being predicted. Seventeen shared enhancers have valid training activities after QC and three missing training measurements; the reference therefore uses **at most 16 other pairs**, with fewer where observations are missing. It does not reuse its target observation. There is no justified claim of a 50-fold reduction from the independent-library test.


Primary common-202-promoter tail audit (per-promoter RMSE, log2 units):

| Method | Mean | 90th percentile | Maximum |
| --- | ---: | ---: | ---: |
| selected | 0.574340 | 0.881456 | 1.936216 |
| full_reference | 0.557051 | 0.844591 | 1.950853 |
| random | 0.614023 | 0.933201 | 1.966848 |

## Coverage and independence

| Stage | Promoters |
| --- | ---: |
| Public annotation rows for nominal 500P library | 503 |
| Found in the downloaded count table | 495 |
| At least 1,000 TSS reads and at least 90% promoter-local starts | 337 |
| After excluding original-library promoter IDs, genes, sequences, and edited derivatives | 282 |
| All four primary calibration pairs measurable under CPM filtering | 270 |
| At least three of six common held-out evaluation enhancers measurable | 202 |
| Both calibration and evaluation criteria satisfied | 202 |

Thus 71.6% of the 282 eligible promoters contribute to the primary error estimate, while 95.7% have all four calibration values. Most exclusions at this final step arise from insufficient measurements of the **evaluation** enhancers. `final_cohort_coverage.tsv` lists every annotated promoter and every exclusion/coverage flag. `transfer_per_promoter.tsv` gives individual results. The independent reviewer additionally found no exact-sequence, reverse-complement, or genomic-interval overlap between the 282 eligible targets and the original promoter annotations.

All comparisons predict the same fixed set of six possible evaluation enhancers, excluded from every calibration panel: `chr19:12995828-12996092-enhancer_rc`, `chr1:9777689-9777953-enhancer`, `chr3:128399440-128399704-enhancer`, `chr3:128399440-128399704-enhancer_rc`, `scramble952-promoter`, and `SV40-promoter`. At least three must pass measurement QC. Predictions therefore concern this restricted panel, **not every unseen enhancer in the genome**.

This is a separate experimental library within the same paper, cell line, laboratory context and reporter integration system. It is not a separate-laboratory replication, a new cell type, endogenous CRISPR validation, or prediction from a promoter’s DNA sequence alone. Each new promoter is measured four times. Training the enhancer activities required the larger original library; that cost must be amortized, not ignored.

## Preprocessing and sensitivity

Primary expression preprocessing follows the manuscript: DNA at least 1 CPM; RNA pseudocount 0.1 CPM; median log2 RNA/DNA across barcodes; at least five qualifying barcodes per pair. Source labels and read-depth totals come from the public processed count files. The repository helper has a different optional CPM default of 0.5 and a raw-count default of DNA20, so the manuscript-matched result is not an exact reproduction of every helper default.

The original 203×78 model is approximately reproduced (R² 0.94046 under manuscript CPM, compared with the manuscript’s rounded 0.94). The raw-count sensitivity gives 0.95309. These are baseline checks, not new results. The earlier within-library sparse/full slope correlations share calibration measurements and are descriptive concordance, not independent prediction evidence.

With **the same frozen CPM panel choices and evaluation IDs**, changing to the authors’ raw-count helper route gives 270 covered new promoters: selected median RMSE 0.41889, random 0.43709, strongest-only 0.43078, full reference 0.39210. The median paired selected/random ratio is 0.9589 (95% interval 0.9498-0.9712). This sensitivity is secondary; its greater coverage is not substituted for the stricter primary result.

The count table contains 169 enhancer labels and 761 promoter labels because a small number of barcode assignments join multiple IDs with `__`. Exact intended 21-enhancer labels account for 99.9525% of DNA reads and 99.9577% of RNA reads; annotated promoter IDs account for 99.9776% and 99.9813%. We restrict inference to the exact intended IDs. Depth normalization retains the complete file totals, so this small excluded read mass is not silently renormalized away.

## Candidates rejected or demoted

- **New biological promoter-responsiveness mechanism:** rejected. The original authors already discovered and validated responsiveness and motif effects. This analysis adds a sparse-calibration benchmark only.
- **Novel panel-selection algorithm:** rejected. Evenly spaced training ranks and two-parameter regression are ordinary methods. The more complicated greedy selector did not consistently beat the simple design in the exploratory in-library analysis.
- **A universally adequate four-pair assay:** rejected. Coverage losses, tail errors, six restricted evaluation enhancers and one study prevent that claim.
- **Immediate new paper:** demoted. The result is a positive exploration note. Promotion needs a stronger contribution and independent cell-type/endogenous validation, plus a fuller priority check.
- **Reciprocal five-protein calibration:** not repeated. Previous exact identifiability work remains mathematically interesting but has unresolved assay/noise utility; this task moved to real regulatory measurements.

## Sources and reproduction

Primary study: [Tan et al., Intrinsic promoter responsiveness dictates sensitivity to transcriptional activation by enhancers](https://pmc.ncbi.nlm.nih.gov/articles/PMC13320843/), bioRxiv version 1, DOI [10.64898/2026.06.25.734173](https://doi.org/10.64898/2026.06.25.734173). Source code and annotations: [yj-tan/ExP-MPRA](https://github.com/yj-tan/ExP-MPRA). Processed data: [GSE334082 FTP directory](https://ftp.ncbi.nlm.nih.gov/geo/series/GSE334nnn/GSE334082/suppl/). Literature discovery and primary-text retrieval used Valyu CLI. Numeric gzip/TAR datasets and the complete 500P annotation were downloaded as binary/scientific data after source discovery; the text extractor truncated the 500P annotation, which was caught before analysis.

Input URLs, sizes and SHA-256 hashes are in `final_data_manifest.json`. The frozen design and model activity are sufficient to rerun the transfer without reselection. After restoring the scientific count file as described in [README.md](README.md), with NumPy and pandas installed:

```sh
python3 -u benchmark_library_transfer.py
python3 -u summarize_transfer.py
```

The earlier training-library exploratory scripts and their pair-score tables remain in the unpublished working archive. This compact package reproduces the transfer from the frozen design. No package was installed for the original analysis. No outreach or public scientific claim was made.

The main curator-friendly outputs are `FROZEN_TRANSFER_DESIGN.json`, `benchmark_library_transfer.py`, `summarize_transfer.py`, `transfer_results.json`, `transfer_matched_uncertainty.json`, `transfer_summary.tsv`, `transfer_matched_summary.tsv`, `transfer_per_promoter.tsv`, `final_cohort_coverage.tsv`, `final_data_manifest.json`, this note, and the independent review. Full-text receipts, raw count archives and the large per-pair prediction table should remain working artifacts rather than be copied into a manuscript package.
