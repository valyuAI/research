# Bridge number four for twenty-five thirteen-crossing knots

**Status:** theorem with finite certificates. For each of the twenty-five knots in the table below,

\[
b(K)=\mu(K)=4,
\]

where `b` is bridge number and `μ` is the minimum number of meridians generating the knot group. All twenty-five had bridge entry `[3,4]` in KnotInfo 2026.10.5 and appeared in the 293-name open list of [Bhattacharjee's release 1.3.0](https://zenodo.org/records/23561157). The result removes **25 entries from that pinned list**, leaving [268 names](verification/remaining-v1.3.0.json) without a new certificate here. That residual ledger includes two trefoil cables whose values already follow from older theorems. It is not an assertion that all 268 values are mathematically unknown.

In the certificate column, **D** means meridians map to double transpositions in `A8`; **C** means they map to 3-cycles. The last column is KnotInfo's alternating flag. KnotInfo calls all twenty-five hyperbolic. Its Conway, Montesinos and pretzel notation fields are blank for **all 9,988 thirteen-crossing rows**, so they provide no family exclusion for these knots.

| Knot | Certificate | Alternating |
| --- | --- | --- |
| `13a_373` | D | Yes |
| `13a_375` | D | Yes |
| `13a_391` | D | Yes |
| `13a_392` | D | Yes |
| `13a_3264` | D | Yes |
| `13a_3266` | D | Yes |
| `13a_3275` | D | Yes |
| `13a_3276` | D | Yes |
| `13n_1005` | D | No |
| `13n_1006` | D | No |
| `13n_1007` | D | No |
| `13n_1011` | D | No |
| `13n_1012` | D | No |
| `13n_1013` | D | No |
| `13n_1043` | D | No |
| `13n_1044` | D | No |
| `13n_1045` | D | No |
| `13n_1046` | D | No |
| `13n_1047` | D | No |
| `13n_1048` | D | No |
| `13n_3842` | D | No |
| `13n_3844` | D | No |
| `13n_3855` | D | No |
| `13n_3856` | D | No |
| `13n_4645` | C | No |

## Why the certificates prove the values

Each saved PD diagram has thirteen meridian arcs. Its certificate assigns each arc a permutation of eight points and checks all thirteen Wirtinger relations. Four seed permutations generate `A8`, hence act transitively. On the eight-dimensional permutation module over `F2`, both a 3-cycle and a double transposition have `rank(P-I)=2`; the common fixed space is the one-dimensional space of constant vectors. If `k` meridians generated the knot group, the intersection of their fixed spaces would have codimension at most `2k`. The actual codimension is seven, so `k≥4`.

The same diagrams have explicit four-seed Wirtinger colorings. [Blair, Kjuchukova, Velazquez and Villanueva](https://arxiv.org/abs/1705.03108v1) show that a four-seed coloring gives `b≤4`. Together with `μ≤b`, this gives `4≤μ≤b≤4`. The [paper](../../../../public-release/papers/bridge-thirteen-crossing-census.pdf) proves the general fixed-space inequality and works through a double-transposition crossing of `13n_1005`.

The certificate file also contains `13n_4587` and `13n_4639`. They pass the same checks with 3-cycle meridians, but KnotInfo identifies them as trefoil cables. [Boileau, Jang and Weidmann, Corollary 1.6](https://arxiv.org/abs/1510.00816v1) gives meridional rank at least four for prime satellite knots; KnotInfo's `[3,4]` upper bound then gives `b=μ=4`. They are independent confirmations, excluded from the twenty-five new determinations.

## Reproduce

From this directory:

```sh
sh build.sh
```

The two standard-library checkers in [`verification/`](verification/) independently reconstruct arcs and replay all **27** certificates. They check 351 Wirtinger relations, 243 coloring moves, the eight-point actions, and exact matrix ranks. The first also enumerates each image group and verifies order `20,160=|A8|`. `build.sh` then compiles `paper.pdf` from [`paper.tex`](paper.tex) with `pdflatex` and `bibtex`.

The saved [KnotInfo source snapshot](verification/source-snapshot.json) records 27 diagram rows, the notation-field coverage audit, and the SHA-256 digest of the 85 MB `database_knotinfo` 2026.10.5 CSV. To compare it with the exact source file:

```sh
KNOTINFO_CSV=/path/to/knotinfo_data_complete.csv sh build.sh
```

The [pinned 293-name list](verification/open-list-v1.3.0.json) and [268-name residual list](verification/remaining-v1.3.0.json) make the count reproducible. An [optional rank-two search script](verification/search_rank_two.py) and its [four-run summary](verification/search-summary.json) reproduce the 3-cycle and double-transposition screens with NumPy and the original KnotInfo CSV. Certificate validity does not rely on the search being exhaustive. The underlying rank calculation is independent of field characteristic for permutation modules: `rank(P-I)` equals eight minus the number of cycles.

## Prior work and confidence

The closest large censuses are [Blair, Kjuchukova and Morrison](https://arxiv.org/abs/2208.09032) for finite Coxeter quotients and [Bhattacharjee's version 1.3.0](https://zenodo.org/records/23561157) for rank-one four-dimensional representations. Finite-order meridian quotient methods are not new. The twenty-four double-transposition witnesses use a different meridian conjugacy class; `13n_4645` was previously obtained by the 3-cycle route.

The [Coxeter overlap audit](verification/coxeter-overlap-summary.json) exhausts four-seed reflection assignments to the rank-four target groups `A4`, `D4` and `H4` used by Blair, Kjuchukova and Morrison. It found no rank-four witness for any of the twenty-five knots. The [optional script](verification/search_coxeter_overlap.py) fixes the first reflection up to conjugacy, tests all `10³`, `12³` and `60³` remaining seed triples, propagates labels through the saved colorings, and checks every crossing and the exact root span over `Z[φ]`. The four seed arcs generate each Wirtinger presentation, so this covers every reflection homomorphism to those groups. As a positive control, the script finds rank-four witnesses in all three groups for KnotInfo's exact-four knot `13a_112`. This rules out overlap with that census's maximal-rank Coxeter certificates, subject to the reproducible finite search.

**Correctness confidence: high.** Every positive claim has two exact certificate replays and a cited bridge-coloring implication. **Originality confidence: moderate.** The pinned release and KnotInfo retain all twenty-five names as `[3,4]`; the Coxeter audit excludes overlap with the main earlier census. A bounded literature search cannot rule out uncatalogued per-knot determinations or broader family theorems; the blank KnotInfo notation fields offer no family evidence, and external peer review is absent.

Review records for this cell include `knots-bridge-adversarial` (`DR-037`), `knots-round2-methods` (`DR-010`), `knots-round2-hit-priority` (`DR-081`), and the final max review `knots-round2-final-adversarial` (`DR-027`). The final review independently reproduced six examples and found no mathematical flaw, but could not inspect the local package or BKM's per-knot workbook. The two local checkers cover all twenty-five, the exact source CSV covers all rows, and the Coxeter audit addresses its BKM overlap objection. Special-family priority remains unresolved.
