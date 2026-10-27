"""Finite-sample singleton rejection and model-based experimental planning.

Scientific calculation, not an analysis of observed gene trajectories. The
false-positive argument is written in README.md; Monte Carlo checks are not
its proof. Each simulated experiment acquires a prespecified episode count.
"""

import json
import math
from pathlib import Path

import numpy as np
import scipy
from scipy.stats import beta, chi2


SEED = 20261018
REPLICATES = 20000
ALPHA = 0.05
BINDING_TO_GATE_RATIO = 180.0


def affine_feasible(lower, upper, doses):
  """Eliminate the intercept from lower <= A+B*c <= upper, A,B >= 0."""
  doses = np.asarray(doses)
  slope_lower = np.zeros(lower.shape[0])
  slope_upper = np.min(upper / doses, axis=1)
  for i, ci in enumerate(doses):
    for j, cj in enumerate(doses):
      if cj > ci:
        slope_upper = np.minimum(slope_upper, (upper[:, j] - lower[:, i]) / (cj - ci))
      elif cj < ci:
        slope_lower = np.maximum(slope_lower, (upper[:, j] - lower[:, i]) / (cj - ci))
  return slope_lower <= slope_upper


def reject_from_sums(on_sums, off_sums, doses, count, alpha=ALPHA):
  """Intersection-union test using exact exponential-null rate intervals."""
  tail = alpha / (2 * len(doses))
  quantiles = chi2.ppf([tail, 1 - tail], 2 * count) / 2
  feasible = []
  for sums in [on_sums, off_sums]:
    feasible.append(affine_feasible(quantiles[0] / sums, quantiles[1] / sums, doses))
  return ~feasible[0] & ~feasible[1]


def dwell_mixture(dose, orientation, binding=BINDING_TO_GATE_RATIO):
  """Exact two-exponential episode law for the four-state witness, gate k=1."""
  a = binding * (1 + dose)
  mean_rate = (1 if orientation == "ON" else dose) / (1 + dose)
  rate_sum = a + 1
  discriminant = math.sqrt(rate_sum**2 - 4 * a * mean_rate)
  fast_rate = (rate_sum + discriminant) / 2
  slow_rate = a * mean_rate / fast_rate
  fast_weight = (1 - slow_rate) / discriminant
  return slow_rate, fast_rate, fast_weight


def phase_sums(rng, dose, orientation, count, size):
  """Sum iid hyperexponential durations using binomial counts and gamma sums."""
  slow, fast, weight = dwell_mixture(dose, orientation)
  fast_count = rng.binomial(count, weight, size=size)
  return rng.gamma(count - fast_count, 1 / slow) + rng.gamma(fast_count, 1 / fast)


def probability_summary(events):
  successes = int(np.count_nonzero(events))
  trials = len(events)
  lower = 0.0 if successes == 0 else float(beta.ppf(0.025, successes, trials - successes + 1))
  upper = 1.0 if successes == trials else float(beta.ppf(0.975, successes + 1, trials - successes))
  return {"rejections": successes, "replicates": trials, "fraction": successes / trials,
          "monte_carlo_95_percent_interval": [lower, upper]}


def verify_sampler(rng):
  """Check phase law against fresh two-state subgenerator resolvents."""
  checks = []
  binding = BINDING_TO_GATE_RATIO
  for dose in [0.1, 0.25, 1, 2, 4, 10]:
    for orientation in ["ON", "OFF"]:
      if orientation == "ON":
        sub = np.array([[-1 - binding * dose, binding * dose], [binding, -binding]])
        entry = np.array([1.0, 0.0])
      else:
        sub = np.array([[-binding * dose, binding * dose], [binding, -binding - 1]])
        entry = np.array([0.0, 1.0])
      exit_rates = -sub @ np.ones(2)
      slow, fast, weight = dwell_mixture(dose, orientation)
      for s in [0.0, 0.01, 0.1, 1.0, 10.0]:
        direct = entry @ np.linalg.solve(s * np.eye(2) - sub, exit_rates)
        mixture = (1 - weight) * slow / (s + slow) + weight * fast / (s + fast)
        assert np.isclose(direct, mixture, rtol=1e-10, atol=1e-12)
      mean = -entry @ np.linalg.solve(sub, np.ones(2))
      second = 2 * entry @ np.linalg.solve(sub, np.linalg.solve(sub, np.ones(2)))
      expected = (1 + dose) / (1 if orientation == "ON" else dose)
      assert np.isclose(mean, expected, rtol=1e-10)
      samples = phase_sums(rng, dose, orientation, 1, 100000)
      mean_se = math.sqrt((second - mean**2) / len(samples))
      assert abs(samples.mean() - mean) < 6 * mean_se
      checks.append({"dose": dose, "orientation": orientation,
                     "sample_mean_z_score": float((samples.mean() - mean) / mean_se)})
  # Feasibility has known answers and invariance to a common time scale.
  doses = [0.25, 1, 4]
  rates = np.array([[0.2, 0.5, 0.8]])
  assert not affine_feasible(rates, rates, doses)[0]
  affine = np.array([[1.25, 2, 5]])
  assert affine_feasible(affine, affine, doses)[0]
  print("PASS: phase laws agree with 60 direct resolvents and 12 simulated means", flush=True)
  return checks


def main():
  rng = np.random.default_rng(SEED)
  sampler_checks = verify_sampler(rng)
  designs = {"original_1_2_4": [1, 2, 4], "balanced_16_fold": [0.25, 1, 4],
             "balanced_100_fold": [0.1, 1, 10]}
  powers = []
  for name, doses in designs.items():
    for count in [25, 50, 100, 200, 500, 1000, 3000]:
      on_sums = np.column_stack([phase_sums(rng, c, "ON", count, REPLICATES) for c in doses])
      off_sums = np.column_stack([phase_sums(rng, c, "OFF", count, REPLICATES) for c in doses])
      events = reject_from_sums(on_sums, off_sums, doses, count)
      assert np.array_equal(events, reject_from_sums(60 * on_sums, 60 * off_sums, doses, count))
      row = {"design": name, "doses": doses, "episodes_per_orientation_per_dose": count,
             "probability": probability_summary(events),
             "expected_total_observation_hours_at_gate_2_over_3_per_minute":
               count * sum((1 + c) + (1 + c) / c for c in doses) * 1.5 / 60}
      powers.append(row)
      print(f"POWER {name}, n={count}: {row['probability']['fraction']:.4f}; "
            f"expected summed record-hours={row['expected_total_observation_hours_at_gate_2_over_3_per_minute']:.2f}", flush=True)

  nulls = []
  doses = designs["balanced_16_fold"]
  for intercept, slope in [(1, 0), (0.2, 0.7), (0, 1)]:
    for count in [25, 100, 500]:
      # Reversible 3-state path: OFF singleton at affine exit rate; ON is a
      # two-state phase-type episode with the same ON law as the witness.
      off_sums = np.column_stack([rng.gamma(count, 1 / (intercept + slope * c), REPLICATES) for c in doses])
      on_sums = np.column_stack([phase_sums(rng, c, "ON", count, REPLICATES) for c in doses])
      events = reject_from_sums(on_sums, off_sums, doses, count)
      assert np.array_equal(events, reject_from_sums(off_sums, on_sums, doses, count))
      row = {"affine_intercept": intercept, "affine_slope": slope, "count": count,
             "probability": probability_summary(events)}
      nulls.append(row)
      print(f"NULL A={intercept}, B={slope}, n={count}: {row['probability']['fraction']:.4f}", flush=True)
  result = {"seed": SEED, "numpy_version": np.__version__, "scipy_version": scipy.__version__,
            "alpha": ALPHA, "binding_to_gate_ratio": BINDING_TO_GATE_RATIO,
            "scope": "Synthetic exact-law experiments, prespecified complete episode counts; no biological data, instrument model, heterogeneity, or dose error.",
            "sampler_checks": sampler_checks, "power": powers, "null_checks": nulls}
  Path(__file__).with_name("design-power.json").write_text(json.dumps(result, indent=2) + "\n")
  print("Saved design-power.json", flush=True)


if __name__ == "__main__":
  main()
