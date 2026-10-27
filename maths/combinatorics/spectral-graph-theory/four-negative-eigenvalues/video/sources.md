# Sources and scope

n(4)=30 for reduced graphs. Four order-30 classes all have inertia (4,22,4), rank 8. W5 and X are the only reduced graphs attaining eleven positive and four negative eigenvalues. No theorem for five or more negatives.

## Scientific provenance

ACK (Akbari, Cameron and Khosrovshahi, 2004) already supplied the four rank-8 classes, both doubling constructions and the compatibility method. Kotlov and Lovasz (1996) supplied the ordinary doubling. CFJK (Charles, Farber, Johnson and Kennedy-Shaffer, 2013) supplied W5/X and the numerical bound; the identity of Elphick and colleagues (2026) makes its implication explicit. Retained increments: exclusion of other ranks, especially 9..15, and uniqueness. Jacobi, the known core lemma, Basso and principal-rank precedents are credited in the paper.

## Local authoritative inputs

- [paper.tex](../paper.tex), SHA-256 `3c474bf5eee2db927aadeeadebf21bef1d44e0f39fb231514235e791f7e74b1a`.
- [readiness.md](../readiness.md), SHA-256 `b3f5955c359d5e208d687197ed21b1c85602f270c75667b40137b7c7e36dadaa`.
- [review.md](../review.md), SHA-256 `0e935bd55f6ace95ae62f172cb7e698f0185fa1a7af8707645aa9a7a83c6c774`.
- [video-brief.md](../video-brief.md), SHA-256 `46ed0e3467219da4557e95be3df71a71c7fedc01c81bb1a3d82553113238c238`.
- [verification/README.md](../verification/README.md), SHA-256 `febc23bc73f275d2bb029d6804b142b34c8f09295a2dde88c60dde3043b8404f`.
- [verification/order30_graphs.g6](../verification/order30_graphs.g6), SHA-256 `042ac5ceca8daa85f0e3611dedf22c95c453981995856a160775db6bd5206b59`.
- [verification/final_order30_check.json](../verification/final_order30_check.json), SHA-256 `0c3007993c965c98ce33697eb4368bea40a99f5845d9f3d792048e1f2d11d120`.
- [verification/extremal_result.json](../verification/extremal_result.json), SHA-256 `b7a381fb5e3a9b238326667fe0419d48ec837d9f79d11c3fc622809cd444d8a2`.
- [verification/census_counts.json](../verification/census_counts.json), SHA-256 `aaacbaa1caf51a404ff58fc5be356e9c50e6a8cb5527c15b61b9669df92ccbde`.
- [verification/final_census_result.json](../verification/final_census_result.json), SHA-256 `0c4d64e6119bb1fce7ee68cf784b7b6e675fda9e0cf8a381853ba4f86361c872`.
- [verification/max_reduced_order.log](../verification/max_reduced_order.log), SHA-256 `cef47900372b0d8fdf388a1c005f9267bcd7ac4ca9166ba69301ac78557daef5`.
- [verification/max_reduced_order_check.log](../verification/max_reduced_order_check.log), SHA-256 `c37c6f1487e9c75230dd9739861325f0902440c1f6ad65f09ad4cae68620de65`.

All research evidence manifest entries were verified during packaging. The full snapshot is in `research-input-sha256.json`. The final research handoff reports correctness confidence high and originality confidence moderate, with the CTLN arithmetic and priority limitations stated in its readiness file.

## Beat-level evidence

| Clip | Source supporting the spoken claim |
|---|---|
| g01 | adjacency action for K2, direct calculation |
| g02 | paper, adjacency matrix definition |
| g03 | K2 exact eigenpair (+1,(1,1)) |
| g04 | K2 exact eigenpair (-1,(1,-1)) |
| g05 | paper definitions; real symmetric spectral theorem |
| g06 | exact small-graph spectra; pentagon values shown as decimals with approximation mark |
| g07 | paper, A4 and n(4) definitions |
| g08 | duplicate vertices add a zero mode |
| g09 | paper, twin and isolated-vertex reduction |
| g10 | paper, reduced definition and nonsingular-basis lemma |
| g11 | paper Theorem 1; four order30 certificates |
| g12 | CFJK 2013; paper uniqueness theorem |
| g13 | nonsingular-basis lemma; prior Ellingham and related work |
| g14 | paper, Section 2 |
| g15 | paper Jacobi-minor lemma |
| g16 | paper Jacobi identity and closure theorem; mechanism sketch |
| g17 | paper Schur-complement sign test |
| g18 | exact K2-to-K3 Schur complement = -2 |
| g19 | two independent completed enumerators |
| g20 | census_counts.json; both enumeration logs |
| g21 | paper closure theorem, induction |
| g22 | final_census_result.json; enumeration logs |
| g23 | paper maximum-order compatibility construction |
| g24 | ACK 2004 method; paper Section 6 |
| g25 | two exact maximum-order runs |
| g26 | Kotlov-Lovasz construction; ACK Construction A |
| g27 | ACK Constructions A and B; exact doubling matches |
| g28 | paper contribution and scope lock |
| g29 | CFJK 2013 graph G4; W5 definition |
| g30 | CFJK graph G5; paper affine-plane description |
| g31 | exact extremal_result.json; no rank15 extensions |
| g32 | paper discussion and review corrections |
| g33 | paper main theorems |
| g34 | paper scope; verification README |
| g35 | paper final section; no k>=5 theorem |
| g36 | paper and complete evidence package |

## Primary references

The research review and its source retrievals are reused from 26 October 2026; no new priority search or claim of fresh online retrieval is made by the video pass. See the finding references.bib for complete citations.
- [https://webspace.maths.qmul.ac.uk/p.j.cameron/preprints/ranksign.pdf](https://webspace.maths.qmul.ac.uk/p.j.cameron/preprints/ranksign.pdf)
- [https://arxiv.org/abs/1108.4810](https://arxiv.org/abs/1108.4810)
- [https://arxiv.org/abs/2609.06319](https://arxiv.org/abs/2609.06319)
- [https://doi.org/10.1016/j.laa.2022.01.011](https://doi.org/10.1016/j.laa.2022.01.011)

## Explanatory simplifications

The K2 eigenpairs, duplicate cancellation and K2-to-triangle Schur complement are exact worked calculations. The general Jacobi, inertia-additivity and reconstruction arguments are mechanism sketches, with full derivations in the paper. All displayed extremal graphs are built and checked from exact definitions. The complete census and maximum-order computations are finalized recorded research evidence, not regenerated for this animation. Torgasev 1987 and Mohammadian 2022 full texts were unavailable in the priority audit; no first-ever assertion is made.

## Media provenance

Local unpublished production. Cedar synthetic narration, gpt-4o-mini-tts-2025-12-15, generated through the installed speech SDK wrapper with credentials from the existing private environment. No credentials are stored here. Audio manifests bind text, voice and instructions; QA also hashes the files. The end card discloses the synthetic voice. No subjective listening review is claimed.
