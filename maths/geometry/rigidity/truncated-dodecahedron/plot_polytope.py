"""Draw the saved exact polytope without recomputing its convex hull."""

import json
import math
from fractions import Fraction
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

ROOT = Path(__file__).resolve().parent


def main():
  data = json.loads((ROOT / "verification" / "modular-obstruction.json").read_text())
  phi = (1 + math.sqrt(5)) / 2
  points = [[float(Fraction(a)) + phi * float(Fraction(b)) for a, b in row]
    for row in data["vertices"]]
  adjacency = {i: set() for i in range(len(points))}
  for i, j in data["edges"]:
    adjacency[i].add(j)
    adjacency[j].add(i)
  polygons, colors = [], []
  for facet in data["facets"]:
    members = set(facet)
    if any(len(adjacency[i] & members) != 2 for i in facet):
      raise ValueError("Facet is not an original-edge cycle")
    cycle = [min(facet)]
    previous = None
    while True:
      candidates = sorted((adjacency[cycle[-1]] & members) - {previous})
      next_vertex = candidates[0]
      if next_vertex == cycle[0]:
        break
      previous = cycle[-1]
      cycle.append(next_vertex)
      if len(cycle) > len(facet):
        raise ValueError("Invalid facet cycle")
    if set(cycle) != members:
      raise ValueError("Incomplete facet cycle")
    polygons.append([points[i] for i in cycle])
    colors.append("#88b0c0" if len(facet) == 3 else "#e0e8eb")
  fig = plt.figure(figsize=(4, 3.3))
  ax = fig.add_subplot(111, projection="3d", proj_type="ortho")
  ax.add_collection3d(Poly3DCollection(polygons, facecolors=colors,
    edgecolors="#26343a", linewidths=.55, zsort="average"))
  extent = max(abs(v) for point in points for v in point)
  ax.set(xlim=(-extent, extent), ylim=(-extent, extent), zlim=(-extent, extent))
  ax.set_box_aspect((1, 1, 1))
  ax.view_init(elev=19, azim=-38)
  ax.set_axis_off()
  fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
  fig.savefig(ROOT / "truncated-dodecahedron.pdf", bbox_inches="tight", pad_inches=0)
  plt.close(fig)
  print("Saved diagram from 60 vertices and 32 exact facet cycles", flush=True)


if __name__ == "__main__":
  main()
