"""Print a longest game against a Blue certificate (Red maximises Blue's stones).

usage: python3 longest_line.py CERT
Uses the same rules and keys as check_cert.py (mode L or D, Blue certificates).
"""
import gzip
import sys
from functools import lru_cache

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from check_cert import neighbours, winning_sets, shortest_blue_path  # noqa: E402

sys.setrecursionlimit(100000)


def main():
    path = sys.argv[1]
    with (gzip.open(path, "rt") if path.endswith(".gz") else open(path)) as fh:
        params = dict(kv.split("=") for kv in fh.readline().split()[1:])
        n, mode, bound, first = int(params["n"]), params["mode"], int(params["bound"]), int(params["first"])
        cert = {}
        for line in fh:
            m, b, rel, mv = line.split()
            cert[(int(m) if mode == "D" else 0, int(b, 16), int(rel, 16))] = int(mv)
    N = n * n
    nb = neighbours(n)
    W = winning_sets(n, bound, nb)
    d = bound if mode == "D" else None

    def key(blue, red):
        m = None if mode == "L" else d - blue.bit_count()
        R = 0
        for w in W:
            if w & red:
                continue
            if m is not None and (w & ~blue).bit_count() > m:
                continue
            R |= w
        return (m if mode == "D" else 0, blue & R, R)

    def won(b):
        sp = shortest_blue_path(n, nb, b)
        return sp is not None and (mode == "D" or sp <= bound)

    @lru_cache(maxsize=None)
    def value(blue, red):
        """Max number of further Blue stones Red can force (Blue to move)."""
        v = cert[key(blue, red)]
        b2 = blue | (1 << v)
        if won(b2):
            return 1
        best = 0
        for y in range(N):
            if not ((b2 | red) >> y) & 1:
                best = max(best, value(b2, red | (1 << y)))
        return 1 + best

    def show(blue, red):
        rows = []
        for r in range(n):
            s = " " * r
            for c in range(n):
                i = r * n + c
                s += ("B " if (blue >> i) & 1 else "R " if (red >> i) & 1 else ". ")
            rows.append(s)
        return "\n".join(rows)

    blue = 1 << first
    # Red's first reply maximising the game
    best, by = -1, None
    for y in range(N):
        if y != first:
            val = value(blue, 1 << y)
            if val > best:
                best, by = val, y
    red = 1 << by
    seq = [("B", first), ("R", by)]
    while True:
        v = cert[key(blue, red)]
        blue |= 1 << v
        seq.append(("B", v))
        if won(blue):
            break
        bv, bb = -1, None
        for y in range(N):
            if not ((blue | red) >> y) & 1:
                val = value(blue, red | (1 << y))
                if val > bv:
                    bv, bb = val, y
        red |= 1 << bb
        seq.append(("R", bb))
    print("moves (row,col 1-based):", " ".join(f"{p}({x // n + 1},{x % n + 1})" for p, x in seq))
    print(f"Blue stones used: {blue.bit_count()}, shortest Blue path: {shortest_blue_path(n, nb, blue)}")
    print(show(blue, red))


if __name__ == "__main__":
    main()
