"""Plot the retained synthetic example without hiding unsuccessful starts."""

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parent
data = json.loads((ROOT / "reconstruction_results.json").read_text())
records = data["experiments"]
noise_levels = sorted({r["relative_phase_speed_noise_std"] for r in records if r["relative_phase_speed_noise_std"]})
compressed, refined = [], []
for noise in noise_levels:
  matches = [r for r in records if r["relative_phase_speed_noise_std"] == noise]
  selected = min(
    (r for r in matches if r["data_mode"] == "compressed-22"),
    key=lambda r: r["scaled_residual_norm"],
  )
  refinement = next(r for r in matches if r["initialization"] == "best-compressed-fit")
  compressed.append(100 * selected["relative_frobenius_error"])
  refined.append(100 * refinement["relative_frobenius_error"])

plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10, "axes.spines.top": False, "axes.spines.right": False})
fig, ax = plt.subplots(figsize=(7.2, 4.8))
xs = [100 * n for n in noise_levels]
ax.loglog(xs, compressed, "o-", color="#343331", lw=1.6, label="22-observable fit, selected by residual")
ax.loglog(xs, refined, "o-", color="#7B3F59", lw=1.8, label="Then refine against all 45 phase speeds")
ax.set_xlabel("Relative phase-speed noise standard deviation (%)")
ax.set_ylabel("Relative Voigt-matrix Frobenius error (%)")
ax.set_xticks(xs, ["0.001", "0.01", "0.1"])
ax.set_yticks([0.01, 0.1, 1, 10, 100], ["0.01", "0.1", "1", "10", "100"])
ax.grid(which="major", color="#E5E3DF", linewidth=0.6)
ax.set_axisbelow(True)
ax.legend(frameon=False, fontsize=9, loc="upper left")
fig.suptitle("Uniqueness and numerical recovery are different questions", x=0.1, ha="left", fontsize=12, fontweight="medium")
fig.text(0.1, 0.02, "One synthetic material; one noise draw per level. All 36 solver attempts are retained.\nThe figure is an illustration, not a general stability or performance guarantee.", fontsize=8, color="#55514D")
fig.subplots_adjust(left=0.13, right=0.97, top=0.86, bottom=0.2)
for extension in ["png", "pdf", "svg"]:
  fig.savefig(ROOT / f"reconstruction_example.{extension}", dpi=180)
svg = ROOT / "reconstruction_example.svg"
svg.write_text("\n".join(line.rstrip() for line in svg.read_text().splitlines()) + "\n")
print("Saved PNG, PDF and SVG figures", flush=True)
