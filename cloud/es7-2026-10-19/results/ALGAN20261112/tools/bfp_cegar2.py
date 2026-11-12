"""BFP-CEGAR, stage 2: like bfp_cegar.py, plus 4-layer subsets; cuts use only the signs a certificate uses, mapped to
every ordered triple (3-layer) or every increasing 4-tuple (4-layer) of layers. Every added clause is appended to
added_clauses.cnf; every certificate is stored in certs2/."""
import sys, json, time, itertools, os
import numpy as np
from multiprocessing import Pool
sys.path.insert(0,'.')
R=os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..'))   # .../results
sys.path.insert(0,R+'/C7UPPER'); import gen
from cegar_gp import gp_clauses
from omtools import orbit_id_map
from bfpcert import rows_for, find_cert, check_cert
from modeltest import bfp_sym
m,K,t=4,8,14; n=m*t; E=gen.Enc(m,K,t)
ids,_=orbit_id_map(m,t)
CHI=None
def _init(chi):
    global CHI; CHI=chi
def _test(L):
    Sx=[l*4+k for l in L for k in range(4)]
    return L, bfp_sym(CHI,Sx,ids,use_pyth=False)
def _cert(L):
    Sx=[l*4+k for l in L for k in range(4)]
    cert=find_cert(rows_for(CHI,Sx,ids))
    if not isinstance(cert,list): return L,None,'extract failed %s'%cert
    ok,msg=check_cert(CHI,cert,ids)
    if not ok: return L,None,'check failed '+msg
    # signs used: every bracket of every relation in the certificate, as (frame triple, sign)
    pos={L[p]*4+k:p*4+k for p in range(len(L)) for k in range(4)}
    used={}
    for r,w in cert:
        a,b,c,d,e=r['rel']
        for x in ((a,b,c),(a,d,e),(a,b,d),(a,c,e),(a,b,e),(a,c,d)):
            fr=tuple(pos[v] for v in x); used[fr]=int(CHI[x[0],x[1],x[2]])
    return L,dict(cert=[dict(rel=r['rel'],j=r['j'],k=r['k'],w=w) for r,w in cert],used=sorted(used.items())),'ok'
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
if __name__=='__main__':
    from pysat.solvers import Cadical195
    TLIM=float(sys.argv[1]); NP=int(sys.argv[2]); T0=time.time()
    log=open('bfp_cegar2.log','a'); add=open('added_clauses.cnf','a'); os.makedirs('certs2',exist_ok=True)
    def P(*a):
        s=' '.join(map(str,a)); print(s,flush=True); log.write(s+'\n'); log.flush()
    S=Cadical195(); nb=0
    for line in open('gp_m4K8t14.work.cnf'):
        if line[0] in 'pc': continue
        cl=list(map(int,line.split()))[:-1]
        if cl: S.add_clause(cl); nb+=1
    def ADD(cl):
        S.add_clause(cl); add.write(' '.join(map(str,cl))+' 0\n')
    def cut(used,size):
        tuples=itertools.permutations(range(t),3) if size==3 else itertools.combinations(range(t),4)
        c=0
        for Lp in tuples:
            cl=[]
            for (a,b,cc),s in used:
                A=Lp[a//4]*4+a%4; B=Lp[b//4]*4+b%4; C=Lp[cc//4]*4+cc%4
                l=E.o(A,B,C); cl.append(-l if s>0 else l)
            ADD(cl); c+=1
        return c
    # re-add stage-1 patterns (full 12-point patterns) as used-sign cuts
    pt=list(itertools.combinations(range(12),3)); np1=0
    for f in sorted(os.listdir('certs')):
        d=json.load(open('certs/'+f)); cut([(tr,s) for tr,s in zip(pt,d['pattern'])],3); np1+=1
    P('stage2 start: base+GP clauses',nb,'stage-1 patterns re-added',np1)
    seen=set(); it=0; npat={3:0,4:0}
    while time.time()-T0<TLIM:
        t1=time.time(); ok=S.solve(); ts=time.time()-t1
        if not ok: P('iter',it,'UNSAT (solve %.0fs)'%ts,'patterns',npat); break
        chi=chi_of(S.get_model()); gv=gp_viol(chi)
        if gv:
            for rel in gv:
                for cl in gp_clauses(E,*rel): ADD(cl)
            P('iter',it,'solve %.0fs'%ts,'GP violations',len(gv)); it+=1; continue
        found=False
        for size in (3,4):
            with Pool(NP,initializer=_init,initargs=(chi,)) as pool:
                bad=[L for L,r in pool.imap_unordered(_test,itertools.combinations(range(t),size),chunksize=8) if r!='FEAS']
                if not bad: continue
                res=pool.map(_cert,bad)
            newp=0
            for L,d,msg in res:
                if d is None: P('  ',L,msg); continue
                key=(size,tuple(map(tuple,(tuple(x) for x in d['used']))))
                if key in seen: continue
                seen.add(key); newp+=1; npat[size]+=1
                json.dump(dict(size=size,layers=L,**d),open('certs2/s%d_%04d.json'%(size,npat[size]),'w'))
                cut([(tuple(tr),s) for tr,s in d['used']],size)
            P('iter',it,'solve %.0fs'%ts,'size',size,'bad subsets',len(bad),'new patterns',newp,'patterns',npat,'elapsed %.0fs'%(time.time()-T0))
            found=True; break
        if not found:
            P('iter',it,'model GP-consistent and BFP-clean on all 3- and 4-layer subsets -> saved')
            json.dump(sorted(x for x in S.get_model() if x>0),open('bfp4clean_model_%d.json'%it,'w')); break
        it+=1
    else:
        P('time limit; patterns',npat)
