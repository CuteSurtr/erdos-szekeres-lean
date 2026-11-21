"""Second family for the Lemma Z / Z* control: random integer points (disk, annulus, or two arcs), distinct x,
general position enforced exactly, then greedy deletion of 7-cups/7-caps. Reuses zstar_ctrl's functions."""
import random, sys, json, importlib.util
spec = importlib.util.spec_from_file_location("zc", sys.argv[4]); zc = importlib.util.module_from_spec(spec)
src = open(sys.argv[4]).read().replace("\nmain()\n", "\n")
exec(compile(src, sys.argv[4], "exec"), zc.__dict__)
seed, nsets, npts = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
rng = random.Random(seed); out = []
def sample(kind):
    pts = []; xs = set()
    while len(pts) < npts:
        if kind == "disk":
            x, y = rng.randint(-10**6, 10**6), rng.randint(-10**6, 10**6)
            if x*x + y*y > 10**12: continue
        elif kind == "annulus":
            x, y = rng.randint(-10**6, 10**6), rng.randint(-10**6, 10**6)
            r2 = x*x + y*y
            if r2 > 10**12 or r2 < (8*10**5)**2: continue
        else:  # two noisy parabolic arcs (many cups and caps)
            t = rng.randint(-1000, 1000); s = rng.choice((1, -1))
            x, y = t * 1000 + rng.randint(-300, 300), s * t * t + rng.randint(-20000, 20000)
        if x in xs: continue
        p = (x, y)
        if any(zc.orient(a, b, p) == 0 for i, a in enumerate(pts) for b in pts[i+1:]): continue
        pts.append(p); xs.add(x)
    return sorted(pts)
for t in range(nsets):
    kind = ("disk", "annulus", "arcs")[t % 3]
    P = sample(kind)
    zc.check(P, list(range(len(P))), rng, f"{kind}{t}", out)
print("SUMMARY", json.dumps(dict(sets=len(out), all_ok=all(r['ok'] for r in out), max_Zs=max(r['Zs'] for r in out),
      sets_with_Zs_ge6=sum(r['Zs'] >= 6 for r in out), neg_cupend_has6cup=sum(r['neg_cupend_cup'] >= 6 for r in out),
      neg_capend_has6cap=sum(r['neg_capend_cap'] >= 6 for r in out))))
