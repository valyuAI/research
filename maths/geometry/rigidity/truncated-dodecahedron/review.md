# Independent review of the arithmetic rigidity argument

Review date: 17 October 2026. Scope: the mathematical implications from the saved finite-field certificate to local rigidity of the classical truncated dodecahedron. The full coefficient and incidence reconstruction is independently replayed by `verification/independent_verification.py`. This review does not establish priority or authorize publication.

**Conclusion: no mathematical gap found in the stated implication. Confidence: high, conditional on the independently checked encoding and certificate identities.** The special-fiber isolation, transfer along the zero section, and removal of Euclidean motions are valid. Flatness, properness, characteristic-zero vanishing of the quadratic obstructions, and constant Jacobian rank are not needed.

I inspected the written argument, the exploratory generator, and the exact certificate now stored in `verification/`. I independently multiplied all four degree-nine identities using dictionary polynomial arithmetic. I also computed the six-gauge determinant exactly over Q(phi): it is **4**. These small checks supplement, rather than replace, the independent full verifier.

## 1. The geometric model matches the source question

The source, Adrian-Himmelmann, Winter and Zhang, *Deformations and second-order rigidity of polytopes*, [arXiv:2607.09252](https://arxiv.org/abs/2607.09252), studies fixed original edge lengths together with coplanarity of each original face. Faces may change shape. Its Sections 2.2 and 2.3 use normalized point-hyperplane coordinates and quotient by Euclidean isometries. Its introduction and computational discussion explicitly leave the truncated dodecahedron unresolved after the second-order test.

The present equations impose precisely those equalities, with additional coordinate gauges. They do not triangulate the decagons or fix their diagonals. Ninety original edges and 180 vertex-face incidences give 270 quadratic equations in 276 variables. The remaining six equations are linear gauges.

Using normalized normals introduces no unwanted restriction locally. Each original facet has three affinely independent vertices and its plane avoids the origin. Those three position vectors are therefore linearly independent. For nearby coplanar vertices, the equations `p_i dot a_f = 1` determine a unique nearby normal, continuously and indeed rationally in those three vertices. All actual nearby polytopal deformations are consequently represented. The equality scheme may contain other degeneracies away from the base configuration; excluding them is unnecessary for this local isolation argument.

## 2. Formal elimination is valid in characteristic 1009

Write `k = F_1009` and `F(u) = Ju + q(u)`, with `q` homogeneous quadratic. The certificate supplies four kernel columns `K`, 272 pivot-coordinate columns `I`, a 272-row range dual `R`, and four independent left-null rows `L`. The relevant identities are

```
JK = 0,    RJI = Id_272,    LJ = 0.
```

The free-coordinate block of `K` is the four-dimensional identity. Thus `(v,w) -> Kv + Iw` is an invertible linear change of all 276 variables. The stacked row transformation `(R;L)` is invertible: any linear relation between its rows restricts on `JI` to a relation among the rows of the identity, leaving only a relation among the independent rows of `L`.

Set `H(v,w) = RF(Kv+Iw)`. Its linear part is exactly `w`. The formal map

```
(v,w) -> (v,H(v,w))
```

therefore has identity linear part and is an automorphism of `k[[v,w]]`. This is the formal inverse-function theorem, or directly the power-series parameter-change result [Stacks, Tag 07NM](https://stacks.math.columbia.edu/tag/07NM). It is valid over every field and requires no division by factorials. It yields a unique `w(v)` with no constant or linear terms and identifies the quotient by the 272 range equations with `k[[v]]`.

The saved correction `W2(v)` has support only in pivot coordinates and satisfies

```
JW2(v) + q(Kv) = 0.
```

Consequently `W2 = Iw_2`, where `w_2` is the homogeneous quadratic part of `w(v)`. In particular `Lq(Kv)=0`. The four remaining series are

```
g(v) = LF(Kv+Iw(v)) = C(v) + O((v)^4),
C(v) = L[q(Kv+W2(v)) - q(Kv) - q(W2(v))].
```

Terms of degree three in the unknown later correction disappear because `LJ=0`; later quadratic cross terms have degree at least four. Thus the recorded cubic forms are the actual leading homogeneous terms of the formally eliminated equations, not merely an unrelated third-order test.

Completion of the original polynomial local ring is the power-series quotient by the same equations. This also follows from exactness of completion for finite modules over a Noetherian ring, [Stacks, Tag 00MA](https://stacks.math.columbia.edu/tag/00MA). We obtain the asserted completed local ring `k[[v]]/(g_1,...,g_4)`.

## 3. The pure-power identities force isolation

Let `S=k[[v_0,v_1,v_2,v_3]]`, `m=(v_0,...,v_3)` and `Jg=(g_1,...,g_4)`. The certificate gives homogeneous degree-six polynomials `A_ji` with

```
v_i^9 = sum_j A_ji C_j.
```

Because `g_j-C_j` has order at least four,

```
v_i^9 = sum_j A_ji g_j + an element of m^10.
```

Every degree-33 monomial in four variables is divisible by some `v_i^9`: otherwise all four exponents would be at most eight, giving total degree at most 32. Multiplying the preceding identities by degree-24 monomials proves

```
m^33 subset Jg + m^34.
```

In the Noetherian local quotient `B=S/Jg`, with maximal ideal `n`, this says `n^33=n^34=n*n^33`. The ideal `n^33` is a finite module, so Nakayama's lemma gives `n^33=0`. See [Stacks, Tag 00DV, part 2](https://stacks.math.columbia.edu/tag/00DV). Hence `B` is Artinian and has dimension zero.

This explicit argument avoids ambiguity between an ordinary polynomial term order and the lowest-degree, maximal-ideal-adic initial ideal. It also shows exactly why arbitrary higher-order terms cannot restore a local branch. The result does not rely on a general assertion that a finite-order rigidity test automatically implies rigidity.

Completion preserves the dimension of a Noetherian local ring, [Stacks, Tag 07NV](https://stacks.math.columbia.edu/tag/07NV). Therefore the original special-fiber local ring has dimension zero. The point is rational, hence closed, and the fiber is of finite type over `k`; it is an isolated fiber point, equivalently a point where the structural morphism is quasi-finite. [Stacks, Tag 01TH](https://stacks.math.columbia.edu/tag/01TH) gives this equivalence.

## 4. Special-fiber isolation transfers to this characteristic-zero point

All saved vertex and normal coefficients have denominators in `{1,5,11}`. The original translated equations therefore admit the concrete integral model

```
A = Z[phi,1/55],    phi^2-phi-1=0,
X = Spec(A[u_1,...,u_276]/(F)).
```

Here `A` is a domain with fraction field `Q(phi)`. The ideal `(1009,phi-627)` defines the chosen residue map to `F_1009`; 55 is a unit there. The modular changes of equations and variables are used only to analyze that fiber. Their entries do not need to lift to a characteristic-zero elimination or to be added to this integral model.

Crucially, `F(0)=0` is an identity over `A`. Thus `u=0` defines a section `sigma: Spec(A) -> X`, not just a finite-field solution with an unspecified lift.

Let `U` be the locus where `X -> Spec(A)` is quasi-finite. This is open by [Stacks, Tag 01TI](https://stacks.math.columbia.edu/tag/01TI). It contains `sigma(p)` by the preceding calculation. Consequently `sigma^{-1}(U)` is a nonempty open subset of the integral scheme `Spec(A)` and contains its generic point `eta`. Thus the specified point `sigma(eta)` is quasi-finite, hence isolated, in the `Q(phi)` fiber.

Quasi-finiteness at points is stable under base change, explicitly [Stacks, Tag 01TM, part 1](https://stacks.math.columbia.edu/tag/01TM). After either embedding `Q(phi) -> C`, the corresponding zero-section point is isolated in the complex fiber. In particular this holds for the positive real embedding defining the classical solid.

This reasoning requires no flatness or properness of `X` over `A`. It makes no claim that modular cubic identities lift coefficientwise, that the characteristic-zero Jacobian has the same rank, or that its quadratic obstructions vanish. The section and openness are the reason a single good finite characteristic suffices here.

## 5. The gauge slice implies rigidity modulo Euclidean motions

For a point `(x,y,z)`, the infinitesimal Euclidean-motion rows used in the generator are

```
[1,0,0, 0,z,-y],
[0,1,0, -z,0,x],
[0,0,1, y,-x,0].
```

Selecting rows `0,1,2,3,4,6` from the saved vertices gives a square six-by-six matrix with determinant **4**, after reduction by `phi^2=phi+1`. I recomputed this independently. This proves real transversality without appealing only to modular rank.

The ordinary real implicit-function theorem applied to these six gauge functions and the six parameters of a nearby rigid motion gives a unique nearby rigid motion placing every sufficiently nearby vertex configuration into the slice. Facet normals transform compatibly: under `p -> Rp+t`, a normalized normal transforms as

```
a -> Ra / (1 + (Ra) dot t).
```

The denominator is nonzero near the identity. All edge-length and incidence equations are preserved by this transformation. Complex isolation of the slice implies real isolation, so every sufficiently nearby allowed configuration is congruent to the original one.

For the source's continuous-motion definition, local rigidity suffices. Along any allowed continuous path, the set of times congruent to the original configuration is open by this local argument and closed by continuity of all pairwise distances. It contains the initial time and therefore is the entire connected parameter interval.

## 6. Remaining boundaries and recommended wording

The theorem is local rigidity of this specific classical polytope in the fixed-edge, flat-face model. It does not establish global uniqueness among all realizations with the same edge lengths, rigidity of its bare bar graph without face constraints, or a classification of Archimedean solids beyond the stated example.

The whole result still depends on the separate exact audit that the supplied points, supporting facets, original edges, Jacobian, row duals, kernel, correction and cubic coefficients are the intended ones. The theoretical implication reviewed here has no remaining gap. No numerical rank or unverified convex-hull triangulation can substitute for those exact checks.

The primary references were read through the Valyu CLI. Their public links are included above and in [the source review](source-review.md). No inference about novelty follows from these foundational references or from this theory audit.

## 7. Exact geometric replay and convention

The standalone checker reconstructs all 1,740 strict supporting inequalities in the positive embedding of Q(sqrt(5)), verifies the 20 regular triangles and 12 regular decagons, identifies all 60 vertices with the uniform truncation of a standard regular dodecahedron, and checks the original edge/facet incidences. Its rotation basis has the opposite sign from the one displayed in Section 5; it therefore reports gauge determinant -4. Both conventions give absolute determinant 4 and the same transverse slice. The saved replay reports the checker convention.

There is no Lean formalization of this rigidity proof. Exact certificate replay and the written algebraic-geometric deductions are distinct verification layers.
