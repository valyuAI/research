# Independent source and certificate audit

17 October 2026. The command below passes using only the Python standard library, including with assertions disabled:

```sh
python3 -B -O verification/independent_verification.py
```

The saved output is `verification/independent_verification.json`, with hashes of the original data, displayed cubic source, direct identities, and checker. The checker imports neither the coordinate probe nor the certificate generator, and never executes Singular. Runtime on the task machine was below one second.

## Geometric object

The primary model is the edge-length and face-coplanarity problem in Adrian-Himmelmann, Winter and Zhang, *Deformations and second-order rigidity of polytopes*, [arXiv:2607.09252](https://arxiv.org/abs/2607.09252), dated 13 July 2026. Its introduction and experimental discussion explicitly leave the truncated dodecahedron's rigidity unresolved by their second-order methods. The retrieved primary text is retained separately in the research record. This audit is not a later-literature priority search.

The saved coordinates are independently converted from `a+b*phi` to `a+b*sqrt(5)` arithmetic. Exact comparisons use rational intervals for the positive square root, not floating-point hull calculations. The following are checked:

- 60 distinct vertices, 90 exact edges, 20 equilateral triangular facets and 12 regular decagonal facets.
- All 180 vertex-facet equalities and all 1740 strict nonincidence inequalities `n_f dot v_i < 1`.
- Each normal reconstructed independently by a cross product and plane-offset normalization.
- Equal circumradii and exact adjacent central-angle cosines for every facet: `-1/2` for triangles and `phi/2` for decagons. Each facet edge graph is a connected cycle.
- Three incident facets and three incident edges at every vertex. The three normals are independent, and the incident edges realize all three pairwise intersections of the supporting planes. Thus the known tangent cone is the complete trihedral tangent cone. There are no unaccounted-for facets or edges of the convex hull.

The identification as the uniform truncated dodecahedron is direct. Let the original dodecahedron have vertices

```text
(±1,±1,±1), and cyclic permutations of (0,±(phi-1),±phi).
```

Its 30 edges, 12 regular pentagonal supporting facets and three-facet incidence at each of its 20 vertices are verified exactly. For each directed edge `a -> b`, the saved 60-point set is exactly

```text
phi*a + (phi-1)*b.
```

Dividing these coordinates by `sqrt(5)=2*phi-1` gives truncation fraction `lambda=1/(phi+2)` from each endpoint. The old-edge remainder and the new cut edge have the same length because `1-2*lambda=phi*lambda`. The 20 triangles correspond to original vertices; the 12 decagons correspond to original pentagons, with both incidence correspondences checked exactly.

## Equations and gauge

There are 276 variables: three coordinates for each of 60 vertices and 32 facet normals. There are 90 squared-edge-length equations and 180 incidence equations `n_f dot v_i=1`. The facet normalization is a local chart: the base planes avoid the origin, and their offsets remain nonzero nearby. It adds no fixed face angles, diagonal lengths, unit-normal constraints or fixed face shapes.

The six gauge coordinates are `[0,1,2,3,4,6]`. In the standard infinitesimal Euclidean-motion convention

```text
delta v = t + omega × v,
delta n = omega × n - (n dot t)*n,
```

the exact gauge determinant is `-4`. The original probe uses `v × omega` instead, reversing all three rotation columns and giving `+4`. The invariant transversality statement is the nonzero absolute determinant 4. The independently reconstructed motions annihilate all 270 ungauged equations modulo 1009. In characteristic zero the same identities follow from the displayed action and the exact base incidences.

## Independent modular algebra

The checker verifies primality of 1009, the residue `phi=627`, and absence of denominator poles at this residue. It reconstructs the 276-by-276 gauged Jacobian and all quadratic terms from the equations above.

It checks `J*K=0` and that the four free-coordinate rows of `K` form the identity. The stored 272-by-276 range dual is verified to be a left inverse on the 272 pivot columns of `J`. These two facts establish rank exactly 272 without trusting a rank calculation. The four stored left-nullspace rows are checked both for independence and annihilation of `J`.

All entries of the second-order correction `W2` are checked through `J*W2 + q(K)=0`, with zero free coordinates. Every one of the 40 second-order obstruction coefficients vanishes. The 80 coefficients of the four cubic obstructions are independently reconstructed as the left-null projection of the degree-three terms of `q(K*t + W2(t))`.

Finally, exact coefficient multiplication verifies all four identities

```text
t_i^9 = sum(j=0..3) A_ji(t)*C_j(t),   i=0,1,2,3,
```

where each multiplier has degree six and `C_j` are the independently reconstructed original cubics. The displayed Singular input is also checked against these cubics, but is never run. The identities imply that their homogeneous ideal has only the origin as its zero set over the algebraic closure of the finite field. No Gröbner basis or computer-algebra dimension readout is assumed.

Seven deliberate corruptions are rejected by `python3 -B -O verification/negative_verification_checks.py`: a facet-normal coordinate, kernel coefficient, range-dual coefficient, left-nullspace coefficient, second-order correction coefficient, cubic coefficient, and final identity coefficient. The mutations preserve valid input types and trigger the intended geometric or arithmetic checks. Results are saved in `verification/negative_verification_results.json`.

## Scope

This audit establishes the exact geometric source, transverse gauge, modular linear algebra, obstruction coefficients and direct polynomial identities. The formal-local elimination argument and the transfer of local isolation to characteristic zero are separate written deductions reviewed by other investigators. The modular rank by itself is not a claimed upper bound on characteristic-zero rank, and the audit is not external peer review or a full formalization.
