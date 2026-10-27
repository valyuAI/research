# Short forced wins in small Hex

How cheaply can the first player force a win at Hex? Campbell (2004) measured this in two ways: $\lambda(n)$, the shortest top-bottom path that Blue (moving first) can force on the $n\times n$ board, and $\delta(n)$, the fewest Blue stones with which Blue can force a win. He conjectured $\lambda(5)=\delta(5)=7$ and $\lambda(6)=\delta(6)=9$. A July 2026 preprint (Casco, Pacifico and Sanhueza, [arXiv:2607.28138v1](https://arxiv.org/abs/2607.28138)) claims a proof that $\lambda(5)=7$ and lists $\lambda(6)$ and $\delta(6)$ as "the most immediate open problem", conjecturing $\lambda(6)=\delta(6)=9$.

Exhaustive search with replayable certificates gives the bold values (those for $n\le4$ are classical; see Campbell):

| | $n=2$ | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|
| $\lambda(n)$ | 2 | 3 | 5 | **6** (conjectured 7; claimed proved 7) | **8** (conjectured 9; $\le8$ by search only) |
| $\delta(n)$ | 2 | 3 | 5 | 7 | **10** (conjectured 9) |

[Paper](../../../../public-release/papers/hex-short-wins.pdf) · [LaTeX](paper.tex) · [Verification](verification/README.md) · [Video brief](video-brief.md)

## Status

- **Theorem (computer-assisted, certificates replayed by an independent checker).**
  1. $\lambda(5)=6$. Opening in the centre, Blue forces a top-bottom path of at most six cells; Red prevents every path of at most five cells after every opening. The same value holds under the strict reading in which ordinary Hex ends at the first connection and that connection must contain a path of at most six cells: $\lambda^*(5)=6$.
  2. $\delta(5)=7$, by certificates independent of the flawed deduction in arXiv:2607.28138.
  3. $\delta(6)=10$. Red stops every Blue connection made with at most nine stones, after each of the 36 openings; Blue wins with at most ten stones by opening at $(3,4)$ or $(4,3)$, the two central cells of the short diagonal.
  4. $\lambda(6)\ge8$. Red prevents every Blue path of at most seven cells, after each of the 36 openings.
  5. Every value in the $5\times5$ opening tables (Figure 1 of the paper) is certified.
- **Computation: $\lambda(6)\le8$, hence $\lambda(6)=8$.** Blue wins $\mathrm{Hex}(6,8)$ by opening at $(3,4)$, found by exhaustive search ($2.9\times10^9$ positions) but not replayed: a Blue certificate would be far larger than the others.
- **Consequences.** Campbell's Conjecture 19 ($\lambda(5)=7$) and Conjecture 20 ($\delta(6)=9$) are false, and so is the $n=6$ half of Conjecture 19 given the search result $\lambda(6)\le8$. Theorem A of arXiv:2607.28138v1 ($\lambda(5)=7$) and its Lemma 5 are false under either reading of the rules. $\lambda(5)<\delta(5)$, so the two parameters already differ at $n=5$, which answers the question of that preprint whether $\lambda(n)=\delta(n)$ for all $n$. The proposed pattern $\lambda(n)=\delta(n)=2n-3$ fails at $n=5$ (for $\lambda$) and $n=6$ (for $\delta$).

## Closest prior work and what is new

- G. Campbell, INTEGERS 4 (2004) #G02: definitions, $\lambda(n)>n$ for $n\ge4$, $\delta(n)\ge n+\lfloor n/4\rfloor$, $6\le\lambda(5)\le\delta(5)\le7$, Conjectures 18 to 22.
- W. Stromquist, INTEGERS 7 (2007) #G05: $\lambda(n)\ge n+\lfloor (n-2)/4\rfloor$ (via $n\times\infty$ Hex).
- S. Casco, M. J. Pacifico, D. Sanhueza, arXiv:2607.28138v1 (30 July 2026): claims $\lambda(5)=7$ by hand case analysis. Its Lemma 5 fixes Blue's winning path before Red replies; an adaptive strategy does not. Our certificate exhibits a six-cell win.
- **KataHex (HZY, DEV Community, 8 September 2024; MathOverflow question 302821).** A self-play Hex network estimated the optimal $6\times6$ game length (first player hurrying, second delaying) at 19 moves, i.e. $\delta(6)=10$ by Campbell's relation depth $=2\delta-1$, and 25 moves for $7\times7$. Its author stresses it is "NOT a exhaustive search" and "can't be called a 'proof'". **This estimate predates our work and agrees with it; we prove the value.** No source we found states $\lambda(5)=6$, $\lambda(6)=8$, or a proof of $\delta(6)=10$.

New here: the values $\lambda(5)=\lambda^*(5)=6$ and $\delta(6)=10$ with checkable certificates, the computed value $\lambda(6)=8$, the identification of the optimal openings, and the error in Lemma 5 of arXiv:2607.28138v1.

## Confidence

- Correctness of the certified statements: **high**. Every certificate is replayed by a standard-library Python checker that shares no code with the search, enumerates the winning paths from scratch, tries every empty cell as the opponent's reply, and detects wins by breadth-first search on the actual stones. Mutation tests confirm it rejects corrupted certificates. The soundness argument for keying positions is in Section 3 of the paper. Residual risk: a shared misreading of the rules, addressed by quoting Campbell's definitions and by proving $\lambda(5)=6$ under both readings.
- $\lambda(6)\le8$: **moderate**; a single exhaustive search by the same program family that produced every certified value, not independently replayed.
- Originality: **moderate**. Searched arXiv listings, Zenodo, GitHub, MathOverflow, Semantic Scholar and the Valyu search index up to 26 October 2026, plus two DeepResearch audits (below). Nothing states these values except the KataHex estimate of $\delta(6)$ via game length.

## Reproduce

```sh
sh build.sh            # 5x5 certificates (shipped), mutation tests, figures, PDF: a few minutes
sh build.sh full       # also regenerates and replays the 6x6 and strict certificates: several hours
```

Requirements: Python 3 (standard library only) for the checkers; a C compiler for the search; `pdflatex` and `bibtex` for the paper. The 100 main $5\times5$ certificates and a small strict-game control certificate are shipped. The $6\times6$ certificates (up to 122 MB each) are not shipped; the search program regenerates them deterministically in seconds to minutes and the checker replays them. See [verification/README.md](verification/README.md) for every command, the certificate format and run times.

## Provenance

Valyu DeepResearch tasks: `recreational-hex-priority` (heavy, DR-065; priority and literature audit), `recreational-hex-review` (max, DR-002; adversarial review, see [review notes](verification/review.md)). Valyu Search and Contents were used to read Campbell (2004), arXiv:2607.28138v1, the KataHex post and MathOverflow question 302821.

## Limitations and open questions

- No Lean formalization; correctness rests on the replayed certificates and the written soundness argument.
- $\lambda^*(6)$ (strict reading on $6\times6$) is not determined; $8\le\lambda^*(6)\le10$.
- $\lambda(7)$, $\delta(7)$ (KataHex suggests $\delta(7)=13$), and $\delta(5\times\infty)\in\{6,7\}$ remain open.
