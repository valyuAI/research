# Research provenance

The initial collection was developed on 17-18 October 2026 and expanded on 25-26 October through literature retrieval, focused research reviews, mathematical derivation by coding agents and independent computation. The [new campaign record](campaigns/2026-10-25-discoveries.md) and [collection index](collection.md) describe the expanded scope; the review identifiers below are the historical first-round record.

## Division of work

The literature work located explicit unresolved claims and checked later papers, author materials, and related formulations. Coding agents running locally produced the proposed constructions and proofs. Focused DeepResearch tasks were then given the statements and arguments for adversarial correctness and priority review. The reports were read critically: several useful attribution concerns were accepted, and several incorrect mathematical corrections were rejected with counterexamples.

DeepResearch is therefore part of the documented research and review process. The collection does not claim that a generated report alone discovered or verified these theorems.

## Focused reviews

| Review | Task identifier | Role |
|---|---|---|
| Prime-successor Hales-Jewett | `DR-006` | Check definitions, construction, earlier modular colorings, exact case, and current priority |
| Generic Lotka-Volterra trees | `DR-047` | Check complete Darboux set, reconstruction, scope of Conjecture 12, and later work |
| Conjugate restart optimality | `DR-023` | Audit global proof, uniqueness, reversibility converse, and closest variational prior art |
| Three-dimensional inverse elasticity | `DR-016` | Completed literature and early-summary audit; did not replay the exact arithmetic certificates |
| Minimal elasticity measurements | `DR-048` | Completed exploratory review; no proof of eight-direction global recovery |
| Full elasticity manuscript | `DR-011` | Completed review of the seven-page draft; no fatal gap found conditional on certificates, which it did not replay; excludes the later eleven-direction extension |
| Thermal series design | `DR-077` | Completed review; model-level argument supported, attribution comparison remains incomplete |
| Nonlinear contact-law exponent | `DR-060` | Completed review; reduced static model supported, no full dynamic contact-law claim |
| Truncated-dodecahedron rigidity | `DR-093` | Completed review of the proof note; obstruction and specialization argument supported, saved certificates not replayed |
| Periodic waiting-time counterexample | `DR-071` | Completed proof and prior-art review; supports the specific conjecture counterexample, with a mistaken auxiliary pointwise-equality claim rejected on checking |

Coding agents developed the elasticity proof during the broader DeepResearch campaign. Independent investigators reconstructed its matrices, checked the geometric argument and audited current primary sources. A separate standard-library checker verifies eleven explicit minor identities. The completed initial report supports the literature audit but is not a replay of these certificates. Its proposed objections were assessed against the actual geometric argument; unsupported objections were not adopted merely because they appeared in a report. The completed manuscript review independently reconstructed several intermediate ranks and supported the geometric argument conditional on the certificates. Two wording improvements concerning initial forms and eligible fixed points were adopted. It reviewed the earlier seven-page draft, not the later eleven-direction theorem.

Task identifiers preserve a connection to the unpublished research record. The curated repository contains no credentials or service configuration. Full retrieved third-party texts and unrelated raw research data are not redistributed with the papers.

The completed rigidity survey (`DR-038`) identified the truncated dodecahedron as an explicit unresolved example and proposed higher-order elimination with a numerical lead. Coding agents then constructed an exact certificate over a finite field and proved that it implies rigidity in characteristic zero. A separate implementation reconstructs the solid directly from its algebraic coordinates and checks every certificate identity; seven deliberately corrupted inputs are rejected. Independent written audits cover the formal elimination, isolation and specialization steps. The completed focused DeepResearch review supports the theoretical implication and independently reconstructed analogous modular obstructions. It did not replay the saved certificate and is not described as having done so.

## Writing and presentation

The manuscripts were revised using primary exposition guidance from Terence Tao and Paul Halmos, AMS author guidance, and short papers in the relevant fields. The practical choices were to state the contribution early, make the novelty boundary explicit, keep notation local, give complete detail at the decisive step, and omit speculative applications. All PDF pages were rendered and inspected.

Useful guidance includes Tao's [introduction advice](https://terrytao.wordpress.com/advice-on-writing-papers/use-the-introduction-to-%E2%80%9Csell%E2%80%9D-the-key-points-of-your-paper/), [appropriate detail](https://terrytao.wordpress.com/advice-on-writing-papers/give-appropriate-amounts-of-detail/), [notation](https://terrytao.wordpress.com/advice-on-writing-papers/use-good-notation/), and the [AMS Author Handbook](https://www.ams.org/arc/handbook/index.html).

An 18 October writing pass also applied the public [scientific-paper-writer skill](https://github.com/eniktab/scientific-paper-writer/blob/main/skills/scientific-paper-writer/SKILL.md): claim-specific prose, verified citations and a clear central result. Its experimental-paper defaults were adapted to theorem-and-proof notes. Some packages include readiness notes and author walkthroughs.

## Authorship, review status and competing interest

Harvey Yorke directed the project. Coding agents developed the arguments, the verification checkers and the manuscript drafts. Valyu DeepResearch carried out the literature, priority and internal adversarial reviews. Narration in the explainer videos is synthetic speech.

The author has not yet completed a line-by-line review of every proof. Correctness rests on the agents' written proofs, independent exact checks and the stated [Lean coverage](formal-coverage.md). No result has been externally peer reviewed. Per-package author walkthroughs are reading guides, not records of human review.

The public PDFs in [`public-release/papers/`](../public-release/papers/) list Harvey Yorke as sole author with that contribution statement. Earlier archival `paper.pdf` builds listed Valyu DeepResearch as a co-author; that presentation was dropped because AI systems cannot take responsibility for a paper, consistent with the [AMS policy](https://www.ams.org/publications/journals/policies/UseofArtificialIntelligence). All presentations share the same mathematical source.

Competing interest: Valyu AI develops DeepResearch, Search and Contents, which were used throughout this work.

## Negative findings retained

An earlier descriptive spaceflight liver association did not meet the discovery standard. A random-matrix proof attempt was discarded after a prior publication was found. A bounded astronomy extension completed all 2,641 discovery targets: 2,073 were processed and 568 had no usable cadences under the stated quality filters. Its 133 screening triggers were not promoted to discoveries. Both control objects were processed but fell below the stricter screening threshold, so this search supports no completeness or detection-sensitivity claim. The earlier astronomy pass included instrumental and detrending artifacts. These are not represented as new discoveries in this collection.

As of 27 October 2026, no author outreach, journal submission or public announcement has occurred.

## Cubic reaction-network construction

The chemical-kinetics exploration (`DR-061`) prompted investigation of the equilibrium bounds in Banaji and Feliu. Coding agents improved an initial higher-degree construction to a source matrix of degree three for every n. Independent agents reviewed the complete interpolation, reaction validity, equilibrium parametrization, nondegeneracy and minimal-degree arguments. Two different exact implementations check the retained finite examples.

The focused review (`DR-009`) received the complete cubic proof, generator and finite certificate. It completed without identifying a new proof defect; its recommendations were independently assessed, including rejection of two erroneous or outdated suggestions. The current published paper was inspected directly after a version-labelled arXiv extraction returned an obsolete manuscript. Two older conjectures already resolved in the publication were discarded as discovery targets. A closely related October 2026 candidate addresses a different full-rank quadratic problem and is cited. These checks establish the bounded comparison, not exhaustive priority.
