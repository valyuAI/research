# Exact manipulability of tournament rules against three-team coalitions, up to eight teams

**Status:** theorem (finitely many cases), proved by exact certificates plus a known lower bound. New-result candidate after completed internal priority and adversarial reviews. Not externally refereed.

[Paper](../../../../public-release/papers/three-team-manipulation-exact.pdf) · [LaTeX](paper.tex) · [Verification](verification/README.md) · [Video brief](video-brief.md) · [Final readiness](readiness.md) · [Review response](review.md)

## Claim

A tournament rule picks a random champion from the results of a round robin. It is *k-SNM-alpha* if no coalition of at most k teams can raise its joint winning probability by more than alpha by fixing the matches among its members, and *Condorcet-consistent* (CC) if a team that wins every match always wins. Let alpha\*\_k(n) be the best alpha achievable by a CC rule on n teams.

- alpha\*\_3(n) = 2/5 for n = 5, 6, 7, 8.
- alpha\*\_3(3) = alpha\*\_3(4) = 1/3.
- alpha\*\_4(7) = 3/7.
- For k = 3 and every 3 <= n <= 8 the optimum is also attained by a rule that is monotone (a team never loses probability by winning one more match) and top-cycle consistent (zero probability outside the top cycle).

So if the conjectured value 2/5 fails for three-team coalitions at some size n, then n >= 9.

The lower bounds are Theorem 3.2 of Schneider, Schvartzman and Weinberg (arXiv:1605.09733, ITCS 2017): alpha >= (k-1)/(2k-1) for n >= 2k-1. The new part is the matching upper bounds: for each case an explicit neutral CC rule with rational probabilities whose largest gain over every coalition of size 2..k and every re-orientation of its internal matches is exactly the lower bound.

## Context

- Schneider, Schvartzman and Weinberg conjectured that (k-1)/(2k-1) is tight.
- Schvartzman, Weinberg, Zlatin and Zuo (arXiv:1906.03324v2, ITCS 2020) showed it fails for some large k; their argument rules out a 939-SNM-1/2 rule on 1878 teams. They ask how large k must be and say their work "does not rule out the existence of a 3-SNM-2/5 tournament rule". They also report exhaustive searches finding k-SNM-1/2 candidates for k, n <= 7.
- Best known for k = 3: 2/5 <= alpha <= 1/2. The upper bound is SignificantOnly (Miksanik, Schvartzman, Soukup, arXiv:2407.17569v1, defined for n >= 6); randomized death match is 3-SNM-31/60 (Dinev and Weinberg, arXiv:2301.07862). Papers from December 2025 (arXiv:2512.05235) and September 2026 (arXiv:2609.07062) still quote these bounds.
- arXiv:2407.17569 Section 5 suggests solving such linear programs for small n and k and attributes an LP to SSW17. We did not find computed optima there or anywhere else.

## What is new, and what is not

- New (as far as our searches show): the exact values above, with certificates; monotone, top-cycle consistent 3-SNM-2/5 rules for every n <= 8 (arXiv:2407.17569 asks for such a rule at n = 25, where it would imply alpha < 1/2 for all larger n); the observation that for k = 3 and 5 <= n <= 8 there is an optimal rule whose only manipulations of gain 2/5 are those in the lower-bound configuration (regular 5-team tournament plus losers).
- Not new: the lower bounds; the symmetrization (neutral rules suffice), which is a routine averaging argument; the idea of an LP for small n.
- Not claimed: anything for n >= 9 or for "all n"; any use in the n = 25 reduction of arXiv:2407.17569 (with n = 8 its bound gives 0.7, useless). For top-cycle consistent rules the optimum cannot decrease as n grows (add a team that loses every match), so a failure at some n would persist, but nothing extends our rules upward.

## Confidence

- Correctness of the stated values: high. Each upper bound is checked by a standard-library Python checker that recomputes isomorphism classes and enumerates every manipulation in exact arithmetic; the discovery code independently checks every LP row exactly. The lower bounds are published and re-derived in the paper.
- Originality: moderate. Searches (arXiv 2025 onward, Zenodo, GitHub, citing papers of SSW17, SWZZ20, Dinev-Weinberg, MSS24; two DeepResearch audits) found no prior exact computation. Small-n LP computations may exist unpublished.
- Significance: modest. It settles finitely many cases of an open question and gives evidence, not proof, that k = 3 is below the failure threshold.

## Method in one paragraph

Averaging any rule over relabellings gives a neutral rule that is no worse, so it suffices to choose one probability vector per isomorphism class of tournaments (6,880 classes at n = 8). The best alpha is then the optimum of a linear program with 54,256 variables and 2,667,216 distinct inequalities at n = 8. An interior-point solve at alpha = 2/5 lands in the relative interior of the optimal face, where only the lower-bound inequalities have zero slack. Rounding that point to rationals, restoring those few equalities exactly and rescaling gives an exact optimal rule.

## Reproduce

```sh
sh build.sh --quick   # checks n = 3..7 (k = 3), negative tests, builds paper.pdf
sh build.sh           # also checks n = 7 (k = 4) and n = 8 (k = 3); the n = 8 check is slow in pure Python
```

Needs Python 3 (standard library only), `pdflatex` and `bibtex`. See [verification/README.md](verification/README.md) for the certificate format, what the checker does, the results and the discovery pipeline.

## Provenance

- DeepResearch tasks: `socialchoice-snm-priority` (heavy, DR-080, priority audit) and `socialchoice-snm-review` (max, DR-040, adversarial review). The review's objections were addressed: the n = 8 value now rests on an exact certificate for the standard definition (coalitions of size at most 3) rather than a floating-point solve; SSW17 Open Question 1 is described as already resolved by SWZZ20; the 939/1878 figures, the RDM 31/60 analysis and SignificantOnly's n >= 6 restriction are stated as in the sources; the LP row count is explained.
- A side observation on Brandt and Lederer's weak-strategyproofness conjecture (arXiv:2412.11977) turned out to be already stated in their Remark 3 and is not included.
