"""analyze.py - describe near-miss sets: convex layers, orbit structure of the
convex 7-gons (via the verify binary), counts. usage: analyze.py verify_binary set_file..."""
import sys, subprocess, tempfile, os
def cross(o, p, q): return (p[0]-o[0])*(q[1]-o[1]) - (p[1]-o[1])*(q[0]-o[0])
def hull(ps):
    ps = sorted(ps); lo = []; up = []
    for p in ps:
        while len(lo) >= 2 and cross(lo[-2], lo[-1], p) <= 0: lo.pop()
        lo.append(p)
    for p in reversed(ps):
        while len(up) >= 2 and cross(up[-2], up[-1], p) <= 0: up.pop()
        up.append(p)
    return lo[:-1] + up[:-1]
def layers(ps):
    ps = list(ps); out = []
    while ps:
        h = hull(ps) if len(ps) > 2 else ps
        out.append(len(h)); hs = set(h); ps = [p for p in ps if p not in hs]
    return out
def sets(fn):
    cur, hdr = [], None
    for line in open(fn):
        if line.startswith('#'):
            if line.startswith('# restart') or line.startswith('# c7'):
                if cur: yield hdr, cur
                cur, hdr = [], line.strip()
            continue
        if line.strip(): cur.append(tuple(map(int, line.split()[:4])))
    if cur: yield hdr, cur
vb = sys.argv[1]
for fn in sys.argv[2:]:
    for hdr, pts in sets(fn):
        uv = [(p[2], p[3]) for p in pts]
        with tempfile.NamedTemporaryFile('w', delete=False, suffix='.txt') as t:
            for p in pts: t.write('%d %d %d %d\n' % p)
        out = subprocess.run([vb, t.name], capture_output=True, text=True).stdout; os.unlink(t.name)
        d = dict(l.split()[:2] for l in out.splitlines() if l.split() and l.split()[0] in ('convex6', 'convex7', 'six_plus_one'))
        gons = [list(map(int, l.split()[1:])) for l in out.splitlines() if l.startswith('convex7gon')]
        orb = [sorted(set(i % 11 for i in g)) for g in gons]
        S = set((p[0], p[1]) for p in pts); sym = all((-b, a-b) in S for a, b, *_ in pts)
        print(os.path.basename(fn), hdr, '| sym', sym, '| layers', layers(uv), '| c7', d.get('convex7'), 'c6', d.get('convex6'),
              '6+1', d.get('six_plus_one'), '| 7-gon orbit reps', orb[:3])
