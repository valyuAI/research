# Source and scope fact check

Checked 18 October 2026. Literature retrieval used the Valyu CLI. No author was contacted and no manuscript was submitted or published.

## The named conjecture

Primary source: Maarten V. de Hoop, Joonas Ilmavirta, Matti Lassas, and Anthony Várilly-Alvarado, *Reconstruction of anisotropic stiffness tensors from partial data around one polarization*, [arXiv:2307.03312v2](https://arxiv.org/abs/2307.03312v2), revised 30 April 2025. The first version was posted in July 2023. A Rice-hosted PDF uploaded in February 2026 is a hosting date, not a new publication date.

The current source's Conjecture E, on physical PDF page 10, asks for generic injectivity of the three-dimensional reduced-stiffness-to-slowness-polynomial map. The tensor has the usual minor and major symmetries and 21 independent coordinates. Its density is absorbed into the stiffness entries.

Theorem D establishes generic two-dimensional uniqueness, four-to-one aligned orthorhombic recovery, and two-to-one aligned monoclinic recovery. These are compatible with a full-space generic theorem: special symmetry families can lie within the exceptional set. The source also gives an exact singleton fiber for a specific material, which is evidence for the conjecture but does not by itself prove generic global injectivity.

Theorems A and B have three-dimensional conclusions conditional on Conjecture E. The present argument removes only that algebraic uniqueness dependency. Their other geometric, admissibility, positivity, and measurement hypotheses remain in force.

The draft's 22-invariant, eleven-generic-direction and fifteen-explicit-direction statements are deductions from the collision proof and its additional certificate. They are not attributed to the source. The sharp minimum direction count remains between eight and eleven.

### Source-version control

The arXiv abstract page inspected on 18 October still identifies v2, revised 30 April 2025, and states the triclinic uniqueness conjecture. However, content retrieval for the explicitly versioned arXiv HTML URL returned an older text with the title *Reconstruction of generic anisotropic stiffness tensors from partial data around one polarization*. Its abstract asserted broader uniqueness than the revised paper. A URL containing `v2` did not establish that the extracted text was v2.

The audit therefore uses the [author-hosted Rice PDF](https://bpb-us-e1.wpmucdn.com/blogs.rice.edu/dist/8/4754/files/2026/02/Reconstruction-of-generic-anisotropic-stiffness-tensors-from-partial-data-around-one-polarization.pdf). Its internal header reads `arXiv:2307.03312v2`, dated 30 April 2025. The corrected abstract, Theorem D, Conjecture E on printed page 10, and the explicit dependencies in Theorems A(2) and B were checked in the extracted full text. Its February 2026 hosting path is not a new manuscript version. The extracted text SHA256 is `e38702c6cf6cbc821dbfc422f4fdd3a8535a8f45dea53322f17747b803c9cb8c`.

The version mismatch is a retrieval issue, not a mathematical contradiction in the current source. The old abstract is not evidence that the conjecture has already been resolved.

### Targeted later-work and classical-prior search

The 18 October search covered the named conjecture and slowness map, global uniqueness from finite phase spectra, and classical recovery of all twenty-one constants. No inspected source supplied the same full-space generic theorem or an eleven-direction global uniqueness theorem. This is a bounded negative search, not proof of originality.

The recent paper by Ilmavirta, Saksala and Schlüter, [*Travel time tomography for elliptically anisotropic elastic planar media*, arXiv:2610.13747v1](https://arxiv.org/abs/2610.13747), was inspected in full. Its setting is two-dimensional elliptically anisotropic media, with conditional lens-rigidity assumptions and a different gauge question. Its main theorems do not settle the three-dimensional full-tensor conjecture here.

The closest classical comparison remains Aristégui and Baste, [*Optimal recovery of the elasticity tensor of general anisotropic materials from ultrasonic velocity data*, JASA 101 (1997), 813-833](https://doi.org/10.1121/1.418040). The publisher abstract supports the manuscript's description of constrained numerical recovery. The full article remains unavailable in this audit. Its exact uniqueness and measurement-count claims must not be inferred from its title, and this missing comparison remains a submission-readiness item.

Harder's [*Inversion of phase velocities for the anisotropic elastic tensor*, JGR 90 (1985), 10275-10280](https://doi.org/10.1029/JB090iB12p10275) describes an iterative method using multiple velocities and propagation directions, with crude polarization estimates. It establishes the long history of inversion methods, while using more information than the unordered phase spectra considered here. No first-inversion-method claim is made.

Norris's [*On the acoustic determination of the elastic moduli of anisotropic solids and acoustic conditions for the existence of symmetry planes*, QJMAM 42 (1989), 413-426](https://doi.org/10.1093/qjmam/42.3.413) states in its publisher abstract that all twenty-one moduli can be recovered from full second-order acoustical tensors in six directions satisfying explicit nondegeneracy conditions. Full acoustical matrices contain polarization information beyond their unordered eigenvalues, so this does not contradict the seven-direction obstruction for spectra alone. Only the primary publisher abstract was available; no claim is made to have audited the full article.

Mah and Schmitt's [*Determination of the complete elastic stiffnesses from ultrasonic phase velocity measurements* (2003)](https://doi.org/10.1029/2001JB001586) reports experimental nonlinear inversion of 779 phase velocities to recover all twenty-one constants. This is direct prior experimental recovery from phase velocities and is not dismissed as polarization-assisted inversion. Its discussion of recovery from three measurement planes cites John J. Ditri, [*On the determination of the elastic moduli of anisotropic media from limited acoustical data*, JASA 95 (1994), 1761-1767](https://doi.org/10.1121/1.408695). Ditri's own publisher abstract explicitly includes the corresponding polarization vectors in its acoustic data; Mah and Schmitt likewise note that assumption. Thus that plane-count result is not an unordered-phase-spectrum uniqueness theorem. Ditri's full article was not available, so the manuscript confines its description to the verified abstract.

## Mathematical and software references

- Borel's fixed-point theorem is used for connected solvable algebraic groups acting on complete complex varieties. The cited primary lecture notes by [Balázs Elek, 10 May 2020](https://pi.math.cornell.edu/~bazse/borel_fixed_point_theorem.pdf), state this result. Borel's *Linear Algebraic Groups*, second edition, Springer, 1991, GTM 126, is the monograph reference.
- [Singular's official manual](https://www.singular.uni-kl.de/Manual/latest/sing_1.htm) identifies the software and its authors. The optional corroborating runs use 4.4.1p5. The main dimension upper bounds instead use explicit original-minor identities, checked with standard-library Python rational arithmetic. The remaining matrix checks use SymPy. Software arithmetic is distinguished from formal verification and from peer review.
- The [Stacks Project, Tag 01WC](https://stacks.math.columbia.edu/tag/01WC), establishes that a locally projective morphism is proper; this is the cited basis for the closed-image specialization argument.
- The named conjecture is the source-backed target. A search finding no later resolution would not establish priority. Priority assessment remains provisional while the closest classical full-text comparison is unresolved; no first-discovery claim is made in this package.

## Excluded interpretations

There is no biological experiment, new material fabrication, density recovery, unconditional uniqueness for every symmetry class, error tolerance, or numerical reconstruction algorithm. Phase speed squares are the Christoffel eigenvalues in unit directions. Nonunit direction vectors require the explicitly stated quadratic rescaling.
