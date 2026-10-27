"""Independent checker for Blue strategies under the STRICT reading of lambda.

Strict reading: the game is ordinary Hex (Blue moves first and joins row 0 to
row n-1; Red joins column 0 to column n-1); it ends as soon as either player
has a connection.  Blue succeeds iff Blue makes the first connection and, at
that moment, Blue's stones contain a top-bottom path of at most l cells.

Certificate lines (after a '#' header "strict n=.. bound=.. first=.."):
    blue_hex  re_hex  kp  move
keyed by (blue stones, relevant empty cells, number of other empty cells),
where the relevant cells R are the union of the top-bottom paths with at
most l cells that contain no Red stone.

The checker plays every Red reply (every empty cell) from every position the
strategy reaches.  It memoises on the key.  This is sound because the key
determines everything the rest of the game depends on when Blue only plays
inside R: the family of still-possible short paths is exactly the short
paths inside blue | re; whether a Blue move creates a connection, and the
length of its shortest path, depend only on the Blue stones; a Red connection
forces R to be empty; and two Red moves outside R lead to the same key.
(The checker nevertheless also checks the Red connection directly.)
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


def short_sets(n, l, nb):
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
    ordered = sorted(found, key=lambda s: bin(s).count("1"))
    minimal = []
    for s in ordered:
        if not any((t & s) == t for t in minimal):
            minimal.append(s)
    return minimal


def blue_shortest(n, nb, blue):
    """Cells in a shortest top-bottom path inside blue, or None."""
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


def red_connected(n, nb, red):
    seen = set(v for v in range(0, n * n, n) if (red >> v) & 1)
    stack = list(seen)
    while stack:
        v = stack.pop()
        if v % n == n - 1:
            return True
        for u in nb[v]:
            if (red >> u) & 1 and u not in seen:
                seen.add(u)
                stack.append(u)
    return False


def main():
    path = sys.argv[1]
    with (gzip.open(path, "rt") if path.endswith(".gz") else open(path)) as fh:
        header = fh.readline().split()
        params = dict(kv.split("=") for kv in header[2:])
        n, l, first = int(params["n"]), int(params["bound"]), int(params["first"])
        if header[:2] != ["#", "strict"] or not (2 <= n <= 8 and 1 <= l <= n * n and 0 <= first < n * n):
            raise SystemExit(f"FAIL: bad header {header}")
        cert = {}
        for line in fh:
            if not line.strip():
                continue
            b, re_, kp, mv = line.split()
            cert[(int(b, 16), int(re_, 16), int(kp))] = int(mv)
    N = n * n
    full = (1 << N) - 1
    nb = neighbours(n)
    W = short_sets(n, l, nb)
    print(f"strict n={n} l={l} first=({first // n + 1},{first % n + 1}) short sets={len(W)} "
          f"certificate keys={len(cert)}", flush=True)
    verified = set()
    stats = {"keys": 0, "max_blue": 0}

    def check(blue, red):
        # Blue to move; nobody has connected yet.
        if red_connected(n, nb, red):
            raise SystemExit(f"FAIL: Red connected, blue={blue:x} red={red:x}")
        R = 0
        for w in W:
            if not (w & red):
                R |= w
        if R == 0:
            raise SystemExit(f"FAIL: no short path possible, blue={blue:x} red={red:x}")
        empty = full & ~blue & ~red
        key = (blue, R & empty, bin(empty & ~R).count("1"))
        if key in verified:
            return
        if key not in cert:
            raise SystemExit(f"FAIL: no move for key {key}")
        v = cert[key]
        if not (R & empty) >> v & 1:
            raise SystemExit(f"FAIL: move {v} not an empty relevant cell at key {key}")
        b2 = blue | (1 << v)
        stats["keys"] += 1
        stats["max_blue"] = max(stats["max_blue"], bin(b2).count("1"))
        if stats["keys"] % 50000 == 0:
            print(f"  checked {stats['keys']} keys", flush=True)
        sp = blue_shortest(n, nb, b2)
        if sp is not None:
            if sp <= l:
                verified.add(key)
                return
            raise SystemExit(f"FAIL: Blue connects with shortest path {sp} > {l}, blue={b2:x}")
        e2 = empty & ~(1 << v)
        for y in range(N):
            if (e2 >> y) & 1:
                check(b2, red | (1 << y))
        verified.add(key)

    blue0 = 1 << first
    for y in range(N):
        if y != first:
            check(blue0, 1 << y)
    print(f"VERIFIED [strict n={n} bound={l} first={first}] (strict reading): Blue opening ({first // n + 1},{first % n + 1}) forces its first "
          f"connection to contain a path of <= {l} cells; keys checked={stats['keys']}, "
          f"max Blue stones={stats['max_blue']}")


if __name__ == "__main__":
    main()
