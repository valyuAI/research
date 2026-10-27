"""Johnson-solid explainer. Display geometry is frozen by prepare_assets.py.

All deformations of J3 use s1 + R(t)s2 from the accepted certificate.
The two-bar obstruction and pyramid trial are explicitly teaching examples.
"""
import json
from pathlib import Path

import numpy as np
from manim import *
from vrvideo import *

SCENES = ['Rules', 'Cupola', 'Addition', 'Flatness', 'Pyramid', 'FirstOrder', 'SecondOrder', 'Census', 'Evidence', 'Ending']
DATA = json.loads((Path(__file__).parent / 'geometry.json').read_text())
S1 = np.array(DATA['s1'])
S2 = np.array(DATA['s2'])
EDGES = DATA['edges']
FACES = DATA['faces']
BLUE_EDGES = {tuple(e) for e in DATA['group1']}


def words(text, at=ORIGIN, scale=0.85, color=INK):
  return Tex(text, color=color).scale(scale).move_to(at)


def formula(text, at=ORIGIN, scale=1., color=INK):
  return MathTex(text, color=color).scale(scale).move_to(at)


def rotz(angle):
  t = angle * DEGREES
  return np.array([[np.cos(t), -np.sin(t), 0], [np.sin(t), np.cos(t), 0], [0, 0, 1]])


def cupola_points(angle=0):
  return S1 + S2 @ rotz(angle).T


def project(points, scale=2.8, shift=ORIGIN, az=-65, el=30):
  az, el = az * DEGREES, el * DEGREES
  right = np.array([-np.sin(az), np.cos(az), 0])
  up = np.array([-np.cos(az)*np.sin(el), -np.sin(az)*np.sin(el), np.cos(el)])
  pts = np.asarray(points)
  return np.column_stack([pts @ right, pts @ up, np.zeros(len(pts))])*scale + shift


def solid(points, edges=EDGES, faces=FACES, scale=2.8, shift=ORIGIN, colours=True, az=-65, el=30):
  pts = project(points, scale, shift, az, el)
  view = np.array([np.cos(az*DEGREES)*np.cos(el*DEGREES), np.sin(az*DEGREES)*np.cos(el*DEGREES), np.sin(el*DEGREES)])
  polys = VGroup(*[Polygon(*[pts[i] for i in face], stroke_width=0, fill_color=PRIMARY, fill_opacity=0.08) for face in sorted(faces, key=lambda f: np.mean(points[f], axis=0) @ view)])
  lines = VGroup(*[Line(pts[a], pts[b], stroke_width=4, color=PRIMARY if not colours or (a, b) in BLUE_EDGES else SECONDARY) for a, b in edges])
  dots = VGroup(*[Dot(p, radius=0.045, color=INK) for p in pts])
  return VGroup(polys, lines, dots)


def cube_points(t):
  t *= DEGREES
  return np.array([[x, y, -0.5] for x, y in [(-0.5,-0.5),(0.5,-0.5),(0.5,0.5),(-0.5,0.5)]] + [[x+np.sin(t), y, np.cos(t)-0.5] for x, y in [(-0.5,-0.5),(0.5,-0.5),(0.5,0.5),(-0.5,0.5)]])


CUBE_FACES = [[0,1,2,3],[4,5,6,7],[0,1,5,4],[1,2,6,5],[2,3,7,6],[3,0,4,7]]
CUBE_EDGES = [(0,1),(1,2),(2,3),(0,3),(4,5),(5,6),(6,7),(4,7),(0,4),(1,5),(2,6),(3,7)]


class Lesson(NarratedScene):
  def head(self, text):
    mob = title(text, scale=0.9)
    self.add(mob)
    return mob

  def clear_stage(self):
    self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=0.7)


class Rules(Lesson):
  def construct(self):
    self.head('Can this shape wobble?')
    t = ValueTracker(0)
    def square():
      a = t.get_value()*DEGREES
      pts = np.array([[-1,-1,0],[1,-1,0],[1+2*np.sin(a),-1+2*np.cos(a),0],[-1+2*np.sin(a),-1+2*np.cos(a),0]])
      pts -= pts.mean(axis=0)
      return Polygon(*pts, color=PRIMARY, stroke_width=6, fill_opacity=0.06).scale(1.35)
    sq = always_redraw(square)
    self.add(sq)
    with self.say('r1'):
      self.wait(2)
      self.play(t.animate.set_value(28), run_time=5, rate_func=smooth)
      self.play(t.animate.set_value(0), run_time=3)
    with self.say('r2'):
      sq.clear_updaters()
      self.play(FadeOut(sq))
      cub = solid(cube_points(0), CUBE_EDGES, CUBE_FACES, colours=False, scale=3.3)
      self.play(Create(cub), run_time=3)
      cap = caption('Fixed edges. Flat faces. Changing angles.', scale=0.85)
      self.play(FadeIn(cap))
    with self.say('r3'):
      self.remove(cub)
      moving = always_redraw(lambda: solid(cube_points(t.get_value()), CUBE_EDGES, CUBE_FACES, colours=False, scale=3.3))
      self.add(moving)
      self.play(t.animate.set_value(25), run_time=5)
      self.wait(1)
      self.play(t.animate.set_value(-16), run_time=4)
      self.play(t.animate.set_value(0), run_time=3)
    with self.say('r4'):
      moving.clear_updaters()
      self.play(FadeOut(moving), FadeOut(cap))
      nums = VGroup(words('47', scale=2.2, color=ACCENT), words('45', scale=2.2, color=PRIMARY)).arrange(RIGHT, buff=3)
      labels = VGroup(words('locally rigid', nums[0].get_center()+DOWN*1.15), words('flexible', nums[1].get_center()+DOWN*1.15))
      self.play(FadeIn(nums), FadeIn(labels), run_time=2)


class Cupola(Lesson):
  def construct(self):
    self.head('J3: the triangular cupola')
    angle = ValueTracker(0)
    mob = always_redraw(lambda: solid(cupola_points(angle.get_value()), colours=False))
    self.add(mob)
    cap = caption(r'9 corners\quad 15 unit edges\quad 8 faces')
    with self.say('c1'):
      self.play(FadeIn(cap))
      for face in [FACES[4], FACES[0], FACES[1], FACES[5]]:
        patch = Polygon(*project(cupola_points()[face]), color=SECONDARY, fill_opacity=0.35)
        self.play(FadeIn(patch), run_time=0.6)
        self.wait(1)
        self.play(FadeOut(patch), run_time=0.5)
    with self.say('c2'):
      self.play(Transform(cap, caption('Locked, or flexible?')))
      self.wait(4)
    with self.say('c3'):
      self.play(Transform(cap, caption('An actual certified motion', color=ACCENT)))
      self.play(angle.animate.set_value(8), run_time=5)
      self.play(angle.animate.set_value(-8), run_time=6)
      self.play(angle.animate.set_value(0), run_time=3)
    with self.say('c4'):
      diag = always_redraw(lambda: DashedLine(*project(cupola_points(angle.get_value())[[0,1]]), color=SECONDARY, stroke_width=5))
      self.add(diag)
      self.play(Transform(cap, caption('A non-edge distance changes')))
      self.play(angle.animate.set_value(8), run_time=5)
      self.play(angle.animate.set_value(-8), run_time=5)
      self.play(angle.animate.set_value(0), run_time=2)
      diag.clear_updaters()
    mob.clear_updaters()


class Addition(Lesson):
  def construct(self):
    self.head('Build a corner by adding positions')
    origin = np.array([-2.,-1.,0])
    b = np.array([2.,0.8,0])
    y = np.array([1.,1.5,0])
    dot = Dot(origin, color=INK)
    arrow1 = Arrow(origin, origin+b, buff=0, color=PRIMARY, stroke_width=7)
    arrow2 = Arrow(origin+b, origin+b+y, buff=0, color=SECONDARY, stroke_width=7)
    sum_arrow = Arrow(origin, origin+b+y, buff=0, color=ACCENT, stroke_width=5)
    with self.say('a1'):
      self.play(FadeIn(dot))
      self.play(GrowArrow(arrow1), run_time=2)
      self.play(GrowArrow(arrow2), run_time=2)
      self.play(GrowArrow(sum_arrow), run_time=2)
      eq = formula(r'\text{blue position}+\text{yellow position}=\text{corner}', DOWN*2.5, scale=0.8)
      self.play(FadeIn(eq))
    with self.say('a2'):
      self.play(*[FadeOut(m) for m in [dot, arrow1, arrow2, sum_arrow, eq]])
      u1 = np.unique(np.round(S1,12),axis=0)
      u2 = np.unique(np.round(S2,12),axis=0)
      tri_edges = [(0,1),(1,2),(0,2)]
      tetra_edges = [(a,b) for a in range(4) for b in range(a+1,4)]
      tri = solid(u1,tri_edges,[],scale=2.8,shift=LEFT*3.1,colours=False)
      tet = solid(u2,tetra_edges,[],scale=2.8,shift=RIGHT*2.6,colours=False).set_color(SECONDARY)
      self.play(Create(tri), Create(tet), run_time=3)
      lab = VGroup(words('triangle',LEFT*3.1+DOWN*2.3,color=PRIMARY),words('tetrahedron',RIGHT*2.6+DOWN*2.3,color=SECONDARY))
      self.play(FadeIn(lab),FadeIn(words('+',scale=1.5)))
    with self.say('a3'):
      self.play(*[FadeOut(m) for m in list(self.mobjects)])
      self.head('Keep blue fixed. Rotate yellow. Add again.')
      ang = ValueTracker(0)
      construction = always_redraw(lambda: solid(cupola_points(ang.get_value())))
      self.add(construction)
      axis = DashedLine(UP*2.5,DOWN*2.1,color=MUTED)
      self.play(Create(axis))
      self.play(ang.animate.set_value(8),run_time=5)
      self.play(ang.animate.set_value(-8),run_time=5)
    with self.say('a4'):
      self.play(FadeOut(axis))
      cap = caption('Each edge belongs to one rigid component')
      self.play(FadeIn(cap))
      self.play(ang.animate.set_value(8),run_time=5)
      self.play(ang.animate.set_value(0),run_time=5)
      construction.clear_updaters()


class Flatness(Lesson):
  def construct(self):
    self.head('Why do the faces stay flat?')
    angle = ValueTracker(0)
    face = FACES[0]
    def hexagon():
      p = cupola_points(angle.get_value())[face].copy()
      p[:,2] = 0
      p -= p.mean(axis=0)
      p *= 2.2
      return VGroup(*[Line(p[j],p[(j+1)%6],color=PRIMARY if tuple(sorted((face[j],face[(j+1)%6]))) in BLUE_EDGES else SECONDARY,stroke_width=7) for j in range(6)])
    hex_mob = always_redraw(hexagon)
    self.add(hex_mob)
    with self.say('f1'):
      cap = caption('Hexagon, viewed from above')
      self.play(FadeIn(cap))
      self.play(angle.animate.set_value(5),run_time=5)
      self.play(angle.animate.set_value(0),run_time=4)
    with self.say('f2'):
      self.play(angle.animate.set_value(5),run_time=5)
      self.play(Transform(cap,caption(r'$5^\circ$ turn: $115^\circ,125^\circ,115^\circ,125^\circ,115^\circ,125^\circ$',scale=0.8)))
      self.wait(3)
    with self.say('f3'):
      hex_mob.clear_updaters()
      self.play(FadeOut(hex_mob),FadeOut(cap))
      t = ValueTracker(0)
      # The teaching parallelogram uses two independent fixed-length directions.
      def unit_para():
        a=np.array([2.,0.,0]); b=np.array([2*np.sin(t.get_value()),2*np.cos(t.get_value()),0])
        pts=np.array([ORIGIN,a,a+b,b]);pts-=pts.mean(axis=0)
        return VGroup(Polygon(*pts,fill_color=PRIMARY,fill_opacity=.15,stroke_width=0),*[Line(pts[j],pts[(j+1)%4],color=PRIMARY if j%2==0 else SECONDARY,stroke_width=7) for j in range(4)])
      par=always_redraw(unit_para)
      self.add(par)
      self.play(FadeIn(caption('Two directions span one plane')))
      self.play(t.animate.set_value(.5),run_time=5)
      self.play(t.animate.set_value(-.3),run_time=4)
      par.clear_updaters()


class Pyramid(Lesson):
  def construct(self):
    self.head('J1: why the square pyramid locks')
    r=1/np.sqrt(2)
    p=np.array([[r,0,0],[0,r,0],[-r,0,0],[0,-r,0],[0,0,r]])
    edges=[(0,1),(1,2),(2,3),(0,3),(0,4),(1,4),(2,4),(3,4)]
    pyr=solid(p,edges,[],colours=False,scale=3.7,shift=DOWN*.5)
    with self.say('p1'):
      self.play(Create(pyr),run_time=3)
      self.play(FadeIn(caption('Could the base become a rhombus?')))
    with self.say('p2'):
      self.play(*[FadeOut(m) for m in list(self.mobjects)])
      self.head('The tip must be equally far from all corners')
      rh=Polygon([3,0,0],[0,1.7,0],[-3,0,0],[0,-1.7,0],color=PRIMARY)
      diag=VGroup(DashedLine(LEFT*3,RIGHT*3,color=MUTED),DashedLine(UP*1.7,DOWN*1.7,color=MUTED))
      self.play(Create(rh),Create(diag),FadeIn(Dot(ORIGIN,color=SECONDARY)),run_time=3)
      la=words('$a$',RIGHT*1.5+DOWN*.35,color=PRIMARY)
      lb=words('$b$',UP*.9+LEFT*.4,color=SECONDARY)
      self.play(FadeIn(la),FadeIn(lb))
    with self.say('p3'):
      self.play(*[FadeOut(m) for m in list(self.mobjects)])
      self.head('Pythagoras forces the diagonals to match')
      eq1=formula(r'a^2+h^2=1',UP*.9,scale=1.3)
      eq2=formula(r'b^2+h^2=1',DOWN*.4,scale=1.3)
      self.play(Write(eq1),run_time=3)
      self.play(Write(eq2),run_time=3)
      result=formula(r'a^2=b^2',DOWN*2,scale=1.4,color=ACCENT)
      self.play(Indicate(eq1[0][2:5],color=SECONDARY),Indicate(eq2[0][2:5],color=SECONDARY))
      self.play(Write(result),run_time=2)
    with self.say('p4'):
      self.play(FadeOut(eq1),FadeOut(eq2),FadeOut(result))
      rh=Polygon([3,0,0],[0,1.7,0],[-3,0,0],[0,-1.7,0],color=WARN)
      square=Polygon([2.3,0,0],[0,2.3,0],[-2.3,0,0],[0,-2.3,0],color=ACCENT)
      self.add(rh)
      self.play(Transform(rh,square),run_time=4)
      self.play(FadeIn(caption('Equal diagonals force a square. Already known.')))


class FirstOrder(Lesson):
  def construct(self):
    self.head('What is allowed at the first instant?')
    with self.say('v1'):
      obj=solid(cupola_points(),colours=False)
      self.play(Create(obj),run_time=2)
      points=project(cupola_points())
      velocities=project(np.cross(np.array([0.,0.,1.]),S2),scale=1.1)
      arrows=VGroup(*[Arrow(p,p+v,buff=0,color=SECONDARY) for p,v in zip(points,velocities) if np.linalg.norm(v)>.05])
      self.play(LaggedStart(*[GrowArrow(a) for a in arrows],lag_ratio=.15),run_time=3)
    with self.say('v2'):
      self.play(FadeOut(obj),FadeOut(arrows))
      rod=Line(LEFT*2,RIGHT*2,color=PRIMARY,stroke_width=7)
      ends=VGroup(Dot(LEFT*2),Dot(RIGHT*2))
      along=Arrow(RIGHT*2,RIGHT*3.5,buff=0,color=WARN)
      side=Arrow(RIGHT*2,RIGHT*2+UP*1.7,buff=0,color=SECONDARY)
      self.play(Create(rod),FadeIn(ends))
      self.play(GrowArrow(along),run_time=2)
      along_caption=caption('Along the bar: length changes immediately',color=WARN)
      self.play(FadeIn(along_caption))
      self.wait(2)
      self.play(FadeOut(along),FadeOut(along_caption))
      self.play(GrowArrow(side),run_time=2)
      cap=caption('Sideways: zero initial rate of length change')
      self.play(FadeIn(cap))
    with self.say('v3'):
      self.clear_stage()
      self.head('Whole-object motion does not count')
      self.play(FadeIn(words('3 slides',LEFT*3,1.4,color=PRIMARY)),FadeIn(words('3 turns',RIGHT*3,1.4,color=SECONDARY)))
      self.play(FadeIn(formula('3+3=6',DOWN*1.8,1.6)))
      arrows=VGroup(Arrow(LEFT*4+UP*1.6,LEFT*2+UP*1.6,color=PRIMARY),CurvedArrow(RIGHT*2+UP*1.5,RIGHT*4+UP*1.5,color=SECONDARY))
      self.play(Create(arrows),run_time=3)
    with self.say('v4'):
      self.clear_stage()
      self.head('No shape-changing velocity survives')
      eq=formula('41',scale=2.5,color=ACCENT)
      self.play(FadeIn(eq))
      self.play(FadeIn(caption('First-order rigidity proves local rigidity')))


class SecondOrder(Lesson):
  def construct(self):
    self.head('A first-instant escape can be an illusion')
    h=ValueTracker(0)
    nails=VGroup(Dot(LEFT*3,color=INK),Dot(RIGHT*3,color=INK))
    rods=always_redraw(lambda: VGroup(Line(LEFT*3,UP*h.get_value(),color=PRIMARY if h.get_value()==0 else WARN,stroke_width=7),Line(UP*h.get_value(),RIGHT*3,color=PRIMARY if h.get_value()==0 else WARN,stroke_width=7),Dot(UP*h.get_value(),color=SECONDARY)))
    self.add(nails,rods)
    with self.say('s1'):
      labels=VGroup(words('1',LEFT*1.5+DOWN*.45),words('1',RIGHT*1.5+DOWN*.45))
      self.play(FadeIn(labels))
      self.play(GrowArrow(Arrow(ORIGIN,UP*1.6,buff=0,color=SECONDARY)),run_time=2)
      self.play(FadeIn(caption('Teaching example: two fixed endpoints')))
    with self.say('s2'):
      self.play(h.animate.set_value(1.6),run_time=4)
      eq=formula(r'1+h^2=1\quad\Longrightarrow\quad h=0',DOWN*1.7,scale=1.1,color=WARN)
      self.play(FadeIn(eq))
      self.play(FadeIn(words('Rejected attempt',UP*2.4,color=WARN)))
      self.wait(3)
      self.play(h.animate.set_value(0),run_time=3)
      rods.clear_updaters()
    with self.say('s3'):
      self.clear_stage()
      self.head('Second-order equations reject every escape')
      origin=LEFT*4
      rays=VGroup(*[Arrow(origin,origin+np.array([2.5*np.cos(a),2.5*np.sin(a),0]),buff=0,color=SECONDARY) for a in np.linspace(-1.1,1.1,7)])
      self.play(LaggedStart(*[GrowArrow(r) for r in rays],lag_ratio=.12),run_time=3)
      self.play(*[r.animate.set_color(WARN) for r in rays],run_time=2)
      self.play(FadeOut(rays),FadeIn(Dot(origin,color=ACCENT)),run_time=2)
      self.play(FadeIn(words('Only the zero direction remains',RIGHT*1.1,scale=.9)))
    with self.say('s4'):
      self.clear_stage()
      self.head('Six first-order flexible, second-order rigid solids')
      ids=VGroup(*[words('J'+str(i),scale=1.2,color=ACCENT if i in [60,82] else PRIMARY) for i in [58,59,60,81,82,83]]).arrange(RIGHT,buff=.6)
      self.play(LaggedStart(*[FadeIn(t) for t in ids],lag_ratio=.2),run_time=3)
      self.play(FadeIn(caption('J60 and J82 are also prestress stable',color=ACCENT)))


def census_cells():
  cells=VGroup()
  for i in range(92):
    x=(i%12-5.5)*.86
    y=2.15-(i//12)*.57
    box=RoundedRectangle(width=.72,height=.45,corner_radius=.05,stroke_color=MUTED,stroke_width=1,fill_color=BACKGROUND,fill_opacity=1).move_to([x,y,0])
    num=words(str(i+1),box.get_center(),scale=.55)
    cells.add(VGroup(box,num))
  return cells


class Census(Lesson):
  def construct(self):
    self.head('All 92 Johnson solids')
    cells=census_cells()
    with self.say('n1'):
      self.play(LaggedStart(*[FadeIn(c) for c in cells],lag_ratio=.015),run_time=4)
    with self.say('n2'):
      colour={'first-order rigid':ACCENT,'flexible':PRIMARY,'first-order flexible, second-order rigid':SECONDARY}
      for kind in colour:
        group=[cells[int(k)-1][0].animate.set_fill(colour[kind],opacity=.45).set_stroke(colour[kind]) for k,r in DATA['classification'].items() if r['class']==kind]
        self.play(*group,run_time=2)
        self.wait(1)
      legend=VGroup(words('41 first-order rigid',scale=.65,color=ACCENT),words('45 flexible',scale=.65,color=PRIMARY),words('6 second-order rigid',scale=.65,color=SECONDARY)).arrange(RIGHT,buff=.65).to_edge(DOWN,buff=.5)
      self.play(FadeIn(legend))
    with self.say('n3'):
      self.play(FadeOut(cells),FadeOut(legend))
      eq=formula(r'41+6=47',UP*.5,scale=2,color=ACCENT)
      self.play(Write(eq),run_time=3)
      self.play(FadeIn(words('locally rigid',DOWN*.8,scale=1.15,color=ACCENT)))
      self.play(FadeIn(caption(r'51 first-order flexible\quad but only 45 actually flex')))


class Evidence(Lesson):
  def construct(self):
    self.head('What the computer actually certifies')
    with self.say('e1'):
      exact=formula(r'(\sqrt{2})^2=2',UP*.9,1.6)
      self.play(Write(exact),run_time=3)
      a=words('modular arithmetic',LEFT*3+DOWN*1,scale=.9,color=PRIMARY)
      b=words('bounded intervals',RIGHT*3+DOWN*1,scale=.9,color=ACCENT)
      self.play(FadeIn(a),FadeIn(b))
      self.play(FadeIn(caption('Two formulations agree on the first-order verdicts')))
    with self.say('e2'):
      self.clear_stage()
      self.head('Different verdicts need different evidence')
      items=VGroup(words('Motion formula',color=PRIMARY),words('All constraints preserved'),words('Some distance changes',color=SECONDARY)).arrange(DOWN,buff=.8)
      self.play(LaggedStart(*[FadeIn(m) for m in items],lag_ratio=.7),run_time=5)
      self.play(FadeIn(caption('Rigid exceptions: no nonzero second-order candidate')))
    with self.say('e3'):
      self.clear_stage()
      self.head('A replayable computer-assisted theorem')
      stages=VGroup(*[Square(.4,color=ACCENT,fill_opacity=.5) for _ in range(17)]).arrange_in_grid(rows=2,buff=.2)
      self.play(LaggedStart(*[FadeIn(m) for m in stages],lag_ratio=.1),run_time=4)
      self.play(FadeIn(caption('17 stages passed in the recorded full replay')))
      self.play(FadeIn(words('Written deductions + exact certificates',DOWN*1.8,scale=.9)))


class Ending(Lesson):
  def construct(self):
    self.head('Three ideas to take away')
    with self.say('z1'):
      ideas=VGroup(words('Flat faces can change shape',color=PRIMARY),words('A motion must preserve every constraint',color=ACCENT),words('First-order freedom can be blocked',color=SECONDARY)).arrange(DOWN,buff=.85)
      self.play(LaggedStart(*[FadeIn(m) for m in ideas],lag_ratio=.6),run_time=5)
    with self.say('z2'):
      self.clear_stage()
      self.head('Local rigidity: no small wobble')
      dot=Dot(LEFT*2,color=ACCENT)
      ring=Circle(1.2,color=ACCENT).move_to(LEFT*2)
      far=Dot(RIGHT*3,color=MUTED)
      self.play(FadeIn(dot),Create(ring),run_time=2)
      self.play(FadeIn(far),FadeIn(words('Distant shapes?',RIGHT*3+UP,color=MUTED)),run_time=2)
      self.play(FadeIn(caption('Other shapes and other flex families are separate questions')))
    with self.say('z3'):
      self.clear_stage()
      lines=VGroup(words('Rigidity of the Johnson solids',scale=1.05),words('with fixed edge lengths and flat faces',scale=.9),words('Valyu Research, 2026',scale=.85,color=PRIMARY),words(r'\texttt{maths/geometry/rigidity/}',scale=.65,color=MUTED),words(r'\texttt{johnson-solids/video/}',scale=.65,color=MUTED),words('Narration uses a synthetic voice.',scale=.7,color=MUTED)).arrange(DOWN,buff=.38)
      self.play(FadeIn(lines),run_time=2)
