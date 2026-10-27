# A finite-sample test for hidden gene-switching states

18 October 2026. Mathematical research note and synthetic experimental design.
No gene measurements have been analyzed here. Correctness confidence is high
conditional on the stated observation and model assumptions; originality and
experimental usefulness remain unresolved.

## What is new within this working investigation

The [four-state equilibrium construction](../bio-chem/EQUILIBRIUM_SWITCHING_LEAD.md)
shows that a changing active fraction can coexist with an exactly constant
switching time computed from mean ON/OFF episodes. The
[independent dose-design proof](../switching-audit-20261018/AUDIT.md) develops
a sharp three-dose screen and optimizes its deterministic error tolerance.
This note adds a statistical implementation with a finite-sample false-positive
guarantee and an exact-law simulation of its power. These are contributions
to this investigation, not yet claims of publication priority.

The test asks whether any continuous-time Markov model with at most three
hidden states and nonnegative concentration-affine rates could explain the
observed dwell data. It does not test energy consumption or establish that
the particular four-state model is correct.

## The null model and acquisition rule

The null consists of finite, time-homogeneous, irreducible CTMCs with two or
three states, a fixed nontrivial binary ON/OFF partition, and off-diagonal rates
`q_ij(c) = u_ij + c v_ij`, with `u_ij,v_ij >= 0`. The same parameters and state
partition apply at every measured concentration. Reversibility is unnecessary.

Choose `m` distinct positive concentrations and a positive complete-episode
count `n` in advance. At each concentration acquire the first `n` complete ON
episodes and first `n` complete OFF episodes following a genuine transition.
Discard a left-censored initial segment. Do not stop at a fixed wall-clock time
and silently discard the last unfinished episode. Pooling cells with different
rates, undetected transitions, uncertain dose, adaptive stopping and inferred
or smoothed ON/OFF labels are not covered by this guarantee.

One side of every such two- or three-state partition must contain a single
state. If ON is the singleton, its complete dwell lengths are independent
`Exp(A+B c)` variables, for constants `A,B >= 0`. The same statement holds for
OFF when OFF is the singleton. This follows directly from the CTMC holding
time law and the strong Markov property at successive genuine entries.
The other side need not have exponential durations or independent episodes.

## Test and proof of size control

For orientation `o` and dose `c_j`, let `S_oj` be the sum of its `n` observed
complete dwell lengths. Define a candidate singleton exit-rate interval

```text
I_oj = [q_(alpha/(2m),2n) / (2 S_oj),
        q_(1-alpha/(2m),2n) / (2 S_oj)],
```

where `q_(p,d)` is the lower-tail `p` quantile of a chi-square law with `d`
degrees of freedom. For each orientation separately, ask whether there exist
`A>=0,B>=0` such that `A+B c_j` belongs to every corresponding interval.
Reject the at-most-three-state null if and only if **both** feasibility
problems are infeasible.

Proof: under a true singleton orientation with rate `r_j=A+B c_j`, its sum
is `Gamma(n, rate=r_j)`, hence `2 r_j S_oj` is exactly `chi-square(2n)`.
Each dose interval covers its true rate with probability `1-alpha/m`.
The union bound therefore gives simultaneous coverage at least `1-alpha`
over all `m` doses, without requiring independence across doses. On this
coverage event the true `A,B` provide a feasible line. Rejecting both
orientations is a subset of rejecting whichever orientation is truly a
singleton. Thus the complete test's false-positive probability is at most
`alpha`, not `2 alpha`. This is an intersection-union construction using
standard gamma pivots and Bonferroni coverage.

No approximation, stationarity assumption, asymptotic normality, or distribution
assumption about the nonsingleton side is used in this size proof. The finite
episode-count acquisition rule is essential. Repeatedly inspecting the test
and stopping on rejection would be a different procedure.

The rate feasibility calculation eliminates `A`. For a candidate slope `B`,
the maximum of zero and all `lower_j - B*c_j` must not exceed the minimum
of all `upper_j - B*c_j`. Pairwise comparisons give an interval of feasible
slopes; the code evaluates that interval directly.

## Synthetic power calculation

The alternative is the previously derived four-state path with `k=1` and
`b/k=180`. Its mean durations are `(1+c)/k` for ON and `(1+c)/(kc)` for OFF.
Successive episodes are independent because every boundary crossing enters
the next macrostate at a unique microstate. Each episode is a positive
mixture of two exponentials. The script samples sums exactly in law: a
binomial draw chooses the number of fast-component episodes, followed by
independent gamma draws for the fast and slow sums. It does not approximate
these dwells as exponential or numerically discretize the CTMC.

The rate-mixture transforms were checked against 60 fresh subgenerator
resolvent evaluations; 12 sample-mean checks and a separate implementation
review corroborate the sampler. The theoretical size guarantee above is
not inferred from simulations. Nine three-state null parameter/count cases
provide additional regression checks, including constant and purely
concentration-proportional singleton exit rates and exchanged output labels.

Each power estimate uses 20,000 independent synthetic experiments, seed
`20261018`, and prespecified `alpha=0.05`. A full experiment comprises both
orientations at all three doses. Dose ratios below are in units of the
model's binding midpoint, whose value is assumed known for planning.

| Doses | Complete ON and OFF episodes per dose | Simulated rejection probability | Expected analyzed record-hours |
| --- | ---: | ---: | ---: |
| 1, 2, 4 | 50 each | 0.06% | 18.44 |
| 0.25, 1, 4 | 200 each | 89.24% | 82.50 |
| 0.1, 1, 10 | 50 each | 99.23% | 35.25 |

Record-hours sum the durations of the analyzed episodes over all three doses,
using illustrative `k=2/3 per minute` (`T_d=1.5 minutes`, `b=120 per minute`).
They exclude discarded initial segments and instrument overhead and are
expectations, not fixed experiment deadlines. Parallel acquisition may reduce
elapsed time only if the shared-parameter assumptions remain appropriate.
The table compares different concentration spans, not designs constrained to
the same span. Monte Carlo confidence intervals and every tested count are
retained in `design-power.json`.

The dose-design result optimizes **deterministic target-box error tolerance**
at fixed span, not this statistical test's power or total recording time.
For span `r^2`, its maximizing triple is `(1/r,1,r)` and its sharp tolerance
is `(r-1)^2/(r^2+6r+1)`. Broader spans allow more curvature to be seen but also
produce longer rare-state waits. The simulations quantify that tradeoff for
the selected grids; they do not prove a globally optimal statistical design.

## What would make this experimentally credible

The existing Drosophila studies use observation and inference steps that
this ideal-data test does not model, including finite frame rate, smoothing,
transcription deconvolution and nonstationary pooling. A next study must
propagate the candidate model through the actual measurement pipeline, or
use independently justified complete dwell observations. No direct fit to
published gene trajectories or rejection of the biological paper has been
performed here. See the separate prior-art audit.

The proof supports a narrow model-class test. Non-affine rates, hidden
heterogeneity or observation error could also cause rejection. The result
does not demonstrate equilibrium regulation in a cell, identify a mutation,
or contradict the existing paper's restricted four-state-cycle theorem.

## Reproduction

```bash
python3 -u check_design_power.py
python3 plot_design_power.py
```

Used Python 3.13, NumPy 2.3.3, SciPy 1.16.3. The simulation logs each design
and count immediately and saves all outputs. The full general proof is written
above; it has not been formalized in Lean.
