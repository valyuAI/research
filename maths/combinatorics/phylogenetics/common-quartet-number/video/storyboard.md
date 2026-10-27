# Four leaves that agree

Audience: GCSE graduate. Exact narration is in narration.json; illustrations introduce definitions before the general formulas. Cedar synthetic voice. The actual witness is read and checked from the retained Newick input; no speculative 23-leaf witness is used.

| Scene / clips | Visual and narration | What the viewer learns / source |
|---|---|---|
| FourLeaves / q01-q05 | Draw an H quartet, change its pairings, attach then remove a fifth tip. | Unrooted binary trees, restriction and common quartet; paper introduction. |
| Witness / q06-q11 | Draw the actual 13-leaf tree, move labels through the two cyclic relabellings, display the exact splits for 1,4,7,13; summarize 715 checks. | One explicit family proves 13 insufficient. Data in witness-data.json; distance and edge checks agree. |
| Separating / q12-q15 | Highlight the cut edge and the two sides; retain 3 blue and 4 teal leaves; build the exhaustive count. | Why separated sets preserve pairings and what the 14-leaf finite check establishes. |
| GridArgument / q16-q20 | Form an illustrative 2x2 count grid; keep a diagonal; animate every arrangement of two failed diagonal cells. | A row or column contradiction guarantees two leaves per side in all three trees. |
| Budget / q21-q26 | Shrink separated bars; calculate min(512,512,2048); show cut counts 7,9,11,21 and diagonal budgets 98,99. | Concrete potential-step mechanism; relabel smaller X and larger Y at every step; normalized cut fractions, crossing of x squared and (1-x)/3, and precise Lean scope. The three added beats q25a-q25c explain the accepted sharp factor. |
| ManyTrees / q27-q30 | Iterate budget inequality, derive threshold, distinguish general bound from sharper small cases, show 23<=h(4)<=28 and prior lower bound. | General guarantee is not an exact threshold; Snir-Yuster attribution. |
| Evidence / q31-q33 | Return to quartet; recap, high correctness / bounded priority, unresolved searches, end card. | What is proved, what was checked and what remains open. |

Comprehension review: the word quartet follows the H picture; the threshold is motivated by a counterexample and a universal argument; the new potential is introduced as a three-number minimum before use. The number 135 counts unlabelled shapes, not all labelled trees. Grid examples are explicit teaching illustrations. The exhaustive checker animation summarizes actual saved verification, not an on-screen replay of every operation. The potential animation shows the two-case crossing but leaves the checks of all three minimum terms and the full DP recursion in the paper; no audience test is claimed.

Accepted production scope (26 October 2026): c=(7-sqrt(13))/18=t^2, t=(sqrt(13)-1)/6, beta=1/t=(1+sqrt(13))/2. The normalized ratio may be capped at 2 only for proving the worst-case inequality; actual leaf counts are not changed to irrational sizes. General upper thresholds 4,7,16,37,85,195 are distinguished from exact h(3)=14 and certified h(4)<=28. The curve crossing is an algebraic guide, not a simulation or a finite-leaf equality example. Optimality is only for this real inequality; the updated Lean file checks the sharp inequality and its equality example. The tree model, iteration, DP/SAT and fourteen-leaf theorem remain outside the formalisation.
