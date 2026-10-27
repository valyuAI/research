# Independent audit: periodic waiting-time estimator

Checked 17 October 2026. Status: the smooth counterexample is analytically sound under the source's stated Markov-network assumptions. This is an internal correctness audit, not an external review or a completed priority search.

## Source meaning

Maier, Deguenther, van der Meer and Seifert, [arXiv:2406.12657](https://arxiv.org/abs/2406.12657), *Inferring kinetics and entropy production from observable transitions in partially accessible, periodically driven Markov networks*, Journal of Statistical Physics (2024) 191:104, [DOI 10.1007/s10955-024-03315-7](https://doi.org/10.1007/s10955-024-03315-7).

The arXiv landing page retrieved on this date links version 1. The initial contents response requested through a version-2 URL must not be treated as evidence that a version 2 exists. For the formulas, the independently inspected [ar5iv rendering](https://ar5iv.labs.arxiv.org/html/2406.12657) preserves the crucial tildes: the denominator in Eq. (14) is `Psi_{reverse(J)->reverse(I)}` under the **same protocol**. Equation (13), in contrast, has a tilde on the waiting-time density itself and uses the reversed protocol. Section 4 explicitly introduces Eq. (14) as avoiding data from the reversed process regardless of protocol symmetry. Equation (15) conjectures that this estimator lies below Eq. (3)'s mean Markov entropy production.

The main setup requires positive periodic rates satisfying local detailed balance, Eq. (1). It does not restrict kinetic prefactors to be constant. The fixed-prefactor parameterization in Eq. (18) belongs to the numerical examples. The construction below satisfies Eq. (1) with all state free energies and edge affinities zero. It varies symmetric rates, not their ratios.

## Independent reconstruction

Use period `T=2*pi`, any `0<epsilon<1`, and three states. On undirected edges 12, 23, 31 set, respectively,

`a(t)=1+epsilon*cos(t)`, `b(t)=1+epsilon*sin(t)`, `c(t)=1`.

Both directions on each edge have that same rate. Observe the four labels `12,21,23,32`; hide `13,31`. Symmetry makes `(1/3,1/3,1/3)` an exact stationary solution at every phase. Strictly positive rates make it the unique periodic stationary state. Every summand of the source's Eq. (3) has logarithm zero, so that entropy production is exactly zero.

For any observed label I, its mean occurrence rate is `n_I=1/3`. Its phase density is `r_I(t)/(2*pi)`, not the uniform phase density: this follows from Eq. (10), `p_origin*r_I(t)`, normalized by its integral over a period. Thus the four labels have equal event probability `1/4`.

Immediately after either 12 or 32 the process is in state 2, from which every exit is visible. Let

`S(t,s)=exp(-integral_[t,t+s] (a(u)+b(u)) du)`.

The two relevant densities are consequently

`f(s)=Psi_12->23(s)=average_t a(t)*b(t+s)*S(t,s)`,

`g(s)=Psi_32->21(s)=average_t b(t)*a(t+s)*S(t,s)`.

These are event-phase-weighted densities for the next observed label and waiting time together; they are not separately normalized to one for each fixed label pair.

At zero lag `f(0)=g(0)=average(a*b)=1`. Differentiation is valid because all functions are smooth and the phase domain is compact. The survival derivative is the same in both expressions and cancels, giving

`(f-g)'(0)=average(a*b'-b*a')=epsilon^2>0`.

More explicitly, `average(a*b')=epsilon^2/2`, `average(b*a')=-epsilon^2/2`, and `average(a*b*(a+b))=2+epsilon^2`. Thus `f'(0)=-2-epsilon^2/2` and `g'(0)=-2-3*epsilon^2/2`. There is an interval of strictly positive lags on which `f>g>0`. The calculation is corroborated by an independent exact Laurent-polynomial checker using rational coefficients.

## Normalization and strict positivity

Every state has an observed exit with rate at least `1-epsilon`. Hence survival without an observed event is at most `exp(-(1-epsilon)*s)`, and an observed event occurs almost surely. For each initial label I, `sum_J integral_0^infinity Psi_I->J(s) ds=1`.

Define probability densities on directed-label pairs and positive waiting times by `P(I,J,s)=Psi_I->J(s)/4` and `Q(I,J,s)=Psi_reverse(J)->reverse(I)(s)/4`. The reversal map permutes the sixteen label pairs, so both densities integrate to one. Equation (14) becomes exactly `(4/3)*D_KL(P||Q)`. Since f and g differ on a set of positive measure, this divergence is strictly positive. Alternatively, pair each term with its reversal: equal weights give `(1/3)*(f-g)*log(f/g)`, a nonnegative contribution that is strictly positive on that interval. Every other reversal orbit contributes nonnegatively.

The supports match. From state 2, the next visible label is 21 or 23. From states 1 or 3, the only hidden edge connects those two states, and the next visible label is 12 or 32. Reversal preserves this allowed-pair set. Impossible pairs are zero on both sides and contribute zero. All allowed densities are positive for s>0.

The divergence is finite. For starting state 2, the density bounds use the constant-rate survival bounds above. For starting states 1 or 3, retain the independent hidden rate-1 chain on {1,3}; its transition probabilities are `(1+exp(-2*s))/2` for the same state and `(1-exp(-2*s))/2` for the other state. Feynman-Kac bounds multiply these by survival factors between `exp(-(1+epsilon)*s)` and `exp(-(1-epsilon)*s)`. Event-phase and final-rate factors lie between `(1-epsilon)^2` and `(1+epsilon)^2`. Each reversal pair has the same hidden-transition parity, so these factors cancel in ratio bounds. Log-density ratios therefore grow at most linearly in s, while the densities have exponential tails.

Consequently the smooth family has `sigma=0<sigma_hat_Psi<infinity`, contradicting the upper inequality in the general conjecture (15). It does not contradict the proved reversed-protocol estimator (13), and it makes no statement about energetic costs of an external device implementing the protocol.

## Audit boundary

The counterexample uses two observed undirected edges sharing a vertex and one hidden edge. The source permits at least one observable pair and arbitrary additional observable pairs; it does not require disjoint observed edges or an unobserved interior state. No assumption is added that polygonal protocols or discontinuous rates are admissible: this construction is analytic and uniformly positive.

This audit checked definitions, event weighting, exact stationarity, the short-lag derivative, support, normalization, and KL positivity. Whether the counterexample or a comparable restriction of the conjecture is already in later literature remains a separate priority question.
