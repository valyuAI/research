"""Strict coronas from exact retained placements and checked upper-bound records."""
import json
from pathlib import Path

from manim import *
from vrvideo import *

SCENES=['Surrounding','Surplus','ThreeRings','FourHexagons','EveryMarking','CertifiedMaxima','PriorAndRecord','Scope']
DATA=json.loads((Path(__file__).parent/'geometry.json').read_text())
RING_COLORS=[WARN,PRIMARY,'#8ebbcf',ACCENT,'#9cd3c8','#5b91b6','#c5dde7']


def lab(text,pos=ORIGIN,scale=.85,color=INK):
  return Tex(text,color=color).scale(scale).move_to(pos)


def eq(text,pos=ORIGIN,scale=1.15,color=INK):
  return MathTex(text,color=color).scale(scale).move_to(pos)


def polygon(points,color=PRIMARY,stroke=1.3):
  return Polygon(*[[p[0],p[1],0] for p in points],stroke_color=INK,stroke_width=stroke,fill_color=color,fill_opacity=1)


def patch(name,height=5.4,center=ORIGIN):
  parts=[polygon(p['points'],RING_COLORS[p['level']],.75 if name!='basic' else .55) for p in DATA[name]['pieces']]
  group=VGroup(*parts).scale_to_fit_height(height).move_to(center)
  rings=[VGroup(*[parts[i] for i,p in enumerate(DATA[name]['pieces']) if p['level']==j]) for j in range(max(p['level'] for p in DATA[name]['pieces'])+1)]
  return group,rings


def base(name,height=3.7,center=ORIGIN):
  return polygon(DATA[name]['base_points'],PRIMARY,2.2).scale_to_fit_height(height).move_to(center)


def base_shape(record,size=1.):
  cells=VGroup()
  for x,y in record['cells']:
    if record['grid']=='hex':
      cells.add(RegularPolygon(6,start_angle=PI/6,radius=1/np.sqrt(3),stroke_color=INK,stroke_width=1.5,fill_color=PRIMARY,fill_opacity=.75).move_to([x+y/2,np.sqrt(3)*y/2,0]))
    else:
      cells.add(Square(1,stroke_color=INK,stroke_width=1.5,fill_color=ACCENT,fill_opacity=.75).move_to([x,y,0]))
  cells.scale_to_fit_width(size)
  if cells.height>size:cells.scale_to_fit_height(size)
  return cells.move_to(ORIGIN)


class Explain(NarratedScene):
  pause_after=.55

  def wipe(self):
    self.play(*[FadeOut(m) for m in list(self.mobjects)],run_time=.6)

  def note(self,text,color=INK):
    if hasattr(self,'_note') and self._note in self.mobjects:
      self.play(FadeOut(self._note),run_time=.25)
    self._note=caption(text,.78,color)
    self.play(FadeIn(self._note),run_time=.45)


class Surrounding(Explain):
  def construct(self):
    _,rings=patch('mono')
    with self.say('t01'):
      self.play(FadeIn(rings[0]))
      for ring in rings[1:]:
        self.play(LaggedStart(*[FadeIn(piece) for piece in ring],lag_ratio=.07),run_time=1.7)
      self.note('How many complete rings can this shape grow?')
    with self.say('t02'):
      self.play(Indicate(rings[0],color=SECONDARY),run_time=1.5)
      self.play(Indicate(rings[1],color=SECONDARY),run_time=1.5)
      self.play(Write(title('Strict corona: fully surrounds the previous cluster',.76)))
      self.note('No overlaps, no holes, no point pinches')
    with self.say('t03'):
      self.wipe()
      squares=VGroup(*[Square(.48,color=MUTED,fill_color=PRIMARY,fill_opacity=.35).move_to([x*.48,y*.48,0]) for x in range(-5,6) for y in range(-3,4)])
      self.play(LaggedStart(*[FadeIn(s) for s in squares],lag_ratio=.02),run_time=3)
      self.note('Ordinary squares can keep tiling. A non-tiler eventually gets stuck.')
    with self.say('t04'):
      self.wipe()
      shapes=[base_shape(t,1.6).move_to([(i%6-2.5)*2,1.2-(i//6)*2.4,0]) for i,t in enumerate(DATA['table'][:12])]
      self.play(LaggedStart(*[FadeIn(s) for s in shapes],lag_ratio=.12),run_time=3)
      self.play(Write(title('34 bases; one centred slot per edge; lattice copies',.75)))
      self.note('All unbalanced markings. Rotations and reflections allowed.')


class Surplus(Explain):
  def construct(self):
    with self.say('t05'):
      pair=VGroup(*[polygon(p['points'],color,2.2) for p,color in zip([DATA['mono']['pieces'][i] for i in [0,5]],[PRIMARY,ACCENT])]).scale(2.5).move_to(ORIGIN)
      target=pair[1].get_center().copy()
      pair[1].shift(RIGHT*2.4)
      self.play(FadeIn(pair[0]),FadeIn(pair[1]),run_time=1.5)
      self.play(pair[1].animate.move_to(target),run_time=2.5)
      self.play(Write(title('A retained adjacent pair: bump fits nick',.85)))
      self.note('Bump--bump overlaps; nick--flat leaves a gap. Flat meets flat.')
    with self.say('t06'):
      self.wipe()
      shape=base('mono',3.5,LEFT*2.5)
      self.play(FadeIn(shape))
      self.play(Write(eq(r'3B-2N=1',[3,1,0],1.3,SECONDARY)))
      self.play(Write(lab('plus one flat edge',[3,-.2,0],.85)))
      self.note('Unbalanced means unequal numbers of bumps and nicks.')
    with self.say('t07'):
      self.wipe()
      bumps=VGroup(*[eq('+',color=PRIMARY).move_to([(i-2)*1.5,.9,0]) for i in range(5)])
      nicks=VGroup(*[eq('-',color=ACCENT).move_to([(i-2)*1.5,-.8,0]) for i in range(4)])
      self.play(FadeIn(bumps),FadeIn(nicks))
      for i in range(4):
        self.play(bumps[i].animate.move_to([(i-2)*1.5,0,0]),nicks[i].animate.move_to([(i-2)*1.5,0,0]),run_time=.5)
        self.play(FadeOut(bumps[i]),FadeOut(nicks[i]),run_time=.3)
      self.note('Internal matches cancel. The surplus remains on the outside.')
    with self.say('t08'):
      self.wipe()
      ax=Axes(x_range=[0,5,1],y_range=[0,25,5],x_length=8.5,y_length=4.3,tips=False)
      area=ax.plot(lambda r:r*r,x_range=[0,5],color=PRIMARY)
      boundary=ax.plot(lambda r:3*r,x_range=[0,5],color=SECONDARY)
      self.play(Create(ax),Create(boundary),run_time=2)
      self.play(Create(area),run_time=3)
      self.play(Write(lab('Area grows quadratically',[0,2.8,0],.9,PRIMARY)))
      self.note('Schematic growth rates: surplus area eventually beats boundary capacity.')


class ThreeRings(Explain):
  def construct(self):
    with self.say('t09'):
      _,rings=patch('mono',5.3)
      counter=eq('1',[5,0,0],1.4,SECONDARY)
      self.play(FadeIn(rings[0]),Write(counter))
      for ring,count in zip(rings[1:],[7,19,37]):
        self.play(LaggedStart(*[FadeIn(p) for p in ring],lag_ratio=.05),Transform(counter,eq(str(count),[5,0,0],1.4,SECONDARY)),run_time=2)
      self.note('Retained exact witness: $1+6+12+18=37$ pieces')
    with self.say('t10'):
      self.wipe()
      cells=VGroup()
      for q in range(-4,5):
        for r in range(-4,5):
          if max(abs(q),abs(r),abs(q+r))<=4:
            cells.add(RegularPolygon(6,start_angle=PI/6,radius=.34,stroke_color=MUTED,stroke_width=1,fill_color=PRIMARY,fill_opacity=.25).move_to([.59*(q+r/2),.59*np.sqrt(3)*r/2,0]))
      self.play(Create(cells),run_time=3)
      self.play(Write(title('Hypothetical fourth ring: 61 cells',.86)))
      self.note('Unmarked geometry only: the required unbalanced marking is impossible.')
    with self.say('t11'):
      self.wipe()
      self.play(Write(eq(r'61\text{ surplus marks}>54\text{ outer edges}',UP*.3,1.2,WARN)),run_time=3)
      self.play(Write(eq(r'3\text{ rings attained},\qquad4\text{ impossible}',DOWN*1.3,1.05,ACCENT)))
      self.note('Epstein\'s classical counting obstruction')


class FourHexagons(Explain):
  def construct(self):
    with self.say('t12'):
      shape=base('row4',4.7,LEFT*2.8)
      self.play(Create(shape),run_time=2)
      self.play(Write(eq(r'9B+1F+8N',[3,.9,0],1.2,PRIMARY)))
      self.play(Write(eq(r'9-8=1',[3,-.5,0],1.4,SECONDARY)))
      self.note('18 outer edges. One actual retained optimal marking.')
    with self.say('t13'):
      self.wipe()
      _,rings=patch('row4',5.5,LEFT*.5)
      counter=eq('4',[5,0,0],1.4,SECONDARY)
      self.play(FadeIn(rings[0]),Write(counter))
      for ring,count in zip(rings[1:3],[24,68]):
        self.play(LaggedStart(*[FadeIn(p) for p in ring],lag_ratio=.06),Transform(counter,eq(str(count),[5,0,0],1.4,SECONDARY)),run_time=2)
      self.note('Cumulative underlying hexagonal cells: 4, 24, 68')
    with self.say('t14'):
      for ring,count in zip(rings[3:],[160,316,524]):
        self.play(LaggedStart(*[FadeIn(p) for p in ring],lag_ratio=.025),Transform(counter,eq(str(count),[5,0,0],1.4,SECONDARY)),run_time=2)
      self.note('5 rings; 524 cells = 131 marked four-cell pieces',ACCENT)
    with self.say('t15'):
      self.play(Write(title('One successful marking proves a lower bound',.82)))
      self.note('To prove a maximum, exclude 6 rings for EVERY permitted marking.')


class EveryMarking(Explain):
  def construct(self):
    with self.say('t16'):
      dials=VGroup(*[lab('B / N / F',[(i%6-2.5)*2,(1-i//6)*1.2,0],.65,PRIMARY) for i in range(18)])
      self.play(LaggedStart(*[FadeIn(d) for d in dials],lag_ratio=.08),run_time=3)
      self.play(Write(title('$3^{18}=387,420,489$ assignments',.9)))
      self.note('Before restrictions and symmetries')
    with self.say('t17'):
      self.wipe()
      columns=VGroup()
      for x,name in [(-3,'Choose marks'),(3,'Choose placements')]:
        switches=VGroup(*[Square(.55,color=PRIMARY,fill_color=PRIMARY,fill_opacity=.5 if i%2 else .05).move_to([x+(i%3-1)*.8,(.5-i//3)*.9,0]) for i in range(6)])
        columns.add(switches)
        self.play(FadeIn(switches),Write(lab(name,[x,1.6,0],.95)))
      self.play(columns[0][0].animate.set_fill(ACCENT,.8),columns[1][3].animate.set_fill(ACCENT,.8),run_time=2)
      self.note('One joint logical puzzle: marks and surrounding placements')
    with self.say('t18'):
      self.play(Write(eq(r'\#B-\#N\ge1',[0,-2,0],1.2,SECONDARY)))
      self.note('SAT: all choices must satisfy all rules simultaneously.')
    with self.say('t19'):
      self.wipe()
      _,rings=patch('row4',4.4)
      self.play(FadeIn(VGroup(*rings[:3])))
      circle=DashedVMobject(Circle(2.9,color=SECONDARY),num_dashes=48)
      self.play(Create(circle),run_time=2)
      self.play(GrowArrow(Arrow([1,.3,0],[2.5,.3,0],color=SECONDARY)))
      self.note('Schematic window: the paper proves a radius bound containing every candidate.')
    with self.say('t20'):
      self.wipe()
      _,rings=patch('mono',4.8,LEFT*2.6)
      self.play(FadeIn(VGroup(*rings)),run_time=2)
      checks=VGroup(*[lab(t,scale=.85,color=ACCENT) for t in ['No overlap','Marks match','Solid disk','Previous union enclosed']]).arrange(DOWN,buff=.45).move_to(RIGHT*3)
      self.play(LaggedStart(*[Write(c) for c in checks],lag_ratio=.4),run_time=3)
      self.note('YES: explicit placements, checked independently')
    with self.say('t21'):
      self.wipe()
      stages=VGroup(*[lab(t,scale=.95,color=c) for t,c in [('Encoded rules',PRIMARY),('DRAT proof steps',SECONDARY),('Independent verification',ACCENT)]]).arrange(DOWN,buff=.7)
      self.play(LaggedStart(*[Write(s) for s in stages],lag_ratio=.5),run_time=4)
      self.note('NO: a proof of inconsistency. The encoding still needs its soundness argument.')


class CertifiedMaxima(Explain):
  def construct(self):
    with self.say('t22'):
      for x,n in [(-3,4),(3,5)]:
        record=next(t for t in DATA['table'] if t['grid']=='hex' and len(t['cells'])==n and 'straight' in t['name'])
        shape=base_shape(record,3.2).move_to([x,.7,0]);self.play(FadeIn(shape))
        self.play(Write(eq(r'5\ \text{yes},\quad6\ \text{no}',[x,-1.6,0],.95,ACCENT)))
      self.note('Maximum over all unbalanced single-slot markings, on the lattice')
    with self.say('t23'):
      self.wipe()
      count=Integer(0,color=PRIMARY).scale(1.7)
      self.play(FadeIn(count));self.play(ChangeDecimalToValue(count,34),run_time=2,rate_func=linear)
      self.play(Write(eq(r'12+21+1=34',DOWN*1.4,1.2)))
      self.note('34 bases: checked witnesses and verified upper-proof records')
    with self.say('t24'):
      self.wipe()
      for i,(n,h) in enumerate([(1,3),(2,4),(3,4),(4,5),(5,5)]):
        record={'grid':'hex','cells':[[j,0] for j in range(n)]}
        x=(i-2)*2.55
        self.play(FadeIn(base_shape(record,2).move_to([x,.6,0])),Write(eq(str(h),[x,-1,0],1.4,ACCENT)),run_time=.8)
      self.play(Write(title('Straight hexagon rows: exact lattice maxima',.83)))
      self.note('Other bases with at most 4 hexagons: at most 3 rings')
    with self.say('t25'):
      self.wipe()
      for x,n in [(-3,4),(3,5)]:
        self.play(FadeIn(base_shape({'grid':'sq','cells':[[i,0] for i in range(n)]},4).move_to([x,.8,0])),Write(eq('h=3',[x,-.5,0],1.2,ACCENT)))
      self.note('Six non-row optimal witnesses have imbalance 2 or 3.')
    with self.say('t26'):
      self.wipe()
      self.play(Write(eq(r'170\text{ witness mutations rejected}',UP*.8,1.1,ACCENT)),run_time=2)
      self.play(Write(eq(r'32\text{ bases}\times2\text{ bounds}=64\text{ agreements}',DOWN*.7,.98,PRIMARY)),run_time=2)
      self.note('Second encoder excludes the two large row cases. No Lean formalisation.')


class PriorAndRecord(Explain):
  def construct(self):
    with self.say('t27'):
      self.play(Write(lab('Mann: five-ring hexapillars (2001--2004)',[0,1,0],.95)))
      self.play(Write(lab('Atlas: five for particular four- and five-row markings',[0,-.4,0],.87)))
      self.note('Existing five-ring results are credited. No new record.')
    with self.say('t28'):
      self.wipe()
      self.play(Write(lab('Maximum over ALL allowed unbalanced markings',[0,.8,0],.92,ACCENT)))
      self.play(Write(lab('Small-table overlap with Mann--Thomas unresolved',[0,-.6,0],.86,WARM)))
      self.note('Novelty is qualified; the earlier full text was unavailable.')
    with self.say('t29'):
      self.wipe()
      _,rings=patch('basic',5.5)
      self.play(FadeIn(rings[0]))
      self.play(Write(title(r"Ba\v{s}i\'c: existing six-ring construction",.83)))
      self.note('Actual retained geometry. Exact audit confirms the published patch.')
    with self.say('t30'):
      for ring in rings[1:]:
        self.play(LaggedStart(*[FadeIn(p) for p in ring],lag_ratio=.015),run_time=1.4)
      self.note('169 pieces: $1+6+10+13+32+52+55$. No holes or pinches.')
    with self.say('t31'):
      self.wipe()
      self.play(Write(lab('Large upper proofs: completed verification records',[0,.8,0],.92,ACCENT)))
      self.play(Write(lab('Hashes, logs and regeneration commands retained',[0,-.5,0],.88)))
      self.note('Large proof files are not all shipped. No new replay during video production.')


class Scope(Explain):
  def construct(self):
    with self.say('t32'):
      items=VGroup(*[lab(t,scale=.95,color=c) for t,c in [('One centred slot; unbalanced markings',PRIMARY),('Strict coronas; lattice copies',ACCENT),('No global off-grid upper bound',WARM)]]).arrange(DOWN,buff=.65)
      self.play(LaggedStart(*[Write(t) for t in items],lag_ratio=.6),run_time=4)
    with self.say('t33'):
      self.wipe()
      self.play(Write(eq(r'\text{witness at }k+\text{exclusion at }k+1',UP*.6,1.1)),run_time=3)
      self.play(Write(eq(r'\Longrightarrow\quad\text{exact maximum }k',DOWN*.9,1.2,ACCENT)),run_time=2)
      self.note('An exact answer requires both halves, inside the same model.')
    with self.say('t34'):
      self.wipe()
      self.play(Write(lab('Exact Heesch numbers of small edge-marked polyforms',[0,1.5,0],.85)))
      self.play(Write(lab('Valyu Research, 2026',[0,.6,0],.9,PRIMARY)))
      self.play(Write(lab('maths/geometry/tilings/',[0,-.6,0],.7,MUTED)))
      self.play(Write(lab('marked-polyform-heesch-numbers',[0,-1.2,0],.73,MUTED)))
      self.play(Write(lab('Narration uses a synthetic voice.',[0,-2.3,0],.7,MUTED)))
