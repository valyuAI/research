"""Explainer: tic-tac-toe where nobody wins, and HJ(p+1, 2; 2) = p+1.

Running example: the 3 by 3 board (the p = 2 case). Scaled example: p = 7, eight digits in seven
dimensions, with the counts from verification/hj8_independent_verification.json (see check_numbers.py).
"""

import itertools
import random

from manim import *
from vrvideo import *

SCENES = ['Hook', 'Lines', 'Puzzle', 'Dimensions', 'Known', 'Rule', 'Hops', 'Clock', 'EightCube', 'Lean',
          'Ending']

BLUE_FILL = '#2d7fbf'
RED_FILL = '#b8433a'
BLUE_OP = 0.95
RED_OP = 0.85
STAR = r'\bigstar'
DIM = '#5b6068'


def is_blue(p, s):
  return s == 0 or (s % p == 1 and s > 1)


def T(s, scale=0.7, color=INK):
  return Tex(s, color=color).scale(scale)


def M(s, scale=0.7, color=INK):
  return MathTex(s, color=color).scale(scale)


def word(chars, scale=0.9, star_color=SECONDARY):
  """A cell name or a pattern such as 3*02**0, with stars in yellow."""
  parts = [STAR if c == '*' else str(c) for c in chars]
  m = MathTex(*parts, arg_separator=r'\,').scale(scale)
  for i, c in enumerate(chars):
    if c == '*':
      m[i].set_color(star_color)
  return m


def tick(scale=0.9):
  return MathTex(r'\checkmark', color=OK).scale(scale)


def cross(pos, r=0.2, color=WARN, width=6):
  return VGroup(Line(pos + UL * r, pos + DR * r), Line(pos + UR * r, pos + DL * r)).set_stroke(color, width)


class Board(VGroup):
  """A k by k grid; cell (x, y) has column x (left to right) and row y (bottom to top)."""

  def __init__(self, k=3, size=1.2, stroke=2.5):
    super().__init__()
    self.k, self.size = k, size
    self.cells = {}
    for y in range(k):
      for x in range(k):
        sq = Square(side_length=size, stroke_color=MUTED, stroke_width=stroke)
        sq.set_fill(BACKGROUND, opacity=0.0)
        sq.move_to(((x - (k - 1) / 2) * RIGHT + (y - (k - 1) / 2) * UP) * size)
        self.cells[(x, y)] = sq
        self.add(sq)

  def c(self, x, y):
    return self.cells[(x, y)]

  def pos(self, x, y):
    return self.cells[(x, y)].get_center()


def fill_anim(sq, col):
  if col == 'B':
    return sq.animate.set_fill(BLUE_FILL, opacity=BLUE_OP)
  if col == 'R':
    return sq.animate.set_fill(RED_FILL, opacity=RED_OP)
  return sq.animate.set_fill(BACKGROUND, opacity=0)


def set_fill(sq, col):
  if col == 'B':
    sq.set_fill(BLUE_FILL, opacity=BLUE_OP)
  elif col == 'R':
    sq.set_fill(RED_FILL, opacity=RED_OP)
  return sq


def band(board, pts, color=SECONDARY, opacity=0.18, width=4):
  """A capsule around a row, column or diagonal of the board."""
  a, b = board.pos(*pts[0]), board.pos(*pts[-1])
  v = b - a
  length = np.linalg.norm(v)
  h = board.size * 0.7
  r = RoundedRectangle(width=length + h, height=h, corner_radius=h / 2 - 0.01, stroke_color=color,
                       stroke_width=width, fill_color=color, fill_opacity=opacity)
  r.rotate(np.arctan2(v[1], v[0])).move_to((a + b) / 2)
  r.set_z_index(2)
  return r


def pair_box(board, a, b, color=WARN):
  return SurroundingRectangle(VGroup(board.c(*a), board.c(*b)), color=color, buff=0.06, stroke_width=7,
                              corner_radius=0.1).set_z_index(2)


ROWS = [[(x, y) for x in range(3)] for y in range(3)]
COLS = [[(x, y) for y in range(3)] for x in range(3)]
DIAG = [(0, 0), (1, 1), (2, 2)]
DRAW3 = {c: ('B' if is_blue(2, sum(c)) else 'R') for c in itertools.product(range(3), repeat=2)}


def draw_board(size=0.6, sums=True, scale=None):
  """The finished p = 2 draw: blue at digit sums 0 and 3."""
  b = Board(3, size, stroke=2)
  for c, v in DRAW3.items():
    set_fill(b.c(*c), v)
  labels = VGroup()
  if sums:
    for c in DRAW3:
      labels.add(M(str(sum(c)), scale or size * 0.9).move_to(b.pos(*c)).set_z_index(3))
  return VGroup(b, labels), b


# Oblique projection for the 3 by 3 by 3 cube.
U3, V3, W3 = np.array([1.0, 0, 0]), np.array([0, 1.0, 0]), np.array([0.62, 0.42, 0])


def proj(x, y, z, origin, s):
  return origin + s * (x * U3 + y * V3 + z * W3)


def make_cube(origin, s, k=3, r=0.09):
  edges = VGroup()
  for x, y, z in itertools.product(range(k), repeat=3):
    p = proj(x, y, z, origin, s)
    for dx, dy, dz in [(1, 0, 0), (0, 1, 0), (0, 0, 1)]:
      if x + dx < k and y + dy < k and z + dz < k:
        edges.add(Line(p, proj(x + dx, y + dy, z + dz, origin, s), stroke_width=1.5, color=MUTED,
                       stroke_opacity=0.35))
  dots = {}
  layers = [VGroup() for _ in range(k)]
  for z in reversed(range(k)):
    for y in range(k):
      for x in range(k):
        d = Dot(proj(x, y, z, origin, s), radius=r * (1 - 0.1 * z), color=GREY_B)
        dots[(x, y, z)] = d
        layers[z].add(d)
  return edges, dots, layers


def all_lines(k, n):
  out = []
  for w in itertools.product(list(range(k)) + ['*'], repeat=n):
    if '*' in w:
      out.append([tuple(a if c == '*' else c for c in w) for a in range(k)])
  return out


def sum_line(lo, hi, length, p, label_scale=0.55, show_removed=True, numbers=None):
  """Number line of digit sums with blue sums marked and the removed sum 1 crossed out."""
  nl = NumberLine(x_range=[lo, hi, 1], length=length, color=MUTED, stroke_width=2, tick_size=0.05,
                  include_tip=False)
  marks, labels = VGroup(), VGroup()
  for s in range(lo, hi + 1):
    if is_blue(p, s):
      marks.add(Dot(nl.n2p(s), radius=0.085, color=PRIMARY))
      labels.add(M(str(s), label_scale, PRIMARY).next_to(nl.n2p(s), DOWN, buff=0.2))
  removed = VGroup()
  if show_removed and lo <= 1 <= hi:
    removed.add(cross(nl.n2p(1), r=0.09, width=4))
    removed.add(M('1', label_scale, WARN).next_to(nl.n2p(1), DOWN, buff=0.2))
  extra = VGroup()
  for s in numbers or []:
    extra.add(M(str(s), label_scale, MUTED).next_to(nl.n2p(s), DOWN, buff=0.2))
  return nl, marks, labels, removed, extra


def land(nl, s, p=7, r=0.07):
  """Where a hop lands: teal on a blue sum, red on the removed sum 1, yellow otherwise."""
  if is_blue(p, s):
    return Dot(nl.n2p(s), radius=r * 1.5, color=ACCENT).set_z_index(5)
  if s == 1:
    return Circle(radius=r * 2, color=WARN, stroke_width=3).move_to(nl.n2p(s)).set_z_index(5)
  return Dot(nl.n2p(s), radius=r, color=SECONDARY).set_z_index(5)


def hop(nl, a, b, color=SECONDARY, angle=-1.4, width=3.5):
  return ArcBetweenPoints(nl.n2p(a), nl.n2p(b), angle=angle, color=color, stroke_width=width)


def clock(m, radius, center, target=1, label_scale=0.62):
  unit = [np.array([np.sin(TAU * h / m), np.cos(TAU * h / m), 0]) for h in range(m)]
  pts = [center + radius * u for u in unit]
  circ = Circle(radius=radius, color=MUTED, stroke_width=2).move_to(center)
  dots = VGroup(*[Dot(pts[h], radius=0.08, color=MUTED) for h in range(m)])
  labels = VGroup(*[M(str(h), label_scale, PRIMARY if h == target else INK).move_to(center + (radius + 0.4) * unit[h])
                    for h in range(m)])
  ring = Circle(radius=0.2, color=PRIMARY, stroke_width=4).move_to(pts[target])
  return VGroup(circ, dots, labels, ring), pts


def chord(pts, a, b, color=SECONDARY):
  return Arrow(pts[a], pts[b], buff=0.12, stroke_width=4, color=color, max_tip_length_to_length_ratio=0.1,
               max_stroke_width_to_length_ratio=8)


# ---------------------------------------------------------------------------------------------------------


class Hook(NarratedScene):
  def construct(self):
    b = Board(3, 1.3).shift(DOWN * 0.15)

    def X(x, y):
      c, r = b.pos(x, y), 0.36
      return VGroup(Line(c + UL * r, c + DR * r), Line(c + UR * r, c + DL * r)).set_stroke(WARM, 7)

    def O(x, y):
      return Circle(radius=0.38, color=ACCENT, stroke_width=7).move_to(b.pos(x, y))

    moves = [X(0, 0), O(1, 1), X(1, 0), O(0, 2), X(2, 0)]
    with self.say('s01_board') as d:
      self.play(Create(b), run_time=0.15 * d)
      for m in moves:
        self.play(Create(m), run_time=0.08 * d)
      strike = Line(b.pos(0, 0) + LEFT * 0.55, b.pos(2, 0) + RIGHT * 0.55, color=WARM, stroke_width=9)
      self.play(Create(strike), run_time=0.15 * d)

    colouring = {(0, 2): 'R', (1, 2): 'R', (2, 2): 'R', (0, 1): 'B', (1, 1): 'R', (2, 1): 'B', (0, 0): 'B',
                 (1, 0): 'B', (2, 0): 'R'}
    with self.say('s01_twist') as d:
      self.play(FadeOut(VGroup(*moves, strike)), run_time=0.12 * d)
      self.wait(0.12 * d)
      self.play(LaggedStart(*[fill_anim(b.c(*c), v) for c, v in colouring.items()], lag_ratio=0.12),
                run_time=0.5 * d)

    with self.say('s01_rules') as d:
      red_hl = SurroundingRectangle(VGroup(*[b.c(x, 2) for x in range(3)]), color=WARN, buff=0.07,
                                    stroke_width=7, corner_radius=0.1)
      red_cap = caption(r'Red wins: a whole red line', 0.7)
      self.play(Create(red_hl), FadeIn(red_cap), run_time=0.18 * d)
      self.wait(0.2 * d)
      blue_hl = pair_box(b, (0, 0), (1, 0))
      blue_cap = caption(r'Blue wins: two blue neighbours on a line', 0.7)
      self.play(FadeOut(red_hl), FadeOut(red_cap), Create(blue_hl), FadeIn(blue_cap), run_time=0.2 * d)

    with self.say('s01_question') as d:
      self.play(FadeOut(blue_hl), FadeOut(blue_cap), *[fill_anim(sq, None) for sq in b.cells.values()],
                run_time=0.15 * d)
      q = T(r'Can you colour it so that nobody wins?', 0.85).to_edge(UP, buff=0.55)
      self.play(Write(q), run_time=0.25 * d)
      self.play(b.animate.scale(0.6).move_to(LEFT * 4.3 + DOWN * 0.4), run_time=0.15 * d)
      b4 = Board(4, 0.55, stroke=2).move_to(DOWN * 0.4)
      edges, dots, layers = make_cube(np.array([2.9, -1.55, 0]), 0.8)
      cube = VGroup(edges, *layers)
      labs = VGroup(M(r'3 \times 3', 0.6, MUTED).next_to(b, DOWN, buff=0.35),
                    M(r'4 \times 4', 0.6, MUTED).next_to(b4, DOWN, buff=0.35),
                    M(r'3 \times 3 \times 3', 0.6, MUTED).next_to(cube, DOWN, buff=0.35))
      labs[2].match_y(labs[0])
      labs[1].match_y(labs[0])
      self.play(FadeIn(b4, shift=LEFT * 0.3), FadeIn(cube, shift=LEFT * 0.3), FadeIn(labs), run_time=0.25 * d)


class Lines(NarratedScene):
  def construct(self):
    b = Board(3, 1.25).move_to(LEFT * 3.4 + DOWN * 0.25)
    colnums = VGroup(*[M(str(x), 0.6, MUTED).next_to(b.c(x, 0), DOWN, buff=0.2) for x in range(3)])
    rownums = VGroup(*[M(str(y), 0.6, MUTED).next_to(b.c(0, y), LEFT, buff=0.2) for y in range(3)])
    collab = T('column', 0.55, MUTED).next_to(colnums, DOWN, buff=0.15)
    rowlab = T('row', 0.55, MUTED).next_to(rownums, UP, buff=0.2)
    names = {(x, y): word([x, y], 0.75).move_to(b.pos(x, y)).set_z_index(3) for x in range(3) for y in range(3)}
    name_grp = VGroup(*names.values())
    PX = 2.8

    with self.say('s02_names') as d:
      self.play(Create(b), run_time=0.15 * d)
      self.play(FadeIn(colnums), FadeIn(collab), run_time=0.1 * d)
      self.play(FadeIn(rownums), FadeIn(rowlab), run_time=0.1 * d)
      self.play(LaggedStart(*[FadeIn(names[(x, y)]) for y in range(3) for x in range(3)], lag_ratio=0.1),
                run_time=0.22 * d)
      hl = SurroundingRectangle(b.c(0, 0), color=SECONDARY, buff=0, stroke_width=6)
      self.wait(0.03 * d)
      self.play(Create(hl), run_time=0.08 * d)
      self.wait(0.12 * d)
      self.play(hl.animate.move_to(b.pos(2, 1)), run_time=0.08 * d)

    pat = word(['*', 1], 1.4).move_to(RIGHT * PX + UP * 2.3)
    pat_lab = T('pattern', 0.6, MUTED).next_to(pat, LEFT, buff=0.5)
    with self.say('s02_pattern') as d:
      self.play(FadeOut(hl), Write(pat), FadeIn(pat_lab), run_time=0.15 * d)
      self.wait(0.05 * d)
      filled, outlines = VGroup(), VGroup()
      for a in range(3):
        w = word([a, 1], 1.0).move_to(RIGHT * (PX - 1.4 + 1.4 * a) + UP * 0.9)
        w[0].set_color(SECONDARY)
        o = SurroundingRectangle(b.c(a, 1), color=SECONDARY, buff=0, stroke_width=6)
        filled.add(w)
        outlines.add(o)
        self.play(TransformFromCopy(pat, w), Create(o), run_time=0.13 * d)
        self.wait(0.04 * d)
      row = band(b, ROWS[1])
      row_lab = T('a row', 0.65, SECONDARY).next_to(filled, DOWN, buff=0.45)
      self.play(FadeIn(row), FadeIn(row_lab), run_time=0.1 * d)

    with self.say('s02_more') as d:
      pat2 = word([1, '*'], 1.4).move_to(pat)
      col = band(b, COLS[1])
      col_lab = T('a column', 0.65, SECONDARY).move_to(row_lab)
      self.play(FadeOut(filled), FadeOut(outlines), ReplacementTransform(row, col),
                ReplacementTransform(pat, pat2), ReplacementTransform(row_lab, col_lab), run_time=0.15 * d)
      self.wait(0.08 * d)
      pat3 = word(['*', '*'], 1.4).move_to(pat)
      self.play(FadeOut(col), FadeOut(col_lab), ReplacementTransform(pat2, pat3), run_time=0.1 * d)
      filled, outlines = VGroup(), VGroup()
      for a in range(3):
        w = word([a, a], 1.0).move_to(RIGHT * (PX - 1.4 + 1.4 * a) + UP * 0.9)
        w.set_color(SECONDARY)
        o = SurroundingRectangle(b.c(a, a), color=SECONDARY, buff=0, stroke_width=6)
        filled.add(w)
        outlines.add(o)
        self.play(TransformFromCopy(pat3, w), Create(o), run_time=0.1 * d)
      diag = band(b, DIAG)
      diag_lab = T('the diagonal', 0.65, SECONDARY).move_to(row_lab)
      self.play(FadeIn(diag), FadeIn(diag_lab), run_time=0.1 * d)
      self.wait(0.05 * d)
      same = T('every star gets the same digit', 0.6, MUTED).next_to(diag_lab, DOWN, buff=0.35)
      self.play(Indicate(pat3, color=SECONDARY, scale_factor=1.15), FadeIn(same), run_time=0.15 * d)

    with self.say('s02_anti') as d:
      self.play(FadeOut(VGroup(filled, outlines, diag, diag_lab, same, pat3, pat_lab)), run_time=0.08 * d)
      anti = DashedLine(b.pos(0, 2) + UL * 0.45, b.pos(2, 0) + DR * 0.45, color=GREY_A, stroke_width=5,
                        dash_length=0.15)
      ws = VGroup(*[word([a, 2 - a], 1.0).move_to(RIGHT * (PX - 1.4 + 1.4 * a) + UP * 1.9) for a in range(3)])
      for w in ws:
        w[0].set_color(ACCENT)
        w[1].set_color(WARM)
      self.play(Create(anti), LaggedStart(*[FadeIn(w) for w in ws], lag_ratio=0.3), run_time=0.22 * d)
      ud = VGroup(T(r'first digit goes up', 0.6, ACCENT), T(r'second digit goes down', 0.6, WARM))
      ud.arrange(DOWN, buff=0.2).next_to(ws, DOWN, buff=0.45)
      self.play(FadeIn(ud[0]), run_time=0.08 * d)
      self.play(FadeIn(ud[1]), run_time=0.08 * d)
      no = cross(b.pos(2, 0) + DR * 0.62, r=0.22)
      not_line = T('not a line', 0.65, WARN).next_to(ud, DOWN, buff=0.4)
      self.play(anti.animate.set_color(WARN).set_opacity(0.6), Create(no), FadeIn(not_line), run_time=0.12 * d)
      self.wait(0.1 * d)
      seven = VGroup()
      for L in ROWS + COLS + [DIAG]:
        mb = Board(3, 0.26, stroke=1.5)
        mb.add(band(mb, L, opacity=0.35, width=2.5))
        seven.add(mb)
      seven.arrange(RIGHT, buff=0.16).move_to(RIGHT * PX + UP * 0.6)
      seven_lab = T('7 lines', 0.85, SECONDARY).next_to(seven, DOWN, buff=0.45)
      self.play(FadeOut(VGroup(anti, no, ws, ud, not_line)), run_time=0.08 * d)
      self.play(LaggedStart(*[FadeIn(m, shift=UP * 0.15) for m in seven], lag_ratio=0.15), FadeIn(seven_lab),
                run_time=0.18 * d)

    with self.say('s02_neighbours') as d:
      pat4 = word(['*', 1], 1.4).move_to(RIGHT * PX + UP * 2.3)
      row = band(b, ROWS[1], opacity=0.06, width=2.5)
      self.play(FadeOut(seven), FadeOut(seven_lab), FadeIn(pat4), FadeIn(row), run_time=0.1 * d)
      top = UP * 0.26

      def arc(a, c, color, angle=-1.7, dashed=False):
        mob = ArcBetweenPoints(b.pos(a, 1) + top, b.pos(c, 1) + top, angle=angle, color=color,
                               stroke_width=5).set_z_index(4)
        return DashedVMobject(mob, num_dashes=14) if dashed else mob

      a1, a2 = arc(0, 1, OK), arc(1, 2, OK)
      n1 = T(r'$0\,1$ and $1\,1$: neighbours', 0.62, OK).move_to(RIGHT * PX + UP * 0.9)
      n2 = T(r'$1\,1$ and $2\,1$: neighbours', 0.62, OK).next_to(n1, DOWN, buff=0.3)
      self.play(Create(a1), FadeIn(n1), run_time=0.12 * d)
      self.wait(0.1 * d)
      self.play(Create(a2), FadeIn(n2), run_time=0.12 * d)
      self.wait(0.15 * d)
      bot = DOWN * 0.3
      far = DashedVMobject(ArcBetweenPoints(b.pos(0, 1) + bot, b.pos(2, 1) + bot, angle=1.0, color=WARN,
                                            stroke_width=5), num_dashes=18).set_z_index(4)
      n3 = T(r'$0\,1$ and $2\,1$: not neighbours', 0.62, WARN).next_to(n2, DOWN, buff=0.3)
      self.play(Create(far), FadeIn(n3), run_time=0.15 * d)


class Puzzle(NarratedScene):
  def construct(self):
    b = Board(3, 1.25).move_to(LEFT * 3.2 + DOWN * 0.35)
    names = {c: word(list(c), 0.75).move_to(b.pos(*c)).set_z_index(3) for c in DRAW3}
    sums = {c: M(str(sum(c)), 0.85).move_to(b.pos(*c)).set_z_index(3) for c in DRAW3}
    goals = VGroup(T(r'every line: at least one blue', 0.62), T(r'no line: two blue neighbours', 0.62))
    goals.arrange(DOWN, aligned_edge=LEFT, buff=0.25)
    goal_card = card(goals, color=MUTED, buff=0.3).move_to(RIGHT * 3.3 + UP * 2.2)
    PX = 3.3

    with self.say('s03_puzzle', pause=1.6) as d:
      self.play(FadeIn(b), FadeIn(VGroup(*names.values())), run_time=0.2 * d)
      self.play(FadeIn(goal_card[0]), FadeIn(goals[0]), run_time=0.15 * d)
      self.play(FadeIn(goals[1]), run_time=0.15 * d)

    with self.say('s03_sums') as d:
      demo = M(r'2 + 1 = 3', 0.9).move_to(RIGHT * PX + UP * 0.2)
      self.play(Indicate(names[(2, 1)], color=SECONDARY), FadeIn(demo), run_time=0.18 * d)
      self.play(LaggedStart(*[ReplacementTransform(names[c], sums[c]) for c in DRAW3], lag_ratio=0.08),
                run_time=0.25 * d)
      self.wait(0.05 * d)
      steps = VGroup()
      for x in range(2):
        mid = (b.pos(x, 0) + b.pos(x + 1, 0)) / 2
        steps.add(M('+1', 0.65, SECONDARY).move_to(np.array([mid[0], b.get_bottom()[1] - 0.4, 0])))
      for y in range(2):
        mid = (b.pos(0, y) + b.pos(0, y + 1)) / 2
        steps.add(M('+1', 0.65, SECONDARY).move_to(np.array([b.get_left()[0] - 0.5, mid[1], 0])))
      self.play(FadeOut(demo), LaggedStart(*[FadeIn(s) for s in steps], lag_ratio=0.25), run_time=0.3 * d)

    with self.say('s03_checker') as d:
      checker = {c: ('B' if sum(c) % 2 else 'R') for c in DRAW3}
      self.play(FadeOut(steps), run_time=0.05 * d)
      self.play(LaggedStart(*[fill_anim(b.c(*c), v) for c, v in checker.items()], lag_ratio=0.08),
                run_time=0.25 * d)
      odd = T(r'odd, odd: never one apart', 0.62, MUTED).move_to(RIGHT * PX + UP * 0.2)
      self.play(FadeIn(odd), run_time=0.1 * d)
      self.wait(0.2 * d)
      row_ticks = VGroup(*[tick(0.75).next_to(b.c(2, y), RIGHT, buff=0.25) for y in range(3)])
      col_ticks = VGroup(*[tick(0.75).next_to(b.c(x, 2), UP, buff=0.2) for x in range(3)])
      self.play(LaggedStart(*[FadeIn(t) for t in [*row_ticks, *col_ticks]], lag_ratio=0.15), run_time=0.3 * d)

    with self.say('s03_fail') as d:
      diag = band(b, DIAG)
      self.play(FadeOut(odd), Create(diag), run_time=0.15 * d)
      self.play(LaggedStart(*[Indicate(sums[c], color=SECONDARY, scale_factor=1.4) for c in DIAG],
                            lag_ratio=0.4), run_time=0.25 * d)
      end = b.pos(2, 2) + UR * 0.95
      x_mark = cross(end, r=0.22)
      all_red = T('all even: all red', 0.65, WARN).move_to(RIGHT * PX + UP * 0.2)
      self.play(diag.animate.set_stroke(WARN).set_fill(WARN, opacity=0.12), Create(x_mark), FadeIn(all_red),
                run_time=0.2 * d)

    with self.say('s04_ponder', pause=1.6) as d:
      q = M('?', 1.2, WARM).next_to(b.c(0, 0), LEFT, buff=0.35)
      self.play(FadeIn(q), run_time=0.2 * d)

    with self.say('s04_add') as d:
      flash = SurroundingRectangle(b.c(0, 0), color=SECONDARY, buff=0, stroke_width=8)
      self.play(FadeOut(q), Create(flash), run_time=0.08 * d)
      self.play(fill_anim(b.c(0, 0), 'B'), run_time=0.1 * d)
      dtick = tick(0.85).move_to(x_mark)
      saved = T('diagonal saved', 0.65, OK).move_to(all_red)
      self.play(FadeOut(flash), FadeOut(diag), ReplacementTransform(x_mark, dtick),
                ReplacementTransform(all_red, saved), run_time=0.12 * d)
      self.wait(0.1 * d)
      p1 = pair_box(b, (0, 0), (1, 0))
      self.play(Create(p1), run_time=0.12 * d)
      self.wait(0.1 * d)
      p2 = pair_box(b, (0, 0), (0, 1))
      self.play(Create(p2), run_time=0.12 * d)
      blue_wins = T('blue neighbours: blue wins', 0.65, WARN).move_to(saved)
      self.play(ReplacementTransform(saved, blue_wins), run_time=0.1 * d)

    with self.say('s04_remove', pause=1.2) as d:
      fl = VGroup(SurroundingRectangle(b.c(1, 0), color=SECONDARY, buff=0, stroke_width=8),
                  SurroundingRectangle(b.c(0, 1), color=SECONDARY, buff=0, stroke_width=8))
      self.play(Create(fl), run_time=0.12 * d)
      self.play(fill_anim(b.c(1, 0), 'R'), fill_anim(b.c(0, 1), 'R'), FadeOut(p1), FadeOut(p2),
                FadeOut(blue_wins), run_time=0.2 * d)
      self.play(FadeOut(fl), FadeOut(row_ticks), FadeOut(col_ticks), FadeOut(dtick), run_time=0.15 * d)

    with self.say('s04_check') as d:
      new_ticks = {}

      def check(L, key, pos, rt):
        bd = band(b, L)
        tk = tick(0.75).move_to(pos)
        new_ticks[key] = tk
        self.play(FadeIn(bd), run_time=rt * 0.45)
        self.play(FadeIn(tk), FadeOut(bd), run_time=rt * 0.55)

      rpos = lambda y: b.c(2, y).get_right() + RIGHT * 0.45
      cpos = lambda x: b.c(x, 2).get_top() + UP * 0.4
      check(ROWS[0], 'r0', rpos(0), 0.12 * d)
      check(COLS[0], 'c0', cpos(0), 0.12 * d)
      self.wait(0.03 * d)
      check(ROWS[1], 'r1', rpos(1), 0.13 * d)
      check(COLS[1], 'c1', cpos(1), 0.13 * d)
      self.wait(0.03 * d)
      check(ROWS[2], 'r2', rpos(2), 0.07 * d)
      check(COLS[2], 'c2', cpos(2), 0.07 * d)
      check(DIAG, 'd', b.pos(2, 2) + UR * 0.95, 0.07 * d)
      draw = T(r'A draw!', 1.3, ACCENT).move_to(RIGHT * PX + DOWN * 0.3)
      self.wait(0.04 * d)
      self.play(Write(draw), run_time=0.12 * d)

    with self.say('s04_note') as d:
      link = DashedLine(b.pos(1, 2), b.pos(2, 1), color=GREY_A, stroke_width=4, dash_length=0.1)
      no_common = T(r'$1\,2$ and $2\,1$: no common line', 0.62, MUTED).move_to(RIGHT * PX + DOWN * 1.5)
      self.play(Create(link), FadeIn(no_common), run_time=0.15 * d)
      self.wait(0.25 * d)
      row = band(b, ROWS[1], color=WARM)
      ring = Circle(radius=0.5, color=WARM, stroke_width=6).move_to(b.pos(2, 1))
      rescued = T(r'middle row: rescued by its last cell', 0.62, WARM).move_to(no_common)
      self.play(FadeOut(link), FadeIn(row), Create(ring), ReplacementTransform(no_common, rescued),
                run_time=0.2 * d)


class Dimensions(NarratedScene):
  def construct(self):
    origin = np.array([-5.3, -1.9, 0])
    s = 1.15
    edges, dots, layers = make_cube(origin, s)
    PX = 3.4

    with self.say('s05_cube') as d:
      self.play(LaggedStart(*[FadeIn(dd) for dd in layers[0]], lag_ratio=0.05), run_time=0.15 * d)
      self.play(FadeIn(edges), FadeIn(layers[1], shift=DL * 0.3), FadeIn(layers[2], shift=DL * 0.5),
                run_time=0.2 * d)
      eg = word([2, 0, 1], 1.0).set_color(SECONDARY).move_to(RIGHT * PX + UP * 2.4)
      eg_dot = dots[(2, 0, 1)]
      ring = Circle(radius=0.2, color=SECONDARY, stroke_width=4).move_to(eg_dot)
      self.play(FadeIn(eg), Create(ring), run_time=0.1 * d)
      lines_shown = VGroup()
      for pat, pts in [(['*', 1, 2], [(a, 1, 2) for a in range(3)]), (['*', '*', '*'], [(a, a, a) for a in range(3)])]:
        w = word(pat, 1.0).move_to(RIGHT * PX + UP * (1.3 if pat[1] == 1 else 0.4))
        ln = Line(dots[pts[0]].get_center(), dots[pts[-1]].get_center(), color=SECONDARY, stroke_width=9,
                  stroke_opacity=0.7)
        lines_shown.add(w, ln)
        self.play(FadeIn(w), Create(ln), run_time=0.12 * d)
        self.wait(0.03 * d)
      n37 = T('37 lines', 0.85, SECONDARY).move_to(RIGHT * PX + DOWN * 0.8)
      self.play(FadeIn(n37), run_time=0.1 * d)

    with self.say('s05_nodraw') as d:
      self.play(FadeOut(VGroup(eg, ring, lines_shown, n37)), run_time=0.08 * d)
      head = T(r'$3 \times 3 \times 3$: no draw', 0.8).move_to(RIGHT * PX + UP * 2.2)
      self.play(FadeIn(head), run_time=0.08 * d)
      L3 = all_lines(3, 3)
      cells = list(dots)
      shown = None
      for i, seed in enumerate([3, 11, 29]):
        rng = random.Random(seed)
        col = {c: rng.choice('RB') for c in cells}
        red = [L for L in L3 if all(col[c] == 'R' for c in L)]
        pairs = [(L[a], L[a + 1]) for L in L3 for a in range(2) if col[L[a]] == 'B' and col[L[a + 1]] == 'B']
        if (i % 2 == 0 and red) or not pairs:
          pts = [red[0][0], red[0][-1]]
          what = 'red line'
        else:
          pts = list(pairs[0])
          what = 'blue neighbours'
        anims = [dots[c].animate.set_color(BLUE_FILL if v == 'B' else RED_FILL) for c, v in col.items()]
        out = [FadeOut(shown)] if shown is not None else []
        self.play(*anims, *out, run_time=0.08 * d)
        win = Line(dots[pts[0]].get_center(), dots[pts[1]].get_center(), color=WARN, stroke_width=12,
                   stroke_opacity=0.85)
        lab = T(what, 0.65, WARN).move_to(RIGHT * PX + UP * (1.0 - 0.7 * i))
        shown = VGroup(win)
        self.play(Create(win), FadeIn(lab), run_time=0.1 * d)
        self.wait(0.05 * d)
      every = T(r'checked: every colouring', 0.6, MUTED).move_to(RIGHT * PX + DOWN * 1.5)
      self.play(FadeIn(every), run_time=0.1 * d)
      self.wait(0.05 * d)

    with self.say('s05_general') as d:
      self.play(FadeOut(Group(*self.mobjects)), run_time=0.1 * d)
      digits = [3, 0, 2, r'\cdots', 1]
      boxes = VGroup()
      for dg in digits:
        sq = Square(0.9, color=MUTED, stroke_width=2.5)
        sq.add(M(str(dg), 0.9).move_to(sq))
        boxes.add(sq)
      boxes.arrange(RIGHT, buff=0.15).move_to(UP * 0.9)
      brace = Brace(boxes, DOWN, color=SECONDARY)
      blab = T(r'$n$ digits $=$ $n$ dimensions', 0.65, SECONDARY).next_to(brace, DOWN, buff=0.2)
      top = T(r'each digit: $0, 1, \dots, k-1$', 0.65).next_to(boxes, UP, buff=0.45)
      self.play(LaggedStart(*[FadeIn(bx) for bx in boxes], lag_ratio=0.15), FadeIn(top), run_time=0.25 * d)
      self.wait(0.15 * d)
      self.play(GrowFromCenter(brace), FadeIn(blab), run_time=0.15 * d)
      self.wait(0.05 * d)
      qn = T(r'smallest $n$ where a draw is impossible?', 0.8).move_to(DOWN * 2.2)
      self.play(Write(qn), run_time=0.2 * d)

    with self.say('s05_name') as d:
      hj = MathTex(r'\mathrm{HJ}(', 'k', ',', '2', ';', '2', ')').scale(1.7).move_to(UP * 1.2)
      self.play(FadeOut(VGroup(boxes, brace, blab, top)), qn.animate.to_edge(UP, buff=0.5).scale(0.85),
                run_time=0.1 * d)
      self.play(Write(hj), run_time=0.15 * d)
      labs = VGroup(T(r'red: a whole line of $k$', 0.6, RED_C), T(r'blue: two neighbours', 0.6, PRIMARY),
                    T(r'two colours', 0.6, MUTED))
      targets = [hj[1], hj[3], hj[5]]
      xs = [-3.4, 0.4, 3.6]
      arrows = VGroup()
      for lab, tgt, x in zip(labs, targets, xs):
        lab.move_to(np.array([x, -0.6, 0]))
        arrows.add(Arrow(lab.get_top(), tgt.get_bottom(), buff=0.12, stroke_width=3, color=MUTED,
                         max_tip_length_to_length_ratio=0.12))
      for i in range(3):
        self.play(FadeIn(labs[i]), GrowArrow(arrows[i]), run_time=0.1 * d)
        self.wait(0.05 * d)
      hj3 = MathTex(r'\mathrm{HJ}(', '3', ',', '2', ';', '2', ')', '=', '3').scale(1.4).move_to(DOWN * 2.3)
      hj3[1].set_color(SECONDARY)
      hj3[8].set_color(ACCENT)
      self.play(TransformMatchingTex(hj.copy(), hj3), run_time=0.2 * d)


class Known(NarratedScene):
  def construct(self):
    with self.say('s06_history') as d:
      head = T(r'Hales and Jewett, 1963', 0.95).to_edge(UP, buff=0.55)
      sub = T(r'classic version: both colours need a whole line', 0.65, MUTED).next_to(head, DOWN, buff=0.35)
      res = T(r'enough dimensions $\Rightarrow$ no draw', 0.85).move_to(DOWN * 0.3)
      self.play(FadeIn(head), run_time=0.15 * d)
      self.play(FadeIn(sub), run_time=0.15 * d)
      self.wait(0.2 * d)
      self.play(Write(res), run_time=0.2 * d)

    with self.say('s06_cfr') as d:
      head2 = T(r'Conlon, Farnsworth and Robertson, 2026', 0.85).to_edge(UP, buff=0.55)
      sub2 = T(r'the lopsided version', 0.65, MUTED).next_to(head2, DOWN, buff=0.3)
      self.play(FadeOut(VGroup(head, sub, res)), run_time=0.1 * d)
      self.play(FadeIn(head2), FadeIn(sub2), run_time=0.15 * d)
      self.wait(0.25 * d)
      ub = MathTex(r'\mathrm{HJ}(k,2;2) \le k').scale(1.05).move_to(UP * 1.35)
      self.play(Write(ub), run_time=0.15 * d)
      ub_lab = T('upper bound', 0.6, SECONDARY).next_to(ub, RIGHT, buff=0.5)
      self.wait(0.07 * d)
      self.play(FadeIn(ub_lab), run_time=0.1 * d)

    ks = list(range(2, 9))
    colw, x0 = 1.25, -3.7
    kx = lambda k: x0 + (k - 2) * colw
    row_y = [0.25, -0.55]
    hdr = VGroup(M('k', 0.8, MUTED).move_to(np.array([x0 - 1.7, row_y[0], 0])),
                 T('answer', 0.65, MUTED).move_to(np.array([x0 - 1.7, row_y[1], 0])))
    knums = VGroup(*[M(str(k), 0.8).move_to(np.array([kx(k), row_y[0], 0])) for k in ks])
    rule = Line(np.array([x0 - 2.5, -0.15, 0]), np.array([kx(8) + 0.9, -0.15, 0]), color=MUTED, stroke_width=1.5)
    ans = {k: M(str(k), 0.8, ACCENT).move_to(np.array([kx(k), row_y[1], 0])) for k in ks[:-1]}
    with self.say('s06_prime') as d:
      self.play(FadeIn(hdr), FadeIn(knums), Create(rule), run_time=0.1 * d)
      self.play(LaggedStart(*[FadeIn(ans[k], scale=1.3) for k in (2, 3, 5, 7)], lag_ratio=0.3), run_time=0.18 * d)
      guess = T(r'guess: always exactly $k$', 0.62, MUTED).move_to(DOWN * 1.6)
      self.play(FadeIn(guess), run_time=0.1 * d)
      self.wait(0.1 * d)
      self.play(LaggedStart(*[FadeIn(ans[k], scale=1.3) for k in (4, 6)], lag_ratio=0.3), run_time=0.15 * d)
      self.wait(0.07 * d)
      eight = M(r'7 \text{ or } 8\,?', 0.75, SECONDARY).move_to(np.array([kx(8), row_y[1], 0]))
      self.play(FadeIn(eight), Indicate(knums[-1], color=SECONDARY), run_time=0.15 * d)

    with self.say('s07_result') as d:
      eight2 = M('8', 0.8, ACCENT).move_to(eight)
      self.play(ReplacementTransform(eight, eight2), Flash(eight.get_center(), color=ACCENT, line_length=0.3),
                run_time=0.2 * d)
      self.wait(0.12 * d)
      thm = MathTex(r'\mathrm{HJ}(', 'p', '+1', ',2;2)', '=', 'p', '+1').scale(1.15).move_to(DOWN * 1.75)
      thm_box = SurroundingRectangle(thm, color=ACCENT, buff=0.25, corner_radius=0.1)
      every = T(r'for every prime $p$', 0.62, ACCENT).next_to(thm_box, DOWN, buff=0.25)
      self.play(FadeOut(guess), run_time=0.05 * d)
      self.play(Write(thm), Create(thm_box), run_time=0.25 * d)
      self.play(FadeIn(every), run_time=0.1 * d)

    with self.say('s07_instances') as d:
      thm_grp = VGroup(thm, thm_box, every)
      self.play(FadeOut(VGroup(head2, sub2, ub, ub_lab, hdr, knums, rule, *ans.values(), eight2)),
                thm_grp.animate.move_to(UP * 2.4), run_time=0.12 * d)
      a7 = MathTex(r'\mathrm{HJ}(', '7', '+1', ',2;2)', '=', '7', '+1').scale(0.95).move_to(LEFT * 3.2 + UP * 0.6)
      a7b = MathTex(r'\mathrm{HJ}(', '8', ',2;2)', '=', '8').scale(0.95).move_to(a7)
      a11 = MathTex(r'\mathrm{HJ}(', '12', ',2;2)', '=', '12').scale(0.95).move_to(RIGHT * 3.2 + UP * 0.6)
      self.play(TransformMatchingTex(thm.copy(), a7), run_time=0.1 * d)
      self.play(TransformMatchingTex(a7, a7b), run_time=0.08 * d)
      self.play(FadeIn(a11, shift=UP * 0.2), run_time=0.08 * d)
      l1 = T(r'dimension $p+1$: always a winner (known)', 0.65, MUTED).move_to(DOWN * 0.7)
      l2 = T(r'dimension $p$: we need a draw', 0.7, SECONDARY).next_to(l1, DOWN, buff=0.3)
      self.play(FadeIn(l1), run_time=0.1 * d)
      self.wait(0.05 * d)
      self.play(FadeIn(l2), run_time=0.1 * d)
      self.wait(0.07 * d)
      grp, _ = draw_board(0.42, sums=False)
      grp.next_to(l2, DOWN, buff=0.35)
      plab = M('p = 2', 0.65, SECONDARY).next_to(grp, RIGHT, buff=0.4)
      self.play(FadeIn(grp), FadeIn(plab), run_time=0.12 * d)


class Rule(NarratedScene):
  def construct(self):
    nl = NumberLine(x_range=[0, 22, 1], length=12.0, color=MUTED, stroke_width=2, tick_size=0.05,
                    include_tip=False).move_to(DOWN * 0.6)
    marks = VGroup(*[Dot(nl.n2p(s), radius=0.09, color=PRIMARY) for s in (8, 15, 22)])
    one_more = VGroup(*[M(f'{m}+1', 0.6, PRIMARY).next_to(nl.n2p(m + 1), UP, buff=0.3) for m in (0, 7, 14, 21)])
    nums = VGroup(*[M(str(s), 0.6, PRIMARY).next_to(nl.n2p(s), DOWN, buff=0.25) for s in (1, 8, 15, 22)])
    one_dot = Dot(nl.n2p(1), radius=0.09, color=PRIMARY)
    with self.say('s08_rule') as d:
      ex = T(r'example: $p = 7$', 0.65, MUTED).to_corner(UL, buff=0.6)
      self.play(Create(nl), FadeIn(ex), run_time=0.12 * d)
      step1 = T(r'add up the digits of a cell', 0.75).to_edge(UP, buff=0.6).shift(RIGHT * 1.2)
      self.play(FadeIn(step1), run_time=0.1 * d)
      self.wait(0.05 * d)
      step2 = T(r'blue: one more than a multiple of $p$', 0.75).move_to(step1)
      self.play(ReplacementTransform(step1, step2), run_time=0.08 * d)
      self.play(LaggedStart(*[FadeIn(VGroup(dt, om, nm)) for dt, om, nm in zip([one_dot, *marks], one_more, nums)],
                            lag_ratio=0.3), run_time=0.2 * d)
      self.wait(0.03 * d)
      zero = Dot(nl.n2p(0), radius=0.09, color=PRIMARY)
      zlab = M('0', 0.6, PRIMARY).next_to(nl.n2p(0), DOWN, buff=0.25)
      step3 = T(r'repair: add the zero cell, remove sum $1$', 0.75).move_to(step1)
      self.play(ReplacementTransform(step2, step3), run_time=0.08 * d)
      self.play(FadeIn(zero, scale=2), FadeIn(zlab), Flash(nl.n2p(0), color=SECONDARY), run_time=0.12 * d)
      rm = cross(nl.n2p(1), r=0.13, width=5)
      self.play(FadeOut(one_dot), Create(rm), nums[0].animate.set_color(WARN), one_more[0].animate.set_opacity(0.3),
                run_time=0.12 * d)

    with self.say('s08_examples') as d:
      self.play(FadeOut(Group(*self.mobjects)), run_time=0.07 * d)
      grp, b3 = draw_board(0.62, sums=True, scale=0.6)
      grp.move_to(LEFT * 5.0 + DOWN * 0.2)
      lab2 = T(r'$p = 2$', 0.7, SECONDARY).next_to(grp, UP, buff=0.35)
      s2 = T(r'blue sums $0, 3$', 0.6).next_to(grp, DOWN, buff=0.35)
      self.play(FadeIn(grp), FadeIn(lab2), FadeIn(s2), run_time=0.15 * d)
      self.wait(0.18 * d)
      layers = VGroup()
      for z in range(4):
        bz = Board(4, 0.48, stroke=1.5)
        for x, y in itertools.product(range(4), repeat=2):
          set_fill(bz.c(x, y), 'B' if is_blue(3, x + y + z) else 'R')
        lz = T(f'layer {z}', 0.55, MUTED).next_to(bz, DOWN, buff=0.25)
        layers.add(VGroup(bz, lz))
      layers.arrange(RIGHT, buff=0.38).move_to(RIGHT * 1.75 + DOWN * 0.35)
      lab3 = T(r'$p = 3$: a $4 \times 4 \times 4$ cube, as four layers', 0.7, SECONDARY).next_to(layers, UP, buff=0.45)
      self.play(FadeIn(lab3), LaggedStart(*[FadeIn(l, shift=UP * 0.2) for l in layers], lag_ratio=0.2),
                run_time=0.25 * d)
      s3 = T(r'blue sums $0, 4, 7$: \;19 of 64 cells', 0.65).next_to(layers, DOWN, buff=0.4)
      self.wait(0.05 * d)
      self.play(FadeIn(s3), run_time=0.12 * d)


class Hops(NarratedMovingCameraScene):
  def construct(self):
    frame = self.camera.frame
    frame.save_state()
    grp, b3 = draw_board(0.85, sums=True, scale=0.7)
    grp.move_to(LEFT * 4.4 + UP * 0.2)
    sums3 = grp[1]
    with self.say('s09_hops') as d:
      self.play(FadeIn(grp), run_time=0.12 * d)
      self.wait(0.2 * d)
      small1 = NumberLine(x_range=[0, 4, 1], length=5.0, color=MUTED, include_numbers=False, tick_size=0.06)
      small1.move_to(RIGHT * 2.2 + UP * 1.2)
      small2 = small1.copy().move_to(RIGHT * 2.2 + DOWN * 1.0)
      row = band(b3, ROWS[1])
      self.play(FadeIn(row), Create(small1), run_time=0.1 * d)
      vals1 = VGroup(*[M(str(v), 0.7).next_to(small1.n2p(v), DOWN, buff=0.25) for v in (1, 2, 3)])
      self.play(LaggedStart(*[TransformFromCopy(sums3[i], vals1[j]) for j, i in enumerate([1, 4, 7])], lag_ratio=0.2),
                run_time=0.12 * d)
      arcs1 = VGroup(hop(small1, 1, 2), hop(small1, 2, 3))
      self.play(LaggedStart(*[Create(a) for a in arcs1], lag_ratio=0.5), run_time=0.1 * d)
      diag = band(b3, DIAG)
      self.play(ReplacementTransform(row, diag), Create(small2), run_time=0.1 * d)
      vals2 = VGroup(*[M(str(v), 0.7).next_to(small2.n2p(v), DOWN, buff=0.25) for v in (0, 2, 4)])
      self.play(LaggedStart(*[TransformFromCopy(sums3[i], vals2[j]) for j, i in enumerate([0, 4, 8])], lag_ratio=0.2),
                run_time=0.1 * d)
      arcs2 = VGroup(hop(small2, 0, 2, angle=-1.2), hop(small2, 2, 4, angle=-1.2))
      self.play(LaggedStart(*[Create(a) for a in arcs2], lag_ratio=0.5), run_time=0.08 * d)
      eq = T('equal steps', 0.7, SECONDARY).move_to(RIGHT * 2.2 + DOWN * 2.6)
      self.play(FadeIn(eq), run_time=0.06 * d)

    pat = word([3, '*', 0, 2, '*', '*', 0], 1.25).move_to(UP * 2.75)
    star_idx, fixed_idx = [1, 4, 5], [0, 2, 3, 6]
    with self.say('s09_formula') as d:
      self.play(FadeOut(Group(*self.mobjects)), run_time=0.07 * d)
      self.play(FadeIn(pat), run_time=0.1 * d)
      star_marks = VGroup(*[Triangle(color=SECONDARY, fill_opacity=1).scale(0.07).rotate(PI).next_to(pat[i], UP, buff=0.12)
                            for i in star_idx])
      d_lab = MathTex('d', r'\text{ stars}').scale(0.7).set_color(SECONDARY).next_to(pat, LEFT, buff=0.6)
      fixed_ul = VGroup(*[Line(LEFT * 0.14, RIGHT * 0.14, color=INK, stroke_width=3).next_to(pat[i], DOWN, buff=0.1)
                          for i in fixed_idx])
      s_lab = MathTex(r'\text{fixed digits add to }', 'S').scale(0.7).next_to(pat, RIGHT, buff=0.6)
      self.play(FadeIn(star_marks), FadeIn(d_lab), run_time=0.1 * d)
      self.play(FadeIn(fixed_ul), FadeIn(s_lab), run_time=0.12 * d)
      self.wait(0.03 * d)
      formula = MathTex(r'\text{sum}', '=', 'S', '+', 'd', r'\times', 'a').scale(1.1).move_to(UP * 1.25)
      formula[4].set_color(SECONDARY)
      self.play(Write(formula), run_time=0.15 * d)
      self.wait(0.05 * d)
      seq = MathTex('S', ',', r'\;S+d', ',', r'\;S+2d', ',', r'\;S+3d', ',', r'\;\dots').scale(0.95).move_to(UP * 0.1)
      self.play(LaggedStart(*[FadeIn(seq[i]) for i in range(len(seq))], lag_ratio=0.15), run_time=0.2 * d)
      hops_txt = T(r'equal hops of $d$', 0.65, SECONDARY).next_to(seq, DOWN, buff=0.3)
      self.play(FadeIn(hops_txt), run_time=0.08 * d)

    nl, marks, labels, removed, _ = sum_line(0, 49, 12.4, 7)
    nl_grp = VGroup(nl, marks, labels, removed).move_to(DOWN * 2.3)
    with self.say('s09_example') as d:
      d_lab2 = MathTex('d', '=', '3').scale(0.7).set_color(SECONDARY).move_to(d_lab)
      s_lab2 = MathTex('S', '=', '3+0+2+0', '=', '5').scale(0.7).move_to(s_lab).align_to(s_lab, LEFT)
      formula2 = MathTex(r'\text{sum}', '=', '5', '+', '3', r'\times', 'a').scale(1.1).move_to(formula)
      formula2[4].set_color(SECONDARY)
      self.play(TransformMatchingTex(d_lab, d_lab2), TransformMatchingTex(s_lab, s_lab2), run_time=0.13 * d)
      self.play(TransformMatchingTex(formula, formula2), run_time=0.12 * d)
      sums = [5 + 3 * a for a in range(8)]
      seq2 = MathTex(*[str(v) + (',' if i < 7 else '') for i, v in enumerate(sums)], arg_separator=r'\;').scale(0.95)
      seq2.move_to(seq)
      seq2[1].set_color(PRIMARY)
      self.play(FadeOut(hops_txt), ReplacementTransform(seq, seq2), FadeIn(nl_grp), run_time=0.15 * d)
      self.wait(0.05 * d)
      land_ = VGroup(land(nl, 5))
      self.play(FadeIn(land_[0]), run_time=0.04 * d)
      arcs = VGroup()
      for a in range(7):
        arc = hop(nl, sums[a], sums[a + 1], angle=-1.6)
        dt = land(nl, sums[a + 1])
        arcs.add(arc)
        land_.add(dt)
        self.play(Create(arc), FadeIn(dt), run_time=0.055 * d)
        if a == 0:
          self.play(Flash(nl.n2p(8), color=ACCENT, line_length=0.25), run_time=0.06 * d)

    with self.say('s09_jobs') as d:
      self.play(FadeOut(VGroup(pat, star_marks, d_lab2, fixed_ul, s_lab2, formula2, seq2)), run_time=0.1 * d)
      jobs = VGroup(T(r'1.\; land on blue at least once', 0.75), T(r'2.\; never on blue twice in a row', 0.75))
      jobs.arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to(UP * 1.6)
      self.play(FadeIn(jobs[0], shift=UP * 0.2), run_time=0.15 * d)
      self.wait(0.15 * d)
      self.play(FadeIn(jobs[1], shift=UP * 0.2), run_time=0.15 * d)

    with self.say('s10_gap') as d:
      self.play(FadeOut(arcs), FadeOut(land_), jobs[0].animate.set_opacity(0.35),
                jobs[1].animate.set_color(SECONDARY), run_time=0.1 * d)
      dlp = MathTex('d', '<', 'p').scale(0.9).next_to(jobs, RIGHT, buff=1.0)
      self.play(FadeIn(dlp), run_time=0.08 * d)
      self.wait(0.06 * d)
      braces = VGroup()
      for a, c in [(8, 15), (15, 22), (22, 29)]:
        br = BraceBetweenPoints(nl.n2p(a), nl.n2p(c), direction=UP, color=PRIMARY, buff=0.45)
        braces.add(VGroup(br, M('7', 0.6, PRIMARY).next_to(br, UP, buff=0.1)))
      self.play(LaggedStart(*[FadeIn(bb) for bb in braces], lag_ratio=0.3), run_time=0.2 * d)
      self.wait(0.05 * d)
      h = hop(nl, 8, 11, color=SECONDARY, angle=-2.0, width=5)
      hd = M('d', 0.6, SECONDARY).next_to(h, LEFT, buff=0.08).shift(UP * 0.1)
      h_dot = Dot(nl.n2p(11), radius=0.07, color=MUTED)
      self.play(FadeOut(braces[1:]), Create(h), FadeIn(hd), FadeIn(h_dot), run_time=0.15 * d)
      notm = T(r'$d = 1, \dots, 6$: never a multiple of 7', 0.65).move_to(UP * 0.2)
      self.play(FadeIn(notm), run_time=0.1 * d)
      self.wait(0.07 * d)
      tk2 = tick(0.8).next_to(jobs[1], LEFT, buff=0.25)
      self.play(FadeIn(tk2), run_time=0.08 * d)

    with self.say('s10_zero') as d:
      self.play(FadeOut(VGroup(braces[0], h, hd, h_dot, notm, dlp)), run_time=0.06 * d)
      z = 0.32
      y0 = nl.n2p(0)[1]
      at = lambda v, dy: np.array([nl.n2p(v)[0], y0 + dy, 0])
      self.play(frame.animate.scale(z).move_to(at(4, 0.3)), run_time=0.13 * d)
      zero_lab = M(r'\text{zero cell}', 0.6 * z, PRIMARY).move_to(at(0, 0.32))
      self.play(FadeIn(zero_lab), Flash(nl.n2p(0), color=PRIMARY, line_length=0.12, flash_radius=0.15),
                run_time=0.1 * d)
      h1 = hop(nl, 0, 1, angle=-3.0, width=3)
      t1 = M(r'd = 1:\ \text{removed}', 0.6 * z, WARN).move_to(at(1.3, 0.5))
      self.play(Create(h1), FadeIn(t1), run_time=0.13 * d)
      self.wait(0.12 * d)
      h3 = hop(nl, 0, 3, angle=-1.6, width=3)
      d3 = Dot(nl.n2p(3), radius=0.04, color=MUTED)
      t3 = M(r'd = 3:\ \text{remainder } 3', 0.6 * z, INK).move_to(at(5.3, 0.62))
      self.play(Create(h3), FadeIn(d3), FadeIn(t3), run_time=0.13 * d)
      self.wait(0.1 * d)
      safe = M(r'\checkmark\ \text{safe}', 0.75 * z, OK).move_to(at(10.0, 0.3))
      self.play(FadeIn(safe), run_time=0.08 * d)

    with self.say('s10_full') as d:
      self.play(Restore(frame), FadeOut(VGroup(zero_lab, h1, t1, h3, d3, t3, safe)), run_time=0.12 * d)
      full = word(['*'] * 7, 1.0).move_to(LEFT * 1.2 + UP * 0.4)
      dp = MathTex('d', '=', 'p', '=', '7').scale(0.8).next_to(full, RIGHT, buff=0.6)
      dp[0].set_color(SECONDARY)
      self.play(FadeIn(full), FadeIn(dp), run_time=0.1 * d)
      dots7 = VGroup(land(nl, 0))
      arcs7 = VGroup()
      mult = VGroup()
      self.add(dots7)
      for m in range(7):
        a, c = 7 * m, 7 * (m + 1)
        arc = hop(nl, a, c, angle=-1.2)
        dt = land(nl, c)
        lb = M(str(c), 0.55, MUTED).next_to(nl.n2p(c), UP, buff=0.22)
        arcs7.add(arc)
        dots7.add(dt)
        mult.add(lb)
        self.play(Create(arc), FadeIn(dt), FadeIn(lb), run_time=0.045 * d)
      only0 = T(r'only $0$ is blue', 0.7, PRIMARY).move_to(DOWN * 0.6 + LEFT * 3.5)
      self.play(Flash(nl.n2p(0), color=ACCENT, line_length=0.25), FadeIn(only0), run_time=0.12 * d)
      self.wait(0.05 * d)
      mini, mb = draw_board(0.42, sums=True, scale=0.42)
      mini.move_to(RIGHT * 5.2 + UP * 2.1)
      mband = band(mb, DIAG)
      mlab = T(r'our diagonal: $0, 2, 4$', 0.55, SECONDARY).next_to(mini, DOWN, buff=0.25)
      self.play(FadeIn(mini), FadeIn(mband), FadeIn(mlab), run_time=0.15 * d)


class Clock(NarratedScene):
  def construct(self):
    c7, p7 = clock(7, 1.85, np.array([-3.3, 0.25, 0]))
    with self.say('s11_clock') as d:
      head = T(r'job 1: land on blue at least once', 0.7, SECONDARY).to_edge(UP, buff=0.45)
      self.play(FadeIn(head), run_time=0.08 * d)
      self.play(Create(c7[0]), FadeIn(c7[1]), FadeIn(c7[2]), run_time=0.15 * d)
      self.play(Create(c7[3]), run_time=0.07 * d)
      rem = T(r'hour $=$ remainder after dividing by $7$', 0.6, MUTED).next_to(c7, DOWN, buff=0.3)
      self.play(FadeIn(rem), run_time=0.07 * d)
      hours = [(5 + 3 * a) % 7 for a in range(7)]
      seq = MathTex(*[str(h) for h in hours], arg_separator=r'\;\to\;').scale(0.8)
      seq.move_to(RIGHT * 3.4 + UP * 1.0)
      seq_lab = T(r'start at $5$, hops of $3$', 0.62, MUTED).next_to(seq, UP, buff=0.35)
      lit = VGroup(Dot(p7[5], radius=0.12, color=SECONDARY))
      self.play(FadeIn(seq_lab), FadeIn(seq[0]), FadeIn(lit[0]), run_time=0.07 * d)
      chords = VGroup()
      for a in range(6):
        ch = chord(p7, hours[a], hours[a + 1])
        dt = Dot(p7[hours[a + 1]], radius=0.12, color=SECONDARY)
        chords.add(ch)
        lit.add(dt)
        self.play(GrowArrow(ch), FadeIn(dt), FadeIn(seq[a + 1]), run_time=0.065 * d)
        if hours[a + 1] == 1:
          s8 = T(r'sum $8$: blue', 0.6, PRIMARY).next_to(seq, DOWN, buff=0.35)
          self.play(Flash(p7[1], color=ACCENT, line_length=0.2), FadeIn(s8), run_time=0.05 * d)
    with self.say('s11_prime') as d:
      prime7 = T(r'$7$ is prime: any hop from $1$ to $6$', 0.62, ACCENT).next_to(c7, DOWN, buff=0.3)
      self.play(FadeOut(VGroup(seq, seq_lab, s8)), ReplacementTransform(rem, prime7), run_time=0.12 * d)
      self.wait(0.12 * d)
      c6, p6 = clock(6, 1.85, np.array([3.4, 0.25, 0]))
      self.play(Create(c6[0]), FadeIn(c6[1]), FadeIn(c6[2]), Create(c6[3]), run_time=0.12 * d)
      lit6 = VGroup(Dot(p6[0], radius=0.12, color=SECONDARY))
      self.play(FadeIn(lit6[0]), run_time=0.04 * d)
      for a, c in [(0, 2), (2, 4), (4, 0)]:
        self.play(GrowArrow(chord(p6, a, c)), FadeIn(Dot(p6[c], radius=0.12, color=SECONDARY)), run_time=0.07 * d)
      miss = cross(p6[1], r=0.18)
      c6lab = T(r'$6$ hours, hops of $2$: never reaches $1$', 0.62, WARN).next_to(c6, DOWN, buff=0.3)
      self.play(Create(miss), c6[3].animate.set_color(WARN), FadeIn(c6lab), run_time=0.12 * d)
      self.wait(0.1 * d)
      self.play(Indicate(prime7, color=ACCENT, scale_factor=1.08), run_time=0.12 * d)

    nl, marks, labels, removed, extra = sum_line(0, 16, 12.0, 7, label_scale=0.65)
    nl_grp = VGroup(nl, marks, labels, removed).move_to(DOWN * 1.2)
    with self.say('s11_snag') as d:
      self.play(FadeOut(Group(*[m for m in self.mobjects if m is not head])), run_time=0.08 * d)
      self.play(FadeIn(nl_grp), run_time=0.12 * d)
      rings = VGroup(*[Circle(radius=0.2, color=SECONDARY, stroke_width=4).move_to(nl.n2p(s)) for s in (1, 8, 15)])
      r1 = T(r'remainder $1$', 0.65, SECONDARY).move_to(UP * 1.4)
      self.play(LaggedStart(*[Create(r) for r in rings], lag_ratio=0.3), FadeIn(r1), run_time=0.18 * d)
      self.wait(0.05 * d)
      usually = T(r'usually blue', 0.65, PRIMARY).next_to(r1, DOWN, buff=0.3)
      self.play(FadeIn(usually), Indicate(marks[1:], color=ACCENT), run_time=0.12 * d)
      self.wait(0.05 * d)
      snag = T(r'snag: the sum is exactly $1$', 0.65, WARN).next_to(usually, DOWN, buff=0.3)
      self.play(rings[0].animate.set_color(WARN), Indicate(removed, color=WARN, scale_factor=1.5), FadeIn(snag),
                run_time=0.15 * d)
      self.wait(0.05 * d)
      two = T(r'only two ways', 0.7).next_to(snag, DOWN, buff=0.3)
      self.play(FadeIn(two), run_time=0.1 * d)

    with self.say('s11_case1') as d:
      self.play(FadeOut(VGroup(rings, r1, usually, snag, two)), run_time=0.07 * d)
      f0 = MathTex('S', '+', 'd', r'\times', '0', '=', '1').scale(1.0).move_to(UP * 1.9 + LEFT * 2.6)
      f0[2].set_color(SECONDARY)
      cap1 = T(r'case 1: the first cell, so $S = 1$', 0.65).next_to(f0, UP, buff=0.35)
      self.play(FadeIn(cap1), Write(f0), run_time=0.15 * d)
      sums = list(range(1, 9))
      first = Circle(radius=0.2, color=WARN, stroke_width=4).move_to(nl.n2p(1))
      self.play(Create(first), run_time=0.06 * d)
      arcs = VGroup(*[hop(nl, sums[a], sums[a + 1], angle=-1.6) for a in range(7)])
      dots = VGroup(*[land(nl, s) for s in sums[1:]])
      self.play(LaggedStart(*[AnimationGroup(Create(a), FadeIn(dt)) for a, dt in zip(arcs, dots)], lag_ratio=0.6),
                run_time=0.17 * d)
      f1 = MathTex('1', '+', 'd', r'\times', 'p').scale(1.0).move_to(f0).align_to(f0, LEFT)
      f1[2].set_color(SECONDARY)
      f1[4].set_color(SECONDARY)
      last = T(r'last cell: every star is $p$', 0.6, MUTED).next_to(nl.n2p(8), UP, buff=0.75)
      self.play(TransformMatchingTex(f0, f1), FadeIn(last), run_time=0.13 * d)
      blue_note = T(r'remainder $1$, bigger than $1$: blue', 0.62, PRIMARY).next_to(f1, RIGHT, buff=0.5)
      self.play(Flash(nl.n2p(8), color=ACCENT, line_length=0.25), FadeIn(blue_note), run_time=0.12 * d)
      self.wait(0.04 * d)
      mini = VGroup()
      for i, c in enumerate([(0, 1), (1, 1), (2, 1)]):
        sq = Square(0.62, color=MUTED, stroke_width=2)
        set_fill(sq, DRAW3[c])
        sq.add(word(list(c), 0.55).move_to(sq).set_z_index(3))
        mini.add(sq)
      mini.arrange(RIGHT, buff=0).move_to(RIGHT * 4.3 + UP * 0.35)
      mlab = T(r'$p=2$: \; $1 + 1 \times 2 = 3$', 0.6, WARM).next_to(mini, UP, buff=0.25)
      ring = Circle(radius=0.36, color=WARM, stroke_width=5).move_to(mini[2])
      self.play(FadeIn(mini), FadeIn(mlab), Create(ring), run_time=0.13 * d)

    with self.say('s11_case2') as d:
      self.play(FadeOut(VGroup(cap1, f1, blue_note, first, arcs, dots, last, mini, mlab, ring)), run_time=0.07 * d)
      f2 = MathTex('S', '+', 'd', r'\times', 'a', '=', '1').scale(1.0).move_to(UP * 1.9 + LEFT * 2.6)
      f2[2].set_color(SECONDARY)
      cap2 = T(r'case 2: a later cell, $a \ge 1$', 0.65).next_to(f2, UP, buff=0.35)
      self.play(FadeIn(cap2), Write(f2), run_time=0.12 * d)
      s0 = MathTex(r'\Rightarrow', 'S', '=', '0').scale(1.0).next_to(f2, RIGHT, buff=0.4)
      self.play(FadeIn(s0), run_time=0.1 * d)
      arcs = VGroup(*[hop(nl, a, a + 1, angle=-1.6) for a in range(7)])
      dots = VGroup(*[land(nl, s) for s in range(0, 8)])
      self.play(FadeIn(dots[0]), LaggedStart(*[Create(a) for a in arcs], lag_ratio=0.4), FadeIn(dots[1:]),
                run_time=0.15 * d)
      zc = T(r'starts at the zero cell: blue', 0.62, PRIMARY).next_to(nl.n2p(0), UP, buff=0.9).shift(RIGHT * 1.4)
      self.play(Flash(nl.n2p(0), color=ACCENT, line_length=0.25), FadeIn(zc), run_time=0.12 * d)
      self.wait(0.1 * d)
      done = T(r'every line has a blue cell', 0.75, OK)
      tk = tick(0.9)
      dgrp = VGroup(tk, done).arrange(RIGHT, buff=0.3).move_to(DOWN * 3.1)
      self.play(FadeIn(dgrp), run_time=0.12 * d)

    with self.say('s11_done') as d:
      self.play(FadeOut(Group(*self.mobjects)), run_time=0.08 * d)
      l1 = VGroup(tick(0.8), T(r'dimension $p$: nobody wins', 0.75)).arrange(RIGHT, buff=0.3)
      l1.move_to(UP * 2.3)
      self.play(FadeIn(l1), run_time=0.1 * d)
      self.wait(0.05 * d)
      pad = MathTex(r'2\,1', r'\;\longrightarrow\;', r'2\,1', r'\,0\,0\,0\,0\,0').scale(0.95).move_to(UP * 1.0)
      pad[3].set_color(MUTED)
      padlab = T(r'smaller boards: pad with zeros', 0.62, MUTED).next_to(pad, DOWN, buff=0.3)
      self.play(FadeIn(pad[0]), run_time=0.06 * d)
      self.play(FadeIn(pad[1]), TransformFromCopy(pad[0], pad[2]), FadeIn(pad[3]), FadeIn(padlab), run_time=0.15 * d)
      self.wait(0.08 * d)
      ineq = MathTex('p+1', r'\le', r'\mathrm{HJ}(p+1,2;2)', r'\le', 'p+1').scale(1.05).move_to(DOWN * 1.1)
      left = T(r'draws up to dimension $p$', 0.55, ACCENT).next_to(ineq[0:2], DOWN, buff=0.35).shift(LEFT * 0.6)
      right = T(r'upper bound', 0.55, SECONDARY).next_to(ineq[3:], DOWN, buff=0.35)
      self.play(Write(ineq), FadeIn(left), FadeIn(right), run_time=0.17 * d)
      self.wait(0.05 * d)
      eq = MathTex(r'\mathrm{HJ}(p+1,2;2)', '=', 'p+1').scale(1.2).move_to(DOWN * 2.6)
      box = SurroundingRectangle(eq, color=ACCENT, buff=0.22, corner_radius=0.1)
      self.play(TransformMatchingTex(ineq.copy(), eq), Create(box), run_time=0.17 * d)


class EightCube(NarratedScene):
  def construct(self):
    with self.say('s12_size') as d:
      head = MathTex(r'p = 7, \qquad k = 8').scale(1.0).to_edge(UP, buff=0.55)
      self.play(Write(head), run_time=0.15 * d)
      self.wait(0.1 * d)
      cellw = word([3, 1, 0, 2, 1, 1, 0], 1.1).move_to(UP * 1.4 + LEFT * 3.0)
      br = Brace(cellw, DOWN, color=SECONDARY)
      brl = T(r'7 digits, each $0$ to $7$', 0.62, SECONDARY).next_to(br, DOWN, buff=0.15)
      self.play(FadeIn(cellw), GrowFromCenter(br), FadeIn(brl), run_time=0.15 * d)
      self.wait(0.05 * d)
      count = MathTex(r'8^7 = 2{,}097{,}152', r'\text{ cells}').scale(0.95).move_to(DOWN * 1.2 + LEFT * 3.0)
      self.play(Write(count), run_time=0.15 * d)
      b8 = Board(8, 0.3, stroke=1.2).move_to(RIGHT * 2.9 + DOWN * 0.1)
      times = MathTex(r'\times\; 32{,}768').scale(0.95).next_to(b8, RIGHT, buff=0.4)
      blab = T(r'boards of $8 \times 8$', 0.6, MUTED).next_to(b8, DOWN, buff=0.3).shift(RIGHT * 0.6)
      self.play(FadeIn(b8), FadeIn(times), FadeIn(blab), run_time=0.15 * d)

    hist = [1, 7, 28, 84, 210, 462, 924, 1716, 2996, 4956, 7812, 11788, 17094, 23898, 32292, 42252, 53613,
            66059, 79128, 92232, 104692, 115788, 124824, 131208, 134512, 134512, 131208, 124824, 115788,
            104692, 92232, 79128, 66059, 53613, 42252, 32292, 23898, 17094, 11788, 7812, 4956, 2996, 1716,
            924, 462, 210, 84, 28, 7, 1]
    assert sum(hist) == 8 ** 7
    blue_sums = [s for s in range(50) if is_blue(7, s)]
    assert sum(hist[s] for s in blue_sums) == 299587
    base_y, max_h, step, x_start = -2.4, 3.7, 0.25, -6.125
    bars = VGroup()
    for s, n in enumerate(hist):
      h = max(0.02, max_h * n / max(hist))
      r = Rectangle(width=0.19, height=h, stroke_width=0, fill_color=DIM, fill_opacity=1)
      r.move_to(np.array([x_start + step * s, base_y + h / 2, 0]))
      bars.add(r)
    axis = Line(np.array([x_start - 0.2, base_y, 0]), np.array([x_start + step * 49 + 0.2, base_y, 0]),
                color=MUTED, stroke_width=2)
    with self.say('s12_hist') as d:
      self.play(FadeOut(Group(*self.mobjects)), run_time=0.06 * d)
      xl = T('digit sum', 0.55, MUTED).next_to(axis, DOWN, buff=0.5).align_to(axis, RIGHT)
      l49 = M('49', 0.6, MUTED).next_to(axis.get_end(), DOWN, buff=0.15).set_x(bars[49].get_x())
      title_ = T(r'how many cells have each digit sum', 0.7, MUTED).to_edge(UP, buff=0.45)
      self.play(Create(axis), FadeIn(title_), FadeIn(xl), FadeIn(l49), run_time=0.08 * d)
      self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.03), run_time=0.18 * d)
      counts = VGroup()
      sum_labels = VGroup()
      for s in blue_sums:
        sum_labels.add(M(str(s), 0.6, PRIMARY).next_to(axis.get_start(), DOWN, buff=0.15).set_x(bars[s].get_x()))
        lab = M(f'{hist[s]:,}'.replace(',', '{,}'), 0.55, PRIMARY)
        lab.move_to(np.array([bars[s].get_x(), base_y + max_h + 0.45, 0]))
        tie = DashedLine(lab.get_bottom() + DOWN * 0.08, bars[s].get_top() + UP * 0.05, color=PRIMARY,
                         stroke_width=1.5, dash_length=0.06, stroke_opacity=0.6)
        counts.add(VGroup(lab, tie))
      self.play(LaggedStart(*[AnimationGroup(bars[s].animate.set_fill(BLUE_FILL), FadeIn(sum_labels[i]))
                              for i, s in enumerate(blue_sums)], lag_ratio=0.35), run_time=0.4 * d)
      self.play(LaggedStart(*[FadeIn(c) for c in counts], lag_ratio=0.15), run_time=0.12 * d)
      total = T(r'blue cells: $1 + 2{,}996 + \dots + 924 = 299{,}587$', 0.75, PRIMARY).to_edge(UP, buff=0.45)
      self.play(FadeOut(title_), FadeIn(total), run_time=0.1 * d)

    with self.say('s12_check') as d:
      self.play(FadeOut(Group(*self.mobjects)), run_time=0.06 * d)
      prog = T(r'a separate program, every line', 0.65, MUTED).to_edge(UP, buff=0.6)
      rows = VGroup()
      lab1 = T('lines checked', 0.75)
      num1 = DecimalNumber(0, num_decimal_places=0, group_with_commas=True).scale(0.95)
      lab2 = T('red lines', 0.75, RED_C)
      num2 = MathTex('0').scale(0.95).set_color(OK)
      lab3 = T('blue neighbour pairs', 0.75, PRIMARY)
      num3 = MathTex('0').scale(0.95).set_color(OK)
      for lab, num, y in [(lab1, num1, 1.3), (lab2, num2, 0.2), (lab3, num3, -0.9)]:
        lab.move_to(np.array([-1.0, y, 0]), aligned_edge=RIGHT)
        num.move_to(np.array([1.0, y, 0]), aligned_edge=LEFT)
      self.play(FadeIn(prog), FadeIn(lab1), FadeIn(num1), run_time=0.08 * d)
      self.play(ChangeDecimalToValue(num1, 2685817), run_time=0.35 * d, rate_func=smooth)
      self.play(FadeIn(lab2), FadeIn(num2), run_time=0.1 * d)
      self.wait(0.04 * d)
      self.play(FadeIn(lab3), FadeIn(num3), run_time=0.1 * d)
      draw = T(r'a draw in 7 dimensions', 0.85, ACCENT).move_to(DOWN * 2.4)
      self.play(FadeIn(draw), run_time=0.1 * d)

    with self.say('s12_meaning') as d:
      self.play(FadeOut(Group(*self.mobjects)), run_time=0.06 * d)
      left = VGroup(T('computer check', 0.75, MUTED), T(r'one board: $p = 7$', 0.65)).arrange(DOWN, buff=0.25)
      right = VGroup(T('proof', 0.75, ACCENT), T(r'every prime $p$', 0.65)).arrange(DOWN, buff=0.25)
      left.move_to(LEFT * 3.3 + UP * 1.5)
      right.move_to(RIGHT * 3.3 + UP * 1.5)
      self.play(FadeIn(left), run_time=0.12 * d)
      self.wait(0.1 * d)
      self.play(FadeIn(right), run_time=0.12 * d)
      self.wait(0.1 * d)
      res = MathTex(r'\mathrm{HJ}(8,2;2) = 8').scale(1.5).move_to(DOWN * 1.2)
      box = SurroundingRectangle(res, color=ACCENT, buff=0.3, corner_radius=0.12)
      self.play(Write(res), Create(box), run_time=0.25 * d)


class Lean(NarratedScene):
  def construct(self):
    code = VGroup(
      Tex(r'\frenchspacing\texttt{theorem HJ\_prime\_successor \{p : }$\mathbb{N}$\texttt{\} (hp : p.Prime) :}'),
      Tex(r'\frenchspacing\texttt{HJ (p + 1) = p + 1}'),
      Tex(r'\frenchspacing\texttt{theorem HJ\_eight : HJ 8 = 8}'),
    ).scale(0.6).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
    code[1].shift(RIGHT * 0.6)
    code_card = card(code, color=MUTED, buff=0.35).move_to(UP * 2.3)
    src = T(r'formal/ValyuResearch/HalesJewett.lean', 0.55, MUTED).next_to(code_card, DOWN, buff=0.2)
    with self.say('s13_lean') as d:
      self.play(FadeIn(code_card), run_time=0.15 * d)
      self.play(FadeIn(src), run_time=0.08 * d)
      steps = VGroup(*[RoundedRectangle(width=3.2, height=0.32, corner_radius=0.08, stroke_color=MUTED,
                                        stroke_width=1.5, fill_color=MUTED, fill_opacity=0.12) for _ in range(6)])
      steps.arrange(DOWN, buff=0.12).move_to(DOWN * 1.15)
      slab = T(r'each step checked against the rules of logic', 0.6, MUTED).next_to(steps, DOWN, buff=0.3)
      self.play(FadeIn(steps), FadeIn(slab), run_time=0.1 * d)
      ticks_grp = VGroup()
      for st in steps:
        tk = tick(0.55).next_to(st, RIGHT, buff=0.15)
        ticks_grp.add(tk)
        self.play(st.animate.set_stroke(OK, opacity=1).set_fill(OK, opacity=0.15), FadeIn(tk), run_time=0.07 * d)

    with self.say('s13_checked') as d:
      self.play(FadeOut(VGroup(steps, slab, ticks_grp)), run_time=0.07 * d)
      items = [r'the colouring works, for every prime $p$', r'the upper bound, re-proved',
               r'$\mathrm{HJ}(p+1,2;2) = p+1$, \;including $8$ and $12$']
      lines = VGroup(*[VGroup(tick(0.7), T(s, 0.65)).arrange(RIGHT, buff=0.3) for s in items])
      lines.arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to(DOWN * 0.9)
      for i, ln in enumerate(lines):
        self.play(FadeIn(ln, shift=UP * 0.15), run_time=0.1 * d)
        self.wait([0.12, 0.12, 0.2][i] * d)
      nosorry = T(r'no step skipped or assumed', 0.62, MUTED).next_to(lines, DOWN, buff=0.4)
      self.play(FadeIn(nosorry), run_time=0.08 * d)

    with self.say('s13_limits') as d:
      self.play(FadeOut(VGroup(lines, nosorry)), run_time=0.06 * d)
      q1 = VGroup(M('?', 0.9, WARM), T(r'do the definitions match the question?', 0.65)).arrange(RIGHT, buff=0.35)
      a1 = T(r'a separate review compared them with the paper', 0.58, MUTED)
      q2 = VGroup(M('?', 0.9, WARM), T(r'is the result new?', 0.65)).arrange(RIGHT, buff=0.35)
      a2 = T(r'a search found nothing earlier; not yet peer reviewed', 0.58, MUTED)
      grp = VGroup(q1, a1, q2, a2).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to(DOWN * 1.0)
      a1.shift(RIGHT * 0.6)
      a2.shift(RIGHT * 0.6)
      q2.shift(DOWN * 0.25)
      a2.shift(DOWN * 0.25)
      self.play(FadeIn(q1), run_time=0.1 * d)
      self.wait(0.12 * d)
      self.play(FadeIn(a1), run_time=0.1 * d)
      self.wait(0.1 * d)
      self.play(FadeIn(q2), run_time=0.1 * d)
      self.wait(0.12 * d)
      self.play(FadeIn(a2), run_time=0.1 * d)


class Ending(NarratedScene):
  def construct(self):
    with self.say('s14_recap') as d:
      head = T(r'Recap', 0.95).to_edge(UP, buff=0.6)
      pts = VGroup(
        T(r'1.\; Blue must hit every line, but never twice in a row.', 0.72),
        T(r'2.\; Digit sums, repaired at $0$ and $1$, give a draw in dimension $p$.', 0.72),
        T(r'3.\; $\mathrm{HJ}(p+1,2;2) = p+1$ for every prime $p$, \;so $\mathrm{HJ}(8,2;2) = 8$.', 0.72),
      ).arrange(DOWN, aligned_edge=LEFT, buff=0.55).move_to(DOWN * 0.2)
      self.play(FadeIn(head), run_time=0.05 * d)
      self.play(FadeIn(pts[0], shift=UP * 0.15), run_time=0.08 * d)
      self.wait(0.17 * d)
      self.play(FadeIn(pts[1], shift=UP * 0.15), run_time=0.08 * d)
      self.wait(0.3 * d)
      self.play(FadeIn(pts[2], shift=UP * 0.15), run_time=0.08 * d)

    with self.say('s14_open') as d:
      self.play(FadeOut(VGroup(head, pts)), run_time=0.06 * d)
      head2 = T(r"What we still don't know", 0.9).to_edge(UP, buff=0.6)
      self.play(FadeIn(head2), run_time=0.06 * d)
      b9 = MathTex(r'8 \le \mathrm{HJ}(9,2;2) \le 9').scale(0.9).move_to(LEFT * 3.2 + UP * 1.3)
      b10 = MathTex(r'8 \le \mathrm{HJ}(10,2;2) \le 10').scale(0.9).move_to(RIGHT * 3.2 + UP * 1.3)
      self.play(FadeIn(b9), run_time=0.1 * d)
      self.wait(0.08 * d)
      self.play(FadeIn(b10), run_time=0.1 * d)
      strip = VGroup()
      for k in range(2, 19):
        settled = all(k % q for q in range(2, k)) or all((k - 1) % q for q in range(2, k - 1))
        sq = Square(0.6, stroke_width=2, stroke_color=ACCENT if settled else SECONDARY)
        sq.set_fill(ACCENT if settled else SECONDARY, opacity=0.2)
        sq.add(M(str(k), 0.6).move_to(sq))
        strip.add(sq)
      strip.arrange(RIGHT, buff=0.1).move_to(DOWN * 0.6)
      klab = M('k', 0.7, MUTED).next_to(strip, LEFT, buff=0.3)
      legend = VGroup(T('settled', 0.6, ACCENT), T('open', 0.6, SECONDARY)).arrange(RIGHT, buff=1.0)
      legend.next_to(strip, DOWN, buff=0.35)
      self.play(LaggedStart(*[FadeIn(s) for s in strip], lag_ratio=0.06), FadeIn(klab), FadeIn(legend),
                run_time=0.2 * d)
      self.wait(0.05 * d)
      guess = T(r'the guess, always $k$, needs a draw in dimension $k-1$', 0.7, MUTED).move_to(DOWN * 2.8)
      self.play(FadeIn(guess), run_time=0.1 * d)

    with self.say('s14_end', pause=4.0) as d:
      self.play(FadeOut(Group(*self.mobjects)), run_time=0.15 * d)
      t1 = T(r'Exact off-diagonal Hales--Jewett numbers at prime successors', 0.85)
      t2 = T(r'Valyu Research, 2026', 0.7, MUTED)
      t3 = T(r'\texttt{maths/combinatorics/ramsey-theory/prime-successor-hales-jewett}', 0.55, MUTED)
      t4 = T(r'Narration uses a synthetic voice.', 0.55, MUTED)
      endc = VGroup(t1, t2, t3).arrange(DOWN, buff=0.4).move_to(UP * 0.3)
      t4.to_edge(DOWN, buff=0.6)
      self.play(FadeIn(endc), FadeIn(t4), run_time=0.3 * d)
