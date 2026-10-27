# Certificate replay and source ledger

[`certificates.json`](certificates.json) contains twenty-seven certificates. Twenty-five have status `new`; `13n_4587` and `13n_4639` have status `prior_cable`. Every entry records a thirteen-crossing PD code, thirteen meridian permutations, four seed arcs, and nine numbered coloring moves. `permutation_type` is `double_transposition` for twenty-four entries and `three_cycle` for three. Points are numbered 0 through 7. Arc `i` ends at the incoming underedge of PD crossing `i`.

A coloring step `[j,k]` says that crossing `j` colors new underarc `k` using an already colored overarc and the other underarc. A double transposition `[[a,b],[c,d]]` swaps `a` with `b` and `c` with `d`. A 3-cycle `[a,b,c]` sends `a` to `b`, `b` to `c`, and `c` to `a`.

Run the dependency-free checks from this directory:

```sh
python3 check.py
python3 check_matrices.py
python3 negative_checks.py
```

`check.py` walks oriented PD edge labels to reconstruct arcs. It checks all 351 permutation relations and 243 explicit coloring moves, confirms a transitive orbit, and enumerates each image group to order 20,160. Since the generators are even, the image is `A8`. `check_matrices.py` reconstructs arcs independently by joining overedge pairs, forms eight-by-eight matrices over `F2`, rechecks all relations and coloring moves, verifies rank two for every `P-I`, and verifies rank seven for the stack of differences in each knot. `negative_checks.py` makes sure damaged cycles, matchings, crossings and coloring moves are rejected.

[`source-snapshot.json`](source-snapshot.json) contains the twenty-seven KnotInfo rows needed to connect the labels and PD codes to `database_knotinfo` version 2026.10.5. It also records that the Conway, Montesinos and pretzel notation fields are blank in all 9,988 thirteen-crossing rows. Its source CSV SHA-256 is `eb511ebc61204bc1c6d700d9da42257dcbb0369cb6756e89ed978a7821867c7d`. The source checker also confirms that all 293 pinned names retain bridge interval `[3,4]` in that CSV. To compare it with the 85 MB source file:

```sh
python3 check_source.py /path/to/knotinfo_data_complete.csv
```

The [pinned version 1.3.0 open list](open-list-v1.3.0.json) has 293 names and was extracted from the [release-tagged source file](https://raw.githubusercontent.com/creelie/conjecture-to-choose/v1.3.0/data/still_open.json). [`remaining-v1.3.0.json`](remaining-v1.3.0.json) is exactly that set minus the twenty-five `new` certificate names, leaving 268. The two prior cable values remain in this mechanical residual list because they were not newly established here. The checker verifies the set arithmetic and source inclusion.

The checks use integer and binary arithmetic and need no knot package. The positive certificates do not depend on the completeness of the search that found them.

## Check earlier Coxeter-census overlap

The optional [`search_coxeter_overlap.py`](search_coxeter_overlap.py) uses NumPy 2.3.3 to exhaust the reflection classes of `A4`, `D4` and `H4` on the twenty-five new diagrams. Those are the rank-four target groups in Blair, Kjuchukova and Morrison's census. The script generates each root system over exact `Z[φ]`, fixes the first seed reflection up to conjugacy, enumerates every remaining seed triple, propagates it across the nine coloring moves, checks all thirteen relations and tests whether the four roots span dimension four. Run it with the KnotInfo CSV to include the `13a_112` positive control:

```sh
python3 search_coxeter_overlap.py /path/to/knotinfo_data_complete.csv
```

The recorded [summary](coxeter-overlap-summary.json) has zero rank-four hits among the twenty-five for each target and a rank-four positive control in each. This audit addresses overlap with that specific Coxeter search. It does not classify the knots against other special-family theorems.

## Reproduce the bounded search

The optional [`search_rank_two.py`](search_rank_two.py) requires NumPy (the run used version 2.3.3) and the exact KnotInfo CSV. It enumerates four seed images up to point relabeling, propagates them through a four-seed Wirtinger coloring, checks all thirteen relations, and requires transitivity. The four runs scanned all 293 pinned names:

```sh
python3 search_rank_two.py C 8 /path/to/knotinfo_data_complete.csv /tmp/search-C8.json
python3 search_rank_two.py C 9 /path/to/knotinfo_data_complete.csv /tmp/search-C9.json
python3 search_rank_two.py D 8 /path/to/knotinfo_data_complete.csv /tmp/search-D8.json
python3 search_rank_two.py D 9 /path/to/knotinfo_data_complete.csv /tmp/search-D9.json
```

`C` denotes 3-cycles and `D` double transpositions. The recorded [`search-summary.json`](search-summary.json) gives the normalized configuration counts and hit names: C8 found 3, D8 found 24, and neither nine-point screen found a hit. The first seed image can be fixed to a standard label by conjugating in the symmetric group. At each later seed, unseen points are numbered on first appearance; only one representative under permutations of those new labels is retained. The script enumerates every old/new support choice and every permutation of the chosen cycle type. Equal seed images are skipped because three distinct rank-two generators cannot act transitively on eight points. For D9, eight transposition edges on nine connected vertices must form a tree, so cyclic partial configurations are pruned.

A transitive action generated by four rank-two permutations cannot have more than nine points, since four generators contribute at most eight edges to a connected support graph. Four-cycle screens on eleven through thirteen points and binary rank-one transvection screens in dimensions five and six supplied no further positive certificate within their stated restrictions. No negative screen is used as a theorem about other possible quotients.
