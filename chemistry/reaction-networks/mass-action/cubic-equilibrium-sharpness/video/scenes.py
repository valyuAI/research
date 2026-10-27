"""Explainer: how many ways can a chemical soup come to rest?

Finding: for every n >= 2 an n-species, n-reaction mass action network with one conservation law reaches
the maximum of n clean (nondegenerate) resting states on one slice, using inputs of at most three molecules;
three is the least possible. Running example n = 2 (2X+Y -> X, 2Y -> X+3Y); scaled example n = 3 and the
n = 4 polynomial. Numbers: ../verification/cubic-sharpness-certificate.json, reproduced by check_numbers.py.
"""

import numpy as np
from manim import *
from vrvideo import *

SCENES = ['Hook', 'MassAction', 'Tank', 'TwoSpecies', 'Plane', 'Question', 'PairFails', 'ThreeSpecies',
          'Slice3', 'Descartes', 'Recipe', 'Honest', 'Evidence', 'Ending']

X_COL, Y_COL, Z_COL = PRIMARY, WARM, EXTRA
SPC = {'X': X_COL, 'Y': Y_COL, 'Z': Z_COL}
CURVE = INK          # balance curves (where rates balance)
SLICE = MUTED        # slices (fixed conserved quantity), always dashed
REST = ACCENT        # resting states / success
MOVE = SECONDARY     # the mixture point and whatever is changing


def T(s, scale=0.75, color=INK):
  return Tex(s, color=color).scale(scale)


def species_color(part):
  found = [k for k in 'XYZ' if k in part]
  return SPC[found[0]] if len(found) == 1 else INK


def MT(*parts, scale=0.85, colors=None):
  """MathTex whose parts are coloured by the single species letter they contain (else white)."""
  m = MathTex(*parts).scale(scale)
  for i, sub in enumerate(m):
    col = (colors or {}).get(i, species_color(parts[i]))
    sub.set_color(col)
  return m


def mol(k, r=0.28):
  c = Circle(radius=r, stroke_width=0, fill_color=SPC[k], fill_opacity=1)
  lab = MathTex(k, color=BACKGROUND).scale(max(0.55, 2.1 * r)).move_to(c)
  return VGroup(c, lab)


def cluster(kinds, r=0.28, gap=0.05):
  return VGroup(*[mol(k, r) for k in kinds]).arrange(RIGHT, buff=gap)


def bounce(m, dt):
  p = m.get_center() + m.vel * dt
  for i in (0, 1):
    if p[i] < m.lo[i]:
      p[i] = 2 * m.lo[i] - p[i]
      m.vel[i] *= -1
    if p[i] > m.hi[i]:
      p[i] = 2 * m.hi[i] - p[i]
      m.vel[i] *= -1
  m.move_to(p)


def drifting(mobs, lo, hi, seed, speed=(0.5, 0.9)):
  """Give each mobject a random position in the box [lo, hi] and a bouncing updater."""
  rng = np.random.default_rng(seed)
  for m in mobs:
    r = m.width / 2
    m.lo = np.array(lo, dtype=float) + r
    m.hi = np.array(hi, dtype=float) - r
    m.move_to(np.array([rng.uniform(m.lo[0], m.hi[0]), rng.uniform(m.lo[1], m.hi[1]), 0]))
    a = rng.uniform(0, TAU)
    m.vel = rng.uniform(*speed) * np.array([np.cos(a), np.sin(a), 0.0])
    m.add_updater(bounce)
  return mobs


def flask(center, s=1.0):
  pts = [(-0.42, 1.7), (-0.42, 0.55), (-1.6, -1.55), (1.6, -1.55), (0.42, 0.55), (0.42, 1.7)]
  outline = VMobject(stroke_color=INK, stroke_width=4)
  outline.set_points_as_corners([np.array([x, y, 0.0]) for x, y in pts])
  ly = -0.2
  hw = 0.42 + (1.6 - 0.42) * (0.55 - ly) / 2.1
  liquid = Polygon(*[np.array([x, y, 0.0]) for x, y in [(-hw, ly), (-1.57, -1.52), (1.57, -1.52), (hw, ly)]],
                   stroke_width=0, fill_color=SOFT, fill_opacity=0.35)
  g = VGroup(liquid, outline).scale(s, about_point=ORIGIN).shift(center)
  return g


def flask_halfwidth(y):
  """Inner half-width of the flask body at height y (unscaled flask coordinates)."""
  return 0.42 + 1.18 * (0.55 - y) / 2.1 - 0.06


def flask_bounce(m, dt):
  c, s, r = m.flask_center, m.flask_scale, m.radius_local
  u = (m.get_center() - c) / s + m.vel * dt
  y_lo, y_hi = -1.5 + r, -0.25 - r
  if u[1] < y_lo or u[1] > y_hi:
    u[1] = np.clip(u[1], y_lo, y_hi)
    m.vel[1] *= -1
  hw = flask_halfwidth(u[1]) - r
  if abs(u[0]) > hw:
    u[0] = np.sign(u[0]) * hw
    m.vel[0] = -np.sign(u[0]) * abs(m.vel[0])
  m.move_to(c + s * u)


def flask_soup(center, s, kinds, seed):
  rng = np.random.default_rng(seed)
  dots = VGroup()
  for k in kinds:
    dt = Dot(radius=0.11 * s, color=SPC[k])
    dt.flask_center, dt.flask_scale, dt.radius_local = np.array(center, dtype=float), s, 0.11
    y = rng.uniform(-1.38, -0.37)
    hw = flask_halfwidth(y) - 0.11
    dt.move_to(center + s * np.array([rng.uniform(-hw, hw), y, 0]))
    a = rng.uniform(0, TAU)
    dt.vel = rng.uniform(0.3, 0.55) * np.array([np.cos(a), np.sin(a), 0.0])
    dt.add_updater(flask_bounce)
    dots.add(dt)
  return dots


def stop(mobs):
  for m in mobs:
    m.clear_updaters()


def recolor(m, col):
  """Change colour without pausing the mobject's drifting updater."""
  c0 = m.get_color()
  return UpdateFromAlphaFunc(m, lambda mob, a: mob.set_color(interpolate_color(c0, col, a)),
                             suspend_mobject_updating=False)


def check_mark(scale=0.9, color=REST):
  return MathTex(r'\checkmark', color=color).scale(scale)


# ------------------------------------------------------------------ shared pictures

def plane2(center=np.array([-3.0, -0.3, 0])):
  ax = Axes(x_range=[0, 8, 1], y_range=[0, 6, 1], x_length=6.4, y_length=4.8, tips=False,
            axis_config={'color': MUTED, 'stroke_width': 2, 'tick_size': 0.05})
  ax.move_to(center)
  xl = MathTex('X', color=X_COL).scale(0.85).next_to(ax.x_axis.get_end(), RIGHT, buff=0.2)
  yl = MathTex('Y', color=Y_COL).scale(0.85).next_to(ax.y_axis.get_end(), UP, buff=0.18)
  nums = VGroup(*[MathTex(str(v), color=MUTED).scale(0.6).next_to(ax.c2p(v, 0), DOWN, buff=0.15)
                  for v in (2, 4, 6, 8)],
                *[MathTex(str(v), color=MUTED).scale(0.6).next_to(ax.c2p(0, v), LEFT, buff=0.15)
                  for v in (2, 4, 6)])
  return ax, VGroup(xl, yl, nums)


def slice_line(ax, c=2.0, x_max=8.0, y_max=6.0):
  """The slice X - Y = c, clipped to the plot."""
  x_end = min(x_max, y_max + c)
  return DashedLine(ax.c2p(c, 0), ax.c2p(x_end, x_end - c), dash_length=0.16, dashed_ratio=0.55,
                    color=SLICE, stroke_width=5)


def parabola(ax, color=CURVE):
  return ax.plot(lambda x: x * x / 9, x_range=[0, 7.35], color=color, stroke_width=5)


def rest_dot(ax, x, y, color=REST, r=0.11):
  return Dot(ax.c2p(x, y), radius=r, color=color).set_z_index(5)


def Q3(t):
  return 11 * t ** 4 - 60 * t ** 3 + 85 * t ** 2


def qplot(center, x_length=6.2, y_length=4.4):
  ax = Axes(x_range=[0, 3.4, 1], y_range=[0, 90, 10], x_length=x_length, y_length=y_length, tips=False,
            axis_config={'color': MUTED, 'stroke_width': 2, 'tick_size': 0.05})
  ax.move_to(center)
  curve = ax.plot(Q3, x_range=[0, 3.33], color=CURVE, stroke_width=5)
  tl = MathTex('t', color=INK).scale(0.8).next_to(ax.x_axis.get_end(), RIGHT, buff=0.2)
  nums = VGroup(*[MathTex(str(v), color=MUTED).scale(0.6).next_to(ax.c2p(v, 0), DOWN, buff=0.15)
                  for v in (1, 2, 3)])
  return ax, curve, VGroup(tl, nums)


def level_line(ax, k):
  return DashedLine(ax.c2p(0, k), ax.c2p(3.4, k), dash_length=0.16, dashed_ratio=0.55, color=SLICE,
                    stroke_width=5)


def positive_roots(coeffs, lo=0.0, hi=3.4):
  rs = np.roots(coeffs)
  return sorted(r.real for r in rs if abs(r.imag) < 1e-7 and lo < r.real < hi)


def sign_arcs(signs, color=MOVE):
  """Numbered arcs over consecutive sign symbols that differ."""
  arcs, nums, k = VGroup(), VGroup(), 0
  for a, b in zip(signs[:-1], signs[1:]):
    k += 1
    arc = ArcBetweenPoints(a.get_top() + UP * 0.12, b.get_top() + UP * 0.12, angle=-PI / 2.2, color=color,
                           stroke_width=4)
    arcs.add(arc)
    nums.add(MathTex(str(k), color=color).scale(0.65).next_to(arc, UP, buff=0.08))
  return arcs, nums


def reaction_rows(rows, ys, x_in=-3.5, x_out=-1.4, r=0.28, rates=None, rate_scale=0.62):
  """rows: list of (inputs, outputs). Inputs end at x_in, outputs start at x_out."""
  out = []
  for i, ((ins, outs), y) in enumerate(zip(rows, ys)):
    a = cluster(ins, r)
    a.move_to(np.array([x_in - a.width / 2, y, 0]))
    b = cluster(outs, r)
    b.move_to(np.array([x_out + 0.45 + b.width / 2, y, 0]))
    arr = Arrow(np.array([x_in + 0.2, y, 0]), np.array([x_out + 0.15, y, 0]), buff=0, stroke_width=4,
                color=MUTED, max_tip_length_to_length_ratio=0.18)
    lab = None
    if rates:
      lab = MathTex(rates[i], color=INK).scale(rate_scale).next_to(arr, UP, buff=0.1)
    out.append((a, arr, b, lab))
  return out


# ------------------------------------------------------------------ 1 Hook

class Hook(NarratedScene):
  def construct(self):
    with self.say('s01_hook') as d:
      c0 = np.array([0, 0.2, 0])
      f0 = flask(c0, 1.35)
      kinds = list('XYXYXYXYXYXYXYXY')
      soup0 = flask_soup(c0, 1.35, kinds, seed=3)
      self.play(Create(f0[1]), FadeIn(f0[0]), run_time=0.08 * d)
      self.play(FadeIn(soup0), run_time=0.06 * d)
      self.wait(0.08 * d)
      # a few reactions happen, then it settles
      flips = [1, 5, 9]
      self.play(*[recolor(soup0[i], X_COL) for i in flips], run_time=0.06 * d)
      self.wait(0.1 * d)
      stop(soup0)
      self.play(FadeOut(VGroup(f0, soup0)), run_time=0.05 * d)
      # two starts, two different resting mixtures
      cl, cr = np.array([-3.6, 0.4, 0]), np.array([3.6, 0.4, 0])
      fl, fr = flask(cl, 1.0), flask(cr, 1.0)
      sl = flask_soup(cl, 1.0, list('XXYXYXXYXYXY'), seed=7)
      sr = flask_soup(cr, 1.0, list('XYYXYYXYXYYY'), seed=11)
      self.play(FadeIn(fl), FadeIn(fr), FadeIn(sl), FadeIn(sr), run_time=0.07 * d)
      self.wait(0.05 * d)
      self.play(*[recolor(sl[i], X_COL) for i in (2, 4, 7, 9)],
                *[recolor(sr[i], Y_COL) for i in (0, 3, 6, 8)], run_time=0.1 * d)
      la = T('one resting mixture', 0.65, MUTED).next_to(fl, DOWN, buff=0.3)
      lb = T('a different one', 0.65, MUTED).next_to(fr, DOWN, buff=0.3)
      self.play(FadeIn(la), FadeIn(lb), run_time=0.05 * d)
      # a two-position switch between them
      body = RoundedRectangle(width=1.5, height=0.72, corner_radius=0.36, stroke_color=INK, stroke_width=4)
      body.move_to(np.array([0, 0.0, 0]))
      knob = Circle(radius=0.26, stroke_width=0, fill_color=X_COL, fill_opacity=1).move_to(body.get_left() + RIGHT * 0.38)
      self.play(Create(body), FadeIn(knob), run_time=0.06 * d)
      self.play(knob.animate.move_to(body.get_right() + LEFT * 0.38).set_fill(Y_COL), run_time=0.06 * d)
      self.play(knob.animate.move_to(body.get_left() + RIGHT * 0.38).set_fill(X_COL), run_time=0.06 * d)

    with self.say('s01_question') as d:
      stop(sl)
      stop(sr)
      top = VGroup(fl, fr, sl, sr, body, knob)
      self.play(FadeOut(la), FadeOut(lb), top.animate.scale(0.72).move_to(UP * 1.5), run_time=0.12 * d)
      q1 = T(r'How many resting states can a small network have?', 0.85)
      q2 = T(r'How complicated must its reactions be?', 0.85)
      VGroup(q1, q2).arrange(DOWN, buff=0.45).move_to(DOWN * 1.9)
      self.play(Write(q1), run_time=0.25 * d)
      self.wait(0.2 * d)
      self.play(Write(q2), run_time=0.2 * d)


# ------------------------------------------------------------------ 2 Mass action

class MassAction(NarratedScene):
  def construct(self):
    with self.say('s02_rate') as d:
      box = Rectangle(width=7.4, height=4.2, stroke_color=MUTED, stroke_width=2).move_to(UP * 0.2)
      ms = VGroup(*[mol(k, 0.26) for k in 'XYXYXYXY'])
      lo = box.get_corner(DL) + np.array([0.05, 0.05, 0])
      hi = box.get_corner(UR) - np.array([0.05, 0.05, 0])
      drifting(ms, lo, hi, seed=5, speed=(0.6, 1.0))
      self.play(Create(box), FadeIn(ms), run_time=0.08 * d)
      self.wait(0.07 * d)
      x, y = ms[0], ms[1]
      stop([x, y])
      meet = np.array([0.4, 0.2, 0])
      self.play(x.animate.move_to(meet + LEFT * 0.27), y.animate.move_to(meet + RIGHT * 0.27), run_time=0.08 * d)
      self.play(Flash(meet, color=MOVE, line_length=0.3, num_lines=12, flash_radius=0.45), run_time=0.07 * d)
      stop(ms)
      self.play(FadeOut(VGroup(box, ms)), run_time=0.05 * d)
      # counting possible meetings
      xs = VGroup(*[mol('X') for _ in range(3)]).arrange(DOWN, buff=0.55).move_to(np.array([-2.4, 0.5, 0]))
      ys = VGroup(*[mol('Y') for _ in range(2)]).arrange(DOWN, buff=0.85).move_to(np.array([2.4, 0.5, 0]))
      lines = VGroup(*[Line(a.get_center(), b.get_center(), color=MOVE, stroke_width=3, stroke_opacity=0.8)
                       for a in xs for b in ys]).set_z_index(-1)
      count = MT('3', r'\times', '2', '=', '6', scale=1.0, colors={0: X_COL, 2: Y_COL}).move_to(DOWN * 2.6)
      self.play(FadeIn(xs), FadeIn(ys), run_time=0.06 * d)
      self.play(LaggedStart(*[Create(l) for l in lines], lag_ratio=0.15), run_time=0.12 * d)
      self.play(Write(count), run_time=0.06 * d)
      xs2 = VGroup(*[mol('X') for _ in range(3)]).arrange(DOWN, buff=0.55).next_to(xs, LEFT, buff=0.7)
      lines2 = VGroup(*[Line(a.get_center(), b.get_center(), color=MOVE, stroke_width=3, stroke_opacity=0.8)
                        for a in xs2 for b in ys]).set_z_index(-1)
      count2 = MT('6', r'\times', '2', '=', '12', scale=1.0, colors={0: X_COL, 2: Y_COL}).move_to(DOWN * 2.6)
      self.play(FadeIn(xs2, shift=RIGHT * 0.2), run_time=0.06 * d)
      self.play(LaggedStart(*[Create(l) for l in lines2], lag_ratio=0.12),
                TransformMatchingTex(count, count2), run_time=0.12 * d)

    with self.say('s02_massaction') as d:
      self.play(FadeOut(VGroup(xs, xs2, ys, lines, lines2, count2)), run_time=0.08 * d)
      law = MT(r'\text{rate}', '=', 'k', r'\times', 'X', r'\times', 'Y', scale=1.4, colors={2: MOVE})
      law.move_to(UP * 0.3)
      self.play(Write(law), run_time=0.2 * d)
      conc = T(r'$X$, $Y$: how concentrated each chemical is', 0.7, MUTED).move_to(DOWN * 1.5)
      conc[0][0].set_color(X_COL)
      conc[0][2].set_color(Y_COL)
      self.play(FadeIn(conc), run_time=0.1 * d)
      br = Brace(law[2], UP, buff=0.15, color=MOVE)
      brl = T('rate constant', 0.7, MOVE).next_to(br, UP, buff=0.12)
      self.play(GrowFromCenter(br), FadeIn(brl), run_time=0.12 * d)
      head = T('the law of mass action', 0.9).to_edge(UP, buff=0.55)
      self.wait(0.12 * d)
      self.play(FadeIn(head), run_time=0.1 * d)

    with self.say('s02_three') as d:
      self.play(FadeOut(VGroup(conc, br, brl, head)), run_time=0.06 * d)
      left_x, right_x = -3.4, 3.4
      self.play(law.animate.scale(0.62).move_to(np.array([left_x, -0.2, 0])), run_time=0.08 * d)
      # three-body: two X and a Y converge
      meet = np.array([right_x, 1.2, 0])
      tri = [mol('X'), mol('X'), mol('Y')]
      starts = [meet + np.array([-1.6, 0.9, 0]), meet + np.array([-1.5, -0.9, 0]), meet + np.array([1.6, 0.4, 0])]
      ends = [meet + LEFT * 0.58, meet, meet + RIGHT * 0.58]
      for m, p in zip(tri, starts):
        m.move_to(p)
      self.play(*[FadeIn(m) for m in tri], run_time=0.05 * d)
      self.play(*[m.animate.move_to(p) for m, p in zip(tri, ends)], run_time=0.1 * d)
      self.play(Flash(meet, color=MOVE, line_length=0.3, flash_radius=0.75), run_time=0.06 * d)
      r3 = MT(r'\text{rate}', '=', 'k', 'X', 'X', 'Y', scale=0.87, colors={2: MOVE})
      r3.move_to(np.array([right_x, -0.2, 0]))
      self.play(Write(r3), run_time=0.08 * d)
      r3b = MT(r'\text{rate}', '=', 'k', 'X^2', 'Y', scale=0.87, colors={2: MOVE}).move_to(r3)
      self.play(TransformMatchingTex(r3, r3b), run_time=0.08 * d)
      h3 = T('three-body collision', 0.8).move_to(np.array([right_x, 2.75, 0]))
      n3 = T('3 molecules in', 0.65, MUTED).move_to(np.array([right_x, -1.3, 0]))
      self.play(FadeIn(h3), FadeIn(n3), run_time=0.07 * d)
      self.wait(0.08 * d)
      pair = cluster('XY').move_to(np.array([left_x, 1.2, 0]))
      h2 = T('pair collision', 0.8).move_to(np.array([left_x, 2.75, 0]))
      n2 = T('at most 2 molecules in', 0.65, MUTED).move_to(np.array([left_x, -1.3, 0]))
      self.play(FadeIn(pair), FadeIn(h2), FadeIn(n2), run_time=0.08 * d)
      div = DashedLine(UP * 3.2, DOWN * 2.0, color=MUTED, stroke_width=2, dash_length=0.1)
      self.play(Create(div), run_time=0.05 * d)


# ------------------------------------------------------------------ 3 Tank

class Tank(NarratedScene):
  def construct(self):
    L, R, B, TOP = -6.2, -3.4, -2.7, 1.3
    HS = 0.95
    Q_IN = 1.5
    C_OUT = 1.5 / np.sqrt(2.0)
    lev = ValueTracker(0.0)

    def q_out(h):
      return C_OUT * np.sqrt(max(h, 0.0))

    walls = VMobject(stroke_color=INK, stroke_width=4)
    walls.set_points_as_corners([np.array(p) for p in [[L, TOP, 0], [L, B, 0], [R, B, 0], [R, TOP, 0]]])
    pipe = Rectangle(width=2.1, height=0.28, stroke_width=0, fill_color=MUTED, fill_opacity=1)
    pipe.move_to(np.array([-6.1, 2.35, 0]))
    spout = Rectangle(width=0.3, height=0.42, stroke_width=0, fill_color=MUTED, fill_opacity=1)
    spout.move_to(np.array([-5.2, 2.07, 0]))
    drain = Rectangle(width=0.55, height=0.22, stroke_width=0, fill_color=MUTED, fill_opacity=1)
    drain.move_to(np.array([R + 0.27, B + 0.2, 0]))

    def surface():
      return B + lev.get_value() * HS

    water = always_redraw(lambda: Rectangle(width=R - L - 0.07, height=max(1e-3, lev.get_value() * HS),
                                            stroke_width=0, fill_color=SOFT, fill_opacity=0.95)
                          .move_to(np.array([(L + R) / 2, B + max(1e-3, lev.get_value() * HS) / 2, 0])))
    stream = always_redraw(lambda: Rectangle(width=0.14, height=max(1e-3, 1.86 - surface() - 0.0 + 0.0),
                                             stroke_width=0, fill_color=SOFT, fill_opacity=0.95)
                           .move_to(np.array([-5.2, (1.86 + surface()) / 2, 0])))
    outflow = always_redraw(lambda: Rectangle(width=0.03 + 0.09 * q_out(lev.get_value()), height=0.7,
                                              stroke_width=0, fill_color=SOFT, fill_opacity=0.95)
                            .move_to(np.array([R + 0.5, B - 0.25, 0])))
    in_arrow = Arrow(np.array([-6.0, 1.6, 0]), np.array([-6.0, 1.6 - 0.6 * Q_IN, 0]), buff=0, color=SLICE,
                     stroke_width=6, max_tip_length_to_length_ratio=0.3)
    in_lab = T('in', 0.7, SLICE).next_to(in_arrow, LEFT, buff=0.15)
    out_arrow = always_redraw(lambda: Arrow(np.array([R + 0.8, B - 0.55, 0]),
                                            np.array([R + 0.8 + max(0.02, 0.6 * q_out(lev.get_value())), B - 0.55, 0]),
                                            buff=0, color=CURVE, stroke_width=6, max_tip_length_to_length_ratio=0.3))
    out_lab = T('out', 0.7, CURVE).move_to(np.array([R + 1.15, B - 1.05, 0]))

    with self.say('s03_tank') as d:
      self.play(Create(walls), FadeIn(pipe), FadeIn(spout), FadeIn(drain), run_time=0.15 * d)
      self.add(water, stream, outflow)
      self.play(GrowArrow(in_arrow), FadeIn(in_lab), run_time=0.1 * d)
      self.add(out_arrow)
      self.play(FadeIn(out_lab), lev.animate.set_value(0.7), run_time=0.55 * d, rate_func=linear)

    ax = Axes(x_range=[0, 4, 1], y_range=[0, 3, 1], x_length=6.0, y_length=4.2, tips=False,
              axis_config={'color': MUTED, 'stroke_width': 2, 'tick_size': 0.05}).move_to(np.array([3.3, -0.4, 0]))
    xl = T('level', 0.7, MUTED).next_to(ax.x_axis.get_end(), DOWN, buff=0.25).shift(LEFT * 0.3)
    yl = T('flow', 0.7, MUTED).next_to(ax.y_axis.get_end(), UP, buff=0.15)
    tap_line = DashedLine(ax.c2p(0, Q_IN), ax.c2p(4, Q_IN), dash_length=0.16, dashed_ratio=0.55, color=SLICE,
                          stroke_width=5)
    tap_lab = T('in', 0.7, SLICE).next_to(tap_line, RIGHT, buff=0.15)
    drain_curve = ax.plot(lambda h: C_OUT * np.sqrt(h), x_range=[0, 4], color=CURVE, stroke_width=5)
    drain_lab = T('out', 0.7, CURVE).next_to(ax.c2p(4, C_OUT * 2), RIGHT, buff=0.15)

    with self.say('s03_balance') as d:
      self.play(lev.animate.set_value(2.0), run_time=0.55 * d, rate_func=lambda t: 1 - (1 - t) ** 3)
      cap = T(r'resting state: in $=$ out', 0.8, REST).move_to(np.array([-4.4, 3.3, 0]))
      self.play(FadeIn(cap), Indicate(in_arrow, color=REST), run_time=0.15 * d)

    with self.say('s03_cross') as d:
      self.play(Create(ax), FadeIn(xl), FadeIn(yl), run_time=0.1 * d)
      self.play(Create(tap_line), FadeIn(tap_lab), run_time=0.08 * d)
      self.play(Create(drain_curve), FadeIn(drain_lab), run_time=0.1 * d)
      probe = ValueTracker(0.3)
      vline = always_redraw(lambda: DashedLine(ax.c2p(probe.get_value(), 0),
                                               ax.c2p(probe.get_value(), max(Q_IN, C_OUT * np.sqrt(probe.get_value()))),
                                               color=MOVE, stroke_width=3, dash_length=0.08))
      d_in = always_redraw(lambda: Dot(ax.c2p(probe.get_value(), Q_IN), radius=0.08, color=MOVE))
      d_out = always_redraw(lambda: Dot(ax.c2p(probe.get_value(), C_OUT * np.sqrt(probe.get_value())), radius=0.08,
                                        color=MOVE))
      self.play(FadeIn(vline), FadeIn(d_in), FadeIn(d_out), run_time=0.04 * d)
      self.play(probe.animate.set_value(3.6), run_time=0.12 * d)
      self.play(probe.animate.set_value(2.0), run_time=0.1 * d)
      cross = Dot(ax.c2p(2, Q_IN), radius=0.12, color=REST).set_z_index(5)
      self.play(FadeOut(vline), FadeOut(d_in), FadeOut(d_out), FadeIn(cross, scale=1.6), run_time=0.06 * d)
      self.wait(0.12 * d)
      wig = ax.plot(lambda h: Q_IN + 0.5 * (h - 0.8) * (h - 2.0) * (h - 3.2), x_range=[0.3, 3.75], color=CURVE,
                    stroke_width=5)
      for mob in (water, stream, outflow, out_arrow):
        mob.clear_updaters()
      tank = VGroup(walls, pipe, spout, drain, water, stream, outflow, in_arrow, in_lab, out_arrow, out_lab, cap)
      dim = [walls.animate.set_stroke(opacity=0.25)] + [m.animate.set_opacity(0.25) for m in tank[1:]]
      self.play(Transform(drain_curve, wig), FadeOut(drain_lab), *dim, run_time=0.12 * d)
      dots3 = VGroup(*[Dot(ax.c2p(h, Q_IN), radius=0.12, color=REST).set_z_index(5) for h in (0.8, 3.2)])
      self.play(LaggedStart(*[FadeIn(dd, scale=1.6) for dd in dots3], lag_ratio=0.4), run_time=0.08 * d)


# ------------------------------------------------------------------ 4 Two species

class TwoSpecies(NarratedScene):
  def construct(self):
    rows = reaction_rows([('XXY', 'X'), ('YY', 'XYYY')], ys=[2.2, 0.55], x_in=-3.7, x_out=-1.9)
    (a1, ar1, b1, _), (a2, ar2, b2, _) = rows
    net1 = VGroup(MT('-1', 'X', scale=0.85, colors={0: WARN}), MT('-1', 'Y', scale=0.85, colors={0: WARN})).arrange(RIGHT, buff=0.45)
    net1.move_to(np.array([3.0, 2.2, 0]))
    net2 = VGroup(MT('+1', 'X', scale=0.85, colors={0: REST}), MT('+1', 'Y', scale=0.85, colors={0: REST})).arrange(RIGHT, buff=0.45)
    net2.move_to(np.array([3.0, 0.55, 0]))
    rate1 = MT(r'\tfrac{1}{9}', 'X^2', 'Y', scale=0.9).move_to(np.array([5.7, 2.2, 0]))
    rate2 = MT('Y^2', scale=0.9).move_to(np.array([5.7, 0.55, 0]))
    h_net = T('overall', 0.65, MUTED).move_to(np.array([3.0, 3.2, 0]))
    h_rate = T('rate', 0.65, MUTED).move_to(np.array([5.7, 3.2, 0]))

    with self.say('s04_a') as d:
      self.wait(0.2 * d)
      self.play(FadeIn(a1), run_time=0.1 * d)
      self.play(GrowArrow(ar1), run_time=0.08 * d)
      self.play(FadeIn(b1), run_time=0.1 * d)
      self.wait(0.12 * d)
      self.play(FadeIn(h_net), FadeIn(net1, shift=LEFT * 0.2), run_time=0.12 * d)

    with self.say('s04_b') as d:
      self.play(FadeIn(a2), run_time=0.08 * d)
      self.play(GrowArrow(ar2), run_time=0.06 * d)
      self.play(FadeIn(b2), run_time=0.08 * d)
      self.play(FadeIn(net2, shift=LEFT * 0.2), run_time=0.1 * d)
      self.wait(0.12 * d)
      self.play(FadeIn(h_rate), Write(rate1), run_time=0.14 * d)
      self.play(Write(rate2), run_time=0.1 * d)

    with self.say('s04_conserve') as d:
      self.play(Indicate(net1, color=MOVE), Indicate(net2, color=MOVE), run_time=0.1 * d)

      def counters(x, y):
        cx = MT('X', '=', str(x), scale=0.95)
        cy = MT('Y', '=', str(y), scale=0.95)
        cd = MT('X', '-', 'Y', '=', str(x - y), scale=0.95, colors={4: REST})
        cx.move_to(np.array([-4.2, -2.1, 0]))
        cy.move_to(np.array([-1.8, -2.1, 0]))
        cd.move_to(np.array([3.0, -2.1, 0]))
        return cx, cy, cd

      cx, cy, cd = counters(5, 3)
      self.play(FadeIn(cx), FadeIn(cy), run_time=0.07 * d)
      self.play(FadeIn(cd), run_time=0.06 * d)
      hl1 = SurroundingRectangle(VGroup(a1, b1), color=MOVE, buff=0.15, corner_radius=0.1)
      self.play(Create(hl1), run_time=0.06 * d)
      nx, ny, nd = counters(4, 2)
      self.play(Transform(cx, nx), Transform(cy, ny), Transform(cd, nd), run_time=0.08 * d)
      hl2 = SurroundingRectangle(VGroup(a2, b2), color=MOVE, buff=0.15, corner_radius=0.1)
      self.play(ReplacementTransform(hl1, hl2), run_time=0.06 * d)
      mx, my, md = counters(5, 3)
      self.play(Transform(cx, mx), Transform(cy, my), Transform(cd, md), run_time=0.08 * d)
      self.play(FadeOut(hl2), Circumscribe(cd, color=REST, buff=0.15), run_time=0.12 * d)
      law = T('a conservation law', 0.75, REST).next_to(cd, DOWN, buff=0.35)
      self.play(FadeIn(law), run_time=0.08 * d)


# ------------------------------------------------------------------ 5 Plane

class Plane(NarratedScene):
  def construct(self):
    ax, deco = plane2()
    px = 3.9
    with self.say('s05_plane') as d:
      self.play(Create(ax), FadeIn(deco), run_time=0.15 * d)
      pt = Dot(ax.c2p(5, 3), radius=0.12, color=MOVE).set_z_index(6)
      ptl = MT(r'(5,\,3)', scale=0.65, colors={0: MOVE}).next_to(pt, LEFT, buff=0.15)
      self.play(FadeIn(pt, scale=1.5), FadeIn(ptl), run_time=0.08 * d)
      sl = slice_line(ax)
      self.wait(0.12 * d)
      cons = MT('X', '-', 'Y', '=', '2', scale=1.0).move_to(np.array([px, 2.6, 0]))
      self.play(Create(sl), FadeIn(cons), FadeOut(ptl), run_time=0.15 * d)
      self.play(pt.animate.move_to(ax.c2p(4, 2)), run_time=0.1 * d)
      self.play(pt.animate.move_to(ax.c2p(6.8, 4.8)), run_time=0.12 * d)
      self.play(pt.animate.move_to(ax.c2p(5, 3)), run_time=0.08 * d)
      sname = T('the slice', 0.75, SLICE).next_to(cons, DOWN, buff=0.25)
      self.play(FadeIn(sname), run_time=0.08 * d)

    with self.say('s05_balance') as d:
      e1 = MT(r'\tfrac{1}{9}', 'X^2', 'Y', '=', 'Y^2', scale=1.0).move_to(np.array([px, 0.6, 0]))
      self.play(FadeOut(pt), Write(e1), run_time=0.22 * d)
      self.wait(0.08 * d)
      e2 = MT(r'\tfrac{1}{9}', 'X^2', '=', 'Y', scale=1.0).move_to(e1)
      self.play(TransformMatchingTex(e1, e2), run_time=0.14 * d)
      e3 = MT('Y', '=', 'X^2', '/', '9', scale=1.0).move_to(e1)
      self.play(TransformMatchingTex(e2, e3), run_time=0.12 * d)
      par = parabola(ax)
      plab = T('balance curve', 0.7, CURVE).move_to(ax.c2p(5.3, 5.6))
      self.play(Create(par), run_time=0.2 * d)
      self.play(FadeIn(plab), run_time=0.08 * d)

    with self.say('s05_cross') as d:
      self.play(e3.animate.scale(0.75).move_to(np.array([px, 1.2, 0])), FadeOut(sname), run_time=0.08 * d)
      c1 = MT('X^2', '/', '9', '=', 'X', '-', '2', scale=0.95).move_to(np.array([px, 0.0, 0]))
      self.play(Write(c1), run_time=0.15 * d)
      self.wait(0.05 * d)
      c2 = MT('X^2', '-', '9', 'X', '+', '18', '=', '0', scale=0.95).move_to(c1)
      self.play(TransformMatchingTex(c1, c2), run_time=0.12 * d)
      c3 = MT('(X-3)', '(X-6)', '=', '0', scale=0.95).move_to(c1)
      self.play(TransformMatchingTex(c2, c3), run_time=0.12 * d)
      self.wait(0.08 * d)
      r1, r2 = rest_dot(ax, 3, 1), rest_dot(ax, 6, 4)
      l1 = MT(r'(3,\,1)', scale=0.7, colors={0: REST}).next_to(r1, DR, buff=0.08)
      l2 = MT(r'(6,\,4)', scale=0.7, colors={0: REST}).next_to(r2, RIGHT, buff=0.2)
      self.play(FadeIn(r1, scale=1.6), FadeIn(l1), run_time=0.1 * d)
      self.play(FadeIn(r2, scale=1.6), FadeIn(l2), run_time=0.1 * d)
      two = T('two resting states', 0.75, REST).move_to(np.array([px, -1.2, 0]))
      self.play(FadeIn(two), run_time=0.08 * d)

    with self.say('s05_clean') as d:
      self.play(FadeOut(VGroup(c3, two, e3)), run_time=0.06 * d)
      ok = T('clean crossings', 0.75, REST).move_to(np.array([px, 1.6, 0]))
      nd = T('(nondegenerate)', 0.65, MUTED).next_to(ok, DOWN, buff=0.15)
      self.play(FadeIn(ok), Indicate(r1, color=REST, scale_factor=1.6), Indicate(r2, color=REST, scale_factor=1.6),
                run_time=0.12 * d)
      self.play(FadeIn(nd), run_time=0.06 * d)
      # an inset touch
      base = np.array([px, -1.6, 0])
      nudge = ValueTracker(0.0)
      t_line = always_redraw(lambda: DashedLine(base + np.array([-1.6, 0.35 + nudge.get_value(), 0]),
                                                base + np.array([1.6, 0.35 + nudge.get_value(), 0]),
                                                dash_length=0.12, color=SLICE, stroke_width=4))
      t_curve = FunctionGraph(lambda x: 0.35 - 0.9 * x * x, x_range=[-0.85, 0.85], color=WARN, stroke_width=5)
      t_curve.shift(base)
      t_dot = Dot(base + UP * 0.35, radius=0.09, color=WARN)
      t_lab = T('a touch', 0.7, WARN).move_to(base + DOWN * 0.75)
      self.play(Create(t_curve), FadeIn(t_line), FadeIn(t_dot), FadeIn(t_lab), run_time=0.12 * d)
      self.wait(0.06 * d)
      c = ValueTracker(2.0)
      self.remove(sl)
      sl2 = always_redraw(lambda: slice_line(ax, c.get_value()))
      self.add(sl2)

      def roots(cv):
        disc = max(0.0, 81 - 36 * cv)
        return (9 - np.sqrt(disc)) / 2, (9 + np.sqrt(disc)) / 2

      r1.add_updater(lambda m: m.move_to(ax.c2p(roots(c.get_value())[0], roots(c.get_value())[0] - c.get_value())))
      r2.add_updater(lambda m: m.move_to(ax.c2p(roots(c.get_value())[1], roots(c.get_value())[1] - c.get_value())))
      self.play(FadeOut(l1), FadeOut(l2), run_time=0.04 * d)
      self.play(c.animate.set_value(1.6), nudge.animate.set_value(0.3), FadeOut(t_dot), run_time=0.2 * d)
      self.wait(0.08 * d)
      self.play(c.animate.set_value(2.0), nudge.animate.set_value(0.0), run_time=0.14 * d)
      r1.clear_updaters()
      r2.clear_updaters()


# ------------------------------------------------------------------ 6 The question

class Question(NarratedScene):
  def construct(self):
    with self.say('s06_bound') as d:
      l1 = T(r'$n$ chemicals, $n$ reactions, one conservation law', 0.8)
      l2 = T(r'at most $n$ clean resting states on a slice', 0.8, REST)
      who = T(r'Banaji and Feliu, \emph{J.~Math.~Biol.}\ 2026', 0.6, MUTED)
      grp = VGroup(l1, l2, who).arrange(DOWN, buff=0.3)
      box = card(grp, color=PRIMARY)
      box.move_to(UP * 2.2)
      self.play(FadeIn(box[0]), Write(l1), run_time=0.2 * d)
      self.play(FadeIn(l2, shift=DOWN * 0.15), run_time=0.14 * d)
      self.play(FadeIn(who), run_time=0.08 * d)
      cells = VGroup()
      marks = VGroup()
      for n in range(2, 7):
        sq = RoundedRectangle(width=1.6, height=1.5, corner_radius=0.12, stroke_color=MUTED, stroke_width=2)
        top = MathTex(f'n={n}').scale(0.7)
        mx = T(f'max {n}', 0.65, MUTED)
        VGroup(top, mx).arrange(DOWN, buff=0.18).move_to(sq)
        cells.add(VGroup(sq, top, mx))
      cells.arrange(RIGHT, buff=0.3).move_to(DOWN * 0.45)
      for i, cell in enumerate(cells):
        m = check_mark(0.9) if i == 0 else MathTex('?', color=MOVE).scale(0.9)
        m.next_to(cell, DOWN, buff=0.2)
        marks.add(m)
      self.play(LaggedStart(*[FadeIn(c_) for c_ in cells], lag_ratio=0.15), run_time=0.18 * d)
      self.play(FadeIn(marks[0], scale=1.4), Indicate(cells[0], color=REST), run_time=0.12 * d)

    with self.say('s06_question') as d:
      q1 = T(r'1. Is the maximum reached for every $n$?', 0.75)
      q2 = T(r'2. How many molecules per collision?', 0.75)
      qs = VGroup(q1, q2).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(DOWN * 3.05)
      self.play(LaggedStart(*[FadeIn(m) for m in marks[1:]], lag_ratio=0.2), run_time=0.15 * d)
      self.play(FadeIn(q1), run_time=0.15 * d)
      self.wait(0.15 * d)
      self.play(FadeIn(q2), run_time=0.15 * d)

    with self.say('s06_answer') as d:
      ticks = VGroup(*[check_mark(0.9).move_to(m) for m in marks[1:]])
      a1 = T(r'1. Yes, for every $n \ge 2$', 0.75, REST)
      a2 = T(r'2. At most three suffice, and three is the least', 0.75, REST)
      ans = VGroup(a1, a2).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(qs)
      self.play(FadeOut(q1), FadeIn(a1), LaggedStart(*[ReplacementTransform(m, t) for m, t in zip(marks[1:], ticks)],
                                                     lag_ratio=0.2), run_time=0.25 * d)
      self.wait(0.12 * d)
      self.play(FadeOut(q2), FadeIn(a2), run_time=0.15 * d)
      self.wait(0.12 * d)
      known = T(r'($n=2$ was known before)', 0.6, MUTED).next_to(cells[0], UP, buff=0.12)
      self.play(FadeIn(known), Indicate(cells[0], color=MUTED), run_time=0.12 * d)


# ------------------------------------------------------------------ 7 Why pair collisions fail

class PairFails(NarratedScene):
  def construct(self):
    ax, deco = plane2()
    sl = slice_line(ax)
    px = 3.9
    with self.say('s07_pause') as d:
      self.play(FadeIn(ax), FadeIn(deco), Create(sl), run_time=0.15 * d)
      r1 = MT('2X', '+', 'Y', r'\to', 'X', scale=1.0).move_to(np.array([px, 1.6, 0]))
      hl = SurroundingRectangle(r1, color=MOVE, buff=0.2, corner_radius=0.1)
      self.play(Write(r1), run_time=0.15 * d)
      self.play(Create(hl), run_time=0.1 * d)
      why = T(r'why three molecules?', 0.8, MOVE).move_to(np.array([px, 0.3, 0]))
      self.play(FadeIn(why), run_time=0.1 * d)
      bars = VGroup(Rectangle(width=0.16, height=0.6), Rectangle(width=0.16, height=0.6)).arrange(RIGHT, buff=0.16)
      bars.set_fill(MUTED, 1).set_stroke(width=0).move_to(np.array([px, -0.9, 0]))
      self.play(FadeIn(bars), run_time=0.08 * d)

    with self.say('s07_input') as d:
      self.play(FadeOut(VGroup(r1, hl, why, bars)), run_time=0.06 * d)
      head = T(r'it destroys an $X$ and a $Y$', 0.75).move_to(np.array([px, 2.6, 0]))
      self.play(FadeIn(head), run_time=0.12 * d)
      self.wait(0.2 * d)
      pair = cluster('XY', r=0.32).move_to(np.array([px, 1.5, 0]))
      pl = T(r'with two molecules: exactly $X + Y$', 0.7, MUTED).move_to(np.array([px, 0.6, 0]))
      self.play(FadeIn(pair, scale=1.2), run_time=0.12 * d)
      self.play(FadeIn(pl), run_time=0.12 * d)

    def vline_curve(x0):
      return Line(ax.c2p(x0, 0), ax.c2p(x0, 6), color=CURVE, stroke_width=5)

    candidates = [
      (ax.plot(lambda x: 0.5 * x, x_range=[0, 8], color=CURVE, stroke_width=5), MT('Y', '=', 'c', 'X', scale=1.0),
       (4.0, 2.0), 'a line from the corner'),
      (ax.plot(lambda x: 6 / x, x_range=[1.0, 8], color=CURVE, stroke_width=5), MT('X', 'Y', '=', 'c', scale=1.0),
       (1 + np.sqrt(7), np.sqrt(7) - 1), 'a falling curve'),
      (ax.plot(lambda x: 3.0, x_range=[0, 8], color=CURVE, stroke_width=5), MT('Y', '=', 'c', scale=1.0),
       (5.0, 3.0), 'a flat line'),
      (vline_curve(3.5), MT('X', '=', 'c', scale=1.0), (3.5, 1.5), 'an upright line'),
    ]
    with self.say('s07_curves') as d:
      self.play(FadeOut(pl), pair.animate.scale(0.8).move_to(np.array([px, 1.7, 0])), run_time=0.05 * d)
      prev = None
      tag = T('1 crossing', 0.75, WARN).move_to(np.array([px, -1.2, 0]))
      for i, (crv, eq, (cx, cy), name) in enumerate(candidates):
        eq.move_to(np.array([px, 0.5, 0]))
        nm = T(name, 0.65, MUTED).next_to(eq, DOWN, buff=0.2)
        dot = Dot(ax.c2p(cx, cy), radius=0.11, color=MOVE).set_z_index(5)
        if prev is None:
          self.play(Create(crv), FadeIn(eq), FadeIn(nm), run_time=0.1 * d)
          self.play(FadeIn(dot, scale=1.5), FadeIn(tag), run_time=0.06 * d)
        else:
          pc, pe, pn, pd = prev
          self.play(ReplacementTransform(pc, crv), FadeTransform(pe, eq), FadeTransform(pn, nm), FadeOut(pd),
                    run_time=0.1 * d)
          self.play(FadeIn(dot, scale=1.5), Indicate(tag, color=WARN, scale_factor=1.1), run_time=0.06 * d)
        self.wait(0.05 * d)
        prev = (crv, eq, nm, dot)

    with self.say('s07_bend') as d:
      pc, pe, pn, pd = prev
      tri = cluster('XXY', r=0.3).move_to(np.array([px, 1.7, 0]))
      self.play(FadeTransform(pair, tri), FadeOut(head), run_time=0.12 * d)
      head2 = T(r'allow three molecules', 0.75).move_to(np.array([px, 2.6, 0]))
      self.play(FadeIn(head2), run_time=0.08 * d)
      par = parabola(ax)
      eq = MT('Y', '=', 'X^2', '/', '9', scale=1.0).move_to(np.array([px, 0.5, 0]))
      self.play(ReplacementTransform(pc, par), FadeTransform(pe, eq), FadeOut(pn), FadeOut(pd), run_time=0.22 * d)
      d1, d2 = rest_dot(ax, 3, 1), rest_dot(ax, 6, 4)
      tag2 = T('2 crossings', 0.75, REST).move_to(tag)
      self.play(FadeIn(d1, scale=1.6), FadeIn(d2, scale=1.6), ReplacementTransform(tag, tag2), run_time=0.15 * d)

    with self.say('s07_general') as d:
      down = DashedLine(ax.c2p(0, 6), ax.c2p(6, 0), dash_length=0.16, dashed_ratio=0.55, color=SLICE,
                        stroke_width=5)
      xs = (-9 + np.sqrt(81 + 216)) / 2
      dd = Dot(ax.c2p(xs, 6 - xs), radius=0.11, color=MOVE).set_z_index(5)
      tag3 = T('1 crossing', 0.75, WARN).move_to(tag2)
      self.play(ReplacementTransform(sl, down), FadeOut(d1), FadeOut(d2), FadeOut(VGroup(tri, head2)),
                ReplacementTransform(tag2, tag3), run_time=0.12 * d)
      self.play(FadeIn(dd, scale=1.5), run_time=0.08 * d)
      self.wait(0.12 * d)
      self.play(FadeOut(VGroup(eq, tag3)), run_time=0.05 * d)
      g1 = T(r'bigger networks, pair collisions:', 0.7).move_to(np.array([px, 1.7, 0]))
      g2 = T(r'at most $2$', 0.85).next_to(g1, DOWN, buff=0.25)
      g3 = T(r'(Banaji and Feliu)', 0.6, MUTED).next_to(g2, DOWN, buff=0.2)
      g4 = T(r'need $n \ge 3$: fall short', 0.8, WARN).next_to(g3, DOWN, buff=0.5)
      self.play(FadeIn(g1), run_time=0.08 * d)
      self.play(FadeIn(g2), FadeIn(g3), run_time=0.1 * d)
      self.wait(0.08 * d)
      self.play(FadeIn(g4), run_time=0.1 * d)


# ------------------------------------------------------------------ 8 Three species

class ThreeSpecies(NarratedScene):
  def construct(self):
    ys = [2.5, 1.0, -0.5]
    rows = reaction_rows([('XXY', 'X'), ('YYZ', 'YZZ'), ('ZZ', 'XYYZ')], ys=ys, x_in=-3.4, x_out=-1.6,
                         rates=[r'1/306000', r'1/79475', r'1/121'])
    nums = VGroup(*[T(str(i + 1), 0.7, MUTED).move_to(np.array([-6.6, y, 0])) for i, y in enumerate(ys)])
    with self.say('s08_net') as d:
      self.wait(0.12 * d)
      for i, (a, arr, b, lab) in enumerate(rows):
        self.play(FadeIn(nums[i]), FadeIn(a), run_time=0.06 * d)
        self.play(GrowArrow(arr), FadeIn(lab), run_time=0.06 * d)
        self.play(FadeIn(b), run_time=0.06 * d)
        self.wait(0.07 * d)

    (a1, ar1, b1, l1), (a2, ar2, b2, l2), (a3, ar3, b3, l3) = rows
    rx = 4.1
    with self.say('s08_equal') as d:
      hx = VGroup(SurroundingRectangle(a1, color=X_COL, buff=0.1, corner_radius=0.08),
                  SurroundingRectangle(b3[0], color=X_COL, buff=0.1, corner_radius=0.08))
      e1 = MT(r'\text{rate } 1', '=', r'\text{rate } 3', scale=0.8).move_to(np.array([rx, 1.9, 0]))
      w1 = T(r'(balances $X$)', 0.62, X_COL).next_to(e1, DOWN, buff=0.12)
      self.play(Create(hx), run_time=0.12 * d)
      self.play(FadeIn(e1), FadeIn(w1), run_time=0.12 * d)
      self.wait(0.08 * d)
      hz = VGroup(SurroundingRectangle(b2[1:], color=Z_COL, buff=0.1, corner_radius=0.08),
                  SurroundingRectangle(a3, color=Z_COL, buff=0.1, corner_radius=0.08))
      e2 = MT(r'\text{rate } 2', '=', r'\text{rate } 3', scale=0.8).move_to(np.array([rx, 0.5, 0]))
      w2 = T(r'(balances $Z$)', 0.62, Z_COL).next_to(e2, DOWN, buff=0.12)
      self.play(FadeOut(hx), Create(hz), run_time=0.12 * d)
      self.play(FadeIn(e2), FadeIn(w2), run_time=0.12 * d)
      self.wait(0.08 * d)
      all3 = T(r'all three rates equal', 0.78, REST).move_to(np.array([rx, -0.9, 0]))
      self.play(FadeOut(hz), FadeIn(all3), run_time=0.12 * d)

    with self.say('s08_curve') as d:
      dial = NumberLine(x_range=[0, 3, 1], length=3.6, color=MUTED, include_numbers=False).move_to(np.array([rx, -1.9, 0]))
      tv = ValueTracker(0.6)
      knob = always_redraw(lambda: Triangle(color=MOVE, fill_opacity=1).scale(0.12).rotate(PI)
                           .move_to(dial.n2p(tv.get_value()) + UP * 0.2))
      tl = MathTex('t', color=MOVE).scale(0.8).next_to(dial, LEFT, buff=0.25)
      curve = MT('X = 60t^3', r',\quad', 'Y = 85t^2', r',\quad', 'Z = 11t^4', scale=0.95)
      curve.move_to(np.array([0, -2.9, 0]))
      self.play(FadeOut(VGroup(e1, w1, e2, w2)), all3.animate.move_to(np.array([rx, 0.6, 0])), run_time=0.1 * d)
      self.play(Create(dial), FadeIn(tl), FadeIn(knob), run_time=0.12 * d)
      self.play(tv.animate.set_value(2.4), run_time=0.15 * d)
      self.play(Write(curve), tv.animate.set_value(1.2), run_time=0.3 * d)

    with self.say('s08_check') as d:
      self.play(FadeOut(VGroup(dial, tl, knob, all3)), VGroup(a2, ar2, b2, l2, a3, ar3, b3, l3, nums[1:]).animate.set_opacity(0.3),
                run_time=0.08 * d)
      num = MT('X^2', 'Y', scale=0.95)
      bar = Line(LEFT * 1.8, RIGHT * 1.8, color=INK, stroke_width=3)
      den = MathTex('306000').scale(0.95)
      frac = VGroup(num, bar, den).arrange(DOWN, buff=0.15).move_to(np.array([3.1, 1.4, 0]))
      self.play(FadeIn(frac), Indicate(l1, color=MOVE), run_time=0.12 * d)
      num2 = MT('(60t^3)^2', r'\cdot', '85t^2', scale=0.95, colors={0: X_COL, 2: Y_COL}).move_to(num)
      self.play(TransformMatchingTex(num, num2), run_time=0.12 * d)
      num3 = MT('3600', r'\cdot', '85', 't^8', scale=0.95, colors={3: MOVE}).move_to(num)
      self.play(TransformMatchingTex(num2, num3), run_time=0.12 * d)
      num4 = MT('306000', 't^8', scale=0.95, colors={1: MOVE}).move_to(num)
      self.play(TransformMatchingTex(num3, num4), run_time=0.12 * d)
      s1 = Line(num4[0].get_corner(DL), num4[0].get_corner(UR), color=WARN, stroke_width=4)
      s2 = Line(den.get_corner(DL), den.get_corner(UR), color=WARN, stroke_width=4)
      res = MT('=', 't^8', scale=1.0, colors={1: REST}).next_to(bar, RIGHT, buff=0.35)
      self.play(Create(s1), Create(s2), run_time=0.08 * d)
      self.play(FadeIn(res), run_time=0.08 * d)
      o2 = MathTex(r'\frac{Y^2 Z}{79475}', '=', 't^8').scale(0.8)
      o3 = MathTex(r'\frac{Z^2}{121}', '=', 't^8').scale(0.8)
      o2[2].set_color(REST)
      o3[2].set_color(REST)
      others = VGroup(o2, o3).arrange(RIGHT, buff=0.7).move_to(np.array([4.0, -0.6, 0]))
      self.play(FadeIn(others), VGroup(a2, ar2, b2, l2, a3, ar3, b3, l3, nums[1:]).animate.set_opacity(1),
                run_time=0.12 * d)


# ------------------------------------------------------------------ 9 The slice for three species

class Slice3(NarratedScene):
  def construct(self):
    with self.say('s09_conserve') as d:
      heads = ['X', 'Y', 'Z', r'Y + Z - X']
      data = [['-1', '-1', '0', '0'], ['0', '-1', '+1', '0'], ['+1', '+2', '-1', '0']]
      xs = [-2.0, -0.6, 0.8, 3.2]
      yrow = [0.9, 0.0, -0.9]
      grid = VGroup()
      hrow = VGroup(*[MT(h, scale=0.85).move_to(np.array([x, 1.9, 0])) for h, x in zip(heads, xs)])
      hrow[3].set_color(INK)
      lab = VGroup(*[T(f'reaction {i + 1}', 0.65, MUTED).move_to(np.array([-4.2, y, 0])) for i, y in enumerate(yrow)])
      for r, y in zip(data, yrow):
        for j, (v, x) in enumerate(zip(r, xs)):
          grid.add(MathTex(v, color=REST if j == 3 else INK).scale(0.85).move_to(np.array([x, y, 0])))
      cap = T('change in each reaction', 0.7, MUTED).move_to(UP * 3.0)
      rule = Line(np.array([-5.2, 1.45, 0]), np.array([4.4, 1.45, 0]), color=MUTED, stroke_width=1.5)
      self.play(FadeIn(cap), FadeIn(hrow[:3]), FadeIn(lab), Create(rule), run_time=0.15 * d)
      self.play(LaggedStart(*[FadeIn(g) for i, g in enumerate(grid) if i % 4 != 3], lag_ratio=0.05), run_time=0.15 * d)
      self.play(FadeIn(hrow[3]), run_time=0.08 * d)
      self.play(LaggedStart(*[FadeIn(grid[i], scale=1.4) for i in (3, 7, 11)], lag_ratio=0.3), run_time=0.15 * d)
      sl = MT('Y', '+', 'Z', '-', 'X', '=', '36', scale=1.0).move_to(DOWN * 2.4)
      sll = T('our slice', 0.7, SLICE).next_to(sl, DOWN, buff=0.2)
      self.play(Write(sl), FadeIn(sll), run_time=0.2 * d)

    ax, curve, deco = qplot(np.array([-3.0, -0.7, 0]))
    with self.say('s09_plug') as d:
      self.play(FadeOut(VGroup(cap, hrow, lab, grid, rule, sll)), sl.animate.scale(0.75).move_to(np.array([3.9, 2.9, 0])),
                run_time=0.1 * d)
      cform = MT('X = 60t^3', r',\;', 'Y = 85t^2', r',\;', 'Z = 11t^4', scale=0.7).move_to(np.array([-3.0, 3.25, 0]))
      self.play(FadeIn(cform), run_time=0.08 * d)
      expr = MathTex(r'11t^4 - 60t^3 + 85t^2').scale(0.8).move_to(np.array([3.9, 1.6, 0]))
      yl = MT('Y + Z - X', scale=0.65).next_to(ax.y_axis.get_end(), UP, buff=0.15)
      self.play(Create(ax), FadeIn(deco), FadeIn(yl), run_time=0.12 * d)
      self.play(Write(expr), run_time=0.15 * d)
      self.play(Create(curve), run_time=0.2 * d)
      poly = T('a polynomial', 0.7, MUTED).next_to(expr, DOWN, buff=0.2)
      self.play(FadeIn(poly), run_time=0.08 * d)
      lv = level_line(ax, 36)
      lvl = MathTex('36', color=SLICE).scale(0.65).next_to(ax.c2p(0, 36), LEFT, buff=0.15)
      self.play(Create(lv), FadeIn(lvl), run_time=0.12 * d)

    with self.say('s09_roots') as d:
      dots = VGroup(*[Dot(ax.c2p(t, 36), radius=0.11, color=REST).set_z_index(5) for t in (1, 2, 3)])
      self.play(LaggedStart(*[FadeIn(dd, scale=1.8) for dd in dots], lag_ratio=0.5), run_time=0.25 * d)
      self.play(FadeOut(poly), run_time=0.04 * d)
      rows = VGroup(
        MT('t=1:', r'(60,\,85,\,11)', scale=0.7),
        MT('t=2:', r'(480,\,340,\,176)', scale=0.7),
        MT('t=3:', r'(1620,\,765,\,891)', scale=0.7),
      ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(np.array([3.9, 0.0, 0]))
      for r in rows:
        r[0].set_color(REST)
      head = MT(r'(X,\,Y,\,Z)', scale=0.7, colors={0: MUTED}).next_to(rows, UP, buff=0.3).align_to(rows[0][1], LEFT)
      self.play(FadeOut(expr), run_time=0.05 * d)
      self.play(FadeIn(head), LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.3), run_time=0.2 * d)
      chk = MT('85', '+', '11', '-', '60', '=', '36', scale=0.8, colors={0: Y_COL, 2: Z_COL, 4: X_COL, 6: REST})
      chk.next_to(rows, DOWN, buff=0.5)
      self.play(Indicate(rows[0], color=MOVE), Write(chk), run_time=0.2 * d)


# ------------------------------------------------------------------ 10 Descartes

class Descartes(NarratedScene):
  def construct(self):
    with self.say('s10_signs') as d:
      parts = ['11t^4', '-', '60t^3', '+', '85t^2', '-', '36', '=', '0']
      poly = MathTex(*parts).scale(1.3).move_to(UP * 1.4)
      self.play(Write(poly), run_time=0.3 * d)
      sym = ['+', '-', '+', '-']
      signs = VGroup(*[MathTex(s, color=MOVE).scale(1.5) for s in sym])
      anchors = [poly[0], poly[2], poly[4], poly[6]]
      for s, a in zip(signs, anchors):
        s.next_to(a, DOWN, buff=0.55)
      self.wait(0.05 * d)
      self.play(LaggedStart(*[FadeIn(s, shift=DOWN * 0.2) for s in signs], lag_ratio=0.25),
                *[Indicate(poly[i], color=MOVE) for i in (1, 3, 5)], run_time=0.25 * d)
      arcs = VGroup()
      labels = VGroup()
      for k, (a, b) in enumerate(zip(signs[:-1], signs[1:]), 1):
        arc = ArcBetweenPoints(a.get_bottom() + DOWN * 0.15, b.get_bottom() + DOWN * 0.15, angle=PI / 2.2,
                               color=MOVE, stroke_width=4)
        arcs.add(arc)
        labels.add(MathTex(str(k), color=MOVE).scale(0.75).next_to(arc, DOWN, buff=0.1))
      self.play(LaggedStart(*[AnimationGroup(Create(a), FadeIn(l)) for a, l in zip(arcs, labels)], lag_ratio=0.35),
                run_time=0.25 * d)

    with self.say('s10_descartes') as d:
      who = T(r'Descartes, 1637', 0.65, MUTED).to_edge(UP, buff=0.5)
      rule = T(r'positive solutions $\le$ sign flips', 0.85).move_to(DOWN * 2.2)
      self.play(FadeIn(who), FadeIn(rule), run_time=0.15 * d)
      self.wait(0.12 * d)
      three = T(r'at most $3$', 0.85, REST).move_to(DOWN * 2.2)
      self.play(FadeTransform(rule, three), run_time=0.12 * d)
      self.wait(0.15 * d)
      fac = MathTex('(t-1)', '(t-2)', '(t-3)', '(11t+6)', '=', '0').scale(1.0)
      for i in range(3):
        fac[i].set_color(REST)
      fac[3].set_color(MUTED)
      fac.move_to(DOWN * 0.6)
      self.play(FadeOut(VGroup(signs, arcs, labels)), run_time=0.06 * d)
      self.play(FadeIn(fac, shift=UP * 0.15), run_time=0.15 * d)
      note = T(r'never zero for $t>0$', 0.62, MUTED).next_to(fac[3], DOWN, buff=0.2)
      self.play(FadeIn(note), run_time=0.08 * d)

    ax, curve, deco = qplot(np.array([0.0, -0.4, 0]), x_length=7.6, y_length=5.0)
    with self.say('s10_robust') as d:
      self.play(FadeOut(VGroup(poly, who, three, fac, note)), run_time=0.08 * d)
      k = ValueTracker(36.0)
      lv = always_redraw(lambda: level_line(ax, k.get_value()))
      lvl = always_redraw(lambda: DecimalNumber(k.get_value(), num_decimal_places=0, color=SLICE).scale(0.65)
                          .next_to(ax.c2p(0, k.get_value()), LEFT, buff=0.15))
      dots = always_redraw(lambda: VGroup(*[Dot(ax.c2p(t, k.get_value()), radius=0.11, color=REST).set_z_index(5)
                                           for t in positive_roots([11, -60, 85, 0, -k.get_value()])]))
      yl = MT('Y + Z - X', scale=0.65).next_to(ax.y_axis.get_end(), UP, buff=0.15)
      self.play(Create(ax), FadeIn(deco), FadeIn(yl), Create(curve), run_time=0.15 * d)
      self.add(lv, lvl, dots)
      cnt = T(r'3 crossings', 0.75, REST).move_to(np.array([3.6, 2.6, 0]))
      self.play(FadeIn(cnt), run_time=0.06 * d)
      self.play(k.animate.set_value(42), run_time=0.18 * d)
      self.play(k.animate.set_value(30), run_time=0.22 * d)
      self.play(k.animate.set_value(36), run_time=0.14 * d)


# ------------------------------------------------------------------ 11 The recipe for every n

class Recipe(NarratedScene):
  def construct(self):
    lx = -3.6
    with self.say('s11_pattern') as d:
      head = T(r'inputs for $n$ chemicals', 0.75, MUTED).move_to(np.array([lx, 3.0, 0]))
      lines = VGroup(
        MathTex(r'2X_1 + X_2'), MathTex(r'2X_2 + X_3'), MathTex(r'\vdots'), MathTex(r'2X_{n-1} + X_n'),
        MathTex(r'2X_n'),
      ).arrange(DOWN, buff=0.3).scale(0.95).move_to(np.array([lx, 0.4, 0]))
      self.play(FadeIn(head), run_time=0.1 * d)
      self.play(LaggedStart(*[FadeIn(l, shift=RIGHT * 0.15) for l in lines[:2]], lag_ratio=0.4), run_time=0.2 * d)
      self.play(LaggedStart(*[FadeIn(l, shift=RIGHT * 0.15) for l in lines[2:]], lag_ratio=0.3), run_time=0.2 * d)
      br = Brace(lines, RIGHT, buff=0.3, color=MOVE)
      brl = T(r'at most $3$ in', 0.72, MOVE).next_to(br, RIGHT, buff=0.15)
      self.play(GrowFromCenter(br), FadeIn(brl), run_time=0.12 * d)
      ex = MT('n=3:', r'2X + Y,\;', r'2Y + Z,\;', '2Z', scale=0.7, colors={0: MUTED}).move_to(np.array([lx, -2.8, 0]))
      ex[1].set_color(INK)
      ex[2].set_color(INK)
      ex[3].set_color(Z_COL)
      self.play(FadeIn(ex), run_time=0.1 * d)

    rx = 3.3
    with self.say('s11_poly') as d:
      self.play(FadeOut(VGroup(br, brl)), run_time=0.05 * d)
      ph = T(r'powers of $t$ on the curve', 0.7, MUTED).move_to(np.array([rx, 3.0, 0]))
      prow = VGroup(
        MathTex(r'n=2:', r'\;1,\ 2'),
        MathTex(r'n=3:', r'\;3,\ 2,\ 4'),
        MathTex(r'n=4:', r'\;5,\ 6,\ 4,\ 8'),
      ).scale(0.8).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to(np.array([rx, 1.6, 0]))
      for r in prow:
        r[0].set_color(MUTED)
      self.play(FadeIn(ph), LaggedStart(*[FadeIn(r) for r in prow], lag_ratio=0.3), run_time=0.22 * d)
      diff = T('all different', 0.65, REST).next_to(prow, DOWN, buff=0.2)
      self.play(FadeIn(diff), run_time=0.08 * d)
      self.wait(0.1 * d)
      s1 = T(r'$n+1$ terms', 0.78).move_to(np.array([rx, -0.7, 0]))
      s2 = T(r'at most $n$ sign flips', 0.78).move_to(np.array([rx, -1.7, 0]))
      s3 = T(r'at most $n$ crossings', 0.78, REST).move_to(np.array([rx, -2.7, 0]))
      a1 = Arrow(s1.get_bottom(), s2.get_top(), buff=0.06, color=MUTED, stroke_width=3, max_tip_length_to_length_ratio=0.35)
      a2 = Arrow(s2.get_bottom(), s3.get_top(), buff=0.06, color=MUTED, stroke_width=3, max_tip_length_to_length_ratio=0.35)
      self.play(FadeIn(s1), run_time=0.1 * d)
      self.play(GrowArrow(a1), FadeIn(s2), run_time=0.1 * d)
      self.play(GrowArrow(a2), FadeIn(s3), run_time=0.1 * d)

    with self.say('s11_backwards') as d:
      self.play(FadeOut(VGroup(ph, prow, diff, s1, s2, s3, a1, a2)), run_time=0.08 * d)
      steps = [
        (r'choose zeros $t = 1, 2, \dots, n$', MOVE),
        (r'the polynomial', INK),
        (r'each output and rate', INK),
        (r'$n$ clean resting states', REST),
      ]
      boxes = VGroup()
      for s, col in steps:
        t = T(s, 0.68, col)
        r = RoundedRectangle(width=t.width + 0.6, height=t.height + 0.4, corner_radius=0.12, stroke_color=col,
                             stroke_width=2)
        r.move_to(t)
        boxes.add(VGroup(r, t))
      boxes.arrange(DOWN, buff=0.45).move_to(np.array([rx, 0.3, 0]))
      arrows = VGroup(*[Arrow(boxes[i].get_bottom(), boxes[i + 1].get_top(), buff=0.05, color=MUTED, stroke_width=3,
                              max_tip_length_to_length_ratio=0.4) for i in range(3)])
      self.play(FadeIn(boxes[0]), run_time=0.12 * d)
      self.play(GrowArrow(arrows[0]), FadeIn(boxes[1]), run_time=0.12 * d)
      self.wait(0.05 * d)
      self.play(GrowArrow(arrows[1]), FadeIn(boxes[2]), run_time=0.12 * d)
      valid = T(r'whole numbers of molecules, positive rates', 0.6, MUTED).next_to(boxes[3], DOWN, buff=0.35)
      self.wait(0.05 * d)
      self.play(GrowArrow(arrows[2]), FadeIn(boxes[3]), FadeIn(valid), run_time=0.14 * d)

    with self.say('s11_four') as d:
      self.play(FadeOut(VGroup(head, lines, ex, boxes, arrows, valid)), run_time=0.08 * d)
      h4 = T(r'four chemicals', 0.8, MUTED).move_to(UP * 2.8)
      parts = ['1169t^8', '-', '66025t^6', '+', '258300t^5', '-', '276388t^4', '+', '82944']
      p4 = MathTex(*parts).scale(0.9).move_to(UP * 1.2)
      self.play(FadeIn(h4), Write(p4), run_time=0.25 * d)
      sym = ['+', '-', '+', '-', '+']
      signs = VGroup(*[MathTex(s, color=MOVE).scale(1.2) for s in sym])
      for s, a in zip(signs, [p4[0], p4[2], p4[4], p4[6], p4[8]]):
        s.next_to(a, DOWN, buff=0.45)
      arcs = VGroup()
      labs = VGroup()
      for k, (a, b) in enumerate(zip(signs[:-1], signs[1:]), 1):
        arc = ArcBetweenPoints(a.get_bottom() + DOWN * 0.12, b.get_bottom() + DOWN * 0.12, angle=PI / 2.4,
                               color=MOVE, stroke_width=4)
        arcs.add(arc)
        labs.add(MathTex(str(k), color=MOVE).scale(0.7).next_to(arc, DOWN, buff=0.08))
      self.play(FadeIn(signs), run_time=0.12 * d)
      self.play(LaggedStart(*[AnimationGroup(Create(a), FadeIn(l)) for a, l in zip(arcs, labs)], lag_ratio=0.3),
                run_time=0.2 * d)
      zeros = T(r'zero at exactly $t = 1, 2, 3, 4$', 0.85, REST).move_to(DOWN * 2.6)
      self.play(FadeIn(zeros), run_time=0.12 * d)


# ------------------------------------------------------------------ 12 What it does not say

class Honest(NarratedScene):
  def construct(self):
    ax, deco = plane2()
    sl = slice_line(ax)
    par = parabola(ax)
    r1, r2 = rest_dot(ax, 3, 1), rest_dot(ax, 6, 4)
    px = 3.9

    def on_slice(x):
      return ax.c2p(x, x - 2)

    with self.say('s12_stable') as d:
      self.play(FadeIn(VGroup(ax, deco, sl, par, r1, r2)), run_time=0.1 * d)
      head = T(r'resting $\neq$ stable', 0.85).move_to(np.array([px, 2.6, 0]))
      self.play(FadeIn(head), run_time=0.1 * d)
      flows = VGroup(*[Arrow(on_slice(a), on_slice(b), buff=0, color=MOVE, stroke_width=5,
                             max_tip_length_to_length_ratio=0.45)
                       for a, b in [(2.85, 2.35), (3.6, 4.3), (4.7, 5.4), (7.6, 6.7)]])
      self.play(LaggedStart(*[GrowArrow(f) for f in flows], lag_ratio=0.2), run_time=0.15 * d)
      m = Dot(on_slice(3.15), radius=0.1, color=MOVE).set_z_index(6)
      self.play(FadeIn(m), run_time=0.04 * d)
      self.play(m.animate.move_to(on_slice(5.97)), run_time=0.2 * d, rate_func=smooth)
      # hilltop and valley icons
      hill = VGroup(Arc(radius=0.45, start_angle=0, angle=PI, color=WARN, stroke_width=5),
                    Dot(UP * 0.55, radius=0.12, color=MOVE))
      valley = VGroup(Arc(radius=0.45, start_angle=PI, angle=PI, color=REST, stroke_width=5),
                      Dot(DOWN * 0.33, radius=0.12, color=MOVE))
      hill.move_to(np.array([px - 1.6, 1.0, 0]))
      valley.move_to(np.array([px - 1.6, -0.4, 0]))
      hl = T(r'$(3,1)$: hilltop', 0.7, WARN).next_to(hill, RIGHT, buff=0.35)
      vl = T(r'$(6,4)$: valley', 0.7, REST).next_to(valley, RIGHT, buff=0.35)
      self.play(FadeIn(hill), FadeIn(hl), Indicate(r1, color=WARN, scale_factor=1.6), run_time=0.12 * d)
      self.play(FadeIn(valley), FadeIn(vl), Indicate(r2, color=REST, scale_factor=1.6), run_time=0.12 * d)

    with self.say('s12_switch') as d:
      c1 = T(r'counts resting states', 0.72, REST)
      c2 = T(r'no claim about stability', 0.72, WARN)
      cc = VGroup(c1, c2).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to(np.array([px, -2.0, 0]))
      self.play(FadeIn(c1), run_time=0.15 * d)
      self.wait(0.1 * d)
      self.play(FadeIn(c2), run_time=0.15 * d)

    with self.say('s12_slice') as d:
      self.play(FadeOut(Group(*self.mobjects)), run_time=0.07 * d)
      q = MT('Y', '+', 'Z', '-', 'X', scale=1.2, colors={3: WARN}).move_to(UP * 3.0)
      self.play(Write(q), run_time=0.08 * d)
      self.play(Indicate(q[3], color=WARN, scale_factor=1.6), run_time=0.05 * d)

      def mini(center):
        a = Axes(x_range=[0, 6, 1], y_range=[0, 6, 1], x_length=3.4, y_length=3.4, tips=False,
                 axis_config={'color': MUTED, 'stroke_width': 2, 'tick_size': 0.04}).move_to(center)
        return a

      la, ra = mini(np.array([-3.4, -0.1, 0])), mini(np.array([3.0, -0.1, 0]))
      seg = Line(la.c2p(0, 5), la.c2p(5, 0), color=SLICE, stroke_width=5)
      ends = VGroup(Dot(la.c2p(0, 5), radius=0.08, color=SLICE), Dot(la.c2p(5, 0), radius=0.08, color=SLICE))
      lt = T(r'a total amount', 0.68).next_to(la, UP, buff=0.2)
      lb = T(r'bounded: at most $2$', 0.68, MUTED).next_to(la, DOWN, buff=0.25)
      ray = DashedLine(ra.c2p(1, 0), ra.c2p(6, 5), dash_length=0.14, color=SLICE, stroke_width=5)
      tip = Arrow(ra.c2p(5.6, 4.6), ra.c2p(6.6, 5.6), buff=0, color=SLICE, stroke_width=5,
                  max_tip_length_to_length_ratio=0.5)
      rt = T(r'with a minus sign', 0.68).next_to(ra, UP, buff=0.2)
      rb = T(r'runs off forever', 0.68, MUTED).next_to(ra, DOWN, buff=0.25)
      self.play(Create(ra), Create(ray), GrowArrow(tip), FadeIn(rt), run_time=0.14 * d)
      self.play(FadeIn(rb), run_time=0.08 * d)
      self.play(Create(la), Create(seg), FadeIn(ends), FadeIn(lt), run_time=0.14 * d)
      who = T(r'(Banaji and Feliu)', 0.6, MUTED).next_to(lb, DOWN, buff=0.12)
      self.play(FadeIn(lb), FadeIn(who), run_time=0.1 * d)
      need = T(r'needed for $n \ge 3$', 0.68, MOVE).next_to(rb, DOWN, buff=0.12)
      self.play(FadeIn(need), run_time=0.1 * d)

    with self.say('s12_outputs') as d:
      self.play(FadeOut(Group(*self.mobjects)), run_time=0.07 * d)
      a = cluster('ZZ', r=0.32)
      b = cluster('XYYZ', r=0.32)
      arr = Arrow(LEFT, RIGHT, buff=0, color=MUTED, stroke_width=4, max_tip_length_to_length_ratio=0.2)
      row = VGroup(a, arr, b).arrange(RIGHT, buff=0.4).move_to(UP * 1.2)
      self.play(FadeIn(a), GrowArrow(arr), FadeIn(b), run_time=0.14 * d)
      ba = Brace(a, DOWN, color=REST)
      bl = T(r'$2$ in', 0.7, REST).next_to(ba, DOWN, buff=0.12)
      bb = Brace(b, DOWN, color=MOVE)
      bbl = T(r'$4$ out', 0.7, MOVE).next_to(bb, DOWN, buff=0.12)
      self.play(GrowFromCenter(ba), FadeIn(bl), GrowFromCenter(bb), FadeIn(bbl), run_time=0.14 * d)
      lim = T(r'the limit of three is on inputs only', 0.72).move_to(DOWN * 1.4)
      self.play(FadeIn(lim), run_time=0.12 * d)
      self.wait(0.08 * d)
      lab = T(r'mathematics of the equations, not a lab mixture', 0.72, MUTED).move_to(DOWN * 2.4)
      self.play(FadeIn(lab), run_time=0.12 * d)


# ------------------------------------------------------------------ 13 Evidence

class Evidence(NarratedScene):
  def construct(self):
    with self.say('s13_proof') as d:
      head = T('How sure can we be?', 0.9).to_edge(UP, buff=0.5)
      self.play(FadeIn(head), run_time=0.08 * d)
      lp = VGroup(T(r'\textbf{Proof}', 0.8, REST), T(r'every $n \ge 2$', 0.7), T(r'written argument', 0.7),
                  T(r'internal reviews', 0.7, MUTED)).arrange(DOWN, buff=0.22)
      lc = VGroup(T(r'\textbf{Computer checks}', 0.8, PRIMARY), T(r'$n = 2$ to $8$', 0.7),
                  T(r'$35$ resting states', 0.7), T(r'exact fractions, two programs', 0.7, MUTED)).arrange(DOWN, buff=0.22)
      cp, cc = card(lp, color=REST), card(lc, color=PRIMARY)
      for g in (cp, cc):
        g[0].stretch_to_fit_width(5.4)
        g[0].stretch_to_fit_height(2.7)
      cp.move_to(np.array([-3.2, 1.0, 0]))
      cc.move_to(np.array([3.2, 1.0, 0]))
      self.play(FadeIn(cp), run_time=0.18 * d)
      self.wait(0.12 * d)
      self.play(FadeIn(cc), run_time=0.18 * d)

    with self.say('s13_limits') as d:
      sq = VGroup()
      for n in range(2, 15):
        checked = n <= 8
        s = Square(0.62, stroke_width=2, stroke_color=PRIMARY if checked else MUTED)
        s.set_fill(PRIMARY if checked else BACKGROUND, opacity=0.25 if checked else 0)
        s.add(MathTex(str(n)).scale(0.55).move_to(s))
        sq.add(s)
      sq.arrange(RIGHT, buff=0.1)
      dots = MathTex(r'\cdots').scale(0.8)
      strip = VGroup(sq, dots).arrange(RIGHT, buff=0.15).move_to(DOWN * 1.0)
      bl = Brace(strip, DOWN, color=REST, buff=0.12)
      bll = T(r'proof: every $n$', 0.68, REST).next_to(bl, DOWN, buff=0.1)
      bc = Brace(sq[:7], UP, color=PRIMARY, buff=0.1)
      bcl = T(r'checked', 0.65, PRIMARY).next_to(bc, UP, buff=0.08)
      self.play(FadeIn(strip), run_time=0.1 * d)
      self.play(GrowFromCenter(bc), FadeIn(bcl), run_time=0.1 * d)
      self.play(GrowFromCenter(bl), FadeIn(bll), run_time=0.1 * d)
      self.wait(0.1 * d)
      n1 = T(r'outside expert review: not yet', 0.68, MOVE)
      n2 = T(r'earlier work: none found (the search is bounded)', 0.68, MOVE)
      VGroup(n1, n2).arrange(DOWN, buff=0.18).move_to(DOWN * 3.2)
      self.play(FadeIn(n1), run_time=0.1 * d)
      self.wait(0.08 * d)
      self.play(FadeIn(n2), run_time=0.1 * d)


# ------------------------------------------------------------------ 14 Ending

class Ending(NarratedScene):
  def construct(self):
    with self.say('s14_recap') as d:
      head = T('Recap', 0.95).to_edge(UP, buff=0.6)
      pts = VGroup(
        T(r'1.\; Resting states are crossings of a balance curve and a slice.', 0.72),
        T(r'2.\; $n$ chemicals, $n$ reactions: three-body collisions reach $n$, for every $n$.', 0.72),
        T(r'3.\; Pair collisions never can, so three is the threshold.', 0.72),
      ).arrange(DOWN, aligned_edge=LEFT, buff=0.55).move_to(DOWN * 0.2)
      self.play(FadeIn(head), run_time=0.05 * d)
      self.play(FadeIn(pts[0], shift=UP * 0.15), run_time=0.08 * d)
      self.wait(0.2 * d)
      self.play(FadeIn(pts[1], shift=UP * 0.15), run_time=0.08 * d)
      self.wait(0.25 * d)
      self.play(FadeIn(pts[2], shift=UP * 0.15), run_time=0.08 * d)

    with self.say('s14_open') as d:
      self.play(FadeOut(VGroup(head, pts)), run_time=0.06 * d)
      head2 = T(r"What we still don't know", 0.9).to_edge(UP, buff=0.6)
      o1 = T(r'How many of the $n$ resting states can be stable at once?', 0.75)
      o2 = T(r'Can the outputs be kept small as well?', 0.75)
      qs = VGroup(o1, o2).arrange(DOWN, aligned_edge=LEFT, buff=0.7).move_to(DOWN * 0.1)
      marks = VGroup(*[MathTex('?', color=MOVE).scale(1.1).next_to(o, LEFT, buff=0.4) for o in qs])
      self.play(FadeIn(head2), run_time=0.06 * d)
      self.play(FadeIn(o1), FadeIn(marks[0]), run_time=0.12 * d)
      self.wait(0.3 * d)
      self.play(FadeIn(o2), FadeIn(marks[1]), run_time=0.12 * d)

    with self.say('s14_end', pause=4.0) as d:
      self.play(FadeOut(Group(*self.mobjects)), run_time=0.3 * d)
      t1 = T(r'Sharp equilibrium counts with cubic sources', 0.9)
      t2 = T(r'Valyu Research, 2026', 0.7, MUTED)
      t3 = T(r'\texttt{chemistry/reaction-networks/mass-action/cubic-equilibrium-sharpness}', 0.55, MUTED)
      t4 = T(r'Narration uses a synthetic voice.', 0.55, MUTED)
      endc = VGroup(t1, t2, t3).arrange(DOWN, buff=0.4).move_to(UP * 0.3)
      t4.to_edge(DOWN, buff=0.6)
      self.play(FadeIn(endc), FadeIn(t4), run_time=0.5 * d)
