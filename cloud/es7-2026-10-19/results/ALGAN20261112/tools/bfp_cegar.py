"""BFP-CEGAR at (m,K,t) = (4,8,14): solve encoder A + GP clauses + symmetric-BFP cuts; per model add violated GP
relations and, for every 3-layer subset without a feasible log-LP, an exact BFP certificate and the cut forbidding that
12-point pattern on every ordered triple of layers. Research run; every cut is stored with its certificate."""
import sys, json, time, itertools, os
import numpy as np
sys.path.insert(0,'.')
R=os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..'))   # .../results
sys.path.insert(0,R+'/C7UPPER'); import gen
from cegar_gp import gp_clauses
from omtools import orbit_id_map
from bfpcert import rows_for, find_cert, check_cert
from modeltest import bfp_sym
from pysat.solvers import Cadical195
m,K,t=4,8,14; n=m*t; E=gen.Enc(m,K,t)
TLIM=float(sys.argv[1]) if len(sys.argv)>1 else 3*3600
T0=time.time(); log=open('bfp_cegar.log','a')
def P(*a):
    s=' '.join(map(str,a)); print(s,flush=True); log.write(s+'\n'); log.flush()
S=Cadical195()
nb=0
with open('gp_m4K8t14.work.cnf') as f:
    for line in f:
        if line[0] in 'pc': continue
        cl=list(map(int,line.split()))[:-1]
        if cl: S.add_clause(cl); nb+=1
P('loaded clauses',nb,'%.0fs'%(time.time()-T0))
ids,_=orbit_id_map(m,t)
# triples of a 3-layer pattern in canonical positions: point (pos,k) -> pos*4+k in a 12-point frame
pat_triples=list(itertools.combinations(range(12),3))
def chi_of(model):
    val=set(x for x in model if x>0); chi=np.zeros((n,n,n),dtype=np.int8)
    for a,b,c in itertools.combinations(range(n),3):
        l=E.o(a,b,c); s=1 if ((l>0 and l in val) or (l<0 and -l not in val)) else -1
        for (i,j,k),sg in (((a,b,c),1),((b,c,a),1),((c,a,b),1),((b,a,c),-1),((a,c,b),-1),((c,b,a),-1)): chi[i,j,k]=s*sg
    return chi
def gp_viol(chi):
    out=[]
    for a in range(n):
        oth=np.array([x for x in range(n) if x!=a]); Q=np.array(list(itertools.combinations(range(n-1),4)),dtype=np.int32)
        b,c,d,e=(oth[Q[:,k]] for k in range(4)); M=chi[a]
        s1=M[b,c]*M[d,e]; s2=-M[b,d]*M[c,e]; s3=M[b,e]*M[c,d]
        for k in np.nonzero((s1==s2)&(s2==s3))[0]: out.append((a,int(b[k]),int(c[k]),int(d[k]),int(e[k])))
    return out
patterns=set(); cuts=0; it=0
os.makedirs('certs',exist_ok=True)
while time.time()-T0<TLIM:
    t1=time.time(); ok=S.solve(); ts=time.time()-t1
    if not ok:
        P('iter',it,'UNSAT after %.0fs solve'%ts,'patterns',len(patterns),'cut clauses',cuts); break
    chi=chi_of(S.get_model())
    gv=gp_viol(chi)
    if gv:
        for rel in gv:
            for cl in gp_clauses(E,*rel): S.add_clause(cl)
        P('iter',it,'solve %.0fs'%ts,'GP violations',len(gv),'-> added'); it+=1; continue
    bad=[]
    for L in itertools.combinations(range(t),3):
        Sx=[l*4+k for l in L for k in range(4)]
        if bfp_sym(chi,Sx,ids,use_pyth=False)!='FEAS': bad.append(L)
    if not bad:
        P('iter',it,'solve %.0fs'%ts,'model is GP-consistent and passes BFP on all 3-layer subsets -> saved')
        json.dump(sorted(x for x in S.get_model() if x>0),open('bfp3clean_model_%d.json'%it,'w')); break
    newp=0
    for L in bad:
        Sx=[l*4+k for l in L for k in range(4)]
        cert=find_cert(rows_for(chi,Sx,ids))
        if not isinstance(cert,list): P('  cert extraction failed for',L,cert); continue
        okc,msg=check_cert(chi,cert,ids)
        if not okc: P('  cert check failed for',L,msg); continue
        # pattern: signs of all triples of the 12 points in canonical positions
        pos={L[p]*4+k:p*4+k for p in range(3) for k in range(4)}
        inv={v:k for k,v in pos.items()}
        pat=tuple(int(chi[inv[a],inv[b],inv[c]]) for a,b,c in pat_triples)
        if pat in patterns: continue
        patterns.add(pat); newp+=1
        json.dump(dict(layers=L,pattern=pat,cert=[dict(rel=r['rel'],j=r['j'],k=r['k'],w=w) for r,w in cert]),open('certs/p%04d.json'%len(patterns),'w'))
        # cut on every ordered triple of distinct layers
        for Lp in itertools.permutations(range(t),3):
            cl=[]
            for (a,b,c),s in zip(pat_triples,pat):
                A=Lp[a//4]*4+a%4; B=Lp[b//4]*4+b%4; C=Lp[c//4]*4+c%4
                l=E.o(A,B,C)   # orient(A,B,C)=+ iff l true
                cl.append(-l if s>0 else l)
            S.add_clause(cl); cuts+=1
    P('iter',it,'solve %.0fs'%ts,'BFP-infeasible 3-layer subsets',len(bad),'new patterns',newp,'total patterns',len(patterns),'elapsed %.0fs'%(time.time()-T0))
    it+=1
else:
    P('time limit reached; patterns',len(patterns))
