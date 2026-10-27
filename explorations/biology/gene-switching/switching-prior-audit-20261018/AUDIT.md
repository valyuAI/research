# Equilibrium switching: prior-art and empirical audit

18 October 2026. Independent source audit. No outreach or data fit was performed.

## Decision

**The four-state construction is an exact two-site instance of a standard equilibrium symmetric exclusion process with a reservoir. It should not be promoted as a new switching architecture or a discovered genetic mechanism. Confidence: high.**

Its use as a particularly small counterexample to a topology-independent inference from constant mean-dwell switching time to dissipation may still be useful. The sharp concentration/state-count certificates and their statistical realization are more plausible subjects for an inference paper. Priority of those precise statements remains **unknown**, not established by this bounded search.

The most directly relevant gene paper restricts its analytic exclusion to a four-state cycle and explicitly leaves general equilibrium models open. We have an architecture outside that restriction, not a refutation of its class-specific proof. A current-supplement access gap remains. Public processed experimental data and the original observation code are available, but the proposed state-count test is not directly applicable to the published pooled burst summaries.

## 1. Exact architectural predecessor: equilibrium exclusion

Justin Salez, [*Universality of cutoff for exclusion with reservoirs*](https://projecteuclid.org/journals/annals-of-probability/volume-51/issue-2/Universality-of-cutoff-for-exclusion-with-reservoirs/10.1214/22-AOP1600.full), Annals of Probability 51(2), 478-494 (2023), DOI 10.1214/22-AOP1600, defines the needed model on arbitrary finite networks. Its [author manuscript, section 1.1](https://arxiv.org/html/2201.03463), gives symmetric exchanges between occupied/vacant vertices and reservoir resampling with a Bernoulli density. It explicitly establishes reversibility with the product Bernoulli distribution. Publication identity was independently checked on the publisher page; full model equations were inspected in the author manuscript.

For our four-state path, let `x1,x2` be binary site occupations. Relabel the states as follows:

| Original state | Two-site occupation | Observed activity |
|---|---|---|
| OFF0 | 00 | site 2 empty |
| OFF1 | 10 | site 2 empty |
| ON1 | 01 | site 2 occupied |
| ON2 | 11 | site 2 occupied |

Site 1 exchanges particles with the reservoir at empty-to-full rate `bc` and full-to-empty rate `b`. The two sites exchange their contents at rate `k`. Exchanges of equal occupations produce no transition. The complete state graph is therefore exactly

`00 <-> 10 <-> 01 <-> 11`,

with the rates in the original lead. In Salez's notation set

`rho=c/(1+c)`, `conductance(1,2)=k`,
`externalRate(1)=b(1+c)`, `externalRate(2)=0`.

Then reservoir creation is `externalRate(1)*rho=bc`, and destruction is `externalRate(1)*(1-rho)=b`. The parameterization is still elementary kinetics even though the reservoir's total reset rate depends on concentration. Product Bernoulli weights are `(1,c,c,c^2)/(1+c)^2` in this ordering.

This is an **exact generator identity**, not an analogy. Salez is a convenient verifiable primary source, not a claim to the first historical invention of exclusion processes. The identification is our direct specialization of the published model. The paper does not need to state our particular mean-dwell formula to preempt architectural novelty.

### General mean-dwell identity

Consider any finite connected undirected graph with symmetric constant hopping rates `h_ij=h_ji>=0`. At reservoir vertices let creation/destruction rates be `b_i*c` and `b_i`, with at least one `b_i>0`. The stationary law is independent site occupations with common probability `rho=c/(1+c)`:

- a hop preserves particle count and connects equal-weight configurations, with equal forward/reverse rates;
- a reservoir addition multiplies stationary weight by `c`, exactly matching the birth/death ratio.

These edge identities establish detailed balance directly. Let the binary observation be occupation of a vertex `i` having **no direct reservoir exchange**, and write `H_i=sum_j h_ij>0`. Its stationary OFF-to-ON crossing intensity is

`J_i=sum_j h_ij P(x_i=0,x_j=1)=H_i*rho*(1-rho)`.

Stationary occupation time divided by crossing frequency gives

`meanON = 1/[H_i*(1-rho)]`,
`meanOFF = 1/[H_i*rho]`,
`T_d = (1/meanON+1/meanOFF)^(-1)=1/H_i`.

No renewal or independence assumption is needed for these mean-episode identities. Larger networks generally do not have independent successive episodes. The two-site case has `H_2=k` and gives the lead exactly.

Consequences:

1. This invariant is a simple corollary of established equilibrium exclusion, with a broader family than one matched four-state path.
2. It survives arbitrary changes of symmetric hopping conductances and reservoir speeds, provided the observed vertex has no direct exchange and all reservoirs impose the same density. The numerical value changes with `H_i`, but its concentration invariance persists.
3. If direct reservoir exchange `b_i*c/b_i` is added at the observed vertex, the crossing intensity becomes `rho*(1-rho)[H_i+b_i*(1+c)]`, hence `T_d=1/[H_i+b_i*(1+c)]`. Exact invariance is lost. This is the physical leakage boundary already encountered in the lead.
4. The binding/translocation interpretation is legitimate mathematics. No evidence currently identifies a real promoter implementing this inaccessible-site geometry. Ordinary DNA sites can bind or release TF directly; deleting those pathways is a mechanistic assumption requiring support.

The standard exclusion generator also closes its dynamics on first moments. For the two-site construction, it acts on centered occupation observables by

`Q [f1,f2]^T = [[-(b(1+c)+k),k],[k,-k]] [f1,f2]^T`.

Its eigenvalues reproduce the two covariance rates in the lead. Thus the reduction of a four-state process to two covariance modes fits the standard exclusion structure too.

## 2. Other close predecessors and what they do not establish

**Yang and Pearson (2012): strongest direct predecessor for concentration-dependent dwell inference.** [*Origins of concentration dependence of waiting times for single-molecule fluorescence binding*](https://pubmed.ncbi.nlm.nih.gov/22755586/), J. Chem. Phys. 136, 244506. The [full author manuscript](https://arxiv.org/html/1206.0858) derives apparent dwell rates from stationary aggregate occupancies and crossing fluxes, explains rational concentration dependence using graph/tree methods, and examines dark binding sites, missed events and buffering.

Its Template III has the exact same four occupation labels and the same two-plus-two observation partition as our exclusion realization. However, its displayed transitions are ligand binding/unbinding at the two sites, whereas our central `10<->01` is ligand-conserving transfer. The graphs and kinetic rules are therefore distinct. Equations 10-12 give different rational dwell curves. This is a close conceptual prior, not an identified reproduction of the invariant path. It preempts any broad claim that concentration-dependent mean dwell curves reveal hidden binding complexity for the first time.

**Ravanelli et al. (2026): different time observable.** [*Decoupling between activation time and steady-state level in input-output responses*](https://pmc.ncbi.nlm.nih.gov/articles/PMC13245878/) investigates changing steady output with nearly invariant mean first-passage activation times, using rate separation and incoherent regulation in chain/ladder models. This is relevant mechanistic context, but first production after input introduction is not stationary ON/OFF episode duration, and its displayed results do not establish the lead's exact `T_d` invariant or finite-dose state-count certificate.

**Siekmann (2026): current identifiability synthesis and original analysis.** [*Modelling ion channels with a view towards identifiability*](https://pmc.ncbi.nlm.nih.gov/articles/PMC12685997/) analyzes aggregated Markov model non-identifiability, including the fully connected three-state case. It reinforces that hidden mechanistic topology is not identified merely because a model fits binary data. Its inspected text does not state our particular three-concentration inverse-mean feasibility test. It should be cited as a nearby theory boundary, not represented as proving uniqueness of our model.

**Equilibrium chromatin/enhancer bursting already exists.** The [2025 chromatin/enhancer model](https://www.biorxiv.org/content/10.1101/2025.11.29.691276.full) expressly uses equilibrium detailed balance in an MWC-like occupancy ladder. It is prior against novelty of equilibrium bursting. Its ON/OFF definitions threshold averaged TF occupancy, and several formulas remain image placeholders in the available extraction. It is not a completed algebraic exclusion of overlap with the narrower invariant.

Searches for optimal dose selection also found an established model-discrimination design literature, including [*Impact of the Error Structure on the Design and Analysis of Enzyme Kinetic Models*](https://pmc.ncbi.nlm.nih.gov/articles/PMC10008308/) and work on T/KL-optimal designs. Those search results are leads for a dedicated priority review, not verified matches to the proposed geometric dose triple. The precise objective matters: deterministic relative target-mean boxes are not D-optimal estimation, KL-optimal discrimination, or automatically an optimal statistical power design.

## 3. What can be claimed about the finite-sample results now

The singleton observation is elementary: any nontrivial binary partition of at most three states has a singleton side; its holding time is exponential with exit rate `A+B*c` for nonnegative affine elementary rates. Excluding both singleton orientations across concentrations excludes all such models. This is a model-class exclusion, not thermodynamic inference, and not identification of the four-state witness.

The matrix-tree rational-function route to concentration dependence is explicitly established in Yang/Pearson. The lead's sharp four-point exact-data certificate, the three-dose interval screen, and the parent thread's optimum-dose expression may be new special statements, but that priority has **not** been established. No exact matching theorem appeared in the inspected sources. Several literal searches were low quality or irrelevant; these are retained in the raw records and are not evidence of novelty.

For the proposed finite-record test:

- Exact exponential confidence intervals apply to truly observed, complete singleton episodes collected under the sampling scheme used in their derivation.
- A fixed number of complete episodes collected by running to the final transition is different from selecting only episodes wholly contained in a fixed observation window. The latter preferentially omits long episodes.
- Under the union null (singleton ON or singleton OFF), requiring rejection of both orientations is an intersection-union test. Each orientation still needs valid simultaneous concentration coverage; no extra factor of two is required merely for taking the intersection.
- Unknown free ligand concentration, heterogeneous fixed parameters across cells, missed short episodes, nonstationarity, or a state label produced by temporal filtering can violate the test's premise without the underlying molecule having four states.
- The proposed optimal triple `(1/r,1,r)` is expressed in dimensionless `c=L/K_d`. It is not directly implementable without knowing or estimating the relevant concentration scale. Optimizing target-box width is also not proof of optimal power or recording time under a finite experimental budget.

## 4. Current PNAS claim and supplement status

The current [Zoller et al. PNAS paper](https://pmc.ncbi.nlm.nih.gov/articles/PMC13367843/) uses `T_C=T_ON*T_OFF/(T_ON+T_OFF)` and explicitly states the analytic equilibrium exclusion applies within its four-state cycle class. Its discussion leaves exclusion of arbitrary equilibrium models open. The exclusion-path observation should therefore be framed as a concrete architecture outside the studied topology.

The paper also requires an effective two-state description with a single dominant covariance time and TF residence much shorter than switching time. Matching `T_d` alone is insufficient. The analytic approximation in the lead is useful because it addresses dominance of the slow covariance mode, but it has not yet been propagated through the actual experimental observation pipeline or compared under matched experimental constraints.

I repeated retrieval of the current supplementary PDF from the publisher and PMC, using high extraction effort. The publisher extraction returned no content; PMC returned a download placeholder. Records: `current-supplement-retry.json`. This does not close the current-SI gap. Previously retrieved preprint captions and author code must remain labeled as such.

## 5. Real public data and the observation boundary

The experiments underlying the theory are [Chen et al., *A conserved coupling of transcriptional ON and OFF periods underlies bursting dynamics*](https://pmc.ncbi.nlm.nih.gov/articles/PMC13137155/), Nat. Struct. Mol. Biol. 32, 1959-1971 (2025), DOI 10.1038/s41594-025-01615-4.

Public processed data are at [Zenodo 15396340](https://zenodo.org/records/15396340), with a verified [API manifest](https://zenodo.org/api/records/15396340). The record describes single-allele time-lapse measurements from hundreds of embryos, seven endogenous genes and three mutant constructs, in MATLAB structures. License: CC BY 4.0. Original full movies are stated to be available on request; no request was made.

| File | Size in decimal GB | Intended role |
|---|---:|---|
| `DataGap.zip` | 4.4935 | processed measured fluorescence traces |
| `OutDeconvGap.zip` | 12.9831 | deconvolution outputs |
| `OutDeconvSim.zip` | 14.1024 | simulations/deconvolution validation |
| `OutDeconvHuman.zip` | 0.1445 | reanalyzed human data |

The [authors' code repository](https://gitlab.pasteur.fr/tglab/liveburstrulepaper) is MIT licensed and includes a small **hunchback NC14 test case**, avoiding an initial multi-GB download. Its verified tree contains:

- `Deconvolution/DataGap/hb_MS2_INTRON_NC14_OutDS.mat`;
- `Deconvolution/OutDeconvGap/DECONV_hb_MS2_INTRON_Nc14_AP16.mat`;
- `Deconvolution/OutDeconvGap/BPHENO_hb_MS2_INTRON_Nc14_AP16.mat`;
- `Deconvolution/OutDeconvGap/Data_hb_MS2_INTRON_Nc14.mat`;
- probe-kernel and measurement-noise files.

Directly inspected source functions include [ExtractIniPheno.m](https://gitlab.pasteur.fr/tglab/liveburstrulepaper/-/raw/main/Deconvolution/ExtractIniPheno.m), [MainSimData.m](https://gitlab.pasteur.fr/tglab/liveburstrulepaper/-/raw/main/LiveAnalysis/MainSimData.m), and [MainAutoCorrelation.m](https://gitlab.pasteur.fr/tglab/liveburstrulepaper/-/raw/main/LiveAnalysis/MainAutoCorrelation.m). The simulation pipeline already convolves initiation events with the probe kernel and adds signal-dependent noise. The original code, not a fresh invented detector, is the right comparison starting point.

The experimental paper documents these material restrictions:

1. Fluorescence is sampled every 10 seconds. Initiations are inferred by Bayesian deconvolution; the measured signal is not a directly observed promoter bit.
2. Burst calls threshold a quartic-smoothed initiation trace, with kernel width 50 seconds and a two-initiation threshold. The article's prose rounds the window to about one minute.
3. Its approximate shortest reliable ON/OFF episodes are 30/10 seconds, respectively. The finite nuclear-cycle duration bounds the available record.
4. Each spot combines two unresolved sister chromatids. Single-gene-copy burst parameters are obtained using independent/weakly correlated copy assumptions.
5. The paper explicitly says pooled dwell distributions reflect nonstationary dynamics and are unsuitable for directly testing stationary exponential distributions.
6. The theory comparison is mainly `T_C` versus activity, not measurements at three calibrated free ligand concentrations with all other kinetic parameters fixed.

Therefore **do not apply the singleton exponential test to the supplied pooled BPHENO summaries and advertise a physical state count**. These data are a legitimate test bed for forward observation and predictive model comparison, after controlling for time dependence and copy structure. They do not currently supply the simple calibrated-dose experiment assumed by the theorem.

### A numerical observability check, not a data fit

At the lead's illustrative `b=120/min`, `k=2/3/min`, `c=1`, direct evaluation gives:

- fast covariance decay time: 0.2493 seconds;
- fast covariance weight: 0.000007716;
- slow covariance time: 1.50418 minutes;
- `T_d`: 1.5 minutes;
- integrated covariance time: 1.50417 minutes;
- both dwell `CV^2`: 1.00278.

The fast mode is far below the 10-second frame spacing; the longer decay differs from the target by about 0.279%. This demonstrates a concrete resolution mismatch. It does **not** prove impossibility of discrimination from the available sample size, because many trajectories can constrain slower statistics and the detector can introduce other effects. Calculation retained in `observability-illustration.json`.

## 6. Concrete next experiment/computation

The worthwhile next result is an identifiability study, not a claim that cells use this equilibrium mechanism.

First reproduce the supplied hunchback test case using the authors' observation functions. Then compare a telegraph baseline, the reversible exclusion witness, and the published cycle, using the same copy structure, initiation process, probe kernel, frame times, noise and burst caller. Fit on one subset of embryos and evaluate held-out traces or predictive statistics. Use both latent and observed episode statistics in simulations so detector-induced signatures are visible.

For a direct experimental state-count test, the required inputs are externally calibrated free ligand doses, a fixed binary state definition, complete well-resolved episodes and controlled stationarity. The Drosophila archive does not by itself verify those premises. A separate calibrated single-molecule or synthetic-switch dataset may be more suitable, but no such dataset has been fully audited here.

The remaining publication question is specific: can the sharp dose/mean-dwell certificate plus a realistic observation analysis add a useful inference result beyond established aggregate Markov and concentration-response theory? This audit supports pursuing that question while explicitly withdrawing architectural novelty.

## Audit artifacts

All web search/fetch work used the Valyu CLI. Full retrievals, search outputs and third-party code extractions remain in the unpublished working record and are not redistributed in this package. The following filenames identify those records:

- `exclusion-primary-full.json`, `exclusion-primary-0.md`: exact standard-model mapping source;
- `current-published-priors.json`: Salez publication identity and Yang/Pearson record;
- `closest-priors-full.json`: Yang/Pearson, Ravanelli et al., Siekmann full texts;
- `public-data-records.json`: verified Zenodo manifest;
- `data-readme-code.json`: public test-data paths and workflow README;
- `observation-code.json`: detector, simulation and covariance-analysis functions;
- `current-supplement-retry.json`: unresolved current-SI retrieval gap;
- `observability-illustration.json`: numerical example, explicitly not fitted.
- `exclusion-mapping-checks.json`: five passing symbolic checks of the exact generator mapping, balance, flux and invariant.
