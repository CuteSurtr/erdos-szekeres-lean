import os
import sys, importlib.util, mpmath as mp
mp.mp.dps=80
spec=importlib.util.spec_from_file_location('cm',os.path.join(os.path.dirname(os.path.abspath(__file__)),'chord_rules_m.py')); CM=importlib.util.module_from_spec(spec); spec.loader.exec_module(CM)
path,m=sys.argv[1],int(sys.argv[2])
Z=[mp.exp(2j*mp.pi*k/m) for k in range(m)]
pts=[]
for line in open(path):
    line=line.split('#')[0].strip()
    if not line: continue
    w=list(map(int,line.split())); z=sum(c*Z[k] for k,c in enumerate(w))
    if abs(z)>0: pts.append(z)          # drop the centre
rad=sorted(set([mp.nstr(abs(z),40) for z in pts]),key=lambda s:-mp.mpf(s))
layers=[[z for z in pts if mp.nstr(abs(z),40)==r] for r in rad]; t=len(layers)
assert all(len(L)==m for L in layers), [len(L) for L in layers]
# rotate so that one vertex of layer 0 has angle 0
rot=mp.exp(-1j*mp.arg(layers[0][0])); layers=[[z*rot for z in L] for L in layers]
U=2*mp.pi/m; P={}; th=[]
for i,L in enumerate(layers):
    ang=[(mp.arg(z))%(2*mp.pi) for z in L]
    for z,a in zip(L,ang):
        k=int(mp.floor(a/U+mp.mpf('1e-60'))) % m
        P[m*i+k]=z
    th.append(min(a for a in ang))
assert len(P)==m*t
E,C=CM.build(m,t); odd=m%2==1; u=mp.pi/m
val={}
for T,v in E.tvar.items():
    a,b,c=(P[x] for x in T); d=mp.im(mp.conj(b-a)*(c-a)); assert abs(d)>mp.mpf(10)**-40; val[v]=d>0
psi=[(x % u) if odd else x for x in th]
for (i,j),v in E.Y.items(): val[v]=psi[i]<psi[j]
if odd:
    for i,v in E.H.items(): val[v]=th[i]<u
bad=sum(1 for c in C if not any((val[abs(l)] if l>0 else not val[abs(l)]) for l in c))
print(path.split('/')[-1], 'm=%d t=%d chord clauses %d violated %d' % (m,t,len(C),bad))
