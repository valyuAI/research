# Research campaign, 25-26 October 2026

This round retains **nineteen research packages**, bringing the collection to **26**. Seventeen are new-result candidates with explicitly bounded originality claims. One gives a new proof and correction of a known theorem; one is an independent verification of an earlier public proof. A count of packages is not a count of established discoveries.

All retained research packages have manuscripts and executed verification evidence. All 26 narrated videos are complete across the collection. The [collection index](../collection.md) gives current links and states. No external specialist review or publication priority is claimed by this inventory.

## Strongest new result candidate

The [common-quartet paper](../../maths/combinatorics/phylogenetics/common-quartet-number/) studies how many leaves force several evolutionary trees to agree on some four-leaf relationship. It proves **h(3)=14** and replaces the previous four-fold iterated-exponential general bound with

\[
2^k+2\le h(k)\le\left\lfloor3\left(\frac{1+\sqrt{13}}2\right)^{k-1}\right\rfloor+1.
\]

The lower bound belongs to Snir and Yuster. The upper bound is the proposed contribution: repeatedly cut the larger retained leaf set and track `min(ad,2a²,2d²)`. Its sharp one-step factor is `(7-sqrt(13))/18`. Lean verifies that numerical inequality and its equality example, not the tree theorem. Exact finite checks separately establish h(3)=14 and the bounds 23<=h(4)<=28, 34<=h(5)<=61 and 66<=h(6)<=125. Correctness confidence is high after review and replay; originality confidence is moderate-high within the inspected literature. The potential's sharpness does not prove the optimal growth base of h(k).

## Other substantial additions

- [Johnson solids](../../maths/geometry/rigidity/johnson-solids/): a complete fixed-edge, planar-face classification, with 47 locally rigid and 45 flexible solids. Six rigid examples have nontrivial first-order flexes. Exact certificates resolve those cases; no general new rigidity criterion is claimed.
- [Qudit codes](../../physics/quantum-information/error-correction/distance-three-qudit-codes/): the full admissible length spectrum for distance-three F_q-linear stabilizer codes with q>=3. The endpoint constructions and twelve table improvements are scoped against earlier Hamming, partial-spread and support-removal results. This is a mathematical classification, not a demonstrated hardware improvement.
- [Chemical robustness](../../chemistry/reaction-networks/mass-action/acr-multistability-bounds/): an obstruction in stoichiometric dimension two, sharp dimension and complex-count minima, and coupled examples that combine robust concentration with two stable positive states. Both sides of every reaction are at most bimolecular. The elementary three-species construction is not the main novelty claim.
- [Covering systems](../../maths/number-theory/covering-systems/min-modulus-six-odd-part-45/): a finite exact search plus a price recurrence rules out finite distinct coverings with minimum modulus six and odd part dividing 45 for every power of two.
- [Permutation races](../../maths/probability/competing-patterns/rotation-wins-penney/): right rotation is a winning reply for every permutation of length at least three in the independent continuous model. A uniform proof handles long patterns; exact counts and rigorous tails handle the shorter ones.

The remaining additions cover tree-balance impossibility, periodic billiards, repetition-free words, spectral graphs, Hex, knots, tournament manipulation, stochastic-network response and finite-field multiplication. Each entry's README states the actual theorem, evidence and nearest prior work.

## Corrections that changed the novelty assessment

The [Latin-tableau formula](../../maths/combinatorics/latin-squares/latin-tableaux-staircase-count/) already had a public proof with the same four-extension mechanism. Its first-resolution claim was withdrawn. The [seven-cube tic-tac-toe package](../../maths/combinatorics/combinatorial-games/cubic-tic-tac-toe-surplus/) gives a smaller certificate and repairs a case-analysis gap in a known result; it does not solve the six-cube game.

The [eleven-neuron CTLN example](../../maths/dynamical-systems/threshold-linear-networks/standard-parameter-counterexamples/) is smaller than the standard-parameter examples implied by prior work. It is minimal under deleting vertices, not proved globally smallest: the minimum lies between eight and eleven. The [spectral graph package](../../maths/combinatorics/spectral-graph-theory/four-negative-eigenvalues/) does not claim the already-known numerical bound A4=11 or the four rank-eight extremizers as new.

The [algebra package](../../maths/algebra/bilinear-complexity/mu-q-2-2/) credits the known symmetric binary value and earlier subspace methods. The [tiling tables](../../maths/geometry/tilings/marked-polyform-heesch-numbers/) establish maxima in a precise lattice marking model; they do not break the Heesch record, and overlap with some older tables remains unresolved. The [knot census](../../maths/topology/knot-theory/bridge-thirteen-crossing-census/) settles 25 entries relative to a pinned list; possible overlap with broader family theorems remains a priority question.

## Verification and remaining work

The combined Lean library builds and passes its axiom audit for **153 project declarations: 96 named theorems and 57 generated helpers**. The earlier independent six-checker Linux replay covered 121 declarations. The retained [26 October replay record](../verification/formal-library-20261026/ci-replay.json) records successful six-checker replay of the expanded 153-declaration library. The [coverage ledger](../formal-coverage.md) separates these checks and lists every formalization boundary; this replay does not cover the separate elasticity determinant package or the papers' unformalized claims.

Package evidence includes written proofs, independent exact implementations, retained certificates and controls that deliberately corrupt inputs. A numerical search is not promoted to a proof: Hex's lambda(6)<=8, the optional odd-part-135 covering extension and three paused 23-leaf quartet searches remain outside the certified results. One unfinished draft is excluded from the collection count and release scope.

The completed videos contain editable scenes, narration, audio, subtitles and a playable MP4. Decode, timing and frame-inspection records are supplied; listening review has not been performed. The final integration review found validation defects. The fixes and targeted checks passed a fresh independent closure review. Local integration and media checks are complete. No public announcement, submission or contact with source authors has been made.
