"""Exact-integer adversarial controls. Geometry/labels/assignments written here.
The residual encoder is imported only as the object under test.
"""
import collections, fractions, functools, gzip, itertools as it, json, math, pathlib, random, sys
from rows66 import S as states66, D
ROOT=pathlib.Path(__file__).resolve().parents[5]
sys.path.insert(0,str(ROOT/'cloud/es7-2026-10-19/results/RES33N20261113/tools'))
import coupled
rng=random.Random(30920261113)
def det(a,b,c): return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
def hull(p):
    p=sorted(p); a=[]; b=[]
    for q in p:
        while len(a)>1 and det(a[-2],a[-1],q)<=0: a.pop()
        a.append(q)
    for q in reversed(p):
        while len(b)>1 and det(b[-2],b[-1],q)<=0: b.pop()
        b.append(q)
    return a[:-1]+b[:-1]
def geometry(points):
    p=sorted(points); n=len(p)
    if len({x for x,y in p})!=n: return None
    signs={q:det(*(p[i] for i in q)) for q in it.combinations(range(n),3)}
    if any(v==0 for v in signs.values()): return None
    end=[{},{}]; start=[{},{}]
    for t in range(2):
        for j in range(n):
            for i in range(j): end[t][i,j]=max([2]+[end[t][k,i]+1 for k in range(i) if (signs[k,i,j]>0)==bool(t)])
        for i in reversed(range(n)):
            for j in range(i+1,n): start[t][i,j]=max([2]+[start[t][j,k]+1 for k in range(j+1,n) if (signs[i,j,k]>0)==bool(t)])
    # Exact maximum polygon via longest upper/lower chains with common endpoints.
    poly=0
    for a in range(n):
        best=[]
        for t in range(2):
            dp={(a,j):2 for j in range(a+1,n)}
            for j in range(a+1,n):
                for i in range(a+1,j):
                    cand=[dp[k,i]+1 for k in range(a,i) if (k,i) in dp and (signs[k,i,j]>0)==bool(t)]
                    if cand: dp[i,j]=max(cand)
            best.append({j:max([0]+[v for (i,k),v in dp.items() if k==j]) for j in range(a+1,n)})
        poly=max([poly]+[best[0][j]+best[1][j]-2 for j in range(a+1,n)])
    return p,end,start,poly
def inclass(g,residual):
    if g is None: return False
    p,e,s,poly=g
    if poly>7 or max(e[0].values(),default=1)>5: return False
    if not residual: return max(e[1].values(),default=1)<=5
    return all(not(max([1]+[v for (i,j),v in e[1].items() if j==u])>=6 and max([1]+[v for (i,j),v in s[0].items() if i==u])>=5) for u in range(len(p)))
rows=[(set(s),d) for s,d in json.loads((D/'used_rows.json').read_text())]
index66={s:i for i,s in enumerate(states66)}; indexR={tuple(s):i for i,s in enumerate(coupled.STATES)}
counts=collections.Counter(); coverage=set(); tight=0
def test(g,residual):
    global tight
    assert inclass(g,residual); p,e,start,poly=g; n=len(p)
    labs={(i,j):(6-start[0][i,j] if residual else e[0][i,j]-1,e[1][i,j]-1) for i,j in it.combinations(range(n),2)}
    owners=[]
    for j in range(n):
        st=tuple(max([0]+[b for (i,k),(a,b) in labs.items() if k==j and a>=col]) for col in range(1,5))
        owners.append(indexR[st+(0,)] if residual else index66[st])
    assert len(set(owners))==n and owners[0]==0
    if not residual:
        occ=set(owners); coverage.update(occ)
        for s,d in rows:
            holes=len(s-occ); assert holes>=d; tight+=holes==d
        counts['N66 sets']+=1; counts['N66 row evaluations']+=len(rows); return
    counts['residual sets']+=1
    for rep in range(3):
        chosen=rng.sample(range(n),min(n,8+rep%2)); support=[owners[i] for i in chosen]
        cnf=coupled.CNF(support); vals={}
        for key,v in cnf.ids.items():
            typ,*q=key
            if typ=='before': vals[v]=chosen[q[0]]<chosen[q[1]]
            elif typ.endswith('_ge'):
                i,j=sorted((chosen[q[0]],chosen[q[1]])); vals[v]=labs[i,j][0 if typ=='cap_ge' else 1]>=q[2]
            elif typ=='orientation': vals[v]=det(*(p[chosen[i]] for i in q))>0
            elif typ=='convex_four': vals[v]=len(hull([p[chosen[i]] for i in q]))==4
            else: raise ValueError(key)
        for c in cnf.clauses: assert any(vals[abs(l)]==(l>0) for l in c),(p,support,c)
        counts['residual CNFs']+=1; counts['residual clause evaluations']+=len(cnf.clauses)
# Archived large point sets are inputs only: all geometry is recomputed.
for line in pathlib.Path('/home/jay/research/data/verify-N66-20261113/etvsets.txt').read_text().splitlines():
    a=list(map(int,line.split())); pts=list(zip(a[1::2],a[2::2])); assert len(pts)==a[0]
    test(geometry(pts),False)
    for _ in range(5): test(geometry(rng.sample(pts,rng.randrange(25,46))),False)
z=json.loads(pathlib.Path('/home/jay/research/data/theory310-20261113/residual57_points.json').read_text())
p=[[fractions.Fraction(c) for c in q] for q in z['R_chart_points']]
den=math.lcm(*(c.denominator for q in p for c in q)); p=[tuple(int(c*den) for c in q) for q in p]
test(geometry(p),True)
for _ in range(40): test(geometry(rng.sample(p,rng.randrange(10,30))),True)
# Own independent generator: random integer insertions, accepting only in-class sets.
for residual in (False,True):
    for seed in range(50):
        pts=[]
        for trial in range(55):
            candidate=pts+[(rng.randrange(-100000,100001),rng.randrange(-100000,100001))]
            g=geometry(candidate)
            if inclass(g,residual): pts=g[0]
            if len(pts)>=16: break
        assert len(pts)>=8
        test(geometry(pts),residual)
print(json.dumps({'result':'COMPUTED: zero violations','counts':dict(counts),'N66_states_seen':len(coverage),'tight_row_evaluations':tight,'seed':30920261113}),flush=True)
