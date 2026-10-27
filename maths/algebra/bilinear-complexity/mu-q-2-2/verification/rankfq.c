// Exhaustive decision of R_{F_q}(F_q[x]/(f)) <= n + m for q in {2,3,4,5,7}, deg f = n <= 4,
// m in {1,...,4}.  Field arithmetic by tables (F_4 = {0,1,w,w^2} coded 0,1,2,3).
// Criterion: rank <= n+m iff some W >= S (slice span), dim W = n+m, is spanned by rank-one
// matrices; W = S + <F_1..F_m> with independent images in V = F_q^{n^2}/S.
// F_1: one representative per orbit of <M -> L_u^T M L_v (u,v units), M -> M^T>.
// F_2 < ... < F_{m-1}: all; F_m: bucketing by projective image modulo the prefix span.
// Usage: rankfq q m c_0 ... c_n
#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

#define MAXN 4
#define D 16
static int q, n, nn, m, dq;
static uint8_t ADD[8][8], MUL[8][8], NEG[8], INV[8];
static uint8_t fc[MAXN + 1];

static int parse_int(const char *text, int lower, int upper, int *value) {
  char *end;
  errno = 0;
  long parsed = strtol(text, &end, 10);
  if (errno || end == text || *end || parsed < lower || parsed > upper) return 0;
  *value = (int)parsed;
  return 1;
}

static void field_init(void) {
  if (q == 4) {
    // w^2 = w + 1; elements a + b w coded as a + 2b
    for (int x = 0; x < 4; x++) for (int y = 0; y < 4; y++) {
      ADD[x][y] = x ^ y;
      int a0 = x & 1, a1 = x >> 1, b0 = y & 1, b1 = y >> 1;
      // (a0 + a1 w)(b0 + b1 w) = a0b0 + (a0b1 + a1b0) w + a1b1 (w + 1)
      int c0 = (a0 & b0) ^ (a1 & b1), c1 = (a0 & b1) ^ (a1 & b0) ^ (a1 & b1);
      MUL[x][y] = c0 | (c1 << 1);
    }
    for (int x = 0; x < 4; x++) NEG[x] = x;
  } else {
    for (int x = 0; x < q; x++) for (int y = 0; y < q; y++) { ADD[x][y] = (x + y) % q; MUL[x][y] = (x * y) % q; }
    for (int x = 0; x < q; x++) NEG[x] = (q - x) % q;
  }
  for (int x = 1; x < q; x++) for (int y = 1; y < q; y++) if (MUL[x][y] == 1) INV[x] = y;
}
#define SUBM(a, f, b) ADD[a][NEG[MUL[f][b]]]   /* a - f*b */

static void mulA(const uint8_t *x, const uint8_t *y, uint8_t *z) {
  uint8_t t[2 * MAXN] = {0};
  for (int i = 0; i < n; i++) for (int j = 0; j < n; j++) t[i + j] = ADD[t[i + j]][MUL[x[i]][y[j]]];
  for (int d = 2 * n - 2; d >= n; d--) if (t[d]) { uint8_t c = t[d]; for (int k = 0; k <= n; k++) t[d - n + k] = SUBM(t[d - n + k], c, fc[k]); }
  for (int i = 0; i < n; i++) z[i] = t[i];
}

static void normalize(uint8_t *v, int len) {
  for (int i = 0; i < len; i++) if (v[i]) { uint8_t s = INV[v[i]]; for (int j = i; j < len; j++) v[j] = MUL[v[j]][s]; return; }
}

// rank of k rows of length len (destroys a copy)
static uint8_t RB[8192][D];
static int rank_rows(uint8_t (*rows)[D], int k, int len) {
  if (k < 0 || k > 8192 || len < 1 || len > D) {
    fprintf(stderr, "Rank workspace capacity exceeded\n");
    exit(2);
  }
  memcpy(RB, rows, (size_t)D * k);
  int r = 0;
  for (int c = 0; c < len && r < k; c++) {
    int p = -1; for (int i = r; i < k; i++) if (RB[i][c]) { p = i; break; }
    if (p < 0) continue;
    if (p != r) { uint8_t t[D]; memcpy(t, RB[p], D); memcpy(RB[p], RB[r], D); memcpy(RB[r], t, D); }
    normalize(RB[r], len);
    for (int i = 0; i < k; i++) if (i != r && RB[i][c]) { uint8_t f = RB[i][c]; for (int j = 0; j < len; j++) RB[i][j] = SUBM(RB[i][j], f, RB[r][j]); }
    r++;
  }
  return r;
}

static int nfun, nr;
static uint8_t (*FUN)[MAXN];
static uint8_t (*R1)[D], (*IM)[D];
static int *fa, *fb;

// echelon helper over the quotient space
typedef struct { int k; int piv[8]; uint8_t b[8][D]; } Ech;
static int ech_add(Ech *E, const uint8_t *v0) {
  uint8_t v[D]; memcpy(v, v0, D);
  for (int i = 0; i < E->k; i++) if (v[E->piv[i]]) { uint8_t f = v[E->piv[i]]; for (int j = 0; j < dq; j++) v[j] = SUBM(v[j], f, E->b[i][j]); }
  int p = -1; for (int j = 0; j < dq; j++) if (v[j]) { p = j; break; }
  if (p < 0) return 0;
  normalize(v, dq);
  for (int i = 0; i < E->k; i++) if (E->b[i][p]) { uint8_t f = E->b[i][p]; for (int j = 0; j < dq; j++) E->b[i][j] = SUBM(E->b[i][j], f, v[j]); }
  memcpy(E->b[E->k], v, D); E->piv[E->k++] = p;
  return 1;
}
static void ech_reduce(const Ech *E, uint8_t *v) {
  for (int i = 0; i < E->k; i++) if (v[E->piv[i]]) { uint8_t f = v[E->piv[i]]; for (int j = 0; j < dq; j++) v[j] = SUBM(v[j], f, E->b[i][j]); }
}

// hash buckets
// At most ((7^4 - 1) / (7 - 1))^2 = 160000 rank-one forms, hence buckets.
#define HB (1 << 18)
static uint64_t hkey[HB]; static int hcnt[HB]; static int htouch[HB], nht;
static int hslot(uint64_t key) {
  uint64_t h = key * 0x9E3779B97F4A7C15ULL; int s = (int)(h >> 46) & (HB - 1);
  while (hcnt[s] && hkey[s] != key) s = (s + 1) & (HB - 1);
  return s;
}

static long long prefixes = 0, cand = 0, hits = 0;
static int *slotof; static int *common; static uint8_t (*rowbuf)[D];

static int test_prefix(const int *pre, int k) {
  Ech E; E.k = 0;
  for (int i = 0; i < k; i++) if (!ech_add(&E, IM[pre[i]])) return 0;
  prefixes++;
  int nc = 0; nht = 0;
  for (int s = 0; s < nr; s++) {
    uint8_t v[D]; memcpy(v, IM[s], D); ech_reduce(&E, v);
    int nz = 0; for (int j = 0; j < dq; j++) if (v[j]) { nz = 1; break; }
    if (!nz) { common[nc++] = s; slotof[s] = -1; continue; }
    normalize(v, dq);
    uint64_t key = 0; for (int j = 0; j < dq; j++) key = key * 8 + v[j];
    key += 1;
    int sl = hslot(key);
    if (!hcnt[sl]) { hkey[sl] = key; htouch[nht++] = sl; }
    hcnt[sl]++; slotof[s] = sl;
  }
  for (int c = 0; c < nc; c++) memcpy(rowbuf[c], R1[common[c]], D);
  int rc = rank_rows(rowbuf, nc, nn);
  int found = 0;
  for (int s = 0; s < nr && !found; s++) {
    int sl = slotof[s];
    if (sl < 0 || hcnt[sl] <= 0) continue;
    if (hcnt[sl] >= n + m - rc) {
      cand++;
      int kk = nc;
      for (int t = 0; t < nr; t++) if (slotof[t] == sl) memcpy(rowbuf[kk++], R1[t], D);
      if (rank_rows(rowbuf, kk, nn) == n + m) {
        found = 1; hits++;
        printf("HIT prefix:");
        for (int i = 0; i < k; i++) printf(" %d", pre[i]);
        printf(" | W rank-ones (a;b):");
        for (int c = 0; c < nc; c++) { printf(" ["); for (int i = 0; i < n; i++) printf("%d", FUN[fa[common[c]]][i]); printf(";"); for (int i = 0; i < n; i++) printf("%d", FUN[fb[common[c]]][i]); printf("]"); }
        for (int t = 0; t < nr; t++) if (slotof[t] == sl) { printf(" ["); for (int i = 0; i < n; i++) printf("%d", FUN[fa[t]][i]); printf(";"); for (int i = 0; i < n; i++) printf("%d", FUN[fb[t]][i]); printf("]"); }
        printf("\n");
      }
    }
    hcnt[sl] = -1;  // processed
  }
  for (int i = 0; i < nht; i++) { hcnt[htouch[i]] = 0; hkey[htouch[i]] = 0; }
  return found;
}

int main(int argc, char **argv) {
  if (argc < 5 || argc > 8) {
    fprintf(stderr, "Usage: rankfq q m c_0 ... c_n (n<=4, monic)\n");
    return 2;
  }
  n = argc - 4; nn = n * n;
  if (!parse_int(argv[1], 2, 7, &q) || q == 6 || !parse_int(argv[2], 1, 4, &m)) {
    fprintf(stderr, "Unsupported field or rank increment\n");
    return 2;
  }
  if (m > nn - n) {
    fprintf(stderr, "Rank increment exceeds the quotient dimension\n");
    return 2;
  }
  setvbuf(stdout, NULL, _IOLBF, 0);
  field_init();
  for (int i = 0; i <= n; i++) {
    int coefficient;
    if (!parse_int(argv[3 + i], 0, q - 1, &coefficient)) {
      fprintf(stderr, "Invalid field coefficient\n");
      return 2;
    }
    fc[i] = (uint8_t)coefficient;
  }
  if (fc[n] != 1) { fprintf(stderr, "Polynomial must be monic\n"); return 2; }
  // slices
  uint8_t sl[MAXN][D]; memset(sl, 0, sizeof sl);
  for (int i = 0; i < n; i++) for (int j = 0; j < n; j++) {
    uint8_t x[MAXN] = {0}, y[MAXN] = {0}, z[MAXN]; x[i] = 1; y[j] = 1; mulA(x, y, z);
    for (int k = 0; k < n; k++) sl[k][i * n + j] = z[k];
  }
  // reduced echelon of S in F_q^{nn}
  uint8_t Sb[MAXN][D]; int piv[MAXN], ns = 0;
  for (int k = 0; k < n; k++) {
    uint8_t v[D]; memcpy(v, sl[k], D);
    for (int i = 0; i < ns; i++) if (v[piv[i]]) { uint8_t f = v[piv[i]]; for (int j = 0; j < nn; j++) v[j] = SUBM(v[j], f, Sb[i][j]); }
    int p = -1; for (int j = 0; j < nn; j++) if (v[j]) { p = j; break; }
    if (p < 0) { printf("dependent slices\n"); return 1; }
    normalize(v, nn);
    for (int i = 0; i < ns; i++) if (Sb[i][p]) { uint8_t f = Sb[i][p]; for (int j = 0; j < nn; j++) Sb[i][j] = SUBM(Sb[i][j], f, v[j]); }
    memcpy(Sb[ns], v, D); piv[ns++] = p;
  }
  int nonp[D]; dq = 0;
  for (int c = 0; c < nn; c++) { int isp = 0; for (int i = 0; i < ns; i++) if (piv[i] == c) isp = 1; if (!isp) nonp[dq++] = c; }
  int qn = 1; for (int i = 0; i < n; i++) qn *= q;
  FUN = malloc((size_t)MAXN * qn); nfun = 0;
  if (!FUN) { fprintf(stderr, "Allocation failed\n"); return 2; }
  for (int code = 1; code < qn; code++) {
    uint8_t v[MAXN] = {0}; int c = code; for (int i = 0; i < n; i++) { v[i] = c % q; c /= q; }
    int first = 0; for (int i = 0; i < n; i++) if (v[i]) { first = v[i]; break; }
    if (first != 1) continue;
    memcpy(FUN[nfun++], v, MAXN);
  }
  nr = nfun * nfun;
  R1 = malloc((size_t)D * nr); IM = malloc((size_t)D * nr); fa = malloc(sizeof(int) * nr); fb = malloc(sizeof(int) * nr);
  slotof = malloc(sizeof(int) * nr); common = malloc(sizeof(int) * nr); rowbuf = malloc((size_t)D * (nr + 16));
  if (!R1 || !IM || !fa || !fb || !slotof || !common || !rowbuf) {
    fprintf(stderr, "Allocation failed\n");
    return 2;
  }
  int t = 0;
  for (int a = 0; a < nfun; a++) for (int b = 0; b < nfun; b++, t++) {
    fa[t] = a; fb[t] = b;
    memset(R1[t], 0, D);
    for (int i = 0; i < n; i++) for (int j = 0; j < n; j++) R1[t][i * n + j] = MUL[FUN[a][i]][FUN[b][j]];
    uint8_t v[D]; memcpy(v, R1[t], D);
    for (int i = 0; i < ns; i++) if (v[piv[i]]) { uint8_t f = v[piv[i]]; for (int j = 0; j < nn; j++) v[j] = SUBM(v[j], f, Sb[i][j]); }
    memset(IM[t], 0, D);
    for (int k = 0; k < dq; k++) IM[t][k] = v[nonp[k]];
  }
  // units and orbits of functionals
  static uint8_t units[4096][MAXN]; int nu = 0;
  for (int code = 1; code < qn; code++) {
    uint8_t u[MAXN] = {0}; int c = code; for (int i = 0; i < n; i++) { u[i] = c % q; c /= q; }
    uint8_t rows[MAXN][D]; memset(rows, 0, sizeof rows);
    for (int j = 0; j < n; j++) { uint8_t e[MAXN] = {0}, z[MAXN]; e[j] = 1; mulA(u, e, z); for (int i = 0; i < n; i++) rows[j][i] = z[i]; }
    if (rank_rows(rows, n, n) == n) memcpy(units[nu++], u, MAXN);
  }
  int *cls = malloc(sizeof(int) * nfun);
  int ncls = 0; int *stack = malloc(sizeof(int) * nfun);
  if (!cls || !stack) { fprintf(stderr, "Allocation failed\n"); return 2; }
  for (int i = 0; i < nfun; i++) cls[i] = -1;
  for (int s = 0; s < nfun; s++) if (cls[s] < 0) {
    int sp = 0; stack[sp++] = s; cls[s] = ncls;
    while (sp) {
      int a = stack[--sp];
      for (int k = 0; k < nu; k++) {
        uint8_t w[MAXN];
        for (int j = 0; j < n; j++) { uint8_t e[MAXN] = {0}, z[MAXN]; e[j] = 1; mulA(units[k], e, z); uint8_t acc = 0; for (int i = 0; i < n; i++) acc = ADD[acc][MUL[FUN[a][i]][z[i]]]; w[j] = acc; }
        normalize(w, n);
        int idx = -1; for (int g = 0; g < nfun; g++) if (!memcmp(FUN[g], w, n)) { idx = g; break; }
        if (idx < 0) { fprintf(stderr, "Unit action left projective forms\n"); return 2; }
        if (cls[idx] < 0) { cls[idx] = ncls; stack[sp++] = idx; }
      }
    }
    ncls++;
  }
  int reps[64], nreps = 0;
  for (int c1 = 0; c1 < ncls; c1++) for (int c2 = c1; c2 < ncls; c2++)
    for (int s = 0; s < nr; s++) if (cls[fa[s]] == c1 && cls[fb[s]] == c2) {
      if (nreps >= (int)(sizeof reps / sizeof reps[0])) {
        fprintf(stderr, "Orbit representative capacity exceeded\n");
        return 2;
      }
      reps[nreps++] = s;
      break;
    }
  printf("q=%d n=%d m=%d target rank %d: units %d, proj functionals %d, classes %d, F1 reps %d, rank-ones %d\n",
         q, n, m, n + m, nu, nfun, ncls, nreps, nr);
  fflush(stdout);
  int found = 0;
  int pre[8];
  for (int ri = 0; ri < nreps && !found; ri++) {
    pre[0] = reps[ri];
    if (m == 1) { found = test_prefix(pre, 0); break; }
    if (m == 2) { found = test_prefix(pre, 1); }
    else if (m == 3) {
      for (int a = 0; a < nr && !found; a++) {
        if (a == pre[0]) continue;
        pre[1] = a; found = test_prefix(pre, 2);
        if (a % 1000 == 0) {
          fprintf(stderr, "rep %d/%d a %d/%d prefixes %lld\n", ri + 1, nreps, a, nr, prefixes);
          fflush(stderr);
        }
      }
    } else if (m == 4) {
      for (int a = 0; a < nr && !found; a++) {
        if (a == pre[0]) continue; pre[1] = a;
        for (int b = a + 1; b < nr && !found; b++) { if (b == pre[0]) continue; pre[2] = b; found = test_prefix(pre, 3); }
        if (a % 200 == 0) { fprintf(stderr, "rep %d/%d a %d/%d prefixes %lld cand %lld\n", ri + 1, nreps, a, nr, prefixes, cand); fflush(stderr); }
      }
    }
    fprintf(stderr, "rep %d/%d done: prefixes %lld cand %lld hits %lld\n", ri + 1, nreps, prefixes, cand, hits); fflush(stderr);
  }
  printf("RESULT q=%d f=", q); for (int i = 0; i <= n; i++) printf("%d%s", fc[i], i < n ? "," : "");
  printf(" rank<=%d: %s (prefixes %lld, candidate buckets %lld)\n", n + m, found ? "YES" : "NO", prefixes, cand);
  return 0;
}
