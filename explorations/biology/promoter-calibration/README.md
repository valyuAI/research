# Four measurements for promoter calibration

Exploratory empirical result, 18 October 2026. **A small-panel feasibility
benchmark, not a new biological mechanism or a manuscript-ready discovery.**

A panel selected in one published enhancer-promoter library predicts additional
measurements in a second library. Each new promoter needs four measured
responses. The evaluation excludes original-library promoters, overlapping
genes and edited derivatives, and uses different enhancer pairs from the
calibration panel.

| Primary CPM result | Selected four | Random four | Full-profile reference |
| --- | ---: | ---: | ---: |
| Median per-promoter RMSE, log2 | 0.504 | 0.540 | 0.509 |
| Mean per-promoter RMSE, log2 | 0.574 | 0.614 | 0.557 |

There are 202 evaluated promoters and 899 held-out pairs. Of 282 eligible
promoters, 270 have all four calibration measurements; 202 also have sufficient
evaluation coverage. Full calibration has better mean and upper-tail error.
The strongest-four baseline is also a close competitor. These results support
further testing of sparse calibration, not equivalence to full calibration.

Both libraries come from the same study, cell line and reporter system. This
is retrospective subset prediction, not a prospective sparse assay, endogenous
validation or prediction from DNA sequence alone. The underlying response
model was already established by the original authors.

**External follow-up weakens broader claims.** A frozen leave-one-promoter-out
test of the same panel-selection rule in a different laboratory's mouse assay
covered 10 promoters and 550 nonpanel responses. Median RMSE was 0.322 for
four-point calibration, 0.237 for full calibration and 0.318 for a simpler
fixed-slope model. This retrained the rule on other mouse promoters; it did
not transfer the literal human panel. The new calculation has not had an
independent numerical review. Its frozen protocol and complete outputs are
preserved in the working archive. These preliminary results do not support
general superiority. Source: [Martínez-Ara et al. 2022](https://doi.org/10.1016/j.molcel.2022.04.009).

## Evidence

- [Findings, comparisons and limitations](FINDINGS.md).
- [Independent leakage and arithmetic review](INDEPENDENT_REVIEW.md).
- [Independent bootstrap and code review](BOOTSTRAP_REVIEW.md): all 12
  comparison intervals reproduced through a different weighted calculation.
- [Frozen panel and training activities](FROZEN_TRANSFER_DESIGN.json).
- [Paired uncertainty](transfer_matched_uncertainty.json),
  [tail errors](primary_tail_statistics.json) and
  [complete cohort accounting](final_cohort_coverage.tsv).
- [Input URLs, sizes and SHA-256 hashes](final_data_manifest.json).

Confidence is high in the checked calculations and low in transfer beyond
this study. The panel freeze was local and preceded target-count analysis;
it was not a public preregistration of the entire analysis.

## Reproduce the transfer

The two promoter-annotation tables, `78P_annotations.txt` and
`500P_annotations.txt`, are third-party data from the source study's
[ExP-MPRA repository](https://github.com/yj-tan/ExP-MPRA), which has no license
file. They are not redistributed in public copies of this package. Fetch them
from a pinned upstream commit with SHA-256 verification:

```bash
python3 fetch_inputs.py            # the two annotation tables
python3 fetch_inputs.py --counts   # also the processed GEO count file below
```

The target TSS counts (`GSM9780095_21Ex500P_TSS_mapping_counts.txt.gz`) come from
the `GSE334082_RAW.tar` supplement of NCBI GEO series GSE334082. All original
sources and hashes are in the input manifest. The approximately 30 MB processed
scientific count file is in the
[GEO directory](https://ftp.ncbi.nlm.nih.gov/geo/series/GSE334nnn/GSE334082/suppl/);
place it beside these scripts as
`GSE334082_21Ex500P_upstream_integrated_BC_counts.txt.gz`.
Its SHA-256 must be
`9e311cb5560905beca4478973ed84dfdaf0227a33f633896f891b8d14ef65dff`.

With NumPy and pandas available, run:

```bash
python3 -u benchmark_library_transfer.py
python3 -u summarize_transfer.py
```

The first script regenerates predictions, coverage and per-promoter results;
the second regenerates matched comparisons and cohort-bootstrap intervals.
The scripts emit progress. Large generated prediction tables and downloaded
count files are working artifacts, not part of this compact package.

The exploratory source-library panel search remains in the unpublished working
archive. This package reproduces the transfer from the frozen design; it does
not reselect the panel. The independent review separately checked that the
frozen activities and panel agree with the source-library calculations.

Primary study: [Tan et al., Intrinsic promoter responsiveness dictates
sensitivity to transcriptional activation by enhancers](https://doi.org/10.64898/2026.06.25.734173).
Annotations and original methods: [ExP-MPRA](https://github.com/yj-tan/ExP-MPRA).

Valyu Search and Contents supported literature discovery, primary-text
verification and data discovery. The numerical transfer and independent
checks were executed locally. This result does not represent an endorsement
from a still-running DeepResearch task.
