# Evidence ledger

Read on 26 October 2026: full ../paper.tex, ../README.md, ../readiness.md, ../video-brief.md, ../verification/README.md, final max review ../verification/reviews/phylo-final-review.md, actual Newick witnesses, both quartet checker implementations and plot_triple.py. Final readiness controls claim scope.

- Definitions and quartet restriction: paper introduction. Primary background: Snir and Yuster, https://arxiv.org/abs/2602.23096 ; Currie et al., https://arxiv.org/abs/2607.12778v2 .
- 13-leaf witness: ../verification/families/triple13.nwk. Video preparation checked all 715 sets with both the distance and edge-split algorithms, no common quartet. Displayed quartet {1,4,7,13}: 47|1,13 then 14|7,13 in both relabelled trees. witness-data.json stores the actual topology, harmonic drawing coordinates and checked splits.
- Pairwise count 137: paper Proposition 3.1. This does not imply common agreement among all three.
- Universal 14-leaf proof: balanced-edge lemma plus exhaustive colouring statement, 135*(2002+3003+3432)=1,138,995 cases, zero failures. Saved resume records are evidence; the video worker does not rerun expensive searches.
- Hand grid argument: paper separated-sets step. The displayed [[2,1],[1,3]] matrix is illustrative, not claimed as a specific extraction from the 13-leaf counterexample.
- Potential: Psi(a,d)=min(ad,2a^2,2d^2). Exact worked example (16,32), options (7,21) and (9,11), budgets 98 and 99, guaranteed minimum 512c approximately 96.553208, with c=(7-sqrt(13))/18. Theorem 2.7 and Lemma 2.6.
- The updated Lean file checks the sharp c inequality and its equality example. Trees, iteration, finite enumeration, SAT, DP and h(3)=14 are not formalised in that file.
- h(3)=14; 23<=h(4)<=28. The 22-leaf family is checked over 7315 sets. Paused 23-leaf searches have no witness or UNSAT result and are not evidence.
- General upper bound: floor(3 beta^(k-1))+1, beta=(1+sqrt(13))/2; it is a bound and gives 16 at k=3. The thresholds for k=1..6 are 4,7,16,37,85,195. Exact DP safe-pair checks give 28 at k=4, without a global strategy-optimality claim.
- General lower bound 2^k+2: already stated by Snir-Yuster, credited explicitly. The contribution does not claim discovery of that bound.
- Novelty is bounded by the documented searches. Correctness high; no external peer review asserted. Prior journal-access limits remain as recorded in readiness.

The citation metadata in primary-source.json records additional background reading, not a new exhaustive priority audit. The full retrieval response remains outside the repository.

Additional primary retrieval succeeded on 2026-10-26 via `valyu contents https://arxiv.org/html/2607.12778v2 --length 25000 --json`. The retrieved definition of h(k) and prior iterated-exponential upper bound were read. The abstract contains the known volume-number typo noted in the retained review; no bibliographic claim is derived from that typo.

## Accepted sharper production source

The updated paper.tex, readiness.md, video-brief.md and verification/reviews/phylo-sharp-potential-review.md were read for this production continuation. The coordinator accepted review DR-017. The exact two-case argument establishes c=t^2=(7-sqrt(13))/18 and beta=1/t. Normalize a=1 and cap d/a at 2 for the worst case; reflect the cut so x+y<=1. At x>=t the first diagonal works; at x<t the second works. The plot shows the crossing x^2=(1-x)/3; the paper checks every term of each minimum. The irrational sharpness example is not animated as a finite tree. Optimality concerns only this real-variable inequality, not the growth base or every tree strategy.

The sharper written proof is accepted and independently reviewed. The review's incomplete tree simulation is not counted as evidence. Root completed the sharp update separately. This video worker read its final readiness and execution records without rerunning the scientific package. Formal production update received directly from the coordinator: potential_step_sharp and potential_step_sharp_witness compiled with exit 0; the subsequent saved axiom audit lists only propext, Classical.choice and Quot.sound for both theorems. These cover the sharp numerical inequality and equality example only. The coordinator also reports 613 exact executable families, k=1..6 at n=4,7,16,37,85,195, with each-step potential/separation and final distance checks. The saved executable log was read and confirms all 613 families passed. This is a randomized executable sanity check with exact checks on each sampled family, not an exhaustive proof over all families. The updated package Lean copy, readiness, brief and axiom record were read directly; these were not rerun by this video worker.

Final readiness update read before delivery: sharp update complete, current nine-page paper inspection passed, old full-game replay retained for unchanged finite computations. The sharp completion manifest is verification/results/sharp-potential-completion-20261026.json. Scientific correctness confidence is high; originality confidence remains bounded by the documented literature search and journal-access limits.

Locked input provenance: all13 scientific file hashes in the final coordinator manifest were checked against disk and match. The manifest is preserved verbatim as scientific-completion-manifest.json; final-scientific-source-sha256.json records the same hashes plus the manifest itself. Older snapshots are retained only as historical production evidence. No mathematical change occurred between rendering and the locked documentation/layout update.
