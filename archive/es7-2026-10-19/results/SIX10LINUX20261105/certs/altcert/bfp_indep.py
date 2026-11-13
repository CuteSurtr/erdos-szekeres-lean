#!/usr/bin/env python3
"""Coordinator's independent exact checker for biquadratic-final-polynomial certificates (altcert format).
For each comparison (quintuple (a,b,c,d,e), minority k, other j, weight w>0):
  GP identity T0 + T1 + T2 = 0, T0=[abc][ade], T1=-[abd][ace], T2=[abe][acd] (anchor a), all brackets nonzero.
  The model's bracket signs must make T_k the unique minority-sign term, so |T_k| = |T_i|+|T_j| > |T_j|.
  Row: log|T_k| - log|T_j| > 0, with log|[xyz]| one unknown per rotation orbit (|det| is rotation invariant).
Checks: sum_w rows == 0 identically (exact integers) -> contradiction; clause = negation of every bracket literal
of every used identity (as in the model), so the cut is sound for any assignment with those signs."""
import sys, json, importlib.util, glob, os
from collections import Counter
import pathlib
R=os.environ.get('ES_RESULTS',str(pathlib.Path(__file__).resolve().parents[3]))
s=importlib.util.spec_from_file_location('g', R+'/C7UPPER/gen.py'); G=importlib.util.module_from_spec(s); s.loader.exec_module(G)
E=G.Enc(6,8,10)
def check(cert, model):
    tv=set(model); acc=Counter(); need=set()
    sgn=lambda x,y,z: (1 if ((abs(E.o(x,y,z)) in tv)==(E.o(x,y,z)>0)) else -1)
    for c in cert['comparisons']:
        a,b,cc,d,e=c['quintuple']; k=c['minority']; j=c['other']; w=c['weight']
        assert len({a,b,cc,d,e})==5 and k in (0,1,2) and j in (0,1,2) and j!=k and type(w) is int and w>0
        br=[(a,b,cc),(a,d,e),(a,b,d),(a,cc,e),(a,b,e),(a,cc,d)]
        for t in br: need.add(E.o(*t) if sgn(*t)>0 else -E.o(*t))     # the literal true in the model
        T=[sgn(*br[0])*sgn(*br[1]), -sgn(*br[2])*sgn(*br[3]), sgn(*br[4])*sgn(*br[5])]
        others=[q for q in range(3) if q!=k]
        if not (T[others[0]]==T[others[1]]!=T[k]): return 'minority wrong'
        P=[(br[0],br[1]),(br[2],br[3]),(br[4],br[5])]
        for t in P[k]: acc[abs(E.o(*t))]+=w
        for t in P[j]: acc[abs(E.o(*t))]-=w
    if any(v for v in acc.values()): return 'rows do not cancel'
    clause=set(cert['clause'])
    if clause!={-l for l in need}: return 'clause != negated used literals (%d vs %d)' % (len(clause),len(need))
    if any(((abs(l) in tv)==(l>0)) for l in clause): return 'clause satisfied by model'
    return 'ok'
if __name__=='__main__':
    W=os.environ.get('SIX10_WORK','<six10-work-dir>'); res=Counter(); bad=[]
    for f in sorted(glob.glob(sys.argv[1]+'/*.json')):
        cert=json.load(open(f)); model=json.load(open(W+'/models/%s.json'%cert['model']))
        r=check(cert,model); res[r]+=1
        if r!='ok': bad.append((os.path.basename(f),r))
    print(dict(res)); [print(b) for b in bad[:10]]
    # corruption tests
    import random; random.seed(1); rej=0; n=0
    for f in random.sample(sorted(glob.glob(sys.argv[1]+'/*.json')),20):
        cert=json.load(open(f)); model=json.load(open(W+'/models/%s.json'%cert['model']))
        c2=json.loads(json.dumps(cert)); x=random.choice(c2['comparisons']); x['weight']+=1
        n+=1; rej+=(check(c2,model)!='ok')
        c3=json.loads(json.dumps(cert)); y=random.choice(c3['comparisons']); y['other']=3-y['other']-y['minority']
        n+=1; rej+=(check(c3,model)!='ok')
    print('corruptions rejected', rej, 'of', n)
