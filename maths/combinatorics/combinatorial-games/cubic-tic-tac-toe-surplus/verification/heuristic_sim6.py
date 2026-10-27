#!/usr/bin/env python3
"""HEURISTIC evidence only (not part of any proof): simulated 6x6x6 Maker-Breaker play.
Breaker blocks immediate threats, otherwise plays the danger-greedy (Erdos-Selfridge) move.
Maker plays randomly, steals the cell on most alive lines, or plays danger-greedy.
After each round we test whether a pairing (slot-saturating matching) exists.
Usage: python3 -I heuristic_sim6.py   (prints the first round with a pairing per game)"""
import random
from itertools import product

n = 6
CELLS = list(product(range(1, n + 1), repeat=3))
DIRS = [d for d in product((-1, 0, 1), repeat=3) if d != (0, 0, 0) and next(v for v in d if v) > 0]
LINES = []
for d in DIRS:
    for s in product(range(1, n + 1), repeat=3):
        if any((d[i] == 1 and s[i] != 1) or (d[i] == -1 and s[i] != n) for i in range(3)):
            continue
        LINES.append(tuple((s[0] + t * d[0], s[1] + t * d[1], s[2] + t * d[2]) for t in range(n)))
assert len(LINES) == 148
THROUGH = {c: [i for i, l in enumerate(LINES) if c in l] for c in CELLS}


def has_pairing(alive, free):
    slots = [[c for c in LINES[i] if c in free] for i in alive for _ in (0, 1)]
    owner = {}

    def aug(s, seen):
        for c in slots[s]:
            if c in seen:
                continue
            seen.add(c)
            if c not in owner or aug(owner[c], seen):
                owner[c] = s
                return True
        return False
    return all(aug(s, set()) for s in range(len(slots)))


def game(kind, seed, maxr=30):
    rng = random.Random(seed)
    free, alive, mk = set(CELLS), set(range(len(LINES))), set()
    danger = lambda c: sum(2.0 ** -sum(1 for x in LINES[i] if x in free) for i in THROUGH[c] if i in alive)
    for r in range(1, maxr + 1):
        fl = sorted(free)
        if kind == "random":
            m = rng.choice(fl)
        else:
            val = (lambda c: sum(1 for i in THROUGH[c] if i in alive)) if kind == "steal" else danger
            best = max(val(c) for c in fl)
            m = rng.choice([c for c in fl if val(c) == best])
        free.discard(m)
        mk.add(m)
        forced = [i for i in alive if sum(1 for x in LINES[i] if x in free) == 1]
        if forced:
            b = next(x for x in LINES[forced[0]] if x in free)
        else:
            best = max(danger(c) for c in free)
            b = rng.choice(sorted(c for c in free if danger(c) == best))
        free.discard(b)
        alive -= set(THROUGH[b])
        if any(all(x in mk for x in LINES[i]) for i in alive):
            return r, "maker completed a line"
        if 2 * len(alive) <= len(free) and has_pairing(sorted(alive), free):
            return r, f"pairing: alive={len(alive)} free={len(free)}"
    return None, "no pairing within limit"


if __name__ == "__main__":
    for kind in ("random", "steal", "danger"):
        for seed in range(3):
            print(kind, seed, *game(kind, seed), flush=True)
