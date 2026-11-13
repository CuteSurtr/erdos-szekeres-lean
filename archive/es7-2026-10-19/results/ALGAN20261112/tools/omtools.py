"""Chirotope tests for m-fold layered configurations (research scratch; positive-control first).
Points indexed p = layer*m + k  (point (layer,k) = zeta^k * w_layer).
chi: numpy int8 array n x n x n, alternating, entries +-1 (0 on diagonal)."""
import numpy as np, itertools, math

def chi_from_gauss(pts):
    """exact chirotope from integer (a,b) coordinates (m=4 Gaussian lattice)."""
    P=np.array(pts,dtype=object); n=len(pts)
    chi=np.zeros((n,n,n),dtype=np.int8)
    for a,b,c in itertools.combinations(range(n),3):
        (xa,ya),(xb,yb),(xc,yc)=pts[a],pts[b],pts[c]
        d=(xb-xa)*(yc-ya)-(yb-ya)*(xc-xa)
        s=1 if d>0 else (-1 if d<0 else 0)
        assert s!=0
        for (i,j,k),sg in (((a,b,c),1),((b,c,a),1),((c,a,b),1),((b,a,c),-1),((a,c,b),-1),((c,b,a),-1)):
            chi[i,j,k]=s*sg
    return chi

def load_c4(f):
    pts=[]
    for l in open(f):
        if l.startswith('#') or not l.strip(): continue
        w=list(map(int,l.split())); pts.append((w[0]-w[2],w[1]-w[3]))
    return pts

def gp3_violations(chi, idx=None, maxreport=5):
    """3-term Grassmann-Pluecker sign condition: for each a and b<c<d<e (others),
    {chi(abc)chi(ade), -chi(abd)chi(ace), chi(abe)chi(acd)} must not be all equal."""
    n=chi.shape[0]; idx=list(range(n)) if idx is None else list(idx)
    bad=0; rep=[]
    for a in idx:
        oth=np.array([x for x in idx if x!=a])
        Q=np.array(list(itertools.combinations(range(len(oth)),4)),dtype=np.int32)
        if len(Q)==0: continue
        b,c,d,e=(oth[Q[:,k]] for k in range(4))
        M=chi[a]
        s1=M[b,c]*M[d,e]; s2=-M[b,d]*M[c,e]; s3=M[b,e]*M[c,d]
        v=(s1==s2)&(s2==s3)
        nb=int(v.sum()); bad+=nb
        if nb and len(rep)<maxreport:
            k=int(np.argmax(v)); rep.append((a,int(b[k]),int(c[k]),int(d[k]),int(e[k])))
    return bad, rep

def arc_violations(chi, m, t):
    """for every ordered pair (p,q) and layer l, the set {k: chi(p,q,(l,k))=+} (over k with (l,k) not in {p,q})
    must be a cyclic interval. For p,q on layer l itself, skip."""
    bad=0; rep=[]
    n=m*t
    for p in range(n):
        for q in range(n):
            if p==q: continue
            for l in range(t):
                if p//m==l or q//m==l: continue
                s=[int(chi[p,q,l*m+k]) for k in range(m)]
                ch=sum(1 for k in range(m) if s[k]!=s[(k+1)%m])
                if ch>2:
                    bad+=1
                    if len(rep)<5: rep.append((p,q,l,s))
    return bad, rep

def orbit_id_map(m, t):
    """canonical id of unordered triple orbits under the rotation p=(l,k)->(l,k+1)."""
    n=m*t; rot=lambda p: (p//m)*m+((p%m)+1)%m
    ids={}; nxt=0
    for tr in itertools.combinations(range(n),3):
        key=tuple(sorted(tr))
        if key in ids: continue
        o=key; orb=[]
        for r in range(m):
            orb.append(tuple(sorted(o))); o=tuple(rot(x) for x in o)
        for x in orb: ids[x]=nxt
        nxt+=1
    return ids, nxt

def bfp_lp(chi, S, ids, margin=1.0):
    """Biquadratic final polynomial test (Bokowski-Richter) on point subset S, with rotation-orbit variables.
    Returns (feasible:bool, info)."""
    from scipy.optimize import linprog
    from scipy.sparse import coo_matrix
    S=sorted(S); rows=[]; cols=[]; vals=[]; r=0
    used={}
    def var(tr):
        o=ids[tuple(sorted(tr))]
        if o not in used: used[o]=len(used)
        return used[o]
    seen=set()
    for a in S:
        oth=[x for x in S if x!=a]
        for b,c,d,e in itertools.combinations(oth,4):
            T=[((a,b,c),(a,d,e)),((a,b,d),(a,c,e)),((a,b,e),(a,c,d))]
            s=[chi[a,b,c]*chi[a,d,e], -chi[a,b,d]*chi[a,c,e], chi[a,b,e]*chi[a,c,d]]
            if s[0]==s[1]==s[2]: return False, ('GP3 sign violation',(a,b,c,d,e))
            j=[k for k in range(3) if s[k]!=s[(k+1)%3] and s[k]!=s[(k+2)%3]][0]
            Tj=[var(x) for x in T[j]]
            for k in range(3):
                if k==j: continue
                Tk=[var(x) for x in T[k]]
                key=(tuple(sorted(Tj)),tuple(sorted(Tk)))
                if key in seen: continue
                seen.add(key)
                # constraint: L_k - L_j <= -margin
                coef={}
                for v in Tk: coef[v]=coef.get(v,0)+1
                for v in Tj: coef[v]=coef.get(v,0)-1
                coef={v:c for v,c in coef.items() if c}
                if not coef: return False, ('trivial contradiction', (a,b,c,d,e))
                for v,c in coef.items(): rows.append(r); cols.append(v); vals.append(c)
                r+=1
    nv=len(used)
    A=coo_matrix((vals,(rows,cols)),shape=(r,nv)).tocsr()
    res=linprog(np.zeros(nv),A_ub=A,b_ub=-margin*np.ones(r),bounds=[(None,None)]*nv,method='highs')
    return res.status==0, dict(status=res.status,msg=res.message,nvars=nv,ncons=r)
