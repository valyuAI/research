// hexstrict2.c - exact search for the "strict" reading of lambda(n): the game is
// ordinary Hex (it ends as soon as either player connects), and Blue succeeds
// iff Blue wins and, at that moment, Blue's stones contain a top-bottom path of
// at most l cells.  Used to prove Blue wins, so Blue is restricted to cells on
// short paths without Red stones (a sound restriction); Red may play anywhere.
// Pruning: Blue completes a short path at once if possible, Red must block a
// unique completion cell, and two distinct completion cells win for Blue.
// Positions are keyed by (Blue stones, relevant empty cells, number of other
// empty cells, side to move) up to the 180 degree rotation.  With CERT=prefix
// set, a winning first move writes a Blue certificate for py/check_strict.py.
//
// usage: hexstrict2 n bound [first-move-index ...]
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#define MAXC 64
#define MAXE 20000
typedef uint64_t u64;

static int n, NC, L;
static u64 nbr[MAXC], ALL, TOPR, BOTR, LEFTC, RIGHTC;
static u64 edges[MAXE];
static int NE;
static long long nodes;
static int ttbits = 24;


static void rec_paths(int *path, int len, u64 mask) {
  int v = path[len - 1];
  if (v / n == n - 1) {
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
    if (nbr[u] & mask & ~(1ULL << v)) continue;
    path[len] = u;
    rec_paths(path, len + 1, mask | (1ULL << u));
  }
}

static int connects(u64 stones, u64 from, u64 to) {
  u64 reach = stones & from, prev = 0;
  while (reach != prev) {
    prev = reach;
    u64 x = reach, add = 0;
    while (x) {
      int v = __builtin_ctzll(x);
      x &= x - 1;
      add |= nbr[v];
    }
    reach |= add & stones;
  }
  return (reach & to) != 0;
}

typedef struct {
  u64 b, r, x;
} tte;
static tte *TT;
static u64 TTMASK;
static inline u64 rot(u64 x) { return __builtin_bitreverse64(x) >> (64 - NC); }
static inline u64 hash2(u64 a, u64 b) {
  u64 h = a * 0x9E3779B97F4A7C15ULL ^ (b + 0x632BE59BD9B4E019ULL) * 0xC2B2AE3D27D4EB4FULL;
  h ^= h >> 29;
  h *= 0xBF58476D1CE4E5B9ULL;
  h ^= h >> 32;
  return h;
}
static void canon3(u64 *b, u64 *r) {
  u64 b2 = rot(*b), r2 = rot(*r);
  if (b2 < *b || (b2 == *b && r2 < *r)) {
    *b = b2;
    *r = r2;
  }
}
// key: blue (all stones), relevant empty cells, number of other empty cells, side
static int ttget3(u64 b, u64 re, int kp, int maker) {
  canon3(&b, &re);
  u64 x = 1 | ((u64)maker << 2) | ((u64)kp << 8);
  tte *t = &TT[(hash2(b, re) ^ (x * 0x9E3779B97F4A7C15ULL)) & TTMASK];
  if (t->b == b && t->r == re && (t->x & ~2ULL) == x) return (t->x >> 1) & 1;
  return -1;
}
static void ttput3(u64 b, u64 re, int kp, int maker, int v) {
  canon3(&b, &re);
  u64 x = 1 | ((u64)maker << 2) | ((u64)kp << 8);
  tte *t = &TT[(hash2(b, re) ^ (x * 0x9E3779B97F4A7C15ULL)) & TTMASK];
  t->b = b;
  t->r = re;
  t->x = x | ((u64)v << 1);
}

static int cdist[MAXC];

// Strict reading, Blue restricted to relevant cells (sound for proving Blue
// wins).  maker = 1 if Blue to move.  Precondition: nobody has connected.
// Key soundness: the live family is {S in W : S subset of blue|re}; Blue only
// plays in re; Red moves outside re are equivalent to one another (they only
// remove a cell Blue never uses), so only their number kp matters.
static int solve(u64 blue, u64 red, int maker) {
  nodes++;
  u64 rel = 0, thr = 0;
  int nthr = 0;
  for (int i = 0; i < NE; i++) {
    u64 e = edges[i];
    if (e & red) continue;
    rel |= e;
    u64 x = e & ~blue;
    if (__builtin_popcountll(x) == 1 && !(thr & x)) {
      thr |= x;
      nthr++;
    }
  }
  if (!rel) return 0;
  if (maker && nthr) return 1;
  if (!maker && nthr >= 2) return 1;
  u64 empty = ALL & ~blue & ~red;
  u64 re = rel & empty;
  int kp = __builtin_popcountll(empty & ~rel);
  int t = ttget3(blue, re, kp, maker);
  if (t >= 0) return t;
  u64 cand = (!maker && nthr == 1) ? thr : re;
  int mv[MAXC], key[MAXC], cnt = 0;
  u64 c = cand;
  while (c) {
    int v = __builtin_ctzll(c);
    c &= c - 1;
    mv[cnt] = v;
    key[cnt++] = cdist[v];
  }
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
      if (connects(b2, TOPR, BOTR)) continue;  // long-only connection: Blue fails
      if (solve(b2, red, 0)) res = 1;
    }
  } else {
    res = 1;
    for (int i = 0; i < cnt && res; i++) {
      u64 r2 = red | (1ULL << mv[i]);
      if (!solve(blue, r2, 1)) res = 0;
    }
    if (res && nthr == 0 && kp > 0) {
      // Red plays some cell outside the relevant set (all such moves equivalent)
      u64 z = empty & ~rel;
      int zz = __builtin_ctzll(z);
      if (!solve(blue, red | (1ULL << zz), 1)) res = 0;
    }
  }
  ttput3(blue, re, kp, maker, res);
  return res;
}


// ---------------- certificate dump (strict reading) ----------------
// One line "blue re kp move" per Blue-to-move key reached by the strategy
// against all Red replies (relevant cells and one representative outside cell).
static FILE *CF;
static long long ncert;
#define SB 25
static u64 *SH_b, *SH_e;
static int *SH_k;
static int seen_ins(u64 b, u64 e, int k) {
  u64 h = (hash2(b, e) ^ ((u64)k * 0x9E3779B97F4A7C15ULL)) & ((1ULL << SB) - 1);
  while (SH_k[h] != -1) {
    if (SH_b[h] == b && SH_e[h] == e && SH_k[h] == k) return 0;
    h = (h + 1) & ((1ULL << SB) - 1);
  }
  SH_b[h] = b;
  SH_e[h] = e;
  SH_k[h] = k;
  return 1;
}

static void dump_blue(u64 blue, u64 red) {
  u64 rel = 0, thr = 0;
  for (int i = 0; i < NE; i++) {
    u64 e = edges[i];
    if (e & red) continue;
    rel |= e;
    u64 x = e & ~blue;
    if (__builtin_popcountll(x) == 1) thr |= x;
  }
  if (!rel) {
    fprintf(stderr, "dump: lost position\n");
    exit(2);
  }
  u64 empty = ALL & ~blue & ~red;
  u64 re = rel & empty;
  int kp = __builtin_popcountll(empty & ~rel);
  if (!seen_ins(blue, re, kp)) return;
  int v = -1;
  if (thr) {
    v = __builtin_ctzll(thr);
  } else {
    int mv[MAXC], key[MAXC], cnt = 0;
    u64 c = re;
    while (c) {
      int x = __builtin_ctzll(c);
      c &= c - 1;
      mv[cnt] = x;
      key[cnt++] = cdist[x];
    }
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
    for (int i = 0; i < cnt && v < 0; i++) {
      u64 b2 = blue | (1ULL << mv[i]);
      if (connects(b2, TOPR, BOTR)) continue;
      if (solve(b2, red, 0)) v = mv[i];
    }
  }
  if (v < 0) {
    fprintf(stderr, "dump: no winning move\n");
    exit(2);
  }
  fprintf(CF, "%llx %llx %d %d\n", (unsigned long long)blue, (unsigned long long)re, kp, v);
  if (++ncert % 100000 == 0) fprintf(stderr, "  cert lines %lld\n", ncert);
  if (thr) return;
  u64 b2 = blue | (1ULL << v);
  u64 c = re & ~(1ULL << v);
  while (c) {
    int y = __builtin_ctzll(c);
    c &= c - 1;
    dump_blue(b2, red | (1ULL << y));
  }
  if (kp > 0) {
    int z = __builtin_ctzll(empty & ~rel);
    dump_blue(b2, red | (1ULL << z));
  }
}

int main(int argc, char **argv) {
  if (argc < 3) {
    fprintf(stderr, "usage: %s n bound [first moves]\n", argv[0]);
    return 1;
  }
  n = atoi(argv[1]);
  L = atoi(argv[2]);
  if (getenv("TTBITS")) ttbits = atoi(getenv("TTBITS"));
  NC = n * n;
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
      if (r == 0) TOPR |= 1ULL << v;
      if (r == n - 1) BOTR |= 1ULL << v;
      if (c == 0) LEFTC |= 1ULL << v;
      if (c == n - 1) RIGHTC |= 1ULL << v;
      int dR = 2 * r - (n - 1), dC = 2 * c - (n - 1), dS = -(dR + dC);
      int a = abs(dR), b = abs(dC), cc = abs(dS);
      int mx = a > b ? a : b;
      cdist[v] = mx > cc ? mx : cc;
    }
  int path[MAXC];
  for (int c = 0; c < n; c++) {
    path[0] = c;
    rec_paths(path, 1, 1ULL << c);
  }
  fprintf(stderr, "winning sets: %d\n", NE);
  TT = calloc((size_t)1 << ttbits, sizeof(tte));
  TTMASK = ((u64)1 << ttbits) - 1;
  int firsts[MAXC], nf = 0;
  if (argc > 3)
    for (int i = 3; i < argc; i++) firsts[nf++] = atoi(argv[i]);
  else
    for (int v = 0; v < NC; v++)
      if (v <= NC - 1 - v) firsts[nf++] = v;
  int any = 0;
  for (int i = 0; i < nf; i++) {
    int v = firsts[i];
    clock_t t0 = clock();
    long long n0 = nodes;
    int res = solve(1ULL << v, 0, 0);
    any |= res;
    if (res && getenv("CERT")) {
      char fn[512];
      snprintf(fn, sizeof fn, "%s_%d.txt", getenv("CERT"), v);
      CF = fopen(fn, "w");
      SH_b = malloc(sizeof(u64) << SB);
      SH_e = malloc(sizeof(u64) << SB);
      SH_k = malloc(sizeof(int) << SB);
      memset(SH_k, 0xff, sizeof(int) << SB);
      ncert = 0;
      fprintf(CF, "# strict n=%d bound=%d first=%d\n", n, L, v);
      for (int y = 0; y < NC; y++)
        if (y != v) dump_blue(1ULL << v, 1ULL << y);
      fclose(CF);
      fprintf(stderr, "certificate %s: %lld lines\n", fn, ncert);
    }
    printf("strict n=%d bound=%d first=(%d,%d) result=%s nodes=%lld time=%.2fs\n", n, L, v / n + 1,
           v % n + 1, res ? "BLUE" : "RED", nodes - n0, (double)(clock() - t0) / CLOCKS_PER_SEC);
    fflush(stdout);
  }
  printf("SUMMARY strict n=%d bound=%d blue_wins=%d\n", n, L, any);
  return 0;
}
