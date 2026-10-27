"""Explainer: the truncated dodecahedron is rigid.

Every number drawn here comes from data.json, which data_prep.py rebuilds from the
certificate in ../verification/.
"""

import json
from pathlib import Path

import numpy as np
from manim import *
from vrvideo import *

SCENES = ['Hook', 'Solid', 'Counting', 'Arrows', 'Fake', 'SolidFlex', 'Layers', 'Obstruction', 'Clock',
          'Cancel', 'Transfer', 'Status', 'Recap']

HERE = Path(__file__).resolve().parent
D = json.loads((HERE / 'data.json').read_text())

# Colour meaning, used in every scene.
STICK = ManimColor('#dfe3e8')
HINGE = ManimColor('#f4f6f8')
DECAGON = PRIMARY
TRIANGLE = WARM
ARROW = SECONDARY
BAD = WARN
GOOD = OK
CLOCK = ACCENT
DARK = ManimColor('#0b0d10')

V0 = np.array(D['vertices'])
FACES = D['faces']
FLEX = np.array(D['flex']['vertex_arrows'])
BASIS = np.array(D['flex']['basis_vertex_arrows'])
W2 = np.array(D['flex']['second_order_vertices'])
CAM = np.array([0.0, 0.0, 20.0])
LIGHT = np.array([-0.45, 0.7, 1.0]) / np.linalg.norm([-0.45, 0.7, 1.0])
RATE = 0.12  # slow turn of the solids, radians per second


def leftover_boxes():
  boxes = VGroup(*[MathTex(f'C_{k}(v)', color=ARROW).scale(1.25) for k in range(1, 5)]).arrange(RIGHT, buff=1.1)
  frames = VGroup(*[SurroundingRectangle(b, color=ARROW, buff=0.25, corner_radius=0.1) for b in boxes])
  return VGroup(boxes, frames)


class Poly:
  def __init__(self, faces):
    self.faces = faces
    ef = {}
    for k, f in enumerate(faces):
      for a, b in zip(f, f[1:] + f[:1]):
        ef.setdefault((min(a, b), max(a, b)), []).append(k)
    self.edges = sorted(ef)
    self.edge_faces = ef


TD = Poly(FACES)
assert len(TD.edges) == 90 and all(len(v) == 2 for v in TD.edge_faces.values())
CUBE = Poly([[0, 1, 3, 2], [4, 5, 7, 6], [0, 1, 5, 4], [2, 3, 7, 6], [0, 2, 6, 4], [1, 3, 7, 5]])
REST = {e: np.linalg.norm(V0[e[0]] - V0[e[1]]) for e in TD.edges}


def rotation(yaw, tilt=0.42):
  cy, sy = np.cos(yaw), np.sin(yaw)
  ry = np.array([[cy, 0, sy], [0, 1, 0], [-sy, 0, cy]])
  ct, st = np.cos(tilt), np.sin(tilt)
  rx = np.array([[1, 0, 0], [0, ct, -st], [0, st, ct]])
  return rx @ ry


def pose(X, yaw, scale, offset, tilt=0.42):
  return (X * scale) @ rotation(yaw, tilt).T + np.asarray(offset, dtype=float)


def shade(color, n):
  k = 0.3 + 0.7 * max(0.0, float(n @ LIGHT))
  return interpolate_color(DARK, ManimColor(color), k)


def segments(A, B, color, width, alpha=1.0):
  """Many straight segments as one stroke-only VMobject (much cheaper than one Line each)."""
  A, B = np.asarray(A, dtype=float), np.asarray(B, dtype=float)
  vm = VMobject(stroke_color=color, stroke_width=width, stroke_opacity=alpha, fill_opacity=0)
  if len(A):
    pts = np.empty((4 * len(A), 3))
    pts[0::4], pts[1::4], pts[2::4], pts[3::4] = A, A + (B - A) / 3, A + 2 * (B - A) / 3, B
    vm.set_points(pts)
  return vm


def triangles(T, color, alpha=1.0):
  """Filled triangles (k x 3 x 3) as one VMobject."""
  vm = VMobject(stroke_width=0, fill_color=color, fill_opacity=alpha)
  if len(T):
    pts = []
    for a, b, c in T:
      for p, q in ((a, b), (b, c), (c, a)):
        pts += [p, p + (q - p) / 3, p + 2 * (q - p) / 3, q]
    vm.set_points(np.array(pts))
  return vm


def draw_poly(poly, P, mode='3d', face_color=lambda k: PRIMARY, opacity=1.0, edge_colors=None,
              edge_width=2.2, alpha=1.0):
  """Faces facing the viewer (shaded) plus their edges. Returns (group, visible vertex set)."""
  center = P.mean(axis=0)
  faces_g, edges_g, visible = VGroup(), VGroup(), []
  for k, f in enumerate(poly.faces):
    pts = P[f]
    c = pts.mean(axis=0)
    n = np.cross(pts[1] - pts[0], pts[2] - pts[0])
    n = n / np.linalg.norm(n)
    if n @ (c - center) < 0:
      n = -n
    view = (CAM - c) if mode == '3d' else OUT
    visible.append(bool(n @ view > 0))
    if not visible[-1]:
      continue
    q = pts.copy()
    if mode == '2d':
      q[:, 2] = 0
    faces_g.add(Polygon(*q, stroke_width=0, fill_color=shade(face_color(k), n), fill_opacity=opacity * alpha))
  verts = set()
  for k, f in enumerate(poly.faces):
    if visible[k]:
      verts.update(f)
  bins = {}
  for e in poly.edges:
    if not any(visible[k] for k in poly.edge_faces[e]):
      continue
    a, b = P[e[0]].copy(), P[e[1]].copy()
    if mode == '2d':
      a[2] = b[2] = 0
    col = edge_colors[e] if edge_colors is not None else 0.0
    bins.setdefault(round(col * 8) / 8, []).append((a, b))
  for level, segs in sorted(bins.items()):
    col = interpolate_color(STICK, ManimColor(BAD), level)
    edges_g.add(segments([a for a, _ in segs], [b for _, b in segs], col, edge_width, alpha))
  return VGroup(faces_g, edges_g), verts


def td_color(highlight=None, amount=1.0):
  def f(k):
    base = DECAGON if len(FACES[k]) == 10 else TRIANGLE
    if highlight is not None and k == highlight:
      return interpolate_color(ManimColor(base), ManimColor(ARROW), amount)
    return base
  return f


def flat(p):
  p = np.array(p, dtype=float)
  p[2] = 0
  return p


def draw_arrows(P, U, verts, project, color=ARROW, min_len=0.05, width=3.5, alpha=1.0, tip=0.13):
  starts, ends, tips = [], [], []
  for i in sorted(verts):
    a, b = project(P[i]), project(P[i] + U[i])
    L = np.linalg.norm(b - a)
    if L < min_len:
      continue
    d = (b - a) / L
    n = np.array([-d[1], d[0], 0.0])
    h = min(tip, 0.45 * L)
    base = b - h * d
    starts.append(a)
    ends.append(base)
    tips.append((b, base + 0.55 * h * n, base - 0.55 * h * n))
  return VGroup(segments(starts, ends, color, width, alpha), triangles(tips, color, alpha))


def solid_icon(yaw=0.5, scale=0.5, center=ORIGIN, X=V0, tilt=0.42, edge_width=1.6):
  P = pose(X, yaw, scale, center, tilt)
  return draw_poly(TD, P, mode='2d', face_color=td_color(), edge_width=edge_width)[0]


def cube_points(shear=0.0, half=1.0):
  up = np.array([np.sin(shear), np.cos(shear), 0.0])
  pts = []
  for x in (-half, half):
    for y in (-half, half):
      for z in (-half, half):
        pts.append(np.array([x, 0, z]) + y * up)
  return np.array(pts)


def cube_icon(shear=0.0, half=0.7, center=ORIGIN, yaw=0.6):
  P = pose(cube_points(shear, half), yaw, 1.0, center, 0.45)
  return draw_poly(CUBE, P, mode='2d', face_color=lambda k: SOFT, edge_width=2.5)[0]


def frame2d(pts, closed=True, color=STICK, width=8, radius=0.09):
  g = VGroup()
  n = len(pts)
  for k in range(n if closed else n - 1):
    g.add(Line(pts[k], pts[(k + 1) % n], color=color, stroke_width=width))
  for p in pts:
    g.add(Dot(p, radius=radius, color=HINGE))
  return g


def txt(s, scale=0.7, color=INK):
  return Tex(s, color=color).scale(scale)


def mtx(s, scale=0.8, color=INK):
  return MathTex(s, color=color).scale(scale)


def count_row(items, scale=1.0):
  """items: (tex, label or None, colour). Numbers sit on one line, labels underneath."""
  cols = VGroup()
  for tex_s, lab, col in items:
    num = MathTex(tex_s, color=col).scale(1.05 * scale)
    if lab:
      cols.add(VGroup(num, Tex(lab, color=MUTED).scale(0.55).next_to(num, DOWN, buff=0.22)))
    else:
      cols.add(VGroup(num))
  cols.arrange(RIGHT, buff=0.32)
  y0 = cols[0][0].get_center()[1]
  for c in cols:
    c.shift(UP * (y0 - c[0].get_center()[1]))
  return cols


class Scene2D(NarratedScene):
  pause_after = 0.3

  def clear_all(self, run_time=0.5):
    mobs = [m for m in self.mobjects if not isinstance(m, ValueTracker)]
    if mobs:
      self.play(*[FadeOut(m) for m in mobs], run_time=run_time)


class Scene3D(NarratedThreeDScene):
  pause_after = 0.3

  def spin(self, start=0.3):
    yaw = ValueTracker(start)
    yaw.add_updater(lambda m, dt: m.increment_value(RATE * dt))
    self.add(yaw)
    return yaw

  def project(self, p):
    return flat(self.camera.project_point(np.asarray(p, dtype=float)))


# 1 ------------------------------------------------------------------------------------------
class Hook(Scene2D):
  def construct(self):
    s = 1.3
    theta = ValueTracker(0.0)
    base = np.array([-3.4, -0.75, 0])

    def sq_pts():
      th = theta.get_value()
      up = 2 * s * np.array([np.sin(th), np.cos(th), 0])
      bl, br = base + LEFT * s, base + RIGHT * s
      return [bl, br, br + up, bl + up]

    square = always_redraw(lambda: frame2d(sq_pts()))
    push = always_redraw(lambda: Arrow(sq_pts()[3] + LEFT * 1.3, sq_pts()[3] + LEFT * 0.2, buff=0,
                                       color=ARROW, stroke_width=6))
    with self.say('s01_square') as d:
      self.play(Create(square), run_time=0.15 * d)
      self.play(FadeIn(push), run_time=0.07 * d)
      self.play(theta.animate.set_value(0.5), run_time=0.18 * d)
      self.play(theta.animate.set_value(-0.38), run_time=0.2 * d)
      self.play(theta.animate.set_value(0.22), run_time=0.15 * d)
      self.play(theta.animate.set_value(0), run_time=0.12 * d)
      lab_sq = txt('wobbles', 0.8, ARROW).move_to(base + DOWN * 0.6)
      self.play(FadeIn(lab_sq), FadeOut(push), run_time=0.08 * d)

    tri_base = np.array([3.4, -0.75, 0])
    side = 2.8
    tri_pts = [tri_base + LEFT * side / 2, tri_base + RIGHT * side / 2, tri_base + UP * side * np.sqrt(3) / 2]
    tri = frame2d(tri_pts)
    with self.say('s01_triangle') as d:
      self.play(Create(tri), run_time=0.25 * d)
      p2 = Arrow(tri_pts[2] + LEFT * 1.4, tri_pts[2] + LEFT * 0.2, buff=0, color=ARROW, stroke_width=6)
      self.play(GrowArrow(p2), run_time=0.15 * d)
      for _ in range(2):
        self.play(p2.animate.shift(RIGHT * 0.12), run_time=0.1 * d, rate_func=there_and_back)
      lab_tri = txt('keeps its shape', 0.8).move_to(tri_base + DOWN * 0.6)
      self.play(FadeIn(lab_tri), FadeOut(p2), run_time=0.12 * d)

    with self.say('s01_rigid') as d:
      self.play(tri.animate.shift(UP * 0.35 + RIGHT * 0.25).rotate(0.35), run_time=0.2 * d)
      self.play(tri.animate.shift(DOWN * 0.35 + LEFT * 0.25).rotate(-0.35), run_time=0.15 * d)
      self.play(Transform(lab_tri, txt('rigid', 0.85, GOOD).move_to(lab_tri)), run_time=0.1 * d)
      xs = np.linspace(-4.2, 4.2, 6)
      bottom = [np.array([x, -3.25, 0]) for x in xs]
      top = [np.array([(a + b) / 2, -2.25, 0]) for a, b in zip(xs, xs[1:])]
      truss = VGroup()
      for a, b in zip(bottom, bottom[1:]):
        truss.add(Line(a, b, color=MUTED, stroke_width=4))
      for a, b in zip(top, top[1:]):
        truss.add(Line(a, b, color=MUTED, stroke_width=4))
      for k, t in enumerate(top):
        truss.add(Line(bottom[k], t, color=MUTED, stroke_width=4), Line(t, bottom[k + 1], color=MUTED, stroke_width=4))
      self.play(Create(truss), run_time=0.35 * d)


# 2 ------------------------------------------------------------------------------------------
class Solid(Scene3D):
  def construct(self):
    yaw = self.spin(0.55)
    shear = ValueTracker(0.0)
    cube_a = ValueTracker(0.0)
    cube_c = np.array([-2.7, 0.1, 0])
    cube = always_redraw(lambda: draw_poly(CUBE, pose(cube_points(shear.get_value(), 1.3), yaw.get_value(), 1.0,
                                                      cube_c, 0.45), face_color=lambda k: SOFT,
                                           edge_width=3.5, alpha=cube_a.get_value())[0])
    self.add(cube)
    rules = VGroup(txt(r'sticks keep their lengths', 0.72),
                   txt(r'faces stay flat, but may change shape', 0.72)).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
    rules.move_to(RIGHT * 3.3 + UP * 1.0)
    with self.say('s02_box') as d:
      self.play(cube_a.animate.set_value(1.0), run_time=0.2 * d)
      self.wait(0.15 * d)
      self.play(Write(rules[0]), run_time=0.2 * d)
      self.wait(0.1 * d)
      self.play(Write(rules[1]), run_time=0.25 * d)

    with self.say('s02_lean') as d:
      self.play(shear.animate.set_value(0.55), run_time=0.35 * d)
      lean = txt('still wobbles', 0.8, ARROW).move_to(RIGHT * 3.3 + DOWN * 0.6)
      self.play(FadeIn(lean), shear.animate.set_value(-0.35), run_time=0.35 * d)
      self.play(shear.animate.set_value(0.3), run_time=0.25 * d)

    hl = {'face': None}
    hl_amt = ValueTracker(0.0)
    td_a = ValueTracker(0.0)
    tdc = np.array([-2.4, 0.0, 0])
    solid = always_redraw(lambda: draw_poly(TD, pose(V0, yaw.get_value(), 0.78, tdc),
                                            face_color=td_color(hl['face'], hl_amt.get_value()),
                                            alpha=td_a.get_value())[0])
    counts = VGroup(
      Tex(r'60 corners \quad 90 sticks').scale(0.75),
      Tex(r'20 ', r'triangles', r' \quad 12 ', r'decagons').scale(0.75)).arrange(DOWN, buff=0.35)
    counts[1][1].set_color(TRIANGLE)
    counts[1][3].set_color(DECAGON)
    counts.move_to(RIGHT * 3.6 + UP * 0.3)
    with self.say('s02_meet') as d:
      self.play(cube_a.animate.set_value(0.0), FadeOut(rules), FadeOut(lean), run_time=0.12 * d)
      self.remove(cube)
      self.add(solid)
      self.play(td_a.animate.set_value(1.0), run_time=0.2 * d)
      self.play(Write(counts[0]), run_time=0.25 * d)
      self.play(Write(counts[1]), run_time=0.3 * d)

    # The decagon facing the viewer most directly right now.
    R = rotation(yaw.get_value() + 0.4)
    best, best_z = None, -2
    for k, f in enumerate(FACES):
      if len(f) == 10:
        n = (V0[f].mean(axis=0) @ R.T)
        nz = n[2] / np.linalg.norm(n)
        if nz > best_z:
          best, best_z = k, nz
    hl['face'] = best
    flexer = ValueTracker(0.0)

    def decagon_ring():
      s = flexer.get_value()
      angles = np.radians(np.arange(5) * 36 + s * np.array([0, 14, -9, 9, -5]))
      dirs = [np.array([np.cos(a), np.sin(a), 0]) for a in angles]
      edges = dirs + [-v for v in dirs]
      pts, p = [], np.zeros(3)
      for e in edges:
        pts.append(p.copy())
        p = p + 0.62 * e
      pts = np.array(pts)
      pts -= pts.mean(axis=0)
      return frame2d(list(pts + np.array([3.7, 0.6, 0])), width=5, radius=0.06).set_color(ARROW)

    ring = always_redraw(decagon_ring)
    ring_lab = txt('one decagon on its own', 0.62, MUTED).move_to(RIGHT * 3.7 + DOWN * 1.35)
    with self.say('s02_ask') as d:
      self.play(FadeOut(counts), hl_amt.animate.set_value(1.0), run_time=0.15 * d)
      self.play(FadeIn(ring), FadeIn(ring_lab), run_time=0.12 * d)
      self.play(flexer.animate.set_value(1.0), run_time=0.15 * d)
      self.play(flexer.animate.set_value(-1.0), run_time=0.18 * d)
      self.play(flexer.animate.set_value(0.0), run_time=0.12 * d)
      q = MathTex('?', color=ARROW).scale(2.4).move_to(RIGHT * 3.7 + DOWN * 2.6)
      self.play(FadeIn(q, scale=0.6), hl_amt.animate.set_value(0.0), run_time=0.12 * d)

    with self.say('s02_open') as d:
      self.play(FadeOut(ring), FadeOut(ring_lab), FadeOut(q), run_time=0.1 * d)
      news = VGroup(txt('31 famous solids tested in 2026', 0.7),
                    txt('only this one undecided', 0.7, MUTED)).arrange(DOWN, buff=0.3).move_to(RIGHT * 3.6 + UP * 0.4)
      self.play(FadeIn(news[0]), run_time=0.15 * d)
      self.play(FadeIn(news[1]), run_time=0.15 * d)
      self.wait(0.2 * d)
      ans = txt('answer: it cannot wobble', 0.75, GOOD).move_to(RIGHT * 3.6 + DOWN * 1.2)
      self.play(FadeIn(ans), run_time=0.15 * d)
    self.play(td_a.animate.set_value(0.0), FadeOut(news), FadeOut(ans), run_time=0.6)


# 3 ------------------------------------------------------------------------------------------
class Counting(Scene2D):
  def construct(self):
    s = 0.75
    sq_c = np.array([-4.6, 1.5, 0])
    sq_pts = [sq_c + np.array(v) * s for v in [(-1, -1, 0), (1, -1, 0), (1, 1, 0), (-1, 1, 0)]]
    square = frame2d(sq_pts, width=6, radius=0.07)
    row1 = count_row([('8', 'numbers', INK), ('-', None, INK), ('4', 'sticks', INK), ('-', None, INK),
                      ('3', 'slides, turn', INK), ('=', None, INK), ('1', 'wobble', ARROW)])
    row1.move_to(RIGHT * 1.0 + UP * 1.35)
    coords = VGroup(*[mtx(r'(x, y)', 0.55, MUTED).next_to(p, d, buff=0.12)
                      for p, d in zip(sq_pts, [DL, DR, UR, UL])])
    with self.say('s03_square') as d:
      self.play(Create(square), run_time=0.12 * d)
      self.play(FadeIn(coords), run_time=0.12 * d)
      self.play(FadeIn(row1[0]), run_time=0.12 * d)
      self.play(FadeOut(coords), FadeIn(row1[1]), FadeIn(row1[2]), run_time=0.2 * d)
      self.play(FadeIn(row1[3]), FadeIn(row1[4]), run_time=0.12 * d)
      self.play(square.animate.shift(RIGHT * 0.4), run_time=0.07 * d, rate_func=there_and_back)
      self.play(square.animate.shift(UP * 0.3), run_time=0.07 * d, rate_func=there_and_back)
      self.play(Rotate(square, 0.4), run_time=0.07 * d, rate_func=there_and_back)

    tri_c = np.array([-4.6, -1.7, 0])
    tri_pts = [tri_c + np.array(v) for v in [(-0.85, -0.6, 0), (0.85, -0.6, 0), (0, 0.87, 0)]]
    tri = frame2d(tri_pts, width=6, radius=0.07)
    row2 = count_row([('6', 'numbers', INK), ('-', None, INK), ('3', 'sticks', INK), ('-', None, INK),
                      ('3', 'slides, turn', INK), ('=', None, INK), ('0', 'rigid', GOOD)])
    row2.move_to(RIGHT * 1.0 + DOWN * 1.75)
    row2.align_to(row1, LEFT)
    with self.say('s03_left') as d:
      self.play(FadeIn(row1[5]), FadeIn(row1[6]), run_time=0.15 * d)
      self.play(Indicate(row1[6][0], color=ARROW), run_time=0.15 * d)
      self.play(Create(tri), run_time=0.12 * d)
      self.play(LaggedStart(*[FadeIn(c) for c in row2[:5]], lag_ratio=0.3), run_time=0.3 * d)
      self.play(FadeIn(row2[5]), FadeIn(row2[6]), run_time=0.12 * d)

    icon = solid_icon(0.5, 0.37, np.array([-5.0, 1.2, 0]))
    row3 = count_row([(r'60 \times 3', 'corners', INK), ('+', None, INK), (r'32 \times 3', 'face planes', INK),
                      ('=', None, INK), ('276', 'numbers', INK)])
    row3.move_to(RIGHT * 1.4 + UP * 1.3)
    plane_note = txt(r'a plane: 2 numbers for its tilt, 1 for its position', 0.58, MUTED).move_to(RIGHT * 1.4 + DOWN * 0.2)
    with self.say('s03_solid') as d:
      self.play(FadeOut(VGroup(square, row1, tri, row2)), run_time=0.15 * d)
      self.play(FadeIn(icon), run_time=0.15 * d)
      self.play(FadeIn(row3[0]), run_time=0.15 * d)
      self.play(FadeIn(row3[1]), FadeIn(row3[2]), FadeIn(plane_note), run_time=0.2 * d)
      self.play(FadeIn(row3[3]), FadeIn(row3[4]), run_time=0.15 * d)

    row4 = count_row([('276', 'numbers', INK), ('-', None, INK), ('90', 'sticks', INK), ('-', None, INK),
                      ('180', r'corner on face', INK), ('-', None, INK), ('6', 'slides, turns', INK),
                      ('=', None, INK), ('0', None, GOOD)])
    row4.move_to(RIGHT * 1.4 + DOWN * 0.6)
    note180 = mtx(r'180 = 20 \times 3 + 12 \times 10', 0.6, MUTED).next_to(row4, DOWN, buff=0.35)
    with self.say('s03_rules') as d:
      self.play(FadeOut(plane_note), run_time=0.08 * d)
      self.play(FadeIn(row4[0]), FadeIn(row4[1]), FadeIn(row4[2]), run_time=0.15 * d)
      self.play(FadeIn(row4[3]), FadeIn(row4[4]), FadeIn(note180), run_time=0.25 * d)
      self.play(FadeIn(row4[5]), FadeIn(row4[6]), run_time=0.2 * d)
      self.play(FadeIn(row4[7]), FadeIn(row4[8]), run_time=0.15 * d)

    cube = cube_icon(0.0, 0.62, np.array([-5.0, -1.95, 0]))
    row5 = count_row([('42', 'numbers', INK), ('-', None, INK), ('12', 'sticks', INK), ('-', None, INK),
                      ('24', 'corner on face', INK), ('-', None, INK), ('6', 'slides, turns', INK),
                      ('=', None, INK), ('0', None, INK)])
    row5.move_to(RIGHT * 1.4 + DOWN * 1.9)
    with self.say('s03_lie') as d:
      self.play(FadeOut(note180), FadeOut(row3), VGroup(icon, row4).animate.shift(UP * 1.1), run_time=0.12 * d)
      self.play(FadeIn(cube), FadeIn(row5), run_time=0.15 * d)
      self.play(Transform(cube, cube_icon(0.5, 0.62, np.array([-5.0, -1.95, 0]))), run_time=0.1 * d)
      wob = txt('but it wobbles!', 0.7, BAD).next_to(row5, DOWN, buff=0.3)
      self.play(FadeIn(wob), run_time=0.1 * d)
      self.wait(0.12 * d)
      euler = VGroup(txt(r"Euler's formula:", 0.7, MUTED), mtx(r'V - E + F = 2', 0.9)).arrange(RIGHT, buff=0.3)
      euler.move_to(RIGHT * 1.4 + DOWN * 1.3)
      self.play(FadeOut(VGroup(row5, wob, cube)), FadeIn(euler), run_time=0.15 * d)
      always = txt('so the count is always 0: counting can never decide', 0.68, BAD).next_to(euler, DOWN, buff=0.45)
      self.play(FadeIn(always), run_time=0.12 * d)
    self.play(FadeOut(VGroup(icon, row4, euler, always)), run_time=0.5)


# 4 ------------------------------------------------------------------------------------------
class Arrows(Scene2D):
  def construct(self):
    s = 1.2
    base = np.array([-3.6, -1.4, 0])
    theta = ValueTracker(0.0)

    def sq_pts():
      th = theta.get_value()
      up = 2 * s * np.array([np.sin(th), np.cos(th), 0])
      bl, br = base + LEFT * s, base + RIGHT * s
      return [bl, br, br + up, bl + up]

    square = always_redraw(lambda: frame2d(sq_pts()))
    with self.say('s04_arrow') as d:
      self.play(FadeIn(square), run_time=0.12 * d)
      self.play(theta.animate.set_value(0.12), run_time=0.15 * d, rate_func=there_and_back)
      self.wait(0.1 * d)
      tops = sq_pts()[2:]
      arrows = VGroup(*[Arrow(p, p + RIGHT * 1.0, buff=0, color=ARROW, stroke_width=7) for p in tops])
      self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.3), run_time=0.35 * d)

    # One stick and the shadows of its two end arrows.
    A, B = np.array([1.2, -1.6, 0]), np.array([4.8, 0.2, 0])
    u = (B - A) / np.linalg.norm(B - A)
    nrm = np.array([-u[1], u[0], 0])
    a_vec = 0.55 * u + 0.95 * nrm
    along = ValueTracker(1.2)  # along-stick part of B's arrow; 0.55 matches A's
    stick = Line(A, B, color=STICK, stroke_width=8)
    guide = DashedLine(A - u * 1.0, B + u * 1.6, color=MUTED, stroke_width=1.5, dash_length=0.08)
    dots = VGroup(Dot(A, radius=0.09, color=HINGE), Dot(B, radius=0.09, color=HINGE))

    def shadow_group():
      b_vec = along.get_value() * u - 0.7 * nrm
      ok = abs(along.get_value() - 0.55) < 0.02
      col = GOOD if ok else BAD
      g = VGroup()
      for P, v in ((A, a_vec), (B, b_vec)):
        foot = P + (v @ u) * u
        g.add(DashedLine(P + v, foot, color=MUTED, stroke_width=2, dash_length=0.07))
        g.add(Line(P, foot, color=col, stroke_width=10))
        g.add(Arrow(P, P + v, buff=0, color=ARROW, stroke_width=5))
      return g

    shadows = always_redraw(shadow_group)
    verdict = always_redraw(lambda: txt('shadows match: no stretch', 0.62, GOOD).move_to(np.array([3.3, -2.9, 0]))
                            if abs(along.get_value() - 0.55) < 0.02
                            else txt('shadows differ: the stick stretches', 0.62, BAD).move_to(np.array([3.3, -2.9, 0])))
    with self.say('s04_shadow') as d:
      self.play(FadeIn(guide), Create(stick), FadeIn(dots), run_time=0.15 * d)
      self.play(FadeIn(shadows), FadeIn(verdict), run_time=0.15 * d)
      self.wait(0.25 * d)
      self.play(along.animate.set_value(0.55), run_time=0.25 * d)

    with self.say('s04_square') as d:
      self.play(FadeOut(VGroup(guide, stick, dots, shadows, verdict)), run_time=0.1 * d)
      pts = sq_pts()
      zeros = VGroup(*[Dot(p, radius=0.16, color=ARROW, fill_opacity=0.0).set_stroke(ARROW, 3) for p in pts[:2]])
      zlab = VGroup(*[mtx('0', 0.6, ARROW).next_to(p, DOWN, buff=0.25) for p in pts[:2]])
      self.play(FadeIn(zeros), FadeIn(zlab), run_time=0.15 * d)
      ra = VGroup(*[RightAngle(Line(p, p + DOWN), Line(p, p + RIGHT), length=0.25, color=MUTED) for p in pts[2:]])
      self.play(Create(ra), run_time=0.15 * d)
      up_checks = VGroup(*[MathTex(r'\checkmark', color=GOOD).scale(0.9).move_to(base + x * RIGHT * (s + 0.5) + UP * s)
                           for x in (-1, 1)])
      self.play(FadeIn(up_checks), run_time=0.15 * d)
      top_check = MathTex(r'\checkmark', color=GOOD).scale(0.9).move_to(base + UP * (2 * s + 0.45))
      bot_check = MathTex(r'\checkmark', color=GOOD).scale(0.9).move_to(base + DOWN * 0.95)
      self.play(Indicate(arrows, color=ARROW), FadeIn(top_check), run_time=0.15 * d)
      self.play(FadeIn(bot_check), run_time=0.1 * d)

    name = VGroup(txt('infinitesimal flex', 0.95, ARROW),
                  txt(r'first-order test: passed', 0.75, GOOD)).arrange(DOWN, buff=0.35).move_to(RIGHT * 3.2 + UP * 0.2)
    with self.say('s04_name') as d:
      self.play(Write(name[0]), run_time=0.3 * d)
      self.wait(0.25 * d)
      self.play(FadeIn(name[1]), run_time=0.2 * d)
    self.clear_all()


# 5 ------------------------------------------------------------------------------------------
class Fake(Scene2D):
  def construct(self):
    L = 3.4
    y0 = 1.0
    A, B, M = np.array([-L, y0, 0]), np.array([L, y0, 0]), np.array([0, y0, 0])
    lift = ValueTracker(0.0)

    def pin(p):
      tri = Polygon(p, p + np.array([-0.28, -0.42, 0]), p + np.array([0.28, -0.42, 0]),
                    stroke_color=MUTED, fill_color=MUTED, fill_opacity=0.35, stroke_width=2)
      ground = Line(p + np.array([-0.45, -0.45, 0]), p + np.array([0.45, -0.45, 0]), color=MUTED, stroke_width=3)
      return VGroup(tri, ground)

    pins = VGroup(pin(A), pin(B))

    def rods():
      m = M + UP * lift.get_value()
      g = VGroup()
      for P in (A, B):
        v = (m - P) / np.linalg.norm(m - P)
        end = P + L * v
        g.add(Line(P, end, color=STICK, stroke_width=8))
        if np.linalg.norm(m - end) > 0.01:
          g.add(Line(end, m, color=BAD, stroke_width=8))
      g.add(Dot(A, radius=0.09, color=HINGE), Dot(B, radius=0.09, color=HINGE), Dot(m, radius=0.1, color=HINGE))
      return g

    sticks = always_redraw(rods)
    push = Arrow(M, M + UP * 1.3, buff=0, color=ARROW, stroke_width=6)
    with self.say('s05_setup') as d:
      self.play(FadeIn(pins), run_time=0.15 * d)
      self.play(Create(sticks), run_time=0.25 * d)
      self.play(GrowArrow(push), run_time=0.2 * d)

    ra = VGroup(RightAngle(Line(M, M + LEFT), Line(M, M + UP), length=0.28, color=MUTED, quadrant=(1, 1)),
                RightAngle(Line(M, M + RIGHT), Line(M, M + UP), length=0.28, color=MUTED, quadrant=(1, 1)))
    status = txt('shadows: 0 and 0', 0.72, MUTED).move_to(DOWN * 1.2)
    with self.say('s05_pass') as d:
      self.play(Create(ra), FadeIn(status), run_time=0.2 * d)
      self.play(Transform(status, txt(r'first-order test: passed', 0.72, GOOD).move_to(status)), run_time=0.15 * d)
      self.wait(0.1 * d)
      self.play(FadeOut(push), FadeOut(ra), lift.animate.set_value(1.1), run_time=0.25 * d)
      stuck = txt('stuck: the sticks would have to stretch', 0.68, BAD).move_to(DOWN * 2.0)
      self.play(FadeIn(stuck), run_time=0.12 * d)

    with self.say('s05_pyth') as d:
      m = M + UP * 1.1
      tri = VGroup(DashedLine(A, M, color=MUTED, stroke_width=2), DashedLine(M, m, color=MUTED, stroke_width=2))
      l1 = mtx('1', 0.7).next_to(Line(A, M), DOWN, buff=0.2)
      lt = mtx('t', 0.75, ARROW).next_to(Line(M, m), RIGHT, buff=0.15)
      hyp = mtx(r'\sqrt{1+t^2}', 0.7).move_to((A + m) / 2 + UP * 0.45 + LEFT * 0.2)
      self.play(FadeOut(status), FadeOut(stuck), Create(tri), FadeIn(l1), FadeIn(lt), run_time=0.2 * d)
      self.play(FadeIn(hyp), run_time=0.15 * d)
      f1 = mtx(r'\sqrt{1+t^2} \;\approx\; 1 + \tfrac{1}{2}t^2', 0.95).move_to(DOWN * 1.25)
      self.play(Write(f1), run_time=0.25 * d)
      f2 = mtx(r't = 0.1:\quad \sqrt{1.01} = 1.00499\ldots \approx 1 + 0.005', 0.75, MUTED).move_to(DOWN * 2.35)
      self.play(FadeIn(f2), run_time=0.2 * d)

    with self.say('s05_clash') as d:
      ax = Axes(x_range=[-1, 1, 1], y_range=[0, 0.6, 1], x_length=2.6, y_length=1.6, tips=False,
                axis_config={'color': MUTED, 'stroke_width': 2}).move_to(np.array([4.6, -1.9, 0]))
      par = ax.plot(lambda x: 0.5 * x * x, color=BAD, x_range=[-1, 1])
      axl = VGroup(mtx('t', 0.55, MUTED).next_to(ax.x_axis, RIGHT, buff=0.1),
                   txt('stretch', 0.55, MUTED).next_to(ax, UP, buff=0.1))
      self.play(FadeOut(VGroup(f1, f2, tri, l1, lt, hyp)), FadeIn(ax), FadeIn(axl), Create(par), run_time=0.22 * d)
      self.play(lift.animate.set_value(0.0), run_time=0.15 * d)
      left = Arrow(M + DOWN * 0.35, M + DOWN * 0.35 + LEFT * 1.4, buff=0, color=ARROW, stroke_width=6)
      right = Arrow(M + DOWN * 0.35, M + DOWN * 0.35 + RIGHT * 1.4, buff=0, color=ARROW, stroke_width=6)
      ll = txt('left stick', 0.6, ARROW).next_to(left.get_end(), DOWN, buff=0.2)
      rl = txt('right stick', 0.6, ARROW).next_to(right.get_end(), DOWN, buff=0.2)
      self.play(GrowArrow(left), FadeIn(ll), run_time=0.15 * d)
      self.play(GrowArrow(right), FadeIn(rl), run_time=0.15 * d)
      imp = txt('impossible', 0.8, BAD).move_to(DOWN * 1.6)
      self.play(left.animate.set_color(BAD), right.animate.set_color(BAD), ll.animate.set_color(BAD),
                rl.animate.set_color(BAD), FadeIn(imp), run_time=0.12 * d)
      self.clash = VGroup(left, right, ll, rl, imp, ax, axl, par)

    with self.say('s05_layers') as d:
      name = txt('a second-order obstruction', 0.8, BAD).move_to(DOWN * 1.6)
      self.play(Transform(self.clash[4], name), run_time=0.2 * d)
      self.wait(0.1 * d)
      self.play(FadeOut(VGroup(sticks, pins, *self.clash)), run_time=0.15 * d)
      rungs = VGroup()
      for k, (lab, err) in enumerate([('first order', 't'), ('second order', 't^2'), ('third order', 't^3')]):
        row = VGroup(txt(lab, 0.72), mtx(r'\text{errors like }' + err, 0.75, MUTED)).arrange(RIGHT, buff=0.5)
        box = RoundedRectangle(width=7.0, height=0.9, corner_radius=0.12, stroke_color=MUTED, stroke_width=1.5)
        row.move_to(box)
        rungs.add(VGroup(box, row))
      rungs.arrange(DOWN, buff=0.25).move_to(UP * 0.5)
      dots = mtx(r'\vdots', 0.8, MUTED).next_to(rungs, DOWN, buff=0.2)
      self.play(LaggedStart(*[FadeIn(r) for r in rungs], lag_ratio=0.4), FadeIn(dots), run_time=0.3 * d)
      marks = VGroup(MathTex(r'\checkmark', color=GOOD).next_to(rungs[0], RIGHT, buff=0.3),
                     MathTex(r'\times', color=BAD).scale(1.2).next_to(rungs[1], RIGHT, buff=0.3))
      self.play(FadeIn(marks), run_time=0.12 * d)
    self.play(FadeOut(VGroup(rungs, dots, marks)), run_time=0.5)


# 6 ------------------------------------------------------------------------------------------
class SolidFlex(Scene3D):
  def construct(self):
    yaw = self.spin(0.9)
    scale = 0.78
    center = np.array([-2.5, -0.1, 0])
    arrow_k = ValueTracker(0.0)
    mix = ValueTracker(0.0)
    t = ValueTracker(0.0)
    fade = ValueTracker(0.0)

    def mixed():
      tau = mix.get_value()
      c = np.array([np.cos(tau), 0.9 * np.sin(tau), 0.7 * np.sin(2 * tau), 0.6 * np.sin(3 * tau)])
      u = np.tensordot(c, BASIS, axes=1)
      return u / np.max(np.linalg.norm(u, axis=1))

    def frame():
      X = V0 + t.get_value() * FLEX
      P = pose(X, yaw.get_value(), scale, center)
      cols = {}
      for e in TD.edges:
        rel = abs(np.linalg.norm(X[e[0]] - X[e[1]]) - REST[e]) / REST[e]
        cols[e] = min(1.0, rel / 0.012)
      body, verts = draw_poly(TD, P, face_color=td_color(), edge_colors=cols, edge_width=2.6, alpha=fade.get_value())
      k = arrow_k.get_value()
      if k > 0.01:
        U = (mixed() * scale * k) @ rotation(yaw.get_value()).T
        body.add(draw_arrows(P, U, verts, self.project, alpha=min(1.0, 3 * k)))
      return body

    solid = always_redraw(frame)
    self.add(solid)
    head = VGroup(txt('4 infinitesimal flexes', 0.8, ARROW),
                  txt('(not counting slides and turns)', 0.62, MUTED)).arrange(DOWN, buff=0.25).move_to(RIGHT * 3.7 + UP * 1.4)
    with self.say('s06_four') as d:
      self.play(fade.animate.set_value(1.0), run_time=0.15 * d)
      self.play(FadeIn(head), run_time=0.25 * d)
      self.play(arrow_k.animate.set_value(1.0), run_time=0.3 * d)

    formula = VGroup(mtx(r'v_0 \times \text{flex}_1 \;+\; v_1 \times \text{flex}_2', 0.72),
                     mtx(r'+\; v_2 \times \text{flex}_3 \;+\; v_3 \times \text{flex}_4', 0.72)).arrange(DOWN, buff=0.3)
    formula.move_to(RIGHT * 3.7 + DOWN * 0.6)
    with self.say('s06_mix') as d:
      self.play(Write(formula), run_time=0.3 * d)
      self.play(mix.animate.set_value(2 * PI), run_time=0.6 * d, rate_func=linear)

    note = VGroup(txt('move straight along the arrows:', 0.66),
                  txt(r'sticks stretch, by about $t^2$', 0.66, BAD)).arrange(DOWN, buff=0.25).move_to(RIGHT * 3.7 + DOWN * 0.4)
    with self.say('s06_stretch') as d:
      self.play(FadeOut(formula), FadeIn(note), arrow_k.animate.set_value(0.0), run_time=0.2 * d)
      self.play(t.animate.set_value(0.36), run_time=0.4 * d)
      self.play(t.animate.set_value(0.24), run_time=0.3 * d)
    self.play(fade.animate.set_value(0.0), FadeOut(head), FadeOut(note), run_time=0.6)


# 7 ------------------------------------------------------------------------------------------
class Layers(Scene2D):
  def construct(self):
    curves = D['error_curves']
    ts = [x for x in curves['t'] if x <= 0.3 + 1e-9]
    n = len(ts)
    ax = Axes(x_range=[0, 0.3, 0.1], y_range=[0, 0.04, 0.01], x_length=7.2, y_length=4.4, tips=False,
              axis_config={'color': MUTED, 'stroke_width': 2, 'include_numbers': True, 'font_size': 28,
                           'decimal_number_config': {'num_decimal_places': 2}},
              y_axis_config={'decimal_number_config': {'num_decimal_places': 2}})
    ax.move_to(LEFT * 1.9 + DOWN * 0.3)
    xl = mtx('t', 0.7, MUTED).next_to(ax.x_axis, RIGHT, buff=0.2)
    yl = txt('worst stick error', 0.6, MUTED).next_to(ax.y_axis, UP, buff=0.2).shift(RIGHT * 0.6)

    def curve(axes, ys, color):
      return VMobject(color=color, stroke_width=5).set_points_smoothly([axes.c2p(x, y) for x, y in zip(ts, ys)])

    straight = curve(ax, curves['straight'][:n], BAD)
    bent = curve(ax, curves['bent'][:n], GOOD)
    sl = txt('straight path', 0.6, BAD).next_to(ax.c2p(0.3, curves['straight'][n - 1]), LEFT, buff=0.2).shift(UP * 0.2)
    bl = txt('bent path', 0.6, GOOD).next_to(ax.c2p(0.3, 0.0), UP + LEFT, buff=0.15).shift(UP * 0.3)
    side = VGroup(txt('second-order numbers:', 0.66), txt('all 40 are zero', 0.75, GOOD)).arrange(DOWN, buff=0.25)
    side.move_to(RIGHT * 4.6 + UP * 1.2)
    stop = txt('where the 2026 paper stopped', 0.58, MUTED).next_to(side, DOWN, buff=0.45)
    with self.say('s07_second') as d:
      self.play(Create(ax), FadeIn(xl), FadeIn(yl), run_time=0.15 * d)
      self.play(Create(straight), FadeIn(sl), run_time=0.2 * d)
      self.play(Create(bent), FadeIn(bl), run_time=0.2 * d)
      self.play(FadeIn(side), run_time=0.15 * d)
      self.play(FadeIn(stop), run_time=0.12 * d)

    ax2 = Axes(x_range=[0, 0.3, 0.1], y_range=[0, 0.0012, 0.0004], x_length=7.2, y_length=4.4, tips=False,
               axis_config={'color': MUTED, 'stroke_width': 2, 'include_numbers': True, 'font_size': 28,
                            'decimal_number_config': {'num_decimal_places': 2}},
               y_axis_config={'decimal_number_config': {'num_decimal_places': 4}})
    ax2.move_to(ax)
    bent2 = curve(ax2, curves['bent'][:n], GOOD)
    zoom = VGroup(txt('zoomed in 33 times:', 0.62, GOOD), txt(r'grows like $t^3$', 0.62, GOOD)).arrange(DOWN, buff=0.2)
    zoom.move_to(RIGHT * 4.6 + DOWN * 0.9)
    lefts = leftover_boxes().move_to(UP * 0.6)
    lab = mtx(r'\text{four leftovers, each a cubic in } v_0, v_1, v_2, v_3', 0.85).next_to(lefts, DOWN, buff=0.7)
    with self.say('s07_third') as d:
      self.play(FadeOut(straight), FadeOut(sl), FadeOut(stop), FadeOut(bl), run_time=0.1 * d)
      self.play(Transform(ax, ax2), Transform(bent, bent2), FadeIn(zoom), run_time=0.25 * d)
      self.wait(0.15 * d)
      self.play(FadeOut(VGroup(ax, bent, xl, yl, side, zoom)), run_time=0.12 * d)
      self.play(FadeIn(lefts), run_time=0.15 * d)
      self.play(FadeIn(lab), run_time=0.12 * d)


# 8 ------------------------------------------------------------------------------------------
class Obstruction(Scene2D):
  def construct(self):
    lb = leftover_boxes().move_to(UP * 0.6)
    eqs = VGroup(*[mtx('= 0', 1.0).next_to(b, DOWN, buff=0.45) for b in lb[1]])
    self.add(lb)
    q = mtx(r'\text{only when } v_0 = v_1 = v_2 = v_3 = 0\,?', 0.8).move_to(DOWN * 1.8)
    with self.say('s08_need') as d:
      self.play(FadeIn(eqs), run_time=0.25 * d)
      self.play(Write(q), run_time=0.35 * d)
      self.play(Indicate(q, color=ARROW), run_time=0.2 * d)

    ax = Axes(x_range=[-2, 2, 1], y_range=[-2, 2, 1], x_length=5.0, y_length=5.0, tips=False,
              axis_config={'color': MUTED, 'stroke_width': 2}).move_to(LEFT * 3.6 + DOWN * 0.2)
    axl = VGroup(mtx('x', 0.7, MUTED).next_to(ax.x_axis, RIGHT, buff=0.15),
                 mtx('y', 0.7, MUTED).next_to(ax.y_axis, UP, buff=0.15))
    e1 = mtx(r'x^2 - y^2', 0.95, PRIMARY)
    e2 = mtx(r'x\,y', 0.95, TRIANGLE)
    lefts = VGroup(VGroup(txt('leftover 1:', 0.7, MUTED), e1).arrange(RIGHT, buff=0.3),
                   VGroup(txt('leftover 2:', 0.7, MUTED), e2).arrange(RIGHT, buff=0.3)).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
    lefts.move_to(RIGHT * 3.2 + UP * 2.2)
    diag = VGroup(Line(ax.c2p(-2, -2), ax.c2p(2, 2), color=PRIMARY, stroke_width=6),
                  Line(ax.c2p(-2, 2), ax.c2p(2, -2), color=PRIMARY, stroke_width=6))
    with self.say('s08_toy') as d:
      self.play(FadeOut(VGroup(lb, eqs, q)), run_time=0.1 * d)
      self.play(Create(ax), FadeIn(axl), run_time=0.15 * d)
      self.play(FadeIn(lefts[0]), run_time=0.15 * d)
      self.play(FadeIn(lefts[1]), run_time=0.15 * d)
      self.wait(0.1 * d)
      self.play(Create(diag), Indicate(e1, color=PRIMARY), run_time=0.25 * d)

    axes_hl = VGroup(Line(ax.c2p(-2, 0), ax.c2p(2, 0), color=TRIANGLE, stroke_width=6),
                     Line(ax.c2p(0, -2), ax.c2p(0, 2), color=TRIANGLE, stroke_width=6))
    origin = Dot(ax.c2p(0, 0), radius=0.13, color=ARROW)
    olab = mtx('(0, 0)', 0.65, ARROW).next_to(origin, DR, buff=0.12)
    with self.say('s08_both') as d:
      self.play(Create(axes_hl), Indicate(e2, color=TRIANGLE), run_time=0.35 * d)
      self.play(FadeIn(origin, scale=2), FadeIn(olab), run_time=0.25 * d)

    a1 = MathTex(r'{{x}} \cdot ({{x^2}} - {{y^2}}) + {{y}} \cdot ({{xy}})').scale(0.95)
    a2 = MathTex(r'{{x^3}} - {{xy^2}} + {{xy^2}}').scale(0.95)
    a3 = MathTex(r'{{x^3}}').scale(0.95)
    for m in (a1, a2, a3):
      m.move_to(RIGHT * 3.2 + DOWN * 0.1)
    with self.say('s08_mult') as d:
      self.play(Write(a1), run_time=0.25 * d)
      self.play(TransformMatchingTex(a1, a2), run_time=0.2 * d)
      self.play(a2[1:].animate.set_color(BAD), run_time=0.1 * d)
      self.play(TransformMatchingTex(a2, a3), run_time=0.15 * d)
      tail = mtx(r'= 0 \;\Rightarrow\; x = 0', 0.95, GOOD).next_to(a3, RIGHT, buff=0.25)
      grp = VGroup(a3, tail)
      self.play(FadeIn(tail), grp.animate.move_to(RIGHT * 3.2 + DOWN * 0.1), run_time=0.15 * d)
      self.toy = VGroup(ax, axl, lefts, diag, axes_hl, origin, olab, grp)

    cert = MathTex(r'{{v_0^9}} = A_1 {{C_1}} + A_2 {{C_2}} + A_3 {{C_3}} + A_4 {{C_4}}').scale(1.0)
    for k in (2, 4, 6, 8):
      cert[k].set_color(ARROW)
    cert[0].set_color(GOOD)
    cert.move_to(UP * 0.7)
    note = txt(r'certificate: numbers anyone can check', 0.66, MUTED).next_to(cert, UP, buff=0.6)
    mult = txt(r'$A_1, \ldots, A_4$: multipliers, with powers adding to 6', 0.66, MUTED).next_to(cert, DOWN, buff=0.45)
    same = mtx(r'\text{and the same for } v_1^9,\; v_2^9,\; v_3^9', 0.75, GOOD).next_to(cert, DOWN, buff=1.3)
    with self.say('s08_cert') as d:
      self.play(FadeOut(self.toy), run_time=0.1 * d)
      self.play(FadeIn(note), run_time=0.15 * d)
      self.play(Write(cert), run_time=0.3 * d)
      self.play(FadeIn(mult), run_time=0.15 * d)
      self.play(FadeIn(same), run_time=0.15 * d)
    self.play(FadeOut(VGroup(cert, note, mult, same)), run_time=0.5)


# 9 ------------------------------------------------------------------------------------------
class Clock(Scene2D):
  def construct(self):
    icon_c = np.array([-3.6, 0.0, 0])
    icon = solid_icon(0.5, 0.62, icon_c)
    # vertex 0 is (-(phi+2), 0, phi-1): label one corner with its coordinates
    g1 = VGroup(txt('golden ratio', 0.72, MUTED), mtx(r'\approx 1.618', 0.9)).arrange(RIGHT, buff=0.3)
    g2 = mtx(r'1.618^2 \approx 2.618 = 1.618 + 1', 0.9)
    grp = VGroup(g1, g2).arrange(DOWN, buff=0.45).move_to(RIGHT * 3.0 + UP * 0.6)
    corner = mtx(r'\text{a corner: } (0,\; 0.618\ldots,\; 3.618\ldots)', 0.62, MUTED).move_to(RIGHT * 3.0 + DOWN * 1.4)
    with self.say('s09_phi') as d:
      self.play(FadeIn(icon), run_time=0.15 * d)
      self.play(FadeIn(g1), run_time=0.2 * d)
      self.play(FadeIn(corner), run_time=0.15 * d)
      self.play(Write(g2), run_time=0.3 * d)

    t = ValueTracker(0.0)
    wob_a = ValueTracker(1.0)
    wob = always_redraw(lambda: draw_poly(TD, pose(V0 + t.get_value() * FLEX + t.get_value() ** 2 * W2, 0.5, 0.62,
                                                   icon_c), mode='2d', face_color=td_color(), edge_width=1.6,
                                          alpha=wob_a.get_value())[0])
    cap = txt('rounded numbers: a wobble?', 0.75, ARROW).move_to(RIGHT * 3.0 + UP * 0.3)
    illus = txt('illustration', 0.55, MUTED).move_to(icon_c + DOWN * 3.1)
    with self.say('s09_round') as d:
      self.remove(icon)
      self.add(wob)
      self.play(FadeOut(VGroup(g1, g2, corner)), run_time=0.1 * d)
      self.play(FadeIn(cap), FadeIn(illus), t.animate.set_value(0.55), run_time=0.4 * d)
      self.wait(0.15 * d)
      cap2 = txt('careful numbers: it snaps back', 0.75, GOOD).move_to(cap)
      self.play(t.animate.set_value(0.0), Transform(cap, cap2), run_time=0.12 * d, rate_func=rush_into)

    R = 2.3
    cc = np.array([-3.4, -0.1, 0])

    def at(n, r=R):
      a = PI / 2 - TAU * n / 1009
      return cc + r * np.array([np.cos(a), np.sin(a), 0])

    dial = Circle(radius=R, color=CLOCK, stroke_width=3).move_to(cc)
    ticks = VGroup(*[Line(at(n, R - (0.22 if n % 250 == 0 else 0.1)), at(n), color=CLOCK if n % 250 == 0 else MUTED,
                          stroke_width=3 if n % 250 == 0 else 1.5) for n in range(0, 1009, 50)])
    nums = VGroup(*[mtx(str(n), 0.55, MUTED).move_to(at(n, R - 0.55)) for n in (0, 250, 500, 750)])
    hand_n = ValueTracker(1000)
    hand = always_redraw(lambda: Line(cc, at(hand_n.get_value(), R - 0.3), color=ARROW, stroke_width=5))
    hub = Dot(cc, radius=0.07, color=ARROW)
    readout = always_redraw(lambda: Integer(int(round(hand_n.get_value())) % 1009, color=ARROW, group_with_commas=False).scale(0.8)
                            .move_to(cc + DOWN * 0.8))
    hours = txt('a clock with 1009 hours', 0.7, CLOCK).next_to(dial, DOWN, buff=0.3)
    with self.say('s09_clock') as d:
      self.play(wob_a.animate.set_value(0.0), FadeOut(cap), FadeOut(illus), run_time=0.1 * d)
      self.remove(wob)
      self.play(Create(dial), FadeIn(ticks), FadeIn(nums), FadeIn(hours), run_time=0.2 * d)
      self.play(FadeIn(hand), FadeIn(hub), FadeIn(readout), run_time=0.1 * d)
      add = mtx(r'1000 + 20 = 1020', 0.9).move_to(RIGHT * 3.2 + UP * 0.9)
      self.play(FadeIn(add), run_time=0.12 * d)
      self.play(hand_n.animate.set_value(1020), run_time=0.2 * d)
      lands = mtx(r'\text{lands on } 11', 0.9, CLOCK).next_to(add, DOWN, buff=0.4)
      self.play(FadeIn(lands), run_time=0.1 * d)

    with self.say('s09_627') as d:
      self.play(FadeOut(add), FadeOut(lands), hand_n.animate.set_value(627), run_time=0.15 * d)
      l1 = mtx(r'627 \times 627 = 393129', 0.9).move_to(RIGHT * 3.2 + UP * 0.9)
      l2 = mtx(r'= 389 \times 1009 + 628', 0.9).next_to(l1, DOWN, buff=0.4).align_to(l1, RIGHT)
      self.play(FadeIn(l1), run_time=0.2 * d)
      self.play(FadeIn(l2), run_time=0.2 * d)
      self.play(hand_n.animate.set_value(628), run_time=0.1 * d)
      l3 = mtx(r'628 = 627 + 1', 0.95, CLOCK).move_to(l2)
      self.play(Transform(l2, l3), run_time=0.15 * d)
      self.play(Indicate(l2, color=CLOCK), run_time=0.12 * d)

    with self.say('s09_prime') as d:
      p1 = txt('1009 is prime, so division works', 0.7).move_to(RIGHT * 3.2 + DOWN * 1.1)
      p2 = mtx(r'\text{e.g. one half} = 505,\ \text{since } 2 \times 505 = 1010 \to 1', 0.62, MUTED).next_to(p1, DOWN, buff=0.3)
      self.play(FadeIn(p1), run_time=0.3 * d)
      self.play(FadeIn(p2), run_time=0.3 * d)
    self.clear_all()


# 10 -----------------------------------------------------------------------------------------
CANCEL = D['cancel']
MON9 = [tuple(m) for m in D['mon9']]


def cell_color(v):
  return interpolate_color(ManimColor(SOFT), ManimColor(PRIMARY), v / 1008)


def make_grid(cols=20, rows=11, size=0.38, pitch=0.46):
  g = VGroup()
  for k in range(220):
    r, c = divmod(k, cols)
    sq = Square(size, stroke_color=MUTED, stroke_width=1, stroke_opacity=0.35, fill_opacity=0.0)
    sq.move_to(np.array([c * pitch, -r * pitch, 0]))
    g.add(sq)
  return g.center()


def stage_anims(grid, values, hi=None):
  anims = []
  for k, (sq, v) in enumerate(zip(grid, values)):
    if v:
      col = ARROW if (hi is not None and k == hi) else cell_color(v)
      anims.append(sq.animate.set_fill(col, opacity=0.95 if hi == k else 0.85))
    else:
      anims.append(sq.animate.set_fill(opacity=0.0))
  return anims


class Cancel(Scene2D):
  def construct(self):
    head = MathTex(r'C_1 = ', r'649', r'\,v_0^3 + ', r'692', r'\,v_0^2 v_1 + ', r'833', r'\,v_0^2 v_2 + \cdots').scale(0.85)
    for k in (1, 3, 5):
      head[k].set_color(CLOCK)
    head.move_to(UP * 3.3)
    sub = txt('20 terms, written in clock numbers', 0.6, MUTED).next_to(head, DOWN, buff=0.25)
    with self.say('s10_cubic') as d:
      self.play(Write(head), run_time=0.45 * d)
      self.play(FadeIn(sub), run_time=0.2 * d)

    grid = make_grid().move_to(LEFT * 1.3 + DOWN * 0.55)
    ex_k = MON9.index((5, 2, 0, 2))
    ex = VGroup(mtx(r'v_0^5\, v_1^2\, v_3^2', 0.75, ARROW), mtx(r'5 + 2 + 2 = 9', 0.7, MUTED)).arrange(DOWN, buff=0.25)
    ex.move_to(RIGHT * 5.3 + UP * 1.0)
    with self.say('s10_grid') as d:
      self.play(FadeOut(sub), FadeIn(grid, lag_ratio=0.002), run_time=0.3 * d)
      self.play(grid[ex_k].animate.set_stroke(ARROW, width=3, opacity=1), FadeIn(ex), run_time=0.2 * d)
      self.wait(0.25 * d)
      self.play(grid[ex_k].animate.set_stroke(MUTED, width=1, opacity=0.35), FadeOut(ex), run_time=0.15 * d)

    stages = CANCEL['v0']['stages']
    counts = CANCEL['v0']['nonzero']
    lab = mtx(r'A_1 C_1', 0.8).move_to(RIGHT * 5.3 + UP * 1.4)
    lit = VGroup(txt('lit squares', 0.6, MUTED), Integer(0).scale(0.9)).arrange(DOWN, buff=0.2).move_to(RIGHT * 5.3 + DOWN * 0.3)
    names = [r'A_1 C_1', r'+\,A_2 C_2', r'+\,A_3 C_3', r'+\,A_4 C_4']
    with self.say('s10_add') as d:
      self.play(FadeIn(lab), FadeIn(lit), run_time=0.08 * d)
      for k in range(3):
        if k:
          self.play(Transform(lab, mtx(names[k], 0.8).move_to(lab)), run_time=0.06 * d)
        self.play(*stage_anims(grid, stages[k]), Transform(lit[1], Integer(counts[k]).scale(0.9).move_to(lit[1])), run_time=0.14 * d)
        self.wait(0.07 * d if k < 2 else 0.02 * d)

    with self.say('s10_last') as d:
      self.play(Transform(lab, mtx(names[3], 0.8).move_to(lab)), run_time=0.1 * d)
      self.play(*stage_anims(grid, stages[3], hi=0), Transform(lit[1], Integer(counts[3]).scale(0.9).move_to(lit[1])), run_time=0.3 * d)
      tag = mtx(r'v_0^9 \text{ with coefficient } 1', 0.75, ARROW).next_to(grid[0], UP, buff=0.3).align_to(grid, LEFT)
      self.play(FadeIn(tag), FadeOut(head), Indicate(grid[0], color=ARROW, scale_factor=1.6), run_time=0.3 * d)

    with self.say('s10_all') as d:
      self.play(FadeOut(lab), FadeOut(lit), FadeOut(tag), run_time=0.08 * d)
      small = []
      for j in range(4):
        g = grid if j == 0 else make_grid()
        small.append(g)
      targets = [np.array([-4.6 + 3.05 * j, 0.6, 0]) for j in range(4)]
      self.play(grid.animate.scale(0.29).move_to(targets[0]), run_time=0.15 * d)
      for j in range(1, 4):
        small[j].scale(0.29).move_to(targets[j])
      self.play(*[FadeIn(small[j]) for j in range(1, 4)], run_time=0.1 * d)
      for st in range(4):
        anims = []
        for j in range(1, 4):
          vals = CANCEL[f'v{j}']['stages'][st]
          hi = MON9.index(tuple(9 if i == j else 0 for i in range(4))) if st == 3 else None
          anims += stage_anims(small[j], vals, hi=hi)
        self.play(*anims, run_time=0.07 * d)
      labels = VGroup(*[mtx(f'v_{j}^9', 0.8, GOOD).next_to(small[j], DOWN, buff=0.3) for j in range(4)])
      self.play(FadeIn(labels), run_time=0.12 * d)
      verdict = txt('no mix of flexes passes the third-order test', 0.72, GOOD).move_to(DOWN * 1.9)
      self.play(FadeIn(verdict), run_time=0.15 * d)

    with self.say('s10_higher') as d:
      h1 = txt(r'terms beyond $t^3$: powers adding to 10 or more', 0.68, MUTED).move_to(DOWN * 2.7)
      h2 = txt(r"Nakayama's lemma: they cannot rescue a wobble", 0.68, GOOD).move_to(DOWN * 2.7)
      self.play(FadeOut(verdict), FadeIn(h1), run_time=0.2 * d)
      self.wait(0.25 * d)
      self.play(Transform(h1, h2), run_time=0.2 * d)
    self.clear_all()


# 11 -----------------------------------------------------------------------------------------
def small_clock(center, r=1.1):
  dial = Circle(radius=r, color=CLOCK, stroke_width=3).move_to(center)
  ticks = VGroup(*[Line(center + (r - 0.12) * np.array([np.cos(a), np.sin(a), 0]),
                        center + r * np.array([np.cos(a), np.sin(a), 0]), color=MUTED, stroke_width=1.5)
                   for a in np.linspace(0, TAU, 21)[:-1]])
  hand = Line(center, center + 0.8 * r * np.array([np.cos(1.1), np.sin(1.1), 0]), color=ARROW, stroke_width=4)
  return VGroup(dial, ticks, hand)


def chip(text, color):
  t = txt(text, 0.66, color)
  box = RoundedRectangle(width=t.width + 0.5, height=t.height + 0.4, corner_radius=0.12, stroke_color=color,
                         stroke_width=2)
  return VGroup(box, t.move_to(box))


class Transfer(Scene2D):
  def construct(self):
    left = VGroup(solid_icon(0.4, 0.38, ORIGIN), txt('the real numbers', 0.7)).arrange(DOWN, buff=0.35)
    right = VGroup(small_clock(ORIGIN), txt('the 1009-hour clock', 0.7, CLOCK)).arrange(DOWN, buff=0.35)
    left.move_to(LEFT * 3.6 + UP * 0.6)
    right.move_to(RIGHT * 3.6 + UP * 0.6)
    q = MathTex('?', color=ARROW).scale(2).move_to(UP * 0.6)
    with self.say('s11_why') as d:
      self.play(FadeIn(left), run_time=0.25 * d)
      self.play(FadeIn(right), run_time=0.25 * d)
      self.play(FadeIn(q), run_time=0.2 * d)

    r1 = mtx(r'0 \;\longmapsto\; 0', 0.95)
    r2 = mtx(r'2020 \;\longmapsto\; 2', 0.95)
    rows = VGroup(r1, r2).arrange(DOWN, buff=0.35).move_to(UP * 0.6)
    concl = mtx(r'\text{reading} \neq 0 \;\Rightarrow\; \text{number} \neq 0', 0.85, GOOD).move_to(DOWN * 2.0)
    with self.say('s11_zero') as d:
      self.play(FadeOut(q), FadeIn(r1), run_time=0.2 * d)
      self.play(FadeIn(r2), run_time=0.2 * d)
      self.play(FadeIn(concl), run_time=0.25 * d)

    c1 = chip('real solid wobbles', INK)
    c2 = chip('clock version wobbles', INK)
    top = VGroup(c1, MathTex(r'\Longrightarrow').scale(1.1), c2).arrange(RIGHT, buff=0.4).move_to(UP * 0.4)
    c3 = chip('clock: no wobble', GOOD)
    c4 = chip('real solid: no wobble', GOOD)
    bot = VGroup(c3, MathTex(r'\Longrightarrow', color=GOOD).scale(1.1), c4).arrange(RIGHT, buff=0.4).move_to(DOWN * 1.4)
    with self.say('s11_wobble') as d:
      self.play(FadeOut(VGroup(left, right, rows, concl)), run_time=0.1 * d)
      self.play(FadeIn(top[0]), run_time=0.12 * d)
      self.play(FadeIn(top[1]), FadeIn(top[2]), run_time=0.2 * d)
      self.wait(0.15 * d)
      self.play(FadeIn(bot), run_time=0.25 * d)

    rev = mtx(r'1009 \neq 0, \text{ but } 1009 \;\longmapsto\; 0', 0.85, BAD).move_to(UP * 2.4)
    one = txt('a clock can invent a wobble, but cannot hide a real one', 0.66, MUTED).move_to(DOWN * 2.8)
    with self.say('s11_reverse') as d:
      self.play(FadeIn(rev), run_time=0.25 * d)
      self.play(FadeIn(one), run_time=0.25 * d)
      self.play(Indicate(bot, color=GOOD, scale_factor=1.05), run_time=0.2 * d)
    self.clear_all()


# 12 -----------------------------------------------------------------------------------------
class Status(Scene3D):
  def construct(self):
    yaw = self.spin(1.6)
    center = np.array([-3.0, -0.1, 0])
    fade = ValueTracker(0.0)
    solid = always_redraw(lambda: draw_poly(TD, pose(V0, yaw.get_value(), 0.74, center), face_color=td_color(),
                                            alpha=fade.get_value())[0])
    self.add(solid)
    pos = RIGHT * 3.3 + UP * 0.3

    def lines(a, b, ca=INK, cb=MUTED):
      return VGroup(txt(a, 0.74, ca), txt(b, 0.62, cb)).arrange(DOWN, buff=0.3).move_to(pos)

    l1 = lines('locally rigid', 'nearby shapes are the same solid, moved or turned', GOOD, INK)
    with self.say('s12_local') as d:
      self.play(fade.animate.set_value(1.0), run_time=0.2 * d)
      self.play(FadeIn(l1[0]), run_time=0.2 * d)
      self.play(FadeIn(l1[1]), run_time=0.25 * d)

    l2 = lines('far-away shapes', 'not covered by this proof')
    with self.say('s12_far') as d:
      self.play(FadeOut(l1), FadeIn(l2), run_time=0.3 * d)

    l3 = lines('computer-assisted', 'an independent exact checker, under a second', INK, MUTED)
    with self.say('s12_computer') as d:
      self.play(FadeOut(l2), FadeIn(l3[0]), run_time=0.25 * d)
      self.play(FadeIn(l3[1]), run_time=0.25 * d)

    l4 = lines('a written proof, reviewed in-project', 'not Lean-checked, not yet refereed', INK, WARM)
    with self.say('s12_written') as d:
      self.play(FadeOut(l3), FadeIn(l4[0]), run_time=0.25 * d)
      self.play(FadeIn(l4[1]), run_time=0.25 * d)
    self.play(fade.animate.set_value(0.0), FadeOut(l4), run_time=0.6)


# 13 -----------------------------------------------------------------------------------------
class Recap(Scene2D):
  def construct(self):
    items = [('1', 'counting always balances, so it cannot decide'),
             ('2', 'four flexes pass two layers of tests; four cubics rule them out'),
             ('3', r"a 1009-hour clock is exact, and its ``no wobble'' carries over")]
    rows = VGroup()
    for n, s in items:
      rows.add(VGroup(mtx(n, 0.85, ARROW), txt(s, 0.72)).arrange(RIGHT, buff=0.4))
    rows.arrange(DOWN, aligned_edge=LEFT, buff=0.55).move_to(UP * 0.3)
    for k, key in enumerate(['s13_recap1', 's13_recap2', 's13_recap3']):
      with self.say(key) as d:
        if k:
          self.play(rows[k - 1].animate.set_opacity(0.45), run_time=0.1 * d)
        self.play(FadeIn(rows[k], shift=RIGHT * 0.2), run_time=0.3 * d)

    open_h = txt('still open', 0.85, ARROW)
    o1 = txt('outside expert review; no Lean check', 0.7)
    o2 = txt('far-away shapes; a general rule for other solids', 0.7)
    opens = VGroup(open_h, o1, o2).arrange(DOWN, buff=0.35).move_to(ORIGIN)
    with self.say('s13_open') as d:
      self.play(FadeOut(rows), run_time=0.12 * d)
      self.play(FadeIn(open_h), run_time=0.12 * d)
      self.play(FadeIn(o1), run_time=0.2 * d)
      self.play(FadeIn(o2), run_time=0.2 * d)
    self.play(FadeOut(opens), run_time=0.6)

    icon = solid_icon(0.7, 0.3, ORIGIN)
    t1 = txt(r'The truncated dodecahedron is rigid', 1.0)
    t2 = txt('Valyu Research, 2026', 0.75, MUTED)
    t3 = Tex(r'\texttt{maths/geometry/rigidity/truncated-dodecahedron}', color=MUTED).scale(0.6)
    t4 = txt('Narration uses a synthetic voice.', 0.55, MUTED)
    card_g = VGroup(icon, t1, t2, t3, t4).arrange(DOWN, buff=0.35)
    self.play(FadeIn(card_g), run_time=1.0)
    self.wait(5.0)
