#!/bin/sh
# Replays the verification and builds the PDF. Requires python3, a C compiler (optional), pdflatex, bibtex.
set -eu
cd "$(dirname "$0")"
python3 -B -O verification/controls.py
python3 -B -O verification/check_ct.py A B
if command -v clang >/dev/null 2>&1; then CC=clang; elif command -v gcc >/dev/null 2>&1; then CC=gcc; else CC=""; fi
if [ -n "$CC" ]; then
  $CC -O2 -o verification/ctproof verification/ctproof.c
  verification/ctproof 2 4 5 00101 00111 01100
  verification/ctproof 3 3 6 000101 000221 022211
fi
pdflatex -interaction=nonstopmode -halt-on-error paper.tex > paper.build.log
bibtex paper >> paper.build.log
pdflatex -interaction=nonstopmode -halt-on-error paper.tex >> paper.build.log
pdflatex -interaction=nonstopmode -halt-on-error paper.tex >> paper.build.log
printf 'Built paper.pdf\n'
