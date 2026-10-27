# Infinite words avoiding long Cartesian-tree squares

**Claim.** There is an infinite binary word with no Cartesian-tree square `uv` with `|u| = |v| >= 4`, and an infinite ternary word with no Cartesian-tree square with `|u| = |v| >= 3`. Both are explicit: apply

```text
h2:  a -> 00101    b -> 00111    c -> 01100     (binary, 0 < 1)
h3:  a -> 000101   b -> 000221   c -> 022211    (ternary, 0 < 1 < 2)
```

to any infinite ternary word with no factor of exponent greater than 7/4 (these exist by Dejean's theorem, for example the fixed point of `a -> abcacbcabcbacbcacba`, `b -> bcabacabcacbacabacb`, `c -> cabcbabcabacbabcbac`).

**Status.** Computer-assisted theorem. A written reduction (Proposition 3.1 of the paper) turns the claim into three finite checks, and two independent programs perform them.

**What it settles.** Shibata, Mieno, Köppl and Inenaga, [*Relaxation of Square-Freeness*](https://arxiv.org/abs/2607.00674) (v2, 14 July 2026, accepted for PSC 2026), Table 1, Cartesian-tree equivalence: the entries (sigma, l) = (2, 4) and sigma = 3, 4, 5 with l = 3, 4 are marked "?", "a case that remains open". Their Table 2 conjectures infinity for (2, 4) and (3, 3) "based on experimental results". The version in the PSC 2026 proceedings (August 2026) keeps the same conjecture. This finding proves both conjectures, so every "?" entry is infinity. The thresholds are sharp by their finite entries 29 (sigma = 2, l = 3) and 9 (sigma >= 3, l = 2).

[Paper](../../../../public-release/papers/cartesian-tree-square-free-words.pdf) · [LaTeX](paper.tex) · [Verification](verification/README.md) · [Video brief](video-brief.md)

## Definitions in one paragraph

`PD(x)[i] = i - max{j < i : x[j] <= x[i]}`, or 0 if there is no such `j` (parent-distance encoding, Park, Amir, Landau and Park, CPM 2019, Definition 2). Two words of equal length have the same Cartesian tree exactly when their encodings agree; this is also the encoding in the source authors' software (`psv_encoding` in github.com/koeppl/squarechecker). A Cartesian-tree (CT) square is a factor `uv` with `PD(u) = PD(v)`.

## Proof outline

For a q-uniform morphism `h` and an infinite 7/4+-free ternary word `w`:

1. (S) `h` is injective on letters and synchronizing, so block images in `h(w)` occur only at multiples of q.
2. (D) Local decoding with radius r = 3: two factors of `h(w)` of length 7 with equal encodings have equal middle letters. Restricting encodings to windows (Lemma 3.3) then shows that the two halves of a CT-square of half-length m agree outside their first and last r letters.
3. Long squares: for m > M = 4(2r + 2q - 2) the agreeing middle part contains whole blocks, which forces a factor of `w` of exponent at least `2 - (2r+2q-2)/m > 7/4`. This is impossible.
4. (F) Short squares, half-length l <= m <= M, are excluded by checking `h(f)` for every 7/4+-free ternary word `f` of length K: 4,596 words of length 24 for `h2` (M = 56), 3,654 words of length 23 for `h3` (M = 64).

## Reproduce

From this directory (Python 3 standard library; clang or gcc optional; pdflatex and bibtex for the PDF):

```sh
sh build.sh
```

This runs `verification/controls.py` (encoding agrees with the source software, reproduces the finite entries 1, 5, 29 and 9 of their table, rejects corrupted morphisms), `verification/check_ct.py A B` (independent standard-library check of (S), (D) and (F), about 30 s per morphism, writes `results_check_ct.json`), the C implementation `verification/ctproof.c`, and then builds `paper.pdf`.

## Confidence

- **Correctness: high.** The deduction is a short written argument; the finite inputs are checked by two separately written programs that agree on every count, and controls show the checks reject wrong inputs. No Lean formalization.
- **Originality: moderate.** The source paper is from July 2026 and its PSC 2026 proceedings version still states the conjecture. The priority audit (task `c509ecab`, 26 October 2026) checked arXiv, the proceedings, the authors' pages and repository, aggregators (alphaXiv, papers.cool) and the AI-research issue tracker the-omega-institute/trureturing, and found no resolution and no source stating these morphisms. The only CT-square literature found is algorithmic (counting CT-squares, arXiv:2509.02179). Residual risk: the authors' repository has a `findmorphism.py --type CARTESIAN` tool, so they may hold an unpublished result; its public commit history (six commits, last on 17 March 2026) contains neither morphism.
- **Significance: modest.** It completes a table in a recent stringology paper and confirms its conjecture. The reduction lemma (Lemma 3.4, CT-squares are near-squares) is the only new idea and may help with the authors' suggested next questions on Cartesian-tree repetition thresholds.

## Priority checks performed (26 October 2026)

- **arXiv** (API, sorted by submission date, from 2026-09-01): abstracts containing "Cartesian tree", "Cartesian-tree", "square-free", "squarefree", "order-preserving" with "square", "parameterized" with "square-free"; author listings for Mieno, Köppl and Shibata. Only unrelated papers (CT-Miner 2610.05330, permutation statistics 2610.01077, number theory); no follow-up by the authors since 2607.00674.
- **Zenodo** (REST API): `"Cartesian tree" AND square`, `"Cartesian-tree square"`, `title:"Cartesian tree"`, `"Relaxation of Square-Freeness"`, `"parent-distance" AND square`: no relevant record.
- **GitHub**: API search for repositories and issues on Cartesian-tree square-freeness (none relevant); commit history of `koeppl/squarechecker` (last commit 17 March 2026, "add short square checker"); the-omega-institute/trureturing issue searches for "2607.00674", "Shibata", "Inenaga", "Cartesian", "CT-square" (nothing relevant).
- **Source authors**: arXiv v2 and the PSC 2026 proceedings PDF (stringology.org/papers/PSC2026.pdf) still state the conjecture; Köppl's and Shibata's publication pages list no follow-up (Mieno's and Inenaga's pages not retrieved).
- **Aggregators and web search**: alphaXiv and papers.cool show only the abstract; web searches for Cartesian-tree square avoidability, including pith.science and vibemathed.com, found nothing. erdosproblems.com is not relevant (not an Erdős problem).
- DeepResearch priority audit `c509ecab` (heavy) reached the same conclusion; the only CT-square literature is algorithmic (arXiv:2509.02179).

## Review

The adversarial review (DeepResearch max task `efbe8c3a`, 26 October 2026) re-derived each step, recomputed (D) and (F) with its own code, including a third method that tests Cartesian-tree equivalence through leftmost minima of all intervals, and found no error and no CT-square. Its corrections are incorporated: the statement is for infinite base words (finite base words would need all lengths up to K; both verifiers run this stronger check, 21,801 and 17,205 words, no CT-square, but the paper states only the infinite version); the bound in the long-square step equals 7/4 exactly at m = M, so m = M belongs to the finite check; the window lemma is Fact 16 of arXiv:2602.08570 and is credited. The review confirmed that the parent-distance encoding with `<=` matches leftmost-minimum Cartesian trees, the convention of the source.

## Independent review

A second, independent referee report (26 October 2026) found the result correct with fixable gaps: correctness confidence high, priority confidence moderate. It re-derived the reduction, rechecked (S), (D) and (F) with a fresh implementation that compares Cartesian-tree shapes directly rather than parent distances (same counts and base-word hashes, no CT-square), and replayed `build.sh`. Three minor corrections are applied:

1. The abstract and the verifier docstrings now state the theorem for infinite 7/4+-free base words, matching Proposition 3.1 and Corollary 4.2. (A finite free word need not extend: `abacaba` has no 7/4+-free one-letter right extension.) The verifiers do run the stronger all-lengths check, and the referee repeated it independently, but the paper does not claim the finite version.
2. Remark 4.3: at a binary descent preceded by a run of t ones, the parent distance is t + 1 if a zero precedes the run and 0 if the run starts the word (previously misstated as t).
3. Section 5: the negative search results (no 4-uniform binary, no 5-uniform ternary triple) hold within injective synchronizing uniform morphisms, since `morphbt.c` rejects non-synchronizing triples.

None of these affects Theorem 1.1.

## Provenance

Found and verified in the 2026-10-25 research campaign (cell `tcs`). The morphisms came from an exhaustive backtracking generator (`verification/morphbt.c`); a random search over unrestricted ternary images of lengths 4 to 16 found nothing, so the exhaustive search was needed for the ternary case. DeepResearch tasks: scouting `DR-088` (scout-tcs-small-instances) and `DR-067` (tcs-fresh-open, which surfaced the open table cells); priority audit `DR-076` (tcs-ct-priority); adversarial review `DR-089` (tcs-ct-review).
