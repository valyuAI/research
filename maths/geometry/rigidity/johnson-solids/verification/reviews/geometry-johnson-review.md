# Adversarial review: classification of the 92 Johnson solids under edge-length and coplanarity constraints

Task DR-070 | mode max | completed 2026-10-26T11:37:10.278Z | cost 15.625

# Adversarial review: classification of the 92 Johnson solids under edge-length and coplanarity constraints

## Executive summary

On paper-level checking, no step of the stated method fails. I checked the vertex-only equivalence, the mod-p rank inequality, the Minkowski reorientation lemma with its planarity cases, the prism flexes, the use of the second-order stress test, the Macaulay criterion and the 41/51/45/6 bookkeeping. None of the numerical certificates could be re-executed, and no source I could reach contradicts a verdict.

Specific defects and gaps:

- **Overstated attribution.** AHWZ (arXiv:2607.09252v1) does not "settle" all 31 Platonic, Archimedean and Catalan solids. The truncated dodecahedron remains open [[1]](https://arxiv.org/pdf/2607.09252).
- **Theorem labels.** The labels "Theorem 4.3" and "Theorem 6.2" do not match AHWZ's own numbering (below).
- **Two model formulations.** The model is attributed to both papers, but they use different formulations (below).
- **Cauchy identification.** The Cauchy step gives uniqueness for a given combinatorial type. It does not certify which J-number a dataset realises.
- **J58 and J59.** The resultant/Sturm argument is hand-assembled and is the weakest link.
- **Unestablished claim.** "Prior art: none" is a negative from a limited search and cannot be established.

Prior art the claim omits:

- Zhang's 2024 Cornell thesis, which poses the problem and proves the regular dodecahedron rigid.
- Kochetkov's "strong rigidity" of convex quadrangular pyramids (arXiv:2008.07285).
- The "Exact Johnson Solids" dataset.
- The authors' own DeformationPaths.jl test file, which already fixes the verdict of several solids in AHWZ's tables.

I found no classification of Johnson solids in this model.

## 1. What was and was not checkable

I re-derived the algebraic steps by hand. These derivations are mine, not sourced, and are marked "reviewer derivation" below. I could not rerun any mod-p rank, interval rank, exact flex dimension, Macaulay matrix, or resultant/Sturm computation. AHWZ Tables 1–2 are embedded images, so their cell values cannot be read as text [[1]](https://arxiv.org/pdf/2607.09252)[[2]](https://arxiv.org/html/2607.09252v1). The authors' unit-test file stands in for the boolean columns; the AHWZ supplement itself says the infinitesimal rigidity of the other convex polytopes can be checked via DeformationPaths.jl unit tests [[3]](https://zenodo.org/records/20595067).

## 2. Step-by-step verdicts

| Item | Verdict | Reason |
|---|---|---|
| Vertex-only equivalence (checker 2) | Confirmed | See below. |
| Mod-p rank bound (checker 1) | Confirmed, with conditions | See below. |
| Minkowski reorientation lemma | Confirmed | See below. |
| Prism and augmented-prism flexes | Confirmed in principle | See below. |
| Stress-test usage (complement of trivial motions) | Confirmed; invariance is the authors' step | See below. |
| Macaulay criterion (J81–J83) | Confirmed as a sufficient test | See below. |
| J58/J59 resultant and Sturm argument | Cannot determine | See below. |
| Cauchy identification | Logically valid; labelling gap | See below. |
| 41/51/45/6 bookkeeping | Confirmed | See below. |
| Attributions and numbering | Errors found | See below. |

**Vertex-only equivalence.** AHWZ state that ȧ is determined by ṗ through the incidence equations [[1]](https://arxiv.org/pdf/2607.09252). Writing a fourth vertex as an affine combination of three non-collinear ones, the incidence row becomes ⟨ṗ_d − αṗ_a − βṗ_b − γṗ_c, a_σ⟩ = 0 with α+β+γ = 1. This is the linearisation of det(b−a, c−a, d−a) = 0 (reviewer derivation). The count also closes. Rows are E + Σ(k_f − 3) = 3V − 6, so rank 3V − 6 means full row rank, equivalent to no stress. Proposition 3.6 gives flex dimension equal to stress dimension [[1]](https://arxiv.org/pdf/2607.09252).

**Mod-p rank.** The inequality rank_p ≤ rank_ℝ holds whenever the ring map is well defined. That requires a monic minimal polynomial over Z_(p), a radicand that is a non-square in K, and normal denominators that are units mod p (reviewer derivation). The same inequality is used elsewhere in the literature: the rank of MᵀM mod a prime bounds its rational rank from below [[4]](https://arxiv.org/abs/2609.12640). This yields only an upper bound on flex dimension. That suffices for (A), because full row rank means first-order rigidity by Corollary 3.2 [[1]](https://arxiv.org/pdf/2607.09252).

**Minkowski lemma.** Face closure of the S1-edges gives s1 and s2 with p = s1 + s2. Each edge lies in one class, so lengths are preserved. A face with S1 and S2 direction spans of dimensions (k1, k2) stays planar in these cases (reviewer derivation):

- k1 = 0, k2 = 0, or (1,1): always planar.
- (2,2): both spans equal the face plane, so the axis must be normal to it.
- (2,1): the axis must be normal to the face, or parallel to the S2 line.
- (1,2): the axis must be normal to the face, or parallel to the S1 line.

These cases are complete. Strict convexity is an open condition, so it persists for small t. HSW's text only states the weaker version, in which summands share no edge directions [[5]](https://arxiv.org/html/2505.00874v3). The edge-wise argument is sharper and fine. AHWZ's warning that coincidental coplanarities can prevent Minkowski flexes from existing [[1]](https://arxiv.org/pdf/2607.09252) is exactly what the (2,2) rule handles.

**Prism flexes.** Prisms, and flexible polygons used in Cartesian products, are published constructions [[5]](https://arxiv.org/html/2505.00874v3). Stacking pyramids onto flexing faces is also published, with the "cube with pyramid roof" dissectable into a flexing cube and a rigid pyramid [[5]](https://arxiv.org/html/2505.00874v3). In the augmented prisms, deforming the base through equilateral n-gons keeps every lateral square a unit square and lets the pyramids follow rigidly. A hand count of base deformations plus an optional tilt reproduced the claimed J49 and J52–J57 dimensions (reviewer derivation).

**Stress test.** Theorem 4.2 is stated for every first-order flex [[1]](https://arxiv.org/pdf/2607.09252). AHWZ parametrise the flex space by a basis of the quotient ker R/T_P [[1]](https://arxiv.org/pdf/2607.09252). AHWZ do not state that the form ξᵀR(Ṗ)Ṗ is invariant under adding trivial motions. It is: differentiating f(g·P) = f(P) and using ξᵀf′ = 0 gives ξᵀf″[T,v] = 0 for trivial T (reviewer derivation). The report should state this explicitly as the authors' own step.

**Macaulay criterion.** If every degree-(k+1) monomial lies in the ideal, then every x_i^(k+1) vanishes on the zero set, so the only common complex zero is 0. That suffices, because AHWZ's criterion needs only the absence of real zeros, and their own Gröbner test certifies emptiness over ℂ, which is sufficient but not necessary [[1]](https://arxiv.org/pdf/2607.09252). The J58/J59 count is consistent: 15 monomials of degree 4 in 3 variables, rank 13, so a degree-2 residual scheme.

**J58/J59.** Here a real zero would matter, and the argument excludes it by a coordinate change, resultants, Sturm and manual exclusion of special points. A residual degree-2 scheme could be a conjugate non-real pair, which is harmless, or a real double point, which is not (reviewer derivation). The Sturm step therefore has to rule out the double-point case explicitly. I recommend an independent real-root count over Q(√5). The claim itself says J58, J59 and J81 are only numerically not prestress stable, so no stronger certificate exists.

**Cauchy.** Cauchy's theorem says a convex polytope is determined by the shapes of its faces and is globally rigid in the convex class [[6]](https://arxiv.org/pdf/2505.00874). This identifies the geometry for a given combinatorial type but not the J-number. For example, ortho versus gyro variants share face counts. The "Exact Johnson Solids" dataset (Zenodo 10729583) gives vertex, facet and incidence data for all 92 solids over exact number fields [[7]](https://zenodo.org/records/10729583). It would serve as an independent combinatorial cross-check. McCooey's page notes that Timofeenko supplied analytic coordinates for eight solids, with most values previously known only numerically [[8]](https://dmccooey.com/polyhedra/Johnson.html). The claim's exact validation covers this, but the labels still need matching.

**Bookkeeping.** The (A) list has 41 members, the (B) list has 51, and every J1–J92 appears exactly once. (C) has 45, and (B) minus (C) is exactly {J58, J59, J60, J81, J82, J83}. The flex dimensions of those six equal the number of forms k used in the second-order step. All of this is arithmetic and checked directly.

**Attributions.**

- AHWZ has Corollary 4.3 (first-order rigid ⇒ prestress stable ⇒ second-order rigid), not a Theorem 4.3 [[1]](https://arxiv.org/pdf/2607.09252).
- The criterion the claim calls "Theorem 6.2" is Proposition 6.2 [[1]](https://arxiv.org/pdf/2607.09252). The AHWZ text itself cross-refers to "Theorem 6.1/6.2/4.3/3.6" for these items [[1]](https://arxiv.org/pdf/2607.09252)[[9]](https://arxiv.org/abs/2607.09252).
- The claim's phrase "Theorem 4.2/4.1/3.3 and Prop. 3.6" matches [[1]](https://arxiv.org/pdf/2607.09252).
- AHWZ cover 31 polytopes but leave the truncated dodecahedron undecided: 4-dimensional flex space, not second-order rigid, rigidity unknown [[1]](https://arxiv.org/pdf/2607.09252)[[2]](https://arxiv.org/html/2607.09252v1). The claim's wording "settle" is overstated.
- The claim attributes the ⟨p_i, a_σ⟩ = 1 model to both papers. HSW use ⟨p_j − p_i, a_σ⟩ = 0 with ‖a_σ‖ = 1 [[5]](https://arxiv.org/html/2505.00874v3). AHWZ say the two are birationally equivalent near convex realisations with the origin interior and that the distinction "can be ignored" [[1]](https://arxiv.org/pdf/2607.09252). A rank-preservation statement for the first-order matrices is not made. It follows from a local change of variables, but should be stated.

**The J83 sentence.** "J83 is being checked" sits in the sentence about prestress certificates. Read that way it does not conflict with (D), which lists J83 as second-order rigid by the Macaulay certificate. The claim should state which is meant.

**Flex families versus dimensions.** The (B) dimensions are first-order counts. AHWZ note that the flex-space dimension equals the tangent-space dimension only at regular points, and that non-regular points are more complicated [[1]](https://arxiv.org/pdf/2607.09252). A reader must not take J55 (dimension 4) or J67 (dimension 2) as single multi-parameter families. They can be unions of branches, selected by conditions such as parallelism of edges (reviewer derivation).

## 3. Consistency with published statements

No verdict I could test contradicts a published statement.

AHWZ's text:

- The dodecahedron and truncated icosahedron each have a 5-dimensional first-order flex space, are not prestress stable, and are second-order rigid [[1]](https://arxiv.org/pdf/2607.09252).
- The cuboctahedron, rhombicuboctahedron and rhombicosidodecahedron are generic Minkowski sums, with reorientation flexes contributing 3 dimensions and summand flexes adding more [[1]](https://arxiv.org/pdf/2607.09252).
- For all three, the first-order dimension equals that lower bound. So the cuboctahedron has dimension 3, contrary to the doubt in the earlier notes [[1]](https://arxiv.org/pdf/2607.09252).

The authors' test file (master, retrieved 2026-10-26) [[10]](https://raw.githubusercontent.com/matthiashimmelmann/DeformationPaths.jl/master/test/Polytope.jl):

| Polytope | Asserted |
|---|---|
| Icosidodecahedron | first-order rigid; rigid |
| Cuboctahedron | not first-order rigid; not rigid |
| Small rhombicosidodecahedron | not first-order rigid; not second-order rigid; not rigid |
| Rhombicuboctahedron | not first-order rigid; not rigid |
| Truncated tetrahedron, truncated cube, icosahedron, snub cube, snub dodecahedron | first-order rigid; rigid |
| Truncated icosahedron | 5 flexes, 5 stresses; not first-order rigid; not prestress stable; second-order rigid; rigid |
| Truncated dodecahedron | 4 flexes, 4 stresses; not prestress stable; not first-order rigid; not second-order rigid; **and** `!is_rigid` |

The snub dodecahedron entry is present in the file. The truncated dodecahedron row shows a caveat: the file asserts `!is_rigid`, while the paper says rigidity is unknown [[1]](https://arxiv.org/pdf/2607.09252). So a `!is_rigid` assertion is not by itself a flexibility proof. The file is master, which may postdate the 1.1.0 release of 2026-04-27 [[11]](https://zenodo.org/records/19830468).

Other checks:

- **J8.** HSW v3's Figure 6 "cube with pyramid roof" is flexible and dissectable [[5]](https://arxiv.org/html/2505.00874v3). In the polyhedra-world list, J8 has 4 triangles and 5 squares [[12]](http://www.polyhedra-world.nc/Johnson_.htm), which matches a cube with a square pyramid, so this is consistent with J8 flexible.
- **J1.** Kochetkov proves a convex quadrangular pyramid is strongly rigid (edge lengths fixed, face shapes free) [[13]](https://arxiv.org/abs/2008.07285). Winter's Figure 16 caption (arXiv:2302.14194) says the pyramid is "(locally) rigid as a polytope" [[14]](https://arxiv.org/abs/2302.14194). Neither is first-order rigidity, but both agree with J1 rigid.
- **Prisms.** They flex [[5]](https://arxiv.org/html/2505.00874v3), consistent with the augmented prisms.
- **Deltahedra.** J12 has 6 triangles and J13 has 10 triangles [[12]](http://www.polyhedra-world.nc/Johnson_.htm). Simplicial polytopes are first-order rigid by Dehn [[1]](https://arxiv.org/pdf/2607.09252), so both are consistent with their (A) placement. J17, J51 and J84 are not shown as all-triangle in the supplied material.
- **Minkowski sums in (A).** I could not run an exhaustive edge-partition search over the 41 (A) solids. A triangle face forces all its edges into one class (reviewer derivation), so strongly triangle-connected chains touching every face force trivial partitions. This matches the Shephard/McMullen indecomposability criterion [[15]](https://arxiv.org/abs/2608.02445)[[16]](https://arxiv.org/abs/1607.00643). It is only a necessary-condition check, not a rigidity proof.
- **Deza–Pournin test.** A polytope P has a summand homothetic to Q iff P and P + Q have the same number of vertices [[17]](https://arxiv.org/abs/1806.07643). That gives a mechanical way to verify claimed decompositions such as J3 = triangle + tetrahedron.
- **Truncated dodecahedron base.** AHWZ's truncated dodecahedron has a 4-dimensional flex space and open rigidity [[1]](https://arxiv.org/pdf/2607.09252). The claimed first-order rigidity of J68–J71, built on it, therefore rests on the rank computation alone.

## 4. Prior art

- **Zhang thesis, Cornell, May 2024.** It states the problem of a polyhedron with fixed edge lengths and facets staying planar [[18]](https://ecommons.cornell.edu/entities/publication/DR-026). It credits Winter with raising it and proves the regular dodecahedron rigid [[19]](https://ecommons.cornell.edu/bitstreams/DR-032/download). I could not read the body for Johnson-solid content. HSW v3 credits the dodecahedron resolution to "Albert Zhang" [[5]](https://arxiv.org/html/2505.00874v3), while AHWZ list Zhen Zhang [[1]](https://arxiv.org/pdf/2607.09252); identity is presumed, not established.
- **HSW arXiv:2505.00874v3** (submitted 9 March 2026; IMRN 2026(7), rnag055, 30 April 2026) [[20]](https://arxiv.org/abs/2505.00874)[[21]](https://research.lancaster-university.uk/en/publications/rigidity-of-polytopes-with-edge-length-and-coplanarity-constraint/). Its §4.1, §4.4, Figure 6 and Question 4.4 (parallel edges) are present in the v3 text [[5]](https://arxiv.org/html/2505.00874v3).
- **Kochetkov, arXiv:2008.07285.** It defines strong flexibility and strong rigidity. A cube is strongly flexible, and a generic polyhedron is strongly rigid [[13]](https://arxiv.org/abs/2008.07285).
- **Winter, arXiv:2302.14194.** It states Question 5.9: a polytope not determined by combinatorial type and edge lengths must be a polygon, a non-trivial Minkowski sum, or have edge directions on a conic at infinity [[14]](https://arxiv.org/abs/2302.14194). J49 and J52–J57 are not Minkowski sums but are dissectable stackings, a published mechanism [[5]](https://arxiv.org/html/2505.00874v3). Nothing in the claim is a counterexample to HSW Question 4.2 on non-dissectable flexes [[5]](https://arxiv.org/html/2505.00874v3).
- **Cupola decompositions.** Wikipedia says only that J3 is half a cuboctahedron [[22]](https://en.wikipedia.org/wiki/Triangular_cupola). I found no Minkowski-decomposition statement for any Johnson solid.
- **No classification found** in arXiv listings since 2026-09-01, the AHWZ citations, or software. This is a limited negative search.

## 5. Significance (judgement)

Much of the table is a routine application of published tools: Dehn, Minkowski reorientation, stacking, and exact linear algebra. The first-order dimensions follow constructions already counted in AHWZ's appendix [[1]](https://arxiv.org/pdf/2607.09252).

The potentially new content:

- **Complete 92-solid table in this model.**
- **Six second-order cases, J58–J60 and J81–J83, if certified.** AHWZ called previous prestress-versus-second-order separating examples "comparatively ad hoc" and presented the dodecahedron and truncated icosahedron as natural examples [[1]](https://arxiv.org/pdf/2607.09252). J60 and J82 would be prestress stable, so they would not separate the two notions. J58, J59 and J81 would, but only numerically on the prestress side.
- **The J80-versus-J81 contrast.** J80 flexes through a common axis, while J81's non-parallel decagon normals leave no admissible axis. This rests on the unverified axis computation.
- **Question 8.1 (extending Dehn).** AHWZ ask about triangle-and-4-gon polytopes [[1]](https://arxiv.org/pdf/2607.09252). The list shows no simple face-type criterion. J10 (12 triangles, 1 square) is in (A), while J8 and J7 are in (B) [[12]](http://www.polyhedra-world.nc/Johnson_.htm). The cuboctahedron is a flexible triangle-and-square polytope [[1]](https://arxiv.org/pdf/2607.09252).

A specialist would likely read this as a careful computational case study extending AHWZ, publishable if the certificates and code are released.

## 6. Synthesis

The logic of the classification is sound. First-order rigidity follows from full row rank, Minkowski flexes follow from the planarity cases, and the second-order cases follow from AHWZ's stress test. Seven things should be corrected or strengthened before relying on it:

1. Fix the AHWZ numbering and drop "settle".
2. State the two model formulations and their equivalence.
3. State the invariance of the quadratic form modulo trivial motions.
4. Match every dataset to its J-number, for example against [[7]](https://zenodo.org/records/10729583).
5. Replace the J58/J59 hand elimination with an independent real-root count.
6. Clarify the J83 sentence.
7. Mention Zhang's thesis, Kochetkov and the test file as prior art or cross-checks.

The headline "47 rigid, 45 flexible" is rigid or flexible in the local sense at the unit-edge realisation. Global rigidity is not addressed; even for the dodecahedron it is posed as an open question [[1]](https://arxiv.org/pdf/2607.09252).

## Sources

[1] Deformations and second-order rigidity of polytopes - https://arxiv.org/pdf/2607.09252
[2] Deformations and second-order rigidity of polytopes - https://arxiv.org/html/2607.09252v1
[3] Supplementary Material: "Deformations and second-order rigidity of polytopes" | Zenodo - https://zenodo.org/records/20595067
[4] Non-convex polytopes realizing kissing contact graphs in dimensions 5-7 - https://arxiv.org/abs/2609.12640
[5] Rigidity of polytopes with edge length and coplanarity constraints - https://arxiv.org/html/2505.00874v3
[6] Rigidity of polytopes with edge length and coplanarity constraints - https://arxiv.org/pdf/2505.00874
[7] Exact Johnson Solids | Zenodo - https://zenodo.org/records/10729583
[8] Johnson Solids - https://dmccooey.com/polyhedra/Johnson.html
[9] Deformations and second-order rigidity of polytopes - https://arxiv.org/abs/2607.09252
[10] https://raw.githubusercontent.com/matthiashimmelmann/DeformationPaths.jl/master/test/Polytope.jl - https://raw.githubusercontent.com/matthiashimmelmann/DeformationPaths.jl/master/test/Polytope.jl
[11] matthiashimmelmann/DeformationPaths.jl: Release 1.1.0 | Zenodo - https://zenodo.org/records/19830468
[12] Johnson's polyhedra - http://www.polyhedra-world.nc/Johnson_.htm
[13] The geometry of quadrangular convex pyramids - https://arxiv.org/abs/2008.07285
[14] Rigidity, Tensegrity and Reconstruction of Polytopes under Metric Constraints - https://arxiv.org/abs/2302.14194
[15] Minkowski decomposability of symmetric edge polytopes - https://arxiv.org/abs/2608.02445
[16] More indecomposable polyhedra - https://arxiv.org/abs/1607.00643
[17] Diameter, Decomposability, and Minkowski Sums of Polytopes - https://arxiv.org/abs/1806.07643
[18] Rigidity Theory of Circles, Polygons, and Polyhedra - https://ecommons.cornell.edu/entities/publication/DR-026
[19] RIGIDITY THEORY OF CIRCLES, POLYGONS, AND POLYHEDRA A Dissertation - https://ecommons.cornell.edu/bitstreams/DR-032/download
[20] Rigidity of polytopes with edge length and coplanarity constraints - https://arxiv.org/abs/2505.00874
[21] Rigidity of Polytopes with Edge Length and Coplanarity Constraints - Lancaster University research directory - https://research.lancaster-university.uk/en/publications/rigidity-of-polytopes-with-edge-length-and-coplanarity-constraint/
[22] Triangular cupola - Wikipedia - https://en.wikipedia.org/wiki/Triangular_cupola
