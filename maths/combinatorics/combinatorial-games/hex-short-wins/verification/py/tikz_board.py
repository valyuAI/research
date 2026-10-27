"""Emit TikZ code for a Hex board with stones, labels and a highlighted path.

Cell (r, c), 0-based, has centre x = c + r/2, y = -r*sqrt(3)/2 (rows shift
right), so its six neighbours are the standard Hex neighbours used everywhere
in this project.  Blue joins the top and bottom rows.
"""
import math


def hexagon(cx, cy, s):
    pts = []
    for k in range(6):
        a = math.radians(90 + 60 * k)
        pts.append((cx + s * math.cos(a), cy + s * math.sin(a)))
    return pts


def board_tikz(n, blue=(), red=(), labels=None, path=(), scale=0.55, numbers=None):
    """blue/red/path: iterables of 0-based (r, c); labels: {(r,c): text};
    numbers: {(r,c): text} printed inside stones."""
    labels = labels or {}
    numbers = numbers or {}
    s = 1 / math.sqrt(3)
    out = [f"\\begin{{tikzpicture}}[scale={scale}]"]
    blue, red, path = set(blue), set(red), set(path)
    for r in range(n):
        for c in range(n):
            cx, cy = c + r / 2, -r * math.sqrt(3) / 2
            pts = hexagon(cx, cy, s)
            poly = " -- ".join(f"({x:.3f},{y:.3f})" for x, y in pts) + " -- cycle"
            fill = "white"
            if (r, c) in blue:
                fill = "blue!55" if (r, c) in path else "blue!20"
            elif (r, c) in red:
                fill = "red!35"
            out.append(f"\\filldraw[fill={fill},draw=black!50,line width=0.3pt] {poly};")
            txt = numbers.get((r, c), labels.get((r, c)))
            if txt:
                out.append(f"\\node[font=\\scriptsize] at ({cx:.3f},{cy:.3f}) {{{txt}}};")
    # edge markers: thick blue lines along top and bottom, red along sides
    top_y = s + 0.08
    out.append(f"\\draw[blue!70,line width=1.6pt] ({-0.5:.3f},{top_y:.3f}) -- ({n - 0.5:.3f},{top_y:.3f});")
    by = -(n - 1) * math.sqrt(3) / 2 - s - 0.08
    bx = (n - 1) / 2
    out.append(f"\\draw[blue!70,line width=1.6pt] ({bx - 0.5:.3f},{by:.3f}) -- ({bx + n - 0.5:.3f},{by:.3f});")
    dx, dy = 0.5, -math.sqrt(3) / 2          # direction down a column
    px, py = -math.sqrt(3) / 2, -0.5         # outward normal on the left side
    for col, sgn in ((0, 1), (n - 1, -1)):
        x0, y0 = col, 0.0
        x1, y1 = col + (n - 1) / 2, -(n - 1) * math.sqrt(3) / 2
        a = (x0 - 0.55 * dx + sgn * 0.62 * px, y0 - 0.55 * dy + sgn * 0.62 * py)
        b = (x1 + 0.55 * dx + sgn * 0.62 * px, y1 + 0.55 * dy + sgn * 0.62 * py)
        out.append(f"\\draw[red!70,line width=1.6pt] ({a[0]:.3f},{a[1]:.3f}) -- ({b[0]:.3f},{b[1]:.3f});")
    out.append("\\end{tikzpicture}")
    return "\n".join(out)
