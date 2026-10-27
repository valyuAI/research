// hexmb.c - exact search for Campbell's Hex parameters delta(n) and lambda(n).
//
// Board: n x n Hex rhombus, cell (r,c) has index r*n+c. Blue (first player)
// connects row 0 to row n-1. Neighbours of (r,c): (r,c-1),(r,c+1),(r-1,c),
// (r-1,c+1),(r+1,c-1),(r+1,c).
//
// Mode D (delta): Blue wins iff after at most d Blue stones the Blue stones
//   contain a top-bottom connection.  Blue moves first.
// Mode L (lambda): Blue wins iff at some point the Blue stones contain a
//   top-bottom path with at most l cells (no limit on the number of moves).
//
// Both are Maker-Breaker games (Red connecting left-right only matters because
// it destroys every Blue path, which the search sees directly).
//
// usage: hexmb n D|L bound [first-move-index ...]
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#define MAXN 8
#define MAXC 64
#define MAXL 24
#define INF 100

typedef uint64_t u64;

static int n, NC, L, MODE, DLIM;  // DLIM: max Blue stones in mode D
static u64 nbr[MAXC];
static u64 TOP, BOT, ALL;
static long long nodes;

// ---------------- transposition table ----------------
#define TTBITS 24
#define TTSIZE (1u << TTBITS)
typedef struct {
  u64 b, r;  // r has bit 63 = valid, bit 62 = value
} tte;
static tte *TT;

static u64 rot(u64 x) {
  // 180 degree rotation: index i -> NC-1-i
  u64 y = __builtin_bitreverse64(x);
  return y >> (64 - NC);
}

static inline u64 hash2(u64 a, u64 b) {
  u64 h = a * 0x9E3779B97F4A7C15ULL ^ (b + 0x632BE59BD9B4E019ULL) * 0xC2B2AE3D27D4EB4FULL;
  h ^= h >> 29;
  h *= 0xBF58476D1CE4E5B9ULL;
  h ^= h >> 32;
  return h;
}

static void canon(u64 *b, u64 *r) {
  u64 b2 = rot(*b), r2 = rot(*r);
  if (b2 < *b || (b2 == *b && r2 < *r)) {
    *b = b2;
    *r = r2;
  }
}

static int ttget(u64 b, u64 r) {
  canon(&b, &r);
  tte *e = &TT[hash2(b, r) & (TTSIZE - 1)];
  if ((e->r >> 63) && e->b == b && (e->r & ((1ULL << 62) - 1)) == r) return (e->r >> 62) & 1;
  return -1;
}

static void ttput(u64 b, u64 r, int v) {
  canon(&b, &r);
  tte *e = &TT[hash2(b, r) & (TTSIZE - 1)];
  e->b = b;
  e->r = r | (1ULL << 63) | ((u64)v << 62);
}

// ---------------- path dynamic programme ----------------
// F[v][k] = min number of empty cells on a walk of at most k cells from the
// top row to v avoiding red; G likewise from the bottom row.
static void dp(u64 blue, u64 red, unsigned char F[MAXC][MAXL + 1], u64 start) {
  unsigned char cur[MAXC], nxt[MAXC];
  for (int v = 0; v < NC; v++) {
    int e = (blue >> v) & 1 ? 0 : 1;
    if ((red >> v) & 1)
      cur[v] = INF;
    else
      cur[v] = ((start >> v) & 1) ? e : INF;
    F[v][1] = cur[v];
  }
  for (int k = 2; k <= L; k++) {
    for (int v = 0; v < NC; v++) {
      if ((red >> v) & 1) {
        nxt[v] = INF;
        F[v][k] = INF;
        continue;
      }
      int e = (blue >> v) & 1 ? 0 : 1;
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

// score[v] = min empties over walks with <= L cells through v (INF if none)
static int scores(u64 blue, u64 red, int *score) {
  static unsigned char F[MAXC][MAXL + 1], G[MAXC][MAXL + 1];
  dp(blue, red, F, TOP);
  dp(blue, red, G, BOT);
  int best = INF;
  for (int v = 0; v < NC; v++) {
    if ((red >> v) & 1) {
      score[v] = INF;
      continue;
    }
    int e = (blue >> v) & 1 ? 0 : 1;
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
  return best;  // min empties of a completable path (INF if none)
}

static int centre_dist(int v) {
  int r = v / n, c = v % n;
  // hex distance from board centre (doubled to avoid fractions)
  int dr = 2 * r - (n - 1), dc = 2 * c - (n - 1);
  int ds = -(dr + dc);
  int a = abs(dr), b = abs(dc), cc = abs(ds);
  int m = a > b ? a : b;
  return m > cc ? m : cc;
}

// Returns 1 iff Blue (Maker) wins from this position with the side to move
// determined by stone counts.  Precondition: Blue has not already won.
static int solve(u64 blue, u64 red) {
  nodes++;
  int nb = __builtin_popcountll(blue), nr = __builtin_popcountll(red);
  int maker = (nb == nr);
  int m = (MODE == 'D') ? DLIM - nb : 64;  // Blue stones still available
  int score[MAXC];
  int best = scores(blue, red, score);
  if (best > m) return 0;
  if (maker && best == 1) return 1;
  int t = ttget(blue, red);
  if (t >= 0) return t;

  int mv[MAXC], key[MAXC], cnt = 0;
  u64 empty = ALL & ~blue & ~red;
  if (!maker) {
    // threats: empty cells completing a path at once
    int thr = 0, tv = -1;
    if (m >= 1)
      for (int v = 0; v < NC; v++)
        if (((empty >> v) & 1) && score[v] == 1) {
          thr++;
          tv = v;
        }
    if (thr >= 2) {
      ttput(blue, red, 1);
      return 1;
    }
    if (thr == 1) {
      mv[cnt] = tv;
      key[cnt++] = 0;
    }
  }
  if (cnt == 0) {
    for (int v = 0; v < NC; v++)
      if (((empty >> v) & 1) && score[v] <= m) {
        mv[cnt] = v;
        key[cnt++] = score[v] * 64 + centre_dist(v);
      }
  }
  // insertion sort by key
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
  int res;
  if (maker) {
    res = 0;
    for (int i = 0; i < cnt && !res; i++) {
      u64 b2 = blue | (1ULL << mv[i]);
      if (solve(b2, red)) res = 1;
    }
  } else {
    res = 1;
    for (int i = 0; i < cnt && res; i++) {
      u64 r2 = red | (1ULL << mv[i]);
      if (!solve(blue, r2)) res = 0;
    }
  }
  ttput(blue, red, res);
  return res;
}

int main(int argc, char **argv) {
  if (argc < 4) {
    fprintf(stderr, "usage: %s n D|L bound [first moves]\n", argv[0]);
    return 1;
  }
  n = atoi(argv[1]);
  MODE = argv[2][0];
  int bound = atoi(argv[3]);
  NC = n * n;
  if (MODE == 'D') {
    DLIM = bound;
    L = bound;  // a connection with <= d stones contains a path of <= d cells
  } else {
    L = bound;
  }
  if (L > MAXL) L = MAXL;
  ALL = (NC == 64) ? ~0ULL : ((1ULL << NC) - 1);
  TOP = BOT = 0;
  for (int r = 0; r < n; r++)
    for (int c = 0; c < n; c++) {
      int v = r * n + c;
      u64 m = 0;
      int dr[6] = {0, 0, -1, -1, 1, 1}, dc[6] = {-1, 1, 0, 1, -1, 0};
      for (int k = 0; k < 6; k++) {
        int rr = r + dr[k], c2 = c + dc[k];
        if (rr >= 0 && rr < n && c2 >= 0 && c2 < n) m |= 1ULL << (rr * n + c2);
      }
      nbr[v] = m;
      if (r == 0) TOP |= 1ULL << v;
      if (r == n - 1) BOT |= 1ULL << v;
    }
  TT = calloc(TTSIZE, sizeof(tte));
  int firsts[MAXC], nf = 0;
  if (argc > 4) {
    for (int i = 4; i < argc; i++) firsts[nf++] = atoi(argv[i]);
  } else {
    for (int v = 0; v < NC; v++)
      if (v <= NC - 1 - v) firsts[nf++] = v;
  }
  int any = 0;
  for (int i = 0; i < nf; i++) {
    int v = firsts[i];
    clock_t t0 = clock();
    long long n0 = nodes;
    u64 b = 1ULL << v;
    int score[MAXC];
    int best = scores(b, 0, score);
    int res;
    if (best == 0)
      res = 1;
    else
      res = solve(b, 0);
    any |= res;
    printf("n=%d mode=%c bound=%d first=(%d,%d) result=%s nodes=%lld time=%.2fs\n", n, MODE, bound,
           v / n + 1, v % n + 1, res ? "BLUE" : "RED", nodes - n0, (double)(clock() - t0) / CLOCKS_PER_SEC);
    fflush(stdout);
  }
  printf("SUMMARY n=%d mode=%c bound=%d blue_wins=%d\n", n, MODE, bound, any);
  return 0;
}
