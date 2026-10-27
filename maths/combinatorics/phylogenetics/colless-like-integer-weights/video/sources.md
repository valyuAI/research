# Evidence ledger

Read 26 October 2026: ../README.md, ../readiness.md, ../video-brief.md, entire ../paper.tex, ../verification/README.md, ../verification/check_colless.py, ../verification/reviews/phylo-colless-prior.md and the final completion manifest. Final readiness takes precedence over older review wording.

- Definition, full symmetry and soundness: paper section 1; original Mir-Rotger-Rossello paper, https://pmc.ncbi.nlm.nih.gov/articles/PMC6155497/ and https://arxiv.org/abs/1805.01329 .
- Exact 13-versus-13 example: readiness and checker, using f(n)=n+1. Diagram edges have no length meaning.
- Universal count: paper section 2, (3m)!/(m!)^3 versus M*24^m+1. The plotted ratio uses lgamma to evaluate the exact factorial expression numerically for display; it is not proof by numerical approximation.
- Hypotheses: nonnegative f, f(2),f(3),f(4) in one gamma Z with gamma positive. No arithmetic restriction on f(0), since equal leaf count cancels it. No claim about all irrational weights.
- Prior 2^n collision and known sound irrational examples: original paper; readiness and prior review. The 2^n collision is explicitly credited on screen and in speech.
- Rank-two limitation: final paper remarks; this fixed-alphabet comparison fails to force a collision. Existence of a sound rank-two rule remains unsettled here.
- Novelty: bounded local priority review, moderate confidence. Correctness high; no Lean formalisation claimed.

Citation metadata for the additional background retrieval is retained in primary-source.json. The full response remains outside the repository; this is not a fresh exhaustive novelty audit.

Primary-source retrieval succeeded on 2026-10-26 via `valyu contents https://pmc.ncbi.nlm.nih.gov/articles/PMC6155497/ --length 25000 --json`. The soundness definition, Lemma 10 and conjecture passage were inspected in the returned text. `example-check.log` records a fresh successful illustrative checker run during video production.
