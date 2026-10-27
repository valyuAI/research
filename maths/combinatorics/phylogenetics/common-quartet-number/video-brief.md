# Video brief: three family trees that never agree on four species

## The question in plain words

Biologists draw evolutionary trees: species sit at the tips, and the branching shows who is most closely related. Different genes often give different trees for the same species. Pick any four species. Each tree answers one simple question about them: which two pairs are separated by the middle edge of the induced four-tip tree? There are only three possible answers.

If you have three different trees on the same species, must there always be some group of four species on which all three trees give the same answer? It depends on how many species there are. The question is: what is the smallest number of species that forces agreement? We show the answer is 14.

## Why anyone cares

- Agreement between trees is how biologists find the parts of evolutionary history that different data sources support. The four-species groups ("quartets") are the smallest building blocks: a tree is completely determined by its quartets.
- This is a "Ramsey-type" question: in a big enough structure, some order is unavoidable. Here the structure is a set of trees and the order is a quartet they all agree on.
- Two trees on 6 or more species always agree on some quartet (known since 1986). For three trees the answer was only known to lie between 11 and 14, after two 2026 papers asked for it.

## The smallest concrete example

Four species a, b, c, d. A tree (unrooted, every branch point has exactly three branches) on these four looks like an H: two pairs joined by a middle edge. The three possible H shapes are

- ab|cd (a with b, c with d),
- ac|bd,
- ad|bc.

Show all three H's side by side. With exactly four species, three trees can choose the three different H's and never agree. With five species, two trees can still avoid agreeing on every one of the 5 quartets. With six species two trees can no longer avoid it.

## Prerequisite ideas, in order

1. An unrooted binary tree: tips labelled 1 to n, internal points have three branches. Number of tips n, number of internal points n - 2.
2. Restricting a tree to four tips: erase everything except the paths between those four tips. What remains is always one of the three H's.
3. Counting: a set of n tips has n(n-1)(n-2)(n-3)/24 groups of four. For 13 tips that is 715; for 14 tips, 1001.
4. Relabelling: moving the labels around (a permutation) keeps the tree's shape but changes which species sit where.
5. Separating edges: cutting one edge of a tree splits the tips into two sides. Any two tips on one side and two tips on the other side form a quartet that the tree resolves as "these two | those two".
6. A balanced edge: every such tree has an edge with at least a third of the tips on each side.

## The key insight in visual steps

### Part 1: why 13 species are not enough (the construction)

1. Draw one tree T on 13 tips (Figure: the left panel of the paper's figure). Colour the tips in five groups: {1,2,3} red, {4,5,6} blue, {7,8,9} green, {10,11,12} orange, {13} grey.
2. Apply the relabelling sigma: inside each coloured group, 1 becomes 2, 2 becomes 3, 3 becomes 1 (and similarly 4 to 5 to 6 to 4, and so on); 13 stays. The drawing keeps exactly the same shape; only the numbers rotate. That is the second tree. Do it again to get the third tree. Animate the labels sliding around their colour group.
3. Pick a random group of four tips, for example {1, 4, 7, 13}. Highlight their paths in each of the three trees and shrink to the H. The exact splits are 4,7 | 1,13 in T, then 1,4 | 7,13 in each of the other two trees. Show that the three H's are not all the same; they need not all be different.
4. Fast montage: run through all 715 groups of four with a counter. Each one lights up "not all equal". The counter ends at 715 / 715.

### Part 2: why 14 species are always enough (the proof idea)

1. Start with the first tree on 14 tips and cut its balanced edge: at least 5 tips on each side (14/3 is more than 4). Colour one side purple and the other yellow.
2. Bring in the second tree, with the colours carried over. A computer check of every possible case (all 135 tree shapes on 14 tips, times every way of choosing 5, 6 or 7 purple tips: 1,138,995 cases, about a minute on a laptop) shows that some edge of the second tree has at least 3 purple tips on one side and at least 4 yellow tips on the other (or 4 purple and 3 yellow). Keep those 3 + 4 tips: call them X and Y. They are separated by one edge in each of the first two trees. Show a scissors mark on one edge of each tree. On 13 tips this fails (891 bad cases with 5 purple tips), which is exactly why 13 is not enough.
3. Bring in the third tree. Look only at the 7 tips of X and Y in it. It has a balanced edge with at least 3 of these 7 tips on each side (call the sides W and Z).
4. Draw a 2-by-2 grid: rows X and Y, columns W and Z. The four cells are A = X and Z, B = X and W, C = Y and Z, D = Y and W. Each row has at least 3 tips and each column has at least 3 tips.
5. Simple counting: either A and D both have at least 2 tips, or B and C both do. (If not, some row or column would have at most 2 tips.) Two tips from A and two from D are separated in all three trees, so all three trees resolve them the same way. That is the common quartet.

### Part 3: many trees (a shrinking budget)

1. Start with one tree on n tips and its balanced edge: two sets X and Y, each with at least n/3 tips. Draw them as a purple bar and a yellow bar.
2. Bring in the next tree. Look only at the bigger set (say yellow, Y) and find an edge with at least a third of the yellow tips on each side (the same balanced-edge argument, counting only yellow tips).
3. The cut splits the bars into the 2-by-2 grid A, B, C, D again. Keep the diagonal pair (A, D) or (B, C) that scores best on the "budget" Psi = min(|X| x |Y|, 2|X|^2, 2|Y|^2). Show the budget as a number shrinking on screen.
4. Key fact (Lemma 2.6): every step keeps at least c = (7 - sqrt(13))/18, about 18.858 percent, of the budget. This is proved exactly, not estimated from simulations. Orient the cut so x+y <= 1, and put t = (sqrt(13)-1)/6, about 0.4343. If x >= t, the first diagonal keeps at least c of the budget; otherwise 1-x > 1-t = 3c, so the other diagonal works. Use the paper for the three terms in each minimum. The unchanged concrete example is |X| = 16, |Y| = 32, budget 512; split Y into 11 and 21 and X into 7 and 9. The two diagonal budgets are 98 and 99. Keep 99, above 512c, approximately 96.553. Relabel the smaller retained set X and the larger Y before repeating.
5. Start with budget at least 2n^2/9. After k trees the budget is above 2 when n > 3 x beta^(k-1), where beta = (1+sqrt(13))/2, about 2.3028, and a budget above 2 forces both sets to have at least 2 tips: a common quartet.
6. Table on screen: k = 1, 2, 3, 4, 5, 6 gives n = 4, 7, 16, 37, 85, 195.
7. For small k a computer can certify stronger strategies: work out, for every pair of sizes, whether every possible next tree leaves a pair that is still winning (a short recursion over how many purple and yellow tips sit below each edge). This gives 4, 7, 14, 28, 61, 125 for k = 1 to 6. The 14 matches the true answer for three trees; for four trees the answer is now known to be between 23 and 28.

### Part 4: how big must n be for many trees? (a sandwich)

1. Lower side: caterpillars (trees that are a single spine with one tip hanging off each spine point) are read left to right; a caterpillar splits four tips into "the first two" and "the last two". Show 3 caterpillars on 9 tips that never agree: 1 2 3 4 5 6 7 8 9, then 1 8 3 6 5 4 7 2 9, then 1 2 7 6 5 4 3 8 9. Picture the 9 tips as 4 mirror pairs {1,9}, {2,8}, {3,7}, {4,6} around the centre 5; each caterpillar decides, pair by pair, which partner goes on the left. The rule uses binary digits of the pair number, so k caterpillars handle 2^(k-1) pairs: 2^k + 1 tips with no common quartet. Snir and Yuster stated this; the note writes out the construction and proof.
2. Upper side: the budget argument of Part 3 gives about 3 x 2.31^(k-1).
3. Sandwich on screen: 2^k + 2 <= h(k) <= floor(3 x beta^(k-1)) + 1, with beta = (1+sqrt(13))/2, approximately 2.3028. The previously published 2026 upper bound was a tower of exponentials.
4. Small values bar chart: k = 3: exactly 14; k = 4: between 23 and 28; k = 5: between 34 and 61; k = 6: between 66 and 125.

## Exact figures, formulas and objects to show

- The three H shapes on four tips: ab|cd, ac|bd, ad|bc.
- The tree T in Newick form: (1,(3,6),(((7,9),(4,(5,12))),((10,11),(2,(8,13))))).
- The permutation sigma = (1 2 3)(4 5 6)(7 8 9)(10 11 12), 13 fixed.
- The numbers: 715 quartets on 13 tips; 1001 on 14 tips; 135 different tree shapes on 14 tips.
- The bounds before: 11 <= h(3) <= 14. After: h(3) = 14.
- The 14-tip check: 135 shapes x (2002 + 3003 + 3432) colourings = 1,138,995 cases, 0 failures; on 13 tips with 5 purple: 891 failures.
- Four trees: the prior general upper bound was a tower; the new 22-tip example and upper bound give 23 <= h(4) <= 28.
- The counting grid A, B, C, D with row and column sizes at least 3.
- The three 9-tip caterpillar orders above and the formula 2^k + 2 <= h(k).
- The budget Psi(a, d) = min(ad, 2a^2, 2d^2), the retained factor c = (7-sqrt(13))/18 per tree, and h(k) <= floor(3 x beta^(k-1)) + 1.

## Proved versus computed versus open

- Proved by hand: the balanced-edge lemma (also with weights), the separation lemma, the counting step, the budget lemma (factor c = (7-sqrt(13))/18 per tree) and the caterpillar construction.
- Checked by computer: the 13-tip example (a direct check anyone can rerun in seconds); the 14-tip colouring statement (every case enumerated, about a minute); a weaker two-tree statement also proved by 135 SAT problems with independently checked proof files; the bounds 28, 61, 125 for four, five and six trees (a short recursion, computed by two separately written programs).
- Already known: h(2) = 6 (Bandelt and Dress, 1986); h(3) <= 14 also follows from a 2026 theorem of Snir and Yuster.
- Also proved here: for k trees, h(k) is at most floor(3 x beta^(k-1)) + 1, beta = (1+sqrt(13))/2 (repeat a balanced-edge and grid step once per tree and track the budget Psi), and at least 2^k + 2 (the caterpillars, stated by Snir and Yuster). Before this, the best upper bound was a tower of exponentials.
- Open: the exact value for four trees (between 23 and 28); the exact growth rate of h(k), somewhere between 2^k and 2.3028^k. Computer experiments suggest that pushing one separated pair through the trees cannot beat about 2.12^k.

## Common misconceptions to avoid

- "Agreeing on a quartet" does not mean the trees are similar overall. Our three trees have no quartet common to all three; pairs of trees can still agree on many quartets. Trees on 14 tips can be very different and still be forced to share one.
- The trees are unrooted. Do not draw a root at the top; the H picture for a quartet has no root.
- The relabelling trick does not make the three trees "the same tree": the shape is the same, but which species sit at which tips differs, and that is all that matters for quartets.
- The computer check is not a simulation or a random sample. It covers every tree shape and every colouring, and it is short enough to rerun.
- The upper bound for 14 tips was already claimed via a 2026 theorem whose small cases were only sketched; what is new for three trees is the 13-tip example and an exact, checkable version of the upper-bound argument.
- 14 is a threshold: for 13 species agreement can be avoided; for 14 or more species it cannot.

## Final production handoff and claim limits

- The general threshold is an upper bound, not an exact value: for two trees the table gives 7 although the true answer is 6. The exact small-k claim here is h(3)=14.
- Lean now checks the exact sharp c budget inequality and its real equality example. Do not label the whole tree theorem or the SAT/DP computation as formally verified.
- The 22-tip family in `verification/families/quad22_k4.nwk` has zero common quartets across all 7315 four-sets. Its cyclic label permutation is (1 2 3 4)(5 6 7 8)(9 10 11 12)(13 14 15 16)(17 18 19 20)(21 22).
- Three 23-tip searches are unresolved; do not animate an alleged 23-tip witness or claim h(4)>=24.
- Use `triple13.pdf`, `plot_triple.py`, the Newick witnesses and the exact 16/32 budget example above as editable animation inputs. The final review response and replay evidence are in `readiness.md`.
- No video is produced in this research task; this brief is the handoff for a separately narrated production.

## Accepted sharper scope (26 October 2026)

The coordinator accepted the exact c lemma after max review `DR-017` found no gap in the proof or iteration. The optimum is for this real-variable inequality only; it is not the optimal growth base of h(k) or of every possible tree strategy. The equality example uses an irrational fraction and must not be drawn as an exact finite leaf count. For the video use the integer 16/32 example and explain the real bound as a guaranteed budget. The paper and this brief supersede the archived 3/16 draft.
