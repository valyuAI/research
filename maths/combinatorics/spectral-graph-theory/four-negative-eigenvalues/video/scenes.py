from manim import *
from vrvideo import *
import json
from pathlib import Path
import itertools

SCENES=['Movement','Signs','Reduced','Cores','Enumeration','Termination','Thirty','Extremal','Scope']
ROOT=Path(__file__).resolve().parent
DATA=json.loads((ROOT/'assets.json').read_text())


def lab(s,p=ORIGIN,scale=.8,color=INK):
  return Tex(s,color=color).scale(scale).move_to(p)


def eq(s,p=ORIGIN,scale=1.,color=INK):
  return MathTex(s,color=color).scale(scale).move_to(p)


def network(n,edges,pts=None,radius=2,color=PRIMARY):
  if pts is None:pts=[radius*np.array([np.cos(PI/2-TAU*i/n),np.sin(PI/2-TAU*i/n),0]) for i in range(n)]
  lines=VGroup(*[Line(pts[i],pts[j],color=color,stroke_width=2 if n<16 else 1.1).set_opacity(.8 if n<16 else .45) for i,j in edges])
  dots=VGroup(*[Dot(p,radius=.13 if n<8 else .08 if n<16 else .055,color=color) for p in pts])
  return VGroup(lines,dots)


def record_graph(rec,radius=2):
  return network(len(rec['matrix']),rec['edges'],radius=radius)


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


class Movement(Lesson):
  def construct(self):
    pts=[LEFT*2,RIGHT*2];g=network(2,[(0,1)],pts)
    with self.say('g01'):
      nums=VGroup(eq('2',pts[0]+UP*.7,1.3,PRIMARY),eq('5',pts[1]+UP*.7,1.3,SECONDARY))
      self.play(Create(g),Write(nums),run_time=2)
      self.play(nums[0].animate(path_arc=-PI/2).move_to(pts[1]+UP*.7),nums[1].animate(path_arc=-PI/2).move_to(pts[0]+UP*.7),run_time=3)
      self.cap('Replace each value by the sum at its neighbours')
      self.source('One edge: the adjacency operation swaps the two entries')
    with self.say('g02'):
      self.play(FadeOut(nums),g.animate.shift(LEFT*2.6).scale(.6),run_time=1)
      mat=Matrix([[0,1],[1,0]],h_buff=1.1,v_buff=.8).scale(.9).shift(RIGHT*1.8)
      self.play(Write(mat),run_time=3)
      self.play(Indicate(mat.get_entries()[1],color=SECONDARY),Indicate(mat.get_entries()[2],color=SECONDARY),run_time=2)
      self.cap('One means connected; zero means not connected');self.source('Adjacency matrix: symmetric table, zero diagonal')
    with self.say('g03'):
      self.clear();a=eq(r'\begin{pmatrix}0&1\\1&0\end{pmatrix}\binom11=\binom11',UP*.7,1.2)
      self.play(Write(a),run_time=3)
      arrow=Arrow([-1,-1.2,0],[1,.2,0],color=ACCENT,buff=0)
      self.play(GrowArrow(arrow),run_time=2)
      self.cap('Same direction, factor $+1$: a positive eigenvalue')
      self.source('Exact calculation: (1,1) is an eigenvector')
    with self.say('g04'):
      self.clear();a=eq(r'\begin{pmatrix}0&1\\1&0\end{pmatrix}\binom{1}{-1}=\binom{-1}{1}',UP*.9,1.2)
      self.play(Write(a),run_time=3)
      origin=np.array([0,-1,0]);arrow=Arrow(origin,origin+np.array([1.5,-.6,0]),color=PRIMARY,buff=0)
      self.play(GrowArrow(arrow));self.play(Transform(arrow,Arrow(origin,origin+np.array([-1.5,.6,0]),color=SECONDARY,buff=0)),run_time=3)
      self.cap('Direction flips: multiply by $-1$');self.source('Exact eigenpair: eigenvalue -1, eigenvector (1,-1)')


class Signs(Lesson):
  def construct(self):
    with self.say('g05'):
      headings=VGroup(lab('positive',LEFT*3.5+UP*1.5,.9,ACCENT),lab('zero',UP*1.5,.9,MUTED),lab('negative',RIGHT*3.5+UP*1.5,.9,SECONDARY))
      self.play(Write(headings),run_time=2)
      dots=VGroup(Dot(LEFT*3.5,radius=.18,color=ACCENT),Dot(RIGHT*3.5,radius=.18,color=SECONDARY))
      self.play(FadeIn(dots));self.play(Write(eq('(1,0,1)',DOWN*1.3,1.3)))
      self.cap('Inertia = counts of positive, zero and negative eigenvalues')
      self.source('For a real symmetric n by n table: n real eigenvalues, with multiplicities')
    with self.say('g06'):
      self.clear();tri=network(3,[(0,1),(1,2),(2,0)],radius=1.2).shift(LEFT*3.2)
      pent=network(5,[(i,(i+1)%5) for i in range(5)],radius=1.2).shift(RIGHT*3.2)
      self.play(Create(tri),run_time=2);self.play(Write(eq('2,-1,-1',[-3.2,-1.8,0],.85)))
      self.play(Create(pent),run_time=2)
      self.play(Write(eq(r'2,\ 0.618,\ 0.618',[3.2,-1.6,0],.7,ACCENT)),Write(eq(r'-1.618,\ -1.618',[3.2,-2.2,0],.7,SECONDARY)))
      self.source('Pentagon values rounded: (sqrt(5)-1)/2 twice, -(sqrt(5)+1)/2 twice')
    with self.say('g07'):
      self.clear();self.play(Write(eq(r'n^-=4',UP*1.8,1.5,SECONDARY)),run_time=2)
      self.play(Write(lab('How many positive values?',LEFT*3+DOWN*.3,.85)),Write(lab('How many dots?',RIGHT*3+DOWN*.3,.85)),run_time=3)
      self.cap('Sign count and graph size are different questions');self.source('Paper: positive-count extremum A4 and reduced-order extremum n(4)')
    with self.say('g08'):
      self.clear();pts=[LEFT*2,ORIGIN,RIGHT*2];g=network(3,[(0,1),(1,2)],pts)
      self.play(Create(g),run_time=2)
      vals=VGroup(*[eq(s,p+UP*.6,1.1,SECONDARY if s=='-1' else PRIMARY) for s,p in zip(['1','0','-1'],pts)])
      self.play(Write(vals),run_time=2)
      self.play(vals[0].animate.move_to(UP*.6),vals[2].animate.move_to(UP*.6),run_time=2)
      self.play(Transform(vals,VGroup(*[eq('0',p+UP*.6,1.1,MUTED) for p in pts])),run_time=2)
      self.cap('The copied difference cancels: a zero eigenvalue');self.source('Exact three-vertex path: (1,0,-1) maps to (0,0,0)')


class Reduced(Lesson):
  def construct(self):
    with self.say('g09'):
      pts=[LEFT*2,ORIGIN,RIGHT*2,UP*1.8];g=network(4,[(0,1),(1,2)],pts)
      self.play(Create(g),run_time=2)
      self.play(FadeOut(g[1][3]),FadeOut(g[1][2]),FadeOut(g[0][1]),run_time=2)
      self.cap('Remove isolated dots and duplicate neighbourhoods');self.source('Inertia signs preserved: eigenvalues themselves need not stay equal')
    with self.say('g10'):
      self.clear();m=Matrix([[0,1,0],[1,0,1],[0,1,0]],h_buff=1,v_buff=.7).scale(.9)
      self.play(Write(m),run_time=2)
      duplicate=lab('Equal rows: this graph is not reduced',UP*2,.85,SECONDARY)
      self.play(Write(duplicate),Indicate(m.get_rows()[0],color=SECONDARY),Indicate(m.get_rows()[2],color=SECONDARY),run_time=2)
      self.play(Transform(m,Matrix([[0,1],[1,0]],h_buff=1,v_buff=.7).scale(1.2)),FadeOut(duplicate),run_time=2)
      self.cap('Reduced: no equal neighbourhood rows, no zero row')
      self.source('Reduced does not imply nonsingular; other dependencies can still give zero eigenvalues')
    with self.say('g11'):
      self.clear();g=record_graph(DATA['doublings']['OOO'],radius=1.8).shift(LEFT*2.8)
      self.play(Create(g),run_time=3)
      self.play(Write(eq('30=4+22+4',[2.5,.7,0],1.1)),Write(lab('positive / zero / negative',[2.5,-.5,0],.7)))
      self.cap('At most 30 dots in a reduced graph with four negatives');self.source('Exact order-30 certificate: ordinary doubling, 155 edges')
    with self.say('g12'):
      self.clear();self.play(Write(eq(r'\text{size maximum}:\ 30',UP*1.2,1.15,PRIMARY)),run_time=2)
      self.play(Write(eq(r'\text{positive maximum}:\ 11\quad(15\text{ dots})',DOWN*.4,1.05,ACCENT)),run_time=3)
      self.cap('Different records, different extremal graphs');self.source('CFJK 2013 supplies bound and examples; this paper supplies uniqueness')


class Cores(Lesson):
  def construct(self):
    with self.say('g13'):
      pts=[LEFT*2,ORIGIN,RIGHT*2];g=network(3,[(0,1),(1,2)],pts)
      self.play(Create(g),run_time=2);self.play(g[1][2].animate.set_color(SECONDARY),g[0][1].animate.set_color(SECONDARY))
      self.play(FadeOut(g[1][2]),FadeOut(g[0][1]),run_time=3)
      self.cap('Keep an induced core with the same positive and negative counts');self.source('Nonsingular-basis lemma; edge inside the path is a concrete example')
    with self.say('g14'):
      self.play(Write(eq(r'(1,1,1)\longrightarrow(1,0,1)',UP*1.8,1.2)),run_time=3)
      self.cap('Core size = rank; nonsingular means no zero eigenvalues')
      self.source('Core reduction is general; deleting duplicates alone is not the full theorem')
    with self.say('g15'):
      self.clear();edge=network(2,[(0,1)],[LEFT*1.7,RIGHT*1.7])
      self.play(FadeIn(edge[1]),run_time=2);self.play(Create(edge[0]),run_time=2)
      self.play(Write(lab('Add two dots together',[0,2,0],.95)))
      top=Dot(UP*1.8,radius=.13,color=SECONDARY)
      self.play(FadeOut(self.mobjects[-1]),FadeIn(top),Create(Line(LEFT*1.7,UP*1.8,color=SECONDARY)),Create(Line(RIGHT*1.7,UP*1.8,color=SECONDARY)),run_time=3)
      self.cap('Then one more dot makes a triangle');self.source('One or two new vertices: Jacobi-minor closure lemma')
    with self.say('g16'):
      self.clear();self.play(Write(eq(r'A^{-1}_{ii}\ne0\ \Longrightarrow\ \text{delete one}',UP*1.3,1.05)),run_time=3)
      self.play(Write(eq(r'\det\begin{pmatrix}0&t\\t&0\end{pmatrix}=-t^2\ne0',DOWN*.5,1.15)),run_time=3)
      self.cap('If every diagonal vanishes, a nonzero pair permits two deletions')
      self.source('Jacobi identity; paper proves the resulting induced graph is nonsingular')


class Enumeration(Lesson):
  def construct(self):
    with self.say('g17'):
      edge=network(2,[(0,1)],[LEFT*1.8,RIGHT*1.8]);new=Dot(UP*1.8,radius=.15,color=SECONDARY)
      self.play(Create(edge),FadeIn(new),run_time=2)
      lines=VGroup(Line(LEFT*1.8,UP*1.8,color=SECONDARY),Line(RIGHT*1.8,UP*1.8,color=SECONDARY))
      label=eq('(0,0)',[0,-1.5,0],1.2);self.play(Write(label))
      for bits in [(1,0),(0,1),(1,1)]:
        self.play(*[l.animate.set_opacity(float(b)) for l,b in zip(lines,bits)],Transform(label,eq(str(bits),[0,-1.5,0],1.2)),run_time=1)
        self.add(lines)
      self.cap('Try every binary connection pattern');self.source('Sign of det(H) times sign of b-transpose adj(H) b is exact')
    with self.say('g18'):
      self.clear();tri=network(3,[(0,1),(1,2),(0,2)],radius=1.3).shift(LEFT*3.4)
      self.play(Create(tri),run_time=2)
      self.play(Write(eq(r'(1,1)\begin{pmatrix}0&1\\1&0\end{pmatrix}\binom11=2',[2.2,.6,0],1.)),run_time=3)
      self.play(Write(eq(r'\text{new sign}=\operatorname{sign}(-2)',[2.2,-1,0],1.,SECONDARY)),run_time=2)
      self.cap('Edge to triangle: gain one negative eigenvalue');self.source('Exact Schur complement example: -b-transpose H-inverse b = -2')
    with self.say('g19'):
      self.clear();positions=[(-4,1.8,0),(-1,1,0),(-1,-1,0),(2,1.8,0),(2,0,0),(2,-1.8,0),(4.7,1,0)]
      ds=VGroup(*[Dot(p,radius=.13,color=PRIMARY) for p in positions])
      es=VGroup(*[Arrow(positions[a],positions[b],buff=.18,color=MUTED,stroke_width=2) for a,b in [(0,1),(0,2),(1,3),(1,4),(2,5),(3,6)]])
      self.play(Create(es),FadeIn(ds),run_time=3)
      self.play(Create(Cross(ds[-1],stroke_color=WARN,scale_factor=.3)),Write(lab('5 negatives',[4.5,-.1,0],.7,WARN)),run_time=2)
      self.cap('Generate all valid one- and two-dot extensions');self.source('Schematic search tree; exact generation and isomorphism merging')
    with self.say('g20'):
      self.clear();counts=DATA['census_exactly_four']
      bars=VGroup(*[Rectangle(width=.55,height=max(.015,3*v/14422),fill_color=PRIMARY if v else WARN,fill_opacity=.8).move_to([(i-6)*.85,-1.4+max(.015,3*v/14422)/2,0]) for i,v in enumerate(counts)])
      labels=VGroup(*[eq(str(i+5),[(i-6)*.85,-1.85,0],.6) for i in range(len(counts))])
      self.play(LaggedStart(*[GrowFromEdge(b,DOWN) for b in bars],lag_ratio=.08),Write(labels),run_time=3)
      self.play(Write(lab('14,422 at order 10',[0,2.3,0],.85)),Write(eq('2',[3.4,-.9,0],.7,SECONDARY)),Write(eq('0',[4.25,-.9,0],.7,WARN)),Write(eq('0',[5.1,-.9,0],.7,WARN)))
      self.cap('Order 15: two. Orders 16 and 17: zero.');self.source('Bars: exactly four negatives; both final empty levels also hold for at most four')


class Termination(Lesson):
  def construct(self):
    with self.say('g21'):
      centers=[np.array([x,0,0]) for x in [-4,-1.3,1.3,4]]
      labels=VGroup(*[eq(str(n),p+UP*.8,1.) for n,p in zip([16,17,18,19],centers)])
      self.play(Write(labels),run_time=2)
      for i in range(4):
        self.play(Write(eq('0',centers[i],1.5,WARN)),run_time=.6)
        if i>=2:
          for j in [i-1,i-2]:
            a=CurvedArrow(centers[j]+DOWN*.45,centers[i]+DOWN*.45,angle=PI/4,color=MUTED)
            self.play(Create(a),run_time=.5)
      self.cap('Two empty levels prevent any restart');self.source('Paper closure theorem: induction using one- or two-vertex parents')
    with self.say('g22'):
      self.clear();counter=Integer(0,group_with_commas=True,color=PRIMARY).scale(1.8)
      self.play(FadeIn(counter));self.play(ChangeDecimalToValue(counter,45242),run_time=4,rate_func=linear)
      self.cap('Complete census: at most four negative eigenvalues')
      self.source('Recorded completed enumeration; exact replay checks inertia and distinctness of all rows')
    with self.say('g23'):
      self.clear();core=network(3,[(0,1),(1,2),(2,0)],radius=1.1).shift(LEFT*3)
      self.play(Create(core),run_time=2)
      self.play(Write(eq(r'b\in\{0,1\}^r',[2.4,1.2,0],1.1)),run_time=2)
      self.play(Write(eq(r'b^{\mathsf T}H^{-1}b=0',[2.4,0,0],1.)),Write(eq(r'b^{\mathsf T}H^{-1}c\in\{0,1\}',[2.4,-1.2,0],1.)),run_time=3)
      self.cap('Extra dots must add zero directions and valid edges')
      self.source('Schematic core illustration; actual search uses every certified core with four negatives')
    with self.say('g24'):
      self.clear();pts=[np.array(p) for p in [(-2,1.5,0),(0,1.5,0),(-1,-.5,0),(2,-1,0),(3,1,0)]]
      g=network(5,[(0,1),(1,2),(0,2),(2,3),(1,4)],pts)
      self.play(Create(g),run_time=2)
      self.play(*[g[1][i].animate.set_color(ACCENT) for i in [0,1,2]],*[g[0][i].animate.set_color(ACCENT) for i in [0,1,2]],run_time=2)
      self.cap('Choose a largest set of mutually compatible patterns')
      self.source('Schematic compatibility graph; method: Akbari, Cameron and Khosrovshahi (2004)')


class Thirty(Lesson):
  def construct(self):
    with self.say('g25'):
      maxima=DATA['maxima'];bars=VGroup();labels=VGroup();values=VGroup()
      for i,v in enumerate(maxima):
        x=(i-5)*.95;height=v*.105
        bars.add(Rectangle(width=.6,height=height,fill_color=ACCENT if i==3 else PRIMARY,fill_opacity=.8,stroke_width=1).move_to([x,-1.4+height/2,0]))
        labels.add(eq(str(i+5),[x,-1.85,0],.6));values.add(eq(str(v),[x,-1.4+height+.28,0],.6,ACCENT if i==3 else INK))
      self.play(LaggedStart(*[GrowFromEdge(b,DOWN) for b in bars],lag_ratio=.1),Write(labels),Write(values),run_time=4)
      self.cap('Maximum reduced size by rank: peak $30$ at rank $8$')
      self.source('Both exact maximum-order runs: ranks 5..15; new exclusion includes ranks 9..15')
    with self.say('g26'):
      self.clear();pts=[np.array(p) for p in [(-3,1,0),(-1,1,0),(-3,-1,0),(-1,-1,0),(1,-1,0),(3,-1,0)]]
      rec=DATA['ordinary_steps'][1];g=network(6,rec['edges'],pts)
      old=Line(pts[0],pts[1],color=PRIMARY,stroke_width=3)
      self.play(Create(old),FadeIn(g[1][:2]),run_time=2)
      self.play(TransformFromCopy(g[1][0],g[1][2]),TransformFromCopy(g[1][1],g[1][3]),run_time=2)
      self.play(*[Create(e) for e,(a,b) in zip(g[0],rec['edges']) if b<4 and (a,b)!=(0,1)],run_time=2)
      self.play(FadeIn(g[1][4:]),*[Create(e) for e,(a,b) in zip(g[0],rec['edges']) if b>=4],run_time=2)
      self.cap('Copy, connect a new dot to all copies, attach a final dot')
      self.source('Kotlov--Lovasz step; ACK (2004), Construction A')
    with self.say('g27'):
      self.clear();g=record_graph(DATA['ordinary_steps'][1],radius=1.7)
      count=eq('6',UP*2.5,1.2)
      self.play(Create(g),Write(count),run_time=2)
      for idx in [2,3]:
        self.play(Transform(g,record_graph(DATA['ordinary_steps'][idx],radius=1.9)),Transform(count,eq(str(len(DATA['ordinary_steps'][idx]['matrix'])),UP*2.5,1.2)),run_time=3)
      self.cap('$2\\to6\\to14\\to30$: each step doubles, then adds two')
      self.source('Variant V also joins the final new dot to originals; words VVV, VVO, VOO, OOO')
      self.wait(.5)
      self.clear()
      pts=[np.array(p) for p in [(-3,1,0),(-1,1,0),(-3,-1,0),(-1,-1,0),(1,-1,0),(3,-1,0)]]
      ordinary=network(6,DATA['ordinary_steps'][1]['edges'],pts)
      self.play(Create(ordinary),run_time=1.5)
      extra=VGroup(*[Line(pts[5],pts[i],color=SECONDARY,stroke_width=4) for i in [0,1]])
      self.play(Create(extra),run_time=2)
      self.cap('Variant: the final dot also joins every original dot')
      self.source('ACK (2004), Construction B; variant steps precede ordinary steps')
    with self.say('g28'):
      self.clear();gs=VGroup(*[record_graph(DATA['doublings'][w],radius=.9).shift(np.array([(i-1.5)*3.1,.2,0])) for i,w in enumerate(['OOO','VOO','VVO','VVV'])])
      labels=VGroup(*[lab(f'{w}: {len(DATA["doublings"][w]["edges"])} edges',[(i-1.5)*3.1,-1.3,0],.6) for i,w in enumerate(['OOO','VOO','VVO','VVV'])])
      self.play(LaggedStart(*[Create(g) for g in gs],lag_ratio=.2),Write(labels),run_time=4)
      self.cap('Four known rank-8 classes; other ranks now excluded')
      self.source('Akbari, Cameron and Khosrovshahi (2004); paper Theorem 1')


def w5_positions():
  return [1.2*np.array([np.cos(PI/2-TAU*i/5),np.sin(PI/2-TAU*i/5),0]) for i in range(5)]+[2.3*np.array([np.cos(PI/2-TAU*i/10),np.sin(PI/2-TAU*i/10),0]) for i in range(10)]


def x_positions():
  return [np.array([(x-1)*1.2,(y-1)*1.2,0]) for x in range(3) for y in range(3)]+[np.array([side,(j-1)*1.7,0]) for side in [-3,3] for j in range(3)]


class Extremal(Lesson):
  def construct(self):
    with self.say('g29'):
      rec=DATA['W5'];pts=w5_positions();g=network(15,rec['edges'],pts)
      self.play(FadeIn(g[1][:5]),*[Create(e) for e,(i,j) in zip(g[0],rec['edges']) if j<5],run_time=2)
      self.play(FadeIn(g[1][5:]),*[Create(e) for e,(i,j) in zip(g[0],rec['edges']) if i<5<=j],run_time=3)
      self.play(*[Create(e) for e,(i,j) in zip(g[0],rec['edges']) if i>=5],run_time=3)
      self.play(g[1][5].animate.set_color(SECONDARY),g[1][0].animate.set_color(SECONDARY),g[1][1].animate.set_color(SECONDARY))
      self.cap('$W_5$: five points, ten pairs, 45 edges');self.source('CFJK (2013), graph G4; pair {0,1} and its points highlighted')
    with self.say('g30'):
      self.clear();rec=DATA['X'];pts=x_positions();g=network(15,rec['edges'],pts)
      self.play(FadeIn(g[1][:9]),*[Create(e) for e,(i,j) in zip(g[0],rec['edges']) if j<9],run_time=2)
      self.play(FadeIn(g[1][9:]),*[Create(e) for e,(i,j) in zip(g[0],rec['edges']) if i<9<=j],run_time=3)
      self.play(*[Create(e) for e,(i,j) in zip(g[0],rec['edges']) if i>=9],run_time=3)
      self.cap('$X$: nine grid points, six line dots, 42 edges');self.source('CFJK (2013), graph G5; affine-plane construction in paper Section 5')
    with self.say('g31'):
      self.clear();a=network(15,DATA['W5']['edges'],w5_positions()).scale(.68).shift(LEFT*3.1)
      b=network(15,DATA['X']['edges'],x_positions()).scale(.68).shift(RIGHT*3.1)
      self.play(Create(a),Create(b),run_time=3)
      self.play(Write(eq('(11,0,4)',[0,2.7,0],1.2,ACCENT)))
      self.cap('Exactly two reduced graphs attain eleven positive eigenvalues')
      self.source('Exact inertia; differing degree patterns; rank15 cores have no reduced extensions')
    with self.say('g32'):
      self.clear();self.play(Write(lab('Charles, Farber, Johnson and Kennedy-Shaffer',[0,1.7,0],.85)),run_time=3)
      self.play(Write(lab('2013: examples and underlying numerical bound',[0,.7,0],.85)),run_time=2)
      self.play(Write(lab('Elphick and colleagues, 2026: inertia identity',[0,-.5,0],.8)),run_time=2)
      self.cap('Retained increment: uniqueness and independent verification')
      self.source('CFJK Theorem 4.7; Elphick et al. Section 2; final review credit correction')


class Scope(Lesson):
  def construct(self):
    with self.say('g33'):
      self.play(Write(eq(r'30=4+22+4',UP*1.2,1.5,PRIMARY)),run_time=2)
      self.play(Write(eq(r'15=11+0+4',DOWN*.5,1.5,ACCENT)),run_time=2)
      self.cap('Total dots = positive + zero + negative');self.source('Reduced size record versus positive-inertia record; different extremal graphs')
    with self.say('g34'):
      self.clear();labels=VGroup(lab('Lemmas',LEFT*4.5,.9),lab('Enumeration',ORIGIN,.9),lab('Reconstruction',RIGHT*4.5,.9))
      self.play(Write(labels),run_time=3)
      self.play(GrowArrow(Arrow([-3.3,0,0],[-1.8,0,0],buff=.1,color=ACCENT)),GrowArrow(Arrow([1.8,0,0],[2.7,0,0],buff=.1,color=ACCENT)),run_time=2)
      self.cap('Computer-assisted proof; no proof-assistant formalisation')
      self.source('Two independent implementations; exact integer/rational decisions; full proof in paper')
    with self.say('g35'):
      self.clear();self.play(Write(eq('2,\ 6,\ 14,\ 30,\ ?',[0,.5,0],1.7)),run_time=3)
      self.cap('Five negatives: the maximum-size case remains open')
      self.source('Known values through k=4; selected failed extensions do not prove completeness for k=5')
    with self.say('g36'):
      self.clear();self.play(Write(lab('Reduced graphs with four negative eigenvalues',[0,2,0],.87)),Write(lab('have at most thirty vertices',[0,1.25,0],.95)),run_time=2)
      self.play(Write(lab('Valyu Research, 2026',[0,.1,0],.9)))
      self.play(Write(lab('maths/combinatorics/spectral-graph-theory/',[0,-.9,0],.65)),Write(lab('four-negative-eigenvalues',[0,-1.5,0],.75)))
      self.play(Write(lab('Narration uses a synthetic voice.',[0,-2.7,0],.55,MUTED)))
