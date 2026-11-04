import os
import sys, math, random, importlib.util
spec=importlib.util.spec_from_file_location('cm',os.path.join(os.path.dirname(os.path.abspath(__file__)),'chord_rules_m.py')); CM=importlib.util.module_from_spec(spec); spec.loader.exec_module(CM)
m,t,N,seed=int(sys.argv[1]),int(sys.argv[2]),int(sys.argv[3]),int(sys.argv[4]); random.seed(seed)
E,C=CM.build(m,t); odd=m%2==1; u=180.0/m
def config():
    rs=sorted([math.exp(random.uniform(-14,0)) for _ in range(t)],reverse=True); rs[0]=1.0
    th=[0.0]+[random.choice([random.uniform(1e-7,2*u-1e-7), random.uniform(1e-7,1e-3), 2*u-random.uniform(1e-7,1e-3), u+random.uniform(-1e-3,1e-3)]) for _ in range(t-1)]
    th=[x if 0<x<2*u or i==0 else random.uniform(1e-4,2*u-1e-4) for i,x in enumerate(th)]
    P=[]
    for i in range(t):
        for k in range(m):
            a=math.radians(th[i]+360.0*k/m); P.append((rs[i]*math.cos(a),rs[i]*math.sin(a)))
    return P,th
viol=0
for _ in range(N):
    P,th=config(); val={}
    for T,v in E.tvar.items():
        a,b,c=(P[x] for x in T); val[v]=((b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0]))>0
    psi=[(x % u) if odd else x for x in th]
    for (i,j),v in E.Y.items(): val[v]=psi[i]<psi[j]
    if odd:
        for i,v in E.H.items(): val[v]=th[i]<u
    for c in C:
        if not any((val[abs(l)] if l>0 else not val[abs(l)]) for l in c): viol+=1
print('m=%d t=%d clauses %d configs %d violations %d' % (m,t,len(C),N,viol))
