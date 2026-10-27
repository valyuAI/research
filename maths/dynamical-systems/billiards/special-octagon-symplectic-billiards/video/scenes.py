"""Explainer: every symplectic billiard path in a special octagon repeats.

Running example: the special octagon O(5,6,1,2) (vertices (2,0),(3,0),(5,2),(5,5),(4,6),(1,6),
(0,5),(0,2)); the rule is taught first in the 4 x 3 rectangle, and the counterexample is the
lopsided octagon Q. All geometry is computed exactly with the paper's own library
../verification/symplectic_billiard.py; check_numbers.py asserts every number shown.
"""

import math
import sys
from fractions import Fraction as Fr
from pathlib import Path

import numpy as np
from manim import *
from vrvideo import *

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'verification'))
from symplectic_billiard import Polygon as Table, special_octagon, critical_set, _image_parameter  # noqa: E402

SCENES = ['Hook', 'Billiards', 'Rule', 'Octagon', 'Corners', 'Boxes', 'Naive', 'Dots', 'Why', 'Conclude',
          'Lopsided', 'Status', 'Ending']

EDGE = INK
CHORD = PRIMARY
EVEN = WARM
ODD = '#c8a2e8'
USE = SECONDARY
CRIT = WARN
GREEN_DOT = OK
BLUE_DOT = '#4f9cff'
ORANGE_DOT = '#ff8c2e'
GRID = '#2a3039'
GHOST = '#6b7078'
NarratedScene.pause_after = 0.3   # slightly tighter pacing between clips than the toolkit default

# ---------------------------------------------------------------- exact data
OCT = special_octagon(5, 6, 1, 2)
P = Table(OCT)
QV = [(1, 0), (3, 0), (4, 1), (4, 4), (3, 5), (2, 5), (0, 3), (0, 1)]
Q = Table(QV)
RECT = Table([(0, 0), (4, 0), (4, 3), (0, 3)])
_, C_SET, _ = critical_set(P)
CRIT_PTS = sorted(P.point(c) for c in C_SET)
HOOK = ((Fr(7, 3), 0), (Fr(11, 3), Fr(2, 3)))
GALLERY = [(4, ((Fr(7, 3), 0), (5, 3))), (16, ((Fr(17, 5), Fr(2, 5)), (Fr(9, 2), Fr(11, 2)))),
           (32, ((Fr(7, 3), 0), (Fr(14, 3), Fr(16, 3)))), (44, ((Fr(17, 5), Fr(2, 5)), (5, Fr(7, 2)))),
           (68, ((Fr(7, 3), 0), (Fr(17, 5), Fr(2, 5)))), (92, HOOK)]
LOOP = [(4, Fr(11, 3)), (Fr(5, 3), 0), (Fr(2, 3), Fr(11, 3)), (4, Fr(7, 3)), (Fr(2, 3), Fr(1, 3)), (Fr(5, 3), Fr(14, 3))]


def locate(T, pt):
  pt = (Fr(pt[0]), Fr(pt[1]))
  for i in range(T.n):
    if T.V[i] == pt:
      return (i, Fr(0))
  for i in range(T.n):
    a, e = T.V[i], T.E[i]
    t = (pt[0] - a[0]) / e[0] if e[0] != 0 else (pt[1] - a[1]) / e[1]
    if 0 < t < 1 and T.point((i, t)) == pt:
      return (i, t)
  raise ValueError(pt)


def orbit_params(T, a, b, n):
  seq = [locate(T, a), locate(T, b)]
  while len(seq) < n + 1:
    seq.append(T.step(seq[-2], seq[-1]))
  return seq


def orbit_points(T, a, b, n):
  return [T.point(q) for q in orbit_params(T, a, b, n)]


def corner_trajectory():
  seq = [(0, Fr(0)), (1, Fr(37, 100))]
  while not P.is_vertex(seq[-1]):
    seq.append(P.step(seq[-2], seq[-1]))
  return [P.point(q) for q in seq]


TRAJ = corner_trajectory()   # 47 points, (2,0) ... (3,0)


def dot_sets():
  lines = [(0, 1, 0), (1, -1, 3), (1, 0, 5), (1, 1, 10), (0, 1, 6), (-1, 1, 5), (1, 0, 0), (1, 1, 2)]
  kinds = 'hdvdhdvd'
  g, bl, o = [], [], []
  for i in range(11):
    for j in range(13):
      x, y = Fr(i, 2), Fr(j, 2)
      for k, (a, b, c) in enumerate(lines):
        v0, v1 = P.V[k], P.V[(k + 1) % 8]
        if a * x + b * y == c and min(v0[0], v1[0]) <= x <= max(v0[0], v1[0]) and \
           min(v0[1], v1[1]) <= y <= max(v0[1], v1[1]):
          if x.denominator == 1 and y.denominator == 1:
            g.append((x, y))
          elif kinds[k] == 'd' and x.denominator == 2 and y.denominator == 2:
            bl.append((x, y))
          elif kinds[k] == 'h' and x.denominator == 2 and y.denominator == 1:
            o.append((x, y))
          break
  return sorted(set(g)), sorted(set(bl)), sorted(set(o))


S_GREEN, S_BLUE, S_ORANGE = dot_sets()


def ordinary_path(start, d, W, Hh, bounces):
  p, (dx, dy) = start, d
  pts = [p]
  for _ in range(bounces):
    ts = []
    if dx > 0:
      ts.append((W - p[0]) / dx)
    if dx < 0:
      ts.append(-p[0] / dx)
    if dy > 0:
      ts.append((Hh - p[1]) / dy)
    if dy < 0:
      ts.append(-p[1] / dy)
    t = min(ts)
    p = (p[0] + t * dx, p[1] + t * dy)
    if abs(p[0]) < 1e-12 or abs(p[0] - W) < 1e-12:
      dx = -dx
    if abs(p[1]) < 1e-12 or abs(p[1] - Hh) < 1e-12:
      dy = -dy
    pts.append(p)
    if p == start:
      break
  return pts


# ---------------------------------------------------------------- drawing helpers
def ftex(q):
  q = Fr(q)
  if q.denominator == 1:
    return str(q.numerator)
  return ('-' if q < 0 else '') + r'\tfrac{%d}{%d}' % (abs(q.numerator), q.denominator)


def ptex(pt):
  return r'(%s,\ %s)' % (ftex(pt[0]), ftex(pt[1]))


def T(s, scale=0.75, color=INK):
  return Tex(s, color=color).scale(scale)


def M(s, scale=0.75, color=INK):
  return MathTex(s, color=color).scale(scale)


class Board:
  """Maps exact (x, y) coordinates to the screen."""

  def __init__(self, xmin, xmax, ymin, ymax, unit, center):
    self.xmin, self.xmax, self.ymin, self.ymax = xmin, xmax, ymin, ymax
    self.unit = unit
    self.c = np.array(center, dtype=float)
    self.cx, self.cy = (xmin + xmax) / 2, (ymin + ymax) / 2

  def p(self, x, y=None):
    if y is None:
      x, y = x
    return self.c + self.unit * np.array([float(x) - self.cx, float(y) - self.cy, 0.0])

  def grid(self, pad=0.4, color=GRID):
    g = VGroup()
    for i in range(math.floor(self.xmin), math.ceil(self.xmax) + 1):
      g.add(Line(self.p(i, self.ymin - pad), self.p(i, self.ymax + pad)))
    for j in range(math.floor(self.ymin), math.ceil(self.ymax) + 1):
      g.add(Line(self.p(self.xmin - pad, j), self.p(self.xmax + pad, j)))
    return g.set_stroke(color, 1.5)

  def poly(self, verts, color=EDGE, width=4):
    return Polygon(*[self.p(v) for v in verts], color=color, stroke_width=width)

  def side(self, verts, i, color=USE, width=9):
    return Line(self.p(verts[i]), self.p(verts[(i + 1) % len(verts)])).set_stroke(color, width)

  def dot(self, pt, color=EVEN, r=0.09):
    return Dot(self.p(pt), radius=r, color=color)

  def polyline(self, pts, color=CHORD, width=2.5, opacity=1.0):
    m = VMobject().set_points_as_corners([self.p(q) for q in pts])
    return m.set_stroke(color, width, opacity)

  def at(self, pts, k):
    n = min(int(math.floor(k)), len(pts) - 1)
    if n >= len(pts) - 1:
      return self.p(pts[-1])
    return interpolate(self.p(pts[n]), self.p(pts[n + 1]), k - n)

  def growing(self, pts, tracker, color=CHORD, width=2.5, opacity=1.0):
    screen = [self.p(q) for q in pts]

    def make():
      k = tracker.get_value()
      n = min(int(math.floor(k)), len(pts) - 1)
      ps = screen[:n + 1]
      if n < len(pts) - 1 and k > n:
        ps = ps + [interpolate(screen[n], screen[n + 1], k - n)]
      m = VMobject()
      if len(ps) >= 2:
        m.set_points_as_corners(ps)
      return m.set_stroke(color, width, opacity)
    return always_redraw(make)


def label(mob, text, direction, scale=0.6, color=INK, buff=0.15):
  return M(text, scale, color).next_to(mob, direction, buff=buff)


def tick(scale=1.0, color=OK):
  return MathTex(r'\checkmark', color=color).scale(scale)


def xmark(center, r=0.18, color=WARN, width=6):
  return VGroup(Line(center + UL * r, center + DR * r), Line(center + UR * r, center + DL * r)).set_stroke(color, width)


def slide_ruler(scene, b, side_line, a, c, through, end, run):
  """Copy a side, slide it parallel until it passes through `through`, stretch it to the chord."""
  ruler = side_line.copy().set_stroke(USE, 5)
  pa, pc, pt = b.p(a), b.p(c), b.p(through)
  u = (pc - pa) / np.linalg.norm(pc - pa)
  w = pt - pa
  shift = w - np.dot(w, u) * u
  scene.play(ruler.animate.shift(shift), run_time=0.55 * run)
  chord = DashedLine(b.p(through), b.p(end), dash_length=0.12).set_stroke(USE, 4)
  scene.play(ReplacementTransform(ruler, chord), run_time=0.45 * run)
  return chord


# ---------------------------------------------------------------- scenes
class Hook(NarratedScene):
  def construct(self):
    b = Board(0, 5, 0, 6, 1.08, LEFT * 2.8)
    grid = b.grid(0.35)
    octo = b.poly(OCT)
    pts = orbit_points(P, HOOK[0], HOOK[1], 92)
    k = ValueTracker(0)
    path = b.growing(pts, k, CHORD, 2.2, 0.85)
    head = always_redraw(lambda: Dot(b.at(pts, k.get_value()), radius=0.1, color=USE))
    start = b.dot(pts[0], EVEN, 0.12)
    hops = VGroup(T('hops', 0.8, MUTED), Integer(0, color=INK).scale(1.1)).arrange(RIGHT, buff=0.35)
    hops.move_to(RIGHT * 3.6 + UP * 2.0)
    hops[1].add_updater(lambda m: m.set_value(int(k.get_value())))
    with self.say('s01_hook') as d:
      self.play(FadeIn(grid), Create(octo), run_time=0.22 * d)
      self.add(path, head)
      self.play(FadeIn(start), FadeIn(hops), run_time=0.1 * d)
      self.play(k.animate.set_value(30), run_time=0.62 * d, rate_func=linear)
    q = T(r'Does every path\\come back?', 1.05, SECONDARY).move_to(RIGHT * 3.6 + DOWN * 0.8)
    with self.say('s01_back') as d:
      self.play(k.animate.set_value(92), run_time=0.42 * d, rate_func=linear)
      self.play(Flash(start, color=OK, flash_radius=0.45), start.animate.set_color(OK).scale(1.3), run_time=0.15 * d)
      self.play(Write(q), run_time=0.25 * d)
    hops[1].clear_updaters()
    self.play(FadeOut(Group(*self.mobjects)), run_time=0.6)


class Billiards(NarratedScene):
  def construct(self):
    b = Board(0, 4, 0, 3, 1.3, LEFT * 2.6 + UP * 0.4)
    table = b.poly([(0, 0), (4, 0), (4, 3), (0, 3)], EDGE, 6)
    pts = ordinary_path((Fr(1, 2), Fr(0)), (Fr(1), Fr(1)), 4, 3, 40)   # closes after 14 bounces
    k = ValueTracker(0)
    path = b.growing(pts, k, CHORD, 3, 0.9)
    ball = always_redraw(lambda: Dot(b.at(pts, k.get_value()), radius=0.13, color=INK))
    head = T('Ordinary billiards', 0.85, MUTED).move_to(RIGHT * 3.7 + UP * 2.6)
    B = b.p(pts[1])
    arc_in = Arc(radius=0.45, start_angle=PI, angle=PI / 4, arc_center=B).set_stroke(USE, 4)
    arc_out = Arc(radius=0.45, start_angle=-PI / 4, angle=PI / 4, arc_center=B).set_stroke(USE, 4)
    rule = T(r'angle in = angle out', 0.75, USE).move_to(RIGHT * 3.7 + UP * 1.6)
    with self.say('s02_pool') as d:
      self.play(Create(table), FadeIn(head), run_time=0.12 * d)
      self.add(path, ball)
      self.play(k.animate.set_value(1), run_time=0.1 * d, rate_func=linear)
      self.play(k.animate.set_value(1.35), Create(arc_in), Create(arc_out), FadeIn(rule), run_time=0.12 * d,
                rate_func=linear)
      self.play(k.animate.set_value(len(pts) - 1), run_time=0.45 * d, rate_func=linear)
      start = b.dot(pts[0], OK, 0.13)
      back = T('back after 14 bounces', 0.75, OK).move_to(RIGHT * 3.7 + UP * 0.7)
      self.play(Flash(start, color=OK), FadeIn(start), FadeIn(back), run_time=0.12 * d)
    pts2 = ordinary_path((0.5, 0.0), (1.0, math.sqrt(2)), 4, 3, 46)
    k2 = ValueTracker(0)
    path2 = b.growing(pts2, k2, WARM, 2, 0.8)
    ball2 = always_redraw(lambda: Dot(b.at(pts2, k2.get_value()), radius=0.13, color=INK))
    slope = T(r'slope $\sqrt{2}$: never repeats', 0.75, WARM).move_to(RIGHT * 3.7 + DOWN * 0.3)
    next_rule = T(r'Now change the rule:\\parallel lines', 0.8, SECONDARY).move_to(RIGHT * 3.7 + DOWN * 2.1)
    with self.say('s02_open') as d:
      self.play(FadeOut(VGroup(arc_in, arc_out, back)), FadeOut(path), FadeOut(ball), FadeOut(start), run_time=0.08 * d)
      self.add(path2, ball2)
      self.play(FadeIn(slope), k2.animate.set_value(len(pts2) - 1), run_time=0.55 * d, rate_func=linear)
      self.play(FadeIn(next_rule), run_time=0.15 * d)
    self.play(FadeOut(Group(*self.mobjects)), run_time=0.6)


class Rule(NarratedScene):
  def construct(self):
    b = Board(0, 4, 0, 3, 1.3, LEFT * 2.9 + DOWN * 0.35)
    R = [(0, 0), (4, 0), (4, 3), (0, 3)]
    grid = b.grid(0.3)
    rect = b.poly(R, EDGE, 5)
    title = T('Symplectic billiards', 1.0, INK).move_to(RIGHT * 3.6 + UP * 2.9)
    who = T('Albers and Tabachnikov, 2018', 0.65, MUTED).next_to(title, DOWN, buff=0.25)
    no = T(r'no angles, only parallel lines', 0.75, SECONDARY).next_to(who, DOWN, buff=0.5)
    with self.say('s03_new') as d:
      self.play(FadeIn(title), FadeIn(who), run_time=0.25 * d)
      self.play(FadeIn(grid), Create(rect), run_time=0.3 * d)
      self.play(FadeIn(no), run_time=0.15 * d)

    pts = [(1, 0), (4, 2), (1, 3), (0, 2)]
    x0 = b.dot(pts[0], EVEN, 0.11)
    x1 = b.dot(pts[1], ODD, 0.11)
    l0 = VGroup(M('x_0', 0.75, EVEN), M('(1,0)', 0.6, MUTED)).arrange(RIGHT, buff=0.15).next_to(x0, DOWN, buff=0.18)
    l1 = VGroup(M('x_1', 0.75, ODD), M('(4,2)', 0.6, MUTED)).arrange(RIGHT, buff=0.15).next_to(x1, RIGHT, buff=0.18)
    with self.say('s03_setup') as d:
      self.play(FadeOut(no), run_time=0.1 * d)
      self.play(FadeIn(x0, scale=2), FadeIn(l0), run_time=0.25 * d)
      self.wait(0.15 * d)
      self.play(FadeIn(x1, scale=2), FadeIn(l1), run_time=0.25 * d)

    r1 = T(r'$x_2$: the line through $x_0$,', 0.75).move_to(RIGHT * 3.6 + UP * 1.2)
    r2 = T(r'parallel to the side of $x_1$', 0.75).next_to(r1, DOWN, buff=0.2)
    rightside = b.side(R, 1)
    x2 = b.dot(pts[2], EVEN, 0.11)
    l2 = VGroup(M('x_2', 0.75, EVEN), M('(1,3)', 0.6, MUTED)).arrange(RIGHT, buff=0.15).next_to(x2, UP, buff=0.18)
    with self.say('s03_step') as d:
      self.play(Write(r1), Write(r2), run_time=0.2 * d)
      self.play(Create(rightside), run_time=0.12 * d)
      c1 = slide_ruler(self, b, rightside, (4, 0), (4, 3), (1, 0), (1, 3), 0.35 * d)
      self.play(FadeIn(x2, scale=2), FadeIn(l2), run_time=0.12 * d)

    top = b.side(R, 2)
    left = b.side(R, 3)
    x3 = b.dot(pts[3], ODD, 0.11)
    l3 = VGroup(M('x_3', 0.75, ODD), M('(0,2)', 0.6, MUTED)).arrange(RIGHT, buff=0.15).next_to(x3, LEFT, buff=0.18)
    l4 = M('x_4 = x_0', 0.75, OK).next_to(l0, DOWN, buff=0.12)
    with self.say('s03_again') as d:
      self.play(FadeOut(rightside), c1.animate.set_stroke(GHOST, 3), run_time=0.06 * d)
      self.play(Create(top), run_time=0.08 * d)
      c2 = slide_ruler(self, b, top, (4, 3), (0, 3), (4, 2), (0, 2), 0.25 * d)
      self.play(FadeIn(x3, scale=2), FadeIn(l3), run_time=0.08 * d)
      self.play(FadeOut(top), c2.animate.set_stroke(GHOST, 3), run_time=0.06 * d)
      self.play(Create(left), run_time=0.08 * d)
      c3 = slide_ruler(self, b, left, (0, 3), (0, 0), (1, 3), (1, 0), 0.22 * d)
      self.play(Flash(x0, color=OK), FadeIn(l4), run_time=0.1 * d)

    loop = b.poly(pts, CHORD, 4)
    per = T(r'periodic: back exactly\\where it started', 0.8, OK).move_to(RIGHT * 3.6 + DOWN * 0.6)
    pts_b = [(3, 0), (4, 1), (3, 3), (0, 1)]
    loop_b = b.poly(pts_b, CHORD, 3).set_stroke(opacity=0.5)
    dots_b = VGroup(*[b.dot(q, EVEN if i % 2 == 0 else ODD, 0.08) for i, q in enumerate(pts_b)])
    every = T('every path in a rectangle', 0.7, MUTED).next_to(per, DOWN, buff=0.4)
    with self.say('s03_period') as d:
      self.play(FadeOut(VGroup(left, c3, c1, c2, r1, r2)), run_time=0.1 * d)
      self.play(Create(loop), run_time=0.25 * d)
      self.bring_to_front(x0, x1, x2, x3)
      self.play(Write(per), run_time=0.2 * d)
      self.play(Create(loop_b), FadeIn(dots_b), FadeIn(every), run_time=0.25 * d)

    even_hop = DashedLine(b.p(pts[0]), b.p(pts[2]), dash_length=0.12).set_stroke(EVEN, 5)
    odd_hop = DashedLine(b.p(pts[1]), b.p(pts[3]), dash_length=0.12).set_stroke(ODD, 5)
    ev = T(r'even chain: $x_0, x_2, x_4, \dots$', 0.75, EVEN).move_to(RIGHT * 3.6 + UP * 1.0)
    od = T(r'odd chain: $x_1, x_3, x_5, \dots$', 0.75, ODD).next_to(ev, DOWN, buff=0.3)
    steer = T(r'each chain steers\\the other', 0.75, SECONDARY).next_to(od, DOWN, buff=0.5)
    with self.say('s03_chains') as d:
      self.play(FadeOut(VGroup(per, every, loop_b, dots_b)), loop.animate.set_stroke(opacity=0.35), run_time=0.12 * d)
      self.play(Create(even_hop), FadeIn(ev), x0.animate.scale(1.3), x2.animate.scale(1.3), run_time=0.25 * d)
      self.play(Create(odd_hop), FadeIn(od), run_time=0.25 * d)
      self.play(FadeIn(steer), run_time=0.2 * d)
    self.play(FadeOut(Group(*self.mobjects)), run_time=0.6)


class Octagon(NarratedScene):
  def construct(self):
    b = Board(0, 5, 0, 6, 1.0, LEFT * 3.4 + DOWN * 0.1)
    grid = b.grid(0.4)
    rect = b.poly([(0, 0), (5, 0), (5, 6), (0, 6)], EDGE, 4)
    cuts = VGroup(*[Polygon(b.p(a), b.p(c), b.p(e), stroke_width=0, fill_color=WARN, fill_opacity=0.45) for a, c, e in
                    [((0, 0), (2, 0), (0, 2)), ((5, 0), (5, 2), (3, 0)), ((5, 6), (4, 6), (5, 5)),
                     ((0, 6), (0, 5), (1, 6))]])
    octo = b.poly(OCT)
    dims = VGroup(M('5', 0.7, MUTED).next_to(b.p(2.5, 0), DOWN, buff=0.55),
                  M('6', 0.7, MUTED).next_to(b.p(0, 3), LEFT, buff=0.6))
    with self.say('s04_build') as d:
      self.play(FadeIn(grid), Create(rect), FadeIn(dims), run_time=0.25 * d)
      self.play(FadeIn(cuts[:2]), run_time=0.2 * d)
      self.play(FadeIn(cuts[2:]), run_time=0.2 * d)
      self.play(FadeOut(cuts, scale=0.5), ReplacementTransform(rect, octo), run_time=0.2 * d)

    eqs_tex = [('y', '0'), ('x - y', '3'), ('x', '5'), ('x + y', '10'), ('y', '6'), ('y - x', '5'), ('x', '0'),
               ('x + y', '2')]
    eqs = VGroup(*[MathTex(l, '=', r, color=INK).scale(0.85) for l, r in eqs_tex])
    for e in eqs:
      e[2].set_color(SECONDARY)
    order = [0, 1, 2, 3, 4, 5, 6, 7]
    col1 = VGroup(*[eqs[i] for i in order[:4]]).arrange(DOWN, buff=0.4, aligned_edge=LEFT)
    col2 = VGroup(*[eqs[i] for i in order[4:]]).arrange(DOWN, buff=0.4, aligned_edge=LEFT)
    table = VGroup(col1, col2).arrange(RIGHT, buff=1.0).move_to(RIGHT * 3.3 + UP * 0.6)
    whole = T('every constant is a whole number', 0.72, SECONDARY).next_to(table, DOWN, buff=0.55)
    with self.say('s04_lines') as d:
      self.play(FadeOut(dims), run_time=0.05 * d)
      for i in range(8):
        s = b.side(OCT, i, SECONDARY, 8)
        self.play(Create(s), FadeIn(eqs[i], shift=0.1 * LEFT), run_time=0.07 * d)
        self.remove(s)
      self.play(FadeIn(whole), run_time=0.15 * d)

    mirror = DashedLine(b.p(2.5, -0.5), b.p(2.5, 6.5), dash_length=0.15).set_stroke(MUTED, 3)
    mlab = M(r'x = \tfrac52', 0.7, MUTED).next_to(b.p(2.5, 6.5), UP, buff=0.05)
    name = T('special octagon', 1.0, PRIMARY).move_to(RIGHT * 3.3 + UP * 1.9)
    facts = VGroup(T('corners on the grid', 0.75), T(r'sides flat, upright or at $45^\circ$', 0.75),
                   T('a mirror', 0.75)).arrange(DOWN, buff=0.3, aligned_edge=LEFT).next_to(name, DOWN, buff=0.5)
    with self.say('s04_mirror') as d:
      self.play(Create(mirror), FadeIn(mlab), run_time=0.15 * d)
      flip = octo.copy().set_stroke(SECONDARY, 4)
      self.play(Rotate(flip, PI, axis=UP, about_point=b.p(2.5, 3)), run_time=0.25 * d)
      self.play(FadeOut(flip), FadeOut(VGroup(table, whole)), run_time=0.1 * d)
      self.play(FadeIn(name), run_time=0.12 * d)
      self.play(LaggedStart(*[FadeIn(f, shift=0.2 * RIGHT) for f in facts], lag_ratio=0.4), run_time=0.25 * d)

    self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)
    cells = VGroup()
    for idx, (per, (a, c)) in enumerate(GALLERY):
      cx = -4.6 + 4.6 * (idx % 3)
      cy = 1.85 if idx < 3 else -2.05
      gb = Board(0, 5, 0, 6, 0.47, [cx, cy + 0.15, 0])
      o = gb.poly(OCT, EDGE, 2.5)
      orb = gb.polyline(orbit_points(P, a, c, per), CHORD, 1.6, 0.85)
      lab = T(f'period {per}', 0.65, SECONDARY).next_to(o, DOWN, buff=0.15)
      cells.add(VGroup(o, orb, lab))
    with self.say('s04_conj') as d:
      self.play(LaggedStart(*[FadeIn(c[0]) for c in cells], lag_ratio=0.15), run_time=0.2 * d)
      self.play(LaggedStart(*[AnimationGroup(Create(c[1]), FadeIn(c[2])) for c in cells], lag_ratio=0.3),
                run_time=0.65 * d)
    conj = statement('Conjecture (2019)', r'In every special octagon, every path is periodic.', width=10.5)
    conj.move_to(UP * 0.6)
    quote = T(r"``we can only give computer evidence''", 0.75, MUTED).next_to(conj, DOWN, buff=0.45)
    now = T('This finding: a proof', 0.9, OK).next_to(quote, DOWN, buff=0.55)
    with self.say('s04_guess') as d:
      self.play(FadeOut(cells), run_time=0.12 * d)
      self.play(FadeIn(conj), run_time=0.25 * d)
      self.play(FadeIn(quote), run_time=0.2 * d)
      self.play(FadeIn(now, scale=1.2), run_time=0.15 * d)
    self.play(FadeOut(Group(*self.mobjects)), run_time=0.6)


class Corners(NarratedScene):
  def construct(self):
    b = Board(0, 5, 0, 6, 1.0, LEFT * 3.2 + DOWN * 0.1)
    grid = b.grid(0.4)
    octo = b.poly(OCT)
    s_right, s_diag = b.side(OCT, 2), b.side(OCT, 3)
    corner = b.dot((5, 5), CRIT, 0.12)
    qm = T('?', 1.0, SECONDARY).next_to(corner, RIGHT, buff=0.25)
    txt = T(r'a corner sits on two sides:\\which one is parallel?', 0.75).move_to(RIGHT * 3.4 + UP * 1.5)
    scope = T(r'paths considered: rule defined\\forever, forwards and backwards', 0.65, MUTED).move_to(RIGHT * 3.4 + DOWN * 0.5)
    with self.say('s05_corner') as d:
      self.play(FadeIn(grid), Create(octo), run_time=0.2 * d)
      self.play(Create(s_right), Create(s_diag), FadeIn(corner, scale=2), run_time=0.25 * d)
      self.play(FadeIn(qm), Write(txt), run_time=0.3 * d)
      self.play(FadeIn(scope), run_time=0.15 * d)

    a, c = (Fr(77, 20), Fr(17, 20)), (Fr(83, 20), Fr(23, 20))
    a2, c2 = (Fr(77, 20), Fr(6)), (Fr(83, 20), Fr(117, 20))
    da, dc = b.dot(a, EVEN, 0.08), b.dot(c, EVEN, 0.08)
    up_a = Arrow(b.p(a), b.p(a2), buff=0, stroke_width=4, tip_length=0.18, color=ACCENT)
    up_c = Arrow(b.p(c), b.p(c2), buff=0, stroke_width=4, tip_length=0.18, color=WARM)
    top_side, diag_side = b.side(OCT, 4, ACCENT, 8), b.side(OCT, 3, WARM, 8)
    ck = b.dot((4, 6), CRIT, 0.12)
    txt2 = T(r'two close starts,\\two different sides', 0.75).move_to(RIGHT * 3.4 + UP * 1.5)
    with self.say('s05_split') as d:
      self.play(FadeOut(VGroup(s_right, s_diag, qm, corner, scope)), FadeOut(txt), run_time=0.1 * d)
      self.play(FadeIn(da, scale=2), FadeIn(dc, scale=2), FadeIn(txt2), run_time=0.2 * d)
      self.play(GrowArrow(up_a), GrowArrow(up_c), run_time=0.3 * d)
      self.play(Create(top_side), Create(diag_side), FadeIn(ck, scale=2), run_time=0.2 * d)

    k = ValueTracker(0)
    path = b.growing(TRAJ, k, CHORD, 1.8, 0.55)
    even_pts = TRAJ[::2]
    reds = VGroup(*[b.dot(q, CRIT, 0.1) for q in even_pts])

    def shown():
      n = int(k.get_value() // 2) + 1
      return VGroup(*[reds[i].copy() for i in range(min(n, len(reds)))])
    red_now = always_redraw(shown)
    head = always_redraw(lambda: Dot(b.at(TRAJ, k.get_value()), radius=0.08, color=USE))
    lab_s = T('start', 0.6, MUTED).next_to(b.p(2, 0), DOWN, buff=0.15).shift(LEFT * 0.3)
    lab_e = T('end', 0.6, MUTED).next_to(b.p(3, 0), DOWN, buff=0.15).shift(RIGHT * 0.3)
    txt3 = T(r'start at a corner;\\mark the even points', 0.75).move_to(RIGHT * 3.4 + UP * 1.5)
    cnt = VGroup(T('hops', 0.7, MUTED), Integer(0).scale(0.9)).arrange(RIGHT, buff=0.3).next_to(txt3, DOWN, buff=0.6)
    cnt[1].add_updater(lambda m: m.set_value(int(k.get_value())))
    with self.say('s05_red') as d:
      self.play(FadeOut(VGroup(da, dc, up_a, up_c, top_side, diag_side, ck, txt2)), run_time=0.08 * d)
      self.play(FadeIn(txt3), FadeIn(lab_s), run_time=0.15 * d)
      self.add(path, red_now, head)
      self.play(FadeIn(cnt), run_time=0.05 * d)
      self.play(k.animate.set_value(46), run_time=0.6 * d, rate_func=linear)
      self.play(FadeIn(lab_e), run_time=0.07 * d)
    cnt[1].clear_updaters()
    allred = VGroup(*[b.dot(q, CRIT, 0.11) for q in CRIT_PTS])
    big = VGroup(Integer(20, color=CRIT).scale(1.6), T('red dots', 0.9, CRIT)).arrange(RIGHT, buff=0.3)
    big.move_to(RIGHT * 3.4 + DOWN * 0.3)
    fin = T('not infinitely many', 0.75, MUTED).next_to(big, DOWN, buff=0.35)
    with self.say('s05_twenty') as d:
      self.play(FadeOut(VGroup(path, head, txt3, cnt, lab_s, lab_e)), run_time=0.12 * d)
      self.remove(red_now)
      self.add(reds)
      self.play(FadeOut(reds), LaggedStart(*[FadeIn(r, scale=2) for r in allred], lag_ratio=0.08), run_time=0.45 * d)
      self.play(FadeIn(big), run_time=0.15 * d)
      self.play(FadeIn(fin), run_time=0.12 * d)
    self.play(FadeOut(Group(*self.mobjects)), run_time=0.6)


def arc_length(param):
  i, t = param
  L = sum(math.hypot(float(P.E[k][0]), float(P.E[k][1])) for k in range(i))
  return L + float(t) * math.hypot(float(P.E[i][0]), float(P.E[i][1]))


PERIM = 10 + 6 * math.sqrt(2)
BREAKS = {i: sorted({Fr(0), Fr(1)} | {t for (j, t) in C_SET if j == i}) for i in range(8)}


def cell_of(param):
  i, t = param
  for a, c in zip(BREAKS[i], BREAKS[i][1:]):
    if a < t < c:
      return (i, a, c)
  return None


def box_sequence():
  """Cells visited by the box of the period-16 orbit (exactly as in check_numbers.py)."""
  a, c = GALLERY[1][1]
  seq = orbit_params(P, a, c, 18)
  cur = (cell_of(seq[0]), cell_of(seq[1]))
  out = [cur]
  for _ in range(16):
    I, J = cur
    mid = P.sigma((I[0], (I[1] + I[2]) / 2), P.E[J[0]])
    kk = mid[0]
    ta = _image_parameter(P, I[0], I[1], P.E[J[0]], kk)
    tb = _image_parameter(P, I[0], I[2], P.E[J[0]], kk)
    cur = (J, (kk, min(ta, tb), max(ta, tb)))
    out.append(cur)
  return seq, out


class Boxes(NarratedScene):
  def construct(self):
    mb = Board(0, 5, 0, 6, 0.6, [-4.9, 1.55, 0])
    octo = mb.poly(OCT, EDGE, 3)
    reds = VGroup(*[mb.dot(q, CRIT, 0.07) for q in CRIT_PTS])
    L = 5.6
    X0, Y0 = -0.3, -3.05
    scale = L / PERIM

    def ax_pt(s):
      return np.array([X0 + s * scale, Y0, 0.0])
    sides = VGroup(*[mb.side(OCT, i, EDGE, 3) for i in range(8)])
    flat = VGroup()
    for i in range(8):
      s0 = arc_length((i, Fr(0)))
      s1 = s0 + math.hypot(float(P.E[i][0]), float(P.E[i][1]))
      flat.add(Line(ax_pt(s0), ax_pt(s1)).set_stroke(EDGE, 3))
    red_s = [arc_length(c) for c in sorted(C_SET)]
    flat_reds = VGroup(*[Dot(ax_pt(s), radius=0.07, color=CRIT) for s in red_s])
    sorted_c = sorted(C_SET)
    reds_in_order = VGroup(*[mb.dot(P.point(c), CRIT, 0.07) for c in sorted_c])
    with self.say('s06_unroll') as d:
      self.play(Create(octo), FadeIn(reds_in_order), run_time=0.2 * d)
      self.add(sides)
      self.play(*[TransformFromCopy(sides[i], flat[i]) for i in range(8)],
                *[TransformFromCopy(reds_in_order[j], flat_reds[j]) for j in range(len(sorted_c))], run_time=0.5 * d)
      pieces = T('20 pieces', 0.7, CRIT).next_to(flat, DOWN, buff=0.15)
      self.play(FadeIn(pieces), run_time=0.15 * d)

    axis_x = VGroup(flat, flat_reds)
    axis_y = axis_x.copy()
    sq = Square(L).set_stroke(MUTED, 2).move_to([X0 + L / 2, Y0 + L / 2, 0])
    lab_x = T('where it is', 0.65, EVEN).next_to(sq, DOWN, buff=0.12).shift(RIGHT * 1.5)
    lab_y = T(r'where it\\goes next', 0.65, ODD).next_to(sq, LEFT, buff=0.25).shift(DOWN * 1.2)
    seq, cells = box_sequence()
    pts16 = [P.point(q) for q in seq]
    sv = [arc_length(q) for q in seq]

    def state_pos(j):
      return np.array([X0 + sv[j] * scale, Y0 + sv[j + 1] * scale, 0.0])
    sdot = Dot(state_pos(0), radius=0.09, color=USE)
    gx = Dot(mb.p(pts16[0]), radius=0.1, color=EVEN)
    gy = Dot(mb.p(pts16[1]), radius=0.1, color=ODD)
    chord = Line(mb.p(pts16[0]), mb.p(pts16[1])).set_stroke(CHORD, 3)
    px = DashedLine(state_pos(0), [state_pos(0)[0], Y0, 0], dash_length=0.08).set_stroke(EVEN, 2)
    py = DashedLine(state_pos(0), [X0, state_pos(0)[1], 0], dash_length=0.08).set_stroke(ODD, 2)
    with self.say('s06_square') as d:
      self.play(FadeOut(pieces), FadeOut(sides), run_time=0.08 * d)
      self.play(Rotate(axis_y, PI / 2, about_point=ax_pt(0)), Create(sq), run_time=0.3 * d)
      self.play(FadeIn(gx, scale=2), FadeIn(gy, scale=2), Create(chord), run_time=0.17 * d)
      self.play(FadeIn(lab_x), FadeIn(lab_y), run_time=0.13 * d)
      self.play(Create(px), Create(py), FadeIn(sdot, scale=2), run_time=0.2 * d)

    vlines = VGroup(*[Line([X0 + s * scale, Y0, 0], [X0 + s * scale, Y0 + L, 0]) for s in red_s])
    hlines = VGroup(*[Line([X0, Y0 + s * scale, 0], [X0 + L, Y0 + s * scale, 0]) for s in red_s])
    gridlines = VGroup(vlines, hlines).set_stroke(CRIT, 1.3, 0.55)

    def box_rect(cell):
      I, J = cell
      x0, x1 = arc_length((I[0], I[1])), arc_length((I[0], I[2]))
      y0, y1 = arc_length((J[0], J[1])), arc_length((J[0], J[2]))
      r = Rectangle(width=(x1 - x0) * scale, height=(y1 - y0) * scale)
      r.move_to([X0 + (x0 + x1) / 2 * scale, Y0 + (y0 + y1) / 2 * scale, 0])
      return r.set_stroke(USE, 3).set_fill(USE, 0.55)
    box = box_rect(cells[0])
    with self.say('s06_boxes') as d:
      self.play(FadeOut(px), FadeOut(py), Create(vlines), Create(hlines), run_time=0.35 * d)
      cnt = T('fewer than 400 boxes', 0.65, CRIT).next_to(sq, UP, buff=0.12)
      self.play(FadeIn(cnt), run_time=0.15 * d)
      self.play(FadeIn(box), run_time=0.2 * d)
      self.bring_to_front(sdot)
    hopn = VGroup(T('hop', 0.7, MUTED), Integer(0).scale(0.85)).arrange(RIGHT, buff=0.25)
    hopn.move_to([-4.9, -1.5, 0])
    with self.say('s06_hop') as d:
      self.play(FadeOut(cnt), FadeIn(hopn), run_time=0.08 * d)
      per = 0.72 * d / 16
      for j in range(16):
        nb = box_rect(cells[j + 1])
        self.play(Transform(box, nb), sdot.animate.move_to(state_pos(j + 1)),
                  gx.animate.move_to(mb.p(pts16[j + 1])), gy.animate.move_to(mb.p(pts16[j + 2])),
                  chord.animate.put_start_and_end_on(mb.p(pts16[j + 1]), mb.p(pts16[j + 2])),
                  hopn[1].animate.set_value(j + 1), run_time=per)
      self.play(Flash(sdot, color=OK, flash_radius=0.4), box.animate.set_color(OK), run_time=0.12 * d)

    lines = VGroup(T('same side sequence = one region', 0.65), T(r'each region contains a box', 0.7),
                   T(r'finitely many regions; each returns', 0.65, OK)).arrange(DOWN, buff=0.35, aligned_edge=LEFT)
    lines.move_to([-4.3, -1.2, 0])
    with self.say('s06_pigeon') as d:
      self.play(FadeOut(hopn), FadeOut(VGroup(octo, reds_in_order, gx, gy, chord)), run_time=0.1 * d)
      lines.move_to([-4.0, 1.0, 0])
      self.play(FadeIn(lines[0], shift=0.2 * RIGHT), run_time=0.15 * d)
      self.wait(0.15 * d)
      self.play(FadeIn(lines[1], shift=0.2 * RIGHT), run_time=0.15 * d)
      self.wait(0.15 * d)
      self.play(FadeIn(lines[2], shift=0.2 * RIGHT), run_time=0.15 * d)

    b0 = Rectangle(width=1.0, height=0.7).set_stroke(USE, 3).set_fill(USE, 0.5).move_to([-5.4, -1.6, 0])
    b0.add(Dot(b0.get_corner(UL) + [0.15, -0.15, 0], radius=0.07, color=BACKGROUND))
    flip = b0.copy().move_to([-3.4, -1.6, 0])
    stretch = b0.copy().move_to([-3.4, -2.9, 0])
    ok = tick(0.8).next_to(flip, RIGHT, buff=0.25)
    no = xmark(stretch.get_right() + RIGHT * 1.0)
    with self.say('s06_stretch') as d:
      self.play(FadeIn(b0), run_time=0.1 * d)
      self.play(Rotate(flip, PI, axis=UP), run_time=0.2 * d)
      self.play(FadeIn(ok), run_time=0.08 * d)
      self.play(stretch.animate.stretch(1.9, 0), run_time=0.2 * d)
      self.play(Create(no), run_time=0.1 * d)
      laps = T(r'2 laps: separate coordinates\\4 laps: undo the flips', 0.65, OK).move_to([-4.0, -0.3, 0])
      self.play(FadeIn(laps), run_time=0.08 * d)
      self.play(Flash(sdot, color=OK), run_time=0.15 * d)
    self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)
    crit = statement('Criterion (Albers, Lander, Westermann)',
                     r'If there are only finitely many red dots, every path is periodic.', width=10.5, color=OK)
    crit.move_to(UP * 0.8)
    ask = T('So: are the red dots finite?', 0.95, SECONDARY).next_to(crit, DOWN, buff=0.8)
    with self.say('s06_rule') as d:
      self.play(FadeIn(crit), run_time=0.3 * d)
      self.wait(0.3 * d)
      self.play(Write(ask), run_time=0.3 * d)
    self.play(FadeOut(Group(*self.mobjects)), run_time=0.6)


def naive_points(cap):
  from collections import deque
  F = [(i, Fr(0)) for i in range(8)]
  seen = set(F)
  queue = deque(F)
  dirs = [(1, 0), (0, 1), (1, 1), (1, -1)]
  while queue and len(F) < cap:
    p = queue.popleft()
    for d in dirs:
      q = P.sigma(p, d)
      if q is not None and q not in seen:
        seen.add(q)
        F.append(q)
        queue.append(q)
  return [P.point(q) for q in F[:cap]]


class Naive(NarratedScene):
  def construct(self):
    b = Board(0, 5, 0, 6, 1.0, LEFT * 3.2 + DOWN * 0.1)
    grid = b.grid(0.4)
    octo = b.poly(OCT)
    pts = naive_points(1200)
    dens = [math.lcm(p[0].denominator, p[1].denominator) for p in pts]
    corners = VGroup(*[b.dot(v, CRIT, 0.1) for v in OCT])
    dirs = VGroup(*[Arrow(ORIGIN, v, buff=0, stroke_width=5, tip_length=0.2, color=SECONDARY)
                    for v in (RIGHT * 0.7, UP * 0.7, (RIGHT + UP) * 0.5, (RIGHT + DOWN) * 0.5)])
    dirs.arrange(RIGHT, buff=0.5).move_to(RIGHT * 3.4 + UP * 2.4)
    t1 = T(r'slide from the corners\\in all four directions', 0.75).next_to(dirs, DOWN, buff=0.4)
    with self.say('s07_naive') as d:
      self.play(FadeIn(grid), Create(octo), FadeIn(corners), run_time=0.25 * d)
      self.play(FadeIn(dirs), FadeIn(t1), run_time=0.25 * d)
      first = VGroup(*[b.dot(q, SECONDARY, 0.06) for q in pts[8:40]])
      self.play(LaggedStart(*[FadeIn(x, scale=2) for x in first], lag_ratio=0.1), run_time=0.35 * d)
    n_lab = VGroup(T('points', 0.7, MUTED), Integer(40).scale(0.85)).arrange(RIGHT, buff=0.3)
    d_lab = VGroup(T('finest fraction', 0.7, MUTED), MathTex(r'\tfrac{1}{%d}' % max(dens[:40])).scale(0.95))
    d_lab.arrange(RIGHT, buff=0.3)
    labs = VGroup(n_lab, d_lab).arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to(RIGHT * 3.4 + DOWN * 0.3)
    with self.say('s07_fail') as d:
      self.play(FadeIn(labs), run_time=0.08 * d)
      marks = [40, 120, 300, 600, 1200]
      for lo, hi in zip(marks, marks[1:]):
        batch = VGroup(*[b.dot(q, SECONDARY, 0.045) for q in pts[lo:hi]])
        newd = MathTex(r'\tfrac{1}{%d}' % max(dens[:hi])).scale(0.95).move_to(d_lab[1], aligned_edge=LEFT)
        self.play(FadeIn(batch), n_lab[1].animate.set_value(hi), Transform(d_lab[1], newd), run_time=0.11 * d)
      more = T(r'after 20{,}000 points: not finished,\\denominators up to 16{,}384', 0.7, CRIT)
      more.next_to(labs, DOWN, buff=0.5)
      self.play(FadeIn(more), run_time=0.15 * d)
    self.play(FadeOut(Group(*self.mobjects)), run_time=0.6)


def half_grid(b):
  g = VGroup()
  for i in range(11):
    for j in range(13):
      g.add(Dot(b.p(Fr(i, 2), Fr(j, 2)), radius=0.03, color=GHOST))
  return g


class Dots(NarratedScene):
  def construct(self):
    b = Board(0, 5, 0, 6, 1.0, LEFT * 3.2 + DOWN * 0.1)
    grid = b.grid(0.4)
    octo = b.poly(OCT)
    hg = half_grid(b)
    eg = M(r'(3\tfrac12,\ 2)', 0.7, MUTED)
    ex = Dot(b.p(Fr(7, 2), 2), radius=0.08, color=SECONDARY)
    eg.next_to(ex, RIGHT, buff=0.15)
    head = T('The half grid', 0.9, INK).move_to(RIGHT * 3.4 + UP * 2.6)
    with self.say('s08_half') as d:
      self.play(FadeIn(grid), Create(octo), FadeIn(head), run_time=0.25 * d)
      self.play(FadeIn(hg, lag_ratio=0.01), run_time=0.35 * d)
      self.play(FadeIn(ex, scale=2), FadeIn(eg), run_time=0.2 * d)

    gd = VGroup(*[b.dot(q, GREEN_DOT, 0.11) for q in S_GREEN])
    bd = VGroup(*[b.dot(q, BLUE_DOT, 0.11) for q in S_BLUE])
    od = VGroup(*[b.dot(q, ORANGE_DOT, 0.11) for q in S_ORANGE])

    def key(color, text):
      return VGroup(Dot(radius=0.12, color=color), T(text, 0.7)).arrange(RIGHT, buff=0.3)
    k1 = key(GREEN_DOT, 'whole number points')
    k2 = key(BLUE_DOT, r'slanted side, both end in $\tfrac12$')
    k3 = key(ORANGE_DOT, r'top or bottom, $x$ ends in $\tfrac12$')
    keys = VGroup(k1, k2, k3).arrange(DOWN, buff=0.4, aligned_edge=LEFT).move_to(RIGHT * 3.5 + UP * 1.0)
    with self.say('s08_kinds') as d:
      self.play(FadeOut(ex), FadeOut(eg), FadeOut(head), hg.animate.set_opacity(0.5), run_time=0.08 * d)
      self.play(FadeIn(k1), LaggedStart(*[FadeIn(x, scale=2) for x in gd], lag_ratio=0.05), run_time=0.22 * d)
      self.play(FadeIn(k2), LaggedStart(*[FadeIn(x, scale=2) for x in bd], lag_ratio=0.1), run_time=0.3 * d)
      self.play(FadeIn(k3), LaggedStart(*[FadeIn(x, scale=2) for x in od], lag_ratio=0.1), run_time=0.3 * d)

    count = MathTex('16', '+', '6', '+', '4', '=', '26').scale(1.0)
    count[0].set_color(GREEN_DOT)
    count[2].set_color(BLUE_DOT)
    count[4].set_color(ORANGE_DOT)
    count.next_to(keys, DOWN, buff=0.5)
    lemma = T(r'\textbf{Key lemma:} every even point of a\\path from a corner lands on a dot', 0.7, SECONDARY)
    lemma.next_to(count, DOWN, buff=0.5)
    rings = VGroup(*[Circle(radius=0.19, color=CRIT, stroke_width=4).move_to(b.p(q)) for q in CRIT_PTS])
    with self.say('s08_claim') as d:
      self.play(Write(count), run_time=0.25 * d)
      self.play(FadeIn(lemma), run_time=0.25 * d)
      self.play(LaggedStart(*[Create(r) for r in rings], lag_ratio=0.05), run_time=0.35 * d)
    self.play(FadeOut(Group(*self.mobjects)), run_time=0.6)


class Why(NarratedScene):
  def construct(self):
    b = Board(0, 5, 0, 6, 0.98, LEFT * 3.7 + DOWN * 0.1)
    grid = b.grid(0.35)
    octo = b.poly(OCT)
    faint = VGroup(*[b.dot(q, c, 0.08).set_opacity(0.45) for qs, c in
                     ((S_GREEN, GREEN_DOT), (S_BLUE, BLUE_DOT), (S_ORANGE, ORANGE_DOT)) for q in qs])
    PX = 3.3

    def icon(v):
      return DoubleArrow(-v * 0.4, v * 0.4, buff=0, stroke_width=5, tip_length=0.16, color=SECONDARY)
    rows = VGroup(
      VGroup(icon(UP), T(r'upright: $x$ stays', 0.75)),
      VGroup(icon(RIGHT), T(r'sideways: $y$ stays', 0.75)),
      VGroup(icon((UP + RIGHT) / math.sqrt(2)), T(r'slope up: $x - y$ stays', 0.75)),
      VGroup(icon((DOWN + RIGHT) / math.sqrt(2)), T(r'slope down: $x + y$ stays', 0.75)))
    for r in rows:
      r.arrange(RIGHT, buff=0.4)
    rows.arrange(DOWN, buff=0.45, aligned_edge=LEFT).move_to(RIGHT * PX + UP * 0.3)
    with self.say('s09_keep') as d:
      self.play(FadeIn(grid), Create(octo), FadeIn(faint), run_time=0.2 * d)
      for r in rows:
        self.play(FadeIn(r, shift=0.15 * RIGHT), run_time=0.15 * d)

    E = TRAJ[::2]

    def hop(i, color=USE):
      return Arrow(b.p(E[i]), b.p(E[i + 1]), buff=0.06, stroke_width=5, tip_length=0.2, color=color)
    d0 = b.dot(E[0], CRIT, 0.11)
    l0 = M(ptex(E[0]), 0.65).next_to(d0, DOWN, buff=0.15)
    line1 = DashedLine(b.p(2, 0), b.p(5, 3), dash_length=0.12).set_stroke(SECONDARY, 2)
    e1 = MathTex('x', '-', 'y', '=', '2').scale(0.95)
    e2 = MathTex('x', '=', '5').scale(0.95)
    eqs = VGroup(e1, e2).arrange(DOWN, buff=0.35).move_to(RIGHT * PX + UP * 1.2)
    e3 = MathTex('5', '-', 'y', '=', '2').scale(0.95).move_to(e1)
    e4 = MathTex('y', '=', '3').scale(0.95).move_to(eqs.get_center() + DOWN * 1.3)
    h1 = hop(0)
    side_x5 = b.side(OCT, 2)
    d1 = b.dot(E[1], CRIT, 0.11)
    l1 = M(ptex(E[1]), 0.65).next_to(d1, RIGHT, buff=0.15)
    with self.say('s09_slope') as d:
      self.play(FadeOut(rows), FadeIn(d0, scale=2), FadeIn(l0), run_time=0.15 * d)
      self.play(GrowArrow(h1), FadeIn(e1), run_time=0.25 * d)
      self.play(FadeIn(e2), Create(side_x5), run_time=0.15 * d)
      self.play(TransformMatchingTex(e1.copy(), e3), FadeOut(e1), run_time=0.15 * d)
      self.play(FadeIn(e4), FadeIn(d1, scale=2), FadeIn(l1), Indicate(e4, color=GREEN_DOT), run_time=0.2 * d)

    mirror = DashedLine(b.p(2.5, -0.4), b.p(2.5, 6.4), dash_length=0.15).set_stroke(MUTED, 3)
    m1 = MathTex(r'x \;\to\; 5 - x').scale(0.95).move_to(RIGHT * PX + UP * 1.6)
    m2 = MathTex(r'5 \;\to\; 0').scale(0.95).next_to(m1, DOWN, buff=0.35)
    m3 = T(r'whole stays whole,\\half stays half', 0.75, GREEN_DOT).next_to(m2, DOWN, buff=0.45)
    h2 = hop(1)
    d2 = b.dot(E[2], CRIT, 0.11)
    with self.say('s09_mirror') as d:
      self.play(FadeOut(VGroup(e2, e3, e4, l0, l1, side_x5)), h1.animate.set_color(CRIT).set_opacity(0.6), run_time=0.1 * d)
      self.play(Create(mirror), FadeIn(m1), run_time=0.2 * d)
      self.play(GrowArrow(h2), FadeIn(m2), run_time=0.2 * d)
      self.play(FadeIn(d2, scale=2), FadeIn(m3), run_time=0.15 * d)
      rest = []
      for i in (2, 3, 4):
        hh = hop(i, CRIT).set_opacity(0.6)
        rest.append(hh)
        self.play(GrowArrow(hh), FadeIn(b.dot(E[i + 1], CRIT, 0.11), scale=2), run_time=0.07 * d)
      h2.set_color(CRIT).set_opacity(0.6)

    l5 = M(ptex(E[5]), 0.65).next_to(b.p(E[5]), UP, buff=0.2).shift(RIGHT * 0.45)
    ln_a = DashedLine(b.p(0, 4), b.p(4, 0), dash_length=0.12).set_stroke(SECONDARY, 2)
    a1 = MathTex('x', '+', 'y', '=', '4').scale(0.95)
    a2 = MathTex('x', '-', 'y', '=', '3').scale(0.95)
    sys_ = VGroup(a1, a2).arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to(RIGHT * PX + UP * 1.7)
    bar = Line(LEFT * 1.1, RIGHT * 1.1).set_stroke(MUTED, 2).next_to(sys_, DOWN, buff=0.2)
    s1 = MathTex('2x', '=', '7').scale(0.95).next_to(bar, DOWN, buff=0.25)
    s2 = MathTex('x', '=', r'\tfrac{7}{2}').scale(0.95).move_to(s1)
    s3 = MathTex('y', '=', r'\tfrac{1}{2}').scale(0.95).next_to(s2, DOWN, buff=0.35)
    h5 = hop(5)
    side_d = b.side(OCT, 1, SECONDARY, 8)
    d6 = b.dot(E[6], BLUE_DOT, 0.13)
    l6 = M(ptex(E[6]), 0.65, BLUE_DOT).next_to(d6, RIGHT, buff=0.15)
    with self.say('s09_halve') as d:
      self.play(FadeOut(VGroup(m1, m2, m3)), FadeIn(l5), run_time=0.08 * d)
      self.play(Create(ln_a), FadeIn(a1), a1[4].animate.set_color(SECONDARY), run_time=0.17 * d)
      self.play(Create(side_d), FadeIn(a2), run_time=0.15 * d)
      self.play(Create(bar), ReplacementTransform(VGroup(a1, a2).copy(), s1), run_time=0.2 * d)
      self.play(TransformMatchingTex(s1, s2), run_time=0.12 * d)
      self.play(FadeIn(s3), GrowArrow(h5), run_time=0.1 * d)
      self.play(FadeIn(d6, scale=2), FadeIn(l6), Flash(d6, color=BLUE_DOT), run_time=0.1 * d)

    rule = T(r'whole $+$ whole, halved:\\whole or half, never a quarter', 0.75, GREEN_DOT)
    rule.move_to(RIGHT * PX + UP * 1.6)
    h6 = hop(6)
    d7 = b.dot(E[7], ORANGE_DOT, 0.13)
    l7 = M(ptex(E[7]), 0.65, ORANGE_DOT).next_to(d7, UP, buff=0.15)
    with self.say('s09_never') as d:
      self.play(FadeOut(VGroup(sys_, bar, s2, s3, ln_a, l5, side_d)), h5.animate.set_color(CRIT).set_opacity(0.6),
                run_time=0.1 * d)
      self.play(FadeIn(rule), run_time=0.3 * d)
      self.play(GrowArrow(h6), run_time=0.25 * d)
      self.play(FadeIn(d7, scale=2), FadeIn(l7), Flash(d7, color=ORANGE_DOT), run_time=0.15 * d)

    bad1, bad2 = (5, Fr(9, 2)), (Fr(5, 4), Fr(3, 4))
    g1 = DashedLine(b.p(E[7]), b.p(bad1), dash_length=0.1).set_stroke(GHOST, 4)
    g2 = DashedLine(b.p(bad1), b.p(bad2), dash_length=0.1).set_stroke(GHOST, 4)
    gb1, gb2 = b.dot(bad1, GHOST, 0.1), b.dot(bad2, GHOST, 0.1)
    gl1 = M(ptex(bad1), 0.65, GHOST).next_to(gb1, RIGHT, buff=0.15)
    gl2 = M(ptex(bad2), 0.65, GHOST).next_to(gb2, LEFT, buff=0.15).shift(UP * 0.2)
    x1, x2 = xmark(b.p(bad1)), xmark(b.p(bad2))
    dang = T(r'if a slanted hop left an orange dot:\\quarters, and the pattern breaks', 0.72, CRIT)
    dang.move_to(RIGHT * PX + UP * 1.6)
    with self.say('s09_danger') as d:
      self.play(FadeOut(rule), run_time=0.08 * d)
      self.play(FadeIn(dang), run_time=0.15 * d)
      self.play(Create(g1), FadeIn(gb1), FadeIn(gl1), run_time=0.22 * d)
      self.play(Create(g2), FadeIn(gb2), FadeIn(gl2), run_time=0.22 * d)
      self.play(Create(x1), Create(x2), run_time=0.15 * d)

    o13, o15 = TRAJ[13], TRAJ[15]
    do13 = b.dot(o13, ODD, 0.12)
    do15 = b.dot(o15, ODD, 0.12)
    lo13 = M('x_{13}', 0.7, ODD).next_to(do13, RIGHT, buff=0.15)
    lo15 = M('x_{15}', 0.7, ODD).next_to(do15, UP, buff=0.2).shift(RIGHT * 0.45)
    rside, lside = b.side(OCT, 2), b.side(OCT, 6)
    oh = Arrow(b.p(o13), b.p(o15), buff=0.08, stroke_width=4, tip_length=0.18, color=ODD)
    r1 = T(r'odd point $x_{13}$: upright side', 0.75)
    r2 = T(r'sideways hop = mirror', 0.75, ODD)
    r3 = T(r'odd point $x_{15}$: upright side', 0.75)
    rs = VGroup(r1, r2, r3).arrange(DOWN, buff=0.4, aligned_edge=LEFT).move_to(RIGHT * PX + UP * 0.9)
    with self.say('s09_rescue') as d:
      self.play(FadeOut(VGroup(dang, g1, g2, gb1, gb2, gl1, gl2, x1, x2)), run_time=0.08 * d)
      self.play(Create(rside), FadeIn(do13, scale=2), FadeIn(lo13), Indicate(h6, color=SECONDARY), FadeIn(r1),
                run_time=0.25 * d)
      self.play(Create(mirror.copy().set_stroke(SECONDARY, 3)), FadeIn(r2), run_time=0.2 * d)
      self.play(GrowArrow(oh), run_time=0.15 * d)
      self.play(Create(lside), FadeIn(do15, scale=2), FadeIn(lo15), FadeIn(r3), run_time=0.2 * d)

    down = Arrow(b.p(E[7]), b.p(E[8]), buff=0.06, stroke_width=6, tip_length=0.22, color=OK)
    fin = T(r'next even hop: upright again,\\$x$ stays $3\tfrac12$', 0.75, OK).next_to(rs, DOWN, buff=0.5)
    ok = tick(1.0).next_to(fin, RIGHT, buff=0.3)
    with self.say('s09_down') as d:
      self.play(GrowArrow(down), run_time=0.35 * d)
      self.play(FadeIn(fin), FadeIn(ok), run_time=0.3 * d)
    self.play(FadeOut(Group(*self.mobjects)), run_time=0.6)


class Conclude(NarratedScene):
  def construct(self):
    s1 = T(r'here: even points from corners\\land on 26 dots', 0.75)
    s2 = T(r'only finitely many\\red dots', 0.8, CRIT)
    s3 = T(r'every path\\is periodic', 0.8, OK)
    chain = VGroup(s1, s2, s3).arrange(RIGHT, buff=1.4).move_to(UP * 2.0)
    chain.scale_to_fit_width(12.5)
    arrows = VGroup(Arrow(s1.get_right(), s2.get_left(), buff=0.2, color=MUTED),
                    Arrow(s2.get_right(), s3.get_left(), buff=0.2, color=MUTED))
    gen = MathTex('N', '=', '4W + 2H - 2(c_1 + c_2)').scale(0.95)
    gen2 = MathTex('N', '=', r'4\cdot 5 + 2\cdot 6 - 2(1 + 2)').scale(0.95)
    gen3 = MathTex('N', '=', '26').scale(0.95)
    gen.move_to(DOWN * 0.1)
    gen2.move_to(gen)
    gen3.move_to(gen)
    every = T('every special octagon: a finite count', 0.75, MUTED).next_to(gen, DOWN, buff=0.4)
    thm = T(r'\textbf{Theorem:} the 2019 conjecture is true', 0.9, OK).move_to(DOWN * 2.3)
    with self.say('s10_done') as d:
      self.play(FadeIn(s1), run_time=0.12 * d)
      self.play(GrowArrow(arrows[0]), FadeIn(s2), run_time=0.15 * d)
      self.play(GrowArrow(arrows[1]), FadeIn(s3), run_time=0.15 * d)
      self.play(FadeIn(gen), FadeIn(every), run_time=0.15 * d)
      self.play(TransformMatchingTex(gen, gen2), run_time=0.12 * d)
      self.play(TransformMatchingTex(gen2, gen3), run_time=0.1 * d)
      self.play(FadeIn(thm, scale=1.1), run_time=0.12 * d)
    bound = MathTex(r'\text{period} \le 4(N^2 - N) = 2600').scale(0.95).move_to(DOWN * 0.3)
    seen = T('largest period in the reported samples: 92', 0.75, SECONDARY).next_to(bound, DOWN, buff=0.5)
    with self.say('s10_bound') as d:
      self.play(FadeOut(VGroup(gen3, every, thm)), run_time=0.1 * d)
      self.play(Write(bound), run_time=0.35 * d)
      self.play(FadeIn(seen), run_time=0.25 * d)
    self.play(FadeOut(Group(*self.mobjects)), run_time=0.6)


class Lopsided(NarratedScene):
  def construct(self):
    b = Board(0, 4, 0, 5, 1.15, LEFT * 3.6 + DOWN * 0.1)
    grid = b.grid(0.4)
    q = b.poly(QV)
    ghost = b.poly([(4 - x, y) for x, y in QV], CRIT, 3).set_stroke(opacity=0.8)
    ghost = DashedVMobject(ghost, num_dashes=40)
    mirror = DashedLine(b.p(2, -0.4), b.p(2, 5.4), dash_length=0.15).set_stroke(MUTED, 3)
    PX = 3.4
    xm = xmark(b.p(Fr(3, 2), 5) + UP * 0.55)
    t1 = T(r'corners on the grid, same\\four directions, no mirror', 0.75).move_to(RIGHT * PX + UP * 2.6)
    with self.say('s11_q') as d:
      self.play(FadeIn(grid), Create(q), run_time=0.25 * d)
      self.play(FadeIn(t1), run_time=0.15 * d)
      self.play(Create(mirror), Create(ghost), run_time=0.3 * d)
      self.play(Create(xm), run_time=0.1 * d)

    lp = [(Fr(a), Fr(c)) for a, c in LOOP]
    loop = b.poly(lp, CHORD, 3.5)
    ld = VGroup(*[b.dot(p, EVEN if i % 2 == 0 else ODD, 0.1) for i, p in enumerate(lp)])
    rows = VGroup(*[MathTex(f'x_{i}', '=', ptex(p), color=EVEN if i % 2 == 0 else ODD).scale(0.7)
                    for i, p in enumerate(lp)]).arrange(DOWN, buff=0.18, aligned_edge=LEFT)
    rows.move_to(RIGHT * PX + UP * 0.3)
    thirds = T('thirds: never on the half grid', 0.7, SECONDARY).next_to(rows, DOWN, buff=0.35)
    with self.say('s11_loop') as d:
      self.play(FadeOut(VGroup(mirror, ghost, xm)), run_time=0.08 * d)
      self.play(Create(loop), LaggedStart(*[FadeIn(x, scale=2) for x in ld], lag_ratio=0.15),
                LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.15), run_time=0.55 * d)
      self.play(FadeIn(thirds), run_time=0.2 * d)

    nl = NumberLine(x_range=[-0.5, 0.5, 0.25], length=5.4, include_tip=False, stroke_width=3,
                    color=MUTED).move_to(RIGHT * PX + DOWN * 1.7)
    zero = M('0', 0.6, MUTED).next_to(nl.n2p(0), DOWN, buff=0.2)
    halfs = VGroup(M(r'-\tfrac12', 0.6, MUTED).next_to(nl.n2p(-0.5), DOWN, buff=0.2),
                   M(r'\tfrac12', 0.6, MUTED).next_to(nl.n2p(0.5), DOWN, buff=0.2))

    def laps(a, c, n):
      pts = orbit_points(Q, a, c, 6 * n)
      return [pts[6 * j:6 * j + 7] for j in range(n)]
    even_laps = laps((4, Fr(11, 3) + Fr(1, 24)), LOOP[1], 4)
    eoffs = [Fr(1, 24), Fr(-1, 12), Fr(1, 6), Fr(-1, 3)]
    head_e = T(r'nudge $x_0$: each lap doubles and flips', 0.72, SECONDARY).next_to(nl, UP, buff=0.5)
    with self.say('s11_stretch') as d:
      self.play(FadeOut(VGroup(rows, thirds)), loop.animate.set_stroke(opacity=0.45), run_time=0.08 * d)
      self.play(Create(nl), FadeIn(zero), FadeIn(halfs), FadeIn(head_e), run_time=0.12 * d)
      prev = None
      marks = VGroup()
      plines = VGroup()
      for j, (lap, off) in enumerate(zip(even_laps, eoffs)):
        col = CRIT if j == 3 else SECONDARY
        pl = b.polyline(lap, col, 3)
        mk = VGroup(Dot(nl.n2p(float(off)), radius=0.09, color=SECONDARY),
                    M(ftex(off), 0.6, SECONDARY))
        mk[1].next_to(mk[0], UP, buff=0.15)
        anims = [Create(pl), FadeIn(mk)]
        if prev is not None:
          anims.append(prev.animate.set_stroke(opacity=0.25))
        self.play(*anims, run_time=0.16 * d)
        marks.add(mk)
        plines.add(pl)
        prev = pl
      off_txt = T('thrown off the loop', 0.7, CRIT).next_to(nl, DOWN, buff=0.75)
      self.play(FadeIn(off_txt), run_time=0.1 * d)
    odd_laps = laps(LOOP[0], (LOOP[1][0] + Fr(1, 4), 0), 4)
    ooffs = [Fr(1, 4), Fr(-1, 8), Fr(1, 16), Fr(-1, 32)]
    head_o = T(r'nudge $x_1$: each lap halves and flips', 0.72, SECONDARY).next_to(nl, UP, buff=0.5)
    with self.say('s11_squeeze') as d:
      self.play(FadeOut(VGroup(marks, plines, head_e, off_txt)), run_time=0.08 * d)
      self.play(FadeIn(head_o), run_time=0.1 * d)
      prev = None
      for j, (lap, off) in enumerate(zip(odd_laps, ooffs)):
        pl = b.polyline(lap, SECONDARY, 3)
        mk = VGroup(Dot(nl.n2p(float(off)), radius=0.09, color=SECONDARY), M(ftex(off), 0.6, SECONDARY))
        mk[1].next_to(mk[0], UP if j % 2 == 0 else DOWN, buff=0.15)
        if j % 2 == 1:
          mk[1].shift(DOWN * (0.25 if j == 1 else 0.8))
        anims = [Create(pl), FadeIn(mk)]
        if prev is not None:
          anims.append(prev.animate.set_stroke(opacity=0.25))
        self.play(*anims, run_time=0.17 * d)
        prev = pl
    never = T(r'closer every lap, never there:\\this path never repeats', 0.75, CRIT).move_to(RIGHT * PX + UP * 1.7)
    concl = T('so the mirror matters', 0.85, OK).next_to(never, DOWN, buff=0.45)
    arrow0 = Arrow(nl.n2p(0.3) + UP * 0.65, nl.n2p(0.03) + UP * 0.2, buff=0, color=CRIT, stroke_width=4,
                   tip_length=0.16)
    with self.say('s11_never') as d:
      self.play(FadeOut(t1), Indicate(zero, color=CRIT), FadeIn(never), run_time=0.35 * d)
      self.play(FadeIn(concl), run_time=0.25 * d)
    self.play(FadeOut(Group(*self.mobjects)), run_time=0.6)


class Status(NarratedScene):
  def construct(self):
    def item(mark, text, color=INK, scale=0.78):
      return VGroup(mark, T(text, scale, color)).arrange(RIGHT, buff=0.35)

    def circ():
      return Circle(0.13, color=MUTED, stroke_width=3)
    i1 = item(tick(0.85), r'written proof: all paths defined for all time are periodic', scale=0.75)
    i2 = item(circ(), r'checked in internal reviews, not yet refereed by a journal', MUTED)
    i3 = item(tick(0.85), r'two exact programs: 1484 parameter tuples, entries up to 14', scale=0.75)
    i4 = item(circ(), r'a computer check, not the proof', MUTED)
    items = VGroup(i1, i2, i3, i4).arrange(DOWN, buff=0.45, aligned_edge=LEFT).move_to(UP * 0.4)
    with self.say('s12_proved') as d:
      self.play(FadeIn(i1, shift=0.2 * RIGHT), run_time=0.25 * d)
      self.wait(0.15 * d)
      self.play(FadeIn(i2, shift=0.2 * RIGHT), run_time=0.25 * d)
    with self.say('s12_computer') as d:
      self.play(FadeIn(i3, shift=0.2 * RIGHT), run_time=0.3 * d)
      self.wait(0.3 * d)
      self.play(FadeIn(i4, shift=0.2 * RIGHT), run_time=0.2 * d)
    priority = VGroup(T('proof: high confidence', 0.85, OK),
                      T('originality: less certain', 0.85, SECONDARY),
                      T('no earlier proof found; priority not established', 0.7, MUTED)).arrange(DOWN, buff=0.55)
    with self.say('s12_priority') as d:
      self.play(FadeOut(items), FadeIn(priority), run_time=0.3 * d)

    hb = Board(0, 6, 0, 5, 0.75, LEFT * 3.0 + DOWN * 0.5)
    house = [(0, 0), (3, 0), (3, 3), (2, 5), (1, 5), (0, 3)]
    wide = [(2 * x, y) for x, y in house]
    hp = hb.poly(house, EDGE, 4)
    hw = hb.poly(wide, EDGE, 4)
    hgrid = hb.grid(0.3)
    roof = VGroup(hb.side(house, 2, SECONDARY, 7), hb.side(house, 4, SECONDARY, 7))
    roofw = VGroup(hb.side(wide, 2, SECONDARY, 7), hb.side(wide, 4, SECONDARY, 7))
    name = T('mirror-symmetric Hexhouse', 0.85, PRIMARY).move_to(RIGHT * 3.6 + UP * 2.0)
    s_a = T(r'roof slopes $\pm 2$', 0.75).next_to(name, DOWN, buff=0.5)
    s_b = T(r'stretch sideways by 2: slopes $\pm 1$', 0.75).next_to(s_a, DOWN, buff=0.35)
    s_c = T(r'a cut-corner shape: also proved', 0.8, OK).next_to(s_b, DOWN, buff=0.5)
    with self.say('s12_hex') as d:
      self.play(FadeOut(priority), run_time=0.08 * d)
      self.play(FadeIn(hgrid), Create(hp), FadeIn(name), run_time=0.2 * d)
      self.play(Create(roof), FadeIn(s_a), run_time=0.15 * d)
      self.play(ReplacementTransform(hp, hw), ReplacementTransform(roof, roofw), FadeIn(s_b), run_time=0.3 * d)
      self.play(FadeIn(s_c), run_time=0.15 * d)

    head = T('Still open', 0.95, SECONDARY).move_to(UP * 2.4)
    o = VGroup(item(circ(), 'lopsided Hexhouses', INK), item(circ(), 'the Penthouse conjecture', INK),
               item(circ(), 'octagons with sizes not in whole-number ratios', INK),
               item(circ(), 'a periodic symplectic path in every convex polygon?', INK, scale=0.7))
    o.arrange(DOWN, buff=0.4, aligned_edge=LEFT).next_to(head, DOWN, buff=0.55)
    with self.say('s12_open') as d:
      self.play(FadeOut(VGroup(hgrid, hw, roofw, name, s_a, s_b, s_c)), run_time=0.1 * d)
      self.play(FadeIn(head), run_time=0.1 * d)
      for x in o:
        self.play(FadeIn(x, shift=0.2 * RIGHT), run_time=0.15 * d)
    self.play(FadeOut(Group(*self.mobjects)), run_time=0.6)


class Ending(NarratedScene):
  def construct(self):
    r1 = T(r'1. Each new point: a parallel line from two steps back', 0.8)
    r2 = T(r'2. Finitely many points from corners $\Rightarrow$ every path repeats', 0.8)
    r3 = T(r'3. Whole-number sides and the mirror keep them on 26 dots', 0.8)
    recap = VGroup(r1, r2, r3).arrange(DOWN, buff=0.5, aligned_edge=LEFT).move_to(UP * 0.2)
    if recap.width > 13:
      recap.scale_to_fit_width(13)
    with self.say('s13_recap') as d:
      self.play(FadeIn(r1, shift=0.2 * UP), run_time=0.12 * d)
      self.wait(0.18 * d)
      self.play(FadeIn(r2, shift=0.2 * UP), run_time=0.12 * d)
      self.wait(0.18 * d)
      self.play(FadeIn(r3, shift=0.2 * UP), run_time=0.12 * d)
    head = T("What we still don't know", 0.95, SECONDARY).move_to(UP * 1.4)
    o1 = T('Do lopsided Hexhouses always repeat?', 0.8).move_to(UP * 0.1)
    o2 = T(r'A repeating symplectic path in every convex polygon?', 0.75).next_to(o1, DOWN, buff=0.45)
    with self.say('s13_end') as d:
      self.play(FadeOut(recap), run_time=0.12 * d)
      self.play(FadeIn(head), run_time=0.15 * d)
      self.play(FadeIn(o1), run_time=0.15 * d)
      self.play(FadeIn(o2), run_time=0.15 * d)
    self.play(FadeOut(VGroup(head, o1, o2)), run_time=0.6)
    t = T(r'All symplectic billiard orbits in\\special octagons are periodic', 0.95).move_to(UP * 1.2)
    org = T('Valyu Research, 2026', 0.8, MUTED).next_to(t, DOWN, buff=0.45)
    path = T(r'\texttt{maths/dynamical-systems/billiards/}\\\texttt{special-octagon-symplectic-billiards}', 0.6,
             MUTED).next_to(org, DOWN, buff=0.45)
    voice = T('Narration uses a synthetic voice.', 0.55, MUTED).to_edge(DOWN, buff=0.5)
    self.play(FadeIn(t), FadeIn(org), FadeIn(path), FadeIn(voice), run_time=1.0)
    self.wait(5)
