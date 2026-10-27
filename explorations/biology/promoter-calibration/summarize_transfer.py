"""Matched-cohort uncertainty and compact artifacts for the frozen transfer."""

import json

import numpy as np
import pandas as pd

from benchmark_library_transfer import ROOT


def main():
  per = pd.read_csv(ROOT / "transfer_per_promoter.tsv", sep="\t")
  annotation = pd.read_csv(ROOT / "500P_annotations.txt", sep="\t", comment="#").set_index("promoter")
  rng = np.random.default_rng(20261018)
  comparisons = []
  for mode in ["cpm", "raw"]:
    selected = per[(per["mode"] == mode) & (per.method == "even_activity")].set_index("promoter")
    for comparator in ["random", "strongest_only", "strongest_plus_controls", "mean_only", "equal_compatibility", "full_reference"]:
      if comparator == "full_reference":
        pair = selected[["rmse_log2", "full_rmse_log2"]].rename(columns={"rmse_log2": "selected", "full_rmse_log2": "comparator"})
      else:
        other = per[(per["mode"] == mode) & (per.method == comparator)].set_index("promoter")
        pair = selected[["rmse_log2"]].rename(columns={"rmse_log2": "selected"}).join(other[["rmse_log2"]].rename(columns={"rmse_log2": "comparator"}), how="inner")
      parents = annotation.reindex(pair.index).modification_of
      pair["cluster"] = [parent if pd.notna(parent) else promoter for promoter, parent in parents.items()]
      clusters = pair.cluster.unique()
      grouped = [pair.loc[pair.cluster == cluster, ["selected", "comparator"]].to_numpy() for cluster in clusters]
      bootstrap_ratios, bootstrap_differences = [], []
      for _ in range(2000):
        sample = np.concatenate([grouped[i] for i in rng.integers(len(grouped), size=len(grouped))])
        bootstrap_ratios.append(np.median(sample[:, 0] / sample[:, 1]))
        bootstrap_differences.append(np.mean(sample[:, 0] - sample[:, 1]))
      ratios = pair.selected / pair.comparator
      comparisons.append({"mode": mode, "comparator": comparator, "n_promoters": len(pair), "n_origin_clusters": len(clusters),
        "selected_median_rmse": float(pair.selected.median()), "comparator_median_rmse": float(pair.comparator.median()),
        "median_paired_rmse_ratio": float(ratios.median()), "median_paired_ratio_95pct_cluster_bootstrap": np.quantile(bootstrap_ratios, [.025, .975]).tolist(),
        "mean_paired_rmse_difference": float((pair.selected - pair.comparator).mean()),
        "mean_difference_95pct_cluster_bootstrap": np.quantile(bootstrap_differences, [.025, .975]).tolist(),
        "selected_wins": int((ratios < 1).sum())})
  (ROOT / "transfer_matched_uncertainty.json").write_text(json.dumps({"seed": 20261018, "bootstrap_draws": 2000,
    "resampling_unit": "parent promoter from modification_of, else promoter ID", "comparisons": comparisons}, indent=2))
  pd.DataFrame(comparisons).drop(columns=["median_paired_ratio_95pct_cluster_bootstrap", "mean_difference_95pct_cluster_bootstrap"]).to_csv(ROOT / "transfer_matched_summary.tsv", sep="\t", index=False)
  # Small curator-friendly provenance manifest, without raw data or full texts.
  cohort = pd.read_csv(ROOT / "transfer_cohort.tsv", sep="\t").set_index("promoter")
  coverage = pd.read_csv(ROOT / "transfer_coverage.tsv", sep="\t")
  frozen = json.loads((ROOT / "FROZEN_TRANSFER_DESIGN.json").read_text())
  export = cohort[["gene", "modification_of", "in_counts", "strict_tss", "overlapping_promoter", "overlapping_gene", "edited_training_promoter", "same_training_sequence", "eligible"]].copy()
  for mode in ["cpm", "raw"]:
    c = coverage[(coverage["mode"] == mode) & (coverage.method == "even_activity")].set_index("promoter")
    for column in ["covered", "calibration_measured", "evaluation_measured"]:
      export[f"{mode}_{column}"] = c[column].reindex(export.index)
  export.to_csv(ROOT / "final_cohort_coverage.tsv", sep="\t")
  manifest_path = ROOT / "final_data_manifest.json"
  if not manifest_path.exists():
    manifest_path = ROOT / "data_manifest.json"
  manifest = json.loads(manifest_path.read_text())
  result = json.loads((ROOT / "transfer_results.json").read_text())
  manifest.append({"file": "GSE334082_21Ex500P_upstream_integrated_BC_counts.txt.gz", "url": "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE334nnn/GSE334082/suppl/GSE334082_21Ex500P_upstream_integrated_BC_counts.txt.gz",
    "sha256": result["target_data_sha256"], "bytes": (ROOT / "GSE334082_21Ex500P_upstream_integrated_BC_counts.txt.gz").stat().st_size,
    "retrieval": "binary scientific-data download; discovered through Valyu CLI"})
  manifest = list({entry["file"]: entry for entry in manifest}.values())
  (ROOT / "final_data_manifest.json").write_text(json.dumps(manifest, indent=2))
  primary = per[(per["mode"] == "cpm") & (per.method == "even_activity")].set_index("promoter")
  random = per[(per["mode"] == "cpm") & (per.method == "random")].set_index("promoter").reindex(primary.index)
  tails = {}
  for label, values in [("selected", primary.rmse_log2), ("full_reference", primary.full_rmse_log2), ("random", random.rmse_log2)]:
    tails[label] = {"mean_rmse_log2": float(values.mean()), "median_rmse_log2": float(values.median()),
      "p90_rmse_log2": float(values.quantile(.9)), "max_rmse_log2": float(values.max()), "worst_promoter": values.idxmax()}
  (ROOT / "primary_tail_statistics.json").write_text(json.dumps(tails, indent=2))
  print(pd.DataFrame(comparisons)[["mode", "comparator", "n_promoters", "median_paired_rmse_ratio", "median_paired_ratio_95pct_cluster_bootstrap", "mean_difference_95pct_cluster_bootstrap"]].to_string(index=False))


if __name__ == "__main__":
  main()
