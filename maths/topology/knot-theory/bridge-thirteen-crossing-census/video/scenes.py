"""Actual knot certificate, elementary swap mechanics and explicit scope limits."""
import json
from pathlib import Path

import numpy as np
from manim import *
from vrvideo import *
from vrvideo import caption as base_caption

SCENES=['Humps','Loops','Permutations','Crossing','FixedValues','Connected','LowerBound','Colouring','Census','Ending']
DATA=json.loads((Path(__file__).parent/'example.json').read_text())
ENTRY=DATA['entry']
POSITIONS={int(k):np.array([*v,0.]) for k,v in DATA['positions'].items()}
EDGE_ARCS={int(k):v for k,v in DATA['edge_arcs'].items()}
COLOURS=[PRIMARY,SECONDARY,ACCENT,EXTRA]


def words(text,at=ORIGIN,scale=.85,color=INK):
  return Tex(text,color=color).scale(scale).move_to(at)


def math(text,at=ORIGIN,scale=1.,color=INK):
  return MathTex(text,color=color).scale(scale).move_to(at)


def caption(text,scale=.8,color=INK):
  mob=base_caption(text,scale,color)
  if mob.width>12.8: mob.scale_to_fit_width(12.8)
  return mob


def diagram(scale=2.8,shift=ORIGIN,colors=None):
  colors=colors or {}
  arcs=VGroup(*[VGroup() for _ in range(13)])
  for edge in range(1,27):
    ends=[i for i,row in enumerate(ENTRY['pd']) if edge in row]
    points=[]
    for crossing in ends:
      p=POSITIONS[crossing].copy()
      if ENTRY['pd'][crossing].index(edge)%2==0:
        v=POSITIONS[13+edge]-p
        p+=v/np.linalg.norm(v)*DATA['crossing_gaps'][str(crossing)]
      points.append(p)
    points=[points[0],POSITIONS[13+edge],points[1]]
    curve=VMobject(color=colors.get(EDGE_ARCS[edge],PRIMARY),stroke_width=4)
    curve.set_points_as_corners([p*scale+shift for p in points])
    arcs[EDGE_ARCS[edge]].add(curve)
  return arcs


def token(number,point,color=PRIMARY):
  return VGroup(Circle(.24,color=color,fill_color=BACKGROUND,fill_opacity=1,stroke_width=3),words(str(number),scale=.7)).move_to(point)


DOT_POS=[np.array([(i%4-1.5)*2.5,1.05-(i//4)*2.1,0.]) for i in range(8)]


def tokens():
  return VGroup(*[token(i,p) for i,p in enumerate(DOT_POS)])


def local_crossing(before=PRIMARY,over=SECONDARY,after=ACCENT,shift=ORIGIN):
  return VGroup(Line(LEFT*3.6,LEFT*.2,color=before,stroke_width=8),Line(RIGHT*.2,RIGHT*3.6,color=after,stroke_width=8),Line(DOWN*1.7,UP*1.7,color=over,stroke_width=8)).shift(shift)


class Lesson(NarratedScene):
  def head(self,text):
    h=title(text,scale=.9)
    if h.width>12.8: h.scale_to_fit_width(12.8)
    self.add(h)
    return h

  def clear_stage(self):
    self.play(*[FadeOut(m) for m in list(self.mobjects)],run_time=.7)


class Humps(Lesson):
  def construct(self):
    self.head('Can this knot ever need fewer humps?')
    knot=diagram(scale=2.65)
    with self.say('h1'):
      self.play(Create(knot),run_time=4)
      point=POSITIONS[0]*2.65
      ring=Circle(.32,color=SECONDARY).move_to(point)
      self.play(Create(ring),run_time=1)
      self.wait(2)
      self.play(FadeOut(ring))
    with self.say('h2'):
      self.clear_stage()
      self.head('Count local high points, then minimise')
      profile=ParametricFunction(lambda t:np.array([t, -.8*np.cos(2.4*t)+.25,0]),t_range=[-5.24,5.24],color=PRIMARY,stroke_width=6)
      self.play(Create(profile),run_time=3)
      tops=VGroup(*[Dot([k*np.pi/2.4,1.05,0],color=SECONDARY) for k in [-3,-1,1,3]])
      # A finite open profile is only a schematic of height maxima, not a knot.
      self.play(FadeIn(caption('Height-profile sketch only; not a knot diagram')))
      self.play(FadeIn(tops),run_time=1)
    with self.say('h3'):
      self.clear_stage()
      self.head('Four are enough does not rule out three')
      arches=VGroup(*[Arc(radius=.8,start_angle=0,angle=PI,color=PRIMARY,stroke_width=6).move_to([x,.3,0]) for x in [-3.6,-1.2,1.2,3.6]])
      self.play(LaggedStart(*[Create(a) for a in arches],lag_ratio=.3),run_time=3)
      self.play(FadeIn(math(r'b\leq4',DOWN*1.5,scale=1.5,color=ACCENT)))
      self.play(FadeIn(caption('Diagram crossings and bridge number are different counts')))
    with self.say('h4'):
      self.clear_stage()
      self.head(r'Our running example: $13n_{1005}$')
      knot=diagram(scale=2.5,shift=LEFT*2.6)
      self.play(Create(knot),run_time=3)
      question=math(r'b=3\ \text{or}\ 4?',RIGHT*3.1,scale=1.4)
      self.play(FadeIn(question))
      self.play(FadeIn(caption('Pinned table: bridge interval [3,4]')))


class Loops(Lesson):
  def construct(self):
    self.head('A little loop around a strand')
    strand=Line(DOWN*2,UP*2,color=PRIMARY,stroke_width=10)
    loop=Ellipse(width=3.8,height=1.4,color=SECONDARY,stroke_width=6)
    with self.say('l1'):
      self.play(Create(strand),run_time=2)
      self.play(Create(loop),run_time=3)
      # The upper half of the journey passes behind the vertical strand.
      self.add(Line(UP*.5,UP*.9,color=BACKGROUND,stroke_width=17),Line(UP*.5,UP*.9,color=PRIMARY,stroke_width=10))
      traveller=Dot(loop.point_from_proportion(0),color=INK)
      self.add(traveller)
      self.play(MoveAlongPath(traveller,loop),run_time=4,rate_func=linear)
      self.play(FadeIn(caption('A loop going once around a strand: a meridian')))
    with self.say('l2'):
      self.clear_stage()
      self.head('Build loop journeys from a few meridians')
      paths=VGroup(*[Circle(.65,color=c).move_to([x,0,0]) for x,c in zip([-3,0,3],COLOURS)])
      self.play(Create(paths),run_time=3)
      joins=VGroup(Arrow(LEFT*2,LEFT*.9,color=INK),Arrow(RIGHT*.9,RIGHT*2,color=INK))
      self.play(Create(joins),run_time=2)
      self.play(FadeIn(caption(r'Meridional rank $\mu$: minimum meridian generators')))
    with self.say('l3'):
      self.clear_stage()
      self.head('Bridge count bounds meridian generators')
      relation=math(r'\mu\leq b',scale=2.4)
      self.play(Write(relation),run_time=3)
      self.play(FadeIn(words('meridional rank',LEFT*3.2+DOWN*1.5,color=SECONDARY)),FadeIn(words('bridge number',RIGHT*3.2+DOWN*1.5,color=PRIMARY)))


class Permutations(Lesson):
  def construct(self):
    self.head('Test the knot with eight numbered dots')
    dots=tokens()
    with self.say('p1'):
      self.play(LaggedStart(*[FadeIn(d) for d in dots],lag_ratio=.15),run_time=3)
      self.play(FadeIn(caption('Algebraic test objects, not points on the knot')))
    with self.say('p2'):
      self.play(Swap(dots[0],dots[1],path_arc=PI/2),Swap(dots[2],dots[3],path_arc=PI/2),run_time=3)
      self.wait(1)
      self.play(Swap(dots[0],dots[1],path_arc=-PI/2),Swap(dots[2],dots[3],path_arc=-PI/2),run_time=3)
      action=math(r'(0\,1)(2\,3)',DOWN*2.25,scale=1.2,color=SECONDARY)
      self.play(FadeIn(action))
    with self.say('p3'):
      self.clear_stage()
      self.head('Every full generator set must pass the test')
      left=words('Knot journeys',LEFT*3.6,scale=1.1,color=PRIMARY)
      right=words('Eight-dot actions',RIGHT*3.6,scale=1.1,color=ACCENT)
      arrow=Arrow(LEFT*1.2,RIGHT*1.2,color=SECONDARY)
      self.play(FadeIn(left),GrowArrow(arrow),FadeIn(right),run_time=3)
      self.play(FadeIn(caption('The finite model can forget information')))


class Crossing(Lesson):
  def construct(self):
    self.head(r'One real crossing of $13n_{1005}$')
    cross=local_crossing()
    with self.say('x1'):
      self.play(Create(cross),run_time=3)
      labels=VGroup(math(r'A=(0\,1)(2\,3)',LEFT*3.1+DOWN*.75,scale=.85,color=PRIMARY),math(r'B=(0\,1)(3\,4)',UP*2.25,scale=.85,color=SECONDARY),math(r'C=(0\,1)(2\,4)',RIGHT*3.1+DOWN*.75,scale=.85,color=ACCENT))
      self.play(LaggedStart(*[FadeIn(t) for t in labels],lag_ratio=.5),run_time=4)
      self.play(FadeIn(caption('Incoming understrand A; overstrand B; outgoing C')))
    with self.say('x2'):
      self.clear_stage()
      self.head('Conjugation: rename a shuffle')
      dots=tokens()
      pairs=VGroup(Line(DOT_POS[0],DOT_POS[1],color=PRIMARY,stroke_width=5),Line(DOT_POS[2],DOT_POS[3],color=PRIMARY,stroke_width=5))
      self.add(pairs,dots)
      cap=caption(r'Rename with $B=(0\,1)(3\,4)$')
      self.play(FadeIn(cap))
      self.wait(2)
    with self.say('x3'):
      self.play(Swap(dots[0],dots[1],path_arc=PI/2),run_time=3)
      self.wait(1)
      self.play(Swap(dots[3],dots[4],path_arc=PI/4),run_time=3)
      self.play(Transform(cap,caption(r'Incoming $(0\,1)(2\,3)$ becomes outgoing $(0\,1)(2\,4)$')))
      self.play(pairs.animate.set_color(ACCENT),run_time=1)
    with self.say('x4'):
      self.clear_stage()
      self.head('The stored labels obey the crossing relation')
      eq=math(r'\underbrace{(0\,1)(3\,4)}_{B}\ \underbrace{(0\,1)(2\,3)}_{A}\ \underbrace{(0\,1)(3\,4)}_{B}\ =\ \underbrace{(0\,1)(2\,4)}_{C}',scale=1.02)
      if eq.width>12.5: eq.scale_to_fit_width(12.5)
      self.play(Write(eq),run_time=5)
      self.play(FadeIn(caption('One demonstrated relation; all 13 relations checked')))


class FixedValues(Lesson):
  def construct(self):
    self.head('Which assignments survive a shuffle?')
    circles=VGroup(*[Circle(.3,color=PRIMARY,fill_color=SOFT,fill_opacity=.35).move_to(p) for p in DOT_POS])
    indices=VGroup(*[words(str(i),p+DOWN*.55,scale=.6,color=MUTED) for i,p in enumerate(DOT_POS)])
    values=[0,1,1,0,0,1,0,1]
    bits=VGroup(*[words(str(v),p,scale=.8,color=SECONDARY) for p,v in zip(DOT_POS,values)])
    self.add(circles,indices,bits)
    with self.say('f1'):
      cap=caption('Inside each circle: a binary value, 0 or 1')
      self.play(FadeIn(cap))
      self.play(Swap(bits[0],bits[1],path_arc=PI/2),run_time=3)
      self.play(Transform(cap,caption('Different values: the assignment changes',color=WARN)))
      self.wait(2)
      self.play(Swap(bits[0],bits[1],path_arc=-PI/2),run_time=2)
    with self.say('f2'):
      self.play(Transform(bits[1],words('0',DOT_POS[1],scale=.8,color=SECONDARY)),Transform(bits[3],words('1',DOT_POS[3],scale=.8,color=SECONDARY)),run_time=2)
      links=VGroup(Line(DOT_POS[0]+RIGHT*.32,DOT_POS[1]-RIGHT*.32,color=ACCENT,stroke_width=4),Line(DOT_POS[2]+RIGHT*.32,DOT_POS[3]-RIGHT*.32,color=ACCENT,stroke_width=4))
      self.add(links)
      self.bring_to_back(links)
      self.play(Create(links),run_time=2)
      self.play(Transform(cap,caption(r'$v_0=v_1$\qquad and\qquad $v_2=v_3$',color=ACCENT)))
    with self.say('f3'):
      self.clear_stage()
      self.head('Two independent equalities remove two choices')
      switches=VGroup(*[RoundedRectangle(width=.8,height=.9,corner_radius=.12,color=PRIMARY,fill_opacity=.2) for _ in range(8)]).arrange(RIGHT,buff=.35)
      self.play(FadeIn(switches))
      self.play(switches[1].animate.set_fill(ACCENT,.8),switches[3].animate.set_fill(ACCENT,.8),run_time=2)
      self.play(FadeIn(math(r'8-2=6',DOWN*1.6,scale=1.5)))
      self.play(FadeIn(caption(r'For one meridian: $\operatorname{rank}(P-I)=2$')))
    with self.say('f4'):
      self.clear_stage()
      self.head('Any meridian has the same two-swap type')
      dots=tokens();self.add(dots)
      old=math(r'(0\,1)(2\,3)',DOWN*2.2,scale=1.25,color=SECONDARY)
      self.play(FadeIn(old))
      self.play(Swap(dots[0],dots[6],path_arc=PI/3),Swap(dots[1],dots[5],path_arc=-PI/3),run_time=4)
      self.play(Transform(old,math(r'(6\,5)(2\,3)',DOWN*2.2,scale=1.25,color=SECONDARY)))
      self.play(FadeIn(caption('Renaming preserves the number of independent conditions')))


TREE_POS={0:np.array([0.,.4,0]),1:np.array([1.6,.4,0]),5:np.array([3.2,.4,0]),6:np.array([4.8,.4,0]),3:np.array([-1.6,.4,0]),2:np.array([-3.2,.4,0]),4:np.array([-4.8,.4,0]),7:np.array([0.,-1.6,0])}


class Connected(Lesson):
  def construct(self):
    self.head('Four actual seed actions connect all eight dots')
    dots=VGroup(*[token(i,TREE_POS[i]) for i in range(8)])
    self.add(dots)
    edges=VGroup()
    with self.say('g1'):
      action=math(r'(0\,1)(2\,3)',UP*2.1,scale=1.05,color=COLOURS[0])
      self.play(FadeIn(action))
      present=set()
      for index,matching in enumerate(DATA['seed_actions']):
        (a,b),(c,d)=matching
        label=math(f'({a}\\,{b})({c}\\,{d})',UP*2.1,scale=1.05,color=COLOURS[index])
        self.play(Transform(action,label),run_time=.4)
        new=VGroup()
        for pair in matching:
          a,b=pair; key=tuple(sorted(pair))
          if key not in present:
            new.add(Line(TREE_POS[a],TREE_POS[b],color=COLOURS[index],stroke_width=5));present.add(key)
        self.add(new)
        self.bring_to_back(new)
        self.play(Create(new),run_time=1.2)
        edges.add(new)
        self.wait(.7)
    with self.say('g2'):
      self.play(FadeOut(action))
      path=[4,2,3,0,1,5,6]
      for i in path: self.play(Indicate(dots[i],color=ACCENT),run_time=.35)
      self.play(Indicate(dots[7],color=ACCENT),run_time=.35)
      row=math(r'0\quad0\quad0\quad0\quad0\quad0\quad0\quad0',DOWN*2.5,scale=.95,color=ACCENT)
      self.play(FadeIn(row))
      self.wait(2)
      self.play(Transform(row,math(r'1\quad1\quad1\quad1\quad1\quad1\quad1\quad1',DOWN*2.5,scale=.95,color=ACCENT)),run_time=2)
    with self.say('g3'):
      self.clear_stage()
      self.head('One shared value instead of eight free values')
      equation=math(r'8-1=7',scale=2,color=ACCENT)
      self.play(Write(equation),run_time=3)
      self.play(FadeIn(caption('Seven independent equality requirements')))


class LowerBound(Lesson):
  def construct(self):
    self.head('Could three meridians generate everything?')
    with self.say('b1'):
      pairs=VGroup(*[VGroup(Square(.65,color=SECONDARY,fill_opacity=.25),Square(.65,color=SECONDARY,fill_opacity=.25)).arrange(RIGHT,buff=.15) for _ in range(3)]).arrange(RIGHT,buff=.75).shift(UP*.4)
      self.play(LaggedStart(*[FadeIn(p) for p in pairs],lag_ratio=.5),run_time=3)
      self.play(FadeIn(math(r'3\times2=6',DOWN*1.4,scale=1.5,color=SECONDARY)))
      self.play(FadeIn(caption('At most six independent requirements')))
    with self.say('b2'):
      self.clear_stage()
      self.head('The actual action needs seven')
      slots=VGroup(*[Square(.8,color=ACCENT,fill_opacity=.15) for _ in range(7)]).arrange(RIGHT,buff=.18)
      self.play(Create(slots),run_time=2)
      fills=VGroup(*[Square(.7,color=SECONDARY,fill_opacity=.6).move_to(slots[i]) for i in range(6)])
      self.play(LaggedStart(*[FadeIn(s) for s in fills],lag_ratio=.18),run_time=3)
      self.play(Indicate(slots[6],color=WARN),run_time=1)
      self.play(FadeIn(math(r'6<7\quad\Longrightarrow\quad\mu\geq4',DOWN*1.6,scale=1.35,color=ACCENT)))
    with self.say('b3'):
      self.clear_stage()
      self.head('At least four bridges are necessary')
      eq=math(r'4\leq\mu\leq b',scale=2,color=ACCENT)
      self.play(Write(eq),run_time=3)
      self.play(FadeIn(caption('Next: show that four are enough')))


class Colouring(Lesson):
  def construct(self):
    self.head('Four seed arcs can colour the whole diagram')
    base={i:MUTED for i in range(13)}
    knot=diagram(colors=base)
    with self.say('u1'):
      self.play(Create(knot),run_time=3)
      for colour,arc in enumerate(ENTRY['seed_arcs']):
        self.play(knot[arc].animate.set_color(COLOURS[colour]),run_time=.7)
      self.play(FadeIn(caption('Seed arcs: 0, 3, 7, 4')))
    with self.say('u2'):
      self.clear_stage()
      self.head('One colouring move: crossing 3')
      cross=local_crossing(before=SECONDARY,over=EXTRA,after=MUTED)
      self.play(Create(cross),run_time=2)
      labels=VGroup(words('known arc 3',LEFT*3+DOWN*.8,color=SECONDARY),words('known overarc 4',UP*2.25,color=EXTRA),words('new arc 2',RIGHT*3+DOWN*.8,color=MUTED))
      self.play(FadeIn(labels))
      self.play(cross[1].animate.set_color(SECONDARY),labels[2].animate.set_color(SECONDARY),run_time=3)
      self.play(FadeIn(caption('Known overarc + one known underarc determines the other')))
    with self.say('u3'):
      self.clear_stage()
      self.head('Replay the nine stored colouring moves')
      colors={i:MUTED for i in range(13)}
      colors.update({arc:COLOURS[i] for i,arc in enumerate(ENTRY['seed_arcs'])})
      knot=diagram(colors=colors);self.add(knot)
      counter=caption('4 of 13 arcs coloured');self.add(counter)
      for i,move in enumerate(DATA['moves']):
        marker=Circle(.2,color=SECONDARY).move_to(POSITIONS[move['crossing']]*2.8)
        self.play(Create(marker),run_time=.25)
        self.play(knot[move['new_arc']].animate.set_color(COLOURS[move['seed_colour']]),Transform(counter,caption(f'{i+5} of 13 arcs coloured')),run_time=.6)
        self.play(FadeOut(marker),run_time=.25)
      self.play(Transform(counter,caption(r'Published colouring theorem: $b\leq4$',color=ACCENT)))
    with self.say('u4'):
      self.clear_stage()
      self.head('Both bounds force the answer')
      chain=math(r'4\leq\mu\leq b\leq4',scale=1.9)
      self.play(Write(chain),run_time=4)
      self.wait(2)
      result=math(r'b=\mu=4',scale=2.3,color=ACCENT)
      self.play(TransformMatchingTex(chain,result),run_time=3)


class Census(Lesson):
  def construct(self):
    self.head('25 determinations relative to the pinned list')
    with self.say('c1'):
      tiles=VGroup(*[Square(.45,color=PRIMARY,fill_opacity=.4) for _ in range(24)]).arrange_in_grid(rows=4,buff=.15).shift(LEFT*2.7)
      self.play(LaggedStart(*[FadeIn(t) for t in tiles],lag_ratio=.03),run_time=2)
      label=words('24 two-swap certificates',LEFT*2.7+DOWN*2,scale=.75,color=PRIMARY)
      self.play(FadeIn(label))
      positions=[np.array([3.3+1.0*np.cos(t),.3+1.0*np.sin(t),0]) for t in [PI/2,7*PI/6,11*PI/6]]
      three=VGroup(*[token(i,p,ACCENT) for i,p in enumerate(positions)])
      self.play(FadeIn(three))
      self.play(*[Transform(three[i],three[i].copy().move_to(positions[(i+1)%3]),path_arc=2*PI/3) for i in range(3)],run_time=3)
      self.play(FadeIn(words(r'$13n_{4645}$: one 3-cycle certificate',RIGHT*3+DOWN*2,scale=.7,color=ACCENT)))
      self.play(FadeIn(caption('A 3-cycle imposes two equalities; it is not two swaps')))
    with self.say('c2'):
      self.clear_stage()
      self.head('A precisely pinned comparison')
      eq=math(r'293-25=268',scale=2)
      self.play(Write(eq),run_time=4)
      self.play(FadeIn(caption(r'Release 1.3.0\quad KnotInfo 2026.10.5')))
    with self.say('c3'):
      self.clear_stage()
      self.head('27 certificates, 25 additions')
      eq=math(r'27=25+2',UP*.5,scale=1.9)
      self.play(Write(eq),run_time=3)
      self.play(FadeIn(words(r'Two prior cable values: $13n_{4587}$ and $13n_{4639}$',DOWN*1.1,scale=.85,color=MUTED)))
      self.play(FadeIn(caption('Residual ledger: not a list of 268 proven unknowns')))


class Ending(Lesson):
  def construct(self):
    self.head('The proof in three steps')
    with self.say('z1'):
      steps=VGroup(words('Check every crossing action',color=PRIMARY),words('Eight connected dots need seven equalities',color=SECONDARY),words('Four seeds supply the matching upper bound',color=ACCENT)).arrange(DOWN,buff=.85)
      self.play(LaggedStart(*[FadeIn(s) for s in steps],lag_ratio=.7),run_time=5)
      self.play(FadeIn(caption('Both exact checkers pass all 27 certificates')))
    with self.say('z2'):
      self.clear_stage()
      self.head('Certificate correctness and priority are separate')
      self.play(FadeIn(words('Exact values for the named knots',UP*.8,color=ACCENT)),run_time=2)
      self.play(FadeIn(words('Broader family-theorem priority remains unresolved',DOWN*.8,scale=.85,color=SECONDARY)),run_time=2)
      self.play(FadeIn(caption('No claim to a new general method or globally first discoveries')))
    with self.say('z3'):
      self.clear_stage()
      lines=VGroup(words('Twenty-five bridge-four knots',scale=1.05),words('from eight-point meridian actions',scale=.95),words('Valyu Research, 2026',scale=.85,color=PRIMARY),words(r'\texttt{maths/topology/knot-theory/}',scale=.65,color=MUTED),words(r'\texttt{bridge-thirteen-crossing-census/video/}',scale=.6,color=MUTED),words('Narration uses a synthetic voice.',scale=.7,color=MUTED)).arrange(DOWN,buff=.38)
      self.play(FadeIn(lines),run_time=2)
