"""Explainer: endless words that never repeat their shape.

Running example: Dejean's word abcacbcabc... and the binary rule a -> 00101, b -> 00111, c -> 01100.
Every example on screen is reproduced by check_numbers.py; the counts 23, 4,596 and 3,654 come from
../verification/results_check_ct.json and results_ctproof.txt.
"""

from manim import *
from vrvideo import *

SCENES = ['Hook', 'TwoLetters', 'Thue', 'Shape', 'BinaryShape', 'Table', 'Rule', 'Window', 'NearSquare',
          'Upstairs', 'Finite', 'Status', 'Ending']

H2 = {'a': '00101', 'b': '00111', 'c': '01100'}
H3 = {'a': '000101', 'b': '000221', 'c': '022211'}
DEJEAN = {'a': 'abcacbcabcbacbcacba', 'b': 'bcabacabcacbacabacb', 'c': 'cabcbabcabacbabcbac'}
FIRST_HALF = PRIMARY
SECOND_HALF = WARM
GREYED = '#5b6068'


def dejean(n):
  w = 'a'
  while len(w) < n:
    w = ''.join(DEJEAN[c] for c in w)
  return w[:n]


W30 = dejean(30)
X30 = ''.join(H2[c] for c in W30[:6])


def pd(x):
  out = []
  for i in range(len(x)):
    js = [j for j in range(i) if x[j] <= x[i]]
    out.append(i - max(js) if js else 0)
  return out


def T(s, scale=0.7, color=INK):
  return Tex(s, color=color).scale(scale)


def M(s, scale=0.7, color=INK):
  return MathTex(s, color=color).scale(scale)


def glyph(ch, size, color=INK):
  g = MathTex(r'\mathtt{' + ch + r'}\vphantom{0p}', color=color)
  return g.scale(1.45 * size)


def tile(ch, size=0.8, color=INK, stroke=MUTED, fill=None, opacity=0.0):
  box = RoundedRectangle(width=size, height=size, corner_radius=0.12 * size, stroke_color=stroke, stroke_width=2)
  box.set_fill(fill or BACKGROUND, opacity if fill else 0.0)
  g = glyph(ch, size, color).move_to(box)
  return VGroup(box, g)


def row(word, size=0.8, gap=0.08, block=None, block_gap=0.22, **kw):
  """Tiles for a word; with block=q, an extra gap after every q letters."""
  g = VGroup()
  x = 0.0
  for i, ch in enumerate(word):
    if block and i and i % block == 0:
      x += block_gap
    g.add(tile(ch, size, **kw).move_to(RIGHT * x))
    x += size + gap
  return g.move_to(ORIGIN)


def columns(vals, width=0.75, gap=0.18, unit=0.42, base=0.3, color=PRIMARY):
  """Mountain profile: one column per value, bottoms on y = 0."""
  g = VGroup()
  for i, v in enumerate(vals):
    r = Rectangle(width=width, height=base + unit * v, stroke_color=color, stroke_width=2, fill_color=color,
                  fill_opacity=0.35)
    r.move_to(RIGHT * i * (width + gap), aligned_edge=DOWN)
    g.add(r)
  return g


def hop(p_from, p_to, color=SECONDARY, down=True, angle=0.75 * PI, width=3.5):
  """Curved arrow from one column foot to an earlier one, bulging downwards (or upwards)."""
  arc = ArcBetweenPoints(p_from, p_to, angle=angle)
  mid = arc.point_from_proportion(0.5)[1] - p_from[1]
  if (mid < 0) != down:
    arc = ArcBetweenPoints(p_from, p_to, angle=-angle)
  arc.set_stroke(color, width)
  arc.add_tip(tip_length=0.16, tip_width=0.16)
  return arc


def code_row(vals, xs, y, scale=0.75, color=ACCENT):
  return VGroup(*[M(str(v), scale, color).move_to([x, y, 0]) for v, x in zip(vals, xs)])


def tick(scale=1.0, color=OK):
  return MathTex(r'\checkmark', color=color).scale(scale)


def xmark(center, r=0.16, color=WARN, width=5):
  return VGroup(Line(center + UL * r, center + DR * r), Line(center + UR * r, center + DL * r)).set_stroke(color, width)


def binary_profile(word, width=0.5, gap=0.1, unit=0.6, base=0.45, color=PRIMARY, digit_scale=0.7):
  """Binary (or ternary) word drawn as low and high columns with the digit under each column."""
  cols = columns([int(c) for c in word], width, gap, unit, base, color)
  digits = VGroup(*[M(c, digit_scale).next_to(col, DOWN, buff=0.18) for c, col in zip(word, cols)])
  return VGroup(cols, digits)


class Hook(NarratedScene):
  def construct(self):
    word = row('banana', size=1.2, gap=0.12).move_to(UP * 0.6)
    with self.say('s01_banana') as d:
      self.play(LaggedStart(*[FadeIn(t, shift=0.2 * UP) for t in word], lag_ratio=0.15), run_time=0.25 * d)
      self.wait(0.1 * d)
      b1 = SurroundingRectangle(word[1:3], color=FIRST_HALF, buff=0.08, corner_radius=0.1, stroke_width=5)
      b2 = SurroundingRectangle(word[3:5], color=SECOND_HALF, buff=0.08, corner_radius=0.1, stroke_width=5)
      self.play(Create(b1), run_time=0.12 * d)
      self.play(Create(b2), run_time=0.12 * d)
      sq = SurroundingRectangle(word[1:5], color=WARN, buff=0.25, corner_radius=0.12, stroke_width=5)
      lab = T('a square', 1.0, WARN).next_to(sq, DOWN, buff=0.35)
      self.play(Create(sq), Write(lab), run_time=0.15 * d)

    ex1 = row('aa', 1.0, 0.1).move_to(LEFT * 3.6 + DOWN * 0.2)
    ex2 = row('abcabc', 1.0, 0.1).move_to(RIGHT * 2.0 + DOWN * 0.2)
    r1 = SurroundingRectangle(ex1, color=WARN, buff=0.18, corner_radius=0.1, stroke_width=5)
    r2 = SurroundingRectangle(ex2, color=WARN, buff=0.18, corner_radius=0.1, stroke_width=5)
    s1 = SurroundingRectangle(ex2[:3], color=FIRST_HALF, buff=0.06, corner_radius=0.08, stroke_width=4)
    s2 = SurroundingRectangle(ex2[3:], color=SECOND_HALF, buff=0.06, corner_radius=0.08, stroke_width=4)
    with self.say('s01_more') as d:
      self.play(FadeOut(VGroup(word, b1, b2, sq, lab), shift=UP * 0.4), run_time=0.2 * d)
      self.play(FadeIn(ex1), Create(r1), run_time=0.25 * d)
      self.play(FadeIn(ex2), Create(s1), Create(s2), Create(r2), run_time=0.3 * d)

    stream = row('abcbacbcabacb', 0.75, 0.07)
    dots = M(r'\cdots', 1.4).next_to(stream, RIGHT, buff=0.25)
    grp = VGroup(stream, dots).move_to(UP * 0.5)
    q = T('An endless string with no square anywhere?', 0.9, SECONDARY).next_to(grp, DOWN, buff=0.9)
    with self.say('s01_question') as d:
      self.play(FadeOut(VGroup(ex1, ex2, r1, r2, s1, s2)), run_time=0.15 * d)
      self.play(LaggedStart(*[FadeIn(t, shift=0.3 * LEFT) for t in stream], lag_ratio=0.08), FadeIn(dots),
                run_time=0.4 * d)
      self.play(Write(q), run_time=0.25 * d)
    self.play(FadeOut(VGroup(grp, q)), run_time=0.6)


class TwoLetters(NarratedScene):
  def construct(self):
    size = 1.0
    head = T('Two letters: a and b', 0.8, MUTED).to_edge(UP, buff=0.5)
    base = row('aba', size, 0.1).move_to(UP * 1.6)
    try_a = tile('a', size).move_to(base[1])
    clash = SurroundingRectangle(VGroup(base[0], try_a), color=WARN, buff=0.08, corner_radius=0.1, stroke_width=5)
    with self.say('s02_try') as d:
      self.play(FadeIn(head), run_time=0.08 * d)
      self.play(FadeIn(base[0], shift=0.2 * DOWN), run_time=0.12 * d)
      self.play(FadeIn(try_a, shift=0.2 * DOWN), run_time=0.1 * d)
      self.play(Create(clash), run_time=0.1 * d)
      self.play(FadeOut(try_a), FadeOut(clash), run_time=0.08 * d)
      self.play(FadeIn(base[1], shift=0.2 * DOWN), run_time=0.12 * d)
      self.play(FadeIn(base[2], shift=0.2 * DOWN), run_time=0.12 * d)
      ok = tick(1.2).next_to(base, RIGHT, buff=0.4)
      self.play(FadeIn(ok), run_time=0.08 * d)

    left = row('abaa', 0.9, 0.08).move_to(LEFT * 3.4 + DOWN * 1.2)
    right = row('abab', 0.9, 0.08).move_to(RIGHT * 3.4 + DOWN * 1.2)
    al = Arrow(base.get_bottom() + LEFT * 0.4, left.get_top() + UP * 0.1, color=MUTED, buff=0.15, stroke_width=4)
    ar = Arrow(base.get_bottom() + RIGHT * 0.4, right.get_top() + UP * 0.1, color=MUTED, buff=0.15, stroke_width=4)
    bad_l = SurroundingRectangle(left[2:], color=WARN, buff=0.08, corner_radius=0.1, stroke_width=5)
    bad_r = SurroundingRectangle(right, color=WARN, buff=0.08, corner_radius=0.1, stroke_width=5)
    hl = VGroup(SurroundingRectangle(right[:2], color=FIRST_HALF, buff=0.04, stroke_width=3),
                SurroundingRectangle(right[2:], color=SECOND_HALF, buff=0.04, stroke_width=3))
    with self.say('s02_stuck') as d:
      self.play(FadeOut(ok), GrowArrow(al), FadeIn(left, shift=0.2 * DOWN), run_time=0.15 * d)
      self.play(Create(bad_l), left[3][0].animate.set_stroke(WARN), run_time=0.15 * d)
      self.play(GrowArrow(ar), FadeIn(right, shift=0.2 * DOWN), run_time=0.15 * d)
      self.play(Create(hl), run_time=0.1 * d)
      self.play(Create(bad_r), run_time=0.1 * d)
      swap = T('starting with b: same, with letters swapped', 0.7, MUTED).to_edge(DOWN, buff=0.6)
      self.play(FadeIn(swap), run_time=0.12 * d)

    verdict = T('Longest square-free word: 3 letters', 0.95, WARN).to_edge(DOWN, buff=0.6)
    with self.say('s02_ponder') as d:
      self.play(FadeOut(swap), run_time=0.15 * d)
      self.play(Write(verdict), run_time=0.35 * d)
    self.play(FadeOut(Group(*self.mobjects)), run_time=0.6)


class Thue(NarratedScene):
  def construct(self):
    head = T('Three letters: a, b and c', 0.8, MUTED).to_edge(UP, buff=0.5)
    r1, r2 = row(W30[:15], 0.6, 0.06), row(W30[15:], 0.6, 0.06)
    word = VGroup(*r1, *r2)
    VGroup(r1, r2).arrange(DOWN, buff=0.15).move_to(UP * 1.9)
    dots = M(r'\cdots', 1.0).next_to(r2, RIGHT, buff=0.15)
    cap = T('Axel Thue: no square, ever', 0.8, ACCENT).move_to(UP * 0.3)
    with self.say('s03_thue') as d:
      self.play(FadeIn(head), run_time=0.1 * d)
      self.play(LaggedStart(*[FadeIn(t) for t in word], lag_ratio=0.06), FadeIn(dots), run_time=0.5 * d)
      self.play(FadeIn(cap), run_time=0.15 * d)

    ex = row('abcab', 1.0, 0.1).move_to(DOWN * 0.9)
    period = Brace(ex[:3], UP, color=SECONDARY, buff=0.12)
    plab = T('repeats every 3', 0.7, SECONDARY).next_to(period, UP, buff=0.12)
    length = Brace(ex, DOWN, color=MUTED, buff=0.12)
    llab = T('5 letters long', 0.7, MUTED).next_to(length, DOWN, buff=0.12)
    again = SurroundingRectangle(ex[3:], color=SECONDARY, buff=0.06, corner_radius=0.08, stroke_width=3)
    expo = M(r'\text{exponent} = \frac{5}{3}', 0.95).next_to(ex, RIGHT, buff=0.7)
    with self.say('s03_period') as d:
      self.play(FadeOut(cap), FadeIn(ex, shift=0.2 * UP), run_time=0.15 * d)
      self.play(GrowFromCenter(period), FadeIn(plab), Create(again), run_time=0.2 * d)
      self.play(GrowFromCenter(length), FadeIn(llab), run_time=0.15 * d)
      self.play(Write(expo), run_time=0.2 * d)
      sq = M(r'\text{a square: exponent } 2', 0.75, WARN).next_to(expo, DOWN, buff=0.5).align_to(expo, LEFT)
      self.play(FadeIn(sq), run_time=0.12 * d)

    # bcacbca: period 4, length 7, exponent 7/4 (letters 2-8 of the word).
    hi = SurroundingRectangle(word[1:8], color=SECONDARY, buff=0.06, corner_radius=0.06, stroke_width=4)
    seven = M(r'\tfrac{7}{4}', 1.0, SECONDARY).next_to(r2, DOWN, buff=0.25).set_x(hi.get_x())
    dej = T(r'Fran\c{c}oise Dejean, 1972: no block above exponent $\tfrac{7}{4}$', 0.8, ACCENT).move_to(DOWN * 1.2)
    with self.say('s03_dejean') as d:
      self.play(FadeOut(VGroup(ex, period, plab, length, llab, again, expo, sq)), run_time=0.15 * d)
      self.play(Write(dej), run_time=0.3 * d)
      self.play(Create(hi), FadeIn(seven), run_time=0.2 * d)
      self.play(Indicate(word[1:8], color=SECONDARY, scale_factor=1.08), run_time=0.15 * d)

    name = T("Dejean's word", 0.85, INK).next_to(VGroup(r1, r2), DOWN, buff=0.45)
    with self.say('s03_keep') as d:
      self.play(FadeOut(VGroup(hi, seven, dej, head)), run_time=0.25 * d)
      self.play(FadeIn(name), run_time=0.25 * d)
    self.play(FadeOut(VGroup(word, dots, name)), run_time=0.6)


class Shape(NarratedScene):
  def construct(self):
    A, B = [3, 1, 4, 1, 5], [2, 0, 7, 0, 9]
    y0 = -0.9
    ca = columns(A).move_to([-3.4, y0, 0], aligned_edge=DOWN)
    cb = columns(B, color=SECOND_HALF).move_to([3.4, y0, 0], aligned_edge=DOWN)
    la = VGroup(*[M(str(v), 0.8).next_to(c, DOWN, buff=0.15) for v, c in zip(A, ca)])
    lb = VGroup(*[M(str(v), 0.8).next_to(c, DOWN, buff=0.15) for v, c in zip(B, cb)])
    with self.say('s04_heights') as d:
      self.play(LaggedStart(*[GrowFromEdge(c, DOWN) for c in ca], lag_ratio=0.2), FadeIn(la), run_time=0.35 * d)
      self.play(LaggedStart(*[GrowFromEdge(c, DOWN) for c in cb], lag_ratio=0.2), FadeIn(lb), run_time=0.35 * d)

    ridge_a = VMobject().set_points_as_corners([c.get_top() for c in ca]).set_stroke(SECONDARY, 4)
    ridge_b = VMobject().set_points_as_corners([c.get_top() for c in cb]).set_stroke(SECONDARY, 4)
    yc = y0 - 2.15
    code_lab = T('code', 0.7, ACCENT).move_to([-6.4, yc, 0])
    with self.say('s04_same') as d:
      self.play(Create(ridge_a), Create(ridge_b), run_time=0.35 * d)
      self.play(FadeOut(ridge_a), FadeOut(ridge_b), FadeIn(code_lab), run_time=0.25 * d)

    xa = [c.get_center()[0] for c in ca]
    xb = [c.get_center()[0] for c in cb]
    codes_a = code_row(pd(A), xa, yc, 0.85)
    codes_b = code_row(pd(B), xb, yc, 0.85)
    arc_y = y0 - 0.65

    def walk(cols, xs, i, run):
      """Act out the rule for column i; returns the arc (or None) and the animations' total time."""
      anims = []
      cur = cols[i]
      self.play(cur.animate.set_fill(SECONDARY, 0.8), run_time=run * 0.2)
      j = i - 1
      while j >= 0 and cols[j].height > cur.height + 1e-6:
        self.play(Indicate(cols[j], color=WARN, scale_factor=1.0), run_time=run * 0.2)
        j -= 1
      arc = None
      if j >= 0:
        self.play(Indicate(cols[j], color=OK, scale_factor=1.0), run_time=run * 0.2)
        arc = hop([xs[i], arc_y, 0], [xs[j], arc_y, 0], SECONDARY)
        self.play(Create(arc), run_time=run * 0.2)
      return arc

    with self.say('s04_rule') as d:
      arc2 = walk(ca, xa, 2, 0.4 * d)
      self.play(Write(codes_a[2]), ca[2].animate.set_fill(PRIMARY, 0.35), run_time=0.06 * d)
      arc3 = walk(ca, xa, 3, 0.4 * d)
      self.play(Write(codes_a[3]), ca[3].animate.set_fill(PRIMARY, 0.35), run_time=0.06 * d)

    with self.say('s04_code') as d:
      arc4 = hop([xa[4], arc_y, 0], [xa[3], arc_y, 0], SECONDARY)
      self.play(Write(codes_a[0]), Write(codes_a[1]), Create(arc4), Write(codes_a[4]), run_time=0.25 * d)
      arcs_b = VGroup(*[hop([xb[i], arc_y, 0], [xb[i - v], arc_y, 0], SECONDARY) for i, v in enumerate(pd(B)) if v])
      self.play(Create(arcs_b), Write(codes_b), run_time=0.3 * d)
      eq = M('=', 1.2, OK).move_to([0, yc, 0])
      box_a = SurroundingRectangle(codes_a, color=OK, buff=0.15, corner_radius=0.08)
      box_b = SurroundingRectangle(codes_b, color=OK, buff=0.15, corner_radius=0.08)
      self.play(Create(box_a), Create(box_b), FadeIn(eq), run_time=0.2 * d)

    name = T('The shape: a \\emph{Cartesian tree}', 0.85, INK).to_edge(UP, buff=0.4)
    with self.say('s04_name') as d:
      self.play(Write(name), run_time=0.3 * d)
    self.play(FadeOut(Group(*self.mobjects)), run_time=0.6)


class BinaryShape(NarratedScene):
  def construct(self):
    words = ['00', '01', '11', '10']
    xs = [-4.8, -1.6, 1.6, 4.8]
    groups = VGroup()
    codes = VGroup()
    for w, x in zip(words, xs):
      p = binary_profile(w, 0.75, 0.2, unit=0.8, base=0.5, digit_scale=0.85).move_to([x, 0.6, 0])
      p.align_to([0, 0.2, 0], DOWN)
      groups.add(p)
      cx = [c.get_center()[0] for c in p[0]]
      codes.add(code_row(pd(w), cx, -1.3, 0.85))
    lab = T('code', 0.7, ACCENT).move_to([-6.4, -1.3, 0])
    head = T('0 is lower than 1', 0.8, MUTED).to_edge(UP, buff=0.5)
    with self.say('s05_binary') as d:
      self.play(FadeIn(head), LaggedStart(*[FadeIn(g, shift=0.2 * UP) for g in groups], lag_ratio=0.15),
                run_time=0.3 * d)
      self.play(FadeIn(lab), LaggedStart(*[Write(c) for c in codes[:3]], lag_ratio=0.2), run_time=0.25 * d)
      same = SurroundingRectangle(VGroup(groups[:3], codes[:3]), color=OK, buff=0.25, corner_radius=0.12)
      self.play(Create(same), run_time=0.15 * d)
      self.play(Write(codes[3]), Indicate(groups[3], color=SECONDARY), run_time=0.15 * d)

    big = binary_profile('0110', 0.7, 0.25, unit=0.9, base=0.55, digit_scale=0.9).move_to(ORIGIN)
    big.align_to([0, -0.4, 0], DOWN)
    bx = [c.get_center()[0] for c in big[0]]
    ay = -1.35
    arcs = VGroup(hop([bx[1], ay, 0], [bx[0], ay, 0]), hop([bx[2], ay, 0], [bx[1], ay, 0]),
                  hop([bx[3], ay, 0], [bx[0], ay, 0], color=ACCENT))
    bcode = code_row(pd('0110'), bx, -2.55, 0.9)
    with self.say('s05_0110') as d:
      self.play(FadeOut(VGroup(groups, codes, lab, same, head)), run_time=0.15 * d)
      self.play(FadeIn(big, shift=0.2 * UP), run_time=0.15 * d)
      self.play(Create(arcs[0]), Write(bcode[0]), Write(bcode[1]), run_time=0.12 * d)
      self.play(Create(arcs[1]), Write(bcode[2]), run_time=0.12 * d)
      self.play(big[0][3].animate.set_fill(SECONDARY, 0.8), run_time=0.08 * d)
      self.play(Create(arcs[2]), Write(bcode[3]), run_time=0.22 * d)

    u, v = '0111', '0011'
    pu = binary_profile(u, 0.55, 0.12, color=FIRST_HALF)
    pv = binary_profile(v, 0.55, 0.12, color=SECOND_HALF)
    pair = VGroup(pu, pv).arrange(RIGHT, buff=0.12, aligned_edge=DOWN).move_to(UP * 0.4)
    ux = [c.get_center()[0] for c in pu[0]]
    vx = [c.get_center()[0] for c in pv[0]]
    cu = code_row(pd(u), ux, -1.45, 0.85)
    cv = code_row(pd(v), vx, -1.45, 0.85)
    bu = Brace(VGroup(pu, cu), DOWN, color=FIRST_HALF, buff=0.15)
    bv = Brace(VGroup(pv, cv), DOWN, color=SECOND_HALF, buff=0.15)
    blu = T('4 letters', 0.7, FIRST_HALF).next_to(bu, DOWN, buff=0.1)
    blv = T('4 letters', 0.7, SECOND_HALF).next_to(bv, DOWN, buff=0.1)
    outer = SurroundingRectangle(VGroup(pair, cu, cv), color=WARN, buff=0.3, corner_radius=0.12, stroke_width=5)
    olab = T('a shape square', 0.9, WARN).next_to(outer, UP, buff=0.2)
    with self.say('s05_square') as d:
      self.play(FadeOut(VGroup(big, arcs, bcode)), run_time=0.12 * d)
      self.play(FadeIn(pu, shift=0.2 * UP), run_time=0.12 * d)
      self.play(FadeIn(pv, shift=0.2 * UP), run_time=0.12 * d)
      self.play(Write(cu), Write(cv), run_time=0.2 * d)
      self.play(GrowFromCenter(bu), GrowFromCenter(bv), FadeIn(blu), FadeIn(blv), run_time=0.12 * d)
      self.play(Create(outer), Write(olab), run_time=0.15 * d)

    l1 = T('Every square is also a shape square', 0.85).move_to(UP * 1.2)
    l2 = T('Short ones are unavoidable, so forbid only long ones:', 0.85).move_to(DOWN * 0.1)
    l3 = T('halves of at least some minimum length', 0.85, SECONDARY).next_to(l2, DOWN, buff=0.35)
    with self.say('s05_harder') as d:
      self.play(FadeOut(VGroup(pair, cu, cv, bu, bv, blu, blv, outer, olab)), run_time=0.12 * d)
      self.play(Write(l1), run_time=0.25 * d)
      self.play(FadeIn(l2), run_time=0.2 * d)
      self.play(Write(l3), run_time=0.2 * d)
    self.play(FadeOut(VGroup(l1, l2, l3)), run_time=0.6)


class Table(NarratedScene):
  def construct(self):
    vals = {2: ['1', '5', '29', '?'], 3: ['1', '9', '?', '?'], 4: ['1', '9', '?', '?'], 5: ['1', '9', '?', '?']}
    cw, ch = 1.8, 0.9
    x0, y0 = -1.4, 1.0
    cells = {}
    grid = VGroup()
    for j in range(4):
      grid.add(M(str(j + 1), 0.95, MUTED).move_to([x0 + j * cw, y0 + ch, 0]))
    colhead = T('halves at least', 0.8, MUTED).next_to(grid, UP, buff=0.25)
    rows = VGroup()
    for i, s in enumerate([2, 3, 4, 5]):
      y = y0 - i * ch
      rows.add(T(f'{s} letters', 0.85, MUTED).move_to([x0 - 2.4, y, 0]))
      for j, v in enumerate(vals[s]):
        color = SECONDARY if v == '?' else INK
        cells[(s, j + 1)] = M(v, 1.05, color).move_to([x0 + j * cw, y, 0])
    hline = Line([x0 - 3.4, y0 + ch / 2, 0], [x0 + 3.5 * cw, y0 + ch / 2, 0], color=GREYED, stroke_width=2)
    vline = Line([x0 - 0.75, y0 + 1.45 * ch, 0], [x0 - 0.75, y0 - 3.5 * ch, 0], color=GREYED, stroke_width=2)
    src = T(r'Shibata, Mieno, K\"oppl and Inenaga (2026)', 0.7, INK).to_edge(UP, buff=0.35)
    longest = T('entry: length of the longest word with no such shape square', 0.65, MUTED).to_edge(DOWN, buff=0.45)
    with self.say('s06_table') as d:
      self.play(FadeIn(src), run_time=0.1 * d)
      self.play(FadeIn(colhead), FadeIn(grid), FadeIn(rows), Create(hline), Create(vline), run_time=0.25 * d)
      self.play(LaggedStart(*[FadeIn(c) for c in cells.values()], lag_ratio=0.05), run_time=0.3 * d)
      self.play(FadeIn(longest), run_time=0.15 * d)

    with self.say('s06_finite') as d:
      b29 = SurroundingRectangle(cells[(2, 3)], color=PRIMARY, buff=0.15)
      b9 = SurroundingRectangle(cells[(3, 2)], color=PRIMARY, buff=0.15)
      self.play(Create(b29), Indicate(cells[(2, 3)], color=PRIMARY), run_time=0.35 * d)
      self.play(Create(b9), Indicate(cells[(3, 2)], color=PRIMARY), run_time=0.35 * d)

    qs = [k for k, c in cells.items() if vals[k[0]][k[1] - 1] == '?']
    key = [(2, 4), (3, 3)]
    with self.say('s06_open') as d:
      self.play(FadeOut(b29), FadeOut(b9), run_time=0.08 * d)
      self.play(LaggedStart(*[Indicate(cells[k], color=SECONDARY, scale_factor=1.3) for k in qs], lag_ratio=0.1),
                run_time=0.2 * d)
      boxes = VGroup(*[SurroundingRectangle(cells[k], color=SECONDARY, buff=0.15, stroke_width=5) for k in key])
      guess = T('guessed: $\\infty$', 0.75, SECONDARY).next_to(boxes[0], RIGHT, buff=0.35)
      self.play(Create(boxes), FadeIn(guess), run_time=0.25 * d)
      rest = [k for k in qs if k not in key]
      self.play(LaggedStart(*[Indicate(cells[k], color=SECONDARY, scale_factor=1.2) for k in rest], lag_ratio=0.1),
                run_time=0.3 * d)

    infs = {k: M(r'\infty', 1.2, OK).move_to(cells[k]) for k in qs}
    res = T('Now proved: every ? is $\\infty$', 0.8, OK).to_edge(DOWN, buff=0.45)
    with self.say('s06_result') as d:
      self.play(FadeOut(guess), FadeOut(longest), boxes.animate.set_color(OK), run_time=0.15 * d)
      self.play(LaggedStart(*[Transform(cells[k], infs[k]) for k in key], lag_ratio=0.3), run_time=0.25 * d)
      self.play(LaggedStart(*[Transform(cells[k], infs[k]) for k in qs if k not in key], lag_ratio=0.1),
                FadeIn(res), run_time=0.3 * d)
    self.wait(0.6)
    self.play(FadeOut(Group(*self.mobjects)), run_time=0.6)


class Rule(NarratedScene):
  def construct(self):
    strip = row(X30[:20], 0.55, 0.02, block=5, block_gap=0.25).move_to(DOWN * 2.3)
    blocks = [strip[5 * i:5 * i + 5] for i in range(4)]
    base = VGroup(*[tile(c, 0.9).move_to([blocks[i].get_center()[0], 2.5, 0]) for i, c in enumerate(W30[:4])])
    more = M(r'\cdots', 1.0).next_to(base, RIGHT, buff=0.3)
    with self.say('s07_idea') as d:
      self.play(LaggedStart(*[FadeIn(t, shift=0.2 * DOWN) for t in base], lag_ratio=0.12), FadeIn(more),
                run_time=0.4 * d)
      self.play(Indicate(base, color=SECONDARY, scale_factor=1.05), run_time=0.2 * d)

    rules = VGroup()
    for k, c in enumerate('abc'):
      lhs = tile(c, 0.6)
      arrow = M(r'\longrightarrow', 0.9, MUTED)
      rhs = row(H2[c], 0.55, 0.03)
      rules.add(VGroup(lhs, arrow, rhs).arrange(RIGHT, buff=0.3))
    rules.arrange(DOWN, buff=0.22, aligned_edge=LEFT).move_to(UP * 0.2)
    with self.say('s07_rule') as d:
      for r in rules:
        self.play(FadeIn(r[0]), GrowFromEdge(r[1], LEFT), LaggedStart(*[FadeIn(t) for t in r[2]], lag_ratio=0.1),
                  run_time=0.25 * d)

    with self.say('s07_grow') as d:
      for i, c in enumerate(W30[:4]):
        src = rules['abc'.index(c)][2].copy()
        self.play(Indicate(base[i], color=SECONDARY), Transform(src, blocks[i]), run_time=0.18 * d)
        self.remove(src)
        self.add(blocks[i])
      self.play(FadeOut(rules), run_time=0.1 * d)

    tern = VGroup()
    for c in 'abc':
      tern.add(VGroup(tile(c, 0.6), M(r'\longrightarrow', 0.9, MUTED), row(H3[c], 0.55, 0.03)).arrange(RIGHT, buff=0.3))
    tern.arrange(DOWN, buff=0.22, aligned_edge=LEFT).move_to(UP * 0.2)
    tlab = T('three-letter version', 0.7, MUTED).next_to(tern, LEFT, buff=0.5)
    with self.say('s07_ternary') as d:
      self.play(FadeIn(tern), FadeIn(tlab), run_time=0.25 * d)
      self.wait(0.4 * d)
      self.play(FadeOut(tern), FadeOut(tlab), run_time=0.15 * d)

    # 111 | 011 at positions 7-12: a shape square with halves of 3 letters (allowed).
    hu = SurroundingRectangle(strip[7:10], color=FIRST_HALF, buff=0.05, stroke_width=4)
    hv = SurroundingRectangle(strip[10:13], color=SECOND_HALF, buff=0.05, stroke_width=4)
    cu = VGroup(*[M(str(v), 0.8, ACCENT).next_to(strip[7 + k], UP, buff=0.2) for k, v in enumerate(pd('111'))])
    cv = VGroup(*[M(str(v), 0.8, ACCENT).next_to(strip[10 + k], UP, buff=0.2) for k, v in enumerate(pd('011'))])
    ok = T('halves of 3: allowed', 0.75, ACCENT).move_to(UP * 0.3)
    claim = T('Claim: no shape square with halves of 4 or more, ever', 0.8, SECONDARY).move_to(DOWN * 0.6)
    with self.say('s07_short') as d:
      self.play(Create(hu), Create(hv), run_time=0.15 * d)
      self.play(Write(cu), Write(cv), run_time=0.2 * d)
      self.play(FadeIn(ok), run_time=0.15 * d)
      self.play(Write(claim), run_time=0.25 * d)
    self.play(FadeOut(Group(*self.mobjects)), run_time=0.6)


class Window(NarratedScene):
  def construct(self):
    strip = row(X30[:20], 0.55, 0.02, block=5, block_gap=0.25).move_to(UP * 2.6)
    win = SurroundingRectangle(strip[0:7], color=SECONDARY, buff=0.07, stroke_width=5, corner_radius=0.06)
    with self.say('s08_window') as d:
      self.play(FadeIn(strip), run_time=0.2 * d)
      self.play(Create(win), run_time=0.15 * d)
      for s in (3, 6, 9):
        self.play(win.animate.become(SurroundingRectangle(strip[s:s + 7], color=SECONDARY, buff=0.07, stroke_width=5,
                                                          corner_radius=0.06)), run_time=0.12 * d)

    # Five-letter windows at positions 5 and 13: 00111 and 00001, same code 0 1 1 1 1.
    w1 = SurroundingRectangle(strip[5:10], color=SECONDARY, buff=0.07, stroke_width=5, corner_radius=0.06)
    w2 = SurroundingRectangle(strip[13:18], color=SECONDARY, buff=0.07, stroke_width=5, corner_radius=0.06)
    p1 = binary_profile(X30[5:10], 0.45, 0.12, unit=0.55, base=0.4).move_to(LEFT * 3.3 + DOWN * 0.2)
    p2 = binary_profile(X30[13:18], 0.45, 0.12, unit=0.55, base=0.4).move_to(RIGHT * 3.3 + DOWN * 0.2)
    p2.align_to(p1, DOWN)
    c1 = code_row(pd(X30[5:10]), [c.get_center()[0] for c in p1[0]], -1.9, 0.8)
    c2 = code_row(pd(X30[13:18]), [c.get_center()[0] for c in p2[0]], -1.9, 0.8)
    eq = M('=', 1.0, OK).move_to([0, -1.9, 0])
    m1 = SurroundingRectangle(p1[1][2], color=WARN, buff=0.08, stroke_width=4)
    m2 = SurroundingRectangle(p2[1][2], color=WARN, buff=0.08, stroke_width=4)
    neq = M(r'\neq', 1.0, WARN).move_to([0, p1[1][2].get_center()[1], 0])
    with self.say('s08_fail5') as d:
      self.play(win.animate.become(w1), run_time=0.12 * d)
      self.play(TransformFromCopy(strip[5:10], p1), run_time=0.15 * d)
      self.play(Create(w2), TransformFromCopy(strip[13:18], p2), run_time=0.15 * d)
      self.play(Write(c1), Write(c2), FadeIn(eq), run_time=0.15 * d)
      self.play(Create(m1), Create(m2), FadeIn(neq), run_time=0.15 * d)
      fail = T('5 letters: not enough', 0.8, WARN).to_edge(DOWN, buff=0.4)
      self.play(FadeIn(fail), run_time=0.1 * d)

    # Seven-letter windows with one shared code: 0010100 and 0010101, both with middle letter 0.
    a, b = '0010100', '0010101'
    q1 = binary_profile(a, 0.42, 0.1, unit=0.55, base=0.4).move_to(LEFT * 3.3 + DOWN * 0.2)
    q2 = binary_profile(b, 0.42, 0.1, unit=0.55, base=0.4).move_to(RIGHT * 3.3 + DOWN * 0.2)
    q2.align_to(q1, DOWN)
    d1 = code_row(pd(a), [c.get_center()[0] for c in q1[0]], -1.9, 0.75)
    d2 = code_row(pd(b), [c.get_center()[0] for c in q2[0]], -1.9, 0.75)
    g1 = SurroundingRectangle(q1[1][3], color=OK, buff=0.08, stroke_width=4)
    g2 = SurroundingRectangle(q2[1][3], color=OK, buff=0.08, stroke_width=4)
    eqm = M('=', 1.0, OK).move_to([0, q1[1][3].get_center()[1], 0])
    s7 = T('7 letters: 23 codes, each with one middle letter', 0.8, OK).to_edge(DOWN, buff=0.4)
    with self.say('s08_seven') as d:
      self.play(FadeOut(VGroup(p1, p2, c1, c2, m1, m2, neq, fail, w2)), win.animate.set_opacity(0), run_time=0.12 * d)
      self.play(FadeIn(q1, shift=0.2 * UP), FadeIn(q2, shift=0.2 * UP), run_time=0.15 * d)
      self.play(Write(d1), Write(d2), run_time=0.15 * d)
      self.play(Create(g1), Create(g2), FadeIn(eqm), run_time=0.15 * d)
      self.play(Write(s7), run_time=0.2 * d)
    self.play(FadeOut(Group(*self.mobjects)), run_time=0.6)


def cell_rows(m=20, size=0.3, y=1.2):
  """Schematic word u v of 2m cells (no letters): first half blue, second half gold."""
  cells = VGroup()
  for i in range(2 * m):
    col = FIRST_HALF if i < m else SECOND_HALF
    sq = Square(size, stroke_color=col, stroke_width=2).set_fill(col, 0.25)
    sq.move_to(RIGHT * (i - (2 * m - 1) / 2) * size + UP * y)
    cells.add(sq)
  return cells


class NearSquare(NarratedScene):
  def construct(self):
    m, size = 20, 0.3
    cells = cell_rows(m, size, 1.0)
    u, v = cells[:m], cells[m:]
    bu = Brace(u, UP, color=FIRST_HALF, buff=0.1)
    bv = Brace(v, UP, color=SECOND_HALF, buff=0.1)
    lu = M('m', 0.9, FIRST_HALF).next_to(bu, UP, buff=0.1)
    lv = M('m', 0.9, SECOND_HALF).next_to(bv, UP, buff=0.1)
    same = T('same code', 0.8, SECONDARY).move_to(DOWN * 0.3)
    note = T('(picture not to scale)', 0.6, MUTED).to_edge(DOWN, buff=0.4)
    with self.say('s09_suppose') as d:
      self.play(LaggedStart(*[FadeIn(c) for c in cells], lag_ratio=0.02), run_time=0.3 * d)
      self.play(GrowFromCenter(bu), GrowFromCenter(bv), FadeIn(lu), FadeIn(lv), FadeIn(same), FadeIn(note),
                run_time=0.25 * d)

    with self.say('s09_slide') as d:
      self.play(FadeOut(same), FadeOut(bv), FadeOut(lv), v.animate.move_to(u.get_center() + DOWN * 0.9),
                run_time=0.18 * d)
      lab_u = T('first half', 0.65, FIRST_HALF).next_to(u, LEFT, buff=0.3)
      lab_v = T('second half', 0.65, SECOND_HALF).next_to(v, LEFT, buff=0.3)
      self.play(FadeOut(bu), FadeOut(lu), run_time=0.05 * d)
      self.play(VGroup(u, v).animate.scale(1.5).move_to(RIGHT * 0.9 + UP * 0.5), run_time=0.08 * d)
      lab_u.next_to(u, LEFT, buff=0.3)
      lab_v.next_to(v, LEFT, buff=0.3)
      self.play(FadeIn(lab_u), FadeIn(lab_v), run_time=0.07 * d)

      def frame(t):
        return SurroundingRectangle(VGroup(u[t - 3:t + 4], v[t - 3:t + 4]), color=SECONDARY, buff=0.06,
                                    stroke_width=5, corner_radius=0.05)

      win = frame(3)
      self.play(Create(win), run_time=0.06 * d)
      steps = list(range(3, m - 3))
      per = 0.55 * d / len(steps)
      for t in steps:
        self.play(win.animate.become(frame(t)), u[t].animate.set_fill(OK, 0.8).set_stroke(OK),
                  v[t].animate.set_fill(OK, 0.8).set_stroke(OK), run_time=per)

    ends = [0, 1, 2, m - 3, m - 2, m - 1]
    eq = T('equal, letter for letter', 0.8, OK).next_to(v, DOWN, buff=0.6)
    with self.say('s09_equal') as d:
      self.play(FadeOut(win), run_time=0.08 * d)
      self.play(*[r[t].animate.set_fill(GREYED, 0.6).set_stroke(GREYED) for r in (u, v) for t in ends],
                run_time=0.15 * d)
      b3l = Brace(v[0:3], DOWN, color=MUTED, buff=0.08)
      b3r = Brace(v[m - 3:m], DOWN, color=MUTED, buff=0.08)
      t3l = M('3', 0.7, MUTED).next_to(b3l, DOWN, buff=0.08)
      t3r = M('3', 0.7, MUTED).next_to(b3r, DOWN, buff=0.08)
      self.play(GrowFromCenter(b3l), GrowFromCenter(b3r), FadeIn(t3l), FadeIn(t3r), run_time=0.15 * d)
      eq.next_to(VGroup(t3l, t3r), DOWN, buff=0.45)
      self.play(Write(eq), run_time=0.2 * d)
    self.play(FadeOut(Group(*self.mobjects)), run_time=0.6)


class Upstairs(NarratedScene):
  def construct(self):
    # Synchronisation: 00101 slid across c a = 01100 00101 fits only at the true boundary.
    pair = row('0110000101', 0.7, 0.05, block=5, block_gap=0.3).move_to(DOWN * 0.4)
    lab_c = T('c', 0.8, MUTED).next_to(pair[:5], DOWN, buff=0.25)
    lab_a = T('a', 0.8, MUTED).next_to(pair[5:], DOWN, buff=0.25)
    probe = row('00101', 0.7, 0.05, stroke=SECONDARY, color=SECONDARY)
    with self.say('s10_sync') as d:
      self.play(FadeIn(pair), FadeIn(lab_c), FadeIn(lab_a), run_time=0.15 * d)
      probe.next_to(pair[0], UP, buff=0.35, aligned_edge=LEFT)
      self.play(FadeIn(probe, shift=DOWN * 0.2), run_time=0.08 * d)
      marks = VGroup()
      for off in range(6):
        target = pair[off:off + 5]
        dx = target[0].get_center()[0] - probe[0].get_center()[0]
        self.play(probe.animate.shift(RIGHT * dx), run_time=0.06 * d)
        good = '0110000101'[off:off + 5] == '00101'
        mk = (tick(0.9) if good else xmark(ORIGIN, 0.14)).next_to(probe, UP, buff=0.15)
        marks.add(mk)
        self.play(FadeIn(mk), run_time=0.06 * d)
      real = T('it only fits where a real block starts', 0.75, OK).to_edge(DOWN, buff=0.5)
      self.play(FadeIn(real), run_time=0.1 * d)

    m, size, p = 20, 0.3, 2
    cells = cell_rows(m, size, 0.9)
    u, v = cells[:m], cells[m:]
    v.move_to(u.get_center() + DOWN * 0.9)
    VGroup(u, v).scale(1.5).move_to(RIGHT * 0.9 + UP * 0.5)
    for r in (u, v):
      for t in range(m):
        if t < 3 or t >= m - 3:
          r[t].set_fill(GREYED, 0.6).set_stroke(GREYED)
        else:
          r[t].set_fill(OK, 0.8).set_stroke(OK)
    lab_u = T('first half', 0.65, FIRST_HALF).next_to(u, LEFT, buff=0.3)
    lab_v = T('second half', 0.65, SECOND_HALF).next_to(v, LEFT, buff=0.3)
    # Block boundaries where (p + t) is a multiple of 5: t = 3, 8, 13, 18.
    starts = [t for t in range(m) if (p + t) % 5 == 0]
    ticks = VGroup()
    for r in (u, v):
      for t in starts:
        x = r[t].get_left()[0]
        ticks.add(Line([x, r.get_top()[1] + 0.12, 0], [x, r.get_bottom()[1] - 0.12, 0], color=INK, stroke_width=3))
    whole = [t for t in starts if t + 5 <= m - 3]
    frames = VGroup(*[SurroundingRectangle(r[t:t + 5], color=ACCENT, buff=0.03, stroke_width=6) for r in (u, v)
                      for t in whole])
    with self.say('s10_align') as d:
      self.play(FadeOut(VGroup(pair, lab_c, lab_a, probe, marks, real)), run_time=0.12 * d)
      self.play(FadeIn(cells), FadeIn(lab_u), FadeIn(lab_v), run_time=0.15 * d)
      self.play(Create(ticks), run_time=0.2 * d)
      self.play(Create(frames), run_time=0.2 * d)
      shiftlab = T('shifted by a whole number of blocks', 0.75, ACCENT).next_to(v, DOWN, buff=0.6)
      self.play(FadeIn(shiftlab), run_time=0.12 * d)

    # Back into one line; read each whole block as a letter of Dejean's word.
    with self.say('s10_up') as d:
      self.play(FadeOut(VGroup(ticks, frames, shiftlab, lab_u, lab_v)), run_time=0.1 * d)
      self.play(VGroup(u, v).animate.scale(1 / 1.5), run_time=0.07 * d)
      self.play(v.animate.next_to(u, RIGHT, buff=0), run_time=0.1 * d)
      self.play(cells.animate.move_to(DOWN * 0.2), run_time=0.1 * d)
      gstarts = [t for t in range(2 * m) if (p + t) % 5 == 0 and t + 5 <= 2 * m]
      letters = 'cabaca' + 'b'
      bl, tl = VGroup(), VGroup()
      for k, t in enumerate(gstarts):
        blk = cells[t:t + 5]
        bl.add(SurroundingRectangle(blk, color=INK, buff=0.02, stroke_width=3))
        tl.add(tile(letters[k], 0.55).next_to(blk, UP, buff=0.55))
      links = VGroup(*[DashedLine(b.get_top(), t.get_bottom(), color=GREYED, stroke_width=2) for b, t in zip(bl, tl)])
      self.play(Create(bl), run_time=0.15 * d)
      self.play(LaggedStart(*[FadeIn(t, shift=0.2 * UP) for t in tl], lag_ratio=0.1), Create(links), run_time=0.2 * d)
      P = m // 5
      arcs = VGroup(*[hop(tl[k + P].get_top() + UP * 0.05, tl[k].get_top() + UP * 0.05, OK, down=False, angle=0.5 * PI)
                      for k in range(2)])
      self.play(Create(arcs), *[tl[k].animate.set_color(OK) for k in (0, 1, P, P + 1)], run_time=0.15 * d)
      rep = T("a stretch of Dejean's word that repeats", 0.75, OK).to_edge(UP, buff=0.4)
      self.play(FadeIn(rep), run_time=0.1 * d)

    lost = M(r'14', 0.9, WARN)
    parts = M(r'= 3 + 3 + 4 + 4', 0.9, MUTED)
    lostg = VGroup(T('letters lost, at most:', 0.8, MUTED), lost, parts).arrange(RIGHT, buff=0.25).move_to(DOWN * 1.6)
    expo = MathTex(r'\text{exponent}', r'\geq', r'2 - \frac{14}{m}').scale(0.95).move_to(DOWN * 2.8)
    with self.say('s10_count') as d:
      self.play(FadeOut(rep), run_time=0.08 * d)
      self.play(FadeIn(lostg), run_time=0.3 * d)
      self.play(Write(expo), run_time=0.3 * d)

    expo2 = MathTex(r'\text{exponent}', r'\geq', r'2 - \frac{14}{m}', r'>', r'2 - \frac{14}{56}', r'=',
                    r'\frac{7}{4}').scale(0.95).move_to(DOWN * 2.8)
    cond = T('when $m$ is bigger than 56:', 0.8, SECONDARY).move_to(DOWN * 1.6)
    contra = T('but Dejean: never above $\\tfrac{7}{4}$. Contradiction.', 0.85, WARN).to_edge(UP, buff=0.4)
    with self.say('s10_contra') as d:
      self.play(FadeOut(lostg), FadeIn(cond), run_time=0.15 * d)
      self.play(TransformMatchingTex(expo, expo2), run_time=0.3 * d)
      self.play(Write(contra), cells.animate.set_stroke(WARN), run_time=0.25 * d)
      self.play(Create(SurroundingRectangle(expo2, color=WARN, buff=0.15)), run_time=0.1 * d)
    self.play(FadeOut(Group(*self.mobjects)), run_time=0.6)


class Finite(NarratedScene):
  def construct(self):
    w24 = dejean(24)
    top = row(w24, 0.45, 0.03).move_to(UP * 2.4)
    x = ''.join(H2[c] for c in w24)
    bar_w = 0.096
    bars = VGroup()
    for i, ch in enumerate(x):
      h = 0.18 if ch == '0' else 0.5
      r = Rectangle(width=bar_w * 0.8, height=h, stroke_width=0, fill_color=PRIMARY, fill_opacity=0.9)
      r.move_to([(i - (len(x) - 1) / 2) * bar_w, 0.7, 0], aligned_edge=DOWN)
      bars.add(r)
    links = VGroup(Line(top.get_corner(DL), bars.get_corner(UL) + UP * 0.55, color=GREYED, stroke_width=2),
                   Line(top.get_corner(DR), bars.get_corner(UR) + UP * 0.55, color=GREYED, stroke_width=2))
    lab = T('halves from 4 to 56 fit inside 24 letters', 0.8, SECONDARY).move_to(DOWN * 0.3)
    with self.say('s11_short') as d:
      self.play(LaggedStart(*[FadeIn(t) for t in top], lag_ratio=0.03), run_time=0.3 * d)
      self.play(Create(links), LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.005), run_time=0.3 * d)
      self.play(FadeIn(lab), run_time=0.15 * d)

    counter = ValueTracker(0)
    num = always_redraw(lambda: Integer(int(counter.get_value()), group_with_commas=True).scale(1.4)
                        .move_to(LEFT * 1.6 + DOWN * 1.4))
    num_lab = T('words checked', 0.75, MUTED).next_to(LEFT * 1.6 + DOWN * 1.4, DOWN, buff=0.55)
    found = VGroup(M('0', 1.4, OK), T('shape squares found', 0.75, MUTED)).arrange(DOWN, buff=0.35)
    found.move_to(RIGHT * 2.6 + DOWN * 1.6)
    with self.say('s11_count') as d:
      self.play(FadeOut(lab), FadeIn(num), FadeIn(num_lab), run_time=0.12 * d)
      self.play(counter.animate.set_value(4596), run_time=0.55 * d, rate_func=linear)
      self.play(FadeIn(found), run_time=0.12 * d)
      self.play(Indicate(found[0], color=OK, scale_factor=1.3), run_time=0.1 * d)

    num.clear_updaters()
    line2 = T('three-letter rule: 3,654 words, halves 3 to 64, 0 found', 0.8, ACCENT).to_edge(DOWN, buff=0.45)
    with self.say('s11_ternary') as d:
      self.play(Write(line2), run_time=0.5 * d)

    prog = VGroup(
      card(VGroup(T('program 1 (C)', 0.75), T('4,596 and 3,654', 0.7, MUTED)).arrange(DOWN, buff=0.15), color=PRIMARY),
      card(VGroup(T('program 2 (Python)', 0.75), T('4,596 and 3,654', 0.7, MUTED)).arrange(DOWN, buff=0.15),
           color=PRIMARY),
    ).arrange(RIGHT, buff=1.2).move_to(UP * 0.6)
    ag = T('agree; broken rules are rejected', 0.8, OK).next_to(prog, DOWN, buff=0.6)
    with self.say('s11_two') as d:
      self.play(FadeOut(VGroup(top, bars, links, num, num_lab, found, line2)), run_time=0.15 * d)
      self.play(FadeIn(prog, shift=0.2 * UP), run_time=0.3 * d)
      self.play(FadeIn(ag), run_time=0.2 * d)
    self.play(FadeOut(Group(*self.mobjects)), run_time=0.6)


class Status(NarratedScene):
  def construct(self):
    def item(mark, text, color):
      return VGroup(mark, T(text, 0.9, color)).arrange(RIGHT, buff=0.35)

    i1 = item(tick(0.9), 'endless part: a written argument', INK)
    i2 = item(tick(0.9), 'short cases: a finite computer check', INK)
    i3 = item(Circle(0.14, color=MUTED, stroke_width=3), 'not checked in a proof assistant (Lean)', MUTED)
    i4 = item(Circle(0.14, color=MUTED, stroke_width=3), 'not yet peer reviewed', MUTED)
    items = VGroup(i1, i2, i3, i4).arrange(DOWN, buff=0.45, aligned_edge=LEFT).move_to(UP * 0.2)
    with self.say('s12_status') as d:
      self.play(FadeIn(i1, shift=0.2 * RIGHT), run_time=0.15 * d)
      self.play(FadeIn(i2, shift=0.2 * RIGHT), run_time=0.15 * d)
      self.play(FadeIn(i3, shift=0.2 * RIGHT), run_time=0.15 * d)
      self.play(FadeIn(i4, shift=0.2 * RIGHT), run_time=0.15 * d)

    scope = T('Completes one table in a 2026 paper', 0.85, INK).move_to(UP * 1.8)
    c1 = VGroup(T('2 letters, halves at least 3:', 0.75, MUTED), M('29', 0.9, PRIMARY)).arrange(RIGHT, buff=0.3)
    c2 = VGroup(T('3 letters, halves at least 2:', 0.75, MUTED), M('9', 0.9, PRIMARY)).arrange(RIGHT, buff=0.3)
    cs = VGroup(c1, c2).arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to(DOWN * 0.1)
    sharp = T('so the 4 and the 3 cannot be lowered', 0.8, SECONDARY).move_to(DOWN * 1.9)
    with self.say('s12_scope') as d:
      self.play(FadeOut(items), run_time=0.12 * d)
      self.play(FadeIn(scope), run_time=0.2 * d)
      self.play(FadeIn(cs), run_time=0.25 * d)
      self.play(FadeIn(sharp), run_time=0.2 * d)
    self.play(FadeOut(Group(*self.mobjects)), run_time=0.6)


class Ending(NarratedScene):
  def construct(self):
    r1 = T('1. Forever: 2 letters with halves $\\geq 4$, 3 letters with halves $\\geq 3$', 0.8)
    r2 = T("2. Build: swap each letter of Dejean's word for a block", 0.8)
    r3 = T('3. Prove: long ones become near-squares; a computer clears short ones', 0.8)
    recap = VGroup(r1, r2, r3).arrange(DOWN, buff=0.5, aligned_edge=LEFT).move_to(UP * 0.2)
    if recap.width > 13:
      recap.scale_to_fit_width(13)
    with self.say('s13_recap') as d:
      self.play(FadeIn(r1, shift=0.2 * UP), run_time=0.12 * d)
      self.wait(0.2 * d)
      self.play(FadeIn(r2, shift=0.2 * UP), run_time=0.12 * d)
      self.wait(0.15 * d)
      self.play(FadeIn(r3, shift=0.2 * UP), run_time=0.12 * d)

    head = T('What we still don\'t know', 0.95, SECONDARY).move_to(UP * 1.4)
    o1 = T('How close to a shape square must an endless word come?', 0.8).move_to(UP * 0.1)
    o2 = T('How rare can shape squares be when they are unavoidable?', 0.8).next_to(o1, DOWN, buff=0.45)
    with self.say('s13_open') as d:
      self.play(FadeOut(recap), run_time=0.12 * d)
      self.play(FadeIn(head), run_time=0.15 * d)
      self.play(FadeIn(o1), run_time=0.15 * d)
      self.play(FadeIn(o2), run_time=0.15 * d)
    self.play(FadeOut(VGroup(head, o1, o2)), run_time=0.6)

    t = T('Infinite words avoiding long Cartesian-tree squares', 0.95).move_to(UP * 1.0)
    org = T('Valyu Research, 2026', 0.8, MUTED).next_to(t, DOWN, buff=0.45)
    path = T(r'\texttt{maths/combinatorics/combinatorics-on-words/}\\\texttt{cartesian-tree-square-free-words}',
             0.6, MUTED).next_to(org, DOWN, buff=0.45)
    voice = T('Narration uses a synthetic voice.', 0.55, MUTED).to_edge(DOWN, buff=0.5)
    self.play(FadeIn(t), FadeIn(org), FadeIn(path), FadeIn(voice), run_time=1.0)
    self.wait(5)
