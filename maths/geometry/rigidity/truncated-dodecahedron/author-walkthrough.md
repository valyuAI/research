# A guide to defending the rigidity argument

This guide identifies what the author needs to understand. It is not a record of human review or agreement.

## The geometric question

Picture a truncated dodecahedron whose original edges are rigid rods and whose faces must remain flat. A decagonal face may shear within its plane: its diagonals and angles are not fixed. Can the whole object move continuously into a different shape?

The theorem says that no sufficiently small such motion changes the solid except by translating or rotating it. Cauchy's familiar rigidity theorem assumes congruent faces, so it cannot simply be invoked. Conversely, our result does not concern rods alone after the face-planarity requirement is dropped.

## Why the equations represent the intended solid

There are three coordinates for each of 60 vertices and each of 32 face normals: 276 variables. Each of 90 edges contributes a squared-length equation. Each of 180 vertex-face incidences contributes `vertex dot normal = 1`.

Writing the right-hand side as one is a local coordinate choice, not an extra physical condition: all original face planes avoid the origin. A nearby plane still has a nonzero offset and can be normalized that way. Three affinely independent vertices on a face determine its normal uniquely nearby.

Six additional coordinate equations remove translations and rotations. Their derivative on infinitesimal Euclidean motions has determinant of absolute value four, so the ordinary implicit-function theorem gives a genuine local slice. Without this check, isolation in an arbitrary slice would not necessarily prove rigidity.

## Why first-order calculations do not settle it

Modulo 1009, the 276-by-276 Jacobian has rank 272. Four infinitesimal parameters remain. This does not exhibit a genuine flex: a first-order motion may fail at higher orders.

The quadratic obstructions vanish. After solving the 272 independent equations formally, the four remaining equations take the form

```text
g_j(v) = C_j(v) + terms of degree at least four,
```

where each `C_j` is a homogeneous cubic in four variables. The checker derives these cubics directly from the original geometric equations. It does not merely trust a polynomial system supplied by a search program.

## Why the cubics kill every local branch

The certificate proves four exact identities

```text
v_i^9 = A_1i*C_1 + A_2i*C_2 + A_3i*C_3 + A_4i*C_4,
```

with degree-six multipliers. Replacing `C_j` by the true series `g_j` introduces only terms of degree at least ten. Every degree-33 monomial in four variables has some exponent at least nine. Consequently, in the quotient by the true equations, the 33rd power of the maximal ideal equals its 34th power.

Nakayama's lemma says that a finite module over a local ring cannot equal its own product with the maximal ideal unless it is zero. Applied to that 33rd power, it makes the entire maximal ideal nilpotent. The local ring is therefore zero-dimensional: there is no local curve, including any curve whose first nonzero terms occur beyond cubic order.

The finite identities alone do not authorize the phrase "third-order rigidity implies rigidity" in arbitrary systems. It is the displayed nilpotence argument that justifies the conclusion here.

## Why one finite field says something about the real solid

All original coefficients lie in the integral domain `A=Z[phi,1/55]`, where `phi^2=phi+1`. The finite-field calculation uses the residue `phi=627` modulo 1009. No denominator vanishes there.

More importantly, the original configuration is the zero displacement **over the entire ring A**. It defines a section of the family of equation spaces. Thus we know which point is being followed as the coefficients change characteristic.

For a finite-type family, the points isolated in their fibers form the quasi-finite locus, which is open. The section passes through this open set at the checked finite-field point. Its inverse image is a nonempty open subset of the integral base, so it contains the generic point. The specified characteristic-zero realization is therefore isolated. Base change through the real embedding into the complex numbers preserves this property.

This argument does not claim that every finite-field solution lifts, that modular rank equals real rank, or that modular polynomial multipliers lift coefficient by coefficient. The section and openness are the crucial ingredients.

## Questions the review should answer

- Which deformations are allowed, and why are Cauchy's theorem and edge-only rigidity different questions?
- Why do the saved coordinates and supporting inequalities identify the exact classical solid?
- What do the six gauge equations remove, and how is their transversality established?
- Why can the four remaining equations be obtained by formal elimination over a finite field?
- Why do degree-nine identities imply nilpotence despite arbitrary higher-order terms?
- Where is Nakayama's lemma used, and which module is finite?
- Why is the zero section necessary in the specialization argument?
- Why are flatness, properness and unchanged Jacobian rank unnecessary?
- Which steps are checked by code, and which are written mathematical deductions?
- Why does local rigidity exclude a nontrivial continuous deformation starting at the solid, while not asserting uniqueness among all distant realizations?

An outside specialist review would be especially valuable for the section argument and the exact correspondence between the local equation scheme and allowed geometric deformations.
