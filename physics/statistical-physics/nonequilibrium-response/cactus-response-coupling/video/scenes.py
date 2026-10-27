"""Explainer: why loops of states respond in a predictable way (cactus networks and the
Fancher-Horowitz response conjecture).

Running example: the driven triangle (clockwise rate 2, anticlockwise rate 1), knob = rate of 0 -> 1.
Every number on screen is recomputed by check_numbers.py, which writes numbers.json (read below).
"""

import json
from fractions import Fraction as Fr
from pathlib import Path

import numpy as np
from manim import *
from vrvideo import *

SCENES = ['Hook', 'Hopping', 'Trees', 'TreeTheorem', 'Knob', 'Families', 'Conjecture', 'Reframe', 'Staircase',
          'Tokens', 'WhyUC', 'Cactus', 'K4', 'Status', 'Ending']

NUM = json.loads((Path(__file__).resolve().parent / 'numbers.json').read_text())
STATE = PRIMARY
ROOT = ACCENT
KNOBC = SECONDARY
E_COL = [ORANGE, PURPLE_B, MAROON_C]  # token colours of edges {0,1}, {1,2}, {2,0}
DIM = '#3a3f47'
LN2 = float(np.log(2))


def T(s, scale=0.75, color=INK):
  return Tex(s, color=color).scale(scale)


def M(s, scale=0.75, color=INK):
  return MathTex(s, color=color).scale(scale)


def ring_pos(i, R=1.0, n=3, center=ORIGIN):
  ang = PI / 2 - 2 * PI * i / n
  return np.array(center, dtype=float) + R * np.array([np.cos(ang), np.sin(ang), 0.0])


def state(i, pos, r=0.34, label=True, color=STATE):
  under = Circle(r, stroke_width=0).set_fill(BACKGROUND, 1).move_to(pos)
  c = Circle(r, color=color, stroke_width=3).set_fill(color, 0.2).move_to(pos)
  g = VGroup(under, c)
  if label:
    g.add(MathTex(str(i)).scale(0.8 * r / 0.34).move_to(pos))
  return g


def dim(m, k):
  """Scale stroke and fill opacity of every part (set_opacity would make translucent fills solid)."""
  for sm in m.family_members_with_points():
    sm.set_stroke(opacity=sm.get_stroke_opacity() * k, family=False)
    sm.set_fill(opacity=sm.get_fill_opacity() * k, family=False)
  return m


def dimmed(m, k):
  return dim(m.copy(), k)


def arrow_between(p, q, r_node, off=0.0, color=INK, width=4, tip=0.2):
  p, q = np.array(p, dtype=float), np.array(q, dtype=float)
  d = (q - p) / np.linalg.norm(q - p)
  nrm = np.array([d[1], -d[0], 0.0])
  s = p + d * (r_node + 0.07) + nrm * off
  e = q - d * (r_node + 0.07) + nrm * off
  return Arrow(s, e, buff=0, stroke_width=width, color=color, tip_length=tip, max_tip_length_to_length_ratio=0.35,
               max_stroke_width_to_length_ratio=30)


def ring_tree(root, cut, n=3):
  """Arcs of the tree rooted at root that cuts edge {cut, cut+1}."""
  c = (cut - root) % n
  arcs = []
  for v in range(n):
    if v == root:
      continue
    s = (v - root) % n
    arcs.append((v, (v - 1) % n) if s <= c else (v, (v + 1) % n))
  return arcs


def tree_weight(arcs, n=3):
  w = 1
  for u, v in arcs:
    w *= 2 if v == (u + 1) % n else 1
  return w


class Ring(VGroup):
  """Bidirected ring of states; clockwise arrows on the inside, anticlockwise on the outside."""

  def __init__(self, n=3, R=1.8, center=ORIGIN, r=0.36, off=0.13, rates=True, rate_scale=0.75, width=4):
    super().__init__()
    self.pos = [ring_pos(i, R, n, center) for i in range(n)]
    self.nodes = VGroup(*[state(i, self.pos[i], r) for i in range(n)])
    self.arcs, self.rates = {}, {}
    arcs, labels = VGroup(), VGroup()
    for v in range(n):
      for u in [(v + 1) % n, (v - 1) % n]:
        a = arrow_between(self.pos[v], self.pos[u], r, off, width=width)
        self.arcs[(v, u)] = a
        arcs.add(a)
        d = (self.pos[u] - self.pos[v]) / np.linalg.norm(self.pos[u] - self.pos[v])
        nrm = np.array([d[1], -d[0], 0.0])
        lab = M('2' if u == (v + 1) % n else '1', rate_scale, MUTED)
        lab.move_to((self.pos[u] + self.pos[v]) / 2 + nrm * (off + 0.3))
        self.rates[(v, u)] = lab
        labels.add(lab)
    self.arc_group, self.label_group = arcs, labels
    self.add(arcs)
    if rates:
      self.add(labels)
    self.add(self.nodes)


class TreePic(VGroup):
  def __init__(self, root, cut, n=3, R=0.8, center=ORIGIN, r=0.24, knob=False, rates=False, cut_line=True,
               width=4):
    super().__init__()
    self.pos = [ring_pos(i, R, n, center) for i in range(n)]
    self.arcs = {}
    self.tree = ring_tree(root, cut, n)
    if cut_line:
      a, b = self.pos[cut], self.pos[(cut + 1) % n]
      d = (b - a) / np.linalg.norm(b - a)
      self.cut = DashedLine(a + d * r, b - d * r, dash_length=0.08, color=MUTED, stroke_width=2)
      self.add(self.cut)
    for (u, v) in self.tree:
      col = KNOBC if (knob and (u, v) == (0, 1)) else INK
      ar = arrow_between(self.pos[u], self.pos[v], r, 0.0, color=col, width=width, tip=0.17)
      self.arcs[(u, v)] = ar
      self.add(ar)
      if rates:
        mid = (self.pos[u] + self.pos[v]) / 2
        out = mid - np.array(center, dtype=float)
        out = out / np.linalg.norm(out)
        self.add(M('2' if v == (u + 1) % n else '1', 0.6, MUTED).move_to(mid + out * 0.3))
    self.nodes = VGroup(*[state(i, self.pos[i], r) for i in range(n)])
    self.ring = Circle(r + 0.09, color=ROOT, stroke_width=5).move_to(self.pos[root])
    self.add(self.nodes, self.ring)
    self.weight = tree_weight(self.tree, n)


def chips(fam, size=0.34, buff=0.08):
  return VGroup(*[RoundedRectangle(width=size, height=size, corner_radius=0.06, stroke_width=0).set_fill(E_COL[e], 1)
                  for e in fam]).arrange(RIGHT, buff=buff)


def tick(scale=1.0, color=OK):
  return MathTex(r'\checkmark', color=color).scale(scale)


def cross(center, r=0.2, color=WARN, width=6):
  return VGroup(Line(center + UL * r, center + DR * r), Line(center + UR * r, center + DL * r)).set_stroke(color, width)


def resp_axes():
  ax = Axes(x_range=[-0.85, 0.25, 1 / 3], y_range=[-0.45, 0.8, 1 / 3], x_length=5.7, y_length=6.5, tips=False,
            axis_config={'color': MUTED, 'stroke_width': 2, 'include_ticks': True, 'tick_size': 0.07})
  xl = T(r'relative response of $\pi_0$', 0.62, MUTED).next_to(ax.x_axis.get_left(), DOWN, buff=0.25).shift(RIGHT * 0.9)
  yl = T(r'relative response\\of $\pi_1$', 0.62, MUTED).next_to(ax.y_axis.get_top(), LEFT, buff=0.15)
  return ax, VGroup(ax, xl, yl)


def perch(ring, i, r=0.42):
  """Where the hopping dot sits next to state i: just outside the disc, away from the ring centre."""
  c = sum(ring.pos) / len(ring.pos)
  out = ring.pos[i] - c
  return ring.pos[i] + out / np.linalg.norm(out) * (r + 0.22)


PTS = {'o': (0, 0), 'a': (-1 / 3, 2 / 3), 'b': (-2 / 3, 1 / 3), 'x': (-1 / 3, -1 / 3)}
RESP = (-10 / 21, 8 / 21)


class Hook(NarratedScene):
  def construct(self):
    ring = Ring(R=2.0, center=UP * 0.35, rates=False, r=0.42)
    dot = Dot(perch(ring, 0), radius=0.13, color=INK).set_z_index(5)
    with self.say('s01_machine') as d:
      self.play(LaggedStart(*[GrowFromCenter(nd) for nd in ring.nodes], lag_ratio=0.2), run_time=0.2 * d)
      self.play(LaggedStart(*[GrowArrow(a) for a in ring.arc_group], lag_ratio=0.1), FadeIn(dot), run_time=0.2 * d)
      spent = 0.4 * d
      for s, hold, nxt in NUM['sim_hops']:
        w, m = min(0.5, 0.2 * hold + 0.05), 0.35
        if spent + w + m > 0.95 * d:
          break
        self.wait(w)
        arc = -0.6 if nxt == (s + 1) % 3 else 0.6
        self.play(dot.animate(path_arc=arc).move_to(perch(ring, nxt)), run_time=m)
        spent += w + m
    knob_arrow = ring.arcs[(0, 1)]
    dial_c = ring.pos[0] + RIGHT * 2.7 + DOWN * 0.2
    dial = VGroup(Circle(0.42, color=KNOBC, stroke_width=4),
                  Line(dial_c, dial_c + UP * 0.36, color=KNOBC, stroke_width=5).shift(-dial_c))
    dial.move_to(dial_c)
    pointer = dial[1]
    q = T('How does the time spent in each state shift?', 0.8, INK).to_edge(DOWN, buff=0.5)
    with self.say('s01_knob') as d:
      self.play(FadeIn(dial), run_time=0.12 * d)
      self.play(Rotate(pointer, -PI / 2, about_point=dial_c), knob_arrow.animate.set_color(KNOBC).set_stroke(width=8),
                run_time=0.25 * d)
      self.play(Write(q), run_time=0.25 * d)
    who = T('Fancher and Horowitz, 2026: a guess', 0.75, MUTED)
    here = T('proved here for a whole family of networks', 0.75, ACCENT)
    VGroup(who, here).arrange(DOWN, buff=0.3).to_edge(DOWN, buff=0.4)
    with self.say('s01_why') as d:
      self.play(FadeOut(q), run_time=0.1 * d)
      self.play(FadeIn(who), run_time=0.2 * d)
      self.wait(0.25 * d)
      self.play(FadeIn(here), run_time=0.2 * d)
    self.play(FadeOut(Group(*self.mobjects)), run_time=0.6)


class Hopping(NarratedScene):
  def construct(self):
    ring = Ring(R=1.9, center=LEFT * 3.4 + DOWN * 0.1, r=0.42, rates=False, rate_scale=0.85)
    self.add(ring.arc_group, ring.nodes)
    with self.say('s02_rates') as d:
      self.play(LaggedStart(*[FadeIn(ring.rates[(v, (v + 1) % 3)]) for v in range(3)], lag_ratio=0.3),
                *[Indicate(ring.arcs[(v, (v + 1) % 3)], color=SECONDARY, scale_factor=1.0) for v in range(3)],
                run_time=0.35 * d)
      self.play(LaggedStart(*[FadeIn(ring.rates[(v, (v - 1) % 3)]) for v in range(3)], lag_ratio=0.3),
                *[Indicate(ring.arcs[(v, (v - 1) % 3)], color=SECONDARY, scale_factor=1.0) for v in range(3)],
                run_time=0.35 * d)
    dot = Dot(perch(ring, 0), radius=0.13, color=INK).set_z_index(5)
    with self.say('s02_sim') as d:
      self.play(FadeIn(dot, scale=2), run_time=0.1 * d)
      spent, idx = 0.1 * d, 0
      for s, hold, nxt in NUM['sim_hops']:
        w, m = min(0.4, 0.2 * hold + 0.05), 0.3
        if spent + w + m > 0.98 * d:
          break
        self.wait(w)
        self.play(dot.animate(path_arc=-0.6 if nxt == (s + 1) % 3 else 0.6).move_to(perch(ring, nxt)), run_time=m)
        spent += w + m
        idx += 1

    # Time-fraction bars on the right.
    base = DOWN * 2.2 + RIGHT * 1.3
    H = 6.0
    xs = [base + RIGHT * 1.6 * i for i in range(3)]

    def bars(fr):
      return VGroup(*[Rectangle(width=0.95, height=max(0.02, H * f), stroke_width=2, stroke_color=STATE)
                      .set_fill(STATE, 0.45).move_to(x, aligned_edge=DOWN) for f, x in zip(fr, xs)])

    axis = Line(base + LEFT * 0.8, base + RIGHT * 4.0, color=MUTED, stroke_width=2)
    names = VGroup(*[M(rf'\pi_{i}', 0.85).next_to(x, DOWN, buff=0.3) for i, x in enumerate(xs)])
    third = DashedLine(base + LEFT * 0.8 + UP * H / 3, base + RIGHT * 4.0 + UP * H / 3, color=ACCENT, dash_length=0.12)
    third_l = M(r'\tfrac{1}{3}', 0.8, ACCENT).next_to(third, RIGHT, buff=0.15)
    cps = NUM['sim_checkpoints']
    b = bars(cps[0][1])
    clock = T(f'time: {cps[0][0]:g} s', 0.7, MUTED).move_to(base + UP * 4.8 + RIGHT * 1.6)
    with self.say('s02_fractions') as d:
      self.play(Create(axis), FadeIn(names), FadeIn(b), FadeIn(clock), run_time=0.12 * d)
      step = 0.55 * d / (len(cps) - 1)
      for tt, fr in cps[1:]:
        nb = bars(fr)
        nc = T(f'time: {tt:,} s', 0.7, MUTED).move_to(clock)
        self.play(Transform(b, nb), Transform(clock, nc), run_time=step)
      self.play(Create(third), FadeIn(third_l), run_time=0.12 * d)
      lab = T('steady state', 0.75, ACCENT).next_to(VGroup(*b), UP, buff=0.35).shift(RIGHT * 0.0)
      self.play(FadeIn(lab), run_time=0.1 * d)
    circ = Arc(radius=0.62, start_angle=PI * 0.75, angle=-1.5 * PI, color=ACCENT, stroke_width=6).move_to(
      sum(ring.pos) / 3)
    circ.add_tip(tip_length=0.22)
    cap = T('steady, but not still', 0.75, ACCENT).next_to(ring, DOWN, buff=0.4)
    with self.say('s02_current') as d:
      self.play(ring.label_group.animate.set_opacity(0.2), run_time=0.1 * d)
      self.play(Create(circ), run_time=0.25 * d)
      self.play(FadeIn(cap), run_time=0.2 * d)
      for s, hold, nxt in NUM['sim_hops'][idx:idx + 6]:
        self.play(dot.animate(path_arc=-0.6 if nxt == (s + 1) % 3 else 0.6).move_to(perch(ring, nxt)), run_time=0.07 * d)
    self.play(FadeOut(Group(*self.mobjects)), run_time=0.6)


class Trees(NarratedScene):
  def construct(self):
    ring = Ring(R=2.0, center=UP * 0.2, r=0.42, rates=True)
    root_ring = Circle(0.52, color=ROOT, stroke_width=6).move_to(ring.pos[0])
    tree = [(1, 2), (2, 0)]
    with self.say('s03_def') as d:
      self.play(FadeIn(ring), run_time=0.12 * d)
      self.play(Create(root_ring), run_time=0.12 * d)
      root_lab = T('root', 0.7, ROOT).next_to(root_ring, LEFT, buff=0.25)
      self.play(FadeIn(root_lab), run_time=0.06 * d)
      others = [ring.arcs[k] for k in ring.arcs if k not in tree]
      self.play(*[a.animate.set_opacity(0.15) for a in others],
                *[ring.rates[k].animate.set_opacity(0.15) for k in ring.arcs if k not in tree], run_time=0.15 * d)
      self.play(*[ring.arcs[k].animate.set_stroke(width=7) for k in tree], run_time=0.1 * d)
      walker = Dot(ring.pos[1], radius=0.12, color=SECONDARY).set_z_index(5)
      self.play(FadeIn(walker), run_time=0.05 * d)
      self.play(walker.animate.move_to(ring.pos[2]), run_time=0.12 * d)
      self.play(walker.animate.move_to(ring.pos[0]), run_time=0.12 * d)
      self.play(FadeOut(walker), run_time=0.05 * d)
    pics = VGroup(*[TreePic(0, e, R=1.3, r=0.36, rates=True) for e in range(3)])
    for i, p in enumerate(pics):
      p.move_to(RIGHT * (i - 1) * 4.5 + UP * 0.8)
    with self.say('s03_ring') as d:
      sc = cross((ring.pos[0] + ring.pos[1]) / 2, 0.22, SECONDARY, 6)
      self.play(Create(sc), run_time=0.15 * d)
      self.play(FadeOut(VGroup(ring, root_ring, root_lab, sc)), run_time=0.15 * d)
      self.play(LaggedStart(*[FadeIn(p, shift=UP * 0.2) for p in pics], lag_ratio=0.3), run_time=0.45 * d)
    ws = [M(r'2 \times 2 = 4', 0.85), M(r'1 \times 2 = 2', 0.85), M(r'1 \times 1 = 1', 0.85)]
    for w, p in zip(ws, pics):
      w.next_to(p, DOWN, buff=0.5)
    lab = T('weight = product of the rates', 0.75, MUTED).to_edge(DOWN, buff=0.7)
    with self.say('s03_weights') as d:
      self.play(FadeIn(lab), run_time=0.12 * d)
      for w in ws:
        self.play(Write(w), run_time=0.22 * d)
    self.play(FadeOut(Group(*self.mobjects)), run_time=0.6)


class TreeTheorem(NarratedScene):
  def construct(self):
    f = M(r'\pi_j = \frac{\text{total tree weight at } j}{\text{sum of all the totals}}', 0.85).to_edge(UP, buff=0.6)
    cols = VGroup()
    for j in range(3):
      mini = VGroup(*[TreePic(j, (j + i) % 3, R=0.6, r=0.24) for i in range(3)]).arrange(DOWN, buff=0.22)
      cols.add(mini)
    cols.arrange(RIGHT, buff=2.4).move_to(DOWN * 0.55)
    wl = VGroup()
    for col in cols:
      for p, w in zip(col, [4, 2, 1]):
        wl.add(M(str(w), 0.8).next_to(p, RIGHT, buff=0.3))
    with self.say('s04_theorem') as d:
      self.play(Write(f), run_time=0.45 * d)
      self.play(FadeIn(cols), FadeIn(wl), run_time=0.3 * d)
    tots = VGroup(*[M(r'4+2+1=7', 0.8, ACCENT).next_to(col, DOWN, buff=0.3) for col in cols])
    res = M(r'\pi_0 = \pi_1 = \pi_2 = \tfrac{7}{21} = \tfrac{1}{3}', 0.85, ACCENT).to_edge(DOWN, buff=0.35)
    with self.say('s04_check') as d:
      self.play(LaggedStart(*[Write(t) for t in tots], lag_ratio=0.3), run_time=0.4 * d)
      self.play(FadeOut(cols), FadeOut(wl), run_time=0.1 * d)
      self.play(*[t.animate.move_to([t.get_center()[0], 0.6, 0]).scale(1.2) for t in tots], run_time=0.15 * d)
      self.play(Write(res), run_time=0.3 * d)
    pics = VGroup(*[TreePic(0, e, R=1.0, r=0.3) for e in range(3)]).arrange(RIGHT, buff=2.2).move_to(UP * 1.2)
    probs = VGroup(*[M(s, 1.0, INK).next_to(p, DOWN, buff=0.35) for s, p in
                     zip([r'\tfrac{4}{7}', r'\tfrac{2}{7}', r'\tfrac{1}{7}'], pics)])
    widths = [4, 2, 1]
    seg = VGroup(*[Rectangle(width=1.3 * w, height=0.5, stroke_color=INK, stroke_width=2).set_fill(STATE, 0.25 + 0.2 * i)
                   for i, w in enumerate(widths)]).arrange(RIGHT, buff=0).move_to(DOWN * 2.6)
    seg_l = VGroup(*[M(s, 0.7).move_to(r) for s, r in zip(['4', '2', '1'], seg)])
    lot = T("root 0's lottery", 0.7, MUTED).next_to(seg, UP, buff=0.2)
    with self.say('s04_lottery') as d:
      self.play(FadeOut(VGroup(f, tots, res)), run_time=0.1 * d)
      self.play(FadeIn(pics), run_time=0.15 * d)
      self.play(FadeIn(seg), FadeIn(seg_l), FadeIn(lot), run_time=0.2 * d)
      self.play(LaggedStart(*[Write(p) for p in probs], lag_ratio=0.35), run_time=0.35 * d)
    self.play(FadeOut(Group(*self.mobjects)), run_time=0.6)


class Knob(NarratedScene):
  def construct(self):
    rows = VGroup()
    wts = []
    ys = [2.3, 0.05, -2.2]
    xs = [-3.9, -0.9, 2.1]
    grid = {}
    for j in range(3):
      lab = T(f'root {j}', 0.65, ROOT).move_to([-6.2, ys[j], 0])
      rows.add(lab)
      for i in range(3):
        e = (j + i) % 3
        p = TreePic(j, e, R=0.72, r=0.25).move_to([xs[i], ys[j], 0])
        w = M(str(p.weight), 0.8).next_to(p, RIGHT, buff=0.3)
        grid[(j, i)] = (p, w)
        rows.add(p, w)
    with self.say('s05_nudge') as d:
      self.play(FadeIn(rows), run_time=0.2 * d)
      ups = []
      for (j, i), (p, w) in grid.items():
        if (0, 1) in p.arcs:
          ups.append((p, w))
      self.play(*[p.arcs[(0, 1)].animate.set_color(KNOBC).set_stroke(width=7) for p, _ in ups], run_time=0.2 * d)
      new = []
      for p, w in ups:
        nw = M(f'{p.weight * 1.01:.2f}', 0.8, KNOBC).move_to(w, aligned_edge=LEFT)
        new.append(Transform(w, nw))
      self.play(*new, run_time=0.25 * d)
    tot_vals = NUM['nudge']['totals']
    tots = VGroup(*[M(rf'\text{{total }} {float(v):g}', 0.75, ACCENT).move_to([4.9, ys[j], 0]) for j, v in enumerate(tot_vals)])
    pct = NUM['nudge']['rel_pct']
    pct_s = [f'{pct[0]:.2f}', f'+{pct[1]:.2f}', f'+{pct[2]:.1f}']
    pcts = VGroup(*[M(rf'\pi_{j}:\ {s}\%', 0.75, KNOBC) for j, s in enumerate(pct_s)])
    for j, p in enumerate(pcts):
      p.move_to([4.9, ys[j] - 0.55, 0])
    with self.say('s05_totals') as d:
      self.play(LaggedStart(*[FadeIn(t) for t in tots], lag_ratio=0.3), run_time=0.35 * d)
      self.play(LaggedStart(*[FadeIn(p) for p in pcts], lag_ratio=0.4), run_time=0.45 * d)
    shares = VGroup(*[M(s, 0.85, KNOBC).move_to(t) for s, t in zip(['0', r'\tfrac{6}{7}', r'\tfrac{4}{7}'], tots)])
    eq1 = MathTex(r'\big(\,', r'0', r',\ ', r'\tfrac{6}{7}', r',\ ', r'\tfrac{4}{7}', r'\,\big)', r'-', r'\tfrac{10}{21}').scale(1.0)
    eq2 = MathTex(r'\big(\,', r'\tfrac{0}{21}', r',\ ', r'\tfrac{18}{21}', r',\ ', r'\tfrac{12}{21}', r'\,\big)', r'-',
                  r'\tfrac{10}{21}').scale(1.0)
    eq3 = MathTex(r'\big(\,', r'-\tfrac{10}{21}', r',\ ', r'\tfrac{8}{21}', r',\ ', r'\tfrac{2}{21}', r'\,\big)').scale(1.0)
    for e in (eq1, eq2, eq3):
      e.move_to(UP * 0.4)
    l1 = T('share of tree weight using the arrow, minus the average', 0.7, MUTED).next_to(eq1, UP, buff=0.7)
    l3 = T(r'relative percent change per percent nudge, as the nudge tends to zero', 0.65, ACCENT).next_to(eq1, DOWN, buff=0.8)
    with self.say('s05_rule') as d:
      self.play(FadeOut(pcts), ReplacementTransform(tots, shares), run_time=0.15 * d)
      self.play(FadeOut(rows), run_time=0.1 * d)
      self.play(FadeIn(l1), *[ReplacementTransform(shares[i], eq1[2 * i + 1]) for i in range(3)],
                FadeIn(VGroup(eq1[0], eq1[2], eq1[4], eq1[6])), run_time=0.15 * d)
      self.play(Write(VGroup(eq1[7], eq1[8])), run_time=0.1 * d)
      for m in list(self.mobjects):
        if m is not l1:
          self.remove(m)
      self.add(eq1)
      self.play(Indicate(eq1[8], color=KNOBC), run_time=0.05 * d)
      self.play(TransformMatchingTex(eq1, eq2), run_time=0.15 * d)
      self.play(TransformMatchingTex(eq2, eq3), run_time=0.15 * d)
      eq3.set_color(ACCENT)
      self.play(FadeIn(l3), run_time=0.1 * d)
    self.play(FadeOut(Group(*self.mobjects)), run_time=0.6)


def family_row(fam, R=0.62, r=0.23, gap=1.0, knob=True):
  return VGroup(*[TreePic(j, e, R=R, r=r, knob=knob) for j, e in enumerate(fam)]).arrange(RIGHT, buff=gap)


class Families(NarratedScene):
  def construct(self):
    fam = family_row((0, 1, 2), R=0.85, r=0.28, gap=1.6).move_to(UP * 1.4)
    br = Brace(fam, UP, color=MUTED)
    bl = T('a tree family: one tree for every root', 0.75, MUTED).next_to(br, UP, buff=0.15)
    cnt = M(r'3 \times 3 \times 3 = 27 \text{ families}', 0.9).move_to(DOWN * 2.3)
    with self.say('s06_family') as d:
      self.play(LaggedStart(*[FadeIn(p, shift=UP * 0.2) for p in fam], lag_ratio=0.3), run_time=0.4 * d)
      self.play(GrowFromCenter(br), FadeIn(bl), run_time=0.2 * d)
      self.play(Write(cnt), run_time=0.25 * d)
    marks = VGroup(*[M(str(int((0, 1) in p.arcs)), 1.0, KNOBC).next_to(p, DOWN, buff=0.45) for p in fam])
    avg = M(r'\text{average } \tfrac{2}{3}', 0.8, MUTED).next_to(marks, RIGHT, buff=0.9)
    block = M(r'\text{block: } \big(-\tfrac{2}{3},\ \tfrac{1}{3},\ \tfrac{1}{3}\big)', 0.95, ACCENT).move_to(DOWN * 2.6)
    with self.say('s06_score') as d:
      self.play(FadeOut(cnt), run_time=0.08 * d)
      self.play(*[Indicate(p.arcs[(0, 1)], color=KNOBC) for p in fam if (0, 1) in p.arcs], run_time=0.15 * d)
      self.play(LaggedStart(*[FadeIn(m, shift=DOWN * 0.2) for m in marks], lag_ratio=0.3), run_time=0.25 * d)
      self.play(FadeIn(avg), run_time=0.15 * d)
      self.play(Write(block), run_time=0.25 * d)
    chance = M(r'\text{chance: } \tfrac{4}{7} \times \tfrac{4}{7} \times \tfrac{4}{7}', 0.8, MUTED).move_to(DOWN * 1.1)
    form = M(r'\text{response} = \text{average over families of their blocks}', 0.85).move_to(DOWN * 3.3)
    with self.say('s06_average') as d:
      self.play(FadeOut(avg), marks.animate.set_opacity(0.4), FadeIn(chance), run_time=0.3 * d)
      self.play(block.animate.shift(UP * 0.3), Write(form), run_time=0.4 * d)
    self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)

    ax, axg = resp_axes()
    axg.move_to(RIGHT * 0.5)
    axg[1].to_edge(DOWN, buff=0.2)
    dots = {k: Dot(ax.c2p(*v), radius=0.11, color=INK if k != 'x' else INK) for k, v in PTS.items()}
    hull = Polygon(*[ax.c2p(*PTS[k]) for k in ['o', 'a', 'b', 'x']], color=MUTED, stroke_width=3).set_fill(MUTED, 0.12)
    resp = Star(5, outer_radius=0.17, color=KNOBC).set_fill(KNOBC, 1).move_to(ax.c2p(*RESP)).set_z_index(5)
    resp_l = T('response', 0.65, KNOBC).next_to(resp, DOWN, buff=0.2)
    note = T('27 families, 4 points', 0.7, MUTED).to_corner(UR, buff=0.6)
    with self.say('s06_hull') as d:
      self.play(FadeIn(axg), run_time=0.15 * d)
      self.play(LaggedStart(*[GrowFromCenter(v) for v in dots.values()], lag_ratio=0.2), FadeIn(note), run_time=0.25 * d)
      self.play(DrawBorderThenFill(hull), run_time=0.25 * d)
      self.play(GrowFromCenter(resp), FadeIn(resp_l), run_time=0.15 * d)


BAG_FAMS = [(0, 1, 1), (1, 1, 0)]


def arc_tex(a):
  return rf'{a[0]}\!\to\!{a[1]}'


class Conjecture(NarratedScene):
  def construct(self):
    rows = VGroup(*[family_row(f, R=0.66, r=0.24, gap=0.45, knob=False) for f in BAG_FAMS]).arrange(DOWN, buff=1.4)
    rows.move_to(LEFT * 3.85)
    bags = VGroup()
    moves = []
    for row, fam in zip(rows, BAG_FAMS):
      arcs = sorted(a for p in row for a in p.tree)
      chips_ = VGroup(*[M(arc_tex(a), 0.72) for a in arcs]).arrange(RIGHT, buff=0.24)
      box = SurroundingRectangle(chips_, color=MUTED, buff=0.2, corner_radius=0.15)
      bag = VGroup(box, chips_).move_to([3.5, row.get_center()[1], 0])
      bags.add(bag)
      srcs = []
      for a in arcs:
        p = next(p for p in row if a in p.tree and all(id(s) != id(p.arcs[a]) for s in srcs))
        srcs.append(p.arcs[a])
      moves.append((srcs, chips_))
    eq = M('=', 1.2, WARN).move_to((bags[0].get_center() + bags[1].get_center()) / 2)
    look = T('look-alikes', 0.75, WARN).next_to(eq, RIGHT, buff=0.3)
    with self.say('s07_bags') as d:
      self.play(FadeIn(rows), run_time=0.15 * d)
      for srcs, chips_ in moves:
        self.play(*[TransformFromCopy(s, c) for s, c in zip(srcs, chips_)], run_time=0.2 * d)
      self.play(*[Create(b[0]) for b in bags], run_time=0.1 * d)
      self.play(FadeIn(eq), FadeIn(look), *[b[0].animate.set_color(WARN) for b in bags], run_time=0.15 * d)
    nums = VGroup(VGroup(M('27', 1.4), T('families', 0.7, MUTED)).arrange(DOWN, buff=0.2),
                  VGroup(M('18', 1.4), T('different bags', 0.7, MUTED)).arrange(DOWN, buff=0.2),
                  VGroup(M('11', 1.4, ACCENT), T('uniquely constructable', 0.7, ACCENT)).arrange(DOWN, buff=0.2))
    nums.arrange(RIGHT, buff=1.5).move_to(DOWN * 0.1)
    with self.say('s07_uc') as d:
      self.play(FadeOut(VGroup(rows, bags, eq, look)), run_time=0.12 * d)
      self.play(FadeIn(nums[0]), run_time=0.15 * d)
      self.play(FadeIn(nums[1]), run_time=0.2 * d)
      self.play(FadeIn(nums[2]), run_time=0.25 * d)
    st = statement('The guess (Fancher and Horowitz, 2026)',
                   r'For every network, all rates and every knob: the response is a weighted average of the building '
                   r'blocks of \emph{uniquely constructable} families only.', width=10.5, color=ACCENT)
    st.move_to(ORIGIN)
    with self.say('s07_guess') as d:
      self.play(FadeOut(nums), run_time=0.12 * d)
      self.play(FadeIn(st), run_time=0.3 * d)
    ax, axg = resp_axes()
    axg.move_to(RIGHT * 0.5)
    dots = {k: Dot(ax.c2p(*v), radius=0.11, color=INK) for k, v in PTS.items()}
    hull4 = Polygon(*[ax.c2p(*PTS[k]) for k in ['o', 'a', 'b', 'x']], color=MUTED, stroke_width=3).set_fill(MUTED, 0.12)
    hull3 = Polygon(*[ax.c2p(*PTS[k]) for k in ['o', 'a', 'b']], color=ACCENT, stroke_width=4).set_fill(ACCENT, 0.18)
    resp = Star(5, outer_radius=0.17, color=KNOBC).set_fill(KNOBC, 1).move_to(ax.c2p(*RESP)).set_z_index(5)
    cap = T('proved for 3 states; asked for every network', 0.7, MUTED).to_edge(DOWN, buff=0.35)
    with self.say('s07_tighter') as d:
      self.play(FadeOut(st), FadeIn(axg), FadeIn(hull4), *[FadeIn(v) for v in dots.values()], FadeIn(resp),
                run_time=0.15 * d)
      self.play(dots['x'].animate.set_color(WARN).scale(1.5), run_time=0.15 * d)
      xl = T('only look-alikes', 0.65, WARN).next_to(dots['x'], LEFT, buff=0.2)
      self.play(FadeIn(xl), run_time=0.1 * d)
      self.play(ReplacementTransform(hull4, hull3), dots['x'].animate.set_opacity(0.6), xl.animate.set_opacity(0.6),
                run_time=0.25 * d)
      self.play(FadeIn(cap), run_time=0.12 * d)
    self.play(FadeOut(Group(*self.mobjects)), run_time=0.6)


class Reframe(NarratedScene):
  def construct(self):
    p = 152 / 343
    W = 10.0
    good = Rectangle(width=W * (1 - p), height=0.8, stroke_width=0).set_fill(ACCENT, 0.7)
    bad = Rectangle(width=W * p, height=0.8, stroke_width=0).set_fill(WARN, 0.75)
    barr = VGroup(good, bad).arrange(RIGHT, buff=0).move_to(UP * 0.3)
    gl = T('uniquely constructable', 0.7, ACCENT).next_to(good, DOWN, buff=0.3)
    bl = T(r'look-alike: $\tfrac{152}{343} \approx 44\%$', 0.75, WARN).next_to(bad, DOWN, buff=0.3)
    head = T('independent lotteries', 0.8, MUTED).next_to(barr, UP, buff=0.6)
    with self.say('s08_naive') as d:
      self.play(FadeIn(head), run_time=0.15 * d)
      self.play(GrowFromEdge(good, LEFT), FadeIn(gl), run_time=0.3 * d)
      self.play(GrowFromEdge(bad, LEFT), FadeIn(bl), run_time=0.3 * d)
    fam = family_row((0, 1, 2), R=1.0, r=0.32, gap=1.6).move_to(UP * 1.0)
    parts = VGroup(*[M(str(int((0, 1) in t.arcs)), 1.0, KNOBC).next_to(t, DOWN, buff=0.5) for t in fam])
    with self.say('s08_insight') as d:
      self.play(FadeOut(VGroup(head, barr, gl, bl)), run_time=0.1 * d)
      self.play(FadeIn(fam), FadeIn(parts), run_time=0.2 * d)
      box = SurroundingRectangle(VGroup(fam[1], parts[1]), color=KNOBC, buff=0.2, corner_radius=0.12)
      self.play(Create(box), Transform(fam[0], dimmed(fam[0], 0.3)), Transform(fam[2], dimmed(fam[2], 0.3)),
                parts[0].animate.set_opacity(0.25), parts[2].animate.set_opacity(0.25), run_time=0.25 * d)
      cap = T("each part sees only its own root's tree", 0.75, INK).to_edge(DOWN, buff=0.8)
      self.play(FadeIn(cap), run_time=0.15 * d)
    g1 = T('Goal: one shared lottery for the whole family', 0.85, INK)
    g2 = T('right odds at every root, never a look-alike', 0.85, ACCENT)
    goal = VGroup(g1, g2).arrange(DOWN, buff=0.45).move_to(UP * 0.4)
    q = T('Pause and think.', 0.75, MUTED).next_to(goal, DOWN, buff=0.9)
    with self.say('s08_goal') as d:
      self.play(FadeOut(VGroup(fam, parts, box, cap)), run_time=0.1 * d)
      self.play(FadeIn(g1), run_time=0.2 * d)
      self.play(FadeIn(g2), run_time=0.25 * d)
      self.play(FadeIn(q), run_time=0.15 * d)
    self.wait(1.2)
    self.play(FadeOut(Group(*self.mobjects)), run_time=0.6)


UNIT = 0.5
BASE_Y = -2.6


def stair_bars(n_bars=5, x0=-1.6, width=1.0, gap=0.4, top=5):
  bars = VGroup()
  for k in range(n_bars):
    h = (top - k) * UNIT
    b = Rectangle(width=width, height=h, stroke_color=E_COL[k % 3], stroke_width=3).set_fill(E_COL[k % 3], 0.35)
    b.move_to([x0 + k * (width + gap), BASE_Y, 0], aligned_edge=DOWN)
    bars.add(b)
  return bars


def edge_lines(pos, width=10, opacity=0.85):
  return VGroup(*[Line(pos[e], pos[(e + 1) % 3], stroke_width=width, color=E_COL[e]).set_opacity(opacity)
                  for e in range(3)])


class Staircase(NarratedScene):
  def construct(self):
    c = LEFT * 4.7 + UP * 0.5
    pos = [ring_pos(i, 1.6, 3, c) for i in range(3)]
    el = edge_lines(pos, 7, 0.85)
    pics = [TreePic(0, e, R=1.6, r=0.36, center=c, cut_line=False, width=5) for e in range(3)]
    for p in pics:
      for a in p.arcs.values():
        a.set_z_index(2)
    mids = [(pos[e] + pos[(e + 1) % 3]) / 2 for e in range(3)]
    cutmark = cross(mids[0], 0.17, INK, 5).set_z_index(3)
    cur = pics[0].copy()
    wl = M('4', 1.0).next_to(VGroup(*pics[0]), DOWN, buff=0.5)
    edge_key = T('root 0; cross = the cut edge', 0.62, MUTED).next_to(VGroup(*pics[0]), UP, buff=0.35)
    with self.say('s09_cut') as d:
      self.play(FadeIn(el), FadeIn(cur), FadeIn(wl), FadeIn(edge_key), FadeIn(cutmark), run_time=0.15 * d)
      for e in (1, 2):
        nxt = pics[e]
        flip_v = e  # the state whose arrow flips
        self.play(FadeTransform(cur, nxt), Transform(wl, M(str(nxt.weight), 1.0).move_to(wl)),
                  cutmark.animate.move_to(mids[e]), run_time=0.22 * d)
        cur = nxt
        half = M(r'\times \tfrac{1}{2}', 0.8, KNOBC).next_to(wl, RIGHT, buff=0.3)
        self.play(Indicate(cur.arcs[next(a for a in nxt.tree if a[0] == flip_v)], color=KNOBC), FadeIn(half),
                  run_time=0.15 * d)
        self.play(FadeOut(half), run_time=0.05 * d)
    bars = stair_bars()
    labs = VGroup(*[M(s, 0.75).next_to(b, DOWN, buff=0.2) for s, b in
                    zip(['1', r'\tfrac12', r'\tfrac14', r'\tfrac18', r'\tfrac1{16}'], bars)])
    scale_note = T('height counts doublings', 0.65, MUTED).next_to(bars, UP, buff=0.5)

    def window(r):
      grp = VGroup(*bars[r:r + 3])
      box = SurroundingRectangle(grp, color=ROOT, buff=0.12, corner_radius=0.1, stroke_width=4)
      box.stretch_to_fit_height(5 * UNIT + 0.3).move_to(box.get_center()[0] * RIGHT + (BASE_Y + 5 * UNIT / 2) * UP)
      lab = T(f'root {r}', 0.7, ROOT).next_to(box, UP, buff=0.15)
      return VGroup(box, lab)

    with self.say('s09_stair') as d:
      self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.15), FadeIn(labs), run_time=0.35 * d)
      self.play(FadeIn(scale_note), run_time=0.1 * d)
      w = window(0)
      self.play(FadeOut(scale_note), Create(w), run_time=0.15 * d)
      for r in (1, 2):
        self.play(Transform(w, window(r)), run_time=0.15 * d)
    brk = ArcBetweenPoints(bars[0].get_top() + UP * 0.15, bars[3].get_top() + UP * 0.15, angle=-PI / 3,
                           color=KNOBC, stroke_width=4)
    brk.add_tip(tip_length=0.18)
    div = M(r'\div 8', 0.9, KNOBC).next_to(brk, UP, buff=0.1)
    with self.say('s09_turn') as d:
      self.play(Transform(w, window(0)), run_time=0.15 * d)
      self.play(LaggedStart(*[Indicate(bars[k], color=INK, scale_factor=1.05) for k in range(3)], lag_ratio=0.3),
                run_time=0.3 * d)
      self.play(FadeOut(w), run_time=0.08 * d)
      self.play(Create(brk), FadeIn(div), run_time=0.25 * d)
    self.play(FadeOut(Group(*self.mobjects)), run_time=0.6)


def bonus_units(g, c=1.4):
  return g / LN2 + c


class Tokens(NarratedScene):
  def construct(self):
    # Gumbel-max on root 0 alone.
    g0 = NUM['demo_draws'][0][0]
    bars = stair_bars(3, x0=-4.2, width=1.0, gap=0.5)
    labs = VGroup(*[M(s, 0.8).next_to(b, DOWN, buff=0.2) for s, b in zip(['4', '2', '1'], bars)])
    curve_ax = Axes(x_range=[-2, 5, 1], y_range=[0, 0.4, 0.2], x_length=3.6, y_length=1.6, tips=False,
                    axis_config={'color': MUTED, 'stroke_width': 2, 'include_ticks': False})
    curve = curve_ax.plot(lambda x: np.exp(-(x + np.exp(-x))), x_range=[-2, 5], color=KNOBC, stroke_width=4)
    cg = VGroup(curve_ax, curve, T('Gumbel', 0.65, KNOBC).next_to(curve_ax, UP, buff=0.1)).move_to(RIGHT * 4.3 + UP * 1.8)
    bon = VGroup()
    for k, b in enumerate(bars):
      hb = bonus_units(g0[k]) * UNIT
      r = Rectangle(width=b.width, height=hb, stroke_width=2, stroke_color=E_COL[k]).set_fill(E_COL[k], 0.9)
      r.next_to(b, UP, buff=0)
      bon.add(r)
    tops = [b.get_top()[1] + r.height for b, r in zip(bars, bon)]
    win = int(np.argmax(tops))
    crown = tick(1.1, OK).next_to(bon[win], UP, buff=0.2)
    with self.say('s10_trick') as d:
      self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.2), FadeIn(labs), run_time=0.25 * d)
      self.play(FadeIn(cg), run_time=0.2 * d)
      self.play(LaggedStart(*[GrowFromEdge(r, DOWN) for r in bon], lag_ratio=0.25), run_time=0.25 * d)
      self.play(FadeIn(crown, scale=1.5), run_time=0.1 * d)
    # Tally for root 0.
    tally = NUM['tally']
    HB = 4.5
    tx = [1.6 + 1.3 * k for k in range(3)]
    ty = -2.6

    def tbars(c, n):
      return VGroup(*[Rectangle(width=0.9, height=max(0.02, HB * c[k] / n), stroke_color=E_COL[k], stroke_width=2)
                      .set_fill(E_COL[k], 0.6).move_to([tx[k], ty, 0], aligned_edge=DOWN) for k in range(3)])

    refs = VGroup(*[DashedLine([tx[k] - 0.55, ty + HB * f, 0], [tx[k] + 0.55, ty + HB * f, 0], color=INK,
                               dash_length=0.08) for k, f in enumerate([4 / 7, 2 / 7, 1 / 7])])
    reflab = VGroup(*[M(s, 0.7).next_to(refs[k], UP, buff=0.12) for k, s in
                      enumerate([r'\tfrac47', r'\tfrac27', r'\tfrac17'])])
    tb = tbars(tally[0][2], tally[0][0])
    cnt = T(f'{tally[0][0]:,} draws', 0.65, MUTED).move_to([tx[1], ty - 0.5, 0])
    with self.say('s10_hist') as d:
      self.play(FadeOut(cg), VGroup(bars, labs, bon, crown).animate.shift(LEFT * 0.4), run_time=0.1 * d)
      self.play(FadeIn(tb), FadeIn(cnt), run_time=0.1 * d)
      for n, _, r0 in tally[1:]:
        self.play(Transform(tb, tbars(r0, n)), Transform(cnt, T(f'{n:,} draws', 0.65, MUTED).move_to(cnt)),
                  run_time=0.5 * d / (len(tally) - 1))
      self.play(Create(refs), FadeIn(reflab), run_time=0.15 * d)
    self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)

    # Shared tokens on the staircase.
    bars = stair_bars(5, x0=-4.0, width=0.85, gap=0.35, top=5)
    cuts = VGroup(*[RoundedRectangle(width=0.3, height=0.3, corner_radius=0.05, stroke_width=0)
                    .set_fill(E_COL[k % 3], 1).next_to(b, DOWN, buff=0.2) for k, b in enumerate(bars)])
    tok_pos = [RIGHT * (3.6 + 1.1 * e) + UP * 1.6 for e in range(3)]

    def token_rects(g):
      out = VGroup()
      for k, b in enumerate(bars):
        hb = bonus_units(g[k % 3]) * UNIT
        out.add(Rectangle(width=b.width, height=hb, stroke_width=2, stroke_color=E_COL[k % 3])
                .set_fill(E_COL[k % 3], 0.9).next_to(b, UP, buff=0))
      return out

    def free_tokens(g):
      return VGroup(*[Rectangle(width=0.7, height=bonus_units(g[e]) * UNIT, stroke_width=2, stroke_color=E_COL[e])
                      .set_fill(E_COL[e], 0.9).move_to(tok_pos[e], aligned_edge=DOWN) for e in range(3)])


    toklab = T('one token per edge', 0.7, MUTED).next_to(VGroup(*[Dot(p) for p in tok_pos]), DOWN, buff=0.45)
    toklab.shift(DOWN * 0.0)
    draws = NUM['demo_draws']
    g = draws[0][0]
    free = free_tokens(g)
    toks = token_rects(g)
    with self.say('s10_share') as d:
      self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.1), FadeIn(cuts), run_time=0.2 * d)
      self.play(LaggedStart(*[FadeIn(t, shift=DOWN * 0.2) for t in free], lag_ratio=0.2), FadeIn(toklab),
                run_time=0.2 * d)
      self.play(*[TransformFromCopy(free[k % 3], toks[k]) for k in range(5)], run_time=0.4 * d)
    fam_slot = RIGHT * 4.7 + DOWN * 0.6
    fam_head = T('family', 0.65, MUTED).move_to(fam_slot + UP * 0.6)
    def markers(tk):
      out, ks = VGroup(), []
      for r in range(3):
        tops = [bars[k].get_top()[1] + tk[k].height for k in range(r, r + 3)]
        k = r + int(np.argmax(tops))
        ks.append(k)
        above = sum(1 for kk in ks[:-1] if kk == k)
        lab = VGroup(Circle(0.2, color=ROOT, stroke_width=3).set_fill(BACKGROUND, 1), M(str(r), 0.55, ROOT))
        lab[1].move_to(lab[0])
        lab.move_to([bars[k].get_center()[0], bars[k].get_top()[1] + tk[k].height + 0.32 + 0.48 * above, 0])
        out.add(lab)
      return out, [k % 3 for k in ks]

    with self.say('s10_draw') as d:
      mk, wins = markers(toks)
      assert wins == draws[0][1]
      for r in range(3):
        grp = VGroup(*bars[r:r + 3], *toks[r:r + 3])
        box = SurroundingRectangle(grp, color=ROOT, buff=0.1, corner_radius=0.1, stroke_width=4)
        self.play(Create(box), run_time=0.07 * d)
        self.play(FadeIn(mk[r], scale=1.4), run_time=0.07 * d)
        self.play(FadeOut(box), run_time=0.04 * d)
      fc = chips(wins, 0.42).move_to(fam_slot)
      self.play(FadeIn(fam_head), FadeIn(fc, shift=UP * 0.2), run_time=0.08 * d)
      hist = VGroup(fc)
      for g2, f2 in draws[1:]:
        nt, nf = token_rects(g2), free_tokens(g2)
        nm, wins2 = markers(nt)
        assert wins2 == f2
        self.play(Transform(toks, nt), Transform(free, nf), FadeOut(mk), run_time=0.08 * d)
        mk = nm
        nc = chips(wins2, 0.42).next_to(hist[-1], DOWN, buff=0.25)
        hist.add(nc)
        self.play(FadeIn(mk), FadeIn(nc, shift=UP * 0.2), run_time=0.08 * d)
    self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)

    # The seven families.
    fams = [tuple(f) for f in NUM['families_sorted']]
    HB = 4.0
    xs = [-4.8 + 1.6 * i for i in range(7)]
    by = -2.4

    def fbars(c, n):
      return VGroup(*[Rectangle(width=1.0, height=max(0.02, HB * c[i] / n * 3), stroke_color=ACCENT, stroke_width=2)
                      .set_fill(ACCENT, 0.5).move_to([xs[i], by, 0], aligned_edge=DOWN) for i in range(7)])

    labs = VGroup(*[chips(f, 0.3, 0.05).move_to([xs[i], by - 0.4, 0]) for i, f in enumerate(fams)])
    ref = DashedLine([xs[0] - 0.7, by + HB * 3 / 7, 0], [xs[-1] + 0.7, by + HB * 3 / 7, 0], color=INK, dash_length=0.12)
    refl = M(r'\tfrac{1}{7}', 0.85).next_to(ref, RIGHT, buff=0.15)
    fb = fbars(tally[0][1], tally[0][0])
    cnt = T(f'{tally[0][0]:,} draws', 0.65, MUTED).move_to([0, by - 1.1, 0])
    uc = T(r'all 7 uniquely constructable', 0.75, ACCENT).to_edge(UP, buff=0.6)
    with self.say('s10_seven') as d:
      self.play(FadeIn(labs), FadeIn(fb), FadeIn(cnt), run_time=0.12 * d)
      for n, c, _ in tally[1:]:
        self.play(Transform(fb, fbars(c, n)), Transform(cnt, T(f'{n:,} draws', 0.65, MUTED).move_to(cnt)),
                  run_time=0.5 * d / (len(tally) - 1))
      self.play(Create(ref), FadeIn(refl), run_time=0.12 * d)
      self.play(FadeIn(uc), run_time=0.12 * d)
    self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)

    # Balance of the seven building blocks.
    ax, axg = resp_axes()
    axg.move_to(LEFT * 1.6)
    hull3 = Polygon(*[ax.c2p(*PTS[k]) for k in ['o', 'a', 'b']], color=ACCENT, stroke_width=4).set_fill(ACCENT, 0.15)
    resp = Star(5, outer_radius=0.17, color=KNOBC).set_fill(KNOBC, 0.3).move_to(ax.c2p(*RESP)).set_z_index(3)
    groups = {'o': [], 'a': [], 'b': []}
    for (x, y), fl in NUM['coupling_groups']:
      pt = (float(Fr(x)), float(Fr(y)))
      key = min(PTS, key=lambda k: abs(PTS[k][0] - pt[0]) + abs(PTS[k][1] - pt[1]))
      groups[key] = [tuple(f) for f in fl]
    coins = VGroup()
    anims = []
    for kname, fl in groups.items():
      base = ax.c2p(*PTS[kname])
      for i, f in enumerate(fl):
        ch = chips(f, 0.22, 0.03)
        ch.move_to(base + RIGHT * 0.75 + UP * (0.3 * i - 0.15 * (len(fl) - 1)))
        if kname == 'b':
          ch.move_to(base + LEFT * 0.75 + UP * (0.3 * i - 0.15 * (len(fl) - 1)))
        coins.add(ch)
      cnt_l = M(str(len(fl)), 0.85, INK).move_to(base + (LEFT if kname == 'b' else RIGHT) * 1.35)
      anims.append((Dot(base, radius=0.11 + 0.035 * len(fl), color=INK), cnt_l))
    eq_text = T('weights $\\tfrac17$ each', 0.8, INK).move_to(RIGHT * 4.4 + UP * 0.9)
    resv = VGroup(T('balance point', 0.7, KNOBC),
                  M(r'\big(-\tfrac{10}{21},\ \tfrac{8}{21}\big)', 0.95, KNOBC)).arrange(DOWN, buff=0.25)
    resv.next_to(eq_text, DOWN, buff=0.7)
    with self.say('s10_balance') as d:
      self.play(FadeIn(axg), FadeIn(hull3), FadeIn(resp), run_time=0.15 * d)
      for dt, cl in anims:
        self.play(GrowFromCenter(dt), FadeIn(cl), run_time=0.1 * d)
      self.play(FadeIn(coins), FadeIn(eq_text), run_time=0.15 * d)
      bal = Dot(ax.c2p(0, 0), radius=0.14, color=KNOBC).set_z_index(6)
      self.play(FadeIn(bal), run_time=0.05 * d)
      self.play(bal.animate.move_to(ax.c2p(*RESP)), run_time=0.2 * d)
      self.play(resp.animate.set_fill(KNOBC, 1).scale(1.3), FadeIn(resv), run_time=0.1 * d)
    self.play(FadeOut(Group(*self.mobjects)), run_time=0.6)


class WhyUC(NarratedScene):
  def construct(self):
    intro = T('one multiplier per edge; both directions share it', 0.75, MUTED).to_edge(UP, buff=0.6)
    ring = Ring(R=1.6, center=LEFT * 3.5, rates=False)
    factors = VGroup()
    for e, name in enumerate(['a', 'b', 'c']):
      pair = VGroup(ring.arcs[(e, (e + 1) % 3)], ring.arcs[((e + 1) % 3, e)])
      pair.set_color(E_COL[e])
      mid = (ring.pos[e] + ring.pos[(e + 1) % 3]) / 2
      outward = mid - LEFT * 3.5
      outward /= np.linalg.norm(outward)
      factors.add(M(r'\div ' + name, 0.85, E_COL[e]).move_to(mid + 0.6 * outward))
    eq = MathTex(r'\frac{w}{bc}', '=', r'\frac{wa}{abc}').scale(1.2).move_to(RIGHT * 2.6)
    note = T('cut edge $a$: use only $b$ and $c$', 0.75).next_to(eq, UP, buff=0.7)
    common = T(r'same denominator for every cut\\winner follows $w$ times its cut multiplier', 0.72, ACCENT).next_to(eq, DOWN, buff=0.75)
    with self.say('s11_factors') as d:
      self.play(FadeIn(intro), FadeIn(ring), run_time=0.25 * d)
      self.play(LaggedStart(*[FadeIn(f) for f in factors], lag_ratio=0.3), run_time=0.5 * d)
    with self.say('s11_cancel') as d:
      self.play(ring.arcs[(0, 1)].animate.set_opacity(0.12), ring.arcs[(1, 0)].animate.set_opacity(0.12),
                FadeIn(note), Write(eq[0]), run_time=0.3 * d)
      self.play(Write(eq[1]), Write(eq[2]), run_time=0.35 * d)
      self.play(FadeIn(common), run_time=0.2 * d)
    self.play(FadeOut(Group(*self.mobjects)), run_time=0.4)
    fam = (0, 1, 2)
    cols = VGroup()
    for j, e in enumerate(fam):
      big = TreePic(j, e, R=0.85, r=0.28)
      others = VGroup(*[dim(TreePic(j, x, R=0.45, r=0.2), 0.5) for x in range(3) if x != e]).arrange(RIGHT, buff=0.35)
      lt = M('>', 0.9, ACCENT)
      col = VGroup(big, lt, others).arrange(DOWN, buff=0.3)
      cols.add(col)
    cols.arrange(RIGHT, buff=1.4).move_to(UP * 0.35)
    cap = T('same new rates for all roots; each winner is strictly heaviest', 0.72, ACCENT).to_edge(DOWN, buff=0.55)
    with self.say('s11_rates') as d:
      self.play(LaggedStart(*[FadeIn(c[0]) for c in cols], lag_ratio=0.25), run_time=0.3 * d)
      self.play(LaggedStart(*[FadeIn(VGroup(c[1], c[2])) for c in cols], lag_ratio=0.25), run_time=0.3 * d)
      self.play(FadeIn(cap), run_time=0.15 * d)
    l1 = M(r'\text{same bag} \;\Rightarrow\; \text{weight(look-alike)} = \text{weight(ours)}', 0.85)
    l2 = M(r'\text{lighter tree somewhere} \;\Rightarrow\; \text{weight(look-alike)} < \text{weight(ours)}', 0.85)
    lines = VGroup(l1, l2).arrange(DOWN, buff=0.6).move_to(DOWN * 0.2)
    with self.say('s11_bag') as d:
      self.play(FadeOut(cap), cols.animate.scale(0.6).to_edge(UP, buff=0.4), run_time=0.15 * d)
      self.play(Write(l1), run_time=0.25 * d)
      self.play(Write(l2), run_time=0.25 * d)
      ctr = T('contradiction: no look-alike exists', 0.8, WARN).to_edge(DOWN, buff=0.6)
      self.play(l1[0].animate.set_color(WARN), l2[0].animate.set_color(WARN), FadeIn(ctr), run_time=0.15 * d)
    self.play(FadeOut(Group(*self.mobjects)), run_time=0.6)


class Cactus(NarratedScene):
  def construct(self):
    c6 = LEFT * 4.3 + UP * 0.3
    pos6 = [ring_pos(i, 1.6, 6, c6) for i in range(6)]
    t6 = TreePic(0, 2, n=6, R=1.6, r=0.28, center=c6)
    el6 = VGroup(*[Line(pos6[i], pos6[(i + 1) % 6], color=MUTED, stroke_width=2).set_opacity(0.4) for i in range(6)])
    lab6 = T('6 states: cut one edge', 0.65, MUTED).next_to(t6, DOWN, buff=0.4)
    # Cactus: triangle + square sharing S, and a branch.
    P = {'S': np.array([1.6, 0.3, 0]), 'T1': np.array([0.5, 1.4, 0]), 'T2': np.array([0.5, -0.8, 0]),
         'Q1': np.array([2.75, 1.45, 0]), 'Q2': np.array([3.9, 0.3, 0]), 'Q3': np.array([2.75, -0.85, 0]),
         'B': np.array([5.3, 0.3, 0])}
    tri_e = [('S', 'T1'), ('T1', 'T2'), ('T2', 'S')]
    sq_e = [('S', 'Q1'), ('Q1', 'Q2'), ('Q2', 'Q3'), ('Q3', 'S')]
    br_e = [('Q2', 'B')]
    r = 0.24

    def edges(lst, col):
      return VGroup(*[Line(P[a], P[b], color=col, stroke_width=8).set_opacity(0.45) for a, b in lst])

    tri, sq, br = edges(tri_e, ORANGE), edges(sq_e, PURPLE_B), edges(br_e, MUTED)
    nodes = VGroup(*[state('', P[k], r, label=False) for k in P])
    root = Circle(r + 0.09, color=ROOT, stroke_width=5).move_to(P['T1'])
    cap = T('a cactus: loops share at most a point', 0.72, MUTED).to_edge(DOWN, buff=0.55)
    with self.say('s12_cactus') as d:
      self.play(FadeIn(el6), FadeIn(t6), FadeIn(lab6), run_time=0.25 * d)
      self.play(Create(tri), Create(sq), Create(br), FadeIn(nodes), run_time=0.35 * d)
      self.play(FadeIn(cap), run_time=0.15 * d)
    tri_t = [('T2', 'T1'), ('S', 'T1')]
    sq_t = [('Q1', 'S'), ('Q2', 'Q1'), ('Q3', 'S')]
    br_t = [('B', 'Q2')]

    def arrows(lst):
      return VGroup(*[arrow_between(P[a], P[b], r, 0, INK, 5, 0.18) for a, b in lst])

    A1, A2, A3 = arrows(tri_t), arrows(sq_t), arrows(br_t)
    done = T('proved: every cactus network', 0.8, ACCENT).to_edge(DOWN, buff=0.55)
    with self.say('s12_glue') as d:
      self.play(FadeOut(VGroup(el6, t6, lab6)), Create(root), run_time=0.1 * d)
      self.play(GrowArrow(A1[0]), GrowArrow(A1[1]), *[GrowArrow(a) for a in A2], GrowArrow(A3[0]), run_time=0.2 * d)
      def copies(keys):
        return VGroup(*[state('', P[k], r, label=False) for k in keys])

      p1 = VGroup(tri, A1, copies(['S', 'T1', 'T2']), root)
      p2 = VGroup(sq, A2, copies(['S', 'Q1', 'Q2', 'Q3']))
      p3 = VGroup(br, A3, copies(['Q2', 'B']))
      self.remove(nodes)
      self.add(p1, p2, p3)
      self.play(p1.animate.shift(LEFT * 1.1), p3.animate.shift(RIGHT * 1.0), run_time=0.2 * d)
      self.wait(0.1 * d)
      self.play(p1.animate.shift(RIGHT * 1.1), p3.animate.shift(LEFT * 1.0), run_time=0.2 * d)
      self.play(FadeOut(cap), FadeIn(done), run_time=0.12 * d)
    self.play(FadeOut(Group(*self.mobjects)), run_time=0.6)


class K4(NarratedScene):
  def construct(self):
    k4 = NUM['k4']
    c = LEFT * 4.4 + UP * 0.2
    pos = [c + v for v in [UP * 1.6, RIGHT * 1.6, DOWN * 1.6, LEFT * 1.6]]
    edges = VGroup(*[Line(pos[a], pos[b], color=MUTED, stroke_width=4) for a in range(4) for b in range(a + 1, 4)])
    nodes = VGroup(*[state(i, pos[i], 0.32) for i in range(4)])
    K = VGroup(edges, nodes)
    facts = VGroup(T('16 trees per root', 0.8), T(r'$16^4 = 65{,}536$ families', 0.8),
                   T(f'{k4["uc"]} uniquely constructable', 0.8, ACCENT)).arrange(DOWN, buff=0.45, aligned_edge=LEFT)
    facts.move_to(RIGHT * 2.6)
    with self.say('s13_k4') as d:
      self.play(Create(edges), FadeIn(nodes), run_time=0.25 * d)
      for f in facts:
        self.play(FadeIn(f, shift=RIGHT * 0.2), run_time=0.17 * d)
    # +/-1 grid.
    cw = 0.44
    grid = VGroup()
    cells = {}
    for r in range(4):
      for i, v in enumerate(k4['grid'][r]):
        sq_ = Square(cw, stroke_width=1.5, stroke_color=BACKGROUND).set_fill(PRIMARY if v > 0 else WARM, 0.55)
        sq_.move_to([-2.9 + i * cw, 1.2 - r * (cw + 0.12), 0])
        sym = M('+' if v > 0 else '-', 0.6).move_to(sq_)
        cells[(r, i)] = VGroup(sq_, sym)
        grid.add(cells[(r, i)])
    rlabs = VGroup(*[T(f'root {r}', 0.6, ROOT).next_to(cells[(r, 0)], LEFT, buff=0.25) for r in range(4)])
    gtitle = T('64 labels: one per root and tree', 0.7, MUTED).next_to(grid, UP, buff=0.45)
    G = VGroup(grid, rlabs, gtitle).move_to(LEFT * 1.3 + UP * 1.1)
    smp = k4['sample']
    hl = VGroup(*[SurroundingRectangle(cells[(r, smp[r])], color=KNOBC, buff=0.03, stroke_width=4) for r in range(4)])
    vals = [k4['grid'][r][smp[r]] for r in range(4)]
    ssum = M(' '.join(('+' if v > 0 else '-') + '1' for v in vals).lstrip('+') + r' = 0', 0.75, KNOBC)
    ssum.next_to(G, DOWN, buff=0.45)
    rule = T(r'every uniquely constructable family scores $0$, $2$ or $4$', 0.75, ACCENT).next_to(ssum, DOWN, buff=0.4)
    with self.say('s13_cert') as d:
      self.play(FadeOut(facts), FadeOut(K), run_time=0.12 * d)
      self.play(FadeIn(gtitle), FadeIn(rlabs), LaggedStart(*[FadeIn(x) for x in grid], lag_ratio=0.01), run_time=0.3 * d)
      self.play(Create(hl), run_time=0.15 * d)
      self.play(Write(ssum), run_time=0.15 * d)
      self.play(FadeIn(rule), run_time=0.15 * d)
    ravg = VGroup(*[M(f'{x:+.4f}', 0.65, INK).next_to(cells[(r, 15)], RIGHT, buff=0.35) for r, x in enumerate(k4['row_avg'])])
    avg_h = T('lottery average', 0.6, MUTED).next_to(ravg, UP, buff=0.2)
    total = M(rf'\text{{total}} = {k4["expect"]}', 0.9, WARN).next_to(ravg, DOWN, buff=0.35).align_to(ravg, LEFT)
    vs = M(r'\text{shared lottery: } \geq 0 \quad \text{vs} \quad ' + f'{k4["expect"]}', 0.85, WARN)
    vs.move_to(DOWN * 3.2)
    with self.say('s13_contra') as d:
      self.play(FadeOut(hl), FadeOut(ssum), FadeIn(avg_h), LaggedStart(*[FadeIn(x) for x in ravg], lag_ratio=0.25),
                run_time=0.25 * d)
      self.play(Write(total), run_time=0.15 * d)
      self.play(FadeOut(rule), Write(vs), run_time=0.2 * d)
      cr = T('no shared lottery (exact fractions)', 0.75, WARN).next_to(vs, UP, buff=0.3)
      self.play(FadeIn(cr), run_time=0.12 * d)
    # Minors: a subdivided K4 shrinks to K4.
    c2 = ORIGIN + UP * 0.3
    pos2 = [c2 + v for v in [UP * 1.8, RIGHT * 1.8, DOWN * 1.8, LEFT * 1.8]]
    mid = (pos2[0] + pos2[1]) / 2 + UR * 0.8
    e2 = VGroup(*[Line(pos2[a], pos2[b], color=MUTED, stroke_width=4) for a, b in
                  [(0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]])
    path = VGroup(Line(pos2[0], mid, color=KNOBC, stroke_width=5), Line(mid, pos2[1], color=KNOBC, stroke_width=5))
    n2 = VGroup(*[state(i, pos2[i], 0.3) for i in range(4)])
    xn = state('', mid, 0.28, label=False, color=KNOBC)
    cap = T(r'connected, hops both ways: some rates have no shared lottery', 0.7, MUTED).to_edge(DOWN, buff=0.5)
    xl_ = T('extra state', 0.62, KNOBC).next_to(mid, UR, buff=0.25)
    with self.say('s13_minor') as d:
      self.play(FadeOut(Group(*self.mobjects)), run_time=0.15 * d)
      self.play(FadeIn(e2), FadeIn(path), FadeIn(n2), FadeIn(xn), FadeIn(xl_), run_time=0.2 * d)
      straight = Line(pos2[0], pos2[1], color=KNOBC, stroke_width=5)
      self.play(Transform(path, straight), xn.animate.move_to((pos2[0] + pos2[1]) / 2).scale(0.01), FadeOut(xl_),
                run_time=0.3 * d)
      self.play(FadeIn(cap), run_time=0.15 * d)
    l1 = T('the method: blocked', 0.8, WARN)
    l2 = T('the guess: never violated in 150 searches', 0.8, ACCENT)
    ls = VGroup(l1, l2).arrange(DOWN, buff=0.45, aligned_edge=LEFT).to_edge(DOWN, buff=0.5)
    with self.say('s13_not') as d:
      self.play(FadeOut(cap), VGroup(e2, path, n2).animate.scale(0.75).shift(UP * 0.7), run_time=0.15 * d)
      self.play(FadeIn(l1), run_time=0.2 * d)
      self.play(FadeIn(l2), run_time=0.25 * d)
    self.play(FadeOut(Group(*self.mobjects)), run_time=0.6)


class Status(NarratedScene):
  def construct(self):
    def item(mark, text, color):
      return VGroup(mark, T(text, 0.8, color)).arrange(RIGHT, buff=0.35)

    def circ():
      return Circle(0.14, color=MUTED, stroke_width=3)

    i1 = item(tick(0.9), 'proved (written): every cactus network, any size, any rates', INK)
    i2 = item(tick(0.9), 'four linked states: exact computer certificate', INK)
    i3 = item(tick(0.9), 'its spread to bigger networks: written proof', INK)
    i4 = item(circ(), 'correctness: high confidence; no external review or software check', MUTED)
    i5 = item(circ(), 'originality: less certain; no earlier result found', SECONDARY)
    items = VGroup(i1, i2, i3, i4, i5).arrange(DOWN, buff=0.5, aligned_edge=LEFT).move_to(DOWN * 0.3)
    head = T('Where things stand', 0.9, MUTED).to_edge(UP, buff=0.7)
    if items.width > 13:
      items.scale_to_fit_width(13)
    with self.say('s14_proved') as d:
      self.play(FadeIn(head), FadeIn(i1, shift=0.2 * RIGHT), run_time=0.2 * d)
      self.wait(0.25 * d)
      self.play(FadeIn(i2, shift=0.2 * RIGHT), run_time=0.15 * d)
      self.play(FadeIn(i3, shift=0.2 * RIGHT), run_time=0.15 * d)
    with self.say('s14_caveat') as d:
      self.play(FadeIn(i4, shift=0.2 * RIGHT), run_time=0.25 * d)
      self.wait(0.2 * d)
      self.play(FadeIn(i5, shift=0.2 * RIGHT), run_time=0.25 * d)
    self.play(FadeOut(Group(*self.mobjects)), run_time=0.6)


class Ending(NarratedScene):
  def construct(self):
    r1 = T('1. Steady state: weighted tree totals; response: family average', 0.75)
    r2 = T('2. On a ring, one token per edge: right odds at every root, no look-alikes', 0.75)
    r3 = T('3. Four linked states block the method, not the guess', 0.75)
    recap = VGroup(r1, r2, r3).arrange(DOWN, buff=0.5, aligned_edge=LEFT).move_to(UP * 0.1)
    if recap.width > 13:
      recap.scale_to_fit_width(13)
    with self.say('s15_recap1') as d:
      self.play(FadeIn(r1, shift=0.2 * UP), run_time=0.25 * d)
    with self.say('s15_recap2') as d:
      self.play(FadeIn(r2, shift=0.2 * UP), run_time=0.15 * d)
      self.wait(0.35 * d)
      self.play(FadeIn(r3, shift=0.2 * UP), run_time=0.15 * d)
    head = T("What we still don't know", 0.9, SECONDARY).to_edge(UP, buff=0.7)
    c = DOWN * 0.3 + LEFT * 3.6
    P = [c + UP * 1.7, c + LEFT * 1.7, c + RIGHT * 1.7, c + DOWN * 1.7]
    dia_e = VGroup(*[Line(P[a], P[b], color=MUTED, stroke_width=4) for a, b in [(0, 1), (0, 2), (1, 2), (1, 3), (2, 3)]])
    dia_e[2].set_color(SECONDARY)
    dia_n = VGroup(*[state('', p, 0.26, label=False) for p in P])
    dia = VGroup(dia_e, dia_n)
    o1 = T('Is the guess true for every network?', 0.75)
    o2 = T('Smallest open case: the diamond', 0.75)
    o3 = T(r'edge tokens: sampled error about $0.06$', 0.7, MUTED)
    os_ = VGroup(o1, o2, o3).arrange(DOWN, buff=0.4, aligned_edge=LEFT).move_to(RIGHT * 2.4 + DOWN * 0.3)
    with self.say('s15_open') as d:
      self.play(FadeOut(recap), FadeIn(head), run_time=0.12 * d)
      self.play(FadeIn(o1), run_time=0.15 * d)
      self.play(FadeIn(dia), FadeIn(o2), run_time=0.2 * d)
      self.play(FadeIn(o3), run_time=0.2 * d)
    self.play(FadeOut(Group(*self.mobjects)), run_time=0.6)
    t = T('Unicyclic and cactus networks satisfy\\\\the topological response conjecture', 0.9).move_to(UP * 1.2)
    org = T('Valyu Research, 2026', 0.75, MUTED).next_to(t, DOWN, buff=0.5)
    path = T(r'\texttt{physics/statistical-physics/nonequilibrium-response/}\\\texttt{cactus-response-coupling}', 0.6,
             MUTED).next_to(org, DOWN, buff=0.45)
    voice = T('Narration uses a synthetic voice.', 0.55, MUTED).to_edge(DOWN, buff=0.5)
    self.play(FadeIn(t), FadeIn(org), FadeIn(path), FadeIn(voice), run_time=1.0)
    self.wait(5)
