# Assessment of the completed focused review

Checked 18 October 2026 against the completed focused DeepResearch report (task DR-071) and the independently inspected primary sources. This is an internal assessment of a generated adversarial report, not external peer review.

## Accepted findings

The report accepts the smooth counterexample to the literal forward-protocol conjecture. Its checks of uniform stationarity, zero Markov entropy production, event-phase weighting, equal mean label rates, the derivative difference `epsilon^2`, reversal-orbit positivity and the KL formulation agree with the independent derivation. No fatal objection to the main proof was identified.

Its distinctions between Maier's forward-only conjecture, Maier's proved reversed-protocol bound, and Harunari's different estimator agree with the primary Section 4 and Harunari Sections II.4, II.5, IV.2 and VI. Its caution that the broad false-positive mechanism is known agrees with the kinetic-hysteresis material independently checked here. Its absence-of-prior-result finding remains bounded and is not a priority certificate.

The report identifies further citations and numbering differences between arXiv and journal versions. Those are useful literature leads. The manuscript retains explicit arXiv-v1 equation numbering, which this reviewer independently verified. The journal numbering was not independently rechecked here because the direct publisher fetch returned a challenge page.

## A substantive error to exclude

Section 3's explanation of the proved reversed-protocol bound incorrectly says that its phase-resolved conditional waiting-time densities equal the forward conditional densities. Conditioning excludes the initial jump and includes the final jump. They generally differ even when full trajectory probabilities agree under physical reversal.

For the selected pair starting at phase t and ending at t+s, the forward conditional density is `b(t+s)*S(t,s)`. The reversed-protocol conditional density for the reversed event pair at reflected phase `-(t+s)` is `a(t)*S(t,s)`. Their ratio is `b(t+s)/a(t)`, generally not one.

The correct identity multiplies each density by its initial event intensity. Forward weighting gives `(a(t)/3)*b(t+s)*S(t,s)`; reversed weighting gives `(b(t+s)/3)*a(t)*S(t,s)`. These joint quantities agree. Equal period-mean event intensities then imply equality of the phase-marginalized forward and reversed-protocol densities after changing phase variable. The total phase-resolved estimator also vanishes through cancellation of initial and final event terms, not pointwise equality of the conditional densities.

This error is ancillary to the main proof and does not weaken the counterexample. It was communicated to the manuscript author and root reviewer; the final manuscript does not use the incorrect assertion.

## Unaccepted extensions

The report's floating-point random-network and time-symmetric examples are exploratory leads. Their underlying numerical artifacts were not independently reconstructed in this audit. They must not be promoted to certified additional counterexamples or inserted into the current theorem. Likewise the suggested fixed-prefactor restriction is a possible research question, not a proved safe replacement for the conjecture.

The report's first-orbit small-amplitude expansion is not needed by the paper and was not independently certified here. The existing exact rational Fourier checker covers the zero-lag derivative identities, not that finite-lag expansion.

## Final manuscript review

The research draft [the paper source](paper.tex) was reviewed in full after the report arrived. Its main theorem, normalization, support, finiteness, common-mean signed-area formula, prior-art paragraph and verification boundary are coherent. No substantive mathematical or code-simplification change was requested. PDF presentation is reviewed separately by its author.
