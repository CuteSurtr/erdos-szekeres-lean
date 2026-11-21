import json
from resstate import *
exec(open('real57.py').read().split("O,Ecup,Ecap,Fcap=tables(P)")[0])
O,Ecup,Ecap,Fcap=tables(P); n=len(P); St=states(P,O,Ecup,Fcap)
Fcup=[[0]*n for _ in range(n)]
for u in range(n-1,-1,-1):
    for v in range(n-1,u,-1):
        b=2
        for w in range(v+1,n):
            if O[(u,v,w)]>0: b=max(b,Fcup[v][w]+1)
        Fcup[u][v]=b
A_fail=sum(1 for v in range(n) if max([Fcup[v][w] for w in range(v+1,n)]+[1])>7-St[v][3])
Y_fail=sum(1 for v in range(1,n) if max([Ecap[u][v] for u in range(v)]+[1])>7-(6-sum(1 for a in range(4) if St[v][a]>=1)))
own={k:[i for i in range(n) if St[i][3]>=k] for k in range(1,7)}
print('real57: A_k pointwise failures',A_fail,' Y pointwise failures',Y_fail)
print('real57: longest cup inside owners of {f4>=k}:',{k:chain_in(P,O,own[k],+1) for k in own}, '(lemma: < 8-k)')
print('real57: longest cap inside owners of {f4=0}:',chain_in(P,O,[i for i in range(n) if St[i][3]==0],-1),'(lemma: <5)')
h=[]
for i,p in enumerate(P):
    while len(h)>=2 and orient(P[h[-2]],P[h[-1]],p)<=0: h.pop()
    h.append(i)
print('real57: lower hull',len(h),'vertices; states',[St[i] for i in h], ' second point state',St[1])
