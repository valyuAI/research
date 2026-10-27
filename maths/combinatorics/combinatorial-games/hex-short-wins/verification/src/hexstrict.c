// hexstrict.c - exact search for the "strict" reading of lambda(n): the game is
// ordinary Hex (it ends as soon as either player connects), and Blue succeeds
// iff Blue wins and, at that moment, Blue's stones contain a top-bottom path of
// at most l cells.  Every empty cell is a legal move for both players; the
// only pruning is: Blue completes a short path at once if possible, Red must
// block a unique completion cell, and two distinct completion cells win for
// Blue.  Positions are keyed exactly (Blue mask, Red mask) up to the 180
// degree rotation.
//
// usage: hexstrict n bound [first-move-index ...]
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
static int blue_rel_only = 0;

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
  u64 b, r;
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
static void canon(u64 *b, u64 *r) {
  u64 b2 = rot(*b), r2 = rot(*r);
  if (b2 < *b || (b2 == *b && r2 < *r)) {
    *b = b2;
    *r = r2;
  }
}
// value stored in bit 63 of r (valid flag bit 62)
static int ttget(u64 b, u64 r) {
  canon(&b, &r);
  tte *t = &TT[hash2(b, r) & TTMASK];
  if (t->b == b && (t->r & ((1ULL << 62) - 1)) == r && ((t->r >> 62) & 1)) return (t->r >> 63) & 1;
  return -1;
}
static void ttput(u64 b, u64 r, int v) {
  canon(&b, &r);
  tte *t = &TT[hash2(b, r) & TTMASK];
  t->b = b;
  t->r = r | (1ULL << 62) | ((u64)v << 63);
}

static int cdist[MAXC];

// Blue to move or Red to move (by counts). Precondition: nobody has connected.
static int solve(u64 blue, u64 red) {
  nodes++;
  int maker = __builtin_popcountll(blue) == __builtin_popcountll(red);
  // live short sets and threats
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
  int t = ttget(blue, red);
  if (t >= 0) return t;
  u64 empty = ALL & ~blue & ~red;
  u64 cand = (!maker && nthr == 1) ? thr : empty;
  if (maker && blue_rel_only) cand &= rel;
  int mv[MAXC], key[MAXC], cnt = 0;
  u64 c = cand;
  while (c) {
    int v = __builtin_ctzll(c);
    c &= c - 1;
    mv[cnt] = v;
    key[cnt++] = (((rel >> v) & 1) ? 0 : 1000) + cdist[v];
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
      // no short completion exists (checked above), so a Blue connection now is a long one
      if (connects(b2, TOPR, BOTR)) continue;  // Blue wins Hex with a long path: failure
      if (solve(b2, red)) res = 1;
    }
  } else {
    res = 1;
    for (int i = 0; i < cnt && res; i++) {
      u64 r2 = red | (1ULL << mv[i]);
      if (connects(r2, LEFTC, RIGHTC)) {
        res = 0;  // Red wins Hex
        break;
      }
      if (!solve(blue, r2)) res = 0;
    }
  }
  ttput(blue, red, res);
  return res;
}

int main(int argc, char **argv) {
  if (argc < 3) {
    fprintf(stderr, "usage: %s n bound [first moves]\n", argv[0]);
    return 1;
  }
  n = atoi(argv[1]);
  L = atoi(argv[2]);
  if (getenv("TTBITS")) ttbits = atoi(getenv("TTBITS"));
  if (getenv("BLUEREL")) blue_rel_only = 1;
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
    int res = solve(1ULL << v, 0);
    any |= res;
    printf("strict n=%d bound=%d first=(%d,%d) result=%s nodes=%lld time=%.2fs\n", n, L, v / n + 1,
           v % n + 1, res ? "BLUE" : "RED", nodes - n0, (double)(clock() - t0) / CLOCKS_PER_SEC);
    fflush(stdout);
  }
  printf("SUMMARY strict n=%d bound=%d blue_wins=%d\n", n, L, any);
  return 0;
}
