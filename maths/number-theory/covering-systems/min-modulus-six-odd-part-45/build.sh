#!/bin/sh
# Replays the C verification (exact-cover self-test, main search, negative control) and builds the paper.
# The independent Python checker is slower; run it separately (see verification/README.md).
set -eu
cd "$(dirname "$0")"
CC=${CC:-cc}
BUILD=$(mktemp -d)
trap 'rm -rf "$BUILD"' EXIT
$CC -O3 -o "$BUILD/test_phi" verification/c/test_phi.c
$CC -O3 -o "$BUILD/dfs2" verification/c/dfs2.c
$CC -O3 -o "$BUILD/gen" verification/c/gen.c
python3 -B verification/run_checks.py "$BUILD"
python3 -B verification/control_m4.py
pdflatex -interaction=nonstopmode -halt-on-error paper.tex > paper.build.log
bibtex paper >> paper.build.log
pdflatex -interaction=nonstopmode -halt-on-error paper.tex >> paper.build.log
pdflatex -interaction=nonstopmode -halt-on-error paper.tex >> paper.build.log
echo "Built paper.pdf"
