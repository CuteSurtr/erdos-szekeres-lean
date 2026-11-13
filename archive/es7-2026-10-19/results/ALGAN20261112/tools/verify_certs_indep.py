"""Independent check (standard library only) of the stage-2 BFP certificates (certs2/*.json).
For each certificate: map every relation into the 4*size-point frame, take the bracket signs ONLY from the stored
'used' list (exactly the literals of the cut clause), recompute the minority term of each 3-term GP relation, and check
that the weighted multisets of rotation orbits (frame rotation (pos,k)->(pos,k+1)) on the greater and smaller sides
coincide. A pass means: the cut's sign conditions alone force prod|greater| > prod|smaller| = prod|greater|."""
import json, sys, os, itertools
from collections import Counter
def perm_sign(t):
    s=1; t=list(t)
    for i in range(len(t)):
        for j in range(i+1,len(t)):
            if t[i]>t[j]: s=-s
    return s
def check(d):
    size=d['size']; L=d['layers']; pos={L[p]*4+k:p*4+k for p in range(size) for k in range(4)}
    sign={}
    for tr,s in d['used']:
        tr=tuple(tr); key=tuple(sorted(tr)); v=s*perm_sign(tr)           # sign of the sorted triple
        if key in sign and sign[key]!=v: return False                    # inconsistent duplicate literal
        sign[key]=v
    def chi(a,b,c):
        key=tuple(sorted((a,b,c)))
        if key not in sign: raise KeyError(key)
        return sign[key]*perm_sign((a,b,c))
    rot=lambda p: (p//4)*4+(p%4+1)%4
    def orb(tr):
        best=None; o=tuple(sorted(tr))
        for _ in range(4):
            o=tuple(sorted(rot(x) for x in o)); best=o if best is None or o<best else best
        return best
    G=Counter(); Lc=Counter()
    for r in d['cert']:
        a,b,c,dd,e=(pos[x] for x in r['rel']); w=r['w']
        T=[((a,b,c),(a,dd,e)),((a,b,dd),(a,c,e)),((a,b,e),(a,c,dd))]
        s=[chi(a,b,c)*chi(a,dd,e), -chi(a,b,dd)*chi(a,c,e), chi(a,b,e)*chi(a,c,dd)]
        mino=[k for k in range(3) if s.count(s[k])==1]
        if mino!=[r['j']] or r['k']==r['j'] or w<=0: return False
        for x in T[r['j']]: G[orb(x)]+=w
        for x in T[r['k']]: Lc[orb(x)]+=w
    return G==Lc and sum(G.values())>0
D=sys.argv[1]; ok=bad=0
for f in sorted(os.listdir(D)):
    d=json.load(open(os.path.join(D,f)))
    try: r=check(d)
    except KeyError as e: r=False
    if r: ok+=1
    else: bad+=1; print('FAIL',f)
print('certificates',ok+bad,'pass',ok,'fail',bad)
