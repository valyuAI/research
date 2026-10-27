"""Audit the neighboring experiment implementation with independent methods.

Checks linear-program feasibility against HiGHS and phase-duration sums against
direct CTMC jump simulation. These numerical checks supplement the proof.
"""

import importlib.util
import json
from pathlib import Path

import numpy as np
from scipy.optimize import linprog
from scipy.stats import ks_2samp


def direct_sums(rng, dose, orientation, count, repetitions, binding):
  """Simulate each actual jump of the killed two-state microstate process."""
  size = count*repetitions
  times = np.zeros(size)
  atGate = np.ones(size, dtype=bool)
  live = np.ones(size, dtype=bool)
  gateAwayRate = binding*dose if orientation == "ON" else binding
  returnRate = binding if orientation == "ON" else binding*dose
  iterations = 0
  while np.any(live):
    active = np.flatnonzero(live)
    gate = atGate[active]
    rates = np.where(gate, gateAwayRate+1, returnRate)
    times[active] += rng.exponential(1/rates)
    exits = gate & (rng.random(len(active)) < 1/(gateAwayRate+1))
    live[active[exits]] = False
    atGate[active] = ~gate
    iterations += 1
  return times.reshape(repetitions, count).sum(axis=1), iterations


def main():
  source = Path(__file__).parent.parent / "switching-experiment-20261018/check_design_power.py"
  spec = importlib.util.spec_from_file_location("experiment", source)
  experiment = importlib.util.module_from_spec(spec)
  spec.loader.exec_module(experiment)
  rng = np.random.default_rng(180104)
  feasibleCount = 0
  cases = 500
  for case in range(cases):
    doses = np.sort(np.exp(rng.uniform(-3, 3, 3)))
    centers = np.exp(rng.uniform(-2, 2, 3))
    width = rng.uniform(0.01, 0.95)
    lower, upper = centers*(1-width), centers*(1+width)
    actual = bool(experiment.affine_feasible(lower[None, :], upper[None, :], doses)[0])
    design = np.column_stack([np.ones(3), doses])
    independent = linprog([0, 0], A_ub=np.vstack([design, -design]),
                          b_ub=np.concatenate([upper, -lower]), bounds=[(0, None), (0, None)],
                          method="highs")
    assert independent.status in (0, 2)
    assert actual == independent.success, (case, doses, lower, upper)
    feasibleCount += actual
  print(f"PASS: {cases} independent linear programs; {feasibleCount} feasible", flush=True)

  simulationChecks = []
  repetitions = 5000
  count = 3
  for dose, orientation in [(0.25, "ON"), (4, "OFF"), (1, "ON")]:
    direct, iterations = direct_sums(rng, dose, orientation, count, repetitions,
                                     experiment.BINDING_TO_GATE_RATIO)
    mixture = experiment.phase_sums(rng, dose, orientation, count, repetitions)
    result = ks_2samp(direct, mixture)
    # Fixed, conservative comparison threshold; never retry failed seeds.
    assert result.statistic < 0.05
    mean = count*(1+dose)/(1 if orientation == "ON" else dose)
    row = {"dose": dose, "orientation": orientation, "episodes_per_sum": count,
           "replicates": repetitions, "direct_mean": float(direct.mean()),
           "mixture_mean": float(mixture.mean()), "exact_mean": float(mean),
           "two_sample_ks_distance": float(result.statistic),
           "jump_simulation_iterations": iterations}
    simulationChecks.append(row)
    print(f"PASS: direct CTMC {dose}/{orientation}, KS={result.statistic:.4f}, "
          f"direct mean={direct.mean():.5f}, exact={mean:.5f}", flush=True)

  output = {"seed": 180104, "linear_program_cases": cases,
            "linear_program_feasible": feasibleCount, "direct_ctmc_checks": simulationChecks,
            "scope": "Independent numerical cross-checks. They are not the proof of type-I error control."}
  Path(__file__).with_name("experiment-audit.json").write_text(json.dumps(output, indent=2)+"\n")


if __name__ == "__main__":
  main()
