# Mirror-symmetric version of the classical (Lovasz form) 2^(n-2) construction,
# Morris-Soltan Thm 2.6: block T_i (C(n-2,i) pts, no (i+2)-cap, no (n-i)-cup, |slopes|<=1)
# near the unit-circle point at angle pi/4 - i*pi/(2(n-2)); here T_{n-2-i} := mirror(T_i).
import math, itertools, time
from fractions import Fraction as F
from sets import Pau, normalize
from check import orient, max_convex

def largest_convex(P):
    n=len(P); best=min(n,2)
    for a in range(n):
        p=P[a]
        up=[i for i in range(n) if P[i][1]>p[1] or (P[i][1]==p[1] and P[i][0]>p[0])]
        up.sort(key=lambda i: math.atan2(float(P[i][1]-p[1]),float(P[i][0]-p[0])))
        m=len(up)
        dp=[[0]*m for _ in range(m)]   # dp[i][j]: chain p->...->up[i]->up[j], vertex count
        for j in range(m):
            for i in range(j):
                dp[i][j]=3 if orient(p,P[up[i]],P[up[j]])>0 else 0
        for j in range(m):
            for i in range(j):
                if dp[i][j]==0: continue
                for k in range(j+1,m):
                    if orient(P[up[i]],P[up[j]],P[up[k]])>0 and dp[i][j]+1>dp[j][k]:
                        dp[j][k]=dp[i][j]+1
        for i in range(m):
            for j in range(i+1,m):
                if dp[i][j] and orient(P[up[i]],P[up[j]],p)>0: best=max(best,dp[i][j])
    return best

def mirror_construction(n, r=F(1,10**4)):
    blocks={}
    for i in range(n-1):
        j=n-2-i
        if i<j:
            T=normalize(Pau(i+2, n-i))   # Pau(a,u): no a-cap, no u-cup
            blocks[i]=T; blocks[j]=[(x,-y) for x,y in T]
        elif i==j:
            blocks[i]=normalize(Pau(i+2,n-i))
    pts=[]
    for i in range(n-1):
        th=math.pi/4 - i*math.pi/(2*(n-2))
        cx=F(round(math.cos(th)*10**6),10**6); cy=F(round(math.sin(th)*10**6),10**6)
        if i>n-2-i:   # mirror centre exactly
            cx2,cy2=centres[n-2-i]; cx,cy=cx2,-cy2
        centres_set(i,(cx,cy))
        pts+=[(cx+r*x, cy+r*y) for x,y in blocks[i]]
    return pts
centres={}
def centres_set(i,c): centres[i]=c

if __name__=='__main__':
    from sets import four, five, ES
    t=time.time()
    for name,P in [("ES6",ES(6)),("4-fold",four),("5-fold",five)]:
        print(name,"largest convex (DP):",largest_convex(P))
    M=mirror_construction(7)
    print("mirror n=7: points",len(M),"min|orient|>0:",min(abs(orient(*q)) for q in itertools.combinations(M,3))>0)
    S=set(M); print("mirror-closed under y->-y:",all((x,-y) in S for x,y in M),"points on axis:",sum(1 for x,y in M if y==0))
    print("largest convex subset:",largest_convex(M),"time",round(time.time()-t,1))
