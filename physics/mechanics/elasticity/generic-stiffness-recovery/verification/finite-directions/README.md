# Exact certificate for the quartic-divisibility bound

17 October 2026. This package certifies one computational ingredient in the proposed eleven-generic-direction elasticity recovery theorem. It does not independently certify the entire geometric theorem or its novelty. The complete incidence argument and its inherited hypotheses are in `INCIDENCE_PROOF.md`.

## Run

Python 3.10 or later, standard library only:

```sh
python3 -O -u verify_gcd4_slice_source.py 11
python3 -O -u verify_direct_powers.py
```

Both commands must exit successfully. They write small audit JSON files. Typical combined runtime is a few seconds. The `-O` flag deliberately disables Python assertions; the checkers use explicit exceptions and remain effective.

No Singular installation, symbolic-algebra package, floating-point tolerance, downloaded data, or network access is needed. The `.sing` file is read as a polynomial-data file; it is not executed.

## What is checked

Write a pair of density-normalized elasticity tensors as `C=X+H`, `C'=X-H`. The trace collision restricts `H` to a 15-dimensional linear space. For the corresponding Christoffel matrices define

```text
Q(X,H;p) = tr(Gamma_X(p) Gamma_H(p)),
R(X,H;p) = [det(Gamma_X(p)+Gamma_H(p))
            - det(Gamma_X(p)-Gamma_H(p))]/2.
```

Introduce an arbitrary homogeneous quadratic `S(p)`. The 28 coefficients of the sextic `R-Q*S` are homogeneous cubics in 42 source variables: 21 coordinates of `X`, 15 of `H`, and 6 of `S`.

`gcd4_slice_n11_input.json` gives a fixed integer 42-by-11 slice matrix, all coefficient orders, and the prime 32003. The source checker verifies its full column rank modulo the prime, verifies that the modulus is prime, and independently reconstructs all 28 cubics from explicit Christoffel entries and the determinant formula. It checks the complete product of two unisolvent simplex grids: 286 parameter points and 28 direction points. The degrees are respectively three and six, below the characteristic. This is an exact polynomial identity check, not a random numerical test.

The second checker verifies eleven explicit identities

```text
F_i = sum(j=1..28) U_ji * J_j    over F_32003[t0,...,t10],
```

where `J_j` are the original cubics. It then verifies that the leading monomials of `F_i`, in graded reverse lexicographic order with `t0 > ... > t10`, are

```text
t0^3, t1^3, t2^3, t3^3, t4^4, t5^4,
t6^5, t7^5, t8^6, t9^6, t10^7.
```

All products use exact integer arithmetic reduced modulo the prime. The coefficient files are grouped by the degree of `F_i`. Each coefficient is indexed by its original generator and its local target within that degree group. The checker requires exact polynomial equality, proper coefficient degree, all eleven distinct leading variables, and complete target coverage.

## Why the certificate gives a characteristic-zero bound

The verified leading monomials generate a zero-dimensional monomial ideal. Because every `F_i` belongs to the original ideal, that ideal has finite-dimensional quotient as well. Its homogeneous zero set over the algebraic closure of the finite field consists only of the origin. No assertion that the eleven polynomials form a Gröbner basis is needed.

Consequently the corresponding projective 10-plane has empty intersection with the projectivized cubic variety modulo 32003. The same intersection is a projective scheme over the integers localized away from 2. Its image in that base is closed by properness. A nonempty generic fiber would force that image to contain the generic point and therefore every closed point, contradicting the verified empty fiber at 32003. The characteristic-zero slice is therefore empty too.

The ambient projective space has dimension 41. A projective 10-plane cannot be disjoint from a projective subvariety of dimension at least 31. Thus the projectivized cubic variety has dimension at most 30, and its affine cone has dimension at most 31.

For `Q != 0`, the relation `Q | R` determines `S` uniquely. Hence the tensor-pair locus where `Q` divides `R`, including `R=0`, has dimension at most 31. The certificate includes all source variables and imposes no hidden saturation or genericity restriction on `H`.

## Scope and provenance

Singular computations and exact finite-field linear algebra found the identities. Those generation procedures, intermediate bases, and their dimension outputs are not trusted by these two checkers. The final certificate is about one megabyte and consists only of the original equations, the slice, the eleven targets, and direct ideal-membership coefficients.

The full eleven-direction argument also uses the previously audited bounds on the rank strata of `X -> Q` and on complete full-slowness collisions. Those are separate ingredients, not proved by this package. Eleven is a sufficient generic bound, not a minimality claim, an arbitrary-direction guarantee, or a numerically stable measurement protocol. Eight directions are necessary by a separate dimension argument; sufficiency at eight, nine, or ten remains unresolved in this work.

Internal independent replay and geometric review are recorded separately. No external peer review or definitive priority assessment is implied.
