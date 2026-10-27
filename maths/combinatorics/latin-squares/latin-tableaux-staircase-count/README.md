# Latin tableaux of shape (k, k-1, ..., 4, 3, 3)

**Status:** independent verification note (short induction plus a finite base case of 576 tableaux). The same formula and a four-extension proof were publicly recorded on 22 October 2026. No first-resolution claim. Research draft; not externally refereed.

[Paper](../../../../public-release/papers/latin-tableaux-staircase-count.pdf) · [LaTeX](paper.tex) · [Checker](verification/check_latin.py) · [Video brief](video-brief.md)

## Claim

For every k >= 5, the number of Latin tableaux of shape lambda_k = (k, k-1, ..., 5, 4, 3, 3) and type lambda_k' is

LT(lambda_k) = 9 * 4^(k-3)  (144, 576, 2304, 9216, ...).

A Latin tableau of shape lambda and type lambda' fills row i with 1, ..., lambda_i (each once) so that no column repeats an entry. In particular every lambda_k is Latin; these partitions are wide, so the wide partition conjecture on free matroids (Chow-Fan-Goemans-Vondrak) holds for this family.

Also: explicit tableaux for the six wide shapes listed after Conjecture 6.3 are in `verification/six_shapes.json`. These are independently checked examples, not new existence results: each has 32 cells and lies within the earlier finite verification reported by Chow-Fan-Goemans-Vondrak.

## Source of the question

Daugherty, Fahnestock, Huxtable, Larson, Al Munayes, Peacock, *Counting and constructing Latin tableaux*, arXiv:2610.29291v1 (21 October 2026), Section 6, Conjecture 6.3, asks for this exact formula. Their discussion concerns the lack of a general result for the family; it does not erase earlier finite verification of Latinness. The cases through k = 10 already fit within the finite verification reported in the 2003 paper.

The public [proof in issue #20269](https://github.com/the-omega-institute/trureturing/issues/20269) and [merged PR #20329](https://github.com/the-omega-institute/trureturing/pull/20329), dated 22 October 2026, give the same formula and the same four-extension mechanism. Both pages were retrieved with Valyu Contents on 26 October 2026. The earlier description of that issue as a preregistration without a solution was wrong. This package retains its independently developed proof and reproducible checks as a verification note. The external Lean development has not been replayed here.

## Proof idea

Deleting the top row of a tableau of shape lambda_k leaves a tableau of shape lambda_{k-1}. Five invariants (I1-I5 in the paper) describe the top row and the column contents: the top row is a permutation of {k-2, k-1, k}, then the forced values k-3, k-4, ..., 4, then a permutation of {1, 2, 3}. If a tableau of shape lambda_{k-1} satisfies the invariants, the new top row is forced up to two independent binary choices (one in the first three columns, one in the last three), and all four extensions again satisfy the invariants. All 576 tableaux of shape lambda_6 satisfy them (finite check), so LT(lambda_k) = 576 * 4^(k-6).

## Evidence

- `verification/check_latin.py` (standard library, no assertions): enumerates lambda_5 and lambda_6 two ways (144 and 576), checks I1-I5 on all 576 base tableaux, confirms 9 * 4^(k-3) by enumeration for k <= 7 (k <= 9 with `--full`; a separate run reached k = 10, 147,456 tableaux), checks the invariants and the "exactly 4 extensions" property for k = 6, 7 (to 8 with `--full`), and checks wideness of lambda_k for k <= 15 from the definition. Results go to `verification/results.json`.

## Confidence

- Correctness: high. The induction is short and fully written; the base case is a finite enumeration replicated two ways; the conclusion is cross-checked by brute force up to k = 10.
- Originality: no first-resolution claim. An earlier public proof covers the same formula and mechanism. Confidence in this priority overlap is high after direct inspection of both pages.
- Significance: an accessible independent reconstruction with executable checks. It should not be counted as a new discovery. The general wide partition conjecture and Rota's basis conjecture are untouched.

## Reproduce

```sh
sh build.sh          # checker (about a minute) and paper.pdf
sh build.sh --full   # longer enumeration (k <= 9)
```

## DeepResearch tasks

- `scout-algebra` DR-054 (scouting; listed this conjecture as candidate 1)
- `algebra-latin-review` DR-004 (adversarial review and priority check)
