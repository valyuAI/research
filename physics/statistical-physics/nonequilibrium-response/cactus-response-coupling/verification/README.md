# Verification

| Script | Needs | Checks | Status |
|---|---|---|---|
| `check_cactus_lemmas.py` | Python 3 standard library | Exact rational checks: on bidirected cycles with n = 3..8 the arborescences rooted at r are the n cut trees and `w_r(k)/w_r(k-1) = a_k/b_k`; spanning-tree sets and laws factorise over blocks on five cacti; sampled dominant families on small cacti are uniquely constructable. Writes `cactus_lemmas_results.json`. | passes |
| `check_k4_obstruction.py` | Python 3 standard library | Enumerates the 16 arborescences per root and all 65536 tree families of the complete four-state digraph, marks the 346 uniquely constructable ones, computes the root laws exactly from the integer rates and replays the Farkas certificate `k4_no_coupling_certificate.json`. Writes `k4_obstruction_results.json`. | passes |
| `check_k4_subdivision.py` | Python 3 standard library | Subdivides the edge {0,1} of the certificate's K4 by a new state with the rates of Lemma 5.2(c), checks that contraction pushes every root law exactly onto the K4 root law, enumerates all 24^5 = 7962624 tree families (86150 distinct multisets, 984 uniquely constructable), checks that contraction maps every one of the 984 UC families to a UC family of K4, and replays the lifted certificate: nonnegative on every UC family, same negative expectation. Writes `k4_subdivision_results.json`. About 30 s. | passes |
| `numerical_evidence.py` | numpy, scipy | Floating-point evidence only: Monte Carlo of the edge-Gumbel coupling (cacti exact, diamond and per-arc noise wrong), coupling linear programs on series-parallel and K4-minor graphs, gradient searches for violations of the conjecture on K4 and for root pairs on K5. Fixed seeds; rerun on 26 October 2026 reproduced the stored JSON exactly (about 90 s). Writes `numerical_evidence_results.json`. | evidence |

```sh
python3 -B check_cactus_lemmas.py
python3 -B check_k4_obstruction.py
python3 -B check_k4_subdivision.py
python3 -B numerical_evidence.py   # optional, about two minutes
```

Scope. The cactus theorem rests on the written proof in `../paper.tex`; the exact scripts check its combinatorial identities on finite instances and do not replace the proof. The Gumbel-max lemma is used as a classical fact and is not re-verified. The K4 statement is fully certified by `check_k4_obstruction.py`: it is an exact Farkas certificate for the specific rates. The extension to every network with a K4 minor (Theorem 5.3) rests on the written proof of Lemma 5.2; `check_k4_subdivision.py` replays its suppression step exactly on one instance. Nothing here is formalised in Lean.

The certificate was found by a floating-point linear program in exploratory code and rounded to values in {-1, +1}; the checker is an independent standard-library implementation that does not reuse that code.
