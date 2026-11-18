"""Independent piecewise wrapper; no finder or record verifier imported."""
import collections, gzip, hashlib, json, pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT / 'scripts'))
from omission_tree import check_tree
R = ROOT / 'cloud/es7-2026-10-19/results'
D = pathlib.Path('/home/jay/research/data/lo33-20261113/bb_64_57')
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
src = ROOT / 'experiments/omission-residual32-rank-global-2026-10-10/source-2650.json.gz'
raw = gzip.decompress(src.read_bytes())
assert hashlib.sha256(raw).hexdigest() == 'e800d5f8a6c5cc45c73ddcc1e57488f2ca8f2ffb704a1515ff7444d589c682f6'
cat = json.loads(raw)
rows = [(r['support'], r['rhs']) for r in cat['constraints']]
assert len(rows) == 2650 and len(cat['states']) == 154
F = [i for i,s in enumerate(cat['states']) if s[0] >= 5]
Lo = [i for i,s in enumerate(cat['states']) if s[0] <= 4]
assert len(F)==84 and len(Lo)==70
extra = json.loads((D/'extra_v1.json').read_text())
certpath = R/'LO33N20261113/data/certified.jsonl'
cert = {tuple(sorted(x['support'])) for l in certpath.open() if (x:=json.loads(l))['verdict']=='s VERIFIED UNSAT'}
caps=[]
for r in extra:
    s=sorted(r['support'])
    if s==F or s==Lo: caps.append(('F' if s==F else 'Lo',r['rhs']))
    else: assert r['rhs']==1 and tuple(s) in cert
    rows.append((s,r['rhs']))
assert sorted(caps)==[('F',20),('Lo',13)]
m=json.loads((D/'master.json').read_text()); assert m['budget']==33
paths={}; seen=set(); stack=[(m['root'],[(0,0)])]
while stack:
    k,path=stack.pop(); assert k not in seen; seen.add(k); nd=m['nodes'][k]
    if nd['type']=='branch':
        assert nd['vertex'] not in [v for v,b in path]
        stack.extend((nd[key],path+[(nd['vertex'],b)]) for key,b in [('zero',0),('one',1)])
    elif nd['type']=='context':
        c=nd['context']; assert c not in paths; paths[c]=path
assert len(seen)==len(m['nodes'])
assert set(paths)==set(range(len(paths)))
assert {p.name for p in D.glob('ctx-*.json.gz')}=={f'ctx-{c}.json.gz' for c in paths}
def wrapped(nodes,root,path,master=False):
    L=len(path); out=[]
    for j,(v,b) in enumerate(path):
        nxt=j+1 if j+1<L else L+root; pend=L+len(nodes)+j
        out.append(dict(type='branch',vertex=v,zero=nxt if b==0 else pend,one=nxt if b==1 else pend))
    for nd in nodes:
        nd=dict(nd)
        if nd['type']=='branch': nd['zero']+=L; nd['one']+=L
        elif master and nd['type']=='context': nd={'type':'pending'}
        else: assert nd['type'] in ('weighted','over_budget')
        out.append(nd)
    out.extend({'type':'pending'} for _ in path)
    return check_tree(154,rows,33,out,0,allow_pending=True)
res=wrapped(m['nodes'],m['root'],[(0,0)],True)
assert res['pending']==len(paths)+1
nodes=len(m['nodes'])+2-len(paths); leaves=res['leaves']-len(paths); minimum=res['minimum_margin']; hashes=[]
for c,path in sorted(paths.items()):
    p=D/f'ctx-{c}.json.gz'; hashes.append([p.name,sha(p)])
    x=json.loads(gzip.decompress(p.read_bytes())); assert x['context']==c
    assert sorted(x['missing'])==sorted(v for v,b in path if b)
    assert sorted(x['occupied'])==sorted(v for v,b in path if not b)
    r=wrapped(x['nodes'],x['root'],path); assert r['pending']==len(path)
    nodes+=len(x['nodes']); leaves+=r['leaves']-len(path)
    if r['minimum_margin'] is not None: minimum=r['minimum_margin'] if minimum is None else min(minimum,r['minimum_margin'])
    if c%100==0: print(json.dumps({'context':c,'total':len(paths)}),flush=True)
assert minimum>=1
print(json.dumps(dict(verdict='EXACT TREE',nodes=nodes,leaves=leaves,pending=1,minimum_margin=minimum,contexts=len(paths),capacity=caps,extra_sha256=sha(D/'extra_v1.json'),master_sha256=sha(D/'master.json'),certified_sha256=sha(certpath),context_hashes=hashes)),flush=True)
