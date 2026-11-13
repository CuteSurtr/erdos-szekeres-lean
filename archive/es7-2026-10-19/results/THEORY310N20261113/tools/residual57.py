"""Independent check of the 57-point residual part (witness 8, root (62,-6399444)):
no 6-cap, no junction, and no convex octagon via the exact cap+cup criterion:
a convex k-gon exists iff some pair (s,t) has longest cap s..t + longest cup s..t >= k+2."""
import json
from fractions import Fraction as Fr
from real_sets import chart, orient, hull, chains
E='/home/jay/research/lean/erdos-szekeres-lean/experiments/es8-lower-bound-search-2026-10-11/saturation/witness8.txt'
S=[tuple(map(int,l.split())) for l in open(E) if l.strip()]
a=(62,-6399444); assert a in hull(S)
P=chart(S,a); n=len(P)
m={u:min((v for v in range(n) if v!=u), key=lambda v:(P[v][1]-P[u][1])/(P[v][0]-P[u][0])) for u in range(n)}
U=[u for u in range(n) if m[u]>u]
ec,ea,sc,sa,lc,la=chains(P,U)
junction=[u for u in U if ec[u]>=6 and sa[u]>=5]
R=[u for u in U if u not in junction]
print('|U|',len(U),'junctions',len(junction),'|R|',len(R))
Q=[P[u] for u in R]; k=len(Q)
# longest cap / cup from s to t (both endpoints fixed), via last-pair DP
def longest_between(sign):
    best={}
    L={}
    for t in range(k):
        for j in range(t):
            for s in range(j+1):
                pass
    # D[s][j][t]: longest chain from s ending with pair (j,t)
    D={}
    for s in range(k):
        for t in range(s+1,k):
            D[s,s,t]=2
        for j in range(s+1,k):
            for t in range(j+1,k):
                vals=[D[s,i,j] for i in range(s,j) if (s,i,j) in D and (i==s or True) and ((orient(Q[i],Q[j],Q[t])>0)==(sign>0)) and i!=j]
                if vals: D[s,j,t]=1+max(vals)
    for (s,j,t),v in D.items():
        best[s,t]=max(best.get((s,t),0),v)
    return best
cap=longest_between(-1); cup=longest_between(+1)
worst=max(cap.get(p,0)+cup.get(p,0) for p in set(cap)|set(cup))
print('max longest cap',max(cap.values()),'max longest cup',max(cup.values()),'max cap+cup over pairs',worst,'=> largest convex polygon',worst-2)
json.dump({'root':a,'R_chart_points':[[str(x),str(y)] for x,y in Q]},open('residual57_points.json','w'))
