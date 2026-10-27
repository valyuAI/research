"""A robust chemical switch, built from reactions to the obstruction proof."""
import json
from pathlib import Path

from manim import *
from vrvideo import *

SCENES = ['OneReaction', 'Robustness', 'ThreeRestingStates', 'TwoDimensions', 'OppositeSlopes', 'BendingRule', 'SharpSizes', 'Evidence']


def label(text, position=ORIGIN, scale=.8, color=INK):
  return Tex(text, color=color).scale(scale).move_to(position)


def formula(text, position=ORIGIN, scale=1., color=INK):
  return MathTex(text, color=color).scale(scale).move_to(position)


def molecule(name, position, color=PRIMARY):
  circle = Circle(.42, color=color, fill_color=color, fill_opacity=.16).move_to(position)
  return VGroup(circle, label(name, position, .85, color))


def mixture(values, center, scale=1.):
  group = VGroup()
  for i, (name, value, color) in enumerate(zip('ABC', values, [PRIMARY, ACCENT, WARM])):
    x = center[0] + (i - 1) * 1.05 * scale
    h = value * .36 * scale
    base = center[1] - 1.15 * scale
    bar = Rectangle(width=.65 * scale, height=h, fill_color=color, fill_opacity=.65, stroke_color=color).move_to([x, base + h / 2, 0])
    group.add(VGroup(bar, label(name, [x, base - .35 * scale, 0], .8 * scale, color), formula(str(value), [x, base + h + .35 * scale, 0], .85 * scale)))
  return group


def network():
  positions = {'C': [-4.2, 1.3, 0], 'A+C': [-.3, 1.3, 0], 'A': [3.5, 1.3, 0],
               'B+C': [-4.2, -1.4, 0], 'B': [-.3, -1.4, 0], '2B': [3.5, -1.4, 0]}
  nodes = {k: formula(k, p, 1.05) for k, p in positions.items()}
  edges = [('C', 'A+C', '1', -.13), ('A+C', 'C', '1', -.13), ('A', 'A+C', '6', 0),
           ('B', '2B', '11', -.13), ('2B', 'B', '1', -.13), ('C', 'B+C', '6', -.13),
           ('B+C', 'C', '6', -.13), ('B+C', 'B', '1', 0)]
  arrows, rates = VGroup(), VGroup()
  for a, b, rate, shift in edges:
    p, q = np.array(positions[a], dtype=float), np.array(positions[b], dtype=float)
    vec = q - p
    unit = vec / np.linalg.norm(vec)
    normal = np.array([-unit[1], unit[0], 0])
    start_gap = abs(unit[0]) * nodes[a].width / 2 + abs(unit[1]) * nodes[a].height / 2 + .18
    end_gap = abs(unit[0]) * nodes[b].width / 2 + abs(unit[1]) * nodes[b].height / 2 + .18
    arr = Arrow(p + normal * shift + unit * start_gap, q + normal * shift - unit * end_gap, buff=0, color=MUTED, stroke_width=2.5, max_tip_length_to_length_ratio=.08)
    arrows.add(arr)
    rates.add(formula(rate, (p + q) / 2 + normal * (shift - .25), .65, SECONDARY))
  return VGroup(*nodes.values()), arrows, rates


class TeachingScene(NarratedScene):
  pause_after = .55

  def clear_board(self):
    self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=.6)

  def note(self, text, color=INK):
    if hasattr(self, '_note') and self._note in self.mobjects:
      self.play(FadeOut(self._note), run_time=.25)
    self._note = caption(text, .78, color)
    self.play(FadeIn(self._note), run_time=.5)


class OneReaction(TeachingScene):
  def construct(self):
    left, right = mixture((1, 2, 3), [-3.3, 0, 0]), mixture((1, 6, 1), [3.3, 0, 0])
    with self.say('a01'):
      self.play(LaggedStart(FadeIn(left), FadeIn(right), lag_ratio=.4), run_time=3)
      self.play(Indicate(left[0]), Indicate(right[0]), run_time=2)
      self.note('Different mixtures. The same resting value of A.')
    with self.say('a02'):
      self.play(Write(title('Can a chemical network be robust and bistable?', .72)))
      self.play(Circumscribe(left[0], color=PRIMARY), Circumscribe(right[0], color=PRIMARY), run_time=2)
    with self.say('a03'):
      self.clear_board()
      a, b = molecule('A', [-3, .6, 0]), molecule('B', [-1.8, .6, 0], ACCENT)
      out1, out2 = molecule('B', [2, .6, 0], ACCENT), molecule('B', [3.2, .6, 0], ACCENT)
      self.play(FadeIn(a), FadeIn(b))
      self.play(GrowArrow(Arrow(LEFT*.6+UP*.6, RIGHT*.9+UP*.6, color=SECONDARY)))
      self.play(TransformFromCopy(a, out1), TransformFromCopy(b, out2), run_time=2.5)
      self.note(r'Teaching reaction: $A+B\longrightarrow2B$')
      self.play(Write(formula(r'\Delta A=-1,\qquad\Delta B=+1', DOWN*1.4, 1.1)))
    with self.say('a04'):
      self.clear_board()
      eq = formula(r'\text{rate}=k\,a\,b', UP*.7, 1.3)
      self.play(Write(eq), run_time=2)
      self.play(TransformMatchingTex(eq, formula(r'\text{rate}=2\times3\times4=24', UP*.7, 1.3)), run_time=3)
      self.note('More reactant concentration means more encounters.')
    with self.say('a05'):
      self.play(Write(formula(r'\dot a=-24,\qquad\dot b=+24', DOWN*.8, 1.15)), run_time=2)
      self.note('At rest: every net rate of change is zero.')


class Robustness(TeachingScene):
  def construct(self):
    with self.say('a06'):
      rx = formula(r'C\ \mathop{\rightleftarrows}^{1}_{1}\ A+C', UP*1.4, 1.35)
      self.play(Write(rx), run_time=2.5)
      gain = formula(r'+c', LEFT*2.2+DOWN*.5, 1.4, ACCENT)
      loss = formula(r'-ac', RIGHT*2.2+DOWN*.5, 1.4, WARN)
      self.play(FadeIn(gain), run_time=1)
      self.play(FadeIn(loss), run_time=1)
      self.note('Rate of A production minus rate of A removal')
    with self.say('a07'):
      self.clear_board()
      eq = formula(r'\dot a=c-ac', UP*1.5, 1.4)
      self.play(Write(eq))
      target = formula(r'\dot a=c(1-a)', UP*1.5, 1.4)
      self.play(TransformMatchingTex(eq, target), run_time=2)
      axis = NumberLine(x_range=[0, 2, .5], length=8, include_numbers=True).shift(DOWN*.4)
      self.play(Create(axis))
      self.play(GrowArrow(Arrow(axis.n2p(.25)+UP*.5, axis.n2p(.9)+UP*.5, color=ACCENT)), GrowArrow(Arrow(axis.n2p(1.8)+UP*.5, axis.n2p(1.1)+UP*.5, color=ACCENT)))
      self.play(FadeIn(Dot(axis.n2p(1), color=PRIMARY, radius=.12)))
      self.note(r'$c>0$ and $\dot a=0$ force $a=1$.', ACCENT)
    with self.say('a08'):
      self.play(Write(title('Absolute concentration robustness (ACR)', .8)))
      self.note('Same A at every positive steady state. A can change in time.')
    with self.say('a09'):
      self.clear_board()
      nodes, arrows, rates = network()
      self.play(FadeIn(nodes), run_time=1.5)
      self.play(LaggedStart(*[GrowArrow(x) for x in arrows], lag_ratio=.2), run_time=4)
      self.play(FadeIn(rates))
      self.play(Write(title('6 complexes, 8 reactions', .9)))
      self.note('At most 2 molecules on BOTH sides of every arrow')
    with self.say('a10'):
      self.clear_board()
      axes = Axes(x_range=[-2, 2, 1], y_range=[-1, 2, 1], x_length=4.4, y_length=2.6, tips=False).shift(LEFT*3)
      axes2 = axes.copy().shift(RIGHT*6)
      valley = axes.plot(lambda x: .55*x*x, x_range=[-1.6, 1.6], color=ACCENT)
      hill = axes2.plot(lambda x: 1.4-.55*x*x, x_range=[-1.6, 1.6], color=WARN)
      ball1, ball2 = Dot(axes.c2p(-1.2, .55*1.2**2), color=SECONDARY), Dot(axes2.c2p(.15, 1.4-.55*.15**2), color=SECONDARY)
      self.play(Create(valley), Create(hill), FadeIn(ball1), FadeIn(ball2))
      self.play(ball1.animate.move_to(axes.c2p(0, 0)), ball2.animate.move_to(axes2.c2p(1.5, 1.4-.55*1.5**2)), run_time=3)
      self.play(Write(label('Returns', [-3, -1.7, 0], .95, ACCENT)), Write(label('Escapes', [3, -1.7, 0], .95, WARN)))
      self.note('A stability analogy: response to a small disturbance')


class ThreeRestingStates(TeachingScene):
  def construct(self):
    with self.say('a11'):
      eq = formula(r'a=1,\qquad\dot c=6a-bc', UP*.7, 1.25)
      self.play(Write(eq), run_time=2)
      eq2 = formula(r'0=6-bc\quad\Longrightarrow\quad c=\frac6b', DOWN*.8, 1.2)
      self.play(Write(eq2), run_time=3)
      self.note('Positive resting states: $a,b,c>0$')
    with self.say('a12'):
      self.clear_board()
      eq = formula(r'\dot b=11b-b^2-6bc+6c', UP*1.35, 1.1)
      self.play(Write(eq))
      sub = formula(r'b\dot b=11b^2-b^3-36b+36', ORIGIN, 1.05)
      self.play(TransformFromCopy(eq, sub), run_time=2.5)
      factor = formula(r'b\dot b=-(b-2)(b-3)(b-6)', DOWN*1.35, 1.15, SECONDARY)
      self.play(TransformMatchingTex(sub.copy(), factor), run_time=3)
      self.note('Only after substituting $a=1$ and $c=6/b$')
    with self.say('a13'):
      self.clear_board()
      rows = VGroup(*[formula(s, scale=1.25, color=c) for s,c in [(r'b=2\ \Rightarrow\ (1,2,3)', ACCENT), (r'b=3\ \Rightarrow\ (1,3,2)', WARM), (r'b=6\ \Rightarrow\ (1,6,1)', ACCENT)]]).arrange(DOWN, buff=.65)
      self.play(LaggedStart(*[Write(row) for row in rows], lag_ratio=.6), run_time=5)
      self.note('Exactly three positive steady states')
    with self.say('a14'):
      self.clear_board()
      ax = Axes(x_range=[.8, 7, 1], y_range=[-5, 5, 2], x_length=10, y_length=4.2, tips=False).shift(DOWN*.05)
      curve = ax.plot(lambda b: -(b-2)*(b-3)*(b-6)/b, x_range=[1.45, 7], color=PRIMARY)
      self.play(Create(ax), Create(curve), run_time=3)
      for b in [2, 3, 6]:
        self.play(FadeIn(Dot(ax.c2p(b, 0), color=SECONDARY)), Write(formula(str(b), ax.c2p(b, 0)+DOWN*.4, .8)), run_time=.7)
      self.play(Write(title('Restricted to $a=1$ and $c=6/b$', .84)))
      self.note('Zeros locate equilibria. This curve is not a flow trajectory.')
    with self.say('a15'):
      self.clear_board()
      data = json.loads((Path(__file__).parent/'trajectory-data.json').read_text())
      ax = Axes(x_range=[1.5, 6.5, 1], y_range=[.7, 3.5, 1], x_length=8.5, y_length=4.2, tips=False)
      self.play(Create(ax), Write(label('$b$', [4.8, -1.8, 0], .85)), Write(label('$c$', [-4.6, 2, 0], .85)))
      for values, col in zip(data['paths'], [PRIMARY, ACCENT]):
        path = VMobject(color=col, stroke_width=4).set_points_as_corners([ax.c2p(p[1], p[2]) for p in values])
        dot = Dot(path.get_start(), color=col, radius=.09)
        self.play(FadeIn(dot))
        self.play(Create(path), MoveAlongPath(dot, path), run_time=2.5, rate_func=linear)
      for b,c,col in [(2,3,ACCENT),(3,2,WARN),(6,1,ACCENT)]:
        self.play(FadeIn(Dot(ax.c2p(b,c), color=col, radius=.11)), run_time=.4)
      self.play(Write(title('Two illustrative trajectories, both with $a=1$', .75)))
      self.note('Outer states: stable. Middle state: unstable. Checked exactly.')


class TwoDimensions(TeachingScene):
  def construct(self):
    with self.say('a16'):
      tri = Polygon([-4,-1.7,0], [3.7,-1.7,0], [0,2.3,0], color=PRIMARY, fill_opacity=.15)
      dot = Dot([-1, -.3, 0], color=SECONDARY)
      self.play(Create(tri), FadeIn(dot), run_time=2)
      self.play(dot.animate.shift(RIGHT*2), run_time=2)
      self.play(dot.animate.shift(UP*.9+LEFT*.7), run_time=2)
      self.play(Write(formula(r'a+b+c=2', DOWN*2.5, 1.2)))
      self.play(Write(title('One fixed total leaves two free amounts', .85)))
    with self.say('a17'):
      self.clear_board()
      self.play(Write(formula(r'A+B\longrightarrow2C\longrightarrow2B,\qquad C\longrightarrow A', UP*1.5, .95)), run_time=3)
      self.play(Write(formula(r'(a,b,c)=(1,\tfrac12,\tfrac12)', LEFT*3+DOWN*.3, .95, WARN)))
      self.play(Write(formula(r'(a,b,c)=(\tfrac12,1,\tfrac12)', RIGHT*3+DOWN*.3, .95, ACCENT)))
      self.play(Write(label('Saddle', [-3,-1.4,0], .85, WARN)), Write(label('Stable', [3,-1.4,0], .85, ACCENT)))
      self.note('Known example: all rates 1; total 2; robust C = $1/2$')
    with self.say('a18'):
      self.clear_board()
      for x, d, color in [(-3,2,WARM),(3,3,ACCENT)]:
        arrows = VGroup(Arrow([x-1,-1,0],[x+1,-1,0], color=color), Arrow([x-1,-1,0],[x-1,1,0], color=color))
        if d == 3:
          arrows.add(Arrow([x-1,-1,0],[x+.3,.3,0], color=color))
        self.play(Create(arrows), Write(label(f'{d} independent directions', [x,1.8,0], .8)), run_time=2)
      self.note('Both have 3 species. Only the right-hand example is full dimensional.')
    with self.say('a19'):
      self.clear_board()
      self.play(Write(title('The two-dimensional obstruction', .9)))
      self.play(Write(formula(r'\text{2 distinct positive nondegenerate equilibria}', UP*.9, .85)), run_time=2)
      self.play(Write(formula(r'\text{in one class}+\text{ACR}\ \Longrightarrow\ \text{one unstable}', DOWN*.4, .9)), run_time=3)
      self.note('At most bimolecular on both reactant and product sides')
    with self.say('a20'):
      self.clear_board()
      sheet = Rectangle(width=9, height=4.5, color=MUTED, fill_opacity=.06)
      line = Line(LEFT*4.3, RIGHT*4.3, color=PRIMARY, stroke_width=5)
      self.play(Create(sheet))
      self.play(Create(line), run_time=2)
      self.play(FadeIn(Dot(LEFT*2, color=SECONDARY)), FadeIn(Dot(RIGHT*2, color=SECONDARY)))
      self.play(Write(label('$L$: robust concentration fixed', [0,1.7,0], .9, PRIMARY)))
      self.note('Schematic coordinates within one stoichiometric class')


class OppositeSlopes(TeachingScene):
  def construct(self):
    with self.say('a21'):
      ax = Axes(x_range=[-3,3,1], y_range=[-2,3,1], x_length=9, y_length=4, tips=False).shift(DOWN*.2)
      curve = ax.plot(lambda x: .7*(x*x-2.25), x_range=[-2.5,2.5], color=PRIMARY)
      self.play(Create(ax), Create(curve), run_time=3)
      roots = VGroup(*[Dot(ax.c2p(x,0), color=SECONDARY, radius=.1) for x in [-1.5,1.5]])
      self.play(FadeIn(roots), Write(title(r'On $L$: roots of one quadratic $\gamma$', .85)))
      self.note('Schematic quadratic: two simple roots, no third root')
    with self.say('a22'):
      for x in [-1.5,1.5]:
        tangent = Line(ax.c2p(x-.5, -.5*1.4*x), ax.c2p(x+.5, .5*1.4*x), color=SECONDARY, stroke_width=5)
        self.play(Create(tangent), run_time=1.5)
      self.play(Write(formula(r'\gamma\prime(p)<0,\qquad\gamma\prime(p\prime)>0', DOWN*2.7, .95)))
      self.note('The slopes have opposite signs.')
    with self.say('a23'):
      self.clear_board()
      center = Dot(LEFT*3, color=WARN, radius=.13)
      self.play(FadeIn(center))
      arrows = VGroup(Arrow([-3.2,0,0],[-4.6,0,0],color=WARN), Arrow([-2.8,0,0],[-1.4,0,0],color=WARN), Arrow([-3,1.5,0],[-3,.25,0],color=ACCENT), Arrow([-3,-1.5,0],[-3,-.25,0],color=ACCENT))
      self.play(LaggedStart(*[GrowArrow(a) for a in arrows],lag_ratio=.3),run_time=3)
      self.play(Write(formula(r'\det=-\ell\,\gamma\prime', RIGHT*2.2+UP*.4,1.3)))
      self.play(Write(label('Negative determinant: saddle', [2.2,-.8,0], .77, WARN)))
      self.note('Local response inside the sheet, near a resting state')
    with self.say('a24'):
      self.clear_board()
      columns = VGroup(*[VGroup(label(t,scale=.9),formula(s,scale=1.3,color=c)).arrange(DOWN,buff=.7) for t,s,c in [('Slopes',r'-\quad+',PRIMARY),(r'Same-sign $\ell$',r'+\quad+',WARM),('Determinants',r'+\quad-',WARN)]]).arrange(RIGHT,buff=1.3)
      self.play(LaggedStart(*[FadeIn(x) for x in columns],lag_ratio=.5),run_time=4)
      self.note('Opposite determinant signs force one saddle.')
    with self.say('a25'):
      self.clear_board()
      horizontal = Line(LEFT*4.4, RIGHT*4.4, color=PRIMARY, stroke_width=4)
      zero = Line([-2,-2.2,0],[2,2.2,0],color=SECONDARY,stroke_width=4)
      self.play(Create(horizontal), FadeIn(Dot(LEFT*2.8,color=PRIMARY)), FadeIn(Dot(RIGHT*2.8,color=PRIMARY)))
      self.play(Create(zero),run_time=2)
      self.play(Write(label(r'$\ell=0$', [2.8,2.1,0], .85, SECONDARY)), Write(label('$L$',[4.8,0,0],.9,PRIMARY)))
      self.note(r'Remaining possibility: $\ell$ changes sign across the gap.')


class BendingRule(TeachingScene):
  def construct(self):
    with self.say('a26'):
      self.play(Write(formula(r'f_1(x_1,x\prime)=P(x\prime)+x_1M(x\prime)+c_{11}x_1^2',UP*.8,.95)),run_time=3)
      self.play(Write(formula(r'P(x\prime)\ge0,\qquad c_{11}\le0',DOWN*.7,1.2,color=SECONDARY)),run_time=2)
      self.note('No consumption from zero. No more than two molecules produced.')
    with self.say('a27'):
      self.clear_board()
      ax = Axes(x_range=[0,5,1],y_range=[-4,2,1],x_length=9,y_length=4.4,tips=False).shift(UP*.1)
      curve = ax.plot(lambda x: 1.1+.5*x-.3*x*x,x_range=[0,4.8],color=PRIMARY)
      self.play(Create(ax), Create(curve),run_time=3)
      point = Dot(ax.c2p(0,1.1),color=SECONDARY,radius=.1)
      self.play(FadeIn(point))
      self.play(MoveAlongPath(point,curve),run_time=4,rate_func=linear)
      self.play(Write(title('Fix every other concentration',.85)))
      self.note('After becoming negative, the rate stays negative to the right.')
    with self.say('a28'):
      p = ax.c2p(3.5,1.1+.5*3.5-.3*3.5**2)
      q = ax.c2p(4.5,1.1+.5*4.5-.3*4.5**2)
      self.play(FadeIn(Dot(p,color=WARN)),Create(DashedLine(ax.c2p(3.5,0),p,color=WARN)))
      self.play(GrowArrow(Arrow(p,q,color=WARN,buff=.1)),run_time=2)
      self.play(Write(formula(r'\text{required }>0\qquad\text{forced }<0',UP*2.8,.9,color=WARN)))
      self.note('One representative sign case: the two requirements clash.', WARN)
    with self.say('a29'):
      self.clear_board()
      self.play(Write(formula(r'\dim S=2\quad\Longrightarrow\quad\text{no ACR multistability}',UP*.5,1.05,color=ACCENT)),run_time=3)
      self.play(Write(label('Full proof: all sign cases and exceptional geometry', [0,-1,0], .85)))
      self.note('The animation shows the proof mechanism, not every case.')


class SharpSizes(TeachingScene):
  def construct(self):
    with self.say('a30'):
      nodes, arrows, rates = network()
      self.play(FadeIn(nodes),Create(arrows),FadeIn(rates),run_time=3)
      self.play(Write(title('Dimension 3 and 6 complexes are attained',.8)))
      self.note('Separate deficiency-one argument excludes 5 complexes.')
    with self.say('a31'):
      self.clear_board()
      switch = RoundedRectangle(width=4.5,height=2.3,corner_radius=.15,color=ACCENT).shift(LEFT*3)
      self.play(Create(switch),Write(label('Two-species switch',[-3,.5,0],.8,ACCENT)))
      self.play(Write(formula(r'X\quad Y',[-3,-.5,0],1.3,ACCENT)))
      self.play(Write(formula(r'0\ \mathop{\rightleftarrows}^{1}_{1}\ Z',[3,.3,0],1.2,PRIMARY)))
      self.play(Write(formula(r'\dot z=1-z',[3,-.8,0],1.,PRIMARY)))
      self.note('Independent pieces: 2 species + 1 species = 3 species')
    with self.say('a32'):
      self.clear_board()
      nodes, arrows, rates = network()
      self.play(FadeIn(nodes),Create(arrows),FadeIn(rates),run_time=2)
      self.play(Indicate(nodes[0],color=SECONDARY),Indicate(nodes[1],color=SECONDARY),Indicate(nodes[3],color=SECONDARY),run_time=2)
      self.note('The running witness is coupled; the simple union is not.')
    with self.say('a33'):
      self.clear_board()
      rows = VGroup(*[VGroup(label(name,scale=.88),formula(values,scale=1.15,color=color)).arrange(RIGHT,buff=1) for name,values,color in [('Dimension',r'2\ \longrightarrow\ 3',ACCENT),('Complexes',r'5\ \longrightarrow\ 6',ACCENT),('Species',r'3\ \longrightarrow\ 3',PRIMARY)]]).arrange(DOWN,aligned_edge=LEFT,buff=.65)
      self.play(LaggedStart(*[Write(row) for row in rows],lag_ratio=.5),run_time=4)
      self.play(Write(title(r'Resting states $\longrightarrow$ stable resting states',.75)))
      self.note('Prior question: Kaihnsa, Nguyen and Shiu (2024). Reactant minimum open.')


class Evidence(TeachingScene):
  def construct(self):
    with self.say('a34'):
      start = formula(r'\text{reactions}', LEFT*4,1)
      middle = formula(r'\text{equations}',ORIGIN,1)
      end = formula(r'\text{exact checks}',RIGHT*4,1,color=ACCENT)
      self.play(Write(start))
      self.play(GrowArrow(Arrow(LEFT*2.8,LEFT*1.5,color=SECONDARY)),Write(middle))
      self.play(GrowArrow(Arrow(RIGHT*1.5,RIGHT*2.8,color=SECONDARY)),Write(end))
      self.note('Two independent implementations; exact equilibrium and stability checks')
    with self.say('a35'):
      self.clear_board()
      self.play(Write(title('Formal proof scope',.95)))
      self.play(Write(label('Lean: vector fields, positive equilibria, ACR', [0,.6,0], .92, ACCENT)),run_time=2)
      self.play(Write(label('Stability and minima: outside that formalisation', [0,-.7,0], .88, WARM)),run_time=2)
    with self.say('a36'):
      self.clear_board()
      items = VGroup(*[label(t,scale=.95,color=c) for t,c in [('ACR: same output at positive rest',PRIMARY),('Multistability: two stable states in one class',ACCENT),('Minima: dimension 3, complexes 6, species 3',WARM)]]).arrange(DOWN,buff=.65)
      self.play(LaggedStart(*[FadeIn(m) for m in items],lag_ratio=.7),run_time=4)
    with self.say('a37'):
      self.clear_board()
      self.play(Write(label('Absolute concentration robustness with multistability',[0,1.6,0],.8)))
      self.play(Write(label('Minimal dimension and minimal number of complexes',[0,.8,0],.78)))
      self.play(Write(label('Valyu Research, 2026',[0,-.1,0],.85,PRIMARY)))
      self.play(Write(label('chemistry/reaction-networks/mass-action/',[0,-1,0],.61,MUTED)))
      self.play(Write(label('acr-multistability-bounds',[0,-1.5,0],.68,MUTED)))
      self.play(Write(label('Narration uses a synthetic voice.',[0,-2.5,0],.67,MUTED)))
