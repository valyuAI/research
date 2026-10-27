#!/usr/bin/env python3
"""Hall-surplus certificate: Breaker wins Maker-Breaker tic-tac-toe on the 7x7x7 cube.

Standard library only. Usage:
    python3 -I surplus_certificate.py [--workers K] [--out results/surplus_python.json]

Definitions. A line is "alive" if Breaker holds none of its cells. The slot graph has two
slots per alive line, each joined to the free cells of that line. Its surplus is
    sigma = min over nonempty slot sets S of |N(S)| - |S|.
If sigma >= d, then after Maker claims ANY d further cells the slot graph still has a
matching saturating all slots, i.e. a pairing strategy for Breaker (Hall's theorem; see
formal/ValyuResearch/CubicTicTacToe.lean). sigma >= d is tested by replication: for every
alive line, give it d extra slots and check that a slot-saturating matching still exists.

Part A (Maker opens at the centre (4,4,4)).
  A1. Every Breaker set made of one non-centre cell on each of the four space diagonals that
      meets at least 26 lines has sigma >= 3 (checked on all symmetry classes; we report the
      exact sigma, capped at 4).
  A2. Breaker's rule: (5,5,5), then three times the free cell on a space diagonal he has not
      used that meets the most lines not yet met by his cells (ties: lexicographically
      smallest). The rule only looks at space-diagonal cells, so we enumerate Maker's moves
      2-4 as "a free space-diagonal cell" or "any other cell"; every leaf gives a set from A1
      meeting 27 lines.
Part B (Maker opens elsewhere).
  B1. Breaker takes the centre, then any free non-centre space-diagonal cell a, then any free
      cell b on a different space diagonal sharing no line with a (each a has exactly 12 such
      b, so one is always free). For every Maker first move m1 and every such pair (a, b),
      sigma >= 2 (checked on all symmetry classes of (m1, {a, b})).
In both parts the unknown later Maker moves number 3 (Part A) and 2 (Part B), so Breaker
then wins by pairing.
"""
import argparse
import json
import sys
import time
from itertools import combinations, permutations, product
from multiprocessing import Pool

N = 7


def build(n):
    cells = [(x, y, z) for x in range(1, n + 1) for y in range(1, n + 1) for z in range(1, n + 1)]
    idx = {c: i for i, c in enumerate(cells)}
    dirs = [d for d in product((-1, 0, 1), repeat=3) if d != (0, 0, 0) and next(v for v in d if v) > 0]
    lines = []
    for d in dirs:
        for s in product(range(1, n + 1), repeat=3):
            if any((d[i] == 1 and s[i] != 1) or (d[i] == -1 and s[i] != n) for i in range(3)):
                continue
            lines.append(tuple(idx[(s[0] + t * d[0], s[1] + t * d[1], s[2] + t * d[2])] for t in range(n)))
    through = [[] for _ in cells]
    for li, l in enumerate(lines):
        for c in l:
            through[c].append(li)
    return cells, idx, lines, through


CELLS, IDX, LINES, THROUGH = build(N)
assert len(LINES) == 3 * N * N + 6 * N + 4 == 193
NC = len(CELLS)
CENTRE = IDX[(4, 4, 4)]
DIAGS = [li for li, l in enumerate(LINES) if all(len({CELLS[c][k] for c in l}) == N for k in range(3))]
assert len(DIAGS) == 4
DIAG_OF = {c: li for li in DIAGS for c in LINES[li] if c != CENTRE}
DCELLS = sorted(DIAG_OF)
SYMS = [(p, s) for p in permutations(range(3)) for s in range(8)]


def apply_sym(g, c):
    p, s = g
    v = CELLS[c]
    return IDX[tuple((N + 1 - v[p[i]]) if (s >> i) & 1 else v[p[i]] for i in range(3))]


def surplus(breaker, maker, cap):
    """Exact surplus of the slot graph, capped at `cap`; -1 if no slot-saturating matching."""
    occ = set(breaker) | set(maker)
    dead = set()
    for b in breaker:
        dead.update(THROUGH[b])
    alive = [li for li in range(len(LINES)) if li not in dead]
    adj = [[c for c in LINES[li] if c not in occ] for li in alive]

    def augment(s, slot_line, match_slot, match_cell):
        seen = set()
        stack = [(s, iter(adj[slot_line[s]]))]
        while stack:
            cur, it = stack[-1]
            for c in it:
                if c in seen:
                    continue
                seen.add(c)
                own = match_cell.get(c)
                if own is None:
                    cell = c
                    for ss, _ in reversed(stack):
                        prev = match_slot[ss]
                        match_slot[ss] = cell
                        match_cell[cell] = ss
                        cell = prev
                    return True
                stack.append((own, iter(adj[slot_line[own]])))
                break
            else:
                stack.pop()
        return False

    slot_line = [k for k in range(len(alive)) for _ in (0, 1)]
    match_slot = [None] * len(slot_line)
    match_cell = {}
    for s in range(len(slot_line)):
        if not augment(s, slot_line, match_slot, match_cell):
            return -1
    best = cap
    for k in range(len(alive)):
        sl = slot_line + [k] * best
        ms = match_slot + [None] * best
        mc = dict(match_cell)
        got = 0
        for j in range(best):
            if augment(len(slot_line) + j, sl, ms, mc):
                got += 1
            else:
                break
        best = min(best, got)
        if best == 0:
            break
    return best


def met(cells_):
    s = set()
    for c in cells_:
        s.update(THROUGH[c])
    return s


def part_a1_classes():
    seen, reps = set(), []
    diag_cells = [sorted(c for c in DCELLS if DIAG_OF[c] == li) for li in DIAGS]
    for combo in product(*diag_cells):
        key = min(tuple(sorted(apply_sym(g, c) for c in combo)) for g in SYMS)
        if key not in seen:
            seen.add(key)
            reps.append(combo)
    return reps


def greedy_reply(breaker, occupied):
    used = {DIAG_OF[b] for b in breaker}
    k = met(breaker)
    cand = [c for c in DCELLS if c not in occupied and DIAG_OF[c] not in used]
    return min(cand, key=lambda c: (-sum(1 for li in THROUGH[c] if li not in k), CELLS[c]))


def part_a2_tree():
    finals = {}

    def rec(r, breaker, maker_diag):
        if r > 4:
            key = tuple(sorted(breaker))
            finals[key] = finals.get(key, 0) + 1
            return
        for m in [c for c in DCELLS if c not in maker_diag and c not in breaker] + [None]:
            md = maker_diag | ({m} if m is not None else set())
            rec(r + 1, breaker + [greedy_reply(breaker, md | set(breaker))], md)

    rec(2, [IDX[(5, 5, 5)]], set())
    return finals


def part_b_classes():
    pairs = [(a, b) for a, b in combinations(DCELLS, 2)
             if DIAG_OF[a] != DIAG_OF[b] and not set(THROUGH[a]) & set(THROUGH[b])]
    partners = {c: sum(1 for p in pairs if c in p) for c in DCELLS}
    classes = {}
    for m1 in range(NC):
        if m1 == CENTRE:
            continue
        for a, b in pairs:
            if m1 in (a, b):
                continue
            key = min((apply_sym(g, m1), tuple(sorted((apply_sym(g, a), apply_sym(g, b))))) for g in SYMS)
            classes.setdefault(key, (m1, a, b))
    return pairs, partners, sorted(classes.values())


def job_a1(combo):
    return [CELLS[c] for c in combo], len(met(combo)), surplus(list(combo), [CENTRE], 4)


def job_b(t):
    m1, a, b = t
    return CELLS[m1], [CELLS[a], CELLS[b]], len(met([CENTRE, a, b])), surplus([CENTRE, a, b], [m1], 3)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=3)
    ap.add_argument("--out", default="results/surplus_python.json")
    args = ap.parse_args()
    t0 = time.time()
    out = {"n": N, "lines": len(LINES)}
    with Pool(args.workers) as pool:
        reps = part_a1_classes()
        print(f"[A1] {len(reps)} symmetry classes of one-cell-per-diagonal Breaker sets", flush=True)
        a1 = []
        for i, r in enumerate(pool.imap(job_a1, reps)):
            a1.append(r)
            if (i + 1) % 10 == 0:
                print(f"  A1 {i + 1}/{len(reps)}  ({time.time() - t0:.0f}s)", flush=True)
        ok_a1 = all(s >= 3 for _, k, s in a1 if k >= 26)
        hist = {}
        for _, k, s in a1:
            hist[f"met={k},sigma={s}"] = hist.get(f"met={k},sigma={s}", 0) + 1
        print(f"[A1] classes by (lines met, sigma capped at 4): {hist}", flush=True)
        print(f"[A1] all classes meeting >= 26 lines have sigma >= 3: {ok_a1}", flush=True)
        finals = part_a2_tree()
        ok_a2 = all(len(met(k)) == 27 and len({DIAG_OF[c] for c in k}) == 4 for k in finals)
        print(f"[A2] greedy pattern tree: {sum(finals.values())} leaves, {len(finals)} distinct final "
              f"Breaker sets, all one-per-diagonal meeting 27 lines: {ok_a2}", flush=True)
        a2_direct = [(sorted(CELLS[c] for c in k), surplus(list(k), [CENTRE], 4)) for k in finals]
        ok_a2b = all(s >= 3 for _, s in a2_direct)
        print(f"[A2] direct surplus of the {len(finals)} reachable sets >= 3: {ok_a2b}", flush=True)
        pairs, partners, breps = part_b_classes()
        print(f"[B] {len(pairs)} compatible (a,b) pairs; partners per diagonal cell: "
              f"{sorted(set(partners.values()))}; {len(breps)} symmetry classes of (m1,{{a,b}})", flush=True)
        bres = []
        for i, r in enumerate(pool.imap(job_b, breps, chunksize=4)):
            bres.append(r)
            if (i + 1) % 100 == 0:
                print(f"  B {i + 1}/{len(breps)}  ({time.time() - t0:.0f}s)", flush=True)
        ok_b = all(s >= 2 for *_, s in bres)
        hb = {}
        for _, _, k, s in bres:
            hb[f"met={k},sigma={s}"] = hb.get(f"met={k},sigma={s}", 0) + 1
        print(f"[B] classes by (lines met, sigma capped at 3): {hb}", flush=True)
        print(f"[B] all classes have sigma >= 2: {ok_b}", flush=True)
    out.update({
        "A1_classes": len(a1), "A1_histogram": hist, "A1_ok": ok_a1,
        "A2_leaves": sum(finals.values()), "A2_final_sets": [s for s, _ in a2_direct],
        "A2_final_sigma": [s for _, s in a2_direct], "A2_ok": ok_a2 and ok_a2b,
        "B_pairs": len(pairs), "B_partner_counts": sorted(set(partners.values())),
        "B_classes": len(bres), "B_histogram": hb, "B_ok": ok_b,
        "seconds": round(time.time() - t0, 1),
    })
    out["THEOREM_VERIFIED"] = bool(ok_a1 and ok_a2 and ok_a2b and ok_b and min(partners.values()) >= 4)
    with open(args.out, "w") as f:
        json.dump(out, f, indent=1)
    print("THEOREM_VERIFIED =", out["THEOREM_VERIFIED"], f"({out['seconds']}s)")
    return 0 if out["THEOREM_VERIFIED"] else 1


if __name__ == "__main__":
    sys.exit(main())
