# A zero-dissipation test of the forward-protocol waiting-time conjecture

Working note, 18 October 2026. Confidence in the analytic calculation: high. An independent source/theory audit and exact Fourier checker pass. Focused prior review found broad waiting-time false-positive precedents; no priority claim is made.

## Literal source claim

Alexander M. Maier, Julius Degunther, Jann van der Meer and Udo Seifert, *Inferring kinetics and entropy production from observable transitions in partially accessible, periodically driven Markov networks*, Journal of Statistical Physics 191:104 (2024), DOI [10.1007/s10955-024-03315-7](https://doi.org/10.1007/s10955-024-03315-7), [arXiv:2406.12657](https://arxiv.org/abs/2406.12657).

The complete [published article](https://link.springer.com/article/10.1007/s10955-024-03315-7), Eq. (17), defines the following estimator. It is Eq. (14) in the [arXiv-v1 rendering](https://ar5iv.labs.arxiv.org/html/2406.12657).

```
sigma_hat = sum_(I,J) nbar_I integral Psi_(I->J)(s)
  log[Psi_(I->J)(s) / Psi_(reverse J -> reverse I)(s)] ds.
```

Both laws use the forward driving protocol. Only the event labels are reversed. Published Eq. (18) conjectures `0 <= sigma_hat <= mean sigma`. The source explicitly distinguishes this from its proven Eq. (16), whose denominator uses reversed-protocol data. These are respectively Eqs. (15) and (13) of arXiv v1.

Equation (3) defines the total Markov entropy-production rate as the period average of `sum_(i,j) p_i k_ij log[p_i k_ij/(p_j k_ji)]`. Section 2 imposes periodic rates and local detailed balance, with no fixed-kinetic-prefactor restriction stated. Appendix A introduces particular numerical rate choices, usually with constant prefactors but also an explicit exception; those choices do not restrict the general conjecture.

## Smooth construction and proof

Take three ordinary states, period `T=2*pi`, and `0<e<1`. Set

```
k12(t)=k21(t)=a(t)=1+e*cos(t),
k23(t)=k32(t)=b(t)=1+e*sin(t),
k31(t)=k13(t)=1.
```

Observe `12,21,23,32` and hide `31,13`. Every rate is positive and smooth. All local detailed-balance ratios equal one, so the source's Eq. (1) holds with all free energies and affinities zero. Each instantaneous generator is symmetric; its periodic stationary distribution is exactly `p_i(t)=1/3`. Every term in Eq. (3) vanishes. Thus `mean sigma=0`.

All four visible directed events have mean rate `nbar_I=1/3`, so their event probabilities are `1/4`. Immediately after either event `12` or `32`, the system is at state 2. Every exit from 2 is visible, so no hidden intermediate jump occurs before the next visible event. If brackets denote period average, the correct event-conditioned laws are

```
H(t,s)=integral_t^(t+s) [a(u)+b(u)] du,
f(s)=Psi_(12->23)(s)=<a(t)b(t+s) exp[-H(t,s)]>,
g(s)=Psi_(32->21)(s)=<b(t)a(t+s) exp[-H(t,s)]>.
```

The initial `a(t)` and `b(t)` factors are the event-conditioned phase weights in source Eq. (5); their means are one. At zero lag `f(0)=g(0)`. Smoothness permits differentiation under the integral. The common survival derivative cancels pointwise, giving

```
(f-g)'(0)=<a*b'-b*a'>
         =<e*cos(t)+e*sin(t)+e^2>
         =e^2>0.
```

Consequently `f(s)>g(s)` on an interval of positive lags. This is an exact identity, requiring no optimization or limiting trajectory simulation.

Define normalized joint pair densities `P(I,J,s)=Psi_(I->J)(s)/4` and `Q(I,J,s)=Psi_(reverse J -> reverse I)(s)/4`. Each has total mass one: every initial-event waiting law has row mass one, and reversal permutes all pairs. Since all mean event rates equal `1/3`, the full estimator is `(4/3) D_KL(P||Q)>0`. Equivalently, reversal pairs contribute a positive multiple of `(f-g)log(f/g)`, and every other pair contributes nonnegatively. Thus the upper inequality in published Eq. (18) fails under its stated general periodic-rate assumptions.

Every state has an observed exit rate at least `delta=1-e`, so the next observed event occurs almost surely and each waiting-density row integrates to one. Matching zero-support pairs contribute zero. For an allowed pair starting in state 1 or 3, let `q_s=(1 +/- exp(-2s))/2` be the transition probability of the hidden rate-one chain, with sign determined by its endpoint parity. With `B=1+e`,

```text
delta² exp(-B*s) q_s <= Psi_(I->J)(s) <= B² exp(-delta*s) q_s.
```

Reversal preserves endpoint parity, so `q_s` cancels in the density ratio. State-2 pairs have analogous bounds with `q_s=1` and doubled decay exponents. All allowed pairs consequently satisfy `|log(Psi/Psi_reverse)| <= 2 log(B/delta)+4e*s`, while each density is at most `B² exp(-delta*s)`. This proves finiteness of the complete estimator, including near zero delay. All states are time-reversal even. The hidden link is real, so the example is partially observed.

The same calculation gives a broader criterion for positive equal-mean smooth rate functions: `(f-g)'(0)=<a b'-b a'>/<a>`. A nonzero oriented area of the closed rate-plane curve therefore suffices. This observation explains the mechanism; it is not a separate priority claim.


## Scope and provenance

The claim concerns the same-forward-protocol conjecture, not the proved estimator that uses reversed-protocol observations. No claim is made about the cost of an autonomous controller producing the external rates. Broad equilibrium waiting-time false positives are established prior art. See [source review](source-review.md), [independent mathematical review](review.md), and [adversarial-review disposition](adversarial-review.md).

DeepResearch identified the published target and supported source comparison. Coding agents developed the explicit family and analytic proof, implemented the exact Fourier checker, and drafted and revised the manuscript. The checker verifies polynomial identities, not the full probabilistic argument. No human author approval, external peer review, Lean formalization or priority guarantee is claimed.
