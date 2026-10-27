"""Brute-force census of nonsingular graphs with n^- <= 4 on N <= 10 vertices, over ALL graphs produced
by nauty's geng (connected or not). Independent of the extension lemmas. Float eigenvalues decide sign
when every |lambda| > 1e-6 (rounding error is below 1e-12 here); otherwise the exact FLINT
characteristic polynomial decides.

Usage: python brute_census.py Nmax
"""
import subprocess, sys, time
import numpy as np
from enumerate_nonsingular import exact_inertia


def decode(lines, n):
  nb = n * (n - 1) // 2
  L = 1 + (nb + 5) // 6
  buf = np.frombuffer(b''.join(lines), dtype=np.uint8).reshape(len(lines), L)
  x = (buf[:, 1:] - 63).astype(np.uint8)
  bits = np.unpackbits(x[:, :, None], axis=2)[:, :, 2:].reshape(len(lines), -1)[:, :nb]
  A = np.zeros((len(lines), n, n), dtype=np.int8)
  ii, jj = [], []
  for j in range(1, n):
    for i in range(j):
      ii.append(i); jj.append(j)
  A[:, ii, jj] = bits
  A[:, jj, ii] = bits
  return A


def main():
  for N in range(2, int(sys.argv[1]) + 1):
    t0 = time.time()
    p = subprocess.Popen(['geng', '-q', str(N)], stdout=subprocess.PIPE)
    counts = {}
    def flush(buf):
      A = decode(buf, N)
      ev = np.linalg.eigvalsh(A.astype(np.float64))
      amb = np.abs(ev).min(axis=1) <= 1e-6
      neg = (ev < -1e-6).sum(axis=1)
      for i in np.nonzero(~amb & (neg <= 4))[0]:
        counts[int(neg[i])] = counts.get(int(neg[i]), 0) + 1
      for i in np.nonzero(amb)[0]:
        pp, z, q = exact_inertia(A[i])
        if z == 0 and q <= 4:
          counts[q] = counts.get(q, 0) + 1
    buf = []
    for line in p.stdout:
      buf.append(line.rstrip(b'\n'))
      if len(buf) == 200000:
        flush(buf); buf = []
    if buf:
      flush(buf)
    print(f'N={N} nonsingular graphs with n^-<=4, by n^-: {dict(sorted(counts.items()))} ({time.time()-t0:.0f}s)', flush=True)


if __name__ == '__main__':
  main()
