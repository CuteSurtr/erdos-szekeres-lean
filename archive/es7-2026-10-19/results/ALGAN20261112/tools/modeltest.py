"""Tests on an abstract 4-fold model (encoder A variables): GP3, arcs, BFP on layer subsets, BFP + symmetric 'Pythagorean' comparisons."""
import sys, json, itertools, time
import numpy as np
import os; sys.path.insert(0,os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..','C7UPPER'))); sys.path.insert(0,'.')
import gen
from omtools import *
m,K,t=4,8,14
def chi_from_model(path):
    val=set(json.load(open(path))); E=gen.Enc(m,K,t); n=m*t
    chi=np.zeros((n,n,n),dtype=np.int8)
    for a,b,c in itertools.combinations(range(n),3):
        l=E.o(a,b,c); s=1 if ((l>0 and l in val) or (l<0 and -l not in val)) else -1
        for (i,j,k),sg in (((a,b,c),1),((b,c,a),1),((c,a,b),1),((b,a,c),-1),((a,c,b),-1),((c,b,a),-1)): chi[i,j,k]=s*sg
    return chi
def pyth_rows(S, var):
    """m=4: for p,s in S (p != s, s not in {p,-p}): 2 x[p,-p,s] < x[p,ip,-p] + x[s,is,-s]  (and with is)."""
    rows=[]
    R=lambda p,k: (p//4)*4+((p%4)+k)%4
    for p in S:
        for s in S:
            if s//4==p//4: continue
            for s2 in (s,R(s,1)):
                A=var((p,R(p,2),s2)); B=var((p,R(p,1),R(p,2))); C=var((s,R(s,1),R(s,2)))
                rows.append({A:2,B:-1,C:-1} if True else None)
    return rows
def bfp_sym(chi,S,ids,use_pyth=True,margin=1.0):
    from scipy.optimize import linprog
    from scipy.sparse import coo_matrix
    S=sorted(S); used={}
    def var(tr):
        o=ids[tuple(sorted(tr))]
        if o not in used: used[o]=len(used)
        return used[o]
    R=[]; seen=set()
    for a in S:
        oth=[x for x in S if x!=a]
        for b,c,d,e in itertools.combinations(oth,4):
            T=[((a,b,c),(a,d,e)),((a,b,d),(a,c,e)),((a,b,e),(a,c,d))]
            s=[chi[a,b,c]*chi[a,d,e], -chi[a,b,d]*chi[a,c,e], chi[a,b,e]*chi[a,c,d]]
            if s[0]==s[1]==s[2]: return 'GPVIOL'
            j=[k for k in range(3) if s[k]!=s[(k+1)%3] and s[k]!=s[(k+2)%3]][0]
            Tj=[var(x) for x in T[j]]
            for k in range(3):
                if k==j: continue
                coef={}
                for v in (var(x) for x in T[k]): coef[v]=coef.get(v,0)+1
                for v in Tj: coef[v]=coef.get(v,0)-1
                coef={v:c for v,c in coef.items() if c}
                key=tuple(sorted(coef.items()))
                if not coef: return 'TRIVIAL'
                if key not in seen: seen.add(key); R.append(coef)
    if use_pyth:
        for coef in pyth_rows(S,var):
            coef={v:c for v,c in coef.items() if c}
            # merge duplicates
            key=tuple(sorted(coef.items()))
            if key not in seen: seen.add(key); R.append(coef)
    rows=[];cols=[];vals=[]
    for r,coef in enumerate(R):
        for v,c in coef.items(): rows.append(r);cols.append(v);vals.append(c)
    A=coo_matrix((vals,(rows,cols)),shape=(len(R),len(used))).tocsr()
    res=linprog(np.zeros(len(used)),A_ub=A,b_ub=-margin*np.ones(len(R)),bounds=[(None,None)]*len(used),method='highs')
    return 'FEAS' if res.status==0 else ('INFEAS' if res.status==2 else 'ST%d'%res.status)
if __name__=='__main__':
    src=sys.argv[1]; size=int(sys.argv[2])
    if src.endswith('.pts'):
        chi=chi_from_gauss(load_c4(src)); tt=len(chi)//4
    else:
        chi=chi_from_model(src); tt=t
    ids,no=orbit_id_map(4,tt)
    if size==0:
        print('GP3',gp3_violations(chi)[0],'arc',arc_violations(chi,4,tt)[0]); sys.exit()
    cnt={}
    t0=time.time()
    for L in itertools.combinations(range(tt),size):
        S=[l*4+k for l in L for k in range(4)]
        r0=bfp_sym(chi,S,ids,use_pyth=False)
        r1=bfp_sym(chi,S,ids,use_pyth=True) if r0=='FEAS' else r0
        cnt[(r0,r1)]=cnt.get((r0,r1),0)+1
        if r0!='FEAS' or r1!='FEAS': print('  layers',L,'plainBFP',r0,'BFP+pyth',r1,flush=True)
    print('size',size,'summary',cnt,'%.0fs'%(time.time()-t0))
