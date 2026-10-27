"""Explainer: global and unique optimality of conjugate restart laws for a walker on a line,
and the reversibility characterisation for finite rooms (finite killed Markov chains).

Running example (paper Example 2.4 with D = 1, r0 = 1): success curve e^{-x}, conjugate map
p(x) = 2 e^{-2x}, best recipe = random (exponential) timer with rate 1, average search time 1.
Competitor costs are read from ../verification/resetting_verification.json. Walker paths in the
first scenes are illustrative simulations (fixed seeds), not data from the paper.
"""

import json
from pathlib import Path

import numpy as np
from manim import *
from vrvideo import *

SCENES = [
  'Keys', 'Walker', 'Average', 'Restart', 'Timers', 'Question', 'Conjugate', 'Result',
  'KeyIdea', 'Example', 'Rooms', 'Wrap',
]

ROOT = Path(__file__).resolve().parent
DATA = json.loads((ROOT.parent / 'verification' / 'resetting_verification.json').read_text())

WALKER = PRIMARY
TARGET = WARM
RESET = MUTED
FLASH = SECONDARY
OURS = ACCENT
RIVAL = EXTRA
BAD = WARN


def T(text, scale=0.7, color=INK):
  return Tex(text, color=color).scale(scale)


def M(text, scale=0.8, color=INK):
  return MathTex(text, color=color).scale(scale)


def house(size=0.6, color=INK):
  body = Square(size, color=color, stroke_width=3)
  roof = Polygon(body.get_corner(UL), body.get_corner(UR), body.get_top() + UP * 0.45 * size,
                 color=color, stroke_width=3)
  door = Rectangle(width=0.22 * size, height=0.4 * size, color=color, stroke_width=2)
  door.move_to(body.get_bottom() + UP * 0.2 * size)
  return VGroup(body, roof, door)


def key_icon(size=0.5, color=TARGET):
  ring = Circle(radius=0.22 * size, color=color, stroke_width=4)
  shaft = Line(ring.get_right(), ring.get_right() + RIGHT * 0.75 * size, color=color, stroke_width=4)
  t1 = Line(shaft.get_end(), shaft.get_end() + DOWN * 0.2 * size, color=color, stroke_width=4)
  t2 = Line(shaft.get_end() + LEFT * 0.22 * size, shaft.get_end() + LEFT * 0.22 * size + DOWN * 0.15 * size,
            color=color, stroke_width=4)
  return VGroup(ring, shaft, t1, t2).move_to(ORIGIN)


def clock_icon(radius=0.4, color=INK):
  face = Circle(radius=radius, color=color, stroke_width=3)
  h1 = Line(ORIGIN, UP * 0.7 * radius, color=color, stroke_width=3)
  h2 = Line(ORIGIN, RIGHT * 0.5 * radius, color=color, stroke_width=3)
  return VGroup(face, h1, h2)


# --------------------------------------------------------------------------------------
# Simulated walker paths (illustration only)
# --------------------------------------------------------------------------------------

DT = 0.01
D_VIS = 0.3
TARGET_Y = 1.0
TAU = 2.5


def bm(seed, n):
  rng = np.random.default_rng(seed)
  return np.concatenate([[0.0], np.cumsum(rng.normal(0, np.sqrt(2 * D_VIS * DT), n))])


def first_hit(p, level=TARGET_Y):
  idx = np.nonzero(p >= level)[0]
  return int(idx[0]) if len(idx) else None


def _find(pred, start=1):
  for seed in range(start, 20000):
    out = pred(seed)
    if out is not None:
      return out
  raise RuntimeError('no seed found')


def _quick(seed):
  p = bm(seed, 800)
  k = first_hit(p)
  if k is not None and 140 <= k <= 220 and p[:k].min() > -0.6 and p[:60].max() < 0.5:
    return p[:k + 1]
  return None


def _wander(seed):
  p = bm(seed, 800)
  k_tau = int(TAU / DT)
  if (first_hit(p) is None and -3.5 < p.min() < -2.3 and p[k_tau] < -1.2 and p[:40].max() < 0.25
      and p[-1] < -1.0):
    return p
  return None


def _fail(seed):
  p = bm(seed, int(TAU / DT))
  if first_hit(p) is None and -1.6 < p.min() and 0.3 < p.max() < 0.85 and -0.9 < p[-1] < 0.2:
    return p
  return None


def _success(seed):
  p = bm(seed, 400)
  k = first_hit(p)
  if k is not None and 90 <= k <= 170 and p[:k].min() > -0.7:
    return p[:k + 1]
  return None


QUICK = _find(_quick)
WANDER = _find(_wander)
FAIL = _find(_fail)
SUCCESS = _find(_success)


def plot_axes():
  ax = Axes(x_range=[0, 8, 1], y_range=[-4, 2, 1], x_length=11, y_length=5.8,
            axis_config={'color': MUTED, 'stroke_width': 2, 'include_ticks': False},
            tips=False).move_to([0.5, -0.35, 0])
  return ax


def path_mob(ax, ys, t0=0.0, color=WALKER, width=3):
  ts = t0 + DT * np.arange(len(ys))
  m = VMobject(color=color, stroke_width=width)
  m.set_points_as_corners([ax.c2p(t, y) for t, y in zip(ts, ys)])
  return m


def plot_frame(ax):
  tlab = T('time', 0.6, MUTED).next_to(ax.x_axis.get_end(), DOWN, buff=0.2).shift(LEFT * 0.3)
  plab = T('position', 0.6, MUTED).next_to(ax.y_axis.get_top(), UP, buff=0.15)
  zero = M('0', 0.6, MUTED).next_to(ax.c2p(0, 0), LEFT, buff=0.15)
  tline = DashedLine(ax.c2p(0, TARGET_Y), ax.c2p(8, TARGET_Y), color=TARGET, stroke_width=3, dash_length=0.12)
  keys = key_icon(0.55).next_to(ax.c2p(0, TARGET_Y), LEFT, buff=0.15)
  return tlab, plab, zero, tline, keys


def tracer(ax, path):
  dot = Dot(radius=0.09, color=WALKER).set_z_index(5)
  dot.add_updater(lambda m: m.move_to(path.get_end()))
  side = Dot(radius=0.11, color=WALKER).set_z_index(5)
  side.add_updater(lambda m: m.move_to(ax.c2p(0, ax.p2c(path.get_end())[1])))
  return dot, side


# --------------------------------------------------------------------------------------
# 1. Hook: lost keys
# --------------------------------------------------------------------------------------

class Keys(NarratedScene):
  def construct(self):
    ground = Line([-6.4, -1.4, 0], [6.4, -1.4, 0], color=MUTED, stroke_width=4)
    home = house(1.4).next_to([-1.5, -1.4, 0], UP, buff=0)
    keys = key_icon(1.1).move_to([-4.6, -1.0, 0]).set_opacity(0.35)
    me = Dot(radius=0.24, color=WALKER).move_to([-1.5, -1.1, 0]).set_z_index(3)
    with self.say('s01_hook') as d:
      self.play(Create(ground), FadeIn(home, shift=0.2 * UP), run_time=0.12 * d)
      self.play(FadeIn(me, scale=0.5), FadeIn(keys), run_time=0.08 * d)
      for x in (0.0, 1.0, 2.6, 3.3, 4.8):
        self.play(me.animate.move_to([x, -1.1, 0]), run_time=0.09 * d, rate_func=smooth)
      a = T('keep going?', 0.9).move_to([4.8, 0.2, 0])
      back = CurvedArrow([4.5, -0.5, 0], [-1.0, 0.6, 0], angle=0.5, color=FLASH, stroke_width=5)
      b = T('or start again?', 0.9, FLASH).move_to([1.7, 2.5, 0])
      self.play(FadeIn(a, shift=0.2 * UP), run_time=0.1 * d)
      self.play(Create(back), FadeIn(b), run_time=0.15 * d)
    with self.say('s01_q') as d:
      self.play(FadeOut(a), run_time=0.1 * d)
      self.play(me.animate.move_to([-1.5, -1.1, 0]), run_time=0.15 * d)
      self.play(me.animate.move_to([-3.6, -1.1, 0]), keys.animate.set_opacity(1), run_time=0.2 * d)
      self.play(Flash(keys, color=TARGET, flash_radius=0.7), run_time=0.15 * d)
      cap = T('restarting can make a search faster on average', 0.85).to_edge(DOWN, buff=0.9)
      self.play(Write(cap), run_time=0.25 * d)
    self.play(*[FadeOut(m) for m in (ground, home, keys, me, back, b, cap)], run_time=0.6)


# --------------------------------------------------------------------------------------
# 2. A random walker
# --------------------------------------------------------------------------------------

class Walker(NarratedScene):
  def construct(self):
    ax = plot_axes()
    y0, y1 = ax.c2p(0, -4)[1], ax.c2p(0, 2)[1]
    length = y1 - y0
    unit = length / 6.0
    # horizontal line with the same scale as the (later) vertical axis, 0 at the screen centre

    big = 1.6

    def n2p(v):
      return np.array([v * unit * big, 0.0, 0.0])
    line = Line(n2p(-4), n2p(2), color=MUTED, stroke_width=3)
    ticks = VGroup(*[Line(n2p(v) + DOWN * 0.08, n2p(v) + UP * 0.08, color=MUTED, stroke_width=2)
                     for v in range(-4, 3)])
    zero = M('0', 0.8, MUTED).next_to(n2p(0), DOWN, buff=0.3)
    home = house(0.8).next_to(n2p(0), UP, buff=0.45)
    keys = key_icon(0.85).next_to(n2p(TARGET_Y), UP, buff=0.5)
    tick_t = Line(n2p(TARGET_Y) + DOWN * 0.18, n2p(TARGET_Y) + UP * 0.18, color=TARGET, stroke_width=5)
    t = ValueTracker(0)
    dot = Dot(radius=0.18, color=WALKER).set_z_index(5)
    dot.add_updater(lambda m: m.move_to(n2p(QUICK[min(int(t.get_value()), len(QUICK) - 1)])))
    coin = VGroup(T('left', 0.8, MUTED), T('or', 0.7, MUTED), T('right', 0.8, MUTED)).arrange(RIGHT, buff=0.3)
    coin.move_to([0, -1.8, 0])
    half = len(QUICK) // 2
    with self.say('s02_walker') as d:
      self.play(Create(line), FadeIn(ticks), FadeIn(zero), run_time=0.15 * d)
      self.play(FadeIn(home), FadeIn(dot, scale=0.5), run_time=0.12 * d)
      self.play(FadeIn(coin), run_time=0.1 * d)
      self.play(t.animate.set_value(half), run_time=0.55 * d, rate_func=linear)
    with self.say('s02_target') as d:
      self.play(FadeIn(keys, shift=0.2 * DOWN), Create(tick_t), run_time=0.2 * d)
      self.play(t.animate.set_value(len(QUICK) - 1), run_time=0.5 * d, rate_func=linear)
      self.play(Flash(dot, color=OURS, flash_radius=0.4), run_time=0.2 * d)
    dot.clear_updaters()

    tlab, plab, zlab, tline, pkeys = plot_frame(ax)
    with self.say('s02_plot') as d:
      grp = VGroup(line, ticks, tick_t)
      self.play(FadeOut(coin), FadeOut(home), FadeOut(zero), FadeOut(keys), FadeOut(dot), run_time=0.08 * d)
      self.play(grp.animate.scale(1 / big, about_point=ORIGIN).rotate(PI / 2, about_point=ORIGIN)
                .shift(ax.c2p(0, 0) - ORIGIN), run_time=0.15 * d)
      self.play(ReplacementTransform(line, ax.y_axis), FadeOut(ticks), FadeOut(tick_t), Create(ax.x_axis),
                FadeIn(tlab), FadeIn(plab), FadeIn(zlab), run_time=0.12 * d)
      self.play(Create(tline), FadeIn(pkeys), run_time=0.1 * d)
      p1 = path_mob(ax, QUICK)
      dt_, side = tracer(ax, p1)
      self.add(dt_, side)
      self.play(Create(p1), run_time=0.35 * d, rate_func=linear)
      self.play(Flash(dt_, color=OURS, flash_radius=0.35), run_time=0.12 * d)
    dt_.clear_updaters()
    side.clear_updaters()

    with self.say('s02_wander') as d:
      self.play(p1.animate.set_stroke(opacity=0.25), FadeOut(dt_), run_time=0.08 * d)
      p2 = path_mob(ax, WANDER)
      d2, s2 = tracer(ax, p2)
      self.remove(side)
      self.add(d2, s2)
      self.play(Create(p2), run_time=0.75 * d, rate_func=linear)
      arr = T('still searching...', 0.7, BAD).move_to(ax.c2p(6.4, -3.6))
      self.play(FadeIn(arr), run_time=0.1 * d)
    d2.clear_updaters()
    s2.clear_updaters()
    self.play(*[FadeOut(m) for m in (ax.x_axis, ax.y_axis, tlab, plab, zlab, tline, pkeys, p1, p2, d2, s2, arr)],
              run_time=0.6)


# --------------------------------------------------------------------------------------
# 3. Average search time (no restart)
# --------------------------------------------------------------------------------------

class Average(NarratedScene):
  def construct(self):
    rng = np.random.default_rng(4)
    z = rng.standard_normal(20000)
    times = 1.0 / (2 * z ** 2)  # first hit of x = 1 with D = 1 (Levy law)
    bins = np.linspace(0, 8, 21)
    counts, _ = np.histogram(times, bins=bins)
    frac = counts / len(times)
    ax = Axes(x_range=[0, 8.8, 1], y_range=[0, 1.12 * frac.max(), 0.05], x_length=10, y_length=4.8,
              axis_config={'color': MUTED, 'stroke_width': 2, 'include_ticks': False}, tips=False)
    ax.move_to([-0.3, -0.1, 0])
    xl = T('search time', 0.65, MUTED).next_to(ax.x_axis, DOWN, buff=0.3)
    yl = T('how often', 0.65, MUTED).next_to(ax.y_axis.get_top(), UP, buff=0.15)
    bars = VGroup()
    for k, f in enumerate(frac):
      x0, x1 = bins[k], bins[k + 1]
      r = Rectangle(width=ax.c2p(x1, 0)[0] - ax.c2p(x0, 0)[0] - 0.04, height=max(ax.c2p(0, f)[1] - ax.c2p(0, 0)[1], 0.01),
                    stroke_width=0, fill_color=WALKER, fill_opacity=0.85)
      r.move_to(ax.c2p((x0 + x1) / 2, 0), aligned_edge=DOWN)
      bars.add(r)
    with self.say('s03_hist') as d:
      self.play(Create(ax), FadeIn(xl), FadeIn(yl), run_time=0.15 * d)
      self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.08), run_time=0.5 * d)
      tail = Arrow(ax.c2p(6.2, 0.04), ax.c2p(8.8, 0.04), color=FLASH, buff=0, stroke_width=4)
      tl = T('rare, very long searches', 0.65, FLASH).next_to(tail, UP, buff=0.15)
      self.play(GrowArrow(tail), FadeIn(tl), run_time=0.2 * d)

    cm = np.cumsum(times) / np.arange(1, len(times) + 1)
    checkpoints = np.unique(np.geomspace(10, len(times), 60).astype(int)) - 1
    k = ValueTracker(0)
    lab = T('average so far:', 0.7).move_to([2.2, 2.6, 0])
    num = always_redraw(lambda: DecimalNumber(cm[checkpoints[int(k.get_value())]], num_decimal_places=1,
                                              color=BAD).scale(0.85).next_to(lab, RIGHT, buff=0.25))
    with self.say('s03_inf') as d:
      self.play(FadeIn(lab), FadeIn(num), run_time=0.1 * d)
      self.play(k.animate.set_value(len(checkpoints) - 1), run_time=0.5 * d, rate_func=linear)
      inf = M(r'\text{average} = \infty', 1.0, BAD).move_to([2.2, 1.6, 0])
      self.play(Write(inf), run_time=0.15 * d)
      note = T('a classic fact, long known', 0.6, MUTED).next_to(inf, DOWN, buff=0.25)
      self.play(FadeIn(note), run_time=0.1 * d)
    self.play(*[FadeOut(m) for m in (ax, xl, yl, bars, tail, tl, lab, num, inf, note)], run_time=0.6)


# --------------------------------------------------------------------------------------
# 4. Restarting
# --------------------------------------------------------------------------------------

class Restart(NarratedScene):
  def construct(self):
    ax = plot_axes()
    tlab, plab, zlab, tline, pkeys = plot_frame(ax)
    ghost = path_mob(ax, WANDER).set_stroke(opacity=0.22)
    self.add(ax.x_axis, ax.y_axis, tlab, plab, zlab, tline, pkeys)
    clock = clock_icon(0.38).move_to([5.6, 3.2, 0])
    rule = VGroup(T('timer rings $\\Rightarrow$', 0.7), T('jump back to 0, start afresh', 0.7, FLASH)) \
      .arrange(RIGHT, buff=0.2).move_to([-0.4, 3.2, 0])
    with self.say('s04_rule') as d:
      self.play(FadeIn(ghost), run_time=0.15 * d)
      self.play(FadeIn(clock, scale=0.6), run_time=0.15 * d)
      self.play(Write(rule), run_time=0.4 * d)

    k = int(TAU / DT)
    a1 = path_mob(ax, WANDER[:k + 1])
    a2 = path_mob(ax, FAIL, t0=TAU)
    a3 = path_mob(ax, SUCCESS, t0=2 * TAU)
    drops = [DashedLine(ax.c2p(TAU, WANDER[k]), ax.c2p(TAU, 0), color=RESET, stroke_width=3, dash_length=0.1),
             DashedLine(ax.c2p(2 * TAU, FAIL[-1]), ax.c2p(2 * TAU, 0), color=RESET, stroke_width=3, dash_length=0.1)]
    marks = VGroup(*[DashedLine(ax.c2p(TAU * j, -4), ax.c2p(TAU * j, 2), color=RESET, stroke_width=1.5,
                                dash_length=0.06, stroke_opacity=0.6) for j in (1, 2)])
    with self.say('s04_cut') as d:
      self.play(Create(marks), run_time=0.06 * d)
      for path, drop in ((a1, drops[0]), (a2, drops[1])):
        dot, side = tracer(ax, path)
        self.add(dot, side)
        self.play(Create(path), run_time=0.22 * d, rate_func=linear)
        self.play(Wiggle(clock, scale_value=1.2), Flash(dot, color=FLASH, flash_radius=0.3), run_time=0.07 * d)
        dot.clear_updaters()
        side.clear_updaters()
        self.play(Create(drop), dot.animate.move_to(ax.c2p(TAU if path is a1 else 2 * TAU, 0)),
                  side.animate.move_to(ax.c2p(0, 0)), run_time=0.05 * d)
        self.remove(dot, side)
      dot, side = tracer(ax, a3)
      self.add(dot, side)
      self.play(Create(a3), run_time=0.15 * d, rate_func=linear)
      self.play(Flash(dot, color=OURS, flash_radius=0.4), run_time=0.08 * d)
    dot.clear_updaters()
    side.clear_updaters()

    with self.say('s04_finite') as d:
      self.play(FadeOut(ghost), run_time=0.1 * d)
      res = M(r'\text{average search time: } {{\infty}} \;\longrightarrow\; {{\text{finite}}}', 0.95)
      res[1].set_color(BAD)
      res[3].set_color(OURS)
      box = BackgroundRectangle(res, color=BACKGROUND, fill_opacity=0.9, buff=0.2)
      g = VGroup(box, res).move_to([0.5, -2.6, 0])
      self.play(FadeIn(box), Write(res), run_time=0.5 * d)
    self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6)


# --------------------------------------------------------------------------------------
# 5. Restart recipes
# --------------------------------------------------------------------------------------

def wait_row(lengths, color, y, x0=-3.6, scale=0.85):
  bars, x = VGroup(), x0
  for L in lengths:
    r = Rectangle(width=max(L * scale - 0.06, 0.05), height=0.42, stroke_width=0, fill_color=color, fill_opacity=0.85)
    r.move_to([x + L * scale / 2, y, 0])
    bell = Line([x + L * scale, y - 0.32, 0], [x + L * scale, y + 0.32, 0], color=FLASH, stroke_width=3)
    bars.add(VGroup(r, bell))
    x += L * scale
  return bars


class Timers(NarratedScene):
  def construct(self):
    fixed = wait_row([1.6] * 6, RESET, 1.6)
    rng = np.random.default_rng(3)
    rand_l = list(rng.exponential(1.6, 12))
    acc, cut = 0.0, []
    for L in rand_l:
      if acc + L > 9.6:
        break
      cut.append(L)
      acc += L
    rnd = wait_row(cut, OURS, 0.0)
    blend_l = [1.6, 0.4, 1.6, 2.7, 1.6, 0.7, 1.6]
    blend = wait_row(blend_l, RIVAL, -1.6)
    l1 = T('fixed timer', 0.7).next_to(fixed, LEFT, buff=0.4)
    l2 = T('random timer', 0.7, OURS).next_to(rnd, LEFT, buff=0.4).align_to(l1, RIGHT)
    l3 = T('a blend', 0.7, RIVAL).next_to(blend, LEFT, buff=0.4).align_to(l1, RIGHT)
    head = T('waits between restarts', 0.65, MUTED).to_edge(UP, buff=0.8)
    with self.say('s05_fixed') as d:
      self.play(FadeIn(head), FadeIn(l1), run_time=0.2 * d)
      self.play(LaggedStart(*[FadeIn(b, shift=0.1 * RIGHT) for b in fixed], lag_ratio=0.3), run_time=0.6 * d)
    with self.say('s05_random') as d:
      self.play(FadeIn(l2), run_time=0.1 * d)
      self.play(LaggedStart(*[FadeIn(b, shift=0.1 * RIGHT) for b in rnd], lag_ratio=0.3), run_time=0.7 * d)
    with self.say('s05_recipe') as d:
      self.play(FadeIn(l3), LaggedStart(*[FadeIn(b, shift=0.1 * RIGHT) for b in blend], lag_ratio=0.3),
                run_time=0.45 * d)
      cap = T('recipe = a rule for picking each wait, fresh every time', 0.7, FLASH).to_edge(DOWN, buff=0.7)
      self.play(Write(cap), run_time=0.35 * d)
    self.play(*[FadeOut(m) for m in (fixed, rnd, blend, l1, l2, l3, head, cap)], run_time=0.5)

    blocks = VGroup()
    for j in range(4):
      ok = j == 3
      r = RoundedRectangle(width=2.0, height=1.0, corner_radius=0.12, stroke_color=OURS if ok else RESET,
                           stroke_width=3, fill_color=OURS if ok else RESET, fill_opacity=0.25)
      lab = T('2 s', 0.7).move_to(r)
      mark = M(r'\checkmark' if ok else r'\times', 0.8, OURS if ok else BAD).next_to(r, UP, buff=0.2)
      blocks.add(VGroup(r, lab, mark))
    blocks.arrange(RIGHT, buff=0.25).move_to([0, 1.2, 0])
    br = Brace(blocks, DOWN, buff=0.25, color=INK)
    tot = M(r'4 \times 2\text{ s} = 8\text{ s}', 0.9).next_to(br, DOWN, buff=0.25)
    chance = T('one in four attempts succeeds', 0.65, OURS).next_to(blocks, UP, buff=0.8)
    with self.say('s05_ratio') as d:
      self.play(LaggedStart(*[FadeIn(b[0]) for b in blocks], lag_ratio=0.3),
                LaggedStart(*[FadeIn(b[1]) for b in blocks], lag_ratio=0.3), run_time=0.3 * d)
      self.play(LaggedStart(*[FadeIn(b[2], scale=0.6) for b in blocks], lag_ratio=0.3), FadeIn(chance), run_time=0.3 * d)
      self.play(GrowFromCenter(br), Write(tot), run_time=0.3 * d)
    num = T('average attempt length', 0.8)
    den = T('success chance', 0.8, OURS)
    bar = Line(LEFT, RIGHT, color=INK, stroke_width=3).set_width(num.width + 0.2)
    frac = VGroup(num, bar, den).arrange(DOWN, buff=0.15)
    formula = VGroup(T('average search time', 0.8), M('=', 0.9), frac).arrange(RIGHT, buff=0.3)
    formula.move_to([0, -2.5, 0])
    with self.say('s05_formula') as d:
      self.play(Write(formula), run_time=0.7 * d)
      self.play(Circumscribe(formula, color=FLASH), run_time=0.25 * d)
    self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6)


# --------------------------------------------------------------------------------------
# 6. The optimisation question
# --------------------------------------------------------------------------------------

def cost_exp(r):
  """Map-average search time for a random timer of rate r, map 2e^{-2x}, D = 1."""
  s = np.sqrt(r)
  return 1.0 / (s * (2 - s))


class Question(NarratedScene):
  def construct(self):
    ax = Axes(x_range=[0, 3, 1], y_range=[0, 2.2, 1], x_length=8.5, y_length=4.8,
              axis_config={'color': MUTED, 'stroke_width': 2, 'include_ticks': False}, tips=False)
    ax.move_to([0, -0.3, 0])
    xl = T('distance from the start', 0.65, MUTED).next_to(ax.x_axis, DOWN, buff=0.3)
    yl = T('chance', 0.65, MUTED).next_to(ax.y_axis.get_top(), UP, buff=0.15)
    mp = ax.plot(lambda x: 2 * np.exp(-2 * x), x_range=[0, 3], color=TARGET, stroke_width=5)
    area = ax.get_area(mp, x_range=[0, 3], color=TARGET, opacity=0.25)
    lab = T('where the target might be', 0.7, TARGET).move_to(ax.c2p(1.7, 1.5))
    keys = key_icon(0.55).next_to(lab, LEFT, buff=0.3)
    with self.say('s06_map') as d:
      self.play(Create(ax), FadeIn(xl), FadeIn(yl), run_time=0.2 * d)
      self.play(Create(mp), FadeIn(area), run_time=0.4 * d)
      self.play(FadeIn(lab), FadeIn(keys), run_time=0.2 * d)
    self.play(*[FadeOut(m) for m in (ax, xl, yl, mp, area, lab, keys)], run_time=0.5)

    bx = Axes(x_range=[0, 4, 1], y_range=[0, 4, 1], x_length=8.5, y_length=5.0,
              axis_config={'color': MUTED, 'stroke_width': 2, 'include_numbers': True, 'font_size': 30},
              tips=False).move_to([0.3, -0.3, 0])
    bxl = T('restart rate of a random timer', 0.65, MUTED).next_to(bx.x_axis, DOWN, buff=0.55)
    byl = T('average search time', 0.65, MUTED).next_to(bx.y_axis.get_top(), UP, buff=0.15)
    curve = bx.plot(cost_exp, x_range=[0.025, 3.45, 0.005], color=INK, stroke_width=4)
    r = ValueTracker(0.12)
    dot = always_redraw(lambda: Dot(bx.c2p(r.get_value(), cost_exp(r.get_value())), radius=0.1, color=FLASH))
    rare = T('too rarely', 0.65, BAD).move_to(bx.c2p(0.75, 3.3))
    often = T('too often', 0.65, BAD).move_to(bx.c2p(2.6, 3.3))
    with self.say('s06_curve') as d:
      self.play(Create(bx), FadeIn(bxl), FadeIn(byl), run_time=0.15 * d)
      self.play(Create(curve), run_time=0.2 * d)
      self.add(dot)
      self.play(FadeIn(rare), run_time=0.08 * d)
      self.play(r.animate.set_value(3.3), run_time=0.2 * d)
      self.play(FadeIn(often), run_time=0.08 * d)
      self.play(r.animate.set_value(1.0), run_time=0.15 * d)
      best = Dot(bx.c2p(1, 1), radius=0.13, color=OURS)
      bl = M(r'\text{rate } 1 \Rightarrow \text{average } 1', 0.75, OURS).next_to(best, DOWN, buff=0.35)
      self.play(FadeIn(best, scale=0.5), FadeIn(bl), run_time=0.1 * d)
    with self.say('s06_ponder') as d:
      grp = VGroup(bx, bxl, byl, curve, best, rare, often)
      self.remove(dot)
      summ = M(r'\text{best random timer: average } 1', 0.85, OURS).to_edge(UP, buff=0.8)
      self.play(FadeOut(grp), ReplacementTransform(bl, summ), run_time=0.15 * d)
      rivals = VGroup(T('a fixed timer?', 0.8), T('a strange blend?', 0.8, RIVAL),
                      T('any recipe at all?', 0.8, FLASH)).arrange(DOWN, buff=0.55)
      rivals.move_to([0, 0.2, 0])
      self.play(LaggedStart(*[FadeIn(m, shift=0.2 * LEFT) for m in rivals], lag_ratio=0.5), run_time=0.45 * d)
      q = M('?', 2.2, FLASH).next_to(rivals, DOWN, buff=0.5)
      self.play(FadeIn(q, scale=0.5), run_time=0.15 * d)
    self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6)


# --------------------------------------------------------------------------------------
# 7. Evans and Ray: the conjugate map (prior work)
# --------------------------------------------------------------------------------------

class Conjugate(NarratedScene):
  def construct(self):
    who = T('Evans and Ray, 2025', 0.75, MUTED).to_edge(UP, buff=0.6)
    a = T('recipe', 0.85, OURS)
    b = T('map', 0.85, TARGET)
    arr = Arrow(LEFT, RIGHT, color=INK, buff=0)
    flip = VGroup(a, arr, b).arrange(RIGHT, buff=0.4).move_to([0, 1.6, 0])
    qn = T('for which map is this recipe the natural choice?', 0.7).next_to(flip, DOWN, buff=0.5)
    with self.say('s07_flip') as d:
      self.play(FadeIn(who), run_time=0.15 * d)
      self.play(FadeIn(a), GrowArrow(arr), FadeIn(b), run_time=0.35 * d)
      self.play(FadeIn(qn), run_time=0.3 * d)
    self.play(FadeOut(qn), FadeOut(flip), run_time=0.4)

    ax = Axes(x_range=[0, 3, 1], y_range=[0, 2.2, 1], x_length=8.5, y_length=4.8,
              axis_config={'color': MUTED, 'stroke_width': 2, 'include_ticks': False}, tips=False)
    ax.move_to([-0.6, -0.5, 0])
    xl = T('distance of the target', 0.65, MUTED).next_to(ax.x_axis, DOWN, buff=0.3)
    one = M('1', 0.65, MUTED).next_to(ax.c2p(0, 1), LEFT, buff=0.15)
    tick1 = Line(ax.c2p(0, 1) + LEFT * 0.08, ax.c2p(0, 1) + RIGHT * 0.08, color=MUTED, stroke_width=2)
    f = ax.plot(lambda x: np.exp(-x), x_range=[0, 3], color=OURS, stroke_width=5)
    fl = M(r'\text{success chance } f(x)', 0.75, OURS).move_to(ax.c2p(2.0, 1.0))
    with self.say('s07_f') as d:
      self.play(Create(ax), FadeIn(xl), FadeIn(one), FadeIn(tick1), run_time=0.2 * d)
      self.play(Create(f), run_time=0.4 * d)
      self.play(FadeIn(fl), run_time=0.15 * d)
      self.play(Indicate(fl, color=FLASH), run_time=0.15 * d)
    f2 = ax.plot(lambda x: np.exp(-2 * x), x_range=[0, 3], color=FLASH, stroke_width=5)
    f2l = M(r'f(x)^2', 0.8, FLASH).move_to(ax.c2p(0.85, 0.55))
    pm = ax.plot(lambda x: 2 * np.exp(-2 * x), x_range=[0, 3], color=TARGET, stroke_width=5)
    pml = T('conjugate map: our map', 0.75, TARGET).move_to(ax.c2p(1.85, 1.55))
    with self.say('s07_square') as d:
      fcopy = f.copy()
      self.play(Transform(fcopy, f2), FadeIn(f2l), f.animate.set_stroke(opacity=0.35), fl.animate.set_opacity(0.4),
                run_time=0.3 * d)
      sc = T('rescale so the total chance is 1', 0.65, MUTED).to_edge(UP, buff=0.6)
      self.play(FadeOut(who), FadeIn(sc), run_time=0.1 * d)
      self.play(Transform(fcopy, pm), FadeOut(f2l), run_time=0.25 * d)
      self.play(FadeIn(pml), run_time=0.2 * d)
    self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.5)

    def g(x):
      return 0.06 * x ** 4 - 0.55 * x ** 2 - 0.35 * x
    land_ax = Axes(x_range=[-3.3, 3.4], y_range=[-2.4, 2.2], x_length=11, y_length=4.6, tips=False,
                   axis_config={'stroke_opacity': 0}).move_to([0, 0.1, 0])
    land = land_ax.plot(g, x_range=[-3.3, 3.4], color=MUTED, stroke_width=4)
    xa = -2.0
    ball = Dot(land_ax.c2p(xa, g(xa)) + UP * 0.2, radius=0.2, color=OURS)
    bal = T('balanced: tiny tweaks do not help', 0.7, OURS).next_to(ball, UP, buff=0.5).shift(RIGHT * 0.6)
    deep = land_ax.c2p(2.27, g(2.27))
    q = M('?', 1.6, FLASH).move_to(deep + UP * 0.9)
    with self.say('s07_flat') as d:
      self.play(Create(land), run_time=0.3 * d)
      self.play(FadeIn(ball, scale=0.5), FadeIn(bal), run_time=0.25 * d)
      self.play(FadeIn(q, scale=0.5), Indicate(land, color=FLASH), run_time=0.3 * d)
    with self.say('s07_checks') as d:
      self.play(FadeOut(bal), run_time=0.1 * d)
      c1 = T('their checks: numerical, inside two families of timers', 0.7).to_edge(UP, buff=0.5)
      c2 = T('still open: the best of \\emph{all} recipes?', 0.75, FLASH).next_to(c1, DOWN, buff=0.35)
      self.play(FadeIn(c1), run_time=0.35 * d)
      self.play(FadeIn(c2), run_time=0.35 * d)
    self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6)


# --------------------------------------------------------------------------------------
# 8. The new theorem
# --------------------------------------------------------------------------------------

class Result(NarratedScene):
  def construct(self):
    head = T(r'\textbf{New theorem} (walker on a line)', 0.85, OURS)
    l1 = T(r'On its own conjugate map, a recipe', 0.8)
    l2 = T(r'beats every other recipe, and is the \emph{only} best.', 0.8)
    cond = T(r'(whenever that map makes sense and its average time is finite)', 0.6, MUTED)
    body = VGroup(head, l1, l2, cond).arrange(DOWN, buff=0.3)
    panel = card(body, color=OURS).scale(1.15).move_to([0, 1.1, 0])
    with self.say('s08_thm') as d:
      self.play(FadeIn(panel[0]), FadeIn(head), run_time=0.15 * d)
      self.play(Write(l1), run_time=0.25 * d)
      self.play(Write(l2), run_time=0.3 * d)
      self.play(FadeIn(cond), run_time=0.15 * d)
    items = VGroup(
      VGroup(M(r'\checkmark', 0.8, OURS), T('any positive, finite waits, picked independently', 0.7)),
      VGroup(M(r'\times', 0.8, BAD), T('smart restarts that react to the walker', 0.7)),
      VGroup(M(r'\times', 0.8, BAD), T('restarts that cost extra time', 0.7)),
    )
    for it in items:
      it.arrange(RIGHT, buff=0.3)
    items.arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to([0, -2.1, 0])
    with self.say('s08_scope') as d:
      self.play(LaggedStart(*[FadeIn(it, shift=0.2 * UP) for it in items], lag_ratio=0.6), run_time=0.85 * d)
    self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6)


# --------------------------------------------------------------------------------------
# 9. The key idea: a symmetric weight and a sum of squares
# --------------------------------------------------------------------------------------

class KeyIdea(NarratedScene):
  def construct(self):
    top = MathTex(r'h(x)', '=', r'\text{add up over } y:', r'\;\min(x,y)', r'\times', r'f(y)').scale(0.9)
    top[0].set_color(OURS)
    top[5].set_color(OURS)
    top[3].set_color(FLASH)
    top.to_edge(UP, buff=0.8)
    hl = T('attempt length', 0.6, OURS).next_to(top[0], DOWN, buff=0.2)
    fl = T('success chance', 0.6, OURS).next_to(top[5], DOWN, buff=0.2)
    line = NumberLine(x_range=[0, 4, 1], length=11, color=MUTED, include_ticks=False, stroke_width=3)
    line.move_to([0, -1.9, 0])
    px, py = 1.0, 3.0
    dx = Dot(line.n2p(px), radius=0.16, color=INK)
    dy = Dot(line.n2p(py), radius=0.16, color=INK)
    lx = M('x', 1.1).next_to(dx, DOWN, buff=0.3)
    ly = M('y', 1.1).next_to(dy, DOWN, buff=0.3)
    arc = ArcBetweenPoints(line.n2p(px), line.n2p(py), angle=-PI / 2, color=FLASH, stroke_width=5)
    wl = M(r'\text{weight} = \min(x, y)', 1.0, FLASH).next_to(arc, UP, buff=0.3)
    with self.say('s09_sym') as d:
      self.play(Write(top), FadeIn(hl), FadeIn(fl), run_time=0.3 * d)
      self.play(Create(line), FadeIn(dx), FadeIn(dy), FadeIn(lx), FadeIn(ly), run_time=0.15 * d)
      self.play(Create(arc), FadeIn(wl), run_time=0.2 * d)
      self.play(Swap(lx, ly), run_time=0.15 * d)
      self.play(Indicate(wl, color=FLASH), run_time=0.12 * d)
    self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.5)

    def pair_card(label, frac):
      head = T(label, 0.7, MUTED)
      body = MathTex(r'w', r'\times', frac).scale(1.1)
      grp = VGroup(head, body).arrange(DOWN, buff=0.3)
      return card(grp, color=RIVAL).scale(1.35)
    c1 = pair_card(r'pair $(x, y)$', r'\frac{u}{v}').move_to([-3.4, 0.9, 0])
    c2 = pair_card(r'pair $(y, x)$', r'\frac{v}{u}').move_to([3.4, 0.9, 0])
    legend = VGroup(T(r'$u, v$ = rival success $\div$ our success, at the two distances', 0.75),
                    T(r'$w$ = the same symmetric weight for both', 0.75)).arrange(DOWN, buff=0.3)
    legend.move_to([0, -1.9, 0])
    with self.say('s09_pairs') as d:
      self.play(FadeIn(legend[0]), run_time=0.25 * d)
      self.play(FadeIn(c1, shift=0.2 * RIGHT), run_time=0.2 * d)
      self.play(FadeIn(c2, shift=0.2 * LEFT), run_time=0.2 * d)
      self.play(FadeIn(legend[1]), run_time=0.2 * d)

    lhs = MathTex(r'\frac{u}{v}', '+', r'\frac{v}{u}').scale(1.3).move_to([0, 0.6, 0])
    full = MathTex(r'\frac{u}{v}', '+', r'\frac{v}{u}', '=', '2', '+', r'\frac{(u-v)^2}{uv}').scale(1.3)
    full.move_to([0, 0.6, 0])
    with self.say('s09_identity') as d:
      self.play(FadeOut(legend), ReplacementTransform(c1[1][1][2], lhs[0]), ReplacementTransform(c2[1][1][2], lhs[2]),
                FadeIn(lhs[1]),
                FadeOut(c1[0]), FadeOut(c2[0]), FadeOut(c1[1][0]), FadeOut(c2[1][0]),
                FadeOut(c1[1][1][:2]), FadeOut(c2[1][1][:2]), run_time=0.3 * d)
      self.play(TransformMatchingTex(lhs, full), run_time=0.4 * d)
      self.play(full[6].animate.set_color(FLASH), run_time=0.2 * d)

    n1 = MathTex(r'\frac{2}{1}', '+', r'\frac{1}{2}', '=', '2.5').scale(1.0)
    n2 = MathTex('2', '+', r'\frac{(2-1)^2}{2 \times 1}', '=', '2.5').scale(1.0)
    nums = VGroup(n1, n2).arrange(RIGHT, buff=1.4).move_to([0, -1.8, 0])
    sub = T(r'$u = 2,\ v = 1$', 0.7, MUTED).next_to(nums, UP, buff=0.35)
    with self.say('s09_check') as d:
      self.play(FadeIn(sub), run_time=0.15 * d)
      self.play(Write(n1), run_time=0.3 * d)
      self.play(Write(n2), run_time=0.35 * d)
      self.play(Indicate(n1[4], color=OURS), Indicate(n2[4], color=OURS), run_time=0.15 * d)

    ge = MathTex(r'\text{rival cost}', '=', r'\text{our cost}', '+', r'\frac{\text{squares}}{\text{positives}}').scale(1.0)
    ge[2].set_color(OURS)
    ge[4].set_color(FLASH)
    ge.move_to([0, -1.6, 0])
    ge_b = Brace(ge[4], DOWN, color=FLASH, buff=0.15)
    ge_l = M(r'\ge 0', 0.85, FLASH).next_to(ge_b, DOWN, buff=0.12)
    with self.say('s09_ge') as d:
      self.play(FadeOut(nums), FadeOut(sub), run_time=0.1 * d)
      self.play(Indicate(full[4], color=OURS), run_time=0.15 * d)
      self.play(Write(ge[:3]), run_time=0.25 * d)
      self.play(Write(ge[3:]), GrowFromCenter(ge_b), FadeIn(ge_l), run_time=0.25 * d)
      verdict = T('no rival can beat it', 0.8, OURS).next_to(full, UP, buff=0.6)
      self.play(FadeIn(verdict), run_time=0.15 * d)
    self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.5)

    ax = Axes(x_range=[0, 3, 1], y_range=[0, 1.1, 1], x_length=7.5, y_length=3.8,
              axis_config={'color': MUTED, 'stroke_width': 2, 'include_ticks': False}, tips=False)
    ax.move_to([-2.0, -0.6, 0])
    ours = ax.plot(lambda x: np.exp(-x), x_range=[0, 3], color=OURS, stroke_width=5)
    rival = ax.plot(lambda x: 0.4 * np.exp(-np.sqrt(0.2) * x) + 0.6 * np.exp(-np.sqrt(5) * x), x_range=[0, 3],
                    color=RIVAL, stroke_width=5)
    lo = T('ours', 0.65, OURS).next_to(ax.c2p(3, np.exp(-3)), RIGHT, buff=0.2).shift(DOWN * 0.15)
    lr = T('rival', 0.65, RIVAL).next_to(ax.c2p(3, 0.4 * np.exp(-np.sqrt(0.2) * 3)), RIGHT, buff=0.2)
    z = M(r'\text{leftover} = 0', 0.85, FLASH).move_to([3.9, 1.6, 0])
    imp = M(r'\Downarrow', 0.9, MUTED).next_to(z, DOWN, buff=0.25)
    same = T('same success curve', 0.75, OURS).next_to(imp, DOWN, buff=0.25)
    imp2 = M(r'\Downarrow', 0.9, MUTED).next_to(same, DOWN, buff=0.25)
    tim = T('same timer (a fingerprint)', 0.75, OURS).next_to(imp2, DOWN, buff=0.25)
    with self.say('s09_unique') as d:
      self.play(Create(ax), Create(ours), Create(rival), FadeIn(lo), FadeIn(lr), run_time=0.2 * d)
      self.play(FadeIn(z), run_time=0.12 * d)
      self.play(Transform(rival, ours.copy().set_color(RIVAL).set_stroke(width=3)), FadeOut(lr), FadeIn(imp),
                FadeIn(same), run_time=0.3 * d)
      self.play(FadeIn(imp2), FadeIn(tim), run_time=0.2 * d)
    self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.5)

    k1 = VGroup(T(r'\textbf{known}', 0.75, MUTED),
                T(r'the pairing trick for symmetric weights', 0.7),
                T(r'(close version: D\'avila and Topp, 2023)', 0.6, MUTED)).arrange(DOWN, buff=0.2)
    k2 = VGroup(T(r'\textbf{new here}', 0.75, OURS),
                T(r'global best and uniqueness on a line,', 0.7),
                T(r'even against rivals with infinite average time', 0.7)).arrange(DOWN, buff=0.2)
    col = VGroup(card(k1, color=MUTED), card(k2, color=OURS)).arrange(DOWN, buff=0.5)
    with self.say('s09_credit') as d:
      self.play(FadeIn(col[0], shift=0.2 * UP), run_time=0.35 * d)
      self.play(FadeIn(col[1], shift=0.2 * UP), run_time=0.35 * d)
    self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6)


# --------------------------------------------------------------------------------------
# 10. The running example, with the verification numbers
# --------------------------------------------------------------------------------------

class Example(NarratedScene):
  def construct(self):
    entries = DATA['brownianExponentialTarget']
    ours, q1, q2, mix = (e['cost'] for e in entries[:4])
    blends = [e['cost'] for e in entries[4:]]
    lo_y, hi_y = 0.9, 1.62
    ax = Axes(x_range=[0, 6, 1], y_range=[lo_y, hi_y, 0.1], x_length=10.5, y_length=5.2, tips=False,
              axis_config={'color': MUTED, 'stroke_width': 2},
              y_axis_config={'include_numbers': True, 'font_size': 30, 'decimal_number_config': {'num_decimal_places': 1}},
              x_axis_config={'include_ticks': False}).move_to([0.2, -0.2, 0])
    yl = T('average search time (axis starts at 0.9)', 0.6, MUTED).next_to(ax.y_axis.get_top(), UP, buff=0.2)
    yl.align_to(ax.y_axis, LEFT)
    best_line = DashedLine(ax.c2p(0, 1), ax.c2p(6, 1), color=OURS, stroke_width=3, dash_length=0.12)
    head = T('our map: best recipe is the random timer with rate 1', 0.7, OURS).to_edge(UP, buff=0.4)
    p0 = Dot(ax.c2p(0.7, ours), radius=0.13, color=OURS)
    l0 = M(r'\text{rate } 1:\ 1', 0.75, OURS).next_to(p0, DOWN, buff=0.3)
    with self.say('s10_ex') as d:
      self.play(FadeIn(head), run_time=0.2 * d)
      self.play(Create(ax), FadeIn(yl), run_time=0.25 * d)
      self.play(Create(best_line), FadeIn(p0, scale=0.5), FadeIn(l0), run_time=0.35 * d)

    def pt(x, y, txt, color=RIVAL, side=UP):
      dot = Dot(ax.c2p(x, y), radius=0.11, color=color)
      lab = M(txt, 0.7, color).next_to(dot, side, buff=0.2)
      return VGroup(dot, lab)
    a = pt(1.5, q1, r'\text{rate } 1/4:\ 4/3')
    b = pt(2.55, q2, r'\text{rate } 9/4:\ 4/3', side=DOWN)
    c = pt(3.75, mix, r'\text{blend of 2}:\ %.2f' % mix, side=DOWN)
    rng = np.random.default_rng(1)
    jit = rng.uniform(-0.22, 0.22, len(blends))
    cloud = VGroup(*[Dot(ax.c2p(5.0 + j, y), radius=0.06, color=RIVAL) for j, y in zip(jit, blends)])
    cl = M(r'36\text{ random blends}', 0.65, RIVAL).next_to(ax.c2p(5.0, hi_y), DOWN, buff=0.15)
    rng_l = M(r'%.3f \text{ to } %.3f' % (min(blends), max(blends)), 0.65, RIVAL).next_to(cl, DOWN, buff=0.15)
    with self.say('s10_bars') as d:
      self.play(FadeIn(a, shift=0.1 * UP), run_time=0.15 * d)
      self.play(FadeIn(b, shift=0.1 * UP), run_time=0.15 * d)
      self.play(FadeIn(c, shift=0.1 * UP), run_time=0.15 * d)
      self.play(LaggedStart(*[FadeIn(p, scale=0.5) for p in cloud], lag_ratio=0.05), FadeIn(cl), run_time=0.3 * d)
      self.play(FadeIn(rng_l), run_time=0.1 * d)
    arr = Arrow(ax.c2p(5.85, 1.15), ax.c2p(5.85, hi_y + 0.08), color=BAD, buff=0, stroke_width=5)
    fl = VGroup(T('fixed timer', 0.7, BAD), M(r'\infty', 0.9, BAD)).arrange(DOWN, buff=0.1).next_to(arr, DOWN, buff=0.1)
    own = T('our own quick calculation, not in the paper', 0.55, MUTED).to_edge(DOWN, buff=0.35)
    with self.say('s10_fixed') as d:
      self.play(GrowArrow(arr), FadeIn(fl), run_time=0.4 * d)
      self.play(FadeIn(own), run_time=0.3 * d)
    with self.say('s10_proof') as d:
      self.play(FadeOut(own), run_time=0.1 * d)
      cap = T('checks agree, but only the proof covers every recipe', 0.7, FLASH).to_edge(DOWN, buff=0.35)
      self.play(FadeIn(cap), run_time=0.4 * d)
    self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6)


# --------------------------------------------------------------------------------------
# 11. Rooms: the finite-state reversibility characterisation
# --------------------------------------------------------------------------------------

ROOM_POS = {1: np.array([-1.9, -1.25, 0]), 2: np.array([0.0, 1.3, 0]), 3: np.array([1.9, -1.25, 0])}
CENTRE = sum(ROOM_POS.values()) / 3


def room(i, shift):
  sq = RoundedRectangle(width=1.1, height=1.1, corner_radius=0.15, stroke_color=WALKER, stroke_width=4)
  sq.set_fill(BACKGROUND, 1).move_to(ROOM_POS[i] + shift)
  lab = M(str(i), 0.75).move_to(sq)
  return VGroup(sq, lab)


def link_arrow(i, j, shift, offset=0.0, color=INK, width=4):
  p, q = ROOM_POS[i] + shift, ROOM_POS[j] + shift
  d = (q - p) / np.linalg.norm(q - p)
  perp = np.array([-d[1], d[0], 0.0])
  return Arrow(p + d * 0.75 + perp * offset, q - d * 0.75 + perp * offset, buff=0, color=color,
               stroke_width=width, tip_length=0.22, max_tip_length_to_length_ratio=0.2)


def exit_arrow(i, shift, rate=None):
  out = ROOM_POS[i] - CENTRE
  out = out / np.linalg.norm(out)
  p = ROOM_POS[i] + shift
  a = Arrow(p + out * 0.62, p + out * 1.4, buff=0, color=OURS, stroke_width=5, tip_length=0.22)
  if rate is None:
    return VGroup(a)
  lab = M(str(rate), 0.65, OURS).next_to(a.get_end(), out, buff=0.12)
  return VGroup(a, lab)


class Rooms(NarratedScene):
  def construct(self):
    shift = np.array([-2.85, -0.1, 0])
    rooms = VGroup(*[room(i, shift) for i in (1, 2, 3)])
    exits = VGroup(*[exit_arrow(i, shift) for i in (1, 2, 3)])
    two_way = VGroup(*[link_arrow(i, j, shift, offset=0.14) for i, j in
                       ((1, 2), (2, 1), (2, 3), (3, 2), (1, 3), (3, 1))])
    walker = Dot(radius=0.13, color=FLASH).move_to(ROOM_POS[1] + shift).set_z_index(5)
    with self.say('s11_rooms') as d:
      self.play(LaggedStart(*[FadeIn(r, scale=0.8) for r in rooms], lag_ratio=0.3), run_time=0.2 * d)
      self.play(Create(two_way), run_time=0.15 * d)
      self.play(FadeIn(walker), FadeIn(exits), run_time=0.1 * d)
      for j in (2, 3, 1):
        self.play(walker.animate.move_to(ROOM_POS[j] + shift), run_time=0.07 * d)
      out = (ROOM_POS[1] - CENTRE) / np.linalg.norm(ROOM_POS[1] - CENTRE)
      self.play(walker.animate.move_to(ROOM_POS[1] + shift + out * 1.6), run_time=0.08 * d)
      self.play(walker.animate.move_to(ROOM_POS[1] + shift), run_time=0.1 * d)
      rl = T('restart: back to the starting room', 0.65, FLASH).move_to([3.8, 2.6, 0])
      self.play(FadeIn(rl), run_time=0.1 * d)
    with self.say('s11_rev') as d:
      self.play(FadeOut(rl), FadeOut(walker), run_time=0.08 * d)
      m1 = T('the map: which room you start in', 0.7, TARGET).move_to([3.8, 2.4, 0])
      self.play(FadeIn(m1), run_time=0.15 * d)
      self.play(two_way.animate.set_color(FLASH), run_time=0.15 * d)
      rv = VGroup(T(r'\textbf{reversible}', 0.75, FLASH), T('equal traffic both ways', 0.7)).arrange(DOWN, buff=0.2)
      rv.move_to([3.8, 0.9, 0])
      self.play(FadeIn(rv), run_time=0.2 * d)
      ok = M(r'\Rightarrow \text{prescription gives the best}', 0.75, OURS).move_to([3.8, -0.4, 0])
      self.play(FadeIn(ok), run_time=0.2 * d)
    with self.say('s11_converse') as d:
      cv = M(r'\text{works for every recipe} \Rightarrow \text{reversible}', 0.7, FLASH).move_to([3.9, -1.6, 0])
      cn = T('(new, under a technical condition)', 0.6, MUTED).next_to(cv, DOWN, buff=0.2)
      self.play(FadeIn(cv), run_time=0.35 * d)
      self.play(FadeIn(cn), run_time=0.25 * d)
    self.play(*[FadeOut(m) for m in (two_way, exits, m1, rv, ok, cv, cn)], run_time=0.5)

    loop = VGroup(*[link_arrow(i, j, shift, color=INK) for i, j in ((1, 2), (2, 3), (3, 1))])
    loop_l = VGroup(*[M('1', 0.6, MUTED).move_to((ROOM_POS[i] + ROOM_POS[j]) / 2 + shift
                                               + 0.35 * ((ROOM_POS[i] + ROOM_POS[j]) / 2 - CENTRE)
                                               / np.linalg.norm((ROOM_POS[i] + ROOM_POS[j]) / 2 - CENTRE))
                      for i, j in ((1, 2), (2, 3), (3, 1))])
    exits2 = VGroup(*[exit_arrow(i, shift, rate=i) for i in (1, 2, 3)])
    head = T('one way loop', 0.75, BAD).move_to([3.8, 2.6, 0])
    ref = VGroup(T('prescribed recipe: random timer, rate 1', 0.65, OURS),
                 M(r'\text{average} = \frac{2332}{4453} \approx 0.5237', 0.8)).arrange(DOWN, buff=0.25)
    ref.move_to([3.8, 1.2, 0])
    with self.say('s11_loop') as d:
      self.play(FadeIn(head), Create(loop), FadeIn(loop_l), run_time=0.3 * d)
      self.play(FadeIn(exits2), run_time=0.2 * d)
      self.play(FadeIn(ref), run_time=0.3 * d)
    beat = VGroup(T('rate 9/10 instead:', 0.65, RIVAL),
                  M(r'\text{lower by } \frac{761111595}{7705213313411} \approx 0.0001', 0.75, RIVAL)) \
      .arrange(DOWN, buff=0.25).move_to([3.8, -0.6, 0])
    fail = T('the prescription fails', 0.8, BAD).move_to([3.8, -2.2, 0])
    with self.say('s11_beat') as d:
      self.play(FadeIn(beat), run_time=0.4 * d)
      self.play(FadeIn(fail), run_time=0.3 * d)
    self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6)


# --------------------------------------------------------------------------------------
# 12. Status, recap, open questions, end card
# --------------------------------------------------------------------------------------

def tick_list(rows, scale=0.75):
  out = VGroup()
  for sym, txt, color in rows:
    s = M(sym, 0.8, color)
    t = T(txt, scale)
    out.add(VGroup(s, t).arrange(RIGHT, buff=0.3))
  return out.arrange(DOWN, buff=0.32, aligned_edge=LEFT)


class Wrap(NarratedScene):
  def construct(self):
    head = T(r'\textbf{How sure are we?}', 0.85).to_edge(UP, buff=0.7)
    s1 = tick_list([
      (r'\checkmark', 'written proofs: main theorem and converse', OURS),
      (r'\times', 'not formalised in Lean: main theorem, converse', BAD),
      (r'\checkmark', 'checked in Lean: finite pairing algebra, three-room numbers', OURS),
    ])
    s2 = tick_list([
      (r'\times', 'not peer reviewed', BAD),
      (r'\cdot', 'earlier work: the conjugate map (Evans and Ray)', MUTED),
      (r'\cdot', r"earlier work: the pairing trick (D\'avila and Topp)", MUTED),
      (r'?', 'novelty of the new parts: full literature check still needed', FLASH),
    ])
    VGroup(s1, s2).arrange(DOWN, buff=0.5, aligned_edge=LEFT).next_to(head, DOWN, buff=0.5)
    with self.say('s12_status') as d:
      self.play(FadeIn(head), run_time=0.1 * d)
      self.play(LaggedStart(*[FadeIn(r, shift=0.2 * UP) for r in s1], lag_ratio=0.7), run_time=0.8 * d)
    with self.say('s12_review') as d:
      self.play(LaggedStart(*[FadeIn(r, shift=0.2 * UP) for r in s2], lag_ratio=0.7), run_time=0.85 * d)
    self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.5)

    rh = T(r'\textbf{Recap}', 0.85).to_edge(UP, buff=0.7)
    recap = VGroup(
      T('1. Restarting can turn an infinite average search into a finite one.', 0.7),
      T("2. Squaring a recipe's success curve gives a map where it is balanced.", 0.7),
      T('3. On a line, it is the one best recipe: symmetry plus a sum of squares.', 0.7),
    ).arrange(DOWN, buff=0.4, aligned_edge=LEFT).next_to(rh, DOWN, buff=0.6)
    recap[2].set_color(OURS)
    with self.say('s12_recap') as d:
      self.play(FadeIn(rh), run_time=0.08 * d)
      for k, line in enumerate(recap):
        self.play(FadeIn(line, shift=0.2 * UP), run_time=0.15 * d)
        self.wait(0.12 * d)
    oh = T(r'\textbf{Still unknown}', 0.8, FLASH)
    opn = VGroup(T('two and three dimensions', 0.7), T('smart or costly restarts', 0.7),
                 T('room networks without the technical condition', 0.7)).arrange(DOWN, buff=0.25, aligned_edge=LEFT)
    og = VGroup(oh, opn).arrange(DOWN, buff=0.3, aligned_edge=LEFT).next_to(recap, DOWN, buff=0.7).align_to(recap, LEFT)
    with self.say('s12_open') as d:
      self.play(FadeIn(oh), run_time=0.15 * d)
      self.play(LaggedStart(*[FadeIn(m, shift=0.2 * UP) for m in opn], lag_ratio=0.6), run_time=0.7 * d)
    self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.5)

    title_t = T(r'\textbf{Global optimality of conjugate restart laws}', 0.95)
    org = T('Valyu Research, 2026', 0.75, MUTED)
    path = T(r'\texttt{physics/statistical-physics/stochastic-resetting/conjugate-restart}', 0.55, MUTED)
    voice = T('Narration uses a synthetic voice.', 0.55, MUTED)
    endc = VGroup(title_t, org, path, voice).arrange(DOWN, buff=0.4).move_to([0, -0.6, 0])
    keys = key_icon(0.9).next_to(endc, UP, buff=0.7)
    with self.say('s12_end') as d:
      self.play(FadeIn(keys, shift=0.2 * DOWN), run_time=0.2 * d)
      self.play(FadeIn(title_t), FadeIn(org), run_time=0.3 * d)
      self.play(FadeIn(path), FadeIn(voice), run_time=0.3 * d)
    self.wait(3)
