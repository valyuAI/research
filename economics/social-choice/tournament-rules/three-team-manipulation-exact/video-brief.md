# Video brief: how much can three teams gain by fixing their own matches?

## The question in plain words

In a round robin every pair of teams plays once. A *tournament rule* looks at all the results and picks a champion, possibly at random ("team A wins with probability 0.3, team B with 0.25, ..."). We want two things.

1. Fairness: if one team beat everybody, it must be the champion. (This is called Condorcet consistency.)
2. Little reward for cheating: a small group of teams should not gain much by secretly fixing the matches *among themselves*, for example one member throwing a game to another.

The cheating reward is measured as the increase in the group's *combined* chance of producing the champion. For groups of three teams, the best possible rule has some unavoidable reward. Researchers proved in 2017 that it is at least 2/5 (40 percentage points) and conjectured that 2/5 is exactly right. In 2020 others showed the analogous guess is wrong for huge groups (hundreds of teams), and asked when it first goes wrong. Our bounded literature audit found no earlier exact computation of the values certified here.

We computed the exact answer for every tournament with up to 8 teams: it is exactly 2/5 every time from 5 teams on (and 1/3 for 3 or 4 teams). So if the conjecture is false for groups of three, the smallest counterexample needs at least 9 teams.

## Why anyone cares

Competition designers want rules where fixing the results within a small group improves that group's chance as little as possible. The number 2/5 is the price you cannot avoid when groups of three collude.

## Smallest concrete example (why at least 2/5)

Five teams A, B, C, D, E sit on a circle. Each beats the next two clockwise: A beats B and C, B beats C and D, C beats D and E, D beats E and A, E beats A and B. Every team has 2 wins and 2 losses, so nobody is unbeaten.

- A loses only to D and E. If D and E throw their games against A, A becomes unbeaten, so any fair rule must now give A probability 1. The group {A, D, E} jumps to combined probability 1.
- The same trick works for every team with its two "beaters": the five groups are {A,D,E}, {B,E,A}, {C,A,B}, {D,B,C}, {E,C,D}.
- Each team appears in exactly 3 of the 5 groups. So, before any cheating, the five groups' combined probabilities add up to 3 x (total probability 1) = 3.
- After cheating each group has 1, so the five gains add up to 5 - 3 = 2. Five gains adding to 2 means at least one gain is 2/5.

Concrete numbers for the rule we found: in this circle tournament it gives every team 1/5. Each group holds 3/5 and can reach 1, gaining exactly 2/5. The rule is built so that no other cheat anywhere gains more.

## Prerequisite ideas, in order

1. A tournament as dots and arrows (arrow from winner to loser).
2. A random champion: probabilities on the teams that add to 1.
3. A cheat: a group can flip only arrows between its own members. Show the before/after picture.
4. A guarantee: we want the rule whose *worst* cheat is as small as possible ("minimise the maximum").
5. Symmetry: renaming the teams should not change the rule, so we only need one probability list per *shape* of tournament. Show two drawings that are the same shape with different labels.
6. Linear programming: many inequalities of the form "probability after minus probability before is at most alpha", and a solver that finds the smallest alpha that can satisfy all of them.

## Key insight of the computation (5 visual steps)

1. **Count shapes.** With 5 teams there are 12 shapes of tournament; with 8 teams, 6,880. Show a grid of the 12 five-team shapes.
2. **Write down every cheat.** For each shape, each group of 2 or 3 teams and each way of re-flipping their internal arrows, write one inequality. For 8 teams that is 2,889,600 cheats.
3. **Solve.** The numerical solver suggests a feasible rule at 2/5, the same number the circle forces. Nothing else pushes it higher.
4. **Make it exact.** Computers solve with decimals, but we want a proof. The solver's answer is nudged to exact fractions (like 3/10 and 1/11), and for the plain CC rule the only manipulation inequalities that must sit exactly at 2/5 come from the circle picture: ten for each class of tournaments formed by adding teams that lose to all five circle teams (twenty at n = 8). Everything else has some room, so the rounding does not break anything.
5. **Check every cheat with fractions.** A separate short program, written independently, re-checks every one of the 2,889,600 cheats with exact fractions. The largest gain is exactly 2/5.

## What should appear on screen

- The 5-team circle with arrows; highlight the group {A, D, E}, flip the two arrows D->A and E->A, A turns gold (unbeaten).
- A bar: "before 3/5, after 1, gain 2/5".
- The five overlapping groups as coloured arcs and the sum 3 + gains 2 = 5.
- The formula (k - 1)/(2k - 1) with k = 2 -> 1/3, k = 3 -> 2/5, k = 4 -> 3/7.
- The results table: n = 3, 4 -> 1/3; n = 5, 6, 7, 8 -> 2/5; groups of four with n = 7 -> 3/7.
- Table 2 of the paper (the full five-team rule: 12 shapes, probabilities such as 1/5, 1/3, 2/5, 11/20, 7/19) as a "here is the actual rule" moment.
- A counter ticking up to 2,889,600 checked cheats with "max gain = 2/5".

## Proved vs computed vs open

- Proved before (2017): no fair rule beats 2/5 for groups of three once there are at least 5 teams. Proved before (2020): the general formula fails for some very large groups.
- Proved here, by exact computer-checked certificates: the best value is exactly 2/5 for 5, 6, 7 and 8 teams, 1/3 for 3 and 4 teams, and 3/7 for groups of four with 7 teams. For groups of three the best value is reached even by rules with two extra good habits: a team never loses chances by winning one more match (monotone), and only teams in the 'top cycle' (teams that can reach everyone through chains of wins) can be champion.
- Open: whether 2/5 is achievable for every number of teams. The rules found for different team counts are separate; nothing here carries over to 9 or more teams.

## Misconceptions to avoid

- This does not prove the conjecture for all tournament sizes; it settles the finite cases shown in the table.
- "Gain 2/5" is about the group's combined probability, not one team's.
- The optimal rules are not simple formulas like "pick a random team that is not dominated"; they are tables of fractions found by computer. The interesting fact is how little forces the value: only the circle configuration.
- The 2020 result is about groups of hundreds of teams; it says nothing directly about groups of three.

## Final scope lock

The n = 8 monotone/top-cycle certificate has now passed exact independent replay: 2,889,600 manipulation checks, 192,640 monotonicity checks, maximum gain 2/5. Use the same finite scope throughout narration and captions. Do not present the already-known weak-strategyproofness observation as a finding. No video files were edited in this research pass.
