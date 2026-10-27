#!/bin/sh
set -eu
cd "$(dirname "$0")"
for document in paper journal; do
  printf 'Building %s\n' "$document"
  pdflatex -interaction=nonstopmode -halt-on-error "$document.tex" > "$document.build.log"
  bibtex "$document" >> "$document.build.log"
  pdflatex -interaction=nonstopmode -halt-on-error "$document.tex" >> "$document.build.log"
  pdflatex -interaction=nonstopmode -halt-on-error "$document.tex" >> "$document.build.log"
  printf 'Built %s.pdf\n' "$document"
done
