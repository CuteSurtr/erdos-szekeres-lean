import json, sys, collections
sys.path.insert(0,'/opt/c3s/cloud/es7-2026-10-19/results/C3a'); sys.path.insert(0,'/opt/c3s/cloud/es7-2026-10-19/results/C3-S/tools')
from hullcase import parse_layers, layers_name, tree_children
D='/home/user/erdos-szekeres-lean/cloud/es7-2026-10-19/results/C3WAVE1/C11'
recs=[json.loads(l) for l in open('/opt/work/out.jsonl')]
cert={r['node']:r for r in recs if r.get('certified')}
split={r['node'] for r in recs if r.get('split')}
tried={r['node']:r for r in recs if 'status' in r}
allt=collections.defaultdict(lambda:[0,0])
for r in recs:
    if 'status' in r: allt[r['node']][0]+=r.get('solve_s',0); allt[r['node']][1]+=r.get('check_s',0)
roots=[l.split()[1] for l in list(open(D+'/roots.txt'))[1:]]
rej=[r['node'] for r in recs if r.get('status')=='UNSATISFIABLE' and not r.get('certified')]
rej_open=[n for n in rej if n not in cert]
sat=[r['node'] for r in recs if r.get('status')=='SATISFIABLE']
def closed(n):
    if n in cert: return True
    if n in split: return all(closed(layers_name(c)) for c in tree_children(11,7,parse_layers(n)))
    return False
def sub(n):
    yield n
    if n in split and n not in cert:
        for c in tree_children(11,7,parse_layers(n)): yield from sub(layers_name(c))
D_all=collections.defaultdict(lambda:[0,0,0])
print('| root | status | certified by depth | splits | solve s | check s |'); print('|---|---|---|---|---|---|')
for r in roots:
    started = r in tried or r in split
    cd=collections.Counter(); sp=0; so=ch=0
    for n in sub(r):
        d=len(parse_layers(n))
        if n in cert: cd[d]+=1; D_all[d][0]+=1
        elif n in split: sp+=1; D_all[d][1]+=1
        elif started: D_all[d][2]+=1
        if n in allt: so+=allt[n][0]; ch+=allt[n][1]
    if not started: continue
    st='closed' if closed(r) else 'open'
    print(f"| {r} | {st} | {', '.join(f'd{d}:{c}' for d,c in sorted(cd.items()))} | {sp} | {so:.0f} | {ch:.0f} |")
print('\n| depth | certified | split | open (frontier, incl. unsolved) |'); print('|---|---|---|---|')
for d in sorted(D_all): print(f'| {d} | '+' | '.join(map(str,D_all[d]))+' |')
print('\nroots started:', sum(1 for r in roots if r in tried or r in split), 'closed:', sum(closed(r) for r in roots), 'of', len(roots))
print('driver PROOF NOT ACCEPTED records:', rej, '; of these still not certified:', rej_open, '; SAT:', sat)
