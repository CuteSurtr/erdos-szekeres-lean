# Independent check: orientation-only clauses of F hold for random mirror-symmetric 33-point
# sets with interior axis point, in the x-sort frame (ties broken as x/(1+eps*y)), y-flip if X(0,1,2) false.
import itertools, random, sys
N=33
def orient(a,b,c): return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
idx={t:n+1 for n,t in enumerate(itertools.combinations(range(N),3))}
nx=len(idx)
cls=[];
for line in open(sys.argv[1]):
    if line[0] in 'pc': continue
    c=list(map(int,line.split()))[:-1]
    if all(abs(l)<=nx for l in c): cls.append(c)
inv={v:t for t,v in idx.items()}
print('X-only clauses',len(cls))
def inside(p,pts):  # strictly inside convex hull (general position) via hull
    P=sorted(set(pts))
    def half(P):
        h=[]
        for q in P:
            while len(h)>=2 and orient(h[-2],h[-1],q)<=0: h.pop()
            h.append(q)
        return h
    lo=half(P); up=half(P[::-1]); H=lo[:-1]+up[:-1]
    return all(orient(H[i],H[(i+1)%len(H)],p)>0 for i in range(len(H)))
def gp(S):
    for a,b,c in itertools.combinations(S,3):
        if orient(a,b,c)==0: return False
    return True
rnd=random.Random(int(sys.argv[2])); ok=bad=hv=0; ties=flips=0
target=int(sys.argv[3])
while ok<target:
    R=rnd.choice([30,1000,10**6])
    xs=[rnd.randint(1,R) for _ in range(16)]
    if rnd.random()<0.4:  # force x ties
        for _ in range(rnd.randint(1,5)): xs[rnd.randrange(16)]=xs[rnd.randrange(16)]
    pairs=[(x,rnd.randint(-R,R)) for x in xs]
    S=[(x,y) for x,y in pairs]+[(-x,y) for x,y in pairs]+[(0,rnd.randint(-R,R))]
    if len(set(S))!=33 or not gp(S): continue
    c=S[-1]
    if not inside(c,S[:-1]): hv+=1; continue
    t=len(set(xs))<16; ties+=t
    # order: by x, ties: left side (x<0) by y ascending, right side (x>0) by y descending
    P=sorted(S,key=lambda p:(p[0], p[1] if p[0]<0 else -p[1]))
    assert P[16]==c
    for i in range(33): assert P[32-i]==(-P[i][0],P[i][1])
    sg={t:orient(P[t[0]],P[t[1]],P[t[2]])>0 for t in idx}
    if not sg[(0,1,2)]: sg={t:not v for t,v in sg.items()}; flips+=1
    val=lambda l: sg[inv[abs(l)]] if l>0 else not sg[inv[abs(l)]]
    viol=sum(1 for cl in cls if not any(val(l) for l in cl))
    if viol: bad+=1; print('VIOLATION',viol,S)
    ok+=1
print(f'interior sets {ok}, with x-ties {ties}, y-flipped {flips}, hull-vertex skipped {hv}, sets with violations {bad}')
