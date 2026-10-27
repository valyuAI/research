// hexmb3.c - exact Maker-Breaker search for Campbell's Hex parameters, using the
// explicit family of minimal winning paths.
//
// Board: n x n Hex rhombus, cell (r,c) has index r*n+c. Blue (first player,
// Maker) connects row 0 to row n-1. Neighbours of (r,c): (r,c-1),(r,c+1),
// (r-1,c),(r-1,c+1),(r+1,c-1),(r+1,c).
//
// Winning sets: minimal top-bottom connections with at most L cells (these are
// exactly the interiors of induced paths between the two virtual edge nodes).
// Mode D (delta, bound d): L = d and Blue may place at most d stones in total.
// Mode L (lambda, bound l): L = l and Blue may place any number of stones.
//
// Pruning rules (each is a sound restriction for Maker-Breaker games):
//  * dead cells: a cell on no live winning set is irrelevant to both players;
//    positions are normalised by treating dead cells as Red.
//  * immediate threats: Breaker must answer a set with one empty cell; two
//    distinct such cells win for Maker.
//  * double-threat must-play: if Maker, moving twice, could play v and obtain
//    two or more distinct completion cells T_v, Breaker must play in
//    {v} u T_v when |T_v| = 2, and at v when |T_v| >= 3.
//  * Breaker domination: if every live set through x also passes through y,
//    Breaker never needs to play x (y kills a superset of sets).
//
// usage: hexmb3 n D|L bound [first-move-index ...]
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#define MAXC 64
#define MAXE 20000
#define EW ((MAXE + 63) / 64)

typedef uint64_t u64;

static int n, NC, L, MODE, DLIM;
static u64 nbr[MAXC];
static u64 ALL;
static u64 edges[MAXE];
static int NE;
static long long nodes;
static int ttbits = 23;
static int use_dom = 1, use_dt = 1;
#define MDEC(m) (MODE == 'D' ? (m) - 1 : (m))

// ---------------- winning-set enumeration ----------------
static void rec_paths(int *path, int len, u64 mask) {
  int v = path[len - 1];
  if (v / n == n - 1) {
    if (NE >= MAXE) {
      fprintf(stderr, "too many edges\n");
      exit(1);
    }
    edges[NE++] = mask;
    return;
  }
  if (len == L) return;
  u64 nb = nbr[v];
  while (nb) {
    int u = __builtin_ctzll(nb);
    nb &= nb - 1;
    if ((mask >> u) & 1) continue;
    if (u / n == 0) continue;
    if (nbr[u] & mask & ~(1ULL << v)) continue;  // chord
    path[len] = u;
    rec_paths(path, len + 1, mask | (1ULL << u));
  }
}

// ---------------- transposition table ----------------
typedef struct {
  u64 b, e, info;
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

static inline void canon(u64 *b, u64 *e) {
  u64 b2 = rot(*b), e2 = rot(*e);
  if (b2 < *b || (b2 == *b && e2 < *e)) {
    *b = b2;
    *e = e2;
  }
}

static int ttget(u64 b, u64 e, int maker, int m) {
  canon(&b, &e);
  u64 info = 1 | ((u64)maker << 2) | ((u64)m << 8);
  tte *t = &TT[hash3(b, e, info) & TTMASK];
  if (t->b == b && t->e == e && (t->info & ~2ULL) == info) return (t->info >> 1) & 1;
  return -1;
}

static void ttput(u64 b, u64 e, int maker, int m, int v) {
  canon(&b, &e);
  u64 info = 1 | ((u64)maker << 2) | ((u64)m << 8);
  tte *t = &TT[hash3(b, e, info) & TTMASK];
  t->b = b;
  t->e = e;
  t->info = info | ((u64)v << 1);
}

// ---------------- search ----------------
static int cdist[MAXC];

static void sortmoves(int *mv, double *key, int cnt) {
  // descending key
  for (int i = 1; i < cnt; i++) {
    int a = mv[i];
    double k = key[i];
    int j = i - 1;
    while (j >= 0 && key[j] < k) {
      mv[j + 1] = mv[j];
      key[j + 1] = key[j];
      j--;
    }
    mv[j + 1] = a;
    key[j + 1] = k;
  }
}

static const double P2[65] = {
    1.0, 0.5, 0.25, 0.125, 0.0625, 0.03125, 0.015625, 0.0078125, 0.00390625, 0.001953125,
    0.0009765625, 0.00048828125, 0.000244140625, 0.0001220703125, 6.103515625e-05,
    3.0517578125e-05, 1.52587890625e-05, 7.62939453125e-06, 3.814697265625e-06,
    1.9073486328125e-06, 9.5367431640625e-07, 4.76837158203125e-07, 2.384185791015625e-07,
    1.1920928955078125e-07, 5.960464477539063e-08, 2.9802322387695312e-08,
    1.4901161193847656e-08, 7.450580596923828e-09, 3.725290298461914e-09,
    1.862645149230957e-09, 9.313225746154785e-10, 4.656612873077393e-10,
    2.3283064365386963e-10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0};

// Returns 1 iff Maker wins. Precondition: no winning set is fully Blue.
static int solve_(u64 blue, u64 red, int maker, int m, const int *plv, int pnl) {
  nodes++;
  // collect live sets (no red, at most m empty cells)
  int nl = 0, minemp = 99;
  u64 rel = 0;
  int lv[pnl];
  unsigned char emp[pnl];
  for (int ii = 0; ii < pnl; ii++) {
    int i = plv ? plv[ii] : ii;
    u64 e = edges[i];
    if (e & red) continue;
    int k = __builtin_popcountll(e & ~blue);
    if (k > m) continue;
    lv[nl] = i;
    emp[nl++] = (unsigned char)k;
    rel |= e;
    if (k < minemp) minemp = k;
  }
  if (nl == 0) {
    return 0;
  }
  u64 empty = ALL & ~blue & ~red;
  u64 re = rel & empty, rb = rel & blue;
  if (maker && minemp == 1) {
    return 1;
  }
  int t = ttget(rb, re, maker, m);
  if (t >= 0) {
    return t;
  }
  u64 nred = ALL & ~rel;  // normalised Red
  double pot[MAXC];
  for (int v = 0; v < NC; v++) pot[v] = 0;
  for (int j = 0; j < nl; j++) {
    u64 e = edges[lv[j]] & empty;
    double w = P2[emp[j]];
    while (e) {
      int v = __builtin_ctzll(e);
      e &= e - 1;
      pot[v] += w;
    }
  }
  int mv[MAXC], cnt = 0;
  double key[MAXC];
  int res;
  if (maker) {
    u64 c = re;
    while (c) {
      int v = __builtin_ctzll(c);
      c &= c - 1;
      mv[cnt] = v;
      key[cnt++] = pot[v] - 1e-6 * cdist[v];
    }
    sortmoves(mv, key, cnt);
    res = 0;
    for (int i = 0; i < cnt && !res; i++) {
      u64 b2 = rb | (1ULL << mv[i]);
      // did Maker complete a set? (cannot: minemp >= 2 here)
      if (solve_(b2, nred, 0, MDEC(m), lv, nl)) res = 1;
    }
    ttput(rb, re, 1, m, res);
    return res;
  }
  // Breaker to move
  u64 thr = 0;
  int nthr = 0;
  if (m >= 1)
    for (int j = 0; j < nl; j++)
      if (emp[j] == 1) {
        u64 x = edges[lv[j]] & empty;
        if (!(thr & x)) {
          thr |= x;
          nthr++;
        }
      }
  u64 cand;
  if (nthr >= 2) {
    ttput(rb, re, 0, m, 1);
    return 1;
  } else if (nthr == 1) {
    cand = thr;
  } else {
    cand = re;
    if (use_dt && m >= 2) {
      // double-threat must-play
      // pair sets with exactly two empty cells: for v, T_v = partners
      u64 T[MAXC];
      int nt[MAXC];
      for (int v = 0; v < NC; v++) {
        T[v] = 0;
        nt[v] = 0;
      }
      for (int j = 0; j < nl; j++)
        if (emp[j] == 2) {
          u64 x = edges[lv[j]] & empty;
          int a = __builtin_ctzll(x);
          int b = 63 - __builtin_clzll(x);
          if (!((T[a] >> b) & 1)) {
            T[a] |= 1ULL << b;
            nt[a]++;
          }
          if (!((T[b] >> a) & 1)) {
            T[b] |= 1ULL << a;
            nt[b]++;
          }
        }
      for (int v = 0; v < NC; v++)
        if (nt[v] >= 2) {
          u64 M = 1ULL << v;
          if (nt[v] == 2) M |= T[v];
          cand &= M;
        }
      if (!cand) {
        ttput(rb, re, 0, m, 1);
        return 1;
      }
    }
    if (use_dom && __builtin_popcountll(cand) > 1) {
      // Breaker domination over live sets
      int W = (nl + 63) / 64;
      u64 *bs = calloc((size_t)NC * W, sizeof(u64));
      for (int j = 0; j < nl; j++) {
        u64 x = edges[lv[j]] & empty;
        while (x) {
          int v = __builtin_ctzll(x);
          x &= x - 1;
          bs[v * W + j / 64] |= 1ULL << (j % 64);
        }
      }
      u64 keep = cand;
      u64 cc = cand;
      while (cc) {
        int x = __builtin_ctzll(cc);
        cc &= cc - 1;
        u64 yy = re & ~(1ULL << x);
        while (yy) {
          int y = __builtin_ctzll(yy);
          yy &= yy - 1;
          int sub = 1, eq = 1;
          for (int w = 0; w < W; w++) {
            u64 a = bs[x * W + w], b = bs[y * W + w];
            if (a & ~b) {
              sub = 0;
              break;
            }
            if (a != b) eq = 0;
          }
          if (!sub) continue;
          if (eq && y > x) continue;  // keep the smaller index among equals
          keep &= ~(1ULL << x);
          break;
        }
      }
      free(bs);
      cand = keep;
    }
  }
  cnt = 0;
  u64 c = cand;
  while (c) {
    int v = __builtin_ctzll(c);
    c &= c - 1;
    mv[cnt] = v;
    key[cnt++] = pot[v] - 1e-6 * cdist[v];
  }
  sortmoves(mv, key, cnt);
  res = 1;
  for (int i = 0; i < cnt && res; i++) {
    if (!solve_(rb, nred | (1ULL << mv[i]), 1, m, lv, nl)) res = 0;
  }
  ttput(rb, re, 0, m, res);
  return res;
}

static int solve(u64 blue, u64 red, int maker, int m) { return solve_(blue, red, maker, m, NULL, NE); }


// ---------------- certificate dump ----------------
// Writes one line "m blue_rel rel move" (hex masks) for every Blue-to-move
// position reachable under the found Blue strategy against all Red replies
// (relevant cells and a pass, which stands for any move on a dead cell).
static FILE *CF;
static long long ncert;
#define SEENBITS 24
static u64 *SH_b, *SH_e;
static int *SH_m;

static int seen_insert(u64 b, u64 e, int m) {
  u64 h = hash3(b, e, (u64)m) & ((1ULL << SEENBITS) - 1);
  while (SH_m[h] != -1) {
    if (SH_b[h] == b && SH_e[h] == e && SH_m[h] == m) return 0;
    h = (h + 1) & ((1ULL << SEENBITS) - 1);
  }
  SH_b[h] = b;
  SH_e[h] = e;
  SH_m[h] = m;
  return 1;
}

static void live_info(u64 blue, u64 red, int m, u64 *rel, int *minemp) {
  *rel = 0;
  *minemp = 99;
  for (int i = 0; i < NE; i++) {
    u64 e = edges[i];
    if (e & red) continue;
    int k = __builtin_popcountll(e & ~blue);
    if (k > m) continue;
    *rel |= e;
    if (k < *minemp) *minemp = k;
  }
}

static void dump_maker(u64 blue, u64 red, int m) {
  u64 rel;
  int minemp;
  live_info(blue, red, m, &rel, &minemp);
  if (!rel || minemp > m) {
    fprintf(stderr, "dump: lost position reached\n");
    exit(2);
  }
  u64 empty = ALL & ~blue & ~red;
  u64 rb = blue & rel, re = rel & empty;
  if (!seen_insert(rb, re, m)) return;
  u64 nred = ALL & ~rel;
  int v = -1;
  if (minemp == 1) {
    for (int i = 0; i < NE && v < 0; i++) {
      u64 e = edges[i];
      if (e & red) continue;
      if (__builtin_popcountll(e & ~blue) == 1) v = __builtin_ctzll(e & ~blue);
    }
  } else {
    // try moves in the solver's potential order
    double pot[MAXC];
    for (int x = 0; x < NC; x++) pot[x] = 0;
    for (int i = 0; i < NE; i++) {
      u64 e = edges[i];
      if (e & red) continue;
      int k = __builtin_popcountll(e & ~blue);
      if (k > m) continue;
      u64 x = e & empty;
      while (x) {
        int z = __builtin_ctzll(x);
        x &= x - 1;
        pot[z] += P2[k];
      }
    }
    int mv[MAXC], cnt = 0;
    double key[MAXC];
    u64 c = re;
    while (c) {
      int x = __builtin_ctzll(c);
      c &= c - 1;
      mv[cnt] = x;
      key[cnt++] = pot[x] - 1e-6 * cdist[x];
    }
    sortmoves(mv, key, cnt);
    // CERTMIN=k: among the first k winning moves pick the one leaving Red the
    // fewest relevant replies (smaller certificates); default k = 1.
    int kmax = getenv("CERTMIN") ? atoi(getenv("CERTMIN")) : 1, found = 0, bestc = 1 << 30;
    for (int i = 0; i < cnt && found < kmax; i++) {
      u64 b2 = rb | (1ULL << mv[i]);
      if (!solve(b2, nred, 0, MDEC(m))) continue;
      found++;
      u64 r2;
      int me2;
      live_info(b2, nred, MDEC(m), &r2, &me2);
      int c2 = __builtin_popcountll(r2 & ~b2);
      // a move that leaves an immediate threat forces Red: count it as one reply
      if (me2 == 1) c2 = 1;
      if (c2 < bestc) {
        bestc = c2;
        v = mv[i];
      }
    }
  }
  if (v < 0) {
    fprintf(stderr, "dump: no winning move found\n");
    exit(2);
  }
  fprintf(CF, "%d %llx %llx %d\n", m, (unsigned long long)rb, (unsigned long long)rel, v);
  ncert++;
  if (ncert % 100000 == 0) {
    fprintf(stderr, "  cert lines %lld\n", ncert);
  }
  u64 b2 = rb | (1ULL << v);
  if (minemp == 1) return;  // Blue completed a winning set
  u64 rel2;
  int me2;
  live_info(b2, nred, MDEC(m), &rel2, &me2);
  u64 re2 = rel2 & ~b2;
  u64 c = re2;
  while (c) {
    int y = __builtin_ctzll(c);
    c &= c - 1;
    dump_maker(b2, nred | (1ULL << y), MDEC(m));
  }
  dump_maker(b2, nred, MDEC(m));  // Red pass / dead-cell move
}

// Breaker certificate: one line "m blue_rel rel move" for every Red-to-move
// position reachable under the found Red strategy against all Blue replies
// (relevant cells, and a pass standing for any Blue move on a dead cell).
static void order_by_potential(u64 blue, u64 red, int m, u64 cells, int *mv, int *cnt) {
  double pot[MAXC];
  u64 empty = ALL & ~blue & ~red;
  for (int x = 0; x < NC; x++) pot[x] = 0;
  for (int i = 0; i < NE; i++) {
    u64 e = edges[i];
    if (e & red) continue;
    int k = __builtin_popcountll(e & ~blue);
    if (k > m) continue;
    u64 x = e & empty;
    while (x) {
      int z = __builtin_ctzll(x);
      x &= x - 1;
      pot[z] += P2[k];
    }
  }
  double key[MAXC];
  *cnt = 0;
  u64 c = cells;
  while (c) {
    int x = __builtin_ctzll(c);
    c &= c - 1;
    mv[*cnt] = x;
    key[(*cnt)++] = pot[x] - 1e-6 * cdist[x];
  }
  sortmoves(mv, key, *cnt);
}

static void dump_breaker(u64 blue, u64 red, int m) {
  u64 rel;
  int minemp;
  live_info(blue, red, m, &rel, &minemp);
  if (!rel || minemp > m) return;  // Blue can no longer win
  u64 empty = ALL & ~blue & ~red;
  u64 rb = blue & rel, re = rel & empty;
  if (!seen_insert(rb, re, m)) return;
  u64 nred = ALL & ~rel;
  int mv[MAXC], cnt, y = -1;
  order_by_potential(rb, nred, m, re, mv, &cnt);
  for (int i = 0; i < cnt && y < 0; i++)
    if (!solve(rb, nred | (1ULL << mv[i]), 1, m)) y = mv[i];
  if (y < 0) {
    fprintf(stderr, "dump_breaker: no holding move found\n");
    exit(2);
  }
  fprintf(CF, "%d %llx %llx %d\n", m, (unsigned long long)rb, (unsigned long long)rel, y);
  ncert++;
  if (ncert % 100000 == 0) fprintf(stderr, "  cert lines %lld\n", ncert);
  u64 r2 = nred | (1ULL << y);
  u64 rel2;
  int me2;
  live_info(rb, r2, m, &rel2, &me2);
  if (!rel2 || me2 > m) return;
  u64 c = rel2 & ~rb;
  while (c) {
    int x = __builtin_ctzll(c);
    c &= c - 1;
    if (MODE == 'D' && m - 1 < 0) continue;
    dump_breaker(rb | (1ULL << x), r2, MDEC(m));
  }
  dump_breaker(rb, r2, MDEC(m));  // Blue pass / dead-cell move
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
  if (getenv("NODOM")) use_dom = 0;
  if (getenv("NODT")) use_dt = 0;
  NC = n * n;
  L = bound;
  if (MODE == 'D') DLIM = bound;
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
      int dR = 2 * r - (n - 1), dC = 2 * c - (n - 1), dS = -(dR + dC);
      int a = abs(dR), b = abs(dC), cc = abs(dS);
      int mx = a > b ? a : b;
      cdist[v] = mx > cc ? mx : cc;
    }
  int path[MAXC];
  for (int c = 0; c < n; c++) {
    path[0] = c;
    if (n == 1)
      edges[NE++] = 1;
    else
      rec_paths(path, 1, 1ULL << c);
  }
  fprintf(stderr, "winning sets: %d\n", NE);
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
    u64 b = 1ULL << v;
    int done = 0;
    for (int j = 0; j < NE; j++)
      if ((edges[j] & ~b) == 0) done = 1;
    int res = done ? 1 : solve(b, 0, 0, m0 - 1);
    any |= res;
    if (!res && getenv("CERT")) {
      char fn[512];
      snprintf(fn, sizeof fn, "%s_%d_red.txt", getenv("CERT"), v);
      CF = fopen(fn, "w");
      SH_b = malloc(sizeof(u64) << SEENBITS);
      SH_e = malloc(sizeof(u64) << SEENBITS);
      SH_m = malloc(sizeof(int) << SEENBITS);
      memset(SH_m, 0xff, sizeof(int) << SEENBITS);
      ncert = 0;
      fprintf(CF, "# n=%d mode=%c bound=%d first=%d side=red\n", n, MODE, bound, v);
      dump_breaker(b, 0, m0 - 1);
      fclose(CF);
      free(SH_b);
      free(SH_e);
      free(SH_m);
      fprintf(stderr, "certificate %s: %lld lines\n", fn, ncert);
    }
    if (res && getenv("CERT") && !done) {
      char fn[512];
      snprintf(fn, sizeof fn, "%s_%d.txt", getenv("CERT"), v);
      CF = fopen(fn, "w");
      SH_b = malloc(sizeof(u64) << SEENBITS);
      SH_e = malloc(sizeof(u64) << SEENBITS);
      SH_m = malloc(sizeof(int) << SEENBITS);
      memset(SH_m, 0xff, sizeof(int) << SEENBITS);
      ncert = 0;
      fprintf(CF, "# n=%d mode=%c bound=%d first=%d\n", n, MODE, bound, v);
      u64 rel;
      int me;
      live_info(b, 0, m0 - 1, &rel, &me);
      u64 c = rel & ~b;
      while (c) {
        int y = __builtin_ctzll(c);
        c &= c - 1;
        dump_maker(b, (ALL & ~rel) | (1ULL << y), m0 - 1);
      }
      dump_maker(b, ALL & ~rel, m0 - 1);
      fclose(CF);
      free(SH_b);
      free(SH_e);
      free(SH_m);
      fprintf(stderr, "certificate %s: %lld lines\n", fn, ncert);
    }
    printf("n=%d mode=%c bound=%d first=(%d,%d) result=%s nodes=%lld time=%.2fs\n", n, MODE, bound,
           v / n + 1, v % n + 1, res ? "BLUE" : "RED", nodes - n0,
           (double)(clock() - t0) / CLOCKS_PER_SEC);
    fflush(stdout);
  }
  printf("SUMMARY n=%d mode=%c bound=%d blue_wins=%d\n", n, MODE, bound, any);
  return 0;
}
