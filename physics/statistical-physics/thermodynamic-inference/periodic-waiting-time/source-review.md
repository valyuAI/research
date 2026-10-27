# Focused prior-art audit of the periodic waiting-time counterexample

Audit performed overnight 17-18 October 2026; persisted 18 October after disk cleanup. All web retrieval used Valyu Search or Contents through the CLI. During ENOSPC, the new source responses were read in memory and retained in the tool transcript, not as local raw files. This note contains paraphrases and primary links, not redistributed full texts.

## Conclusion and scope

No exact prior counterexample to the forward-protocol conjecture in Maier et al., published Eq. (18), corresponding to arXiv-v1 Eq. (15), was located in the inspected primary material. This is bounded evidence, not an exhaustive priority claim. The broad warning that waiting-time asymmetry can produce a false dissipation inference is already established and must be credited. The prospective contribution is specifically the smooth, uniformly positive three-state counterexample to that published periodic estimator.

The mathematical distinction between these sources is high-confidence. Publication priority remains provisional. The separate [independent mathematical review](review.md) checks the counterexample itself.

## Harunari, Fiore and Barato: the closest periodic comparison

Pedro E. Harunari, Carlos E. Fiore and Andre C. Barato, *Inference of entropy production for periodically driven systems*, Physical Review E **110**, 064126 (2024), [DOI 10.1103/PhysRevE.110.064126](https://doi.org/10.1103/PhysRevE.110.064126). The [arXiv record](https://arxiv.org/abs/2406.12792) gives first submission 18 June 2024 and version 2 dated 16 December 2024. The [primary ar5iv rendering](https://ar5iv.labs.arxiv.org/html/2406.12792) was read in full through the conclusions, including the estimator definitions and proof; its content length was 56,750 characters. The abstract and publication date were also checked against the publisher result.

- Section II.4, Eq. (13), explicitly defines the reversed driving protocol. Section II.5, Eq. (14), uses a dagger on the reverse waiting-time density. It requires both forward- and reversed-protocol observations.
- Section IV.2, Eqs. (25)-(28), proves `sigma >= sigma_hat - X`, with `X >= 0`, after phase marginalization. The authors explicitly leave the stronger uncorrected inequality unproved and describe their supporting numerics as restricted to one model.
- Section VI explicitly discusses Maier et al.'s forward-only estimator as a numerical conjecture and calls the approaches complementary. It contains no explicit refutation of that conjecture or the smooth zero-entropy false positive constructed here.
- The three-state model rotates energies and barriers. Eqs. (3)-(4) allow time-dependent symmetric barriers. Eq. (5) and the accompanying explanation assign the modeled entropy production to energy changes and state that barriers enter through occupation probabilities. This supports the admissibility of barrier-only modulation with zero modeled entropy production; it is not a claim about the cost of an external actuator.

The need to distinguish protocol reversal from reversal of observed labels is therefore existing knowledge. The new candidate must not claim that distinction itself as a discovery.

## Schwarz, Hartich and Godec: a relevant earlier false-positive mechanism

Tassilo Schwarz, David Hartich and Aljaz Godec, *Milestoning Markov-jump dynamics: Stationary properties, thermodynamic consistency, kinetic hysteresis, and fluctuation symmetries*, [arXiv:2606.17033](https://arxiv.org/abs/2606.17033), submitted 15 June 2026. The setup, abstract, relevant kinetic-hysteresis section and references were inspected in the [primary text](https://arxiv.org/html/2606.17033v1); the complete text response contained 86,583 characters. This audit did not read every appendix.

The setup uses a time-independent generator and state milestoning. Section I.C.4, Eqs. (43)-(52), gives distinct conditional waiting-time densities at thermodynamic equilibrium. Their KL divergence stays positive even with arbitrarily fast hidden dynamics, approaching a reported value about 0.079. The paper explicitly explains why a naive reversal of the coarse-grained record then gives a false dissipation inference.

This is material prior art for the broad phenomenon. It concerns finite transition-path times and a coarse-graining operation that does not commute with reversal. Our candidate instead observes actual instantaneous edge transitions, marginalizes the periodic phase, and compares both label directions under the same forward protocol. The displayed result is not a direct counterexample to Maier's periodic Eq. (15). Maier's 2024 article appears in the general references; no explicit discussion of its conjecture was found in the inspected sections.

The related primary record is David Hartich and Aljaz Godec, *Comment on “Inferring broken detailed balance in the absence of observable currents”*, Nature Communications **15**, 8678 (2024), [DOI 10.1038/s41467-024-52602-0](https://doi.org/10.1038/s41467-024-52602-0). Its [author-deposited PDF](https://pure.mpg.de/rest/items/item_3617205_2/component/file_3617245/content) was located. The publisher page returned a client challenge to this reviewer, so the full primary read was delegated to the root reviewer; this note does not claim that read was completed here. The arXiv identifier 2112.08978 was not independently matched by this reviewer.

## Current author material and search limits

[Harunari's primary publication page](https://pedroharunari.github.io/website/) was retrieved through Valyu Search, including its full approximately 3 KB text. Direct Contents returned empty. The page reports a postdoctoral move after September 2025 and lists 19 works, including the periodic inference paper and later work on stochastic excursions and network currents. No explicitly named refutation of Maier's conjecture appears in that list. A publication list is not evidence that no unlisted or unpublished result exists.

Targeted searches combined the original title or author names with conjecture, counterexample, periodic driving, barrier modulation and waiting-time inference. No inspected primary hit supplied the specific counterexample. One query combining only the numeric arXiv identifier and years returned irrelevant records and is not counted as negative evidence. Search snippets were used to locate sources, not to certify absence of a theorem.

Recommended framing: an explicit analytic counterexample to a specific conjectured estimator, with prior work credited for protocol reversal and kinetic-hysteresis false positives. Do not frame it as the first demonstration that time asymmetry and thermodynamic dissipation can differ.

## Supplementary primary read

The lead reviewer subsequently read Hartich and Godec's full [arXiv:2112.08978 preprint](https://arxiv.org/abs/2112.08978) through Valyu Contents. Its title and authors match the published comment's metadata. Its explicit equilibrium waiting-time false positive and kinetic-hysteresis discussion support the paper's prior-work paragraph. The publisher and author-deposit fetches were blocked, so identity of the complete published text with the consulted preprint is not asserted. The bibliography says explicitly that the preprint was consulted.

The completed focused DeepResearch review independently accepts the literal counterexample. Its source findings are assessed in [the review disposition](adversarial-review.md). The present paper gives the verified published equation numbers first, alongside their arXiv-v1 equivalents, and does not rely on unverified numerical extensions in that report.

## Published-version verification, 18 October 2026

A subsequent Valyu Contents request successfully retrieved the complete [17-page Springer publisher PDF](https://link.springer.com/content/pdf/10.1007/s10955-024-03315-7.pdf), despite the article's HTML page still returning a challenge. The extracted primary text contains all page markers and the title-page publication date, 14 August 2024. The [Stuttgart publications page](https://www.itp2.uni-stuttgart.de/publications/), entry 256, independently links to that same PDF. Mathematical-font extraction artifacts were cross-checked against arXiv v1 and the publisher's prose.

The published equation mapping is now directly verified:

| Object | Published article | arXiv v1 |
| --- | --- | --- |
| Mean Markov entropy production | Eq. (3), p. 3 | Eq. (3) |
| Proven reversed-protocol estimator | Eq. (16), p. 7 | Eq. (13) |
| Same-forward-protocol estimator | Eq. (17), p. 7 | Eq. (14) |
| Conjectured bound | Eq. (18), p. 7 | Eq. (15) |

On p. 7, the text preceding Eq. (17) explicitly says these estimators do not require waiting distributions from the time-reversed process, regardless of driving symmetry. The paragraph after Eq. (18) explicitly retains the conjecture for periodically driven Markov networks. Section 5.1, p. 9, contrasts it with Harunari et al.'s reversed-protocol estimator. Section 5.2, p. 10, again calls the proof open and explains that reversing the driving is unnecessary for this proposed estimator. The published target is therefore the same as the arXiv-v1 target.

Section 2, pp. 2-3, requires periodic rates and local detailed balance, Eq. (1), with no constant symmetric-prefactor condition in the general model. The numerical appendix introduces its own parametrization and usually sets its prefactors to one. It also explicitly uses `k13=1` and `k31=exp[-F1(t)+F3(t)+f31]` in the three-state family, p. 12. Thus a claim that every simulated edge has a constant symmetric prefactor would be inaccurate. These numerical choices do not impose a restriction on the general conjecture.

Five targeted searches and the current institution publication list did not identify a specific correction, but several queries returned irrelevant records. They do not certify that no erratum, later counterexample or unpublished result exists. A request for the later Nature Reviews Physics article returned a subscription preview and references, not its main text; no absence-of-counterexample claim is based on that response. The new evidence materially resolves the published-source interpretation, while priority remains open.

## Submission-preparation refresh, 18 October 2026

A fresh domain-restricted search returned the full [publisher HTML](https://link.springer.com/article/10.1007/s10955-024-03315-7), including the retained Eq. (18) conjecture, as well as the already reviewed Harunari et al. paper. The publisher extraction contains approximately 80,000 characters and agrees with the PDF on the estimator's definition and general assumptions. No correction notice was present in the retrieved article text. This does not certify that no correction exists elsewhere.

The search also returned Maier, Häsler and Seifert, [*Compensating random transition-detection blackouts in Markov networks*](https://arxiv.org/html/2511.14679). Its abstract, setup, main construction, conclusions and references were inspected. It studies a stationary underlying Markov network with random failures to detect otherwise observable transitions. The authors explain that asymmetric detection can create false nonequilibrium indications, then derive a correction method. Periodically driven systems are mentioned as a prospective extension. Our model records every occurrence of its four chosen directed edges and has no random detection blackout. Thus the inspected work supplies related inference context, not this counterexample to the periodic forward-protocol conjecture. No assertion of having inspected every supplementary derivation is made.

An initial broad query returned mostly irrelevant material and is not counted as useful negative evidence. Raw search responses remain outside the curated package. The novelty assessment stays bounded and provisional.
