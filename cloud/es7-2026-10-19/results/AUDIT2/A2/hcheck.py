# Independent check: orientation-only clauses of the sub-case (i) CNF hold for random mirror-symmetric
# 33-point sets whose axis point p is a hull vertex. Frame: y-flip if p is the bottom point; label 0 = p,
# labels 1..32 = the other points sorted by u = x/(y0-y); X(i,j,k) = [orient > 0] on the ORIGINAL points.
import itertools, random, sys
from fractions import Fraction as Fr
N=33
def orient(a,b,c): return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
idx={t:n+1 for n,t in enumerate(itertools.combinations(range(N),3))}; nx=len(idx); inv={v:t for t,v in idx.items()}
cls=[]
for line in open(sys.argv[1]):
    if line[0] in 'pc': continue
    c=list(map(int,line.split()))[:-1]
    if all(abs(l)<=nx for l in c): cls.append(c)
print('X-only clauses',len(cls))
def gp(S): return all(orient(a,b,c)!=0 for a,b,c in itertools.combinations(S,3))
rnd=random.Random(int(sys.argv[2])); ok=bad=0; bottoms=0; target=int(sys.argv[3])
while ok<target:
    R=rnd.choice([30,1000,10**6])
    pairs=[(rnd.randint(1,R),rnd.randint(-R,R)) for _ in range(16)]
    top=rnd.random()<0.5
    ymax=max(y for _,y in pairs); ymin=min(y for _,y in pairs)
    y0=ymax+rnd.randint(1,R) if top else ymin-rnd.randint(1,R)
    S=[(x,y) for x,y in pairs]+[(-x,y) for x,y in pairs]+[(0,y0)]
    if len(set(S))!=33 or not gp(S): continue
    if not top: S=[(x,-y) for x,y in S]; bottoms+=1
    p=S[-1]; y0=p[1]
    others=sorted(S[:-1],key=lambda q:Fr(q[0],y0-q[1]))
    P=[p]+others
    for i in range(1,33): assert P[33-i]==(-P[i][0],P[i][1])
    sg={t:orient(P[t[0]],P[t[1]],P[t[2]])>0 for t in idx}
    val=lambda l: sg[inv[abs(l)]] if l>0 else not sg[inv[abs(l)]]
    viol=sum(1 for cl in cls if not any(val(l) for l in cl))
    if viol: bad+=1; print('VIOLATION',viol)
    ok+=1
print(f'hull-vertex sets {ok} (bottom, flipped: {bottoms}), sets with violations {bad}')
