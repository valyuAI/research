"""Synthetic finite-direction reconstruction; numerical evidence, not a proof."""

import json
from pathlib import Path
import time

import numpy as np
import scipy
from scipy.optimize import least_squares


ROOT = Path(__file__).resolve().parent
PAIR_ORDER = [(0, 0), (1, 1), (2, 2), (1, 2), (0, 2), (0, 1)]
PAIR_INDEX = {pair: k for k, pair in enumerate(PAIR_ORDER)}
PAIR_INDEX.update({(b, a): k for (a, b), k in list(PAIR_INDEX.items())})
UPPER = np.triu_indices(6)
LOWER = np.tril_indices(6)
DIAGONAL = np.flatnonzero(LOWER[0] == LOWER[1])
NODES = [(a, b, 1) for a in range(5) for b in range(5 - a)]
DIRECTIONS = np.array(NODES, dtype=float)
DIRECTIONS /= np.linalg.norm(DIRECTIONS, axis=1)[:, None]
TRACE_NODES = [k for k, (a, b, _) in enumerate(NODES) if a + b <= 2]


def christoffel(stiffness):
  tensor = np.array([
    stiffness[PAIR_INDEX[i, j], PAIR_INDEX[k, l]]
    for i in range(3) for j in range(3)
    for k in range(3) for l in range(3)
  ]).reshape(3, 3, 3, 3)
  return np.einsum("ijkl,nj,nk->nil", tensor, DIRECTIONS, DIRECTIONS)


def observables_from_eigenvalues(eigenvalues):
  traces = eigenvalues.sum(axis=1)
  second = (traces**2 - (eigenvalues**2).sum(axis=1)) / 2
  return np.concatenate([traces[TRACE_NODES], second, [np.prod(eigenvalues[0])]])


def decode(parameters):
  lower = np.zeros((6, 6))
  values = parameters.copy()
  values[DIAGONAL] = np.exp(values[DIAGONAL])
  lower[LOWER] = values
  return lower @ lower.T


def encode(stiffness):
  values = np.linalg.cholesky(stiffness)[LOWER]
  values[DIAGONAL] = np.log(values[DIAGONAL])
  return values


def main():
  started = time.monotonic()
  rng = np.random.default_rng(20261017)
  integer_matrix = rng.integers(-3, 4, size=(6, 6))
  true_stiffness = (integer_matrix @ integer_matrix.T + 20 * np.eye(6)) / 20
  eigenvalues = np.linalg.eigvalsh(christoffel(true_stiffness))
  phase_speeds = np.sqrt(eigenvalues)
  exact_observables = observables_from_eigenvalues(eigenvalues)
  diagonal_start = np.eye(6) * np.trace(true_stiffness) / 6
  starts = [encode(diagonal_start)]
  for _ in range(3):
    seed = rng.normal(size=(6, 6))
    starts.append(encode(seed @ seed.T / 6 + np.eye(6)))

  experiments = []
  conditioning = {}
  noise_levels = [0, 1e-5, 1e-4, 1e-3]
  for noise in noise_levels:
    observed_speeds = phase_speeds * (1 + noise * rng.normal(size=phase_speeds.shape))
    compressed_candidates = []
    for mode in ["compressed-22", "all-45-speeds"]:
      observed = (
        observables_from_eigenvalues(observed_speeds**2)
        if mode == "compressed-22" else observed_speeds.ravel()
      )

      def matrix_residual(stiffness):
        predicted_eigenvalues = np.linalg.eigvalsh(christoffel(stiffness))
        predicted = (
          observables_from_eigenvalues(predicted_eigenvalues)
          if mode == "compressed-22" else np.sqrt(predicted_eigenvalues).ravel()
        )
        return (predicted - observed) / observed

      def residual(parameters):
        return matrix_residual(decode(parameters))

      if noise == 0:
        derivatives = []
        for i, j in zip(*UPPER):
          perturbation = np.zeros((6, 6))
          step = 1e-5 * max(1, abs(true_stiffness[i, j]))
          perturbation[i, j] = perturbation[j, i] = step
          derivatives.append((
            matrix_residual(true_stiffness + perturbation) -
            matrix_residual(true_stiffness - perturbation)
          ) / (2 * step))
        singular_values = np.linalg.svd(np.column_stack(derivatives), compute_uv=False)
        conditioning[mode] = {
          "coordinate_convention": "Upper-triangular Voigt entries; relative observable residuals",
          "singular_values": singular_values.tolist(),
          "condition_number": float(singular_values[0] / singular_values[-1]),
          "finite_difference_relative_step": 1e-5,
        }

      mode_starts = [(f"independent-{j}", start) for j, start in enumerate(starts)]
      if mode == "all-45-speeds":
        best_compressed = min(compressed_candidates, key=lambda item: item[0])
        mode_starts.append(("best-compressed-fit", best_compressed[1]))
      for start_index, (initialization, start) in enumerate(mode_starts):
        fit = least_squares(
          residual, start, method="trf", jac="3-point",
          xtol=1e-12, ftol=1e-12, gtol=1e-12, max_nfev=1500,
        )
        recovered = decode(fit.x)
        if mode == "compressed-22":
          compressed_candidates.append((float(np.linalg.norm(fit.fun)), fit.x.copy()))
        error = np.linalg.norm(recovered - true_stiffness) / np.linalg.norm(true_stiffness)
        record = {
          "data_mode": mode,
          "relative_phase_speed_noise_std": noise,
          "start_index": start_index,
          "initialization": initialization,
          "success": bool(fit.success),
          "status": int(fit.status),
          "function_evaluations": int(fit.nfev),
          "relative_frobenius_error": float(error),
          "scaled_residual_norm": float(np.linalg.norm(fit.fun)),
          "smallest_stiffness_eigenvalue": float(np.linalg.eigvalsh(recovered)[0]),
          "recovered_stiffness": recovered.tolist(),
        }
        experiments.append(record)
        print(
          f"{len(experiments)}/36 {mode} noise={noise:g} start={initialization} "
          f"matrix_error={error:.3g} residual={np.linalg.norm(fit.fun):.3g} "
          f"nfev={fit.nfev} elapsed={time.monotonic()-started:.1f}s",
          flush=True,
        )

  result = {
    "purpose": "Synthetic illustration of 22-observable reconstruction from 15 directions",
    "limitations": [
      "Not a proof of global uniqueness at this particular tensor",
      "Not experimental data or a general conditioning guarantee",
      "One deterministic tensor and one noise realization per level",
      "All attempted starts are retained, including failed or inaccurate fits",
    ],
    "seed": 20261017,
    "dependencies": {"numpy": np.__version__, "scipy": scipy.__version__},
    "integer_matrix": integer_matrix.tolist(),
    "true_stiffness": true_stiffness.tolist(),
    "units": "dimensionless density-normalized stiffness and phase speeds",
    "unscaled_directions": NODES,
    "unit_directions": DIRECTIONS.tolist(),
    "phase_speeds": phase_speeds.tolist(),
    "exact_22_observables": exact_observables.tolist(),
    "local_jacobian_conditioning": conditioning,
    "experiments": experiments,
    "elapsed_seconds": time.monotonic() - started,
  }
  (ROOT / "reconstruction_results.json").write_text(json.dumps(result, indent=2) + "\n")
  print("Saved every reconstruction attempt", flush=True)


if __name__ == "__main__":
  main()
