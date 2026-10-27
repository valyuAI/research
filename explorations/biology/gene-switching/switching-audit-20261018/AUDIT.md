# Finite-dose gene-switching audit

18 October 2026. Mathematical correctness: high confidence. Biological applicability and originality of the inference/design consequences: unresolved. The mechanism itself has an exact symmetric-exclusion interpretation and must not be presented as a new architecture. This audit introduces no biological observations and makes no priority claim.

The existing four-state construction and both finite-dose statements are correct. The apparent contradiction comes from a missing quantifier: four doses are necessary for a **universal** inference from equal switching times plus any change of activity; three well-chosen doses can exclude smaller models using the **numerical shape** of the activity or mean-dwell curves. The three-dose screen can be substantially strengthened by choosing doses around the affinity scale.

## 1. Precisely what is assumed

At every positive concentration `c`, the model is a fixed finite irreducible continuous-time Markov chain with fixed nonempty ON and OFF sets and off-diagonal rates

`q_ij(c)=a_ij+b_ij*c`, with `a_ij,b_ij>=0`.

The state graph and binary labels do not change with concentration. Define complete episode means `mON`, `mOFF`, stationary ON probability `p`, each-direction stationary crossing flux `J`, and

`Td=(1/mON+1/mOFF)^(-1)=p(1-p)/J`.

This is a mean-dwell timescale. It is not generally the integrated autocorrelation time or a single-exponential relaxation time. Elementary mass-action ligand kinetics form a narrower class; arbitrary mixed rates `A+B*c` need not have a single elementary ligand-binding interpretation.

If the chain has at most three microstates, one binary class is a singleton. Its complete durations are exponential with rate `A+B*c`; consequently at least one of `1/mON` and `1/mOFF` is nonnegative affine. This necessary condition needs neither reversibility nor stationarity at the start of an episode. The identities relating dwell means to `p` and `J` concern stationary occupation and flux.

## 2. Four versus three

For any at-most-three-state model, the Markov tree formula writes the opposite-class probability as `N(c)/Z(c)`, with both polynomials of degree at most two and `Z>0`. If `Td=tau` at four distinct positive doses, then

`N(c)-tau*(A+B*c)*Z(c)`

has four roots and degree at most three. It vanishes identically. Since the resulting probability `tau*(A+B*c)` is bounded as `c` grows, `B=0`, and the activity is constant. Thus **four equal Td values with any unequal activities** exclude every at-most-three-state model.

Three is insufficient for that universal implication. The elementary reversible path

`0 --(13c forward, 13 reverse)-- 1 --(c forward, 1 reverse)-- 2`

with only state 1 ON has `pi=(1,c,c^2)/(1+c+c^2)` and

`Td(c)-1/21=-(c-1)(c-2)(c-4)/[21(c+13)(c^2+c+1)]`.

At `c=(1,2,4)`, all three timescales equal `1/21`, while activity is `(1/3,2/7,4/21)`.

But specific triples of dwell means can violate both possible singleton conditions. There is no requirement to separately measure new observables: quantitatively known `p,Td` already determine `mON=Td/(1-p)` and `mOFF=Td/p`. The distinction is using the curve's values, rather than merely checking whether activity changes.

Suggested corrected campaign wording:

> Four equal switching-time measurements with any activity change give a universal exact lower bound of four states. Three suitably placed concentrations also suffice when the quantitative dwell curves exclude a singleton on either side; a deterministic interval test is available, and its tolerance depends strongly on dose placement.

## 3. Independent construction verification

The four-state elementary path has rates

`OFF0 --(bc,b)-- OFF1 --(k,k)-- ON1 --(bc,b)-- ON2`.

Direct generator calculations give

`pi=(1,c,c,c^2)/(1+c)^2`, `p=c/(1+c)`,

`mON=(1+c)/k`, `mOFF=(1+c)/(k*c)`, `Td=1/k`.

Every edge satisfies detailed balance. Complete dwell means were independently computed by solving the killed subgenerator equations, rather than copying the flux identities. This verifies the construction but does not demonstrate that a real promoter has this architecture.

The parallel prior-art audit identified an exact interpretation as a two-site symmetric exclusion process. Label the states `00,10,01,11`: a reservoir exchanges particles with site 1 at rates `bc,b`, and an occupied site 1 exchanges with empty site 2 at rate `k` in either direction (`10<->01`). ON means site 2 is occupied. This reproduces every displayed edge and both binary labels exactly. The construction is therefore a special case of that established model family. Any prospective contribution must be framed as a specific switching-inference or measurement-design consequence, with literature comparison of that consequence still required.

## 4. Exact deterministic interval criterion

Given known doses `c_j` and positive mean intervals `[l_j,u_j]`, test each orientation for feasibility of

`A>=0, B>=0, 1/u_j <= A+B*c_j <= 1/l_j`.

If neither orientation is feasible, every at-most-three-state affine-rate model is excluded. If either is feasible, the generic test is inconclusive.

For this particular four-state target, write doses as `x<y<z`, and let each mean interval be centered on its target with relative halfwidth `epsilon<1`. Scale time so `k=1`.

The ON inverse means are `g(c)=1/(1+c)`. The nondecreasing singleton-ON requirement fails whenever

`epsilon < (z-x)/(2+x+z)`.

The OFF inverse means are `f(c)=c/(1+c)`. Every affine function obeys

`(z-y)f(x)-(z-x)f(y)+(y-x)f(z)=0`.

Define `P=(z-y)f(x)+(y-x)f(z)` and `M=(z-x)f(y)`. The maximum possible contrast over the inverse-mean boxes is

`P/(1-epsilon)-M/(1+epsilon)`.

It is negative exactly when

`epsilon < E(x,y,z) = (y-x)(z-y)/(2xyz+xy+xz+y^2+yz+2y)`.

This supplies an explicit separating linear inequality, so numerical optimization is not needed to prove exclusion. The strict inequality matters: at equality a nonnegative affine OFF inverse-mean curve exists.

## 5. Stronger sharpness: a full three-state fit at the boundary

The old note only established sharpness for affine-line feasibility. For these target mean curves, it can be strengthened to exact model feasibility in the broader affine-rate class.

Take the three-state path `OFF0 <-> ON1 <-> ON2` with

`q01=A+B*c`, `q10=k`, `q12=d*c`, `q21=d`, for positive `k,d`.

Then `mOFF=1/(A+B*c)` and `mON=(1+c)/k`. The chain is irreducible and reversible, with unnormalized stationary weights `(k,A+B*c,c*(A+B*c))`.

At `epsilon=E(x,y,z)`, choose

`A+B*c = k*(c+xz)/[(1+x)(1+z)(1-epsilon)]`.

The OFF fitted means equal `(1-epsilon)` times their targets at the endpoints, and `(1+epsilon)` times their target at the middle dose. The ON means equal their targets exactly. Thus the entire six-mean box contains a valid three-state model at the threshold, and for every larger halfwidth. This proves the deterministic threshold is sharp for the information being used, whenever singleton ON has already been excluded.

For the old `(1,2,4)` example, this gives `epsilon=1/19`, `A/k=19/45`, `B/k=19/180`, exactly the prior affine witness. The new part is its explicit realization as a full CTMC.

The same construction shows any **two** exact target mean pairs can be fitted: set `A+B*c=k*(c+xz)/[(1+x)(1+z)]` for the two selected doses `x,z`. Thus three is the minimal number of concentrations for excluding at-most-three states from these mean curves in the stated broad model class.

Scope: the mixed `A+B*c` transition is allowed by the broad theorem but is not asserted to be an elementary ligand-binding reaction with fixed occupancy. Also, a one-dose test of the *full* dwell distributions could detect that neither side is exponential; the three-dose minimum here concerns the mean information only.

## 6. Optimal three-dose placement for a fixed concentration span

The chord under `f(c)=c/(1+c)` at an interior dose is

`h(y)=(y+xz)/[(1+x)(1+z)]`.

Maximizing the threshold is equivalent to maximizing `R=f(y)/h(y)`. Its derivative is

`dR/dy=(1+x)(1+z)*(xz-y^2)/[(1+y)^2*(y+xz)^2]`.

Thus, for fixed endpoints, the optimal middle dose is the geometric mean `y=sqrt(xz)`.

For a fixed endpoint ratio `z/x=r^2`, write the triple `(a/r,a,a*r)`. Then

`R=(1+a/r)(1+a*r)/(1+a)^2`,

`dR/da=(r-1)^2*(1-a)/[r*(1+a)^3]`.

Hence the optimal center is `a=1`, the model's affinity scale. The best triple is

`(1/r,1,r)`, with `E=(r-1)^2/(r^2+6r+1)`.

The ON exclusion threshold is `(r-1)/(r+1)`, which is larger for every `r>1`; OFF curvature is the limiting condition.

| Dose triple | Dose span | Sharp target-box halfwidth | ON means, k=1 | OFF means, k=1 |
| --- | ---: | ---: | --- | --- |
| 1, 2, 4 | 4-fold | 1/19 = 5.26% | 2, 3, 5 | 2, 1.5, 1.25 |
| 0.5, 1, 2 | 4-fold | 1/17 = 5.88% | 1.5, 2, 3 | 3, 2, 1.5 |
| 0.25, 1, 4 | 16-fold | 9/41 = 21.95% | 1.25, 2, 5 | 5, 2, 1.25 |
| 0.1, 1, 10 | 100-fold | 81/161 = 50.31% | 1.1, 2, 11 | 11, 2, 1.1 |

The improvement from 5.26% to 21.95% is mostly the wider concentration range, not a free statistical gain. The wider design also creates longer episodes at the outer doses. Optimal placement assumes the affinity scale is known or estimated in a separate pilot. It does not establish optimal statistical power, optimal total observation time, or robustness to uncertain concentrations.

A numerical instance: choose `k=1/60 per second`, `b=1 per second`, and doses `(0.25,1,4)`. ON means are `(75,120,300)` seconds, OFF means `(300,120,75)` seconds, activities `(0.2,0.5,0.8)`, and `Td=60` seconds. At 10% target-centered mean boxes, the OFF affine contrast has maximum `-49/132` in units `k=1`, while the ON endpoint monotonicity gap is `50/99`. Both exclusions are strict. These are synthetic model values, not experimental measurements.

## 7. Statistical test review

The adjacent `switching-experiment-20261018` analysis proposes an actual finite-sample null test, which is different from the target-centered interval calculation above.

Fix three doses and acquire the first `n` complete episodes of each orientation at each dose. If an orientation is a singleton with rate `lambda_j=A+B*c_j`, its duration sum `S_j` satisfies `2*lambda_j*S_j ~ chi-square(2n)`. Use the interval

`[chi2_quantile(alpha/6,2n)/(2*S_j), chi2_quantile(1-alpha/6,2n)/(2*S_j)]`.

For the true singleton orientation, all three intervals cover simultaneously with probability at least `1-alpha`, by Bonferroni. Reject the at-most-three-state null only if neither orientation admits a nonnegative affine line through its rate boxes. The rejection event is a subset of rejecting whichever orientation is truly singleton. Therefore the overall false-positive probability is at most `alpha`, **not** `2*alpha`. No distributional assumption about the other orientation is required for this size proof.

The relevant complete singleton episodes are independent by the strong Markov property. Independence between doses is unnecessary for the Bonferroni bound. A stationary initial state is unnecessary if genuine entries are used. Discard the initial left-censored segment, fix the episode count in advance, and do not replace this protocol with all episodes completed before a fixed time without rederiving coverage.

The neighboring implementation's alpha split, gamma-mixture summation, and affine-intercept elimination were reviewed. Its four-state episode laws reset at fixed entry microstates, so successive ON and OFF episodes are independent; simulating their sums separately is legitimate. Its exact phase-type law is a positive mixture of two exponentials. Conditional on the number of fast components among `n` iid durations, the two component sums are independent gamma variables, including zero-shape sums interpreted as zero.

The simulation's expected record-hours are the expected sum of the specified complete analyzed durations. Any initial discarded segment, lost records, cell turnover, tracking failures, dose changes, and experimental overhead add acquisition cost. No heterogeneity, missed events, concentration error, or detector model is included. Its power numbers are model-based synthetic estimates, not guarantees for live measurements.

## 8. Reproduction and limits

Run `python3 check_switching_audit.py` in this directory. It passes 36 exact symbolic checks, including the generator equations, sharpness counterexamples, threshold formula, optimal-placement derivatives, and full three-state boundary realization. Output: `checks.json`.

Run `python3 check_experiment_audit.py` for a separate numerical audit of the adjacent simulation. It compares its affine feasibility calculation with 500 independent HiGHS linear programs, then compares its gamma-mixture sums with direct simulation of actual CTMC jumps. Output: `experiment-audit.json`. The numerical cross-checks supplement the mathematical proof and are not its substitute.

This audit used local proof notes, code, and source-audit records. No new literature retrieval was needed for these algebraic checks. The current published supplement and complete close-prior comparison remain separate blockers for a novelty claim. The singleton condition is elementary, and the optimal-dose calculation is a relative approximation problem; neither should be marketed as novel without a targeted literature comparison. The scientific contribution, if any, would require the full mechanism/inference comparison and a credible experimental use case.
