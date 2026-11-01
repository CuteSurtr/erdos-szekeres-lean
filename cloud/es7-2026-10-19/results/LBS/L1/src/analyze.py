# Near-miss analysis of a point set: convex k-gon counts (k=4..7), the convex
# 7-gons themselves, how many distinct convex 6-gons lie in a convex 7-gon
# ("6-gons-plus-one"), points whose deletion leaves no convex 7-gon, and the
# sizes of the convex-hull layers (onion peeling).
import sys, itertools
pts=[tuple(map(int,l.split())) for l in open(sys.argv[1]) if l.strip() and not l.startswith('#')]
n=len(pts)
def cr(o,a,b): return (a[0]-o[0])*(b[1]-o[1])-(a[1]-o[1])*(b[0]-o[0])
def hull(ix):
    P=sorted(ix,key=lambda i:pts[i]); lo=[];up=[]
    for p in P:
        while len(lo)>=2 and cr(pts[lo[-2]],pts[lo[-1]],pts[p])<=0: lo.pop()
        lo.append(p)
    for p in reversed(P):
        while len(up)>=2 and cr(pts[up[-2]],pts[up[-1]],pts[p])<=0: up.pop()
        up.append(p)
    return lo[:-1]+up[:-1]
level=[c for c in itertools.combinations(range(n),4) if len(hull(c))==4]; lv={4:level}
for k in range(5,8):
    S=set(level); level=[c+(j,) for c in level for j in range(c[-1]+1,n) if all((c+(j,))[:i]+(c+(j,))[i+1:] in S for i in range(k-1)) and len(hull(c+(j,)))==k]; lv[k]=level
print("n",n,"convex k-gons k=4..7:",*[len(lv[k]) for k in range(4,8)])
s6=set(); part=[0]*n
for g in lv[7]:
    for i in range(7): s6.add(g[:i]+g[i+1:])
    for i in g: part[i]+=1
print("convex 7-gons:",lv[7][:10],"..." if len(lv[7])>10 else "")
print("distinct convex 6-gons inside a convex 7-gon:",len(s6),"of",len(lv[6]))
print("points in some 7-gon:",sum(1 for x in part if x),"max participation:",max(part))
print("deleting one point leaves 0 convex 7-gons for:",[i for i in range(n) if part[i]==len(lv[7])])
rest=list(range(n)); layers=[]
while rest:
    h=hull(rest) if len(rest)>2 else rest; layers.append(len(h)); rest=[i for i in rest if i not in h]
print("hull layers:",layers)
