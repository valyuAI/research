"""Exact boundary-cycle test, independent of Euler-characteristic calculations."""
from collections import Counter, defaultdict


def boundary_cycle(polygons):
  edges = Counter()
  for points in polygons:
    for a, b in zip(points, points[1:] + points[:1]):
      edges[frozenset((a, b))] += 1
  assert edges and all(len(e) == 2 and n in (1, 2) for e, n in edges.items()), 'invalid face incidence'
  adjacency = defaultdict(set)
  for edge, count in edges.items():
    if count == 1:
      a, b = tuple(edge)
      adjacency[a].add(b)
      adjacency[b].add(a)
  assert adjacency and all(len(v) == 2 for v in adjacency.values()), 'boundary pinch or endpoint'
  start = next(iter(adjacency))
  seen, stack = {start}, [start]
  while stack:
    for point in adjacency[stack.pop()]:
      if point not in seen:
        seen.add(point)
        stack.append(point)
  assert len(seen) == len(adjacency), 'multiple boundary cycles (hole or disconnected component)'
  return len(adjacency)
