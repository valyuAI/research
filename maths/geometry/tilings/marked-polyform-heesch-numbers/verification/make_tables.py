#!/usr/bin/env python3
"""Write tables.tex and drat-table.tex for the paper from results.json.  Standard library only."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.dirname(HERE)
T = json.load(open(os.path.join(HERE, 'results.json')))


def cells(t):
  return '$' + ',\\,'.join(f'({a},{b})' for a, b in t['cells']) + '$'


def copies(t):
  return len(json.load(open(os.path.join(HERE, t['witness'])))['placements'])


def fmt_int(n):
  return f'{n:,}'.replace(',', '\\,')


def row(t):
  u = t['upper_bound']
  if not u or 'nvars' not in u:
    return f"{cells(t)} & {t['h']} & {copies(t)} & -- & -- & -- \\\\"
  return f"{cells(t)} & {t['h']} & {copies(t)} & {u['k']} & {fmt_int(u['nvars'])} & {fmt_int(u['nclauses'])} \\\\"


hexes = [t for t in T['tiles'] if t['grid'] == 'hex']
sqs = [t for t in T['tiles'] if t['grid'] == 'sq']
with open(os.path.join(PKG, 'tables.tex'), 'w') as f:
  f.write('\\begin{table}[ht]\n\\centering\\small\n')
  f.write('\\caption{Exact values $h(P)$ for polyhexes with at most four cells and the straight row of five, in axial coordinates (neighbours $(\\pm1,0)$, $(0,\\pm1)$, $\\pm(1,-1)$). ``Copies'' is the size of the witness patch; the last three columns describe the unsatisfiable base formula $F(P,h+1)$.}\\label{tab:hex}\n')
  f.write('\\begin{tabular}{lrrrrr}\\toprule\nbase cells & $h$ & copies & $k$ refuted & variables & clauses\\\\\\midrule\n')
  for t in hexes:
    f.write(row(t) + '\n')
  f.write('\\bottomrule\\end{tabular}\n\\end{table}\n\n')
  f.write('\\begin{table}[ht]\n\\centering\\small\n')
  f.write('\\caption{Exact values $h(P)$ for polyominoes with at most five cells. Columns as in Table~\\ref{tab:hex}.}\\label{tab:sq}\n')
  f.write('\\begin{tabular}{lrrrrr}\\toprule\nbase cells & $h$ & copies & $k$ refuted & variables & clauses\\\\\\midrule\n')
  for t in sqs:
    f.write(row(t) + '\n')
  f.write('\\bottomrule\\end{tabular}\n\\end{table}\n')
big = [t for t in T['tiles'] if (t['upper_bound'] or {}).get('nclauses', 0) > 3_000_000 and t['upper_bound'].get('drat_trim_seconds')]
with open(os.path.join(PKG, 'drat-table.tex'), 'w') as f:
  f.write('\\begin{table}[ht]\n\\centering\\small\n')
  f.write('\\caption{The largest refuted formulas. Times are wall-clock on a shared, heavily loaded laptop; all other formulas are smaller and are listed in \\texttt{results.json}.}\\label{tab:drat}\n')
  f.write('\\begin{tabular}{lrrrrr}\\toprule\nbase cells & $k$ & clauses & CaDiCaL (s) & proof (GB) & drat-trim (s)\\\\\\midrule\n')
  for t in big:
    u = t['upper_bound']
    f.write(f"{cells(t)} & {u['k']} & {fmt_int(u['nclauses'])} & {fmt_int(u['cadical_seconds'])} & {u['proof_bytes'] / 1e9:.1f} & {fmt_int(u['drat_trim_seconds'])} \\\\\n")
  f.write('\\bottomrule\\end{tabular}\n\\end{table}\n')
print('wrote tables.tex and drat-table.tex')
