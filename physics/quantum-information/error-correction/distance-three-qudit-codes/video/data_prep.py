"""Extract and re-check every number the explainer shows. Writes data.json.

Standard library only. Reads the certificates in ../verification/ and recomputes the small
geometry facts used on screen (point and slice counts of the 5-question qutrit space, the
hole count, the slope-line construction and its running Plucker total).
"""

import itertools
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
VER = HERE.parent / 'verification'
Q = 3


def load(path):
  d = json.loads(path.read_text())
  A = json.loads(d['stabilizer_X_part_A']) if isinstance(d['stabilizer_X_part_A'], str) else d['stabilizer_X_part_A']
  B = json.loads(d['stabilizer_Z_part_B']) if isinstance(d['stabilizer_Z_part_B'], str) else d['stabilizer_Z_part_B']
  return d, A, B


def col(M, i):
  return tuple(row[i] % Q for row in M)


def add(u, v, s=1, t=1):
  return tuple((s * a + t * b) % Q for a, b in zip(u, v))


def span2(u, v):
  return {add(u, v, s, t) for s in range(Q) for t in range(Q)}


def normalise(v):
  """Projective point: scale so the first nonzero entry is 1."""
  for x in v:
    if x:
      inv = pow(x, Q - 2, Q)
      return tuple(a * inv % Q for a in v)
  return None


def wedge(u, v):
  n = len(u)
  return tuple((u[i] * v[j] - u[j] * v[i]) % Q for i in range(n) for j in range(i + 1, n))


# 1. The extremal [[28,23,3]]_3 certificate: fingerprints and skewness.
cert, A, B = load(VER / 'certificates' / 'maximal' / 'q3_r5_n28.json')
n, r = cert['n'], cert['r_ambient']
assert (n, r) == (28, 5)
sheets = []
for i in range(n):
  twist = col(A, i)                       # syndrome of a unit twist (Z) on qutrit i
  shift = tuple((-x) % Q for x in col(B, i))  # syndrome of a unit shift (X) on qutrit i
  sheets.append((shift, twist))
lines = [frozenset(normalise(v) for v in span2(*s) if any(v)) for s in sheets]
assert all(len(l) == 4 for l in lines)
assert all(not (a & b) for a, b in itertools.combinations(lines, 2)), 'lines must be skew'
syndromes = [add(s, t, a, b) for s, t in sheets for a in range(Q) for b in range(Q) if (a, b) != (0, 0)]
assert len(syndromes) == 8 * n == len(set(syndromes)) and all(any(v) for v in syndromes)
total = tuple(sum(c) % Q for c in zip(*[wedge(t, s) for s, t in sheets]))
assert not any(total)

# 2. The 5-question qutrit space: points, slices, incidences, holes.
vectors = [v for v in itertools.product(range(Q), repeat=r) if any(v)]
points = sorted({normalise(v) for v in vectors})
slices = points  # a slice is {x : h.x = 0}, one per projective point h
assert len(points) == 121


def on(h, x):
  return sum(a * b for a, b in zip(h, x)) % Q == 0


slice_sizes = {sum(on(h, x) for x in points) for h in slices}
per_point = {sum(on(h, x) for h in slices) for x in points}
assert slice_sizes == {40} and per_point == {40}
# Every line lies inside a slice or meets it in exactly one point.
meets = {sum(on(h, x) for x in l) for h in slices for l in lines}
assert meets <= {1, 4}
covered = set().union(*lines)
holes28 = len(points) - len(covered)
assert holes28 == 121 - 112 == 9
# Hole arithmetic for a hypothetical 29 lines.
holes29 = 121 - 29 * 4
per_slice_options = [40 - (29 - x) - 4 * x for x in range(0, 4)]
assert holes29 == 5 and per_slice_options == [11, 8, 5, 2]
assert holes29 * 40 == 200 < 121 * 2 == 242

# 3. The slope-line construction in GF(27) = GF(3)[w]/(w^3 - w - 1).
def fmul(a, b):
  # a, b are coefficient triples (c0, c1, c2) for c0 + c1 w + c2 w^2
  prod = [0] * 5
  for i, x in enumerate(a):
    for j, y in enumerate(b):
      prod[i + j] += x * y
  for k in (4, 3):  # w^3 = w + 1
    c = prod[k]
    prod[k] = 0
    prod[k - 3] += c
    prod[k - 2] += c
  return tuple(c % Q for c in prod[:3])


W = (0, 1, 0)
field = list(itertools.product(range(Q), repeat=3))
assert len(field) == 27


def slope_line(a):
  u = (1, 0) + a
  v = (0, 1) + fmul(a, W)
  return u, v


slope = {a: slope_line(a) for a in field}
slope_lines = {a: frozenset(normalise(x) for x in span2(*slope[a]) if any(x)) for a in field}
vertical = ((0, 0, 1, 0, 0), (0, 0) + W)  # the line <iota(1), iota(w)> inside the leftover space
vertical_line = frozenset(normalise(x) for x in span2(*vertical) if any(x))
all28 = list(slope_lines.values()) + [vertical_line]
assert all(not (a & b) for a, b in itertools.combinations(all28, 2))


def total_of(weighted):
  acc = [0] * 10
  run = []
  for (u, v), lam in weighted:
    p = wedge(u, v)
    acc = [(x + lam * y) % Q for x, y in zip(acc, p)]
    run.append(list(acc))
  return run


order = sorted(field)
plain = total_of([(slope[a], 1) for a in order])
assert not any(plain[-1])
special = {(2, 0, 0): 2, (0, 0, 0): -1, (1, 0, 0): 2}  # a = -1, 0, 1
reweighted = total_of([(slope[a], special.get(a, 1)) for a in order])
leftover = reweighted[-1]
closing = total_of([(slope[a], special.get(a, 1)) for a in order] + [(vertical, -2)])
assert any(leftover) and not any(closing[-1])
with_plain_extra = total_of([(slope[a], 1) for a in order] + [(vertical, 1)])
assert any(with_plain_extra[-1])

# 4. Classical warm-up: the repetition code and the [7,4] Hamming code.
ham_cols = [tuple(int(b) for b in format(i, '03b')) for i in range(1, 8)]

data = {
  'example_qutrit': 13,
  'shift': list(sheets[13][0]),
  'twist': list(sheets[13][1]),
  'sheet': sorted([list(add(sheets[13][0], sheets[13][1], a, b)) for a in range(Q) for b in range(Q)]),
  'example_points': sorted([list(p) for p in lines[13]]),
  'n_points': 121, 'slice_size': 40, 'slices_per_point': 40, 'holes28': holes28,
  'per_slice_options': per_slice_options,
  'plain_running': plain, 'reweighted_running': reweighted, 'reweighted_leftover': leftover,
  'special_slopes': [list(a) for a in special], 'closing_final': closing[-1],
  'plain_plus_extra_final': with_plain_extra[-1], 'vertical_plucker': list(wedge(*vertical)),
  'hamming_columns': [list(c) for c in ham_cols],
}
(HERE / 'data.json').write_text(json.dumps(data, indent=1))
print('shift', data['shift'], 'twist', data['twist'])
print('points of line 13', data['example_points'])
print('reweighted leftover', leftover, 'vertical plucker', data['vertical_plucker'])
print('plain + unweighted extra', with_plain_extra[-1])
print('all checks passed')
