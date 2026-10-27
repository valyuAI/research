# Final readiness: CTLN

**Status: computational verification complete at the scope below, recorded on 26 October 2026.** The author has not yet completed a line-by-line review of every proof.

## Exact retained claim

At eps=1/4, delta=1/2 and any theta>0, every CTLN is nondegenerate by the mod-3 principal/Cramer determinant argument. G11, the complete directed graph on 11 vertices with the listed 21 arcs deleted, has a linearly stable fixed point with full nonclique support. No proper induced subgraph has a stable nonclique full support. No digraph on at most seven vertices has one at these parameters. Therefore the minimum possible support size is between 8 and 11 inclusive; eleven is vertex-minimal, not proved globally minimum.

## Verification and review response

- Two independent exact checkers pass G11, W4, G27 and G100. The standard-library checker uses agreeing characteristic-polynomial algorithms plus Routh and Lienard-Chipart; the separate FLINT checker uses exact solves, characteristic polynomials and all Hurwitz determinants.
- Every proper G11 subset of size 2..10 is accounted for: 2,035 = 90 cliques + 1,778 nonpermitted + 167 permitted but unstable. There are zero stable nonclique subsets.
- All three original n7 shards completed: 139,411,110 + 193,878,344 + 548,743,986 = 882,033,440 graphs. Original source/logs/candidate files are preserved unchanged in `verification/recovery/`. Fresh rational replay checks all 35,842 coefficient-positive candidates and finds zero stable candidates with no criterion disagreement.
- The original n7 scan uses a rigorously bounded residual permission filter under IEEE binary64 arithmetic. The proof and integer-overflow bounds are documented in `verification/README.md`; actual prefilter constants pass exact rational comparisons. This final pass did not redo 882 million graphs with rational solves.
- Fresh complete n2..6 standard scans disable that filter and use signed-overflow sanitization. Counts are 3,16,218,9,608,1,540,944; candidate counts are 0,0,2,15,372; all are exactly rejected. The six-vertex positive control checks 1,540,944 graphs and 2,322 candidates and finds exactly two stable examples.
- Pipeline stages, totals and expected exact outcomes are mandatory. Negative tests reject missing/duplicate candidates and wrong count/outcome expectations. The build does not silently skip FLINT or nauty.
- `review.md` answers the final review. Stronger attribution was accepted: hturcotte1/CLTN commit `3744200` (15 October 2026) already implies standard-point counterexamples with 23 and 31+ vertices. Its parameter map also implies the n<=7 exclusion. Our contribution is the explicit small example, vertex-minimality, mod-3 proof and independently certified bracket.

**Correctness confidence: high**, subject to the documented enumeration and IEEE arithmetic model for recovered n7 rejection decisions. **Originality confidence: moderate for G11 and the mod-3 lemma; low to moderate for independent small-order exclusion.** DeepResearch reports reused: `DR-024`, `DR-029`, `DR-074`.

## Not proved or claimed

No global exclusion at n=8,9,10, no first-ever failure at the standard parameters, no first eleven-vertex example at arbitrary parameters, and no failure at every legal parameter pair. The parameter-region plot and sampled perturbation trajectories are numerical illustrations. They do not classify attractors or prove a uniform 30% basin. Clique subsets can be stable, so the deletion result must retain the word nonclique.

## Reproduce

`PYTHON=/path/to/python nice -n 10 sh build.sh` reruns both example checkers, all G11 proper subsets, the full n2..6 scans and control, saved n7 rational replay, count/hash audit, prefilter-constant audit and PDF. `--full-scan` additionally regenerates n7. Requirements: Python with python-flint, nauty, a C compiler and LaTeX. The final run used the existing environment `<unpublished-record-3b990ef1b83c>`; no new dependency was installed. `python3 verification/test_recheck_failures.py` repeats negative tests.

| Evidence | SHA-256 |
|---|---|
| `paper.pdf` | `9465f455dec9dfa9f8ac3a3eef2eba864956f5086e90a8650eee49793f566726` |
| `verification/examples/G11.json` | `b53e47dadbfe7ddbad4215595a6d0dd281e6bd46fabc6e83ae543fc224de70b0` |
| `verification/examples/G11_certificate.json` | `1ea68e4220ce97d8151685841fe19f874707aa7f60b7d99731be8313d141d196` |
| `verification/final_validation.log` | `2be6e925a6fb7c26535ba30beda60cc0af169f5278bcec08ffc8774d12200d60` |
| `verification/scan_results/n7_recovered.recheck.json` | `a40ea26dc21ddd4ca548cb10b00b1ffc04b6bf96e3c6a8cd79128c80bae13b94` |
| `verification/scan_results/final_summary.json` | `b0c8b3e6a1d9113442a4071f371f7b9847c18b9e81e4f4e5f0d4705af90e4b46` |
| `verification/scan_results/prefilter_constants.json` | `224677253216a1c59b2bcbd3c692fb817e7cbe56d972aa5b2a1ed700108a0762` |
| `verification/recovery/source-provenance.json` | `2cc4c684a0c3f21d810ee750b66c64902a30d8c27202d7a82b68b289df4f715b` |
| `verification/scan_results/recheck_failure_tests.json` | `8ade1f8b08208afc29499c3cfb3da402b26ec275be808363fc0faf83a1dc05da` |

## Artifact integrity and paths

- Package: `maths/dynamical-systems/threshold-linear-networks/standard-parameter-counterexamples`.
- Final paper: `paper.pdf` (6 pages); editable source: `paper.tex` and `references.bib`.
- Complete evidence manifest: `verification/evidence.sha256`, SHA-256 `d8f7e6411c070da51192e5959994dd4af2d4758cf1fba93f2a69765cc75de918`. It covers sources, certificates, recorded results, original logs and final PDF/inspection files. It excludes this readiness file itself, generated caches/binaries and the regenerable graph output directory.
- Verify from this package with `shasum -a 256 -c verification/evidence.sha256`.
- Every final page was rendered at 100 dpi and individually inspected. `verification/pdf-inspection/inspection.json` binds the inspected PNGs to the final PDF hash. No clipping, overlap or unresolved reference remains.
- The scope for the explainer is recorded in `video-brief.md`. The checks above do not constitute external peer review.
