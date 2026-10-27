# Exact short-lag verification

Run `python3 -B -O check_short_lag.py` here, or use the command in the parent README.

The independent checker represents a polynomial as a dictionary with keys `(k, d)` for `exp(i*k*t) * epsilon**d`, and coefficients as pairs of rational numbers. It implements finite sums, multiplication, differentiation and period averaging. Failed identities raise an exception even under Python optimization.

The six checked identities are:

1. Mean `a` is one.
2. Mean `b` is one.
3. `f(0) = g(0) = 1`.
4. `f'(0) = -2 - epsilon^2/2`.
5. `g'(0) = -2 - 3*epsilon^2/2`.
6. `(f-g)'(0) = epsilon^2`.

These identities are exact for the declared smooth rate functions. They establish the algebraic part of the short-lag argument. They do not check the source's hypotheses, conditional-density interpretation, probability normalization, support, integration bounds, or publication priority. Those are addressed in the paper and independent written review. No theorem-prover coverage is claimed.

The illustration is separate. Its optional matplotlib script evaluates the displayed phase integrals by periodic quadrature and compares 128 with 256 nodes. It is a visualization, not a certificate for the theorem.

[Build and presentation review](build-review.md) records the completed replay and PDF inspection.
