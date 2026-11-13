# Invariance tests for gen canon: relabeling + orientation-preserving integer
# affine maps keep canon; reflections keep canonm; one point moved across a
# line (order type changes) must change canon.
import random, subprocess, sys
BIN = sys.argv[1]; files = sys.argv[2:]
def orient(a,b,c): return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
def canon(sets):
    inp = "".join(f"{len(s)} " + " ".join(f"{x} {y}" for x,y in s) + "\n" for s in sets)
    out = subprocess.run([BIN, "canon"], input=inp, capture_output=True, text=True, check=True).stdout.split("\n")
    return [tuple(l.split()) for l in out if l]
rng = random.Random(5)
fails = 0; tests = 0
for fn in files:
    S = [tuple(map(int, l.split())) for l in open(fn) if l.strip()]
    base = canon([S])[0]
    variants, kinds = [], []
    for t in range(30):
        P = S[:]; rng.shuffle(P)
        while True:
            a,b,c,d = (rng.randint(-3,3) for _ in range(4))
            if a*d-b*c != 0: break
        tx, ty = rng.randint(-50,50), rng.randint(-50,50)
        Q = [(a*x+b*y+tx, c*x+d*y+ty) for x,y in P]
        variants.append(Q); kinds.append(1 if a*d-b*c > 0 else -1)
    res = canon(variants)
    for r,k in zip(res,kinds):
        tests += 1
        if r[1] != base[1]: fails += 1; print("canonm differs", fn)
        if k > 0 and r[0] != base[0]: fails += 1; print("canon differs under det>0", fn)
    # mirror chirality info
    print(fn.split('/')[-1], "n=", len(S), "achiral" if canon([[(-x,y) for x,y in S]])[0][0]==base[0] else "chiral")
    # move one point slightly across a line through two others -> must differ
    changed = 0; trials = 0
    for t in range(20):
        i = rng.randrange(len(S))
        others = [p for j,p in enumerate(S) if j!=i]
        # pick the line (a,b) closest to S[i] in a crude sense and reflect point to other side by scaling
        a,b = rng.sample(others, 2)
        # candidate: mirror of S[i] across line ab, scaled to integers
        px,py = S[i]; dx,dy = b[0]-a[0], b[1]-a[1]
        num = (px-a[0])*dx+(py-a[1])*dy; den = dx*dx+dy*dy
        # reflection: 2*proj - p, multiply everything by den to stay integral
        T = [(x*den, y*den) for x,y in S]
        rx = 2*(a[0]*den+num*dx) - px*den; ry = 2*(a[1]*den+num*dy) - py*den
        T[i] = (rx, ry)
        if any(orient(T[u],T[v],T[w])==0 for u in range(len(T)) for v in range(u+1,len(T)) for w in range(v+1,len(T))): continue
        if max(abs(c) for p in T for c in p) >= 2**26: continue
        trials += 1
        # brute-force order-type change test: are orientation vectors equal under identity labeling?
        same = all((orient(S[u],S[v],S[w])>0)==(orient(T[u],T[v],T[w])>0) for u in range(len(S)) for v in range(u+1,len(S)) for w in range(v+1,len(S)))
        r = canon([T])[0]
        if same and r[0]!=base[0]: fails+=1; print("BUG same labeled OT, diff canon")
        if not same: changed += 1
        # (different labeled OT may still be isomorphic; only report)
        tests += 1
    print("  reflected-point trials", trials, "labeled-OT changed", changed)
print("tests", tests, "fails", fails)
