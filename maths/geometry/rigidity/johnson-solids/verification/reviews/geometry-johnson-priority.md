# Priority and prior-art audit: rigidity of Johnson solids in the edge-length + coplanarity (point-hyperplane) model

Task DR-022 | mode heavy | completed 2026-10-26T00:00:42.975Z | cost 3.125

# Priority and prior-art audit: rigidity of Johnson solids in the edge-length + coplanarity (point-hyperplane) model

## Executive summary

**No prior work on Johnson solids in this model was found.** No source reached treats any Johnson solid, cupola, rotunda or augmented/diminished solid under fixed edge lengths and planar but deformable faces. No source lists a Johnson solid as first-order rigid, first-order flexible, prestress stable or second-order rigid. No source records the augmented dodecahedra as first-order flexible. The only polytope families classified in this model are the five Platonic, 13 Archimedean and 13 Catalan solids [[1]](https://arxiv.org/abs/2607.09252)[[2]](https://arxiv.org/html/2607.09252v1). This is an absence-of-evidence finding limited to what could be retrieved. The main unresolved risks are listed in the last section.

Four points qualify the priority claim:

1. **The Johnson classification is not in arXiv:2607.09252 (v1).** That paper restricts its computations to the Platonic, Archimedean and Catalan solids. It says only the truncated dodecahedron cannot be decided [[1]](https://arxiv.org/abs/2607.09252)[[2]](https://arxiv.org/html/2607.09252v1). The paper that claims the 92-solid classification could not be retrieved, so it cannot be audited here.
2. **The Minkowski reorientation mechanism is published prior art.** It appears in arXiv:2505.00874 §4.1 [[3]](https://arxiv.org/html/2505.00874)[[4]](https://arxiv.org/html/2505.00874v3) and in 2607.09252 Appendix A.1 [[2]](https://arxiv.org/html/2607.09252v1). Only its application to specific Johnson solids would be new.
3. **The two Zenodo deposits do not describe Johnson-solid content.** Their contents were not inspected, so this is not settled (see Question 1).
4. **No source records the specific Minkowski decompositions asserted** (triangular cupola = triangle + tetrahedron; J72–J83 = augmented-dodecahedron-type + diminished-icosahedron-type summands) in the decomposability literature reached. They are also not found in Zefiro's dissection page or the Wikipedia-derived pages on the rhombicosidodecahedron.

## Exact citations of the anchor papers

- **IMRN version.** M. Himmelmann, B. Schulze, M. Winter, "Rigidity of Polytopes with Edge Length and Coplanarity Constraints", *International Mathematics Research Notices* 2026(7), article rnag055, DOI 10.1093/imrn/rnag055. It was published 30 April 2026, with early online access on 8 April 2026 [[5]](https://research.lancaster-university.uk/en/publications/rigidity-of-polytopes-with-edge-length-and-coplanarity-constraint/). The journal record lists the first author as "Matthias Himmelmann", not "Adrian-Himmelmann".
- **arXiv:2505.00874.** v1 was published 1 May 2025 [[6]](https://arxiv.org/abs/2505.00874). v2 is dated 23 November 2025 [[7]](https://arxiv.org/html/2505.00874v2) and v3 is dated 9 March 2026 [[4]](https://arxiv.org/html/2505.00874v3). The HTML renderings of v2 and v3 both carry a "Date: August 24, 2026" line. That does not establish a separate later version.
- **arXiv:2607.09252.** M. Adrian-Himmelmann, M. Winter, Z. Zhang, "Deformations and second-order rigidity of polytopes" [[1]](https://arxiv.org/abs/2607.09252). It was submitted 10 July 2026 and shows v1 only, with MSC 51M20, 52C25, 52B11, 14Q30, 65H14 [[1]](https://arxiv.org/abs/2607.09252). The Zenodo record for its supplementary material calls the manuscript "Second-order rigidity and deformations of polytopes with edge length and coplanarity constraints" [[8]](https://doi.org/10.5281/zenodo.20595067).

## Question 1: prior studies of Johnson solids, cupolae, rotundae, augmented or diminished solids

### The model papers

The 2025 paper states its setting: "we ask which convex polytopes P ⊂ R^d permit continuous deformations that preserve the combinatorial type, edge lengths and the planarity of faces; but not necessarily the shapes of the faces" [[3]](https://arxiv.org/html/2505.00874). It collects flexible constructions (Minkowski sums, zonotopes, affine flexes, stacking) [[3]](https://arxiv.org/html/2505.00874). The examples it shows are the cube, a zonotope, the cuboctahedron, a five-edge-direction polytope and a "cube with pyramid roof" [[3]](https://arxiv.org/html/2505.00874)[[4]](https://arxiv.org/html/2505.00874v3). The dodecahedron is the one non-trivial Platonic case [[3]](https://arxiv.org/html/2505.00874). The excerpts retrieved do not contain Johnson solids, cupolae or rotundae.

The 2026 paper states: "we analyze the rigidity properties of the Platonic, Archimedean and Catalan solids (see Table 1 and Table 2)… Solely the rigidity of the truncated dodecahedron… cannot be determined by our techniques" [[1]](https://arxiv.org/abs/2607.09252). Its Section 8 is titled "Computational results: Platonic, Archimedean and Catalan solids" [[1]](https://arxiv.org/abs/2607.09252)[[2]](https://arxiv.org/html/2607.09252v1). Its conclusion says "Among the 31 polytopes we considered, the truncated dodecahedron is the only one whose rigidity we are unable to determine" [[2]](https://arxiv.org/html/2607.09252v1), and 5 + 13 + 13 = 31. Its stated reason for choosing these classes is that "combinatorial data and exact vertex and normal coordinates are readily available" [[1]](https://arxiv.org/abs/2607.09252).

### Theses, software and Q&A

- **Himmelmann's thesis**, "Approximating Continuous Motions of Geometric Constraint Systems" (arXiv:2602.08016): its polytope section follows the 2025 paper and says "Even the rigidity properties of the Platonic solids under these constraints are not completely understood" [[9]](https://arxiv.org/html/2602.08016). The excerpts retrieved show no Johnson solids.
- **DeformationPaths.jl on GitHub**: the "Polytopes with Coplanarity Constraints" section gives one worked example, the cuboctahedron [[10]](https://github.com/matthiashimmelmann/DeformationPaths.jl).
- **MathOverflow**: the relevant thread is "Is the dodecahedron flexible (as a polytope with fixed edge-lengths)?", asked 17 Nov 2022 by M. Winter [[11]](https://mathoverflow.net/questions/434771/is-the-dodecahedron-flexible-as-a-polytope-with-fixed-edge-lengths). It concerns the regular dodecahedron only, and the 2025 paper cites it [[3]](https://arxiv.org/html/2505.00874). A separate thread, "The 'Johnson polychora'" (2018), concerns 4-dimensional regular-faced polytopes and has no rigidity content [[12]](https://mathoverflow.net/questions/296444/the-johnson-polychora). A thread on which (semi)regular polyhedra are combinations of two others [[13]](https://mathoverflow.net/questions/36994/which-semiregular-polyhedra-are-combinations-of-two-others) was reached only in its opening text, so its answers are not reviewed.
- **Other rigidity preprints** reached were off-topic for Johnson solids. The coned-polytope paper (arXiv:2607.14878) treats coned 1-skeleta [[14]](https://arxiv.org/abs/2607.14878)[[15]](https://arxiv.org/html/2607.14878). The intrinsic-rigidity paper by Adrian-Himmelmann (arXiv:2610.17004, 12 Oct 2026) treats bar-and-joint frameworks on Riemannian manifolds [[16]](https://arxiv.org/html/2610.17004v1).

### The two Zenodo deposits

- **10.5281/zenodo.20595067** is "Supplementary Material: 'Deformations and second-order rigidity of polytopes'", published 8 June 2026 (v1) [[8]](https://doi.org/10.5281/zenodo.20595067). Its description reads: "We provide animations of the flexible Archimedean and Platonic solids… a candidate for a continuous motion of the truncated dodecahedron and a symmetric motion of the cuboctahedron." The code covers the dodecahedron, truncated icosahedron and truncated dodecahedron. It adds: "The infinitesimal rigidity of the other convex polytopes can be checked via the unit tests in DeformationPaths.jl" [[8]](https://doi.org/10.5281/zenodo.20595067).
- **10.5281/zenodo.19830468** is DeformationPaths.jl Release 1.1.0, published 27 April 2026. Its changelog lists a README update, a `prestress_stability` fix, a dependency bump, a DOI link update and a `pin_GCS` keyword [[17]](https://doi.org/10.5281/zenodo.19830468).

Neither description mentions Johnson solids, cupolae, rotundae or augmented/diminished solids. The zip contents (20.3 MB and 11.4 MB) were not inspected [[8]](https://doi.org/10.5281/zenodo.20595067)[[17]](https://doi.org/10.5281/zenodo.19830468). Whether either archive, including the DeformationPaths.jl unit tests, contains Johnson-solid data is **unestablished**.

## Question 2: any listing of Johnson solids as first-order flexible, prestress stable or second-order rigid; any note on augmented dodecahedra

None was found. The augmented dodecahedron J58 is described in geometry sources as a dodecahedron with a pentagonal pyramid on one face: 21 vertices, 35 edges, 16 faces [[18]](https://www.qfbox.info/4d/J58)[[19]](https://mathworld.wolfram.com/AugmentedDodecahedron.html)[[20]](https://dmccooey.com/polyhedra/java/AugmentedDodecahedron.html). J68 is a truncated dodecahedron with a pentagonal cupola attached to a decagon [[21]](https://handwiki.org/wiki/Augmented_truncated_dodecahedron). These sources are purely descriptive and say nothing about rigidity.

Context that bears on plausibility, though no source states the claimed Johnson results:

- The regular dodecahedron has a 5-dimensional first-order flex space and is not prestress stable. It is nonetheless second-order rigid, hence rigid [[1]](https://arxiv.org/abs/2607.09252).
- The truncated dodecahedron has a 4-dimensional first-order flex space, is not prestress stable and not second-order rigid, and its rigidity is open [[1]](https://arxiv.org/abs/2607.09252).
- The 2026 paper observes that first-order flexibility of these three polytopes is sensitive to geometry: changing the truncation height gives first-order rigid polytopes [[1]](https://arxiv.org/abs/2607.09252).

Because J58–J60 are built on a first-order-flexible dodecahedron, the claimed first-order flexibility of the augmented dodecahedra is not surprising. But no source records it, and nothing in the literature reached supports or contradicts the specific dimensions (3, 3, 1, 4, 2, 2) or the prestress-stability pattern.

## Question 3: Minkowski decompositions in the decomposability literature

### What the literature records

- **Criteria for indecomposability.** Shephard gave criteria via strong chains of indecomposable faces. McMullen weakened them to strongly connected families of indecomposable faces touching all facets. Padrol and Poullot introduced the graph of implicit edge dependencies [[22]](https://arxiv.org/abs/2608.02445).
- **Classical references.** Shephard, *Mathematika* 10 (1963) 89–95; Smilansky, PhD thesis (Hebrew University, 1986) and *Geom. Dedicata* 24 (1987) 29–49; Kallay, PhD thesis (1979) and *Israel J. Math.* 41 (1982) 235–243; McMullen, *Israel J. Math.* 58 (1987) 321–323; Przesławski–Yost, *Discrete Comput. Geom.* 39 (2008) 460–468, and *Extracta Math.* 31(2) (2016) 169–188 [[23]](https://revista-em.unex.es/index.php/EM/article/view/2605-5686.31.2.169)[[24]](https://dl.acm.org/doi/10.1007/s00454-001-0024-0)[[25]](https://www.cambridge.org/core/journals/mathematika/article/abs/an-indecomposable-polytope-all-of-whose-facets-are-decomposable/587365B6202FFC85B460474AD71D11FF).
- **Przesławski–Yost 2016** complete "the classification, in terms of decomposability, of the 260 combinatorial types of polyhedra with 15 or fewer edges" [[23]](https://revista-em.unex.es/index.php/EM/article/view/2605-5686.31.2.169).
- **Smilansky:** conditionally decomposable 3-polytopes with V vertices and F facets exist only if V ≤ F ≤ 2V − 8, and his examples have a line segment as a summand [[26]](https://doi.org/10.1515/advgeom-2026-0006).
- **Wang–Yost**, arXiv:2102.10868: the first conditionally decomposable d-polytopes for d ≥ 4. Its 3-dimensional examples are Federico's #282, #288 and the gyrobifastigium #287 [[27]](https://arxiv.org/pdf/2102.10868)[[28]](https://arxiv.org/abs/2102.10868).
- **Deza–Pournin**, *Canad. Math. Bull.* 62(4) (2018): P has a summand homothetic to Q iff P and P + Q have the same number of vertices [[29]](https://arxiv.org/pdf/1806.07643)[[30]](https://www.cambridge.org/core/journals/canadian-mathematical-bulletin/article/diameter-decomposability-and-minkowski-sums-of-polytopes/2FAF87EA12CE35ABC5294CDAC9CB7999).
- **Recent papers.** Minkowski decomposability of symmetric edge polytopes (arXiv:2608.02445, Aug 2026) [[22]](https://arxiv.org/abs/2608.02445) and indecomposability of 0/1-polytopes (arXiv:2605.22594, May 2026) [[31]](https://arxiv.org/abs/2605.22594) concern other polytope classes.

None of these sources, in the passages reached, discusses a triangular cupola, a rotunda, or any of J72–J83.

### The nearest relevant records

- **Cuboctahedron.** The 2025 paper says "The cuboctahedron is the Minkowski sum of two simplices" [[3]](https://arxiv.org/html/2505.00874). MathWorld lists regular tetrahedron + regular tetrahedron = cuboctahedron [[32]](https://mathworld.wolfram.com/MinkowskiSum.html). Wang–Yost record that for a tetrahedron T, the difference set T − T is a cuboctahedron, and that the cuboctahedron is the first known conditionally decomposable polytope (from Meyer's thesis) [[27]](https://arxiv.org/pdf/2102.10868).
- **Triangular cupola (J3).** It is described as "half a cuboctahedron", with 4 triangles, 3 squares, 1 hexagon, 15 edges and 9 vertices [[33]](https://en.wikipedia.org/wiki/Triangular_cupola)[[34]](https://polytope.miraheze.org/wiki/Triangular_cupola). No source states that J3 is a triangle plus a tetrahedron. That the cuboctahedron is a tetrahedron sum and J3 is half of it is suggestive only.
- **Rhombicosidodecahedron (Archimedean).** It is recorded as the Minkowski sum of a regular dodecahedron and its dual icosahedron [[35]](https://grokipedia.com/page/Rhombicosidodecahedron)[[32]](https://mathworld.wolfram.com/MinkowskiSum.html)[[2]](https://arxiv.org/html/2607.09252v1). The 2026 paper adds that both summands are first-order rigid or inheritable, and that the dodecahedron's 5-dimensional flex space "gets inherited by the Minkowski sum" [[2]](https://arxiv.org/html/2607.09252v1). This concerns the Archimedean solid, not the gyrate or diminished Johnson solids.
- **J72–J83.** Zefiro's page dissects the rhombicosidodecahedron into a tridiminished rhombicosidodecahedron and three pentagonal cupolae. Rotating one, two or three cupolas by 180° (or an odd multiple of 36°) yields J72–J75, and removal plus rotation yields the rest [[36]](http://www.mi.sanu.ac.rs/vismath/zefiro2009sept/___RID_dissection.htm). This is dissection and reassembly, not a Minkowski sum, and the page does not use the word "Minkowski". Wikipedia-derived text likewise describes diminution and rotation [[37]](https://www.wikiwand.com/en/Rhombicosidodecahedron).

The specific decompositions are therefore **not recorded** in the sources reached. This does not show they are false or non-novel in the broader literature.

## Question 4: later citations of arXiv:2607.09252 and arXiv:2505.00874

No citing paper treating Johnson solids was found.

- **For 2607.09252**, the only derivative items found are a Pith AI review dated 13 July 2026, which calls the paper a "classif[ication of] the classical solids" with one open case [[38]](https://pith.science/paper/2607.09252), and a ResearchGate listing [[39]](https://www.researchgate.net/publication/376785099_Rigidity_Tensegrity_and_Reconstruction_of_Polytopes_Under_Metric_Constraints). Neither treats Johnson solids.
- **For 2505.00874**, the items found are a ResearchGate citation stub [[40]](https://www.researchgate.net/figure/Morphologically-spherical-but-geometrically-polyhedral-formations-A-The-virion-like_fig1_343860128) and the IMRN record [[5]](https://research.lancaster-university.uk/en/publications/rigidity-of-polytopes-with-edge-length-and-coplanarity-constraint/). Himmelmann's thesis cites it [[9]](https://arxiv.org/html/2602.08016).
- **Related, with the same authors:** arXiv:2607.14878 (Pachyli, Prosanov, Winter, 16 July 2026) cites "the rigidity of exceptional polytopal point-hyperplane frameworks [[6]](https://arxiv.org/abs/2505.00874)" but treats coned polytope frameworks only [[14]](https://arxiv.org/abs/2607.14878)[[15]](https://arxiv.org/html/2607.14878).
- No Semantic Scholar or Google Scholar "cited by" listing was obtained, so the check is not exhaustive. The paper was only about 3.5 months old on 25 October 2026.

## Summary of checks

| Question | Finding | Basis |
|---|---|---|
| 1. Prior Johnson/cupola/rotunda rigidity study in this model | None found; only Platonic, Archimedean, Catalan | [[1]](https://arxiv.org/abs/2607.09252)[[2]](https://arxiv.org/html/2607.09252v1)[[3]](https://arxiv.org/html/2505.00874)[[9]](https://arxiv.org/html/2602.08016)[[10]](https://github.com/matthiashimmelmann/DeformationPaths.jl) |
| 1. Zenodo deposits | Descriptions mention no Johnson solids; zip contents not inspected | [[8]](https://doi.org/10.5281/zenodo.20595067)[[17]](https://doi.org/10.5281/zenodo.19830468) |
| 2. Johnson solids listed as FO-flexible / prestress stable / SO-rigid; J58 noted not FO-rigid | None found | [[1]](https://arxiv.org/abs/2607.09252)[[18]](https://www.qfbox.info/4d/J58)[[21]](https://handwiki.org/wiki/Augmented_truncated_dodecahedron) |
| 3. Decompositions recorded in decomposability literature | Not found; related facts only (cuboctahedron, Archimedean rhombicosidodecahedron, Zefiro dissection) | [[23]](https://revista-em.unex.es/index.php/EM/article/view/2605-5686.31.2.169)[[26]](https://doi.org/10.1515/advgeom-2026-0006)[[27]](https://arxiv.org/pdf/2102.10868)[[32]](https://mathworld.wolfram.com/MinkowskiSum.html)[[36]](http://www.mi.sanu.ac.rs/vismath/zefiro2009sept/___RID_dissection.htm) |
| 4. Later citing papers treating Johnson solids | None found; no citation-graph query possible | [[38]](https://pith.science/paper/2607.09252)[[39]](https://www.researchgate.net/publication/376785099_Rigidity_Tensegrity_and_Reconstruction_of_Polytopes_Under_Metric_Constraints)[[15]](https://arxiv.org/html/2607.14878) |

## What could undermine priority

1. **The classification paper itself was not retrieved.** The notes' premise that 2607.09252 contains it is wrong. Anything in its supplement that goes beyond the anchor paper cannot be audited here.
2. **The Zenodo archives are uninspected.** The 2026 supplement says other polytopes' infinitesimal rigidity "can be checked via the unit tests in DeformationPaths.jl" [[8]](https://doi.org/10.5281/zenodo.20595067). That could include Johnson-solid data.
3. **The flex mechanism is not novel.** Reorientation flexes of Minkowski sums, and the cuboctahedron as a sum of two simplices, are in the 2025 paper [[3]](https://arxiv.org/html/2505.00874)[[4]](https://arxiv.org/html/2505.00874v3). The 2026 paper also decomposes flex spaces into summand flexes and reorientation flexes [[2]](https://arxiv.org/html/2607.09252v1). Claims of novelty should rest on the Johnson-specific classification and the six "first-order flexible but rigid" solids, not on the technique.
4. **A recent preprint may have been missed.** Searches were targeted, and absence from the listings reached does not prove absence.

## Synthesis

Within the evidence available up to 25 October 2026, the claimed classification of the 92 Johnson solids has no identified prior art, and the six first-order-flexible-but-rigid solids are not anticipated. Priority is supported but not certified. The Minkowski reorientation flexes must be credited to Himmelmann–Schulze–Winter [[3]](https://arxiv.org/html/2505.00874) and Adrian-Himmelmann–Winter–Zhang [[2]](https://arxiv.org/html/2607.09252v1). Before asserting priority publicly, the author should do three things:

- inspect the two Zenodo archives, especially the DeformationPaths.jl tests;
- run a citation-graph query for both anchor papers;
- cite the classical decomposability literature and Zefiro's dissection page as the closest precedents for the Minkowski and gyration structure.

## Sources

[1] Deformations and second-order rigidity of polytopes - https://arxiv.org/abs/2607.09252
[2] Deformations and second-order rigidity of polytopes - https://arxiv.org/html/2607.09252v1
[3] Rigidity of polytopes with edge length and coplanarity constraints - https://arxiv.org/html/2505.00874
[4] Rigidity of polytopes with edge length and coplanarity constraints - https://arxiv.org/html/2505.00874v3
[5] Rigidity of Polytopes with Edge Length and Coplanarity Constraints - Lancaster University research directory - https://research.lancaster-university.uk/en/publications/rigidity-of-polytopes-with-edge-length-and-coplanarity-constraint/
[6] Rigidity of polytopes with edge length and coplanarity constraints - https://arxiv.org/abs/2505.00874
[7] Rigidity of polytopes with edge length and coplanarity constraints - https://arxiv.org/html/2505.00874v2
[8] Supplementary Material: "Deformations and second-order rigidity of polytopes" | Zenodo - https://doi.org/10.5281/zenodo.20595067
[9] 2602.08016 - https://arxiv.org/html/2602.08016
[10] GitHub - matthiashimmelmann/DeformationPaths.jl: Julia package for approximating continuous motions of geometric constraint systems · GitHub - https://github.com/matthiashimmelmann/DeformationPaths.jl
[11] mg.metric geometry - Is the dodecahedron flexible (as a polytope with fixed edge-lengths)? - MathOverflow - https://mathoverflow.net/questions/434771/is-the-dodecahedron-flexible-as-a-polytope-with-fixed-edge-lengths
[12] discrete geometry - The "Johnson polychora" - MathOverflow - https://mathoverflow.net/questions/296444/the-johnson-polychora
[13] reference request - Which (semi)regular polyhedra are combinations of two others? - MathOverflow - https://mathoverflow.net/questions/36994/which-semiregular-polyhedra-are-combinations-of-two-others
[14] Second-order rigidity of coned polytope frameworks and the stress-flex conjecture from a vector-valued Schläfli formula - https://arxiv.org/abs/2607.14878
[15] Second-order rigidity of coned polytope frameworks and the stress-flex conjecture from a vector-valued Schläfli formula - https://arxiv.org/html/2607.14878
[16] Intrinsic Rigidity of Bar-and-Joint Frameworks on Riemannian Manifolds - https://arxiv.org/html/2610.17004v1
[17] matthiashimmelmann/DeformationPaths.jl: Release 1.1.0 | Zenodo - https://doi.org/10.5281/zenodo.19830468
[18] The Augmented Dodecahedron - https://www.qfbox.info/4d/J58
[19] Augmented Dodecahedron -- from Wolfram MathWorld - https://mathworld.wolfram.com/AugmentedDodecahedron.html
[20] Augmented Dodecahedron - https://dmccooey.com/polyhedra/java/AugmentedDodecahedron.html
[21] Augmented truncated dodecahedron - HandWiki - https://handwiki.org/wiki/Augmented_truncated_dodecahedron
[22] Minkowski decomposability of symmetric edge polytopes - https://arxiv.org/abs/2608.02445
[23] More Indecomposable Polyhedra | Extracta Mathematicae - https://revista-em.unex.es/index.php/EM/article/view/2605-5686.31.2.169
[24] Decomposition of Polytopes and Polynomials - https://dl.acm.org/doi/10.1007/s00454-001-0024-0
[25] An indecomposable polytope all of whose facets are decomposable | Mathematika | Cambridge Core - https://www.cambridge.org/core/journals/mathematika/article/abs/an-indecomposable-polytope-all-of-whose-facets-are-decomposable/587365B6202FFC85B460474AD71D11FF
[26] Lower bound results for conditionally decomposable polytopes - https://doi.org/10.1515/advgeom-2026-0006
[27] Conditionally decomposable polytopes - https://arxiv.org/pdf/2102.10868
[28] Conditionally decomposable polytopes - https://arxiv.org/abs/2102.10868
[29] Diameter, Decomposability, and Minkowski Sums of Polytopes - https://arxiv.org/pdf/1806.07643
[30] Diameter, Decomposability, and Minkowski Sums of Polytopes | Canadian Mathematical Bulletin | Cambridge Core - https://www.cambridge.org/core/journals/canadian-mathematical-bulletin/article/diameter-decomposability-and-minkowski-sums-of-polytopes/2FAF87EA12CE35ABC5294CDAC9CB7999
[31] Indecomposability of 0/1-polytopes - https://arxiv.org/abs/2605.22594
[32] Minkowski Sum -- from Wolfram MathWorld - https://mathworld.wolfram.com/MinkowskiSum.html
[33] Triangular cupola - Wikipedia - https://en.wikipedia.org/wiki/Triangular_cupola
[34] Triangular cupola - Polytope Wiki - https://polytope.miraheze.org/wiki/Triangular_cupola
[35] Rhombicosidodecahedron — Grokipedia - https://grokipedia.com/page/Rhombicosidodecahedron
[36] Rhomb-icosidodecahedron - http://www.mi.sanu.ac.rs/vismath/zefiro2009sept/___RID_dissection.htm
[37] Rhombicosidodecahedron - Wikiwand - https://www.wikiwand.com/en/Rhombicosidodecahedron
[38] Deformations and second-order rigidity of polytopes · Pith Review - https://pith.science/paper/2607.09252
[39] (PDF) Rigidity, Tensegrity, and Reconstruction of Polytopes Under Metric Constraints - https://www.researchgate.net/publication/376785099_Rigidity_Tensegrity_and_Reconstruction_of_Polytopes_Under_Metric_Constraints
[40] Morphologically spherical but geometrically polyhedral formations. A:... - https://www.researchgate.net/figure/Morphologically-spherical-but-geometrically-polyhedral-formations-A-The-virion-like_fig1_343860128
