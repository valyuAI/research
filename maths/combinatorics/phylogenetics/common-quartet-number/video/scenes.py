from manim import *
from vrvideo import *
import json
from pathlib import Path

SCENES = ['FourLeaves', 'Witness', 'Separating', 'GridArgument', 'Budget', 'ManyTrees', 'Evidence']


def lab(s, pos, scale=.8, color=INK):
  return Tex(s, color=color).scale(scale).move_to(pos)


def quartet(names=('a','b','c','d'), center=ORIGIN, size=1., color=PRIMARY):
  pts=[np.array(p)*size+center for p in [(-1.8,.9,0),(-1.8,-.9,0),(1.8,.9,0),(1.8,-.9,0),(-.65,0,0),(.65,0,0)]]
  edges=VGroup(*[Line(pts[a],pts[b],color=color,stroke_width=3) for a,b in [(0,4),(1,4),(4,5),(5,2),(5,3)]])
  dots=VGroup(*[Dot(p,radius=.065,color=color) for p in pts])
  labels=VGroup(*[MathTex(str(n)).scale(.8).move_to(p+(LEFT if i<2 else RIGHT)*.3) for i,(n,p) in enumerate(zip(names,pts))])
  return VGroup(edges,dots,labels)


def witness():
  data=json.loads((Path(__file__).parent/'witness-data.json').read_text())
  points={k:np.array(v) for k,v in data['positions'].items()}
  edges=VGroup(*[Line(points[a],points[b],color=MUTED,stroke_width=2.5) for a,b in data['edges']])
  labels={}
  for i in range(1,14):
    pos=points[f'l{i}']
    color=[PRIMARY,ACCENT,WARM,EXTRA,MUTED][(i-1)//3]
    labels[i]=MathTex(str(i),color=color).scale(.75).move_to(pos*1.13)
  return edges,labels,points


def grid(values, colors=(PRIMARY,ACCENT), center=ORIGIN):
  cells=VGroup()
  for row in range(2):
    for col in range(2):
      p=center+np.array([(col-.5)*3,(.5-row)*1.8,0])
      rect=Rectangle(width=2.7,height=1.5,stroke_color=MUTED,stroke_width=1.5).move_to(p)
      num=MathTex(str(values[row][col]),color=colors[row]).scale(1.25).move_to(p)
      cells.add(VGroup(rect,num))
  return cells


class FourLeaves(NarratedScene):
  def construct(self):
    q=quartet(size=1.5)
    with self.say('q01'):
      self.play(Create(q),run_time=2)
      self.play(Indicate(q[0][2],color=SECONDARY),run_time=2)
      self.play(FadeIn(caption('$ab\\mid cd$: the middle edge separates the pairs')))
    with self.say('q02'):
      self.play(*[FadeOut(m) for m in list(self.mobjects)])
      qs=VGroup(*[quartet(ns,np.array([x,0,0]),.8) for ns,x in [(('a','b','c','d'),-4.5),(('a','c','b','d'),0),(('a','d','b','c'),4.5)]])
      self.play(LaggedStart(*[Create(x) for x in qs],lag_ratio=.4),run_time=3)
      self.play(FadeIn(caption('Three possible quartet pairings')))
    with self.say('q03'):
      self.play(FadeIn(title('Three trees: when must some quartet agree?',.78)))
      self.play(Indicate(qs,color=SECONDARY),run_time=2)
    with self.say('q04'):
      self.play(*[FadeOut(m) for m in list(self.mobjects)])
      q=quartet(size=1.45)
      # Subdivide the first leaf edge; attach a fifth leaf, preserving binary degrees.
      p=(q[0][0].get_start()+q[0][0].get_end())/2
      extra=VGroup(Line(p,p+UP*1.2,color=MUTED),Dot(p+UP*1.2,color=MUTED),lab('e',p+UP*1.6,.8,MUTED))
      self.play(Create(q),Create(extra),run_time=2)
      self.play(q[0].animate.set_color(SECONDARY),run_time=1.5)
    with self.say('q05'):
      self.play(FadeOut(extra),run_time=2)
      self.play(q[0].animate.set_color(PRIMARY))
      self.play(FadeIn(caption('Keep four leaves and their connecting paths')))


class Witness(NarratedScene):
  def construct(self):
    edges,labels,positions=witness()
    with self.say('q06'):
      self.play(Create(edges),LaggedStart(*[FadeIn(x) for x in labels.values()],lag_ratio=.08),run_time=3)
      tag=title('The actual 13-leaf witness: $T$',.85)
      self.play(Write(tag))
    with self.say('q07'):
      def inverse(i):return i if i==13 else 3*((i-1)//3)+(i-2)%3+1
      self.play(*[x.animate.move_to(positions[f'l{inverse(i)}']*1.13) for i,x in labels.items()],run_time=3)
      self.play(Transform(tag,title('Same branches, relabelled: $\\sigma T$',.85)))
      self.wait(1)
      self.play(*[x.animate.move_to(positions[f'l{inverse(inverse(i))}']*1.13) for i,x in labels.items()],run_time=3)
      self.play(Transform(tag,title('Rotate again: $\\sigma^2 T$',.85)))
    with self.say('q08'):
      self.play(*[x.animate.move_to(positions[f'l{i}']*1.13) for i,x in labels.items()],Transform(tag,title('$T$: keep leaves 1, 4, 7 and 13',.85)),run_time=2)
      self.play(*[labels[i].animate.set_color(SECONDARY) for i in [1,4,7,13]])
      data=json.loads((Path(__file__).parent/'witness-data.json').read_text())
      adjacency={p:[] for p in positions}
      for a,b in data['edges']:
        adjacency[a].append(b)
        adjacency[b].append(a)
      kept=set()
      for target in ['l4','l7','l13']:
        queue=[('l1',[])]
        seen={'l1'}
        while queue:
          node,path=queue.pop(0)
          if node==target:
            kept.update(path)
            break
          for other in adjacency[node]:
            if other not in seen:
              seen.add(other)
              queue.append((other,path+[tuple(sorted((node,other)))]))
      self.play(*[e.animate.set_color(SECONDARY).set_opacity(1) if tuple(sorted(ab)) in kept else e.animate.set_opacity(.12) for e,ab in zip(edges,data['edges'])],run_time=1.5)
      self.wait(.5)
      self.play(*[FadeOut(m) for m in list(self.mobjects)])
      qs=VGroup(*[quartet(ns,np.array([x,0,0]),.75) for ns,x in [((4,7,1,13),-4.5),((1,4,7,13),0),((1,4,7,13),4.5)]])
      tags=VGroup(*[MathTex(s).scale(.85).move_to([x,1.9,0]) for s,x in [('T',-4.5),(r'\sigma T',0),(r'\sigma^2T',4.5)]])
      self.play(Create(qs),Write(tags),run_time=3)
      self.play(FadeIn(caption('Not all three answers match',color=SECONDARY)))
    with self.say('q09'):
      self.play(Indicate(qs[1]),Indicate(qs[2]),run_time=2)
      self.play(FadeIn(title('Pairwise agreement is allowed',.85)))
    with self.say('q10'):
      self.play(*[FadeOut(m) for m in list(self.mobjects)])
      counter=Integer(0,color=PRIMARY).scale(1.6).move_to(LEFT*.9)
      total=MathTex('/715').scale(1.6).move_to(RIGHT*1.5)
      self.play(FadeIn(counter),Write(total))
      self.play(ChangeDecimalToValue(counter,715),run_time=4,rate_func=linear)
      self.play(FadeIn(title('0 common quartets',.95)),FadeIn(caption('Exhaustive verification, summarized here')))
    with self.say('q11'):
      self.play(*[FadeOut(m) for m in list(self.mobjects)])
      self.play(Write(MathTex(r'13\text{ can fail}\quad\Longrightarrow\quad h(3)\ge14').scale(1.05)),run_time=3)
      self.play(FadeIn(caption('Next: prove every triple on 14 succeeds')))


class Separating(NarratedScene):
  def construct(self):
    q=quartet(('x',r'x\prime','y',r'y\prime'),size=1.4)
    with self.say('q12'):
      self.play(Create(q),run_time=2)
      self.play(Create(DashedLine(UP*1.8,DOWN*1.8,color=SECONDARY)),run_time=1)
      self.play(q[1][0:2].animate.set_color(PRIMARY),q[1][2:4].animate.set_color(ACCENT))
      self.play(FadeIn(caption('One edge separates $X$ from $Y$')))
    with self.say('q13'):
      self.play(*[FadeOut(m) for m in list(self.mobjects)])
      left=VGroup(*[Dot([-.9-(i%3)*.8,1-(i//3)*.8,0],color=PRIMARY,radius=.12) for i in range(6)])
      right=VGroup(*[Dot([.9+(i%3)*.8,1-(i//3)*.8,0],color=ACCENT,radius=.12) for i in range(8)])
      self.play(FadeIn(left),FadeIn(right),Create(DashedLine(UP*2,DOWN*2,color=SECONDARY)),run_time=2)
      self.play(Write(title('$14/3>4$: at least 5 on each side',.85)))
      self.play(FadeIn(caption('Illustrative balanced split: 6 and 8')))
    with self.say('q14'):
      self.play(*[FadeOut(m) for m in list(self.mobjects)])
      blue=VGroup(*[Dot([-2+i*.6,.5,0],color=PRIMARY,radius=.15) for i in range(3)])
      teal=VGroup(*[Dot([.9+i*.6,.5,0],color=ACCENT,radius=.15) for i in range(4)])
      self.play(FadeIn(blue),FadeIn(teal),Create(DashedLine(UP*2,DOWN*2,color=SECONDARY)),run_time=2)
      self.play(FadeIn(title('Separated in the first two trees',.85)),FadeIn(caption('Keep 3 blue leaves and 4 teal leaves')))
    with self.say('q15'):
      self.play(*[FadeOut(m) for m in list(self.mobjects)])
      formula=MathTex('135(2002+3003+3432)').scale(1.1).shift(UP*.7)
      result=MathTex('=1{,}138{,}995').scale(1.2).shift(DOWN*.6)
      self.play(Write(formula),run_time=2)
      self.play(Write(result),run_time=2)
      self.play(FadeIn(caption('All shapes and colourings. Zero failures.',color=ACCENT)))


class GridArgument(NarratedScene):
  def construct(self):
    cells=grid([[2,1],[1,3]])
    with self.say('q16'):
      self.play(Create(cells),run_time=2)
      headers=VGroup(lab('$Z$',[-1.5,2.1,0]),lab('$W$',[1.5,2.1,0]),lab('$X$',[-3.4,.9,0],color=PRIMARY),lab('$Y$',[-3.4,-.9,0],color=ACCENT))
      self.play(Write(headers))
      self.play(FadeIn(caption('Rows: old sets. Columns: the third tree\'s cut')))
    with self.say('q17'):
      self.play(Create(boxed(cells[0],SECONDARY)),Create(boxed(cells[3],SECONDARY)),run_time=2)
      self.play(Indicate(cells[0][1]),Indicate(cells[3][1]),run_time=2)
    with self.say('q18'):
      self.play(*[FadeOut(m) for m in list(self.mobjects)])
      q=quartet(('x_1','x_2','y_1','y_2'),size=1.4)
      self.play(Create(q),run_time=2)
      self.play(Indicate(q[0][2],color=ACCENT),run_time=2)
      self.play(FadeIn(caption('Two from each diagonal cell: one common quartet',color=ACCENT)))
    with self.say('q19'):
      self.play(*[FadeOut(m) for m in list(self.mobjects)])
      cells=grid([['A','B'],['C','D']])
      self.play(Create(cells))
      for ids in [(0,1),(0,2),(3,1),(3,2)]:
        marks=VGroup(*[boxed(cells[i],WARN) for i in ids])
        self.play(Create(marks),run_time=.5)
        self.wait(.65)
        self.play(FadeOut(marks),run_time=.3)
      self.play(FadeIn(caption('Two failed diagonals force a row or column $\\le2$',color=WARN)))
    with self.say('q20'):
      self.play(*[FadeOut(m) for m in list(self.mobjects)])
      self.play(Write(MathTex(r'14\le h(3)\le14').scale(1.5)),run_time=2)
      self.play(Transform(self.mobjects[0],MathTex('h(3)=14',color=ACCENT).scale(1.8)),run_time=2)


class Budget(NarratedScene):
  def construct(self):
    with self.say('q21'):
      blue=Rectangle(width=4,height=.6,color=PRIMARY,fill_opacity=.6).shift(UP*.6)
      teal=Rectangle(width=6,height=.6,color=ACCENT,fill_opacity=.6).shift(DOWN*.6)
      self.play(GrowFromEdge(blue,LEFT),GrowFromEdge(teal,LEFT),run_time=2)
      self.play(blue.animate.stretch(.6,0),teal.animate.stretch(.55,0),run_time=2)
      self.play(FadeIn(caption('Keep two separated sets through each new tree')))
    with self.say('q22'):
      self.play(*[FadeOut(m) for m in list(self.mobjects)])
      eq=MathTex(r'\Psi(a,d)=\min\{ad,\ 2a^2,\ 2d^2\}').scale(1.1)
      self.play(Write(eq),run_time=3)
      self.play(FadeIn(caption('Budget $>2$ forces $a,d\\ge2$')))
    with self.say('q23'):
      self.play(Transform(eq,MathTex(r'\Psi(16,32)=\min\{512,512,2048\}=512').scale(.95)),run_time=3)
      self.play(FadeIn(title('A concrete budget calculation',.85)))
    with self.say('q24'):
      self.play(*[FadeOut(m) for m in list(self.mobjects)])
      cells=grid([[7,9],[11,21]]).shift(UP*.3)
      self.play(Create(cells),run_time=2)
      values=VGroup(MathTex(r'\Psi(7,21)=98').scale(.8).move_to([-3,-2.2,0]),MathTex(r'\Psi(9,11)=99').scale(.8).move_to([3,-2.2,0]))
      self.play(Create(boxed(cells[0],SECONDARY)),Create(boxed(cells[3],SECONDARY)),Write(values[0]),run_time=2)
      self.play(Create(boxed(cells[1],ACCENT)),Create(boxed(cells[2],ACCENT)),Write(values[1]),run_time=2)
    with self.say('q25'):
      self.play(Indicate(values[1],color=ACCENT),run_time=1.5)
      self.play(FadeIn(title('$c=(7-\\sqrt{13})/18\\approx0.18858$',.85)))
      self.play(FadeIn(caption('$99\\ge512c\\approx96.553$',color=ACCENT)))
    with self.say('q25a'):
      self.play(*[FadeOut(m) for m in list(self.mobjects)])
      cells=grid([['xa','(1-x)a'],['yd','(1-y)d']])
      self.play(Create(cells),run_time=2)
      self.play(Write(title('$X$ smaller, $Y$ larger: $a\\le d$',.85)))
      self.play(FadeIn(caption('Balance $Y$ again: $1/3\\le y\\le2/3$')))
    with self.say('q25b'):
      self.play(*[FadeOut(m) for m in list(self.mobjects)])
      size=MathTex(r'(a,d)\ \longrightarrow\ (1,r),\qquad 1\le r\le2').scale(1.05).shift(UP*.8)
      cut=MathTex(r'(x,y)\ \longleftrightarrow\ (1-x,1-y)').scale(1.05).shift(DOWN*.6)
      self.play(Write(size),run_time=3)
      self.play(Write(cut),run_time=2)
      self.play(FadeIn(caption('Orient the cut so $x+y\\le1$')))
    with self.say('q25c'):
      self.play(*[FadeOut(m) for m in list(self.mobjects)])
      t=(np.sqrt(13)-1)/6
      c=t*t
      axes=Axes(x_range=[0,2/3,.2],y_range=[0,.45,.1],x_length=7,y_length=3.5,tips=False,axis_config={'color':MUTED}).shift(LEFT*2+UP*.25)
      rising=axes.plot(lambda x:x*x,x_range=[0,2/3],color=PRIMARY)
      falling=axes.plot(lambda x:(1-x)/3,x_range=[0,2/3],color=ACCENT)
      labels=VGroup(MathTex('x^2',color=PRIMARY).scale(.8).move_to(axes.c2p(.62,.42)),MathTex(r'(1-x)/3',color=ACCENT).scale(.8).move_to(axes.c2p(.13,.34)))
      self.play(Create(axes),Create(rising),Create(falling),Write(labels),run_time=3)
      crossing=Dot(axes.c2p(t,c),color=SECONDARY,radius=.09)
      guide=DashedLine(axes.c2p(t,0),axes.c2p(t,c),color=SECONDARY)
      self.play(Create(guide),FadeIn(crossing),Write(MathTex('t',color=SECONDARY).scale(.8).move_to(axes.c2p(t,-.045))),run_time=1.5)
      formulas=VGroup(MathTex(r't=\frac{\sqrt{13}-1}{6}').scale(.85),MathTex(r'c=t^2').scale(1.05),MathTex(r'x\ge t:\ \text{diagonal 1}',color=PRIMARY).scale(.7),MathTex(r'x<t:\ \text{diagonal 2}',color=ACCENT).scale(.7)).arrange(DOWN,buff=.4).move_to([3.8,.3,0])
      self.play(Write(formulas),run_time=3)
      self.play(FadeIn(title('Where the two cases meet',.85)),FadeIn(caption('The proof checks all three terms in each budget')))
    with self.say('q26'):
      self.play(*[FadeOut(m) for m in list(self.mobjects)])
      sharp=MathTex(r'\Psi_{\rm kept}\ge c\Psi_{\rm before}').scale(1.25).shift(UP*1.1)
      checked=Tex('Sharp $c$: independently reviewed written proof').scale(.75).shift(DOWN*.1)
      lean=Tex('Lean: sharp inequality and equality example').scale(.8).shift(DOWN*1.2)
      self.play(Write(sharp),run_time=2)
      self.play(FadeIn(checked),FadeIn(lean),run_time=2)
      self.play(FadeIn(caption('Optimality only for this real-variable inequality',color=SECONDARY)))


class ManyTrees(NarratedScene):
  def construct(self):
    with self.say('q27'):
      start=MathTex(r'\frac{2n^2}{9}c^{k-1}>2').scale(1.2).shift(UP*.9)
      end=MathTex(r'h(k)\le\left\lfloor3\beta^{k-1}\right\rfloor+1').scale(1.2).shift(DOWN*.9)
      self.play(Write(start),run_time=3)
      self.play(Write(end),run_time=3)
      self.play(FadeIn(caption('$\\beta=1/\\sqrt c=(1+\\sqrt{13})/2\\approx2.3028$')))
    with self.say('q28'):
      self.play(*[FadeOut(m) for m in list(self.mobjects)])
      table=MathTable([['1','2','3','4','5','6'],['4','7','16','37','85','195']],row_labels=[MathTex('k'),Tex('bound')],include_outer_lines=False,h_buff=.7,v_buff=.7).scale(.8)
      self.play(Create(table),run_time=2)
      self.wait(3)
      self.play(FadeOut(table))
      a=MathTex(r'k=3:\quad 16\ \longrightarrow\ 14').scale(1.3).shift(UP*.8)
      b=MathTex(r'k=4:\quad 37\ \longrightarrow\ 28').scale(1.3).shift(DOWN*.8)
      self.play(Write(a),Write(b),run_time=3)
      self.play(FadeIn(caption('General guarantee $\\longrightarrow$ sharper small-case bound')))
    with self.say('q29'):
      self.play(*[FadeOut(m) for m in list(self.mobjects)])
      self.play(Write(title('4 trees, 22 leaves: 0 common quartets',.8)))
      self.play(Write(MathTex(r'\binom{22}{4}=7315').scale(1.2).shift(UP*.7)),run_time=2)
      self.play(Write(MathTex(r'23\le h(4)\le28',color=SECONDARY).scale(1.4).shift(DOWN*.8)),run_time=2)
      self.play(FadeIn(caption('The exact value is not settled')))
    with self.say('q30'):
      self.play(*[FadeOut(m) for m in list(self.mobjects)])
      self.play(Write(MathTex(r'2^k+2\le h(k)\le\left\lfloor3\beta^{k-1}\right\rfloor+1').scale(1.05)),run_time=3)
      self.play(FadeIn(title('Lower bound credited to Snir and Yuster',.83)))
      self.play(FadeIn(caption('New general upper bound; exact $h(3)=14$')))


class Evidence(NarratedScene):
  def construct(self):
    with self.say('q31'):
      q=quartet(size=1.25)
      self.play(Create(q),run_time=2)
      self.play(FadeIn(title('Pairing $\\rightarrow$ separation $\\rightarrow$ budget',.8)))
      self.play(FadeIn(caption('Guaranteed local agreement')))
    with self.say('q32'):
      self.play(*[FadeOut(m) for m in list(self.mobjects)])
      self.play(Write(title('Correctness: high. Priority search: bounded.',.78)))
      self.play(Write(MathTex(r'23\le h(4)\le28').scale(1.5)))
      self.play(FadeIn(caption('Paused 23-leaf searches supply no further bound',color=SECONDARY)))
    with self.say('q33'):
      self.play(*[FadeOut(m) for m in list(self.mobjects)])
      end=VGroup(Tex('Three phylogenetic trees on fourteen leaves'),Tex('always share a quartet'),Tex('Valyu Research, 2026',color=ACCENT),Tex(r'\texttt{maths/combinatorics/phylogenetics/}'),Tex(r'\texttt{common-quartet-number/}'),Tex('Narration uses a synthetic voice.',color=MUTED)).arrange(DOWN,buff=.35)
      for i,x in enumerate(end):x.scale(.8 if i<3 else .58)
      self.play(FadeIn(end),run_time=2)
