"""Rebuild the 4x4 model and check every used row without importing research code.
Certificate verdicts here are inventory checks, not independent LRAT replays.
"""
import collections, functools, hashlib, itertools as it, json, pathlib
D=pathlib.Path('/home/jay/research/data/n66-20261113/p2/b12/it1')
S=sorted((p for p in it.product(range(5),repeat=4) if list(p)==sorted(p,reverse=True)),key=lambda p:(sum(p),p))
C=[{(a+1,b) for a,h in enumerate(p) for b in range(1,h+1)} for p in S]
assert len(S)==70
tau=[C.index({(b,a) for a,b in c}) for c in C]
plain=[[C[t]-C[s] for t in range(70)] for s in range(70)]
ref=[[{(a,b) for a,b in plain[s][t] if a<=sum(h>0 for h in S[s])+1 and b<=S[s][0]+1} for t in range(70)] for s in range(70)]
@functools.lru_cache(None)
def positive(a,b,c):
    for p in it.permutations(range(3)):
        x,y,z=[(a,b,c)[k] for k in p]
        if not plain[x][y] or not plain[y][z] or not plain[x][z]: continue
        axis=sum(p[i]>p[j] for i in range(3) for j in range(i+1,3))%2
        if max(v[axis] for v in plain[y][z])>min(v[axis] for v in plain[x][y]): return False
    return True
def valid(t,s):
    typ,*v=t
    if typ=='positive': return positive(*(s[i] for i in v))
    if typ=='empty': return not ref[s[v[0]]][s[v[1]]]
    if typ=='domain': return tuple(v[2:]) not in ref[s[v[0]]][s[v[1]]]
    raise ValueError(t)
def run():
    J=json.loads((D/'tcert/justification.json').read_text()); rows=json.loads((D/'used_rows.json').read_text())
    assert hashlib.sha256((D/'used_rows.json').read_bytes()).hexdigest()==J['rows_sha256']
    T={x['id']:x for l in (D/'tcert/template_certs.jsonl').open() if (x:=json.loads(l))}
    K={tuple(x['support']):x for l in (D/'tcert/core_certs.jsonl').open() if (x:=json.loads(l))}
    usedT=set(); usedK=set()
    def verify(j):
        s=j['support']; assert s==sorted(set(s)); assert all(0<=i<70 for i in s)
        if j['kind']=='mirror':
            o=j['of']; assert sorted(tau[i] for i in o['support'])==s and j['demand']==o['demand']; verify(o)
        elif j['kind']=='cycle':
            order=j['order']; assert sorted(order)==s and j['demand']==len(s)-7
            assert all(positive(*q) for q in it.combinations(order,3))
        elif j['kind']=='core':
            assert j['demand']==1 and K[tuple(s)]['verdict']=='s VERIFIED UNSAT'; usedK.add(tuple(s))
        elif j['kind']=='transported':
            t=T[j['template']]; sig=j['sigma']; assert j['demand']==1
            assert len(sig)==len(t['core']) and sorted(sig)==s
            assert t['verdict']=='s VERIFIED UNSAT'
            assert hashlib.sha256(json.dumps([t['core'],t['tests'],t.get('octs')]).encode()).hexdigest()[:16]==j['template']
            assert all(valid(test,sig) and valid(test,t['core']) for test in t['tests'])
            usedT.add(j['template'])
        else: raise ValueError(j['kind'])
    assert collections.Counter((tuple(s),d) for s,d in rows)==collections.Counter((tuple(j['support']),j['demand']) for j in J['justifications'])
    for j in J['justifications']: verify(j)
    print(json.dumps(dict(result='ROW JUSTIFICATIONS PASS; underlying certificate replays separate',rows=len(rows),kinds=dict(collections.Counter(j['kind'] for j in J['justifications'])),templates=len(usedT),cores=len(usedK))),flush=True)
if __name__=='__main__': run()
