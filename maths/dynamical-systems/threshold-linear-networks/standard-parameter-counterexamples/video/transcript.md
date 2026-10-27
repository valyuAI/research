# A stable pattern outside the clique prediction

## Rates / c01

Imagine two neurons whose activity settles to a steady pattern. Give the pattern a small nudge. If it returns, the model can hold that pattern like a memory. Can you predict these memories just from the wiring?

## Rates / c02

A firing rate is a nonnegative number describing activity. We are studying a mathematical network model, not measuring a real brain. Its rate changes by balancing natural decay against input from the other neurons and a constant drive.

## Rates / c03

The threshold is simple. If the total input is positive, keep it. If it is negative, replace it by zero. Draw the output against input: flat on the left, then rising on the right.

## Rates / c04

At the settings used here, an arrow means weaker inhibition, with weight minus three quarters. Without an arrow, the weight is minus three halves. Both interactions suppress activity. An arrow is not a positive excitatory connection.

## Balance / c05

Take two neurons with arrows both ways. If both fire at rate x, each receives input one minus three quarters of x. At equilibrium, the firing rate equals that input, so the rate stops changing.

## Balance / c06

Move the three quarters of x to the left. One and three quarters of x equals one. Multiply by four, then divide by seven. Each neuron settles at exactly four sevenths.

## Balance / c07

Now raise the first rate a little. It suppresses the second more strongly. That drop then releases some inhibition on the first. This is positive feedback through two negative connections, even though neither arrow is excitatory.

## Balance / c08

But feedback does not automatically win. Here the natural decay is strong enough to damp the difference. One rate falls while the other rises back toward four sevenths. Returning after sufficiently small nudges is local stability.

## Prediction / c09

The active neurons are called the support. A clique is a group with arrows in both directions between every pair. Our two-neuron example is a clique. Here is the same idea with three neurons.

## Prediction / c10

A target is an outside neuron receiving arrows from the whole group. Remove one of those arrows and that outside neuron is no longer a target. A clique is target-free when no outside neuron receives from all of it.

## Prediction / c11

Curto, Geneson and Morrison conjectured that only target-free cliques could support stable memories. The direction saying these cliques work is proved. The converse is the vulnerable part: could a stable pattern use a group missing an arrow?

## Prediction / c12

We will examine an eleven-neuron example at the standard settings: epsilon one quarter, delta one half, and drive one. All eleven neurons stay active and stable, although their group is not a clique.

## Witness / c13

Start with every possible arrow between different neurons. There are a hundred and ten. Delete these twenty-one arrows. The red dashed arrows show absences. Every connection still acts; the missing arrows mean stronger inhibition.

## Witness / c14

Here is the actual equilibrium. The bars show exact numerators, all divided by two hundred and ninety-two. Every bar is positive, so the support really contains all eleven neurons. The unequal heights are part of the pattern.

## Witness / c15

Check neuron zero. Its stronger inhibitors are neurons five and eight, with numerators thirty-seven and ten. The other ten rates have total numerator three hundred and thirteen. Start with weak inhibition from all ten, then add the extra inhibition from those two.

## Witness / c16

The input becomes one minus three quarters times three hundred and sixty over two hundred and ninety-two. That equals twenty-two over two hundred and ninety-two, exactly neuron zero's rate. The certificate verifies the same balance for all eleven.

## Matrix / c17

A matrix is just a rectangular table that records a linear calculation. For this network, collect the equilibrium equations and multiply by four. The diagonal entries become four. An arrow gives three; a missing arrow gives six.

## Matrix / c18

Reading one row means multiplying its entries by the corresponding rates and adding. The whole table times the rate list must give four in every row. Our exact rate list passes this test, with no decimal rounding.

## Matrix / c19

Balance alone is not enough. A pencil balanced on its tip is at rest, but a nudge grows. Here we examine deviations from the equilibrium. Since every rate stays positive nearby, the threshold does not interfere with this local calculation.

## Matrix / c20

For one changing number, a negative multiplier in its rate-of-change equation pulls it back toward zero. In several dimensions a deviation can also rotate. What matters is whether the rotating motion shrinks or grows.

## Stability / c21

Eigenvalues describe these basic modes of change. A complex pair combines rotation with growth or decay. Its real part controls the envelope. Here the deviation equation uses minus one quarter of the matrix K.

## Stability / c22

So we need every eigenvalue of K to lie to the right of zero. Numerically they do. The closest real part is about zero point zero three seven seven. That thin margin warns us that a picture alone is not a proof.

## Stability / c23

The exact test works with a polynomial instead. Even for a quadratic, coefficients can tell you whether all roots lie on the stable side. The Hurwitz criterion generalises this idea using determinants, precise numbers built from the coefficients.

## Stability / c24

For this degree-eleven polynomial, all eleven required Hurwitz determinants are positive. The first three are forty-four, seven thousand five hundred and fourteen, and one million eight hundred and sixty-seven thousand nine hundred and twenty. Exact arithmetic certifies local stability.

## Nondegenerate / c25

One more technical issue matters. The conjecture assumes certain equation systems have no accidental zero determinants. A determinant tells us whether a linear system collapses a direction. Nonzero means its square table can be inverted.

## Nondegenerate / c26

At these settings there is a neat whole-number argument. Look only at remainders after division by three. Four leaves remainder one. Three and six leave zero. So every such network matrix becomes the identity table.

## Nondegenerate / c27

The identity has determinant one. Therefore each principal determinant of the original integer table has remainder one, and cannot equal zero. For the other required determinants, replace one column by ones. The same remainder argument still gives one.

## Nondegenerate / c28

This works for every graph at the standard parameters, not just eleven neurons. It proves nondegeneracy, not stability. Stability still needs the positive equilibrium and the separate exact Hurwitz checks we just saw.

## Size / c29

How small can a counterexample be? For this particular graph, every proper induced nonclique subgraph fails. That means keep a subset of neurons and all arrows between them. It does not mean every smaller graph in the world fails.

## Size / c30

A separate exhaustive enumeration covers all seven-neuron directed graph shapes, over eight hundred and eighty-two million, plus smaller sizes. Certified rejection bounds remove impossible cases. All thirty-five thousand eight hundred and forty-two saved seven-neuron candidates fail exact stability tests.

## Size / c31

The result brackets the smallest possible nonclique support between eight and eleven neurons. Eight, nine and ten remain unresolved globally. Eleven is minimal under vertex deletion, but it is not proved to be the global minimum.

## Size / c32

A numerical trajectory shows one small perturbation returning to the actual equilibrium. This illustrates the behaviour, while the algebra proves local return. It does not show that every starting state returns, or certify a fixed percentage-sized basin.

## Credit / c33

This is not the first counterexample. Geneson disproved the general conjecture with six neurons at different settings. The public repository hturcotte1 slash C L T N already implied counterexamples at the standard settings, including one with twenty-three neurons.

## Credit / c34

Those repository results were present in commit three seven four four two zero zero, dated the fifteenth of October, twenty twenty-six. Our eleven-neuron graph came from shrinking its twenty-three-neuron example and modifying arrows. Its parameter map also already implied the small-order exclusion.

## Credit / c35

The retained contribution is this smaller explicit witness, exact checks of its vertex-minimality, the universal remainder argument, and an independently certified size bracket. Remember: equilibrium means balanced rates; stability means local return; the full active group need not be a clique.

## Credit / c36

The companion paper and certificates provide the complete graph, rational rates and stability calculations. This film develops their mechanism and proof structure. The exact minimum at the standard parameters is still an open question between eight and eleven.
