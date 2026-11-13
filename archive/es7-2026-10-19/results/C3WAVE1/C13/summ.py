import sys,json,collections
sys.path.insert(0,'/opt/c3s/cloud/es7-2026-10-19/results/C3a'); sys.path.insert(0,'/opt/c3s/cloud/es7-2026-10-19/results/C3-S/tools')
from hullcase import layers_name, parse_layers, tree_children
D='/home/user/erdos-szekeres-lean/cloud/es7-2026-10-19/results/C3WAVE1/C13/'
recs=[json.loads(l) for l in open(D+'out.jsonl')]
cert={r['node']:r for r in recs if r.get('certified')}
split={r['node'] for r in recs if r.get('split')}
solved=collections.defaultdict(list)
for r in recs:
    if 'status' in r: solved[r['node']].append(r)
roots=[l.split('\t')[1] for l in open(D+'roots.tsv')][1:]
dep=lambda n: len(parse_layers(n))
G=collections.defaultdict(lambda: collections.Counter())
def walk(n,acc):
    acc['nodes'].add(n)
    if n in cert: return True
    if n in split:
        ok=True
        for c in tree_children(11,7,parse_layers(n)):
            ok&=walk(layers_name(c),acc)
        return ok
    return False
out=[]
for R in roots:
    acc={'nodes':set()}
    started = R in cert or R in split or R in solved
    if not started: out.append((R,'not started','','','','')); continue
    ok=walk(R,acc)
    c=collections.Counter(); s=collections.Counter(); o=collections.Counter(); ts=tc=0
    for n in acc['nodes']:
        d=dep(n)
        if n in cert: c[d]+=1; G[d]['certified']+=1
        elif n in split: s[d]+=1; G[d]['split']+=1
        else: o[d]+=1; G[d]['open']+=1
        for r in solved.get(n,[]): ts+=r.get('solve_s',0); tc+=r.get('check_s',0) or 0
    f=lambda C:' '.join(f'd{k}:{C[k]}' for k in sorted(C)) or '-'
    out.append((R,'CLOSED' if ok else 'open',f(c),f(s),f(o),f'{ts:.0f}/{tc:.0f}'))
print('| root | status | certified by depth | split by depth | open by depth | solve/check s |')
print('|---|---|---|---|---|---|')
for r in out: print('| '+' | '.join(r)+' |')
print('\n| depth | certified | split | open |\n|---|---|---|---|')
for d in sorted(G): print(f"| {d} | {G[d]['certified']} | {G[d]['split']} | {G[d]['open']} |")
print('\nclosed roots:',sum(1 for r in out if r[1]=='CLOSED'),'/',len(roots),' started:',sum(1 for r in out if r[1]!='not started'))
print('statuses:',collections.Counter(r['status'] for r in recs if 'status' in r))
