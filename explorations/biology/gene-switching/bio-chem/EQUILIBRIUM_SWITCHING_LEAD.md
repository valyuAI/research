# Reversible switching with an invariant mean-dwell timescale

Exploratory result, 18 October 2026. Correctness confidence: high for the
identities below, checked independently by two agents and by symbolic algebra.
The architecture is a known two-site equilibrium exclusion process, as established
in the [current prior-art audit](../switching-prior-audit-20261018/AUDIT.md).
Originality of the inference consequences is unresolved. This is not a paper
or a claim about the operating regime of any real gene.

## The construction

For dimensionless ligand concentration `c>0` and rates `b,k>0`, take the path

```text
     b c              k              b c
OFF0 <--> OFF1       <--> ON1         <--> ON2
      b               k               b
```

The four states have ligand occupancies `0,1,1,2`; the first two are OFF and
the last two ON. In this ordering the generator is

```text
Q = [ -bc    bc      0      0  ]
    [   b  -b-k      k      0  ]
    [   0     k   -k-bc    bc  ]
    [   0     0      b     -b  ].
```

All association rates are linear in concentration; all dissociation and
conformation rates are constant. The stationary distribution is

`pi=(1,c,c,c²)/(1+c)²`.

Every edge satisfies detailed balance, so steady entropy production of this
regulatory chain is zero. Transcriptional readout, ligand-reservoir maintenance
and the biological cell can consume energy. The result concerns insufficiency
of switching observations to infer nonequilibrium of the switch; it does not
say that real transcription or cellular function can run without energy.
The ON probability and stationary OFF-to-ON event flux are

`p=c/(1+c)`, `J=k c/(1+c)²`.

The successive OFF and ON episodes start in states OFF1 and ON1 respectively.
By occupation-time/event-frequency accounting, their mean lengths are

`E[T_OFF]=(1+c)/(kc)`, `E[T_ON]=(1+c)/k`.

Consequently the switching timescale computed from mean dwell times is
**exactly**

`T_d=(1/E[T_OFF]+1/E[T_ON])^(-1)=1/k`

at every positive concentration, although the mean ON fraction ranges from
zero to one. This is a finite elementary-kinetics equilibrium construction,
not an effective two-state generator with postulated nonlinear rates.

## Full activity autocorrelation: a two-dimensional proof

Let `f=(0,0,1,1)-p*1` be the centered ON indicator and put `a=b(1+c)`.
Direct multiplication gives

`Q f=(0,k,-k,0)`,

`Q² f+(a+2k)Q f+ak f=0`.

For the normalized stationary covariance

`C(t)=<f,exp(tQ)f>_pi / [p(1-p)]`,

this implies the scalar ODE

`C''+(a+2k)C'+ak C=0`, `C(0)=1`, `C'(0)=-k`.

Hence, with `D=sqrt(a²+4k²)`,

`r_-=(a+2k-D)/2`, `r_+=(a+2k+D)/2`,

`w_-=(1+a/D)/2`, `w_+=(1-a/D)/2`,

we obtain

`C(t)=w_- exp(-r_- t)+w_+ exp(-r_+ t)`.

Both weights are positive at finite `b,k,c`. The output is therefore not an
exact telegraph process and does not have an exactly single-exponential
autocorrelation. The distinction is essential.

In particular, `C''(0)=2k²`, whereas `exp(-kt)` has second derivative `k²`.
The fast boundary layer permits uniform approximation of the function
without convergence of its second derivative at zero. Sufficient temporal
resolution could therefore expose an exact difference even for large `b/k`.

Its normalized integrated autocorrelation time is

`tau_int = integral_0^infty C(t) dt = 1/k + 1/[b(1+c)]`.

This also follows from the resolvent

`Laplace[C](s)=(s+a+k)/(s²+(a+2k)s+ak)`.

Thus `0 < k*tau_int-1 <= k/b` uniformly over **all** positive concentrations.

For `epsilon=k/b<1`, one also has a uniform-in-time, uniform-in-concentration
bound

`sup_(c>0,t>=0) |C(t)-exp(-kt)| <= epsilon/[e(1-epsilon)]`.

Proof: `k-r_-=2k²/(D+a)<=k²/a`, so
`r_->=k(1-epsilon)`. The mixture has mean decay rate
`w_-r_-+w_+r_+=k`, so Jensen's inequality gives
`exp(-kt)<=C(t)<=exp(-r_-t)`. The mean value theorem bounds the difference
of these endpoints by `(k-r_-)/(e*r_-)`. Separately, the fast-mode weight
obeys `w_+=2k²/[D(D+a)]<=epsilon²`.

The same calculations therefore establish approximate single-exponential
behavior, not merely agreement of one time integral.

## Episode statistics and a quantitative telegraph approximation

The exact squared coefficients of variation of the ON/OFF dwell times are

`CV_OFF²=1+2k/[b(1+c)²]`,

`CV_ON²=1+2kc/[b(1+c)²]`.

These differ from the exponential value one but approach it uniformly as
`k/b` decreases. They provide a potential discrimination observable if the
measurement resolution is sufficient. The extra exponential component in
`C(t)` is another such observable. Neither observable distinguishes all
equilibrium models from all nonequilibrium models.

More strongly, either dwell distribution is a positive mixture of two
exponentials. Write `r=kc/(1+c)` for OFF or `r=k/(1+c)` for ON. The two decay
rates `l_-<l_+` satisfy

`l_-+l_+=a+k`, `l_- l_+=a*r`.

The survival probability is

`S(t)=(1-w) exp(-l_-t)+w exp(-l_+t)`,

`w=(k-l_-)/(l_+-l_-)`.

Because the corresponding quadratic is nonpositive at `k` and at `a`,
`l_-<=k<=l_+` and `l_-<=a<=l_+`. If `a>k`, then

`r/(1+k/a)<=l_-<=r`, `0<=w<=k/(a+k)`.

For the weight bound, cross-multiplication reduces to
`(a-k)*l_->=0`.

Two exponential densities cross once; their total variation distance equals
the maximum difference of their survival functions. The mean value theorem
and `r/l_-=l_+/a<=1+k/a` bound this distance by `k/(ea)`.
Mixture convexity then gives, uniformly over concentration,

`TV(Law(T), Exp(r)) <= epsilon/(1+epsilon) + epsilon/e`.

Successive dwell times are independent with alternating ON and OFF laws,
since every crossing enters the opposite macrostate at a unique microstate.
By product coupling, the law of any fixed `m` successive dwell times, started
at a transition, differs in total variation from the corresponding telegraph
dwells by at most `m*[epsilon/(1+epsilon)+epsilon/e]` (or the trivial bound 1).
This is an event-indexed statement. It is not a demonstrated bound for
stationary mRNA distributions, sampled experimental trajectories, or an
unbounded observation horizon.

## Thermodynamic and biological scope

An occupancy-based thermodynamic interpretation needs no artificial
concentration-dependent internal energy. Take the four standard-state
energies equal and ligand chemical potential proportional to `log c`.
Grand-canonical weights are then `c^n`, with `n=(0,1,1,2)`, exactly as above.
The central conformation change preserves ligand count. For dimensional
concentration `L`, replace `c` by `L/K_d` and use association constant `b/K_d`.

This interpretation makes an architectural assumption: the OFF conformation
has the modeled occupancy states 0 and 1, and the ON conformation 1 and 2.
It is a gated-binding model, not the published one-enhancer four-state cycle.
No specific promoter or ligand has been shown to implement it.

The average number of bound ligands is `2c/(1+c)` and the association-event
flux is `bc/(1+c)`. Under an ordinary tagged-ligand realization of the modeled
occupancy transitions, occupation/arrival accounting gives mean ligand
residence `2/b`. Thus promoter switching can be arbitrarily slower than the
mean ligand residence, with ratio `b/(2k)`.

This is a statement about the mean. A small population of long residence
events can occur during gating. Fast internal equilibration alone would not
have justified a claim about ligand residence, and this calculation does not
show that every residence event is fast or determine a unique labeled-ligand
residence distribution from the unlabeled four-state generator.

For a concrete mathematical scale, `k=2/3 min^-1`, `b=120 min^-1` gives
`T_d=1.5 min` and mean ligand residence `1 s`. The integrated covariance time
differs from `T_d` by at most `0.00834 min`, and the uniform covariance bound
is below `0.00206`. This is an illustrative parameter choice, not a data fit.
Across `c=0.001` to `1000`, activity varies from `1/1001` to `1000/1001`.

Exact invariance uses matched binding equilibria and symmetric gate rates.
It must not be advertised as generic or automatically robust to arbitrary
mutations. Small detailed-balance-preserving kinetic perturbations preserve
approximate agreement on any fixed compact concentration range by finite
matrix continuity. Additional concentration-dependent cross-partition edges
generally destroy exact invariance; for example adding reversible edges
`0<->2` and `1<->3` with forward rate `eta*b*c` and backward `eta*b` changes
the exact mean-dwell time to `1/[k+eta*b*(1+c)]`. Approximation on a specified
finite range survives if `eta*b*(1+c_max)` is small compared with `k`.

## An exact boundary that explains the distinction

Let a finite irreducible reversible generator have elementary concentration-
affine off-diagonal rates `q_ij(c)=u_ij+c*v_ij`, with `u_ij,v_ij>=0`. Suppose a
nontrivial binary output has an **exactly single-exponential** normalized
stationary covariance `exp(-kt)` with the same `k>0` for every concentration
in an interval. Its stationary mean must then be constant on that interval.

Proof: reversibility makes the covariance a positive spectral mixture.
A single exponential therefore implies `Q(c)(F-p(c))=-k(F-p(c))`.
For every OFF state the total rate into ON is `k*p(c)`; for every ON state
the total rate into OFF is `k*(1-p(c))`. Add one rate from each kind of state.
The result is the constant `k`, but every coefficient of `c` in the sum is
nonnegative. Each such coefficient must vanish. The OFF rate, and hence
`p(c)`, is constant. This is a short consequence of reversible spectral
theory and lumpability, not currently asserted as a new theorem.

The constructed path escapes this exact boundary through a small positive
fast mode. It shows why arbitrarily accurate approximate single-exponential
behavior cannot be substituted for exact single-exponential behavior in
that argument.

## Four states are minimal in the elementary affine-rate class

Consider any finite irreducible CTMC with a fixed nontrivial ON/OFF partition
and off-diagonal rates `q_ij(c)=u_ij+c*v_ij`, where `u_ij,v_ij>=0`.
Assume irreducibility for every `c>0`. If it has at most three states and its
switching timescale `T_d` is exactly constant on any nonempty open
concentration interval, its stationary ON probability is constant too.
Reversibility is not needed for this lower bound.

Proof: one side of a nontrivial binary partition of at most three states is
a singleton. If OFF consists of state `i`, its mean dwell time is
`1/q_i(c)`, where `q_i(c)=sum_(j!=i)q_ij(c)=A+B*c`, `A,B>=0`.
For stationary ON probability `p(c)` and OFF-to-ON event flux `J(c)`,

`J(c)=(1-p(c))*q_i(c)`,

`T_d=p(c)*(1-p(c))/J(c)=p(c)/q_i(c)`.

Thus constancy `T_d=tau>0` implies `p(c)=tau*(A+B*c)` on the interval.
The stationary probabilities are rational functions of `c`, by the
finite-state matrix-tree formula (or Cramer's rule for the stationary linear
system). Their denominators are nonzero for `c>0` by irreducibility.
The identity therefore holds for every `c>0`. Since `0<p(c)<1`, letting
`c` grow forces `B=0`, so `p(c)` is constant. If ON is the singleton, apply
the same argument to `1-p(c)`.

Our four-state path attains the bound within the still narrower reversible,
grand-canonical, occupancy-local elementary-kinetics class. The result does
not apply to postulated effective rates containing rational functions of
concentration, negative concentration coefficients, or a concentration-
dependent definition of ON. Exact constancy, not a finite-accuracy fit, is
essential. The elementary argument still requires a priority check before
it can be called new.

The independently checked finite-sampling obstruction is concrete: a
reversible three-state path with rates `0->1:13c`, `1->0:13`, `1->2:c`,
`2->1:1` and ON state `{1}` has

`T_d=(1+c²)/[(1+c+c²)(13+c)]`.

It equals `1/21` at `c=1,2,4`, despite changing activity, because

`T_d-1/21=-(c-1)(c-2)(c-4)/[21(c+13)(c²+c+1)]`.

Thus even three exact equal measurements do not establish interval
invariance or the four-state lower bound. The independent review is saved in
the dose-design audit linked below.

### Four concentrations suffice, and the threshold is sharp

Under the same finite-state, irreducible, nonnegative-affine-rate assumptions,
suppose `T_d(c_j)=tau` at four distinct positive concentrations. If the measured
activities at those concentrations are not all equal, the model has at least
four states. This statement does not require reversibility.

For at most three states, choose a singleton side of the binary partition
and write the probability of the opposite side as `p_opp=N(c)/Z(c)`.
The Markov-chain tree formula gives numerator and denominator polynomials
of degree at most two, with `Z(c)>0` for all `c>0`. The singleton's exit rate
is `A+Bc`, with `A,B>=0`, and stationary crossing balance gives
`T_d=p_opp/(A+Bc)`. Thus the four measurements are four distinct roots of

`R(c)=N(c)-tau*(A+Bc)*Z(c)`.

This polynomial has degree at most three, so it vanishes identically.
Consequently `p_opp=tau*(A+Bc)` for every positive concentration. Since a
probability is bounded, `B=0`; activity is therefore constant, a contradiction.
The three-state example above attains equality at three distinct points with
three distinct activities, so four is the smallest universal sample count.

This is an **exact-data certificate**. Measurement error, finite-record dwell
estimation, missing short episodes and uncertain concentration calibration
are outside the result. No robust statistical state-count test is claimed.
The symbolic checker verifies the sharpness example and its exact polynomial
factorization; the general degree argument is the written proof above.

### A three-concentration dwell-curve screen with deterministic error bounds

There is a simpler necessary condition when the two mean dwell curves are
available separately. In every model with at most three states, one
macrostate is a singleton. Its episode duration is exponential with exit
rate `A+B*c`, where `A,B>=0`. Consequently at least one of `1/meanON(c)` and
`1/meanOFF(c)` must be a nonnegative affine function. This argument requires
neither reversibility nor exponential durations for the other macrostate.

For a positive mean-dwell interval `[l_j,u_j]` at known concentration `c_j`,
the corresponding inverse mean lies in `[1/u_j,1/l_j]`. Test the two
macrostate series separately for feasibility of

`A>=0, B>=0, 1/u_j <= A+B*c_j <= 1/l_j` for every `j`.

If both systems are infeasible, all at-most-three-state models in this
affine-rate class are excluded. If either system is feasible, this screen
is inconclusive; it does not construct a compatible three-state model.
The checker implements the two-variable feasibility calculation with exact
rational arithmetic by eliminating the intercept.

For the four-state witness with `k=1`, concentrations `c=(1,2,4)` give
`meanON=(2,3,5)` and `meanOFF=(2,3/2,5/4)`. Specify **deterministic boxes
centered on these target means**: each allowable mean is between
`(1-epsilon)` and `(1+epsilon)` times its target, with `0<=epsilon<1`.
Their inverse intervals are the target inverse means divided by
`1+epsilon` and `1-epsilon`.

The singleton-ON hypothesis requires a nondecreasing inverse mean, but its
concentration-1 lower bound exceeds its concentration-4 upper bound when

`1/[2(1+epsilon)] - 1/[5(1-epsilon)]`
`= (3-7*epsilon)/[10(1-epsilon²)] > 0`.

Thus singleton ON is excluded for `epsilon<3/7`. For singleton OFF, every
affine function at concentrations 1,2,4 satisfies `2*f(1)-3*f(2)+f(4)=0`.
The target inverse OFF means are `(1/2,2/3,4/5)`, and the largest possible
contrast over their error boxes is

`(9/5)/(1-epsilon) - 2/(1+epsilon)`
`= (-1+19*epsilon)/[5(1-epsilon²)]`.

It remains strictly negative for `epsilon<1/19`. Therefore these three
concentrations exclude **every model with at most three states** if all
six mean dwells belong to the stated boxes with relative halfwidth less
than `1/19`, about 5.26%. No constancy of a fitted switching timescale is
needed. At `epsilon=1/19`, the inverse-OFF line
`A=19/45, B=19/180` intersects all three inverse intervals. This makes the
threshold sharp for this affine-line feasibility screen; it neither proves
existence of a full three-state fit at the threshold nor limits stronger
tests using more information.

These are deterministic interval implications, not statistical confidence
statements. An experiment would need justified simultaneous bounds for the
actual mean dwell times, accurately known concentrations, and complete
episodes without missed short events or changing state labels. An error
bound around an observed estimate is not automatically the same as a box
centered on these theoretical targets. The singleton/affine observation is
elementary and is not claimed as a new theorem; its role here is a concrete
way to distinguish the proposed architecture within the stated model class.

## Current primary-source assessment

The exact model is the standard two-site symmetric exclusion process with a
reservoir at site 1 and the occupancy of site 2 as the binary observation.
[Salez, Annals of Probability (2023), DOI 10.1214/22-AOP1600](https://projecteuclid.org/journals/annals-of-probability/volume-51/issue-2/Universality-of-cutoff-for-exclusion-with-reservoirs/10.1214/22-AOP1600.full)
provides a verified primary definition and the product-Bernoulli equilibrium.
The invariant mean-dwell time extends to a non-reservoir site in any connected
symmetric exclusion network. Thus it is not a newly discovered architecture.

The current Zoller et al. PNAS paper, DOI 10.1073/pnas.2524855123,
restricts its analytic equilibrium exclusion to its four-state cycle and
leaves other equilibrium topologies open. Our path is outside that class,
not a counterexample to the stated class-specific theorem. Its current
supplement was not successfully extracted. The original experimental data
use deconvolution, temporal smoothing, unresolved gene copies and
nonstationary pooling; the ideal complete-dwell test cannot be applied to
those summaries directly.

The [source and observation audit](../switching-prior-audit-20261018/AUDIT.md)
contains verified predecessor mappings, data access points and remaining
uncertainties. The [dose-design audit](../switching-audit-20261018/AUDIT.md)
strengthens the three-concentration result above: it proves the optimal
relative-error design for a fixed concentration span and constructs a full
three-state model at the limiting error threshold. Its
[statistical extension](../switching-experiment-20261018/README.md) has a
finite-sample false-positive bound under its explicit acquisition assumptions.
No priority or biological-validation claim is made for these extensions.

## Reproduction

Run `python3 check_equilibrium_switching.py` in this directory with SymPy
1.14.0. On 18 October 2026 it passed 31 exact symbolic/feasibility checks plus 2,944
finite numerical evaluations of the analytic covariance bound. The checks
derive stationary balance, dwell moments, invariant-subspace identity,
resolvent and ligand accounting directly from the generator. The finite
bound grid is a sanity check; the uniform result rests on the inequalities
above. Results are in `equilibrium_switching_checks.json`.

The research task and revised review brief are recorded in the exploration README.
Full retrievals and service receipts remain in the unpublished working record.

Terminology correction after launch: the third submitted brief calls `T_d`
a harmonic mean. The displayed formula is correct, but `T_d` is half the
ordinary harmonic mean of the two dwell means. This note uses the explicit
switching-time definition throughout; the submitted prompt is retained as a
record of what was sent.
