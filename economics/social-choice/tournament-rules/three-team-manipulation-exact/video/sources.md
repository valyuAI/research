# Sources and scope

Exact optimum 1/3 for n=3,4 and 2/5 for n=5..8, for coalitions of at most three; monotone/top-cycle certificates attain the same optima. Separate n=7, k=4 optimum 3/7. No arbitrary-team-count result.

## Scientific provenance

The five-team lower-bound argument is Schneider, Schvartzman and Weinberg (2017), Theorem 3.2. The broad conjecture was refuted for some large coalitions by Schvartzman, Weinberg, Zlatin and Zuo (2020). The finite fraction tables are the contribution illustrated here.

## Local authoritative inputs

- [paper.tex](../paper.tex), SHA-256 `a9052fd995db03dffed717f78089f3a93b3f94f15fc63e237d9d6cf598a4ed1b`.
- [readiness.md](../readiness.md), SHA-256 `c780c3516a0ce70b25635b6a7abbf6677e160e03b8a4bf8bf6a9179df2886995`.
- [review.md](../review.md), SHA-256 `222c9628584be5629f7f9c456f6e9a35d6ecaeea563f468168e9da9206e6f478`.
- [video-brief.md](../video-brief.md), SHA-256 `7090d70145ab0f5d94fccc569fd676f59a921c5815fdc5a1d396d9338ae491a2`.
- [verification/README.md](../verification/README.md), SHA-256 `7e908f9a725b4cbf50ee7330e79436dcbd16b60441b4099b70e97b63e38057fd`.
- [verification/certificates/rule_n5_k3_mt_small.json](../verification/certificates/rule_n5_k3_mt_small.json), SHA-256 `b28b3326f8191c770df226399e922da45c0eb0f74b1b3e14e37d443fb5ebec28`.
- [verification/results/rule_n8_k3.result.json](../verification/results/rule_n8_k3.result.json), SHA-256 `f405afba9c91106de81d53925cb07638741093305c51b0b4ed7e58fd03f7c916`.
- [verification/results/rule_n8_k3_mt.result.json](../verification/results/rule_n8_k3_mt.result.json), SHA-256 `a81f6934a81ea57efc62fbd6abaab6e1386c4224ee9cca77ccb7b3c479414970`.
- [verification/results/rule_n7_k4.result.json](../verification/results/rule_n7_k4.result.json), SHA-256 `8c4444a2c37685f2366d4bf36a8020715b17f73d19b82ecbe41caabcf6ee6c1f`.

All research evidence manifest entries were verified during packaging. The full snapshot is in `research-input-sha256.json`. The final research handoff reports correctness confidence high and originality confidence moderate, with the CTLN arithmetic and priority limitations stated in its readiness file.

## Beat-level evidence

| Clip | Source supporting the spoken claim |
|---|---|
| s01 | paper, Sections 1 and 2 |
| s02 | paper, Section 1 |
| s03 | compact five-team certificate, regular class |
| s04 | paper, Section 1 |
| s05 | video brief; regular certificate |
| s06 | paper, manipulation definition |
| s07 | paper, lower-bound construction |
| s08 | paper, Section 2 |
| s09 | Schneider, Schvartzman and Weinberg, 2017 |
| s10 | paper, lower-bound averaging proof |
| s11 | paper, Section 2; separate hypothetical manipulations |
| s12 | SSW 2017, Theorem 3.2 |
| s13 | paper, main theorem and certificate method |
| s14 | paper, symmetrization lemma |
| s15 | rule_n5_k3_mt_small.json |
| s16 | paper Table 2; compact certificate |
| s17 | paper, finite linear program |
| s18 | certificate mode le; review correction |
| s19 | paper, finite linear program |
| s20 | paper, exact certificates |
| s21 | paper, Section 4; plain CC only, n=5..8 |
| s22 | verification/verify_rule.py |
| s23 | verification/results/rule_n8_k3.result.json |
| s24 | paper checker argument; verification/verify_labelled.py |
| s25 | MT certificates; 192,640 n8 monotonicity checks |
| s26 | paper, TCC definition |
| s27 | readiness; n8 MT exact replay |
| s28 | paper, Theorem 1 |
| s29 | paper results table |
| s30 | paper, discussion and corollary |
| s31 | SSW 2017; SWZZ 2020; final scoped theorem |
| s32 | paper; verification README |

## Primary references

The research review and its source retrievals are reused from 26 October 2026; no new priority search or claim of fresh online retrieval is made by the video pass. See the finding references.bib for complete citations.
- [https://arxiv.org/html/1605.09733](https://arxiv.org/html/1605.09733)
- [https://arxiv.org/html/1906.03324v2](https://arxiv.org/html/1906.03324v2)
- [https://arxiv.org/html/2407.17569v1](https://arxiv.org/html/2407.17569v1)

## Explanatory simplifications

The linear-program feasible region and slack bars are explicitly schematic. The averaging proof is animated in full for five teams; the complete canonical-form and rational replay algorithms remain in the paper. Fourteen pass results are from the finalized research handoff, not fresh full replays by this video worker.

## Media provenance

Local unpublished production. Cedar synthetic narration, gpt-4o-mini-tts-2025-12-15, generated through the installed speech SDK wrapper with credentials from the existing private environment. No credentials are stored here. Audio manifests bind text, voice and instructions; QA also hashes the files. The end card discloses the synthetic voice. No subjective listening review is claimed.
