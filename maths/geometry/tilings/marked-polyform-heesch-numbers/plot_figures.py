#!/usr/bin/env python3
"""Draw the figures of the paper from the witness files (needs matplotlib).

  patch-bar4.pdf   five-corona patch of a marked straight row of four hexagons
  table-tiles.pdf  every polyhex with <= 4 cells and polyomino with <= 5 cells, with h(P)
"""
import json
import math
import os

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Wedge

HERE = os.path.dirname(os.path.abspath(__file__))
W = os.path.join(HERE, 'verification', 'witnesses')
NB = {'hex': [(1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1), (1, -1)], 'sq': [(1, 0), (0, 1), (-1, 0), (0, -1)]}
LEVEL_COLOURS = ['#c0392b', '#2f5f8f', '#a9c4de', '#4f7fae', '#cddcec', '#7a9cc0', '#e3ebf4']


def xy(grid, c):
  if grid == 'hex':
    return (c[0] + c[1] / 2, c[1] * math.sqrt(3) / 2)
  return (float(c[0]), float(c[1]))


def cell_poly(grid, c):
  x, y = xy(grid, c)
  if grid == 'hex':
    R = 1 / math.sqrt(3)
    return [(x + R * math.cos(math.radians(30 + 60 * i)), y + R * math.sin(math.radians(30 + 60 * i))) for i in range(6)]
  return [(x - .5, y - .5), (x + .5, y - .5), (x + .5, y + .5), (x - .5, y + .5)]


def mat(M, v):
  return (M[0][0] * v[0] + M[0][1] * v[1], M[1][0] * v[0] + M[1][1] * v[1])


def draw_patch(ax, Wt, r=0.18, max_level=None):
  grid = Wt['grid']
  nb = NB[grid]
  labels = {(tuple(c), nb[d]): l for (c, d), l in zip(Wt['edges'], Wt['labels'])}
  marks = []
  for pl in Wt['placements']:
    lev = pl['level']
    if max_level is not None and lev > max_level:
      continue
    M, t = pl['M'], pl['t']
    col = LEVEL_COLOURS[min(lev, len(LEVEL_COLOURS) - 1)]
    cells = []
    for c in Wt['cells']:
      m = mat(M, c)
      cells.append((m[0] + t[0], m[1] + t[1]))
    for c in cells:
      ax.add_patch(Polygon(cell_poly(grid, c), closed=True, facecolor=col, edgecolor=col, lw=0.3))
    cs = set(cells)
    for (c, n), l in labels.items():
      m = mat(M, c)
      pc = (m[0] + t[0], m[1] + t[1])
      pn = mat(M, n)
      a = xy(grid, pc)
      b = xy(grid, (pc[0] + pn[0], pc[1] + pn[1]))
      mid = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
      ang = math.degrees(math.atan2(b[1] - a[1], b[0] - a[0]))
      marks.append((l, mid, ang, col))
      # outline of the tile: edge perpendicular to (a, b) through mid
      h = (1 / math.sqrt(3)) / 2 if grid == 'hex' else .5
      dx, dy = -(b[1] - a[1]), b[0] - a[0]
      nrm = math.hypot(dx, dy)
      dx, dy = dx / nrm * h, dy / nrm * h
      ax.plot([mid[0] - dx, mid[0] + dx], [mid[1] - dy, mid[1] + dy], color='white', lw=0.9, zorder=3)
  for l, mid, ang, col in marks:
    if l == 'n':
      ax.add_patch(Wedge(mid, r, ang + 90, ang + 270, facecolor='white', edgecolor='none', zorder=4))
  for l, mid, ang, col in marks:
    if l == 'b':
      ax.add_patch(Wedge(mid, r, ang - 90, ang + 90, facecolor=col, edgecolor='none', zorder=5))
  ax.set_aspect('equal')
  ax.axis('off')
  ax.autoscale_view()


def patch_figure():
  Wt = json.load(open(os.path.join(W, 'hex4_line_k5.json')))
  fig, ax = plt.subplots(figsize=(6.2, 6.2))
  draw_patch(ax, Wt)
  fig.savefig(os.path.join(HERE, 'patch-bar4.pdf'), bbox_inches='tight')
  plt.close(fig)


def table_figure():
  T = json.load(open(os.path.join(HERE, 'verification', 'results.json')))
  rows = [('hex', [t for t in T['tiles'] if t['grid'] == 'hex']), ('sq', [t for t in T['tiles'] if t['grid'] == 'sq'])]
  ncol = 11
  nrow = sum((len(ts) + ncol - 1) // ncol for _, ts in rows)
  fig, axes = plt.subplots(nrow, ncol, figsize=(ncol * 1.05, nrow * 1.25))
  k = 0
  for grid, ts in rows:
    for i in range(((len(ts) + ncol - 1) // ncol) * ncol):
      ax = axes.flat[k]
      k += 1
      ax.axis('off')
      if i >= len(ts):
        continue
      t = ts[i]
      for c in t['cells']:
        ax.add_patch(Polygon(cell_poly(grid, c), closed=True, facecolor='#3b6ea5' if t['h'] == T['max'][grid] else '#9cc3e6',
                             edgecolor='white', lw=1))
      pts = [xy(grid, c) for c in t['cells']]
      cx, cy = sum(p[0] for p in pts) / len(pts), sum(p[1] for p in pts) / len(pts)
      ax.set_xlim(cx - 2.6, cx + 2.6)
      ax.set_ylim(cy - 2.6, cy + 2.6)
      ax.set_aspect('equal')
      ax.set_title(f"h = {t['h']}", fontsize=9)
  fig.savefig(os.path.join(HERE, 'table-tiles.pdf'), bbox_inches='tight')
  plt.close(fig)


if __name__ == '__main__':
  patch_figure()
  if os.path.exists(os.path.join(HERE, 'verification', 'results.json')):
    table_figure()
