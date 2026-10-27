# Why four negative eigenvalues permit at most thirty essential dots

## Movement / g01

Put a number on each end of this line. Replace each number by the number at its neighbour. Two numbers simply swap places. This tiny operation will lead to a question about how large a network can be.

## Movement / g02

A graph is a collection of dots joined by lines. Its adjacency table has a one when two dots are joined and a zero otherwise. Multiplying by this table means adding the numbers at each dot's neighbours.

## Movement / g03

Start with one at each end. After the swap, nothing changes. The pattern has been multiplied by positive one. A pattern that only gets scaled is an eigenvector, and the scale factor is its eigenvalue.

## Movement / g04

Now start with one and minus one. The swap reverses the signs. The new pattern is minus one times the old pattern. This gives an eigenvalue of negative one: the direction flips.

## Signs / g05

A graph with n dots has n eigenvalues, counting repeats. Because its adjacency table is symmetric, they are real numbers. We count how many are positive, zero and negative. These three counts are called the inertia.

## Signs / g06

A triangle has eigenvalues two, minus one, minus one. One positive and two negative. A pentagon has three positive and two negative. So the same negative count can coexist with different positive counts.

## Signs / g07

We fix the negative count at four. How many positive values are possible? And how many dots can a network have? Those are different questions, because some dots can add zero eigenvalues without adding positive or negative ones.

## Signs / g08

Copy one endpoint of our original edge, giving the copy exactly the same neighbours. Put one on the original, minus one on the copy, and zero in the middle. Every neighbour sum is zero. The copied difference disappears.

## Reduced / g09

Copies leave the positive and negative counts unchanged, though the individual eigenvalues may change. Lonely dots also add only zeros. To ask a finite size question, remove these easy ways of making a graph bigger.

## Reduced / g10

A reduced graph has no lonely dots and no two dots with identical sets of neighbours. Reduced does not mean no zero eigenvalues. Other linear dependencies can still create zeros, and they matter for our size problem.

## Reduced / g11

The answer for four negatives is thirty dots in a reduced graph. Exactly four reduced graphs reach thirty. Each has four positive, twenty-two zero, and four negative eigenvalues. The zeros explain why thirty dots need not mean thirty active directions.

## Reduced / g12

The largest possible positive count is eleven, achieved by two reduced graphs with fifteen dots and no zeros. The numerical bound and these examples were already supplied by earlier work. The classification proves that no other reduced graph attains eleven.

## Cores / g13

How can a finite computation settle all graphs? First keep an induced core with the same positive and negative counts but no zero eigenvalues. Induced means that, among the dots you keep, you retain every original connecting line.

## Cores / g14

The number of dots in a core is its rank. With no zero eigenvalues, its table is nonsingular: an inverse table can undo the calculation. Reduced graphs can be larger than their cores, so we must add zero directions back later.

## Cores / g15

The second ingredient says every nonsingular graph can be built from a smaller one by adding one dot, or sometimes two. Two are essential: our first edge has a nonsingular two-by-two table, while a lone dot has the zero table.

## Cores / g16

Why does the rule cover every case? Jacobi's determinant identity examines the inverse table. Either a nonzero diagonal entry permits one deletion, or a nonzero off-diagonal entry permits two. The paper proves these alternatives leave a nonsingular core.

## Enumeration / g17

For each core, try every possible zero-or-one list of connections to a new dot. A calculation using the inverse tells which sign is added. Written with the determinant and adjugate, its sign is decided using whole numbers.

## Enumeration / g18

Watch a concrete case. Join the new dot to both ends of the edge, making a triangle. The connection list is one, one. The inverse table is the same swap table, so the calculation gives two. Its negative contributes one new negative eigenvalue.

## Enumeration / g19

The program grows every allowed graph, merges copies made by renaming, and discards anything exceeding four negatives. It also tries the required two-dot extensions. This is exhaustive generation guided by a lemma, rather than a random search.

## Enumeration / g20

For exactly four negatives, the number of cores rises and then falls. At fifteen dots, just two remain. At sixteen and seventeen, none remain even when we allow fewer than four negatives. These empty levels are the stopping certificate.

## Termination / g21

Why are two empty levels enough? Suppose there were a first larger core. Remove one or two dots using the lemma. Its parent would have to sit on an earlier level. Starting from two empty levels, neither route can ever restart.

## Termination / g22

The complete census contains forty-five thousand two hundred and forty-two cores with at most four negatives. Two implementations agree. Exact replay checks every recorded graph and its sign counts, and the mathematical extension rule is what establishes completeness.

## Termination / g23

Now reconstruct a larger reduced graph from a core. Each extra dot gets a nonzero binary connection pattern. Its self-calculation must be zero to avoid changing rank. Between two added dots, the corresponding calculation must be either zero or one.

## Termination / g24

Compatible patterns can coexist. An exact search finds the largest mutually compatible collection for every core. This is the method of Akbari, Cameron and Khosrovshahi. Applying it across all relevant ranks supplies the missing size bound.

## Thirty / g25

Here are the maximum reduced sizes for ranks five through fifteen. The peak is thirty, at rank eight. Above rank eight, the maxima fall below thirty. Excluding those higher ranks is the central new step in the size theorem.

## Thirty / g26

Thirty is actually attainable. Start with one edge. Copy every dot and its connection pattern. Join a new dot to all copies, then attach one more dot to that new dot. The old two dots become six.

## Thirty / g27

Repeat the same operation: six becomes fourteen, then thirty. A second version adds connections from the final new dot to the original dots. Using the variant first and the ordinary version afterwards gives the four maximum graphs.

## Thirty / g28

Those four rank-eight classes were already known to Akbari, Cameron and Khosrovshahi in two thousand and four. This work proves that allowing other ranks with four negative eigenvalues does not produce a bigger graph or another thirty-dot class.

## Extremal / g29

For the eleven-positive record, the first graph is called W five. Start with five mutually connected point dots. Add a dot for each of their ten pairs. Join each pair dot to its two points, and join pair dots when their pairs are disjoint.

## Extremal / g30

The other graph, X, begins with a three-by-three grid. Join points sharing a row or column. Add six dots for the wrap-around diagonals in the two directions. Join each to its three points, and join parallel line dots together.

## Extremal / g31

Each graph has fifteen eigenvalues: eleven positive and four negative. Their degree patterns differ, so they cannot be the same graph with renamed dots. The completed census and reconstruction checks show that these are the only reduced graphs attaining eleven positives.

## Extremal / g32

Charles, Farber, Johnson and Kennedy-Shaffer supplied both examples and the numerical bound underlying this result in twenty thirteen. The later inertia identity of Elphick and colleagues makes the implication explicit. The retained increment here is uniqueness, alongside independent verification.

## Scope / g33

Keep the two records separate. Thirty is the maximum number of dots after copies and isolated dots are removed. Eleven is the maximum positive count, with four negatives. The size champions and positive-count champions are different graphs.

## Scope / g34

The proof combines written linear-algebra arguments with complete exact computations. It is not a proof-assistant formalisation. Integer and rational tests make the decisions; decimal eigenvalue pictures are only illustrations. Both the lemmas and the computation are needed.

## Scope / g35

For five negative eigenvalues, the corresponding maximum-size question remains open. A pattern in the small cases is a clue, not a proof. Failed searches through selected examples cannot replace the exhaustive generation and stopping argument used here.

## Scope / g36

You have seen the whole route: moving numbers gives eigenvalues; removing zero directions gives cores; complete generation and compatible reconstruction give the bound. The paper and verification files contain the full arguments, exact census and explicit extremal graphs.
