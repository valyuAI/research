# Hales-Jewett formal statement review

Reviewed 17 October 2026. Source: [HalesJewett.lean](../formal/ValyuResearch/HalesJewett.lean), SHA-256 `dac198f4fff3bbe6437170575bf4ff7cd8cc2860949eb0c28800628f44df862e`.

**Finding:** no semantic mismatch, vacuous main theorem, or missing dimensional hypothesis was found. The formal statements match the paper's off-diagonal number with a red full line and a blue consecutive two-point partial line. This review concerns what the declarations mean and how their hypotheses connect. Compilation, axiom inspection, and kernel replay are recorded separately in the formal-coverage ledger.

## Coloring and line definitions

`Word k n` is exactly the cube of length-`n` words on the alphabet `{0,...,k-1}`. `linePoint s w a` replaces every coordinate in `s` by the same alphabet value `a` and preserves the other coordinates. The `s.Nonempty` requirement in `Avoids` excludes empty wildcard sets. Every ordinary variable word has such a representation; redundant choices of `w` on wildcard coordinates do not change the line.

The predicate supplied to `Avoids` is the blue class; its complement is red. The first conjunct says every full line contains a blue point, which excludes a red full line. The second forbids two blue points whose alphabet values satisfy `b.val = a.val + 1`. It does not forbid arbitrary separated values, introduce wraparound adjacency, or admit reversed wildcards. For a nonempty wildcard set those consecutive points are necessarily distinct.

The auxiliary `Consecutive` relation describes the same partial-line geometry: the words differ in at least one coordinate, and every changed coordinate uses the same transition from `a` to `a+1`. Unchanged coordinates may take any alphabet values. `avoids_no_consecutive` explicitly constructs the nonempty set of changed coordinates, so the upper-bound argument uses only configurations forbidden by `Avoids`.

## Prime construction and lower dimensions

`blue p s` matches the paper's rule: `s=0`, or `s>1` with remainder one modulo `p`. `sum_linePoint` correctly expresses the coordinate sum as the fixed-coordinate sum plus wildcard count times the alphabet value.

For wildcard count strictly below a prime `p`, `residue_one` uses a nonzero element of `ZMod p`, so inversion is justified by the actual primality hypothesis. `line_contains_blue` handles the deleted sum-one case explicitly: it either uses the alphabet value `p` or the zero word. The condition `p < k` is exactly what makes the extra alphabet value available. When all `p` coordinates are wildcards, the proof establishes that the fixed sum is zero before using that boundary case.

The stronger theorem `prime_coloring_avoids_of_le` constructs an avoiding coloring in every dimension `n <= p`, not merely dimension `p`. Thus the subsequent lower-bound proof does not assume an unproved monotonicity principle for forcing dimensions. Dimension zero causes no false lower-bound inference: there are no nonempty wildcard sets, so an avoiding coloring exists there, as required.

## Upper bound

`forces_self` proves forcing in dimension `k` for every `k >= 2`. Its `k` axis lines are indexed by the number of initial coordinates changed from `a` to `a+1`, while the last coordinate is free. Blue completions exist by the first clause of `Avoids`. Two completions with the same final value would be a forbidden consecutive pair, so the chosen final-value map is injective and hence surjective on `Fin k`.

A blue constant word comes from the full diagonal line. If its value has a successor, surjectivity supplies a blue completion consecutive to it. If it is the last alphabet value, the proof instead uses its predecessor. In both cases the final coordinate guarantees distinct words. The argument is a valid coordinate-reversed version of the paper's upper-bound proof; no extra forbidden configuration is assumed.

## Least dimension and exact values

For `k >= 2`, `HJ k` is `Nat.find` of the proposition that a forcing dimension exists, with `forces_self` furnishing existence. `forces_HJ` proves that the selected dimension forces the configurations, and `HJ_le_self` uses the leastness property to give the upper bound. `prime_lower_bound` rules out every dimension at most `p`, yielding `p+1 <= HJ k` for prime `p < k`. Consequently `HJ_prime_successor`, `HJ_eight`, and `HJ_twelve` express the stated exact values.

The definition assigns zero to `HJ 0` and `HJ 1`; those convenience cases lie outside the paper's `k >= 2` domain. They do not affect the prime-successor theorem. The formal file does not establish publication priority or the separate reported geometric value `G(8,2)=7`, and it should not be described as doing so.
