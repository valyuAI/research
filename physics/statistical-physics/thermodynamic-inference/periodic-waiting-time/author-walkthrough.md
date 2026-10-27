# The counterexample in plain language

## What the conjecture proposed

Suppose you can see some transitions of a physical system, but not all of them. Measure the time between visible transitions. If a sequence and its reversed sequence have different waiting-time statistics, can that difference safely provide a lower bound on dissipation?

The source proposed that this works even when the transition rates are driven periodically, using only data from the forward driving protocol. Our example shows that it can instead return a positive number when the defined entropy production is exactly zero.

## The smallest picture we use

There are three states, arranged in a triangle. Movement along every edge is equally fast in both directions at any given moment:

```text
1 <-> 2     speed a(t) = 1 + epsilon*cos(t)   visible
2 <-> 3     speed b(t) = 1 + epsilon*sin(t)   visible
1 <-> 3     speed 1                         hidden
```

Here `0 < epsilon < 1`, so every rate stays strictly positive. Think of the two visible links as doors whose widths open and close on different schedules. Neither door favors one direction over the other.

The probability of occupying each state is always `1/3`. Every forward probability flux equals its reverse. Every term of the entropy-production formula used in the source is therefore exactly zero.

## Where the false positive comes from

Compare the visible sequence `1 -> 2`, then `2 -> 3`, with its reverse: `3 -> 2`, then `2 -> 1`.

Both first jumps land in state 2. The subsequent waiting time depends on which door will open next. Since the two doors follow different periodic schedules, their order matters even though there is no directional probability current.

There is a crucial conditioning point. An event on the first door is more likely to occur when that door is wide open. Its starting phase is weighted by `a(t)`. The reversed event starts with phase weighted by `b(t)`. Averaging both starting phases uniformly would compute the wrong observation law.

With the correct weights, the two waiting densities `f(s)` and `g(s)` obey

```text
f(0) = g(0) = 1,
f'(0) - g'(0) = epsilon² > 0.
```

They therefore differ for small positive delays.

## Why one unequal pair proves that the whole estimate is positive

All four visible directed events occur at the same mean rate, `1/3`. After normalizing the event-pair distributions, the full proposed estimate is exactly `4/3` times a Kullback-Leibler divergence. This is a standard measure of the difference between probability distributions: it is nonnegative and is zero only when the two distributions agree almost everywhere.

Our one unequal pair proves they do not agree. The estimate is therefore strictly positive. The paper also checks the parts this argument needs: each waiting distribution row integrates to one, reverse pairs have the same support, and the logarithmic integral is finite.

## What the result does and does not change

The example disproves a specific proposed bound, not thermodynamics. It shows that the observed timing difference can record the order of changes in the driving protocol rather than entropy production under the chosen definition.

Reversing the labels is not the same experiment as reversing the whole driving schedule. The source's separately proved theorem uses the latter and is untouched. An external machine that changes the rates might itself consume energy; its cost is not included in the target entropy-production formula and is not determined here.

## Questions the human author should be able to answer

1. Why does instantaneous rate symmetry keep the state probabilities uniform?
2. Why is the event-conditioned phase distribution not uniform?
3. Which two sequences are compared, and why do both enter state 2?
4. Why does the derivative difference imply inequality on an interval, rather than only at one point?
5. Why does equal mean event rate let the complete estimator become a KL divergence?
6. Why are support and finiteness checks necessary?
7. Which exact conjecture is refuted, and which reversed-protocol theorem survives?

This is a guide for author review, not a record of completed human approval. The exact arithmetic checker verifies the derivative identities; the full probability argument remains a written proof.
