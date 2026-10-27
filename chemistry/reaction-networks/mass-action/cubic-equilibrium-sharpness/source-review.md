# Source and priority review

Checked 18 October 2026. This is a bounded primary-source assessment, not an assertion of exhaustive historical priority.

## The current published question

Murad Banaji and Elisenda Feliu, *Positive equilibria in mass action networks: geometry and bounds*, Journal of Mathematical Biology **93**, article 37 (2026), [DOI 10.1007/s00285-026-02429-8](https://doi.org/10.1007/s00285-026-02429-8), published 17 August 2026.

The relevant sections of the complete publisher PDF were read directly:

- Corollary 4.21(i), printed page 38: `(n,n,n-1)` networks have at most `n` positive nondegenerate equilibria on one stoichiometric class.
- Remark 4.23, pages 38-39: attainability for general `n` and the minimum source molecularity remain explicit questions.
- Corollary 4.21(ii), page 38: bounded classes admit at most two positive nondegenerate equilibria.
- Corollary 5.16, page 56: quadratic `(n,n,n-1)` networks admit at most two such equilibria; the smallest `n` attaining two in the quadratic class is three. This includes the exclusion needed for the two-species minimality claim.

The manuscript supplies the cubic-source construction and combines it with the last statement to establish minimum maximum source molecularity three. The monomial parametrisation method, general upper bound and quadratic obstruction are credited to the published source. Descartes' rule of signs and the implicit function theorem are classical ingredients.

An arXiv content extraction previously returned an obsolete single-author manuscript despite a later-version URL. It is not used to determine which questions remain open. Current publisher statements, authorship and equation context control this package's attribution.

## Closely related October 2026 manuscript

The complete ten-page [*Sharp positive-equilibrium counts in quadratic mass-action networks with two more reactions than species*](https://zenodo.org/records/23146115/files/paper.pdf?download=1), signed **Anonymous**, dated 4 October 2026, publication candidate version 2, was read. It presents a quadratic `(n,n+2,n)` family with `n+1` positive nondegenerate equilibria, addressing Remark 5.8 of Banaji and Feliu. It explicitly credits a Phillipson-Rojas polynomial family for its underlying extremal root construction.

That manuscript concerns full-rank networks with two additional reactions. The present result concerns rank `n-1`, exactly `n` reactions, and optimal maximum source molecularity for attaining `n` equilibria on one stoichiometric class. No direct collision with this statement was identified in the inspected manuscript. Its repository maintainer is not substituted for the scholarly author; the bibliography records Anonymous and publication-candidate status.

An independent source audit also inspected the introduction, examples, main theorems, rank-deficient results and conclusions of Banaji's [*On the computation of fold and cusp bifurcations in mass action networks via dual equations*, arXiv:2609.07265v1](https://arxiv.org/html/2609.07265v1). That work concerns fold/cusp criteria and quadratic cusp exclusions; no all-`n` cubic-source attainability or minimum-source-three theorem was found in those inspected sections. This is a bounded comparison, not an exhaustive priority finding.

## What is established locally

Independent local review agrees with the all-`n` argument, the valid-product construction, restricted Jacobian nondegeneracy, the open parameter-neighbourhood argument and the published minimality implication. A separate rational checker reproduces all 35 recorded finite examples without importing the generator or using a computer algebra system.

These checks do not establish external peer review, exhaustive priority, experimental realizability or simultaneous stability of the equilibria. No conclusion relies on the absence of search matches. No third-party full text is redistributed in this package.

## Submission-preparation refresh, 18 October 2026

A fresh full-text retrieval from [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC13481394/) returned the joint-authored published article, including Corollary 4.21, Remark 4.23 and Corollary 5.16. These statements agree with the previously inspected publisher PDF. A search hit for the arXiv record again carried the obsolete single-author title; it was not treated as the current source.

The complete [Feliu publication list](https://web.math.ku.dk/~efeliu/research.html) was retrieved and its current preprint entries inspected. The [Banaji fold/cusp record](https://arxiv.org/abs/2609.07265) still identifies the 7 September 2026 submission and version 1. No exact matching cubic sharpness theorem appeared in the inspected entries. The fresh exact-title/source-molecularity search located the same anonymous full-rank quadratic candidate already compared above; unrelated general-chemistry hits were excluded. These are bounded checks of named primary records, not evidence about unlisted work.

The dedicated DeepResearch review subsequently completed on 18 October. Its proof assessment agrees with the local all-`n` argument and identifies no mathematical defect. Each recommendation was checked against the current manuscript and published source. Two clarifications were accepted: attainment at `n = 2` was already known, and the construction has exactly `n` distinct, nontrivial reactions.

Two recommendations were rejected. Corollary 5.16 does explicitly exclude quadratic attainment at `n = 2`, through its statement that the smallest attaining dimension is three. Also, our two-species network is different from the source's example: our reactions are `2X+Y -> X` and `2Y -> X+3Y`, whereas its example is `X+2Y -> 3Y` and `Y -> X`. Prior attainment is credited without claiming the networks coincide.

The remote report's supplied-source hash was not confirmed, so its reported computation is not treated as a replay of the current canonical files. The independently run local checkers remain the controlling computational evidence. The report located no exact earlier all-`n` construction in its search, but this remains a bounded novelty assessment, not established priority or external peer review. Raw retrievals, the report and its detailed adjudication are retained outside the curated paper package.
