"""Explainer: a periodically driven three-state machine with zero entropy production whose
forward-protocol waiting-time estimate is strictly positive.

Running example (paper Eq. rates): door a on line 1-2 has rate a(t) = 1 + eps cos t, door b
on line 2-3 has rate b(t) = 1 + eps sin t, the hidden line 1-3 has rate 1. Pictures use
eps = 1/2. Waiting densities f, g are evaluated by periodic quadrature exactly as in the
finding's plot_counterexample.py; the identities shown on screen are the exact ones replayed
by verification/check_short_lag.py.
"""

import numpy as np
from manim import *
from vrvideo import *

SCENES = [
  'ArrowOfTime', 'BoardGame', 'Balance', 'Entropy', 'Hidden', 'Schedule', 'ZeroWaste',
  'TimeOrder', 'Proof', 'Verdict', 'Scope', 'Recap',
]

DOOR_A = PRIMARY
DOOR_B = WARM
HIDDEN = MUTED
GOOD = OK
EPS = 0.5
TAU_ = 2 * np.pi

LINK_COLOR = {'12': DOOR_A, '23': DOOR_B, '13': HIDDEN}
TRI = {1: np.array([-2.0, -1.2, 0.0]), 2: np.array([0.0, 1.45, 0.0]), 3: np.array([2.0, -1.2, 0.0])}
CENTROID = sum(TRI.values()) / 3


def rate_a(t, eps=EPS):
  return 1 + eps * np.cos(t)


def rate_b(t, eps=EPS):
  return 1 + eps * np.sin(t)


_PHASES = TAU_ * np.arange(512) / 512


def fg(s, eps=EPS):
  """Event-conditioned waiting densities f = Psi(12->23), g = Psi(32->21) (paper Eq. fg)."""
  t = _PHASES
  a, b = 1 + eps * np.cos(t), 1 + eps * np.sin(t)
  an, bn = 1 + eps * np.cos(t + s), 1 + eps * np.sin(t + s)
  hazard = 2 * s + eps * (np.sin(t + s) - np.sin(t)) + eps * (np.cos(t) - np.cos(t + s))
  e = np.exp(-hazard)
  return float(np.mean(a * bn * e)), float(np.mean(b * an * e))


def T(text, scale=0.7, color=INK):
  return Tex(text, color=color).scale(scale)


def M(text, scale=0.8, color=INK):
  return MathTex(text, color=color).scale(scale)


def arrow_lbl(i, j, scale=0.6, color=INK):
  return MathTex(rf'{i}\!\to\!{j}', color=color).scale(scale)


def jump_color(i, j):
  return DOOR_A if {i, j} == {1, 2} else DOOR_B if {i, j} == {2, 3} else HIDDEN


# --------------------------------------------------------------------------------------
# The board: three squares in a triangle
# --------------------------------------------------------------------------------------

class Board:
  def __init__(self, center=ORIGIN, scale=1.0, hidden=False, dynamic=None):
    """dynamic: ValueTracker for t; then lines 1-2 and 2-3 redraw with width ~ rate."""
    self.center = np.array(center, dtype=float)
    self.scale = scale
    self.side = 0.72 * scale
    self.r = 0.5 * self.side * 1.15
    self.squares, self.labels, self.links = {}, {}, {}
    for i in TRI:
      sq = RoundedRectangle(width=self.side, height=self.side, corner_radius=0.1 * scale,
                            stroke_color=INK, stroke_width=3).set_fill(BACKGROUND, 1)
      sq.move_to(self.pos(i))
      out = TRI[i] - CENTROID
      out = out / np.linalg.norm(out)
      lab = MathTex(str(i)).scale(0.75 * scale).move_to(self.pos(i) + out * 0.68 * scale)
      self.squares[i], self.labels[i] = sq, lab
    for key in ('12', '23', '13'):
      self.links[key] = self._link(key, hidden=(hidden and key == '13'), tracker=dynamic)
    self.group = VGroup(*self.links.values(), *self.squares.values(), *self.labels.values())

  def pos(self, i):
    return self.center + self.scale * TRI[i]

  def prob_pos(self, i):
    off = {1: DOWN * 0.82, 2: RIGHT * 0.88, 3: DOWN * 0.82}[i]
    return self.pos(i) + self.scale * off

  def _link(self, key, hidden=False, tracker=None, width=6):
    i, j = int(key[0]), int(key[1])
    if hidden:
      return DashedLine(self.pos(i), self.pos(j), buff=self.r, color=HIDDEN, stroke_width=4,
                        dash_length=0.14)
    if tracker is not None and key in ('12', '23'):
      fn = rate_a if key == '12' else rate_b
      return always_redraw(lambda: Line(self.pos(i), self.pos(j), buff=self.r, color=LINK_COLOR[key],
                                        stroke_width=6 * fn(tracker.get_value())))
    return Line(self.pos(i), self.pos(j), buff=self.r, color=LINK_COLOR[key], stroke_width=width)

  def mid(self, key, out=0.0):
    i, j = int(key[0]), int(key[1])
    m = (self.pos(i) + self.pos(j)) / 2
    d = m - (self.center + self.scale * CENTROID)
    return m + out * d / np.linalg.norm(d)

  def hidden_link(self):
    return self._link('13', hidden=True)


def make_counter(board, i):
  c = Dot(radius=0.15 * board.scale, color=INK).move_to(board.pos(i))
  c.set_z_index(5)
  return c


def simulate(rates, start, n_hops, seed):
  """Gillespie walk on the triangle with fixed rates {(i, j): k}. Returns [(time, i, j)]."""
  rng = np.random.default_rng(seed)
  s, t, out = start, 0.0, []
  for _ in range(n_hops):
    exits = [(j, rates[(s, j)]) for j in (1, 2, 3) if j != s]
    tot = sum(r for _, r in exits)
    t += rng.exponential(1 / tot)
    u, acc = rng.random() * tot, 0.0
    for j, r in exits:
      acc += r
      if u <= acc:
        break
    out.append((t, s, j))
    s = j
  return out


def play_walk(scene, counter, board, hops, total, hop_time=0.22, on_hop=None):
  """Animate a list of hops [(time, i, j)] so that the whole walk lasts `total` seconds."""
  n = len(hops)
  span = hops[-1][0] if hops else 1.0
  idle = max(total - n * hop_time, 0.2)
  last = 0.0
  for (tt, i, j) in hops:
    gap = (tt - last) / span * idle
    last = tt
    if gap > 1 / 30:
      scene.wait(gap)
    anims = [counter.animate.move_to(board.pos(j))]
    if on_hop is not None:
      extra = on_hop(i, j)
      if extra:
        anims += extra
    scene.play(*anims, run_time=hop_time, rate_func=smooth)


UNIT = {(i, j): 1.0 for i in TRI for j in TRI if i != j}
CLOCKWISE = {(1, 2): 2.0, (2, 3): 2.0, (3, 1): 2.0, (2, 1): 1.0, (3, 2): 1.0, (1, 3): 1.0}


def play_icon(backwards=False, color=INK):
  tri = Triangle(color=color, fill_opacity=1, stroke_width=0).scale(0.16)
  if backwards:
    t1 = tri.copy().rotate(PI / 2)
    t2 = tri.copy().rotate(PI / 2).next_to(t1, RIGHT, buff=-0.05)
    icon = VGroup(t1, t2)
  else:
    icon = tri.rotate(-PI / 2)
  return icon


def clock(center, radius=0.5, tracker=None, color=INK):
  face = Circle(radius=radius, color=color, stroke_width=3).move_to(center)
  ticks = VGroup(*[Line(center + 0.82 * radius * np.array([np.sin(k * PI / 2), np.cos(k * PI / 2), 0]),
                        center + radius * np.array([np.sin(k * PI / 2), np.cos(k * PI / 2), 0]),
                        color=MUTED, stroke_width=2) for k in range(4)])
  if tracker is None:
    hand = Line(center, center + 0.8 * radius * UP, color=SECONDARY, stroke_width=4)
  else:
    hand = always_redraw(lambda: Line(center, center + 0.8 * radius * np.array(
      [np.sin(tracker.get_value()), np.cos(tracker.get_value()), 0]), color=SECONDARY, stroke_width=4))
  return VGroup(face, ticks, hand)


def traffic_arrow(board, i, j, width, color, offset=0.2, frac=0.55):
  p, q = board.pos(i), board.pos(j)
  d = (q - p) / np.linalg.norm(q - p)
  perp = np.array([-d[1], d[0], 0.0])
  m = (p + q) / 2
  half = np.linalg.norm(q - p) * frac / 2
  return Arrow(m - d * half + perp * offset, m + d * half + perp * offset, buff=0, color=color,
               stroke_width=width, max_tip_length_to_length_ratio=0.18,
               max_stroke_width_to_length_ratio=30, tip_length=0.2)


# --------------------------------------------------------------------------------------
# 1. Hook: the arrow of time
# --------------------------------------------------------------------------------------

class ArrowOfTime(NarratedScene):
  def construct(self):
    floor_y, R = -2.4, 0.3
    floor = Line([-5.8, floor_y, 0], [5.8, floor_y, 0], color=MUTED, stroke_width=3)
    g, h0, ratio, nb = 20.0, 3.6, 0.6, 6
    segs, t, h = [], 0.0, h0
    tf = np.sqrt(2 * h0 / g)
    segs.append((0.0, tf, 'fall', h0))
    t = tf
    impacts = [tf]
    for _ in range(1, nb):
      h *= ratio
      dur = 2 * np.sqrt(2 * h / g)
      segs.append((t, t + dur, 'arc', h))
      t += dur
      impacts.append(t)
    total = t

    def y_of(tt):
      for (a, b, kind, hh) in segs:
        if tt <= b + 1e-9:
          if kind == 'fall':
            return hh - 0.5 * g * (tt - a) ** 2
          v = np.sqrt(2 * g * hh)
          return v * (tt - a) - 0.5 * g * (tt - a) ** 2
      return 0.0

    def x_of(tt):
      return -5.0 + 9.8 * tt / total

    clock_t = ValueTracker(0.0)
    ball = Circle(radius=R, color=INK, stroke_width=2).set_fill(GREY_A, 1)
    ball.add_updater(lambda m: m.move_to([x_of(clock_t.get_value()), floor_y + R + y_of(clock_t.get_value()), 0]))
    heat = VGroup()
    for k, ti in enumerate(impacts):
      xi = x_of(ti)
      puff = VGroup(*[MathTex(r'\sim', color=EXTRA).scale(1.2).move_to([xi + dx, floor_y + 0.2 + dy, 0])
                      for dx, dy in ((-0.45, 0.05), (0.0, 0.25), (0.45, 0.05))])
      puff.t_imp = ti
      puff.set_opacity(0)
      heat.add(puff)

    def heat_update(group):
      tt = clock_t.get_value()
      for p in group:
        age = tt - p.t_imp
        p.set_opacity(float(np.clip(1 - age / 0.45, 0, 1)) if age >= 0 else 0)
    heat.add_updater(heat_update)

    fwd = VGroup(play_icon(), T('forward', 0.65)).arrange(RIGHT, buff=0.2).to_corner(UL, buff=0.6)
    bwd = VGroup(play_icon(True, WARN), T('backwards', 0.65, WARN)).arrange(RIGHT, buff=0.2).to_corner(UL, buff=0.6)

    with self.say('s01_ball') as d:
      self.play(Create(floor), FadeIn(fwd), FadeIn(ball), run_time=0.12 * d)
      self.add(heat)
      self.play(clock_t.animate.set_value(total), run_time=0.8 * d, rate_func=linear)

    with self.say('s01_reverse') as d:
      self.play(ReplacementTransform(fwd, bwd), run_time=0.08 * d)
      self.play(clock_t.animate.set_value(0.0), run_time=0.62 * d, rate_func=linear)
      q = M(r'?', 1.6, WARN).next_to(ball, UR, buff=0.2)
      self.play(FadeIn(q, scale=0.6), run_time=0.08 * d)
      cap = caption('the arrow of time', 0.75)
      self.play(Write(cap), run_time=0.12 * d)

    with self.say('s01_measure') as d:
      ball.clear_updaters()
      heat.clear_updaters()
      self.play(*[FadeOut(m) for m in (ball, heat, floor, bwd, q, cap)], run_time=0.15 * d)
      top = T(r'how wrong the \emph{backwards} film looks', 0.8)
      mid = M(r'\Big\Updownarrow', 0.9, MUTED)
      bot = T('how much energy is wasted', 0.8)
      grp = VGroup(top, mid, bot).arrange(DOWN, buff=0.35)
      self.play(FadeIn(top, shift=0.2 * DOWN), run_time=0.25 * d)
      self.play(FadeIn(mid), FadeIn(bot, shift=0.2 * UP), run_time=0.3 * d)

    with self.say('s01_tiny') as d:
      self.play(grp.animate.scale(0.75).to_edge(UP, buff=0.6).set_opacity(0.45), run_time=0.12 * d)
      tape = Line([-5.5, -0.4, 0], [5.5, -0.4, 0], color=MUTED, stroke_width=3)
      times = [0.5, 1.4, 1.9, 3.2, 3.8, 5.1, 5.6, 6.9, 8.0, 8.7]
      xs = [-5.0 + 10.0 * tt / 9.2 for tt in times]
      ticks = VGroup(*[Line([x, -0.65, 0], [x, -0.15, 0], color=INK, stroke_width=4) for x in xs])
      self.play(Create(tape), run_time=0.1 * d)
      self.play(LaggedStart(*[FadeIn(tk, shift=0.15 * DOWN) for tk in ticks], lag_ratio=0.5), run_time=0.4 * d)
      br = Brace(Line([xs[2], -0.4, 0], [xs[3], -0.4, 0]), DOWN, buff=0.35, color=SECONDARY)
      wl = T('wait', 0.65, SECONDARY).next_to(br, DOWN, buff=0.12)
      jl = T('jumps', 0.65, MUTED).next_to(ticks[5], UP, buff=0.25)
      self.play(GrowFromCenter(br), FadeIn(wl), FadeIn(jl), run_time=0.15 * d)
      qq = M(r'\text{waits} \;\Rightarrow\; \text{waste?}', 0.85).move_to([0, -2.6, 0])
      self.play(Write(qq), run_time=0.15 * d)

    with self.say('s01_guess') as d:
      self.play(*[FadeOut(m) for m in (grp, tape, ticks, br, wl, jl, qq)], run_time=0.12 * d)
      head = T(r'\textbf{conjecture}', 0.85, SECONDARY)
      body = M(r'\text{waiting-time test} \;\le\; \text{true waste}', 0.95)
      note = T('published paper, 2024: machines on a repeating schedule', 0.6, MUTED)
      conj = VGroup(head, body, note).arrange(DOWN, buff=0.4)
      self.play(FadeIn(head, shift=0.2 * DOWN), run_time=0.15 * d)
      self.play(Write(body), run_time=0.3 * d)
      self.play(FadeIn(note), run_time=0.15 * d)

    with self.say('s01_plan') as d:
      self.play(FadeOut(note), VGroup(head, body).animate.scale(0.75).to_edge(UP, buff=0.6), run_time=0.15 * d)
      w0 = M(r'\text{true waste} = 0', 1.0, GOOD)
      w1 = M(r'\text{test} > 0', 1.0, WARN)
      pair = VGroup(w0, w1).arrange(RIGHT, buff=1.6).move_to([0, -0.4, 0])
      self.play(FadeIn(w0, shift=0.2 * UP), run_time=0.2 * d)
      self.play(FadeIn(w1, shift=0.2 * UP), run_time=0.2 * d)
      q2 = M('?', 2.0, SECONDARY).next_to(pair, DOWN, buff=0.6)
      self.play(FadeIn(q2, scale=0.5), run_time=0.15 * d)
    self.play(*[FadeOut(m) for m in (head, body, pair, q2)], run_time=0.6)


# --------------------------------------------------------------------------------------
# 2. The board game
# --------------------------------------------------------------------------------------

def die(face, color):
  box = RoundedRectangle(width=1.0, height=1.0, corner_radius=0.14, stroke_color=INK, stroke_width=3)
  txt = T(face, 0.62, color).move_to(box)
  return VGroup(box, txt)


class BoardGame(NarratedScene):
  def construct(self):
    b = Board(center=[0, 0.1, 0], scale=1.15)
    counter = make_counter(b, 1)
    with self.say('s02_board') as d:
      self.play(LaggedStart(*[FadeIn(b.squares[i], scale=0.8) for i in TRI], lag_ratio=0.3), run_time=0.25 * d)
      self.play(LaggedStart(*[Create(b.links[k]) for k in ('12', '23', '13')], lag_ratio=0.3),
                FadeIn(VGroup(*b.labels.values())), run_time=0.3 * d)
      self.play(FadeIn(counter, scale=0.4), run_time=0.15 * d)

    # Move the board left; positions follow.
    shift = np.array([-3.2, -0.2, 0])
    with self.say('s02_dice') as d:
      self.play(b.group.animate.shift(shift), counter.animate.shift(shift), run_time=0.1 * d)
      b.center = b.center + shift
      tick = T('tick 1', 0.7, MUTED).move_to([3.2, 2.2, 0])
      d1, d2 = die('stay', MUTED).move_to([2.3, 0.6, 0]), die('stay', MUTED).move_to([4.1, 0.6, 0])
      l1 = T(r'to 2', 0.6, DOOR_A).next_to(d1, DOWN, buff=0.25)
      l2 = T(r'to 3', 0.6, HIDDEN).next_to(d2, DOWN, buff=0.25)
      self.play(FadeIn(d1), FadeIn(d2), FadeIn(l1), FadeIn(l2), FadeIn(tick), run_time=0.1 * d)
      for k, faces in enumerate([('stay', 'stay'), ('stay', 'stay'), ('go', 'stay')], start=1):
        new_tick = T(f'tick {k}', 0.7, MUTED).move_to(tick)
        n1 = die(faces[0], GOOD if faces[0] == 'go' else MUTED).move_to(d1)
        n2 = die(faces[1], MUTED).move_to(d2)
        self.play(Rotate(d1, PI / 2), Rotate(d2, -PI / 2), run_time=0.07 * d)
        self.play(Transform(d1, n1), Transform(d2, n2), Transform(tick, new_tick), run_time=0.06 * d)
        self.wait(0.05 * d)
      self.play(Indicate(d1, color=GOOD), run_time=0.08 * d)
      self.play(counter.animate.move_to(b.pos(2)), run_time=0.08 * d)

    with self.say('s02_rate') as d:
      self.play(*[FadeOut(m) for m in (d1, d2, l1, l2, tick)], run_time=0.1 * d)

      def strip(n_go):
        cells = VGroup(*[Square(0.3, stroke_color=INK, stroke_width=2).set_fill(GOOD if k < n_go else BACKGROUND, 1)
                         for k in range(10)]).arrange(RIGHT, buff=0.07)
        return cells
      r1 = VGroup(T('rate 1', 0.65), strip(1)).arrange(RIGHT, buff=0.35).move_to([3.1, 0.9, 0])
      r2 = VGroup(T('rate 2', 0.65, SECONDARY), strip(2)).arrange(RIGHT, buff=0.35).move_to([3.1, -0.4, 0])
      hint = T('faces that say go', 0.55, MUTED).next_to(r1, UP, buff=0.35)
      self.play(FadeIn(r1), FadeIn(hint), run_time=0.2 * d)
      self.play(FadeIn(r2), b.links['12'].animate.set_stroke(width=13, color=DOOR_A), run_time=0.25 * d)
      self.wait(0.25 * d)
      self.play(b.links['12'].animate.set_stroke(width=6), run_time=0.1 * d)

    with self.say('s02_play') as d:
      self.play(FadeOut(r1), FadeOut(r2), FadeOut(hint), run_time=0.1 * d)
      ones = VGroup(*[M('1', 0.65, LINK_COLOR[k]).move_to(b.mid(k, out=0.42)) for k in ('12', '23', '13')])
      self.play(FadeIn(ones), run_time=0.1 * d)
      hops = simulate(UNIT, 2, 12, seed=7)
      play_walk(self, counter, b, hops, total=0.7 * d)

    with self.say('s02_probs') as d:
      long = simulate(UNIT, 1, 4000, seed=11)
      occ, last, state = np.zeros(3), 0.0, 1
      checkpoints = np.unique(np.geomspace(25, len(long), 70).astype(int))
      fracs, k = [], 0
      for n, (tt, i, j) in enumerate(long, start=1):
        occ[i - 1] += tt - last
        last = tt
        if k < len(checkpoints) and n == checkpoints[k]:
          fracs.append(occ / occ.sum())
          k += 1
      fracs = np.array(fracs)
      base_y, scale_h, xs = -1.8, 4.2, (2.3, 3.3, 4.3)
      idx = ValueTracker(0)
      baseline = Line([1.7, base_y, 0], [4.9, base_y, 0], color=MUTED, stroke_width=2)

      def bars():
        f = fracs[int(round(idx.get_value()))]
        return VGroup(*[Rectangle(width=0.6, height=max(min(f[q], 0.8) * scale_h, 0.01), stroke_width=0)
                        .set_fill(INK, 0.75).move_to([xs[q], base_y, 0], aligned_edge=DOWN) for q in range(3)])
      bar_grp = always_redraw(bars)
      third = DashedLine([1.7, base_y + scale_h / 3, 0], [4.9, base_y + scale_h / 3, 0], color=SECONDARY,
                         stroke_width=3, dash_length=0.12)
      third_l = M(r'\frac13', 0.7, SECONDARY).next_to(third, RIGHT, buff=0.15)
      names = VGroup(*[M(str(q + 1), 0.65).move_to([xs[q], base_y - 0.35, 0]) for q in range(3)])
      head = T('share of time on each square', 0.6, MUTED).move_to([3.3, 2.4, 0])
      self.play(FadeIn(baseline), FadeIn(names), FadeIn(head), FadeIn(bar_grp), run_time=0.12 * d)
      self.play(idx.animate.set_value(len(fracs) - 1), run_time=0.5 * d, rate_func=linear)
      self.play(Create(third), FadeIn(third_l), run_time=0.15 * d)
      probs = VGroup(*[M(r'\frac13', 0.6, SECONDARY).move_to(b.prob_pos(i)) for i in TRI])
      self.play(FadeIn(probs), run_time=0.12 * d)
    self.wait(0.3)


# --------------------------------------------------------------------------------------
# 3. Detailed balance versus a driven cycle
# --------------------------------------------------------------------------------------

class Balance(NarratedScene):
  def construct(self):
    b = Board(center=[-3.3, -0.35, 0], scale=1.1)
    counter = make_counter(b, 2)
    probs = VGroup(*[M(r'\frac13', 0.6, MUTED).move_to(b.prob_pos(i)) for i in TRI])
    self.add(b.group, counter, probs)

    def arrows_for(rates, base=7.0):
      out = {}
      for (i, j), k in rates.items():
        key = ''.join(sorted(f'{i}{j}'))
        out[(i, j)] = traffic_arrow(b, i, j, width=4.0 * k + 0.5, color=LINK_COLOR[key])
      return out

    ar = arrows_for(UNIT)
    with self.say('s03_traffic') as d:
      self.play(GrowArrow(ar[(1, 2)]), run_time=0.15 * d)
      l1 = M(r'\text{traffic } 1\!\to\!2', 0.8)
      l1b = M(r'= (\text{chance on } 1) \times (\text{rate } 1\!\to\!2)', 0.72)
      l2 = M(r'= \frac13 \times 1', 0.8, DOOR_A)
      panel = VGroup(l1, l1b, l2).arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to([2.7, 1.8, 0])
      self.play(Write(l1), run_time=0.15 * d)
      self.play(Write(l1b), run_time=0.3 * d)
      self.play(FadeIn(l2, shift=0.2 * RIGHT), run_time=0.2 * d)

    with self.say('s03_detailed') as d:
      self.play(GrowArrow(ar[(2, 1)]), run_time=0.15 * d)
      l3 = M(r'\text{traffic } 2\!\to\!1 = \frac13 \times 1', 0.8).next_to(panel, DOWN, buff=0.5, aligned_edge=LEFT)
      self.play(FadeIn(l3), run_time=0.15 * d)
      rest = [ar[k] for k in ((2, 3), (3, 2), (1, 3), (3, 1))]
      self.play(LaggedStart(*[GrowArrow(a) for a in rest], lag_ratio=0.2), run_time=0.25 * d)
      name = T(r'detailed balance: \emph{equilibrium}', 0.8, GOOD).move_to([2.7, -1.5, 0])
      self.play(Write(name), run_time=0.25 * d)

    with self.say('s03_backwards') as d:
      icon = VGroup(play_icon(True, MUTED), T('backwards', 0.6, MUTED)).arrange(RIGHT, buff=0.15)
      icon.to_corner(UL, buff=0.6)
      self.play(FadeIn(icon), run_time=0.1 * d)
      hops = simulate(UNIT, 2, 8, seed=3)
      play_walk(self, counter, b, hops, total=0.75 * d)

    cw = arrows_for(CLOCKWISE)
    with self.say('s03_clockwise') as d:
      self.play(FadeOut(icon), FadeOut(VGroup(l1, l1b, l2, l3, name)), run_time=0.12 * d)
      self.play(*[Transform(ar[k], cw[k]) for k in ar], run_time=0.35 * d)
      ctr = b.center + b.scale * CENTROID + 0.15 * UP
      loop = Arc(radius=0.55, start_angle=PI / 2 + 0.3, angle=-(TAU - 0.9), color=SECONDARY, stroke_width=4).move_arc_center_to(ctr)
      loop.add_tip(tip_length=0.18)
      r2 = M(r'\text{clockwise: rate } 2', 0.8).move_to([2.7, 1.2, 0])
      r1 = M(r'\text{anticlockwise: rate } 1', 0.8, MUTED).next_to(r2, DOWN, buff=0.4)
      self.play(Create(loop), FadeIn(r2), FadeIn(r1), run_time=0.3 * d)

    with self.say('s03_arrow') as d:
      t2 = M(r'\text{clockwise traffic} = \frac13\times 2 = \frac23', 0.75).move_to(r2)
      t1 = M(r'\text{anticlockwise traffic} = \frac13\times 1 = \frac13', 0.75, MUTED).move_to(r1).shift(0.15 * DOWN)
      self.play(Transform(r2, t2), Transform(r1, t1), run_time=0.15 * d)
      hops = simulate(CLOCKWISE, counter_state(counter, b), 12, seed=5)
      play_walk(self, counter, b, hops, total=0.55 * d)
      arrow_t = T('an arrow of time', 0.8, SECONDARY).move_to([2.7, -1.4, 0])
      self.play(Write(arrow_t), run_time=0.15 * d)
    self.wait(0.3)


def counter_state(counter, board):
  c = counter.get_center()
  return min(TRI, key=lambda i: np.linalg.norm(board.pos(i) - c))


# --------------------------------------------------------------------------------------
# 4. Entropy production
# --------------------------------------------------------------------------------------

class Entropy(NarratedScene):
  def construct(self):
    with self.say('s04_name') as d:
      name = VGroup(T('entropy production', 0.95), M(r'=\;\sigma', 1.1, SECONDARY)).arrange(RIGHT, buff=0.3)
      self.play(Write(name), run_time=0.4 * d)
      self.play(name.animate.scale(0.75).to_edge(UP, buff=0.55), run_time=0.25 * d)

    with self.say('s04_log') as d:
      ax = Axes(x_range=[0, 3.5, 1], y_range=[-1.6, 1.4, 1], x_length=6.5, y_length=3.6, tips=False,
                axis_config={'color': MUTED, 'stroke_width': 2}).move_to([0, -0.6, 0])
      xl = VGroup(*[M(str(v), 0.55, MUTED).next_to(ax.c2p(v, 0), DOWN, buff=0.15) for v in (1, 2, 3)])
      curve = ax.plot(np.log, x_range=[0.2, 3.45], color=INK, stroke_width=4)
      lab = M(r'\log x', 0.7).next_to(ax.c2p(3.45, np.log(3.45)), RIGHT, buff=0.15)
      self.play(Create(ax), FadeIn(xl), run_time=0.15 * d)
      self.play(Create(curve), FadeIn(lab), run_time=0.25 * d)
      dot = Dot(ax.c2p(1, 0), color=SECONDARY, radius=0.09)
      l0 = M(r'\log 1 = 0', 0.7, SECONDARY).next_to(dot, UL, buff=0.2)
      self.play(FadeIn(dot, scale=0.5), Write(l0), run_time=0.18 * d)
      plus = T('positive', 0.6).move_to(ax.c2p(2.5, 0.45))
      minus = T('negative', 0.6).move_to(ax.c2p(0.8, -1.2))
      self.play(FadeIn(plus), run_time=0.1 * d)
      self.play(FadeIn(minus), run_time=0.1 * d)

    with self.say('s04_formula') as d:
      self.play(*[FadeOut(m) for m in (ax, xl, curve, lab, dot, l0, plus, minus)], run_time=0.12 * d)
      f = MathTex(r'\sigma', '=', r'\text{add up}', r'\Big[', r'\text{traffic}', r'\times',
                  r'\log', r'\frac{\text{traffic this way}}{\text{traffic that way}}', r'\Big]').scale(0.85)
      f[0].set_color(SECONDARY)
      sub = T('over every line, in each direction', 0.6, MUTED).next_to(f, DOWN, buff=0.45)
      self.play(Write(f), run_time=0.5 * d)
      self.play(FadeIn(sub), run_time=0.15 * d)
    formula = VGroup(f, sub)

    with self.say('s04_examples') as d:
      self.play(FadeOut(sub), f.animate.scale(0.8).next_to(name, DOWN, buff=0.45), run_time=0.15 * d)
      e1h = T('clockwise game', 0.65, MUTED)
      e1 = M(r'3\times\Big(\frac23\log 2+\frac13\log\frac12\Big)=\log 2\approx 0.69', 0.8)
      e2h = T('balanced game', 0.65, MUTED)
      e2 = M(r'\text{every ratio} = 1,\ \ \log 1 = 0\ \ \Rightarrow\ \ \sigma = 0', 0.8)
      rows = VGroup(VGroup(e1h, e1).arrange(DOWN, buff=0.2), VGroup(e2h, e2).arrange(DOWN, buff=0.2)).arrange(DOWN, buff=0.6)
      rows.move_to([0, -1.2, 0])
      e2[0][-3:].set_color(GOOD)
      self.play(FadeIn(e1h), Write(e1), run_time=0.35 * d)
      self.play(FadeIn(e2h), Write(e2), run_time=0.35 * d)

    with self.say('s04_key') as d:
      self.play(FadeOut(rows), run_time=0.15 * d)
      rule = M(r'\text{balanced at every moment}\ \Rightarrow\ \sigma = 0', 0.95)
      rule.move_to([0, -1.0, 0])
      box = boxed(rule, color=GOOD, buff=0.3)
      self.play(Write(rule), run_time=0.4 * d)
      self.play(Create(box), run_time=0.2 * d)
    self.wait(0.3)


# --------------------------------------------------------------------------------------
# 5. Hidden line, waiting times, the estimator
# --------------------------------------------------------------------------------------

class Hidden(NarratedScene):
  def construct(self):
    b = Board(center=[-3.5, 1.0, 0], scale=0.8)
    counter = make_counter(b, 1)
    self.add(b.group, counter)
    tape_y = -2.3
    tape = Line([-6.2, tape_y, 0], [6.2, tape_y, 0], color=MUTED, stroke_width=3)
    tlab = T('time', 0.55, MUTED).next_to(tape, RIGHT, buff=0.1).shift(0.35 * UP + 0.5 * LEFT)
    script = [(0.6, 1, 2), (1.35, 2, 3), (2.0, 3, 1), (2.7, 1, 2), (3.55, 2, 1), (4.15, 1, 3),
              (4.95, 3, 2), (5.7, 2, 1)]

    def x_of(tt):
      return -5.8 + 11.0 * tt / 6.2

    with self.say('s05_hidden') as d:
      dashed = b.hidden_link()
      hid = T('hidden', 0.55, HIDDEN).next_to(dashed, DOWN, buff=0.12)
      old = b.links['13']
      self.play(ReplacementTransform(old, dashed), FadeIn(hid), run_time=0.15 * d)
      b.group.remove(old)
      b.group.add_to_back(dashed)
      b.links['13'] = dashed
      self.play(Create(tape), FadeIn(tlab), run_time=0.1 * d)
      marks = VGroup()
      tick_of = {}
      span, idle, last = script[-1][0], 0.5 * d, 0.0
      for n, (tt, i, j) in enumerate(script):
        gap = (tt - last) / span * idle
        last = tt
        self.wait(max(gap - 0.2, 1 / 30))
        anims = [counter.animate.move_to(b.pos(j))]
        if {i, j} != {1, 3}:
          x = x_of(tt)
          tk = Line([x, tape_y - 0.2, 0], [x, tape_y + 0.2, 0], color=jump_color(i, j), stroke_width=4)
          lb = arrow_lbl(i, j, 0.55, jump_color(i, j)).next_to(tk, UP, buff=0.12)
          grp = VGroup(tk, lb)
          marks.add(grp)
          tick_of[n] = grp
          anims.append(FadeIn(grp, shift=0.1 * DOWN))
        else:
          anims.append(Indicate(dashed, color=HIDDEN, scale_factor=1.0))
        self.play(*anims, run_time=0.2)

    with self.say('s05_tape') as d:
      first, second = tick_of[0], tick_of[1]
      others = [m for m in marks if m is not first and m is not second]
      self.play(*[m.animate.set_opacity(0.25) for m in others], run_time=0.2 * d)
      br = Brace(VGroup(first[0], second[0]), DOWN, buff=0.12, color=SECONDARY)
      bl = M(r'\text{wait } s', 0.6, SECONDARY).next_to(br, DOWN, buff=0.1)
      self.play(GrowFromCenter(br), FadeIn(bl), run_time=0.3 * d)

    with self.say('s05_reverse') as d:
      def pair_row(l1, c1, l2, c2, y, x0=1.2, w=2.2):
        t1 = Line([x0, y - 0.2, 0], [x0, y + 0.2, 0], color=c1, stroke_width=4)
        t2 = Line([x0 + w, y - 0.2, 0], [x0 + w, y + 0.2, 0], color=c2, stroke_width=4)
        a1 = MathTex(l1, color=c1).scale(0.65).next_to(t1, UP, buff=0.12)
        a2 = MathTex(l2, color=c2).scale(0.65).next_to(t2, UP, buff=0.12)
        base = Line([x0 - 0.4, y, 0], [x0 + w + 0.4, y, 0], color=MUTED, stroke_width=2)
        brc = Brace(VGroup(t1, t2), DOWN, buff=0.1, color=SECONDARY)
        s_l = M(r's', 0.6, SECONDARY).next_to(brc, DOWN, buff=0.08)
        return VGroup(base, t1, t2, a1, a2, brc, s_l)
      fwd = pair_row(r'1\!\to\!2', DOOR_A, r'2\!\to\!3', DOOR_B, 1.6)
      bwd = pair_row(r'3\!\to\!2', DOOR_B, r'2\!\to\!1', DOOR_A, -0.3)
      fl = T('pair', 0.6, MUTED).next_to(fwd, LEFT, buff=0.45)
      bl2 = T('backwards', 0.6, MUTED).next_to(bwd, LEFT, buff=0.45)
      self.play(TransformFromCopy(VGroup(first, second, br, bl), fwd), FadeIn(fl), run_time=0.25 * d)
      ghost = fwd.copy()
      self.play(ghost.animate.move_to(bwd).stretch(-1, 0), run_time=0.25 * d)
      self.play(ReplacementTransform(ghost, bwd), FadeIn(bl2), run_time=0.2 * d)

    with self.say('s05_curves') as d:
      self.play(*[FadeOut(m) for m in (b.group, counter, hid, tape, tlab, marks, br, bl, fwd, bwd, fl, bl2)],
                run_time=0.12 * d)
      ax = Axes(x_range=[0, 2.5, 0.5], y_range=[0, 1.1, 0.5], x_length=6.6, y_length=4.0, tips=False,
                axis_config={'color': MUTED, 'stroke_width': 2}).move_to([-1.6, -0.3, 0])
      xl = M(r'\text{wait } s', 0.6, MUTED).next_to(ax.x_axis, DOWN, buff=0.3)
      yl = T('how likely', 0.6, MUTED).next_to(ax.y_axis, UP, buff=0.2)
      self.play(Create(ax), FadeIn(xl), FadeIn(yl), run_time=0.12 * d)
      w = 0.125
      bars = VGroup(*[Rectangle(width=ax.x_length * w / 2.5 * 0.92, height=ax.y_length * np.exp(-2 * (k + 0.5) * w) / 1.1,
                                stroke_width=0).set_fill(DOOR_A, 0.35).move_to(ax.c2p((k + 0.5) * w, 0), aligned_edge=DOWN)
                      for k in range(20)])
      self.play(LaggedStart(*[GrowFromEdge(r, DOWN) for r in bars], lag_ratio=0.08), run_time=0.25 * d)
      f_curve = ax.plot(lambda s: np.exp(-2 * s), x_range=[0, 2.5], color=DOOR_A, stroke_width=5)
      g_curve = DashedVMobject(ax.plot(lambda s: np.exp(-2 * s), x_range=[0, 2.5], color=DOOR_B, stroke_width=5),
                               num_dashes=40)
      lf = M(r'1\!\to\!2,\ \text{then}\ 2\!\to\!3', 0.65, DOOR_A).move_to([4.0, 1.2, 0])
      lg = M(r'3\!\to\!2,\ \text{then}\ 2\!\to\!1', 0.65, DOOR_B).move_to([4.0, 0.4, 0])
      self.play(Create(f_curve), FadeOut(bars), FadeIn(lf), run_time=0.2 * d)
      self.play(Create(g_curve), FadeIn(lg), run_time=0.2 * d)
      same = T('same curve', 0.65, GOOD).move_to([4.0, -0.6, 0])
      self.play(FadeIn(same), run_time=0.08 * d)
    plot = VGroup(ax, xl, yl, f_curve, g_curve, lf, lg, same)

    with self.say('s05_estimator') as d:
      self.play(FadeOut(plot), run_time=0.15 * d)
      est = MathTex(r'\hat\sigma', '=', r'\text{add up over pairs}', r'\big[', r'\text{how often}', r'\times',
                    r'\text{mismatch}', r'\big]').scale(0.9).move_to([0, 0.4, 0])
      est[0].set_color(SECONDARY)
      sub = T(r'an estimate of $\sigma$ from waits alone', 0.62, MUTED).next_to(est, DOWN, buff=0.45)
      self.play(Write(est), run_time=0.45 * d)
      self.play(FadeIn(sub), run_time=0.15 * d)

    with self.say('s05_hope') as d:
      self.play(FadeOut(sub), est.animate.scale(0.75).to_edge(UP, buff=0.6), run_time=0.12 * d)
      frames = VGroup(*[RoundedRectangle(width=0.9, height=0.7, corner_radius=0.06, stroke_color=INK, stroke_width=2)
                        .set_fill(GREY_B, 0.45) for _ in range(9)]).arrange(RIGHT, buff=0.12).move_to([0, 0.5, 0])
      whole = M(r'\text{whole film: backwards wrongness} = \sigma', 0.7).next_to(frames, DOWN, buff=0.4)
      self.play(LaggedStart(*[FadeIn(fr) for fr in frames], lag_ratio=0.1), FadeIn(whole), run_time=0.25 * d)
      part = M(r'\text{part of the film: catch less}', 0.7).move_to(whole)
      dark = [frames[k] for k in (0, 2, 3, 5, 6, 8)]
      self.play(*[fr.animate.set_fill(BACKGROUND, 1).set_stroke(opacity=0.3) for fr in dark],
                ReplacementTransform(whole, part), run_time=0.25 * d)
      hope = M(r'\hat\sigma \;\le\; \sigma', 1.2, SECONDARY).move_to([0, -2.2, 0])
      hl = T('the hope', 0.65, MUTED).next_to(hope, LEFT, buff=0.5)
      self.play(Write(hope), FadeIn(hl), run_time=0.2 * d)
    self.wait(0.3)


# --------------------------------------------------------------------------------------
# 6. The periodic schedule and the conjecture
# --------------------------------------------------------------------------------------

class Schedule(NarratedScene):
  def construct(self):
    t = ValueTracker(0.0)
    b = Board(center=[-3.6, -0.6, 0], scale=0.85, hidden=True, dynamic=t)
    clk = clock(np.array([-3.6, 2.45, 0]), 0.5, t)
    tl = M('t', 0.7, SECONDARY).next_to(clk, RIGHT, buff=0.2)

    with self.say('s06_driven') as d:
      self.play(FadeIn(b.group), run_time=0.15 * d)
      self.play(FadeIn(clk), FadeIn(tl), run_time=0.1 * d)
      self.play(t.animate.set_value(TAU_), run_time=0.7 * d, rate_func=linear)

    with self.say('s06_doors') as d:
      fa = M(r'a(t) = 1 + \varepsilon\cos t', 0.85, DOOR_A)
      fb = M(r'b(t) = 1 + \varepsilon\sin t', 0.85, DOOR_B)
      fh = M(r'\text{hidden line: } 1', 0.75, HIDDEN)
      forms = VGroup(fa, fb, fh).arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to([2.9, 2.55, 0])
      la = M('a', 0.7, DOOR_A).move_to(b.mid('12', out=0.45))
      lb = M('b', 0.7, DOOR_B).move_to(b.mid('23', out=0.45))
      self.play(t.animate.set_value(TAU_ + 0.25 * d * 0.9), FadeIn(la), FadeIn(lb), Indicate(tl), run_time=0.25 * d, rate_func=linear)
      self.play(Write(fa), t.animate.set_value(t.get_value() + 0.3 * d * 0.9), run_time=0.3 * d, rate_func=linear)
      self.play(Write(fb), t.animate.set_value(t.get_value() + 0.25 * d * 0.9), run_time=0.25 * d, rate_func=linear)
      self.play(FadeIn(fh), t.animate.set_value(t.get_value() + 0.1 * d * 0.9), run_time=0.1 * d, rate_func=linear)

    with self.say('s06_epsilon') as d:
      ax = Axes(x_range=[0, TAU_, PI / 2], y_range=[0, 1.6, 0.5], x_length=6.0, y_length=2.5, tips=False,
                axis_config={'color': MUTED, 'stroke_width': 2}).move_to([2.9, -1.55, 0])
      ca = ax.plot(rate_a, x_range=[0, TAU_], color=DOOR_A, stroke_width=4)
      cb = ax.plot(rate_b, x_range=[0, TAU_], color=DOOR_B, stroke_width=4)
      lo = DashedLine(ax.c2p(0, 0.5), ax.c2p(TAU_, 0.5), color=MUTED, stroke_width=2, dash_length=0.1)
      hi = DashedLine(ax.c2p(0, 1.5), ax.c2p(TAU_, 1.5), color=MUTED, stroke_width=2, dash_length=0.1)
      ylo = M(r'\frac12', 0.55, MUTED).next_to(ax.c2p(0, 0.5), LEFT, buff=0.15)
      yhi = M(r'\frac32', 0.55, MUTED).next_to(ax.c2p(0, 1.5), LEFT, buff=0.15)
      y1 = M(r'1', 0.55, MUTED).next_to(ax.c2p(0, 1.0), LEFT, buff=0.15)
      xt = M(r'\text{one turn of } t', 0.55, MUTED).next_to(ax.x_axis, DOWN, buff=0.15)
      eps = M(r'0 < \varepsilon < 1, \qquad \varepsilon = \frac12', 0.8, SECONDARY).next_to(forms, DOWN, buff=0.3)
      eps.set_x(forms.get_center()[0])
      marker = always_redraw(lambda: Line(ax.c2p(t.get_value() % TAU_, 0), ax.c2p(t.get_value() % TAU_, 1.6),
                                          color=SECONDARY, stroke_width=2))
      w = 0.9
      t0 = t.get_value()
      self.play(Write(eps), t.animate.set_value(t0 + w * 0.3 * d), run_time=0.3 * d, rate_func=linear)
      self.play(Create(ax), FadeIn(xt), t.animate.set_value(t0 + w * 0.45 * d), run_time=0.15 * d, rate_func=linear)
      self.add(marker)
      self.play(Create(ca), Create(cb), FadeIn(VGroup(lo, hi, ylo, yhi, y1)),
                t.animate.set_value(t0 + w * 0.7 * d), run_time=0.25 * d, rate_func=linear)
      self.play(t.animate.set_value(t0 + w * 0.95 * d), run_time=0.25 * d, rate_func=linear)

    with self.say('s06_order') as d:
      nxt = TAU_ * np.ceil(t.get_value() / TAU_ + 1e-6)
      self.play(t.animate.set_value(nxt), run_time=0.25 * d, rate_func=linear)
      pa = Dot(ax.c2p(0, 1.5), color=DOOR_A, radius=0.09)
      pb = Dot(ax.c2p(PI / 2, 1.5), color=DOOR_B, radius=0.09)
      ta = T('a widest', 0.55, DOOR_A).next_to(pa, UP, buff=0.18).shift(0.6 * RIGHT)
      tb = T('b widest', 0.55, DOOR_B).next_to(pb, UP, buff=0.18).shift(0.25 * RIGHT)
      self.play(FadeIn(pa, scale=0.5), FadeIn(ta), FadeOut(eps), run_time=0.2 * d)
      self.play(FadeIn(pb, scale=0.5), FadeIn(tb), run_time=0.2 * d)
      qb = Brace(Line(ax.c2p(0, 0), ax.c2p(PI / 2, 0)), DOWN, buff=0.15, color=SECONDARY)
      ql = T('quarter turn', 0.5, SECONDARY).next_to(qb, DOWN, buff=0.08)
      self.play(GrowFromCenter(qb), FadeIn(ql), FadeOut(xt), run_time=0.2 * d)

    with self.say('s06_conjecture') as d:
      right = VGroup(forms, ax, ca, cb, lo, hi, ylo, yhi, y1, pa, pb, ta, tb, qb, ql)
      self.remove(marker)
      self.play(FadeOut(right), run_time=0.12 * d)
      who = T(r'Maier, Deg\"unther, van der Meer \& Seifert', 0.62)
      where = T(r'\emph{J.\ Stat.\ Phys.}\ 191, 104 (2024)', 0.55, MUTED)
      conj = M(r'\text{conjecture:}\quad \hat\sigma \;\le\; \sigma', 0.95, SECONDARY)
      how = T('test built from forward-schedule data only', 0.6, MUTED)
      card_g = VGroup(who, where, conj, how).arrange(DOWN, buff=0.28)
      cardm = card(card_g, color=MUTED).move_to([2.8, 1.2, 0])
      self.play(FadeIn(cardm), run_time=0.35 * d)
      self.play(Indicate(conj, color=SECONDARY), t.animate.set_value(t.get_value() + 0.3 * d), run_time=0.35 * d, rate_func=linear)

    with self.say('s06_forward') as d:
      c1 = clock(np.array([-0.3, -1.35, 0]), 0.32)
      arc1 = Arc(radius=0.48, start_angle=PI / 2 - 0.2, angle=1.6, color=ACCENT, stroke_width=3).move_arc_center_to(c1[0].get_center())
      arc1.add_tip(tip_length=0.13)
      r1 = T('true backwards film: schedule reversed too', 0.6, ACCENT).next_to(c1, RIGHT, buff=0.45)
      c2 = clock(np.array([-0.3, -2.55, 0]), 0.32)
      arc2 = Arc(radius=0.48, start_angle=PI / 2 + 0.2, angle=-1.6, color=WARN, stroke_width=3).move_arc_center_to(c2[0].get_center())
      arc2.add_tip(tip_length=0.13)
      r2 = T('the test: jumps reversed, schedule forwards', 0.6, WARN).next_to(c2, RIGHT, buff=0.45)
      t0 = t.get_value()
      self.play(FadeIn(c1), Create(arc1), FadeIn(r1), t.animate.set_value(t0 + 0.35 * d), run_time=0.4 * d, rate_func=linear)
      self.play(FadeIn(c2), Create(arc2), FadeIn(r2), t.animate.set_value(t0 + 0.7 * d), run_time=0.4 * d, rate_func=linear)
    self.wait(0.3)


# --------------------------------------------------------------------------------------
# 7. Zero waste
# --------------------------------------------------------------------------------------

class ZeroWaste(NarratedScene):
  def construct(self):
    t = ValueTracker(0.0)
    b = Board(center=[-3.2, -0.3, 0], scale=1.0, hidden=True, dynamic=t)
    la = M('a', 0.7, DOOR_A).move_to(b.mid('12', out=0.75))
    lb = M('b', 0.7, DOOR_B).move_to(b.mid('23', out=0.75))
    self.add(b.group, la, lb)

    def arrows():
      tt = t.get_value()
      out = VGroup()
      for (i, j), fn, col in (((1, 2), rate_a, DOOR_A), ((2, 1), rate_a, DOOR_A), ((2, 3), rate_b, DOOR_B),
                              ((3, 2), rate_b, DOOR_B), ((1, 3), lambda _: 1.0, HIDDEN), ((3, 1), lambda _: 1.0, HIDDEN)):
        out.add(traffic_arrow(b, i, j, width=1.0 + 5.0 * fn(tt), color=col, offset=0.19))
      return out
    arr = always_redraw(arrows)

    with self.say('s07_symmetric') as d:
      self.play(FadeIn(arr), run_time=0.2 * d)
      eq = M(r'\text{rate } 1\!\to\!2 \;=\; \text{rate } 2\!\to\!1 \;=\; a(t)', 0.72).move_to([3.0, 1.6, 0])
      eq2 = M(r'\text{rate } 2\!\to\!3 \;=\; \text{rate } 3\!\to\!2 \;=\; b(t)', 0.72).next_to(eq, DOWN, buff=0.35)
      eq[0][-4:].set_color(DOOR_A)
      eq2[0][-4:].set_color(DOOR_B)
      self.play(Write(eq), t.animate.set_value(1.6), run_time=0.4 * d, rate_func=linear)
      self.play(Write(eq2), t.animate.set_value(3.2), run_time=0.35 * d, rate_func=linear)

    with self.say('s07_third') as d:
      probs = VGroup(*[M(r'\frac13', 0.62, SECONDARY).move_to(b.prob_pos(i)) for i in TRI])
      self.play(FadeIn(probs), t.animate.set_value(4.4), run_time=0.3 * d, rate_func=linear)
      io = M(r'\text{traffic in} \;=\; \text{traffic out}', 0.75).move_to([3.0, -0.4, 0])
      self.play(Write(io), t.animate.set_value(6.0), run_time=0.35 * d, rate_func=linear)
      self.play(Indicate(probs, color=SECONDARY), t.animate.set_value(7.0), run_time=0.25 * d, rate_func=linear)

    with self.say('s07_zero') as d:
      z = M(r'\sigma = 0', 1.4, GOOD).move_to([3.0, -2.0, 0])
      zb = boxed(z, color=GOOD, buff=0.25)
      nw = T('no waste', 0.65, GOOD).next_to(zb, RIGHT, buff=0.35)
      self.play(Write(z), t.animate.set_value(8.0), run_time=0.35 * d, rate_func=linear)
      self.play(Create(zb), FadeIn(nw), t.animate.set_value(9.0), run_time=0.3 * d, rate_func=linear)
    self.play(t.animate.set_value(9.6), run_time=0.4, rate_func=linear)


# --------------------------------------------------------------------------------------
# 8. Where the waiting-time asymmetry comes from
# --------------------------------------------------------------------------------------

def phase_samples(weight, n, seed):
  rng = np.random.default_rng(seed)
  out = []
  while len(out) < n:
    x = rng.random() * TAU_
    if rng.random() * 1.5 < weight(x):
      out.append(x)
  return np.array(out)


class TimeOrder(NarratedScene):
  def construct(self):
    ax = Axes(x_range=[0, TAU_, PI / 2], y_range=[0, 1.6, 0.5], x_length=9.5, y_length=3.4, tips=False,
              axis_config={'color': MUTED, 'stroke_width': 2}).move_to([0.3, 0.9, 0])
    ca = ax.plot(rate_a, x_range=[0, TAU_], color=DOOR_A, stroke_width=4)
    cb = ax.plot(rate_b, x_range=[0, TAU_], color=DOOR_B, stroke_width=4)
    na = M('a', 0.75, DOOR_A).next_to(ax.c2p(TAU_, rate_a(TAU_)), RIGHT, buff=0.15)
    nb = M('b', 0.75, DOOR_B).next_to(ax.c2p(TAU_, rate_b(TAU_)), RIGHT, buff=0.15)
    xlabels = VGroup(M(r'\text{start}', 0.55, MUTED).next_to(ax.c2p(0, 0), DOWN, buff=0.15),
                     M(r'\text{quarter turn}', 0.55, MUTED).next_to(ax.c2p(PI / 2, 0), DOWN, buff=0.15),
                     M(r'\text{next start}', 0.55, MUTED).next_to(ax.c2p(TAU_, 0), DOWN, buff=0.15))
    self.add(ax, ca, cb, na, nb, xlabels)

    strip_a_y, strip_b_y = -1.55, -2.55
    sa = phase_samples(rate_a, 46, seed=21)
    sb = phase_samples(rate_b, 46, seed=22)
    jit = np.random.default_rng(5).uniform(-0.12, 0.12, 46)
    dots_a = VGroup(*[Dot([ax.c2p(x, 0)[0], strip_a_y + jit[k], 0], radius=0.05, color=DOOR_A) for k, x in enumerate(sa)])
    dots_b = VGroup(*[Dot([ax.c2p(x, 0)[0], strip_b_y + jit[k], 0], radius=0.05, color=DOOR_B) for k, x in enumerate(sb)])
    lab_a = M(r'\text{hops } 1\!\to\!2', 0.58, DOOR_A).next_to(np.array([ax.c2p(0, 0)[0], strip_a_y, 0]), LEFT, buff=0.35)
    lab_b = M(r'\text{hops } 3\!\to\!2', 0.58, DOOR_B).next_to(np.array([ax.c2p(0, 0)[0], strip_b_y, 0]), LEFT, buff=0.35)

    def tangent(fn, dfn, x0, half=0.55, color=SECONDARY):
      p = np.array(ax.c2p(x0, fn(x0)))
      q = np.array(ax.c2p(x0 + 0.5, fn(x0) + 0.5 * dfn(x0)))
      u = (q - p) / np.linalg.norm(q - p)
      return Arrow(p - 0.1 * u, p + half * 2 * u, buff=0, color=color, stroke_width=5,
                   max_tip_length_to_length_ratio=0.25, tip_length=0.2)

    with self.say('s08_weight') as d:
      self.play(FadeIn(lab_a), run_time=0.12 * d)
      self.play(LaggedStart(*[FadeIn(dd, scale=0.5) for dd in dots_a], lag_ratio=0.04), run_time=0.45 * d)
      hl = VGroup(SurroundingRectangle(VGroup(*[dd for dd, x in zip(dots_a, sa) if x < 0.9]), color=SECONDARY, buff=0.08),
                  SurroundingRectangle(VGroup(*[dd for dd, x in zip(dots_a, sa) if x > TAU_ - 0.9]), color=SECONDARY, buff=0.08))
      self.play(Create(hl), Indicate(ca, color=DOOR_A), run_time=0.25 * d)

    with self.say('s08_forward') as d:
      ta0 = tangent(rate_b, lambda x: EPS * np.cos(x), 0.0)
      ta1 = tangent(rate_b, lambda x: EPS * np.cos(x), TAU_ - 0.35)
      txt = T('b opening', 0.6, SECONDARY).move_to(ax.c2p(0.8, 0.72))
      self.play(GrowArrow(ta0), GrowArrow(ta1), FadeIn(txt), run_time=0.35 * d)
      up = M(r'\text{next hop } 2\!\to\!3: \text{ chance rising}', 0.65, DOOR_B).move_to([2.8, 3.05, 0])
      self.play(FadeIn(up), run_time=0.25 * d)

    with self.say('s08_backward') as d:
      self.play(FadeOut(hl), dots_a.animate.set_opacity(0.3), lab_a.animate.set_opacity(0.4),
                ta0.animate.set_opacity(0.3), ta1.animate.set_opacity(0.3), txt.animate.set_opacity(0.3),
                up.animate.set_opacity(0.35), run_time=0.1 * d)
      self.play(FadeIn(lab_b), LaggedStart(*[FadeIn(dd, scale=0.5) for dd in dots_b], lag_ratio=0.04), run_time=0.35 * d)
      tb0 = tangent(rate_a, lambda x: -EPS * np.sin(x), PI / 2)
      txt2 = T('a closing', 0.6, SECONDARY).move_to(ax.c2p(2.5, 0.4))
      self.play(GrowArrow(tb0), FadeIn(txt2), run_time=0.25 * d)
      dn = M(r'\text{next hop } 2\!\to\!1: \text{ chance falling}', 0.65, DOOR_A).move_to([2.8, 3.05, 0])
      self.play(FadeOut(up), FadeIn(dn), run_time=0.15 * d)

    with self.say('s08_meaning') as d:
      allm = VGroup(ax, ca, cb, na, nb, xlabels, dots_a, dots_b, lab_a, lab_b, ta0, ta1, tb0, txt, txt2, dn)
      self.play(FadeOut(allm), run_time=0.15 * d)
      m1 = T(r"the schedule's arrow: \textbf{a opens before b}", 0.85, SECONDARY)
      m2 = VGroup(T('not waste:', 0.75), M(r'\sigma = 0', 0.95, GOOD)).arrange(RIGHT, buff=0.3)
      VGroup(m1, m2).arrange(DOWN, buff=0.5).move_to([0, 0.2, 0])
      self.play(Write(m1), run_time=0.4 * d)
      self.play(FadeIn(m2, shift=0.2 * UP), run_time=0.2 * d)
    self.wait(0.3)


# --------------------------------------------------------------------------------------
# 9. The exact slope identity
# --------------------------------------------------------------------------------------

class Proof(NarratedScene):
  def construct(self):
    ax = Axes(x_range=[0, 1.2, 0.4], y_range=[0, 1.1, 0.5], x_length=5.4, y_length=4.0, tips=False,
              axis_config={'color': MUTED, 'stroke_width': 2}).move_to([-3.3, -0.4, 0])
    xl = M(r'\text{wait } s', 0.6, MUTED).next_to(ax.x_axis, DOWN, buff=0.25)
    y1 = M('1', 0.55, MUTED).next_to(ax.c2p(0, 1), LEFT, buff=0.15)
    fc = ax.plot(lambda s: fg(s)[0], x_range=[0, 1.2], color=DOOR_A, stroke_width=4)
    gc = ax.plot(lambda s: fg(s)[1], x_range=[0, 1.2], color=DOOR_B, stroke_width=4)
    fl = M('f', 0.75, DOOR_A).next_to(ax.c2p(1.2, fg(1.2)[0]), UR, buff=0.08)
    gl = M('g', 0.75, DOOR_B).next_to(ax.c2p(1.2, fg(1.2)[1]), DR, buff=0.08)

    with self.say('s09_curves') as d:
      self.play(Create(ax), FadeIn(xl), FadeIn(y1), run_time=0.15 * d)
      self.play(Create(fc), FadeIn(fl), run_time=0.2 * d)
      self.play(Create(gc), FadeIn(gl), run_time=0.2 * d)
      lf = M(r'f:\ \ 1\!\to\!2,\ \text{then}\ 2\!\to\!3', 0.7, DOOR_A)
      lg = M(r'g:\ \ 3\!\to\!2,\ \text{then}\ 2\!\to\!1', 0.7, DOOR_B)
      l0 = M(r'f(0) = g(0) = 1', 0.8)
      leg = VGroup(lf, lg, l0).arrange(DOWN, buff=0.4, aligned_edge=LEFT).move_to([3.2, 0.6, 0])
      self.play(FadeIn(lf), FadeIn(lg), run_time=0.15 * d)
      self.play(Write(l0), Flash(ax.c2p(0, 1), color=SECONDARY), run_time=0.2 * d)

    with self.say('s09_slopes') as d:
      tf = Line(ax.c2p(0, 1), ax.c2p(0.42, 1 - 2.125 * 0.42), color=DOOR_A, stroke_width=3).set_opacity(0.9)
      tg = Line(ax.c2p(0, 1), ax.c2p(0.42, 1 - 2.375 * 0.42), color=DOOR_B, stroke_width=3).set_opacity(0.9)
      tfd, tgd = DashedVMobject(tf, num_dashes=12), DashedVMobject(tg, num_dashes=12)
      self.play(Create(tfd), Create(tgd), run_time=0.3 * d)
      n1 = M(r"a' = \text{how fast } a \text{ changes}", 0.7)
      n2 = M(r"\langle\,\cdots\rangle = \text{average over one turn}", 0.7)
      notes = VGroup(n1, n2).arrange(DOWN, buff=0.4, aligned_edge=LEFT).move_to([3.2, -1.9, 0])
      self.play(FadeIn(n1), run_time=0.25 * d)
      self.play(FadeIn(n2), run_time=0.25 * d)
    graph = VGroup(ax, xl, y1, fc, gc, fl, gl, tfd, tgd)

    with self.say('s09_split') as d:
      self.play(FadeOut(graph), FadeOut(VGroup(lf, lg, l0)), notes.animate.scale(0.8).to_corner(UR, buff=0.4),
                run_time=0.12 * d)
      e1 = MathTex(r"f'(0)", '=', r"\langle a\,b' \rangle", '-', r"\langle a\,b\,(a+b) \rangle").scale(0.95)
      e2 = MathTex(r"g'(0)", '=', r"\langle b\,a' \rangle", '-', r"\langle a\,b\,(a+b) \rangle").scale(0.95)
      e1[0].set_color(DOOR_A)
      e2[0].set_color(DOOR_B)
      eqs = VGroup(e1, e2).arrange(DOWN, buff=0.5).move_to([0, 1.4, 0])
      e2.shift((e1[1].get_center()[0] - e2[1].get_center()[0]) * RIGHT)
      self.play(Write(e1), run_time=0.18 * d)
      self.play(Write(e2), run_time=0.18 * d)
      common = VGroup(boxed(e1[4], buff=0.08), boxed(e2[4], buff=0.08))
      lv = T('leaving square 2', 0.6, SECONDARY).next_to(common, RIGHT, buff=0.3)
      self.play(Create(common), FadeIn(lv), run_time=0.15 * d)
      diff = MathTex(r"(f-g)'(0)", '=', r"\langle a\,b' \rangle", '-', r"\langle b\,a' \rangle").scale(0.95)
      diff.move_to([0, -0.6, 0])
      strike = VGroup(Line(e1[4].get_left(), e1[4].get_right(), color=WARN, stroke_width=5),
                      Line(e2[4].get_left(), e2[4].get_right(), color=WARN, stroke_width=5))
      self.play(Create(strike), run_time=0.1 * d)
      self.play(TransformFromCopy(e1[2], diff[2]), TransformFromCopy(e2[2], diff[4]), FadeIn(diff[0]), FadeIn(diff[1]),
                FadeIn(diff[3]), FadeOut(lv), run_time=0.14 * d)
      self.remove(*diff)
      self.add(diff)

    with self.say('s09_left') as d:
      self.play(FadeOut(VGroup(e1, e2, common, strike)), diff.animate.move_to([0, 1.8, 0]), run_time=0.25 * d)
      diff2 = MathTex(r"(f-g)'(0)", '=', r"\langle\, a\,b' - b\,a' \,\rangle").scale(0.95).move_to([0, 1.8, 0])
      self.play(TransformMatchingTex(diff, diff2), run_time=0.45 * d)

    with self.say('s09_plug') as d:
      da = M(r"a = 1+\varepsilon\cos t, \qquad a' = -\varepsilon\sin t", 0.72, DOOR_A)
      db = M(r"b = 1+\varepsilon\sin t, \qquad b' = \varepsilon\cos t", 0.72, DOOR_B)
      doors = VGroup(da, db).arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to([0, 0.35, 0])
      self.play(FadeIn(da), run_time=0.2 * d)
      self.play(FadeIn(db), run_time=0.2 * d)
      p1 = MathTex(r"a\,b'", '=', r'\varepsilon\cos t', '+', r'\varepsilon^2\cos^2 t').scale(0.85)
      p2 = MathTex(r"b\,a'", '=', r'-\varepsilon\sin t', '-', r'\varepsilon^2\sin^2 t').scale(0.85)
      prods = VGroup(p1, p2).arrange(DOWN, buff=0.35).move_to([0, -1.6, 0])
      p2.shift((p1[1].get_center()[0] - p2[1].get_center()[0]) * RIGHT)
      self.play(Write(p1), run_time=0.25 * d)
      self.play(Write(p2), run_time=0.25 * d)

    with self.say('s09_pythag') as d:
      self.play(FadeOut(doors), prods.animate.move_to([0, 0.5, 0]), run_time=0.1 * d)
      s1 = MathTex(r"a\,b' - b\,a'", '=', r'\varepsilon\cos t', '+', r'\varepsilon\sin t', '+', r'\varepsilon^2',
                   r'(\cos^2 t + \sin^2 t)').scale(0.85).move_to([0, -1.0, 0])
      self.play(TransformFromCopy(prods, s1), run_time=0.2 * d)
      py = boxed(s1[7], color=SECONDARY, buff=0.08)
      one = M(r'=1', 0.7, SECONDARY).next_to(py, DOWN, buff=0.15)
      self.play(Create(py), FadeIn(one), run_time=0.12 * d)
      s2 = MathTex(r"a\,b' - b\,a'", '=', r'\varepsilon\cos t', '+', r'\varepsilon\sin t', '+', r'\varepsilon^2').scale(0.85)
      s2.move_to(s1)
      self.play(FadeOut(py), FadeOut(one), TransformMatchingTex(s1, s2), FadeOut(prods), run_time=0.15 * d)
      # A cosine wave whose positive and negative areas cancel over a full turn.
      wax = Axes(x_range=[0, TAU_, PI], y_range=[-1.2, 1.2, 1], x_length=3.6, y_length=1.3, tips=False,
                 axis_config={'color': MUTED, 'stroke_width': 1.5}).move_to([0, -2.6, 0])
      wave = wax.plot(np.cos, x_range=[0, TAU_], color=INK, stroke_width=3)
      pos = VGroup(wax.get_area(wave, x_range=[0, PI / 2], color=SECONDARY, opacity=0.4),
                   wax.get_area(wave, x_range=[3 * PI / 2, TAU_], color=SECONDARY, opacity=0.4))
      neg = wax.get_area(wave, x_range=[PI / 2, 3 * PI / 2], color=MUTED, opacity=0.4)
      avg = M(r'\langle \cos t \rangle = \langle \sin t \rangle = 0', 0.65).next_to(wax, RIGHT, buff=0.4)
      self.play(Create(wax), Create(wave), FadeIn(pos), FadeIn(neg), FadeIn(avg), run_time=0.18 * d)
      self.play(s2[2].animate.set_opacity(0.25), s2[4].animate.set_opacity(0.25), run_time=0.08 * d)
      res = MathTex(r"(f-g)'(0)", '=', r'\varepsilon^2').scale(1.15).move_to([0, -1.0, 0])
      self.play(FadeOut(diff2), FadeOut(VGroup(wax, wave, pos, neg, avg)), ReplacementTransform(s2, res), run_time=0.12 * d)
      rb = boxed(res, color=SECONDARY, buff=0.2)
      self.play(Create(rb), run_time=0.05 * d)

    with self.say('s09_numbers') as d:
      key = VGroup(res, rb)
      self.play(key.animate.scale(0.8).to_edge(UP, buff=0.6), FadeOut(notes), run_time=0.08 * d)
      v1 = M(r"f'(0) = -2-\frac12\varepsilon^2 = -2.125", 0.8, DOOR_A)
      v2 = M(r"g'(0) = -2-\frac32\varepsilon^2 = -2.375", 0.8, DOOR_B)
      v3 = M(r'\text{gap} = \frac14 > 0 \qquad (\varepsilon = \frac12)', 0.8, SECONDARY)
      vals = VGroup(v1, v2, v3).arrange(DOWN, buff=0.35).move_to([0, 0.4, 0])
      self.play(FadeIn(v1), run_time=0.14 * d)
      self.play(FadeIn(v2), run_time=0.14 * d)
      self.play(FadeIn(v3), run_time=0.12 * d)
      lines = [r"PASS f'(0) = -2 - epsilon\^{}2/2", r"PASS g'(0) = -2 - 3 epsilon\^{}2/2",
               r"PASS (f-g)'(0) = epsilon\^{}2"]
      chk = VGroup(*[Tex(r'\texttt{' + s + '}', color=GOOD).scale(0.55) for s in lines]).arrange(DOWN, buff=0.15, aligned_edge=LEFT)
      head = T(r'\texttt{check\_short\_lag.py}, exact fractions', 0.55, MUTED)
      box = card(VGroup(head, chk).arrange(DOWN, buff=0.22, aligned_edge=LEFT), color=GOOD, buff=0.3).move_to([0, -2.3, 0])
      self.play(FadeIn(box, shift=0.2 * UP), run_time=0.2 * d)
    self.wait(0.3)


# --------------------------------------------------------------------------------------
# 10. The verdict
# --------------------------------------------------------------------------------------

class Verdict(NarratedScene):
  def construct(self):
    ax = Axes(x_range=[0, 2.5, 0.5], y_range=[-0.02, 0.04, 0.01], x_length=9.0, y_length=4.6, tips=False,
              axis_config={'color': MUTED, 'stroke_width': 2}).move_to([0.2, -0.3, 0])
    ylabs = VGroup(*[M(f'{v:.2f}', 0.5, MUTED).next_to(ax.c2p(0, v), LEFT, buff=0.15) for v in (-0.01, 0.0, 0.01, 0.02, 0.03)])
    xlabs = VGroup(*[M(f'{v:g}', 0.5, MUTED).next_to(ax.c2p(v, -0.02), DOWN, buff=0.15) for v in (0.5, 1, 1.5, 2, 2.5)])
    xl = M(r'\text{wait } s', 0.6, MUTED).next_to(ax.c2p(1.25, -0.02), DOWN, buff=0.55)
    diff = ax.plot(lambda s: fg(s)[0] - fg(s)[1], x_range=[0, 2.5], color=WARN, stroke_width=4)
    title_ = M(r'f - g \qquad (\varepsilon = \frac12)', 0.8, WARN).to_edge(UP, buff=0.55)

    with self.say('s11_plot') as d:
      self.play(Create(ax), FadeIn(ylabs), FadeIn(xlabs), FadeIn(xl), FadeIn(title_), run_time=0.2 * d)
      self.play(Create(diff), run_time=0.35 * d)
      tan = DashedLine(ax.c2p(0, 0), ax.c2p(0.13, 0.25 * 0.13), color=SECONDARY, stroke_width=3, dash_length=0.06)
      tl = M(r'\text{slope } \frac14', 0.6, SECONDARY).next_to(ax.c2p(0.13, 0.0325), RIGHT, buff=0.15)
      self.play(Create(tan), FadeIn(tl), run_time=0.15 * d)
      over = T('g overtakes', 0.6, DOOR_B).next_to(ax.c2p(1.6, -0.011), DOWN, buff=0.1)
      self.play(FadeIn(over), Indicate(diff, color=WARN, scale_factor=1.0), run_time=0.15 * d)
    plot1 = VGroup(ax, ylabs, xlabs, xl, diff, title_, tan, tl, over)

    with self.say('s11_nocancel') as d:
      self.play(FadeOut(plot1), run_time=0.1 * d)
      ax2 = Axes(x_range=[0, 4.5, 0.5], y_range=[0, 0.005, 0.001], x_length=9.0, y_length=3.0, tips=False,
                 axis_config={'color': MUTED, 'stroke_width': 2}).move_to([0.2, -1.5, 0])
      ax2l = M(r'\text{wait } s', 0.6, MUTED).next_to(ax2.x_axis, DOWN, buff=0.25)

      def score(s):
        f, g = fg(s)
        return (f - g) * np.log(f / g) if f > 0 and g > 0 else 0.0
      sc = ax2.plot(score, x_range=[0, 4.5], color=WARN, stroke_width=4)
      area = ax2.get_area(sc, x_range=[0, 4.5], color=WARN, opacity=0.35)
      st = M(r'\text{score} = (f-g)\times\log\frac{f}{g}', 0.85).move_to([0, 2.6, 0])
      r1 = M(r'f > g:\ \ (+)\times(+) > 0', 0.72).move_to([-2.6, 1.3, 0])
      r2 = M(r'g > f:\ \ (-)\times(-) > 0', 0.72).move_to([2.8, 1.3, 0])
      self.play(Write(st), run_time=0.25 * d)
      self.play(FadeIn(r1), run_time=0.15 * d)
      self.play(FadeIn(r2), run_time=0.15 * d)
      sl = M(r'\text{never below zero}', 0.65, WARN).move_to(ax2.c2p(3.6, 0.0042))
      self.play(Create(ax2), FadeIn(ax2l), Create(sc), run_time=0.15 * d)
      self.play(FadeIn(area), FadeIn(sl), run_time=0.12 * d)

    with self.say('s11_allpairs') as d:
      self.play(FadeOut(VGroup(ax2, ax2l, sc, area, st, r1, r2, sl)), run_time=0.12 * d)
      fourj = VGroup(*[arrow_lbl(i, j, 0.8, jump_color(i, j)) for (i, j) in ((1, 2), (2, 1), (2, 3), (3, 2))]).arrange(RIGHT, buff=0.7)
      each = M(r'\text{each: } \frac13 \text{ per unit of time}', 0.7, MUTED).next_to(fourj, DOWN, buff=0.35)
      top = VGroup(fourj, each).move_to([0, 1.3, 0])
      self.play(LaggedStart(*[FadeIn(x, shift=0.2 * DOWN) for x in fourj], lag_ratio=0.2), FadeIn(each), run_time=0.3 * d)
      kl = MathTex(r'\hat\sigma', '=', r'\frac43', r'\times', r'\text{mismatch}', '>', '0').scale(1.0).move_to([0, -0.6, 0])
      kl[0].set_color(WARN)
      kn = T('a standard measure: zero only when nothing mismatches', 0.6, MUTED).next_to(kl, DOWN, buff=0.4)
      self.play(Write(kl), run_time=0.3 * d)
      self.play(FadeIn(kn), run_time=0.15 * d)

    with self.say('s11_verdict') as d:
      self.play(FadeOut(VGroup(top, kn)), kl.animate.move_to([0, 1.8, 0]), run_time=0.12 * d)
      fin = T('and finite', 0.6, MUTED).next_to(kl, RIGHT, buff=0.4)
      self.play(FadeIn(fin), run_time=0.1 * d)
      sz = M(r'\sigma = 0', 1.2, GOOD).move_to([0, 0.4, 0])
      self.play(Write(sz), run_time=0.15 * d)
      cj = M(r'\text{conjecture:}\quad \hat\sigma \le \sigma', 1.0, SECONDARY).move_to([0, -1.2, 0])
      self.play(FadeIn(cj), run_time=0.18 * d)
      cross = Cross(cj[0][-4:], stroke_color=WARN, stroke_width=7, scale_factor=1.3)
      ff = T(r'\textbf{false}', 0.9, WARN).next_to(cj, DOWN, buff=0.45)
      self.play(Create(cross), FadeIn(ff, scale=0.7), run_time=0.2 * d)

    with self.say('s11_every') as d:
      self.play(FadeOut(VGroup(kl, fin, sz, cj, cross, ff)), run_time=0.12 * d)
      e = ValueTracker(0.05)
      nl = NumberLine(x_range=[0, 1, 0.25], length=7, color=MUTED, include_numbers=False).move_to([0, 0.4, 0])
      n0 = M('0', 0.6, MUTED).next_to(nl.n2p(0), DOWN, buff=0.2)
      n1 = M('1', 0.6, MUTED).next_to(nl.n2p(1), DOWN, buff=0.2)
      dot = always_redraw(lambda: Dot(nl.n2p(e.get_value()), color=SECONDARY, radius=0.11))
      el = always_redraw(lambda: M(r'\varepsilon', 0.75, SECONDARY).next_to(nl.n2p(e.get_value()), UP, buff=0.25))
      readout = always_redraw(lambda: VGroup(
        M(r'\text{slope gap } \varepsilon^2 =', 0.8),
        DecimalNumber(e.get_value() ** 2, num_decimal_places=3, color=WARN).scale(0.8)).arrange(RIGHT, buff=0.25).move_to([0, -1.2, 0]))
      rr = M(r'\text{rates stay between } 1-\varepsilon \text{ and } 1+\varepsilon:\ \text{never zero}', 0.65, MUTED).move_to([0, -2.4, 0])
      self.play(Create(nl), FadeIn(n0), FadeIn(n1), FadeIn(dot), FadeIn(el), FadeIn(readout), run_time=0.15 * d)
      self.play(e.animate.set_value(0.95), run_time=0.5 * d, rate_func=smooth)
      self.play(FadeIn(rr), run_time=0.15 * d)
    self.wait(0.3)


# --------------------------------------------------------------------------------------
# 11. Scope and status
# --------------------------------------------------------------------------------------

class Scope(NarratedScene):
  def construct(self):
    def show(card_mob, d, prev=None):
      anims = [FadeIn(card_mob, shift=0.2 * UP)]
      if prev is not None:
        anims.append(FadeOut(prev, shift=0.2 * UP))
      self.play(*anims, run_time=0.25 * d)

    with self.say('s12_kills') as d:
      c1 = statement('Disproved', r'the forward-only conjecture $\hat\sigma\le\sigma$, in its general form '
                     r'(Maier et al., \emph{J.\ Stat.\ Phys.}\ 2024, Eq.~18)', width=10, color=WARN)
      show(c1, d)

    with self.say('s12_survives') as d:
      c2 = statement('Still stands', r"the same paper's theorem that uses data from the schedule run "
                     r'backwards (Eq.~16)', width=10, color=ACCENT)
      c2.move_to([0, 0.9, 0])
      self.play(FadeOut(c1, shift=0.2 * UP), FadeIn(c2, shift=0.2 * UP), run_time=0.25 * d)
      a1 = T('reverse the jumps', 0.65, MUTED)
      ne = M(r'\neq', 0.9)
      a2 = T('reverse the whole film', 0.65, ACCENT)
      row = VGroup(a1, ne, a2).arrange(RIGHT, buff=0.45).move_to([0, -1.2, 0])
      self.play(FadeIn(row, shift=0.2 * UP), run_time=0.3 * d)

    with self.say('s12_prior') as d:
      c3 = statement('Known before', r'waiting-time false alarms at equilibrium (Hartich \& Godec); '
                     r'backwards-schedule data for driven machines (Harunari, Fiore \& Barato)', width=10, color=MUTED)
      self.play(FadeOut(VGroup(c2, row), shift=0.2 * UP), FadeIn(c3, shift=0.2 * UP), run_time=0.25 * d)
      new = T(r'new here: an exact counterexample to this conjecture', 0.7, SECONDARY).next_to(c3, DOWN, buff=0.6)
      self.wait(0.35 * d)
      self.play(FadeIn(new), run_time=0.2 * d)

    with self.say('s12_device') as d:
      c4 = statement('Not claimed', r'anything about the energy used by the device that turns the doors; '
                     r'it is not part of this $\sigma$', width=10, color=MUTED)
      self.play(FadeOut(VGroup(c3, new), shift=0.2 * UP), FadeIn(c4, shift=0.2 * UP), run_time=0.25 * d)

    with self.say('s12_status') as d:
      self.play(FadeOut(c4, shift=0.2 * UP), run_time=0.1 * d)
      head = T(r'\textbf{status}', 0.8, SECONDARY)
      rows = [
        (r'\checkmark', GOOD, 'written proof, no simulation needed'),
        (r'\checkmark', GOOD, 'exact computer check of the slope algebra'),
        (r'\checkmark', GOOD, 'internal reviews of the probability steps'),
        (r'\circ', MUTED, 'not yet: formal machine proof, outside peer review'),
      ]
      items = VGroup(*[VGroup(M(sym, 0.8, col), T(txt, 0.65, INK if col == GOOD else MUTED)).arrange(RIGHT, buff=0.3)
                       for sym, col, txt in rows]).arrange(DOWN, buff=0.32, aligned_edge=LEFT)
      grp = VGroup(head, items).arrange(DOWN, buff=0.5).move_to(ORIGIN)
      self.play(FadeIn(head), run_time=0.1 * d)
      for k, it in enumerate(items):
        self.play(FadeIn(it, shift=0.15 * RIGHT), run_time=0.13 * d)
        self.wait(0.05 * d)
    self.wait(0.3)


# --------------------------------------------------------------------------------------
# 12. Recap, open questions, end card
# --------------------------------------------------------------------------------------

class Recap(NarratedScene):
  def construct(self):
    lines = [
      ('s13_one', r'\textbf{1.}\ \ entropy production measures waste; here $\sigma = 0$'),
      ('s13_two', r'\textbf{2.}\ \ doors open in a fixed order, so a pair and its reverse wait differently'),
      ('s13_three', r'\textbf{3.}\ \ a forward-schedule test mistakes that order for waste: the bound fails'),
    ]
    mobs = VGroup(*[T(txt, 0.72) for _, txt in lines]).arrange(DOWN, buff=0.6, aligned_edge=LEFT).move_to(ORIGIN)
    for k, (key, _) in enumerate(lines):
      with self.say(key) as d:
        if k > 0:
          self.play(mobs[k - 1].animate.set_opacity(0.45), run_time=0.1 * d)
        self.play(FadeIn(mobs[k], shift=0.2 * RIGHT), run_time=0.3 * d)

    with self.say('s13_open') as d:
      self.play(FadeOut(mobs), run_time=0.1 * d)
      head = T(r'\textbf{still unknown}', 0.85, SECONDARY)
      q1 = T('is a narrower forward-only test safe, with extra rules on the rates?', 0.68)
      q2 = T('was this counterexample found before? (search careful, not complete)', 0.68)
      grp = VGroup(head, q1, q2).arrange(DOWN, buff=0.5).move_to(ORIGIN)
      self.play(FadeIn(head), run_time=0.12 * d)
      self.play(FadeIn(q1, shift=0.2 * UP), run_time=0.2 * d)
      self.wait(0.2 * d)
      self.play(FadeIn(q2, shift=0.2 * UP), run_time=0.2 * d)

    with self.say('s13_end') as d:
      self.play(FadeOut(grp), run_time=0.3)
      t1 = T(r'A counterexample to a periodic waiting-time entropy bound', 0.85)
      t2 = T('Valyu Research, 2026', 0.7, MUTED)
      t3 = Tex(r'\texttt{physics/statistical-physics/thermodynamic-inference/periodic-waiting-time}', color=MUTED).scale(0.55)
      t4 = T('Narration uses a synthetic voice.', 0.55, MUTED)
      endc = VGroup(t1, t2, t3, t4).arrange(DOWN, buff=0.45).move_to(ORIGIN)
      self.play(FadeIn(t1, shift=0.2 * UP), run_time=0.5)
      self.play(FadeIn(VGroup(t2, t3, t4)), run_time=0.5)
    self.wait(3.5)
