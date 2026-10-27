# Review notes

## Adversarial DeepResearch review

Task `recreational-hex-review` (Valyu DeepResearch, max mode, task DR-002, completed 26 October 2026). The task received the full statements, definitions, method and our diagnosis of Lemma 5 of arXiv:2607.28138v1, and was asked to find errors and prior art, with code execution enabled.

What it reproduced with its own Maker-Breaker solver: the winning-set counts $|\mathcal W_5|,|\mathcal W_6|,|\mathcal W_7|=48,106,164$ (5x5) and $306,560,848,1301$ (6x6); the centre wins $\mathrm{Hex}(5,6)$ and $\mathrm{Hex}_7(5)$; no opening wins $\mathrm{Hex}(5,5)$ or $\mathrm{Hex}_6(5)$; the literal Conjecture 18 cells $(3,2)$, $(2,3)$ fail $\mathrm{Hex}(5,6)$; $\mathrm{Hex}_9(6)$ fails after $(3,4)$ and $(3,3)$; and the 23-move game of Figure 2 (legal, first Blue connection at move 23, shortest path six cells). Its solver uses the same reduction, so it checks the numbers rather than the reduction.

It found no fatal flaw and no prior source stating $\lambda(5)=6$, $\delta(6)=10$ or $\lambda(6)=8$. Its objections and our responses:

| Objection | Severity given | Response |
|---|---|---|
| The strict claim $\lambda^*(5)=6$ needs its own checker with all Blue stones in the key; a Maker-Breaker win does not exclude an earlier long connection | needs fix | Already so: `check_strict.py` keys on all Blue stones, plays ordinary Hex to the first connection and fails on any long Blue connection or Red connection. 875,938 keys verified. The paper now says explicitly that the refutation of Theorem A under the preprint's own (strict) rules rests on this certificate. |
| $\lambda(6)=8$ is search only | needs fix | Already labelled a computation (Proposition 1.3). The lower bound $\lambda(6)\ge8$ is now certified (36 Red certificates for $\mathrm{Hex}(6,7)$). |
| $\delta(6)=10$ only partly reproduced by the reviewer | needs fix | The reviewer's solver timed out; our certificates cover all 36 openings and the Blue win, and `run_checks.sh full` regenerates and replays them (regeneration is byte-identical to the original runs). |
| Theorem D of the preprint: conclusion right, proof invalid | wording | The paper says exactly this. |
| Campbell and the preprint draw Blue left-right | cosmetic | Orientation note added in Section 2; the reported optimal openings are invariant under transposition. |
| Conjecture 18: do not claim failure at $n=6$ | cosmetic | The paper says the literal statement fails at $n=5$ (certified) and reports the $n=6$ cell $(3,3)$ only as a search result, noting the likely intended reading. |
| $F(n)\to\delta(n)$ via depth $=2\delta-1$ is our inference, not HZY's | cosmetic | Wording says "By Campbell's relation this corresponds to". |

## Independent audit of the checkers

A separate agent, given only the two checkers, the rules and the shipped certificates (not our argument), was asked to make them print VERIFIED for a false claim. It read both files, wrote a search for any key-to-move table the checker would accept, and compared against exact minimax over full positions: 3x3 in modes L, D and strict for every bound, all openings and both sides; 4x4 mode D (bounds 3 to 5, all openings, both sides) and mode L (bounds 4 to 6, ten openings). It found no false acceptance on any board with $n\ge2$ (its confidence about 90%). Findings and our fixes:

| Finding | Severity | Fix |
|---|---|---|
| Empty certificates verify trivially on $1\times1$ and $0\times0$ boards | cosmetic | Checkers now reject headers with $n<2$, an unknown mode or side, or an out-of-range bound or opening. |
| A certified move need not transfer literally to another position with the same key (a Red move outside $R$ may be occupied there); soundness rests on the pass-domination argument, so a replay proves the game value rather than that the table can be followed move by move | wording | Paper Section 3 now says exactly this. |
| The driver trusted file names: the final VERIFIED line did not show $n$, mode or bound | could matter | The checkers now print `[n=.. mode=.. bound=.. first=.. side=..]` and `run_checks.sh`, `table5.sh` require it to match the file name. |
| Blank lines crash the parser | cosmetic | Blank lines are skipped. |

It confirmed: the winning-set enumeration is complete; every opponent reply is tried; keys are marked verified only after their whole subtree passes; the stone budget in mode D, Red connections, long Blue connections (continue in mode L, fail in the strict game) and full boards are handled correctly; `check_strict.py` keys are sound literally. The 6x6 and strict replays in `logs/` were run with the checker before these header changes; the replay logic is unchanged.

## Priority audit

Task `recreational-hex-priority` (heavy, DR-065): no source states $\lambda(6)$, $\delta(6)$ or a proved minimum depth for 6x6 Hex; the only numerical precursor is the KataHex estimate $F(6)=19$ (HZY, 2024), which the paper credits. Our own searches (arXiv listings, the arXiv abstract page, Zenodo API, GitHub repository and issue search, MathOverflow 302821, Valyu search with 2026 date filters) found no citing paper, erratum or second version of arXiv:2607.28138 as of 26 October 2026.
