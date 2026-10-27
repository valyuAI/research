# Reduced graphs with four negative eigenvalues have at most thirty vertices

**Claim (computer-assisted theorem).** A graph is reduced if it has no isolated vertices and no two vertices with the same neighbourhood. Every reduced graph with exactly four negative adjacency eigenvalues has at most 30 vertices. This proves Mohammadian's conjectured bound 2^{k+1} − 2 at k = 4, the first open case. Exactly four reduced graphs attain 30 vertices: the four largest reduced graphs of rank 8, already computed by Akbari–Cameron–Khosrovshahi (2004), which arise from K₂ by their Constructions A (Kotlov–Lovász) and B. New here is that no other rank reaches 30, and that all four have inertia (4,22,4).

**Second result (classification).** Every graph with exactly four negative eigenvalues has at most eleven positive ones, so Torgašev's A₄ = 11. Up to twins and isolated vertices, exactly two graphs attain this. Equivalently, exactly two graphs on 15 vertices have only four nonpositive eigenvalues. The two graphs are:

- W₅: K₅ plus the Petersen graph on its 2-subsets, with each point joined to the pairs containing it;
- X: the 3×3 rook graph (Paley(9)) plus the six lines of the two diagonal parallel classes of AG(2,3), with parallel lines adjacent.

Both appear in Charles–Farber–Johnson–Kennedy-Shaffer (CFJK, Discrete Math. 313 (2013), [arXiv:1108.4810](https://arxiv.org/abs/1108.4810)) as G₄ and G₅. The bound A₄ ≤ 11 is equivalent to CFJK's computer-proved NPO(5) = 16, via the identity M(k) = P(k) + k of Elphick–Kumar–Pragada–Spier ([arXiv:2609.06319](https://arxiv.org/abs/2609.06319)). The new parts are uniqueness and an independent proof.

[Paper](../../../../public-release/papers/four-negative-eigenvalues.pdf) · [LaTeX](paper.tex) · [References](references.bib) · [Verification](verification/README.md) · [Video brief](video-brief.md) · [Final readiness](readiness.md) · [Review response](review.md)

## Status

| | |
|---|---|
| Type | Computer-assisted theorems: a complete exact enumeration with a written completeness proof |
| Open question settled | Mohammadian's conjecture (Linear Algebra Appl. 640 (2022) 6–11; restated as Conjecture 2.2 of Akbari et al., Discrete Math. 349 (2026) 114953, [arXiv:2508.01163](https://arxiv.org/abs/2508.01163)), case k = 4. It was known for k ≤ 3 from Torgašev's values 2, 6, 14. |
| Also new | Uniqueness of the two extremal graphs for A₄. The census of all 45,242 nonsingular graphs with n⁻ ≤ 4; orders 8–15 are new, and orders 4–7 match Akbari–Cameron–Khosrovshahi (2004). The largest reduced order for each rank with n⁻ = 4. An independent proof of NPO(5) = 16. |
| Closest prior work | Basso (LAA 618 (2021) 144–149) proved n(k) ≤ 2R(k+2) (Ramsey) and a two-consecutive-orders termination criterion close to our Theorem 3.3, but did not compute k = 4. Ghorbani–Mohammadian–Tayfeh-Rezaie (Combinatorica 35 (2015), [arXiv:1201.3060](https://arxiv.org/abs/1201.3060)) record that the Akbari–Cameron–Khosrovshahi rank bound m(r) is verified for rank ≤ 9; this gives ≤ 30 vertices for ranks ≤ 8 but only ≤ 38 at rank 9 and nothing for ranks 10–15, so the condition n⁻ = 4 is what does the work. The nonsingular-basis lemma is Ellingham (1993) and Elphick et al. Lemma 2.3. The order computation (basis plus clique of isotropic vectors) is the Akbari–Cameron–Khosrovshahi algorithm, and their Table 1 already lists exactly four reduced graphs of rank 8 and maximum order (31 in their convention, which allows one isolated vertex). The termination clause of our closure theorem is also close to the 'no 001' theorem for principal rank sequences (Brualdi–Deaett–Olesky–van den Driessche 2012). |
| Not new | A₄ = 11 itself. It follows from CFJK (2013) and Elphick et al. (2026), although Chen–Li ([arXiv:2605.07196](https://arxiv.org/abs/2605.07196)) still called n⁻ = 4 unsettled in May 2026. The graphs W₅ and X are also not new. |
| Correctness confidence | High. An independent reviewer recomputation reproduced the census through N = 9 and the per-rank maxima for ranks 5–9 and 15. Two implementations of the enumeration agree (they share the closure theorem but not code). An exact re-verification of every listed graph found no failures. Brute force agrees through 10 vertices. The run reproduces Akbari–Cameron–Khosrovshahi's Table 2 for all reduced graphs of rank ≤ 7 with t ≤ 4, Torgašev's values for k ≤ 3 including his 32 maximal canonical graphs, and CFJK's NPO(5) = 16. |
| Originality confidence | Moderate for n(4) = 30 and uniqueness. Three DeepResearch audits and our own searches found no earlier statement. Residual risk: Torgašev, *Minimal graphs with four negative eigenvalues* (An. Şt. Univ. Iaşi 33 (1987) 283–287) and Mohammadian's 2022 full text could not be read; the former is about minimal (smallest) graphs, and Torgašev in 1990 still listed A_k only for k ≤ 3. The order-30 graphs themselves and their count are not new (ACK 2004). |
| Formalization | None |

## How the proof works

1. **Reduction.** Every graph contains a nonsingular induced subgraph with the same n⁺ and n⁻ (Lemma 2.1).
2. **Closure (Jacobi minors).** Every nonsingular graph is obtained from a smaller one by adding one vertex, or by adding two isotropic vertices; in the second case the inertia changes by (1,0,1) (Lemma 3.2, Theorem 3.3). If two consecutive levels of the generation are empty, every later level is empty too.
3. **Exact enumeration.** All signs are signs of integer quadratic or bilinear forms in the adjugate. For n⁻ = 4, the nonsingular counts at orders 5–15 are `1, 17, 295, 3648, 10384, 14422, 10810, 4473, 993, 110, 2`, and orders 16 and 17 are empty.
4. **Maximum order.** A reduced graph is a nonsingular basis X together with a clique of pairwise compatible isotropic 0/1 vectors. Exact clique numbers give the largest reduced order for each rank 5..15: `5, 10, 18, 30, 26, 22, 20, 17, 15, 15, 15`. A second implementation (exact rational inversion and its own clique search) agrees.

## Reproduce

```sh
bash build.sh                       # standard-library check of W5 and X, then build the PDF
uv venv .venv && uv pip install --python .venv numpy networkx python-flint==0.9.0 pynauty==2.8.8.1
PYTHON=.venv/bin/python bash build.sh --full   # full replay; needs nauty's geng; roughly 1-2 hours
```

The runs used Python 3.13.7, numpy 2.4.6, networkx 3.6.1, python-flint 0.9.0, pynauty 2.8.8.1 and nauty 2.9.3. Each script and its expected output are listed in [verification/README.md](verification/README.md).

## What is and is not claimed

- **Claimed:** n(4) = 30, attained by exactly four reduced graphs, all of rank 8 with inertia (4,22,4) (the four graphs are ACK's; the exclusion of all other ranks is new). A question (paper, Section 7): does every reduced graph with k negative eigenvalues and 2^{k+1} − 2 vertices have rank 2k? True for k ≤ 4. A₄ = 11, with W₅ and X the only reduced extremal graphs. The census in Table 1.
- **Not claimed:** anything proved for k ≥ 5. Known: A₅ ≥ 16 (W₆, its three CFJK variants and CFJK's G₆). CFJK suspect NPO(6) = 22, i.e. A₅ = 16. Evidence only: none of the six known 21-vertex (16,0,5) graphs has a 22nd-vertex extension keeping n⁻ = 5 (exact check of all 2²¹ neighbourhoods, `verification/k5_extension_check.py`), and heuristic beam searches over nonsingular graphs with n⁻ = 5 stopped at 21 vertices. No asymptotics; no Lean proof.
- **Proof versus computation:** Lemmas 2.1–3.2 and Theorem 3.3 are proved in the paper. The rest is finite exact computation, replayed by the scripts.

## Provenance

DeepResearch tasks `graphs-priority-a4` (DR-091, priority audit), `graphs-review-a4` (DR-087, adversarial review of the first draft) and `graphs-review-final` (DR-063, max-mode adversarial review of the final claims). The first review found the CFJK precedent, which changed the framing of this package. The final review found no mathematical error, reproduced the census through 9 vertices and the per-rank maxima for ranks 5–9 and 15, found no prior statement of n(4) = 30 or of the uniqueness, and pointed to ACK's Table 1 (four maximum rank-8 graphs), the ACK algorithm and the 'no 001' theorem; all are now credited.

## Priority checks (26 October 2026)

| Where | What was searched | Result |
|---|---|---|
| arXiv | Title search "inertia graph" sorted newest (latest relevant: 2605.07196); title search "negative eigenvalues graph"; author listings for Elphick, H. Kumar, Pragada, Mohammadian and Spier through 2610.13852 | No paper on n(4), A₄ or Mohammadian's conjecture after 2609.06319 |
| Zenodo | REST API queries: "negative eigenvalues" with reduced/twin; Mohammadian; Torgašev; "positive inertia"; "nonpositive eigenvalues"; "four negative eigenvalues" | Nothing relevant. The only "nonpositive eigenvalues" hit (record 22063302) is unrelated. |
| GitHub | `gh search issues/repos` on Mohammadian, Torgašev, twin-free negative eigenvalues and NPO; Valyu search of the-omega-institute/trureturing and google-deepmind/formal-conjectures | No issue, repository or formalization found |
| Literature (26 Oct) | Valyu paper/web search: "twin-free graph negative eigenvalues log2(n+2)", "reduced graph exactly four negative eigenvalues maximum order", "Mohammadian conjecture ... 2^{k+1}-2 proof", "graphs with four negative eigenvalues classification 2026"; read Basso (2021) in full (open access) and the computational remark in Ghorbani–Mohammadian–Tayfeh-Rezaie (2015) | Basso and GMT added as closest prior work (see Status). No statement of n(4) = 30, of the order-30 classification, or of the uniqueness for A₄ |
| Other | pith.science (reviews of 2605.07196 and 2609.06319); Valyu web search on the result statements | Nothing beyond the papers above |
| DeepResearch | `graphs-priority-a4` (heavy) and `graphs-review-a4` (max) | The review found the 2013 CFJK precedent for A₄ ≤ 11 and for both extremal graphs; neither task found n(4) or the uniqueness statement |

Not accessible: Torgašev, *Minimal graphs with four negative eigenvalues* (1987); Torgašev's 1985 Dubrovnik paper; the Cvetković–Doob–Gutman–Torgašev monograph; Mohammadian's 2022 full text (only the abstract was read).
