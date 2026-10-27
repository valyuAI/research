"""Frozen four-pair calibration, transferring to an independent MPRA library.

Primary analysis uses paper CPM preprocessing, entirely new promoters/genes,
and a common evaluation enhancer set excluded from every compared panel.
The raw-count route is sensitivity only. This script never selects a panel.
"""

from pathlib import Path
import hashlib
import json

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent


def fit_line(x, y):
  if len(x) < 3 or np.ptp(x) < 1e-8:
    return np.nan, np.nan
  beta = np.cov(x, y, ddof=0)[0, 1] / np.var(x)
  return float(y.mean() - beta * x.mean()), float(beta)


def main():
  frozen_path = ROOT / "FROZEN_TRANSFER_DESIGN.json"
  frozen = json.loads(frozen_path.read_text())
  source = ROOT / "GSE334082_21Ex500P_upstream_integrated_BC_counts.txt.gz"
  print("Loading independent 21E x 500P barcode table", flush=True)
  counts = pd.read_csv(source, sep="\t")
  print(f"Read {len(counts):,} barcode records", flush=True)
  pa = pd.read_csv(ROOT / "78P_annotations.txt", sep="\t", comment="#").set_index("promoter")
  target = pd.read_csv(ROOT / "500P_annotations.txt", sep="\t", comment="#").set_index("promoter")
  tss = pd.read_csv(ROOT / "GSM9780095_21Ex500P_TSS_mapping_counts.txt.gz", sep="\t").set_index("promoter")
  cohort = target[["gene", "modification_of", "clean_TSS"]].copy()
  cohort["in_counts"] = cohort.index.isin(counts.promoter.unique())
  cohort["has_tss"] = cohort.index.isin(tss.index)
  cohort["strict_tss"] = ((tss.aligned_reads >= 1000) & (tss.fraction_of_reads_in_promoter >= 0.9)).reindex(cohort.index, fill_value=False)
  cohort["overlapping_promoter"] = cohort.index.isin(pa.index)
  cohort["overlapping_gene"] = cohort.gene.isin(pa.gene.dropna())
  cohort["edited_training_promoter"] = cohort.modification_of.isin(pa.index)
  cohort["same_training_sequence"] = target.seq.isin(pa.seq.dropna())
  cohort["eligible"] = (cohort.in_counts & cohort.strict_tss & ~cohort[["overlapping_promoter", "overlapping_gene", "edited_training_promoter", "same_training_sequence"]].any(axis=1))
  cohort.to_csv(ROOT / "transfer_cohort.tsv", sep="\t")
  promoters = cohort.index[cohort.eligible]
  report = {"frozen_design_sha256": hashlib.sha256(frozen_path.read_bytes()).hexdigest(),
    "target_data_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
    "barcode_records": len(counts), "target_counts_promoters": int(counts.promoter.nunique()),
    "target_counts_enhancers": int(counts.enhancer.nunique()),
    "target_dna_reads": int(counts.DNA.sum()), "target_rna_reads": int(counts.RNA.sum()),
    "cohort_counts": {col: int(cohort[col].fillna(False).sum()) for col in cohort.columns if col not in ["gene", "modification_of"]},
    "primary": "CPM >=1 DNA, RNA pseudocount 0.1 CPM; independent promoters with >=1000 TSS reads and >=90% promoter-local starts",
    "mode_details": {}}
  pair_rows, coverage_rows = [], []
  for mode in ["cpm", "raw"]:
    print(f"Aggregating {mode} target expression and evaluating frozen panels", flush=True)
    d = dict(frozen["designs"]["cpm"])
    # Sensitivity changes measurement preprocessing and training activity,
    # while retaining the exact primary frozen panel/evaluation design.
    if mode == "raw":
      d["activity"] = frozen["designs"]["raw"]["activity"]
    dna, rna = counts.DNA.to_numpy(float), counts.RNA.to_numpy(float)
    if mode == "cpm":
      dna = dna / (dna.sum() / 1e6)
      rna = rna / (rna.sum() / 1e6)
    keep = dna >= (1 if mode == "cpm" else 20)
    selected = counts.loc[keep, ["enhancer", "promoter"]].copy()
    selected["score"] = np.log2((rna[keep] + (0.1 if mode == "cpm" else 1)) / dna[keep])
    scores = selected.groupby(["enhancer", "promoter"]).score.agg(["median", "size"])
    scores.loc[scores["size"] < 5, "median"] = np.nan
    scores.to_csv(ROOT / f"target_pair_scores_{mode}.tsv", sep="\t")
    matrix = scores["median"].unstack().reindex(columns=promoters)
    activity = pd.Series({e: x for e, x in d["activity"].items() if x is not None and e not in d["excluded_for_promoter_activity"]})
    available = matrix.index.intersection(activity.index)
    matrix = matrix.reindex(available)
    activity = activity.reindex(available)
    # Exclude every candidate and the alternative fixed controls from the
    # primary evaluation set: all methods see exactly these same enhancer IDs.
    panel_union = set(d["candidates"] + d["strongest_plus_controls"])
    common_evaluation = [e for e in available if e not in panel_union]
    report["mode_details"][mode] = {"evaluation_enhancers": common_evaluation,
      "available_enhancers": list(available), "candidate_enhancers": d["candidates"],
      "calibration_pairs_required": 4, "minimum_common_evaluation_pairs": 3}
    if mode == "raw":
      common_evaluation = report["mode_details"]["cpm"]["evaluation_enhancers"]
      report["mode_details"][mode]["evaluation_enhancers"] = common_evaluation
      report["mode_details"][mode]["evaluation_note"] = "Same frozen CPM panels/evaluation IDs; raw measurements and training activity."
    methods = {"even_activity": [d["even_activity"]], "strongest_only": [d["strongest_only"]],
      "strongest_plus_controls": [d["strongest_plus_controls"]], "random": d["random"],
      "mean_only": [d["even_activity"]], "equal_compatibility": [d["even_activity"]]}
    for pi, promoter in enumerate(promoters):
      if pi % 50 == 0:
        print(f"{mode}: {pi}/{len(promoters)} promoters", flush=True)
      y = matrix[promoter].dropna()
      evaluation = [e for e in common_evaluation if e in y.index]
      # Leave-one-enhancer-out full-profile reference. Its prediction for an
      # evaluated pair cannot use that pair's own measured expression.
      full_predictions = {}
      for e in evaluation:
        fitting = [q for q in y.index if q != e]
        intercept, beta = fit_line(activity.loc[fitting].to_numpy(), y.loc[fitting].to_numpy())
        full_predictions[e] = intercept + beta * activity[e]
      for method, panels in methods.items():
        for trial, panel in enumerate(panels):
          no_overlap = not set(panel).intersection(common_evaluation)
          covered = no_overlap and all(e in y.index for e in panel) and len(evaluation) >= 3
          coverage_rows.append({"mode": mode, "method": method, "trial": trial, "promoter": promoter,
            "calibration_measured": sum(e in y.index for e in panel), "evaluation_measured": len(evaluation),
            "no_evaluation_overlap": no_overlap, "covered": covered})
          if not covered:
            continue
          xp, yp = activity.loc[panel].to_numpy(), y.loc[panel].to_numpy()
          intercept, beta = fit_line(xp, yp)
          if method == "mean_only":
            intercept, beta = float(yp.mean()), 0.0
          if method == "equal_compatibility":
            intercept, beta = float(np.mean(yp - xp)), 1.0
          for e in evaluation:
            pair_rows.append({"mode": mode, "method": method, "trial": trial, "promoter": promoter,
              "gene": target.loc[promoter, "gene"], "enhancer": e,
              "observed": float(y[e]), "predicted": float(intercept + beta * activity[e]),
              "full_reference": float(full_predictions[e]), "slope": float(beta),
              "panel": "|".join(panel)})
    print(f"{mode}: complete", flush=True)
  pairs = pd.DataFrame(pair_rows)
  pairs.to_csv(ROOT / "transfer_pair_predictions.tsv", sep="\t", index=False)
  coverage = pd.DataFrame(coverage_rows)
  coverage.to_csv(ROOT / "transfer_coverage.tsv", sep="\t", index=False)
  pairs["squared_error"] = (pairs.predicted - pairs.observed) ** 2
  pairs["full_squared_error"] = (pairs.full_reference - pairs.observed) ** 2
  pairs["absolute_error"] = abs(pairs.predicted - pairs.observed)
  per_trial = pairs.groupby(["mode", "method", "trial", "promoter"])[["squared_error", "full_squared_error", "absolute_error"]].mean()
  per_trial["rmse_log2"] = np.sqrt(per_trial.squared_error)
  per_trial["full_rmse_log2"] = np.sqrt(per_trial.full_squared_error)
  per_trial.to_csv(ROOT / "transfer_per_promoter_trial.tsv", sep="\t")
  per_promoter = per_trial.groupby(["mode", "method", "promoter"]).mean()
  per_promoter["rmse_ratio"] = per_promoter.rmse_log2 / per_promoter.full_rmse_log2
  per_promoter.to_csv(ROOT / "transfer_per_promoter.tsv", sep="\t")
  summary = per_promoter.groupby(["mode", "method"])[["rmse_log2", "full_rmse_log2", "rmse_ratio", "absolute_error"]].median()
  summary["promoters"] = per_promoter.groupby(["mode", "method"]).size()
  summary["coverage"] = coverage.groupby(["mode", "method"]).covered.mean()
  summary.to_csv(ROOT / "transfer_summary.tsv", sep="\t")
  report["summary"] = summary.reset_index().to_dict("records")
  (ROOT / "transfer_results.json").write_text(json.dumps(report, indent=2))
  print(summary.to_string(), flush=True)


if __name__ == "__main__":
  main()
