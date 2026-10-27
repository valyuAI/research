#!/usr/bin/env python3
"""Convert an encoder result (orientation index + lattice translation) into the
independent checker's witness format (exact integer coordinates)."""
import json, sys
sys.path.insert(0, __import__('os').path.dirname(__file__))
import thd, heesch_enc


def to_checker_pt4(p):
  # 4x lattice coordinates -> checker coordinates (X, Y) = (2 X4 + Y4, Y4)
  return [2 * p[0] + p[1], p[1]]


def main(tile_json, res_json, out):
  tile = [tuple(a) for a in json.load(open(tile_json))['atoms']]
  thd.register_region(80)
  tile = heesch_enc.recentre(tile)
  R = json.load(open(res_json))
  hexes, drafters = [], []
  for a in tile:
    if a[0] == 'H':
      hexes.append(to_checker_pt4((a[1], a[2])))
    else:
      drafters.append([to_checker_pt4(p) for p in thd.DRAFTER_CORNERS[a]])
  pls = []
  for pl in R['placements']:
    a, b, d, e = thd.ORIENTS[pl['orient']]
    # L = C M C^{-1}, C = [[8,4],[0,4]], C^{-1} = (1/32) [[4,-4],[0,8]]
    C = [[8, 4], [0, 4]]
    M = [[a, b], [d, e]]
    Ci = [[4, -4], [0, 8]]
    CM = [[sum(C[i][k] * M[k][j] for k in range(2)) for j in range(2)] for i in range(2)]
    L = [[sum(CM[i][k] * Ci[k][j] for k in range(2)) for j in range(2)] for i in range(2)]
    tx, ty = pl['t']
    pls.append({'L': L, 'den': 32, 'T': [8 * tx + 4 * ty, 4 * ty], 'level': pl['level']})
  json.dump({'tile': {'hexagons': hexes, 'drafters': drafters}, 'placements': pls}, open(out, 'w'))
  print(f'wrote {out}: {len(hexes)} hexagons, {len(drafters)} drafters, {len(pls)} placements')


if __name__ == '__main__':
  main(*sys.argv[1:4])
