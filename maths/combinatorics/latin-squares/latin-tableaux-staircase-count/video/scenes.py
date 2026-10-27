from manim import *
from vrvideo import *
from itertools import permutations

SCENES=['Rules','Grow','ForcedMiddle','FourWays','Invariants','Induction','Scope']
BASE5=[[4,5,2,1,3],[3,1,4,2],[2,3,1],[1,2,3]]
BASE6=[[5,4,6,3,1,2],*BASE5]
BASE7=[[6,7,5,4,2,1,3],*BASE6]
COLOURS=[INK,PRIMARY,ACCENT,WARM,EXTRA,SECONDARY,GREEN_C,BLUE_D,RED_C,TEAL_D,GOLD_C]


def formula(s,pos=ORIGIN,scale=1.0,color=INK):
  return MathTex(s,color=color).scale(scale).move_to(pos)


def tableau(rows, size=.76, centre=ORIGIN):
  group=VGroup()
  width=max(map(len,rows));height=len(rows)
  for i,row in enumerate(rows):
    line=VGroup()
    for j,v in enumerate(row):
      pos=centre+np.array([(j-(width-1)/2)*size,((height-1)/2-i)*size,0])
      square=Square(size,stroke_color=MUTED,stroke_width=1.5,fill_color=BACKGROUND,fill_opacity=1).move_to(pos)
      number=formula(str(v) if v else r'\phantom{0}',pos,.82 if size>=.7 else .7,COLOURS[v] if v else INK).set_z_index(1)
      line.add(VGroup(square,number))
    group.add(line)
  return group


def valid(rows):
  return all(sorted(r)==list(range(1,len(r)+1)) for r in rows) and all(len(c)==len(set(c)) for c in zip_columns(rows))


def zip_columns(rows):
  return [[row[c] for row in rows if c<len(row)] for c in range(len(rows[0]))]


def extensions(rows):
  k=len(rows[0])+1
  choices=[]
  for a in permutations([k-2,k-1,k]):
    for b in permutations([1,2,3]):
      top=list(a)+list(range(k-3,3,-1))+list(b)
      if valid([top,*rows]):choices.append(top)
  return choices


class Lesson(NarratedScene):
  def clear_frame(self):
    if self.mobjects:self.play(*[FadeOut(m) for m in list(self.mobjects)],run_time=.6)

  def heading(self,s):
    self.play(FadeIn(title(s,.88)),run_time=.6)

  def fill(self,cell,value,color=SECONDARY):
    self.play(Transform(cell[1],formula(str(value),cell.get_center(),.82,color)),cell[0].animate.set_stroke(color),run_time=.8)

  def column(self,tab,j,color=SECONDARY):
    return VGroup(*[boxed(row[j],color,buff=.02) for row in tab if j<len(row)])


class Rules(Lesson):
  def construct(self):
    with self.say('l01'):
      tab=tableau(BASE5)
      self.play(LaggedStart(*[FadeIn(r) for r in tab],lag_ratio=.3),run_time=3)
      self.heading('How many ways can this staircase grow?')
    with self.say('l02'):
      self.clear_frame()
      tab=tableau([[1,2,3],[2,3,1],[3,1,2]],1)
      self.play(LaggedStart(*[Write(r) for r in tab],lag_ratio=.25),run_time=3)
      for row in tab:self.play(Indicate(row),run_time=.8)
      self.heading('Latin square: no repeats in a row or column')
    with self.say('l03'):
      self.clear_frame()
      tab=tableau(BASE5)
      self.play(LaggedStart(*[Create(r) for r in tab],lag_ratio=.35),run_time=3)
      labels=VGroup(*[formula(str(len(r)),r[0].get_center()+LEFT*1.1,.9) for r in tab])
      self.play(Write(labels))
      self.heading('A Latin tableau: shape $(5,4,3,3)$')
    with self.say('l04'):
      for row in tab:self.play(Indicate(row,color=SECONDARY),run_time=1.2)
      self.play(FadeIn(caption(r'A row of length $m$ uses $1,2,\ldots,m$ exactly once')))
    with self.say('l05'):
      h=self.column(tab,0)
      self.play(Create(h),run_time=1)
      self.play(Transform(h,self.column(tab,1)),run_time=1.5)
      self.play(Transform(h,self.column(tab,0)),run_time=.7)
      self.play(Transform(tab[1][0][1],formula('4',tab[1][0].get_center(),.82,WARN)),Transform(tab[1][2][1],formula('3',tab[1][2].get_center(),.82,WARM)),run_time=.7)
      self.play(Indicate(VGroup(tab[0][0],tab[1][0]),color=WARN),run_time=1.5)
      self.play(Transform(tab[1][0][1],formula('3',tab[1][0].get_center(),.82,WARM)),Transform(tab[1][2][1],formula('4',tab[1][2].get_center(),.82,EXTRA)),FadeOut(h))
    with self.say('l06'):
      self.clear_frame()
      tab=tableau(BASE5).shift(LEFT*2.4)
      note=VGroup(Tex('Independent verification',color=ACCENT).scale(.8),Tex('Earlier proof: 22 October 2026').scale(.72)).arrange(DOWN,buff=.5).shift(RIGHT*3)
      self.play(Create(tab),Write(note),run_time=2)
      self.play(FadeIn(caption('The same formula and four-extension mechanism were already proved')))


class Grow(Lesson):
  def construct(self):
    with self.say('l07'):
      tab=tableau([[0]*6,*BASE5],.76,DOWN*.15)
      self.play(Create(VGroup(*tab[1:])),run_time=2)
      self.play(LaggedStart(*[Create(c) for c in tab[0]],lag_ratio=.2),run_time=2)
      self.heading('Keep the lower filling fixed')
    with self.say('l08'):
      for cell,v in zip(tab[0],BASE6[0]):self.fill(cell,v,COLOURS[v])
      self.play(Indicate(self.column(tab,0)),Indicate(self.column(tab,1)),run_time=2)
    with self.say('l09'):
      self.clear_frame()
      cards=VGroup(*[Square(.55,color=PRIMARY,fill_opacity=.2) for _ in range(24)]).arrange_in_grid(rows=4,cols=6,buff=.25)
      self.play(LaggedStart(*[Create(c) for c in cards],lag_ratio=.06),run_time=2)
      self.heading('All 576 fillings of shape $(6,5,4,3,3)$')
      self.play(FadeIn(caption('Schematic collection; every base filling is checked')))
    with self.say('l10'):
      self.clear_frame()
      tab=tableau([[0]*7,*BASE6],.74,DOWN*.2)
      self.play(Create(tab),run_time=2)
      highlights=VGroup(*[self.column(VGroup(*tab[1:]),j) for j in range(3)])
      self.play(Create(highlights),run_time=2)
      self.heading('First three columns already contain $1,2,3,4$')
    with self.say('l11'):
      self.play(FadeOut(highlights))
      fives=VGroup(*[boxed(tab[i+1][j],SECONDARY) for i,row in enumerate(BASE6) for j,v in enumerate(row) if v==5])
      self.play(Create(fives),run_time=1)
      self.fill(tab[0][2],5)
      self.play(FadeOut(fives))
    with self.say('l12'):
      self.fill(tab[0][0],6,ACCENT);self.fill(tab[0][1],7,ACCENT)
      a,b=tab[0][0][1],tab[0][1][1]
      p,q=a.get_center(),b.get_center()
      self.play(a.animate(path_arc=PI/2).move_to(q),b.animate(path_arc=PI/2).move_to(p),run_time=2)
      self.play(a.animate(path_arc=PI/2).move_to(p),b.animate(path_arc=PI/2).move_to(q),run_time=2)
      self.play(FadeIn(caption('Two choices on the left: swap 6 and 7')))


class ForcedMiddle(Lesson):
  def construct(self):
    with self.say('l13'):
      tab=tableau([[6,7,5,0,0,0,0],*BASE6],.74,DOWN*.2)
      self.play(Create(tab))
      h=self.column(VGroup(*tab[1:]),3)
      self.play(Create(h))
      self.fill(tab[0][3],4)
      self.heading('Column four blocks $1,2,3$: insert 4')
    with self.say('l14'):
      self.clear_frame()
      rows=BASE7
      for _ in range(3):rows=[extensions(rows)[0],*rows]
      tab10=tableau([rows[0],rows[1],rows[2]],.82,UP*.3)
      self.play(Create(tab10),run_time=2)
      for j in range(3,7):self.play(Indicate(tab10[0][j],color=SECONDARY),run_time=1)
      self.heading('The ten-column top row: middle values $7,6,5,4$')
      self.play(FadeIn(caption('Top three rows shown; lower rows continue the staircase')))
    with self.say('l15'):
      self.clear_frame()
      tab=tableau([[6,7,5,4,0,0,0],*BASE6],.74,DOWN*.2)
      self.play(Create(tab))
      self.play(Create(self.column(VGroup(*tab[1:]),4)),run_time=1.5)
      self.fill(tab[0][4],2)
      self.heading('Column five blocks 1 and 3: insert 2')
    with self.say('l16'):
      self.fill(tab[0][5],1,ACCENT);self.fill(tab[0][6],3,ACCENT)
      a,b=tab[0][5][1],tab[0][6][1];p,q=a.get_center(),b.get_center()
      self.play(a.animate(path_arc=PI/2).move_to(q),b.animate(path_arc=PI/2).move_to(p),run_time=2)
      self.play(a.animate(path_arc=PI/2).move_to(p),b.animate(path_arc=PI/2).move_to(q),run_time=2)
      self.play(FadeIn(caption('Two choices on the right: swap 1 and 3')))


class FourWays(Lesson):
  def construct(self):
    with self.say('l17'):
      options=extensions(BASE6)
      rows=VGroup(*[tableau([r],.68) for r in options]).arrange(DOWN,buff=.4)
      self.play(LaggedStart(*[Create(r) for r in rows],lag_ratio=.35),run_time=4)
      self.heading(r'Exactly $2\times2=4$ new top rows')
      self.play(FadeIn(caption('Every row extends the same fixed six-column tableau')))
    with self.say('l18'):
      forced=VGroup(*[boxed(row[0][j],SECONDARY,buff=.015) for row in rows for j in [2,3,4]])
      self.play(Create(forced),run_time=2)
      self.play(Indicate(VGroup(*[row[0][0] for row in rows]),color=ACCENT),Indicate(VGroup(*[row[0][6] for row in rows]),color=ACCENT),run_time=2)
    with self.say('l19'):
      self.clear_frame()
      tab=tableau(BASE6,.8,LEFT*1.8)
      checks=VGroup(*[Circle(.22,color=MUTED) for _ in range(5)]).arrange(DOWN,buff=.45).shift(RIGHT*4)
      self.play(Create(tab),Create(checks))
      for c in checks:self.play(c.animate.set_color(ACCENT).set_fill(ACCENT,.6),run_time=.6)
      self.heading('Five facts that survive every extension')
    with self.say('l20'):
      self.clear_frame()
      tab=tableau(BASE7,.74,DOWN*.15)
      self.play(Create(tab))
      blocks=VGroup(boxed(VGroup(*tab[0][:3]),PRIMARY),boxed(tab[0][3],SECONDARY),boxed(VGroup(*tab[0][4:]),ACCENT))
      self.play(Create(blocks),run_time=2)
      self.play(Indicate(VGroup(*[row[0] for row in tab[1:]])),run_time=2)
      self.heading('Large block, forced middle, small block')


class Invariants(Lesson):
  def construct(self):
    with self.say('l21'):
      tab=tableau(BASE6,.85)
      self.play(Create(tab))
      h=VGroup(boxed(tab[0][2],SECONDARY),boxed(tab[1][1],ACCENT))
      self.play(Create(h),run_time=2)
      self.heading('Largest entries of the top two rows: different columns')
    with self.say('l22'):
      self.clear_frame()
      tab=tableau(BASE7,.74,DOWN*.1)
      self.play(Create(tab))
      h=VGroup(boxed(tab[0][1],SECONDARY),boxed(tab[1][2],ACCENT))
      self.play(Create(h))
      a,b=tab[0][0][1],tab[0][1][1]
      p,q=a.get_center(),b.get_center()
      self.play(a.animate(path_arc=PI/2).move_to(q),b.animate(path_arc=PI/2).move_to(p),Transform(h[0],boxed(tab[0][0],SECONDARY)),run_time=2)
      self.heading('Either position for 7 differs from the old position of 6')
    with self.say('l23'):
      self.clear_frame()
      tab=tableau(BASE6,.85)
      self.play(Create(tab))
      self.play(Create(boxed(tab[0][-1],SECONDARY)),Create(boxed(tab[1][-1],ACCENT)),run_time=2)
      self.heading(r'Row ends differ: $2\ne3$')
      self.play(Indicate(VGroup(tab[0][-2],tab[1][-1]),color=WARM),run_time=2)
      self.play(FadeIn(caption('The missing small value is 2')))
    with self.say('l24'):
      self.clear_frame()
      tab=tableau(BASE7,.74,DOWN*.15)
      self.play(Create(tab))
      self.play(Create(boxed(tab[0][-1],SECONDARY)),Create(boxed(tab[1][-1],ACCENT)))
      self.play(Indicate(self.column(tab,3),color=ACCENT),run_time=2)
      self.heading(r'New row ends differ: $3\ne2$ (or $1\ne2$)')
      self.play(FadeIn(caption('The column sets and both safeguards are restored')))


class Induction(Lesson):
  def construct(self):
    with self.say('l25'):
      a=formula('576',LEFT*3,1.8,PRIMARY);b=formula('576',RIGHT*3,1.8,ACCENT)
      self.play(Write(a),Write(b))
      self.play(Create(Arrow(a.get_right(),b.get_left(),buff=.25,color=SECONDARY)),run_time=2)
      self.heading('Two enumeration methods agree')
      self.play(FadeIn(caption('All 576 base tableaux satisfy all five invariants')))
    with self.say('l26'):
      self.clear_frame()
      parent=Dot(UP*1.3,color=PRIMARY,radius=.18)
      kids=VGroup(*[Dot([x,-.6,0],color=ACCENT,radius=.18) for x in [-4.5,-1.5,1.5,4.5]])
      lines=VGroup(*[Line(parent.get_center(),d.get_center(),color=PRIMARY) for d in kids])
      self.play(FadeIn(parent))
      self.play(LaggedStart(*[Create(l) for l in lines],lag_ratio=.3),FadeIn(kids),run_time=3)
      self.play(Write(formula(r'576\ \to\ 2304\ \to\ 9216',DOWN*2,1.3)))
      self.heading('Each parent has exactly four children')
    with self.say('l27'):
      self.clear_frame()
      tab=tableau(BASE7,.72)
      self.play(Create(tab))
      self.play(tab[0].animate.shift(UP*1.1).set_opacity(.35),run_time=2)
      self.play(Indicate(VGroup(*tab[1:]),color=ACCENT),run_time=2)
      self.heading('Delete the top row: one unique parent')
      self.play(FadeIn(caption('No double counting; every larger filling is reached')))
    with self.say('l28'):
      self.clear_frame()
      eq=formula(r'576\cdot4^{k-6}',scale=1.8)
      self.play(Write(eq),run_time=2)
      self.play(TransformMatchingTex(eq,formula(r'9\cdot4^{k-3}',scale=1.8,color=ACCENT)),run_time=3)
      self.heading(r'For every $k\ge5$')
      self.play(FadeIn(caption('Size five is checked separately: 144')))


class Scope(Lesson):
  def construct(self):
    with self.say('l29'):
      sizes=VGroup(*[formula(s,scale=1.4) for s in ['144','576','2304']]).arrange(RIGHT,buff=1.1)
      self.play(LaggedStart(*[Write(n) for n in sizes],lag_ratio=.35),run_time=3)
      self.heading('Reproduced by both counting methods')
      self.play(FadeIn(caption('Finite checks support the induction')))
    with self.say('l30'):
      self.clear_frame()
      tab=tableau([[0]*5,[0]*4,[0]*3,[0]*3],.75)
      self.play(Create(tab))
      self.play(Indicate(tab[0]),run_time=1)
      self.play(Indicate(self.column(tab,0)),run_time=1.5)
      self.play(tab[0].animate.shift(UP*.8).set_opacity(.3),run_time=2)
      self.heading('Wideness: a condition on row and column lengths')
      self.play(FadeIn(caption('The general wide partition conjecture remains open')))
    with self.say('l31'):
      self.clear_frame()
      tab=tableau([BASE7[0]],1)
      self.play(Create(tab))
      for j in [2,3,4]:self.play(Indicate(tab[0][j],color=SECONDARY),run_time=.7)
      self.play(Indicate(VGroup(*tab[0][:2]),color=ACCENT),Indicate(VGroup(*tab[0][5:]),color=ACCENT),run_time=2)
      self.heading('Forced cells + two independent swaps = four extensions')
    with self.say('l32'):
      self.clear_frame()
      end=VGroup(Tex(r'Latin tableaux of shape $(k,k-1,\ldots,4,3,3)$').scale(.9),Tex('Independent verification note',color=ACCENT).scale(.85),Tex('Valyu Research, 2026').scale(.8),Tex(r'\texttt{maths/combinatorics/latin-squares/}').scale(.6),Tex(r'\texttt{latin-tableaux-staircase-count}').scale(.6),Tex('Narration uses a synthetic voice.',color=MUTED).scale(.65)).arrange(DOWN,buff=.32)
      self.play(FadeIn(end),run_time=2)
