"""Explainer: recovering a material's stiffness from wave speeds.

Every number drawn here comes from data.json, which data_prep.py rebuilds (with assertions)
from ../paper.tex and ../verification/.
"""

import json
from pathlib import Path

import numpy as np
from manim import *
from vrvideo import *

SCENES = ['Hook', 'Springs', 'Waves', 'SpeedSurface', 'Slice', 'TwentyOne', 'Summaries', 'Twins', 'Result',
          'Split', 'Balance', 'Computer', 'Directions', 'Status', 'Recap']

HERE = Path(__file__).resolve().parent
D = json.loads((HERE / 'data.json').read_text())

# Colour meaning, used in every scene.
CRYSTAL = PRIMARY                 # our crystal, its table and its speeds; midpoints M
TWIN = WARM                       # a competing or twin table
GAP = ManimColor('#E68AB8')       # the half-gap D
HL = SECONDARY                    # the thing currently changing
BAD = WARN
GOOD = OK
DIM = ManimColor('#5b6168')
PANEL = ManimColor('#161a1f')

PAIRS = [(0, 0), (1, 1), (2, 2), (1, 2), (0, 2), (0, 1)]
PIDX = {p: k for k, p in enumerate(PAIRS)}
PIDX.update({(b, a): k for (a, b), k in list(PIDX.items())})


def tensor(V):
  V = np.asarray(V, dtype=float)
  return np.array([V[PIDX[i, j], PIDX[k, l]] for i in range(3) for j in range(3) for k in range(3)
                   for l in range(3)]).reshape(3, 3, 3, 3)


A4 = tensor(D['A'])


def fast_speed(n):
  return float(np.sqrt(np.linalg.eigvalsh(np.einsum('ijkl,j,k->il', A4, n, n))[2]))


def T(s, scale=0.75, color=INK):
  return Tex(s, color=color).scale(scale)


def M(s, scale=0.8, color=INK):
  return MathTex(s, color=color).scale(scale)


def spring(a, b, coils=6, amp=0.15, width=3, color=INK, lead=0.15, opacity=1.0):
  a, b = np.array(a, dtype=float), np.array(b, dtype=float)
  L = np.linalg.norm(b - a)
  u = (b - a) / L
  nrm = np.array([-u[1], u[0], 0.0])
  pts = [a, a + lead * u]
  body = L - 2 * lead
  for k in range(2 * coils):
    t = (k + 0.5) / (2 * coils)
    pts.append(a + (lead + t * body) * u + (amp if k % 2 == 0 else -amp) * nrm)
  pts += [b - lead * u, b]
  return VMobject(stroke_color=color, stroke_width=width, stroke_opacity=opacity).set_points_as_corners(pts)


def everything(scene):
  return Group(*[m for m in scene.mobjects if not isinstance(m, ValueTracker)])


def ball(p, r=0.2, color=INK, opacity=1.0):
  return Dot(p, radius=r, color=color, fill_opacity=opacity)


def check(color=GOOD, scale=1.0):
  return M(r'\checkmark', 0.9 * scale, color)


def cross_mark(color=BAD, scale=1.0):
  return M(r'\times', 1.0 * scale, color)


def polar_curve(radii, angles, scale, center=ORIGIN, color=CRYSTAL, width=4, dashed=False):
  pts = [center + scale * r * np.array([np.cos(a), np.sin(a), 0]) for r, a in zip(radii, angles)]
  vm = VMobject(stroke_color=color, stroke_width=width).set_points_smoothly(pts)
  if dashed:
    return DashedVMobject(vm, num_dashes=90, dashed_ratio=0.55)
  return vm


def fmt(v, dp=2):
  if abs(v - round(v)) < 1e-9 and dp == 0:
    return str(int(round(v)))
  s = f'{v:.{dp}f}'
  return s


def value_table(V, color, cell=0.82, scale=0.55, dp=2, zero_dim=False):
  """6 x 6 grid of cells with entries; returns (cells, entries) indexed [i][j]."""
  cells, entries = VGroup(), VGroup()
  rows_c, rows_e = [], []
  for i in range(6):
    rc, re = [], []
    for j in range(6):
      sq = Square(cell, stroke_color=MUTED, stroke_width=1.5).move_to([(j - 2.5) * cell, (2.5 - i) * cell, 0])
      v = V[i][j]
      txt = fmt(v, dp) if dp else (str(int(v)) if abs(v - round(v)) < 1e-9 else f'{v:g}')
      col = DIM if (zero_dim and abs(v) < 1e-12) else color
      e = M(txt, scale, col).move_to(sq)
      rc.append(sq)
      re.append(e)
      cells.add(sq)
      entries.add(e)
    rows_c.append(rc)
    rows_e.append(re)
  return VGroup(cells, entries), rows_c, rows_e


def cube_icon(F, side=0.85):
  """Oblique drawing of a unit cube deformed by the 3 x 3 matrix F (three visible faces)."""
  P = lambda v: np.array([v[0] + 0.5 * v[1], v[2] + 0.32 * v[1], 0.0]) * side
  V = {(a, b, c): P(np.asarray(F) @ np.array([a, b, c], dtype=float)) for a in (0, 1) for b in (0, 1) for c in (0, 1)}
  front = [V[0, 0, 0], V[1, 0, 0], V[1, 0, 1], V[0, 0, 1]]
  top = [V[0, 0, 1], V[1, 0, 1], V[1, 1, 1], V[0, 1, 1]]
  right = [V[1, 0, 0], V[1, 1, 0], V[1, 1, 1], V[1, 0, 1]]
  g = VGroup(
    Polygon(*right, fill_color=ManimColor('#2b4152'), fill_opacity=1, stroke_color=INK, stroke_width=2),
    Polygon(*top, fill_color=ManimColor('#3f5c72'), fill_opacity=1, stroke_color=INK, stroke_width=2),
    Polygon(*front, fill_color=ManimColor('#24343f'), fill_opacity=1, stroke_color=INK, stroke_width=2),
  )
  return g


def dot_triangle(rows, spacing=0.36, r=0.07, color=CRYSTAL):
  g = VGroup()
  for i in range(rows):
    for j in range(i + 1):
      g.add(Dot([(j - i / 2) * spacing, -i * spacing, 0], radius=r, color=color))
  return g


def sheet_with_curve(side=4.6, center=ORIGIN):
  sheet = Square(side, stroke_color=MUTED, stroke_width=2, fill_color=PANEL, fill_opacity=1).move_to(center)
  h = side / 2 - 0.35
  curve = ParametricFunction(lambda t: center + np.array([t, 0.75 * np.sin(1.3 * t) + 0.18 * t, 0]),
                             t_range=[-h, h], stroke_color=BAD, stroke_width=5)
  return sheet, curve


# ---------------------------------------------------------------------------------------------------------


class Hook(NarratedScene):
  def construct(self):
    c = UP * 0.35
    block = RoundedRectangle(width=10.6, height=5.6, corner_radius=0.35, stroke_color=MUTED, stroke_width=2,
                             fill_color=PANEL, fill_opacity=1).move_to(c)
    grain = VGroup()
    for k in range(9):
      y0, ph = -2.2 + k * 0.55, 0.7 * k
      grain.add(ParametricFunction(lambda t, y0=y0, ph=ph: c + np.array([t, y0 + 0.08 * np.sin(0.9 * t + ph), 0]),
                                   t_range=[-4.9, 4.9], stroke_color=EARTH, stroke_width=2.5, stroke_opacity=0.7))
    t = ValueTracker(0.0)

    def ripples():
      g = VGroup()
      for lag in (0.0, 0.33, 0.66):
        s = t.get_value() - lag
        if 0 < s <= 1.0001:
          g.add(Ellipse(width=9.2 * s, height=3.9 * s, stroke_color=CRYSTAL, stroke_width=5,
                        stroke_opacity=1 - 0.6 * s).move_to(c))
      return g

    rip = always_redraw(ripples)
    with self.say('s01_tap') as d:
      self.play(FadeIn(block), Create(grain), run_time=0.14 * d)
      tap = Dot(c, radius=0.13, color=HL)
      self.play(FadeIn(tap, scale=2), Flash(c, color=HL, line_length=0.35, flash_radius=0.3), run_time=0.07 * d)
      self.add(rip)
      self.play(t.animate.set_value(1.66), run_time=0.36 * d, rate_func=linear)
      self.remove(rip)
      final = Ellipse(width=9.2, height=3.9, stroke_color=CRYSTAL, stroke_width=5).move_to(c)
      self.add(final)
      fast = DoubleArrow(c + LEFT * 4.5, c + RIGHT * 4.5, color=HL, buff=0, stroke_width=5,
                         max_tip_length_to_length_ratio=0.04)
      slow = DoubleArrow(c + DOWN * 1.9, c + UP * 1.9, color=HL, buff=0, stroke_width=5,
                         max_tip_length_to_length_ratio=0.1)
      cap = caption(r'faster along the grain, slower across it', 0.75)
      self.play(GrowFromCenter(fast), GrowFromCenter(slow), FadeIn(cap), run_time=0.15 * d)

    # Arrows as long as the real crystal's fastest speed in a slice through it.
    sl = D['slice']
    fastv = np.array(sl['speeds'][2])
    ang = np.array(sl['angles'])
    scale = 2.45 / fastv.max()
    arrows = VGroup()
    for k in range(0, 240, 10):
      tip = c + scale * fastv[k] * np.array([np.cos(ang[k]), np.sin(ang[k]), 0])
      arrows.add(Arrow(c, tip, buff=0, color=CRYSTAL, stroke_width=4, max_tip_length_to_length_ratio=0.12))
    with self.say('s01_question') as d:
      self.play(FadeOut(VGroup(grain, final, fast, slow, cap)), run_time=0.12 * d)
      self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.06), run_time=0.4 * d)
      q = caption(r'Speeds in every direction $\;\longrightarrow\;$ what is the material?', 0.8)
      self.play(Write(q), run_time=0.2 * d)
    self.wait(0.6)


class Springs(NarratedScene):
  def construct(self):
    wall_x = -4.4

    def wall(y):
      g = VGroup(Line([wall_x, y - 0.7, 0], [wall_x, y + 0.7, 0], stroke_width=5, color=MUTED))
      for k in range(6):
        yy = y - 0.62 + k * 0.25
        g.add(Line([wall_x, yy, 0], [wall_x - 0.28, yy - 0.22, 0], stroke_width=2, color=MUTED))
      return g

    ys, widths, names = [1.5, -0.9], [7, 2.2], ['stiff', 'soft']
    sq = ValueTracker(0.0)
    rest = 1.8

    def system(y, w):
      bx = rest - sq.get_value()
      return VGroup(spring([wall_x, y, 0], [bx - 0.28, y, 0], coils=7, amp=0.22, width=w), ball([bx, y, 0], 0.28))

    systems = [always_redraw(lambda y=y, w=w: system(y, w)) for y, w in zip(ys, widths)]
    labels = VGroup(*[T(n, 0.8).move_to([-1.3, y + 0.8, 0]) for n, y in zip(names, ys)])
    with self.say('s02_spring') as d:
      self.play(FadeIn(wall(ys[0])), FadeIn(wall(ys[1])), *[FadeIn(s) for s in systems], FadeIn(labels),
                run_time=0.15 * d)
      pushes = VGroup(*[Arrow([rest + 1.9, y, 0], [rest + 0.32, y, 0], buff=0, color=INK, stroke_width=5) for y in ys])
      self.play(GrowArrow(pushes[0]), GrowArrow(pushes[1]), run_time=0.1 * d)
      self.play(sq.animate.set_value(0.9), pushes.animate.shift(LEFT * 0.9), run_time=0.15 * d)
      self.play(FadeOut(pushes), run_time=0.05 * d)
      bx = rest - 0.9
      backs = VGroup(Arrow([bx + 0.3, ys[0], 0], [bx + 3.6, ys[0], 0], buff=0, color=HL, stroke_width=7),
                     Arrow([bx + 0.3, ys[1], 0], [bx + 1.3, ys[1], 0], buff=0, color=HL, stroke_width=7))
      self.play(GrowArrow(backs[0]), GrowArrow(backs[1]), run_time=0.15 * d)
      cap = caption(r'stiffness $=$ push-back for each bit of squash', 0.75)
      self.play(FadeIn(cap), run_time=0.1 * d)

    # A chain of balls carrying a squash.
    n, y0 = 13, 0.5
    s = ValueTracker(-2.0)

    def chain(y, svalue, width=3.0, amp=0.38, wd=1.0, x0=-6.0, sp=1.0, count=13, r=0.2):
      xs = [x0 + i * sp + amp * np.exp(-((i - svalue) / wd) ** 2) for i in range(count)]
      g = VGroup()
      for i in range(count - 1):
        g.add(spring([xs[i] + r, y, 0], [xs[i + 1] - r, y, 0], coils=4, amp=0.12, width=width, lead=0.05))
      for i in range(count):
        k = np.exp(-((i - svalue) / wd) ** 2)
        g.add(ball([xs[i], y, 0], r, interpolate_color(ManimColor(INK), ManimColor(HL), k)))
      return g

    ch = always_redraw(lambda: chain(y0, s.get_value()))
    with self.say('s02_chain') as d:
      self.play(FadeOut(everything(self)), run_time=0.12 * d)
      self.play(FadeIn(ch), run_time=0.1 * d)
      push = Arrow([-7.0, y0, 0], [-6.25, y0, 0], buff=0, color=HL, stroke_width=6)
      self.play(GrowArrow(push), run_time=0.08 * d)
      self.play(s.animate.set_value(14.0), FadeOut(push), run_time=0.5 * d, rate_func=linear)
      cap = caption(r'a travelling squash: a sound wave', 0.75)
      self.play(FadeIn(cap), run_time=0.1 * d)

    t = ValueTracker(-1.5)
    top = always_redraw(lambda: chain(1.9, 2 * t.get_value(), width=6, x0=-5.0, count=11))
    bot = always_redraw(lambda: chain(0.3, t.get_value(), width=2, x0=-5.0, count=11))
    lt = T(r'stiff springs: fast', 0.65).move_to([-3.6, 2.75, 0])
    lb = T(r'soft springs: slow', 0.65).move_to([-3.6, 1.15, 0])
    formula = MathTex(r'\text{speed}^2', '=', r'{\text{stiffness} \over \text{density}}').scale(1.0).move_to(DOWN * 1.9)
    with self.say('s02_ratio') as d:
      self.remove(ch)
      self.play(FadeOut(cap), FadeIn(top), FadeIn(bot), FadeIn(lt), FadeIn(lb), run_time=0.1 * d)
      self.play(t.animate.set_value(6.0), run_time=0.3 * d, rate_func=linear)
      self.play(Write(formula), run_time=0.2 * d)
      self.play(Indicate(formula[2], color=HL, scale_factor=1.08), run_time=0.12 * d)
      note = caption(r'waves only reveal this ratio', 0.7, MUTED)
      self.play(FadeIn(note), run_time=0.08 * d)
    self.wait(0.4)


class Waves(NarratedScene):
  def construct(self):
    ys = [2.4, 0.5, -1.4]
    names = [r'push--pull', r'shake: up--down', r'shake: in--out']
    xs = np.linspace(-1.6, 5.6, 10)
    ts = [ValueTracker(0.0) for _ in range(3)]
    k = 1.5
    omegas = [4.2, 2.6, 2.2]

    def row(i):
      tt = ts[i].get_value()
      g = VGroup()
      for x in xs:
        ph = np.sin(k * x - omegas[i] * tt)
        if i == 0:
          g.add(ball([x + 0.24 * ph, ys[i], 0], 0.17))
        elif i == 1:
          g.add(ball([x, ys[i] + 0.33 * ph, 0], 0.17))
        else:
          g.add(ball([x, ys[i], 0], 0.17 * (1 + 0.5 * ph), INK, 0.55 + 0.45 * ph))
      return g

    rows = [always_redraw(lambda i=i: row(i)) for i in range(3)]
    labs = VGroup(*[T(n, 0.68).move_to([-4.4, y, 0]) for n, y in zip(names, ys)])
    with self.say('s03_three') as d:
      self.play(*[FadeIn(r) for r in rows], run_time=0.1 * d)
      for i in range(3):
        self.play(FadeIn(labs[i]), run_time=0.05 * d)
        self.play(ts[i].animate.set_value(ts[i].get_value() + 3.0), run_time=0.18 * d, rate_func=linear)
      cap = caption(r'one direction: three speeds', 0.75)
      self.play(FadeIn(cap), *[tr.animate.set_value(tr.get_value() + 2.0) for tr in ts], run_time=0.2 * d,
                rate_func=linear)

    # A spring grid that is stiff left-right and soft up-down.
    gx, gy = range(-3, 4), range(-2, 3)
    grid = VGroup()
    for j in gy:
      for i in gx:
        if i < 3:
          grid.add(spring([i + 0.12, j, 0], [i + 0.88, j, 0], coils=3, amp=0.08, width=5, lead=0.04))
        if j < 2:
          grid.add(spring([i, j + 0.12, 0], [i, j + 0.88, 0], coils=3, amp=0.08, width=1.5, lead=0.04,
                          color=MUTED))
    balls = VGroup(*[ball([i, j, 0], 0.11) for i in gx for j in gy])
    grid_all = VGroup(grid, balls).shift(DOWN * 0.1)
    legend = T(r'thick springs: stiff \qquad thin springs: soft', 0.65).to_edge(UP, buff=0.4)
    px, py = ValueTracker(-3.3), ValueTracker(-2.4)
    vfront = always_redraw(lambda: Line([px.get_value(), -2.5, 0], [px.get_value(), 2.3, 0], color=CRYSTAL,
                                        stroke_width=7))
    hfront = always_redraw(lambda: Line([-3.4, py.get_value(), 0], [3.4, py.get_value(), 0], color=CRYSTAL,
                                        stroke_width=7))
    with self.say('s03_grain') as d:
      self.play(FadeOut(VGroup(*rows, labs, cap)), run_time=0.06 * d)
      self.play(FadeIn(grid_all), FadeIn(legend), run_time=0.1 * d)
      self.add(vfront, hfront)
      self.play(px.animate.set_value(3.3), py.animate.set_value(-0.1), run_time=0.17 * d, rate_func=linear)
      self.play(FadeOut(vfront), FadeOut(hfront), grid_all.animate.set_opacity(0.15), FadeOut(legend),
                run_time=0.06 * d)
      a, b = 3.0, 1.5
      cen = DOWN * 0.1
      arrows = VGroup()
      for th in np.linspace(0, TAU, 32, endpoint=False):
        r = np.sqrt((a * np.cos(th)) ** 2 + (b * np.sin(th)) ** 2)
        arrows.add(Arrow(cen, cen + r * np.array([np.cos(th), np.sin(th), 0]), buff=0, color=CRYSTAL, stroke_width=3,
                         max_tip_length_to_length_ratio=0.1))
      self.play(LaggedStart(*[GrowArrow(x) for x in arrows], lag_ratio=0.05), run_time=0.22 * d)
      curve = ParametricFunction(lambda th: cen + np.sqrt((a * np.cos(th)) ** 2 + (b * np.sin(th)) ** 2)
                                 * np.array([np.cos(th), np.sin(th), 0]), t_range=[0, TAU], color=HL, stroke_width=6)
      self.play(Create(curve), run_time=0.12 * d)
      cap2 = caption(r'anisotropy: speed depends on direction', 0.75)
      self.play(FadeIn(cap2), run_time=0.08 * d)
    self.wait(0.4)


class SpeedSurface(NarratedScene):
  """The fastest wave's speed surface, projected and shaded by hand (much faster than the 3D camera)."""

  def construct(self):
    nu, nv, sc = 22, 44, 1.5
    th, ph = np.linspace(0, PI, nu + 1), np.linspace(0, TAU, nv + 1)
    P = np.zeros((nu + 1, nv + 1, 3))
    for i, t in enumerate(th):
      for j, f in enumerate(ph):
        n = np.array([np.sin(t) * np.cos(f), np.sin(t) * np.sin(f), np.cos(t)])
        P[i, j] = sc * fast_speed(n) * n
    quads = np.array([[P[i, j], P[i + 1, j], P[i + 1, j + 1], P[i, j + 1]] for i in range(nu) for j in range(nv)])
    light = np.array([-0.5, -0.8, 0.75])
    light /= np.linalg.norm(light)
    dark, base = ManimColor('#0b1d27'), ManimColor(BLUE_B)
    centre = UP * 0.05
    yaw = ValueTracker(-0.9)
    tilt = 0.42
    grow = ValueTracker(0.0)

    def rot(a):
      ca, sa, ct, st = np.cos(a), np.sin(a), np.cos(tilt), np.sin(tilt)
      rz = np.array([[ca, -sa, 0], [sa, ca, 0], [0, 0, 1]])
      rx = np.array([[1, 0, 0], [0, ct, -st], [0, st, ct]])
      return rx @ rz

    def mesh():
      Q = quads @ rot(yaw.get_value()).T * max(grow.get_value(), 1e-3)
      cen = Q.mean(axis=1)
      nrm = np.cross(Q[:, 2] - Q[:, 0], Q[:, 3] - Q[:, 1])
      ln = np.linalg.norm(nrm, axis=1)
      ok = ln > 1e-9
      nrm[ok] /= ln[ok][:, None]
      nrm *= np.sign((nrm * cen).sum(axis=1) + 1e-12)[:, None]
      g = VGroup()
      for k in np.argsort(-cen[:, 1]):
        if not ok[k] or nrm[k, 1] > 0.05:
          continue
        shade = 0.22 + 0.78 * max(0.0, float(nrm[k] @ light))
        pts = [centre + np.array([q[0], q[2], 0]) for q in Q[k]]
        col = interpolate_color(dark, base, shade)
        g.add(VMobject(fill_color=col, fill_opacity=1, stroke_color=interpolate_color(col, ManimColor(INK), 0.25),
                       stroke_width=0.6).set_points_as_corners(pts + [pts[0]]))
      return g

    surf = always_redraw(mesh)
    top = T(r'our crystal: no symmetry at all', 0.75).to_edge(UP, buff=0.4)
    cap = caption(r'fastest wave: an arrow tip for every direction', 0.72)
    with self.say('s03_surface') as d:
      self.add(surf)
      self.play(FadeIn(cap), grow.animate.set_value(1.0), yaw.animate.increment_value(0.12 * d * 0.25),
                run_time=0.12 * d)
      self.play(yaw.animate.increment_value(0.25 * 0.88 * d), FadeIn(top, run_time=0.1 * d), run_time=0.88 * d,
                rate_func=linear)
    self.play(yaw.animate.increment_value(0.25 * 0.8), run_time=0.8, rate_func=linear)


class Slice(NarratedScene):
  def construct(self):
    sl = D['slice']
    ang = np.array(sl['angles'])
    sp = np.array(sl['speeds'])
    cen = LEFT * 1.8 + DOWN * 0.1
    scale = 3.25 / sp.max()
    cols = [BLUE_D, BLUE_A, CRYSTAL]
    names = [r'shake (slowest)', r'shake', r'push--pull (fastest)']
    curves = [polar_curve(sp[k], ang, scale, cen, cols[k], 5 if k == 2 else 4) for k in range(3)]
    centre = Dot(cen, radius=0.06, color=MUTED)
    legend = VGroup()
    for k in (2, 1, 0):
      legend.add(VGroup(Line(ORIGIN, RIGHT * 0.6, color=cols[k], stroke_width=6), T(names[k], 0.62)).arrange(RIGHT,
                                                                                                         buff=0.25))
    legend.arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([4.6, 0.9, 0])
    title = T(r'a slice through all three surfaces', 0.75).to_edge(UP, buff=0.35)
    with self.say('s03_slice') as d:
      self.play(FadeIn(title), FadeIn(centre), run_time=0.08 * d)
      for k in (2, 1, 0):
        self.play(Create(curves[k]), FadeIn(legend[2 - k]), run_time=0.15 * d)
      sw = M(r'\text{slowness} = {1 \over \text{speed}}', 0.85).move_to([4.6, -1.6, 0])
      self.play(Write(sw), run_time=0.2 * d)
    self.wait(0.4)


class TwentyOne(NarratedScene):
  def construct(self):
    mats = [np.diag([1.45, 1, 1]), np.diag([1, 1.7, 1]), np.diag([1, 1, 1.45]),
            np.array([[1, 0, 0], [0, 1, 0.55], [0, 0, 1.0]]), np.array([[1, 0, 0.45], [0, 1, 0], [0, 0, 1.0]]),
            np.array([[1, 0, 0], [0.55, 1, 0], [0, 0, 1.0]])]
    slots = [np.array([-5.6 + 2.24 * i, 0.9, 0]) for i in range(6)]
    rest = [cube_icon(np.eye(3)).move_to(p) for p in slots]
    deformed = [cube_icon(F).move_to(p) for F, p in zip(mats, slots)]
    nums = VGroup(*[M(str(i + 1), 0.7, MUTED).move_to(slots[i] + DOWN * 1.25) for i in range(6)])
    b1 = Brace(VGroup(nums[0], nums[2]), DOWN, color=MUTED)
    b2 = Brace(VGroup(nums[3], nums[5]), DOWN, color=MUTED)
    l1 = T('stretch', 0.7).next_to(b1, DOWN, buff=0.15)
    l2 = T('skew', 0.7).next_to(b2, DOWN, buff=0.15)
    with self.say('s04_modes') as d:
      self.play(LaggedStart(*[FadeIn(c) for c in rest], lag_ratio=0.1), FadeIn(nums), run_time=0.2 * d)
      for i in range(6):
        tgt = deformed[i].copy()
        tgt[0].set_stroke(HL)
        tgt[1].set_stroke(HL)
        tgt[2].set_stroke(HL)
        anims = [Transform(rest[i], tgt)]
        if i == 0:
          anims += [GrowFromCenter(b1), FadeIn(l1)]
        if i == 3:
          anims += [GrowFromCenter(b2), FadeIn(l2)]
        self.play(*anims, run_time=0.1 * d)
        self.play(rest[i].animate.set_stroke(INK), run_time=0.02 * d)

    A = D['A']
    cell = 0.82
    tab, rc, re = value_table(A, CRYSTAL, cell=cell, scale=0.55)
    tab.move_to([-2.4, -0.45, 0])
    chead = VGroup(*[M(str(j + 1), 0.6, MUTED).next_to(rc[0][j], UP, buff=0.15) for j in range(6)])
    rhead = VGroup(*[M(str(i + 1), 0.6, MUTED).next_to(rc[i][0], LEFT, buff=0.18) for i in range(6)])
    ctitle = T(r'push back in way', 0.62, MUTED).next_to(chead, UP, buff=0.15)
    rtitle = T(r'deform in way', 0.62, MUTED).rotate(PI / 2).next_to(rhead, LEFT, buff=0.15)
    with self.say('s04_table') as d:
      self.play(FadeOut(VGroup(*rest, nums, b1, b2, l1, l2)), run_time=0.08 * d)
      self.play(Create(tab[0]), FadeIn(chead), FadeIn(rhead), FadeIn(ctitle), FadeIn(rtitle), run_time=0.1 * d)
      self.play(LaggedStart(*[FadeIn(e) for e in tab[1]], lag_ratio=0.02), run_time=0.18 * d)
      diag = VGroup(*[rc[i][i].copy().set_stroke(HL, 4).set_fill(HL, 0.16) for i in range(6)])
      self.add_foreground_mobjects(tab[1])
      self.play(FadeIn(diag), run_time=0.07 * d)
      lower = VGroup(*[re[i][j] for i in range(6) for j in range(i)])
      pairs = [(1, 0), (2, 0), (3, 1), (4, 2), (5, 3)]
      self.play(*[Indicate(VGroup(re[i][j], re[j][i]), color=HL, scale_factor=1.15) for i, j in pairs],
                run_time=0.08 * d)
      self.play(lower.animate.set_opacity(0.22), run_time=0.06 * d)
      counts = VGroup()
      for i in range(6):
        cnt = M(str(6 - i), 0.7, HL).next_to(rc[i][5], RIGHT, buff=0.3)
        counts.add(cnt)
        self.play(Indicate(VGroup(*re[i][i:]), color=HL, scale_factor=1.1), FadeIn(cnt), run_time=0.035 * d)
      total = M(r'6+5+4+3+2+1 = 21', 0.85).move_to([3.9, 0.6, 0])
      self.play(Write(total), run_time=0.1 * d)
      big = T(r'21 unknowns', 1.0, CRYSTAL).move_to([3.9, -0.6, 0])
      self.play(FadeIn(big, scale=1.2), run_time=0.07 * d)
    self.wait(0.4)


class Summaries(NarratedScene):
  def construct(self):
    up = D['up']
    arrow = Arrow([-5.7, -1.4, 0], [-5.7, 1.6, 0], buff=0, color=HL, stroke_width=7)
    alab = T('straight up', 0.62).next_to(arrow, DOWN, buff=0.2)
    ys = [1.2, 0.3, -0.6]
    h1 = T('speeds', 0.62, MUTED).move_to([-3.6, 2.2, 0])
    h2 = T('squared', 0.62, MUTED).move_to([-0.8, 2.2, 0])
    h3 = T('three summaries', 0.62, MUTED).move_to([3.9, 2.2, 0])
    sp = VGroup(*[M(f'{v:.2f}', 0.9, CRYSTAL).move_to([-3.6, y, 0]) for v, y in zip(up['speeds'], ys)])
    names = 'abc'
    sq = VGroup(*[M(f'{names[i]} = {up["squares"][i]:.3f}', 0.9, CRYSTAL).move_to([-0.8, ys[i], 0]) for i in range(3)])
    sm = VGroup(M(r'a+b+c = 6.1', 0.9), M(r'ab+ac+bc \approx 11.8', 0.9), M(r'abc \approx 7.1', 0.9))
    for m, y in zip(sm, ys):
      m.move_to([3.9, y, 0])
    arr1 = Arrow([-2.85, 0.3, 0], [-2.15, 0.3, 0], buff=0, color=MUTED, stroke_width=4)
    arr2 = Arrow([0.75, 0.3, 0], [1.45, 0.3, 0], buff=0, color=MUTED, stroke_width=4)
    with self.say('s05_speeds') as d:
      self.play(GrowArrow(arrow), FadeIn(alab), run_time=0.12 * d)
      self.play(FadeIn(h1), LaggedStart(*[FadeIn(x) for x in sp], lag_ratio=0.3), run_time=0.3 * d)
      self.play(GrowArrow(arr1), FadeIn(h2), LaggedStart(*[FadeIn(x) for x in sq], lag_ratio=0.2), run_time=0.15 * d)
      self.play(GrowArrow(arr2), FadeIn(h3), run_time=0.06 * d)
      for x in sm:
        self.play(Write(x), run_time=0.09 * d)

    toy = M(r'?+? = 5, \quad ? \times ? = 6 \;\;\Longrightarrow\;\; 2 \text{ and } 3', 0.85)
    toyc = card(toy, color=MUTED).move_to(DOWN * 2.45)
    with self.say('s05_toy') as d:
      self.play(Indicate(VGroup(sq, sm), color=HL, scale_factor=1.04), run_time=0.25 * d)
      self.play(FadeIn(toyc), run_time=0.25 * d)

    parts = [r'\text{sum}', '=', '7.1', 'x^2', '+', '6.3', 'y^2', '+', '6.1', 'z^2', '-', '2.4', 'xy', '-', '1.1',
             'xz', '+', '0.7', 'yz']
    f = MathTex(*parts).scale(0.95).move_to(UP * 0.7)
    coef = [2, 5, 8, 11, 14, 17]
    dirlab = M(r'\text{direction} = (x, y, z)', 0.8).move_to(UP * 2.4)
    with self.say('s05_formula') as d:
      self.play(FadeOut(VGroup(arrow, alab, h1, h2, h3, sp, sq, sm[1], sm[2], arr1, arr2, toyc)),
                sm[0].animate.move_to([4.9, 3.35, 0]).set_color(MUTED), run_time=0.08 * d)
      self.play(FadeIn(dirlab), run_time=0.08 * d)
      self.play(Write(f), run_time=0.18 * d)
      br = Brace(VGroup(f[2], f[18]), DOWN, color=HL)
      six = T(r'six numbers fix it', 0.7, HL).next_to(br, DOWN, buff=0.15)
      self.play(*[f[i].animate.set_color(HL) for i in coef], GrowFromCenter(br), FadeIn(six), run_time=0.14 * d)
      put = M(r'\text{straight up: } x = 0,\; y = 0,\; z = 1', 0.8).move_to(DOWN * 1.6)
      self.play(FadeOut(br), FadeOut(six), FadeIn(put), run_time=0.1 * d)
      gone = [2, 3, 4, 5, 6, 7, 10, 11, 12, 13, 14, 15, 16, 17, 18]
      self.play(*[f[i].animate.set_opacity(0.18) for i in gone], run_time=0.1 * d)
      res = MathTex(r'\text{sum}', '=', '6.1', r'\times 1^2', '=', '6.1').scale(0.95).move_to(DOWN * 2.7)
      res[5].set_color(GOOD)
      self.play(TransformFromCopy(VGroup(f[0], f[1], f[8], f[9]), res[:4]), run_time=0.12 * d)
      tick = check().next_to(res, RIGHT, buff=0.3)
      self.play(Write(res[4:]), FadeIn(tick), sm[0].animate.set_color(GOOD), run_time=0.1 * d)

    tris = [dot_triangle(n) for n in (3, 5, 7)]
    xs = [-4.5, 0.0, 4.5]
    for tr, x in zip(tris, xs):
      tr.move_to([x, 0, 0]).align_to(np.array([0, -0.5, 0]), DOWN)
    labs = [T(s, 0.7) for s in (r'sum: 6', r'pairs: 15', r'product: 28')]
    for lb, tr in zip(labs, tris):
      lb.next_to(tr, DOWN, buff=0.35)
    eq = M(r'6 + 15 + 28 = 49', 0.95).move_to(DOWN * 2.3)
    note = T(r'all set by the 21 stiffness numbers', 0.68, MUTED).move_to(DOWN * 3.2)
    with self.say('s05_count') as d:
      self.play(FadeOut(VGroup(f, dirlab, put, res, tick, sm[0])), run_time=0.08 * d)
      self.play(FadeIn(tris[0]), FadeIn(labs[0]), run_time=0.1 * d)
      self.play(LaggedStart(*[FadeIn(x) for x in tris[1]], lag_ratio=0.03), FadeIn(labs[1]), run_time=0.2 * d)
      self.play(LaggedStart(*[FadeIn(x) for x in tris[2]], lag_ratio=0.02), FadeIn(labs[2]), run_time=0.22 * d)
      self.play(Write(eq), run_time=0.15 * d)
      self.play(FadeIn(note), run_time=0.1 * d)
    self.wait(0.4)


class Twins(NarratedScene):
  def construct(self):
    top = M(r'49 \text{ measurements} \;>\; 21 \text{ unknowns}', 0.85).move_to(UP * 2.5)
    q = M('?', 1.1, HL).next_to(top, RIGHT, buff=0.3)
    eq = M(r'x^2 = 4', 1.4).move_to(UP * 0.5)
    a1 = M(r'x = 2', 1.1, CRYSTAL).move_to([-2.3, -1.3, 0])
    a2 = M(r'x = -2', 1.1, TWIN).move_to([2.3, -1.3, 0])
    ar1 = Arrow(eq.get_bottom() + LEFT * 0.3, a1.get_top(), buff=0.15, color=MUTED, stroke_width=4)
    ar2 = Arrow(eq.get_bottom() + RIGHT * 0.3, a2.get_top(), buff=0.15, color=MUTED, stroke_width=4)
    cap = caption(r'one equation, one unknown, two answers', 0.72)
    with self.say('s06_counting') as d:
      self.play(Write(top), run_time=0.15 * d)
      self.play(FadeIn(q, scale=1.5), run_time=0.15 * d)
      self.play(Write(eq), run_time=0.2 * d)
      self.play(GrowArrow(ar1), FadeIn(a1), run_time=0.12 * d)
      self.play(GrowArrow(ar2), FadeIn(a2), FadeIn(cap), run_time=0.12 * d)

    tw = D['twins']
    cell = 0.74
    t1, rc1, re1 = value_table(tw['T1'], CRYSTAL, cell=cell, scale=0.62, dp=0, zero_dim=True)
    t2, rc2, re2 = value_table(tw['T2'], TWIN, cell=cell, scale=0.62, dp=0, zero_dim=True)
    t1.move_to([-3.4, -0.2, 0])
    t2.move_to([3.4, -0.2, 0])
    h1 = T('material 1', 0.75, CRYSTAL).next_to(t1, UP, buff=0.3)
    h2 = T('material 2', 0.75, TWIN).next_to(t2, UP, buff=0.3)
    diff = [(0, 1), (1, 0), (0, 2), (2, 0)]
    with self.say('s06_twins') as d:
      self.play(FadeOut(VGroup(top, q, eq, a1, a2, ar1, ar2, cap)), run_time=0.08 * d)
      self.play(FadeIn(t1), FadeIn(t2), FadeIn(h1), FadeIn(h2), run_time=0.15 * d)
      boxes = VGroup(*[SurroundingRectangle(rc[i][j], color=HL, buff=0.0, stroke_width=5) for rc in (rc1, rc2)
                       for i, j in diff])
      self.play(Create(boxes), run_time=0.12 * d)
      self.play(FadeOut(VGroup(t1, t2, boxes)), h1.animate.move_to([4.9, 1.6, 0]), h2.animate.move_to([4.9, 0.5, 0]),
                run_time=0.1 * d)
      ang = np.array(D['slice']['angles'])
      sp = np.array(tw['slice_speeds'])
      scale = 2.75 / sp.max()
      cen = LEFT * 1.2 + UP * 0.1
      blue = VGroup(*[polar_curve(sp[k], ang, scale, cen, CRYSTAL, 6) for k in range(3)])
      gold = VGroup(*[polar_curve(sp[k], ang, scale, cen, TWIN, 3.5, dashed=True) for k in range(3)])
      l1 = Line(ORIGIN, RIGHT * 0.6, color=CRYSTAL, stroke_width=6).next_to(h1, LEFT, buff=0.25)
      l2 = DashedLine(ORIGIN, RIGHT * 0.6, color=TWIN, stroke_width=4).next_to(h2, LEFT, buff=0.25)
      self.play(Create(blue), FadeIn(l1), run_time=0.2 * d)
      self.play(Create(gold), FadeIn(l2), run_time=0.2 * d)
      cap2 = caption(r'identical speeds in every direction', 0.72)
      note = T(r'illustration: two box-symmetric tables', 0.58, MUTED).to_corner(UL, buff=0.45)
      self.play(FadeIn(cap2), FadeIn(note), run_time=0.08 * d)

    card_ = statement('Conjecture E', r'A typical three-dimensional material, with no special symmetry, is pinned '
                      r'down by its wave speeds.', width=10.5, color=CRYSTAL).move_to(UP * 0.9)
    who = T(r"de Hoop, Ilmavirta, Lassas and V\'arilly-Alvarado", 0.68, MUTED).next_to(card_, UP, buff=0.4)
    d2 = T(r'2D: proved', 0.8, GOOD).move_to([-2.4, -1.8, 0])
    d3 = T(r'3D: conjectured', 0.8, HL).move_to([2.4, -1.8, 0])
    with self.say('s06_conjecture') as d:
      self.play(FadeOut(VGroup(blue, gold, l1, l2, h1, h2, cap2, note)), run_time=0.08 * d)
      self.play(FadeIn(who), run_time=0.12 * d)
      self.play(FadeIn(d2), run_time=0.15 * d)
      self.play(FadeIn(d3), run_time=0.1 * d)
      self.play(FadeIn(card_), run_time=0.2 * d)
    self.wait(0.4)


class Result(NarratedScene):
  def construct(self):
    head = VGroup(T(r'Conjecture E:', 0.95), T(r'proved', 0.95, GOOD)).arrange(RIGHT, buff=0.25).move_to(UP * 2.7)
    sub = T(r'a typical material has no twin', 0.75).next_to(head, DOWN, buff=0.3)
    u = 0.38
    blocks = VGroup(Rectangle(width=6 * u, height=1.0, fill_color=CRYSTAL, fill_opacity=0.55, stroke_color=CRYSTAL),
                    Rectangle(width=15 * u, height=1.0, fill_color=CRYSTAL, fill_opacity=0.35, stroke_color=CRYSTAL),
                    Rectangle(width=1 * u, height=1.0, fill_color=HL, fill_opacity=0.8, stroke_color=HL))
    blocks.arrange(RIGHT, buff=0.22)
    eq22 = M(r'= 22', 1.0, GOOD)
    row = VGroup(blocks, eq22).arrange(RIGHT, buff=0.4).move_to(DOWN * 0.3)
    nums = VGroup(M('6', 0.8).move_to(blocks[0]), M('15', 0.8).move_to(blocks[1]))
    one = M('1', 0.8, HL).next_to(blocks[2], UP, buff=0.2)
    labs = VGroup(T(r'sum formula', 0.62).next_to(blocks[0], DOWN, buff=0.25),
                  T(r'pair formula', 0.62).next_to(blocks[1], DOWN, buff=0.25),
                  T(r'one product', 0.62, HL).next_to(blocks[2], DOWN, buff=0.25))
    labs[2].shift(RIGHT * 0.35)
    with self.say('s07_result') as d:
      self.play(Write(head), run_time=0.15 * d)
      self.play(FadeIn(sub), run_time=0.15 * d)
      self.wait(0.05 * d)
      self.play(FadeIn(blocks[0]), FadeIn(nums[0]), FadeIn(labs[0]), run_time=0.15 * d)
      self.play(FadeIn(blocks[1]), FadeIn(nums[1]), FadeIn(labs[1]), run_time=0.15 * d)
      self.play(FadeIn(blocks[2]), FadeIn(one), FadeIn(labs[2]), run_time=0.12 * d)
      self.play(Write(eq22), run_time=0.1 * d)

    sheet, curve = sheet_with_curve(4.6, DOWN * 0.15)
    lab = T(r'all materials', 0.7).next_to(sheet, UP, buff=0.25)
    cl = T(r'might have twins', 0.62, BAD).next_to(sheet, RIGHT, buff=0.3).align_to(curve.get_end(), UP)
    dl = VGroup(T(r'sheet: 2 dials', 0.62), T(r'curve: 1 dial', 0.62, BAD)).arrange(DOWN, aligned_edge=RIGHT, buff=0.3)
    dl.next_to(sheet, LEFT, buff=0.4)
    rng = np.random.default_rng(7)
    cpts = np.array([curve.point_from_proportion(a) for a in np.linspace(0, 1, 300)])
    darts = VGroup()
    while len(darts) < 14:
      p = sheet.get_center() + np.array([*rng.uniform(-2.0, 2.0, size=2), 0])
      if np.min(np.linalg.norm(cpts - p, axis=1)) > 0.35:
        darts.add(Dot(p, radius=0.09, color=GOOD))
    with self.say('s07_dart') as d:
      self.play(FadeOut(VGroup(head, sub, blocks, nums, one, labs, eq22)), run_time=0.08 * d)
      self.play(FadeIn(sheet), FadeIn(lab), run_time=0.1 * d)
      self.play(Create(curve), FadeIn(cl), run_time=0.15 * d)
      self.play(FadeIn(dl), run_time=0.1 * d)
      self.play(LaggedStart(*[FadeIn(x, scale=2.5) for x in darts], lag_ratio=0.2), run_time=0.35 * d)
      cap = caption(r'a dart misses the curve with probability one', 0.7, GOOD)
      self.play(FadeIn(cap), run_time=0.08 * d)
    self.wait(0.4)


class Split(NarratedScene):
  def construct(self):
    pA, pB = np.array([-4.8, 1.8, 0]), np.array([-1.6, -1.2, 0])
    pM = (pA + pB) / 2
    dA, dB, dM = Dot(pA, 0.13, color=CRYSTAL), Dot(pB, 0.13, color=TWIN), Dot(pM, 0.11, color=INK)
    lA = M('A', 0.9, CRYSTAL).next_to(dA, UL, buff=0.12)
    lB = M('B', 0.9, TWIN).next_to(dB, DR, buff=0.12)
    lM = M('M', 0.9).next_to(dM, DL, buff=0.15)
    vD = Arrow(pM, pA, buff=0.12, color=GAP, stroke_width=6)
    vN = Arrow(pM, pB, buff=0.12, color=GAP, stroke_width=6)
    lD = M('D', 0.85, GAP).next_to(vD.get_center(), UR, buff=0.12)
    lN = M('-D', 0.85, GAP).next_to(vN.get_center(), UR, buff=0.12)
    e1 = MathTex('A', '=', 'M', '+', 'D').scale(0.95)
    e2 = MathTex('B', '=', 'M', '-', 'D').scale(0.95)
    for e, c in ((e1, CRYSTAL), (e2, TWIN)):
      e[0].set_color(c)
      e[4].set_color(GAP)
    eqs = VGroup(e1, e2).arrange(RIGHT, buff=0.9).move_to([2.6, 2.7, 0])

    def counter(label, value, color):
      return VGroup(M(label, 0.9, color), Integer(value).scale(0.9).set_color(color), T('dials', 0.75, color)).arrange(
        RIGHT, buff=0.25)

    cM = counter('M:', 21, CRYSTAL).move_to([1.9, 1.3, 0])
    cD = counter('D:', 21, GAP).move_to([1.9, 0.35, 0])
    cD.align_to(cM, LEFT)
    with self.say('s08_split') as d:
      self.play(FadeIn(dA), FadeIn(lA), FadeIn(dB), FadeIn(lB), run_time=0.15 * d)
      self.play(FadeIn(dM), FadeIn(lM), run_time=0.1 * d)
      self.play(GrowArrow(vD), FadeIn(lD), GrowArrow(vN), FadeIn(lN), run_time=0.15 * d)
      self.play(Write(eqs), run_time=0.22 * d)
      self.play(FadeIn(cM), FadeIn(cD), run_time=0.15 * d)

    def test_cap(s):
      return T(s, 0.75).move_to(DOWN * 2.9)

    def set_count(cnt, v, color):
      new = Integer(v).scale(0.9).set_color(HL).move_to(cnt[1])
      self.play(Transform(cnt[1], new), Flash(cnt[1], color=HL, flash_radius=0.4), run_time=0.15 * self._d)
      self.play(cnt[1].animate.set_color(color), run_time=0.05 * self._d)

    with self.say('s08_test1') as d:
      self._d = d
      t1 = test_cap(r'Test 1: the sum formulas match')
      self.play(FadeIn(t1), run_time=0.15 * d)
      set_count(cD, 15, GAP)

    with self.say('s08_test2') as d:
      self._d = d
      t2 = test_cap(r'Test 2: the pair formulas match')
      self.play(FadeOut(t1), FadeIn(t2), run_time=0.1 * d)
      neq = T(r'15 equations for $M$', 0.68, MUTED).next_to(cM, RIGHT, buff=0.45)
      self.play(FadeIn(neq), run_time=0.12 * d)
      self.wait(0.2 * d)
      set_count(cM, 6, CRYSTAL)
      tot = MathTex('15', '+', '6', '=', '21').scale(1.0).move_to([2.4, -1.1, 0])
      tot[0].set_color(GAP)
      tot[2].set_color(CRYSTAL)
      self.play(Write(tot), run_time=0.15 * d)

    with self.say('s08_test3') as d:
      t3 = test_cap(r'Test 3: one product matches')
      self.play(FadeOut(t2), FadeIn(t3), run_time=0.12 * d)
      tot2 = MathTex('21', '-', '1', '=', '20', '?').scale(1.0).move_to(tot)
      tot2[5].set_color(HL)
      self.play(TransformMatchingTex(tot, tot2), run_time=0.2 * d)
      self.play(Indicate(tot2[5], color=HL, scale_factor=1.4), run_time=0.15 * d)

    # The paper's exact witness: M = 0 and an isotropic D.
    w = D['witness']
    head = T(r'$M = 0$, and $D$ treats every direction the same', 0.75).to_edge(UP, buff=0.45)
    rows_y = [1.6, 0.55, -0.45, -1.45]
    rlab = VGroup(*[T(s, 0.7, MUTED).move_to([-4.3, y, 0]) for s, y in
                    zip((r'straight up', r'sum', r'pairs', r'product'), rows_y)])
    cD_h = M('D', 0.95, GAP).move_to([-0.6, 2.4, 0])
    cN_h = M('-D', 0.95, TWIN).move_to([2.6, 2.4, 0])

    def nums(v):
      return ',\\;'.join(str(int(x)) for x in v)

    colD = VGroup(M(nums(w['D']), 0.85, GAP), *[M(str(int(x)), 0.85, GAP) for x in w['D_summaries']])
    colN = VGroup(M(nums(w['minusD']), 0.85, TWIN), *[M(str(int(x)), 0.85, TWIN) for x in w['minusD_summaries']])
    for m, y in zip(colD, rows_y):
      m.move_to([-0.6, y, 0])
    for m, y in zip(colN, rows_y):
      m.move_to([2.6, y, 0])
    marks = VGroup(check().move_to([4.6, rows_y[1], 0]), check().move_to([4.6, rows_y[2], 0]),
                   cross_mark().move_to([4.6, rows_y[3], 0]))
    foot = T(r'not real materials, but the proof covers every table', 0.6, MUTED).move_to(DOWN * 2.55)
    with self.say('s08_witness') as d:
      self.play(FadeOut(everything(self)), run_time=0.07 * d)
      self.play(FadeIn(head), run_time=0.1 * d)
      self.play(FadeIn(rlab[0]), FadeIn(cD_h), FadeIn(colD[0]), run_time=0.12 * d)
      self.play(FadeIn(cN_h), FadeIn(colN[0]), run_time=0.12 * d)
      self.play(FadeIn(rlab[1]), FadeIn(colD[1]), FadeIn(colN[1]), FadeIn(marks[0]), run_time=0.08 * d)
      self.play(FadeIn(rlab[2]), FadeIn(colD[2]), FadeIn(colN[2]), FadeIn(marks[1]), run_time=0.08 * d)
      self.play(FadeIn(rlab[3]), FadeIn(colD[3]), FadeIn(colN[3]), run_time=0.1 * d)
      self.play(FadeIn(marks[2], scale=1.5), Indicate(VGroup(colD[3], colN[3]), color=BAD), run_time=0.1 * d)
      res = M(r'21 - 1 = 20 \text{ dials}', 0.85, GOOD).move_to(DOWN * 3.35)
      self.play(FadeIn(foot), Write(res), run_time=0.12 * d)
    self.wait(0.4)


class Balance(NarratedScene):
  def construct(self):
    e1 = M(r'x + y = 2', 0.95).move_to([-3.2, 2.7, 0])
    e2 = M(r'2x + 2y = 4', 0.95).move_to([-3.2, 1.85, 0])
    br = Brace(VGroup(e1, e2), RIGHT, color=MUTED)
    bl = T(r'really one equation', 0.68).next_to(br, RIGHT, buff=0.2)
    strips = VGroup(*[Rectangle(width=3.0, height=0.14, fill_color=INK, fill_opacity=0.9, stroke_width=0)
                      for _ in range(15)]).arrange(DOWN, buff=0.1).move_to([-3.5, -1.2, 0])
    slab = T(r'15 equations for $M$', 0.65, MUTED).next_to(strips, UP, buff=0.25)
    r_genuine = 9
    gb = Brace(strips[:r_genuine], RIGHT, color=HL)
    gl = T(r'$r$ genuinely different', 0.65, HL).next_to(gb, RIGHT, buff=0.15)
    keeps = M(r'M \text{ keeps } 21 - r \text{ dials}', 0.9, CRYSTAL).move_to([3.4, -2.4, 0])
    with self.say('s09_repeat') as d:
      self.play(Write(e1), run_time=0.12 * d)
      self.play(Write(e2), run_time=0.12 * d)
      self.play(GrowFromCenter(br), FadeIn(bl), e2.animate.set_color(DIM), run_time=0.12 * d)
      self.play(FadeIn(strips), FadeIn(slab), run_time=0.12 * d)
      self.play(*[s.animate.set_fill(DIM, 0.5) for s in strips[r_genuine:]], run_time=0.12 * d)
      self.play(GrowFromCenter(gb), FadeIn(gl), run_time=0.12 * d)
      self.play(Write(keeps), run_time=0.15 * d)

    lm = M(r'M: \;\; 21 - r \text{ dials}', 1.0, CRYSTAL).move_to(UP * 1.4)
    ld = M(r'D: \;\; \text{at most } r - 1 \text{ dials}', 1.0, GAP).move_to(UP * 0.2)
    ld.align_to(lm, LEFT)
    hard = T(r'the hard part, proved in the paper', 0.62, HL).next_to(ld, DOWN, buff=0.3).align_to(ld, LEFT)
    with self.say('s09_balance') as d:
      self.play(FadeOut(VGroup(e1, e2, br, bl, strips, slab, gb, gl)), ReplacementTransform(keeps, lm),
                run_time=0.2 * d)
      self.play(Write(ld), run_time=0.25 * d)
      self.play(FadeIn(hard), run_time=0.15 * d)
      arr_up = Arrow(lm.get_right() + RIGHT * 0.3 + DOWN * 0.25, lm.get_right() + RIGHT * 0.3 + UP * 0.35, buff=0,
                     color=CRYSTAL, stroke_width=6)
      arr_dn = Arrow(ld.get_right() + RIGHT * 0.3 + UP * 0.35, ld.get_right() + RIGHT * 0.3 + DOWN * 0.25, buff=0,
                     color=GAP, stroke_width=6)
      self.play(GrowArrow(arr_up), GrowArrow(arr_dn), run_time=0.15 * d)

    s1 = MathTex('(', 'r', '-', '1', ')', '+', '(', '21', '-', 'r', ')').scale(1.2).move_to(DOWN * 1.6)
    s1[1:4].set_color(GAP)
    s1[7:10].set_color(CRYSTAL)
    s2 = MathTex('r', '-', '1', '+', '21', '-', 'r').scale(1.2).move_to(DOWN * 1.6)
    with self.say('s09_cancel') as d:
      self.play(FadeOut(hard), Write(s1), run_time=0.25 * d)
      self.play(TransformMatchingTex(s1, s2), run_time=0.2 * d)
      self.play(s2[0].animate.set_color(HL), s2[6].animate.set_color(HL), run_time=0.1 * d)
      strikes = VGroup(Line(s2[0].get_corner(DL), s2[0].get_corner(UR), color=BAD, stroke_width=5),
                       Line(s2[5].get_corner(DL), s2[6].get_corner(UR), color=BAD, stroke_width=5))
      self.play(Create(strikes), run_time=0.12 * d)
      res = M(r'= 20', 1.2, GOOD).next_to(s2, RIGHT, buff=0.35)
      self.play(Write(res), run_time=0.15 * d)

    ax = Axes(x_range=[4.5, 15.5, 1], y_range=[0, 22, 5], x_length=10.4, y_length=5.0, tips=False,
              axis_config={'color': MUTED, 'stroke_width': 2, 'font_size': 30},
              x_axis_config={'numbers_to_include': list(range(5, 16))},
              y_axis_config={'numbers_to_include': [0, 5, 10, 15, 20]}).move_to([0.4, -0.2, 0])
    xl = T(r'genuinely different equations $r$', 0.62, MUTED).next_to(ax.x_axis, DOWN, buff=0.55)
    yl = T(r'dials', 0.62, MUTED).next_to(ax.y_axis, UP, buff=0.15)
    line21 = DashedLine(ax.c2p(4.5, 21), ax.c2p(15.5, 21), color=INK, stroke_width=3)
    l21 = T(r'all materials: 21', 0.62).next_to(ax.c2p(9.5, 21), UP, buff=0.12)
    leg = VGroup(VGroup(Square(0.3, fill_color=GAP, fill_opacity=0.85, stroke_width=0), T(r'$D$', 0.65, GAP)).arrange(
      RIGHT, buff=0.15), VGroup(Square(0.3, fill_color=CRYSTAL, fill_opacity=0.85, stroke_width=0),
                                T(r'$M$', 0.65, CRYSTAL)).arrange(RIGHT, buff=0.15)).arrange(RIGHT, buff=0.5)
    leg.next_to(line21, UP, buff=0.12).align_to(line21, RIGHT)
    xu = ax.x_axis.unit_size
    yu = ax.y_axis.unit_size

    def bar(x, y0, h, color):
      return Rectangle(width=0.62 * xu, height=max(h * yu, 1e-3), fill_color=color, fill_opacity=0.85,
                       stroke_width=0).move_to(ax.c2p(x, y0 + h / 2))

    rows = D['strata']
    with self.say('s09_bars') as d:
      self.play(FadeOut(VGroup(lm, ld, arr_up, arr_dn, s2, strikes, res)), run_time=0.06 * d)
      self.play(Create(ax), FadeIn(xl), FadeIn(yl), Create(line21), FadeIn(l21), FadeIn(leg), run_time=0.14 * d)
      r15 = [x for x in rows if x['r'] == 15][0]
      bD = bar(15, 0, r15['D'], GAP)
      bM = bar(15, r15['D'], r15['M'], CRYSTAL)
      self.play(GrowFromEdge(bD, DOWN), run_time=0.06 * d)
      self.play(GrowFromEdge(bM, DOWN), run_time=0.06 * d)
      cap1 = bar(15, 20, 1, HL)
      t3 = T(r'test 3', 0.58, HL).next_to(cap1, RIGHT, buff=0.12)
      self.play(FadeIn(cap1), FadeIn(t3), run_time=0.06 * d)
      bM2 = bar(15, r15['D'], r15['M'] - 1, CRYSTAL)
      self.play(FadeOut(cap1, shift=DOWN * 0.3), Transform(bM, bM2), run_time=0.07 * d)
      self.play(FadeOut(t3), run_time=0.03 * d)
      others = []
      for x in sorted(rows, key=lambda q: -q['r']):
        if x['r'] == 15:
          continue
        others.append((bar(x['r'], 0, x['D'], GAP), bar(x['r'], x['D'], x['M'], CRYSTAL)))
      self.play(LaggedStart(*[AnimationGroup(GrowFromEdge(a, DOWN), GrowFromEdge(b, DOWN)) for a, b in others],
                            lag_ratio=0.35), run_time=0.3 * d)
      x5 = cross_mark(scale=0.9).move_to(ax.c2p(5, 1.3))
      n5 = T(r'\shortstack{only\\$D = 0$}', 0.58, BAD).next_to(x5, UP, buff=0.15)
      self.play(FadeIn(x5), FadeIn(n5), run_time=0.08 * d)
      self.play(Indicate(line21, color=HL), run_time=0.08 * d)

    big = M(r'20 \;<\; 21', 1.5).move_to([-2.6, 0.5, 0])
    sheet, curve = sheet_with_curve(3.4, np.array([3.2, 0.4, 0]))
    cap = caption(r'a typical material has no twin', 0.8, GOOD)
    with self.say('s09_conclude') as d:
      chart = VGroup(ax, xl, yl, line21, l21, leg, bD, bM, x5, n5, *[m for pair in others for m in pair])
      self.play(FadeOut(chart), run_time=0.12 * d)
      self.play(Write(big), run_time=0.2 * d)
      self.play(FadeIn(sheet), Create(curve), run_time=0.25 * d)
      self.play(FadeIn(cap), run_time=0.15 * d)
    self.wait(0.4)


class Computer(NarratedScene):
  def construct(self):
    region = RoundedRectangle(width=8.4, height=5.0, corner_radius=0.3, stroke_color=MUTED, stroke_width=2,
                              fill_color=PANEL, fill_opacity=1).move_to([-1.9, 0.25, 0])
    rlab = T(r'all half-gaps $D$', 0.65, MUTED).next_to(region.get_corner(UL), DR, buff=0.25)
    P6, P11, P15 = np.array([-4.3, -0.9, 0]), np.array([-1.3, 1.1, 0]), np.array([1.0, -1.1, 0])
    pts = VGroup(Dot(P6, 0.13, color=BAD), Dot(P11, 0.13, color=BAD))
    plabs = VGroup(M('6', 0.75, BAD).next_to(P6, DOWN, buff=0.62), M('11', 0.75, BAD).next_to(P11, UP, buff=0.62))
    fam = VGroup()
    for through, offs in ((P6, [(-0.9, 1.1), (1.0, 0.9), (0.8, -0.5)]), (P11, [(-1.1, -0.7), (1.2, 0.4)])):
      for ox, oy in offs:
        a = through + np.array([ox, oy, 0])
        b = through - np.array([ox * 0.8, oy * 0.6 - 0.3, 0])
        fam.add(VMobject(stroke_color=BAD, stroke_width=3, stroke_opacity=0.75).set_points_smoothly(
          [a, (a + through) / 2 + np.array([0.2, -0.15, 0]), through, (b + through) / 2 + np.array([-0.15, 0.2, 0]), b]))
    side = VGroup(T(r'rotation symmetry', 0.68), T(r'$\Rightarrow$ two special tables', 0.68)).arrange(
      DOWN, aligned_edge=LEFT, buff=0.25).move_to([4.7, 1.4, 0])
    with self.say('s10_points') as d:
      self.play(FadeIn(region), FadeIn(rlab), run_time=0.08 * d)
      self.play(Create(fam), run_time=0.15 * d)
      self.play(FadeIn(side), run_time=0.08 * d)
      self.play(LaggedStart(*[FadeIn(p, scale=2) for p in pts], lag_ratio=0.3), FadeIn(plabs), run_time=0.17 * d)
      self.play(Indicate(fam, color=HL), run_time=0.12 * d)
      lens = VGroup(Circle(0.5, color=HL, stroke_width=5).move_to(P6), Circle(0.5, color=HL, stroke_width=5).move_to(P11))
      look = T(r'look closely here', 0.68, HL).move_to([4.7, -0.2, 0])
      self.play(Create(lens), FadeIn(look), run_time=0.12 * d)
      sl = Line([1.55, 2.45, 0], [2.0, -1.95, 0], color=HL, stroke_width=4)
      sll = T(r'plus a few flat slices', 0.68, HL).move_to([4.7, -1.1, 0])
      self.play(Create(sl), FadeIn(sll), run_time=0.12 * d)

    cc = np.array([-3.6, 0.1, 0])
    R = 1.9
    dial = VGroup(Circle(R, color=MUTED, stroke_width=3).move_to(cc))
    for k in range(24):
      a = TAU * k / 24
      u = np.array([np.sin(a), np.cos(a), 0])
      dial.add(Line(cc + u * (R - 0.18), cc + u * R, color=MUTED, stroke_width=2))
    zero = M('0', 0.7).move_to(cc + UP * (R + 0.35))
    hours = T(r'a clock with 32003 hours', 0.65).next_to(dial, DOWN, buff=0.45)
    hand = Line(cc, cc + UP * (R - 0.35), color=HL, stroke_width=6)
    hand.rotate(TAU * 0.05, about_point=cc)
    seven = Dot(cc + (R - 0.35) * np.array([np.sin(TAU * 0.06), np.cos(TAU * 0.06), 0]), 0.08, color=GOOD)
    top = T(r'exact whole numbers, no rounding', 0.75).to_edge(UP, buff=0.45)
    s1 = M(r'32000 + 10 = 32010', 0.9).move_to([2.9, 0.9, 0])
    s2 = M(r'\longrightarrow \; 7 \text{ on the clock}', 0.9, GOOD).next_to(s1, DOWN, buff=0.35).align_to(s1, LEFT)
    cert = VGroup(check(), T(r'certificates: identities anyone can multiply out and check', 0.68)).arrange(
      RIGHT, buff=0.25).move_to(DOWN * 3.0)
    with self.say('s10_exact') as d:
      self.play(FadeOut(everything(self)), run_time=0.07 * d)
      self.play(FadeIn(top), run_time=0.08 * d)
      self.play(Create(dial), FadeIn(zero), FadeIn(hours), FadeIn(hand), run_time=0.12 * d)
      self.play(Write(s1), run_time=0.12 * d)
      self.play(Rotate(hand, angle=-TAU * 0.11, about_point=cc), run_time=0.2 * d)
      self.play(FadeIn(seven), Write(s2), run_time=0.12 * d)
      self.play(FadeIn(cert), run_time=0.12 * d)
    self.wait(0.4)


class Directions(NarratedScene):
  def construct(self):
    xs = [-6.3 + 0.9 * i for i in range(15)]
    y = 2.1
    circles = VGroup(*[Circle(0.34, color=MUTED, stroke_width=3).move_to([x, y, 0]) for x in xs])
    labels = VGroup(*[M(str(i + 1), 0.6).move_to([x, y, 0]) for i, x in enumerate(xs)])
    head = T(r'number of directions measured', 0.65, MUTED).next_to(circles, UP, buff=0.3)
    f = VGroup(*[M(x, 1.15) for x in ('6', '+', '7', '+', '7', '=', '20', '<', '21')]).arrange(RIGHT, buff=0.5)
    f.move_to(UP * 0.2)
    f[6].set_color(BAD)
    under = VGroup(T('sums', 0.6).next_to(f[0], DOWN, buff=0.3), T('pairs', 0.6).next_to(f[2], DOWN, buff=0.3),
                   T('products', 0.6).next_to(f[4], DOWN, buff=0.3), T('unknowns', 0.6).next_to(f[8], DOWN, buff=0.3))
    cap7 = T(r'seven directions: one short', 0.72, BAD).move_to(DOWN * 1.9)
    with self.say('s11_seven') as d:
      self.play(FadeIn(head), Create(circles), FadeIn(labels), run_time=0.15 * d)
      self.play(*[circles[i].animate.set_fill(BAD, 0.4).set_stroke(BAD) for i in range(7)], run_time=0.15 * d)
      self.play(Write(f[0]), FadeIn(under[0]), run_time=0.15 * d)
      self.play(Write(f[1:5]), FadeIn(under[1:3]), run_time=0.15 * d)
      self.play(Write(f[5:]), FadeIn(under[3]), run_time=0.12 * d)
      self.play(FadeIn(cap7), run_time=0.08 * d)

    g = VGroup(*[M(x, 1.1) for x in ('21', '+', r'2 \times 11', '=', '43', '>', '42')]).arrange(RIGHT, buff=0.5)
    g.move_to(UP * 0.2)
    g[4].set_color(GOOD)
    gu = VGroup(T('material', 0.6).next_to(g[0], DOWN, buff=0.3),
                T(r'11 directions', 0.6).next_to(g[2], DOWN, buff=0.3),
                T(r'all twin cases', 0.6).next_to(g[6], DOWN, buff=0.3))
    each = T(r'each direction: 2 dials', 0.58, MUTED).next_to(gu[1], DOWN, buff=0.2)
    nodes = D['nodes']
    tri = VGroup(*[Dot([a * 0.45, b * 0.45, 0], 0.09, color=GOOD) for a, b in nodes]).move_to([-1.8, -2.35, 0])
    tl = T(r'15 specific directions also work', 0.65, GOOD).next_to(tri, RIGHT, buff=0.6)
    with self.say('s11_eleven') as d:
      self.play(FadeOut(VGroup(f, under, cap7)), run_time=0.08 * d)
      self.play(circles[10].animate.set_fill(GOOD, 0.55).set_stroke(GOOD),
                *[circles[i].animate.set_fill(GOOD, 0.25).set_stroke(GOOD) for i in range(11, 15)], run_time=0.12 * d)
      self.play(Write(g[:3]), FadeIn(gu[:2]), FadeIn(each), run_time=0.2 * d)
      self.play(Write(g[3:]), FadeIn(gu[2]), run_time=0.2 * d)
      self.play(LaggedStart(*[FadeIn(x, scale=2) for x in tri], lag_ratio=0.08), FadeIn(tl), run_time=0.25 * d)

    qs = VGroup(*[M('?', 0.9, HL).next_to(circles[i], DOWN, buff=0.2) for i in (7, 8, 9)])
    with self.say('s11_open') as d:
      self.play(*[circles[i].animate.set_fill(MUTED, 0.35).set_stroke(INK) for i in (7, 8, 9)],
                LaggedStart(*[FadeIn(q, shift=UP * 0.2) for q in qs], lag_ratio=0.3), run_time=0.4 * d)
      self.play(Indicate(VGroup(circles[7:10], labels[7:10]), color=HL), run_time=0.3 * d)
    self.wait(0.4)


class Status(NarratedScene):
  def construct(self):
    head = T(r'Proved', 1.0, GOOD).to_edge(UP, buff=0.6)

    def line(mark, text):
      return VGroup(mark, T(text, 0.75)).arrange(RIGHT, buff=0.3)

    p1 = VGroup(line(check(), r'a typical material has no twin'),
                line(check(), r'computer-assisted: written proof plus exact certificates')).arrange(
      DOWN, aligned_edge=LEFT, buff=0.55).move_to(UP * 0.4)
    p2 = VGroup(line(check(), r'Lean checked eleven key identities, not the whole argument'),
                line(M(r'\circ', 0.9, MUTED), r'reviewed internally, not yet by outside referees')).arrange(
      DOWN, aligned_edge=LEFT, buff=0.55).move_to(DOWN * 1.9)
    with self.say('s12_proved') as d:
      self.play(FadeIn(head), run_time=0.08 * d)
      self.play(FadeIn(p1[0]), run_time=0.12 * d)
      self.play(FadeIn(p1[1]), run_time=0.15 * d)
      self.wait(0.12 * d)
      self.play(p1.animate.set_opacity(0.35), FadeIn(p2[0]), run_time=0.15 * d)
      self.play(FadeIn(p2[1]), run_time=0.15 * d)

    head2 = T(r'Not claimed', 1.0, BAD).to_edge(UP, buff=0.6)
    sub = M(r'\text{unique} \;\neq\; \text{stable}', 1.0).next_to(head2, DOWN, buff=0.45)
    n = D['noise']
    scale = 7.0 / 0.5
    y1, y2 = 0.1, -0.9
    lab1 = T(r'noise in the speeds', 0.65).move_to([-3.6, y1, 0])
    lab2 = T(r'error of the best 22-number fit', 0.65).move_to([-3.6, y2, 0])
    x0 = -0.9
    bar1 = Rectangle(width=max(n['noise'] * scale, 0.06), height=0.45, fill_color=MUTED, fill_opacity=1,
                     stroke_width=0)
    bar1.move_to([x0, y1, 0], aligned_edge=LEFT)
    bar2 = Rectangle(width=n['compressed_error'] * scale, height=0.45, fill_color=BAD, fill_opacity=0.9, stroke_width=0)
    bar2.move_to([x0, y2, 0], aligned_edge=LEFT)
    v1 = M(r'0.1\%', 0.75).next_to(bar1, RIGHT, buff=0.25)
    v2 = M(r'45\%', 0.75, BAD).next_to(bar2, RIGHT, buff=0.25)
    one = T(r'one simulated test material', 0.6, MUTED).move_to(DOWN * 1.9)
    q1 = T(r'symmetric materials can still have twins', 0.72).move_to(DOWN * 2.6)
    q2 = T(r'density is never separated from stiffness', 0.72).move_to(DOWN * 3.3)
    with self.say('s12_not') as d:
      self.play(FadeOut(VGroup(head, p1, p2)), FadeIn(head2), run_time=0.08 * d)
      self.play(Write(sub), run_time=0.1 * d)
      self.play(FadeIn(lab1), GrowFromEdge(bar1, LEFT), FadeIn(v1), run_time=0.12 * d)
      self.play(FadeIn(lab2), GrowFromEdge(bar2, LEFT), FadeIn(v2), run_time=0.18 * d)
      self.play(FadeIn(one), run_time=0.08 * d)
      self.wait(0.1 * d)
      self.play(FadeOut(one), FadeIn(q1), run_time=0.1 * d)
      self.play(FadeIn(q2), run_time=0.1 * d)
    self.wait(0.4)


class Recap(NarratedScene):
  def construct(self):
    head = T(r'Recap', 1.0).to_edge(UP, buff=0.6)
    pts = VGroup(
      T(r'1.~ 21 unknowns: counting alone cannot rule out twins', 0.75),
      T(r'2.~ all twin pairs fill at most 20 of the 21 dials', 0.75),
      T(r'3.~ 22 numbers, or 11 random directions, suffice; 7 do not', 0.75),
    ).arrange(DOWN, aligned_edge=LEFT, buff=0.6).move_to(DOWN * 0.2)
    with self.say('s13_recap') as d:
      self.play(FadeIn(head), run_time=0.08 * d)
      self.play(FadeIn(pts[0], shift=RIGHT * 0.2), run_time=0.12 * d)
      self.wait(0.18 * d)
      self.play(FadeIn(pts[1], shift=RIGHT * 0.2), run_time=0.12 * d)
      self.wait(0.2 * d)
      self.play(FadeIn(pts[2], shift=RIGHT * 0.2), run_time=0.12 * d)

    head2 = T(r'Still unknown', 1.0, HL).to_edge(UP, buff=0.6)
    qs = VGroup(T(r'are 8, 9 or 10 directions enough?', 0.75),
                T(r'exactly which special materials have twins?', 0.75),
                T(r'how to recover stiffness reliably from noisy data?', 0.75)).arrange(
      DOWN, aligned_edge=LEFT, buff=0.55).move_to(DOWN * 0.2)
    with self.say('s13_open') as d:
      self.play(FadeOut(VGroup(head, pts)), FadeIn(head2), run_time=0.1 * d)
      for q in qs:
        self.play(FadeIn(q, shift=RIGHT * 0.2), run_time=0.15 * d)
        self.wait(0.1 * d)

    t1 = T(r'Generic Recovery of Three-Dimensional Elasticity', 0.9)
    t2 = T(r'from the Slowness Polynomial', 0.9)
    who = T(r'Valyu Research, 2026', 0.72, MUTED)
    path = T(r'\texttt{physics/mechanics/elasticity/generic-stiffness-recovery}', 0.55, MUTED)
    voice = T(r'Narration uses a synthetic voice.', 0.5, MUTED)
    end = VGroup(t1, t2, who, path, voice).arrange(DOWN, buff=0.35)
    who.shift(DOWN * 0.2)
    path.shift(DOWN * 0.2)
    voice.shift(DOWN * 0.5)
    self.play(FadeOut(VGroup(head2, qs)), run_time=0.6)
    self.play(FadeIn(end), run_time=1.0)
    self.wait(6.0)
