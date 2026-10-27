#!/bin/sh
# Replays the exact verification and builds the PDF.
#   sh build.sh                  exact checks of all examples, scan of n <= 6, positive control, PDF
#   sh build.sh --full-scan      also rescans all digraphs on 7 vertices (882,033,440; hours; nauty + C compiler)
#   sh build.sh --redraw-figure  also redraws region.pdf (numpy + matplotlib; floating point, illustration only)
set -eu
export PYTHONOPTIMIZE=0
cd "$(dirname "$0")"
SCAN_N=6
PY=${PYTHON:-python3}
for arg in "$@"; do
  case "$arg" in
    --full-scan) SCAN_N=7 ;;
    --redraw-figure) python3 -B verification/region.py verification/examples/G11.json region 0.005 0.6 0.02 2.0 160 ;;
    *) printf 'Usage: sh build.sh [--full-scan] [--redraw-figure]\n' >&2; exit 2 ;;
  esac
done
cd verification
"$PY" -u -B check_ctln.py examples/G11.json examples/W4.json examples/G27.json examples/G100.json
"$PY" -u -B check_flint.py examples/G11.json examples/W4.json examples/G27.json examples/G100.json
"$PY" -u -B check_induced.py examples/G11.json
PYTHON="$PY" sh scan.sh "$SCAN_N"
"$PY" -u -B recheck.py 3 3 1 recovery/n7_std_0.txt recovery/n7_std_1.txt recovery/n7_std_2.txt \
  --expect-candidates 35842 --expect-stable 0 --output scan_results/n7_recovered.recheck.json
"$PY" -B check_scan_results.py
"$PY" -B check_prefilter_constants.py
cd ..
pdflatex -interaction=nonstopmode -halt-on-error paper.tex > paper.build.log
bibtex paper >> paper.build.log
pdflatex -interaction=nonstopmode -halt-on-error paper.tex >> paper.build.log
pdflatex -interaction=nonstopmode -halt-on-error paper.tex >> paper.build.log
printf 'Built paper.pdf\n'
