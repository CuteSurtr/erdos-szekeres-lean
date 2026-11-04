import random, itertools, sys, math, importlib.util
from functools import cmp_to_key
src=open('verify60.py').read()
# reuse the DP code only (copy of function body) for testing on arbitrary point lists
def cr(o,p,q): return (p[0]-o[0])*(q[1]-o[1])-(p[1]-o[1])*(q[0]-o[0])
def largest(P,key):
    best=0
    for p in P:
        Q=[q for q in P if key(q)>key(p)]
        Q.sort(key=cmp_to_key(lambda u,v: -1 if cr(p,u,v)>0 else 1))
        m=len(Q); L={}
        for j in range(m):
            for i in range(j):
                v=3
                for h in range(i):
                    if (h,i) in L and cr(Q[h],Q[i],Q[j])>0 and L[(h,i)]+1>v: v=L[(h,i)]+1
                L[(i,j)]=v
                if cr(Q[i],Q[j],p)>0 and v>best: best=v
    return best
assert 'def largest(key):' in src and 'cr(Q[i],Q[j],p)>0' in src   # same DP as verify60.py
def convex_pos(S):
    # brute force: every point is a hull vertex <=> no point inside a triangle of the others (general position)
    for x in S:
        for a,b,c in itertools.combinations([y for y in S if y!=x],3):
            o1,o2,o3=cr(a,b,x),cr(b,c,x),cr(c,a,x)
            if (o1>0 and o2>0 and o3>0) or (o1<0 and o2<0 and o3<0): return False
    return True
def brute(P):
    for k in range(len(P),2,-1):
        for S in itertools.combinations(P,k):
            if convex_pos(S): return k
    return 2
random.seed(5); bad=0
for t in range(150):
    n=random.randint(6,11)
    while True:
        P=[(random.randint(-40,40),random.randint(-40,40)) for _ in range(n)]
        if len(set(P))==n and all(cr(a,b,c)!=0 for a,b,c in itertools.combinations(P,3)): break
    b1=brute(P); d1=largest(P,lambda q:(q[1],q[0])); d2=largest(P,lambda q:(q[0],q[1]))
    if not (b1==d1==d2): bad+=1; print('MISMATCH', P, b1, d1, d2)
print('random small sets vs brute force: 150 tested, mismatches', bad)
# planted convex 9-gon plus noise
for t in range(20):
    R=10**6; pts=[(int(R*math.cos(2*math.pi*k/9+0.1)), int(R*math.sin(2*math.pi*k/9+0.1))) for k in range(9)]
    pts+= [(random.randint(-10**5,10**5),random.randint(-10**5,10**5)) for _ in range(30)]
    pts=list(dict.fromkeys(pts))
    if any(cr(a,b,c)==0 for a,b,c in itertools.combinations(pts,3)): continue
    d=largest(pts,lambda q:(q[1],q[0]))
    assert d>=9, d
print('planted convex 9-gons detected: OK')
