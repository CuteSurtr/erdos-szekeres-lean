import random, sys, json
from resstate import *
def gen(rng,n):
    pts=set()
    mode=rng.randrange(3)
    while len(pts)<n:
        if mode==0:
            x=rng.randrange(-10**6,10**6); y=rng.randrange(-10**6,10**6)
        elif mode==1:  # near a parabola (cup-rich) with noise
            x=rng.randrange(-1000,1000); y=x*x+rng.randrange(-200000,200000)
        else:          # mixture of two convex arcs
            x=rng.randrange(-1000,1000); s=rng.choice([1,1,-1]); y=s*x*x//3+rng.randrange(-120000,120000)
        pts.add((x,y))
    P=sorted(pts)
    xs=[p[0] for p in P]
    if len(set(xs))<len(xs): return None
    return P
def clean(P,rng):
    while True:
        n=len(P)
        if n<3: return P
        try: O,Ecup,Ecap,Fcap=tables(P)
        except AssertionError: return None
        bad=None
        for v in range(n):
            for u in range(v):
                if Ecap[u][v]>=6 or Ecup[u][v]>=8: bad=v; break
            if bad is not None: break
        if bad is None:
            for v in range(n):
                ce=max([Ecup[u][v] for u in range(v)]+[1]); cs=max([Fcap[v][w] for w in range(v+1,n)]+[1])
                if ce>=6 and cs>=5: bad=v; break
        if bad is None: return P
        P=P[:bad]+P[bad+1:]
def lower_hull_idx(P):
    h=[]
    for i,p in enumerate(P):
        while len(h)>=2 and orient(P[h[-2]],P[h[-1]],p)<=0: h.pop()
        h.append(i)
    return h
seed=int(sys.argv[1]) if len(sys.argv)>1 else 1; trials=int(sys.argv[2]) if len(sys.argv)>2 else 300
rng=random.Random(seed)
stats=dict(sets=0,points=0,inj_fail=0,A_fail={k:0 for k in range(1,7)},A_pt_fail=0,Y_fail=0,Y_pt_fail=0,
           flat_fail=0,second_fail=0,LoCup6=0,FCap5=0,
           neg_A1_has6cup=0,neg_f4eq1_has6cup=0,max_FA2=0,max_n=0,f4ge2_sets=0,FA2_nonempty=0)
flat=set((k,k,k,k) for k in range(1,7)); second={(1,0,0,0),(1,1,0,0),(1,1,1,0),(1,1,1,1)}
t=0
while stats['sets']<trials and t<trials*20:
    t+=1
    n=rng.randrange(18,46)
    P=gen(rng,n)
    if P is None: continue
    P=clean(P,rng)
    if P is None or len(P)<6: continue
    O,Ecup,Ecap,Fcap=tables(P); n=len(P)
    assert junction_free(n,Ecup,Fcap)
    St=states(P,O,Ecup,Fcap)
    stats['sets']+=1; stats['points']+=n; stats['max_n']=max(stats['max_n'],n)
    if len(set(St))!=n: stats['inj_fail']+=1
    # A_k lemma: owners of {f4>=k} have no (8-k)-cup
    for k in range(1,7):
        own=[i for i in range(n) if St[i][3]>=k]
        if chain_in(P,O,own,+1)>=8-k: stats['A_fail'][k]+=1
    # pointwise: cups starting at v have <= 7-f4(v) points
    cupstart=[1]*n
    # longest cup starting at v: max over w>v of longest cup starting with (v,w)
    Fcup=[[0]*n for _ in range(n)]
    for u in range(n-1,-1,-1):
        for v in range(n-1,u,-1):
            b=2
            for w in range(v+1,n):
                if O[(u,v,w)]>0: b=max(b,Fcup[v][w]+1)
            Fcup[u][v]=b
    for v in range(n):
        cs=max([Fcup[v][w] for w in range(v+1,n)]+[1])
        if cs>7-St[v][3]: stats['A_pt_fail']+=1
    # Y lemma: v != first: m(v)=6-#nonzero cols; caps ending at v have <= 7-m(v) points; owners of {f4=0} no 5-cap
    for v in range(1,n):
        nz=sum(1 for a in range(4) if St[v][a]>=1); m=6-nz
        ce=max([Ecap[u][v] for u in range(v)]+[1])
        if ce>7-m: stats['Y_pt_fail']+=1
    own=[i for i in range(n) if St[i][3]==0]
    if chain_in(P,O,own,-1)>=5: stats['Y_fail']+=1
    # hull facts
    lh=lower_hull_idx(P)
    if St[0]!=(0,0,0,0): stats['flat_fail']+=1
    for i in lh[1:]:
        if St[i] not in flat: stats['flat_fail']+=1
    if St[1] not in second: stats['second_fail']+=1
    # Lemma A sanity
    Lo_own=[i for i in range(n) if St[i][0]<=4]; F_own=[i for i in range(n) if St[i][0]>=5]
    if chain_in(P,O,Lo_own,+1)>=6: stats['LoCup6']+=1
    if chain_in(P,O,F_own,-1)>=5: stats['FCap5']+=1
    # negative controls
    if chain_in(P,O,[i for i in range(n) if St[i][3]>=1],+1)>=6: stats['neg_A1_has6cup']+=1
    if chain_in(P,O,[i for i in range(n) if St[i][3]==1],+1)>=6: stats['neg_f4eq1_has6cup']+=1
    fa2=sum(1 for i in range(n) if St[i][0]>=5 and St[i][3]>=2)
    stats['max_FA2']=max(stats['max_FA2'],fa2); stats['FA2_nonempty']+= (fa2>0)
    stats['f4ge2_sets']+= any(St[i][3]>=2 for i in range(n))
print(json.dumps(stats))
