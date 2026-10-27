# Source and claim ledger

Read locally on 26 October 2026 from the locked completed package. All 45 non-video input files are frozen in `scientific-input-sha256.json`. Production does not edit or rerun research code. No raw web retrieval responses or signed URLs are retained.

- [Paper](../paper.tex), Theorem 1.1 and potential section; [readiness](../readiness.md): for every a>=0, no finite distinct covering with every modulus >=6 dividing 2^a*45. Clips c04-c06, c17-c22, c31-c32.
- [Video brief](../video-brief.md): exact warm-up congruences 0 mod2, 0 mod3, 1 mod4, 5 mod6, 7 mod12. They cover all residues modulo12. Clips c01-c03.
- [Paper, columns and doubling potential](../paper.tex): CRT coordinates, six odd divisor types, minimum weighted cover definition with repetitions allowed in that relaxation, and phi(S)<=phi(S minus C)+price(C). Clips c07-c18.
- [Paper, doubling lemma and dead-state corollary](../paper.tex): Q'>=2Q-R, and Q>=R prevents every later finite completion. The animation derives and iterates the actual inequality. Clips c17-c20, c25, c32.
- [Prices](../verification/prices.txt): eleven recorded vectors; the displayed (14,7,4,2,2,1) has R=30. The first all-ones vector is inert at depth2; the video does not suggest all eleven are necessary or equally useful. Clips c13-c25.
- [Readiness](../readiness.md), [brief](../video-brief.md), [review](../review.md): exact four-board pattern with 0,17,18,24 uncovered cells and minimum costs 0,8,12,12. `scenes.py` embeds those exact arrays. Natural grid order is u=0..8 left to right and v=0..4 top to bottom. Clips c15-c16, c23-c25.
- [Finish summary](../verification/finish-summary.json), [finish build log](../verification/logs/finish-build.log), [Python slice logs](../verification/logs/): main C 498,464 nodes/0 survivors; generic C 66,821/0; Python 135 roots, 4,684,432/0. The Python logs are retained original checks, not fresh runs. Controls include 20,000 exact-cover comparisons, known finite covering, tight infinite truncation, and rejected incomplete summaries. Clips c26-c27.
- Harrington, Klein, Lowrance and Trifonov, [Covering systems where the prime divisors of all moduli are only 2, 3, or 5](https://arxiv.org/abs/2605.18644v1): Problem 2 and infinite-covering Theorem 1.10, discussed in the locked paper. Clips c28-c30. No reproduction of their full text is shipped.
- [Readiness and exclusions](../readiness.md): odd-part135/minimum8 exploratory work excluded; no Lean formalisation; confidence high for the retained proof/model, moderate for bounded novelty. Clips c27, c30, c33.

The moving gap on a number line is a labelled quantifier illustration, not the actual infinite construction. Counters summarise existing run records. No claims about the broader classification corollary are narrated, so its separate ordering hypotheses are not dropped. No external research, publication or contact occurred.

Production uses built-in Cedar through the secure installed toolkit. Voice/model/text digests live in `audio/manifest.json`. Captions are measured-clip phrase timings. Waveform correspondence is not a listening test.
