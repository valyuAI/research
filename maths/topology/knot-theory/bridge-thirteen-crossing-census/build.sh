#!/bin/sh
set -eu
cd "$(dirname "$0")"

printf 'Checking permutation and coloring certificates\n'
python3 verification/check.py
printf 'Checking binary matrix ranks and relations\n'
python3 verification/check_matrices.py
python3 verification/negative_checks.py
if [ -n "${KNOTINFO_CSV:-}" ]; then
  printf 'Comparing against KnotInfo CSV\n'
  python3 verification/check_source.py "$KNOTINFO_CSV"
fi

printf 'Building paper, pass 1 of 3\n'
pdflatex -interaction=nonstopmode -halt-on-error paper.tex > paper.build.log
bibtex paper >> paper.build.log
printf 'Building paper, pass 2 of 3\n'
pdflatex -interaction=nonstopmode -halt-on-error paper.tex >> paper.build.log
printf 'Building paper, pass 3 of 3\n'
pdflatex -interaction=nonstopmode -halt-on-error paper.tex >> paper.build.log
printf 'Built paper.pdf\n'
