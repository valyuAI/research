# Verification

All programs build the 7x7x7 board and its 193 lines from scratch. None of them reads data produced by another.

| Program | Language | What it checks | Runtime (loaded laptop) |
|---|---|---|---|
| `surplus_certificate.py` | Python 3, standard library | Proposition 3.1 on 66 symmetry classes and the 10,627-leaf pattern tree. Proposition 3.2 on 1,158 symmetry classes. Writes `results/surplus_python.json`. | about 6 min with 3 workers |
| `surplus7.c` | C | Exact surplus (capped at 4) for all 1,296 central-case Breaker sets (`./surplus7 1`) and all non-central configurations (`./surplus7 2`). No symmetry reduction. | seconds / tens of minutes |
| `replicate_published.c` | C | The published strategy of arXiv:2509.21494 (central case: all 22,163,142 positions; non-central case: 19 orbit classes of Maker's first move x all second and third moves = 2,196,381 positions, with a greedy rule on the 270 opposite-octant class-move pairs not covered by the published text). Checks for a pairing in every position. | 10-60 CPU min |
| `obstruction6.py` | Python 3, standard library | Counting facts for Proposition 5.1 (6x6x6) and Remark 3.3 (7x7x7). | seconds |

Commands (from this directory):

```sh
python3 -I obstruction6.py
python3 -I surplus_certificate.py --workers 3
cc -O2 -o bin/surplus7 surplus7.c && ./bin/surplus7 1 && ./bin/surplus7 2
cc -O2 -o bin/replicate_published replicate_published.c && ./bin/replicate_published 2 && ./bin/replicate_published 1
```

or `sh ../build.sh` (add `--full` to include `replicate_published`).

## How the surplus is computed

Slot graph: two slots per alive line (a line with no Breaker cell), each adjacent to the free cells of that line. A slot-saturating matching is a pairing strategy. The surplus is sigma = min over nonempty slot sets S of |N(S)| - |S|. Both implementations first find a slot-saturating matching. Then, for each alive line, they add extra copies of one of its slots and augment until augmentation fails or the cap is reached. By Lemma 2.1(2) of the paper, sigma is the minimum over lines of the number of copies that succeed. Lemma 2.1(1), together with the replication direction of Lemma 2.1(2), is proved in Lean: `formal/ValyuResearch/CubicTicTacToe.lean`, theorem `pairing_of_replication`.

## Results (26 October 2026)

- `results/surplus_python.json`: A1 histogram {met 27: sigma 4 (18 classes), met 26: sigma 4 (15), met 25: sigma 2 (24), met 22: no pairing (9)}. The A2 tree has 10,627 leaves and 14 distinct final Breaker sets, all meeting 27 lines and all with sigma >= 3. Part B: all 1,158 classes have sigma = 3 (cap 3; 2 needed). `THEOREM_VERIFIED = true`.
- `results/surplus_c_centre.txt`: met 27: 576 sets with sigma >= 4; met 26: 288 with sigma >= 4; met 25: 384 with sigma = 2; met 22: 48 with no pairing.
- `results/surplus_c_noncentre.txt`: 48,960 configurations (318 x 144 + 24 x 132), all with sigma = 3 exactly.
- `results/replicate_centre.txt`: 22,163,142 positions, 0 failures. `results/replicate_noncentre.txt`: 2,196,381 positions (270 gap class-move pairs, 91,530 gap positions), 0 failures.
- `results/obstruction6.json`: 6x6x6 degree histogram {7: 24, 4: 144, 3: 48}; at most 6 non-space-diagonal lines per cell; a pairing is excluded by counting for k <= 7 rounds.

The heuristic 6x6x6 simulations quoted in Section 5 of the paper (pairing first available after 9-11 rounds) are evidence only. They are not part of any proof and are not replayed here.
