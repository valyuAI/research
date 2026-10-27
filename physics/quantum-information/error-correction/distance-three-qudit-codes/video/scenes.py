"""Explainer: every qudit stabilizer code of distance three.

Running example: qutrits (q = 3) with five questions (r = 5). Every number drawn here comes
from data.json, which data_prep.py rebuilds and re-checks from ../verification/.
"""

import json
from pathlib import Path

import numpy as np
from manim import *
from vrvideo import *

SCENES = ['Hook', 'Cube', 'Questions', 'Efficiency', 'Quantum', 'Dials', 'Sheets', 'Counting', 'Lines',
          'Bridge', 'Fano', 'Holes', 'Cheaters', 'Build', 'Balance', 'Answer', 'Table', 'Status', 'Recap']

HERE = Path(__file__).resolve().parent
D = json.loads((HERE / 'data.json').read_text())

# Colour meaning, used in every scene.
CODE = PRIMARY      # codewords, qudits, their lines
CHANGE = SECONDARY  # the thing currently changing
BAD = WARN          # errors, collisions, contradictions
GOOD = OK           # success
HOLE = WARM         # uncovered points
CLEAR = MUTED       # all clear, background points
SLOPE = ACCENT      # the slope lines of the construction


def digits(vals, scale=0.8, color=INK, sep=r'\,'):
  return MathTex(sep.join(str(v) for v in vals), color=color).scale(scale)


def bracket(n, k, q, d=None, scale=0.8, color=INK):
  inner = f'{n},{k}' + (f',{d}' if d is not None else '')
  return MathTex(r'[\![' + inner + r']\!]_{' + str(q) + '}', color=color).scale(scale)


# ---------------------------------------------------------------------------------------
# The schematic point field: 121 points drawn as 30 slots of four plus one spare point.
# A "line" is drawn as a bar through the four points of a slot. Layout is schematic; which
# points belong together is what matters.
SP = 0.4
BAR = 3 * SP
PX = BAR + 0.62
PY = 0.78


def slot_points(rows, cols, center):
  width = (cols - 1) * PX + BAR
  height = (rows - 1) * PY
  x0 = center[0] - width / 2
  y0 = center[1] + height / 2
  slots = []
  for i in range(rows):
    for j in range(cols):
      slots.append([np.array([x0 + j * PX + t * SP, y0 - i * PY, 0.0]) for t in range(4)])
  return slots


class Field:
  def __init__(self, rows=6, cols=5, center=(-2.0, 0.55), spare=True, radius=0.075):
    self.slots = slot_points(rows, cols, np.array([*center, 0.0]))
    pos = [p for s in self.slots for p in s]
    if spare:
      pos.append(np.array([center[0], self.slots[-1][0][1] - PY, 0.0]))
    self.pos = pos
    self.dots = VGroup(*[Dot(p, radius=radius, color=CLEAR) for p in pos])

  def slot_dots(self, k):
    return VGroup(*self.dots[4 * k:4 * k + 4])

  def bar(self, k, color=CODE, width=11, opacity=0.55):
    a, b = self.slots[k][0], self.slots[k][3]
    return Line(a + LEFT * 0.12, b + RIGHT * 0.12, color=color, stroke_width=width, stroke_opacity=opacity)


def dial(radius=1.0, color=CODE, value=0, ring=False, label_scale=0.75):
  center = ORIGIN
  face = Circle(radius, color=color, stroke_width=4)
  labels = VGroup(*[MathTex(str(k)).scale(label_scale).move_to(center + 0.68 * radius * clock_dir(k))
                    for k in range(3)])
  needle = Line(center, center + 0.42 * radius * clock_dir(value), color=CHANGE, stroke_width=6)
  hub = Dot(center, radius=0.06, color=CHANGE)
  parts = [face, labels, needle, hub]
  if ring:
    ring_c = DashedVMobject(Circle(1.28 * radius, color=CLEAR, stroke_width=2), num_dashes=30)
    marker = Dot(center + 1.28 * radius * UP, radius=0.09, color=ACCENT)
    parts += [ring_c, marker]
  g = VGroup(*parts)
  return g


def clock_dir(k):
  ang = np.pi / 2 - 2 * np.pi * k / 3
  return np.array([np.cos(ang), np.sin(ang), 0.0])


def turn(d, steps, run_time):
  """Rotate a dial's needle clockwise by `steps` settings."""
  needle = d[2]
  return Rotate(needle, angle=-2 * np.pi * steps / 3, about_point=d[0].get_center(), run_time=run_time)


def end_card():
  t = Tex(r'All qudit stabilizer codes of distance three').scale(1.0)
  v = Tex(r'Valyu Research, 2026', color=MUTED).scale(0.75)
  p1 = Tex(r'\texttt{physics/quantum-information/error-correction/}', color=MUTED).scale(0.55)
  p2 = Tex(r'\texttt{distance-three-qudit-codes}', color=MUTED).scale(0.55)
  s = Tex(r'Narration uses a synthetic voice.', color=MUTED).scale(0.5)
  g = VGroup(t, v, p1, p2).arrange(DOWN, buff=0.3)
  p2.next_to(p1, DOWN, buff=0.12)
  s.to_edge(DOWN, buff=0.5)
  return VGroup(g.move_to(UP * 0.4), s)


# ---------------------------------------------------------------------------------------
class Hook(NarratedScene):
  def construct(self):
    left, right = np.array([-5.2, 0.4, 0]), np.array([5.2, 0.4, 0])
    you = VGroup(Circle(0.5, color=CODE, stroke_width=4), Tex('you').scale(0.7)).arrange(DOWN, buff=0.2)
    you[0].move_to(left)
    you[1].next_to(you[0], DOWN, buff=0.2)
    friend = VGroup(Circle(0.5, color=CODE, stroke_width=4), Tex('friend').scale(0.7))
    friend[0].move_to(right)
    friend[1].next_to(friend[0], DOWN, buff=0.2)
    rng = np.random.default_rng(3)
    xs = np.linspace(-4.5, 4.5, 90)
    amp = np.where(np.abs(xs) < 1.3, 0.28, 0.05)
    pts = [np.array([x, 0.4 + a * rng.uniform(-1, 1), 0]) for x, a in zip(xs, amp)]
    wire = VMobject(color=CLEAR, stroke_width=3).set_points_as_corners(pts)
    static = Tex('static', color=BAD).scale(0.75).move_to(DOWN * 0.35)

    with self.say('s01_hook') as d:
      self.play(FadeIn(you), FadeIn(friend), Create(wire), run_time=0.2 * d)
      self.play(FadeIn(static), run_time=0.08 * d)
      bit = MathTex('1', color=CODE).scale(1.5).move_to(left + RIGHT * 1.0 + UP * 0.75)
      self.play(FadeIn(bit), run_time=0.08 * d)
      self.play(bit.animate.move_to(UP * 1.15 + RIGHT * 0), run_time=0.18 * d, rate_func=linear)
      zero = MathTex('0', color=BAD).scale(1.5).move_to(bit)
      self.play(Transform(bit, zero), Flash(bit, color=BAD), run_time=0.1 * d)
      self.play(bit.animate.move_to(right + LEFT * 1.0 + UP * 0.75), run_time=0.16 * d, rate_func=linear)
      hears = Tex('hears ``no\'\'', color=BAD).scale(0.75).next_to(friend, DOWN, buff=0.25)
      self.play(FadeIn(hears), run_time=0.1 * d)

    with self.say('s01_repeat') as d:
      self.play(FadeOut(bit), FadeOut(hears), run_time=0.06 * d)
      msg = VGroup(*[MathTex('1', color=CODE).scale(1.5) for _ in range(3)]).arrange(RIGHT, buff=0.35)
      msg.move_to(left + RIGHT * 1.6 + UP * 0.8)
      self.play(FadeIn(msg), run_time=0.1 * d)
      self.play(msg.animate.move_to(UP * 1.2), run_time=0.2 * d, rate_func=linear)
      z = MathTex('0', color=BAD).scale(1.5).move_to(msg[1])
      self.play(Transform(msg[1], z), Flash(msg[1], color=BAD), run_time=0.1 * d)
      self.play(msg.animate.move_to(right + LEFT * 1.6 + UP * 0.8), run_time=0.2 * d, rate_func=linear)
      vote = VGroup(Tex('majority:').scale(0.75), MathTex('1', color=GOOD).scale(1.5)).arrange(RIGHT, buff=0.25)
      vote.next_to(friend, DOWN, buff=0.45).shift(LEFT * 0.9)
      box = boxed(vote[1], color=GOOD)
      self.play(FadeIn(vote), Create(box), run_time=0.15 * d)

    with self.say('s01_question') as d:
      self.play(*[FadeOut(m) for m in [you, friend, wire, static, msg, vote, box]], run_time=0.12 * d)
      cost = MathTex(r'1', r'\;\longrightarrow\;', r'1\;1\;1').scale(1.6)
      cost[0].set_color(CODE)
      cost[2].set_color(CODE)
      cost.move_to(UP * 0.9)
      br = Brace(cost[2], DOWN, color=MUTED)
      lab = Tex('3 symbols for 1', color=MUTED).scale(0.75).next_to(br, DOWN, buff=0.15)
      self.play(Write(cost), run_time=0.2 * d)
      self.play(GrowFromCenter(br), FadeIn(lab), run_time=0.15 * d)
      q = Tex(r'How little extra can repair any single error?', color=CHANGE).scale(0.85).move_to(DOWN * 2.3)
      self.play(Write(q), run_time=0.3 * d)
    self.play(*[FadeOut(m) for m in [cost, br, lab, q]], run_time=0.6)


# ---------------------------------------------------------------------------------------
class Cube(NarratedScene):
  def construct(self):
    X, Y, Z = np.array([3.0, 0, 0]), np.array([1.5, 1.1, 0]), np.array([0, 2.9, 0])
    O = np.array([-2.6, -2.5, 0])

    def P(b):
      return O + b[0] * X + b[1] * Y + b[2] * Z

    corners = [(a, b, c) for a in range(2) for b in range(2) for c in range(2)]
    center = P((0.5, 0.5, 0.5))
    edges = VGroup(*[Line(P(u), P(v), color=CLEAR, stroke_width=3) for u in corners for v in corners
                     if u < v and sum(abs(x - y) for x, y in zip(u, v)) == 1])
    dots = {c: Dot(P(c), radius=0.09, color=INK) for c in corners}
    labels = {}
    for c in corners:
      out = P(c) - center
      out = out / np.linalg.norm(out)
      labels[c] = MathTex(''.join(map(str, c))).scale(0.75).move_to(P(c) + 0.5 * out)

    with self.say('s02_cube') as d:
      self.play(Create(edges), run_time=0.15 * d)
      self.play(*[FadeIn(dots[c]) for c in corners], *[FadeIn(labels[c]) for c in corners], run_time=0.12 * d)
      e = Line(P((0, 0, 0)), P((1, 0, 0)), color=CHANGE, stroke_width=7)
      self.play(Create(e), Indicate(labels[(1, 0, 0)], color=CHANGE), run_time=0.12 * d)
      self.play(FadeOut(e), run_time=0.04 * d)
      a, b = (0, 0, 0), (1, 1, 1)
      self.play(dots[a].animate.set_color(CODE).scale(1.6), labels[a].animate.set_color(CODE),
                dots[b].animate.set_color(ACCENT).scale(1.6), labels[b].animate.set_color(ACCENT), run_time=0.15 * d)
      path = VGroup(*[Line(P(u), P(v), color=CHANGE, stroke_width=7)
                      for u, v in [((0, 0, 0), (1, 0, 0)), ((1, 0, 0), (1, 1, 0)), ((1, 1, 0), (1, 1, 1))]])
      for seg in path:
        self.play(Create(seg), run_time=0.07 * d)
      dist = MathTex(r'\text{distance} = 3', color=CHANGE).scale(0.9).to_corner(UR, buff=0.6)
      self.play(Write(dist), run_time=0.1 * d)

    def hull(c, color):
      nbrs = [c] + [tuple(x if i != j else 1 - x for i, x in enumerate(c)) for j in range(3)]
      pts = np.array([P(n) for n in nbrs])
      mid = pts.mean(axis=0)
      ang = np.arctan2(pts[:, 1] - mid[1], pts[:, 0] - mid[0])
      pts = pts[np.argsort(ang)]
      grown = [mid + (p - mid) * 1.0 + 0.45 * (p - mid) / np.linalg.norm(p - mid) for p in pts]
      poly = Polygon(*grown, color=color, stroke_width=3, fill_color=color, fill_opacity=0.16)
      return poly.round_corners(0.35), nbrs

    with self.say('s02_balls') as d:
      self.play(FadeOut(path), run_time=0.06 * d)
      ha, na = hull((0, 0, 0), CODE)
      hb, nb = hull((1, 1, 1), ACCENT)
      self.play(FadeIn(ha), *[dots[n].animate.set_color(CODE) for n in na[1:]], run_time=0.18 * d)
      self.play(FadeIn(hb), *[dots[n].animate.set_color(ACCENT) for n in nb[1:]], run_time=0.18 * d)
      note = Tex('bubbles do not overlap', color=GOOD).scale(0.8).next_to(dist, DOWN, buff=0.3).align_to(dist, RIGHT)
      self.play(FadeIn(note), run_time=0.12 * d)
      # one error from 000 lands on 010, still inside the blue bubble
      ring = Circle(0.32, color=BAD, stroke_width=5).move_to(P((0, 1, 0)))
      self.play(Create(ring), run_time=0.1 * d)
      self.play(ring.animate.move_to(P((0, 0, 0))).set_color(GOOD), run_time=0.14 * d)
    self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.45)


# ---------------------------------------------------------------------------------------
class Questions(NarratedScene):
  def construct(self):
    xs = [-1.6, 0, 1.6]
    boxes = VGroup(*[Square(1.0, color=CODE, stroke_width=4).move_to([x, 1.75, 0]) for x in xs])
    vals = VGroup(*[MathTex('1').scale(1.2).move_to(b) for b in boxes])
    names = VGroup(*[Tex(f'bit {i + 1}', color=MUTED).scale(0.6).next_to(b, DOWN, buff=0.12) for i, b in enumerate(boxes)])
    arc1 = ArcBetweenPoints(boxes[0].get_top() + UP * 0.05, boxes[1].get_top() + UP * 0.05, angle=-1.6, color=CHANGE)
    arc2 = ArcBetweenPoints(boxes[1].get_top() + UP * 0.05, boxes[2].get_top() + UP * 0.05, angle=-1.6, color=CHANGE)
    q1 = Tex('Q1', color=CHANGE).scale(0.7).next_to(arc1, UP, buff=0.05)
    q2 = Tex('Q2', color=CHANGE).scale(0.7).next_to(arc2, UP, buff=0.05)
    key = Tex(r'agree $\to 0$, \; disagree $\to 1$', color=MUTED).scale(0.8).move_to([4.6, 1.75, 0])

    with self.say('s03_questions') as d:
      self.play(FadeIn(boxes), FadeIn(vals), FadeIn(names), run_time=0.2 * d)
      self.play(Create(arc1), FadeIn(q1), run_time=0.2 * d)
      self.play(Create(arc2), FadeIn(q2), run_time=0.2 * d)
      self.play(FadeIn(key), run_time=0.12 * d)

    head = VGroup(Tex('error', color=MUTED).scale(0.8), Tex('Q1 \\; Q2', color=MUTED).scale(0.8))
    rows_spec = [('none', '0', '0', None), ('bit 1', '1', '0', 0), ('bit 2', '1', '1', 1), ('bit 3', '0', '1', 2)]
    ys = [-0.1, -0.75, -1.4, -2.05, -2.7]
    head[0].move_to([-1.3, ys[0], 0])
    head[1].move_to([1.3, ys[0], 0])
    rule = Line([-2.4, ys[0] - 0.3, 0], [2.4, ys[0] - 0.3, 0], color=MUTED, stroke_width=2)

    with self.say('s03_table') as d:
      self.play(FadeIn(head), Create(rule), run_time=0.08 * d)
      rows = VGroup()
      for (name, a, b, flip), y in zip(rows_spec, ys[1:]):
        if flip is not None:
          red = MathTex('0', color=BAD).scale(1.2).move_to(boxes[flip])
          old = vals[flip]
          self.play(FadeOut(old), FadeIn(red), Flash(boxes[flip], color=BAD), run_time=0.06 * d)
        row = VGroup(Tex(name).scale(0.8).move_to([-1.3, y, 0]),
                     MathTex(a + r'\;\;' + b, color=CODE if flip is not None else CLEAR).scale(0.95).move_to([1.3, y, 0]))
        self.play(FadeIn(row), run_time=0.08 * d)
        rows.add(row)
        if flip is not None:
          self.play(FadeOut(red), FadeIn(old), run_time=0.04 * d)
      zeros = VGroup(*[MathTex('0', color=ACCENT).scale(1.2).move_to(b) for b in boxes])
      self.play(*[Transform(v, z) for v, z in zip(vals, zeros)], run_time=0.1 * d)
      self.play(Indicate(rows[0], color=ACCENT), run_time=0.12 * d)
    self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.45)


# ---------------------------------------------------------------------------------------
class Efficiency(NarratedScene):
  def construct(self):
    top = MathTex(r'r \text{ questions}', r'\;\Rightarrow\;', r'2^r \text{ answer lists}').scale(0.9).to_edge(UP, buff=0.6)
    cols = D['hamming_columns']
    lists = [[0, 0, 0]] + cols
    xs = np.linspace(-5.25, 5.25, 8)
    stacks = VGroup()
    for x, c in zip(xs, lists):
      col = VGroup(*[MathTex(str(b)).scale(1.0) for b in c]).arrange(DOWN, buff=0.2)
      frame = RoundedRectangle(width=0.9, height=col.height + 0.4, corner_radius=0.12,
                               color=CLEAR if not any(c) else CODE, stroke_width=3)
      g = VGroup(frame, col).move_to([x, 0.75, 0])
      stacks.add(g)
    tags = VGroup(Tex('all clear', color=CLEAR).scale(0.65).next_to(stacks[0], DOWN, buff=0.2))
    for i in range(1, 8):
      tags.add(Tex(f'bit {i}', color=CODE).scale(0.65).next_to(stacks[i], DOWN, buff=0.2))

    with self.say('s04_count') as d:
      self.play(Write(top), run_time=0.25 * d)
      self.play(LaggedStart(*[FadeIn(s) for s in stacks], lag_ratio=0.1), run_time=0.35 * d)
      self.play(FadeIn(tags[0]), stacks[0][0].animate.set_color(CHANGE), run_time=0.15 * d)
      self.play(stacks[0][0].animate.set_color(CLEAR), run_time=0.05 * d)

    eq = MathTex(r'1 + n \le 2^r', color=INK).scale(1.0).move_to(DOWN * 2.1)
    eq2 = MathTex(r'1 + n \le 8', color=INK).scale(1.0).move_to(eq)
    eq3 = MathTex(r'n \le 7', color=GOOD).scale(1.0).move_to(eq)
    with self.say('s04_hamming') as d:
      t3 = MathTex(r'3 \text{ questions}', r'\;\Rightarrow\;', r'2^3 = 8 \text{ answer lists}').scale(0.9).move_to(top)
      self.play(TransformMatchingTex(top, t3), run_time=0.15 * d)
      self.play(LaggedStart(*[FadeIn(t) for t in tags[1:]], lag_ratio=0.1), run_time=0.25 * d)
      self.play(Write(eq), run_time=0.12 * d)
      self.play(TransformMatchingShapes(eq, eq2), run_time=0.12 * d)
      self.play(TransformMatchingShapes(eq2, eq3), run_time=0.12 * d)
      ham = Tex(r'7 bits = 4 message + 3 checks', color=GOOD).scale(0.75).next_to(eq3, DOWN, buff=0.3)
      self.play(FadeIn(ham), run_time=0.12 * d)

    with self.say('s04_points') as d:
      self.play(FadeOut(eq3), FadeOut(ham), FadeOut(tags), FadeOut(stacks[0]), run_time=0.15 * d)
      dots = VGroup(*[Dot(s.get_center(), radius=0.16, color=CODE) for s in stacks[1:]])
      self.play(*[ReplacementTransform(s, dt) for s, dt in zip(stacks[1:], dots)], run_time=0.3 * d)
      cap = Tex(r'each position is a point; all points different', color=CODE).scale(0.8).move_to(DOWN * 1.4)
      self.play(FadeIn(cap), run_time=0.2 * d)
    self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.45)


# ---------------------------------------------------------------------------------------
class Quantum(NarratedScene):
  def construct(self):
    with self.say('s05_fragile') as d:
      q = dial(1.6, value=1).move_to(UP * 0.3)
      self.play(FadeIn(q), run_time=0.2 * d)
      look = Tex('look', color=CHANGE).scale(0.9).next_to(q, LEFT, buff=1.2)
      arrow = Arrow(look.get_right(), q.get_left(), color=CHANGE, buff=0.15)
      self.play(FadeIn(look), GrowArrow(arrow), run_time=0.2 * d)
      self.play(q[0].animate.set_color(BAD), Rotate(q[2], angle=2.3, about_point=q[0].get_center()), run_time=0.12 * d)
      self.play(Wiggle(q, scale_value=1.1, rotation_angle=0.05 * TAU), run_time=0.13 * d)
      lost = Tex('disturbed', color=BAD).scale(0.8).next_to(q, DOWN, buff=0.35)
      self.play(FadeIn(lost), run_time=0.12 * d)
    with self.say('s05_parity') as d:
      self.play(FadeOut(q), FadeOut(look), FadeOut(arrow), FadeOut(lost), run_time=0.06 * d)
      a = dial(1.3, value=2).move_to(LEFT * 2.4 + UP * 0.4)
      b = dial(1.3, value=2).move_to(RIGHT * 2.4 + UP * 0.4)
      arc = ArcBetweenPoints(a.get_top() + UP * 0.1, b.get_top() + UP * 0.1, angle=-1.2, color=CHANGE)
      ask = Tex('agree?', color=CHANGE).scale(0.8).next_to(arc, UP, buff=0.08)
      self.play(FadeIn(a), FadeIn(b), run_time=0.1 * d)
      self.play(Create(arc), FadeIn(ask), run_time=0.12 * d)
      ans = Tex('yes, and nothing is disturbed', color=GOOD).scale(0.85).move_to(DOWN * 1.9)
      self.play(FadeIn(ans), run_time=0.12 * d)
      self.wait(0.12 * d)
      self.play(*[FadeOut(m) for m in [a, b, arc, ask, ans]], run_time=0.06 * d)
      s = dial(1.2, value=0, ring=True).move_to(LEFT * 2.8 + UP * 0.4)
      t = dial(1.2, value=0, ring=True).move_to(RIGHT * 2.8 + UP * 0.4)
      ls = Tex('shift', color=CHANGE).scale(0.85).next_to(s, DOWN, buff=0.35)
      lt = Tex('twist', color=ACCENT).scale(0.85).next_to(t, DOWN, buff=0.35)
      self.play(FadeIn(s), FadeIn(t), run_time=0.08 * d)
      self.play(turn(s, 1, 0.12 * d), FadeIn(ls), run_time=0.12 * d)
      self.play(Rotate(t[5], angle=-2 * np.pi / 3, about_point=t[0].get_center()), FadeIn(lt), run_time=0.12 * d)
    self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.45)


# ---------------------------------------------------------------------------------------
class Dials(NarratedScene):
  def construct(self):
    q = dial(1.6, value=2, label_scale=1.0).move_to(LEFT * 3.3 + UP * 0.2)
    name = Tex('a qutrit: $q = 3$', color=CODE).scale(0.8).next_to(q, DOWN, buff=0.4)
    with self.say('s06_dial') as d:
      self.play(FadeIn(q), run_time=0.15 * d)
      self.play(FadeIn(name), run_time=0.1 * d)
      self.wait(0.15 * d)
      e1 = MathTex(r'2 + 2 = 4 \to 1').scale(1.0).move_to(RIGHT * 2.8 + UP * 1.0)
      self.play(Write(e1), turn(q, 2, 0.2 * d), run_time=0.2 * d)
      e2 = MathTex(r'2 \times 2 = 4 \to 1').scale(1.0).next_to(e1, DOWN, buff=0.5)
      self.play(Write(e2), run_time=0.15 * d)
    with self.say('s06_errors') as d:
      self.play(*[FadeOut(m) for m in [e1, e2, name]], q.animate.scale(0.8).move_to(LEFT * 4.6 + UP * 0.2), run_time=0.1 * d)
      cells = VGroup()
      size = 1.25
      for t in range(3):
        for s in range(3):
          none = s == 0 and t == 0
          sq = Square(size, color=CLEAR if none else BAD, stroke_width=3,
                      fill_color=CLEAR if none else BAD, fill_opacity=0.12)
          sq.move_to(np.array([0.3 + s * size, 1.4 - t * size, 0]))
          cells.add(sq)
      lab_s = VGroup(*[MathTex(str(s), color=CHANGE).scale(0.85).next_to(cells[s], UP, buff=0.15) for s in range(3)])
      lab_t = VGroup(*[MathTex(str(t), color=ACCENT).scale(0.85).next_to(cells[3 * t], LEFT, buff=0.15) for t in range(3)])
      hs = Tex('shift', color=CHANGE).scale(0.75).next_to(lab_s, UP, buff=0.15)
      ht = Tex('twist', color=ACCENT).scale(0.75).next_to(lab_t, LEFT, buff=0.2)
      self.play(FadeIn(lab_s), FadeIn(hs), run_time=0.12 * d)
      self.play(FadeIn(lab_t), FadeIn(ht), run_time=0.12 * d)
      self.play(LaggedStart(*[FadeIn(c) for c in cells], lag_ratio=0.08), run_time=0.25 * d)
      none = Tex('none', color=CLEAR).scale(0.65).move_to(cells[0])
      self.play(FadeIn(none), run_time=0.08 * d)
      eight = MathTex(r'9 - 1 = 8 \text{ errors per qutrit}', color=BAD).scale(0.9).move_to(DOWN * 2.6 + RIGHT * 1.55)
      self.play(Write(eight), run_time=0.15 * d)
    self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.45)


# ---------------------------------------------------------------------------------------
def combo(s, t):
  return [(s * a + t * b) % 3 for a, b in zip(D['shift'], D['twist'])]


class Sheets(NarratedScene):
  def construct(self):
    S, T = D['shift'], D['twist']
    qlabels = VGroup(*[Tex(f'Q{i + 1}', color=MUTED).scale(0.6) for i in range(5)]).arrange(DOWN, buff=0.28)
    qlabels.move_to(LEFT * 6.0 + UP * 0.2)
    colS = VGroup(*[MathTex(str(v), color=CHANGE).scale(0.85) for v in S])
    colT = VGroup(*[MathTex(str(v), color=ACCENT).scale(0.85) for v in T])
    for i, (a, b) in enumerate(zip(colS, colT)):
      a.move_to([-4.9, qlabels[i].get_y(), 0])
      b.move_to([-3.9, qlabels[i].get_y(), 0])
    hS = Tex('shift 1', color=CHANGE).scale(0.6).next_to(colS, UP, buff=0.3)
    hT = Tex('twist 1', color=ACCENT).scale(0.6).next_to(colT, UP, buff=0.3)
    who = Tex(r'qutrit 14 of a real 28-qutrit code', color=MUTED).scale(0.6).to_edge(UP, buff=0.4).align_to(qlabels, LEFT)

    with self.say('s07_finger') as d:
      self.play(FadeIn(qlabels), run_time=0.2 * d)
      self.play(FadeIn(who), run_time=0.1 * d)
      self.play(FadeIn(hS), LaggedStart(*[FadeIn(x) for x in colS], lag_ratio=0.15), run_time=0.25 * d)
      self.play(FadeIn(hT), LaggedStart(*[FadeIn(x) for x in colT], lag_ratio=0.15), run_time=0.25 * d)

    # 3 x 3 grid of the nine lists s*S + t*T, on a slanted sheet
    origin = np.array([-0.4, -1.2, 0])
    ex = np.array([2.1, 0.0, 0])
    ey = np.array([0.55, 1.3, 0])
    sheet = Polygon(origin - 0.7 * ex - 0.4 * ey, origin + 2.55 * ex - 0.4 * ey, origin + 2.55 * ex + 2.45 * ey,
                    origin - 0.7 * ex + 2.45 * ey, color=CODE, stroke_width=2, fill_color=CODE, fill_opacity=0.12)
    cellmobs = {}
    for s in range(3):
      for t in range(3):
        v = combo(s, t)
        col = CLEAR if (s, t) == (0, 0) else INK
        m = digits(v, scale=0.62, color=col).move_to(origin + s * ex + t * ey)
        cellmobs[(s, t)] = m
    sl = VGroup(*[MathTex(f's={s}', color=CHANGE).scale(0.6).move_to(origin + s * ex - 0.75 * ey) for s in range(3)])
    tl = VGroup(*[MathTex(f't={t}', color=ACCENT).scale(0.6).move_to(origin + t * ey - 0.95 * ex + 0.1 * ey) for t in range(3)])
    form = MathTex(r's \times', r'\text{shift}', r'+\, t \times', r'\text{twist}').scale(0.8).to_edge(UP, buff=0.45).shift(RIGHT * 2.6)
    form[1].set_color(CHANGE)
    form[3].set_color(ACCENT)

    with self.say('s07_sheet') as d:
      self.play(Write(form), run_time=0.12 * d)
      self.play(FadeIn(sheet), FadeIn(sl), FadeIn(tl), run_time=0.1 * d)
      self.play(LaggedStart(*[FadeIn(cellmobs[k]) for k in sorted(cellmobs)], lag_ratio=0.12), run_time=0.3 * d)
      zero_ring = SurroundingRectangle(cellmobs[(0, 0)], color=CLEAR, buff=0.08, corner_radius=0.08)
      self.play(Create(zero_ring), run_time=0.08 * d)
      z0 = cellmobs[(0, 0)].get_center()
      other = sheet.copy().set_color(ACCENT).set_fill(ACCENT, 0.08).scale(0.5, about_point=z0).rotate(2.2, about_point=z0)
      self.play(FadeIn(other), run_time=0.15 * d)
      rule = Tex(r'two sheets share only $0\,0\,0\,0\,0$', color=GOOD).scale(0.75).to_edge(DOWN, buff=0.35).shift(RIGHT * 2.0)
      self.play(FadeIn(rule), Indicate(zero_ring, color=GOOD), run_time=0.15 * d)
    self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.45)


# ---------------------------------------------------------------------------------------
class Counting(NarratedScene):
  def construct(self):
    e1 = MathTex(r'3^5', r'=', r'243').scale(1.3).move_to(UP * 1.6)
    e2 = MathTex(r'1', r'+', r'8n', r'\le', r'243').scale(1.3).move_to(UP * 1.6)
    e3 = MathTex(r'n', r'\le', r'30').scale(1.3).move_to(UP * 1.6)
    with self.say('s08_count') as d:
      self.play(Write(e1), run_time=0.2 * d)
      self.play(TransformMatchingTex(e1, e2), run_time=0.25 * d)
      self.play(Indicate(e2[0], color=CLEAR), run_time=0.1 * d)
      self.play(Indicate(e2[2], color=BAD), run_time=0.1 * d)
      self.play(TransformMatchingTex(e2, e3), run_time=0.15 * d)
      self.play(e3.animate.set_color(CHANGE), run_time=0.08 * d)

    nl = NumberLine(x_range=[25, 31, 1], length=11, include_numbers=True, font_size=48, color=MUTED).move_to(DOWN * 1.2)
    with self.say('s08_tables') as d:
      self.play(Create(nl), e3.animate.scale(0.85).move_to(UP * 2.8), run_time=0.15 * d)
      k28 = Dot(nl.n2p(28), radius=0.18, color=GOOD)
      c28 = bracket(28, 23, 3, 3, scale=0.95, color=GOOD).next_to(k28, UP, buff=0.45)
      self.play(FadeIn(k28), FadeIn(c28), run_time=0.15 * d)
      key = Tex(r'28 qutrits, 23 of message, distance 3', color=MUTED).scale(0.7).next_to(c28, UP, buff=0.3)
      self.play(FadeIn(key), run_time=0.12 * d)
      q29 = MathTex('?', color=CHANGE).scale(1.6).next_to(nl.n2p(29), UP, buff=0.45)
      q30 = MathTex('?', color=CHANGE).scale(1.6).next_to(nl.n2p(30), UP, buff=0.45)
      self.play(FadeIn(q29), run_time=0.12 * d)
      self.play(FadeIn(q30), run_time=0.1 * d)
      guess = Tex('pause and guess', color=CHANGE).scale(0.8).to_edge(DOWN, buff=0.6)
      self.play(FadeIn(guess), run_time=0.1 * d)
    self.wait(1.2)
    self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.45)


# ---------------------------------------------------------------------------------------
class Lines(NarratedScene):
  def construct(self):
    v = D['shift']
    dv = [(2 * x) % 3 for x in v]
    with self.say('s09_double') as d:
      a = digits(v, scale=1.1).move_to(UP * 1.2 + LEFT * 2.5)
      b = digits(dv, scale=1.1, color=CHANGE).move_to(DOWN * 0.2 + LEFT * 2.5)
      times2 = MathTex(r'\times 2', color=CHANGE).scale(0.9).next_to(VGroup(a, b), LEFT, buff=0.4)
      self.play(FadeIn(a), run_time=0.15 * d)
      self.play(TransformFromCopy(a, b), FadeIn(times2), run_time=0.25 * d)
      brace = Brace(VGroup(a, b), RIGHT, color=MUTED)
      pt = Dot(brace.get_tip() + RIGHT * 0.9, radius=0.18, color=CODE)
      lab = Tex('one point', color=CODE).scale(0.8).next_to(pt, RIGHT, buff=0.3)
      self.play(GrowFromCenter(brace), run_time=0.12 * d)
      self.play(FadeIn(pt, scale=2), FadeIn(lab), run_time=0.15 * d)
    with self.say('s09_count') as d:
      self.play(*[FadeOut(m) for m in [a, b, times2, brace, pt, lab]], run_time=0.05 * d)
      cnt = MathTex(r'242 \div 2 = 121', r'\text{ points}').scale(0.8).move_to([4.65, 2.7, 0])
      F = Field()
      self.play(FadeIn(F.dots, lag_ratio=0.01), Write(cnt), run_time=0.22 * d)
      # the qutrit-14 sheet: 8 nonzero lists pair into 4 points
      pts = D['example_points']
      top = VGroup(*[digits(p, scale=0.62) for p in pts])
      bot = VGroup(*[digits([(2 * x) % 3 for x in p], scale=0.62, color=CHANGE) for p in pts])
      pairs = VGroup(*[VGroup(a, b).arrange(RIGHT, buff=0.5) for a, b in zip(top, bot)]).arrange(DOWN, buff=0.32)
      pairs.move_to([4.65, -0.8, 0])
      self.play(FadeIn(pairs), run_time=0.15 * d)
      targets = F.slot_dots(0)
      merged = VGroup(*[Dot(t.get_center(), radius=0.12, color=CODE) for t in targets])
      self.play(*[ReplacementTransform(pairs[i], merged[i]) for i in range(4)], run_time=0.2 * d)
      bar0 = F.bar(0)
      self.play(Create(bar0), run_time=0.1 * d)
      lab = Tex('one qutrit = a line', color=CODE).scale(0.8).move_to([4.65, 1.6, 0])
      self.play(FadeIn(lab), run_time=0.08 * d)
      more = VGroup(*[F.bar(k) for k in range(1, 9)])
      self.play(LaggedStart(*[Create(m) for m in more], lag_ratio=0.15), run_time=0.15 * d)
      # an attempted collision: a bar sliding onto a used point flashes red
      bad = F.bar(9, color=BAD, opacity=0.8).move_to(F.slots[8][1] + RIGHT * 0.6 * SP)
      self.play(FadeIn(bad), run_time=0.05 * d)
      self.play(Flash(F.slots[8][3], color=BAD), run_time=0.06 * d)
      skew = Tex(r'lines never meet:\\ they are skew', color=GOOD).scale(0.8).move_to([4.65, 0.3, 0])
      self.play(FadeOut(bad), FadeIn(skew), run_time=0.08 * d)
    self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.45)


# ---------------------------------------------------------------------------------------
class Bridge(NarratedThreeDScene):
  def construct(self):
    self.set_camera_orientation(phi=62 * DEGREES, theta=-50 * DEGREES, zoom=0.95)
    road = Prism(dimensions=[8, 1.0, 0.12], fill_color=GREY_D, fill_opacity=1, stroke_width=0)
    stripe = Line3D(start=[-4, 0, 0.08], end=[4, 0, 0.08], color=CLEAR, thickness=0.03)
    deck = Prism(dimensions=[1.0, 7, 0.16], fill_color=CODE, fill_opacity=0.9, stroke_width=0).shift(OUT * 2.0)
    pillars = VGroup(*[Prism(dimensions=[0.25, 0.25, 2.0], fill_color=SOFT, fill_opacity=1, stroke_width=0)
                       .move_to([0, y, 1.0]) for y in (-3.2, 3.2)])
    gap = DashedLine([0, 0, 0.1], [0, 0, 1.9], color=CHANGE)
    cap = Tex('not parallel, never touching: skew', color=GOOD).scale(0.8).to_edge(DOWN, buff=0.5)
    with self.say('s10_bridge') as d:
      self.play(FadeIn(road), FadeIn(stripe), run_time=0.2 * d)
      self.play(FadeIn(deck), FadeIn(pillars), run_time=0.2 * d)
      self.begin_ambient_camera_rotation(rate=0.12)
      self.play(Create(gap), run_time=0.15 * d)
      self.add_fixed_in_frame_mobjects(cap)
      self.play(FadeIn(cap), run_time=0.15 * d)
    self.wait(0.3)
    self.stop_ambient_camera_rotation()
    self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.45)


# ---------------------------------------------------------------------------------------
class Fano(NarratedScene):
  def construct(self):
    R = 2.4
    c = np.array([0, -0.2, 0])
    A = c + R * np.array([0, 1, 0])
    B = c + R * np.array([-np.sqrt(3) / 2, -0.5, 0])
    C = c + R * np.array([np.sqrt(3) / 2, -0.5, 0])
    mAB, mBC, mCA = (A + B) / 2, (B + C) / 2, (C + A) / 2
    pts = [A, B, C, mAB, mBC, mCA, c]
    lines = [Line(A, B), Line(B, C), Line(C, A), Line(A, mBC), Line(B, mCA), Line(C, mAB),
             Circle(radius=R / 2).move_to(c)]
    lines = VGroup(*[l.set_stroke(CODE, 4) for l in lines])
    point_of = {0: [0, 1, 3], 1: [1, 2, 4], 2: [2, 0, 5], 3: [0, 4, 6], 4: [1, 5, 6], 5: [2, 3, 6], 6: [3, 4, 5]}
    dots = VGroup(*[Dot(p, radius=0.13, color=INK) for p in pts])
    title_ = Tex('7 points, 7 lines', color=MUTED).scale(0.75).to_corner(UL, buff=0.5)
    with self.say('s10_fano') as d:
      self.play(Create(lines), FadeIn(dots), run_time=0.3 * d)
      self.play(FadeIn(title_), run_time=0.1 * d)
      for i, j in [(0, 6), (3, 4), (1, 5)]:
        common = (set(point_of[i]) & set(point_of[j])).pop()
        hi = VGroup(lines[i].copy().set_stroke(CHANGE, 7), lines[j].copy().set_stroke(CHANGE, 7))
        self.play(FadeIn(hi), run_time=0.07 * d)
        self.play(Flash(dots[common], color=BAD, flash_radius=0.4), dots[common].animate.set_color(BAD), run_time=0.07 * d)
        self.play(FadeOut(hi), dots[common].animate.set_color(INK), run_time=0.04 * d)
    with self.say('s10_ten') as d:
      self.play(FadeOut(lines), FadeOut(dots), FadeOut(title_), run_time=0.1 * d)
      F = Field(rows=2, cols=5, center=(0, 0.6), spare=False, radius=0.09)
      bars = VGroup(*[F.bar(k, color=CODE if k % 2 == 0 else ACCENT, opacity=0.7) for k in range(10)])
      VGroup(F.dots, bars).scale(1.3).move_to(UP * 0.5)
      self.play(FadeIn(F.dots, lag_ratio=0.02), run_time=0.15 * d)
      four = Tex('4 questions: 40 points', color=MUTED).scale(0.8).to_edge(UP, buff=0.7)
      self.play(FadeIn(four), run_time=0.1 * d)
      self.play(LaggedStart(*[Create(b) for b in bars], lag_ratio=0.1), *[F.dots[i].animate.set_color(INK) for i in range(40)],
                run_time=0.3 * d)
      cap = VGroup(Tex('10 skew lines cover every point', color=GOOD).scale(0.8),
                   bracket(10, 6, 3, 3, scale=0.9, color=GOOD)).arrange(DOWN, buff=0.3).to_edge(DOWN, buff=0.8)
      self.play(FadeIn(cap), run_time=0.15 * d)
    self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.45)


# ---------------------------------------------------------------------------------------
class Holes(NarratedScene):
  def construct(self):
    F = Field()
    holes = list(range(116, 121))
    bars = VGroup(*[F.bar(k) for k in range(29)])
    side = 4.65

    with self.say('s11_setup') as d:
      self.play(FadeIn(F.dots), run_time=0.12 * d)
      t1 = MathTex(r'121 \text{ points}').scale(0.8).move_to([side, 2.7, 0])
      self.play(FadeIn(t1), run_time=0.08 * d)
      self.play(LaggedStart(*[Create(b) for b in bars], lag_ratio=0.03),
                *[F.dots[i].animate.set_color(CODE) for i in range(116)], run_time=0.3 * d)
      t2 = MathTex(r'29 \times 4 = 116').scale(0.8).next_to(t1, DOWN, buff=0.35)
      self.play(Write(t2), run_time=0.12 * d)
      t3 = MathTex(r'121 - 116 = 5 \text{ holes}', color=HOLE).scale(0.8).next_to(t2, DOWN, buff=0.35)
      self.play(*[F.dots[i].animate.set_color(HOLE).scale(1.8) for i in holes], Write(t3), run_time=0.15 * d)
      tag = Tex('(if 29 lines fit)', color=MUTED).scale(0.6).next_to(t3, DOWN, buff=0.3)
      self.play(FadeIn(tag), run_time=0.08 * d)

    # A schematic slice: two whole lines, one point of every other line, and the 5 holes = 40 points.
    inside = [0, 1]
    chosen = [i for k in inside for i in range(4 * k, 4 * k + 4)]
    chosen += [4 * k + (k % 4) for k in range(2, 29)] + holes
    assert len(chosen) == 40
    rings = VGroup(*[Circle(0.17, color=CHANGE, stroke_width=3).move_to(F.dots[i]) for i in chosen])
    with self.say('s11_slice') as d:
      self.play(FadeOut(tag), run_time=0.05 * d)
      self.play(LaggedStart(*[Create(r) for r in rings], lag_ratio=0.01), run_time=0.3 * d)
      s1 = Tex('a slice: 40 points', color=CHANGE).scale(0.8).next_to(t3, DOWN, buff=0.45)
      self.play(FadeIn(s1), run_time=0.1 * d)
      self.play(Indicate(VGroup(bars[0], bars[1]), color=CHANGE), run_time=0.15 * d)
      self.play(Indicate(VGroup(*[F.dots[4 * k + (k % 4)] for k in range(2, 29)]), color=CHANGE), run_time=0.15 * d)

    with self.say('s11_mod') as d:
      m1 = MathTex(r'\text{holes} = 40 - 29 - 3x').scale(0.8).next_to(s1, DOWN, buff=0.45)
      self.play(Write(m1), run_time=0.25 * d)
      m2 = MathTex(r'= 11,\ 8,\ 5,\ 2', color=CHANGE).scale(0.8).next_to(m1, DOWN, buff=0.3).align_to(m1, LEFT).shift(RIGHT * 1.0)
      self.play(Write(m2), run_time=0.25 * d)
      m3 = MathTex(r'\ge 2', color=HOLE).scale(1.0).next_to(m2, DOWN, buff=0.3)
      self.play(FadeIn(m3, scale=1.4), run_time=0.15 * d)

    with self.say('s11_tally') as d:
      self.play(*[FadeOut(m) for m in [F.dots, bars, rings, t1, t2, t3, s1, m1, m2, m3]], run_time=0.08 * d)
      need = MathTex(r'121 \times 2 = 242', r'\text{ needed}').scale(0.95).move_to(UP * 2.0 + LEFT * 1.6)
      have = MathTex(r'5 \times 40 = 200', r'\text{ available}', color=HOLE).scale(0.95).move_to(UP * 0.2 + LEFT * 1.6)
      unit = 9.0 / 242
      bneed = Rectangle(width=242 * unit, height=0.45, color=CHANGE, fill_opacity=0.5, stroke_width=2)
      bhave = Rectangle(width=200 * unit, height=0.45, color=HOLE, fill_opacity=0.5, stroke_width=2)
      bneed.next_to(need, DOWN, buff=0.25).to_edge(LEFT, buff=1.2)
      bhave.next_to(have, DOWN, buff=0.25).to_edge(LEFT, buff=1.2)
      need.align_to(bneed, LEFT)
      have.align_to(bhave, LEFT)
      self.play(Write(need), run_time=0.15 * d)
      self.play(GrowFromEdge(bneed, LEFT), run_time=0.15 * d)
      self.play(Write(have), run_time=0.15 * d)
      self.play(GrowFromEdge(bhave, LEFT), run_time=0.15 * d)
      short = DashedLine(bhave.get_right(), bhave.get_right() + RIGHT * 42 * unit, color=BAD, stroke_width=6)
      self.play(Create(short), run_time=0.1 * d)

    with self.say('s11_contra') as d:
      lt = MathTex(r'200 < 242', color=BAD).scale(1.2).move_to(DOWN * 1.6)
      self.play(Write(lt), bhave.animate.set_color(BAD), run_time=0.15 * d)
      res = MathTex(r'\text{at most } 28 \text{ lines}', color=GOOD).scale(1.0).next_to(lt, DOWN, buff=0.45)
      self.play(FadeIn(res), run_time=0.15 * d)
      credit = Tex('hole count for skew lines: Beutelspacher, 1975', color=MUTED).scale(0.6).to_edge(DOWN, buff=0.3)
      self.play(FadeIn(credit), run_time=0.1 * d)
    self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.45)


# ---------------------------------------------------------------------------------------
class Cheaters(NarratedScene):
  def construct(self):
    with self.say('s12_cheat') as d:
      e1 = Tex('error A', color=BAD).scale(0.85).move_to(LEFT * 5.3 + UP * 2.3)
      e2 = Tex('error B', color=BAD).scale(0.85).move_to(LEFT * 5.3 + UP * 0.5)
      ans = VGroup(Tex('same answers').scale(0.85)).move_to(LEFT * 1.4 + UP * 1.4)
      box = boxed(ans, color=CHANGE)
      a1 = Arrow(e1.get_right(), box.get_left(), color=BAD, buff=0.15)
      a2 = Arrow(e2.get_right(), box.get_left(), color=BAD, buff=0.15)
      self.play(FadeIn(e1), FadeIn(e2), run_time=0.08 * d)
      self.play(GrowArrow(a1), GrowArrow(a2), FadeIn(ans), Create(box), run_time=0.12 * d)
      ok = Tex(r'allowed if their difference\\ is harmless to the message', color=MUTED).scale(0.75)
      ok.move_to([-3.0, -0.8, 0])
      self.play(FadeIn(ok), run_time=0.1 * d)
      big = Square(3.4, color=CODE, stroke_width=3).move_to(RIGHT * 4.3 + UP * 0.7)
      bl = Tex('5 questions', color=CODE).scale(0.75).next_to(big, UP, buff=0.15)
      small = Square(2.1, color=CHANGE, stroke_width=3).move_to(big.get_center() + DOWN * 0.45 + RIGHT * 0.45)
      sl = Tex('4 questions', color=CHANGE).scale(0.7).move_to(small)
      self.play(Create(big), FadeIn(bl), run_time=0.12 * d)
      self.play(TransformFromCopy(big, small), FadeIn(sl), run_time=0.15 * d)
      eq = MathTex(r'2 + 10 = 12', r'\;<\; 28', color=GOOD).scale(1.1).move_to(DOWN * 2.5)
      self.play(Write(eq), run_time=0.2 * d)
    self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.45)


# ---------------------------------------------------------------------------------------
class Build(NarratedScene):
  def construct(self):
    ax = Axes(x_range=[-3, 3, 1], y_range=[-3, 3, 1], x_length=5.6, y_length=5.6,
              axis_config={'color': MUTED, 'include_ticks': False}).move_to(LEFT * 2.6)
    with self.say('s13_slopes') as d:
      self.play(Create(ax), run_time=0.15 * d)
      cols = [CODE, ACCENT, CHANGE, WARM, SOFT]
      ls = VGroup()
      for a, c in zip([-2, -0.5, 0.4, 1, 3], cols):
        x = min(3, 3 / abs(a))
        ls.add(Line(ax.c2p(-x, -a * x), ax.c2p(x, a * x), color=c, stroke_width=4))
      self.play(LaggedStart(*[Create(l) for l in ls], lag_ratio=0.2), run_time=0.35 * d)
      hole = Circle(0.14, color=CLEAR, stroke_width=4, fill_color=BACKGROUND, fill_opacity=1).move_to(ax.c2p(0, 0))
      self.play(FadeIn(hole), run_time=0.1 * d)
      eq = MathTex(r'y = a\,x').scale(1.0).move_to(RIGHT * 3.4 + UP * 1.6)
      note = Tex(r'centre = all zeros:\\ does not count', color=MUTED).scale(0.7).next_to(eq, DOWN, buff=0.4)
      self.play(Write(eq), FadeIn(note), run_time=0.2 * d)

    with self.say('s13_family') as d:
      self.play(*[FadeOut(m) for m in [ax, ls, hole, note]], eq.animate.move_to(UP * 2.6), run_time=0.1 * d)
      La = MathTex(r'L_a', r'=', r'\{\,(', r'x,\ y,', r'\ a\,(x + y\,\omega)', r')\,\}').scale(1.1).move_to(UP * 1.3)
      La[3].set_color(CODE)
      La[4].set_color(SLOPE)
      self.play(TransformMatchingShapes(eq, La[0:2]), FadeIn(La[2:]), run_time=0.2 * d)
      b1 = Brace(La[3], DOWN, color=CODE)
      b1l = Tex('2 free entries', color=CODE).scale(0.7).next_to(b1, DOWN, buff=0.12)
      b2 = Brace(La[4], DOWN, color=SLOPE)
      b2l = Tex('3 entries', color=SLOPE).scale(0.7).next_to(b2, DOWN, buff=0.12)
      self.play(GrowFromCenter(b1), FadeIn(b1l), run_time=0.12 * d)
      self.play(GrowFromCenter(b2), FadeIn(b2l), run_time=0.12 * d)
      f27 = Tex(r'$a$: one of 27 elements of a number system built from clock digits', color=MUTED).scale(0.7)
      f27.move_to(DOWN * 1.0)
      self.play(FadeIn(f27), run_time=0.15 * d)
      n27 = Tex(r'27 slopes $\Rightarrow$ 27 skew lines', color=SLOPE).scale(0.85).next_to(f27, DOWN, buff=0.5)
      self.play(FadeIn(n27), run_time=0.15 * d)

    with self.say('s13_27') as d:
      self.play(*[FadeOut(m) for m in [La, b1, b1l, b2, b2l, f27, n27]], run_time=0.08 * d)
      F = Field()
      bars = VGroup(*[F.bar(k, color=SLOPE) for k in range(27)])
      self.play(FadeIn(F.dots), FadeIn(bars), *[F.dots[i].animate.set_color(SLOPE) for i in range(108)], run_time=0.2 * d)
      extra = F.bar(27, color=CHANGE, opacity=0.8)
      lab = Tex(r'$x = y = 0$: a plane,\\ room for one more line', color=CHANGE).scale(0.7).move_to([4.65, 0.4, 0])
      self.play(FadeIn(lab), run_time=0.15 * d)
      self.play(Create(extra), *[F.dots[i].animate.set_color(CHANGE) for i in range(108, 112)], run_time=0.15 * d)
      tot = MathTex(r'27 + 1 = 28', color=GOOD).scale(1.0).move_to([4.65, -1.4, 0])
      self.play(Write(tot), run_time=0.15 * d)
    self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.45)


# ---------------------------------------------------------------------------------------
class Balance(NarratedScene):
  def construct(self):
    n = 10
    boxes = VGroup(*[Square(0.98, color=MUTED, stroke_width=3) for _ in range(n)]).arrange(RIGHT, buff=0.12)
    boxes.move_to(UP * 0.3)

    def row(vals, hot=None, color=INK):
      g = VGroup()
      for i, (b, v) in enumerate(zip(boxes, vals)):
        c = hot if hot is not None and v != 0 else color
        g.add(MathTex(str(v), color=c).scale(1.15).move_to(b))
      return g

    with self.say('s14_rule') as d:
      t = Tex('signature: 10 clock numbers per line', color=MUTED).scale(0.75).to_edge(UP, buff=0.6)
      self.play(FadeIn(t), run_time=0.12 * d)
      self.play(Create(boxes), run_time=0.15 * d)
      goal = Tex(r'total must be all zeros', color=GOOD).scale(0.8).next_to(boxes, DOWN, buff=0.6)
      self.play(FadeIn(goal), run_time=0.15 * d)
      w = MathTex(r'\text{relabel twists:}\ \ \text{signature} \times 2 \;=\; \text{weight } 2', color=CHANGE).scale(0.8)
      w.next_to(goal, DOWN, buff=0.45)
      self.play(Write(w), run_time=0.25 * d)

    plain = D['plain_running']
    cur = row([0] * n)
    counter = Tex('slope lines added: 0', color=SLOPE).scale(0.75).next_to(boxes, UP, buff=0.45)
    with self.say('s14_run') as d:
      self.play(FadeOut(goal), FadeOut(w), FadeIn(cur), FadeIn(counter), run_time=0.08 * d)
      step = 0.5 * d / 27
      for k, vals in enumerate(plain, 1):
        new = row(vals, color=GOOD if k == 27 else INK)
        c2 = Tex(f'slope lines added: {k}', color=SLOPE).scale(0.75).move_to(counter)
        self.play(Transform(cur, new), Transform(counter, c2), run_time=step)
      self.wait(0.08 * d)
      plus = Tex('+ the extra line (weight 1)', color=CHANGE).scale(0.75).next_to(boxes, DOWN, buff=0.6)
      self.play(FadeIn(plus), run_time=0.1 * d)
      self.play(Transform(cur, row(D['plain_plus_extra_final'], hot=BAD)), run_time=0.12 * d)
      self.play(Indicate(cur[7], color=BAD, scale_factor=1.5), run_time=0.1 * d)

    rew = D['reweighted_running']
    with self.say('s14_fix') as d:
      c2 = Tex('three slope lines get weight 2', color=CHANGE).scale(0.75).move_to(counter)
      self.play(Transform(counter, c2), FadeOut(plus), Transform(cur, row([0] * n)), run_time=0.1 * d)
      step = 0.25 * d / 27
      for k, vals in enumerate(rew, 1):
        self.play(Transform(cur, row(vals, hot=CHANGE if k == 27 else None)), run_time=step)
      two = Tex('slope lines leave a 2', color=CHANGE).scale(0.75).next_to(boxes, DOWN, buff=0.6)
      self.play(FadeIn(two), Indicate(cur[7], color=CHANGE, scale_factor=1.5), run_time=0.1 * d)
      add1 = MathTex(r'2 + 1 = 3 \to 0', color=GOOD).scale(0.95).next_to(two, DOWN, buff=0.35)
      self.play(Write(add1), run_time=0.12 * d)
      self.play(Transform(cur, row(D['closing_final'], color=GOOD)), run_time=0.12 * d)
      done = bracket(28, 23, 3, 3, scale=0.95, color=GOOD).next_to(add1, DOWN, buff=0.4)
      self.play(FadeIn(done), run_time=0.1 * d)
    self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.45)


# ---------------------------------------------------------------------------------------
class Answer(NarratedScene):
  def construct(self):
    with self.say('s15_theorem') as d:
      st = statement('Theorem (q $\\ge 3$, a prime or prime power)',
                     r'A code with $n$ qudits and $r$ questions that repairs any single error exists '
                     r'exactly when $r \ge 4$ and $n \le$ the largest number of skew lines that fit.',
                     width=10.5, color=CODE)
      st.move_to(UP * 0.4)
      self.play(FadeIn(st), run_time=0.3 * d)
    with self.say('s15_five') as d:
      self.play(st.animate.scale(0.88).to_edge(UP, buff=0.3), run_time=0.1 * d)
      ev = Tex(r'even $r$: equals the counting limit \quad odd $r$: $q - 1$ lower', color=MUTED).scale(0.75)
      ev.next_to(st, DOWN, buff=0.3)
      self.play(FadeIn(ev), run_time=0.15 * d)
      rows = [(3, 30, 28), (4, 68, 65), (5, 130, 126)]
      unit = 6.0 / 130
      grp = VGroup()
      for i, (q, cnt, true) in enumerate(rows):
        y = -0.75 - i * 0.85
        lab = MathTex(f'q = {q}').scale(0.75).move_to([-5.3, y, 0])
        bc = Rectangle(width=cnt * unit, height=0.32, color=MUTED, fill_opacity=0.25, stroke_width=2)
        bt = Rectangle(width=true * unit, height=0.32, color=GOOD, fill_opacity=0.6, stroke_width=0)
        bc.move_to([-4.3 + cnt * unit / 2, y, 0])
        bt.move_to([-4.3 + true * unit / 2, y, 0])
        nums = MathTex(f'{true}', r'\text{ of }', f'{cnt}').scale(0.7).next_to(bc, RIGHT, buff=0.3)
        nums[0].set_color(GOOD)
        nums[2].set_color(MUTED)
        grp.add(VGroup(lab, bc, bt, nums))
      head = MathTex(r'r = 5:\quad q^3 + 1 \ \text{ instead of } \ q^3 + q', color=INK).scale(0.8)
      head.next_to(ev, DOWN, buff=0.3)
      self.play(Write(head), run_time=0.15 * d)
      for g in grp:
        self.play(FadeIn(g[0]), FadeIn(g[1]), GrowFromEdge(g[2], LEFT), FadeIn(g[3]), run_time=0.1 * d)
      every = Tex(r'every length in between: built too', color=GOOD).scale(0.75).to_edge(DOWN, buff=0.35)
      self.play(FadeIn(every), run_time=0.1 * d)
    self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.45)


# ---------------------------------------------------------------------------------------
class Table(NarratedScene):
  def construct(self):
    head = VGroup(Tex('code', color=MUTED), Tex('tables said', color=MUTED), Tex('now', color=MUTED))
    entries = [((59, 54, 4), '2 or 3', '3'), ((61, 56, 4), '2 or 3', '3'), ((62, 57, 4), '2 or 3', '3'),
               ((65, 60, 4), '2 or 3', '3'), ((29, 24, 3), '2 or 3', '2'), ((66, 61, 4), '2 or 3', '2')]
    xs = [-3.2, 0.4, 3.2]
    y0 = 2.5
    for m, x in zip(head, xs):
      m.scale(0.85).move_to([x, y0, 0])
    sub = Tex('best possible distance', color=MUTED).scale(0.6).next_to(head[1:], UP, buff=0.15)
    sub.move_to([(xs[1] + xs[2]) / 2, y0 + 0.5, 0])
    rule = Line([-4.8, y0 - 0.35, 0], [4.4, y0 - 0.35, 0], color=MUTED, stroke_width=2)
    rows = []
    for i, ((n, k, q), was, now) in enumerate(entries):
      y = y0 - 0.85 - i * 0.66
      good = now == '3'
      col = GOOD if good else BAD
      r = VGroup(bracket(n, k, q, scale=0.9).move_to([xs[0], y, 0]),
                 Tex(was, color=MUTED).scale(0.8).move_to([xs[1], y, 0]),
                 MathTex(now, color=col).scale(1.0).move_to([xs[2], y, 0]))
      rows.append(r)
    note_new = Tex('new codes', color=GOOD).scale(0.75).move_to([5.6, (rows[0].get_y() + rows[3].get_y()) / 2, 0])
    note_no = Tex('impossible', color=BAD).scale(0.75).move_to([5.6, (rows[4].get_y() + rows[5].get_y()) / 2, 0])
    with self.say('s16_table') as d:
      self.play(FadeIn(head), FadeIn(sub), Create(rule), run_time=0.12 * d)
      for r in rows[:4]:
        self.play(FadeIn(r), run_time=0.08 * d)
      self.play(FadeIn(note_new), run_time=0.08 * d)
      self.wait(0.1 * d)
      for r in rows[4:]:
        self.play(FadeIn(r), run_time=0.08 * d)
      self.play(FadeIn(note_no), run_time=0.08 * d)
    with self.say('s16_more') as d:
      more = Tex(r'+ 6 more entries at larger distance', color=INK).scale(0.8).move_to(DOWN * 2.6)
      tot = Tex(r'12 improved, 11 now exact \quad (some rows use Thas, 1971)', color=MUTED).scale(0.7)
      tot.next_to(more, DOWN, buff=0.25)
      self.play(FadeIn(more), run_time=0.25 * d)
      self.play(FadeIn(tot), run_time=0.25 * d)
    self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.45)


# ---------------------------------------------------------------------------------------
class Status(NarratedScene):
  def construct(self):
    def item(head, body, color):
      h = Tex(r'\textbf{' + head + '}', color=color).scale(0.8)
      b = Tex(body).scale(0.68)
      g = VGroup(h, b).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
      return card(g, color=color)

    a = item('Proved', 'short written proofs: the limit and the constructions', GOOD)
    b = item('Checked by computer', '255 explicit codes pass an independent exact checker; 7 broken ones rejected', ACCENT)
    c = item('Not yet', r'no Lean proof, no peer review; stabilizer codes only; Thas (1971) cited', BAD)
    grp = VGroup(a, b, c).arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to(UP * 0.3)
    with self.say('s17_proof') as d:
      self.play(FadeIn(a), run_time=0.2 * d)
      self.play(FadeIn(b), run_time=0.25 * d)
    with self.say('s17_limits') as d:
      sat = Tex(r'a computer search alone found 28 lines but could not rule out 29', color=MUTED).scale(0.65)
      sat.to_edge(DOWN, buff=0.45)
      self.play(FadeIn(sat), run_time=0.2 * d)
      self.play(FadeIn(c), run_time=0.25 * d)
    self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.45)


# ---------------------------------------------------------------------------------------
class Recap(NarratedScene):
  def construct(self):
    pts = VGroup(
      Tex(r'1.\ Repair = every error leaves a different answer'),
      Tex(r'2.\ Quantum: each qudit is a line; lines never meet, and balance'),
      Tex(r'3.\ Counting holes gives the limit; a construction reaches it'),
    ).arrange(DOWN, aligned_edge=LEFT, buff=0.5).scale(0.85).move_to(UP * 0.1)
    pts[1].set_color(CODE)
    pts[2].set_color(GOOD)
    with self.say('s18_recap') as d:
      for p in pts:
        self.play(FadeIn(p, shift=RIGHT * 0.3), run_time=0.15 * d)
    with self.say('s18_open') as d:
      self.play(FadeOut(pts), run_time=0.1 * d)
      t = Tex(r'Open: distance 4, qutrits, 7 questions', color=CHANGE).scale(0.85).to_edge(UP, buff=0.8)
      self.play(FadeIn(t), run_time=0.15 * d)
      nl = NumberLine(x_range=[0, 30, 5], length=11, include_numbers=True, font_size=36, color=MUTED).move_to(DOWN * 0.3)
      self.play(Create(nl), run_time=0.15 * d)
      k = Dot(nl.n2p(16), radius=0.15, color=GOOD)
      kl = Tex('16 known', color=GOOD).scale(0.7).next_to(k, UP, buff=0.3)
      b = Dot(nl.n2p(29), radius=0.15, color=BAD)
      bl = Tex('29 proven limit', color=BAD).scale(0.7).next_to(b, UP, buff=0.3)
      gap = Line(nl.n2p(16), nl.n2p(29), color=CHANGE, stroke_width=10, stroke_opacity=0.6)
      self.play(FadeIn(k), FadeIn(kl), run_time=0.12 * d)
      self.play(FadeIn(b), FadeIn(bl), run_time=0.12 * d)
      q = MathTex('?', color=CHANGE).scale(1.3).next_to(gap, DOWN, buff=0.6)
      self.play(Create(gap), FadeIn(q), run_time=0.15 * d)
    self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.45)
    ec = end_card()
    self.play(FadeIn(ec), run_time=1.0)
    self.wait(3.5)
