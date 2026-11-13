import sys, gzip, json, itertools
import numpy as np
sys.path.insert(0, '/home/jay/research/data/theory310-20261113')
from fan import load
S, C, A, B = load('res')
# model.py's triple_table, reimplemented verbatim (with and without the (1,6) cell)
def cellsf(s): return {(i+1,y) for i,h in enumerate(s) for y in range(1,h+1)}
def boxes(states, drop16):
    n=len(states); sets=[cellsf(s) for s in states]
    ne=np.zeros((n,n),bool); mn=np.zeros((2,n,n),np.int16); mx=np.zeros((2,n,n),np.int16)
    for a in range(n):
        for b in range(n):
            d=sets[b]-sets[a]
            if drop16: d=d-{(1,6)}
            if d:
                ne[a,b]=True
                mn[0,a,b]=min(z[0] for z in d); mx[0,a,b]=max(z[0] for z in d)
                mn[1,a,b]=min(z[1] for z in d); mx[1,a,b]=max(z[1] for z in d)
    return ne,mn,mx
def tt(ne,mn,mx):
    n=ne.shape[0]; idx=np.arange(n,dtype=np.int16)
    Aa,Bb,Cc=np.meshgrid(idx,idx,idx,indexing='ij'); T=(Aa!=Bb)&(Bb!=Cc)&(Aa!=Cc); g=(Aa,Bb,Cc)
    for perm in itertools.permutations(range(3)):
        odd=sum(perm[i]>perm[j] for i in range(3) for j in range(i+1,3))%2; coord=1 if odd else 0
        p,q,r=(g[perm[k]] for k in range(3))
        present=ne[p,q]&ne[q,r]&ne[p,r]; forced=mx[coord][q,r]<=mn[coord][p,q]
        T&=(~present)|forced
    return T
Tb=np.load('T_res_base.npy')
for drop in [False, True]:
    T=tt(*boxes(S,drop))
    print('model.py triple_table drop16=',drop,'sum',int(T.sum()),'equal to my base:',bool((T==Tb).all()), 'mine-only',int((Tb&~T).sum()),'theirs-only',int((T&~Tb).sum()))
T=tt(*boxes(S,True))
diff=np.argwhere(Tb&~T)
print(diff[:5])
a,b,c=diff[0]
from fan import tables, domains
cupP,capP,ok=tables(S,A,B,'res',fan=False)
dom=domains(S,A,B,'res')
ne,mn,mx=boxes(S,True)
for perm in itertools.permutations(range(3)):
    g=(a,b,c); p,q,r=(g[perm[k]] for k in range(3))
    odd=sum(perm[i]>perm[j] for i in range(3) for j in range(i+1,3))%2
    print(perm,'odd',odd,'pqr',p,q,r,'present',ne[p,q]&ne[q,r]&ne[p,r],'theirs forced', mx[1 if odd else 0][q,r]<=mn[1 if odd else 0][p,q],
          'my cupP',cupP[p,q,r],'capP',capP[p,q,r], 'D1',dom[p][q][:6],'D2',dom[q][r][:6])
