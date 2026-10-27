"""Exact remainder geometry and a potential that cannot reach zero."""
from manim import *
from vrvideo import *

SCENES=['ClockCover','RemainderBoards','Doubling','Prices','TheTrap','ExactEnumeration','FiniteAndInfinite']
PATTERNS=[['.........']*5,['..#..#..#','..#..#..#','...#.#..#','..##.#..#','..##.#..#'],['.##.##.##','.##.##.##','.........','.##.##.##','.........'],['.##.##.##','.##.##.##','.........','.##.##.##','.##.##.##']]


def lab(text,pos=ORIGIN,scale=.85,color=INK):
  return Tex(text,color=color).scale(scale).move_to(pos)


def eq(text,pos=ORIGIN,scale=1.15,color=INK):
  return MathTex(text,color=color).scale(scale).move_to(pos)


class Grid(VGroup):
  def __init__(self,cell=.62,center=ORIGIN,pattern=None):
    super().__init__();self.cells={};self.centers={}
    for v in range(5):
      for u in range(9):
        p=np.array(center)+np.array([(u-4)*cell,(2-v)*cell,0])
        active=pattern is None or pattern[v][u]=='#'
        square=Square(cell*.94,stroke_width=1,color=MUTED,fill_color=PRIMARY,fill_opacity=.5 if active else .03).move_to(p)
        self.cells[(u,v)]=square;self.centers[(u,v)]=p;self.add(square)

  def mark(self,cells,color=SECONDARY):
    return VGroup(*[self.cells[p].copy().set_fill(color,.35).set_stroke(color,3) for p in cells])


def shape(d):
  return [(u,v) for v in range(5) for u in range(9) if (d==1 or d==3 and u%3==0 or d==5 and v==2 or d==9 and u==4 or d==15 and u%3==0 and v==2 or d==45 and (u,v)==(4,2))]


class Explain(NarratedScene):
  pause_after=.55

  def wipe(self):
    self.play(*[FadeOut(m) for m in list(self.mobjects)],run_time=.6)

  def note(self,text,color=INK):
    if hasattr(self,'_note') and self._note in self.mobjects:
      self.play(FadeOut(self._note),run_time=.25)
    self._note=caption(text,.78,color)
    self.play(FadeIn(self._note),run_time=.45)


class ClockCover(Explain):
  def construct(self):
    points={i:np.array([2.2*np.sin(i*TAU/12),2.2*np.cos(i*TAU/12),0]) for i in range(12)}
    dots={i:Dot(p,radius=.22,color=MUTED) for i,p in points.items()}
    labels=VGroup(*[lab(str(i),p*1.22,.8) for i,p in points.items()])
    with self.say('c01'):
      self.play(FadeIn(VGroup(*dots.values())),Write(labels),run_time=2)
      self.play(*[dots[i].animate.set_color(PRIMARY) for i in [0,2,4,6,8,10]],run_time=1.5)
      self.play(*[dots[i].animate.set_color(ACCENT) for i in [3,9]],run_time=1.5)
      self.note('Remainder 0 modulo 2, then remainder 0 modulo 3')
    with self.say('c02'):
      for cells,color in [([1,5],SECONDARY),([11],WARM),([7],EXTRA)]:
        self.play(*[dots[i].animate.set_color(color) for i in cells],run_time=1.4)
      self.note(r'Then $1\bmod4$, $5\bmod6$, $7\bmod12$: all 12 positions covered.')
    with self.say('c03'):
      self.wipe()
      mods=eq(r'2,\quad3,\quad4,\quad6,\quad12',UP*.6,1.7,PRIMARY)
      self.play(Write(mods),run_time=3)
      self.play(Write(lab('Each modulus is used once',[0,-.8,0],1,ACCENT)))
      self.note('A covering system: every integer satisfies at least one rule.')
    with self.say('c04'):
      self.wipe()
      self.play(Write(eq(r'm\ge6,\qquad m\mid 2^a\cdot45',UP*.7,1.5)),run_time=3)
      self.play(Write(lab('Distinct moduli. Finite list. Any power of two.',[0,-.8,0],.95)))
    with self.say('c05'):
      self.play(Write(title(r'No finite covering, for every $a\ge0$',.9)))
      self.note('A finite exact check + an inequality valid at every later depth')


class RemainderBoards(Explain):
  def construct(self):
    with self.say('c06'):
      values=[1,3,5,9,15,45]
      row=VGroup(*[eq(str(d),scale=1.5,color=PRIMARY) for d in values]).arrange(RIGHT,buff=.9)
      self.play(LaggedStart(*[Write(x) for x in row],lag_ratio=.3),run_time=3)
      self.play(Write(eq(r'm=2^i d',DOWN*1.5,1.35)))
      self.note('Six odd parts: the divisors of 45')
    with self.say('c07'):
      self.wipe()
      g=Grid(.68)
      self.play(Create(g),run_time=2)
      for u in range(9):self.add(lab(str(u),g.centers[(u,0)]+UP*.65,.65))
      for v in range(5):self.add(lab(str(v),g.centers[(0,v)]+LEFT*.65,.65))
      self.play(Create(g.mark([(8,2)])),run_time=1.5)
      self.play(Write(title(r'$17\bmod9=8,\quad17\bmod5=2$',.9)))
      self.note('Columns: remainder modulo 9. Rows: remainder modulo 5.')
    with self.say('c08'):
      self.wipe()
      g=Grid(.68);self.play(Create(g))
      mark=None
      for d,name in [(9,'One column'),(5,'One row'),(45,'One cell')]:
        new=g.mark(shape(d))
        if mark is None:
          self.play(Create(new),run_time=1.2)
        else:
          self.play(FadeOut(mark),Create(new),run_time=1.2)
        mark=new;self.note(f'{name}: a rule modulo {d}')
    with self.say('c09'):
      for d,name in [(3,'Three spaced columns'),(15,'Three cells within one row'),(1,'The whole board')]:
        new=g.mark(shape(d))
        self.play(FadeOut(mark),Create(new),run_time=1.2)
        mark=new;self.note(f'{name}: type {d}')


class Doubling(Explain):
  def construct(self):
    with self.say('c10'):
      root=Grid(.16,[0,2,0])
      children=[Grid(.16,[x,.2,0]) for x in [-3,3]]
      leaves=[Grid(.16,[x,-1.7,0]) for x in [-4.8,-1.6,1.6,4.8]]
      self.play(Create(root))
      self.play(*[TransformFromCopy(root,c) for c in children],run_time=2)
      self.play(*[TransformFromCopy(children[i//2],c) for i,c in enumerate(leaves)],run_time=2)
      self.note(r'1 board $\to$ 2 parity boards $\to$ 4 boards modulo 4')
    with self.say('c11'):
      mark=children[0].mark(shape(9))
      self.play(Create(mark))
      self.play(TransformFromCopy(mark,leaves[0].mark(shape(9))),TransformFromCopy(mark,leaves[1].mark(shape(9))),run_time=2.5)
      self.note('An old remainder rule is inherited by both child boards.')
    with self.say('c12'):
      self.wipe()
      panels=VGroup()
      for i,d in enumerate([1,3,5,9,15,45]):
        x=(i%3-1)*4.1;y=1.3-(i//3)*2.4
        grid=Grid(.31,[x,y,0],['.........']*5)
        group=VGroup(grid,grid.mark(shape(d)),lab(f'Type {d}',[x,y-1.1,0],.75))
        panels.add(group)
      self.play(LaggedStart(*[FadeIn(p) for p in panels],lag_ratio=.25),run_time=3)
      self.note('At most one new rule of each type at a fixed depth.')


class Prices(Explain):
  def construct(self):
    with self.say('c13'):
      for i,(d,price) in enumerate(zip([1,3,5,9,15,45],[14,7,4,2,2,1])):
        x=(i%3-1)*4.1;y=1.3-(i//3)*2.4
        grid=Grid(.31,[x,y,0],['.........']*5)
        self.play(FadeIn(grid),Create(grid.mark(shape(d))),Write(lab(f'Type {d}: price {price}',[x,y-1.1,0],.73)),run_time=.8)
    with self.say('c14'):
      self.wipe()
      self.play(Write(eq(r'\phi(S)=\text{cheapest price covering the gaps}',UP*.6,.95)),run_time=3)
      self.play(Write(lab('Repeated types allowed in this measuring tool',[0,-.8,0],.9,SECONDARY)))
      self.note('Actual remainder rules still have distinct moduli.')
    with self.say('c15'):
      self.wipe()
      g=Grid(.67,pattern=PATTERNS[1]);self.play(Create(g))
      covers=[]
      for u in [2,3,5,8]:
        cover=g.mark([(u,v) for v in range(5)],ACCENT);covers.append(cover)
        self.play(Create(cover),run_time=.75)
      cost_title=title('17 uncovered cells; minimum cost 8',.85)
      self.play(Write(cost_title))
      self.note(r'Four columns at price 2 each: $4\times2=8$')
    with self.say('c16'):
      self.play(FadeOut(covers[0]),*[g.cells[(2,v)].animate.set_fill(BACKGROUND,0) for v in range(5)],run_time=2)
      self.play(Transform(cost_title,title('One column removed; remaining cost 6',.85)),Write(eq(r'8\le6+2',UP*2.5,1.1,SECONDARY)))
      self.note('Cover what remains, then buy the removed piece back.')


class TheTrap(Explain):
  def construct(self):
    with self.say('c17'):
      source=Grid(.35,LEFT*3,pattern=PATTERNS[1])
      top,bottom=Grid(.35,[3,1.2,0],PATTERNS[1]),Grid(.35,[3,-1.2,0],PATTERNS[1])
      self.play(Create(source),Write(lab('cost 8',[-3,-1.5,0],.9)))
      self.play(TransformFromCopy(source,top),TransformFromCopy(source,bottom),run_time=3)
      self.play(Write(title('Copying doubles the sum of minimum costs',.83)))
      self.note(r'Before new rules: $Q\longmapsto2Q$')
    with self.say('c18'):
      self.wipe()
      total=eq(r'R=14+7+4+2+2+1=30',UP*.9,1.2,SECONDARY)
      self.play(Write(total),run_time=3)
      self.play(Write(eq(r'Q^{\prime}\ge2Q-R',DOWN*.7,1.65,PRIMARY)),run_time=3)
      self.note('New pieces reduce the doubled cost by at most their total price.')
    with self.say('c19'):
      self.wipe()
      current=eq(r'Q\ge30',ORIGIN,1.7,PRIMARY)
      self.play(Write(current))
      for text in [r'Q^{\prime}\ge2(30)-30=30',r'Q^{\prime\prime}\ge30',r'Q_{\text{every later depth}}\ge30']:
        nxt=eq(text,ORIGIN,1.5,PRIMARY)
        self.play(TransformMatchingTex(current,nxt),run_time=2)
        current=nxt;self.wait(.5)
      self.note('The threshold is preserved by every doubling.')
    with self.say('c20'):
      self.play(Write(eq(r'\text{complete covering}\ \Longrightarrow\ Q=0',DOWN*1.5,1.0,WARN)))
      self.note('A positive cost forever prevents every finite completion.',WARN)


class ExactEnumeration(Explain):
  def construct(self):
    with self.say('c21'):
      self.play(Write(eq(r'6,9,10,12,15,18,20',UP*.7,1.1)),run_time=2)
      self.play(Write(eq(r'30,36,45,60,90,180',DOWN*.5,1.1)),run_time=2)
      self.play(Write(title('Depth 2: 13 possible distinct moduli',.9)))
      self.note('All moduli at least 6 dividing 180; every remainder choice considered.')
    with self.say('c22'):
      self.wipe()
      cards=VGroup(*[VGroup(Rectangle(width=.8,height=1.6,color=PRIMARY),lab(str(i),scale=.7)).move_to([(i-6)*1.08,0,0]) for i in range(1,12)])
      self.play(LaggedStart(*[FadeIn(c) for c in cards],lag_ratio=.12),run_time=3)
      self.play(Circumscribe(cards[-1],color=SECONDARY),run_time=2)
      self.note('For each configuration, at least one of the 11 lists reaches its threshold.')
    with self.say('c23'):
      self.wipe()
      boards=[]
      for i,pattern in enumerate(PATTERNS):
        x=(-1 if i%2==0 else 1)*3.25;y=1.4 if i<2 else -1.4
        g=Grid(.46,[x,y,0],pattern);boards.append(g)
        self.play(Create(g),Write(lab(f'{[0,17,18,24][i]} uncovered',[x,2.95 if i<2 else 0,0],.75)),run_time=.75)
      self.note('Actual retained four-board state, not a schematic pattern')
    with self.say('c24'):
      covers=[[],[(u,v) for u in [2,3,5,8] for v in range(5)],[(u,v) for v in [0,1,3] for u in range(9)],[(u,v) for u in [1,2,4,5,7,8] for v in range(5)]]
      for g,cells in zip(boards,covers):
        if cells:self.play(Create(g.mark(cells,ACCENT)),run_time=1)
      self.note(r'$Q=0+8+12+12=32\ge30=R$',ACCENT)
    with self.say('c25'):
      self.wipe()
      current=eq('32',ORIGIN,1.8,PRIMARY)
      self.play(Write(current))
      for text in [r'2(32)-30=34',r'2(34)-30=38',r'2(38)-30=46']:
        nxt=eq(text,ORIGIN,1.6,PRIMARY)
        self.play(TransformMatchingTex(current,nxt),run_time=2)
        current=nxt
      self.note('Lower bounds on later costs. A different price list can miss this state.')
    with self.say('c26'):
      self.wipe()
      counter=Integer(0,color=PRIMARY).scale(1.6)
      self.play(FadeIn(counter));self.play(ChangeDecimalToValue(counter,498464),run_time=3,rate_func=linear)
      self.play(Write(title('Main C: 498,464 nodes, 0 survivors',.86)))
      self.play(Write(eq(r'\text{Python: }135\text{ roots},\quad4{,}684{,}432\text{ nodes}',DOWN*1.4,.88,ACCENT)))
      self.note('Generic C: 66,821 nodes, 0 survivors. Retained completed runs.')
    with self.say('c27'):
      self.wipe()
      self.play(Write(eq(r'\text{finite exact enumeration}+\text{doubling lemma}',UP*.6,.95)),run_time=3)
      self.play(Write(eq(r'\Longrightarrow\quad\text{every exponent }a',DOWN*.8,1.3,ACCENT)),run_time=2)
      self.note('Three implementations and controls. No Lean formalisation.')


class FiniteAndInfinite(Explain):
  def construct(self):
    with self.say('c28'):
      self.play(Write(lab('No finite covering',[0,1.2,0],1.2,WARN)))
      self.play(Write(lab('An infinite covering exists',[0,-.4,0],1.15,ACCENT)))
      self.note('No finite stage finishes every integer.')
    with self.say('c29'):
      self.wipe()
      dots=VGroup(*[Dot([(i-6)*.8,0,0],color=MUTED,radius=.17) for i in range(13)])
      self.play(FadeIn(dots))
      for i in range(3,12,3):
        self.play(*[d.animate.set_color(ACCENT) for d in dots[:i]],run_time=1)
        self.play(Circumscribe(dots[i],color=SECONDARY),run_time=.7)
      self.play(Write(title('The missed integer can depend on the finite stage',.8)))
      self.note('Schematic illustration of the quantifiers, not the actual infinite construction')
    with self.say('c30'):
      self.wipe()
      self.play(Write(lab('Harrington, Klein, Lowrance and Trifonov',[0,1.2,0],.93)))
      self.play(Write(lab('Problem 2: finite covering excluded',[0,-.1,0],1.05,ACCENT)))
      self.note('Minimum 8 and odd-part 135 extensions are not claimed.')
    with self.say('c31'):
      self.wipe()
      items=VGroup(*[lab(t,scale=1) for t in ['Finite list','Distinct moduli',r'$m\ge6$ and $m\mid2^a\cdot45$']]).arrange(DOWN,buff=.65)
      self.play(LaggedStart(*[Write(t) for t in items],lag_ratio=.6),run_time=4)
      self.note('Under all these conditions, at least one gap remains.')
    with self.say('c32'):
      self.wipe()
      self.play(Write(eq(r'Q\ge R\quad\Longrightarrow\quad Q^{\prime}\ge2Q-R\ge R',ORIGIN,1.15,ACCENT)),run_time=4)
      self.note('Every start is trapped by some price list. Every finite continuation stays trapped.')
    with self.say('c33'):
      self.wipe()
      self.play(Write(lab('No distinct covering with these moduli',[0,1.5,0],1.1)))
      self.play(Write(lab('Valyu Research, 2026',[0,.5,0],.9,PRIMARY)))
      self.play(Write(lab('maths/number-theory/covering-systems/',[0,-.7,0],.68,MUTED)))
      self.play(Write(lab('min-modulus-six-odd-part-45',[0,-1.3,0],.75,MUTED)))
      self.play(Write(lab('Narration uses a synthetic voice.',[0,-2.4,0],.7,MUTED)))
