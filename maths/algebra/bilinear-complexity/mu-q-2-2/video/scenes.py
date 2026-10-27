from manim import *
from vrvideo import *

SCENES = ['ThreeProducts', 'TinyArithmetic', 'ProductGrids', 'SearchSpace', 'OtherFields', 'Convolution', 'Evidence']


def formula(s, pos=ORIGIN, scale=1.05, color=INK):
  return MathTex(s, color=color).scale(scale).move_to(pos)


def grid(values, size=.62, color=PRIMARY):
  cells = VGroup()
  n, m = len(values), len(values[0])
  for i, row in enumerate(values):
    for j, v in enumerate(row):
      cell = Square(size, stroke_color=MUTED, stroke_width=1.5)
      cell.set_fill(color, .8 if v else .03)
      cell.move_to([(j-(m-1)/2)*size, ((n-1)/2-i)*size, 0])
      cells.add(cell)
  return cells


def tokens(n, color=PRIMARY):
  return VGroup(*[Circle(.23, color=color, fill_opacity=.4) for _ in range(n)]).arrange_in_grid(rows=1 if n<=9 else 4, buff=.22)


class Lesson(NarratedScene):
  def clear_frame(self):
    if self.mobjects:
      self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=.6)

  def heading(self, text):
    self.play(FadeIn(title(text, .88)), run_time=.7)


class ThreeProducts(Lesson):
  def construct(self):
    left = VGroup(formula('a_0',[-3,1.4,0]),formula('a_1',[-3,-.3,0]))
    right = VGroup(formula('b_0',[3,1.4,0]),formula('b_1',[3,-.3,0]))
    links = VGroup(*[Line(a.get_center()+RIGHT*.5,b.get_center()+LEFT*.5,color=PRIMARY) for a in left for b in right])
    with self.say('a01'):
      self.play(Write(left),Write(right))
      self.play(LaggedStart(*[Create(l) for l in links],lag_ratio=.4),run_time=3)
      self.heading('Four products. Could three be enough?')
    with self.say('a02'):
      self.clear_frame()
      self.play(Write(formula(r'(2+3x)(4+5x)',UP*2)))
      tiles=VGroup(*[formula(s,scale=1.15,color=c) for s,c in [('8',PRIMARY),('10x',SECONDARY),('12x',SECONDARY),('15x^2',ACCENT)]]).arrange(RIGHT,buff=.8)
      self.play(LaggedStart(*[Write(t) for t in tiles],lag_ratio=.3),run_time=4)
      ans=formula(r'8+22x+15x^2',DOWN*1.9,1.4)
      self.play(TransformFromCopy(tiles,ans),run_time=2)
    with self.say('a03'):
      self.clear_frame()
      outer=Rectangle(width=6,height=3,color=SECONDARY,fill_opacity=.15)
      a=Rectangle(width=2.4,height=4/3,color=PRIMARY,fill_opacity=.55).align_to(outer,UL)
      b=Rectangle(width=3.6,height=5/3,color=ACCENT,fill_opacity=.55).align_to(outer,DR)
      la=formula('8',a.get_center());lb=formula('15',b.get_center())
      self.play(Create(outer),Write(formula('(2+3)(4+5)=45',UP*2.3)))
      self.play(FadeIn(a),FadeIn(b),Write(la),Write(lb))
      self.play(a.animate.set_fill(BACKGROUND,1),b.animate.set_fill(BACKGROUND,1),FadeOut(la),FadeOut(lb),run_time=2)
      self.play(Write(formula('45-8-15=22',DOWN*2.3,1.3,color=SECONDARY)))
    with self.say('a04'):
      self.clear_frame()
      t=tokens(4).shift(UP*.6)
      self.play(Create(t))
      self.play(Transform(t,tokens(3,ACCENT).shift(UP*.6)),run_time=2)
      self.play(Write(formula(r'P_1=8\quad P_2=15\quad P_3=45',DOWN*.8)))
      self.heading('Karatsuba: count input multiplications')
      self.play(FadeIn(caption('Additions and fixed scalar operations are free')))


class TinyArithmetic(Lesson):
  def construct(self):
    with self.say('a05'):
      points=VGroup(Circle(.55,color=PRIMARY).shift(LEFT*1.5),Circle(.55,color=PRIMARY).shift(RIGHT*1.5))
      nums=VGroup(formula('1',LEFT*1.5),formula('1',RIGHT*1.5))
      self.play(Create(points),Write(nums))
      self.play(points.animate.move_to(ORIGIN),nums.animate.move_to(ORIGIN),run_time=2)
      self.play(FadeOut(points),Transform(nums,formula('0',scale=2)),run_time=1)
      self.heading('Arithmetic modulo two')
      self.play(FadeIn(caption('$1+1=0$: duplicate contributions cancel')))
    with self.say('a06'):
      self.clear_frame()
      slots=VGroup(*[Square(1.25,color=PRIMARY) for _ in range(4)]).arrange(RIGHT,buff=.25)
      labels=VGroup(*[formula(s,box.get_center()+UP*1.15,.9) for box,s in zip(slots,['1','x','x^2','x^3'])])
      digits=VGroup(*[formula(s,box.get_center(),1.3) for box,s in zip(slots,['1','0','0','1'])])
      self.play(Create(slots),Write(labels))
      self.play(LaggedStart(*[Write(d) for d in digits],lag_ratio=.3),run_time=3)
      self.play(FadeIn(caption('$1+x^3$: four polynomial coefficients')))
    with self.say('a07'):
      self.clear_frame()
      eq=formula(r'{{x^3}}\cdot{{x}}={{x^4}}',scale=1.6)
      self.play(Write(eq))
      self.wait(2)
      self.play(TransformMatchingTex(eq,formula(r'{{x^4}}={{1}}+{{x^2}}',scale=1.6)),run_time=2)
      self.play(FadeIn(caption('Fixed reduction rule: $x^4=x^2+1$')))
    with self.say('a08'):
      self.clear_frame()
      g=grid([[1]*4 for _ in range(4)],.7).shift(LEFT*3.4)
      self.play(Create(g),Write(formula('16',LEFT*3.4+DOWN*2)))
      nested=VGroup(*[tokens(3,ACCENT) for _ in range(3)]).arrange(DOWN,buff=.65).shift(RIGHT*2.5)
      self.play(LaggedStart(*[Create(r) for r in nested],lag_ratio=.3),run_time=3)
      self.play(Write(formula(r'3\times3=9',RIGHT*2.5+DOWN*2)))
      self.heading('Apply the three-product trick twice')
    with self.say('a09'):
      self.clear_frame()
      self.play(Create(tokens(9,ACCENT).shift(UP*.8)))
      self.play(Create(tokens(8,SECONDARY).shift(DOWN*.8)))
      self.heading('Nine suffice. Can eight ever work?')


class ProductGrids(Lesson):
  def construct(self):
    with self.say('a10'):
      g=grid([[0]*4 for _ in range(4)],.85)
      rows=VGroup(*[formula('a_'+str(i),g[i*4].get_center()+LEFT*.9,.8) for i in range(4)])
      cols=VGroup(*[formula('b_'+str(j),g[j].get_center()+UP*.85,.8) for j in range(4)])
      self.play(Create(g),Write(rows),Write(cols))
      for i in [0,2]: self.play(rows[i].animate.set_color(SECONDARY),run_time=.5)
      for j in [1,3]: self.play(cols[j].animate.set_color(ACCENT),run_time=.5)
      self.play(*[g[4*i+j].animate.set_fill(PRIMARY,.85) for i in [0,2] for j in [1,3]],run_time=2)
      self.play(FadeIn(caption('$(a_0+a_2)(b_1+b_3)$')))
    with self.say('a11'):
      self.play(Indicate(rows),Indicate(cols),run_time=2)
      self.heading(r'15 row choices $\times$ 15 column choices = 225')
    with self.say('a12'):
      self.clear_frame()
      vals1=[[1,1],[0,0]]; vals2=[[0,1],[0,1]]
      g1=grid(vals1,1).shift(LEFT*4);g2=grid(vals2,1,color=ACCENT);result=grid([[1,0],[0,1]],1,color=SECONDARY).shift(RIGHT*4)
      self.play(Create(g1),Create(g2),Write(formula('+',LEFT*2)))
      self.play(TransformFromCopy(VGroup(g1,g2),result),Write(formula('=',RIGHT*2)),run_time=3)
      self.play(Indicate(g1[1]),Indicate(g2[1]),run_time=2)
      self.play(FadeIn(caption('Add grids square by square; the overlap cancels')))
    with self.say('a13'):
      self.clear_frame()
      const=[[1,0,0,0],[0,0,0,1],[0,0,1,0],[0,1,0,1]]
      g=grid([[0]*4 for _ in range(4)],.85)
      self.play(Create(g))
      for i,row in enumerate(const):
        for j,v in enumerate(row):
          if v:self.play(g[4*i+j].animate.set_fill(PRIMARY,.85),run_time=.35)
      self.heading('Target: the constant coefficient')
      self.play(FadeIn(caption('Each square represents one $a_i b_j$ product')))
    with self.say('a14'):
      self.clear_frame()
      targets=[const,[[0,1,0,0],[1,0,0,0],[0,0,0,1],[0,0,1,0]],[[0,0,1,0],[0,1,0,1],[1,0,1,0],[0,1,0,0]],[[0,0,0,1],[0,0,1,0],[0,1,0,1],[1,0,1,0]]]
      gs=VGroup(*[grid(v,.52) for v in targets]).arrange(RIGHT,buff=.65).shift(UP*.7)
      product=grid([[0,1,0,1],[0,0,0,0],[0,1,0,1],[0,0,0,0]],.37,color=SECONDARY).shift(DOWN*1.8)
      self.play(Create(gs),Create(product),run_time=2)
      self.play(*[Create(Arrow(product.get_top(),t.get_bottom(),buff=.15,color=SECONDARY)) for t in gs],run_time=2)
      self.play(FadeIn(caption('Reuse products across the four outputs')))


class SearchSpace(Lesson):
  def construct(self):
    with self.say('a15'):
      gs=VGroup(*[grid(v,.7) for v in [[[0,0],[0,0]],[[1,0],[0,0]],[[0,0],[0,1]],[[1,0],[0,1]]]]).arrange(RIGHT,buff=1)
      self.play(LaggedStart(*[Create(g) for g in gs],lag_ratio=.45),run_time=4)
      self.heading('Span: every sum you can make')
      self.play(FadeIn(caption(r'$0,\ A,\ B,\ A+B$')))
    with self.say('a16'):
      self.clear_frame()
      box=RoundedRectangle(width=10.8,height=4.1,color=MUTED)
      targets=VGroup(*[Square(.9,color=PRIMARY,fill_opacity=.45) for _ in range(4)]).arrange(RIGHT,buff=.65).shift(UP*.7)
      self.play(Create(box),LaggedStart(*[Create(t) for t in targets],lag_ratio=.3),run_time=3)
      self.heading('A schematic span, not a physical room')
      self.play(FadeIn(caption('Four independent target directions')))
    with self.say('a17'):
      extra=VGroup(*[Square(.9,color=SECONDARY,fill_opacity=.4) for _ in range(4)]).arrange(RIGHT,buff=.65).shift(DOWN*.8)
      self.play(LaggedStart(*[Create(t) for t in extra],lag_ratio=.4),run_time=3)
      self.play(Indicate(VGroup(targets,extra),color=ACCENT),run_time=2)
      self.play(FadeIn(Tex('Eight directions; must be generated by product grids',color=ACCENT).scale(.7).shift(UP*2.55)))
    with self.say('a18'):
      self.clear_frame()
      boxes=VGroup(*[Rectangle(width=1.2,height=.85,color=PRIMARY) for _ in range(12)]).arrange_in_grid(rows=3,cols=4,buff=.35)
      self.play(LaggedStart(*[Create(b) for b in boxes],lag_ratio=.1),run_time=2)
      self.play(LaggedStart(*[Create(Cross(b,color=WARN)) for b in boxes],lag_ratio=.13),run_time=3)
      self.heading('103,406,616 eligible four-sets: zero successes')
      self.play(FadeIn(caption('Separate symmetry search: 74,377 prefixes')))
    with self.say('a19'):
      self.clear_frame()
      self.play(Write(formula(r'\text{exhaustive exclusion: }r>8',UP*.9)),run_time=2)
      self.play(Write(formula(r'\text{construction: }r\le9',DOWN*.4)),run_time=2)
      self.play(Write(formula('r=9',DOWN*1.9,1.5,ACCENT)),run_time=2)
      self.heading('Completeness turns a search into a proof')


class OtherFields(Lesson):
  def construct(self):
    with self.say('a20'):
      dial=Circle(1.5,color=PRIMARY)
      labels=VGroup(*[formula(str(i),1.9*np.array([np.cos(PI/2-i*TAU/3),np.sin(PI/2-i*TAU/3),0]),1.25) for i in range(3)])
      arrow=Arrow(ORIGIN,UP*1.3,buff=0,color=SECONDARY)
      self.play(Create(dial),Write(labels),Create(arrow))
      self.play(Rotate(arrow,-4*TAU/3,about_point=ORIGIN),run_time=3)
      self.play(FadeIn(caption('Modulo three: $2+2=1$')))
    with self.say('a21'):
      self.clear_frame()
      self.play(Create(tokens(8,ACCENT).shift(UP)))
      self.play(Write(formula(r'(f_0+f_2)(g_0+g_2)',DOWN*.5,1.3)))
      self.play(FadeIn(caption('One of the eight actual products; same combination on both sides')))
      self.heading('Symmetric recipe')
    with self.say('a22'):
      self.clear_frame()
      g=grid([[0]*4 for _ in range(4)],.8)
      self.play(Create(g))
      for i in range(4):
        self.play(*[g[4*i+j].animate.set_fill(ACCENT,.7) for j in range(4)],run_time=1)
      self.heading('Check all 16 pairs of basis monomials')
      self.play(FadeIn(caption(r'$1,\ x,\ x^2,\ x^3$ generate every input')))
    with self.say('a23'):
      self.clear_frame()
      tracks=VGroup(*[Rectangle(width=4.5,height=1.2,color=PRIMARY).move_to([0,y,0]) for y in [1,-.6]])
      self.play(Create(tracks))
      self.play(Write(formula('73{,}000',tracks[0].get_center())),Write(formula('73{,}000',tracks[1].get_center())))
      self.heading('$q=5$: two exact checkers, no rank-seven recipe')
      self.play(FadeIn(caption('Each: 17,417,506 residual buckets; positive controls pass',color=ACCENT)))
    with self.say('a24'):
      self.clear_frame()
      top=VGroup(*[formula(s,scale=1.15) for s in ['q=2','3','4','5',r'\ge7']]).arrange(RIGHT,buff=1.1).shift(UP*.7)
      bottom=VGroup(*[formula(s,[m.get_x(),-.7,0],1.5,ACCENT) for m,s in zip(top,['9','8','8','8','7'])])
      self.play(Write(top))
      self.play(LaggedStart(*[Write(b) for b in bottom],lag_ratio=.3),run_time=3)
      self.heading('Unrestricted and symmetric costs agree')
      self.play(FadeIn(caption(r'$q$ is a prime power; $\mathbb F_4$ is not arithmetic mod 4')))


class Convolution(Lesson):
  def construct(self):
    pts=[2*np.array([np.cos(PI/2-i*TAU/6),np.sin(PI/2-i*TAU/6),0]) for i in range(6)]
    with self.say('a25'):
      ring=Circle(2,color=MUTED)
      nodes=VGroup(*[Circle(.3,color=PRIMARY).move_to(p) for p in pts])
      labels=VGroup(*[formula(str(i),p*1.3,.8) for i,p in enumerate(pts)])
      self.play(Create(ring),Create(nodes),Write(labels))
      dot=Dot(pts[0],color=SECONDARY,radius=.15)
      self.add(dot)
      for p in pts[1:]+pts[:1]: self.play(dot.animate.move_to(p),run_time=.45)
      self.play(FadeIn(caption('Positions wrap after six: $x^6=1$')))
    with self.say('a26'):
      self.play(FadeOut(dot))
      bits=VGroup(*[Dot(pts[i],radius=.14,color=SECONDARY) for i in [0,1,5]])
      self.play(FadeIn(bits))
      duplicate=Dot(pts[5],radius=.14,color=ACCENT)
      self.add(duplicate)
      self.play(duplicate.animate.move_to(pts[0]),run_time=2)
      self.play(FadeOut(duplicate),FadeOut(bits[0]),run_time=1)
      self.heading('$(1+x^5)(1+x)=1+x+x^5+x^6$')
    with self.say('a27'):
      self.clear_frame()
      small=VGroup(*[Square(.8,color=PRIMARY,fill_opacity=.2) for _ in range(2)]).arrange(RIGHT).shift(LEFT*3)
      large=VGroup(*[Square(.8,color=ACCENT,fill_opacity=.2) for _ in range(4)]).arrange(RIGHT).shift(RIGHT*2.3)
      self.play(Create(small),Create(large),run_time=2)
      self.play(Write(formula('3',small.get_center()+DOWN*1.5,1.8,PRIMARY)),Write(formula('9',large.get_center()+DOWN*1.5,1.8,ACCENT)))
      self.heading('Split into two arithmetic components')
    with self.say('a28'):
      self.clear_frame()
      self.play(Write(formula('3+9=12',scale=2,color=ACCENT)),run_time=3)
      self.heading("Ja'Ja'--Takche: a special additivity theorem")
      self.play(FadeIn(caption(r'One component has format $2\times2\times2$')))


class Evidence(Lesson):
  def construct(self):
    with self.say('a29'):
      a=grid([[1,0],[0,0]],1).shift(LEFT*2.5)
      b=grid([[1,0],[0,0]],1).shift(RIGHT*2.5)
      self.play(Create(a),Create(b))
      self.heading('Symmetric binary value 9: Rambaud, 2014')
      self.play(Transform(b,grid([[0,1],[0,0]],1,color=SECONDARY).shift(RIGHT*2.5)),run_time=2)
      self.play(FadeIn(caption('This binary lower bound also allows asymmetric recipes')))
    with self.say('a30'):
      self.clear_frame()
      self.play(Write(Tex('Subspace methods: BDEZ, Covanov, Rambaud').scale(.85).shift(UP*.8)))
      self.play(Write(Tex('Prior survey claim for $q=4$').scale(.85).shift(DOWN*.5)))
      self.play(FadeIn(caption('Surviving contributions: unrestricted $q=2$, explicit $q=3$, $C_6$')))
    with self.say('a31'):
      self.clear_frame()
      dots=VGroup(*[Circle(.22,color=ACCENT,fill_opacity=.6) for _ in range(12)]).arrange_in_grid(rows=2,cols=6,buff=.45)
      self.play(LaggedStart(*[Create(d) for d in dots],lag_ratio=.12),run_time=3)
      self.heading('12 compiled checks passed')
      self.play(FadeIn(caption('Large logical proof archived outside repo; no Lean claim')))
    with self.say('a32'):
      self.clear_frame()
      self.play(Create(tokens(3).shift(LEFT*4)),Create(grid([[1,0],[0,1]],.8)),Write(formula('9',RIGHT*4,2,ACCENT)),run_time=3)
      self.wait(3)
      self.clear_frame()
      end=VGroup(Tex(r'The bilinear complexity of $\mathbb F_{q^2}[u]/(u^2)$').scale(.82),Tex(r'and length-six cyclic convolution over $\mathbb F_2$').scale(.78),Tex('Valyu Research, 2026').scale(.8),Tex(r'\texttt{maths/algebra/bilinear-complexity/mu-q-2-2}').scale(.55),Tex('Narration uses a synthetic voice.',color=MUTED).scale(.65)).arrange(DOWN,buff=.38)
      self.play(FadeIn(end),run_time=1)
