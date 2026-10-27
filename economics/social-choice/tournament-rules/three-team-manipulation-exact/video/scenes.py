from manim import *
from vrvideo import *
from pathlib import Path
import json
import itertools

SCENES = ['Matches', 'Cheat', 'Unavoidable', 'Search', 'Constraints', 'Certificate', 'GoodRules', 'Scope']
ROOT = Path(__file__).resolve().parent


def lab(text, pos=ORIGIN, scale=.8, color=INK):
  return Tex(text, color=color).scale(scale).move_to(pos)


def eq(text, pos=ORIGIN, scale=1., color=INK):
  return MathTex(text, color=color).scale(scale).move_to(pos)


def circle_tournament(n=5, bits=None, radius=2., center=ORIGIN, labels=True):
  pts = [center+radius*np.array([np.cos(PI/2-TAU*i/n), np.sin(PI/2-TAU*i/n), 0]) for i in range(n)]
  arcs = {}
  for k,(i,j) in enumerate(itertools.combinations(range(n),2)):
    a,b = ((i,j) if bits[k]=='1' else (j,i)) if bits is not None else ((i,j) if (j-i)%n<=n//2 else (j,i))
    arcs[a,b] = Arrow(pts[a], pts[b], buff=.23 if labels else .1, stroke_width=2.3, max_tip_length_to_length_ratio=.09, color=PRIMARY)
  dots = VGroup(*[Dot(p, radius=.16 if labels else .07, color=PRIMARY) for p in pts])
  names = VGroup(*[lab(chr(65+i),center+(p-center)*1.2,.9) for i,p in enumerate(pts)]) if labels else VGroup()
  return VGroup(VGroup(*arcs.values()),dots,names), arcs, pts


def probability_bar(value, y=-1.5, color=ACCENT, width=7.):
  track=Rectangle(width=width,height=.48,stroke_color=MUTED).move_to([0,y,0])
  fill=Rectangle(width=max(.001,value*width),height=.48,stroke_width=0,fill_color=color,fill_opacity=.8).align_to(track,LEFT).set_y(y)
  return VGroup(track,fill)


class Lesson(NarratedScene):
  def source(self,text):
    new=lab(text,[0,-3.55,0],.5,MUTED)
    if new.width>12.8:new.scale_to_fit_width(12.8)
    if hasattr(self,'src') and self.src in self.mobjects:self.play(Transform(self.src,new),run_time=.35)
    else:self.src=new;self.add(new)

  def cap(self,text,color=INK):
    new=lab(text,[0,-2.8,0],.8,color)
    if new.width>12.5:new.scale_to_fit_width(12.5)
    if hasattr(self,'cp') and self.cp in self.mobjects:self.play(Transform(self.cp,new),run_time=.6)
    else:self.cp=new;self.play(FadeIn(new),run_time=.6)

  def clear(self):
    self.play(*[FadeOut(m) for m in list(self.mobjects)],run_time=.6)


class Matches(Lesson):
  def construct(self):
    g,arcs,pts=circle_tournament(radius=1.8)
    with self.say('s01'):
      self.play(FadeIn(g[1]),Write(g[2]),run_time=1.5)
      self.play(LaggedStart(*[GrowArrow(a) for a in arcs.values()],lag_ratio=.12),run_time=3)
      self.cap('How much can three teams gain?')
      self.source('Paper, Sections 1--2: fairness and coalition gain')
    with self.say('s02'):
      self.clear()
      a=Dot(LEFT*2,radius=.16,color=PRIMARY);b=Dot(RIGHT*2,radius=.16,color=PRIMARY)
      arrow=Arrow(a,b,buff=.25,color=SECONDARY)
      self.play(FadeIn(a),FadeIn(b),Write(lab('A',LEFT*2+UP*.6)),Write(lab('B',RIGHT*2+UP*.6)))
      self.play(GrowArrow(arrow),run_time=2)
      self.cap('Winner $\\longrightarrow$ loser')
      self.wait(2)
      self.clear();self.play(Create(g),run_time=2)
      self.source('Paper, Section 1: one winner per pair')
    with self.say('s03'):
      self.play(g.animate.scale(.65).shift(UP*.7),run_time=1)
      segments=VGroup(*[Rectangle(width=1.25,height=.55,fill_color=PRIMARY if i%2==0 else ACCENT,fill_opacity=.8,stroke_width=1).move_to([(i-2)*1.25,-1.5,0]) for i in range(5)])
      labels=VGroup(*[eq(r'\frac15',s.get_center()+DOWN*.65,.75) for s in segments])
      self.play(LaggedStart(*[GrowFromEdge(s,LEFT) for s in segments],lag_ratio=.3),run_time=3)
      self.play(Write(labels));self.cap('Five chances add to $1$')
      self.source('Compact five-team certificate: regular tournament lottery')
    with self.say('s04'):
      self.clear();g,arcs,pts=circle_tournament(bits='1111111111',radius=1.8)
      self.play(Create(g),run_time=2)
      self.play(*[arcs[0,j].animate.set_color(SECONDARY) for j in range(1,5)],g[1][0].animate.set_color(SECONDARY),run_time=2)
      self.cap('Unbeaten $\\Longrightarrow$ champion with probability $1$')
      self.source('Condorcet consistency: paper, Section 1')


class Cheat(Lesson):
  def construct(self):
    g,arcs,pts=circle_tournament(center=LEFT*2.2,radius=1.8)
    with self.say('s05'):
      self.play(Create(g),run_time=2);self.cap('Every team has two wins and two losses')
      self.play(arcs[0,1].animate.set_color(SECONDARY),arcs[0,2].animate.set_color(SECONDARY),run_time=2)
      self.source('SSW 2017 lower-bound tournament; paper, Section 2')
    with self.say('s06'):
      self.play(*[g[1][i].animate.set_color(SECONDARY) for i in [0,3,4]],run_time=1)
      self.play(*[a.animate.set_opacity(.2) for (i,j),a in arcs.items() if not ({i,j}<={0,3,4})],run_time=1)
      p=eq(r'\frac15+\frac15+\frac15=\frac35',RIGHT*3.1,.9)
      self.play(Write(p),run_time=2);self.cap('Only matches within $\\{A,D,E\\}$ can change')
    with self.say('s07'):
      for j in [3,4]:
        a=arcs[j,0];new=Arrow(pts[0],pts[j],buff=.23,color=SECONDARY,stroke_width=4)
        self.play(Transform(a,new),run_time=2)
      self.play(g[1][0].animate.scale(1.5).set_color(WARM),run_time=1)
      self.play(Transform(p,eq('1',RIGHT*3.1,2,ACCENT)),run_time=2)
      self.cap('A now beats everybody',ACCENT)
    with self.say('s08'):
      self.clear();bar=probability_bar(.6,y=.3)
      self.play(Create(bar[0]),GrowFromEdge(bar[1],LEFT),run_time=2)
      self.play(Write(eq(r'\frac35',[0,1.2,0],1.3)))
      extra=Rectangle(width=2.8,height=.48,fill_color=SECONDARY,fill_opacity=.8,stroke_width=0).move_to([2.1,.3,0])
      self.play(GrowFromEdge(extra,LEFT),run_time=3)
      self.play(Write(eq(r'1-\frac35=\frac25',[0,-1.1,0],1.5)),run_time=2)
      self.cap('Gain: 40 percentage points for the group')
      self.source('Exact regular-class calculation: compact five-team certificate')


class Unavoidable(Lesson):
  def construct(self):
    groups=[[0,3,4],[1,4,0],[2,0,1],[3,1,2],[4,2,3]]
    g,arcs,pts=circle_tournament(radius=1.8)
    with self.say('s09'):
      self.play(Create(g),run_time=2)
      for group in groups:
        self.play(*[g[1][i].animate.set_color(SECONDARY if i in group else PRIMARY) for i in range(5)],run_time=.7)
        self.wait(.45)
      self.cap('Every team has a coalition that can make it unbeaten')
      self.source('Schneider, Schvartzman and Weinberg (2017), Theorem 3.2')
    with self.say('s10'):
      self.clear()
      heads=VGroup(*[lab(chr(65+i),[(i-2)*1.5,2.1,0],.9) for i in range(5)])
      marks=VGroup(*[Dot([(i-2)*1.5,1.2-row*.65,0],radius=.12,color=PRIMARY if i in group else MUTED).set_opacity(1 if i in group else .13) for row,group in enumerate(groups) for i in range(5)])
      self.play(Write(heads),LaggedStart(*[FadeIn(m) for m in marks],lag_ratio=.04),run_time=3)
      self.play(*[marks[5*r].animate.set_color(SECONDARY) for r in [0,1,2]],run_time=1)
      self.cap('Each probability appears in exactly three groups')
      self.source('Five separate possible cheats, not simultaneous match changes')
    with self.say('s11'):
      self.clear()
      first=eq(r'3(p_A+p_B+p_C+p_D+p_E)=3',[0,.8,0],1.1)
      second=eq(r'5-3=2',[0,-.9,0],1.6)
      self.play(Write(first),run_time=3);self.wait(2);self.play(Write(second),run_time=3)
      self.cap('Five gains add to two');self.source('Paper, Section 2: averaging proof for any fair lottery')
    with self.say('s12'):
      self.clear()
      bars=VGroup(*[Rectangle(width=.7,height=1.6,fill_color=PRIMARY,fill_opacity=.7).move_to([(i-2)*1.5,-.3,0]) for i in range(5)])
      line=DashedLine([-4,.5,0],[4,.5,0],color=SECONDARY)
      self.play(LaggedStart(*[GrowFromEdge(b,DOWN) for b in bars],lag_ratio=.2),run_time=3)
      self.play(Create(line),Write(eq(r'\text{average gain}=\frac25',[0,1.7,0],1.15)),run_time=2)
      self.cap('At least one gain reaches the average',ACCENT)
      self.source('Schematic equal-gain picture; SSW 2017 lower bound applies to all lotteries')


class Search(Lesson):
  def construct(self):
    with self.say('s13'):
      line=NumberLine(x_range=[0,1,.2],length=9,include_numbers=True,decimal_number_config={'num_decimal_places':1}).shift(DOWN*.3)
      self.play(Create(line));self.play(GrowArrow(Arrow(line.n2p(.1)+UP,line.n2p(.4)+UP,color=ACCENT,buff=0)),run_time=2)
      self.play(Write(lab('unavoidable',[0,2,0],.9,ACCENT)))
      self.cap('Can we also guarantee no more than $2/5$?')
      self.source('Exact optimum needs a lower bound and an achieving rule')
    with self.say('s14'):
      self.clear();g,_,pts=circle_tournament(radius=1.8)
      self.play(Create(g),run_time=2)
      self.play(*[g[2][i].animate.move_to(pts[(i+1)%5]*1.2) for i in range(5)],run_time=3)
      self.cap('Same shape, different team names');self.source('Paper, symmetrization lemma: averaging over all names')
    with self.say('s15'):
      self.clear()
      data=json.loads((ROOT.parent/'verification/certificates/rule_n5_k3_mt_small.json').read_text())
      thumbnails=VGroup(*[circle_tournament(bits=c['T'],radius=.55,center=np.array([(i%4-1.5)*2.5,(1-i//4)*1.5,0]),labels=False)[0] for i,c in enumerate(data['classes'])])
      self.play(LaggedStart(*[Create(t) for t in thumbnails],lag_ratio=.12),run_time=4)
      self.cap('12 actual shapes, one exact lottery each');self.source('Certificate: rule\_n5\_k3\_mt\_small.json')
    with self.say('s16'):
      self.clear();g,_,_=circle_tournament(bits='1011111011',radius=1.5,center=LEFT*3.5)
      self.play(Create(g),run_time=2)
      vals=[.4,.3,.2,.1,0];strings=[r'\frac25',r'\frac3{10}',r'\frac15',r'\frac1{10}','0']
      bars=VGroup(*[Rectangle(width=.55,height=max(.02,v*5),color=PRIMARY,fill_opacity=.7).move_to([.4+i,-1+v*2.5,0]) for i,v in enumerate(vals)])
      labels=VGroup(*[eq(s,[.4+i,-1.7,0],.75) for i,s in enumerate(strings)])
      self.play(LaggedStart(*[GrowFromEdge(b,DOWN) for b in bars],lag_ratio=.25),Write(labels),run_time=3)
      self.cap('A real row, in team order $A,B,C,D,E$');self.source('Paper Table 2: tournament 1011111011')


class Constraints(Lesson):
  def construct(self):
    with self.say('s17'):
      after=eq(r'p_A(T\prime)+p_D(T\prime)+p_E(T\prime)',UP*.9,.9,ACCENT)
      before=eq(r'-\bigl(p_A(T)+p_D(T)+p_E(T)\bigr)',DOWN*.1,.9,PRIMARY)
      self.play(Write(after),run_time=2);self.play(Write(before),run_time=2)
      self.play(Write(eq(r'\le\alpha',DOWN*1.3,1.3,SECONDARY)),run_time=2)
      self.cap('After minus before: one inequality per cheat');self.source('Paper, finite linear program')
    with self.say('s18'):
      self.clear();g,arcs,pts=circle_tournament(n=3,radius=1.6)
      self.play(Create(g),run_time=2)
      self.play(arcs[0,1].animate.set_color(SECONDARY),run_time=1)
      self.play(Transform(arcs[0,1],Arrow(pts[1],pts[0],buff=.23,color=SECONDARY)),run_time=2)
      self.cap('Check every group of size 2 or 3')
      self.source('Standard definition: coalition size at most 3 (mode le)')
      for bits in ['000','001','010','011','100','101','110']:
        self.play(Transform(g,circle_tournament(n=3,bits=bits,radius=1.6)[0]),run_time=.55)
    with self.say('s19'):
      self.clear()
      axes=Axes(x_range=[0,1,.5],y_range=[0,1,.5],x_length=5,y_length=4,tips=False).shift(UP*.1)
      region=Polygon(axes.c2p(.1,.1),axes.c2p(.85,.1),axes.c2p(.1,.85),color=PRIMARY,fill_opacity=.18)
      self.play(Create(axes),FadeIn(region),run_time=2)
      for points in [[(.1,.1),(.65,.1),(.1,.65)],[(.2,.2),(.45,.2),(.2,.45)]]:
        self.play(Transform(region,Polygon(*[axes.c2p(*p) for p in points],color=ACCENT,fill_opacity=.35)),run_time=2)
      self.cap('Find probabilities satisfying every inequality')
      self.source('Schematic feasible region, not coordinates of the actual linear program')
    with self.say('s20'):
      self.clear();n=eq('0.400000\ldots',UP*.4,1.7)
      self.play(Write(n),run_time=2)
      box=SurroundingRectangle(n,color=WARN,buff=.3)
      self.play(Create(box))
      self.wait(2)
      fraction=eq(r'\frac25',UP*.4,2,ACCENT)
      self.play(Transform(n,fraction),Transform(box,SurroundingRectangle(fraction,color=ACCENT,buff=.3)),run_time=3)
      self.cap('Exact fractions decide the boundary');self.source('Paper, exact rounding and rational verification')


class Certificate(Lesson):
  def construct(self):
    with self.say('s21'):
      bars=VGroup(*[Rectangle(width=v*8,height=.38,color=SECONDARY if i==0 else PRIMARY,fill_opacity=.7).move_to([-4+v*4,1.5-i*.8,0]) for i,v in enumerate([.4,.34,.29,.21])])
      limit=DashedLine([-.8,2,0],[-.8,-1.5,0],color=SECONDARY)
      self.play(LaggedStart(*[GrowFromEdge(b,LEFT) for b in bars],lag_ratio=.25),Create(limit),run_time=3)
      self.play(Write(eq(r'\frac25',[-.8,2.5,0],1.)))
      self.cap('Circle equalities are pinned; other cheats have slack')
      self.source('Schematic slack bars; plain CC certificates only, n=5..8')
    with self.say('s22'):
      self.clear();x=eq(r'\frac15+\frac15+\frac15+\frac15+\frac15=1',UP*.7,1.2)
      self.play(Write(x),run_time=3)
      self.play(Write(eq(r'1-\frac35=\frac25\le\frac25',DOWN*.8,1.25,ACCENT)),run_time=3)
      self.cap('Independent checker, exact rational arithmetic');self.source('verification/verify\_rule.py; no discovery-code imports')
    with self.say('s23'):
      self.clear();count=Integer(0,group_with_commas=True,color=PRIMARY).scale(1.65)
      self.play(FadeIn(count));self.play(ChangeDecimalToValue(count,2889600),run_time=5,rate_func=linear)
      self.play(Write(lab('6,880 shapes',[0,1.8,0],1.)))
      self.cap('Recorded maximum gain $=2/5$',ACCENT);self.source('Completed exact replay: n8 CC result; counter animation is a summary')
    with self.say('s24'):
      self.clear()
      g,_,_=circle_tournament(radius=1.)
      self.play(Create(g),run_time=2)
      others=VGroup(g.copy().scale(.75).shift(LEFT*3.6),g.copy().scale(.75).shift(RIGHT*3.6))
      self.play(TransformFromCopy(g,others[0]),TransformFromCopy(g,others[1]),run_time=3)
      self.cap('Relabel shape and lottery together');self.source('Independent labelled checks cover every tournament for n=3..6')


class GoodRules(Lesson):
  def construct(self):
    with self.say('s25'):
      g,arcs,pts=circle_tournament(n=3,radius=1.4,center=LEFT*2.8)
      self.play(Create(g),run_time=2)
      b=probability_bar(.3,y=.2,width=3).shift(RIGHT*3)
      self.play(Create(b));self.play(Transform(arcs[2,0],Arrow(pts[0],pts[2],buff=.23,color=SECONDARY)),run_time=2)
      self.play(b[1].animate.stretch_to_fit_width(1.8).align_to(b[0],LEFT),run_time=2)
      self.cap('Winning another match cannot lower your own chance')
      self.source('Monotonicity illustration; separate exact MT certificate checks')
    with self.say('s26'):
      self.clear();pts=[np.array(p) for p in [(-3,1.4,0),(-4,-.9,0),(-1.8,-.9,0),(2,1,0),(3,-1,0)]]
      edges=[(0,1),(1,2),(2,0)]+[(i,j) for i in range(3) for j in [3,4]]+[(3,4)]
      dots=VGroup(*[Dot(p,radius=.18,color=ACCENT if i<3 else MUTED) for i,p in enumerate(pts)])
      arr=VGroup(*[Arrow(pts[i],pts[j],buff=.25,color=ACCENT if j<3 else MUTED,stroke_width=2) for i,j in edges])
      self.play(Create(arr),FadeIn(dots),run_time=3)
      self.play(Create(SurroundingRectangle(dots[:3],color=ACCENT,buff=.35)),run_time=1)
      self.play(Write(eq('0',pts[3]+UP*.6,.9)),Write(eq('0',pts[4]+DOWN*.6,.9)))
      self.cap('Top cycle: reach everyone by chains of wins');self.source('Paper, top-cycle consistency; outsiders receive zero probability')
    with self.say('s27'):
      self.clear();cards=VGroup(*[RoundedRectangle(width=.7,height=.9,corner_radius=.05,color=ACCENT).move_to([(i%7-3)*1.2,(.5-i//7)*1.5,0]) for i in range(14)])
      self.play(LaggedStart(*[Create(c) for c in cards],lag_ratio=.1),run_time=3)
      self.play(Write(lab('14 exact certificates',[0,2,0],1.)))
      self.cap('n=8 also passes monotonicity and top-cycle checks',ACCENT)
      self.source('Final readiness: 192,640 n8 monotonicity checks; all 14 certificates pass')


class Scope(Lesson):
  def construct(self):
    with self.say('s28'):
      left=eq(r'\text{lower}\ge\frac25',LEFT*3,1.1);right=eq(r'\text{upper}\le\frac25',RIGHT*3,1.1)
      self.play(Write(left),Write(right),run_time=2)
      self.play(ReplacementTransform(VGroup(left,right),eq(r'\text{optimum}=\frac25',ORIGIN,1.6,ACCENT)),run_time=3)
      self.cap('Five, six, seven and eight teams');self.source('SSW lower bound + exact upper certificates = paper Theorem 1')
    with self.say('s29'):
      self.clear()
      self.play(Write(eq(r'n=3,4:\quad\frac13',[0,1.4,0],1.1)),run_time=2)
      self.play(Write(eq(r'n=5,6,7,8:\quad\frac25',[0,.1,0],1.1,ACCENT)),run_time=2)
      self.play(Write(eq(r'n=7,\ k=4:\quad\frac37',[0,-1.3,0],1.1,SECONDARY)),run_time=2)
      self.source('First two rows: groups of at most 3. Last row: groups of at most 4.')
    with self.say('s30'):
      self.clear();line=NumberLine(x_range=[3,11,1],length=10,include_numbers=True).shift(DOWN*.3)
      self.play(Create(line),run_time=2)
      marks=VGroup(*[Dot(line.n2p(i)+UP*.6,radius=.13,color=ACCENT) for i in range(3,9)])
      self.play(LaggedStart(*[FadeIn(m) for m in marks],lag_ratio=.2),run_time=2)
      self.play(Write(eq('?',line.n2p(9)+UP*.8,1.4,SECONDARY)),Write(eq('?',line.n2p(10)+UP*.8,1.4,SECONDARY)),run_time=2)
      self.cap('No matching upper bound here for $n\\ge9$')
      self.source('Paper, discussion: separate tables do not extend automatically')
    with self.say('s31'):
      self.clear();g,_,_=circle_tournament(radius=1.3,center=LEFT*3)
      self.play(Create(g),Write(eq(r'\frac25',[2.7,.6,0],1.8,ACCENT)),run_time=2)
      self.play(Write(lab('through eight teams',[2.7,-.8,0],.9)))
      self.cap('The general three-team question remains open')
      self.source('Prior: SSW 2017; large-coalition refutation: SWZZ 2020')
    with self.say('s32'):
      self.clear()
      self.play(Write(lab('Exact optimal manipulability',[0,2.5,0],.95)),Write(lab('of Condorcet-consistent tournament rules',[0,1.8,0],.8)),Write(lab('against three-team coalitions on at most eight teams',[0,1.1,0],.75)),run_time=2)
      self.play(Write(lab('Valyu Research, 2026',[0,.1,0],.9)))
      self.play(Write(lab('economics/social-choice/tournament-rules/',[0,-1,0],.6)),Write(lab('three-team-manipulation-exact',[0,-1.55,0],.7)))
      self.play(Write(lab('Narration uses a synthetic voice.',[0,-2.7,0],.55,MUTED)))
