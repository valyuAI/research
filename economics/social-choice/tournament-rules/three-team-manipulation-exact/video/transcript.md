# How much can three teams gain by fixing their matches?

## Matches / s01

Five teams. Everyone plays everyone. Could three of them improve their combined chance of taking the trophy by fixing just their own matches? Even the best fair rule must sometimes let them gain forty percentage points.

## Matches / s02

Start with one result. An arrow from A to B means A beat B. Each pair gets exactly one arrow. The complete picture records results, rather than the order in which games were played.

## Matches / s03

A rule turns that picture into a champion. It may use a lottery. Here each team gets one fifth of the chance. Five equal pieces make one whole probability, or a hundred percent.

## Matches / s04

We impose one clear fairness requirement. If somebody beats everybody, that team must win the trophy for certain. This is called Condorcet consistency. When nobody is unbeaten, the rule has more freedom.

## Cheat / s05

Return to the circle. Every team beats the next two clockwise and loses to the other two. Each has two wins, so there is no unbeaten team to settle the choice for us.

## Cheat / s06

Now highlight A, D and E. Together they currently hold three fifths of the lottery. They are allowed to change only matches inside this group. Matches against B and C stay exactly as they were.

## Cheat / s07

A already beat B and C. If D and E now throw their games against A, those two arrows reverse. Watch A become unbeaten. Fairness forces the rule to give A the entire trophy chance.

## Cheat / s08

The group goes from three fifths to one. Subtract the starting chance and the gain is two fifths. That means forty percentage points, measured for the group together, rather than for every member separately.

## Unavoidable / s09

Could an uneven lottery avoid this? Perhaps give A almost nothing. The difficulty is that every team has its own version of this trick: join with the two teams that beat you, and become unbeaten.

## Unavoidable / s10

Write those five groups underneath the teams. A appears in three groups. So does B, and so does every other team. Whatever probabilities the rule chooses, each probability is counted exactly three times.

## Unavoidable / s11

The team probabilities add to one, so the five starting group chances add to three. Each group can separately cheat its way to chance one. Their five possible gains therefore add to five minus three, which is two.

## Unavoidable / s12

Five numbers adding to two cannot all be smaller than two fifths. At least one group gains that much. This is the known lower-bound argument from Schneider, Schvartzman and Weinberg. No choice of a fair rule escapes it.

## Search / s13

But a lower bound is only half the answer. We also need a rule that never allows a bigger gain. One nasty tournament anywhere could ruin the guarantee. So we must control the worst cheat across every possible result.

## Search / s14

First remove duplicate work. Rename the five teams without changing any arrows. The shape is the same. We can average over names without worsening the guarantee, so it is enough to store one lottery per shape.

## Search / s15

Five teams have twelve different shapes. Here are the twelve representatives in the actual small certificate. The rule is a lookup table: recognise the shape, read its fractions, then transfer them back to the original team names.

## Search / s16

Take this real row. The five chances are two fifths, three tenths, one fifth, one tenth, and zero. They add to one. The table contains different rows because different match results need different lotteries.

## Constraints / s17

For every allowed cheat, compare two rows. Add the cheating group's chances after the change, subtract its chances before, and require the answer to be at most our proposed limit. This creates one inequality.

## Constraints / s18

Do that for every group of two or three, and every way to change its internal matches. Groups of two matter too. The guarantee covers groups of at most three; checking only groups of exactly three would leave a gap.

## Constraints / s19

Imagine each inequality cutting away forbidden choices of probabilities. A linear program searches the choices that remain. We ask whether all constraints can fit at two fifths, the limit already forced by the circle.

## Constraints / s20

The numerical solver suggests yes. But a decimal close to two fifths is not an exact guarantee. A tiny rounding error could put a constraint on the wrong side. The final rule must be a table of exact fractions.

## Certificate / s21

The discovery process rounds to fractions, repairs the constraints that must be equalities, and checks everything again. In the plain fair-rule certificates, only the known five-team circle configurations reach the worst-case limit.

## Certificate / s22

A separately written checker reads the resulting table. It verifies that every lottery sums to one, that unbeaten teams win, and that every permitted manipulation stays within the bound. It calculates with fractions throughout.

## Certificate / s23

At eight teams there are six thousand eight hundred and eighty shapes. The checker covers two million, eight hundred and eighty-nine thousand, six hundred manipulations. Its exact largest gain is two fifths. These are recorded completed checks.

## Certificate / s24

Why does checking shapes cover named teams? The lottery respects every symmetry of its shape. Relabelling therefore gives a consistent answer. For up to six teams, a second checker also expands all labelled tournaments and agrees.

## GoodRules / s25

The same optimal values can satisfy two extra requirements. First, winning one more match never lowers that team's chance. This is monotonicity. We check it separately; it does not follow just from being hard to manipulate.

## GoodRules / s26

Second, winners come only from the top cycle. Picture a group whose members can reach every team by chains of wins. Teams outside that group get zero chance. Here a three-team cycle beats two outsiders.

## GoodRules / s27

The eight-team certificate with both extra requirements passes the same manipulation checks, plus the extra tests. Across this package, fourteen certificates pass. The recovered eight-team result is an exact certificate, not an unfinished numerical solve.

## Scope / s28

Now put the two halves together. The old argument says no rule can beat two fifths. The new tables achieve two fifths for five, six, seven and eight teams. Matching lower and upper bounds give the exact optimum.

## Scope / s29

With three or four teams, the optimum for groups of at most three is one third. A separate seven-team certificate handles groups of at most four and reaches three sevenths. These are different finite cases, not one universal rule.

## Scope / s30

For nine or more teams, this work gives no matching upper bound. A table for eight teams does not tell us how to extend it. If three-team collusion ever needs more than two fifths, the first failure needs at least nine teams.

## Scope / s31

Remember three ideas. Arrows describe results. A five-team circle forces an unavoidable cheating reward. Exact fraction tables meet that reward through eight teams. Earlier work already refuted the broader guess for some large groups; the small-group question remains open.

## Scope / s32

The companion paper contains the full definitions, tables and independent checkers. This animation shows the lower-bound mechanism and the certificate logic. It does not replace the complete mathematical and computational proof.
