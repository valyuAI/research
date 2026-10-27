# A guide to defending the Hales-Jewett proof

This is a reading guide, not a record of author approval. Work through the examples and then explain the proof without following the text line by line.

## What is being proved?

A word is a point in a discrete cube. For alphabet `{0,1,2,3}`, the variable word `(*,1,*)` traces the four points `(0,1,0)`, `(1,1,1)`, `(2,1,2)`, `(3,1,3)`. The full set is a combinatorial line. The first two points form a consecutive partial line; the first and last do not.

We color every word red or blue. We want to avoid both an entirely red full line and a blue pair at consecutive positions on a line. `HJ(k,2;2)` is the first dimension in which avoiding both becomes impossible. Showing an avoiding coloring in dimension `p` gives a lower bound `p+1`; a separate known argument gives the upper bound `k`.

## Why this coloring?

For prime `p`, in dimension `p`, make a word blue precisely when its coordinate sum is zero, or is greater than one and congruent to one modulo `p`.

For `p=3`, alphabet size four, the possible blue sums are `0,4,7`. For `p=7`, alphabet size eight, they are `0,8,15,22,29,36,43`.

The unrepaired residue-one rule meets every line with fewer than `p` wildcards, since the wildcard count is invertible modulo `p`. It misses the all-wildcard line, whose sums are multiples of `p`. Making the zero word blue repairs that line, but creates a forbidden consecutive pair with each unit vector. Removing precisely those unit vectors completes the repair.

## The entire proof reduces to two integers

Let `d` be the number of wildcards and `S` the sum of fixed coordinates. The sum at line position `a` is `S+d*a`.

**Case `d=p`.** Every coordinate varies, so `S=0`. Only position zero is blue. The full line is not red and no adjacent pair is blue.

**Case `d<p`: adjacent positions.** Their sums differ by `d`, so they cannot both have residue one modulo `p`. The only new blue point is zero. A line adjacent to it has next sum `d`. If `d=1`, that point was deliberately removed; if `d>1`, it has the wrong residue. No blue consecutive pair appears.

**Case `d<p`: a blue point somewhere.** Since `d` is invertible modulo `p`, some `a` between zero and `p-1` gives residue one. That point works unless its sum equals one. If its position is zero, then `S=1`; position `p` has sum `1+d*p` and is blue. If its position is positive, nonnegativity forces `S=0` and `d=a=1`; the zero point is blue instead. This is exactly why the alphabet must include `p`.

Three concrete lines for `p=3`, alphabet four:

| `d,S` | Sums along the line | Blue sums | Exceptional issue |
|---|---|---|---|
| `3,0` | `0,3,6,9` | `0` | All wildcards |
| `2,1` | `1,3,5,7` | `7` | The sum-one point is replaced using position `p` |
| `1,0` | `0,1,2,3` | `0` | The removed unit point is replaced by zero |

Restricting this coloring to a coordinate face yields a coloring in every smaller dimension with the same avoidance property. Therefore the least forcing dimension exceeds `p`.

## Where the upper bound comes from

In dimension `k`, a coloring avoiding red full lines has a blue point on every line, including a blue constant word `c^k`. Consider the `k` axis lines whose first `k-1` entries move successively from a symbol `a` to its successor `a+1`; their final coordinate is free. Choose a blue point on each. If two chosen points have the same final coordinate, they form a forbidden consecutive pair, so their final coordinates are all distinct. They therefore use every alphabet value.

Choose `a=c` if `c` has a successor, or `a=c-1` if `c` is the last alphabet value. One chosen point then forms a forbidden consecutive pair with `c^k`. This contradiction gives dimension at most `k`. Combining it with the construction for `k=p+1` gives equality.

## Questions the review should answer

- Why does the argument need a prime, and exactly where is primality used?
- Why are consecutive positions essential? Could a line contain two blue points farther apart?
- Why is the maximum-wildcard case different?
- Why does deleting a sum-one point not leave a completely red line?
- Why does avoiding a configuration in dimension `p` also avoid it in smaller dimensions?
- What does the source contribute, and what is new in this manuscript?
- What does Lean certify? Why does it not establish the `G(8,2)` computation or priority?
- Why does this not prove the full conjecture at alphabet sizes nine and ten?

Being able to answer these is a useful starting point for author review. It is not a record that the review has occurred.
