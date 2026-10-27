# Storyboard: Global optimality of conjugate restart laws

Audience: GCSE maths and physics. Running example (paper Example 2.4, verification
`resetting_verification.json`): walker spreading coefficient D = 1, target distance map
p(x) = 2e^{-2x}, best recipe = random (exponential) timer with rate 1, average search time 1.

Colour meaning: walker and its paths blue (PRIMARY); target, keys and the target map gold (WARM);
restart jumps and timers grey dashed with a yellow flash when the timer rings (SECONDARY = the
thing changing now); the reference recipe and its success curve teal (ACCENT); rival recipes
maroon (EXTRA); infinite or failing values red (WARN).

| # | Scene | Narration summary | Visual | Viewer now understands |
|---|-------|-------------------|--------|------------------------|
| 1 | Keys | Lost keys: keep going, or go back and start again? Restarting can be faster on average. | House, a path, a figure-dot drifting away, keys somewhere unseen; a dashed "go back" arrow. | The question. |
| 2 | Walker | A walker takes random coin-flip steps on a line; the target is a point; turning the line upright and letting time run across draws each search as a jagged path. One quick hit, one that wanders off. | Horizontal number line with house at 0 and keys; the line rotates into the vertical axis of a position-time plot; two seeded paths. | Random walk, target, first hit, space-time picture. |
| 3 | Average | Thousands of searches: most short, a few enormous; average infinite on a line (classic fact). | Histogram of first-hit times (exact Levy law, x = 1/2) with a tail arrow and "average = infinity" in red. | Average search time, and why it can be infinite. |
| 4 | Restart | A timer rings; if not found, jump back to 0 and start a fresh attempt. The unlucky path is cut short and a later attempt succeeds; average becomes finite. | Same plot; the wandering path is cut at the timer; yellow flash; grey dashed drop to 0; new attempts; success marked teal. "infinite -> finite". | What restart means and why it helps. |
| 5 | Timers | Fixed timer vs random timer (constant chance per moment, like radioactive decay); a recipe is any rule for picking each wait independently; average time = attempt length / success chance (2 s, 1 in 4, so 8 s). | Two rows of wait bars: equal (fixed) and varied (random); a row of four attempt blocks, the last teal; the formula. | Restart recipes and the renewal ratio. |
| 6 | Question | The target position is unknown: a map, near likely. Averaging over the map, random timers with rate r give average 1/(sqrt r (2 - sqrt r)): too often bad, too rare bad, best rate 1 gives 1. But is a random timer the best shape at all? | Gold map curve 2e^{-2x}; then cost curve over rate r with the minimum at (1, 1); rival icons with a question mark. | The optimisation question over all recipes. |
| 7 | Conjugate | Evans and Ray (2025): for a recipe, find the map where it is natural. Success curve e^{-x}; square and rescale gives 2e^{-2x}, exactly our map. On it the recipe is balanced (stationary), but balanced is not best; their checks were numerical, inside two families. | Teal success curve; it squares into a lower curve, which rescales onto the gold map; a landscape with a small dip and a deeper valley. | The prior construction and the open gap. |
| 8 | Result | New theorem for the walker on a line: the recipe is the global and unique best on its conjugate map (whenever that map exists and the average time on it is finite). Scope: positive, finite, independent waits; no adaptive or costly restarts. | Statement card; a small scope list. | What is claimed, and what is not. |
| 9 | KeyIdea | Attempt length is built from the success curve with weight min(x, y), symmetric. Rival cost = sum over pairs; pairs (x, y) and (y, x) give u/v and v/u. u/v + v/u = 2 + (u-v)^2/(uv). Check with u = 2, v = 1. Twos give our cost; squares are never negative. Zero leftover forces equal success curves, and the success curve fingerprints the timer, so unique. The pairing trick is known (Davila and Topp); the use here is new. | Two dots on a line, weight label, swap; two pair cards merge; TransformMatchingTex of the identity; numeric check; rival cost = our cost + squares >= 0. | The decisive step of the proof. |
| 10 | Example | Best: random timer rate 1, average 1. Computer check: rates 1/4 and 9/4 give 4/3; a blend gives 1.27; 36 random blends 1.002 to 1.451. Every fixed timer is infinite on this map (our own short calculation). Checks do not replace proof. | Dot plot of costs above a dashed line at 1; a red arrow off the top for the fixed timer. | Real numbers from the verification file. |
| 11 | Rooms | Finite rooms with exits; map = starting room; trick needs reversibility; converse under a technical condition (cyclicity). One-way loop with exit rates 1, 2, 3: prescribed cost 2332/4453; rate 9/10 is lower by 761111595/7705213313411 (about 1e-4). | Three rooms, two-way arrows (balanced), then a one-way loop; exact fractions. | The reversibility characterisation and the counterexample. |
| 12 | Wrap | Written proofs; Lean checks only the finite algebra and the three-room numbers; no peer review; novelty provisional. Recap three points, open questions, end card. | Status list with ticks and crosses, recap list, open list, end card. | Status and what is unknown. |

## Number ledger

- Exponential timer rate r, D = 1: success curve f(x) = e^{-x sqrt r}; for r = 1, f = e^{-x}, f^2 = e^{-2x},
  Z = 1/2, map p = 2e^{-2x} (paper Example 2.4 with r0 = 1, D = 1).
- Average over the map for exponential rate r: J(r) = 1/(sqrt r (2 - sqrt r)), from m(x) = (e^{x sqrt r} - 1)/r.
  J(1) = 1, J(1/4) = J(9/4) = 4/3 (verification entries 1-3).
- Blend of rates 0.2 and 5 with weights 0.4 and 0.6: 1.27063 (verification entry 4).
- 36 random four-rate blends: min 1.00202, max 1.45146 (verification entries 5-40).
- Fixed timer t: f(x) = erfc(x / sqrt(4t)) decays like e^{-x^2/(4t)}, so h/f grows like e^{x^2/(4t)} and the
  map-average diverges for every t. Own calculation, checked numerically (truncated integrals grow without bound);
  not in the paper.
- No restart: first-hit time T = x^2/(2 Z^2) for standard normal Z (D = 1); infinite mean. Classic.
- Three rooms: Q = [[-2,1,0],[0,-3,1],[1,0,-4]], exit rates 1, 2, 3; J(Exp(1)) = 2332/4453 = 0.52369;
  J(Exp(9/10)) - J(Exp(1)) = -761111595/7705213313411 = -9.88e-5; Exp(11/10) is higher by 1.24e-4.

## First-time viewer review

- "Conjugate" and "prescription" are named only after the square-and-rescale picture.
- "Reversible" is shown as equal two-way traffic before it is named.
- The theorem's finiteness condition is said in words ("its conjugate map makes sense, and the average time is finite").
- Laplace-transform injectivity is reduced to "the success curve is a fingerprint of the timer".
- The finite-chain map is a starting-room distribution, said explicitly.
