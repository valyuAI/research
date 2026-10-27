# Readiness

Updated 18 October 2026. **Technically prepared for human review.** The manuscript has not been submitted to a journal or externally reviewed.

## The claim to defend

A generic three-dimensional density-normalized elasticity tensor has twenty-one independent parameters. Its three unordered phase speeds, known as functions of direction, uniquely determine that tensor, even against exceptional complex competitors. More economical sufficient data are twenty-two scalar polynomial invariants, or the spectra in eleven generic directions. Seven or fewer directions cannot suffice; the minimum among eight, nine, ten and eleven remains open.

This resolves Conjecture E in the verified 30 April 2025 revision of de Hoop, Ilmavirta, Lassas and Várilly-Alvarado. It does not claim that ultrasonic inversion was invented here, that every symmetric material is identifiable, or that noisy measurements can be inverted stably.

## Completed checks

- Complete written-proof review, including both recursive normal-space reductions and the full eleven-direction collision incidence. No gap identified in this internal review.
- A completed DeepResearch review of the full eleven-direction draft independently checked the dimension argument and found no mathematical error. It did not replay every certificate; its findings were adjudicated against the current proof, primary sources and successful verification records.
- Fresh full exact-arithmetic replay on 18 October: all default gates passed. The source matrices are reconstructed from the elasticity equations; the verifier does not merely accept embedded matrices.
- All eleven second-normal-quotient determinant identities compiled in Lean and passed the axiom audit in CI run `39114539272` (an earlier CI whose log is not retained here; see the [formal coverage ledger](../../../../docs/formal-coverage.md#linux-ci-execution-record)). Allowed axioms are `propext`, `Classical.choice`, and `Quot.sound`.
- Separate exact, standard-library verification of the finite-direction cubic slice and its eleven membership identities. This part is not formalized in Lean.
- Current target-paper version and the precise conjecture checked against the actual v2 text. A misleading older extraction from an explicitly versioned URL was excluded.
- Targeted later-work search and comparison of classical inversion literature. See [the source audit](SOURCE_FACTCHECK.md) for what was read and what remains unavailable.
- Sole-author variant ([public paper](../../../../public-release/papers/generic-stiffness-recovery.pdf)), editable LaTeX and a reproducible exact-arithmetic package are present. The research-assistance statement records contributions to proof development and manuscript drafting, as well as literature retrieval.

## Remaining work

1. **Human author review.** The author has not yet completed a line-by-line review of the argument, the exact claims or the assistance statement.
2. **Closest-prior full text.** Obtain and inspect Aristégui and Baste (1997), DOI [10.1121/1.418040](https://doi.org/10.1121/1.418040), especially its uniqueness and finite-measurement claims. The present audit has the publisher abstract only.
3. **Outside mathematical scrutiny.** A specialist review of the algebraic-geometric deductions is strongly advisable and has not occurred.

Correctness confidence is high for the checked arithmetic and moderate-to-high for the written geometric argument. Originality confidence remains moderate while the closest classical full-text comparison is unresolved. Neither confidence label is a publication guarantee.

## Author walkthrough

The central idea is to prove that ambiguous measurements occupy too few parameters to affect a generic material. Work through these checkpoints in order, with the paper open.

1. **What the instrument measures.** In a unit direction `n`, the Christoffel matrix has the three squared phase speeds as eigenvalues. Their unordered values determine trace, second characteristic coefficient and determinant. They do not give the polarization eigenvectors. Density has already been divided into stiffness.
2. **Turn ambiguity into equations.** For two tensors write `C = X + H` and `C' = X - H`. An ambiguity means `H != 0`. Equality of the measurements gives a trace-zero condition on `H`, a bilinear quartic equation in `X,H`, and a cubic determinant equation.
3. **Why the difficult object is linear algebra.** For fixed `H`, the quartic equation is the linear system `L_H X = 0`, a 15-by-21 matrix. The trace-zero differences form a 15-dimensional space. If `L_H` has rank `r`, its solution space for `X` has dimension `21-r`.
4. **Why one rank check is insufficient.** A full-rank example only handles an open set of differences. Low-rank differences have larger kernels and could create a dominant family of ambiguities. The key proposition bounds every rank locus: `dim R_r <= r-1` for ranks 6 through 14, with no nonzero rank below 6.
5. **How the rank proposition is proved.** Borel fixed points force each projective component through a short explicit list of points. Successive normal-space calculations bound local dimensions there. Exact minor identities handle the small normal matrix; empty projective slices handle the highest ranks. Be able to explain why the tangent cone is contained in the linearized rank locus, rather than equal to it.
6. **The dimension finish.** Every deficient-rank family has dimension at most `(r-1)+(21-r)=20`. The full-rank incidence has dimension 21, but one determinant evaluation cuts it properly: it is nonzero at an explicit isotropic difference tensor and zero midpoint. Its dimension drops to at most 20. Projection cannot raise dimension, so the ambiguous tensors lie in a proper subset of the 21-dimensional tensor space.
7. **Why finite-field arithmetic is enough.** A Bezout or pure-power certificate excludes zeros over the algebraic closure of the finite field. The intersection is projective over the integers, hence its image is closed. A nonempty generic fiber would force a point above every prime. This argument does not pretend that a modular polynomial identity lifts coefficient by coefficient to characteristic zero.
8. **Why eleven directions work.** Classify common zeros of the quartic and sextic collision polynomials by their common-factor degree. Count the parameters of the tensor pair and allowable direction choices in every case, including when either polynomial vanishes identically. All totals are at most 42, below the 43 parameters of a tensor plus eleven directions. The separate cubic-slice certificate closes the degree-four case.
9. **Why seven cannot work.** At seven directions, the trace data have at most six independent parameters and the other two scalar invariants provide at most fourteen. Twenty data parameters cannot generically distinguish twenty-one tensor parameters.
10. **Where the proof stops.** Genericity excludes a proper algebraic subset; it does not describe every exceptional material. The theorem supplies no explicit eleven-direction configuration, robust solver, noise bound, or separation of density from stiffness. Lean checks specified identities, not this entire argument.

A useful final exercise is to explain the proof without saying only that “the computer checked it”: identify exactly which equations the certificates verify, which geometric theorems turn those identities into dimension bounds, and why those bounds exclude all competitors.
