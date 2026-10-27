// Verification pipeline for: tau(w) is l+-CT-square-free for every infinite 7/4+-free ternary word w.
// Usage: ctproof s l q img_a img_b img_c   (images as digit strings over 0..s-1)
// Steps: (a) injective + synchronizing; (b) minimal local decoding radius r;
// (c) M = 4(2r+2q-2): no CT-square with half-length in [l, M] in tau(f), f 7/4+-free of every length 1..K.
// The theorem (Proposition 3.1 of the paper) is for infinite w and needs only length K.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
static int s, L, q; static int img[3][64];
// ---- enumerate 7/4+-free ternary words of length K (callback) ----
static int wbuf[256];
static int ok_ext(int n){ // check suffixes of wbuf[0..n)
  for (int p = 1; p < n; p++){ int Lr = p; while (Lr < n && wbuf[n-1-Lr] == wbuf[n-1-Lr+p]) Lr++; if (4*Lr > 7*p) return 0; }
  return 1;
}
typedef void (*cb_t)(int *w, int n);
static int ALL = 1; // also visit every shorter length 1..K-1
static void enum_words(int n, int K, cb_t cb){
  if (n == K){ cb(wbuf, K); return; }
  if (ALL && n >= 1) cb(wbuf, n);
  for (int c = 0; c < 3; c++){ wbuf[n] = c; if (ok_ext(n+1)) enum_words(n+1, K, cb); }
}
// ---- psv ----
static void psv_of(const int *x, int n, int *out){ // psv relative to start
  int g[4096];
  for (int i = 0; i < n; i++){ int j = i-1; while (j >= 0 && x[j] > x[i]) j = g[j]; g[i] = j; out[i] = j >= 0 ? i - j : 0; }
}
// ---- (b) local decoding: store factors of length W with their psv; check middle letter determined ----
#define MAXF 2000000
static int W, R; static int nf; static unsigned char *facs; // each factor W letters
static void add_factors(int *w, int K){
  int x[4096], n = 0; for (int i = 0; i < K; i++) for (int t = 0; t < q; t++) x[n++] = img[w[i]][t];
  for (int p = 0; p + W <= n; p++){ if (nf >= MAXF) { fprintf(stderr, "MAXF\n"); exit(3);} for (int t = 0; t < W; t++) facs[(size_t)nf*W + t] = x[p+t]; nf++; }
}
static int cmp_fac(const void *a, const void *b){ return memcmp(a, b, W); }
static int check_decoding(void){
  // dedupe factors, compute psv keys, sort by key, check middle letter constant within key
  qsort(facs, nf, W, cmp_fac);
  int u = 0; for (int i = 0; i < nf; i++){ if (u == 0 || memcmp(facs + (size_t)i*W, facs + (size_t)(u-1)*W, W)) { memmove(facs + (size_t)u*W, facs + (size_t)i*W, W); u++; } }
  nf = u;
  // key = psv sequence
  unsigned char *keys = malloc((size_t)nf * (W + 1));
  for (int i = 0; i < nf; i++){ int x[256], ps[256]; for (int t=0;t<W;t++) x[t]=facs[(size_t)i*W+t]; psv_of(x, W, ps);
    for (int t=0;t<W;t++) keys[(size_t)i*(W+1)+t] = (unsigned char)ps[t]; keys[(size_t)i*(W+1)+W] = x[R]; }
  W = W + 1; qsort(keys, nf, W, cmp_fac); W = W - 1;
  int ok = 1;
  for (int i = 1; i < nf; i++) if (!memcmp(keys + (size_t)i*(W+1), keys + (size_t)(i-1)*(W+1), W) && keys[(size_t)i*(W+1)+W] != keys[(size_t)(i-1)*(W+1)+W]) { ok = 0; break; }
  free(keys);
  return ok;
}
// ---- (c) small squares ----
static int M; static long long nchecked; static int bad;
static void check_small(int *w, int K){
  int x[4096], n = 0; for (int i = 0; i < K; i++) for (int t = 0; t < q; t++) x[n++] = img[w[i]][t];
  int g[4096]; for (int i = 0; i < n; i++){ int j = i-1; while (j >= 0 && x[j] > x[i]) j = g[j]; g[i] = j; }
  for (int m = L; m <= M && 2*m <= n; m++)
    for (int p = 0; p + 2*m <= n; p++){
      int t; for (t = 0; t < m; t++){ int a = g[p+t] >= p ? t - (g[p+t]-p) : 0; int b = g[p+m+t] >= p+m ? t - (g[p+m+t]-p-m) : 0; if (a != b) break; }
      if (t == m){ if (!bad){ printf("CT-SQUARE m=%d at %d in tau(", m, p); for (int i=0;i<K;i++) putchar('a'+w[i]); printf(")\n"); } bad = 1; return; }
    }
  nchecked++;
}
int main(int argc, char **argv){
  s = atoi(argv[1]); L = atoi(argv[2]); q = atoi(argv[3]);
  for (int a = 0; a < 3; a++){ if ((int)strlen(argv[4+a]) != q){ fprintf(stderr, "bad length\n"); return 1; } for (int t = 0; t < q; t++) img[a][t] = argv[4+a][t]-'0'; }
  // (a)
  int inj = memcmp(img[0], img[1], sizeof img[0]) && memcmp(img[0], img[2], sizeof img[0]) && memcmp(img[1], img[2], sizeof img[0]);
  int sync = 1;
  for (int a=0;a<3;a++) for (int b=0;b<3;b++) for (int c=0;c<3;c++) for (int off=1; off<q; off++){
    int eq=1; for (int t=0;t<q;t++){ int pos=off+t; int ch = pos<q? img[a][pos] : img[b][pos-q]; if (ch!=img[c][t]){eq=0;break;} } if (eq) sync = 0; }
  printf("injective=%d synchronizing=%d\n", inj, sync); if (!inj || !sync) return 1;
  // (b)
  facs = malloc((size_t)MAXF * 64);
  for (R = 0; R <= 25; R++){
    W = 2*R + 1; nf = 0; int K = (W - 1 + q - 1)/q + 1; // ceil((W-1)/q)+1
    enum_words(0, K, add_factors);
    int ok = check_decoding();
    printf("radius r=%d (window %d, base length %d, distinct factors %d): %s\n", R, W, K, nf, ok ? "DECODES" : "ambiguous"); fflush(stdout);
    if (ok) break;
  }
  if (R > 25){ printf("no decoding radius <= 25\n"); return 2; }
  // (c)
  M = 4*(2*R + 2*q - 2);
  int K = (2*M - 1 + q - 1)/q + 1;
  printf("M=%d, checking all 7/4+-free ternary f of length 1..K=%d for CT-squares with half-length in [%d,%d]\n", M, K, L, M); fflush(stdout);
  bad = 0; nchecked = 0; enum_words(0, K, check_small);
  printf("checked %lld words: %s\n", nchecked, bad ? "FAIL" : "no CT-square found");
  if (!bad) printf("THEOREM VERIFIED: tau(w) is %d+-CT-square-free for every infinite 7/4+-free ternary word w (q=%d, r=%d, M=%d; source lengths 1..K also checked)\n", L, q, R, M);
  return bad;
}
