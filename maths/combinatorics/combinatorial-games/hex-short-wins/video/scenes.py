"""Adaptive Hex strategies and the two distinct costs of winning."""
import json
from pathlib import Path

from manim import *
from vrvideo import *

SCENES=['TinyStrategy','TwoCosts','TheActualGame','AdaptiveProof','Checking','SixBySix','Evidence']
DATA=json.loads((Path(__file__).parent/'witness-data.json').read_text())


def lab(text,pos=ORIGIN,scale=.85,color=INK):
  return Tex(text,color=color).scale(scale).move_to(pos)


def eq(text,pos=ORIGIN,scale=1.1,color=INK):
  return MathTex(text,color=color).scale(scale).move_to(pos)


class Board(VGroup):
  def __init__(self,n=5,radius=.52,center=ORIGIN):
    super().__init__()
    self.n=n;self.radius=radius;self.cells={};self.centers={}
    origin=np.array([np.sqrt(3)*radius*(n-1)*.75,-1.5*radius*(n-1)/2,0])
    for r in range(1,n+1):
      for c in range(1,n+1):
        p=np.array([np.sqrt(3)*radius*((c-1)+(r-1)/2),-1.5*radius*(r-1),0])-origin+np.array(center)
        self.centers[(r,c)]=p
        cell=RegularPolygon(6,start_angle=PI/2,radius=radius*.97,stroke_width=1.8,color=MUTED,fill_color=SOFT,fill_opacity=.12).move_to(p)
        self.cells[(r,c)]=cell;self.add(cell)
    goals=VGroup()
    for row in [1,n]:
      v=UP if row==1 else DOWN
      goals.add(Line(self.centers[(row,1)]+v*radius*1.15+LEFT*radius*.6,self.centers[(row,n)]+v*radius*1.15+RIGHT*radius*.6,color=PRIMARY,stroke_width=6))
    for col in [1,n]:
      v=LEFT if col==1 else RIGHT
      goals.add(Line(self.centers[(1,col)]+v*radius*1.15,self.centers[(n,col)]+v*radius*1.15,color=WARN,stroke_width=6))
    self.add(goals)

  def stone(self,cell,blue=True,text=None):
    color=PRIMARY if blue else WARN
    p=self.centers[tuple(cell)]
    dot=Circle(self.radius*.64,color=color,fill_color=color,fill_opacity=.85,stroke_width=1).move_to(p)
    word=str(text) if text is not None else ('B' if blue else 'R')
    return VGroup(dot,lab(word,p, max(.48,min(.8,self.radius*1.15)),WHITE))

  def path(self,cells,color=SECONDARY):
    return VGroup(*[self.cells[tuple(c)].copy().set_fill(color,.25).set_stroke(color,5) for c in cells])


class Explain(NarratedScene):
  pause_after=.55

  def wipe(self):
    self.play(*[FadeOut(m) for m in list(self.mobjects)],run_time=.6)

  def note(self,text,color=INK):
    if hasattr(self,'_note') and self._note in self.mobjects:
      self.play(FadeOut(self._note),run_time=.25)
    self._note=caption(text,.78,color)
    self.play(FadeIn(self._note),run_time=.45)


class TinyStrategy(Explain):
  def construct(self):
    b=Board(3,.68)
    with self.say('h01'):
      self.play(Create(b),run_time=2)
      self.play(FadeIn(b.stone((1,2))),FadeIn(b.stone((2,1),False)))
      self.play(GrowArrow(Arrow([3.2,2,0],[3.2,-2,0],color=PRIMARY)),Write(lab('Blue',[4,0,0],.85,PRIMARY)))
      self.note('Blue: top to bottom. Red: left to right.')
    with self.say('h02'):
      self.wipe()
      b=Board(3,.68)
      self.play(Create(b),FadeIn(b.stone((2,2))))
      cells=[(2,1),(2,3),(1,2),(3,2),(1,3),(3,1)]
      self.play(LaggedStart(*[Indicate(b.cells[p],color=SECONDARY) for p in cells],lag_ratio=.3),run_time=4)
      self.note('Share an edge. Take turns. No swap rule.')
    with self.say('h03'):
      self.wipe()
      b=Board(2,1)
      self.play(Create(b),FadeIn(b.stone((1,2))))
      threats=VGroup(*[DashedVMobject(Circle(.66,color=SECONDARY).move_to(b.centers[p]),num_dashes=12) for p in [(2,1),(2,2)]])
      self.play(Create(threats),run_time=2)
      self.note('One Blue move creates two possible completions.')
    with self.say('h04'):
      self.wipe()
      left,right=Board(2,.85,LEFT*3),Board(2,.85,RIGHT*3)
      self.play(Create(left),Create(right),FadeIn(left.stone((1,2))),FadeIn(right.stone((1,2))))
      self.play(FadeIn(left.stone((2,1),False)),FadeIn(right.stone((2,2),False)),run_time=2)
      self.play(FadeIn(left.stone((2,2))),FadeIn(right.stone((2,1))),run_time=2)
      self.play(Create(left.path([(1,2),(2,2)])),Create(right.path([(1,2),(2,1)])),run_time=2)
      self.note('Red blocks one route. Blue completes the other.',ACCENT)
    with self.say('h05'):
      self.play(Write(title('The route adapts to the reply',.95)))
      self.play(Indicate(left),Indicate(right),run_time=2)


class TwoCosts(Explain):
  def construct(self):
    with self.say('h06'):
      b=Board(5,.56)
      self.play(Create(b),run_time=2)
      route=[(r,3) for r in range(1,6)]
      for r,c in route:
        self.play(FadeIn(b.stone((r,c),text=r)),run_time=.6)
      self.note('A possible 5-cell path is not yet a forced 5-cell win.')
    with self.say('h07'):
      self.wipe()
      self.play(Write(eq(r'\lambda(n):\ \text{path cells}',UP*.7,1.3,PRIMARY)),run_time=2)
      self.play(Write(eq(r'\delta(n):\ \text{all Blue stones}',DOWN*.7,1.3,ACCENT)),run_time=2)
      self.note('Both are worst-case guarantees against every Red defence.')


class TheActualGame(Explain):
  def construct(self):
    b=Board(5,.59,LEFT*.7)
    stones={}
    counter=eq('0',[5.1,.3,0],1.5,SECONDARY)
    counter_label=lab('Move',[5.1,1.2,0],.85)
    def moves(start,end):
      for i in range(start,end):
        p=tuple(DATA['moves'][i])
        stone=b.stone(p,i%2==0,i+1)
        stones[p]=stone
        self.play(FadeIn(stone,scale=.65),Transform(counter,eq(str(i+1),[5.1,.3,0],1.5,SECONDARY)),run_time=.75)
    with self.say('h08'):
      self.play(Create(b),Write(counter),Write(counter_label))
      self.note('Actual retained game: odd moves Blue, even moves Red')
      moves(0,8)
    with self.say('h09'):
      moves(8,16)
      self.play(Indicate(stones[(1,5)]),Indicate(stones[(5,1)]),run_time=2)
    with self.say('h10'):
      moves(16,23)
      self.note('First connection on move 23. One branch of the strategy.')
    with self.say('h11'):
      outlines=VGroup()
      for p in DATA['path']:
        outline=b.path([p]);outlines.add(outline)
        self.play(Create(outline),run_time=.8)
      self.play(Transform(counter,eq('6',[5.1,.3,0],1.5,SECONDARY)),Transform(counter_label,lab('Path cells',[5.1,1.2,0],.75)))
      self.note('Shortest connecting path: 6 cells',SECONDARY)
    with self.say('h12'):
      path={tuple(p) for p in DATA['path']}
      extras=[stones[tuple(p)] for p in DATA['moves'][::2] if tuple(p) not in path]
      self.play(LaggedStart(*[Circumscribe(s,color=ACCENT) for s in extras],lag_ratio=.25),run_time=3)
      self.play(Transform(counter,eq('12',[5.1,.3,0],1.5,ACCENT)),Transform(counter_label,lab('Blue stones',[5.1,1.2,0],.75)))
      self.note('12 Blue stones = 6 on this path + 6 elsewhere',ACCENT)
    with self.say('h13'):
      self.wipe()
      lower=eq(r'\lambda(5)\ge6',LEFT*3,1.4,PRIMARY)
      upper=eq(r'\lambda(5)\le6',RIGHT*3,1.4,PRIMARY)
      self.play(Write(lower),Write(upper),run_time=3)
      self.play(TransformMatchingTex(VGroup(lower,upper),eq(r'\lambda(5)=6',ORIGIN,1.8,ACCENT)),run_time=2)
      self.note('Red stops 5. Blue forces at most 6. Both certified.')
    with self.say('h14'):
      self.play(Write(eq(r'\delta(5)=7',DOWN*1.4,1.6,ACCENT)),run_time=2)
      self.note('A separate strategy minimises total stones. It needs 7.')


class AdaptiveProof(Explain):
  def construct(self):
    with self.say('h15'):
      b=Board(5,.57)
      path=[(r,3) for r in range(1,6)]
      self.play(Create(b),Create(b.path(path)),run_time=2)
      self.play(FadeIn(b.stone((3,3),False)),run_time=1.5)
      self.play(Create(Cross(b.cells[(3,3)],stroke_color=WARN)),run_time=1)
      self.note('Blocking one preselected route does not defeat every strategy.')
    with self.say('h16'):
      self.wipe()
      b=Board(2,1)
      self.play(Create(b),FadeIn(b.stone((1,2))))
      p1=b.path([(1,2),(2,1)])
      self.play(Create(p1))
      self.play(FadeIn(b.stone((2,1),False)),FadeOut(p1))
      self.play(Create(b.path([(1,2),(2,2)])),FadeIn(b.stone((2,2))),run_time=2)
      self.note('Choose the strategy first. Adapt the route after the reply.')
    with self.say('h17'):
      self.wipe()
      root=Dot([0,2,0],color=PRIMARY,radius=.15)
      mids=[Dot([x,.3,0],color=WARN,radius=.13) for x in [-4,0,4]]
      self.play(FadeIn(root),Write(lab('Blue: one good choice',[0,2.8,0],.85,PRIMARY)))
      self.play(*[Create(Line(root.get_center(),d.get_center(),color=MUTED)) for d in mids],*[FadeIn(d) for d in mids])
      self.play(Circumscribe(mids[1],color=SECONDARY),mids[0].animate.set_opacity(.2),mids[2].animate.set_opacity(.2))
      leaves=[Dot([x,-1.7,0],color=PRIMARY,radius=.13) for x in [-2,0,2]]
      self.play(*[Create(Line(mids[1].get_center(),d.get_center(),color=ACCENT)) for d in leaves],*[FadeIn(d) for d in leaves],run_time=2)
      self.note('Red: every reply must have an answer.')


class Checking(Explain):
  def construct(self):
    with self.say('h18'):
      blocks=VGroup(*[VGroup(RoundedRectangle(width=3.2,height=1.5,corner_radius=.1,color=c),lab(t,scale=.85,color=c)) for t,c in [('Search',PRIMARY),('Move table',SECONDARY),('Checker',ACCENT)]]).arrange(RIGHT,buff=1)
      self.play(LaggedStart(*[FadeIn(b) for b in blocks],lag_ratio=.5),run_time=3)
      self.play(GrowArrow(Arrow(blocks[0].get_right(),blocks[1].get_left(),buff=.08)),GrowArrow(Arrow(blocks[1].get_right(),blocks[2].get_left(),buff=.08)))
      self.note('A checker verifies proposed moves independently of search shortcuts.')
    with self.say('h19'):
      self.wipe()
      b=Board(3,.74)
      self.play(Create(b),FadeIn(b.stone((2,2))))
      for p in b.cells:
        if p!=(2,2):
          reply=b.stone(p,False)
          self.play(FadeIn(reply),run_time=.25)
          self.play(FadeOut(reply),run_time=.2)
      self.note('Schematic replay step: enumerate every legal opponent reply.')
    with self.say('h20'):
      self.wipe()
      b=Board(5,.56)
      self.play(Create(b))
      candidates=[t for t in DATA['minimal_targets'] if [3,3] in t][:3]
      targets=VGroup(*[b.path(t,c) for t,c in zip(candidates,[PRIMARY,ACCENT,SECONDARY])])
      self.play(LaggedStart(*[Create(t) for t in targets],lag_ratio=.5),run_time=3)
      self.play(FadeIn(b.stone((3,3),False)))
      self.play(FadeOut(targets),run_time=1.5)
      self.note('106 minimal target sets in total; 3 actual targets illustrated.')
    with self.say('h21'):
      self.wipe()
      count=Integer(0,color=PRIMARY).scale(1.8)
      self.play(FadeIn(count))
      self.play(ChangeDecimalToValue(count,106826),run_time=4,rate_func=linear)
      self.play(Write(title('Central 5 by 5, path at most 6',.85)))
      self.note('Retained independent replay: checked positions, not a live run')
    with self.say('h22'):
      self.wipe()
      self.play(Write(lab('Continued play',[-3.2,1.3,0],1,PRIMARY)),Write(lab('First connection', [3.2,1.3,0],1,ACCENT)))
      self.play(Write(lab('Long Blue connection:',[0,.1,0],.9)))
      self.play(Write(lab('short-path task continues',[-3.2,-1,0],.8,PRIMARY)),Write(lab('game stops',[3.2,-1,0],.9,ACCENT)))
      self.note('Two stopping rules for the short-path question')
    with self.say('h23'):
      self.play(Write(eq(r'\lambda(5)=\lambda^*(5)=6',[0,-2.3,0],1.2,SECONDARY)))
      self.note('Separate strict certificate. Both readings resolved on 5 by 5.')


class SixBySix(Explain):
  def construct(self):
    with self.say('h24'):
      b=Board(6,.49)
      self.play(Create(b),run_time=2)
      self.play(FadeIn(b.stone((3,4))),Circumscribe(b.cells[(3,4)],color=SECONDARY),run_time=2)
      self.play(Write(title(r'$\delta(6)=10$: certified',.95)))
      self.note('Certified Blue opening: row 3, column 4. Red stops any 9-stone win.')
    with self.say('h25'):
      self.wipe()
      dots=VGroup()
      for i in range(19):
        p=np.array([(i-9)*.6,.3,0])
        dots.add(Dot(p,radius=.15,color=PRIMARY if i%2==0 else WARN))
      self.play(LaggedStart(*[FadeIn(d) for d in dots],lag_ratio=.15),run_time=3)
      self.play(Write(eq(r'10+9=2(10)-1=19',DOWN*1.1,1.3)))
      self.note('10 Blue turns, with 9 Red turns between them')
    with self.say('h26'):
      self.wipe()
      b=Board(6,.49)
      self.play(Create(b))
      self.play(LaggedStart(*[Indicate(cell,color=WARN,scale_factor=1.08) for cell in b.cells.values()],lag_ratio=.05),run_time=4)
      self.play(Write(title(r'$\lambda(6)\ge8$: certified',.95)))
      self.note('All 36 openings: Red can stop paths of 7 or fewer cells.')
    with self.say('h27'):
      self.wipe()
      count=Integer(0,color=PRIMARY).scale(1.7)
      self.play(FadeIn(count))
      self.play(ChangeDecimalToValue(count,22780097),run_time=4,rate_func=linear)
      self.play(Write(title('36 of 36 defence certificates',.9)))
      self.note('Recovered completed replays; no production rerun claimed')
    with self.say('h28'):
      self.wipe()
      self.play(Write(eq(r'\lambda(6)\ge8',[0,1,0],1.5,ACCENT)),Write(lab('CERTIFIED',[0,2,0],.85,ACCENT)))
      self.play(Write(eq(r'\lambda(6)\le8',[0,-1.1,0],1.5,WARM)),Write(lab('SEARCH ONLY',[0,-.2,0],.85,WARM)))
      self.note('The upper bound has no independently replayed certificate.',WARM)
    with self.say('h29'):
      self.wipe()
      self.play(Write(eq(r'8\le\lambda^*(6)\le10',ORIGIN,1.7,SECONDARY)),run_time=3)
      self.play(Write(title('Strict first-connection reading',.9)))
      self.note('No exact strict 6 by 6 value is claimed.')


class Evidence(Explain):
  def construct(self):
    with self.say('h30'):
      self.play(Write(lab('Campbell (2004): measures and conjectures',[0,1.2,0],.9)))
      self.play(Write(eq(r'\lambda(5):\quad 7\ \longrightarrow\ 6',[0,-.1,0],1.5,ACCENT)),run_time=3)
      self.note('Also contradicts the 2026 preprint\'s claimed value 7.')
    with self.say('h31'):
      self.wipe()
      self.play(Write(eq(r'\delta(6):\quad9\ \longrightarrow\ 10',UP*.8,1.4,ACCENT)))
      self.play(Write(lab('HZY / KataHex (2024): earlier 19-move estimate',[0,-.7,0],.84)))
      self.note('The estimate is prior work. The certificate supplies a proof.')
    with self.say('h32'):
      self.wipe()
      self.play(Write(lab('Valid strategy',[-3,1,0],.95,ACCENT)),Write(lab('Corrupted strategy',[3,1,0],.95,WARN)))
      self.play(Write(lab('accepted',[-3,-.2,0],1.1,ACCENT)),Write(lab('rejected',[3,-.2,0],1.1,WARN)))
      self.note('Independent replay and negative controls. No Lean formalisation.')
    with self.say('h33'):
      self.wipe()
      items=VGroup(*[lab(t,scale=1,color=c) for t,c in [('Routes adapt',PRIMARY),('Path cells and placed stones differ',SECONDARY),('Replay checks every defence',ACCENT)]]).arrange(DOWN,buff=.65)
      self.play(LaggedStart(*[Write(t) for t in items],lag_ratio=.6),run_time=4)
    with self.say('h34'):
      self.wipe()
      self.play(Write(eq(r'\lambda(5)=\lambda^*(5)=6,\quad\delta(5)=7',UP*.8,1.15,ACCENT)),run_time=2)
      self.play(Write(eq(r'\delta(6)=10,\quad\lambda(6)\ge8',DOWN*.7,1.2,ACCENT)),run_time=2)
      self.note('Certified conclusions. The 6 by 6 upper path bound remains search-only.')
    with self.say('h35'):
      self.wipe()
      self.play(Write(lab('Short forced wins in small Hex',[0,1.5,0],1.15)))
      self.play(Write(lab('Valyu Research, 2026',[0,.4,0],.9,PRIMARY)))
      self.play(Write(lab('maths/combinatorics/combinatorial-games/',[0,-.8,0],.65,MUTED)))
      self.play(Write(lab('hex-short-wins',[0,-1.4,0],.8,MUTED)))
      self.play(Write(lab('Narration uses a synthetic voice.',[0,-2.4,0],.7,MUTED)))
