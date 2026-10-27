# Readiness

Checked 18 October 2026. **Prepared for human author review.** No external referee has reviewed this manuscript. The dedicated literature and proof review has completed and its recommendations have been independently assessed.

## Exact contribution

For every integer `n >= 2`, the manuscript constructs a mass action network with `n` species, `n` reactions and stoichiometric rank `n - 1`. Exactly `n` positive equilibria occur on one stoichiometric class, all nondegenerate. Maximum source molecularity three is sufficient and, using the published quadratic obstruction, necessary. The count persists on an open set of rate constants and class levels.

The claim is about the mathematical mass action class. The conservation vector has mixed signs, the class is unbounded and some product complexes contain more than three molecules. Nondegeneracy is not stability. This does not construct a closed mass-balanced chemical mechanism.

## Proof and verification

The proof has five independent obligations, all addressed in the text:

1. The cubic source matrix has determinant `2^n`; its explicitly computed monomial exponents are distinct positive integers.
2. Descartes' rule proves interpolation rank, nonzero alternating coefficients, and exactly the prescribed simple positive roots.
3. Every displayed product is a nonnegative integral complex. The stoichiometric matrix has rank `n - 1`, right kernel spanned by the all-ones vector and left kernel spanned by the selected sign vector.
4. Taking logarithms describes the **entire** positive equilibrium set. Transversality to the conservation hyperplane proves invertibility of the restricted Jacobian.
5. The published quadratic obstruction excludes attainment for every `n >= 2`, including the special two-species case. The perturbation argument uses Descartes' rule to exclude additional degenerate roots.

Both exact programs were rerun successfully with Python assertions disabled. The generator checks 35 equilibria for `n = 2,...,8`; the separate standard-library checker reconstructs and differentiates the actual mass action equations and rejects corrupted products, concentrations and rates. Those finite checks support the formulas. **There is no Lean formalization of this theorem.** The all-`n` assertion rests on its written proof, not on enumerating examples.

## Sources and novelty boundary

The controlling source is Banaji and Feliu, *Positive equilibria in mass action networks: geometry and bounds*, Journal of Mathematical Biology 93, article 37 (2026), [publisher DOI](https://doi.org/10.1007/s00285-026-02429-8). The complete publisher PDF and the [PMC full text](https://pmc.ncbi.nlm.nih.gov/articles/PMC13481394/) agree on Corollary 4.21, the explicit open questions in Remark 4.23 and the quadratic obstruction in Corollary 5.16.

The obsolete single-author arXiv text returned by one extraction is excluded from the novelty assessment. The closely related anonymous October manuscript concerns `(n,n+2,n)` quadratic networks, not the `(n,n,n-1)` problem here. Banaji's September fold/cusp preprint and Feliu's current publication list have also been checked within the scope recorded in [source-review.md](source-review.md).

No exact earlier all-`n` theorem was located in those bounded checks. That is **not** a proof of priority. The completed dedicated review found no proof defect. Its recommendations were checked against the current manuscript and primary source: prior attainment at `n = 2` is now explicit, while two inaccurate suggestions about the source's quadratic exclusion and example were rejected. See [source-review.md](source-review.md).

## Files and remaining decisions

- The [public PDF](../../../../public-release/papers/cubic-equilibrium-sharpness.pdf) lists Harvey Yorke and Valyu DeepResearch as co-authors and records the contribution and review status. The earlier archival `paper.pdf` is omitted from the public export; its hash is retained in the release records.
- The two four-page presentations checked on 18 October built with no LaTeX warning, unresolved citation, overfull or underfull box in the recorded logs. These are historical build checks.
- The public presentation discloses the actual coding-agent contribution to the construction, proof, verification programs and manuscript, alongside DeepResearch's literature work. It does not claim that the human author has already approved the argument.
- [author-walkthrough.md](author-walkthrough.md) gives the argument in plain language and a short set of questions to resolve before the author signs off.
- Remaining work: human line-by-line review of the proof and the bounded priority assessment, and author approval. External specialist scrutiny would strengthen the result but has not occurred.

Correctness confidence: **high for the written argument and stated finite checks**. Originality confidence: **moderate** for the all-`n` construction, based on bounded primary-source checks. No acceptance forecast is implied.
