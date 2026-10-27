"""Exact sparse linear algebra over a number field K (nf.NF or tower.QuadExt). Standard library only.

Matrices are lists of sparse rows {column: element}. All arithmetic is exact, so ranks and kernels computed
here are ranks and kernels over K, hence over the reals."""


def rref(K, rows, ncols):
  """Fully reduced row echelon form. Returns {pivot column: row} with row[pivot] == 1 and every pivot column
  of the other rows equal to zero."""
  piv = {}
  for r0 in rows:
    r = {c: x for c, x in r0.items() if not K.is0(x)}
    for c in sorted(set(r) & set(piv)):
      if c in r:
        f = r[c]
        for cc, y in piv[c].items():
          v = K.sub(r.get(cc, K.zero), K.mul(f, y))
          if K.is0(v):
            r.pop(cc, None)
          else:
            r[cc] = v
    # columns may have been re-introduced below previous pivots only if they are pivots; repeat until clean
    while set(r) & set(piv):
      c = min(set(r) & set(piv))
      f = r[c]
      for cc, y in piv[c].items():
        v = K.sub(r.get(cc, K.zero), K.mul(f, y))
        if K.is0(v):
          r.pop(cc, None)
        else:
          r[cc] = v
    if not r:
      continue
    c0 = min(r)
    inv = K.inv(r[c0])
    r = {c: K.mul(x, inv) for c, x in r.items()}
    for pc, pr in piv.items():
      if c0 in pr:
        f = pr[c0]
        for cc, y in r.items():
          v = K.sub(pr.get(cc, K.zero), K.mul(f, y))
          if K.is0(v):
            pr.pop(cc, None)
          else:
            pr[cc] = v
    piv[c0] = r
  return piv


def nullspace(K, rows, ncols):
  """Basis of {x : row . x = 0 for every row}, as sparse dicts; and the rank."""
  piv = rref(K, rows, ncols)
  free = [c for c in range(ncols) if c not in piv]
  basis = []
  for f in free:
    v = {f: K.one}
    for pc, pr in piv.items():
      if f in pr:
        v[pc] = K.neg(pr[f])
    basis.append(v)
  return basis, len(piv)


def transpose(rows, ncols):
  cols = [dict() for _ in range(ncols)]
  for i, r in enumerate(rows):
    for c, x in r.items():
      cols[c][i] = x
  return cols, len(rows)


def apply(K, rows, v):
  out = []
  for r in rows:
    s = K.zero
    for c, x in r.items():
      if c in v:
        s = K.add(s, K.mul(x, v[c]))
    out.append(s)
  return out


def rank(K, rows, ncols):
  return len(rref(K, rows, ncols))
