#!/usr/bin/env python3
"""Replay the Basic patch with an additional simple-boundary-cycle test at every level.

Geometry comes from the original exact refined-grid checker. The boundary-cycle
test uses edge incidence and vertex degrees, independently of its vertex-fan and
Euler-characteristic tests. This is not an independent geometry reconstruction.
"""
from pathlib import Path
import sys

from boundary import boundary_cycle
from check_marked import corners

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / 'basic'))
import check_corona


def controls():
  def square_set(cells):
    return [corners('sq', c) for c in cells]

  boundary_cycle(square_set([(0, 0)]))
  boundary_cycle(square_set([(0, 0), (1, 0)]))
  bad = [
    [(0, 0), (1, 1)],  # two disks meeting at a single point
    [(0, 0), (2, 0)],  # disconnected disks
    [(x, y) for x in range(3) for y in range(3) if (x, y) != (1, 1)],  # hole
  ]
  for cells in bad:
    try:
      boundary_cycle(square_set(cells))
    except AssertionError:
      continue
    raise AssertionError('invalid topology accepted')
  print('Topology controls: 2 disks accepted; pinch, disconnected union and hole rejected', flush=True)


def main():
  if not __debug__:
    raise SystemExit('FAIL: verification requires Python assertions enabled')
  controls()
  original = check_corona.check_disk

  def check_disk(complex_, faces, level):
    original(complex_, faces, level)
    count = boundary_cycle([check_corona.cyclic(list(face[2])) for face in faces])
    print(f'U_{level}: one simple boundary cycle, {count} edges', flush=True)

  check_corona.check_disk = check_disk
  check_corona.main(str(HERE / 'basic/basic_patch.json'))


if __name__ == '__main__':
  main()
