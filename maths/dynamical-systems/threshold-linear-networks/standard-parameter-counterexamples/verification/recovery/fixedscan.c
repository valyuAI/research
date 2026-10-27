/* Exact exhaustive scan at fixed integer (beta,t): reads digraph6 lines (interpreted as nonedge matrix N),
   reports N != 0 with (I+beta N)^{-1} 1 > 0 and K = I + beta N + t J positive stable (Hurwitz, exact int128). */
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <math.h>
typedef __int128 i128;
static int n; static long long BETA, T, DEN = 1;
static i128 bareiss_det(i128 a[16][16], int m) { /* destroys a */
  i128 prev = 1; int sign = 1;
  for (int k = 0; k < m - 1; k++) {
    if (a[k][k] == 0) { int p = -1; for (int r = k + 1; r < m; r++) if (a[r][k] != 0) { p = r; break; }
      if (p < 0) return 0; for (int c = 0; c < m; c++) { i128 tmp = a[k][c]; a[k][c] = a[p][c]; a[p][c] = tmp; } sign = -sign; }
    for (int i = k + 1; i < m; i++) for (int j = k + 1; j < m; j++) a[i][j] = (a[i][j] * a[k][k] - a[i][k] * a[k][j]) / prev;
    prev = a[k][k];
  }
  return sign * a[m - 1][m - 1];
}
int main(int argc, char **argv) {
  BETA = atoll(argv[1]); T = atoll(argv[2]); if (argc > 3) DEN = atoll(argv[3]);
  char line[256]; long long floatrej = 0, coefpos = 0, cnt = 0, nonzero = 0, permitted = 0, hits = 0, undecided = 0;
  int N[16][16];
  while (fgets(line, sizeof line, stdin)) {
    char *s = line; if (*s == '&') s++;
    n = s[0] - 63; int bit = 0; s++;
    for (int i = 0; i < n; i++) for (int j = 0; j < n; j++) { int ch = s[bit / 6] - 63; N[i][j] = (ch >> (5 - bit % 6)) & 1; bit++; }
    cnt++; if (cnt % 20000000 == 0) { fprintf(stderr, "progress %lld permitted %lld hits %lld undecided %lld\n", cnt, permitted, hits, undecided); fflush(stderr); }
    int nz = 0; for (int i = 0; i < n; i++) for (int j = 0; j < n; j++) nz |= N[i][j]; if (!nz) continue; nonzero++;
    /* rigorous float prefilter (beta = 3, den = 1, n <= 9): solve C yh = 1 in double and compute the residual
       r = 1 - C yh. det C is an integer congruent to 1 mod 3, so |det C| >= 1; every (n-1)-minor of C is at most
       rn^(n-1) with rn = sqrt(1 + 9(n-1)) (Hadamard), so ||C^{-1}||_inf <= n rn^(n-1) and |y - yh| <= that * ||r||_inf.
       Reject only when yh_i + bound < 0 for some i; everything else goes to the exact test below. */
    if (n <= 9 && BETA == 3 && DEN == 1) {
      double A[16][17], yh[16]; for (int i = 0; i < n; i++) { for (int j = 0; j < n; j++) A[i][j] = (i == j) + 3.0 * N[i][j]; A[i][n] = 1; }
      int sing = 0;
      for (int c = 0; c < n; c++) { int p = c; for (int r = c + 1; r < n; r++) if (fabs(A[r][c]) > fabs(A[p][c])) p = r;
        if (fabs(A[p][c]) < 1e-12) { sing = 1; break; }
        if (p != c) for (int k = 0; k <= n; k++) { double tmp = A[c][k]; A[c][k] = A[p][k]; A[p][k] = tmp; }
        for (int r = 0; r < n; r++) if (r != c) { double f = A[r][c] / A[c][c]; for (int k = c; k <= n; k++) A[r][k] -= f * A[c][k]; } }
      if (!sing) {
        for (int i = 0; i < n; i++) yh[i] = A[i][n] / A[i][i];
        double rmax = 0; for (int i = 0; i < n; i++) { double r = 1.0; for (int j = 0; j < n; j++) r -= ((i == j) + 3.0 * N[i][j]) * yh[j]; if (fabs(r) > rmax) rmax = fabs(r); }
        double ymx = 0; for (int i = 0; i < n; i++) if (fabs(yh[i]) > ymx) ymx = fabs(yh[i]);
        double rn = sqrt(1.0 + 9.0 * (n - 1)), cinv = n * pow(rn, n - 1) * 1.01; /* Hadamard bound on ||C^{-1}||_inf, |det C| >= 1 */
        double err = cinv * (rmax + 1e-13 * (1 + 3.0 * n * ymx)); /* residual rounding allowance */
        int bad = 0; for (int i = 0; i < n; i++) if (yh[i] + err < 0) bad = 1;
        if (bad) { floatrej++; continue; }
      }
    }
    /* exact permission by fraction-free Gauss-Jordan on [C | 1]: ends with det*I | det*y */
    int ok = 1;
    { i128 g[16][17]; for (int i = 0; i < n; i++) { for (int j = 0; j < n; j++) g[i][j] = DEN * (i == j) + BETA * N[i][j]; g[i][n] = 1; }
      i128 prev = 1; int sing = 0;
      for (int k = 0; k < n; k++) {
        if (g[k][k] == 0) { int p = -1; for (int r = k + 1; r < n; r++) if (g[r][k] != 0) { p = r; break; }
          if (p < 0) { sing = 1; break; } for (int c = 0; c <= n; c++) { i128 tmp = g[k][c]; g[k][c] = g[p][c]; g[p][c] = tmp; } }
        for (int i = 0; i < n; i++) if (i != k) { for (int j = 0; j <= n; j++) if (j != k) g[i][j] = (g[k][k] * g[i][j] - g[i][k] * g[k][j]) / prev; g[i][k] = 0; }
        prev = g[k][k];
      }
      if (sing) { undecided++; printf("SINGULAR_C %s", line); continue; }
      /* now g[i][i] = +-det (all equal), g[i][n] = g[i][i]*y_i */
      for (int i = 0; i < n; i++) { i128 num = g[i][n], den = g[i][i]; if (num == 0 || (num > 0) != (den > 0)) { ok = 0; break; } }
    }
    if (!ok) continue; permitted++;
    /* charpoly of K via Berkowitz-free approach: c_k = (-1)^k sum of principal k-minors -> use det(zI+K) coeffs = e_k(K) = sum principal minors */
    long long K[16][16]; for (int i = 0; i < n; i++) for (int j = 0; j < n; j++) K[i][j] = DEN * (i == j) + BETA * N[i][j] + T;
    /* Berkowitz (division free, int128): C = charpoly coefficients of leading blocks, det(xI - K) */
    i128 Cp[17], col[18], v[16], w[16]; int deg = 1; Cp[0] = 1; Cp[1] = -K[0][0];
    for (int r = 1; r < n; r++) {
      col[0] = 1; col[1] = -K[r][r];
      for (int i = 0; i < r; i++) v[i] = K[i][r];
      for (int k = 0; k < r; k++) {
        i128 s2 = 0; for (int j = 0; j < r; j++) s2 += (i128)K[r][j] * v[j]; col[k + 2] = -s2;
        for (int i = 0; i < r; i++) { i128 s3 = 0; for (int j = 0; j < r; j++) s3 += (i128)K[i][j] * v[j]; w[i] = s3; }
        for (int i = 0; i < r; i++) v[i] = w[i];
      }
      i128 nc[18];
      for (int i = 0; i < r + 2; i++) { i128 s4 = 0; for (int j = 0; j <= (i < r ? i : r); j++) if (i - j < r + 2) s4 += col[i - j] * Cp[j]; nc[i] = s4; }
      for (int i = 0; i < r + 2; i++) Cp[i] = nc[i]; deg = r + 1;
    }
    i128 e[17]; for (int k = 0; k <= n; k++) e[k] = (k % 2 ? -Cp[k] : Cp[k]);  /* det(zI+K) coefficients */
    int pos = 1; for (int k = 1; k <= n; k++) if (e[k] <= 0) pos = 0;
    if (!pos) continue;
    /* Routh array in long double; flag near-zero pivots as undecided */
    long double R[2][10]; int L = n / 2 + 1; int stable = 1, und = 0;
    for (int j = 0; j < L; j++) { R[0][j] = (2 * j <= n) ? (long double)e[2 * j] : 0; R[1][j] = (2 * j + 1 <= n) ? (long double)e[2 * j + 1] : 0; }
    long double scale = 0; for (int k = 0; k <= n; k++) if ((long double)e[k] > scale) scale = (long double)e[k];
    for (int row = 2; row <= n; row++) {
      long double nr[10]; for (int j = 0; j < L; j++) { long double a1 = (j + 1 < L) ? R[0][j + 1] : 0, b1 = (j + 1 < L) ? R[1][j + 1] : 0; nr[j] = (R[1][0] * a1 - R[0][0] * b1) / R[1][0]; }
      for (int j = 0; j < L; j++) { R[0][j] = R[1][j]; R[1][j] = nr[j]; }
      if (fabsl(R[1][0]) < 1e-12L * scale) { und = 1; break; }
      if (R[1][0] < 0) { stable = 0; break; }
    }
    coefpos++;
    if (und) { undecided++; printf("UNDECIDED %s", line); continue; }
    if (stable) { hits++; printf("HIT %s", line); fflush(stdout); } else printf("REJ %s", line);
  }
  fprintf(stderr, "beta=%lld t=%lld den=%lld total=%lld nonzero=%lld permitted=%lld coefpos=%lld hits=%lld undecided=%lld floatrej=%lld\n", BETA, T, DEN, cnt, nonzero, permitted, coefpos, hits, undecided, floatrej);
  return 0;
}
