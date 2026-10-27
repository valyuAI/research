# Video brief: a chemical thermostat that is also a switch needs three dimensions

Audience: a bright 16-year-old who has just finished GCSE maths or physics (or chemistry). Target length: 6 to 8 minutes.

## 1. The question in plain words

Cells contain chemical reaction networks: molecules meet, react and turn into other molecules. Two behaviours matter a lot.

- **Robustness (ACR, "absolute concentration robustness").** One chemical has the *same* concentration at every positive resting state, even across different compatible totals. This is a statement about resting states; it does not guarantee that every trajectory settles. It resembles a thermostat at equilibrium.
- **Switching (multistability).** Within one stoichiometric class, the system has two *different* stable resting states, like a light switch with two positions. When conservation laws exist, the class fixes their totals; our full-dimensional example has no such conserved total.

Can one small network be both a thermostat and a switch? In 2024 Kaihnsa, Nguyen and Shiu found the smallest networks that combine robustness with merely having two resting states, and conjectured that combining robustness with two *stable* resting states needs a strictly bigger network in every one of four size measures: number of chemicals (species), number of independent directions of change (dimension), number of reactant combinations, and number of combinations overall (complexes).

We show: the dimension really must go up (from 2 to 3) and the number of complexes really must go up (from 5 to 6), and both new minima are achieved. But the number of chemicals does not go up: three chemicals are enough. So the conjecture is right in two respects and wrong in one (the fourth, reactant combinations, is only partly settled).

## 2. Why anyone cares

- Biologists want circuits that are both precise (a robust output level) and decisive (a switch, for example in cell-fate decisions). Knowing the smallest possible circuit tells you what nature, or a synthetic biologist, must at least build.
- "Smallest network that can do X" questions are a whole research programme (smallest bistable network, smallest oscillator). This one was explicitly posed in a 2024 journal paper.
- The proof shows a geometric reason why a flat (two-dimensional) world is too cramped for a robust switch.

## 3. The smallest concrete example (star of the video)

Three chemicals A, B, C. Arrows are reactions; the number in brackets is how fast each runs (the rate constant).

```text
C -> A+C [1]        A+C -> C [1]        A -> A+C [6]
B -> 2B [11]        2B -> B [1]
C -> B+C [6]        B+C -> C [6]        B+C -> B [1]
```

Mass-action rule ("rate = rate constant times the product of the concentrations of what goes in") gives, with a, b, c the amounts of A, B, C:

```text
da/dt = c(1 - a)
db/dt = 11b - b^2 - 6bc + 6c
dc/dt = 6a - bc
```

- **Thermostat:** da/dt = c(1 - a). With c > 0, A stops changing only when a = 1. So at rest, a = 1 always.
- **Resting states:** put a = 1. Then dc/dt = 0 gives c = 6/b. Substitute: b x (db/dt) = -(b - 2)(b - 3)(b - 6). Three resting states: (a, b, c) = (1, 2, 3), (1, 3, 2), (1, 6, 1).
- **Stability:** (1, 2, 3) and (1, 6, 1) are stable; (1, 3, 2) is a tipping point (a saddle).

Simulated trajectories to animate (time t, values (a, b, c)):

| start | t = 0.5 | t = 2 | t = 10 | t = 60 |
|---|---|---|---|---|
| (3, 1, 1) | (1.37, 1.57, 4.43) | (1.00, 1.67, 3.85) | (1.00, 1.98, 3.04) | (1, 2, 3) |
| (0.2, 5, 0.5) | (0.31, 9.79, 0.19) | (0.52, 9.35, 0.32) | (1.00, 6.07, 0.99) | (1, 6, 1) |
| (1, 2.5, 2.4) | | (1.00, 2.32, 2.55) | (1.00, 2.03, 2.94) | (1, 2, 3) |
| (1, 3.5, 1.7) | | (1.00, 4.17, 1.47) | (1.00, 6.00, 1.00) | (1, 6, 1) |

Show a in every case heading to 1 (thermostat) while (b, c) ends at either (2, 3) or (6, 1) (switch). The last two rows start on either side of the tipping point (1, 3, 2).

On screen, the one-variable picture: the curve y = -(b - 2)(b - 3)(b - 6)/b for b > 0, with arrows on the b-axis: right-pointing on (0, 2), left on (2, 3), right on (3, 6), left beyond 6. Stable dots at 2 and 6, hollow dot at 3. (This is the sign pattern along the line of possible resting states, not the full 3D motion; say so.)

This network has 6 complexes (A, C, A+C, B, 2B, B+C), the proven minimum.

## 4. Prerequisite ideas, in order

1. Concentration as a number that changes in time; a rate of change dx/dt; "at rest" means dx/dt = 0.
2. Mass-action kinetics with one worked reaction: A + B -> 2B at rate 2 contributes -2ab to da/dt and +2ab to db/dt.
3. Stable versus unstable rest points: ball in a valley versus ball on a hilltop. A saddle: valley in one direction, hill in another (a mountain pass).
4. Conservation laws and "dimension": in A + B -> 2C -> 2B, C -> A the total a + b + c never changes, so the motion stays on a flat sheet (a plane): dimension 2. In the star example nothing is conserved, so it moves freely in 3D: dimension 3.
5. For two directions, the "determinant" of the local stretching (Jacobian) tells you: negative determinant means saddle (a guaranteed unstable direction).

## 5. The key insight (dimension two is impossible) in five visual steps

Use the Kaihnsa-Nguyen-Shiu network A + B -> 2C, 2C -> 2B, C -> A (all rates 1) as the warm-up: total a + b + c = T is fixed, C is always 1/2 at rest, and with T = 2 the two resting states are (a, b, c) = (1, 1/2, 1/2) and (1/2, 1, 1/2). The first is a saddle (eigenvalues on the sheet about 0.109 and -4.609), the second is stable (about -0.114 and -4.386). The theorem says this is unavoidable in two dimensions.

1. **The sheet and the line.** The system moves on a flat sheet (2D). The thermostat says every rest point lies on the line "a = alpha" across the sheet. Draw the sheet with a vertical line L.
2. **At most two rest points, alternating.** Along L the rest points are roots of a quadratic (because every reaction has at most two molecules going in, the formulas are at most quadratic). A quadratic has at most two roots, and its slope has opposite signs at them: draw a downward parabola crossing zero at p and p'.
3. **The determinant splits into two factors.** At a rest point, determinant = -(cross factor l) x (slope of the parabola). The slope flips sign between p and p'. For both to be stable, the cross factor l must also flip, so the line where l = 0 (draw it, a slanted line Pi) must cross L between p and p'.
4. **The thermostat forbids rest points on Pi off L.** Off the line L, a rest point would need both l = 0 and one more quantity f1 = 0. The thermostat says no rest points off L, so f1 keeps one sign all along Pi. Colour Pi in a single colour, say red for "f1 > 0".
5. **Chemistry forces bending the wrong way.** For bimolecular reactions, f1, as a function of a alone, is an upside-down parabola that starts non-negative at a = 0 (a chemical cannot be destroyed if it is absent). Once it goes negative it stays negative. Follow a horizontal path from just outside p (where f1 < 0) across to Pi: the bending rule forces f1 < 0 on Pi too, contradicting the single red colour. Each sign case ends in such a clash. Conclusion: in 2D, one of the two rest points always has a real unstable direction.

Then: dimension 3 is enough (star example), and a separate counting argument with Feinberg's 1987 Deficiency One Theorem shows 5 complexes is too few, so 6 is exact.

## 6. Exact figures and objects to show

- Table:

| size measure | robust + 2 rest points (2024) | robust + switch (now) |
|---|---|---|
| dimension | 2 | 3, exact |
| complexes | 5 | 6, exact |
| species | 3 | 3, exact (conjecture false here) |
| reactant complexes | 3 | between 4 and 6 (open) |

- The star network as a graph: nodes are the 6 complexes, arrows labelled with rates.
- Formulas: da/dt = c(1 - a); b x db/dt = -(b - 2)(b - 3)(b - 6) along a = 1 and c = 6/b; rest points (1,2,3), (1,3,2), (1,6,1).
- Characteristic polynomials (optional, for the stability check): lambda^3 + 16 lambda^2 + 43 lambda + 12 at (1,2,3); lambda^3 + 12 lambda^2 + 17 lambda - 6 at (1,3,2) (negative last coefficient means a positive eigenvalue); (lambda + 1)^2 (lambda + 12) at (1,6,1).
- Determinant formula: det = -l(x) x gamma'(s).
- The second example (6 reactions): A+B -> 2B [2], B -> 0 [2], 0 -> A+C [60], 2C -> A+C [1], A+C -> 2C [13], B+C -> B [2]; db/dt = 2b(a - 1); at a = 1, dc/dt = -(c - 3)(c - 4)(c - 5); rest points (1,15,3) stable, (1,12,4) saddle, (1,10,5) stable.

## 7. Proved versus computed versus open

- Proved by hand: no 2D robust switch (any network of this kind); dimension at least 3; at least 6 complexes; at least 4 reactant complexes (5 when there are only three chemicals).
- Checked by exact computer arithmetic (two independent programs): both example networks, their rest points and stability; a finite enumeration used to show 4 reactant complexes would need at least 5 chemicals.
- Open: whether 4 or 5 reactant complexes can work, and the minimum number of reactions (our examples use 6 and 8).

## 8. Misconceptions to avoid

- "Thermostat" means one chemical is fixed at every resting state, not that it is constant at all times. It moves during the transient (a goes from 3 down to 1).
- The species bound failing is partly cheap: gluing a two-chemical switch to a separate chemical Z made by 0 <-> Z also gives 3 species. Say this honestly; our examples are genuinely coupled.
- Two rest points is not the same as a switch: the 2024 minimal networks have two rest points but one is always a saddle.
- The theorem is about networks where at most two molecules go in and come out of each reaction (bimolecular). It says nothing about bigger reactions.
- Do not show the 1D arrow picture as the actual 3D motion; it is the sign pattern along the line of rest states.


## Final production scope

- ACR describes all positive steady states, not convergence of every trajectory. Stability is within a stoichiometric class, not strict negativity of the full Jacobian when conservation laws produce zero eigenvalues.
- Both implementations now use exact arithmetic for the example stability claims. The independent checker uses cubic Routh-Hurwitz inequalities and a negative constant coefficient to certify a positive real eigenvalue; no rounded eigenvalue sign is used.
- Lean checks the example vector fields, exact positive steady-state lists and ACR. It does not check stability, the dimension-two theorem or the minimal-complex theorem.
- The optional Tang-Zhang screen finished with no sampled bistable ACR example under its restricted certificate search. It is not an exhaustive exclusion or a priority proof.
