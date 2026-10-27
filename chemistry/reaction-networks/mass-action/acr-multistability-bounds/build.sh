#!/bin/sh
set -eu
cd "$(dirname "$0")"
python3 -B verification/verify_examples.py > verification/verify_examples.log
python3 -B verification/four_reactant_exponents.py > verification/four_reactant_exponents.log
if python3 -c "import sympy" 2>/dev/null; then
  python3 -B verification/independent_check.py > verification/independent_check.log
else
  printf 'sympy not available: skipping verification/independent_check.py\n' >&2
fi
LEAN_FILE=../../../../formal/ValyuResearch/AcrMultistability.lean
if command -v lake >/dev/null 2>&1 && [ -f "$LEAN_FILE" ]; then
  (cd ../../../../formal && lake env lean ValyuResearch/AcrMultistability.lean) > verification/lean_check.log 2>&1
  printf 'Lean check passed\n'
else
  printf 'lake not found: skipping the Lean check\n' >&2
fi
pdflatex -interaction=nonstopmode -halt-on-error paper.tex > paper.build.log
bibtex paper >> paper.build.log
pdflatex -interaction=nonstopmode -halt-on-error paper.tex >> paper.build.log
pdflatex -interaction=nonstopmode -halt-on-error paper.tex >> paper.build.log
printf 'Built paper.pdf\n'
