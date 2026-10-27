# Cactus networks satisfy the topological response conjecture

**Status:** theorem (partial resolution of an open conjecture) plus a proved obstruction to the method. Research draft, not externally refereed.

[Paper](../../../../public-release/papers/cactus-response-coupling.pdf) · [LaTeX](paper.tex) · [Verification](verification/README.md) · [Video brief](video-brief.md)

## Claim

Fancher and Horowitz, [arXiv:2607.12096v1](https://arxiv.org/abs/2607.12096) (13 July 2026), Eq. (6), conjecture that for any Markov jump process the steady-state logarithmic response `d ln pi_j / d lambda` is a convex combination of the responses `G^alpha_j - <G^alpha>` of *uniquely constructable* (UC) families of rooted spanning trees. Its consequence, their Eq. (8), is a topological bound on the sensitivity of any observable. They verified the conjecture analytically only for three states and call a formal proof "the most obvious next step".

**Theorem.** If the underlying undirected graph of the network is a cactus (every edge on at most one cycle), the conjecture holds for all positive rates. This includes every unicyclic network of any size. The convex weights are `theta^alpha = Theta(alpha)` for a probability measure `Theta` on UC families whose marginal at each root `j` is that root's spanning-tree law `P_j(T) = w(T)/w(T_j)`. The weights do not depend on the perturbation `d`, and the sensitivity bound (8) follows.

**Construction.** On a cycle, multiply both arcs of each undirected edge by `exp(-gamma)` with one independent standard Gumbel variable per edge, and take each root's heaviest spanning tree. A tree rooted at `r` is a choice of deleted edge `k` in a window of `n` consecutive integers, with weight `c_r * lambda_k` for a single sequence `lambda` that does not depend on the root. Each window contains each edge once, so the Gumbel-max lemma gives the exact law at every root simultaneously. The heaviest-tree family is dominant, hence UC (Fancher and Horowitz, Lemma 4). Spanning-tree laws factorise over blocks, so cacti follow by gluing. Missing arcs and parallel arcs are handled by limit and copy-choice lemmas.

**Obstruction.** For the complete digraph on four states with integer rates in `verification/k4_no_coupling_certificate.json`, no such measure exists. A `{-1,+1}` Farkas certificate on the 64 (root, tree) pairs is nonnegative on all 346 UC families but has expectation `-74467043099669441/1314877998480476367` under the root laws. Three reduction lemmas (spanning subgraphs, pendant states, suppression of degree-2 states, each with an exact push-forward of the root laws that preserves unique constructability) carry the obstruction to **every bidirected network whose graph has a `K4` minor** (Theorem 5.3). So the coupling method can at most reach series-parallel graphs, and it provably reaches the cacti among them. This does not refute the conjecture, which asks for much less than a coupling (paper, hierarchy (i)-(iv) in Section 5); the conjecture itself survived every numerical test on `K4` and on five-state graphs.

## What is new, and what is not

- New (to our search): proof of FH Eq. (6) and (8) for all cactus networks (a new proof of FH's three-state case is a special case); the explicit Gumbel weights; the reduction "a measure with the right root marginals suffices"; the `K4` obstruction to that reduction and its extension to all graphs with a `K4` minor.
- Not new: the response formula (FH Eq. 5), the dominant-implies-UC lemma (FH Lemma 4, reproved here), the Gumbel-max lemma (Yellott 1977) and perturb-and-MAP sampling (Papandreou and Yuille 2011; Maddison, Tarlow and Minka 2014).
- Not claimed: the general conjecture. It remains open for networks whose underlying graph is not a cactus, for example `K4`, the three-site binding cube and kinetic-proofreading ladders.
- Conjecture (half proved): coherent couplings exist for all rates exactly on graphs without a `K4` minor. The "only if" half is Theorem 5.3. The "if" half is proved for cacti; for other series-parallel graphs it is numerical only (linear programs found couplings for all sampled rates on the diamond, `K_{2,3}` and a five-cycle with a chord). The per-edge Gumbel construction fails on the diamond (error about 0.06), so a different construction would be needed.

## Confidence

- Correctness of the cactus theorem: high. The proof is short and elementary; exact checks replay the cycle identity (n <= 8) and block factorisation (five cacti); Monte Carlo matches the predicted laws on a 6-cycle and a cactus within sampling error. Two adversarial DeepResearch reviews (heavy, then max on the final text) found no fatal error; the max review independently reproduced the K4 certificate in exact arithmetic and the Gumbel marginals on further cacti, and checked Eq. (6) end to end against finite differences.
- Correctness of the `K4` obstruction: high (exact rational replay, independent enumeration). Correctness of the `K4`-minor extension: high for the written proof (three short push-forward lemmas); its suppression step is replayed exactly on the subdivided `K4` (984 UC families, same negative expectation), and UC preservation under the reduction maps was brute-forced on small graphs.
- Originality: moderate. Searches found no proof, partial proof or counterexample of the conjecture (details below), but the source is three months old and priority cannot be established by search.
- Significance: low to moderate. It covers the physically common single-loop class and gives an explicit construction, but stops at graphs with two cycles sharing an edge: cacti are exactly the graphs without a diamond minor, so the four-state diamond is the smallest open case. The `K4`-minor theorem marks the outer limit of the coupling technique.
- Reading of the conjecture: FH's Eq. (6) can be read with `theta` allowed to depend on `d` (their numerics) or with one `theta` for all `d` (their three-state proof). The theorem gives the stronger reading, hence both.

## Priority checks performed (26 October 2026)

- arXiv: Valyu paper search for the conjecture's terms, "uniquely constructable", "tree families", response space, from 2026-07-01 and from 2026-09-01; author query "Fancher" from 2026-07-14; arXiv abstract page of 2607.12096 (still v1 as retrieved).
- Zenodo: Valyu web search with `zenodo.org` as source for the conjecture's terms; the authors' code record `zenodo.org/records/21359479`. The Zenodo search UI and API pages did not return query-specific results through the contents tool, so Zenodo coverage relies on the search index.
- GitHub: Valyu search with `github.com` as source (including the `the-omega-institute/trureturing` and `google-deepmind/formal-conjectures` trackers) for "Fancher Horowitz", "uniquely constructable", "topological building blocks".
- Author pages: Horowitz lab publications page (no newer related item listed). Pith review of 2607.12096 (abstract-only, no resolution).
- erdosproblems.com is not relevant to this problem.
- DeepResearch priority audits inside tasks `DR-066` (heavy) and `DR-036` (max): arXiv record still v1, only the authors' Zenodo code record, an abstract-only Pith review, and one paper (2608.06368) that merely cites FH. Neither found a proof, partial proof or counterexample. Neither enumerated the arXiv listings exhaustively.
- Prior art for the technique: Gumbel-max and perturb-and-MAP (Yellott 1977; Papandreou and Yuille 2011; Hazan and Jaakkola 2012; Maddison, Tarlow and Minka 2014), Gumbel perturbations of spanning trees and arborescences in machine learning (Paulus et al. 2020, arXiv:2006.08063; Struminsky et al. 2021, arXiv:2110.15072), cycle popping (Propp and Wilson 1998). None couples rooted laws across roots on UC families.

## Reproduce

```sh
sh build.sh             # exact checks (standard library) and the PDF
sh build.sh --numerics  # also the floating-point evidence (numpy, scipy; about two minutes)
```

## Provenance

The conjecture was found by Valyu paper search during a stochastic-thermodynamics scouting pass. Exploratory code (enumeration of UC families, gauge and linear-programming tests, critical-point construction, coupling linear programs) is kept outside the collection. DeepResearch tasks: scouting report `DR-013` (did not list this conjecture); adversarial and priority review `DR-066` (heavy; asked for explicit gluing, non-periodic lift, parallel-copy dominance and a hierarchy framing of the K4 result, all now in the paper); max-mode adversarial review of the final text `DR-036` (no fatal error; wording fixes on the reading of Eq. (6), weak duality, the non-strict hierarchy, priority phrasing, seed dependence of one Monte Carlo figure, all integrated); heavy review of the `K4`-minor extension `DR-028` (no fatal error; expository gaps in the UC-lifting bookkeeping, leaf order, cycle-length argument and citation, all fixed).

References were checked against the sources: arXiv abstract pages (FH, Paulus et al., Struminsky et al., Maddison et al., Hazan and Jaakkola), Crossref records (Hill, Schnakenberg, Yellott, Papandreou and Yuille, Owen and Horowitz article 1280, Propp and Wilson, Diestel Graph Theory 5th edition), and the FH full text for every statement attributed to them.
