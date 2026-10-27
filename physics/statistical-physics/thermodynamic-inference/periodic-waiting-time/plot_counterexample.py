"""Small illustrative quadrature; the short-lag proof is exact and separate."""

from math import cos, exp, pi, sin
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def difference(lag, nodes, epsilon=0.5):
  total = 0.0
  for index in range(nodes):
    phase = 2 * pi * index / nodes
    a = 1 + epsilon * cos(phase)
    b = 1 + epsilon * sin(phase)
    next_a = 1 + epsilon * cos(phase + lag)
    next_b = 1 + epsilon * sin(phase + lag)
    hazard = 2 * lag + epsilon * (
      sin(phase + lag) - sin(phase) + cos(phase) - cos(phase + lag)
    )
    total += (a * next_b - b * next_a) * exp(-hazard)
  return total / nodes


def main():
  delays = [0.3 * index / 120 for index in range(121)]
  values = [difference(delay, 128) for delay in delays]
  refinement_error = max(
    abs(value - difference(delay, 256)) for value, delay in zip(values, delays)
  )
  if refinement_error > 1e-12 or min(values[1:]) <= 0:
    raise ValueError("Illustrative quadrature check failed")
  plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9})
  fig, (network, curve) = plt.subplots(1, 2, figsize=(6.2, 2.05))
  points = {1: (0.05, 0.0), 2: (0.5, 0.9), 3: (0.95, 0.0)}
  blue = "#185c83"
  for start, end, color, style in [(1, 2, blue, "-"), (2, 3, blue, "-"), (1, 3, "0.5", "--")]:
    x1, y1 = points[start]
    x2, y2 = points[end]
    network.plot([x1, x2], [y1, y2], color=color, linestyle=style, linewidth=1.6)
  for label, (x, y) in points.items():
    network.scatter([x], [y], s=420, facecolor="white", edgecolor="0.15", zorder=3)
    network.text(x, y, str(label), ha="center", va="center", zorder=4)
  network.text(0.09, 0.57, "$a(t)$", ha="center", color=blue)
  network.text(0.92, 0.57, "$b(t)$", ha="center", color=blue)
  network.text(0.5, -0.13, "1 (hidden)", ha="center", color="0.4")
  network.set(xlim=(-0.12, 1.12), ylim=(-0.23, 1.08), aspect="equal")
  network.axis("off")
  curve.plot(delays, values, color=blue, linewidth=1.8, label="$f(s)-g(s)$")
  curve.plot(delays, [0.25 * delay for delay in delays], color="0.5", linestyle="--", linewidth=1.2, label="$\\varepsilon^2s$")
  curve.set(xlabel="Delay $s$", ylabel="Density difference", xlim=(0, 0.3), ylim=(0, 0.08))
  curve.spines[["top", "right"]].set_visible(False)
  curve.legend(frameon=False, loc="upper left", fontsize=8)
  fig.tight_layout(w_pad=1.4, pad=0.4)
  output = Path(__file__).with_name("counterexample.pdf")
  fig.savefig(output)
  plt.close(fig)
  print(f"Figure saved; 128/256-node refinement difference {refinement_error:.2g}", flush=True)


if __name__ == "__main__":
  main()
