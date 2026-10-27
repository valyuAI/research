# An arithmetic certificate for rigidity of the truncated dodecahedron

Proof and certificate record, 17 October 2026. The result is local rigidity under fixed edge lengths and facet coplanarity. The exact encoding and certificate have passed independent local replay, and the written implications have been reviewed within the project. Priority review remains pending; this is not an external referee report.

## Target and source

Matthias Adrian-Himmelmann, Martin Winter and Zhen Zhang, *Deformations and second-order rigidity of polytopes*, [arXiv:2607.09252](https://arxiv.org/abs/2607.09252), leave the truncated dodecahedron's rigidity unresolved. Their constraints permit changes in the shape of a face while requiring its vertices to remain coplanar and all original edge lengths to stay fixed. Cauchy's theorem for fixed face shapes does not answer this question. The source establishes that all second-order stress obstructions vanish for this polytope.

The DeepResearch rigidity report identified this target, suggested reducing to four cubic obstructions, and supplied numerical evidence. Local work instead constructs a certificate in one finite characteristic and transfers isolation of the actual configuration to characteristic zero. The standard specialization machinery is not claimed as a new theorem.

## Coordinates and equations

Let phi=(1+sqrt(5))/2. The sixty vertices are the cyclic coordinate permutations of the following signed patterns, with signs chosen independently:

```
(0, ±(phi-1), ±(phi+2)),
(±(phi-1), ±phi, ±2phi),
(±phi, ±2, ±(phi+1)).
```

Duplicate zero signs are discarded. The exact edge length squared is 8-4phi. There are ninety such edges, twenty triangular facets and twelve decagonal facets. Every facet normal a_f is normalized by p_i dot a_f=1 on that facet. The certificate includes all vertex and normal coordinates, incidences and edges in Q(phi). Supporting-plane inequalities are checked by exact arithmetic in the positive real embedding, not a numerical tolerance.

One exact identification with the usual Archimedean solid is as follows. Take the twenty standard dodecahedral vertices (±1,±1,±1) and cyclic permutations of (0,±(phi-1),±phi). For each directed original edge a -> b, form phi*a+(phi-1)*b. These are precisely the sixty vertices above. Dividing by sqrt(5)=2phi-1 gives truncation parameter lambda=1/(phi+2). The regular pentagon edge-angle relation makes the new cut edges and shortened old edges equal: phi*lambda=1-2lambda.

There are 276 coordinate variables: three for each of sixty vertices and thirty-two normalized facet normals. Write u for their displacement from the saved configuration. For every original edge and vertex-facet incidence impose

```
|p_i+u_i-p_j-u_j|^2-|p_i-p_j|^2 = 0,
(p_i+u_i) dot (a_f+u_f)-1 = 0.
```

These give ninety edge and 180 incidence equations, all of degree two. Add six linear coordinate gauges, fixing displacement coordinates 0,1,2,3,4,6 in the saved ordering. Their derivative on the six-dimensional Euclidean-motion space is invertible. Thus near the original real configuration, every nearby framework can be moved uniquely into this slice by a nearby Euclidean motion. The normalized normals transform smoothly under that motion because no facet plane passes through the origin.

Call the 276 resulting equations F(u). They have an integral model over A=Z[phi,1/D], where D clears their finitely many rational denominators. All equations vanish identically at u=0, giving an actual zero-section over this integral base. The denominators are nonzero at the chosen prime below.

## Finite-field local isolation

Reduce modulo 1009 with phi mapped to 627; indeed 627^2-627-1=0 modulo 1009. The saved certificate has the following independently replayable structure.

1. The Jacobian J is 276 by 276 and has rank 272. Its four-dimensional kernel is the column span of K. A row transform splits the equations into 272 range equations and four complementary equations. A supplied range dual verifies a left inverse on the 272 pivot columns; the four left-null rows are independent. These identities certify the rank and an invertible equation transformation.
2. Put u=Kv+Iw, where v has four coordinates and I includes the 272 pivot coordinates. The derivative of the range equations with respect to w is the identity. The formal implicit-function theorem gives a unique w(v) with no constant or linear term.
3. Write F(u)=Ju+q(u), with q exactly quadratic. The supplied degree-two correction W2(v) satisfies J W2(v)+q(Kv)=0 in all 276 equations. In particular every quadratic complementary obstruction vanishes.
4. In the four complementary equations after formal elimination, the cubic terms are

```
C(v) = L [q(Kv+W2(v))-q(Kv)-q(W2(v))],
```

where L is the four-row left-null matrix. The bracket is homogeneous of degree three. Thus the four reduced series are g_i(v)=C_i(v)+terms of degree at least four.
5. The small certificate supplies four direct identities

```
v_i^9 = sum_(j=1)^4 A_ji(v) C_j(v),  i=0,1,2,3,
```

with every A_ji homogeneous of degree six over F_1009. Direct polynomial multiplication verifies these identities. No Gröbner-basis correctness assertion, sampled nonvanishing test or floating-point calculation is required.

The four cubic initial forms generate an ideal containing the ninth power of every variable, so the initial ideal of (g_1,...,g_4) is primary to the maximal ideal. More explicitly, every monomial of degree 33 contains some v_i^9, so m^33 is contained in (g)+m^34. In the quotient, the finite module m^33 equals its product with m; Nakayama's lemma gives m^33=0. Therefore

```
F_1009[[v0,v1,v2,v3]]/(g1,g2,g3,g4)
```

is Artinian. This is the completed local ring of the gauge-fixed special fiber at the original configuration. Completion preserves local dimension, hence that point is isolated in its fiber.

## Why one finite characteristic suffices here

Let X be the scheme over Spec(A) defined by the actual gauge-fixed equations F, and let sigma be the zero-section. The special point sigma(p) is isolated in its fiber, hence X -> Spec(A) is quasi-finite there. The quasi-finite locus is open. Its inverse image under sigma is a nonempty open subset of the integral base, and consequently contains the generic point. Thus the characteristic-zero point sigma(eta), over Q(phi), is also isolated in its fiber. Quasi-finiteness is preserved by field extension, so it remains isolated after extension to C.

Relevant primary references are the Stacks Project, [Tag 01TH](https://stacks.math.columbia.edu/tag/01TH) for isolated fiber points, [Tag 01TI](https://stacks.math.columbia.edu/tag/01TI) for openness, and [Tag 01TM](https://stacks.math.columbia.edu/tag/01TM) for base change. This argument does not infer a characteristic-zero identity from its reduction modulo a prime. It does not require flatness, properness, constancy of Jacobian rank or vanishing of the characteristic-zero quadratic obstructions.

Finally, transversality of the six gauges and the local Euclidean-action argument turn isolation in the slice into rigidity modulo Euclidean motions. A nearby polytope with the same original edge lengths and flat facets gives a nearby solution of the point-normal equations: its facet normals are uniquely and continuously normalized because the original facets are nondegenerate and avoid the origin. Therefore such a polytope is congruent to the original truncated dodecahedron.

## Verification boundary

The numerical convex hull in the generator only proposes incidence data. The independent checker validates exact supporting planes and identifies the points as a uniform truncation of the standard dodecahedron. It also validates the field schema, integer prime, denominator units, gauge transversality, all linear and quadratic identities, cubic assembly and four direct pure-power identities. The generator's own successful checks are not independent review.

The statement is rigidity of this particular classical polytope in the source's model, not a classification of all polytope rigidity or a general third-order jet criterion without hypotheses. The exact characteristic-zero proof uses local isolation and arithmetic specialization; a blanket assertion that third-order rigidity always implies rigidity would be false.

No public announcement, submission or contact with the source's authors has occurred. Originality is still subject to the current literature audit.
