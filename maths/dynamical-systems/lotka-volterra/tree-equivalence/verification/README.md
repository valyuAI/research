# Lotka-Volterra: exact finite checks

```bash
python3 verify_lv_tree.py
```

Tested with Python 3.13.7 and NetworkX 3.6. NetworkX supplies enumeration and graph isomorphism. All coefficient calculations use integers and `fractions.Fraction`; no floating-point rank threshold is used.

The script writes `lv_tree_exact_checks.json` beside itself and emits progress by tree order. It checks dependent triples and reconstruction on all 986 unlabelled trees of orders 2 through 12. It also exhausts linear-form supports at explicit generic parameters on all 200 unlabelled trees of orders 2 through 10.

These finite examples are consistency checks for the all-order written proof. They do not establish publication priority or formalize the entire theorem. The associated Lean module checks only the three-vertex path obstruction.
