# A periodic waiting-time entropy counterexample

A smooth three-state Markov network has exactly zero entropy production under the source's definition, but its proposed forward-protocol waiting-time estimator is strictly positive and finite. This disproves the unrestricted conjecture in published Eq. (18) of Maier et al., [Journal of Statistical Physics 191, 104 (2024)](https://doi.org/10.1007/s10955-024-03315-7), with the estimator defined in Eq. (17). These correspond to Eqs. (15) and (14) of [arXiv:2406.12657v1](https://arxiv.org/abs/2406.12657v1). The separate reversed-protocol theorem, published Eq. (16) and arXiv-v1 Eq. (13), is unaffected.

[Paper](../../../../public-release/papers/periodic-waiting-time.pdf) · [LaTeX](paper.tex) · [Written proof](proof.md) · [Independent review](review.md) · [Source review](source-review.md)

[Readiness](readiness.md) · [Plain-language author walkthrough](author-walkthrough.md)

Both presentations are four pages. The main PDF has Harvey Yorke and Valyu DeepResearch in an archival two-name author layout; the journal variant has Harvey Yorke as sole author and a statement identifying the literature, proof-development, verification and writing assistance. The mathematical text is identical. This is a research draft, not an externally refereed publication. Human author approval and priority review remain open.

## The example

Take period `2*pi` and `0 < epsilon < 1`. On the undirected edges `12`, `23`, and `13`, use symmetric rates `1 + epsilon*cos(t)`, `1 + epsilon*sin(t)`, and `1`, respectively. Observe the first two edges in both directions and hide the third.

The distribution is uniformly `1/3` at every phase, so the defined entropy production is zero. Event-conditioned waiting densities `f = Psi(12 -> 23)` and `g = Psi(32 -> 21)` instead satisfy `(f-g)'(0) = epsilon^2`. Equal mean event rates make the full estimator `4/3` times a normalized KL divergence. The derivative proves it is positive.

## Reproduce

Using only Python 3 and its standard library:

```sh
python3 -B -O verification/check_short_lag.py
```

This replays six exact rational Fourier-polynomial identities. The checker does not use floating-point arithmetic or Python assertions. See [verification scope](verification/README.md).

Run `sh build.sh` to rebuild both PDFs with `pdflatex` and BibTeX, using the supplied diagram. `sh build.sh --redraw-figure` also needs matplotlib and regenerates a small illustrative quadrature plot. The exact theorem does not depend on that quadrature. The plotted 128- and 256-node results differed by less than `7e-17` in the checked build.

## Scope and prior work

Hartich and Godec already showed equilibrium waiting-time false positives. Harunari, Fiore and Barato already distinguish reversed-protocol waiting data in the periodic setting. The specific contribution here is an explicit counterexample to Maier et al.'s forward-only conjecture, not the general observation that apparent time asymmetry can differ from dissipation.

The [independent mathematical audit](review.md) checks the event-phase weighting, normalization, support, and finiteness arguments. The [focused review disposition](adversarial-review.md) records an ancillary error in a completed adversarial report that was excluded from the paper. That report's extra numerical leads are not part of this result.

The complete publisher PDF was retrieved and inspected on 18 October 2026. It retains the same forward-only conjecture and adds no constant-prefactor restriction to the general setup. The numerical appendix has its own rate choices, including an explicit exception to its usual prefactor choice; those choices are not asserted as a general hypothesis. The dated comparison is in [the source review](source-review.md#published-version-verification-18-october-2026).

There is no Lean formalization of this proof. The exact checker covers only the stated polynomial identities. No claim is made about the energetic cost of an external device implementing the time-dependent rates. No third-party full text is redistributed in this package.
