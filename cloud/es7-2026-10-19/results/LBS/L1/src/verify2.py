# Second independent exact check (pure Python integers): general position, and
# number of 7-subsets in convex position, computed as subsets whose convex hull
# (Andrew's monotone chain) has all 7 points as vertices. Prunes with the fact
# that a subset of a convex-position set is in convex position: enumerates
# convex 4-sets, then extends only convex sets.
import sys, itertools
pts=[tuple(map(int,l.split())) for l in open(sys.argv[1]) if l.strip() and not l.startswith('#')]
n=len(pts)
def cr(o,a,b): return (a[0]-o[0])*(b[1]-o[1])-(a[1]-o[1])*(b[0]-o[0])
gp=len(set(pts))==n and all(cr(pts[a],pts[b],pts[c])!=0 for a,b,c in itertools.combinations(range(n),3))
def hullsize(ix):
    P=sorted(pts[i] for i in ix)
    lo=[];up=[]
    for p in P:
        while len(lo)>=2 and cr(lo[-2],lo[-1],p)<=0: lo.pop()
        lo.append(p)
    for p in reversed(P):
        while len(up)>=2 and cr(up[-2],up[-1],p)<=0: up.pop()
        up.append(p)
    return len(lo)+len(up)-2
level=[c for c in itertools.combinations(range(n),4) if hullsize(c)==4]
counts={4:len(level)}
for k in range(5,8):
    S=set(level); nxt=[]
    for c in level:
        for j in range(c[-1]+1,n):
            d=c+(j,)
            # all k-1 subsets must be convex (checked via S) before the hull test
            if all(d[:i]+d[i+1:] in S for i in range(k-1)) and hullsize(d)==k: nxt.append(d)
    level=nxt; counts[k]=len(level)
print("n",n,"general_position","yes" if gp else "NO", "convex4..7", counts[4],counts[5],counts[6],counts[7])
