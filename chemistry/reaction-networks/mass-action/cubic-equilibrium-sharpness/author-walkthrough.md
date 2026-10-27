# The proof in plain language

## What we are trying to achieve

Fix a number `n`. We want a network with only `n` chemical species and `n` reactions that has as many distinct positive steady states as the published theorem allows: `n` of them on the same conservation surface. We also want the reactions' input sides to stay simple as the network grows.

“Cubic” refers to those input sides. A reaction such as `2X + Y -> X` has three input molecules and contributes a rate proportional to `X²Y`. It does not mean that every output also has at most three molecules.

## The central idea: turn steady states into roots of one polynomial

The network is designed so that all reaction fluxes must agree at a steady state. Its input matrix is invertible, so this equality forces every positive steady state onto one curve:

```text
x_i(t) = c_i t^(p_i),   t > 0.
```

The constants `c_i` are positive and the integer exponents `p_i` are distinct. A conservation law then cuts this curve in exactly the places where one sparse polynomial vanishes.

We choose the polynomial to vanish at any `n` distinct positive rational numbers, such as `1, 2, ..., n`. It has only `n + 1` terms. Descartes' rule of signs says such a polynomial cannot have more than `n` positive roots, counting repeated roots. Because we already supplied `n` distinct roots, they are all simple and there are no others.

That is the mathematical engine of the construction. The remaining work is to turn the selected polynomial into legal nonnegative input/output complexes and positive rate constants. The paper supplies those formulas and proves their validity for every `n`.

## A complete three-species instance

The reactions are

```text
2X + Y -> X              rate constant 1/306000
2Y + Z -> Y + 2Z         rate constant 1/79475
2Z     -> X + 2Y + Z     rate constant 1/121
```

Every positive steady state lies on `(X,Y,Z) = (60t³,85t²,11t⁴)`. All three reaction fluxes there equal `t⁸`, and the reaction vectors sum to zero, so the net change in each species vanishes.

On the conservation surface `-X + Y + Z = 36`, we get

```text
11t⁴ - 60t³ + 85t² - 36 = (t - 1)(t - 2)(t - 3)(11t + 6).
```

There are exactly three positive roots. They give the steady states `(60,85,11)`, `(480,340,176)` and `(1620,765,891)`.

## Why “nondegenerate” needs a separate argument

A simple root means the curve crosses the conservation surface instead of touching it tangentially. The paper proves that this transverse crossing is exactly what makes the dynamical Jacobian invertible **within** that surface. The full Jacobian is necessarily singular because the system has a conservation law.

Nondegenerate does not mean attracting or stable. We have not proved that a trajectory converges to any particular one of these states.

## Why three input molecules is optimal

Banaji and Feliu proved that quadratic networks of this size and rank have at most two nondegenerate positive equilibria. That immediately excludes the required `n` when `n >= 3`. Their separate two-species exclusion rules out two equilibria for `n = 2` as well. Our construction works with three input molecules, so the minimum is exactly three.

## Questions the human author should be able to answer

1. Why does a polynomial with `n + 1` terms and `n` distinct positive roots have no extra or repeated positive root?
2. Why are the displayed products nonnegative for either choice of each sign?
3. Why does equal flux describe every positive equilibrium, rather than only selected examples?
4. Why is the Jacobian restricted to the conservation surface the relevant one?
5. Why does the two-species case require its own published exclusion?
6. What prevents describing this as `n` stable states of a closed chemical system?

These questions are a guide for author review, not a record that review has happened. Exact checks of 35 finite examples are supporting evidence; the general proof is the argument above and its formulas in the manuscript.
