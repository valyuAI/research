"""Independent plain solver for Hex(n, l) in Campbell's sense (Maker-Breaker).

Winning sets: cell sets of top-bottom paths with at most l cells (all simple
paths, then reduced to inclusion-minimal sets).  Search: plain minimax with
memoisation; the only restriction is that both players' moves are limited to
cells lying on some winning set that contains no Red stone (a move elsewhere
is equivalent to passing, which never helps either player in a Maker-Breaker
game).
"""
import sys
from functools import lru_cache

sys.setrecursionlimit(10000)


def board(n):
    nb = {}
    for r in range(n):
        for c in range(n):
            s = []
            for dr, dc in ((0, -1), (0, 1), (-1, 0), (-1, 1), (1, -1), (1, 0)):
                rr, cc = r + dr, c + dc
                if 0 <= rr < n and 0 <= cc < n:
                    s.append(rr * n + cc)
            nb[r * n + c] = s
    return nb


def winning_sets(n, l):
    nb = board(n)
    sets = set()

    def dfs(path, used):
        v = path[-1]
        if v // n == n - 1:
            sets.add(used)
            return
        if len(path) == l:
            return
        for u in nb[v]:
            if not (used >> u) & 1:
                dfs(path + [u], used | (1 << u))

    for c in range(n):
        dfs([c], 1 << c)
    sets = sorted(sets, key=lambda s: bin(s).count("1"))
    minimal = []
    for s in sets:
        if not any((t & s) == t for t in minimal):
            minimal.append(s)
    return minimal


def make_solver(n, l):
    W = winning_sets(n, l)

    @lru_cache(maxsize=None)
    def maker_wins(blue, red, maker_to_move):
        live = [w for w in W if not (w & red)]
        if not live:
            return False
        if any((w & ~blue) == 0 for w in live):
            return True
        rel = 0
        for w in live:
            rel |= w
        cells = [v for v in range(n * n) if (rel >> v) & 1 and not (blue >> v) & 1]
        if maker_to_move:
            return any(maker_wins(blue | (1 << v), red, False) for v in cells)
        return all(maker_wins(blue, red | (1 << v), True) for v in cells)

    return W, maker_wins


if __name__ == "__main__":
    n, l = int(sys.argv[1]), int(sys.argv[2])
    firsts = [int(x) for x in sys.argv[3:]] or list(range(n * n))
    W, mw = make_solver(n, l)
    print("winning sets", len(W))
    for f in firsts:
        print("first", (f // n + 1, f % n + 1), "Blue wins" if mw(1 << f, 0, False) else "Red holds",
              "cache", mw.cache_info().currsize, flush=True)
