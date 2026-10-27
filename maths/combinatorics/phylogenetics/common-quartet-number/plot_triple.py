"""Draw the three 13-leaf trees T, sigma T, sigma^2 T (radial layout), leaves coloured by sigma-orbit."""
import math, re, sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
T1 = "(1,(3,6),(((7,9),(4,(5,12))),((10,11),(2,(8,13)))));"
sig = {1: 2, 2: 3, 3: 1, 4: 5, 5: 6, 6: 4, 7: 8, 8: 9, 9: 7, 10: 11, 11: 12, 12: 10, 13: 13}
app = lambda s: re.sub(r'\d+', lambda m: str(sig[int(m.group())]), s)
trees = [T1, app(T1), app(app(T1))]
def parse(s):
    s = s.strip().rstrip(';'); pos = [0]
    def rec():
        if s[pos[0]] == '(':
            pos[0] += 1; ch = [rec()]
            while s[pos[0]] == ',':
                pos[0] += 1; ch.append(rec())
            pos[0] += 1; return ch
        j = pos[0]
        while s[pos[0]].isdigit(): pos[0] += 1
        return int(s[j:pos[0]])
    return rec()
orbit_col = {}
cols = ['#b2182b', '#2166ac', '#1b7837', '#b35806', '#555555']
for i, orb in enumerate([(1, 2, 3), (4, 5, 6), (7, 8, 9), (10, 11, 12), (13,)]):
    for v in orb: orbit_col[v] = cols[i]
def leaves(t): return [t] if isinstance(t, int) else [x for c in t for x in leaves(c)]
def draw(ax, t, title):
    L = leaves(t); n = len(L)
    ang = {v: 2 * math.pi * i / n for i, v in enumerate(L)}
    def place(node, depth):
        if isinstance(node, int):
            a = ang[node]; r = 3.2
            return (r * math.cos(a), r * math.sin(a)), a
        pts = [place(c, depth + 1) for c in node]
        a = math.atan2(sum(math.sin(p[1]) for p in pts), sum(math.cos(p[1]) for p in pts))
        r = 0 if depth == 0 else 0.55 * depth + 0.1
        me = (r * math.cos(a), r * math.sin(a))
        for (xy, _) in pts:
            ax.plot([me[0], xy[0]], [me[1], xy[1]], color='#333333', lw=1.2, zorder=1)
        return me, a
    place(t, 0)
    for v in L:
        a = ang[v]; x, y = 3.2 * math.cos(a), 3.2 * math.sin(a)
        ax.scatter([x], [y], s=210, color=orbit_col[v], zorder=2, edgecolors='white', linewidths=1)
        ax.text(x, y, str(v), ha='center', va='center', color='white', fontsize=8, fontweight='bold', zorder=3)
    ax.set_title(title, fontsize=11); ax.set_aspect('equal'); ax.axis('off')
fig, axs = plt.subplots(1, 3, figsize=(11, 3.9))
for ax, t, ttl in zip(axs, trees, ['$T$', r'$\sigma T$', r'$\sigma^2 T$']):
    draw(ax, parse(t), ttl)
plt.tight_layout()
out = sys.argv[1] if len(sys.argv) > 1 else 'triple13.pdf'
plt.savefig(out, bbox_inches='tight'); plt.savefig(out.replace('.pdf', '.png'), dpi=150, bbox_inches='tight')
print('wrote', out)
