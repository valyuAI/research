"""Replay the illustrated certificate and freeze its display coordinates.

Run with python -B. No checker outputs or research files are modified.
Floating checks validate the display, not the theorem.
"""
import hashlib
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent
VERIFY = ROOT.parent / 'verification'
sys.path.insert(0, str(VERIFY))
import minkflex
import nfsolid


def require(value, message):
  if not value:
    raise ValueError(message)


def main():
  evidence = json.loads((VERIFY / 'results/flex_finite.json').read_text())['3']
  exact = minkflex.check(VERIFY / 'data/J03.json', evidence['S1_edges'])
  require(exact['ok'], 'Exact J3 flex check failed')
  print('Exact J3 partition, admissible axis and nontriviality: PASS', flush=True)
  _, field, raw, faces = nfsolid.load(VERIFY / 'data/J03.json')
  points, _, edges, _ = nfsolid.validate(field, raw, faces)
  for _ in range(100):
    mid = (field.lo + field.hi) / 2
    if field._msign(mid) == field._msign(field.lo):
      field.lo = mid
    else:
      field.hi = mid
  p = np.array([[field.to_float(x) for x in v] for v in points])
  group1 = {tuple(e) for e in evidence['S1_edges']}
  s1 = np.full_like(p, np.nan)
  s1[0] = 0
  while np.isnan(s1).any():
    changed = False
    for a, b in edges:
      for u, v in [(a, b), (b, a)]:
        if not np.isnan(s1[u]).any() and np.isnan(s1[v]).any():
          s1[v] = s1[u] + (p[v] - p[u] if (a, b) in group1 else 0)
          changed = True
    require(changed or not np.isnan(s1).any(), 'Disconnected integration')
  s1 -= s1.mean(axis=0)
  s2 = p - s1
  z = np.ones(3) / np.sqrt(3)
  x = np.array([1., -1., 0.]) / np.sqrt(2)
  y = np.cross(z, x)
  basis = np.stack([x, y, z])
  p, s1, s2 = [a @ basis.T for a in [p, s1, s2]]
  max_edge_error = max_plane_error = 0.
  min_convex_margin = float('inf')
  angles = []
  for angle in np.linspace(-8, 8, 161):
    t = np.deg2rad(angle)
    rot = np.array([[np.cos(t), -np.sin(t), 0], [np.sin(t), np.cos(t), 0], [0, 0, 1]])
    q = s1 + s2 @ rot.T
    max_edge_error = max(max_edge_error, max(abs(np.linalg.norm(q[a] - q[b]) - 1) for a, b in edges))
    for face in faces:
      n = np.cross(q[face[1]] - q[face[0]], q[face[2]] - q[face[0]])
      n /= np.linalg.norm(n)
      if np.dot(n, q[face].mean(axis=0)) < 0:
        n *= -1
      residual = (q - q[face[0]]) @ n
      max_plane_error = max(max_plane_error, max(abs(residual[face])))
      min_convex_margin = min(min_convex_margin, min(-residual[j] for j in range(len(q)) if j not in face))
    if abs(angle - 5) < 1e-9:
      face = faces[0]
      for j, v in enumerate(face):
        a = q[face[j - 1]] - q[v]
        b = q[face[(j + 1) % 6]] - q[v]
        angles.append(float(np.rad2deg(np.arccos(np.dot(a, b) / np.linalg.norm(a) / np.linalg.norm(b)))))
  require(max_edge_error < 1e-12 and max_plane_error < 1e-12, 'Display violates metric constraints')
  require(min_convex_margin > 0, 'Display leaves convex neighbourhood')
  require(np.allclose(sorted(angles), [115]*3 + [125]*3), 'Hexagon angle mismatch')
  classification = json.loads((VERIFY / 'results/classification.json').read_text())
  counts = {c: sum(r['class'] == c for r in classification.values()) for c in set(r['class'] for r in classification.values())}
  files = [ROOT.parent / 'readiness.md', ROOT.parent / 'paper.tex', VERIFY / 'data/J03.json', VERIFY / 'results/flex_finite.json', VERIFY / 'results/classification.json', VERIFY / 'results/second_order.json', VERIFY / 'results/prestress_replay.json']
  assets = {'p': p.tolist(), 's1': s1.tolist(), 's2': s2.tolist(), 'faces': faces, 'edges': edges, 'group1': sorted(group1), 'classification': classification}
  (ROOT / 'geometry.json').write_text(json.dumps(assets, indent=2))
  report = {'exact_J3_certificate_replayed': exact, 'display_angles_sampled': 161, 'display_angle_range_degrees': [-8, 8], 'max_edge_error': max_edge_error, 'max_plane_error': max_plane_error, 'minimum_convex_margin': min_convex_margin, 'hexagon_angles_at_five_degrees': angles, 'counts': counts, 'input_hashes': {str(p.relative_to(ROOT.parent)): hashlib.sha256(p.read_bytes()).hexdigest() for p in files}, 'scope': 'Exact certificate replay plus float validation of rendered geometry. Not a new full research audit.'}
  (ROOT / 'qa/geometry-check.json').write_text(json.dumps(report, indent=2))
  print(json.dumps({k: v for k, v in report.items() if k not in ['input_hashes', 'exact_J3_certificate_replayed']}, indent=2), flush=True)


if __name__ == '__main__':
  main()
