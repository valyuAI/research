#!/usr/bin/env python3
"""Draw Figure 1: the special octagon O(5,6,1,2), the set S, and one trajectory from a vertex."""
import sys
from fractions import Fraction as Fr
sys.path.insert(0, 'verification')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from symplectic_billiard import Polygon, special_octagon

W, H, c1, c2 = 5, 6, 1, 2
P = Polygon(special_octagon(W, H, c1, c2))
x, y = (0, Fr(0)), (1, Fr(37, 100))        # x0 = vertex (2,0), x1 on the lower right 45-degree side
pts = [P.point(x), P.point(y)]
while not P.is_vertex(y):
  z = P.step(x, y)
  x, y = y, z
  pts.append(P.point(y))
even = [(float(a), float(b)) for i, (a, b) in enumerate(pts) if i % 2 == 0]
odd = [(float(a), float(b)) for i, (a, b) in enumerate(pts) if i % 2 == 1]

fig, ax = plt.subplots(figsize=(4.2, 4.8))
V = [(float(a), float(b)) for a, b in P.V] + [(float(P.V[0][0]), float(P.V[0][1]))]
ax.plot([v[0] for v in V], [v[1] for v in V], color='black', lw=1.2)
# the set S: lattice points, half-lattice points on 45-degree sides, half-integer abscissae on horizontal sides
S0, Sd, Sh = [], [], []
for i in range(2 * W + 1):
  for j in range(2 * H + 1):
    X, Y = Fr(i, 2), Fr(j, 2)
    on = None
    for k in range(8):
      a, b = P.V[k], P.V[(k + 1) % 8]
      e = (b[0] - a[0], b[1] - a[1])
      if e[0] * (Y - a[1]) - e[1] * (X - a[0]) == 0 and min(a[0], b[0]) <= X <= max(a[0], b[0]) and min(a[1], b[1]) <= Y <= max(a[1], b[1]):
        on = k
    if on is None:
      continue
    if X.denominator == 1 and Y.denominator == 1:
      S0.append((X, Y))
    elif on in (1, 3, 5, 7) and X.denominator == 2 and Y.denominator == 2:
      Sd.append((X, Y))
    elif on in (0, 4) and X.denominator == 2 and Y.denominator == 1:
      Sh.append((X, Y))
ax.scatter([float(p[0]) for p in S0], [float(p[1]) for p in S0], s=14, color='black', zorder=3, label='$S_0$ (lattice)')
ax.scatter([float(p[0]) for p in Sd], [float(p[1]) for p in Sd], s=18, facecolors='white', edgecolors='black', zorder=3, label='$S_d$')
ax.scatter([float(p[0]) for p in Sh], [float(p[1]) for p in Sh], s=18, marker='s', facecolors='white', edgecolors='black', zorder=3, label='$S_h$')
ax.plot([p[0] for p in even], [p[1] for p in even], color='#1f5fa8', lw=0.9, zorder=2, label='even points')
ax.plot([p[0] for p in odd], [p[1] for p in odd], color='#b0b0b0', lw=0.7, ls='--', zorder=1, label='odd points')
ax.set_aspect('equal')
ax.set_xlim(-0.4, W + 0.4)
ax.set_ylim(-0.4, H + 0.4)
ax.axvline(W / 2, color='#999999', lw=0.5, ls=':')
ax.set_xticks(range(W + 1))
ax.set_yticks(range(H + 1))
ax.tick_params(labelsize=7)
ax.legend(fontsize=6.5, loc='upper center', bbox_to_anchor=(0.5, -0.07), ncol=3, frameon=False)
fig.tight_layout()
fig.savefig('octagon-figure.pdf')
print('even points:', [(str(a), str(b)) for i, (a, b) in enumerate(pts) if i % 2 == 0])
