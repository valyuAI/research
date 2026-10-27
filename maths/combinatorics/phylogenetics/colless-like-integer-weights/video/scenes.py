from manim import *
from vrvideo import *
import math

SCENES = ['Trees', 'Weights', 'FalseZero', 'Recipes', 'Counting', 'Boxes', 'Crossing', 'Scope']


def label(text, point, scale=0.75, color=INK):
  return Tex(text, color=color).scale(scale).move_to(point)


def tree(word, center=ORIGIN, width=4.4, height=2.7, color=PRIMARY):
  levels = [[np.array([0., height / 2, 0.])]]
  count = 1
  for depth, degree in enumerate(word, 1):
    count *= degree
    levels.append([np.array([width * ((i + 0.5) / count - 0.5), height / 2 - height * depth / len(word), 0.]) for i in range(count)])
  edges, dots = VGroup(), VGroup()
  for depth, degree in enumerate(word):
    for i, pos in enumerate(levels[depth]):
      for j in range(degree):
        edges.add(Line(pos, levels[depth + 1][i * degree + j], color=color, stroke_width=2.5))
  for depth, positions in enumerate(levels):
    for pos in positions:
      dots.add(Dot(pos, radius=0.065 if len(positions) < 15 else 0.035, color=ACCENT if depth == len(word) else color))
  return VGroup(edges, dots).shift(center)


def recipes():
  import itertools
  return VGroup(*[MathTex(','.join(map(str, p))).scale(0.9) for p in itertools.permutations([2, 3, 4])]).arrange_in_grid(rows=2, cols=3, buff=(1.4, 0.7))


class Trees(NarratedScene):
  def construct(self):
    a = tree([2, 2], LEFT * 3.3)
    b = tree([6], RIGHT * 3.3)
    with self.say('c01'):
      self.play(Create(a), Create(b), run_time=2)
      self.play(FadeIn(caption('Different shapes. Can a score tell?')), run_time=1)
    with self.say('c02'):
      root = label('root', [-3.3, 2.1, 0])
      leaf = label('leaves', [-3.3, -2.0, 0], color=ACCENT)
      self.play(FadeIn(root), FadeIn(leaf))
      self.play(Indicate(a[1][0], color=SECONDARY), run_time=1.5)
      self.play(Indicate(VGroup(*a[1][-4:]), color=SECONDARY), run_time=1.5)
    with self.say('c03'):
      self.play(FadeOut(root), FadeOut(leaf))
      self.play(Indicate(a[0][2:4]), Indicate(a[0][4:6]), run_time=2)
      self.play(FadeIn(title('Same children at every fork', 0.85)))


class Weights(NarratedScene):
  def construct(self):
    a, b = tree([2, 2], LEFT * 3.3 + UP * 0.2), tree([6], RIGHT * 3.3 + UP * 0.2)
    self.add(a, b)
    rule = MathTex('f(n)=n+1').scale(1.05).to_edge(UP, buff=0.45)
    nums_a = VGroup(*[MathTex(str(3 if i < 3 else 1), color=SECONDARY).scale(0.7).next_to(d, UP, buff=0.1) for i, d in enumerate(a[1])])
    nums_b = VGroup(*[MathTex(str(7 if i == 0 else 1), color=SECONDARY).scale(0.7).next_to(d, UP, buff=0.1) for i, d in enumerate(b[1])])
    with self.say('c04'):
      self.play(Write(rule))
      self.play(LaggedStart(*[FadeIn(x) for x in nums_a], lag_ratio=0.15), FadeIn(nums_b), run_time=3)
    with self.say('c05'):
      sum_a = MathTex('3+2\\cdot3+4\\cdot1=13').scale(0.85).move_to([-3.3, -2.4, 0])
      self.play(Write(sum_a), run_time=3)
      self.play(Indicate(sum_a, color=ACCENT))
    with self.say('c06'):
      sum_b = MathTex('7+6\\cdot1=13').scale(0.85).move_to([3.3, -2.4, 0])
      self.play(Write(sum_b), run_time=2)
      self.play(FadeIn(caption('A collision: two shapes, one size', color=ACCENT)))


class FalseZero(NarratedScene):
  def construct(self):
    a, b = tree([2, 2], LEFT * 3.0 + DOWN * 0.6, width=3.8, height=2.2), tree([6], RIGHT * 3.0 + DOWN * 0.6, width=3.8, height=2.2)
    self.add(a, b)
    top = Dot([0, 2.35, 0], color=SECONDARY)
    joins = VGroup(Line(top.get_center(), a[1][0].get_center()), Line(top.get_center(), b[1][0].get_center()))
    sizes = VGroup(label('13', [-2.2, 1.3, 0], 1, ACCENT), label('13', [2.2, 1.3, 0], 1, ACCENT))
    with self.say('c07'):
      self.play(Create(joins), FadeIn(top), run_time=2)
      self.play(FadeIn(sizes))
      self.play(FadeIn(label('equal sizes', [0, 3.1, 0], 0.85)))
    with self.say('c08'):
      zeros = VGroup(*[MathTex('0', color=ACCENT).scale(0.8).next_to(d, LEFT, buff=0.15) for d in [a[1][0], a[1][1], a[1][2], b[1][0], top]])
      self.play(LaggedStart(*[FadeIn(z) for z in zeros], lag_ratio=0.25), run_time=3)
      self.play(FadeIn(caption('Score 0, but not fully symmetric', color=WARN)))
    with self.say('c09'):
      self.play(Indicate(joins, color=WARN), run_time=2)
    with self.say('c10'):
      self.play(*[FadeOut(m) for m in list(self.mobjects)])
      self.play(Write(title('Could better whole-number weights work?', 0.8)))
      weights = MathTex('3,7\\quad\\longrightarrow\\quad 100,999,\\ldots').scale(1.2)
      self.play(Write(weights), run_time=2)
      self.play(FadeIn(caption('No. Counting eventually forces a collision.', color=WARN)))


class Recipes(NarratedScene):
  def construct(self):
    a = tree([2, 3], width=6, height=3)
    word = MathTex('(2,3)').scale(1.15).to_edge(UP)
    with self.say('c11'):
      self.play(Create(a), Write(word), run_time=2)
      result = caption('$2\\times3=6$ leaves')
      self.play(FadeIn(result))
    with self.say('c12'):
      self.play(Transform(a, tree([3, 2], width=6, height=3)), Transform(word, MathTex('(3,2)').scale(1.15).to_edge(UP)), run_time=3)
      self.play(Transform(result, caption('$3\\times2=6$ leaves')))
    with self.say('c13'):
      self.play(FadeOut(a), FadeOut(word), FadeOut(result))
      r = recipes().shift(UP * 0.3)
      self.play(LaggedStart(*[Write(x) for x in r], lag_ratio=0.15), run_time=3)
      leaf_caption = caption('$2\\times3\\times4=24$ leaves, every time')
      self.play(Write(leaf_caption))
    with self.say('c14'):
      self.play(FadeOut(r))
      six = MathTex('2,2,3,3,4,4').scale(1.2).shift(UP)
      n = MathTex('90\\text{ recipes}').scale(1.1).shift(DOWN * 0.5)
      self.play(Write(six), Write(n), run_time=2)
      self.play(Transform(leaf_caption, caption('$24^2=576$ leaves, every time')))
      self.play(FadeIn(title('$m$ copies of each: $24^m$ leaves', 0.85)))


class Counting(NarratedScene):
  def construct(self):
    count = MathTex('N_m=',r'\frac{(3m)!}{m!\,m!\,m!}').scale(1.35).shift(UP * 0.8)
    with self.say('c15'):
      self.play(Write(count[0]), Write(count[1]), run_time=3)
      self.play(FadeIn(caption('$m=2:\\quad 6!/(2!\\,2!\\,2!)=720/8=90$')))
    with self.say('c16'):
      self.play(*[FadeOut(x) for x in list(self.mobjects)])
      all_strings = MathTex('3^{3m}=27^m').scale(1.3).shift(UP * 1.8)
      bars = VGroup(*[Rectangle(width=0.38, height=h, color=PRIMARY, fill_opacity=0.65).move_to([i * .5 - 2.5, -1.2 + h / 2, 0]) for i, h in enumerate([.25,.4,.7,1,1.5,2.1,1.5,1,.7,.4,.25])])
      bars[5].set_color(SECONDARY)
      self.play(Write(all_strings), LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars]), run_time=3)
      self.play(FadeIn(caption('Grouped by symbol counts (schematic)')))
    with self.say('c17'):
      self.play(FadeOut(bars))
      lower = MathTex(r'N_m\geq\frac{27^m}{\binom{3m+2}{2}}').scale(1.25).shift(DOWN * 0.4)
      self.play(Write(lower), run_time=3)
      self.play(Indicate(lower, color=SECONDARY))


class Boxes(NarratedScene):
  def construct(self):
    eq1 = MathTex('S_1=I_1+', '24^m f(0)').scale(1.05).shift(UP * 1.2)
    eq2 = MathTex('S_2=I_2+', '24^m f(0)').scale(1.05).shift(DOWN * 0.2)
    with self.say('c18'):
      self.play(Write(eq1), Write(eq2), run_time=2)
      self.play(eq1[1].animate.set_color(ACCENT), eq2[1].animate.set_color(ACCENT))
      self.play(Create(Cross(eq1[1], stroke_color=SECONDARY)), Create(Cross(eq2[1], stroke_color=SECONDARY)))
      self.play(FadeIn(caption('The same leaf contribution cancels')))
    with self.say('c19'):
      self.play(*[FadeOut(m) for m in list(self.mobjects)])
      self.play(Write(title('$M=\\max\\{f(2),f(3),f(4)\\}$', 0.9)))
      a = tree([2, 2, 2], width=7, height=3.6)
      self.play(Create(a), run_time=2)
    with self.say('c20'):
      counts = VGroup(*[MathTex(str(n), color=SECONDARY if n < 8 else ACCENT).scale(0.85).move_to([4.5, y, 0]) for n, y in zip([1,2,4,8], [1.8,.6,-.6,-1.8])])
      self.play(LaggedStart(*[Write(n) for n in counts], lag_ratio=0.3), run_time=3)
      self.play(FadeIn(caption('$1+2+4<8$; the same bound holds at every depth')))
    with self.say('c21'):
      self.play(*[FadeOut(m) for m in list(self.mobjects)])
      numberline = NumberLine(x_range=[0, 6, 1], length=10, include_numbers=False, color=MUTED)
      self.play(Create(numberline), run_time=2)
      labels = VGroup(MathTex('0').scale(.9).next_to(numberline.n2p(0), DOWN), MathTex('M24^m').scale(.9).next_to(numberline.n2p(6), DOWN))
      self.play(Write(labels), Write(title('Integer sums: at most $M24^m+1$ boxes', .85)))
    with self.say('c22'):
      self.play(*[FadeOut(m) for m in list(self.mobjects)])
      boxes = VGroup(*[Square(1.4, color=MUTED).move_to([x,-.7,0]) for x in [-3,0,3]])
      tokens = VGroup(*[Dot([x,1.7,0], radius=.16, color=PRIMARY) for x in [-3,-1,1,3]])
      self.play(Create(boxes), FadeIn(tokens))
      self.play(*[tokens[i].animate.move_to(boxes[i].get_center()) for i in range(3)], run_time=2)
      self.play(tokens[3].animate.move_to(boxes[1].get_center()+RIGHT*.35).set_color(SECONDARY), run_time=1.5)
      self.play(FadeIn(caption('More objects than boxes forces a collision')))


class Crossing(NarratedScene):
  def construct(self):
    axes = Axes(x_range=[0, 80, 20], y_range=[-3, 2, 1], x_length=9.5, y_length=4.7, axis_config={'include_tip': False, 'color': MUTED}).shift(UP*.1)
    def logratio(m):
      return (math.lgamma(3*m+1)-3*math.lgamma(m+1)-math.log(5*24**m+1))/math.log(10)
    points = [axes.c2p(m,logratio(m)) for m in range(1,81) if -3 <= logratio(m) <= 2]
    curve = VMobject(color=PRIMARY).set_points_as_corners(points)
    one = Line(axes.c2p(0,0),axes.c2p(80,0),color=ACCENT,stroke_width=2)
    with self.say('c23'):
      self.play(Create(axes), Create(one), run_time=1)
      self.play(Write(title('Exact recipes / possible boxes, $M=5$', .8)))
      ticks = VGroup(*[MathTex(t).scale(.6).next_to(axes.c2p(0,y),LEFT,buff=.15) for y,t in [(-3,'0.001'),(-2,'0.01'),(-1,'0.1'),(0,'1'),(1,'10'),(2,'100')]])
      xticks = VGroup(*[MathTex(str(m)).scale(.65).move_to(axes.c2p(m,-3)+DOWN*.3) for m in [20,40,60,80]])
      self.play(FadeIn(ticks),FadeIn(xticks),Create(curve),run_time=4)
      self.play(FadeIn(caption('Logarithmic ratio scale; horizontal axis: $m$')))
    with self.say('c24'):
      crossing = next(m for m in range(1,100) if logratio(m)>0)
      dot = Dot(axes.c2p(crossing,logratio(crossing)),color=SECONDARY,radius=.1)
      self.play(FadeIn(dot), FadeIn(label('More recipes than boxes', [1,2.0,0], .7, SECONDARY)))
      self.play(Indicate(dot), run_time=2)
    with self.say('c25'):
      self.play(*[FadeOut(m) for m in list(self.mobjects)])
      a, b = tree([2,2], LEFT*3+DOWN*.7,width=3.8,height=2.1), tree([6],RIGHT*3+DOWN*.7,width=3.8,height=2.1)
      self.play(Create(a),Create(b),run_time=1.5)
      top = np.array([0.,2.3,0.])
      self.play(Create(VGroup(Line(top,a[1][0].get_center()),Line(top,b[1][0].get_center()))), FadeIn(Dot(top,color=SECONDARY)))
      self.play(FadeIn(title('Collision $\\Rightarrow$ false zero', .9)), FadeIn(caption('Return to our illustrative 13-versus-13 example')))


class Scope(NarratedScene):
  def construct(self):
    with self.say('c26'):
      self.play(Write(title('The precise theorem', .9)))
      unit = MathTex(r'f(2),f(3),f(4)\in\gamma\mathbb Z,\quad\gamma>0').scale(1.05)
      self.play(Write(unit),run_time=3)
      self.play(FadeIn(caption('All weights nonnegative; one common unit')))
    with self.say('c27'):
      self.play(Transform(unit,MathTex(r'24^m f(0)-24^m f(0)=0').scale(1.1)))
      self.play(Indicate(unit,color=ACCENT))
    with self.say('c28'):
      self.play(*[FadeOut(m) for m in list(self.mobjects)])
      self.play(Write(title('2018 conjecture; prior collisions credited', .78)))
      prior = MathTex(r'f(n)=2^n:\quad (2,3)\ne(3,2),\quad 26=26').scale(.9)
      self.play(Write(prior), run_time=2)
      self.play(FadeIn(caption('Mir, Rotger and Rossell\'o: earlier example')))
    with self.say('c29'):
      self.play(*[FadeOut(m) for m in list(self.mobjects)])
      grid = VGroup(*[Dot([i*.6-2.1,j*.6-1.2,0],radius=.045,color=PRIMARY) for i in range(8) for j in range(5)])
      self.play(Create(grid),Write(title('Two units: $a+b\\sqrt{2}$', .9)),run_time=2)
      self.play(FadeIn(caption('This argument does not settle the rank-two case',color=SECONDARY)))
    with self.say('c30'):
      self.play(*[FadeOut(m) for m in list(self.mobjects)])
      recap=VGroup(Tex('Same size'),MathTex(r'\Downarrow'),Tex('False zero'),MathTex(r'\Downarrow'),Tex('Counting forces failure')).arrange(DOWN,buff=.25).scale(.85)
      self.play(LaggedStart(*[FadeIn(x) for x in recap],lag_ratio=.25),run_time=3)
      self.play(FadeIn(caption('Correctness: high. Originality: moderate.',.75)))
    with self.say('c31'):
      self.play(*[FadeOut(m) for m in list(self.mobjects)])
      end=VGroup(Tex('Integer weights never give a sound'),Tex('Colless-like balance index'),Tex('Valyu Research, 2026',color=ACCENT),Tex(r'\texttt{maths/combinatorics/phylogenetics/}'),Tex(r'\texttt{colless-like-integer-weights/}'),Tex('Narration uses a synthetic voice.',color=MUTED)).arrange(DOWN,buff=.35)
      for i,x in enumerate(end): x.scale(.85 if i<3 else .58)
      self.play(FadeIn(end),run_time=2)
