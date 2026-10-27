# Evidence ledger

Read 26 October 2026: complete ../paper.tex, ../README.md, ../video-brief.md, ../verification/README.md, ../verification/results.json, ../verification/length-three.json, ../verification/execution-log.txt, ../verification/review-record.md and ../verification/priority-audit.md. No readiness.md exists in this package. Final paper and completed execution records control the claims.

- Model and theorem: independent observations from one common continuous/atomless distribution; consecutive relative-order patterns; every k>=3; right rotation wins strictly more than half. Not a uniform-rank Markov chain. Winning reply need not be optimal.
- Worked bars: .2,.4,.6,.1 has rank pattern 2341. Race stream .10,.20,.40,.60,.15 gives 1234 first and then, if continued, 2341.
- Local count: two B-to-A orders x0<x4<x1<x2<x3 and x4<x0<x1<x2<x3; one B-to-B order; other one-shift pairs impossible for A=2341, B=1234. (2-1)/5!=1/120 is a signed contribution, not final winning advantage.
- Inclusion-exclusion toy 6+5-2=9 is explicitly illustrative. Actual pointwise recurrence u0=-1, uj=-sum(ui within earlier k-1 starts), with values -1,0,+1 and at most two nonzero coefficients in any k consecutive start positions. For k=4 and starts0..5, the displayed sequence is -1,+1,0,0,-1,+1.
- Half-binomial lemma: two private ordered chains; differing private rank sets give disjoint colour-swapped interleaving sets. First-blue example is a teaching special case, not a claimed universal rank condition.
- Root-clump tail: r=2(k-1)/k!, conditional union bounds using observations after anchor ending times; no independence assertion between overlapping candidate windows. Counts only anchors in root clump, not global infinite anchor sequence.
- Uniform k>=8 margin: 1-256699/300300-144/2879-1/3360 = 218738049/2305503200 >0. On screen K=1/[2(-C(1))]>0 abbreviates the proved first-occurrence identity. This is not a 9.5% winning advantage.
- Finite k=4..7: 12+60+360+2520=2952 complement representatives. All integer arrays independently reconstructed by Python and actual compiled C++; the production worker only rechecks archived arithmetic, unless explicitly recorded otherwise.
- Length3: prior Elizalde-Lin result; extra horizon18 certificate. Displayed worst complement representative A=132, B=213 uses winsA=2947998300006576 and unresolved=12132147428205, denominator18!. Worst-case A probability <47/100. No novelty claim for this case.
- Original source: Elizalde and Lin, https://arxiv.org/html/2404.06585v4 ; journal https://doi.org/10.46298/dmtcs.16361 . Prior cluster method: Elizalde and Noy, https://arxiv.org/abs/1210.6061 .
- Correctness high; originality moderate under bounded audit. No full formalisation or external peer review claimed. Optimal reply and closed formulas for all races are outside scope.

Citation metadata for the additional primary-source retrieval is retained in primary-source.json; this is background corroboration, not an exhaustive new novelty search. The full response and temporary image URLs remain outside the repository.

Primary retrieval succeeded on 2026-10-26 via `valyu contents https://arxiv.org/html/2404.06585v4 --length 30000 --json`. Conjecture 6.1, the known length-three case, truncated short-case evidence and non-optimality discussion were read. `archived-certificate-check.log` records a successful fresh arithmetic/coverage comparison against archived independent outputs; it is not a fresh C++ reconstruction. `mechanism-check.json` records an independent brute-force check of the 120-order teaching example, cancellation example, interleaving example and exact displayed margins.
