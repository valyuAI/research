// Generate the symmetry-reduced LP for optimal k-SNM manipulability of Condorcet-consistent tournament rules.
// usage: gentourng -q n | gen_snm n k mode(eq|le) out_prefix
// Output files: prefix.vars (class orbit sizes, CW info), prefix.ub (rows: nnz idx:coef ... ), all coefficients integer.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

#define MAXN 10
static int n, k, npairs;
static int pa[64], pb[64];
static int pid[MAXN][MAXN];

typedef struct { uint64_t code; int orb[MAXN]; int norb; int osize[MAXN]; int cw; int var0; } Cls;
static Cls *cls; static int ncls = 0, capcls = 0;
// hash map code->class
#define HB 24
static uint64_t *hk; static int *hv;
static void hput(uint64_t c, int v) { uint64_t h = (c * 0x9E3779B97F4A7C15ull) >> (64 - HB); while (hv[h] >= 0) h = (h + 1) & ((1u << HB) - 1); hk[h] = c; hv[h] = v; }
static int hget(uint64_t c) { uint64_t h = (c * 0x9E3779B97F4A7C15ull) >> (64 - HB); while (hv[h] >= 0) { if (hk[h] == c) return hv[h]; h = (h + 1) & ((1u << HB) - 1); } return -1; }

// canonical form: min code over invariant-respecting perms. perm[newlabel] = oldvertex.
static uint64_t best; static int bestperm[MAXN]; static int nbest; static int autos[4096][MAXN]; static int collect;
static int adjg[MAXN][MAXN];
static int order[MAXN], gstart[MAXN + 1], ngroups;
static int cur[MAXN]; static int used[MAXN];

static void rec(int pos) {
  if (pos == n) {
    uint64_t c = 0;
    for (int t = 0; t < npairs; t++) if (adjg[cur[pa[t]]][cur[pb[t]]]) c |= 1ull << t;
    if (c < best) { best = c; memcpy(bestperm, cur, sizeof cur); nbest = 0; if (collect) { memcpy(autos[0], cur, sizeof cur); nbest = 1; } }
    else if (c == best && collect && nbest < 4096) { memcpy(autos[nbest++], cur, sizeof cur); }
    return;
  }
  // group containing pos
  int g = 0; while (!(gstart[g] <= pos && pos < gstart[g + 1])) g++;
  for (int i = gstart[g]; i < gstart[g + 1]; i++) {
    int v = order[i];
    if (used[v]) continue;
    used[v] = 1; cur[pos] = v; rec(pos + 1); used[v] = 0;
  }
}

static uint64_t canon(int adj[MAXN][MAXN], int want_autos) {
  memcpy(adjg, adj, sizeof adjg);
  long key[MAXN];
  int sc[MAXN];
  for (int v = 0; v < n; v++) { sc[v] = 0; for (int w = 0; w < n; w++) sc[v] += adj[v][w]; }
  for (int v = 0; v < n; v++) { long s2 = 0, s3 = 0; for (int w = 0; w < n; w++) if (adj[v][w]) { s2 += sc[w]; } for (int w = 0; w < n; w++) if (adj[v][w]) for (int x = 0; x < n; x++) if (adj[w][x]) s3 += sc[x]; key[v] = (long)sc[v] * 1000000 + s2 * 1000 + s3; }
  for (int i = 0; i < n; i++) order[i] = i;
  for (int i = 0; i < n; i++) for (int j = i + 1; j < n; j++) if (key[order[j]] > key[order[i]]) { int t = order[i]; order[i] = order[j]; order[j] = t; }
  ngroups = 0; gstart[0] = 0;
  for (int i = 1; i <= n; i++) if (i == n || key[order[i]] != key[order[i - 1]]) gstart[++ngroups] = i;
  best = ~0ull; nbest = 0; collect = want_autos;
  memset(used, 0, sizeof used);
  rec(0);
  return best;
}

int main(int argc, char **argv) {
  n = atoi(argv[1]); k = atoi(argv[2]); int le = strcmp(argv[3], "le") == 0; const char *pre = argv[4];
  npairs = 0;
  for (int i = 0; i < n; i++) for (int j = i + 1; j < n; j++) { pa[npairs] = i; pb[npairs] = j; pid[i][j] = npairs; npairs++; }
  hk = malloc(sizeof(uint64_t) << HB); hv = malloc(sizeof(int) << HB); memset(hv, -1, sizeof(int) << HB);
  char line[256]; int adj[MAXN][MAXN];
  capcls = 1 << 20; cls = malloc(sizeof(Cls) * capcls);
  int nvars = 0;
  while (fgets(line, sizeof line, stdin)) {
    int len = strlen(line); while (len && (line[len - 1] == '\n')) line[--len] = 0;
    if (len != npairs) continue;
    memset(adj, 0, sizeof adj);
    for (int t = 0; t < npairs; t++) { if (line[t] == '1') adj[pa[t]][pb[t]] = 1; else adj[pb[t]][pa[t]] = 1; }
    uint64_t c = canon(adj, 0);
    // canonical adjacency
    int cadj[MAXN][MAXN]; memset(cadj, 0, sizeof cadj);
    for (int t = 0; t < npairs; t++) { if (c >> t & 1) cadj[pa[t]][pb[t]] = 1; else cadj[pb[t]][pa[t]] = 1; }
    uint64_t c2 = canon(cadj, 1);
    if (c2 != c) { fprintf(stderr, "canon mismatch\n"); return 1; }
    Cls *C = &cls[ncls];
    C->code = c;
    int par[MAXN]; for (int v = 0; v < n; v++) par[v] = v;
    for (int a = 0; a < nbest; a++) for (int v = 0; v < n; v++) {
      int x = v, y = autos[a][v]; while (par[x] != x) x = par[x]; while (par[y] != y) y = par[y];
      if (x != y) { if (x < y) par[y] = x; else par[x] = y; }
    }
    int rid[MAXN]; for (int v = 0; v < n; v++) rid[v] = -1;
    C->norb = 0;
    for (int v = 0; v < n; v++) { int x = v; while (par[x] != x) x = par[x]; if (rid[x] < 0) { rid[x] = C->norb; C->osize[C->norb] = 0; C->norb++; } C->orb[v] = rid[x]; C->osize[rid[x]]++; }
    C->cw = -1;
    for (int v = 0; v < n; v++) { int s = 0; for (int w = 0; w < n; w++) s += cadj[v][w]; if (s == n - 1) C->cw = C->orb[v]; }
    C->var0 = nvars; nvars += C->norb;
    hput(c, ncls);
    ncls++;
  }
  fprintf(stderr, "n=%d: %d classes, %d rule variables\n", n, ncls, nvars);
  char fn[512];
  snprintf(fn, sizeof fn, "%s.vars", pre);
  FILE *fv = fopen(fn, "w");
  fprintf(fv, "%d %d\n", ncls, nvars);
  for (int i = 0; i < ncls; i++) {
    fprintf(fv, "%llu %d %d", (unsigned long long)cls[i].code, cls[i].norb, cls[i].cw);
    for (int o = 0; o < cls[i].norb; o++) fprintf(fv, " %d", cls[i].osize[o]);
    fprintf(fv, "\n");
  }
  fclose(fv);
  snprintf(fn, sizeof fn, "%s.ub", pre);
  FILE *fu = fopen(fn, "w");
  snprintf(fn, sizeof fn, "%s.meta", pre);
  FILE *fm = fopen(fn, "w");
  long long nrows = 0;
  int alpha = nvars;
  for (int ci = 0; ci < ncls; ci++) {
    Cls *C = &cls[ci];
    int cadj[MAXN][MAXN]; memset(cadj, 0, sizeof cadj);
    for (int t = 0; t < npairs; t++) { if (C->code >> t & 1) cadj[pa[t]][pb[t]] = 1; else cadj[pb[t]][pa[t]] = 1; }
    for (int sz = le ? 2 : k; sz <= k; sz++) {
      // enumerate subsets S of size sz
      int S[MAXN];
      for (int mask = 0; mask < (1 << n); mask++) {
        if (__builtin_popcount(mask) != sz) continue;
        int m = 0; for (int v = 0; v < n; v++) if (mask >> v & 1) S[m++] = v;
        int inner[64][2], ni = 0;
        for (int a = 0; a < m; a++) for (int b = a + 1; b < m; b++) { inner[ni][0] = S[a]; inner[ni][1] = S[b]; ni++; }
        for (int bits = 0; bits < (1 << ni); bits++) {
          int adj2[MAXN][MAXN]; memcpy(adj2, cadj, sizeof adj2);
          int changed = 0;
          for (int t = 0; t < ni; t++) {
            int a = inner[t][0], b = inner[t][1], want = bits >> t & 1;
            if (adj2[a][b] != want) changed = 1;
            adj2[a][b] = want; adj2[b][a] = !want;
          }
          if (!changed) continue;
          uint64_t c2 = canon(adj2, 0);
          int cj = hget(c2);
          if (cj < 0) { fprintf(stderr, "class not found\n"); return 1; }
          int inv[MAXN]; for (int a = 0; a < n; a++) inv[bestperm[a]] = a;
          // row: sum_{v in S} x[cj][orb(inv v)] - x[ci][orb v] - alpha <= 0
          int idx[32], coef[32], nz = 0;
          for (int t = 0; t < m; t++) {
            int v = S[t];
            int i1 = cls[cj].var0 + cls[cj].orb[inv[v]], i2 = C->var0 + C->orb[v];
            int f;
            f = 0; for (int q = 0; q < nz; q++) if (idx[q] == i1) { coef[q] += 1; f = 1; } if (!f) { idx[nz] = i1; coef[nz] = 1; nz++; }
            f = 0; for (int q = 0; q < nz; q++) if (idx[q] == i2) { coef[q] -= 1; f = 1; } if (!f) { idx[nz] = i2; coef[nz] = -1; nz++; }
          }
          int out = 0; for (int q = 0; q < nz; q++) if (coef[q] != 0) out++;
          if (out == 0) continue;
          fprintf(fu, "%d", out + 1);
          for (int q = 0; q < nz; q++) if (coef[q] != 0) fprintf(fu, " %d:%d", idx[q], coef[q]);
          fprintf(fu, " %d:-1\n", alpha);
          fprintf(fm, "%d %d %d\n", ci, mask, bits);
          nrows++;
        }
      }
    }
  }
  if (argc > 5 && strcmp(argv[5], "pairs") == 0) {
    snprintf(fn, sizeof fn, "%s.pairs", pre);
    FILE *fo = fopen(fn, "w");
    for (int ci = 0; ci < ncls; ci++) {
      Cls *C = &cls[ci];
      int cadj[MAXN][MAXN]; memset(cadj, 0, sizeof cadj);
      for (int t = 0; t < npairs; t++) { if (C->code >> t & 1) cadj[pa[t]][pb[t]] = 1; else cadj[pb[t]][pa[t]] = 1; }
      for (int i = 0; i < n; i++) for (int j = 0; j < n; j++) {
        if (i == j || !cadj[i][j]) continue;
        int adj2[MAXN][MAXN]; memcpy(adj2, cadj, sizeof adj2);
        adj2[i][j] = 0; adj2[j][i] = 1;
        uint64_t c2 = canon(adj2, 0);
        int cj = hget(c2);
        int inv[MAXN]; for (int a = 0; a < n; a++) inv[bestperm[a]] = a;
        fprintf(fo, "%d %d %d %d\n", C->var0 + C->orb[i], C->var0 + C->orb[j], cls[cj].var0 + cls[cj].orb[inv[i]], cls[cj].var0 + cls[cj].orb[inv[j]]);
      }
    }
    fclose(fo);
  }
  if (argc > 5 && (strcmp(argv[5], "mono") == 0 || strcmp(argv[5], "pairs") == 0)) {
    snprintf(fn, sizeof fn, "%s.mono", pre);
    FILE *fo = fopen(fn, "w");
    long long nm = 0;
    for (int ci = 0; ci < ncls; ci++) {
      Cls *C = &cls[ci];
      int cadj[MAXN][MAXN]; memset(cadj, 0, sizeof cadj);
      for (int t = 0; t < npairs; t++) { if (C->code >> t & 1) cadj[pa[t]][pb[t]] = 1; else cadj[pb[t]][pa[t]] = 1; }
      for (int i = 0; i < n; i++) for (int j = 0; j < n; j++) {
        if (i == j || !cadj[j][i]) continue;
        int adj2[MAXN][MAXN]; memcpy(adj2, cadj, sizeof adj2);
        adj2[i][j] = 1; adj2[j][i] = 0;
        uint64_t c2 = canon(adj2, 0);
        int cj = hget(c2);
        int inv[MAXN]; for (int a = 0; a < n; a++) inv[bestperm[a]] = a;
        int i1 = C->var0 + C->orb[i], i2 = cls[cj].var0 + cls[cj].orb[inv[i]];
        if (i1 == i2) continue;
        fprintf(fo, "2 %d:1 %d:-1\n", i1, i2);
        nm++;
      }
    }
    fclose(fo);
    fprintf(stderr, "%lld monotonicity rows\n", nm);
  }
  fclose(fu); fclose(fm);
  fprintf(stderr, "%lld rows written\n", nrows);
  return 0;
}
