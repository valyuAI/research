#!/usr/bin/env bash
# Replays the standard-library checks and builds the PDF.
#   bash build.sh          quick: saved-evidence audit, extremal-graph check (stdlib only) + PDF
#   bash build.sh --full   also replays the complete enumeration and every cross-check
#                        (needs python3 with numpy, networkx, python-flint 0.9.0, pynauty 2.8.8.1,
#                         and nauty's geng on PATH; about 1-3 hours on a laptop)
set -euo pipefail
export PYTHONOPTIMIZE=0
cd "$(dirname "$0")"
PY="${PYTHON:-python3}"
case "${1:-}" in ""|--full) ;; *) printf 'Usage: bash build.sh [--full]\n' >&2; exit 2 ;; esac
python3 -B verification/audit_recorded.py
python3 -B verification/verify_extremal.py > verification/extremal_result.json
printf 'Extremal graphs W5 and X: inertia (11,0,4) verified (verification/extremal_result.json)\n'
if [ "${1:-}" = "--full" ]; then
  cd verification
  "$PY" -B enumerate_nonsingular.py 4 | tee enumerate_nonsingular.log
  "$PY" -B enumerate_check.py 4 | tee enumerate_check.log
  "$PY" -B check_census.py > check_census_result.json
  "$PY" -B max_reduced_order.py 4 | tee max_reduced_order.log
  "$PY" -B max_reduced_order_check.py 4 | tee max_reduced_order_check.log
  "$PY" -B ack_check.py | tee ack_check.log
  "$PY" -B classify_max_order.py 4 8 30 | tee classify_max_order.log
  "$PY" -B order30_check.py > order30_check.json
  "$PY" -B extremal_doubling_check.py | tee extremal_doubling_check.log
  "$PY" -B k5_extension_check.py | tee k5_extension_check.log
  "$PY" -B brute_census.py 10 | tee brute_census.log
  for k in 1 2 3; do "$PY" -B enumerate_nonsingular.py "$k" | tail -1; "$PY" -B max_reduced_order.py "$k" | tail -1; done
  "$PY" -B point_determining_bfs.py 3 2 | tail -1
  "$PY" -B torgasev_maximal_k3.py
  "$PY" -B audit_recorded.py --require-generated
  cd ..
fi
pdflatex -interaction=nonstopmode -halt-on-error paper.tex > paper.build.log
bibtex paper >> paper.build.log
pdflatex -interaction=nonstopmode -halt-on-error paper.tex >> paper.build.log
pdflatex -interaction=nonstopmode -halt-on-error paper.tex >> paper.build.log
printf 'Built paper.pdf\n'
