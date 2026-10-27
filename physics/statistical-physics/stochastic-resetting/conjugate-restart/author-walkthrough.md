# Understanding the restart proof

The question is whether a restart strategy that is locally stationary might still lose to a very different waiting-time distribution. Here the answer is no for the stated one-dimensional Brownian problem and its conjugate target density.

1. **An attempt has two quantities.** Its success probability is f(x); its expected duration is h(x). Independent repeated attempts cost h(x)/f(x) on average. The target stays fixed between attempts.
2. **Brownian motion connects those quantities.** The Green kernel min(x,y)/D gives h(x) as an integral of f(y). Check both boundary conditions in the deterministic-waiting-time calculation; mixing uses nonnegative integrals.
3. **Choose the target density from the reference strategy.** It is proportional to the square of its success function. This conjugate construction comes from Evans and Ray.
4. **Subtract the reference cost.** Symmetrizing produces a weighted integral of a square divided by a positive product. It cannot be negative. The underlying ratio inequality is known, and Dávila-Topp is cited.
5. **Handle infinite competitor cost honestly.** The identity is a finite baseline plus a nonnegative integral, not subtraction of two infinities.
6. **Equality identifies the strategy.** Zero gap forces proportional success functions; their limit at zero makes the factor one. A weighted Laplace-transform argument then identifies the actual waiting-time law.
7. **Finite chains need a different equality claim.** Reversibility supplies the symmetric Green matrix. Under cyclicity, exponential mixtures fill an open set; universal optimality then forces detailed balance. Finite success vectors do not uniquely identify waiting-time laws.

For a concrete example, if the diffusion coefficient is 1 and target distance has exponential rate 2, the uniquely optimal iid waiting law is exponential with rate 1 and the mean completion time is 1. Adaptive choices, observation-dependent resets and reset costs are outside the theorem.

During line-by-line review, the author should be able to explain why the symmetric-kernel calculation is prior work, why uniqueness needs the transform argument, and which parts Lean actually checks. Agent review cannot establish that the human author has completed this step.
