// Exhaustive test: does the multiplication tensor of F2[x]/(f), deg f = n <= 4,
// have bilinear rank <= n + m over F2?
// Method: rank <= R iff some subspace W of F2^{n x n}, dim W = R, contains the slice
// span S (dim n) and is spanned by rank-one matrices.  WLOG W = S + span(F_1..F_m)
// with F_i rank-one and images in the quotient independent.
// Usage: subsp <f as int> <m>
#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

static int n, m, NB;
static uint32_t S[8];          // slice basis (reduced)
static int piv[8], ns;
static uint32_t R1[256];       // rank-one matrices
static int img[256];           // image index in quotient
static int nr;

static int parse_int(const char *text, int lower, int upper, int *value) {
  char *end;
  errno = 0;
  long parsed = strtol(text, &end, 10);
  if (errno || end == text || *end || parsed < lower || parsed > upper) return 0;
  *value = (int)parsed;
  return 1;
}

static uint32_t reduceS(uint32_t v) {
  for (int i = 0; i < ns; i++) if (v >> piv[i] & 1) v ^= S[i];
  return v;
}

static int rank_of(uint32_t *v, int k) {
  uint32_t b[64]; int r = 0;
  for (int i = 0; i < k; i++) {
    uint32_t x = v[i];
    for (int j = 0; j < r; j++) if ((x ^ b[j]) < x) x ^= b[j];
    if (x) {
      b[r++] = x;
      // keep sorted descending by top bit for the min-trick
      for (int j = r - 1; j > 0 && b[j] > b[j - 1]; j--) { uint32_t t = b[j]; b[j] = b[j - 1]; b[j - 1] = t; }
    }
  }
  return r;
}

int main(int argc, char **argv) {
  if (argc != 3) {
    fprintf(stderr, "Usage: subsp polynomial_bitmask rank_increment\n");
    return 2;
  }
  int f;
  if (!parse_int(argv[1], 2, 31, &f) || !parse_int(argv[2], 0, 8, &m)) {
    fprintf(stderr, "Require a degree-1..4 polynomial bitmask and rank increment 0..8\n");
    return 2;
  }
  n = 31 - __builtin_clz((unsigned)f); NB = n * n;
  if (m > NB - n) {
    fprintf(stderr, "Rank increment exceeds the quotient dimension\n");
    return 2;
  }
  // slices: S_k(i,j) = coeff of x^k in x^{i+j} mod f
  uint32_t sl[8] = {0};
  for (int i = 0; i < n; i++) for (int j = 0; j < n; j++) {
    uint32_t v = 1u << (i + j);
    for (int d = 2 * n; d >= n; d--) if (v >> d & 1) v ^= (uint32_t)f << (d - n);
    for (int k = 0; k < n; k++) if (v >> k & 1) sl[k] |= 1u << (i * n + j);
  }
  // reduced echelon basis of S
  ns = 0;
  for (int k = 0; k < n; k++) {
    uint32_t v = sl[k];
    for (int i = 0; i < ns; i++) if (v >> piv[i] & 1) v ^= S[i];
    if (!v) continue;
    int p = 31 - __builtin_clz(v);
    for (int i = 0; i < ns; i++) if (S[i] >> p & 1) S[i] ^= v;
    S[ns] = v; piv[ns++] = p;
  }
  printf("n=%d dimS=%d m=%d target rank %d\n", n, ns, m, ns + m);
  // rank-one matrices a b^T
  nr = 0;
  for (int a = 1; a < (1 << n); a++) for (int b = 1; b < (1 << n); b++) {
    uint32_t M = 0;
    for (int i = 0; i < n; i++) if (a >> i & 1) M |= (uint32_t)b << (i * n);
    R1[nr++] = M;
  }
  // image coordinates: non-pivot bits of reduced vector, compressed
  int nonp[32], nnp = 0;
  for (int b = 0; b < NB; b++) { int isp = 0; for (int i = 0; i < ns; i++) if (piv[i] == b) isp = 1; if (!isp) nonp[nnp++] = b; }
  for (int t = 0; t < nr; t++) {
    uint32_t v = reduceS(R1[t]); int x = 0;
    for (int q = 0; q < nnp; q++) if (v >> nonp[q] & 1) x |= 1 << q;
    img[t] = x;
    if (!x) { printf("rank-one inside S: rank <= ... (degenerate)\n"); }
  }
  int Q = 1 << nnp;
  uint8_t *inQ = calloc(Q, 1);
  if (!inQ) { fprintf(stderr, "Allocation failed\n"); return 2; }
  long long tested = 0, found = 0;
  int idx[8];
  // enumerate m-subsets of rank-ones (indices increasing)
  for (int k = 0; k < m; k++) idx[k] = k;
  while (1) {
    // check independence of images
    uint32_t iv[8];
    for (int k = 0; k < m; k++) iv[k] = img[idx[k]];
    if (rank_of(iv, m) == m) {
      tested++;
      int span[256], sz = 1; span[0] = 0;
      for (int k = 0; k < m; k++) { for (int s = 0; s < sz; s++) span[sz + s] = span[s] ^ iv[k]; sz *= 2; }
      for (int s = 0; s < sz; s++) inQ[span[s]] = 1;
      uint32_t L[256]; int nl = 0;
      for (int t = 0; t < nr; t++) if (inQ[img[t]]) L[nl++] = R1[t];
      int rk = rank_of(L, nl);
      if (rk == ns + m) {
        found++;
        if (found <= 3) {
          printf("FOUND W: rank-ones in W = %d:", nl);
          for (int t = 0; t < nl; t++) printf(" %x", L[t]);
          printf("\n");
        }
      }
      for (int s = 0; s < sz; s++) inQ[span[s]] = 0;
    }
    int k = m - 1;
    while (k >= 0 && idx[k] == nr - m + k) k--;
    if (k < 0) break;
    idx[k]++;
    for (int j = k + 1; j < m; j++) idx[j] = idx[j - 1] + 1;
    if (k == 0) { fprintf(stderr, "progress idx0=%d/%d tested=%lld found=%lld\n", idx[0], nr, tested, found); }
  }
  printf("RESULT f=%d n=%d rank<=%d: %s (independent %d-subsets tested %lld, hits %lld)\n",
         f, n, ns + m, found ? "YES" : "NO", m, tested, found);
  return 0;
}
