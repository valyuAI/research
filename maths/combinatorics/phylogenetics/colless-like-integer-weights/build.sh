#!/bin/sh
# Replays the standard-library checks and builds the PDF.
set -eu
cd "$(dirname "$0")"
python3 -B verification/check_colless.py
printf 'Building paper\n'
pdflatex -interaction=nonstopmode -halt-on-error paper.tex > paper.build.log
bibtex paper >> paper.build.log
pdflatex -interaction=nonstopmode -halt-on-error paper.tex >> paper.build.log
pdflatex -interaction=nonstopmode -halt-on-error paper.tex >> paper.build.log
printf 'Built paper.pdf\n'
