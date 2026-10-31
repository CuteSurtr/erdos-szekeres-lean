import json,sys,collections
sys.path.insert(0,'/opt/c3s/cloud/es7-2026-10-19/results/C3a'); sys.path.insert(0,'/opt/c3s/cloud/es7-2026-10-19/results/C3-S/tools')
from hullcase import parse_layers, layers_name, tree_children
D='/home/user/erdos-szekeres-lean/cloud/es7-2026-10-19/results/C3WAVE1/C03/'
recs=[json.loads(l) for l in open(D+'out.jsonl')]
cert={r['node'] for r in recs if r.get('certified')}
split={r['node'] for r in recs if r.get('split')}
tried={r['node']:r for r in recs if 'status' in r}
roots=[l.strip() for l in open(D+'roots.txt') if l.strip()]
from functools import lru_cache
@lru_cache(None)
def closed(n):
    if n in cert: return True
    if n in split: return all(closed(layers_name(c)) for c in tree_children(11,7,parse_layers(n)))
    return False
def sub(n):
    yield n
    if n in split:
        for c in tree_children(11,7,parse_layers(n)): yield from sub(layers_name(c))
dep=lambda n: len(parse_layers(n))
tot=collections.defaultdict(lambda: collections.Counter())
print('| root | status | certified by depth | splits | solve s | check s |'); print('|---|---|---|---|---|---|')
for r in roots:
    if r not in cert and r not in split and r not in tried: print(f'| {r} | not started | | | | |'); continue
    cd=collections.Counter(); sp=0; so=ch=0
    for n in sub(r):
        d=dep(n)
        if n in cert: cd[d]+=1; tot[d]['certified']+=1
        elif n in split: sp+=1; tot[d]['split']+=1
        else: tot[d]['open']+=1
        if n in tried: so+=tried[n].get('solve_s',0); ch+=tried[n].get('check_s',0) or 0
    print(f"| {r} | {'closed' if closed(r) else 'open'} | {', '.join(f'd{k}:{v}' for k,v in sorted(cd.items()))} | {sp} | {so:.0f} | {ch:.0f} |")
print('\n| depth | certified | split | open |'); print('|---|---|---|---|')
for d in sorted(tot): print(f"| {d} | {tot[d]['certified']} | {tot[d]['split']} | {tot[d]['open']} |")
bad=[r['node']+(' (later certified on recheck)' if r['node'] in cert else '') for r in recs if r.get('status')=='UNSATISFIABLE' and not r.get('certified')]
sat=[r['node'] for r in recs if r.get('status')=='SATISFIABLE']
print(f"\nclosed roots: {sum(closed(r) for r in roots)}/{len(roots)}; SAT: {sat}; rejected proofs: {bad}")
