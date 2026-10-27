from manim import *
from vrvideo import *
import itertools
import math

SCENES = ['RankAndRace', 'LocalOverlap', 'CancelMarks', 'Interleavings', 'Tail', 'UniformRange', 'Certificates', 'Conclusion']


def text_at(s,pos,scale=.8,color=INK):
  return Tex(s,color=color).scale(scale).move_to(pos)


def bars(values):
  xs=[(i-(len(values)-1)/2)*2 for i in range(len(values))]
  bs=VGroup(*[Rectangle(width=.8,height=v*5,color=PRIMARY,fill_opacity=.65).move_to([x,-1.6+v*2.5,0]) for x,v in zip(xs,values)])
  labels=VGroup(*[MathTex(f'{v:.2f}').scale(.85).move_to([x,-2.2,0]) for x,v in zip(xs,values)])
  return bs,labels


def chain(order,y,color=PRIMARY):
  xs=[-4,-2,0,2,4]
  dots=VGroup(*[Dot([x,y,0],color=ACCENT if k==0 else WARM if k==4 else color,radius=.11) for x,k in zip(xs,order)])
  labels=VGroup(*[MathTex(f'x_{k}').scale(.9).next_to(d,DOWN,buff=.2) for k,d in zip(order,dots)])
  signs=VGroup(*[MathTex('<').scale(.9).move_to([(xs[i]+xs[i+1])/2,y,0]) for i in range(4)])
  return VGroup(dots,labels,signs)


class RankAndRace(NarratedScene):
  def construct(self):
    bs,labels=bars([.2,.4,.6,.1])
    with self.say('p01'):
      self.play(LaggedStart(*[GrowFromEdge(x,DOWN) for x in bs],lag_ratio=.2),Write(labels),run_time=2)
      ranks=VGroup(*[MathTex(str(k),color=SECONDARY).scale(1.15).move_to(l) for k,l in zip([2,3,4,1],labels)])
      self.play(Transform(labels,ranks),run_time=3)
      self.play(FadeIn(caption('Relative order: $2341$')))
    with self.say('p02'):
      self.play(FadeIn(title('First pattern to appear wins',.9)))
      self.play(Indicate(labels,color=SECONDARY),run_time=2)
    with self.say('p03'):
      self.play(*[FadeOut(m) for m in list(self.mobjects)])
      digits=VGroup(*[MathTex(str(n)).scale(1.7).move_to([(i-1.5)*1.7,0,0]) for i,n in enumerate([2,3,4,1])])
      self.play(Write(digits),run_time=2)
      self.play(digits[3].animate(path_arc=-PI/2).move_to(digits[0].get_center()),*[digits[i].animate.shift(RIGHT*1.7) for i in range(3)],run_time=3)
      self.play(FadeIn(title('Move the last symbol to the front',.85)),FadeIn(caption('$2341\\longrightarrow1234$: right rotation',color=ACCENT)))
    with self.say('p04'):
      self.play(*[FadeOut(m) for m in list(self.mobjects)])
      bs,labels=bars([.1,.2,.4,.6,.15])
      window=Rectangle(width=7.3,height=4.3,color=ACCENT).move_to([-1,-.45,0])
      self.play(Create(bs),Write(labels),Create(window),run_time=2)
      result=title('$B=1234$ appears first',.95)
      self.play(Write(result))
      self.wait(1)
      self.play(window.animate.shift(RIGHT*2).set_color(SECONDARY),run_time=2)
      self.play(Transform(result,title('$A=2341$ would arrive one draw later',.85)))
    with self.say('p05'):
      self.play(*[FadeOut(m) for m in list(self.mobjects)])
      points=VGroup(*[Dot([x,y,0],radius=.11,color=PRIMARY) for x,y in [(-4,.7),(-2,-.2),(0,1.1),(2,.1),(4,-.6)]])
      self.play(LaggedStart(*[FadeIn(p) for p in points],lag_ratio=.4),run_time=3)
      self.play(FadeIn(title('Independent draws; one continuous distribution',.75)),FadeIn(caption('Only ranks matter; ties have probability zero')))
    with self.say('p06'):
      self.play(*[FadeOut(m) for m in list(self.mobjects)])
      cards=VGroup(*[MathTex(''.join(map(str,p)),color=ACCENT if p==(1,2,3,4) else SECONDARY if p==(2,3,4,1) else MUTED).scale(.65) for p in itertools.permutations(range(1,5))]).arrange_in_grid(rows=4,cols=6,buff=(.55,.45))
      self.play(LaggedStart(*[FadeIn(c) for c in cards],lag_ratio=.04),run_time=2)
      self.play(FadeIn(title('24 orders; each has probability $1/24$',.85)),FadeIn(caption('Equal snapshots do not imply equal arrival chances')))


class LocalOverlap(NarratedScene):
  def construct(self):
    with self.say('p07'):
      base=chain([0,1,2,3,4],.8)
      base[2].remove(base[2][-1])
      base[0][-1].move_to([-4,-1.4,0])
      base[1][-1].move_to([-4,-1.9,0])
      self.play(Create(base),run_time=2)
      self.play(Create(Arrow([-3.6,-1.3,0],[-2,.6,0],color=WARM,buff=.1)))
      self.play(FadeIn(title('$B$ then $A$: two values below the shared chain',.75)))
    with self.say('p08'):
      self.play(*[FadeOut(m) for m in list(self.mobjects)])
      c1=chain([0,4,1,2,3],1)
      c2=chain([4,0,1,2,3],-1)
      self.play(Create(c1),run_time=2)
      self.play(TransformFromCopy(c1,c2),run_time=2)
      self.play(FadeIn(caption('Exactly two compatible orders')))
    with self.say('p09'):
      self.play(*[FadeOut(m) for m in list(self.mobjects)])
      c=chain([0,1,2,3,4],.7)
      self.play(Create(c),Write(title('$B$ then $B$: exactly one order',.85)),run_time=2)
      bad=MathTex(r'A\to A:\ \times\qquad A\to B:\ \times',color=WARN).scale(1.1).shift(DOWN*1.5)
      self.play(Write(bad),run_time=2)
    with self.say('p10'):
      self.play(*[FadeOut(m) for m in list(self.mobjects)])
      eq=MathTex(r'\frac{2-1}{5!}=\frac1{120}').scale(1.6)
      self.play(Write(eq),run_time=3)
      self.play(FadeIn(title('One-step signed contribution',.85)),FadeIn(caption('Not the final probability or winning advantage',color=SECONDARY)))
    with self.say('p11'):
      self.play(Transform(eq,MathTex(r'\text{one-step contribution}\ \ge\ \frac1{(k+1)!}').scale(.95)),run_time=3)


class CancelMarks(NarratedScene):
  def construct(self):
    with self.say('p12'):
      a=Circle(1.5,color=PRIMARY,fill_opacity=.12).shift(LEFT*.8)
      b=Circle(1.5,color=ACCENT,fill_opacity=.12).shift(RIGHT*.8)
      values=VGroup(text_at('4',[-1.6,0,0],1),text_at('2',[0,0,0],1,SECONDARY),text_at('3',[1.6,0,0],1))
      self.play(Create(a),Create(b),Write(values),run_time=2)
      self.play(FadeIn(title('Counting illustration',.85)),FadeIn(caption('$6+5-2=9$ distinct objects')))
    with self.say('p13'):
      self.play(*[FadeOut(m) for m in list(self.mobjects)])
      line=NumberLine(x_range=[0,6,1],length=10,include_numbers=False)
      self.play(Create(line))
      windows=VGroup(*[Line(line.n2p(i)+UP*(1+.45*j),line.n2p(i+3)+UP*(1+.45*j),color=PRIMARY,stroke_width=8) for j,i in enumerate([0,1,2])])
      self.play(LaggedStart(*[Create(w) for w in windows],lag_ratio=.4),run_time=3)
      self.play(FadeIn(caption('Overlapping marked occurrences form a cluster')))
    with self.say('p14'):
      self.play(*[FadeOut(m) for m in list(self.mobjects)])
      xs=[-3,0,3]
      dots=VGroup(*[Dot([x,.8,0],radius=.12,color=PRIMARY) for x in xs])
      tags=VGroup(*[MathTex(str(i)).scale(.9).next_to(d,UP) for i,d in enumerate(dots)])
      self.play(FadeIn(dots),Write(tags))
      two=VGroup(*[Circle(.25,color=ACCENT).move_to(dots[i]) for i in [0,2]])
      plus=MathTex('+1',color=ACCENT).scale(1.4).shift(DOWN)
      self.play(Create(two),Write(plus),run_time=2)
      self.play(Create(Circle(.25,color=SECONDARY).move_to(dots[1])),Transform(plus,MathTex('-1',color=SECONDARY).scale(1.4).shift(DOWN)),run_time=2)
      self.play(Transform(plus,MathTex('+1-1=0',color=ACCENT).scale(1.3).shift(DOWN)),run_time=2)
      self.play(FadeIn(caption('Two marks: $+1$. Three marks: $-1$. Total: $0$.')))
    with self.say('p15'):
      self.play(*[FadeOut(m) for m in list(self.mobjects)])
      self.play(Write(MathTex(r'u_j=-\!\sum_{0<t_j-t_i<k}u_i').scale(1.2)),run_time=3)
      self.play(FadeIn(title('Add nearby earlier coefficients, then negate',.8)),FadeIn(caption('Start with $u_0=-1$')))
    with self.say('p16'):
      self.play(*[FadeOut(m) for m in list(self.mobjects)])
      seq=VGroup(*[MathTex(s,color=ACCENT if s=='+1' else SECONDARY if s=='-1' else MUTED).scale(1.2).move_to([(i-2.5)*1.6,0,0]) for i,s in enumerate(['-1','+1','0','0','-1','+1'])])
      self.play(LaggedStart(*[Write(s) for s in seq],lag_ratio=.3),run_time=3)
      window=Rectangle(width=6.4,height=1.4,color=MUTED).move_to([-1.6,0,0])
      self.play(Create(window))
      self.play(window.animate.shift(RIGHT*3.2),run_time=2)
      self.play(FadeIn(caption('$k=4$: at most two nonzero terms per four starts')))


class Interleavings(NarratedScene):
  def construct(self):
    words=['BBTT','BTBT','BTTB','TBBT','TBTB','TTBB']
    def word(s):
      return VGroup(*[MathTex(c,color=PRIMARY if c=='B' else ACCENT).scale(1.1) for c in s]).arrange(RIGHT,buff=.25)
    with self.say('p17'):
      left=VGroup(MathTex('B_1',color=PRIMARY),MathTex('<'),MathTex('B_2',color=PRIMARY)).arrange(RIGHT).scale(1.2).shift(UP)
      right=VGroup(MathTex('T_1',color=ACCENT),MathTex('<'),MathTex('T_2',color=ACCENT)).arrange(RIGHT).scale(1.2).shift(DOWN)
      self.play(Write(left),Write(right),run_time=2)
      self.play(FadeIn(caption('Two ordered chains; preserve the order within each')))
    with self.say('p18'):
      self.play(*[FadeOut(m) for m in list(self.mobjects)])
      rows=VGroup(*[word(w) for w in words]).arrange_in_grid(rows=3,cols=2,buff=(2.3,.6))
      self.play(LaggedStart(*[Write(r) for r in rows],lag_ratio=.2),run_time=3)
      boxes=VGroup(*[boxed(rows[i],SECONDARY) for i,w in enumerate(words) if w[0]=='B'])
      self.play(Create(boxes))
      self.play(FadeIn(title('Example: first private entry must be blue',.8)),FadeIn(caption('3 allowed out of 6 interleavings')))
    with self.say('p19'):
      targets={w:i for i,w in enumerate(words)}
      arrows=VGroup(*[Arrow(rows[i].get_center(),rows[targets[w.translate(str.maketrans('BT','TB'))]].get_center(),color=SECONDARY,buff=.5,stroke_width=2) for i,w in enumerate(words) if w[0]=='B'])
      self.play(FadeOut(boxes),Create(arrows),run_time=2)
      self.play(*[FadeOut(m) for m in list(self.mobjects)])
      self.play(Write(MathTex(r'\text{allowed}\le\frac12\binom{2s}{s}').scale(1.4)),run_time=3)
      self.play(FadeIn(caption('Different private ranks: colour swap gives a disjoint set')))


class Tail(NarratedScene):
  def construct(self):
    with self.say('p20'):
      axis=NumberLine(x_range=[0,12,2],length=11,include_numbers=False)
      self.play(Create(axis))
      segments=VGroup(*[Line(axis.n2p(s)+UP*(.6+.45*i),axis.n2p(s+3)+UP*(.6+.45*i),color=PRIMARY,stroke_width=7) for i,s in enumerate([0,2,5])])
      labels=VGroup(*[MathTex(str(n)).scale(.7).next_to(axis.n2p(n),DOWN,buff=.2) for n in [0,2,5,8,12]])
      self.play(LaggedStart(*[Create(s) for s in segments],lag_ratio=.4),Write(labels),run_time=3)
      self.play(FadeIn(caption('A clump: successive occurrence starts differ by less than 4')))
    with self.say('p21'):
      self.play(*[FadeOut(m) for m in list(self.mobjects)])
      axis=NumberLine(x_range=[0,9,1],length=10,include_numbers=False).shift(DOWN*.7)
      ticks=VGroup(*[MathTex(str(n)).scale(.65).next_to(axis.n2p(n),DOWN,buff=.15) for n in range(10)])
      root=Line(axis.n2p(0)+UP*.65,axis.n2p(3)+UP*.65,color=MUTED,stroke_width=8)
      self.play(Create(axis),Write(ticks),Create(root))
      cand=VGroup(*[Line(axis.n2p(s)+UP*(1.2+.6*i),axis.n2p(s+3)+UP*(1.2+.6*i),color=PRIMARY,stroke_width=7) for i,s in enumerate([4,5,6])])
      self.play(LaggedStart(*[Create(c) for c in cand],lag_ratio=.5),run_time=3)
      self.play(FadeIn(title('Candidate anchor starts: 4, 5 or 6',.83)),FadeIn(caption('All use fresh observations after the old anchor ends')))
    with self.say('p22'):
      self.play(FadeOut(root),FadeOut(cand),FadeOut(axis),FadeOut(ticks))
      eq=MathTex(r'\Pr(\text{any candidate})\le 3\cdot\frac2{24}=\frac14').scale(1.05)
      self.play(Write(eq),run_time=3)
      self.play(FadeIn(text_at('Union bound',[0,-1.6,0],.9,SECONDARY)))
    with self.say('p23'):
      self.play(*[FadeOut(m) for m in list(self.mobjects)])
      self.play(Write(title('$r=2(k-1)/k!<1$',.95)))
      heights=[3, .75, .1875, .046875]
      shapes=VGroup(*[Rectangle(width=1.2,height=h,color=PRIMARY,fill_opacity=.6).move_to([-3+i*2,-1.7+h/2,0]) for i,h in enumerate(heights)])
      labels=VGroup(*[MathTex(s).scale(.8).move_to([-3+i*2,-2.3,0]) for i,s in enumerate([r'\frac14',r'\frac1{16}',r'\frac1{64}',r'\frac1{256}'])])
      self.play(LaggedStart(*[GrowFromEdge(x,DOWN) for x in shapes],lag_ratio=.3),Write(labels),run_time=3)
      self.play(FadeIn(caption('$r+r^2+r^3+\\cdots=r/(1-r)$')))
    with self.say('p24'):
      self.play(*[FadeOut(m) for m in list(self.mobjects)])
      line=Line(LEFT*5,RIGHT*5,color=MUTED)
      dots=VGroup(*[Dot([x,0,0],radius=.12,color=PRIMARY if i<3 else MUTED) for i,x in enumerate([-4.5,-3.5,-1.5,2.5,4])])
      group=SurroundingRectangle(VGroup(*dots[:3]),color=ACCENT,buff=.35)
      self.play(Create(line),FadeIn(dots),Create(group),run_time=2)
      self.play(FadeIn(title('Only the clump rooted at start zero',.85)),FadeIn(caption('Later, separate clumps do not extend this one')))


class UniformRange(NarratedScene):
  def construct(self):
    with self.say('p25'):
      nums=VGroup(*[MathTex(str(n)).scale(1.2).move_to([-5+(n-3)*1.6,0,0]) for n in range(3,10)])
      nums[0].set_color(SECONDARY)
      for x in nums[1:5]:x.set_color(ACCENT)
      for x in nums[5:]:x.set_color(PRIMARY)
      self.play(LaggedStart(*[Write(x) for x in nums],lag_ratio=.2),run_time=2)
      labels=VGroup(text_at('known',[-5,-1,0],.7,SECONDARY),text_at('exact certificates',[-1,-1,0],.75,ACCENT),text_at('uniform proof',[3.8,-1,0],.75,PRIMARY))
      self.play(Write(labels))
      self.play(FadeIn(title('Pattern lengths',.9)),FadeIn(caption('3: Elizalde--Lin. 4--7: finite. $8,9,\\ldots$: analytic.')))
    with self.say('p26'):
      self.play(*[FadeOut(m) for m in list(self.mobjects)])
      bar=Rectangle(width=10,height=.7,color=ACCENT,fill_opacity=.6).shift(UP*.6)
      self.play(GrowFromEdge(bar,LEFT),Write(title('Scaled positive starting amount: 1',.85)),run_time=2)
      short=256699/300300
      tail=144/2879
      remainder=1-short-tail-1/3360
      cut1=Rectangle(width=10*short,height=.7,color=WARN,fill_opacity=1).align_to(bar,LEFT).set_y(.6)
      cut2=Rectangle(width=10*(tail+1/3360),height=.7,color=WARM,fill_opacity=1).next_to(cut1,RIGHT,buff=0)
      self.play(FadeIn(cut1),run_time=2)
      self.play(FadeIn(cut2),run_time=1)
      exact=MathTex(r'1-\frac{256699}{300300}-\frac{144}{2879}-\frac1{3360}>0').scale(.85).shift(DOWN*.7)
      self.play(Write(exact),run_time=2)
      self.play(FadeIn(caption('Remaining scaled margin: $0.094876\\ldots>0$',color=ACCENT)))
    with self.say('p27'):
      self.play(*[FadeOut(m) for m in list(self.mobjects)])
      eq=MathTex(r'\Pr(B\text{ first})-\tfrac12=K D,\qquad K>0').scale(1.0)
      self.play(Write(eq),run_time=3)
      self.play(FadeIn(title('A proved first-occurrence identity',.85)),FadeIn(caption('$D>0$ determines the sign; it is not the probability itself')))


class Certificates(NarratedScene):
  def construct(self):
    with self.say('p28'):
      line=NumberLine(x_range=[0,1, .25],length=10,include_numbers=False)
      self.play(Create(line))
      lower=line.n2p(.35); upper=line.n2p(.75)
      bound=Line(lower,upper,color=ACCENT,stroke_width=9)
      self.play(Create(bound),FadeIn(Dot(lower,color=ACCENT)),run_time=2)
      self.play(FadeIn(title('Partial sum minus worst possible tail stays positive',.72)),FadeIn(caption('Illustration of the certificate test: $D_S>T$')))
      self.play(FadeIn(MathTex('0').scale(.8).next_to(line.n2p(0),DOWN)))
    with self.say('p29'):
      self.play(*[FadeOut(m) for m in list(self.mobjects)])
      table=MathTable([['4','>3/4','5/12'],['5','>9/10','4/35'],['6','>49/50','28/71'],['7','>99/100','32/419']],col_labels=[Tex('length'),Tex('partial sum'),Tex('tail bound')],include_outer_lines=False,h_buff=1.1,v_buff=.35).scale(.72)
      self.play(Write(table),run_time=3)
      self.play(FadeIn(title('Exact bounds, scaled by $(k+1)!$',.85)))
      self.play(FadeIn(caption('Every partial sum exceeds its entire omitted tail',color=ACCENT)))
    with self.say('p30'):
      self.play(*[FadeOut(m) for m in list(self.mobjects)])
      cases=MathTex('12+60+360+2520=2952').scale(1.2).shift(UP*.7)
      complement=MathTex(r'1234\longleftrightarrow4321').scale(1.1).shift(DOWN*.9)
      self.play(Write(cases),Write(complement),run_time=3)
      self.play(FadeIn(title('Independent integer reconstructions agree',.8)),FadeIn(caption('Reflect ranks; preserve race probabilities')))
    with self.say('p31'):
      self.play(*[FadeOut(m) for m in list(self.mobjects)])
      total=Rectangle(width=10,height=.7,color=MUTED).shift(UP*.5)
      original=Rectangle(width=10*2947998300006576/math.factorial(18),height=.7,color=PRIMARY,fill_opacity=.6).align_to(total,LEFT).set_y(.5)
      unresolved=Rectangle(width=10*12132147428205/math.factorial(18),height=.7,color=SECONDARY,fill_opacity=.9).next_to(original,RIGHT,buff=0)
      self.play(Create(total),FadeIn(original),FadeIn(unresolved),run_time=2)
      self.play(Write(title('$A=132$, $B=213$: horizon 18',.85)))
      self.play(Write(MathTex(r'\Pr(A\text{ first})\le\frac{W_A+R}{18!}<47\%<50\%').scale(.95).shift(DOWN*.9)),run_time=3)
      self.play(FadeIn(caption('Worst representative shown; unresolved races assigned to $A$')))


class Conclusion(NarratedScene):
  def construct(self):
    with self.say('p32'):
      theorem=MathTex(r'a_1\cdots a_k\longrightarrow a_k a_1\cdots a_{k-1}').scale(1.2).shift(UP*.8)
      prob=MathTex(r'\Pr(\text{rotation wins})>\frac12\qquad(k\ge3)',color=ACCENT).scale(1.1).shift(DOWN*.9)
      self.play(Write(theorem),Write(prob),run_time=3)
      self.play(FadeIn(caption('Independent observations; common continuous distribution')))
    with self.say('p33'):
      self.play(*[FadeOut(m) for m in list(self.mobjects)])
      self.play(Write(Tex('A winning reply need not be the best reply').scale(.95)),run_time=3)
      self.play(FadeIn(caption('Optimal replies and all exact probabilities remain outside scope')))
    with self.say('p34'):
      self.play(*[FadeOut(m) for m in list(self.mobjects)])
      rec=VGroup(Tex('Shared observations'),MathTex(r'\Downarrow'),Tex('Directional overlap advantage'),MathTex(r'\Downarrow'),Tex('Cancellation and tail control')).arrange(DOWN,buff=.25).scale(.85)
      self.play(LaggedStart(*[FadeIn(x) for x in rec],lag_ratio=.25),run_time=3)
      self.play(FadeIn(caption('Correctness: high. Originality: moderate.',.75)))
    with self.say('p35'):
      self.play(*[FadeOut(m) for m in list(self.mobjects)])
      end=VGroup(Tex('Right rotation wins Penney\'s game'),Tex('for permutations'),Tex('Valyu Research, 2026',color=ACCENT),Tex(r'\texttt{maths/probability/competing-patterns/}'),Tex(r'\texttt{rotation-wins-penney/}'),Tex('Narration uses a synthetic voice.',color=MUTED)).arrange(DOWN,buff=.35)
      for i,x in enumerate(end):x.scale(.85 if i<3 else .58)
      self.play(FadeIn(end),run_time=2)
