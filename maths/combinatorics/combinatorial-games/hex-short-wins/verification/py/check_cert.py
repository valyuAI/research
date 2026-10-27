"""Independent checker for strategy certificates in Campbell's Hex games.

Games (G. Campbell, INTEGERS 4 (2004) #G02).  Board: n x n Hex rhombus, cell
(r, c) -> index r*n + c, Blue moves first and joins row 0 to row n-1; the six
neighbours of (r, c) are (r, c-1), (r, c+1), (r-1, c), (r-1, c+1), (r+1, c-1),
(r+1, c).
  mode L, bound l (Campbell's Hex(n, l)): Blue wins as soon as Blue's stones
    contain a top-bottom path of at most l cells; play continues after a
    longer Blue connection; there is no limit on the number of moves.
  mode D, bound d (Campbell's Hex_d(n)): Blue wins iff Blue's stones contain a
    top-bottom connection while Blue has placed at most d stones.

Certificate files: header "# n=.. mode=.. bound=.. first=.. [side=red]", then
lines "m blue_rel rel move" (hex masks).  A Blue certificate gives Blue's move
in every Blue-to-move position its strategy reaches against all Red replies;
a Red certificate (side=red) gives Red's move in every Red-to-move position
its strategy reaches against all Blue replies.

Winning sets are recomputed here from scratch: all simple top-bottom paths
with at most l (or d) cells, reduced to inclusion-minimal cell sets.

Keys.  Let m be the number of Blue stones still allowed (mode D; unbounded in
mode L) and let the live sets be the winning sets with no Red stone (and, in
mode D, at most m empty cells).  R is their union and the key is
(m, blue & R, R).  The live family is exactly the set of winning sets inside R
(with at most m cells outside blue in mode D), so the key determines the rest
of the game: a move outside R changes no live set, and in mode D a Blue stone
outside R only uses up one of Blue's stones.  The checker therefore memoises
on keys.  Every reply of the opponent (every empty cell) is examined.
"""
import gzip
import sys
from collections import deque

sys.setrecursionlimit(100000)


def neighbours(n):
    nb = []
    for r in range(n):
        for c in range(n):
            s = []
            for dr, dc in ((0, -1), (0, 1), (-1, 0), (-1, 1), (1, -1), (1, 0)):
                rr, cc = r + dr, c + dc
                if 0 <= rr < n and 0 <= cc < n:
                    s.append(rr * n + cc)
            nb.append(s)
    return nb


def winning_sets(n, l, nb):
    found = set()

    def dfs(v, used, length):
        if v // n == n - 1:
            found.add(used)
            return
        if length == l:
            return
        for u in nb[v]:
            if not (used >> u) & 1:
                dfs(u, used | (1 << u), length + 1)

    for c in range(n):
        dfs(c, 1 << c, 1)
    ordered = sorted(found, key=lambda s: s.bit_count())
    minimal = []
    for s in ordered:
        if not any((t & s) == t for t in minimal):
            minimal.append(s)
    return minimal


def shortest_blue_path(n, nb, blue):
    """Fewest cells of a top-bottom path inside blue (BFS); None if none."""
    dist = {}
    dq = deque()
    for v in range(n):
        if (blue >> v) & 1:
            dist[v] = 1
            dq.append(v)
    while dq:
        v = dq.popleft()
        if v // n == n - 1:
            return dist[v]
        for u in nb[v]:
            if (blue >> u) & 1 and u not in dist:
                dist[u] = dist[v] + 1
                dq.append(u)
    return None


def main():
    path = sys.argv[1]
    with (gzip.open(path, "rt") if path.endswith(".gz") else open(path)) as fh:
        header = fh.readline().split()
        params = dict(kv.split("=") for kv in header[1:])
        n, mode = int(params["n"]), params["mode"]
        bound, first = int(params["bound"]), int(params["first"])
        side = params.get("side", "blue")
        if not (2 <= n <= 8 and mode in ("L", "D") and 1 <= bound <= n * n and 0 <= first < n * n
                and side in ("blue", "red")):
            raise SystemExit(f"FAIL: bad header {header}")
        cert = {}
        for line in fh:
            if not line.strip():
                continue
            m, b, rel, mv = line.split()
            cert[(int(m) if mode == "D" else 0, int(b, 16), int(rel, 16))] = int(mv)
    N = n * n
    nb = neighbours(n)
    W = winning_sets(n, bound, nb)
    print(f"n={n} mode={mode} bound={bound} first=({first // n + 1},{first % n + 1}) side={side} "
          f"winning sets={len(W)} certificate entries={len(cert)}", flush=True)
    d = bound if mode == "D" else None
    verified = set()
    stats = {"positions": 0, "max_blue": 0}

    def restrict(live, blue, red, m):
        """Live sets: no Red stone and (mode D) at most m empty cells."""
        if m is None:
            return [w for w in live if not w & red]
        return [w for w in live if not w & red and (w & ~blue).bit_count() <= m]

    def blue_has_won(b):
        sp = shortest_blue_path(n, nb, b)
        if sp is None:
            return False
        return True if mode == "D" else sp <= bound

    def progress():
        stats["positions"] += 1
        if stats["positions"] % 50000 == 0:
            print(f"  checked {stats['positions']} positions", flush=True)

    # ---- Blue strategy: Blue to move at (blue, red) ----
    def check_blue(blue, red, live):
        nbl = blue.bit_count()
        m = None if mode == "L" else d - nbl
        live = restrict(live, blue, red, m)
        R = 0
        for w in live:
            R |= w
        if R == 0:
            raise SystemExit(f"FAIL: Blue cannot win any more at blue={blue:x} red={red:x}")
        key = (m if mode == "D" else 0, blue & R, R)
        if key in verified:
            return
        if key not in cert:
            raise SystemExit(f"FAIL: no certificate move for key {key}")
        v = cert[key]
        if not (0 <= v < N) or ((blue | red) >> v) & 1 or not (R >> v) & 1:
            raise SystemExit(f"FAIL: illegal or irrelevant move {v} at key {key}")
        b2 = blue | (1 << v)
        progress()
        stats["max_blue"] = max(stats["max_blue"], nbl + 1)
        if blue_has_won(b2):
            verified.add(key)
            return
        if mode == "D" and nbl + 1 >= d:
            raise SystemExit(f"FAIL: Blue out of stones at blue={b2:x} red={red:x}")
        for y in range(N):
            if not ((b2 | red) >> y) & 1:
                check_blue(b2, red | (1 << y), live)
        verified.add(key)

    # ---- Red strategy: Red to move at (blue, red) ----
    def check_red(blue, red, live):
        nbl = blue.bit_count()
        m = None if mode == "L" else d - nbl
        live = restrict(live, blue, red, m)
        R = 0
        for w in live:
            R |= w
        if R == 0:
            return  # Blue can no longer complete any winning set
        key = (m if mode == "D" else 0, blue & R, R)
        if key in verified:
            return
        if key not in cert:
            raise SystemExit(f"FAIL: no Red move for key {key}")
        y = cert[key]
        if not (0 <= y < N) or ((blue | red) >> y) & 1:
            raise SystemExit(f"FAIL: illegal Red move {y} at key {key}")
        red2 = red | (1 << y)
        progress()
        for x in range(N):
            if ((blue | red2) >> x) & 1:
                continue
            b2 = blue | (1 << x)
            if blue_has_won(b2):
                raise SystemExit(f"FAIL: Blue wins at blue={b2:x} red={red2:x}")
            if mode == "D" and nbl + 1 >= d:
                continue  # Blue has used all its stones without connecting
            check_red(b2, red2, live)
        verified.add(key)

    blue0 = 1 << first
    tag = f"[n={n} mode={mode} bound={bound} first={first} side={side}]"
    if blue_has_won(blue0):
        print("trivial: Blue has won after its first stone")
        return
    if side == "red":
        check_red(blue0, 0, W)
        print(f"VERIFIED {tag}: Red stops Blue after first move ({first // n + 1},{first % n + 1}); "
              f"Red-to-move positions checked={stats['positions']}")
    else:
        for y in range(N):
            if y != first:
                check_blue(blue0, 1 << y, W)
        print(f"VERIFIED {tag}: Blue wins with first move ({first // n + 1},{first % n + 1}); "
              f"Blue-to-move positions checked={stats['positions']}, max Blue stones={stats['max_blue']}")


if __name__ == "__main__":
    main()
