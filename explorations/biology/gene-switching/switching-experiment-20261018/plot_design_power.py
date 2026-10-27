"""Plot the retained ideal-observation simulations without smoothing fits."""

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter, ScalarFormatter


HERE = Path(__file__).resolve().parent
data = json.loads((HERE / "design-power.json").read_text())
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10,
                     "axes.spines.top": False, "axes.spines.right": False})
fig, axes = plt.subplots(1, 2, figsize=(11, 4.6), constrained_layout=True)
designs = [
  ("original_1_2_4", "1, 2, 4", "#939aa2", "o"),
  ("balanced_16_fold", "0.25, 1, 4", "#5c8fba", "s"),
  ("balanced_100_fold", "0.1, 1, 10", "#165f93", "D"),
]
for name, label, color, marker in designs:
  rows = [row for row in data["power"] if row["design"] == name]
  probabilities = [row["probability"]["fraction"] for row in rows]
  errors = [[row["probability"]["fraction"] - row["probability"]["monte_carlo_95_percent_interval"][0]
             for row in rows],
            [row["probability"]["monte_carlo_95_percent_interval"][1] - row["probability"]["fraction"]
             for row in rows]]
  for ax, field in zip(axes, ["episodes_per_orientation_per_dose",
                             "expected_total_observation_hours_at_gate_2_over_3_per_minute"]):
    ax.errorbar([row[field] for row in rows], probabilities, yerr=errors,
                color=color, marker=marker, markersize=4, linewidth=1.6, capsize=2,
                label=label)
for ax in axes:
  ax.set_xscale("log")
  ax.set_ylim(-0.025, 1.04)
  ax.yaxis.set_major_formatter(PercentFormatter(1))
  ax.xaxis.set_major_formatter(ScalarFormatter())
  ax.grid(axis="y", color="#e3e6e8", linewidth=0.6)
  ax.set_ylabel("Detection probability")
axes[0].set_xlabel("Complete ON and OFF episodes per dose")
axes[0].set_xticks([25, 100, 500, 3000])
axes[1].set_xlabel("Expected analyzed record-hours, summed across doses")
axes[1].set_xticks([10, 35, 100, 500, 2000])
axes[0].set_title("Dose placement changes the required episode count", loc="left", fontsize=11)
axes[1].set_title("Wider dose spans also lengthen rare-state waits", loc="left", fontsize=11)
axes[1].legend(title="Three doses / binding midpoint", loc="lower right", frameon=False, fontsize=9)
fig.suptitle("Detecting hidden switching states: ideal-observation planning", fontsize=14, x=0.01, ha="left")
fig.savefig(HERE / "design-power.png", dpi=180, facecolor="white")
fig.savefig(HERE / "design-power.svg", facecolor="white")
print("Saved design-power.png and design-power.svg", flush=True)
