import os
import importlib.util, math, random, collections, sys
spec=importlib.util.spec_from_file_location('cr',os.path.join(os.path.dirname(os.path.abspath(__file__)),'chord_rules.py')); C=importlib.util.module_from_spec(spec); _a=sys.argv; sys.argv=['x']; spec.loader.exec_module(C); sys.argv=_a
E=C.E
def config():
    rs=sorted([math.exp(random.uniform(-16,0)) for _ in range(10)], reverse=True); rs[0]=1.0
    th=[0.0]+[random.choice([random.uniform(1e-6,60-1e-6), random.uniform(1e-6,1e-3), 60-random.uniform(1e-6,1e-3)]) for _ in range(9)]
    P=[]
    for i in range(10):
        for k in range(6):
            a=math.radians(th[i]+60*k); P.append((rs[i]*math.cos(a), rs[i]*math.sin(a)))
    return P,th
def truth(P,th):
    val={}
    for T,v in E.tvar.items():
        a,b,c=(P[x] for x in T); d=(b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0]); val[v]=d>0
    for (i,j),v in E.Y.items(): val[v]=th[i]<th[j]
    return val
random.seed(int(sys.argv[2]) if len(sys.argv)>2 else 0); R=C.rules(); bad=collections.Counter(); ex={}
for _ in range(int(sys.argv[1]) if len(sys.argv)>1 else 60):
    P,th=config(); val=truth(P,th)
    lv=lambda l:(val[abs(l)] if l>0 else not val[abs(l)])
    for idx,(lit,cond) in enumerate(R):
        if cond in (None,True) or (cond is not False and lv(cond)):
            if not lv(lit): bad[idx]+=1; ex[idx]=(lit,cond)
print('rules', len(R), 'violated rules', len(bad))
for idx,c in list(bad.items())[:5]: print(idx, c, ex[idx])
