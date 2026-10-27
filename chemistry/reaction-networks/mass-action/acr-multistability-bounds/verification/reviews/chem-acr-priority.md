# Coexistence of ACR and multistability in mass-action networks: priority and literature audit (status 25 Oct 2026)

Task DR-033 | mode heavy | completed 2026-10-25T23:11:05.807Z | cost 3.125

# Coexistence of ACR and multistability in mass-action networks: priority and literature audit (status 25 Oct 2026)

## Executive summary

**No retrieved paper proves, disproves or refines the Kaihnsa–Nguyen–Shiu (KNS) conjecture.** The retrieved literature contains no 3-species at-most-bimolecular network with ACR and two stable positive steady states. It contains no proof or disproof for dimension-2 networks, and no minimum count of reactant complexes or complexes for ACR plus multistability. The conjecture appears word for word in the published EJAM paper. The arXiv listing shows only v1.

The only ACR-plus-bistability exhibit found is Joshi–Nguyen–Johnston (arXiv:2605.11389, May 2026). It is a dual-site futile cycle with 8 species, so it cannot test the minimality conjecture. The smallest multistable zero-one networks (3 species, 6 reactions, dimension 3) are now classified, but no source tests them for ACR.

These negative results rest on the sources retrieved. Citation lists for arXiv:2307.04186 on Semantic Scholar and Google Scholar were not retrieved, only the arXiv links to them [[1]](https://arxiv.org/abs/2307.04186). A citing paper that is not indexed could have been missed.

## 1. The open statement and its published form

**Theorem.** For an at-most-bimolecular network G with n species, ACR plus nondegenerate multistationarity requires [[2]](https://arxiv.org/html/2307.04186):

- at least 3 species;
- at least 3 reactant complexes and at least 5 complexes;
- dimension at least 2.

If G is full-dimensional, it also requires at least n + 2 reactant complexes and dimension at least 3 [[2]](https://arxiv.org/html/2307.04186). The bounds on species, complexes and dimension are tight, attained by {A+B→2C→2B, C→A} (Example 4.10) [[2]](https://arxiv.org/html/2307.04186). The abstract states the bounds as "at least 3 species, 5 complexes, and 3 reactions" [[1]](https://arxiv.org/abs/2307.04186).

**Conjecture (Section 6), arXiv HTML text:** "Another interesting direction, therefore, is to investigate conditions for coexistence of ACR and multistability, rather than multistationarity. The 'minimal' networks in the current work admit only two positive steady states and are not multistable. Hence, we conjecture that the lower bounds (on dimension and the numbers of species, reactant complexes, and all complexes) for the coexistence of ACR and multistability are strictly larger than the bounds proven here for ACR and multistationarity." [[2]](https://arxiv.org/html/2307.04186)

**EJAM text:** the Cambridge Core version of Section 6 has the same wording, with only "multistability" italicised [[3]](https://www.cambridge.org/core/journals/european-journal-of-applied-mathematics/article/absolute-concentration-robustness-and-multistationarity-in-reaction-networks-conditions-for-coexistence/BEABF13EA90E50ED45F64650BDEAC003). The journal reference is Eur. J. Appl. Math. 35(4), 566–600, DOI 10.1017/S0956792523000335, published online 2 January 2024 [[1]](https://arxiv.org/abs/2307.04186)[[4]](https://researchprofiles.ku.dk/en/publications/absolute-concentration-robustness-and-multistationarity-in-reacti/)[[3]](https://www.cambridge.org/core/journals/european-journal-of-applied-mathematics/article/absolute-concentration-robustness-and-multistationarity-in-reaction-networks-conditions-for-coexistence/BEABF13EA90E50ED45F64650BDEAC003). The conjecture is retained.

**Versions.** The arXiv abstract page lists only "[v1] Sun, 9 Jul 2023" [[1]](https://arxiv.org/abs/2307.04186). The snapshot's date is not stated. The arXiv HTML copy carries a date line "August 24, 2026" [[2]](https://arxiv.org/html/2307.04186). That may be only a build date, but it means the absence of a v2 as of 25 Oct 2026 is not fully nailed down.

**How to read the conjecture.** It is phrased as a statement about several bounds at once (dimension, species, reactant complexes, complexes). Refuting it would need an example that does not exceed the old bound in at least one of those measures. An example larger than the minimal one, such as the 8-species network below, cannot do that.

## 2. Papers checked

| Paper | ID, date | Bearing on ACR + multistability |
|---|---|---|
| Joshi, Nguyen, Johnston, "Bistability, Absolute Concentration Robustness, and Hysteresis in Dual-Site Futile Cycles with Bifunctional Enzymes" | arXiv:2605.11389v1, 12 May 2026 [[5]](https://arxiv.org/abs/2605.11389) | Exhibits ACR plus bistability in one 8-species network (Section 3). Its passages here do not mention KNS, but its reference list was not available. |
| Jiao, Tang, Zeng, "Multistability of Small Zero-One Reaction Networks" | arXiv:2406.11586, 17 Jun 2024 [[6]](https://arxiv.org/html/2406.11586)[[7]](https://arxiv.org/abs/2406.11586) | Multistability only, no ACR. Cites KNS as background [[6]](https://arxiv.org/html/2406.11586). Version count not established. |
| Tang, Zhang, "The Ubiquity of Three Steady States: Minimal Multistable Zero-One Reaction Networks" | arXiv:2608.01116, 2 Aug 2026 [[8]](https://arxiv.org/html/2608.01116)[[9]](https://arxiv.org/abs/2608.01116) | Classifies minimal multistable networks. The passages available do not address ACR. |
| Si, Tang, ACR of non-redundant zero-one networks (v5 title "Obstruction of Absolute Concentration Robustness by Conservation Laws in Non-Redundant Zero-One Networks") | arXiv:2604.14592, v1 16 Apr 2026, v5 3 Sep 2026 [[10]](https://arxiv.org/abs/2604.14592) | ACR classification only. It cites "the co-occurrence prevalence of multistationarity and ACR" as its ref. [[11]](https://www.researchgate.net/publication/372248289_Absolute_Concentration_Robustness_and_Multistationarity_in_Reaction_Networks_Conditions_for_Coexistence), which is not identified in the text shown. The description matches Joshi et al. [[12]](https://arxiv.org/abs/2301.10337) but does not establish it. |
| García Puente et al., "Absolute concentration robustness: Algebra and geometry" | arXiv:2401.00078, v1 29 Dec 2023, v3 12 Nov 2024; J. Symbolic Comput. 128:102398 (2025) [[13]](https://arxiv.org/abs/2401.00078)[[14]](https://www.sciencedirect.com/science/article/pii/S0747717124001020) | Methods for deciding ACR. Mentions KNS as background on ACR and multistationarity [[14]](https://www.sciencedirect.com/science/article/pii/S0747717124001020). No ACR + multistability result in the passages seen. |
| Meshkat, Shiu, Torres, ACR in low-dimensional networks | arXiv:2105.00109 (2021, outside the date window) [[15]](https://arxiv.org/abs/2105.00109) | Characterises ACR for 2-species, 2-reaction and one-dimensional networks. Defines "stable ACR". No multistability result. |
| Kaihnsa, Telek | arXiv:2403.16556, 25 Mar 2024 [[16]](https://arxiv.org/abs/2403.16556) | Multistationarity-region connectivity. Not ACR. |
| Kaihnsa, Wang | arXiv:2607.25456, 28 Jul 2026 [[17]](https://arxiv.org/abs/2607.25456) | Multistationarity-region connectivity. Not ACR. |
| Joshi, Kaihnsa, Nguyen, Shiu, "Prevalence of multistationarity and ACR" | arXiv:2301.10337, 24 Jan 2023; SIAM J. Appl. Math. 83(6):2260–2283 [[12]](https://arxiv.org/abs/2301.10337)[[18]](https://researchprofiles.ku.dk/en/publications/prevalence-of-multistationarity-and-absolute-concentration-robust/) | Predecessor of KNS. Multistationarity only. |
| Joshi, Nguyen, bifunctional enzymes and ACR | arXiv:2304.02679 [[19]](https://arxiv.org/abs/2304.02679); arXiv:2504.21011 [[20]](https://arxiv.org/abs/2504.21011) | ACR sources for the dual-site networks (the hypergraph paper is evidently the "[[10]](https://arxiv.org/abs/2604.14592)" cited by Joshi–Nguyen–Johnston). Nothing on multistability in the passages seen. |
| CRITERIA tool paper | arXiv:2604.20683, 22 Apr 2026 [[21]](https://arxiv.org/abs/2604.20683); PLOS Comput. Biol. version [[22]](https://pubmed.ncbi.nlm.nih.gov/PMC13475990) | See below. |
| Mendoza et al., ACR in rank-one kinetic systems | arXiv:2304.03611 [[23]](https://arxiv.org/abs/2304.03611)[[24]](https://www.researchgate.net/publication/369911878_Absolute_Concentration_Robustness_in_Rank-One_Kinetic_Systems) | Power-law kinetic systems. Gives a necessary condition for ACR in rank-one multistationary systems [[24]](https://www.researchgate.net/publication/369911878_Absolute_Concentration_Robustness_in_Rank-One_Kinetic_Systems). Not a mass-action multistability result. |
| "Approximating Parameter Regions for Multistationarity and Multistability in Mass-Action Systems" | arXiv:2610.05242, 4 Oct 2026 [[25]](https://arxiv.org/abs/2610.05242) | Only a numerical-verification appendix was seen. No ACR statement seen. |

**The CRITERIA paper.** It treats the EnvZ–OmpR network (14 reactions), which has ACR in Yp, and shows it can have two positive equilibria or none [[21]](https://arxiv.org/abs/2604.20683)[[22]](https://pubmed.ncbi.nlm.nih.gov/PMC13475990). It also treats a CRISPRi toggle switch model with 17 species and 42 reactions. There it shows ACR in dCas9 "in addition to the system's capacity for multistationarity", and it attributes the bistability to an analysis in a different paper [[22]](https://pubmed.ncbi.nlm.nih.gov/PMC13475990). Stability is not established in the passages seen, and both models are large, so neither bears on minimality.

**An earlier ACR plus multistationarity example.** The 2023 prevalence paper gives {A⇌A+B, 2B⇌3B, A⇌2A}. It has ACR in A and, for one rate vector, exactly three positive steady states [[12]](https://arxiv.org/abs/2301.10337). The source does not discuss stability. The network contains a trimolecular complex (3B), so it falls outside KNS's at-most-bimolecular class.

## 3. The ACR plus bistability exhibit (arXiv:2605.11389v1)

- **Abstract:** the (E, E, C2, C2) network "simultaneously exhibits bistability and ACR in the final modification state, where the system can settle into either of two stable steady states with different intermediate concentrations yet identical final product concentration." [[5]](https://arxiv.org/abs/2605.11389)
- **Discussion:** "It is bistable, admitting two simultaneously stable positive steady states within the same compatibility class, and it has ACR in S2." [[5]](https://arxiv.org/abs/2605.11389)
- **ACR:** in S2, with value k2/k*3 [[5]](https://arxiv.org/abs/2605.11389).
- **Theorem 4.12, part 4:** "There exists a choice of positive rate constants and Te, Ts > 0 for which there are two positive stable steady states." [[5]](https://arxiv.org/abs/2605.11389)
- **Evidence for stability:** the claim rests on one explicit parameter point (k+1 = 645, k−1 = 2.2, k1 = 2.2, k+2 = 76.8, k−2 = 4, k2 = 4, k+3 = 8, k−3 = 1, k3 = 1, k+4 = 51, k−4 = 10.87, k4 = 10.87, Te = 12.45, Ts = 19.5). Jacobian eigenvalues at the three positive steady states there show two stable [[26]](https://arxiv.org/html/2605.11389).
- **Uniqueness:** the authors call it "the only one among the four that simultaneously exhibits bistability and ACR" [[26]](https://arxiv.org/html/2605.11389).
- **The other three networks:** (E,E,C2,C1) and (E,E,C1,C1) have multiple positive steady states and ACR but no bistability. (E,E,C1,C2) is bistable but has no ACR [[5]](https://arxiv.org/abs/2605.11389).

**Size.** The model has 8 species (e, c1, c2, c3, c4, s0, s1, s2) and two listed conservation laws, T_s and T_e [[5]](https://arxiv.org/abs/2605.11389). Its rate terms involve at most two concentrations multiplied. That is consistent with at-most-bimolecular mass action, but the paper does not classify it that way, and its reaction diagram is not reproduced here. With 8 species it is far above the 3-species bound, so it neither supports nor contradicts the conjecture. It does show that ACR and bistability can coexist.

## 4. Status of questions 2(a)–(d)

**(a) A 3-species, at-most-bimolecular network with ACR and two stable positive steady states.** None found in the sources retrieved. The only ACR-plus-bistability exhibit has 8 species [[5]](https://arxiv.org/abs/2605.11389). The Tang–Zhang classification gives 373 bistable (3,6,3) quadratic zero-one networks [[8]](https://arxiv.org/html/2608.01116), but the passages available do not test any of them for ACR. Whether one of them has ACR is therefore unestablished.

**(b) Dimension-2 networks.** Nothing proves or disproves that dimension-2 at-most-bimolecular networks cannot combine ACR with multistability. Related results:

- KNS prove dimension at least 2 is necessary for ACR with nondegenerate multistationarity [[2]](https://arxiv.org/html/2307.04186).
- KNS prove ACR is equivalent to non-multistationarity, outside a few exceptional cases, for bimolecular networks that are one-dimensional or have up to two species [[4]](https://researchprofiles.ku.dk/en/publications/absolute-concentration-robustness-and-multistationarity-in-reacti/).
- Jiao–Tang–Zeng prove that two-dimensional zero-one networks with up to three species admit no nondegenerate multistationarity or multistability [[7]](https://arxiv.org/abs/2406.11586). This covers the zero-one class only. KNS's tight example contains a "2C" complex, so it is not zero-one.

**(c) Minimum reactant complexes or complexes.** Nothing was found. For ACR plus multistationarity the KNS bounds stand [[2]](https://arxiv.org/html/2307.04186). For multistability alone, zero-one networks with three species and dimension 3 need at least six reactions, and a six-reaction multistable example exists. Verbatim: "If G admits multistability, then G has at least six reactions." [[7]](https://arxiv.org/abs/2406.11586) That is multistability without any ACR requirement. The complete statement is "the smallest zero-one networks that admit multistability contain three species and six reactions" [[6]](https://arxiv.org/html/2406.11586).

**(d) Proving, disproving or refining the conjecture.** None found. The Jiao–Tang–Zeng paper cites KNS only as background ("an at-most-bimolecular network admitting both multistationarity and absolute concentration robustness is at least two-dimensional and has at least three species and three reactions") [[6]](https://arxiv.org/html/2406.11586). No retrieved passage engages the conjecture itself.

## 5. Classical small ACR networks and bistability

The Shinar–Feinberg criterion gives ACR in species A_i when the deficiency is 1 and two non-terminal complexes differ only in A_i [[15]](https://arxiv.org/abs/2105.00109). The original activation/deactivation network {A+B→2B, B→A} is the basic example [[27]](https://arxiv.org/abs/1310.3761). Meshkat–Shiu–Torres show the criterion characterises ACR for networks with two reactions and no catalyst-only species. Up to ACR-preserving operations there are three families with two species and two reactions [[15]](https://arxiv.org/abs/2105.00109).

No bistable network of this classical small kind was found. The relevant statements are:

- Joshi et al. note that known ACR examples such as those of Shinar–Feinberg "typically are non-multistationary" [[12]](https://arxiv.org/abs/2301.10337).
- The single-site bifunctional-enzyme cycle (E, C1) has ACR in S1 and a unique, locally asymptotically stable positive steady state [[26]](https://arxiv.org/html/2605.11389).
- Deficiency-one ACR does not imply stability. {A+B→2B, B→0, A→2A} has deficiency 1 and static ACR in both species, but its unique positive steady state is never attracting [[28]](https://arxiv.org/abs/2104.14070).
- A Shinar–Feinberg-type network is also reported with an unstable ACR equilibrium [[27]](https://arxiv.org/abs/1310.3761).

The only ACR network found with demonstrated bistability is the 8-species dual-site cycle in Section 3.

## 6. Negative results and limits

- No retrieved paper cites KNS while addressing ACR plus multistability. The citing papers seen are background citations only [[6]](https://arxiv.org/html/2406.11586)[[14]](https://www.sciencedirect.com/science/article/pii/S0747717124001020).
- The Tang–Zhang data repository was not inspected, so the ACR status of the 373 bistable (3,6,3) networks is open.
- The Joshi–Nguyen–Johnston reference list was not available. The absence of a KNS citation is based only on the passages retrieved.
- The "August 24, 2026" HTML date and the undated abstract snapshot leave a small residual doubt about later arXiv versions of KNS.

## Synthesis

As of 25 Oct 2026, the conjecture is open. Two literatures have advanced separately. The minimal multistable zero-one networks are fully classified (3 species, 6 reactions, dimension 3) [[6]](https://arxiv.org/html/2406.11586)[[8]](https://arxiv.org/html/2608.01116). ACR plus bistability has been demonstrated in one 8-species futile cycle [[5]](https://arxiv.org/abs/2605.11389). Nobody has yet joined these by asking whether any minimal multistable network also has ACR, and that is the open step. A positive answer in a small class would test the conjecture directly. A proof that dimension-2 networks cannot combine the two properties would support its dimension part.

## Sources

[1] Absolute Concentration Robustness and Multistationarity in Reaction Networks: Conditions for Coexistence - https://arxiv.org/abs/2307.04186
[2] Absolute concentration robustness and multistationarity in reaction networks: Conditions for coexistence - https://arxiv.org/html/2307.04186
[3] Absolute concentration robustness and multistationarity in reaction networks: Conditions for coexistence | European Journal of Applied Mathematics | Cambridge Core - https://www.cambridge.org/core/journals/european-journal-of-applied-mathematics/article/absolute-concentration-robustness-and-multistationarity-in-reaction-networks-conditions-for-coexistence/BEABF13EA90E50ED45F64650BDEAC003
[4] Absolute concentration robustness and multistationarity in reaction networks: Conditions for coexistence - University of Copenhagen Research Portal - https://researchprofiles.ku.dk/en/publications/absolute-concentration-robustness-and-multistationarity-in-reacti/
[5] Bistability, Absolute Concentration Robustness, and Hysteresis in Dual-Site Futile Cycles with Bifunctional Enzymes - https://arxiv.org/abs/2605.11389
[6] Multistability of Small Zero-One Reaction Networks - https://arxiv.org/html/2406.11586
[7] Multistability of Small Zero-One Reaction Networks - https://arxiv.org/abs/2406.11586
[8] The Ubiquity of Three Steady States: Minimal Multistable Zero-One Reaction Networks - https://arxiv.org/html/2608.01116
[9] The Ubiquity of Three Steady States: Minimal Multistable Zero-One Reaction Networks - https://arxiv.org/abs/2608.01116
[10] Absolute Concentration Robustness of Non-Redundant Zero-One Networks with Conservation Laws - https://arxiv.org/abs/2604.14592
[11] Absolute Concentration Robustness and Multistationarity in Reaction Networks: Conditions for Coexistence - https://www.researchgate.net/publication/372248289_Absolute_Concentration_Robustness_and_Multistationarity_in_Reaction_Networks_Conditions_for_Coexistence
[12] Prevalence of multistationarity and absolute concentration robustness in reaction networks - https://arxiv.org/abs/2301.10337
[13] [2401.00078] Absolute concentration robustness: Algebra and geometry - https://arxiv.org/abs/2401.00078
[14] Absolute concentration robustness: Algebra and geometry - ScienceDirect - https://www.sciencedirect.com/science/article/pii/S0747717124001020
[15] Absolute concentration robustness in networks with low-dimensional stoichiometric subspace - https://arxiv.org/abs/2105.00109
[16] Connectivity of Parameter Regions of Multistationarity for Multisite Phosphorylation Networks - https://arxiv.org/abs/2403.16556
[17] Disconnectivity in Multistationarity Regions of Cascade of Goldbeter--Koshland Loops - https://arxiv.org/abs/2607.25456
[18] Prevalence of Multistationarity and Absolute Concentration Robustness in Reaction Networks - University of Copenhagen Research Portal - https://researchprofiles.ku.dk/en/publications/prevalence-of-multistationarity-and-absolute-concentration-robust/
[19] Bifunctional enzyme provides absolute concentration robustness in multisite covalent modification networks - https://arxiv.org/abs/2304.02679
[20] Bifunctional enzyme action as a source of robustness in biochemical reaction networks: a novel hypergraph approach - https://arxiv.org/abs/2504.21011
[21] CRITERIA: A network decomposition and elementary flux mode translation-based tool for computing equilibria of biochemical systems - https://arxiv.org/abs/2604.20683
[22] CRITERIA: A network decomposition and elementary flux mode translation-based tool for computing equilibria of biochemical systems - https://pubmed.ncbi.nlm.nih.gov/PMC13475990
[23] Absolute Concentration Robustness in Rank-One Kinetic Systems - https://arxiv.org/abs/2304.03611
[24] (PDF) Absolute Concentration Robustness in Rank-One Kinetic Systems - https://www.researchgate.net/publication/369911878_Absolute_Concentration_Robustness_in_Rank-One_Kinetic_Systems
[25] Approximating Parameter Regions for Multistationarity and Multistability in Mass-Action Systems - https://arxiv.org/abs/2610.05242
[26] Bistability, Absolute Concentration Robustness, and Hysteresis in Dual-Site Futile Cycles with Bifunctional Enzymes - https://arxiv.org/html/2605.11389
[27] Stochastic analysis of biochemical reaction networks with absolute concentration robustness - https://arxiv.org/abs/1310.3761
[28] Foundations of static and dynamic absolute concentration robustness - https://arxiv.org/abs/2104.14070
