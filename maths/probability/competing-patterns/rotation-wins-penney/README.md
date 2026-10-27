# Right rotation wins Penney's game for permutations

[Paper](../../../../public-release/papers/rotation-wins-penney.pdf) · [LaTeX](paper.tex)

**Status: computer-assisted theorem.**

The argument and computations were developed and checked on 26 October 2026. The manuscript uses the campaign's 25 October date convention.

For every permutation `a = a1...ak` of length `k >= 3`, let `b = ak a1...a(k-1)`. In a sequence of independent observations from a common continuous distribution,

\[
\Pr(b\text{ appears before }a)>\tfrac12.
\]

An appearance means a consecutive block with the specified relative order. For example, `0.2, 0.4, 0.6, 0.1` has order `2341`. Moving its final symbol to the front gives `1234`.

This proves Conjecture 6.1 of [Elizalde and Lin, arXiv:2404.06585v4](https://arxiv.org/abs/2404.06585v4), published in [DMTCS 28:1 (2026)](https://doi.org/10.46298/dmtcs.16361). The length-three case belongs to that source. The rotation need not be the best reply.

## What is new

The source supplies exact recurrences for length three and reports truncated numerical evidence at lengths four and five. The contribution here is a uniform proof for all lengths at least eight, together with exact certificates and rigorous tails for lengths four through seven. An additional horizon-18 certificate independently verifies the known length-three case. The result resolves the winning-reply conjecture for the independent continuous model. It does not calculate the optimal reply or all pairwise winning probabilities.

The cluster method and its interpretation through linear extensions are established tools, credited to [Elizalde and Noy (2012)](https://doi.org/10.1016/j.aam.2012.08.003). The theorem is the novelty claim; no separate priority claim is made for the general cluster identities or cancellation device.

## Evidence

- The one-position overlap has signed advantage at least `1/(k+1)!`.
- A written interleaving comparison and a proved clump tail yield a positive uniform scaled margin of `218738049/2305503200` for every `k >= 8`.
- For lengths 4 through 7, Python and C++ independently reconstruct every signed integer coefficient for 2,952 representatives under complementation. Each partial sum exceeds a proved bound on the entire omitted tail.
- A direct enumeration of permutations through length nine independently checks the first-hit generating-function signs for `2341` versus `1234`.
- For length three, two different integer recurrences agree on all first-hit counts through horizon 18. A direct C++ oracle independently checks all six races at horizons 8, 9 and 10. Even assigning every unresolved case to the first player leaves their probability below `47/100` for every complement representative.
- The theorem is not Lean-formalized. Its infinite-range proof and probabilistic tail argument are written mathematics; its finite enumeration is replayable exact computation.

| Length | Cutoff in start span | Representatives | Scaled partial sum | Scaled absolute tail |
|---|---|---|---|---|
| 4 | 15 | 12 | greater than 3/4 | 5/12 |
| 5 | 12 | 60 | greater than 9/10 | 4/35 |
| 6 | 5 | 360 | greater than 49/50 | 28/71 |
| 7 | 6 | 2,520 | greater than 99/100 | 32/419 |

The scale is `(k+1)!`. Full rational minima are saved in [verification/results.json](verification/results.json).

## Reproduce

Run from this finding directory:

```sh
./build.sh
```

This compiles the independent C++ enumerator, reconstructs all coefficient arrays, compares them with the saved certificates, checks coverage and exact inequalities, runs direct controls, and builds `paper.pdf`. It uses one worker at a time, with `nice -n 10`. It needs Python 3, a C++17 compiler with 128-bit integers, `pdflatex`, and `bibtex`. No third-party Python packages are needed.

For the independent standard-library Python reconstruction:

```sh
nice -n 10 python3 verification/replay_python.py
```

This is slower and prints progress and heartbeats. To check only the stored arithmetic and representative coverage:

```sh
python3 verification/verify.py
```

That last command does not reconstruct the stored coefficient counts. The separate command `python3 verification/check_length_three.py` reconstructs the length-three horizon certificate by both methods. See [verification/README.md](verification/README.md) for the certificate schema and exact scope of each check.

## Correctness and originality

Correctness confidence is high after independently executed exact reconstructions and adversarial reviews of every part of the proof. The max review and focused follow-up found no material mathematical gap after the requested clarifications and additional base-case check. Originality confidence is moderate: the bounded audit below found no resolution, but cannot establish the absence of unpublished or unindexed work. No external peer review is claimed.

## Priority checks performed on 26 October 2026

- Read the source's Conjecture 6.1, comparison formulas and known short cases through Valyu Contents. Verified arXiv metadata: latest version v4, 6 July 2026. The journal article page records publication on 8 July and modification on 7 September 2026.
- Searched Penney-permutation and winning-rotation terms with a 1 September 2026 start date, plus general searches for resolutions. Consulted Elizalde's current research page, which lists the DMTCS paper; no relevant follow-up was identified there.
- Performed Zenodo- and GitHub-restricted searches. These initially returned unrelated results and are weak negative evidence.
- Fetched GitHub REST search through Valyu Contents for the exact arXiv ID. Its one result was [problem-bank proposal 688](https://github.com/elder-plinius/V3R1T4S/pull/688), created on 24 October. Read its pull record and discussion: it was closed without merging on 25 October because the maintainer added the target directly. The maintainer explicitly retained the conjecture as open. This is a target proposal, not a proof.
- Successful direct Zenodo queries for the exact arXiv ID and for `"Penney" AND "permutations"` returned zero records. GitHub's exact-ID README repository search returned zero; the title-restricted issue search returned the target proposal and one unrelated word-game proposal. GitHub code search required authentication and was not available.
- Semantic Scholar listed two citing papers. Relevant primary passages in arXiv:2601.16580v2 and arXiv:2511.13287 were read; they discuss different word models and supply no resolution. Recent arXiv keyword queries and an Erdos Problems domain query identified no relevant resolution. The attempted Erdos site-search URL returned 404.

The exact successful queries, returned counts, failures and limitations are recorded in [verification/priority-audit.md](verification/priority-audit.md).

These checks are bounded. A problem-bank entry is evidence of contemporary open status, not a correctness or priority certificate for this result.

## Review record

- Literature scout `probability-fresh-scout`: `DR-056`, heavy.
- Focused priority audit `probability-penney-priority`: `DR-042`, heavy.
- Final adversarial review `probability-penney-final-review`: `DR-044`, max, code execution enabled. No fatal mathematical error or prior proof found; all length-4-through-7 inequalities independently reproduced. Its requested clarifications and supplementary length-three check have been implemented, and actual C++ outputs are archived.
- Follow-up audit `probability-penney-review-closure`: `DR-014`, heavy, code execution enabled. Completed 26 October 2026 at 12:21 UTC: no material mathematical or computational gap found in the new base case. It audited the code and arithmetic but did not obtain an execution result. Separate local execution and independent exhaustive checks through length 10 close that operational item.
- Three independent mathematical review rounds passed the uniform proof, the refined finite-tail and enumeration arguments, and the new length-three rank-state certificate. Requested completions were a finite bound on `P(1)`, a filtration argument counting only anchors in the root clump, and an explicit integer condition on the tail index. All are included in the paper. The C++ output is archived, and both full reconstructions were actually run locally.

The campaign cell log and full request/status/report files retain the audit trail. No credentials or third-party full texts are included in this finding.
