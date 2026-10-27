# Readiness

Checked 18 October 2026. **Prepared for human author review.** No external referee has reviewed this manuscript.

## Exact contribution

For every `0 < epsilon < 1`, a smooth three-state periodically driven Markov network has zero entropy production under the target paper's definition, while its same-forward-protocol waiting-time estimator is strictly positive and finite. This contradicts the unrestricted upper inequality in **published Eq. (18)** of Maier et al.; the estimator is their Eq. (17).

The result does not contradict the source's reversed-protocol theorem, Eq. (16), and does not claim zero energetic cost for an external device implementing the protocol. Earlier equilibrium waiting-time false positives are explicitly credited. The candidate novelty is the explicit refutation of this particular periodic conjecture.

## Proof and verification

The argument has six obligations:

1. Symmetric rates leave the probability distribution uniform and make each term of the defined Markov entropy production zero.
2. Occurrence of an observed event biases its starting phase. The correct densities are weighted by `a(t)` or `b(t)`, not by a uniform phase independently of the event.
3. The reversed event pair has derivative difference `(f-g)'(0) = epsilon² > 0`, so its two waiting densities differ on a positive-measure interval.
4. Every state has an observed exit rate bounded below by `1 - epsilon`; the next observed event therefore occurs almost surely, which normalizes each row of waiting distributions.
5. All four observed events have mean rate `1/3`. The full estimator is consequently `4/3` times a KL divergence between two normalized distributions, hence strictly positive.
6. Allowed pairs have reversal-invariant support. Explicit exponential bounds on their densities and linear bounds on log ratios prove that the KL divergence is finite, including near zero delay for pairs requiring a hidden transition.

The exact standard-library checker was rerun with Python assertions disabled and passed all six rational Fourier-polynomial identities. **There is no Lean formalization.** That checker covers the local derivative calculation; event conditioning, normalization, support and integrability are established by the written proof and internal audit.

## Sources and priority boundary

The complete published article is Maier, Degünther, van der Meer and Seifert, *Journal of Statistical Physics* 191, article 104 (2024), [DOI 10.1007/s10955-024-03315-7](https://doi.org/10.1007/s10955-024-03315-7). Both the 17-page publisher PDF and a fresh full publisher HTML extraction were inspected. The conjecture remains explicit in the inspected source. Its general setup permits periodic rates satisfying local detailed balance and does not impose constant symmetric kinetic prefactors.

Published Eqs. (17), (18) and (16) correspond respectively to arXiv-v1 Eqs. (14), (15) and (13). The manuscript uses published numbering first. This avoids presenting a claim based only on an obsolete or differently numbered version.

Hartich and Godec's earlier equilibrium false-positive example and Harunari, Fiore and Barato's reversed-protocol analysis are distinguished in the text. A fresh search also inspected Maier, Häsler and Seifert's later transition-detection-blackout preprint; its stationary setting and missing-event mechanism do not supply this periodic counterexample. See [source-review.md](source-review.md) for the precise reads and limits.

No exact earlier counterexample was found in the inspected material. Search absence does not establish priority. A completed focused DeepResearch review supports the literal counterexample, but its incorrect auxiliary reversal claim was rejected and is not used; see [adversarial-review.md](adversarial-review.md).

## Files and remaining decisions

- The [public PDF](../../../../public-release/papers/periodic-waiting-time.pdf) lists the human author and records the contribution and review status. The earlier archival `paper.pdf` is omitted from the public export; its hash is retained in the release records.
- The two four-page presentations checked on 18 October built with no LaTeX warning, unresolved citation, overfull or underfull box in the recorded logs. These are historical build checks.
- The sole-author version discloses the actual coding-agent contributions to the counterexample, proof, checker and manuscript, alongside DeepResearch literature work. It does not assert human approval.
- [author-walkthrough.md](author-walkthrough.md) explains the model and the inference failure without relying on thermodynamics jargon.
- Remaining work: human line-by-line review and approval of every proof step, and a final source and priority refresh. Specialist scrutiny of the physical interpretation remains valuable and has not occurred.

Correctness confidence: **high for the explicit mathematical counterexample**. Originality confidence: **moderate**, bounded by the source searches. No experimental validation or peer review is claimed.
