# No distinct covering with minimum modulus 6 and moduli dividing 2^a · 45

**Status:** theorem, proved by a short lemma plus an exhaustive finite computation that three independent implementations replicate (two in C, one in standard-library Python). Not formalised in Lean. Not externally refereed.

**Claim.** For every a ≥ 0 there is no finite system of congruences with pairwise distinct moduli, each at least 6 and dividing 2^a · 3^2 · 5, that covers the integers.

This answers **Problem 2** of Harrington, Klein, Lowrance and Trifonov, [*Covering systems where the prime divisors of all moduli are only 2, 3, or 5*](https://arxiv.org/abs/2605.18644) (arXiv:2605.18644v1, 18 May 2026). They asked whether some a gives a distinct covering with minimum modulus 6 and LCM 2^a 3^2 5, and conjectured that none exists. Their abstract describes the open m = 6 case as "b = c = 1". Their Theorem 1.8(i) shows b ≥ 2, and parts (ii)-(viii) settle every other exponent pattern, so the case actually left open is b = 2, c = 1. That case is this one, so the result completes their description of the quadruples (6, a, b, c). For a ≥ b ≥ c ≥ 1, a distinct covering with minimum modulus 6 and LCM 2^a 3^b 5^c exists if and only if c ≥ 2 and (a ≥ 5, or a = 4 and b ≥ 3), or c = 1 and (a ≥ 6 and b ≥ 3, or a = 5 and b ≥ 4) (paper, Corollary 1.3). A further consequence: every distinct covering with minimum modulus at least 6 and 5-smooth LCM has 27 | L or 25 | L, which is relevant to the paper's Problems 1 and 3 for finite coverings.

[Paper](../../../../public-release/papers/min-modulus-six-odd-part-45.pdf) · [LaTeX](paper.tex) · [Verification](verification/README.md) · [Video brief](video-brief.md)

## Idea in four lines

1. Write residues mod 2^k·45 as pairs (x, y), with x = b mod 2^k and y = b mod 45. The uncovered y's above each x form a "column".
2. Fix prices ρ_d ≥ 0 for the six divisors d of 45. Let φ(S) be the cheapest way to cover S ⊆ Z/45 by classes mod divisors of 45, and let Q = Σ φ(column).
3. **Doubling lemma:** going from 2^k to 2^(k+1), every column splits into two copies, and each modulus 2^(k+1)d contributes one class. Hence Q' ≥ 2Q - R, where R = Σ ρ_d. Once Q ≥ R, Q never drops below R, so the system can never become a covering. This holds for every a, including arbitrarily large ones.
4. **Computation:** every system with moduli in {6, 9, 10, 12, 15, 18, 20, 30, 36, 45, 60, 90, 180} already has Q ≥ R for one of 11 explicit integer price vectors ([`verification/prices.txt`](verification/prices.txt)). An exhaustive depth-first search with an exact cover routine and a pruning bound proves this.

## Evidence

| Check | What it does | Result |
|---|---|---|
| `verification/c/dfs2.c` | DFS over the 14 orbits of level-0 classes under (S3 wr S3) × S5, with tree symmetry | 498,464 nodes, **0 survivors** |
| `verification/check_p2.py` | Standard-library Python; residues mod 45 directly; translations only (135 roots); independently coded exact cover, self-tested against exhaustive search | 4,684,432 nodes, **0 survivors** |
| `verification/c/gen.c` | Generic code (odd part 3^B·5): exact cover by dynamic programming over the 3-adic tree, symmetry by swapping identical sibling subtrees, rows and 2-adic halves; level-0 moduli may be skipped | 66,821 nodes, **0 survivors** |
| `verification/c/dfsg.c` | Translations only, no tree symmetry | Partial run: 17.8M nodes explored, 0 survivors; stopped to free CPU |
| Negative control 1 | Same searches with only the first 10 price vectors | 1704 survivors in `dfs2.c` (orbits 3 and 8). The Python checker reproduces the orbit-3 figures exactly (200,024 nodes, 1,560 survivors) |
| Negative control 2 | `verification/control_m4.py`: a minimum-modulus-4 covering with moduli dividing 360 (CP-SAT) | Its level-2 state is alive under all 11 vectors, as the lemma requires. The level-2 part of the source paper's infinite covering has Q_2 = R exactly for vectors 3, 9 and 10 |
| Calibration | `verification/calib.py` grows its own prices from scratch for other (odd part, minimum modulus) pairs | Proves the known negative cases (9, 4) and (15, 5); reports alive states for (9, 3) and (27, 4), where coverings exist |
| `verification/c/test_phi.c` | Structured exact cover vs brute-force branching | 20,000 random instances, 0 mismatches |

**Confidence.** Correctness: high. The lemma is elementary, and the computation is small (0.5M to 4.7M search nodes depending on the symmetry used). It is replicated by three independent implementations, two of which agree node for node on shared roots, and the adversarial review found no error in the argument. Originality: moderate. A heavy DeepResearch audit (task `DR-090`, 26 Oct 2026) found no resolution of Problem 2 and no lemma of this form. We also checked arXiv listings for "covering system" through 2610.05149, Zenodo, GitHub (trureturing, We-Solve, Foundation-0, formal-conjectures) and erdosproblems.com threads. An adversarial max-mode review (task `DR-073`) found no error and no prior art; it is summarised, with our responses, in [`review.md`](review.md). A search that finds nothing does not prove novelty.

**What is not claimed.** Nothing about infinite coverings: Theorem 1.10 of the source paper builds an infinite distinct covering with these moduli, and the potential argument is consistent with it. Problems 1 and 3 of the source paper remain open. The only consequence drawn here is the divisibility condition above, which applies to finite coverings.

## Reproduce

```sh
sh build.sh            # compiles and runs the C checks (about 2 minutes), then builds paper.pdf
python3 -B verification/check_p2.py verification/prices.txt          # independent check, 135 roots
python3 -B verification/check_p2.py verification/prices.txt 0 45     # or split into slices
```

The Python checker needs only the standard library. On a heavily loaded laptop it took about 65 minutes per 45-root slice. The C checks need a C compiler. `verification/discover_prices.py` (needs numpy and scipy) shows how the prices were found; verification does not need it.

## Side remark (erratum)

The system 1 mod 6, 6 mod 8, 0 mod 9, 8 mod 10, 5 mod 12, 5 mod 15, 3 mod 18, 12 mod 20, 10 mod 24, 14 mod 30, 23 mod 36, 16 mod 40, 24 mod 45, 40 mod 60, 66 mod 72, 33 mod 90, 26 mod 120, 11 mod 180 and 359 mod 360 leaves 51 residues mod 360 uncovered. The source paper's table lists 52 for L = 2^3·3^2·5. The theorem does not depend on this.

## Provenance

Found in the Valyu Research campaign of 25-26 October 2026 (cell `erdos`). Literature scouting used Valyu Search, Contents and DeepResearch. The price vectors come from alternating the exhaustive search with a column-generation linear program: for each surviving system, find prices that make it dead, then add them. Exploratory CP-SAT searches with the same model did not terminate; the custom search with multi-price pruning finishes in about a minute.
