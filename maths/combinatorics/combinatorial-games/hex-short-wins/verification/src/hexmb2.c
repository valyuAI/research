// hexmb2.c - exact search for Campbell's Hex parameters delta(n) and lambda(n),
// with dead-cell normalisation and must-play pruning via null-move supports.
//
// Board: n x n Hex rhombus, cell (r,c) has index r*n+c. Blue (first player)
// connects row 0 to row n-1. Neighbours of (r,c): (r,c-1),(r,c+1),(r-1,c),
// (r-1,c+1),(r+1,c-1),(r+1,c).
//
// Mode D (delta): Blue wins iff Blue completes a top-bottom connection using
//   at most d Blue stones in total.
// Mode L (lambda): Blue wins iff Blue's stones at some point contain a
//   top-bottom path of at most l cells (no limit on the number of moves).
//
// Support lemma (used for pruning): if Maker wins position P (Maker to move)
// and S is a support of that win, then Maker also wins P plus any extra Red
// stones placed outside S.  Hence at a Breaker node Q, if Maker wins the
// null-move position (Breaker passes) with support S, every Breaker move
// outside S loses and only moves inside S need to be examined.
//
// usage: hexmb2 n D|L bound [first-move-index ...]
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#define MAXC 64
#define MAXL 32
#define INF 100

typedef uint64_t u64;

static int n, NC, L, MODE, DLIM;
static u64 nbr[MAXC];
static u64 TOP, BOT, ALL;
static long long nodes;
static int ttbits = 23;

typedef struct {
  u64 b, e;    // relevant blue cells, relevant empty cells (canonical)
  u64 sup;     // support of a Maker win (canonical frame)
  u64 info;    // bit 0 valid, bit 1 value, bit 2 maker-to-move, bits 8.. m
} tte;
static tte *TT;
static u64 TTMASK;

static inline u64 rot(u64 x) { return __builtin_bitreverse64(x) >> (64 - NC); }

static inline u64 hash3(u64 a, u64 b, u64 c) {
  u64 h = a * 0x9E3779B97F4A7C15ULL;
  h ^= (b + 0x632BE59BD9B4E019ULL) * 0xC2B2AE3D27D4EB4FULL;
  h ^= (c + 0x1234567ULL) * 0x94D049BB133111EBULL;
  h ^= h >> 29;
  h *= 0xBF58476D1CE4E5B9ULL;
  h ^= h >> 32;
  return h;
}

// lookup; returns -1 if absent, else value, and sets *sup (in the caller frame)
static int ttget(u64 b, u64 e, int maker, int m, u64 *sup) {
  int flip = 0;
  u64 b2 = rot(b), e2 = rot(e);
  if (b2 < b || (b2 == b && e2 < e)) {
    b = b2;
    e = e2;
    flip = 1;
  }
  u64 info = 1 | ((u64)maker << 2) | ((u64)m << 8);
  tte *t = &TT[hash3(b, e, info) & TTMASK];
  if (t->b == b && t->e == e && (t->info & ~2ULL) == info) {
    if (sup) *sup = flip ? rot(t->sup) : t->sup;
    return (t->info >> 1) & 1;
  }
  return -1;
}

static void ttput(u64 b, u64 e, int maker, int m, int v, u64 sup) {
  u64 b2 = rot(b), e2 = rot(e);
  if (b2 < b || (b2 == b && e2 < e)) {
    b = b2;
    e = e2;
    sup = rot(sup);
  }
  u64 info = 1 | ((u64)maker << 2) | ((u64)m << 8);
  tte *t = &TT[hash3(b, e, info) & TTMASK];
  t->b = b;
  t->e = e;
  t->sup = sup;
  t->info = info | ((u64)v << 1);
}

// F[v][k]: min empties on a walk of at most k cells from start-row to v avoiding red
static void dp(u64 blue, u64 red, unsigned char F[MAXC][MAXL + 1], u64 start) {
  unsigned char cur[MAXC], nxt[MAXC];
  for (int v = 0; v < NC; v++) {
    int e = ((blue >> v) & 1) ? 0 : 1;
    cur[v] = ((red >> v) & 1) ? INF : (((start >> v) & 1) ? e : INF);
    F[v][1] = cur[v];
  }
  for (int k = 2; k <= L; k++) {
    for (int v = 0; v < NC; v++) {
      if ((red >> v) & 1) {
        nxt[v] = INF;
        F[v][k] = INF;
        continue;
      }
      int e = ((blue >> v) & 1) ? 0 : 1;
      int best = cur[v];
      u64 nb = nbr[v];
      while (nb) {
        int u = __builtin_ctzll(nb);
        nb &= nb - 1;
        int c = cur[u] + e;
        if (c < best) best = c;
      }
      nxt[v] = best > INF ? INF : best;
      F[v][k] = nxt[v];
    }
    memcpy(cur, nxt, NC);
  }
}

static int scores(u64 blue, u64 red, int *score) {
  unsigned char F[MAXC][MAXL + 1], G[MAXC][MAXL + 1];
  dp(blue, red, F, TOP);
  dp(blue, red, G, BOT);
  int best = INF;
  for (int v = 0; v < NC; v++) {
    if ((red >> v) & 1) {
      score[v] = INF;
      continue;
    }
    int e = ((blue >> v) & 1) ? 0 : 1;
    int s = INF;
    for (int k = 1; k <= L; k++) {
      int a = F[v][k], b = G[v][L + 1 - k];
      if (a >= INF || b >= INF) continue;
      int t = a + b - e;
      if (t < s) s = t;
    }
    score[v] = s;
    if (s < best) best = s;
  }
  return best;
}

static int cdist[MAXC];

static void sortmoves(int *mv, int *key, int cnt) {
  for (int i = 1; i < cnt; i++) {
    int a = mv[i], k = key[i], j = i - 1;
    while (j >= 0 && key[j] > k) {
      mv[j + 1] = mv[j];
      key[j + 1] = key[j];
      j--;
    }
    mv[j + 1] = a;
    key[j + 1] = k;
  }
}

// solve: returns 1 iff Maker (Blue) wins. maker = 1 if Blue to move.
// m = number of Blue stones still allowed (mode D) or 64 (mode L).
// On a Maker win, *sup receives a support (set of empty cells).
static int solve(u64 blue, u64 red, int maker, int m, u64 *sup) {
  nodes++;
  int score[MAXC];
  int best = scores(blue, red, score);
  if (best > m) return 0;
  u64 rel = 0;
  for (int v = 0; v < NC; v++)
    if (score[v] <= m) rel |= 1ULL << v;
  u64 empty = ALL & ~blue & ~red;
  u64 rb = blue & rel, re = empty & rel;
  if (maker && best == 1) {
    for (int v = 0; v < NC; v++)
      if (((re >> v) & 1) && score[v] == 1) {
        *sup = 1ULL << v;
        return 1;
      }
  }
  u64 tsup;
  int t = ttget(rb, re, maker, m, &tsup);
  if (t >= 0) {
    if (t) *sup = tsup;
    return t;
  }
  // normalised position: everything outside rel is red
  u64 nred = ALL & ~rel;
  u64 nblue = rb;
  int mv[MAXC], key[MAXC], cnt = 0;
  if (maker) {
    for (int v = 0; v < NC; v++)
      if ((re >> v) & 1) {
        mv[cnt] = v;
        key[cnt++] = score[v] * 64 + cdist[v];
      }
    sortmoves(mv, key, cnt);
    for (int i = 0; i < cnt; i++) {
      u64 s;
      if (solve(nblue | (1ULL << mv[i]), nred, 0, m - 1, &s)) {
        s |= 1ULL << mv[i];
        s &= re;
        ttput(rb, re, 1, m, 1, s);
        *sup = s;
        return 1;
      }
    }
    ttput(rb, re, 1, m, 0, 0);
    return 0;
  }
  // Breaker to move
  int thr = 0;
  u64 tmask = 0;
  if (m >= 1)
    for (int v = 0; v < NC; v++)
      if (((re >> v) & 1) && score[v] == 1) {
        thr++;
        tmask |= 1ULL << v;
      }
  if (thr >= 2) {
    // two disjoint completions: support = two of them
    u64 s = tmask & -tmask;
    u64 r2 = tmask & ~s;
    s |= r2 & -r2;
    ttput(rb, re, 0, m, 1, s);
    *sup = s;
    return 1;
  }
  u64 cand, total;
  if (thr == 1) {
    cand = tmask;
    total = tmask;
  } else {
    // null move: Maker to move in the same position
    u64 ps;
    if (!solve(nblue, nred, 1, m, &ps)) {
      ttput(rb, re, 0, m, 0, 0);
      return 0;
    }
    cand = ps & re;
    total = ps;
  }
  cnt = 0;
  for (int v = 0; v < NC; v++)
    if ((cand >> v) & 1) {
      mv[cnt] = v;
      key[cnt++] = score[v] * 64 + cdist[v];
    }
  sortmoves(mv, key, cnt);
  for (int i = 0; i < cnt; i++) {
    u64 s;
    if (!solve(nblue, nred | (1ULL << mv[i]), 1, m, &s)) {
      ttput(rb, re, 0, m, 0, 0);
      return 0;
    }
    total |= s;
  }
  total &= re;
  ttput(rb, re, 0, m, 1, total);
  *sup = total;
  return 1;
}

int main(int argc, char **argv) {
  if (argc < 4) {
    fprintf(stderr, "usage: %s n D|L bound [first moves]\n", argv[0]);
    return 1;
  }
  n = atoi(argv[1]);
  MODE = argv[2][0];
  int bound = atoi(argv[3]);
  if (getenv("TTBITS")) ttbits = atoi(getenv("TTBITS"));
  NC = n * n;
  L = bound;
  if (MODE == 'D') DLIM = bound;
  if (L > MAXL) L = MAXL;
  ALL = (NC == 64) ? ~0ULL : ((1ULL << NC) - 1);
  for (int r = 0; r < n; r++)
    for (int c = 0; c < n; c++) {
      int v = r * n + c;
      u64 msk = 0;
      int dr[6] = {0, 0, -1, -1, 1, 1}, dc[6] = {-1, 1, 0, 1, -1, 0};
      for (int k = 0; k < 6; k++) {
        int rr = r + dr[k], c2 = c + dc[k];
        if (rr >= 0 && rr < n && c2 >= 0 && c2 < n) msk |= 1ULL << (rr * n + c2);
      }
      nbr[v] = msk;
      if (r == 0) TOP |= 1ULL << v;
      if (r == n - 1) BOT |= 1ULL << v;
      int dR = 2 * r - (n - 1), dC = 2 * c - (n - 1), dS = -(dR + dC);
      int a = abs(dR), b = abs(dC), cc = abs(dS);
      int mx = a > b ? a : b;
      cdist[v] = mx > cc ? mx : cc;
    }
  TT = calloc((size_t)1 << ttbits, sizeof(tte));
  TTMASK = ((u64)1 << ttbits) - 1;
  int firsts[MAXC], nf = 0;
  if (argc > 4) {
    for (int i = 4; i < argc; i++) firsts[nf++] = atoi(argv[i]);
  } else {
    for (int v = 0; v < NC; v++)
      if (v <= NC - 1 - v) firsts[nf++] = v;
  }
  int any = 0;
  int m0 = (MODE == 'D') ? DLIM : 64;
  for (int i = 0; i < nf; i++) {
    int v = firsts[i];
    clock_t t0 = clock();
    long long n0 = nodes;
    u64 b = 1ULL << v, s = 0;
    int score[MAXC];
    int best = scores(b, 0, score);
    int res = (best == 0) ? 1 : solve(b, 0, 0, m0 - 1, &s);
    any |= res;
    printf("n=%d mode=%c bound=%d first=(%d,%d) result=%s nodes=%lld time=%.2fs\n", n, MODE, bound,
           v / n + 1, v % n + 1, res ? "BLUE" : "RED", nodes - n0,
           (double)(clock() - t0) / CLOCKS_PER_SEC);
    fflush(stdout);
  }
  printf("SUMMARY n=%d mode=%c bound=%d blue_wins=%d\n", n, MODE, bound, any);
  return 0;
}
