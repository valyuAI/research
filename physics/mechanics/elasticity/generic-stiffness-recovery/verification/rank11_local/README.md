# Rank-eleven local certificate

The exact calculation over `Q(i)` gives **affine tangent dimension 8** at the harmonic-degree-two highest-weight point of the locus `rank L_H ≤ 11`. The projective tangent dimension is **7**. This passes the requested affine bound of 10.

The physical coefficient map and the limitation of the collision-incidence strategy are described in `../INVERSE_ELASTICITY_STATUS.md`. The calculation here concerns the complexified, 15-dimensional trace-kernel parameter space; its highest-weight point is not a real physical stiffness tensor.

## Certificate

`check_rank11_tangent.py` parses the exact integer-coefficient 15-by-21 matrix in `../collision_incidence_matrix.sing`. The file's finite-field declaration is not used: all coefficients are interpreted in characteristic zero. The point is the `harmonic_degree2_times_norm` entry in `../minimum_rank_borel_checks.json`.

At that point, the matrix has rank 11. Exact left and right nullspace bases have dimensions 4 and 10. With ordinary algebraic transpose, define

\[
T(\delta H)=N^T L_{\delta H}R.
\]

Flattening the 4-by-10 normal block gives a 40-by-15 linear map. Its rank is exactly 7:

- Rows `[0,2,12,20,22,30,32]` and columns `[0,1,2,3,4,6,9]`, using zero-based indices, give a 7-by-7 minor of determinant **81**.
- The supplied 15-by-8 kernel matrix is annihilated exactly. Its rows `[5,7,8,10,11,12,13,14]` form the identity, certifying independence and hence the reverse rank bound.

The tangent condition is exact at a rank-11 point: after invertible row and column changes making the base matrix `diag(I_11,0)`, the first derivatives of its 12-by-12 minors are precisely the entries of the lower-right normal block. Thus the Zariski tangent space has dimension `15−7=8`.

## Projective normalization and incidence dimension

The chosen point has `h9=1`. The radial vector lies in the affine tangent kernel and has nonzero `h9` coordinate. Imposing `δh9=0` therefore adds one independent equation. The normalized projective tangent has dimension `14−7=7`, as also checked directly.

Consequently each irreducible component of the rank-at-most-11 locus containing this point has affine dimension at most 8. On its rank-exactly-11 part, the `X` kernel has dimension `21−11=10`; the associated affine incidence has dimension at most **18**. Equivalently, projective dimension 7 plus one scale parameter plus the ten-dimensional `X` fiber gives 18. Additional determinant-difference equations cannot increase this bound.

This does **not** control a component whose only Borel-fixed degeneration is the harmonic-degree-four rank-six point. That separate local problem remains necessary for the global incidence argument. No generic-injectivity conclusion is drawn here.

Run `python3 -u check_rank11_tangent.py`. Full exact matrices, kernel bases, projective chart checks and input hashes are retained in `rank11_tangent_certificate.json`; progress and summary are in `rank11_tangent_checks.log`.
