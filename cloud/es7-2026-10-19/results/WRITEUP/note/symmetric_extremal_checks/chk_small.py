from itertools import combinations
def orient(a,b,c): return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
P=[(-18,-62),(1,66),(-88,-82),(37,-76),(-7,49)]
n=len(P)
print("turns:",[orient(P[i-1],P[i],P[(i+1)%n]) for i in range(n)])
# winding number of polygon about centroid-ish: sum of angle changes
import math
ang=0
for i in range(n):
    a=P[i];b=P[(i+1)%n];c=P[(i+2)%n]
    v1=(b[0]-a[0],b[1]-a[1]);v2=(c[0]-b[0],c[1]-b[1])
    ang+=math.atan2(v1[0]*v2[1]-v1[1]*v2[0], v1[0]*v2[0]+v1[1]*v2[1])
print("total turning/2pi:",ang/(2*math.pi))
q=(-18,-62);A,B,C=(-88,-82),(37,-76),(1,66)
print("inside tri signs:",orient(A,B,q),orient(B,C,q),orient(C,A,q),"tri orient",orient(A,B,C))
# k=5 classification example
S=[(10,0),(-10,0),(0,10),(0,-10),(3,1),(-1,3),(-3,-1),(1,-3)]
col=sum(1 for t in combinations(S,3) if orient(*t)==0)
def convex(pts):
    for p in pts:
        others=[q for q in pts if q!=p]
        for t in combinations(others,3):
            s=[orient(t[0],t[1],p),orient(t[1],t[2],p),orient(t[2],t[0],p)]
            if all(x>0 for x in s) or all(x<0 for x in s): return False
    return True
print("collinear:",col,"convex4:",sum(convex(c) for c in combinations(S,4)),"convex5:",sum(convex(c) for c in combinations(S,5)))
# rotation invariance under (x,y)->(-y,x)
print("4-fold invariant:", set((-y,x) for x,y in S)==set(S))
