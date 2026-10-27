# Sharp equilibrium counts with cubic sources

For every integer `n >= 2`, an explicit mass action network with `n` species, `n` reactions and rank `n - 1` attains exactly `n` positive nondegenerate equilibria on one stoichiometric class. Maximum source molecularity **three** suffices and is minimal, using the published quadratic obstruction. The count persists on an open neighbourhood of the constructed rates and class level.

- [Paper](../../../../public-release/papers/cubic-equilibrium-sharpness.pdf), with shared [LaTeX source](paper.tex).
- [Independent mathematical and computational review](review.md).
- [Source, related work and priority scope](source-review.md).
- [Build and presentation checks](verification/build-review.md).
- [Readiness](readiness.md) and [plain-language author walkthrough](author-walkthrough.md).

The theorem answers the two questions in Remark 4.23 of Banaji and Feliu, *Positive equilibria in mass action networks: geometry and bounds*, Journal of Mathematical Biology 93, article 37 (2026), [DOI 10.1007/s00285-026-02429-8](https://doi.org/10.1007/s00285-026-02429-8). Local independent proof checks passed. External review and exhaustive priority assessment remain open.

For three species, the construction has equilibrium curve `(60t³, 85t², 11t⁴)`. Its intersections with `-X + Y + Z = 36` correspond exactly to the positive roots `1, 2, 3` of

```text
11t⁴ - 60t³ + 85t² - 36 = (t - 1)(t - 2)(t - 3)(11t + 6).
```

The conserved linear quantity has mixed signs and the class is unbounded. This counts equilibria, not stable states. Products can have molecularity above three. No closed mass-balanced chemical mechanism or experimental implementation is asserted.

## Reproduce

From this directory, using Python 3:

```sh
python3 -B -O verification/independent_cubic_check.py
sh build.sh
```

The independent checker uses only standard-library rational arithmetic. It reconstructs reaction vectors from the supplied source and product complexes, evaluates and differentiates the mass action monomials, and checks positivity, class membership and constrained Jacobian nonsingularity for all 35 recorded equilibria at `n = 2,...,8`. It also rejects corrupted products, concentrations and rates.

The build repeats that check and compiles both author presentations with `pdflatex` and `bibtex`. To regenerate the certificate as well, install SymPy and run:

```sh
sh build.sh --regenerate-certificate
```

The generator and independent checker are separate implementations. Their finite checks corroborate the explicit data; the all-`n` theorem is an analytic proof in the paper, not a finite computation or a Lean formalization. See [verification notes](verification/README.md).
