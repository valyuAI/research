# Evidence ledger

Read on 26 October 2026: full ../paper.tex, ../README.md, ../readiness.md, ../video-brief.md, ../verification/README.md, final max review ../verification/reviews/phylo-final-review.md, actual Newick witnesses, both quartet checker implementations and plot_triple.py. Final readiness controls claim scope.

- Definitions and quartet restriction: paper introduction. Primary background: Snir and Yuster, https://arxiv.org/abs/2602.23096 ; Currie et al., https://arxiv.org/abs/2607.12778v2 .
- 13-leaf witness: ../verification/families/triple13.nwk. Video preparation checked all 715 sets with both the distance and edge-split algorithms, no common quartet. Displayed quartet {1,4,7,13}: 47|1,13 then 14|7,13 in both relabelled trees. witness-data.json stores the actual topology, harmonic drawing coordinates and checked splits.
- Pairwise count 137: paper Proposition 3.1. This does not imply common agreement among all three.
- Universal 14-leaf proof: balanced-edge lemma plus exhaustive colouring statement, 135*(2002+3003+3432)=1,138,995 cases, zero failures. Saved resume records are evidence; the video worker does not rerun expensive searches.
- Hand grid argument: paper separated-sets step. The displayed [[2,1],[1,3]] matrix is illustrative, not claimed as a specific extraction from the 13-leaf counterexample.
- Potential: Psi(a,d)=min(ad,2a^2,2d^2). Exact worked example (16,32), options (7,21) and (9,11), budgets 98 and 99, guaranteed minimum 96. Theorem 2.7 and Lemma 2.6.
- Lean proves only the real potential inequality. Trees, iteration, finite enumeration, SAT, DP and h(3)=14 are not formalised in that file.
- h(3)=14; 23<=h(4)<=28. The 22-leaf family is checked over 7315 sets. Paused 23-leaf searches have no witness or UNSAT result and are not evidence.
- General upper bound: floor(3(4/sqrt(3))^(k-1))+1; it is a bound and gives 17 at k=3. Exact DP safe-pair checks give 28 at k=4, without a global strategy-optimality claim.
- General lower bound 2^k+2: already stated by Snir-Yuster, credited explicitly. The contribution does not claim discovery of that bound.
- Novelty is bounded by the documented searches. Correctness high; no external peer review asserted. Prior journal-access limits remain as recorded in readiness.

The original-source retrieval retained in primary-source.json is additional background reading, not a new exhaustive priority audit.

Additional primary retrieval succeeded on 2026-10-26 via `valyu contents https://arxiv.org/html/2607.12778v2 --length 25000 --json`. The retrieved definition of h(k) and prior iterated-exponential upper bound were read. The abstract contains the known volume-number typo noted in the retained review; no bibliographic claim is derived from that typo.
