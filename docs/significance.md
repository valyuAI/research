# Significance and publication position

This is an editorial assessment of the current evidence, not an external referee report. Mathematical correctness, originality and importance are different questions.

## 26 October update

The [new campaign](campaigns/2026-10-25-discoveries.md) adds nineteen packages. The strongest new candidate is [common quartets](../maths/combinatorics/phylogenetics/common-quartet-number/): an exact h(3)=14 result and a general upper bound with exponential base about 2.303, replacing a four-fold iterated exponential. This is a change in the known growth scale, not merely an additional finite case. The prior lower bound has base two, so the argument places the growth rate in a substantially narrower range. Correctness confidence is high after exact replay and adversarial proof review; originality confidence is moderate-high within the inspected sources. Its sharp potential lemma is formalized, but the tree theorem is not. This is the leading candidate from the new round for a substantial specialist contribution; it is not yet an externally reviewed major result.

The [Johnson-solid classification](../maths/geometry/rigidity/johnson-solids/) is another substantial specialist candidate: 47 rigid and 45 flexible in the fixed-edge, planar-face model, with exact treatment of the six cases invisible to first-order rigidity. Its contribution is a complete natural classification, not a new general rigidity theorem. The [qudit-code classification](../physics/quantum-information/error-correction/distance-three-qudit-codes/) covers every admissible length in the stated linear stabilizer class and improves twelve pinned table entries. Its closest constructions and reduction techniques are credited; the entire subject and all endpoint cases are not new. Correctness confidence is high for both; originality confidence remains moderate to moderate-high and bounded by the recorded searches.

The [chemical robustness package](../chemistry/reaction-networks/mass-action/acr-multistability-bounds/) supplies a dimension-two obstruction and sharp minima, rather than just an isolated network. The [covering-system obstruction](../maths/number-theory/covering-systems/min-modulus-six-odd-part-45/), [permutation-race theorem](../maths/probability/competing-patterns/rotation-wins-penney/), [integer tree-weight impossibility](../maths/combinatorics/phylogenetics/colless-like-integer-weights/) and [special-octagon periodicity](../maths/dynamical-systems/billiards/special-octagon-symplectic-billiards/) are credible focused theorem candidates. Their exact hypotheses, primary comparisons and verification limits control their significance.

Several other packages settle finite cases, certify a table or improve a known example. Those are useful contributions but should not be described as general breakthroughs. In particular, the [Latin-tableau note](../maths/combinatorics/latin-squares/latin-tableaux-staircase-count/) has an earlier public proof with the same mechanism and carries no novelty claim. The [tic-tac-toe note](../maths/combinatorics/combinatorial-games/cubic-tic-tac-toe-surplus/) improves a proof of the known seven-cube result and repairs a case-analysis gap; the six-cube question is untouched. The [collection index](collection.md) records the boundary for every package.

## 1. Elasticity: generic inverse recovery

The [elasticity paper](../public-release/papers/generic-stiffness-recovery.pdf) gives an exact computational proof of generic three-dimensional stiffness recovery from wave-slowness data. It addresses Conjecture E of de Hoop, Ilmavirta, Lassas and Várilly-Alvarado, still stated as a conjecture in the [latest retrieved version](https://arxiv.org/abs/2307.03312) of their paper. The theorem works over the complex numbers and rules out every distinct partner for a generic tensor, including partners outside the generic set.

The proof also gives stronger data statements: six trace coefficients, fifteen second-characteristic coefficients and one determinant evaluation suffice, and fifteen explicit directions recover those data. A further exact certificate proves that eleven generic directions suffice. A dimension argument rules out seven or fewer, leaving eight through ten unresolved. The eleven-direction result is generic in the choice of directions; it does not say that every set of eleven works. These results concern identifiability, without guaranteeing stable inversion of noisy measurements or separate recovery of mass density and physical stiffness.

This is a substantive inverse-problems result. It removes the conjectural algebraic step from the source paper's three-dimensional tensor-recovery and two-layer results, while retaining their other hypotheses. The potential relevance is to anisotropic material characterization and geometric seismic inverse problems. It does not establish a new experimental instrument or measured performance improvement.

**Assessment:** the collection's strongest candidate for a substantial specialist paper. Correctness confidence is high after independent reconstruction of the tensor algebra, geometric review and exact certificate replay. Eleven explicit polynomial identities certify the two hardest recursive rank bounds; a separate set of eleven identities certifies the new finite-direction dimension bound. Both replay without a Gröbner-basis engine. Lean verifies the collision algebra and eleven original-minor determinant identities, not the full geometric theorem. Originality confidence is moderate: current author pages and closely related 2026 papers were checked, with no earlier resolution identified, but priority and external peer review remain open. The full text of the classical Aristégui-Baste measurement-design paper remains an unresolved comparison for the finite-direction extension. Journal acceptance and broad impact cannot yet be predicted.

## 2. Truncated dodecahedron: a resolved rigidity example

The [rigidity paper](../public-release/papers/truncated-dodecahedron.pdf) proves that the classical truncated dodecahedron cannot deform continuously while preserving its original edge lengths and keeping its faces flat. Face shapes are allowed to change, so the familiar theorem for fixed rigid faces does not answer this question. The [July 2026 source](https://arxiv.org/abs/2607.09252) leaves this solid as the single unresolved case in its tested collection because its second-order obstructions vanish.

The proof finds a higher-order obstruction through exact arithmetic: four cubic polynomials over a finite field admit direct identities forcing all four infinitesimal parameters to vanish locally. A standard specialization argument then proves isolation of the actual characteristic-zero configuration. The complete arithmetic certificate replays in a fraction of a second using only Python's standard library, including a separate reconstruction of the solid and its equations.

**Assessment:** a substantial specialist research-note candidate and the collection's clearest geometric demonstration. Correctness confidence is high after independent source reconstruction, certificate replay and theoretical audit. This closes an explicit recent open example; it does not solve the general rigidity problem, introduce a new physical material, or establish an ancient unresolved claim. Originality confidence is moderate: the source and current author materials retain the question, and the bounded search identified no earlier solution. The completed focused review found no earlier resolution within its bounded search; external specialist review remains open. The argument is computer-assisted but not Lean-formalized.

## 3. Hales-Jewett: a compact exact-family theorem

The explicit coloring establishes an infinite prime-successor family of exact off-diagonal Hales-Jewett numbers. In particular, it closes the first undecided alphabet size in the cited July 2026 paper. The construction also improves its prime-based lower bound by one for every larger alphabet. Combined with that source's reported geometric computation, it gives a negative answer to the source's comparison question; that computation has not been independently certified here.

The contribution is compact and mathematically substantive: a boundary repair turns a modular construction into an exact-family theorem. Its strongest feature is the combination of a readable proof, exhaustive verification of the first new instance and a full Lean formalization of the combinatorial result.

**Assessment:** a credible specialist research-note candidate. Correctness confidence is high. Originality confidence is moderate after the bounded literature review. There is presently no basis for claiming a major breakthrough or premier-journal significance. The best lead is the actual theorem and proof, not an inflated account of its applications.

## 4. Conjugate restart: broader context, unsettled priority

The written result strengthens a stationary conjugate prescription to a global and unique optimum over the stated class of renewal laws. Its finite-state converse identifies reversibility through a universal optimality property under cyclicity. These are potentially useful structural results for first-passage and resetting theory.

The ratio-gap inequality is established machinery and is credited explicitly. The exponential conjugate pair was also known. The possible contribution is the global renewal-law conclusion, its equality case and the reversibility characterization. The paper does not establish an improvement in a deployed search system, and its Brownian theorem and converse are not yet formalized in Lean.

**Assessment:** potentially a useful specialist theoretical paper, with broader subject appeal than the combinatorics note. Originality remains provisional and deserves focused review by researchers in resetting and stochastic-process optimization before a strong novelty claim.

## 5. Lotka-Volterra: verification note, no priority claim

Generic equivalence of tree families is a substantive algebraic classification question. The self-contained reconstruction proof and explicit genericity conditions are useful, and the path obstruction is formally checked.

However, the earlier withdrawn SSRN record announces a closely matching theorem. Its mathematical text was unavailable, so exact overlap, hypotheses and proof methods cannot be compared. Withdrawal does not erase the announcement. This collection does not claim the first resolution.

**Assessment:** retain it as an independent reconstruction and verification note. It is not currently a defensible new-discovery headline. A stronger publication case would require a demonstrably new extension, a materially different contribution, or a substantive comparison with the unavailable earlier manuscript.

## 6. Periodic entropy inference: a specific conjecture counterexample

The [four-page paper](../public-release/papers/periodic-waiting-time.pdf) gives a smooth three-state Markov network with zero entropy production under the source definition and a strictly positive, finite waiting-time estimate. It disproves the unrestricted forward-protocol upper-bound conjecture in Maier et al., Journal of Statistical Physics 191:104 (2024), Eq. (18), corresponding to arXiv:2406.12657v1, Eq. (15). A derivative identity proves the violation for every modulation amplitude between zero and one; no simulation is needed.

The practical lesson is specific: changing kinetic rates can create time-order information that this estimator confuses with dissipation. Results using the reversed protocol remain intact. The energetic cost of a device generating the protocol is outside the model. Hartich and Godec already established other equilibrium waiting-time false positives, and Harunari, Fiore and Barato provide close periodic-protocol context.

**Assessment:** a credible short theoretical note or comment, with high confidence in the explicit counterexample after independent source, algebra and probability audits. Originality confidence is moderate for the specific conjecture resolution and low for any broad claim of a new false-positive mechanism. The completed focused review found no exact collision in the sources it inspected. This is useful corrective science, not a new thermodynamic law or an experimental discovery.

## 7. Cubic reaction networks: a sharp bound and minimum degree

The [four-page chemistry paper](../public-release/papers/cubic-equilibrium-sharpness.pdf) constructs, for every n ≥ 2, an n-species, n-reaction network of stoichiometric rank n−1 with exactly n positive nondegenerate equilibria on one class. Maximum source molecularity three suffices for every n. The published quadratic obstruction proves that three is also minimal. This addresses both questions in Remark 4.23 of [Banaji and Feliu, Journal of Mathematical Biology 93:37 (2026)](https://doi.org/10.1007/s00285-026-02429-8).

The proof combines a fixed cubic source matrix, sparse interpolation, valid integral reaction products and a transversality argument. The count persists on an open neighborhood of rate constants and class levels. Two exact checkers validate all 35 equilibria for n = 2 through 8; the second uses only standard-library rational arithmetic and differentiates the actual mass-action equations independently. The general theorem rests on the written proof, not those finite tests, and is not Lean-formalized.

**Assessment:** a strong specialist research-note candidate with high correctness confidence after independent proof review and exact replay. The dedicated literature audit is complete and independently assessed; originality confidence remains moderate because its search is bounded. The current published paper explicitly leaves the general question open; attainment at n = 2 was already known and is credited. A related October 2026 candidate resolves a different, full-rank quadratic problem and is credited. The conserved quantity has mixed signs and the classes are unbounded; product molecularities can exceed three. No simultaneous stability, closed mass-balanced mechanism or experimental discovery is claimed. Its significance is an exact answer about the minimum kinetic degree needed to attain a sharp equilibrium count.

## Relative strength of evidence

By correctness and originality evidence, the strongest results of the 25-26 October round are the common-quartet growth bound and the Johnson-solid and qudit-code classifications. In the earlier collection, elasticity is the broadest inverse-problems result, the truncated dodecahedron settles a concrete geometric open problem, and Hales-Jewett has a compact proof with complete formalization. Restart's priority is provisional, and Lotka-Volterra and Latin tableaux are independent verification notes. The damping draft and one further unfinished draft remain exploratory. These assessments are limited to the documented checks and literature comparisons.
