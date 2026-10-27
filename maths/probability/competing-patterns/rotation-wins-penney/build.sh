#!/bin/sh
set -eu
baseDir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
buildDir=$(mktemp -d "${TMPDIR:-/tmp}/penney-rotation.XXXXXX")
compiler=${CXX:-c++}
printf 'Verification work directory: %s\n' "$buildDir"
nice -n 10 "$compiler" -std=c++17 -O2 "$baseDir/verification/enumerate_independent.cpp" -o "$buildDir/enumerate"
for spec in '4 15' '5 12' '6 5' '7 6'; do
  set -- $spec
  nice -n 10 "$buildDir/enumerate" "$1" "$2" "$buildDir/k$1.jsonl"
done
nice -n 10 python3 -B "$baseDir/verification/verify.py" --generated "$buildDir"
nice -n 10 python3 -B "$baseDir/verification/controls.py"
nice -n 10 python3 -B "$baseDir/verification/check_length_three.py"
nice -n 10 "$compiler" -std=c++17 -O2 "$baseDir/verification/length_three_oracle.cpp" -o "$buildDir/length-three-oracle"
nice -n 10 "$buildDir/length-three-oracle" "$buildDir/length-three-oracle.jsonl"
nice -n 10 python3 -B "$baseDir/verification/compare_length_three_oracle.py" "$buildDir/length-three-oracle.jsonl"
cp "$baseDir/paper.tex" "$baseDir/references.bib" "$buildDir/"
cd "$buildDir"
nice -n 10 pdflatex -interaction=nonstopmode -halt-on-error paper.tex
nice -n 10 bibtex paper
nice -n 10 pdflatex -interaction=nonstopmode -halt-on-error paper.tex
nice -n 10 pdflatex -interaction=nonstopmode -halt-on-error paper.tex
cp "$buildDir/paper.pdf" "$baseDir/paper.pdf"
printf 'Verified coefficients and built %s/paper.pdf\n' "$baseDir"
