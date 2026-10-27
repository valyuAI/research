# Finite-direction recovery: proved reductions and current certificate

17 October 2026. This extension of the audited full-slowness theorem is now included in the companion paper after independent internal arithmetic replay and geometric review. Eight-direction sufficiency is **not proved**.

## 1. Necessary lower bound: eight directions

At m fixed directions, unordered Christoffel spectra give m traces, m second elementary symmetric values, and m determinant values. Trace is a homogeneous ternary quadratic, so all trace measurements together have rank at most min(m,6). The data-map image therefore has dimension at most min(m,6)+2m. At m=7 this is 20, less than the 21-dimensional tensor space. The generic fiber has positive dimension, so seven directions cannot give generic recovery. This is a dimension obstruction, not a noise or algorithm statement.

The existing proof gives fifteen explicit sufficient directions. The argument below gives eleven **generic** directions, with no assertion that an arbitrary eleven-direction configuration works.

## 2. Collision notation and inherited bounds

Work over C. Write C=X+H and C'=X-H, with H nonzero. For a direction p, let

  Q(X,H;p) = tr(Gamma_X(p) Gamma_H(p)),
  R(X,H;p) = tr(adj(Gamma_X(p)) Gamma_H(p)) + det Gamma_H(p).

For direction configurations on which quadratic evaluation has rank six, equality of the sampled trace data implies tr Gamma_H=0 identically. Thus H lies in the 15-dimensional space K and (X,H) has ambient dimension36.

The audited rank theorem gives R_5={0}, dim R_r<=r-1 for6<=r<=14, and a nonempty full-rank locus of L_H:X->Q with rank15. Its two consequences used here are:

- The locus Q=0, H nonzero has dimension at most21: the full-rank kernel bundle has dimension15+6, and every deficient-rank stratum gives at most20.
- The locus Q=R=0, H nonzero has dimension at most20. This is the complete off-diagonal full-slowness collision bound, including every nongeneric H.

The second bullet is essential. One must not simply assign eight/eleven curve parameters when Q and R both vanish identically: in that case every direction is allowed, so its full direction-factor dimension is2m.

## 3. General-position configurations and incidence counting

For eleven ordered projective directions, take the nonempty Zariski-open set Omega in (P2)^11 with:

- no three directions collinear;
- no six directions on any degree-two plane curve;
- no ten directions on any degree-three plane curve;
- all directions nonisotropic if unit-vector physical interpretation is wanted.

These conditions are nonempty: polynomial evaluation at suitably chosen nodes is full rank for degrees1,2,3; each determinant condition defines a nonempty open set, and finitely many such open sets intersect in the irreducible configuration space. Reducible and nonreduced curves are included. In particular, quadratic evaluation has rank six.

For Q nonzero and R nonzero, let G be their complete greatest common divisor, up to scale, and d=degree G. When R=0 and Q nonzero, define G=Q, so d=4. The common-zero set consists of the curve G=0 and a finite set of common zeros of the coprime residual factors. Thus if k selected directions lie on G, the dimension of their choices over a fixed pair is at most k; the other choices have dimension zero. On Omega, k<=2,5,9 for d=1,2,3. For d=4 use k<=11.

The space of a tensor together with an eleven-direction configuration has dimension21+22=43. An off-diagonal collision incidence of dimension at most42 cannot dominate it. Once the bounds below hold, the fiber-dimension theorem gives a nonempty open set of direction configurations for which a generic tensor has no partner at all. The competing partner need not be generic.

## 4. Pair-locus bounds for factor degrees1,2,3

Let A_d be the cone of quartics with a degree-d factor. For d=1 or3, dim A_d=3+10-1=12. For d=2, dim A_2=6+6-1=11. These parameter counts include reducible and repeated factors. A nonzero quartic has only finitely many degree-d divisors up to scalar, by unique factorization; hence multiplicity creates no extra factor-choice dimension.

Over full-rank H, the map X->Q is surjective with a six-dimensional kernel. Thus imposing Q in A_d gives dimension at most15+6+dim A_d. For rank r<=14, the dimension is at most

  (r-1)+(21-r)+dim A_d = 20+dim A_d.

This includes all nongeneric H; it does not assume transversality of im L_H with A_d. Consequently the pair-locus bounds are33,32,33 for d=1,2,3. Requiring the same factor to divide R can only decrease these dimensions.

For eleven directions the resulting incidence bounds are35,37,42, respectively. No extra determinant-divisibility argument is needed for these cases.

### Stronger degree-two gate for the eight-direction investigation

For eight directions one needs the degree-two pair locus to have dimension at most31. The deficient-H estimate already gives31. For full-rank H, retain the quadratic factor [G] in P5 and the complementary nonzero quadratic A. The parameter space of (G,A) with Q=GA is the total space of a rank-six vector bundle over P5, with its zero section removed; it is irreducible of dimension11. Its pullback under the surjective L_H map, with the six-dimensional X kernel, is irreducible of dimension32. This avoids splitting into supposedly generic irreducible-factor components: reducible and square factors are in the same irreducible parameter space.

The condition G divides R is closed in this space, as the zero of the quotient-bundle section modulo G times the quartics. It is proper. Fix the full-rank isotropic H0 with Gamma_H0=3pp^T-qI and det Gamma_H0=2q^3. Choose G=p1^2+p2^2+2p3^2, which does not divide q^3, and any nonzero quadratic A. Surjectivity gives X1 with L_H0 X1=GA. Along X=tX1, t nonzero, Q=tGA remains nonzero and

  R(tX1,H0) mod G = t^2 [tr(adj Gamma_X1 Gamma_H0)] + [2q^3].

The constant term in this quotient is nonzero, so the section cannot vanish identically along the family. One explicit point of G=0 is p=(i,i,1), where q=-1 and the constant term is-2. Therefore the closed locus is proper in the entire irreducible32-dimensional parameter space and has dimension at most31. This single witness is sufficient because irreducibility has been established; it is not being silently assumed to work on multiple components.

## 5. New degree-four certificate and eleven-direction candidate theorem

Introduce a homogeneous quadratic S with six coefficients. In the42-dimensional affine space

  E_X (21) + K_H (15) + Sym2_S (6),

let V be the cone defined by the28 coefficients of

  R(X,H;p) - Q(X,H;p) S(p) = 0.

These are homogeneous cubics in the42 source variables. If Q is nonzero, a factor of degree four means precisely Q divides R; S is then unique. This also includes R=0, with S=0. Thus dim V<=31 is sufficient for the needed pair-locus bound31. Including the H=0 and Q=0 components in V only strengthens the bound being certified; they are not discarded by a hidden saturation.

A fixed integer42-by-11 linear map defines a projective P10 slice. Its matrix has rank11 modulo32003, hence over Q. Substitution gives28 cubic equations in11 variables over F32003. Singular4.4.1p5 returns a standard basis of2085 elements, affine dimension zero, in25.12seconds. The leading ideal includes a pure power of every variable, with exponents

  3,3,3,3,4,4,5,5,6,6,7.

Because the equations are homogeneous, zero-dimensionality means that the only affine zero over the algebraic closure is the origin. The corresponding projective slice is empty. Projective properness transfers this emptiness from the finite-field geometric fiber to characteristic zero. A projective P10 disjoint from P(V) in P41 gives dim P(V)<=30, hence dim V<=31.

The source polynomials were independently reconstructed using explicit Christoffel entries and the determinant odd-part identity. The check used286 parameter-grid points times28 direction-grid points. These grids are unisolvent for the full bidegree (3,6), so this is a polynomial-identity verification, not a random evaluation screen. It also verifies the slice rank and pure-power leading terms.

**Certificate status (completed 17 October 2026):** all eleven explicit ideal-membership witnesses now pass independent standard-library modular polynomial multiplication against the original 28 cubics. They are direct identities, without intermediate basis assumptions. The final degree-seven identity was obtained through eleven degree-six right-hand sides in the original cubic Macaulay system and then flattened; generation is not trusted by the verifier. Source reconstruction also passes on the complete unisolvent grids. The compact package is this directory. Run `python3 -O -u verify_direct_powers.py` and `python3 -O -u verify_gcd4_slice_source.py 11` here. Two independent internal investigators replayed both checkers, and the full incidence argument received independent geometric review without an identified gap. This closes the computational gate and supports its inclusion in the companion research draft. No external peer review is implied.

The full eleven-direction incidence table is:

| Pair class | Pair dimension bound | Direction-fiber bound | Total |
|---|---:|---:|---:|
| Q,R coprime |36|0|36|
| gcd degree1 |33|2|35|
| gcd degree2 |32|5|37|
| gcd degree3 |33|9|42|
| gcd degree4, including R=0 |31|11|42|
| Q=0,R nonzero |21|11|32|
| Q=R=0,H nonzero |20|22|42|

Every total is less than43. Together with the verified degree-four bound, this argument establishes eleven generic directions as sufficient, globally against all competing tensors. The dimension lower bound establishes eight as necessary. Neither claim implies eight-direction sufficiency.

## 6. What remains open for eight, nine, or ten directions

For eight directions, the degree1 and strengthened degree2 cases are closed, as are coprime, Q=0, and all rank-H<=8 cases. Gcd degrees3 and4 still need pair dimension at most28. No such bound has been proved.

For ten directions, a degree-four pair bound30 and a degree-three pair bound31 would suffice. A12-variable empty homogeneous slice of V would give the first bound. It would not close the second bound. One cannot announce ten-direction sufficiency from that slice alone.

For nine directions, both degree3 and degree4 pair loci would need dimension at most29. Jacobian rank or a single affine singleton fiber does not prove any of these global statements.

## 7. Bounded failed experiment

`prepare_eight_direction_fiber.py` constructs one fixed eight-direction affine fiber over F32003, with a rational full-rank Jacobian at the known tensor. The slimgb computation was killed at its120-second budget before a basis was produced. Files `eight_direction_fiber.sing`, `_input.json`, `.log`, and `_run.json` retain the attempt. It supplies no uniqueness or generic-degree evidence.

## 8. Literature scope

The primary reference remains de Hoop, Ilmavirta, Lassas, and Várilly-Alvarado, arXiv:2307.03312v2, 30April2025. Classical papers located include Aristégui and Baste, *Optimal recovery of the elasticity tensor of general anisotropic materials from ultrasonic velocity data*, JASA101(1997),813-833, DOI10.1121/1.418040; and Every and Sachse, *Determination of the elastic constants of anisotropic solids from acoustic-wave group-velocity measurements*, Physical Review B42(1990),8196, DOI10.1103/PhysRevB.42.8196. The latter primary abstract describes an optimization method demonstrated for cubic crystals and group velocities, not a generic full-tensor finite phase-spectrum uniqueness theorem. The Aristégui publisher full-text fetch failed, so its exact finite-direction claims remain unverified. Search results suggesting six-direction reconstruction with particle displacement/polarization measurements describe richer data than unordered phase spectra and cannot invalidate the eight-direction lower bound.

This targeted search is not an exhaustive priority audit. No novelty conclusion follows from the absence of an eight-direction theorem in the inspected material.
