# Sources and scope

G11 at epsilon=1/4, delta=1/2, theta=1 has stable nonclique full support and is vertex-minimal. Every CTLN at this epsilon/delta pair is nondegenerate. Complete exclusion through seven gives an 8..11 minimum support-size bracket. No global minimum-11 or first-standard-counterexample assertion.

## Scientific provenance

Curto, Geneson and Morrison proposed the target-free clique conjecture. Geneson (2026) disproved it at other parameters. hturcotte1/CLTN commit 3744200 (15 October 2026) already implied standard-point counterexamples, including W4 on 23 vertices, and the n<=7 exclusion. G11 was found by shrinking and modifying that example.

## Local authoritative inputs

- [paper.tex](../paper.tex), SHA-256 `ebfd033245a0e955550958229d2341ef8ce3d041b8cfc12c5470435212669c6f`.
- [readiness.md](../readiness.md), SHA-256 `9839a14dce10c703fd8a8c2ba4c946e9e9eb870c4fc04690acde12fb1f00fe49`.
- [review.md](../review.md), SHA-256 `b2bcfc508e2c40f5684d12f83a5d2c7be27f99f3d94e5fef1398a11185579769`.
- [video-brief.md](../video-brief.md), SHA-256 `b0d469b8a08ef34045a162ce7899dd7f762ee4dd1c04748f3662c4a84dfbe240`.
- [verification/README.md](../verification/README.md), SHA-256 `3857636861288581f4eb76ae62e2f1a4211cce87863b726428f061ec276e7e47`.
- [verification/examples/G11.json](../verification/examples/G11.json), SHA-256 `b53e47dadbfe7ddbad4215595a6d0dd281e6bd46fabc6e83ae543fc224de70b0`.
- [verification/examples/G11_certificate.json](../verification/examples/G11_certificate.json), SHA-256 `1ea68e4220ce97d8151685841fe19f874707aa7f60b7d99731be8313d141d196`.
- [verification/scan_results/n7_recovered.recheck.json](../verification/scan_results/n7_recovered.recheck.json), SHA-256 `a40ea26dc21ddd4ca548cb10b00b1ffc04b6bf96e3c6a8cd79128c80bae13b94`.
- [verification/scan_results/final_summary.json](../verification/scan_results/final_summary.json), SHA-256 `b0c8b3e6a1d9113442a4071f371f7b9847c18b9e81e4f4e5f0d4705af90e4b46`.

All research evidence manifest entries were verified during packaging. The full snapshot is in `research-input-sha256.json`. The final research handoff reports correctness confidence high and originality confidence moderate, with the CTLN arithmetic and priority limitations stated in its readiness file.

## Beat-level evidence

| Clip | Source supporting the spoken claim |
|---|---|
| c01 | paper, question and fixed-point definition |
| c02 | paper equation 1 |
| c03 | paper equation 1; [u]+ = max(u,0) |
| c04 | standard epsilon=1/4, delta=1/2, theta=1 |
| c05 | locked brief two-neuron warm-up |
| c06 | direct two-neuron fixed-point calculation |
| c07 | two-neuron linearized dynamics |
| c08 | Jacobian of bidirected pair: eigenvalues -7/4 and -1/4 |
| c09 | paper, support and target-free clique definition |
| c10 | paper, target-free clique definition |
| c11 | CGM conjecture; paper Section 1 |
| c12 | G11.json; G11_certificate.json |
| c13 | G11.json deleted_arcs |
| c14 | G11_certificate.json fixed_point_theta_1 |
| c15 | exact row-zero identity in locked brief |
| c16 | exact rational fixed-point identity |
| c17 | paper K=I+3N+3J |
| c18 | G11 exact fraction check |
| c19 | paper full-support lemma |
| c20 | local linear stability; illustrative phase portraits |
| c21 | paper full-support lemma; eigenvalue illustrations are numerical |
| c22 | G11 certificate min real eigenvalue; numerical plot |
| c23 | paper exact Hurwitz criterion |
| c24 | G11_certificate.json Hurwitz determinants |
| c25 | paper nondegeneracy definition; geometric teaching illustration |
| c26 | paper mod-3 lemma |
| c27 | paper principal and Cramer determinant proof |
| c28 | paper main theorem parts 1 and 2 |
| c29 | exact check of all 2,035 proper subsets sizes 2..10 |
| c30 | recovered n7 scan and exact rational replay |
| c31 | final readiness scope |
| c32 | paper robustness limits; locally generated numerical illustration |
| c33 | paper provenance; Geneson 2026; CLTN repository |
| c34 | hturcotte1/CLTN commit 3744200 |
| c35 | readiness and final review scope |
| c36 | paper and verification README |

## Primary references

The research review and its source retrievals are reused from 26 October 2026; no new priority search or claim of fresh online retrieval is made by the video pass. See the finding references.bib for complete citations.
- [https://github.com/hturcotte1/CLTN/commit/3744200](https://github.com/hturcotte1/CLTN/commit/3744200)
- [https://arxiv.org/abs/2301.12638](https://arxiv.org/abs/2301.12638)

## Explanatory simplifications

The Hurwitz criterion is introduced through the quadratic case and its actual first three determinants, with all eleven positive checks displayed; its general theorem is not derived. Matrix entries and rates are actual certificate data. prepare_assets.py verifies every fixed-point row exactly. The G11 plot is one numerical 0.1% sinusoidal relative perturbation and is not a basin theorem. The two-neuron return uses an exact decaying mode. The n7 scan uses certified residual rejections under the documented IEEE model and exact saved-candidate replay, not 882 million exact eigenvalue calculations.

## Media provenance

Local unpublished production. Cedar synthetic narration, gpt-4o-mini-tts-2025-12-15, generated through the installed speech SDK wrapper with credentials from the existing private environment. No credentials are stored here. Audio manifests bind text, voice and instructions; QA also hashes the files. The end card discloses the synthetic voice. No subjective listening review is claimed.
