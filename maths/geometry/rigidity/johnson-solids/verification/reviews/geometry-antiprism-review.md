# Adversarial review: first-order rigidity of antiprisms in the point-hyperplane polytope model

Task DR-039 | mode heavy | completed 2026-10-26T11:56:25.319Z | cost 3.125

# Adversarial review: first-order rigidity of antiprisms in the point-hyperplane polytope model

## Executive summary

- **The proof sketch holds up under review.** I found no error in the eigenspace decomposition, the triangle step, the treatment of the low modes, or the "every height" claim. The one apparent gap, that the cap condition "does not force η = 0 for n ≥ 4", comes from reading the cap condition without splitting it by Fourier mode. It is not an error in the sketch.
- **No prior art was located.** None of the retrieved passages state first-order rigidity, rigidity or flexibility of antiprisms in this model. The searched material includes HSW (arXiv:2505.00874v3), AHWZ (arXiv:2607.09252v1), the extrusion-symmetry paper, classical symmetry-adapted rigidity papers and the DeformationPaths.jl test folder. This is absence in the material retrieved, not a proof of absence in the literature.
- **The final "settles every regular-faced polyhedron except the truncated dodecahedron" claim is not supported as stated.** The 41 / 6 / 45 classification of the Johnson solids appears in none of the retrieved sources, and AHWZ covers only Platonic, Archimedean and Catalan solids. The antiprism result alone does not close the problem.
- **The classification of regular-faced polyhedra is correct** for strictly convex polyhedra. The usual date for Zalgaller's proof is imprecise (the original is 1967), and the 13 Archimedean solids rely on vertex-transitivity.
- **No source claims that all regular-faced convex polyhedra have been settled** in this model. The truncated dodecahedron is explicitly undecided in AHWZ.

## 1. Review of the argument

### Setup and cited background

The setup matches the sources. AHWZ's realization constraint is ⟨p_i, a_σ⟩ = 1, so facet hyperplanes avoid the origin [[1]](https://arxiv.org/abs/2607.09252). The stress conditions (3.4) and (3.5) are exactly as stated in the question [[1]](https://arxiv.org/abs/2607.09252). For a polyhedron, the first-order flex space has the same dimension as the stress space, so first-order rigidity is equivalent to having no non-zero stress (Prop. 3.6) [[1]](https://arxiv.org/abs/2607.09252). Trivial motions form a space of dimension C(d+1, 2), which is 6 for d = 3 [[1]](https://arxiv.org/abs/2607.09252). First-order rigidity implies rigidity (Theorem 3.3) [[1]](https://arxiv.org/abs/2607.09252).

HSW use a slightly different normalisation (unit normals, ⟨p_j − p_i, a_σ⟩ = 0) [[2]](https://arxiv.org/abs/2505.00874). AHWZ state that the two realization spaces are birationally equivalent near convex realizations with the origin in the interior [[1]](https://arxiv.org/abs/2607.09252). A centred antiprism satisfies this condition at every height.

### Triangle step: correct

On a triangular facet, the three vertices lie on an affine plane not through the origin. They are therefore linearly independent, and Σ η_i p_i = 0 forces η = 0 on that facet. This uses the normalisation ⟨p_i, a_σ⟩ = 1 [[1]](https://arxiv.org/abs/2607.09252). The cap normals are ±e_z/z0, since the cap planes are z = ±z0 (reviewer's check).

### The alleged cap-condition gap: not a gap

The cap condition Σ_k η_k a_k = 0 has three equations and n unknowns, so it does not force η = 0 as a whole. The sketch does not claim it does. It claims this only in the eigenmodes j = 0, ±1, and that claim is correct. A reviewer's check:

- The cap vertices a_k = (R cos 2kφ, R sin 2kφ, z0) have Fourier content only in modes j = 0 (the z0 component) and j = ±1 (the horizontal components).
- In a mode ζ = e^{2πij/n} with j ∉ {0, ±1}, the cap condition is vacuous, as expected.
- In the modes j = 0, ±1, the cap condition is one non-trivial scalar equation per cap, in the single unknown η_A (respectively η_B). It forces that unknown to vanish.
- In generic modes, the horizontal components of vertex equilibrium contain no η, because the cap normals are vertical and the triangle η's vanish. They give the 4×4 system in ω. Once M4 is invertible, ω = 0, and the vertical component then gives η = 0. This is the route the sketch takes.

### Eigenspace decomposition over ℂ

Complexifying the real stress space and decomposing under the cyclic rotation is valid. The rotation by 2π/n is a symmetry of the framework, with a_k → a_{k+1} and b_k → b_{k+1}. A real non-zero stress has a non-zero component in some complex eigenspace. Showing every eigenspace is zero therefore shows the real space is zero. The four edge orbits (top, bottom, a_k b_k, b_k a_{k+1}) account for all 4n edges.

The factors in det M4 vanish exactly at ζ = 1 and ζ = e^{±2iφ}, which are the modes j = 0, ±1. The factors (c−1)³(c+1) are non-zero because c = cos(π/n) lies in [1/2, 1) for n ≥ 3. So M4 is invertible exactly for the generic modes. For n = 3 there are no generic modes and the argument rests entirely on the low-mode minors. For n = 4 the single generic mode is j = 2.

### "Every height"

M4 involves only horizontal components of edge vectors, which are independent of z0. The low-mode minors carry the factors z0 and z0², which are non-zero for z0 > 0. So the argument as written is uniform in height. This is a different situation from the height sensitivity AHWZ report for truncated polytopes, where changing the truncation height turns first-order flexible realizations into first-order rigid ones [[3]](https://arxiv.org/html/2607.09252v1). It does not contradict that observation.

### What cannot be verified here

The closed-form determinants and minors (for example −64 R³ sin φ z0 (c−1)²(c+1)²) appear in no retrieved source. I checked structure and consistency only, not the algebra. The numerical confirmation for n = 3..24 is consistency evidence, not a proof for all n. An independent symbolic check of the minors is the main remaining step.

Two small points:

- The n = 3 case (the octahedron) is covered independently. The octahedron is the 3-antiprism [[4]](https://arxiv.org/abs/1807.08297). Any simplicial convex polyhedron is first-order rigid by Dehn's theorem [[3]](https://arxiv.org/html/2607.09252v1)[[2]](https://arxiv.org/abs/2505.00874).
- The classical Alexandrov–Whiteley extension of Dehn's theorem assumes rigid faces [[5]](https://arxiv.org/pdf/2505.00874). Rigidity in the deformable-face model is a different statement, and a stronger one.

## 2. Prior art

### Antiprisms in this model

None of the retrieved passages mention antiprisms in the point-hyperplane model.

- **HSW (arXiv:2505.00874v3).** It proves that 3-polytopes are generically rigid (Theorem 1.2), which concerns generic realizations, not the regular antiprism [[2]](https://arxiv.org/abs/2505.00874). It treats prisms and duoprisms as flexible via Minkowski flexes [[2]](https://arxiv.org/abs/2505.00874)[[5]](https://arxiv.org/pdf/2505.00874), and notes that the cube is flexible [[2]](https://arxiv.org/abs/2505.00874).
- **AHWZ (arXiv:2607.09252v1).** Its computations cover the five Platonic and 13 Archimedean solids (Table 1) and the 13 Catalan solids (Table 2) [[3]](https://arxiv.org/html/2607.09252v1). Its Question 8.1 asks whether Dehn's theorem extends to non-simplicial polytopes, suggesting polytopes whose only faces are triangles and 4-gons as a candidate class [[3]](https://arxiv.org/html/2607.09252v1). The square antiprism (triangles plus squares) falls in that class.
- **Software.** DeformationPaths.jl is introduced in arXiv:2602.08016 [[6]](https://arxiv.org/html/2602.08016). Its test folder lists Framework.jl, Polytope.jl, SpherePacking.jl, VolumeHypergraph.jl, runtests.jl and various.jl [[7]](https://github.com/matthiashimmelmann/DeformationPaths.jl/tree/master/test). The visible part of Polytope.jl contains dodecahedron, truncated dodecahedron, truncated icosahedron and great rhombicosidodecahedron tests [[8]](https://raw.githubusercontent.com/matthiashimmelmann/DeformationPaths.jl/master/test/Polytope.jl). The visible part includes the truncated dodecahedron's 4 extra flexes and 4 stresses, matching AHWZ [[8]](https://raw.githubusercontent.com/matthiashimmelmann/DeformationPaths.jl/master/test/Polytope.jl). The retrieved file text is partial, and the other test files and AHWZ's supplementary material were not seen. An antiprism test therefore cannot be excluded.

### Prisms

HSW states that Cartesian products of flexible polygons give "many flexible polytopes … (such as prisms or duoprisms)" [[2]](https://arxiv.org/abs/2505.00874). The Minkowski reorientation mechanism applies even when the summands move trivially, provided the orientations are generic [[5]](https://arxiv.org/pdf/2505.00874). HSW's wording is "many", so the universal "every prism is flexible" is a natural extension of the stated mechanism rather than a quoted theorem. AHWZ also mention a hexagonal prism with a non-zonotopal flex [[3]](https://arxiv.org/html/2607.09252v1).

### Classical symmetry-adapted rigidity

- **Counting rules.** The Fowler–Guest symmetry-extended Maxwell rule is Γ(m) − Γ(s) = Γ(v)×Γ_T − Γ(e) − Γ_T − Γ_R [[9]](https://arxiv.org/abs/2108.06620)[[10]](https://arxiv.org/html/0812.3785). It gives necessary conditions for symmetric bar-joint frameworks. The Kangwai–Guest papers are cited alongside it [[11]](https://dl.acm.org/doi/abs/10.5555/3116673.3117146).
- **Related symmetric-framework papers.** Isostaticity conditions appear in Connelly et al. [[12]](https://arxiv.org/pdf/0803.2325), and a short proof of the counting rule in Owen–Power [[10]](https://arxiv.org/html/0812.3785). Block-and-hole polyhedra appear in the Guest–Fowler perforated-polyhedra paper [[13]](https://sciencedirect.com/science/article/pii/S0020768316000603). Guest's applications list has no antiprism entry [[14]](https://www3.eng.cam.ac.uk/~sdg/symmetry/).
- **Extrusion symmetry.** Owen–Schulze treat prisms as extruded point-hyperplane frameworks. Their triangular prism framework in ℝ² is continuously flexible [[15]](https://arxiv.org/abs/2304.12740), and a constrained cube has three shearing flexes [[15]](https://arxiv.org/abs/2304.12740). These are prism and cube flexibility results, not antiprism results.
- **Surfaces.** He–Robertz (arXiv:2506.22019v2) concerns higher-order rigidity of polyhedral surfaces in other models [[16]](https://arxiv.org/abs/2506.22019).

Verdict: none of these contain an antiprism first-order rigidity theorem for planar-cap frameworks in this model. This conclusion is limited to the passages retrieved, and the primary papers were mostly seen in excerpt only.

## 3. Is the classification correct?

The statement "5 Platonic + 13 Archimedean + prisms + antiprisms + 92 Johnson solids" is correct for strictly convex polyhedra with regular faces [[17]](https://tupelo-schneck.org/polyhedra/background.html)[[18]](https://proofwiki.org/wiki/Classification_of_Convex_Polyhedra_whose_Faces_are_Regular_Polygons)[[19]](https://arxiv.org/abs/2512.05577)[[20]](https://arxiv.org/abs/1610.06425).

| Point | Finding |
|---|---|
| Johnson's role | Listed 92 solids and conjectured completeness, *Canad. J. Math.* 18 (1966), 169–200 [[21]](https://www.cambridge.org/core/journals/canadian-journal-of-mathematics/article/convex-polyhedra-with-regular-faces/5E3FAE0232E2158F93E0A62BB5B1AD39)[[22]](https://dmccooey.com/polyhedra/Johnson.html) |
| Zalgaller's proof | Zap. Nauchn. Sem. LOMI 2 (1967), 5–221 [[23]](https://www.mathnet.ru/php/archive.phtml?wshow=paper&jrnid=znsl&paperid=1408&option_lang=eng)[[24]](https://www.mathnet.ru/php/archive.phtml?jrnid=znsl&wshow=contents&option_lang=eng&viewarchiveID=12). Described as "taking 220 pages" [[19]](https://arxiv.org/abs/2512.05577) and dated 1967 [[25]](https://arxiv.org/abs/2101.10743) |
| 1969 | Consultants Bureau English translation [[26]](https://www.wikidata.org/wiki/Q135221954). Many secondary sources cite "Zalgaller 1969" [[27]](https://mathworld.wolfram.com/JohnsonSolid.html)[[28]](https://en.wikipedia.org/wiki/Johnson_solid). The English book is listed at 95 pages [[29]](https://books.google.com/books/about/Convex_Polyhedra_with_Regular_Faces.html?id=W53koQEACAAJ) or 101 pages [[30]](https://us.amazon.com/Convex-Polyhedra-Regular-Seminars-mathematics/dp/1489956719), versus roughly 217 pages for the Russian original. The sources do not say why they differ. |
| Overlaps | The cube is a prism and the octahedron an antiprism [[17]](https://tupelo-schneck.org/polyhedra/background.html) |
| Rigor of the proof | A secondary source (Math StackExchange, quoting Timofeenko) says Zalgaller's theorem was given with only a brief indication of proof [[31]](https://math.stackexchange.com/questions/3498904/what-are-the-main-ideas-needed-to-prove-that-only-92-johnson-solids-exist). This is not independently verified. Timofeenko later gave a computer-algebra-assisted treatment [[32]](https://www.interocitors.com/tmp/papers/timo-parquet.pdf)[[33]](https://www.researchgate.net/publication/238877133_Convex_polyhedra_with_parquet_faces) |
| Independent confirmation | arXiv:2512.05577 classifies regular-polygon spherical tilings without using the Johnson–Zalgaller result [[19]](https://arxiv.org/abs/2512.05577) |

Three caveats apply.

- **Archimedean count.** The count of 13 requires vertex-transitivity. The elongated square gyrobicupola (J37) is locally vertex-regular. Some Russian authors counted it as a 14th Archimedean solid [[34]](https://faculty.washington.edu/moishe/branko/BG53.Regular-faced%20polyh.pdf)[[35]](https://alchetron.com/Elongated-square-gyrobicupola).
- **Strict convexity.** "Convex regular-faced" in the Johnson–Zalgaller sense means strictly convex. Allowing coplanar adjacent regular faces forming a single "parquet" face adds another 76 polyhedra to the list [[32]](https://www.interocitors.com/tmp/papers/timo-parquet.pdf). Whether such polyhedra matter depends on how faces are defined in this model.
- **Truncated dodecahedron.** It is an Archimedean solid, so it is in the list [[36]](https://en.wikipedia.org/wiki/Truncated_dodecahedron)[[17]](https://tupelo-schneck.org/polyhedra/background.html).

## 4. Has all of this been settled before?

No source settles rigidity of all regular-faced convex polyhedra in this model. The established results are:

- **Platonic, Archimedean and Catalan solids (AHWZ).** Of these 31 polytopes, the truncated dodecahedron is the only one left undecided. It has a 4-dimensional first-order flex space, is not prestress stable and is not second-order rigid, and no available method tests rigidity beyond second order [[3]](https://arxiv.org/html/2607.09252v1). Initial higher-order experiments suggest it is third-order rigid [[3]](https://arxiv.org/html/2607.09252v1).
- **Generic rigidity for 3-polytopes (HSW).** This concerns generic realizations only [[2]](https://arxiv.org/abs/2505.00874).
- **Johnson solids.** AHWZ does not test them [[3]](https://arxiv.org/html/2607.09252v1). The split into 41 first-order rigid, 6 first-order flexible but second-order rigid, and 45 flexible is not in any retrieved source. Without that classification, the "settles everything except the truncated dodecahedron" conclusion is unestablished.
- **Prisms and antiprisms.** Prisms are covered by HSW's flexibility constructions. Antiprisms are covered only if the proof sketch is accepted.

## 5. Implications and next steps

1. **Check the algebra independently.** Verify det M4 and the low-mode minors symbolically. Confirm the ranks of the full rigidity matrix for a range of n and heights.
2. **Position the result carefully.** The claim is new as far as the retrieved record shows. It should not be presented as having been checked against the full literature, nor as a final step towards classification until the Johnson-solid split is documented.
3. **Cite the classification precisely.** Use Johnson 1966 for the list and Zalgaller 1967 (Russian original) for completeness, and state "strictly convex" and the vertex-transitive definition of Archimedean.
4. **Keep the prism claim at the level of the source.** Cite HSW's Minkowski construction [[2]](https://arxiv.org/abs/2505.00874)[[5]](https://arxiv.org/pdf/2505.00874) and make the tilt argument explicit for the triangular prism, where the base polygon is itself rigid.

## Sources

[1] Deformations and second-order rigidity of polytopes - https://arxiv.org/abs/2607.09252
[2] Rigidity of polytopes with edge length and coplanarity constraints - https://arxiv.org/abs/2505.00874
[3] Deformations and second-order rigidity of polytopes - https://arxiv.org/html/2607.09252v1
[4] The volume of a compact hyperbolic antiprism - https://arxiv.org/abs/1807.08297
[5] Rigidity of polytopes with edge length and coplanarity constraints - https://arxiv.org/pdf/2505.00874
[6] 2602.08016 - https://arxiv.org/html/2602.08016
[7] DeformationPaths.jl/test at master · matthiashimmelmann/DeformationPaths.jl · GitHub - https://github.com/matthiashimmelmann/DeformationPaths.jl/tree/master/test
[8] https://raw.githubusercontent.com/matthiashimmelmann/DeformationPaths.jl/master/test/Polytope.jl - https://raw.githubusercontent.com/matthiashimmelmann/DeformationPaths.jl/master/test/Polytope.jl
[9] States of self-stress in symmetric frameworks and applications - https://arxiv.org/abs/2108.06620
[10] FRAMEWORKS SYMMETRY AND RIGIDITY - https://arxiv.org/html/0812.3785
[11] Coning, Symmetry and Spherical Frameworks - https://dl.acm.org/doi/abs/10.5555/3116673.3117146
[12] [arXiv:0803.2325v2 [math.MG] 27 Sep 2008](http://arxiv.org/abs/0803.2325v2) - https://arxiv.org/pdf/0803.2325
[13] Mobility of a class of perforated polyhedra - ScienceDirect - https://sciencedirect.com/science/article/pii/S0020768316000603
[14] Simon Guest: Symmetry - https://www3.eng.cam.ac.uk/~sdg/symmetry/
[15] Mobility of geometric constraint systems with extrusion symmetry - https://arxiv.org/abs/2304.12740
[16] Second-order prestress stability and third-order rigidity of polyhedral surfaces - https://arxiv.org/abs/2506.22019
[17] Regular-faced Polyhedra - https://tupelo-schneck.org/polyhedra/background.html
[18] Classification of Convex Polyhedra whose Faces are Regular Polygons - ProofWiki - https://proofwiki.org/wiki/Classification_of_Convex_Polyhedra_whose_Faces_are_Regular_Polygons
[19] Tiling the Sphere with Regular Polygons - https://arxiv.org/abs/2512.05577
[20] A classification of polyhedral graph by combinatorially rigid vertices - https://arxiv.org/abs/1610.06425
[21] Convex Polyhedra with Regular Faces | Canadian Journal of Mathematics | Cambridge Core - https://www.cambridge.org/core/journals/canadian-journal-of-mathematics/article/convex-polyhedra-with-regular-faces/5E3FAE0232E2158F93E0A62BB5B1AD39
[22] Johnson Solids - https://dmccooey.com/polyhedra/Johnson.html
[23] V. A. Zalgaller, “Convex polyhedra with regular faces”, Zap. Nauchn. Sem. LOMI, 2, Nauka, Moscow–Leningrad, 1967, 5–221 - https://www.mathnet.ru/php/archive.phtml?wshow=paper&jrnid=znsl&paperid=1408&option_lang=eng
[24] Zapiski Nauchnykh Seminarov POMI: Archive - https://www.mathnet.ru/php/archive.phtml?jrnid=znsl&wshow=contents&option_lang=eng&viewarchiveID=12
[25] The Rest of the Tilings of the Sphere by Regular Polygons. - https://arxiv.org/abs/2101.10743
[26] Convex Polyhedra with Regular Faces - Wikidata - https://www.wikidata.org/wiki/Q135221954
[27] Johnson Solid -- from Wolfram MathWorld - https://mathworld.wolfram.com/JohnsonSolid.html
[28] Johnson solid - Wikipedia - https://en.wikipedia.org/wiki/Johnson_solid
[29] Convex Polyhedra with Regular Faces - Viktor A. Zalgaller - Google Books - https://books.google.com/books/about/Convex_Polyhedra_with_Regular_Faces.html?id=W53koQEACAAJ
[30] Amazon.com: Convex Polyhedra with Regular Faces (Seminars in mathematics): 9781489956712: Zalgaller, Viktor A.: Books - https://us.amazon.com/Convex-Polyhedra-Regular-Seminars-mathematics/dp/1489956719
[31] polyhedra - What are the main ideas needed to prove that only $92$ Johnson solids exist? - Mathematics Stack Exchange - https://math.stackexchange.com/questions/3498904/what-are-the-main-ideas-needed-to-prove-that-only-92-johnson-solids-exist
[32] Convex Polyhedra with Parquet Faces - https://www.interocitors.com/tmp/papers/timo-parquet.pdf
[33] Convex polyhedra with parquet faces - https://www.researchgate.net/publication/238877133_Convex_polyhedra_with_parquet_faces
[34] THE FACES OF A REGULAR-FACED POLYHEDRON B. GRUNBAUM and N. W. JOHNSON - https://faculty.washington.edu/moishe/branko/BG53.Regular-faced%20polyh.pdf
[35] Elongated square gyrobicupola - Alchetron, the free social encyclopedia - https://alchetron.com/Elongated-square-gyrobicupola
[36] Truncated dodecahedron - Wikipedia - https://en.wikipedia.org/wiki/Truncated_dodecahedron
