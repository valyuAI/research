from manim import *
from vrvideo import *
from itertools import product

SCENES=['Pairing','Cube','Matching','Surplus','Central','Noncentral','Correction','SixCube','Scope']
PAIRS=[[2,6,8,5,8],[11,10,3,1,10],[11,4,0,4,12],[9,1,9,5,12],[7,6,3,7,2]]


def formula(s,pos=ORIGIN,scale=1.0,color=INK):
  return MathTex(s,color=color).scale(scale).move_to(pos)


def board(rows,size=.82):
  group=VGroup()
  n=len(rows)
  for i,row in enumerate(rows):
    line=VGroup()
    for j,v in enumerate(row):
      pos=np.array([(j-(n-1)/2)*size,((n-1)/2-i)*size,0])
      square=Square(size,stroke_color=MUTED,stroke_width=1.4).move_to(pos)
      num=formula(str(v) if v else r'\cdot',pos,.8,PRIMARY if v else MUTED)
      line.add(VGroup(square,num))
    group.add(line)
  return group


def project(p,n=7):
  x,y,z=np.array(p)-(n+1)/2
  return np.array([.58*x+.29*z,.58*y+.19*z,0])


def cube(n=7,points=True):
  vertices=list(product([1,n],repeat=3))
  edges=VGroup(*[Line(project(a,n),project(b,n),color=MUTED,stroke_width=1.7) for i,a in enumerate(vertices) for b in vertices[i+1:] if sum(x!=y for x,y in zip(a,b))==1])
  dots=VGroup(*[Dot(project(p,n),radius=.023,color=SOFT) for p in product(range(1,n+1),repeat=3)]) if points else VGroup()
  return VGroup(edges,dots)


def all_lines(n):
  cells=list(product(range(1,n+1),repeat=3));out=[]
  for d in product([-1,0,1],repeat=3):
    if d==(0,0,0) or next(x for x in d if x)!=1:continue
    for p in cells:
      end=tuple(p[i]+(n-1)*d[i] for i in range(3))
      if all(1<=x<=n for x in end):out.append(tuple(tuple(p[i]+k*d[i] for i in range(3)) for k in range(n)))
  return out


LINES=all_lines(7)
DIAGONALS=[l for l in LINES if all(l[0][i]!=l[-1][i] for i in range(3))]


def mark(p,kind='O',color=ACCENT):
  return formula(kind,project(p),.85,color)


def graph(nslots=4,ncells=7):
  slots=VGroup(*[Circle(.18,color=PRIMARY,fill_opacity=.5).move_to([-2.4,1.8-i*3.6/max(1,nslots-1),0]) for i in range(nslots)])
  cells=VGroup(*[Dot([2.4,2.1-j*4.2/max(1,ncells-1),0],radius=.13,color=ACCENT) for j in range(ncells)])
  return slots,cells


class Lesson(NarratedScene):
  def clear_frame(self):
    if self.mobjects:self.play(*[FadeOut(m) for m in list(self.mobjects)],run_time=.6)

  def heading(self,s):
    new=title(s,.85)
    if getattr(self,'_heading',None) in self.mobjects:
      self.play(Transform(self._heading,new),run_time=.6)
    else:
      self._heading=new
      self.play(FadeIn(new),run_time=.6)


class Pairing(Lesson):
  def construct(self):
    with self.say('t01'):
      b=board([[0]*3 for _ in range(3)],1.1)
      self.play(Create(b))
      for j in [0,1]:self.play(Transform(b[0][j][1],formula('X',b[0][j].get_center(),1.1,SECONDARY)),run_time=.8)
      self.play(Transform(b[0][2][1],formula('O',b[0][2].get_center(),1.1,ACCENT)),run_time=1)
      self.heading('Maker makes a line. Breaker blocks every line.')
    with self.say('t02'):
      self.clear_frame()
      b=board(PAIRS,.87)
      self.play(LaggedStart(*[Create(row) for row in b],lag_ratio=.25),run_time=3)
      self.heading('Every winning line contains a complete pair')
      h=VGroup(boxed(b[0][2],SECONDARY),boxed(b[0][4],SECONDARY))
      self.play(Create(h),run_time=1.5)
    with self.say('t03'):
      self.play(FadeOut(h))
      for a,c in [((0,2),(0,4)),((1,0),(2,0)),((1,3),(3,1))]:
        self.play(Transform(b[a[0]][a[1]][1],formula('X',b[a[0]][a[1]].get_center(),.8,SECONDARY)),run_time=.7)
        self.play(Transform(b[c[0]][c[1]][1],formula('O',b[c[0]][c[1]].get_center(),.8,ACCENT)),run_time=.7)
      self.play(FadeIn(caption('Answer each numbered move by taking its partner')))
    with self.say('t04'):
      self.clear_frame()
      points=VGroup(*[Dot(p,radius=.16,color=PRIMARY) for p in [LEFT*3,ORIGIN,RIGHT*3]])
      links=VGroup(Line(LEFT*3,ORIGIN,color=PRIMARY),Line(ORIGIN,RIGHT*3,color=SECONDARY))
      self.play(Create(points),Create(links))
      self.play(Create(Circle(.4,color=WARN).move_to(ORIGIN)))
      self.heading('A cell cannot be promised to two different lines')
      self.play(FadeIn(caption('Two private cells per surviving line')))


class Cube(Lesson):
  def construct(self):
    with self.say('t05'):
      c=cube()
      self.play(Create(c[0]),FadeIn(c[1]),run_time=3)
      demos=[((1,1,1),(7,1,1)),((1,1,1),(7,7,1)),((1,1,1),(7,7,7))]
      for (a,b),col in zip(demos,[PRIMARY,SECONDARY,ACCENT]):self.play(Create(Line(project(a),project(b),color=col,stroke_width=6)),run_time=1.4)
      self.heading('Axis line, plane diagonal, space diagonal')
    with self.say('t06'):
      self.clear_frame()
      c=cube().scale(.72).shift(LEFT*3)
      self.play(Create(c))
      terms=VGroup(formula(r'3\cdot7^2=147'),formula(r'6\cdot7=42'),formula('4')).arrange(DOWN,buff=.45).shift(RIGHT*2.6)
      self.play(LaggedStart(*[Write(t) for t in terms],lag_ratio=.3),run_time=3)
      self.play(FadeIn(caption('$147+42+4=193$ lines; two cells each needs $386$')))
    with self.say('t07'):
      self.clear_frame()
      c=cube();self.play(Create(c))
      self.play(FadeIn(mark((4,4,4))))
      centre_lines=VGroup(*[Line(project(l[0]),project(l[-1]),color=ACCENT,stroke_width=2) for l in LINES if (4,4,4) in l])
      self.play(LaggedStart(*[Create(l) for l in centre_lines],lag_ratio=.08),run_time=2)
      self.play(centre_lines.animate.set_color(MUTED).set_opacity(.35),run_time=1)
      self.heading('Only 343 cells: first kill lines with Breaker marks')


class Matching(Lesson):
  def construct(self):
    with self.say('t08'):
      slots,cells=graph(4,5)
      edges=VGroup(*[Line(slots[i].get_center(),cells[j].get_center(),color=SOFT,stroke_width=2) for i,js in enumerate([[0,1,2],[0,1,2],[2,3,4],[2,3,4]]) for j in js])
      self.play(Create(slots),Create(cells));self.play(Create(edges),run_time=2)
      assignments=VGroup(*[Line(slots[i].get_center(),cells[j].get_center(),color=ACCENT,stroke_width=5) for i,j in enumerate([0,1,3,4])])
      self.play(LaggedStart(*[Create(e) for e in assignments],lag_ratio=.3),run_time=2)
      self.heading('Two slots per line; one distinct cell per slot')
      self.play(FadeIn(caption('Illustrative graph, not the full cube')))
    with self.say('t09'):
      self.clear_frame()
      slots,cells=graph(3,5)
      edges=VGroup(*[Line(s.get_center(),cells[j].get_center(),color=WARN,stroke_width=2) for s in slots for j in [0,1]])
      self.play(Create(slots),Create(cells),Create(edges))
      shortage_slots=boxed(slots,WARN)
      shortage_cells=boxed(VGroup(*cells[:2]),WARN)
      self.play(Create(shortage_slots),Create(shortage_cells))
      self.heading('Three slots reach only two cells: impossible')
    with self.say('t10'):
      more=VGroup(*[Line(s.get_center(),cells[2].get_center(),color=PRIMARY,stroke_width=2) for s in slots])
      self.play(Create(more),run_time=2)
      self.play(*[Create(Line(slots[i].get_center(),cells[i].get_center(),color=ACCENT,stroke_width=5)) for i in range(3)],run_time=2)
      self.play(shortage_slots.animate.set_color(ACCENT),Transform(shortage_cells,boxed(VGroup(*cells[:3]),ACCENT)),run_time=.7)
      self.heading('A third reachable cell repairs this shortage')
      self.play(FadeIn(caption("Hall: every group must reach at least its own number of cells")))


class Surplus(Lesson):
  def construct(self):
    slots,cells=graph()
    with self.say('t11'):
      edges=VGroup(*[Line(s.get_center(),c.get_center(),color=SOFT,stroke_width=1) for s in slots for c in cells])
      self.play(Create(slots),Create(cells),Create(edges),run_time=2)
      self.heading('Illustration: four slots reach seven cells')
      before=caption(r'Before deletion: surplus $=\min_{S\ne\emptyset}(|N(S)|-|S|)=3$')
      self.play(FadeIn(before))
    with self.say('t12'):
      self.heading('Delete three cells, then reroute the matching')
      assigned=VGroup(*[Line(slots[i].get_center(),cells[i].get_center(),color=ACCENT,stroke_width=5) for i in range(4)])
      self.play(Create(assigned))
      self.play(*[Create(Cross(cells[j],color=WARN,scale_factor=2)) for j in [0,2,5]],run_time=2)
      self.play(*[edges[i*7+j].animate.set_opacity(.08) for i in range(4) for j in [0,2,5]],run_time=.7)
      remaining=[1,3,4,6]
      self.play(*[Transform(assigned[i],Line(slots[i].get_center(),cells[j].get_center(),color=SECONDARY,stroke_width=5)) for i,j in enumerate(remaining)],run_time=3)
      self.play(Transform(before,caption('After deletion: $4-4=0$; a matching still exists')),run_time=.7)
    with self.say('t13'):
      self.play(Indicate(assigned,color=ACCENT),run_time=2)
      self.play(FadeIn(Tex('Any three deletions still leave a matching',color=ACCENT).scale(.78).shift(UP*2.65)))
    with self.say('t14'):
      self.clear_frame()
      slots,cells=graph(4,7)
      self.play(Create(slots),Create(cells))
      copies=VGroup(*[Circle(.16,color=SECONDARY,fill_opacity=.5).move_to([-3.8,y,0]) for y in [1.8,.5,-.8]])
      self.play(TransformFromCopy(slots[0],copies),run_time=2)
      allslots=[*slots,*copies]
      assigned=VGroup(*[Line(s.get_center(),c.get_center(),color=ACCENT,stroke_width=3) for s,c in zip(allslots,cells)])
      self.play(LaggedStart(*[Create(e) for e in assigned],lag_ratio=.2),run_time=3)
      self.heading('Replication test: add three copies of one slot')
    with self.say('t15'):
      self.play(Create(boxed(VGroup(slots[0],slots[1],*copies),SECONDARY)),run_time=2)
      self.play(Indicate(VGroup(*cells[:2],*cells[4:]),color=ACCENT),run_time=2)
      self.play(FadeIn(caption('Test each line; its two slots have identical neighbours')))


class Central(Lesson):
  def construct(self):
    known=(4,4,4);chosen=[(5,5,5)];used={next(i for i,l in enumerate(DIAGONALS) if chosen[0] in l)}
    while len(chosen)<4:
      old={i for i,l in enumerate(LINES) if any(b in l for b in chosen)}
      candidates=[(sum(p in l and i not in old for i,l in enumerate(LINES)),p,j) for j,line in enumerate(DIAGONALS) if j not in used for p in line if p!=known]
      _,p,j=min(candidates,key=lambda v:(-v[0],v[1]))
      chosen.append(p);used.add(j)
    with self.say('t16'):
      c=cube();self.play(Create(c))
      diagonal_lines=VGroup(*[Line(project(l[0]),project(l[-1]),color=PRIMARY,stroke_width=3) for l in DIAGONALS])
      self.play(Create(diagonal_lines),FadeIn(mark(known,'X',SECONDARY)))
      for p in chosen:self.play(FadeIn(mark(p)),run_time=1.2)
      self.heading('Central opening: one Breaker cell on each space diagonal')
    with self.say('t17'):
      killed=[l for l in LINES if any(p in l for p in chosen)]
      overlay=VGroup(*[Line(project(l[0]),project(l[-1]),color=ACCENT,stroke_width=1.3) for l in killed])
      self.play(Create(overlay),run_time=2)
      self.play(overlay.animate.set_color(MUTED).set_opacity(.35),run_time=2)
      self.play(FadeIn(caption('27 lines met; 166 alive; three Maker moves unspecified')))
    with self.say('t18'):
      self.clear_frame()
      spare=VGroup(*[Circle(.4,color=ACCENT,fill_opacity=.4) for _ in range(4)]).arrange(RIGHT,buff=.5)
      self.play(Create(spare))
      self.play(LaggedStart(*[Create(Cross(x,color=SECONDARY)) for x in spare[:3]],lag_ratio=.4),run_time=3)
      self.heading('Surplus at least four absorbs any three unknown moves')
    with self.say('t19'):
      self.clear_frame()
      root=Dot(UP*1.5,color=PRIMARY,radius=.16)
      branches=VGroup(*[Dot([x,-.3,0],color=PRIMARY,radius=.12) for x in [-4,-2,0,2,4]])
      self.play(Create(root),Create(branches))
      self.play(*[Create(Line(root.get_center(),b.get_center(),color=PRIMARY)) for b in branches],run_time=2)
      self.play(Write(formula(r'10{,}627\text{ leaves}\ \longrightarrow\ 14\text{ final sets}',DOWN*1.8,1.1)))
      self.heading('The greedy opening survives every relevant reply')
    with self.say('t20'):
      self.clear_frame()
      rows=[('27','576',r'\ge4'),('26','288',r'\ge4'),('25','384','2'),('22','48',r'\text{none}')]
      table=VGroup(*[formula(rf'{met}\quad {count}\quad {surplus}',scale=1.15,color=ACCENT if i<2 else MUTED) for i,(met,count,surplus) in enumerate(rows)]).arrange(DOWN,buff=.45)
      self.play(LaggedStart(*[Write(r) for r in table],lag_ratio=.3),run_time=3)
      self.heading('Lines met / number of sets / surplus')
      self.play(FadeIn(caption('All 1,296 central configurations; surplus capped at four')))
    with self.say('t21'):
      self.play(table[2].animate.set_color(SECONDARY),table[3].animate.set_color(WARN),run_time=2)
      self.play(Create(boxed(VGroup(*table[:2]),ACCENT)),run_time=2)


class Noncentral(Lesson):
  def construct(self):
    a=(1,1,1)
    partners=[p for line in DIAGONALS if a not in line for p in line if p!=(4,4,4) and not any(a in l and p in l for l in LINES)]
    b=sorted(partners)[0]
    with self.say('t22'):
      self.play(Create(cube()),FadeIn(mark((2,3,4),'X',SECONDARY)))
      self.play(FadeIn(mark((4,4,4))),FadeIn(mark(a)),run_time=2)
      candidates=VGroup(*[Circle(.09,color=WARM).move_to(project(p)) for p in partners])
      self.play(Create(candidates),run_time=2)
      self.play(FadeIn(mark(b)),run_time=1)
      self.heading('Every diagonal choice has 12 compatible partners')
    with self.say('t23'):
      self.clear_frame()
      cells=VGroup(*[Circle(.42,color=ACCENT,fill_opacity=.4) for _ in range(3)]).arrange(RIGHT,buff=.65)
      self.play(Create(cells))
      self.play(Create(Cross(cells[0],color=SECONDARY)),Create(Cross(cells[1],color=SECONDARY)),run_time=2)
      self.heading('48,960 legal configurations: surplus exactly 3')
      self.play(FadeIn(caption('25 lines met; two unknown Maker moves removed')))
    with self.say('t24'):
      self.clear_frame()
      self.play(Write(formula(r'24{,}480+24{,}480=48{,}960',UP*.7,1.35)),run_time=3)
      self.play(Write(formula(r'1{,}158\text{ symmetry classes}',DOWN*.8,1.15,ACCENT)),run_time=2)
      self.heading('Independent reconstruction agrees')
      self.play(FadeIn(caption('Each position needs multiple matching tests')))


class Correction(Lesson):
  def construct(self):
    with self.say('t25'):
      c=cube();self.play(Create(c))
      self.heading(r'Known seven-cube result: Cain, Raymond, K\"allersj\"o (2025)')
      self.play(FadeIn(caption('New certificate and correction; the theorem remains true')))
    with self.say('t26'):
      self.clear_frame()
      c=cube(points=False);self.play(Create(c))
      p=(1,7,1);q=(6,2,6)
      a=mark(p,'X',SECONDARY);b=mark(q,'X',WARN)
      self.play(FadeIn(a),FadeIn(b))
      sign_a=formula(r'(-,+,-)',LEFT*4.8+UP*2,.9,SECONDARY)
      sign_b=formula(r'(+,-,+)',RIGHT*4.8+DOWN*2,.9,WARN)
      self.play(Write(sign_a),Write(sign_b))
      self.heading('Opposite octants: $(1,7,1)$ and $(6,2,6)$')
    with self.say('t27'):
      self.heading('Axis swaps and reflections preserve opposite signs')
      for transform in [lambda v:(v[2],v[0],v[1]),lambda v:(8-v[0],v[1],v[2])]:
        pp,qq=transform(p),transform(q)
        signs=lambda v:'('+','.join('+' if x>4 else '-' for x in v)+')'
        self.play(a.animate.move_to(project(pp)),b.animate.move_to(project(qq)),Transform(sign_a,formula(signs(pp),sign_a.get_center(),.9,SECONDARY)),Transform(sign_b,formula(signs(qq),sign_b.get_center(),.9,WARN)),run_time=2)
      self.play(FadeIn(caption('2,916 unordered pairs; 5,832 ordered pairs')))
    with self.say('t28'):
      self.clear_frame()
      self.play(Create(cube(points=False)))
      sequence=[((1,7,1),'X'),((4,4,4),'O'),((6,2,6),'X'),((5,5,5),'O'),((7,1,7),'X')]
      for p,k in sequence:self.play(FadeIn(mark(p,k,SECONDARY if k=='X' else ACCENT)),run_time=.8)
      for p in [(6,2,6),(7,1,7)]:self.play(Create(Circle(.24,color=WARN).move_to(project(p))),run_time=.8)
      self.heading('Both prescribed third replies are already occupied')
      self.play(FadeIn(caption('A gap in the written case analysis; unseen code is not assessed')))


class SixCube(Lesson):
  def construct(self):
    with self.say('t29'):
      c=cube(6).shift(LEFT*3)
      self.play(Create(c))
      vals=VGroup(formula(r'216-14=202'),formula(r'202/2=101'),formula(r'148-101=47',color=SECONDARY)).arrange(DOWN,buff=.55).shift(RIGHT*2.6)
      self.play(LaggedStart(*[Write(v) for v in vals],lag_ratio=.5),run_time=4)
      self.heading('After seven rounds: at least 47 lines must be killed')
    with self.say('t30'):
      self.clear_frame()
      groups=VGroup(*[VGroup(*[Dot(radius=.075,color=PRIMARY) for _ in range(6)]).arrange(RIGHT,buff=.13) for _ in range(7)]).arrange(DOWN,buff=.22).shift(LEFT*2)
      extras=VGroup(*[Dot(radius=.12,color=ACCENT) for _ in range(4)]).arrange(DOWN,buff=.45).shift(RIGHT*1.5)
      self.play(LaggedStart(*[Create(g) for g in groups],lag_ratio=.17),Create(extras),run_time=3)
      self.play(Write(formula(r'7\cdot6+4=46<47',DOWN*2.5,1.35,WARN)))
      self.heading('At most six ordinary lines per cell, plus four space diagonals')
    with self.say('t31'):
      self.clear_frame()
      cells=VGroup(*[Square(.8,color=PRIMARY,fill_opacity=.2) for _ in range(6)]).arrange(RIGHT,buff=.2)
      self.play(Create(cells))
      self.play(Create(boxed(VGroup(*cells[:2]),ACCENT)))
      capacity=formula(r'6-2=4',DOWN*1.7,1.6)
      self.play(Write(capacity))
      self.play(Create(Cross(cells[-1],color=SECONDARY)),run_time=1.5)
      self.play(Transform(capacity,formula('5-2=3',DOWN*1.7,1.6,SECONDARY)),run_time=1)
      self.heading('One surviving line caps surplus at four')


class Scope(Lesson):
  def construct(self):
    with self.say('t32'):
      c7=cube(7,False).scale(.65).shift(LEFT*3.3);c6=cube(6,False).scale(.65).shift(RIGHT*3.3)
      self.play(Create(c7),Create(c6))
      self.play(Write(formula(r'7^3:\ \text{Breaker wins}',LEFT*3.3+DOWN*2,1,ACCENT)),Write(formula(r'6^3:\ \text{OPEN}',RIGHT*3.3+DOWN*2,1,SECONDARY)))
      self.heading('The $5^3$ and $6^3$ games remain open')
    with self.say('t33'):
      self.clear_frame()
      blocks=VGroup(Tex('Abstract Hall / surplus lemmas',color=ACCENT).scale(.85),Tex('Finite board certificates: exact programs').scale(.85),Tex('Whole-game argument: written proof').scale(.85)).arrange(DOWN,buff=.8)
      self.play(LaggedStart(*[Write(b) for b in blocks],lag_ratio=.3),run_time=3)
      self.heading('Lean scope is the abstract mathematics')
      self.play(FadeIn(caption('No formal board enumeration or whole-game claim')))
    with self.say('t34'):
      self.clear_frame()
      pair=VGroup(Dot(LEFT*.5,color=PRIMARY,radius=.15),Dot(RIGHT*.5,color=ACCENT,radius=.15),Line(LEFT*.5,RIGHT*.5,color=ACCENT)).shift(LEFT*4)
      spare=VGroup(*[Circle(.22,color=ACCENT) for _ in range(3)]).arrange(RIGHT).shift(RIGHT*3)
      self.play(Create(pair),Create(spare),Write(formula(r'\ge',scale=1.6)),run_time=2)
      self.wait(3)
      self.clear_frame()
      end=VGroup(Tex(r'A Hall-surplus certificate for $7\times7\times7$ tic-tac-toe').scale(.85),Tex('Valyu Research, 2026').scale(.8),Tex(r'\texttt{maths/combinatorics/combinatorial-games/}').scale(.59),Tex(r'\texttt{cubic-tic-tac-toe-surplus}').scale(.62),Tex('Narration uses a synthetic voice.',color=MUTED).scale(.65)).arrange(DOWN,buff=.38)
      self.play(FadeIn(end),run_time=1)
