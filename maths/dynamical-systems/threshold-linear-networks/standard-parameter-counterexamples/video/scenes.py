from manim import *
from vrvideo import *
import json
from pathlib import Path

SCENES = ['Rates','Balance','Prediction','Witness','Matrix','Stability','Nondegenerate','Size','Credit']
ROOT=Path(__file__).resolve().parent
DATA=json.loads((ROOT/'assets.json').read_text())


def lab(s,p=ORIGIN,scale=.8,color=INK):
  return Tex(s,color=color).scale(scale).move_to(p)


def eq(s,p=ORIGIN,scale=1.,color=INK):
  return MathTex(s,color=color).scale(scale).move_to(p)


class Lesson(NarratedScene):
  def source(self,s):
    new=lab(s,[0,-3.55,0],.5,MUTED)
    if new.width>12.8:new.scale_to_fit_width(12.8)
    if hasattr(self,'src') and self.src in self.mobjects:self.play(Transform(self.src,new),run_time=.3)
    else:self.src=new;self.add(new)

  def cap(self,s,color=INK):
    new=lab(s,[0,-2.8,0],.8,color)
    if new.width>12.5:new.scale_to_fit_width(12.5)
    if hasattr(self,'cp') and self.cp in self.mobjects:self.play(Transform(self.cp,new),run_time=.5)
    else:self.cp=new;self.play(FadeIn(new),run_time=.5)

  def clear(self):
    self.play(*[FadeOut(m) for m in list(self.mobjects)],run_time=.6)


def rate_bar(value,x,color=PRIMARY):
  return Rectangle(width=.7,height=max(.02,value*3),fill_color=color,fill_opacity=.8,stroke_width=1).move_to([x,-1+value*1.5,0])


def pair():
  points=[LEFT*2,RIGHT*2]
  dots=VGroup(*[Dot(p,radius=.28,color=PRIMARY) for p in points])
  arrows=VGroup(Arrow(points[0]+UP*.18,points[1]+UP*.18,buff=.35,color=PRIMARY),Arrow(points[1]+DOWN*.18,points[0]+DOWN*.18,buff=.35,color=PRIMARY))
  return VGroup(arrows,dots)


def missing_graph(radius=2.1):
  pts=[radius*np.array([np.cos(PI/2-TAU*i/11),np.sin(PI/2-TAU*i/11),0]) for i in range(11)]
  dots=VGroup(*[Dot(p,radius=.1,color=PRIMARY) for p in pts])
  names=VGroup(*[eq(str(i),p*1.16,.65) for i,p in enumerate(pts)])
  missing=VGroup(*[DashedVMobject(Arrow(pts[j],pts[i],buff=.14,color=WARN,stroke_width=2,max_tip_length_to_length_ratio=.06),num_dashes=14) for j,i in DATA['deleted_arcs']])
  return VGroup(missing,dots,names),pts


def matrix_cells(values,spacing=.45,scale=.65):
  n=len(values)
  return VGroup(*[eq(str(v),[(j-(n-1)/2)*spacing,((n-1)/2-i)*spacing,0],scale,SECONDARY if v==6 else ACCENT if i==j else MUTED) for i,row in enumerate(values) for j,v in enumerate(row)])


class Rates(Lesson):
  def construct(self):
    a,b=rate_bar(.2,-1.5),rate_bar(.9,1.5)
    with self.say('c01'):
      self.play(GrowFromEdge(a,DOWN),GrowFromEdge(b,DOWN),run_time=2)
      self.play(Transform(a,rate_bar(4/7,-1.5)),Transform(b,rate_bar(4/7,1.5)),run_time=3)
      self.play(Transform(a,rate_bar(.7,-1.5,SECONDARY)),run_time=1)
      self.play(Transform(a,rate_bar(4/7,-1.5)),run_time=3)
      self.cap('Can wiring predict a stable pattern?');self.source('A mathematical rate model; schematic warm-up')
    with self.say('c02'):
      self.clear();bar=rate_bar(.65,0)
      self.play(GrowFromEdge(bar,DOWN));self.play(GrowArrow(Arrow([-2,1,0],[-.5,.5,0],color=ACCENT)),Write(lab('input',[-3,1,0])))
      self.play(GrowArrow(Arrow([.5,.2,0],[2,-.8,0],color=WARN)),Write(lab('decay',[3,-.8,0])))
      self.play(Transform(bar,rate_bar(.45,0)),run_time=2)
      self.cap('Rate of change = input after threshold $-$ current rate');self.source('Paper, equation 1; no biological measurement is shown')
    with self.say('c03'):
      self.clear();ax=Axes(x_range=[-2,2,1],y_range=[0,2,1],x_length=7,y_length=3,tips=False).shift(DOWN*.2)
      self.play(Create(ax));self.play(Create(ax.plot(lambda x:max(x,0),x_range=[-2,2],color=SECONDARY)),run_time=3)
      self.play(Write(eq(r'[u]_+=\max(u,0)',UP*2.2,1.1)))
      self.cap('Negative input becomes zero');self.source('Threshold-linear rule; horizontal axis input, vertical axis output')
    with self.say('c04'):
      self.clear();g=pair();self.play(Create(g),run_time=2)
      weight=eq(r'-\frac34',UP*1.2,1.4,PRIMARY)
      self.play(Write(weight),run_time=2)
      self.play(FadeOut(g[0][1]),Transform(g[0][0],DashedVMobject(g[0][0].copy().set_color(WARN))),run_time=2)
      self.play(Transform(weight,eq(r'-\frac32',UP*1.2,1.4,WARN)),run_time=2)
      self.cap('Arrow = weaker inhibition; absence = stronger inhibition')
      self.source('Standard parameters: epsilon=1/4, delta=1/2, drive=1')


class Balance(Lesson):
  def construct(self):
    with self.say('c05'):
      g=pair().shift(UP*.8);self.play(Create(g),run_time=2)
      statement=eq(r'x=1-\frac34x',DOWN*.8,1.4)
      self.play(Write(statement),run_time=3);self.cap('Equilibrium: rate equals its thresholded input')
      self.source('Two-neuron clique, standard parameters')
    with self.say('c06'):
      self.play(TransformMatchingTex(statement,eq(r'\frac74x=1',DOWN*.8,1.4)),run_time=2)
      self.wait(1)
      self.play(*[FadeOut(m) for m in list(self.mobjects) if isinstance(m,MathTex)],run_time=.4)
      statement=eq(r'7x=4',DOWN*.8,1.5);self.play(Write(statement),run_time=2)
      self.play(TransformMatchingTex(statement,eq(r'x=\frac47',DOWN*.8,1.6,ACCENT)),run_time=2)
    with self.say('c07'):
      self.clear();a,b=rate_bar(4/7,-2),rate_bar(4/7,2)
      self.play(Create(a),Create(b));self.play(Transform(a,rate_bar(.7,-2,SECONDARY)),run_time=2)
      ab=Arrow([-1.4,.5,0],[1.4,.5,0],color=WARN)
      self.play(GrowArrow(ab),Transform(b,rate_bar(.45,2)),run_time=2)
      self.play(GrowArrow(Arrow([1.4,-.3,0],[-1.4,-.3,0],color=ACCENT)),run_time=2)
      self.play(Write(eq(r'(-)\times(-)=+',UP*2,1.1)))
      self.cap('Less inhibition feeds back positively');self.source('Two inhibitory connections; no excitatory weight')
    with self.say('c08'):
      self.clear();t=ValueTracker(0)
      bars=always_redraw(lambda:VGroup(rate_bar(4/7+.12*np.exp(-t.get_value()/4),-2),rate_bar(4/7-.12*np.exp(-t.get_value()/4),2)))
      line=DashedLine([-3,-1+12/7,0],[3,-1+12/7,0],color=ACCENT)
      self.add(bars);self.play(Create(line),Write(eq(r'\frac47',[3.7,-1+12/7,0],.9)))
      self.play(t.animate.set_value(20),run_time=7,rate_func=linear);bars.clear_updaters()
      self.cap('Natural decay wins: the difference shrinks',ACCENT)
      self.source('Exact difference mode: deviations proportional to exp(-t/4)')


class Prediction(Lesson):
  def construct(self):
    pts=[np.array(p) for p in [(-3,1.4,0),(-4,-1.2,0),(-1.7,-1.2,0),(2,.2,0)]]
    dots=VGroup(*[Dot(p,radius=.2,color=PRIMARY if i<3 else MUTED) for i,p in enumerate(pts)])
    edges=VGroup(*[DoubleArrow(pts[i],pts[j],buff=.25,stroke_width=3,color=PRIMARY) for i,j in [(0,1),(1,2),(2,0)]])
    with self.say('c09'):
      self.play(Create(edges),FadeIn(dots[:3]),run_time=3)
      self.cap('Clique: every pair has arrows both ways');self.source('Paper, target-free clique definition')
    with self.say('c10'):
      targets=VGroup(*[Arrow(pts[i],pts[3],buff=.25,color=SECONDARY) for i in range(3)])
      self.play(FadeIn(dots[3]),LaggedStart(*[GrowArrow(a) for a in targets],lag_ratio=.3),run_time=3)
      tag=lab('target',[3.5,.2,0],.9,SECONDARY);self.play(Write(tag));self.wait(2)
      self.play(FadeOut(targets[2]),Transform(tag,lab('not a target',[3.8,.2,0],.8,ACCENT)),run_time=2)
      self.cap('Target-free: no outsider receives from the whole clique')
    with self.say('c11'):
      self.clear()
      self.play(Write(eq(r'\text{target-free clique}\ \Longrightarrow\ \text{stable}',UP*.7,.95,ACCENT)),run_time=3)
      self.play(Write(eq(r'\text{stable}\ \overset{?}{\Longrightarrow}\ \text{target-free clique}',DOWN*.8,.95,SECONDARY)),run_time=3)
      self.cap('The converse is the conjecture');self.source('Curto, Geneson and Morrison; 2019 preprint / 2024 paper')
    with self.say('c12'):
      self.clear();g,_=missing_graph(radius=1.9);self.play(Create(g),run_time=3)
      self.cap('G11: stable full support, but not a clique')
      self.source('Exact example at epsilon=1/4, delta=1/2, theta=1')


class Witness(Lesson):
  def construct(self):
    with self.say('c13'):
      g,pts=missing_graph(radius=1.9)
      all_edges=VGroup(*[Arrow(pts[i],pts[j],buff=.13,stroke_width=1,max_tip_length_to_length_ratio=.035,color=MUTED).set_opacity(.18) for i in range(11) for j in range(11) if i!=j])
      self.play(Create(all_edges),FadeIn(g[1:]),run_time=3)
      self.play(FadeOut(all_edges),LaggedStart(*[Create(a) for a in g[0]],lag_ratio=.04),run_time=3)
      self.cap('21 missing arrows, shown dashed red');self.source('Actual G11 deleted arcs; all other ordered pairs are arrows')
    with self.say('c14'):
      self.clear()
      nums=DATA['numerators']
      bars=VGroup(*[Rectangle(width=.58,height=v/67*3.1,fill_color=PRIMARY,fill_opacity=.8).move_to([(i-5)*.95,-1.4+v/67*1.55,0]) for i,v in enumerate(nums)])
      vals=VGroup(*[eq(str(v),b.get_top()+UP*.32,.65) for v,b in zip(nums,bars)])
      names=VGroup(*[eq(str(i),[(i-5)*.95,-1.85,0],.6,MUTED) for i in range(11)])
      self.play(LaggedStart(*[GrowFromEdge(b,DOWN) for b in bars],lag_ratio=.12),Write(vals),Write(names),run_time=3)
      self.play(Write(lab('Every numerator is divided by 292',[0,2.6,0],.85)))
      self.cap('All eleven rates are strictly positive',ACCENT);self.source('G11\_certificate.json: fixed\_point\_theta\_1')
    with self.say('c15'):
      self.play(bars[5].animate.set_color(SECONDARY),bars[8].animate.set_color(SECONDARY),run_time=1)
      self.play(Indicate(vals[5]),Indicate(vals[8]),run_time=2)
      self.cap('All other numerators: $313$; stronger pair: $37+10=47$')
      self.source('Neuron 0 misses arrows from 5 and 8; exact row calculation')
    with self.say('c16'):
      self.clear();a=eq(r'1-\frac34\frac{313+47}{292}',UP*.7,1.4)
      self.play(Write(a),run_time=3)
      self.play(TransformMatchingTex(a,eq(r'1-\frac{270}{292}=\frac{22}{292}',UP*.7,1.4,ACCENT)),run_time=3)
      self.cap('Input = rate: neuron 0 is balanced');self.source('Exact fraction arithmetic; all 11 rows checked in prepare\_assets.py')


class Matrix(Lesson):
  def construct(self):
    with self.say('c17'):
      cells=matrix_cells(DATA['K'],spacing=.43,scale=.63)
      self.play(LaggedStart(*[FadeIn(c) for c in cells],lag_ratio=.008),run_time=3)
      self.play(*[Indicate(cells[i*11+i],color=ACCENT) for i in range(11)],run_time=2)
      self.cap('$K$: diagonal $4$, arrow $3$, absence $6$');self.source('Actual 11 by 11 matrix: K=4(I-W)=I+3N+3J')
    with self.say('c18'):
      self.play(cells.animate.scale(.8).shift(LEFT*2.5),run_time=1)
      self.play(*[cells[j].animate.set_color(SECONDARY) for j in range(11)],run_time=1)
      self.play(Write(eq(r'Kx^*=(4,\ldots,4)^{\mathsf T}',[2.7,.6,0],.95)),run_time=2)
      self.play(Write(eq(r'\frac{4\cdot22+3\cdot313+3\cdot47}{292}=4',[2.5,-1.2,0],.78)),run_time=3)
      self.cap('Row times rate list: multiply, then add');self.source('Exact matrix identity; vector of ones means one entry for every neuron')
    with self.say('c19'):
      self.clear()
      for x,good in [(-3,True),(3,False)]:
        line=NumberLine(x_range=[-2,2,1],length=4,include_ticks=False).move_to([x,.2,0]);dot=Dot(line.n2p(0),color=ACCENT if good else WARN,radius=.14)
        self.play(Create(line),FadeIn(dot),run_time=.7)
        self.play(dot.animate.move_to(line.n2p(.4)),run_time=.7)
        self.play(dot.animate.move_to(line.n2p(0 if good else 1.8)),run_time=2)
      self.cap('Balanced does not automatically mean stable');self.source('Local deviations; all active rates stay above threshold sufficiently nearby')
    with self.say('c20'):
      self.clear()
      for x,stable in [(-3,True),(3,False)]:
        curve=ParametricFunction(lambda t,x=x,stable=stable:np.array([x+(1.5*np.exp(-.2*t) if stable else .25*np.exp(.2*t))*np.cos(t), (1.5*np.exp(-.2*t) if stable else .25*np.exp(.2*t))*np.sin(t),0]),t_range=[0,8],color=ACCENT if stable else WARN)
        self.play(Create(curve),run_time=3)
        self.play(Write(lab('shrinks' if stable else 'grows',[x,-2,0],.85,ACCENT if stable else WARN)))
      self.source('Schematic phase portraits: rotation plus decay or growth')


class Stability(Lesson):
  def construct(self):
    with self.say('c21'):
      curve=ParametricFunction(lambda t:np.array([2*np.exp(-.2*t)*np.cos(t),2*np.exp(-.2*t)*np.sin(t),0]),t_range=[0,12],color=ACCENT)
      self.play(Create(curve),run_time=5)
      self.play(Write(eq(r'\dot u=-\frac14Ku',UP*2.6,1.15)),run_time=2)
      self.cap('A mode can rotate while its size shrinks');self.source('u=x-x*: deviation from the positive equilibrium; paper full-support lemma')
    with self.say('c22'):
      self.clear();ax=Axes(x_range=[-.02,.08,.02],y_range=[-4,4,2],x_length=7,y_length=4,tips=False).shift(LEFT*.8)
      self.play(Create(ax));self.play(Write(lab('real part',[1,-2.3,0],.65)),Write(lab('imaginary part',[-4,2.6,0],.65)))
      vals=[v for v in DATA['eigenvalues'] if v[0]<.1]
      points=VGroup(*[Dot(ax.c2p(r,i),color=ACCENT,radius=.08) for r,i in vals])
      self.play(FadeIn(points),run_time=2)
      self.play(Write(eq('0',ax.c2p(0,0)+DOWN*.65+LEFT*.1,.55)),Write(eq('0.04',ax.c2p(.04,0)+DOWN*.65,.55)),Write(eq('0.08',ax.c2p(.08,0)+DOWN*.65,.55)),run_time=.6)
      self.play(Write(eq(r'\min\Re(\lambda)\approx0.03772',[0,3.1,0],.85)))
      self.play(Write(lab('Also: four at 1; one near 39.7',[3.7,1.8,0],.55,MUTED)))
      self.cap('Numerical zoom: the margin is positive but thin');self.source('K eigenvalues, numerical illustration; exact certificate follows')
    with self.say('c23'):
      self.clear();p=eq(r'z^2+bz+c',UP*.8,1.5)
      self.play(Write(p),run_time=2)
      self.play(Write(eq(r'b>0,\quad c>0',DOWN*.6,1.3,ACCENT)),run_time=2)
      self.cap('Both roots have negative real part exactly under these conditions')
      self.source('Quadratic warm-up; Hurwitz criterion extends the coefficient test')
    with self.say('c24'):
      self.clear();p=eq(r'\det(zI+K)=z^{11}+44z^{10}+\cdots+1168',UP*2,1.05)
      self.play(Write(p),run_time=3)
      nums=VGroup(*[eq(v,[(i-1)*3.6,.5,0],.9,ACCENT) for i,v in enumerate(['44','7514','1867920'])])
      self.play(LaggedStart(*[Write(n) for n in nums],lag_ratio=.3),run_time=3)
      checks=VGroup(*[eq('+',[(i-5)*.8,-1.25,0],.95,ACCENT) for i in range(11)])
      self.play(LaggedStart(*[FadeIn(c) for c in checks],lag_ratio=.1),run_time=2)
      self.cap('All 11 Hurwitz determinants are positive',ACCENT);self.source('Exact certificate: Delta1=44, Delta2=7514, Delta3=1867920; two checkers')


class Nondegenerate(Lesson):
  def construct(self):
    with self.say('c25'):
      sq=Square(2.6,color=PRIMARY,fill_opacity=.15)
      self.play(Create(sq),run_time=2)
      self.play(Transform(sq,Line(DOWN*1.3,UP*1.3,color=PRIMARY)),run_time=3)
      determinant=eq(r'\det=0',RIGHT*2.3,1.2,WARN)
      self.play(Write(determinant))
      self.play(Transform(sq,Square(2.6,color=PRIMARY,fill_opacity=.15)),Transform(determinant,eq(r'\det\ne0',RIGHT*2.7,1.2,ACCENT)),run_time=3)
      self.cap('Nonzero determinant: no direction collapses');self.source('Geometric teaching example; nondegeneracy concerns all required submatrices')
    with self.say('c26'):
      self.clear();vals=[[4,3,6],[6,4,3],[3,6,4]]
      m=matrix_cells(vals,spacing=1.,scale=1.2)
      self.play(Write(m),run_time=2)
      ident=matrix_cells([[1,0,0],[0,1,0],[0,0,1]],spacing=1.,scale=1.2)
      self.play(Transform(m,ident),run_time=3)
      self.cap('Remainders modulo 3: $4\\to1$, $3\\to0$, $6\\to0$')
      self.source('Paper mod-3 lemma; representative block, argument applies to every size')
    with self.say('c27'):
      self.play(Write(eq(r'\det K_\sigma\equiv1\pmod3',UP*2.3,1.)))
      cramer=matrix_cells([[1,1,0],[0,1,0],[0,1,1]],spacing=1.,scale=1.2)
      self.play(Transform(m,cramer),run_time=3)
      self.play(Create(SurroundingRectangle(VGroup(*m[3:6]),color=SECONDARY,buff=.2)),run_time=1)
      self.cap('Replace a column by ones: determinant still $1$ modulo $3$')
      self.source('Expand along the middle row; remaining minor is the identity')
    with self.say('c28'):
      self.clear()
      a=lab('No accidental zero determinants',[0,1.3,0],.9,ACCENT)
      b=lab('Positive rates + stable local dynamics',[0,-.2,0],.9,PRIMARY)
      self.play(Write(a),run_time=2);self.play(Write(b),run_time=2)
      self.cap('Nondegeneracy and stability are different claims');self.source('Paper main theorem: universal mod-3 result, specific G11 stability certificate')


class Size(Lesson):
  def construct(self):
    with self.say('c29'):
      g,_=missing_graph(radius=1.7);self.play(Create(g),run_time=2)
      self.play(g[1][0].animate.set_opacity(.1),g[2][0].animate.set_opacity(.1),*[g[0][i].animate.set_opacity(.05) for i,arc in enumerate(DATA['deleted_arcs']) if 0 in arc],run_time=2)
      self.cap('Vertex-minimal among nonclique full supports')
      self.source('All 2,035 proper subsets: 90 cliques, 1,778 nonpermitted, 167 unstable')
    with self.say('c30'):
      self.clear()
      numbers=['882{,}033{,}440','35{,}842','0']
      for i,n in enumerate(numbers):
        self.play(Write(eq(n,[(i-1)*4.5,.5,0],1.05,ACCENT if i==2 else PRIMARY)),run_time=2)
        if i<2:self.play(GrowArrow(Arrow([(i-1)*4.5+1.65,.5,0],[(i)*4.5-1.65,.5,0],buff=.1,color=MUTED)),run_time=.5)
      self.cap('All shapes $\\to$ saved candidates $\\to$ stable survivors')
      self.source('n7 complete enumeration; bounded rejection filter; exact rational candidate replay')
    with self.say('c31'):
      self.clear();line=NumberLine(x_range=[2,11,1],length=11,include_numbers=True).shift(DOWN*.3)
      self.play(Create(line),run_time=2)
      for i in range(2,8):self.add(Cross(Square(.3).move_to(line.n2p(i)+UP*.6),stroke_color=WARN,stroke_width=3))
      self.play(*[Write(eq('?',line.n2p(i)+UP*.7,1.2,SECONDARY)) for i in [8,9,10]],run_time=2)
      self.play(FadeIn(Dot(line.n2p(11)+UP*.6,color=ACCENT,radius=.15)))
      self.cap('Minimum nonclique support size: $8\\le m\\le11$')
      self.source('No global exclusion of orders 8, 9 or 10')
    with self.say('c32'):
      self.clear();ax=Axes(x_range=[0,800,200],y_range=[-.004,.004,.002],x_length=9,y_length=4,tips=False)
      self.play(Create(ax))
      self.play(*[Write(eq(str(t),ax.c2p(t,0)+DOWN*2.35,.55)) for t in [0,400,800]],run_time=.6)
      sim=DATA['simulation'];values=np.array(sim['values']);rates=np.array([float(__import__('fractions').Fraction(v)) for v in DATA['rates']])
      curves=VGroup()
      for j,col in [(0,PRIMARY),(5,SECONDARY),(7,ACCENT)]:
        curve=VMobject(color=col,stroke_width=2.5);curve.set_points_as_corners([ax.c2p(t,v) for t,v in zip(sim['times'],values[:,j]-rates[j])]);curves.add(curve)
      self.play(Create(curves),run_time=6)
      self.cap('One small perturbation returns; three rate deviations shown')
      self.source('Numerical G11 simulation: 0.1 percent perturbation; time 0..800; rate deviations')


class Credit(Lesson):
  def construct(self):
    with self.say('c33'):
      self.play(Write(lab('Geneson: six neurons, different parameters',[0,1.4,0],.9)),run_time=3)
      self.play(Write(lab('hturcotte1/CLTN: standard-point examples',[0,0,0],.9)),run_time=3)
      self.cap('Prior counterexamples are part of this story');self.source('Paper, provenance: repository W4 has 23 neurons')
    with self.say('c34'):
      self.clear();self.play(Write(lab('hturcotte1/CLTN',[0,2,0],1.1)),run_time=1)
      self.play(Write(lab('commit 3744200, 15 October 2026',[0,1,0],.9)),run_time=2)
      self.play(Write(eq(r'23\ \longrightarrow\ 11',[0,-.5,0],1.7,PRIMARY)),run_time=3)
      self.cap('Shrink vertices and repair arrows');self.source('Prior map already implies exclusion through seven; independently verified here')
    with self.say('c35'):
      self.clear();g,_=missing_graph(radius=1.3);g.shift(LEFT*3.2)
      self.play(Create(g),run_time=2)
      self.play(Write(lab('Balanced rates',[2.7,1.3,0],.9)),Write(lab('Local return',[2.7,.1,0],.9,ACCENT)),Write(lab('A nonclique support',[2.7,-1.1,0],.9,SECONDARY)),run_time=3)
      self.source('Retained: explicit G11, vertex-minimality, mod-3 lemma, independently certified bracket')
    with self.say('c36'):
      self.clear();self.play(Write(lab('Small counterexamples to the target-free clique conjecture',[0,2,0],.78)),Write(lab('at the standard CTLN parameters',[0,1.3,0],.9)),run_time=2)
      self.play(Write(lab('Valyu Research, 2026',[0,.2,0],.9)))
      self.play(Write(lab('maths/dynamical-systems/threshold-linear-networks/',[0,-.9,0],.58)),Write(lab('standard-parameter-counterexamples',[0,-1.5,0],.7)))
      self.play(Write(lab('Narration uses a synthetic voice.',[0,-2.7,0],.55,MUTED)))
