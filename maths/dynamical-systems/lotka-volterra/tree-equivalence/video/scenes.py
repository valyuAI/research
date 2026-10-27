"""Explainer: generic Lotka-Volterra tree systems remember their trees.

Running example: the four-species chain 1-2-3-4 against the four-species star (centre 1).
Their tables are the verifier's explicit generic parameters (generic_matrix in
../verification/verify_lv_tree.py); check_numbers.py re-derives every number shown here.
The fox-rabbit equations in the opening scenes are an illustration with round numbers.
"""

from manim import *
from vrvideo import *

SCENES = ['Hook', 'Growth', 'PredatorPrey', 'ManySpecies', 'Trees', 'Mixing', 'Invariants', 'Fingerprint',
          'Complete', 'Rebuild', 'Status', 'Recap']

FOX = EXTRA
PAIR = WARM            # two-species mixtures and their triangles
BRANCH = [ACCENT, EXTRA, EARTH]
DIM = '#5b6068'

CHAIN = [[-25, 1, 1, 1], [1, -26, 1, 1], [1, 2, -27, 1], [1, 2, 2, -28]]
STAR = [[-25, 1, 1, 1], [1, -26, 1, 1], [2, 1, -27, 1], [3, 1, 1, -28]]
CHAIN_EDGES = [(1, 2), (2, 3), (3, 4)]
STAR_EDGES = [(1, 2), (1, 3), (1, 4)]


def T(s, scale=0.7, color=INK):
  return Tex(s, color=color).scale(scale)


def M(s, scale=0.7, color=INK):
  return MathTex(s, color=color).scale(scale)


def tinted(color, amount=0.35):
  """An opaque tint, so lines behind a dot stay hidden."""
  return interpolate_color(ManimColor(BACKGROUND), ManimColor(color), amount)


# ---------------------------------------------------------------- numerics

def rk4(f, x0, h, steps):
  xs = [np.array(x0, dtype=float)]
  x = xs[0]
  for _ in range(steps):
    k1 = f(x)
    k2 = f(x + h / 2 * k1)
    k3 = f(x + h / 2 * k2)
    k4 = f(x + h * k3)
    x = x + h / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
    xs.append(x)
  return np.array(xs)


def fox_rabbit(p):
  r, f = p
  return np.array([r * (2 - f), f * (r - 3)])


def plane_field(p):
  """The chain on the plane where species 3 and 4 are absent."""
  x1, x2 = p
  return np.array([x1 * (-25 * x1 + x2), x2 * (x1 - 26 * x2)])


def unit_flow(p):
  v = plane_field(p)
  n = np.linalg.norm(v)
  return v / n if n > 1e-12 else v


def plane_path(start, stop=0.035, h=0.004):
  pts = [np.array(start, dtype=float)]
  while np.linalg.norm(pts[-1]) > stop and len(pts) < 3000:
    pts.append(rk4(unit_flow, pts[-1], h, 1)[-1])
  return np.array(pts)


# ---------------------------------------------------------------- drawing helpers

def species_dot(k, r=0.3, color=PRIMARY, label=True, scale=0.62):
  c = Circle(radius=r, color=color, stroke_width=4).set_fill(BACKGROUND, opacity=1)
  g = VGroup(c)
  if label:
    g.add(M(str(k), scale, color=INK).move_to(c))
  return g


def tree_icon(kind, size=1.0, r=0.3, scale=0.62):
  """Dots keyed 1..4 and lines keyed by edge, centred at the origin."""
  if kind == 'chain':
    pos = {k: np.array([(k - 2.5) * 1.5 * size, 0, 0]) for k in range(1, 5)}
    edges = CHAIN_EDGES
  else:
    pos = {1: ORIGIN.copy()}
    for k, ang in zip([2, 3, 4], [90, 210, 330]):
      pos[k] = 1.35 * size * np.array([np.cos(ang * DEGREES), np.sin(ang * DEGREES), 0])
    edges = STAR_EDGES
  dots = {k: species_dot(k, r, scale=scale).move_to(p).set_z_index(2) for k, p in pos.items()}
  lines = {e: Line(pos[e[0]], pos[e[1]], color=MUTED, stroke_width=4).set_z_index(0) for e in edges}
  grp = VGroup(*lines.values(), *dots.values())
  grp.dots, grp.lines = dots, lines
  return grp


class Grid(VGroup):
  """A 4 by 4 table of numbers with species dots as row and column headers."""

  def __init__(self, A, cell=0.8, scale=0.62, header=True):
    super().__init__()
    n = len(A)
    self.cells, self.nums = {}, {}
    for i in range(n):
      for j in range(n):
        sq = Square(cell, stroke_color=DIM, stroke_width=2).set_fill(BACKGROUND, opacity=0)
        sq.move_to(np.array([(j - (n - 1) / 2) * cell, ((n - 1) / 2 - i) * cell, 0]))
        num = M(str(A[i][j]), scale).move_to(sq)
        self.cells[(i, j)], self.nums[(i, j)] = sq, num
        self.add(sq, num)
    self.rows, self.cols = VGroup(), VGroup()
    if header:
      for k in range(n):
        d = species_dot(k + 1, 0.2 * cell / 0.8, scale=0.5).next_to(self.cells[(k, 0)], LEFT, buff=0.18)
        e = species_dot(k + 1, 0.2 * cell / 0.8, scale=0.5).next_to(self.cells[(0, k)], UP, buff=0.18)
        self.rows.add(d)
        self.cols.add(e)
      self.add(self.rows, self.cols)

  def tint(self, i, j, color, opacity=0.35):
    return self.cells[(i, j)].animate.set_fill(color, opacity=opacity)


def arrow_at(start, direction, length, color=MUTED, width=3, opacity=1.0):
  d = np.array([direction[0], direction[1], 0.0])
  d = d / (np.linalg.norm(d) + 1e-12)
  a = Arrow(start, start + d * length, buff=0, stroke_width=width, color=color,
            max_tip_length_to_length_ratio=0.38, max_stroke_width_to_length_ratio=14)
  a.set_opacity(opacity)
  return a


class SpeciesPlane:
  """Species 1 across, species 2 up, on [0, 1] squared, with equal units."""

  def __init__(self, origin=np.array([-5.9, -0.15, 0]), unit=3.35):
    self.o, self.u = origin, unit

  def p(self, x1, x2):
    return self.o + self.u * np.array([x1, x2, 0])

  def grid(self):
    g = VGroup()
    for k in range(1, 6):
      t = k / 5
      g.add(Line(self.p(t, 0), self.p(t, 1), color=SOFT, stroke_width=1.5))
      g.add(Line(self.p(0, t), self.p(1, t), color=SOFT, stroke_width=1.5))
    return g

  def axes(self):
    return VGroup(Line(self.p(0, 0), self.p(1.08, 0), color=INK, stroke_width=3),
                  Line(self.p(0, 0), self.p(0, 1.08), color=INK, stroke_width=3))

  def arrows(self, step=0.125, length=0.27, axis=False):
    g = VGroup()
    vals = np.arange(step, 1.0001, step)
    for a in vals:
      for b in vals:
        g.add(arrow_at(self.p(a, b), plane_field((a, b)), length, color=GREY_B, width=3, opacity=0.85))
    if axis:
      for a in vals:
        g.add(arrow_at(self.p(a, 0), plane_field((a, 0)), length, color=GREY_B, width=3, opacity=0.85))
    return g

  def labels(self):
    return VGroup(M('x_1', 0.7).next_to(self.p(1.08, 0), RIGHT, buff=0.15),
                  M('x_2', 0.7).next_to(self.p(0, 1.08), UP, buff=0.12))

  def curve(self, pts, color=SECONDARY, width=4):
    return VMobject(stroke_color=color, stroke_width=width).set_points_smoothly(
      [self.p(*q) for q in pts[::6]] + [self.p(*pts[-1])])


SHEAR = np.array([[1, 0], [-26 / 27, 1]])


# ---------------------------------------------------------------- scenes

class Hook(NarratedScene):
  def construct(self):
    ts = rk4(fox_rabbit, (5.0, 1.0), 0.01, 1200)
    ax = Axes(x_range=[0, 12, 2], y_range=[0, 7, 1], x_length=11, y_length=5, tips=False,
              axis_config={'color': MUTED, 'stroke_width': 2, 'include_ticks': False}).shift(DOWN * 0.3)
    times = np.arange(len(ts)) * 0.01
    rab = ax.plot_line_graph(times, ts[:, 0], add_vertex_dots=False, line_color=PRIMARY, stroke_width=5)
    fox = ax.plot_line_graph(times, ts[:, 1], add_vertex_dots=False, line_color=FOX, stroke_width=5)
    lr = T('rabbits', 0.7, PRIMARY).next_to(ax.c2p(12, ts[-1, 0]), RIGHT, buff=0.15)
    lf = T('foxes', 0.7, FOX).next_to(ax.c2p(12, ts[-1, 1]), RIGHT, buff=0.15)
    xl = T('time', 0.6, MUTED).next_to(ax.c2p(12, 0), DOWN, buff=0.2).shift(LEFT * 0.4)
    yl = T('population', 0.6, MUTED).next_to(ax.c2p(0, 7), UP, buff=0.15).shift(RIGHT * 0.6)
    plot = VGroup(ax, rab, fox, xl, yl)
    with self.say('s01_cycles') as d:
      self.play(Create(ax), FadeIn(xl), FadeIn(yl), run_time=0.12 * d)
      self.play(Create(rab), Create(fox), run_time=0.75 * d, rate_func=linear)
      self.play(FadeIn(lr), FadeIn(lf), run_time=0.08 * d)

    chain = tree_icon('chain', 1.05, r=0.38, scale=0.75).move_to(LEFT * 3.5 + UP * 0.4)
    star = tree_icon('star', 1.2, r=0.38, scale=0.75).move_to(RIGHT * 3.7 + UP * 0.4)
    ylab = star.get_bottom()[1] - 0.45
    nc = T('chain', 0.75, MUTED).move_to([chain.get_center()[0], ylab, 0])
    ns = T('star', 0.75, MUTED).move_to([star.get_center()[0], ylab, 0])
    q = M('?', 1.6, SECONDARY).move_to(UP * 0.3)
    with self.say('s01_question') as d:
      self.play(FadeOut(plot), FadeOut(lr), FadeOut(lf), run_time=0.12 * d)
      self.play(LaggedStart(*[GrowFromCenter(v) for v in chain.dots.values()], lag_ratio=0.15),
                LaggedStart(*[GrowFromCenter(v) for v in star.dots.values()], lag_ratio=0.15),
                run_time=0.2 * d)
      self.play(*[Create(l) for l in chain.lines.values()], *[Create(l) for l in star.lines.values()],
                FadeIn(nc), FadeIn(ns), run_time=0.2 * d)
      self.play(Write(q), run_time=0.15 * d)

    neq = M(r'\neq', 1.6, SECONDARY).move_to(q)
    note = VGroup(T('An independent check of a result', 0.75), T('that was announced earlier', 0.75)
                  ).arrange(DOWN, buff=0.15)
    note = card(note, color=MUTED).to_edge(DOWN, buff=0.5)
    with self.say('s01_status', pause=0.6) as d:
      self.play(ReplacementTransform(q, neq), run_time=0.2 * d)
      self.play(FadeIn(note, shift=UP * 0.2), run_time=0.2 * d)
    self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)


class Growth(NarratedScene):
  def construct(self):
    ax = Axes(x_range=[0, 12, 1], y_range=[0, 350, 100], x_length=9, y_length=5, tips=False,
              axis_config={'color': MUTED, 'stroke_width': 2, 'include_ticks': False}).shift(DOWN * 0.4 + LEFT * 0.6)
    curve = ax.plot(lambda t: 100 * np.exp(0.1 * t), x_range=[0, 12], color=PRIMARY, stroke_width=5)
    xl = T('months', 0.6, MUTED).next_to(ax.c2p(12, 0), DOWN, buff=0.2)
    yl = T('rabbits', 0.6, PRIMARY).next_to(ax.c2p(0, 350), UP, buff=0.15)
    dots = VGroup(*[Dot(ax.c2p(t, 100 * np.exp(0.1 * t)), color=SECONDARY, radius=0.08) for t in range(3)])
    seq = M(r'100 \;\to\; 110 \;\to\; 122 \;\to\; \dots', 0.85).to_edge(UP, buff=0.6)
    with self.say('s02_growth') as d:
      self.play(Create(ax), FadeIn(xl), FadeIn(yl), run_time=0.15 * d)
      self.play(LaggedStart(*[GrowFromCenter(x) for x in dots], lag_ratio=0.5), Write(seq), run_time=0.35 * d)
      self.play(Create(curve), run_time=0.4 * d)

    t0 = 8
    y0, slope = 100 * np.exp(0.1 * t0), 10 * np.exp(0.1 * t0)
    tan = Line(ax.c2p(t0 - 2.6, y0 - 2.6 * slope), ax.c2p(t0 + 2.6, y0 + 2.6 * slope), color=SECONDARY,
               stroke_width=4)
    pt = Dot(ax.c2p(t0, y0), color=SECONDARY, radius=0.09)
    eq = MathTex(r'\frac{dr}{dt}', '=', '0.1', r'\times', 'r').scale(1.0)
    eq[0].set_color(SECONDARY)
    eq[4].set_color(PRIMARY)
    eq.move_to(seq)
    gl = T('gradient = rate of change', 0.6, SECONDARY).next_to(tan.get_end(), RIGHT, buff=0.1).shift(DOWN * 0.3)
    with self.say('s02_rate', pause=0.6) as d:
      self.play(FadeIn(pt), Create(tan), run_time=0.25 * d)
      self.play(FadeIn(gl), run_time=0.15 * d)
      self.play(FadeOut(seq), Write(eq), run_time=0.3 * d)
    self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)


class PredatorPrey(NarratedScene):
  def construct(self):
    e1 = MathTex(r'\frac{dr}{dt}', '=', 'r', r'\times', '(2 -', 'f', ')')
    e1[2].set_color(PRIMARY)
    e1[5].set_color(FOX)
    e2 = MathTex(r'\frac{df}{dt}', '=', 'f', r'\times', '(', 'r', '- 3)')
    e2[2].set_color(FOX)
    e2[5].set_color(PRIMARY)
    eqs = VGroup(e1, e2).arrange(DOWN, buff=0.5, aligned_edge=LEFT).scale(1.0).move_to(UP * 0.3)
    with self.say('s03_rabbits') as d:
      self.play(Write(e1), run_time=0.5 * d)
      self.play(Indicate(e1[5], color=SECONDARY), run_time=0.3 * d)
    with self.say('s03_foxes') as d:
      self.play(Write(e2), run_time=0.6 * d)

    ax = Axes(x_range=[0, 7, 1], y_range=[0, 5, 1], x_length=7.7, y_length=5.5, tips=False,
              axis_config={'color': INK, 'stroke_width': 3, 'include_ticks': False})
    ax.move_to(RIGHT * 2.45 + DOWN * 0.35)
    xl = T('rabbits', 0.65, PRIMARY).next_to(ax.c2p(7, 0), DOWN, buff=0.2).shift(LEFT * 0.5)
    yl = T('foxes', 0.65, FOX).next_to(ax.c2p(0, 5), LEFT, buff=0.2)
    arrows = VGroup()
    for r in np.arange(0.5, 6.6, 0.5):
      for f in np.arange(0.5, 4.6, 0.5):
        v = fox_rabbit((r, f))
        arrows.add(arrow_at(ax.c2p(r, f), v, 0.34, color=GREY_B, width=3, opacity=0.8))
    with self.say('s03_plane') as d:
      self.play(eqs.animate.scale(0.75).to_corner(UL, buff=0.6), run_time=0.15 * d)
      self.play(Create(ax), FadeIn(xl), FadeIn(yl), run_time=0.2 * d)
      self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.01), run_time=0.45 * d)

    orbit = rk4(fox_rabbit, (5.0, 1.0), 0.01, 330)
    path = VMobject().set_points_smoothly([ax.c2p(*p) for p in orbit[::3]])
    dot = Dot(ax.c2p(*orbit[0]), color=SECONDARY, radius=0.11)
    trail = TracedPath(dot.get_center, stroke_color=SECONDARY, stroke_width=5)
    name = T('the Lotka--Volterra equations', 0.75, INK).next_to(eqs, DOWN, buff=0.5).align_to(eqs, LEFT)
    self.add(trail)
    with self.say('s03_loop', pause=0.6) as d:
      self.play(FadeIn(dot), run_time=0.05 * d)
      self.play(MoveAlongPath(dot, path), run_time=0.55 * d, rate_func=linear)
      self.play(FadeIn(name, shift=UP * 0.2), run_time=0.15 * d)
    self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)


class ManySpecies(NarratedScene):
  def construct(self):
    eq = MathTex(r'\frac{dx_1}{dt}', '=', 'x_1', r'\times', '(', '-25', 'x_1', '+', '1', 'x_2', '+', '1', 'x_3',
                 '+', '1', 'x_4', ')').scale(0.95)
    for k in (2, 6, 9, 12, 15):
      eq[k].set_color(PRIMARY)
    eq.to_edge(UP, buff=0.7)
    sub = T('no constant birth or death numbers', 0.65, MUTED).next_to(eq, DOWN, buff=0.35)
    with self.say('s04_many') as d:
      self.play(Write(eq), run_time=0.45 * d)
      self.play(FadeIn(sub), run_time=0.15 * d)

    g = Grid(CHAIN, cell=1.08, scale=0.82).move_to(DOWN * 1.15)
    rl = T('row: who responds', 0.65, MUTED).next_to(g, LEFT, buff=0.5)
    cl = T('column: who acts', 0.65, MUTED).next_to(g, RIGHT, buff=0.5)
    row1 = VGroup(*[g.nums[(0, j)] for j in range(4)])
    with self.say('s04_table') as d:
      self.play(FadeOut(sub), FadeIn(VGroup(*[m for m in g if m not in row1])), run_time=0.25 * d)
      self.play(*[g.tint(0, j, SECONDARY, 0.3) for j in range(4)],
                *[TransformFromCopy(eq[k], g.nums[(0, j)]) for j, k in enumerate((5, 8, 11, 14))],
                run_time=0.35 * d)
      self.play(FadeIn(rl), FadeIn(cl), run_time=0.2 * d)
    with self.say('s04_diag', pause=0.6) as d:
      self.play(*[g.tint(0, j, BACKGROUND, 0) for j in range(4)],
                *[g.tint(i, i, WARN, 0.35) for i in range(4)], run_time=0.4 * d)
    self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)


class Trees(NarratedScene):
  def construct(self):
    pos = [LEFT * 4.5 + UP * 1.2, LEFT * 1.5 + UP * 1.2, RIGHT * 1.5 + UP * 1.2, RIGHT * 4.5 + UP * 1.2]
    loose = VGroup(*[species_dot(k + 1).move_to(p) for k, p in enumerate(pos)])
    sq = VGroup(*[species_dot(k + 1).move_to(p) for k, p in
                  enumerate([LEFT * 1 + DOWN * 1.3, RIGHT * 1 + DOWN * 1.3, RIGHT * 1 + DOWN * 3.3,
                             LEFT * 1 + DOWN * 3.3])])
    chain = tree_icon('chain', 1.05, r=0.36, scale=0.72).move_to(LEFT * 3.4 + UP * 0.4)
    star = tree_icon('star', 1.2, r=0.36, scale=0.72).move_to(RIGHT * 3.7 + UP * 0.4)
    loop = VGroup(*[Line(sq[i].get_center(), sq[(i + 1) % 4].get_center(), color=WARN, stroke_width=4)
                    for i in range(4)])
    loop.set_z_index(-1)
    loop_grp = VGroup(loop, sq).scale(1.1).move_to(UP * 0.3)
    loop_cap = T('a loop: not a tree', 0.75, WARN).next_to(loop_grp, DOWN, buff=0.3)
    with self.say('s05_graph') as d:
      self.play(LaggedStart(*[GrowFromCenter(x) for x in loose], lag_ratio=0.2), run_time=0.15 * d)
      lines = VGroup(*[Line(pos[i], pos[i + 1], color=MUTED, stroke_width=4) for i in range(3)])
      lines.set_z_index(-1)
      self.play(Create(lines), run_time=0.15 * d)
      self.play(FadeOut(loose), FadeOut(lines), FadeIn(loop_grp), FadeIn(loop_cap), run_time=0.15 * d)
      self.wait(0.15 * d)
      self.play(FadeOut(loop_grp), FadeOut(loop_cap), FadeIn(chain), FadeIn(star), run_time=0.2 * d)
    ylab = star.get_bottom()[1] - 0.45
    nc = T('chain', 0.7, MUTED).move_to([chain.get_center()[0], ylab, 0])
    ns = T('star', 0.7, MUTED).move_to([star.get_center()[0], ylab, 0])
    warn = VGroup(T('not a food web:', 0.75, INK), T('a rule about which effects are equal', 0.75, SECONDARY)
                  ).arrange(DOWN, buff=0.18).to_edge(DOWN, buff=0.6)
    with self.say('s05_warn') as d:
      self.play(FadeIn(nc), FadeIn(ns), run_time=0.15 * d)
      self.play(FadeIn(warn[0]), run_time=0.2 * d)
      self.play(FadeIn(warn[1]), run_time=0.25 * d)

    g = Grid(CHAIN, cell=0.92, scale=0.72).move_to(DOWN * 1.15)
    with self.say('s05_cut') as d:
      self.play(FadeOut(star), FadeOut(ns), FadeOut(nc), FadeOut(warn), chain.animate.scale(0.85).move_to(UP * 2.85),
                run_time=0.2 * d)
      self.play(FadeIn(g), run_time=0.15 * d)
      self.play(chain.dots[2].animate.set_opacity(0.2), chain.lines[(1, 2)].animate.set_opacity(0.15),
                chain.lines[(2, 3)].animate.set_opacity(0.15), run_time=0.15 * d)
      self.play(chain.dots[1][0].animate.set_stroke(BRANCH[0]).set_fill(tinted(BRANCH[0], 0.35), opacity=1),
                *[chain.dots[k][0].animate.set_stroke(BRANCH[1]).set_fill(tinted(BRANCH[1], 0.35), opacity=1) for k in (3, 4)],
                run_time=0.2 * d)
    free = VGroup(T('ten free numbers,', 0.72), T('not sixteen', 0.72, MUTED)).arrange(DOWN, buff=0.15)
    free.move_to(RIGHT * 4.75 + DOWN * 1.15)
    with self.say('s05_column') as d:
      self.play(g.tint(0, 1, BRANCH[0], 0.45), Indicate(g.nums[(0, 1)], color=INK), run_time=0.2 * d)
      self.play(g.tint(2, 1, BRANCH[1], 0.45), g.tint(3, 1, BRANCH[1], 0.45), run_time=0.2 * d)
      self.play(FadeIn(free), run_time=0.2 * d)
    gs = Grid(STAR, cell=0.92, scale=0.72).move_to(g)
    star2 = tree_icon('star', 0.62, r=0.28, scale=0.6).move_to(UP * 2.55)
    with self.say('s05_star', pause=0.6) as d:
      self.play(FadeOut(free), ReplacementTransform(chain, star2), ReplacementTransform(g, gs), run_time=0.25 * d)
      self.play(star2.dots[1].animate.set_opacity(0.2), *[l.animate.set_opacity(0.15) for l in star2.lines.values()],
                *[star2.dots[k][0].animate.set_stroke(BRANCH[k - 2]).set_fill(tinted(BRANCH[k - 2], 0.35), opacity=1)
                  for k in (2, 3, 4)], run_time=0.2 * d)
      self.play(*[gs.tint(k - 1, 0, BRANCH[k - 2], 0.45) for k in (2, 3, 4)], run_time=0.2 * d)
    self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)


class Mixing(NarratedScene):
  def construct(self):
    P = SpeciesPlane()
    grid, axes, arrows, labels = P.grid(), P.axes(), P.arrows(), P.labels()
    icon = tree_icon('chain', 0.55, r=0.22, scale=0.5).move_to(RIGHT * 3.2 + UP * 2.6)
    e1 = MathTex(r'\frac{dx_1}{dt}', '=', 'x_1', r'\times', r'(-25x_1 + x_2)').scale(0.75)
    e2 = MathTex(r'\frac{dx_2}{dt}', '=', 'x_2', r'\times', r'(x_1 - 26x_2)').scale(0.75)
    eqs = VGroup(e1, e2).arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to(RIGHT * 3.2 + UP * 0.6)
    with self.say('s06_absent') as d:
      self.play(FadeIn(icon), run_time=0.1 * d)
      self.play(icon.dots[3].animate.set_opacity(0.2), icon.dots[4].animate.set_opacity(0.2),
                icon.lines[(3, 4)].animate.set_opacity(0.15), icon.lines[(2, 3)].animate.set_opacity(0.15),
                run_time=0.2 * d)
      self.play(Create(grid), Create(axes), FadeIn(labels), run_time=0.2 * d)
      self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.01), Write(eqs), run_time=0.35 * d)

    mix = VGroup(MathTex('y_1', '=', 'x_1').scale(0.8),
                 MathTex('y_2', '=', '27x_2 - 26x_1').scale(0.8)).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
    for m in mix:
      m[0].set_color(SECONDARY)
    mix.move_to(RIGHT * 3.2 + DOWN * 1.9)
    moving = VGroup(grid, axes, arrows)
    vaxis = Line(P.p(0, -1.02), P.p(0, 1.08), color=MUTED, stroke_width=2).set_z_index(-2)
    haxis = Line(P.p(0, 0), P.p(1.08, 0), color=MUTED, stroke_width=2).set_z_index(-2)
    newl = VGroup(M('y_1', 0.7, SECONDARY).next_to(P.p(1.08, 0), RIGHT, buff=0.15),
                  M('y_2', 0.7, SECONDARY).next_to(P.p(0, 1.08), LEFT, buff=0.15))
    with self.say('s06_mix') as d:
      self.play(Write(mix), run_time=0.35 * d)
      self.add(haxis)
      self.play(ApplyMatrix(SHEAR, moving, about_point=P.o), Create(vaxis), FadeOut(labels), FadeIn(newl),
                run_time=0.4 * d)

    before = MathTex(r'\begin{pmatrix} -25 & 1 \\ 1 & -26 \end{pmatrix}').scale(0.7)
    after = MathTex(r'\tfrac{1}{27}\begin{pmatrix} -649 & 1 \\ -1351 & -26 \end{pmatrix}').scale(0.7)
    tabs = VGroup(VGroup(T('before', 0.6, MUTED), before).arrange(DOWN, buff=0.2),
                  VGroup(T('after', 0.6, SECONDARY), after).arrange(DOWN, buff=0.2)).arrange(RIGHT, buff=0.7)
    tabs.move_to(RIGHT * 3.3 + DOWN * 0.2)
    shape = MathTex(r'\frac{dy_i}{dt}', '=', 'y_i', r'\times', r'(\text{weighted sum})').scale(0.75)
    shape.move_to(RIGHT * 3.3 + UP * 2.2)
    with self.say('s06_same') as d:
      self.play(FadeOut(icon), FadeOut(eqs), FadeOut(mix), run_time=0.15 * d)
      self.play(Write(shape), run_time=0.3 * d)
      self.play(FadeIn(tabs[0]), run_time=0.15 * d)
      self.play(FadeIn(tabs[1]), run_time=0.15 * d)

    chain = tree_icon('chain', 0.8).move_to(LEFT * 3.6 + DOWN * 0.2)
    star = tree_icon('star', 0.95).move_to(RIGHT * 3.6 + DOWN * 0.2)
    q = M('?', 1.5, SECONDARY).move_to(DOWN * 0.2)
    head = VGroup(T('equivalent', 0.85, SECONDARY), T('= the same system in disguise', 0.85)).arrange(RIGHT, buff=0.2)
    head.to_edge(UP, buff=0.7)
    with self.say('s06_equiv') as d:
      self.play(FadeOut(VGroup(moving, vaxis, haxis, newl, shape, tabs)), run_time=0.15 * d)
      self.play(FadeIn(head), run_time=0.2 * d)
      self.play(FadeIn(chain), FadeIn(star), run_time=0.2 * d)
      self.play(Write(q), run_time=0.15 * d)
    conj = VGroup(T('van der Kamp, 2025: conjectured no,', 0.7), T('checked up to eight species', 0.7, MUTED)
                  ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.6)
    with self.say('s06_conj', pause=0.6) as d:
      self.play(FadeIn(conj, shift=UP * 0.2), run_time=0.3 * d)
    self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)


class Invariants(NarratedScene):
  def construct(self):
    P = SpeciesPlane()
    grid, axes, arrows, labels = P.grid(), P.axes(), P.arrows(axis=True), P.labels()
    why = VGroup(T('Why this mixture?', 0.8), M('27x_2 - 26x_1', 0.9, PAIR)).arrange(DOWN, buff=0.3)
    why.move_to(RIGHT * 3.2 + UP * 0.5)
    with self.say('s07_why') as d:
      self.play(FadeIn(grid), FadeIn(axes), FadeIn(labels), FadeIn(arrows), run_time=0.3 * d)
      self.play(FadeIn(why), run_time=0.3 * d)

    e = MathTex(r'\frac{dx_2}{dt}', '=', 'x_2', r'\times', r'(\dots)').scale(0.85)
    e[2].set_color(SECONDARY)
    e.move_to(RIGHT * 3.2 + UP * 1.8)
    stay = T('zero stays zero', 0.75, SECONDARY).next_to(e, DOWN, buff=0.4)
    axis_hi = Line(P.p(0, 0), P.p(1, 0), color=SECONDARY, stroke_width=7)
    dot = Dot(P.p(0.98, 0), color=SECONDARY, radius=0.1)
    with self.say('s07_extinct') as d:
      self.play(FadeOut(why), Write(e), run_time=0.25 * d)
      self.play(Create(axis_hi), FadeIn(dot), run_time=0.2 * d)
      self.play(dot.animate.move_to(P.p(0.05, 0)), FadeIn(stay), run_time=0.4 * d)

    l1 = MathTex(r'\frac{d}{dt}', '(27x_2 - 26x_1)').scale(0.75)
    l2 = MathTex('=', r'650x_1^2 + x_1x_2 - 702x_2^2').scale(0.75)
    l3 = MathTex('=', '(27x_2 - 26x_1)', r'(-25x_1 - 26x_2)').scale(0.75)
    l1[1].set_color(PAIR)
    l3[1].set_color(PAIR)
    work = VGroup(l1, l2, l3).arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to(RIGHT * 3.25 + UP * 0.9)
    with self.say('s07_factor') as d:
      self.play(FadeOut(e), FadeOut(stay), FadeOut(axis_hi), FadeOut(dot), Write(l1), run_time=0.25 * d)
      self.play(Write(l2), run_time=0.25 * d)
      self.play(Write(l3), run_time=0.25 * d)
      self.play(Indicate(l3[1], color=SECONDARY), run_time=0.15 * d)

    ray = Line(P.p(0, 0), P.p(1.04, 1.04 * 26 / 27), color=PAIR, stroke_width=6)
    ratio = T('ratio 27 : 26 stays fixed', 0.75, PAIR).move_to(RIGHT * 3.25 + DOWN * 1.3)
    d_on = Dot(P.p(0.98, 0.98 * 26 / 27), color=SECONDARY, radius=0.1)
    others = [plane_path(s) for s in [(0.2, 0.98), (0.98, 0.2), (0.55, 0.98)]]
    dots = VGroup(*[Dot(P.p(*o[0]), color=GREY_A, radius=0.08) for o in others])
    with self.say('s07_ray') as d:
      self.play(Create(ray), run_time=0.25 * d)
      self.play(FadeIn(d_on), FadeIn(dots), FadeIn(ratio), run_time=0.15 * d)
      path_on = Line(d_on.get_center(), P.p(0.04, 0.04 * 26 / 27))
      self.play(MoveAlongPath(d_on, path_on),
                *[MoveAlongPath(x, P.curve(o)) for x, o in zip(dots, others)], run_time=0.5 * d, rate_func=linear)

    name = VGroup(T('Darboux polynomials', 0.85, PAIR), T('hidden invariants: their zeros are conserved', 0.65)
                  ).arrange(DOWN, buff=0.2).move_to(RIGHT * 3.25 + DOWN * 2.4)
    vaxis = Line(P.p(0, -1.02), P.p(0, 1.08), color=MUTED, stroke_width=2).set_z_index(-2)
    with self.say('s07_name') as d:
      self.play(FadeOut(ratio), FadeOut(d_on), FadeOut(dots), FadeIn(name), run_time=0.3 * d)
      self.play(ApplyMatrix(SHEAR, VGroup(grid, axes, arrows, ray), about_point=P.o), Create(vaxis), FadeOut(labels),
                run_time=0.4 * d)
      self.play(Indicate(ray, color=SECONDARY), run_time=0.2 * d)

    chain = tree_icon('chain', 1.2).move_to(UP * 1.6)
    mids = VGroup(*[Dot((chain.dots[a].get_center() + chain.dots[b].get_center()) / 2, color=PAIR, radius=0.13)
                    for a, b in CHAIN_EDGES])
    singles = M(r'x_1,\quad x_2,\quad x_3,\quad x_4', 0.85, PRIMARY)
    pairs = M(r'27x_2 - 26x_1,\quad x_2 - x_3,\quad x_3 - x_4', 0.85, PAIR)
    lst = VGroup(singles, pairs).arrange(DOWN, buff=0.35).move_to(DOWN * 0.9)
    tot = M(r'4 + 3 = 7', 0.9).to_edge(DOWN, buff=0.7)
    star_note = T('the star: also 7', 0.65, MUTED).next_to(tot, RIGHT, buff=0.8)
    with self.say('s07_list', pause=0.6) as d:
      self.play(FadeOut(VGroup(grid, axes, arrows, ray, vaxis, work, name)), run_time=0.12 * d)
      self.play(FadeIn(chain), run_time=0.12 * d)
      self.play(Write(singles), run_time=0.18 * d)
      self.play(LaggedStart(*[GrowFromCenter(m) for m in mids], lag_ratio=0.3), Write(pairs), run_time=0.25 * d)
      self.play(FadeIn(tot), run_time=0.1 * d)
      self.play(FadeIn(star_note), run_time=0.1 * d)
    self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)


def triple_layout(kind, scale=1.0):
  """Scrambled positions for the 7 invariants: species 1..4, then the three pair mixtures."""
  if kind == 'chain':
    pts = {'s1': (-2.6, 1.6), 's2': (-0.4, -0.6), 's3': (1.6, 1.4), 's4': (2.6, -1.4),
           'e12': (-2.3, -1.5), 'e23': (-0.2, 2.1), 'e34': (0.5, -2.0)}
    tris = [('s1', 's2', 'e12'), ('s2', 's3', 'e23'), ('s3', 's4', 'e34')]
  else:
    pts = {'s1': (0.0, 0.0)}
    for k, ang in zip([2, 3, 4], [90, 210, 330]):
      a1, a2 = (ang - 22) * DEGREES, (ang + 22) * DEGREES
      pts[f's{k}'] = (2.2 * np.cos(a1), 2.2 * np.sin(a1))
      pts[f'e1{k}'] = (2.2 * np.cos(a2), 2.2 * np.sin(a2))
    tris = [('s1', 's2', 'e12'), ('s1', 's3', 'e13'), ('s1', 's4', 'e14')]
  return {k: scale * np.array([x, y, 0]) for k, (x, y) in pts.items()}, tris


def triangle_set(dots, tris, opacity=0.22):
  return VGroup(*[Polygon(*[dots[k].get_center() for k in t], stroke_color=PAIR, stroke_width=3,
                          fill_color=PAIR, fill_opacity=opacity) for t in tris])


class Fingerprint(NarratedScene):
  def construct(self):
    before = ['x_1', 'x_2', 'x_3', 'x_4', '27x_2 - 26x_1', 'x_2 - x_3', 'x_3 - x_4']
    after = ['y_1 + y_2', 'y_2 + y_3', 'y_1 + y_3 + y_4', 'y_3 + y_4', '-26y_1 + y_2 + 27y_3',
             '-y_1 + y_2 - y_4', 'y_1']
    colors = [PRIMARY] * 4 + [PAIR] * 3
    lb = VGroup(*[M(s, 0.85, c) for s, c in zip(before, colors)]).arrange(DOWN, buff=0.3)
    la = VGroup(*[M(s, 0.85, c) for s, c in zip(after, colors)])
    lb.move_to(LEFT * 3.0 + DOWN * 0.2)
    for a, b in zip(la, lb):
      a.move_to(RIGHT * 3.0 + b.get_center()[1] * UP)
    hb = T('before', 0.7, MUTED).next_to(lb, UP, buff=0.4)
    ha = T('after mixing', 0.7, MUTED).next_to(la, UP, buff=0.4).align_to(hb, DOWN)
    arr = Arrow(LEFT * 0.8, RIGHT * 0.8, color=SECONDARY, buff=0).move_to(DOWN * 0.2)
    with self.say('s08_carry') as d:
      self.play(FadeIn(hb), LaggedStart(*[FadeIn(x) for x in lb], lag_ratio=0.1), run_time=0.3 * d)
      self.play(GrowArrow(arr), FadeIn(ha), run_time=0.15 * d)
      self.play(LaggedStart(*[TransformFromCopy(b, a) for b, a in zip(lb, la)], lag_ratio=0.08), run_time=0.4 * d)
    box = SurroundingRectangle(VGroup(lb[6], la[6]), color=SECONDARY, buff=0.12, corner_radius=0.08)
    with self.say('s08_scramble') as d:
      self.play(Create(box), run_time=0.25 * d)
      self.wait(0.3 * d)
      self.play(FadeOut(box), *[x.animate.set_color(GREY_B) for x in la], run_time=0.3 * d)

    rel = MathTex('-26y_1 + y_2 + 27y_3', '=', '27', '(y_2 + y_3)', '- 26', '(y_1 + y_2)').scale(0.7)
    rel[0].set_color(PAIR)
    rel[3].set_color(PRIMARY)
    rel[5].set_color(PRIMARY)
    rel.scale(1.15).to_edge(DOWN, buff=0.45)
    tick = MathTex(r'\checkmark', color=OK).scale(0.9).next_to(rel, RIGHT, buff=0.3)
    linked = T('a linked triple', 0.75, PAIR).next_to(rel, UP, buff=0.25)
    with self.say('s08_linked') as d:
      sel = VGroup(*[SurroundingRectangle(VGroup(lb[i], la[i]), color=PAIR, buff=0.08, corner_radius=0.06)
                     for i in (0, 1, 4)])
      self.play(Create(sel), *[la[i].animate.set_color(colors[i]) for i in (0, 1, 4)], run_time=0.25 * d)
      self.play(VGroup(hb, ha, lb, la, arr, sel).animate.scale(0.82).shift(UP * 0.75), run_time=0.1 * d)
      self.play(Write(rel), run_time=0.3 * d)
      self.play(FadeIn(tick), FadeIn(linked), run_time=0.15 * d)

    # The chain drawn with each pair mixture sitting just off its line, then scrambled.
    chain = tree_icon('chain', 1.75, r=0.3)
    start = {f's{k}': chain.dots[k].get_center() for k in range(1, 5)}
    for a, b in CHAIN_EDGES:
      start[f'e{a}{b}'] = (chain.dots[a].get_center() + chain.dots[b].get_center()) / 2 + DOWN * 0.75
    pos, tris = triple_layout('chain')
    dots = {k: Dot(p, radius=0.19, color=PRIMARY if k[0] == 's' else PAIR).set_z_index(3) for k, p in start.items()}
    tri0 = triangle_set(dots, tris)
    tri = always_redraw(lambda: triangle_set(dots, tris))
    with self.say('s08_triangles') as d:
      self.play(FadeOut(VGroup(hb, ha, lb, la, arr, sel, rel, tick, linked)), run_time=0.12 * d)
      self.play(FadeIn(chain.lines[(1, 2)]), FadeIn(chain.lines[(2, 3)]), FadeIn(chain.lines[(3, 4)]),
                *[GrowFromCenter(x) for x in dots.values()], run_time=0.2 * d)
      self.play(FadeIn(tri0), run_time=0.15 * d)
      self.remove(tri0)
      self.add(tri)
      self.play(FadeOut(VGroup(*chain.lines.values())),
                *[dots[k].animate.move_to(pos[k]).set_color(INK) for k in dots], run_time=0.35 * d)

    s_pos, s_tris = triple_layout('star', 0.85)
    left, right = LEFT * 3.5, RIGHT * 3.5
    sdots = {k: Dot(p + right, radius=0.17, color=INK).set_z_index(3) for k, p in s_pos.items()}
    stri = triangle_set(sdots, s_tris)
    cl = T('chain', 0.7, MUTED).move_to(left + DOWN * 3.2)
    sl = T('star', 0.7, MUTED).move_to(right + DOWN * 3.2)
    with self.say('s08_count', pause=0.6) as d:
      self.play(*[dots[k].animate.move_to(0.85 * pos[k] + left + UP * 0.2).scale(0.9) for k in dots], run_time=0.15 * d)
      self.play(*[FadeIn(x) for x in sdots.values()], FadeIn(stri), FadeIn(cl), FadeIn(sl), run_time=0.15 * d)
      c2 = VGroup(*[M('2', 0.8, SECONDARY).move_to(dots[k].get_center() + np.array([0.42, 0.38, 0]))
                    for k in ('s2', 's3')])
      self.play(*[dots[k].animate.set_color(SECONDARY).scale(1.4) for k in ('s2', 's3')], FadeIn(c2),
                run_time=0.2 * d)
      c3 = M('3', 0.8, SECONDARY).move_to(sdots['s1'].get_center() + np.array([0.42, 0.42, 0]))
      self.play(sdots['s1'].animate.set_color(SECONDARY).scale(1.4), FadeIn(c3), run_time=0.2 * d)
    tri.clear_updaters()
    self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)


class Complete(NarratedScene):
  def construct(self):
    pos, tris = triple_layout('chain', 0.8)
    dots = {k: Dot(p, radius=0.13, color=INK).set_z_index(3) for k, p in pos.items()}
    base = triangle_set(dots, tris)
    extra = DashedVMobject(Polygon(dots['e12'].get_center(), dots['e23'].get_center(), dots['s4'].get_center(),
                                   stroke_color=WARN, stroke_width=4), num_dashes=30)
    qm = M('?', 1.1, WARN).next_to(extra, RIGHT, buff=0.1).shift(DOWN * 0.5)
    with self.say('s09_hole') as d:
      self.play(FadeIn(base), *[FadeIn(x) for x in dots.values()], run_time=0.2 * d)
      self.play(Create(extra), FadeIn(qm), run_time=0.35 * d)
    chain = tree_icon('chain', 0.9, r=0.28, scale=0.58).move_to(UP * 2.95)
    g = Grid(CHAIN, cell=0.7, scale=0.58).move_to(RIGHT * 4.55 + DOWN * 0.5)
    with self.say('s09_skip') as d:
      self.play(FadeOut(base), FadeOut(extra), FadeOut(qm), *[FadeOut(x) for x in dots.values()], run_time=0.12 * d)
      self.play(FadeIn(chain), FadeIn(g), run_time=0.15 * d)
      self.play(*[chain.dots[k][0].animate.set_stroke(SECONDARY).set_fill(tinted(SECONDARY, 0.3), opacity=1) for k in (1, 3)],
                run_time=0.15 * d)
      self.play(g.tint(0, 1, WARN, 0.5), g.tint(2, 1, WARN, 0.5), run_time=0.2 * d)
      neq = M(r'1 \neq 2', 1.2, WARN).move_to(LEFT * 2.6 + DOWN * 0.5)
      self.play(Write(neq), run_time=0.15 * d)

    # Three in a row: aligned columns for p1, p2, p3.
    X = [-5.5, -3.4, -1.3, 0.3]
    Y = [1.1, 0.0, -1.1]

    def row(terms, y):
      grp = VGroup()
      for t, x in zip(terms, X):
        m = M(t, 1.05) if t else VectorizedPoint()
        m.move_to([x, y, 0])
        grp.add(m)
      return grp

    r1 = row(['27p_1', '+\\,26p_2', '', '=0'], Y[0])
    r2 = row(['', 'p_2', '+\\,p_3', '=0'], Y[1])
    r3 = row(['28p_1', '', '+\\,26p_3', '=0'], Y[2])
    with self.say('s09_three') as d:
      self.play(FadeOut(neq), g.tint(0, 1, BACKGROUND, 0), g.tint(2, 1, BACKGROUND, 0),
                chain.dots[2][0].animate.set_stroke(SECONDARY).set_fill(tinted(SECONDARY, 0.3), opacity=1), run_time=0.2 * d)
      self.play(FadeIn(r1), run_time=0.2 * d)
      self.play(FadeIn(r2), run_time=0.2 * d)
      self.play(FadeIn(r3), run_time=0.2 * d)

    r2b = row(['', '-\\,26p_2', '-\\,26p_3', '=0'], Y[1])
    tag = M(r'\times(-26)', 0.75, SECONDARY).next_to(r2b, RIGHT, buff=0.3)
    rule = Line([-6.4, -1.75, 0], [0.9, -1.75, 0], color=MUTED, stroke_width=2)
    res = MathTex('55', 'p_1', '=', '0', color=WARN).scale(1.1).move_to([-2.8, -2.45, 0])
    with self.say('s09_cancel') as d:
      self.play(ReplacementTransform(r2, r2b), FadeIn(tag), run_time=0.25 * d)
      self.play(Create(rule), run_time=0.08 * d)
      self.play(r1[1].animate.set_color(SECONDARY), r2b[1].animate.set_color(SECONDARY), run_time=0.15 * d)
      self.play(r1[1].animate.set_opacity(0.25), r2b[1].animate.set_opacity(0.25), run_time=0.1 * d)
      self.play(r2b[2].animate.set_color(SECONDARY), r3[2].animate.set_color(SECONDARY), run_time=0.15 * d)
      self.play(r2b[2].animate.set_opacity(0.25), r3[2].animate.set_opacity(0.25), run_time=0.1 * d)
      self.play(Write(res), run_time=0.12 * d)

    nz = M(r'\text{but } p_1 \neq 0', 0.9, WARN).next_to(res, RIGHT, buff=0.8)
    only = VGroup(T('only single species', 0.7, PRIMARY), T('and the tree\'s own pairs', 0.7, PAIR)
                  ).arrange(DOWN, buff=0.15).move_to(RIGHT * 4.55 + DOWN * 3.2)
    with self.say('s09_contra') as d:
      self.play(Write(nz), run_time=0.2 * d)
      self.play(Indicate(VGroup(res, nz), color=WARN), run_time=0.2 * d)
      self.play(FadeIn(only), run_time=0.2 * d)

    split = MathTex('55', '=', '(1 + 26)', '+', '(2 + 26)').scale(1.0).move_to([-2.8, -2.45, 0])
    with self.say('s09_generic') as d:
      self.play(FadeOut(nz), FadeOut(only), TransformMatchingTex(res, split), run_time=0.25 * d)
      self.play(g.tint(0, 1, SECONDARY, 0.4), g.tint(2, 1, SECONDARY, 0.4), g.tint(1, 1, SECONDARY, 0.4),
                Indicate(split[2], color=SECONDARY), Indicate(split[4], color=SECONDARY), run_time=0.3 * d)
      gen = T('generic: no such sum is zero', 0.7, SECONDARY).next_to(split, DOWN, buff=0.3)
      self.play(FadeIn(gen), run_time=0.15 * d)
    lean = card(T('checked in Lean, with letters for numbers', 0.65, OK), color=OK, buff=0.2)
    lean.move_to(RIGHT * 3.35 + DOWN * 3.25)
    with self.say('s09_lean', pause=0.6) as d:
      self.play(FadeIn(lean, shift=UP * 0.2), run_time=0.3 * d)
    self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)


class Rebuild(NarratedScene):
  def construct(self):
    pts = {'s2': (-4.4, 0.6), 's4': (-2.4, -0.7), 's6': (-1.5, 1.1),
           's1': (-6.0, 1.5), 'e12': (-5.8, -0.5), 's3': (-3.5, 2.4), 'e23': (-5.0, 2.5),
           'e24': (-3.9, -1.5), 's5': (-3.0, -2.9), 'e45': (-1.3, -2.5), 'e46': (-0.8, -0.4),
           's7': (-2.4, 2.4), 'e67': (-0.7, 2.3)}
    tris = [('s2', 's1', 'e12'), ('s2', 's3', 'e23'), ('s2', 's4', 'e24'), ('s4', 's5', 'e45'),
            ('s4', 's6', 'e46'), ('s6', 's7', 'e67')]
    dots = {k: Dot(np.array([x, y, 0]), radius=0.13, color=INK).set_z_index(3) for k, (x, y) in pts.items()}
    tri = triangle_set(dots, tris)
    shared = ['s2', 's4', 's6']
    with self.say('s10_rule') as d:
      self.play(FadeIn(tri), *[FadeIn(x) for x in dots.values()], run_time=0.2 * d)
      self.play(*[dots[k].animate.set_color(SECONDARY).scale(1.5) for k in shared], run_time=0.25 * d)
      self.play(Indicate(tri[2], color=SECONDARY), run_time=0.2 * d)
      self.play(Indicate(tri[0], color=SECONDARY), run_time=0.2 * d)

    vpos = {'s2': (2.0, 0.3), 's4': (3.8, 0.3), 's6': (5.4, 1.4), 's1': (0.9, 1.6), 's3': (0.9, -1.0),
            's5': (3.8, -1.6), 's7': (6.6, 0.2)}
    nodes = {k: Dot(np.array([*vpos[k], 0]), radius=0.2, color=PRIMARY).set_z_index(3) for k in vpos}
    for k in shared:
      nodes[k].set_color(SECONDARY)
    order = [(2, ('s2', 's4')), (4, ('s4', 's6')), (0, ('s2', 's1')), (1, ('s2', 's3')), (3, ('s4', 's5')),
             (5, ('s6', 's7'))]
    arrow = Arrow(LEFT * 0.4, RIGHT * 0.4, color=MUTED, buff=0).move_to(RIGHT * 0.0 + DOWN * 2.6)
    done = T('rebuilt exactly', 0.75, OK).move_to(RIGHT * 3.7 + DOWN * 3.0)
    with self.say('s10_big', pause=0.6) as d:
      self.play(*[GrowFromCenter(nodes[k]) for k in shared], run_time=0.1 * d)
      for i, (a, b) in order:
        ln = Line(nodes[a].get_center(), np.array([*vpos[b], 0]), color=MUTED, stroke_width=5).set_z_index(1)
        anims = [Indicate(tri[i], color=SECONDARY, scale_factor=1.05), Create(ln)]
        if b not in shared:
          anims.append(GrowFromCenter(nodes[b]))
        self.play(*anims, run_time=0.09 * d)
      self.play(FadeIn(done), run_time=0.1 * d)
    self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)


class Status(NarratedScene):
  def construct(self):
    line = Line(LEFT * 6.2, RIGHT * 6.2, color=MUTED, stroke_width=3).shift(UP * 1.6)
    xs = [-4.8, -1.6, 1.6, 4.8]
    years = ['2023', '2025', r'Sept.\ 2026', r'Oct.\ 2026']
    labs = [['tree families', 'introduced'], ['conjecture', '(van der Kamp)'], ['Zeng preprint', 'announces it'],
            ['this note', 'independent proof']]
    ticks, ylab, desc = VGroup(), VGroup(), VGroup()
    for x, yv, l in zip(xs, years, labs):
      p = np.array([x, 1.6, 0])
      ticks.add(Dot(p, radius=0.11, color=INK))
      ylab.add(T(yv, 0.7, SECONDARY).next_to(p, UP, buff=0.25))
      desc.add(VGroup(T(l[0], 0.66), T(l[1], 0.66, MUTED)).arrange(DOWN, buff=0.12).next_to(p, DOWN, buff=0.3))
    with self.say('s11_history') as d:
      self.play(Create(line), run_time=0.15 * d)
      for i in (0, 1):
        self.play(FadeIn(ticks[i]), FadeIn(ylab[i]), FadeIn(desc[i]), run_time=0.2 * d)
    stamp = T('withdrawn; text unavailable', 0.62, WARN).next_to(desc[2], DOWN, buff=0.25)
    with self.say('s11_zeng') as d:
      self.play(FadeIn(ticks[2]), FadeIn(ylab[2]), FadeIn(desc[2]), run_time=0.25 * d)
      self.play(FadeIn(stamp), run_time=0.25 * d)
    note = card(VGroup(T('a verification note,', 0.8), T('no priority claimed', 0.8, SECONDARY)
                       ).arrange(DOWN, buff=0.15), color=MUTED).move_to(DOWN * 2.4)
    with self.say('s11_ours') as d:
      self.play(FadeIn(ticks[3]), FadeIn(ylab[3]), FadeIn(desc[3]), run_time=0.25 * d)
      self.play(FadeIn(note, shift=UP * 0.2), run_time=0.25 * d)

    def status_row(mark, color, text):
      sym = MathTex(mark, color=color).scale(0.85)
      return VGroup(sym, T(text, 0.8)).arrange(RIGHT, buff=0.35)

    rows1 = VGroup(status_row(r'\checkmark', OK, 'written proof: every size'),
                   status_row(r'\checkmark', OK, r'exact checks: 986 trees up to 12 species,'),
                   T(r'and full invariant lists for 200 trees up to 10', 0.8, MUTED)
                   ).arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to(UP * 0.2)
    rows1[2].shift(RIGHT * 0.7)
    cons = T('consistency checks, not a proof', 0.68, SECONDARY).next_to(rows1, DOWN, buff=0.55)
    with self.say('s11_checks') as d:
      self.play(FadeOut(VGroup(line, ticks, ylab, desc, stamp, note)), run_time=0.1 * d)
      self.play(FadeIn(rows1[0]), run_time=0.15 * d)
      self.play(FadeIn(rows1[1]), run_time=0.2 * d)
      self.play(FadeIn(rows1[2]), run_time=0.2 * d)
      self.play(FadeIn(cons), run_time=0.15 * d)
    rows2 = VGroup(status_row(r'\checkmark', OK, 'Lean: the three-in-a-row step only'),
                   status_row(r'\circ', MUTED, 'not yet refereed externally')
                   ).arrange(DOWN, buff=0.4, aligned_edge=LEFT).move_to(UP * 0.2)
    with self.say('s11_lean') as d:
      self.play(FadeOut(rows1), FadeOut(cons), run_time=0.15 * d)
      self.play(FadeIn(rows2[0]), run_time=0.25 * d)
      self.play(FadeIn(rows2[1]), run_time=0.25 * d)

    eqrows = [[1, 2, 3, 4]] * 4
    g = Grid(eqrows, cell=0.7, scale=0.58, header=False).move_to(LEFT * 3.6 + DOWN * 0.1)
    for c in g.cells.values():
      c.set_fill(WARN, opacity=0.25)
    gl = VGroup(T('every row the same:', 0.65), T('every mixture is an invariant', 0.65, WARN)
                ).arrange(DOWN, buff=0.12).next_to(g, DOWN, buff=0.35)
    fw = VGroup(T('the tree is a rule about equal effects,', 0.65),
                T('not a food web read from data', 0.65, SECONDARY)).arrange(DOWN, buff=0.12)
    fw.move_to(RIGHT * 3.3 + DOWN * 0.1)
    with self.say('s11_scope', pause=0.6) as d:
      self.play(FadeOut(rows2), run_time=0.1 * d)
      self.play(FadeIn(g), FadeIn(gl), run_time=0.3 * d)
      self.play(FadeIn(fw), run_time=0.25 * d)
    self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)


class Recap(NarratedScene):
  def construct(self):
    pts = VGroup(
      T(r'1. Each tree defines a family of population systems.', 0.75),
      T(r'2. Hidden invariants form linked triples; mixing keeps how they overlap.', 0.75),
      T(r'3. The overlaps rebuild the tree: different trees, different systems.', 0.75),
    ).arrange(DOWN, buff=0.55, aligned_edge=LEFT).scale(1.1).move_to(DOWN * 0.1)
    if pts.width > 12.6:
      pts.scale_to_fit_width(12.6)
    with self.say('s12_recap') as d:
      self.wait(0.08 * d)
      self.play(FadeIn(pts[0], shift=UP * 0.15), run_time=0.1 * d)
      self.wait(0.18 * d)
      self.play(FadeIn(pts[1], shift=UP * 0.15), run_time=0.1 * d)
      self.wait(0.24 * d)
      self.play(FadeIn(pts[2], shift=UP * 0.15), run_time=0.1 * d)
    head = T('Still open', 0.9, SECONDARY)
    q = VGroup(T('What happens at the special tables, where extra invariants appear?', 0.72),
               T('Which networks beyond trees can be recovered this way?', 0.72)
               ).arrange(DOWN, buff=0.4, aligned_edge=LEFT)
    blk = VGroup(head, q).arrange(DOWN, buff=0.5)
    with self.say('s12_open', pause=1.0) as d:
      self.play(FadeOut(pts), run_time=0.1 * d)
      self.play(FadeIn(head), FadeIn(q[0]), run_time=0.2 * d)
      self.play(FadeIn(q[1]), run_time=0.2 * d)
    end = VGroup(
      T(r'Linear equivalence of Lotka--Volterra tree systems', 0.95),
      T('Valyu Research, 2026', 0.75, MUTED),
      T(r'\texttt{maths/dynamical-systems/lotka-volterra/tree-equivalence}', 0.55, MUTED),
      T('Narration uses a synthetic voice.', 0.5, MUTED),
    ).arrange(DOWN, buff=0.4)
    self.play(FadeOut(blk), run_time=0.6)
    self.play(FadeIn(end), run_time=0.8)
    self.wait(3.5)
