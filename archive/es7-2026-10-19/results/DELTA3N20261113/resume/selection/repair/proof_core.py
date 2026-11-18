#!/usr/bin/env python3
"""Extract a small, human-checkable private-polygon obstruction subformula."""
import hashlib
import itertools as it
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
out=['# Private-polygon proof candidates','',
     'The integer predicates are COMPUTED by two geometry implementations.',
     'The implication from these predicates is PROVED in THEORY.md.',
     'The core CNFs have not been solved or certified by this track.','']
for tag in ('rightmost-n7','rightmost-n8','arbitrary-n7'):
    d=json.loads((HERE/'data'/f'{tag}-audit.json').read_text());T=set(d['A']+[d['r']]);V=set(range(d['m']))-T
    assert sorted(T) in d['fourcaps']
    records=[];clauses=[[-(i+1) for i in sorted(T)]]
    out.extend([f'## {tag}', '',f'T={sorted(T)} is a four-cap; A=T minus r, r={d["r"]}.','',
                '| Deleted vertex t | Blue supports of private polygons H={t} union Q |',
                '|---|---|'])
    for t in sorted(T):
        private=[set(H)-{t} for H in d['targets'] if set(H)&T=={t}]
        selected=None
        for size in range(1,len(private)+1):
            for choice in it.combinations(private,size):
                if not set.intersection(*choice):selected=choice;break
            if selected is not None:break
        assert selected is not None
        records.append(dict(t=t,blue_supports=[sorted(Q) for Q in selected],intersection=[]))
        for Q in selected:clauses.append([i+1 for i in sorted(Q|{t})])
        out.append(f'| {t} | '+ '; '.join(str(sorted(Q)) for Q in selected)+' |')
    clauses.extend([[-(i+1),-(j+1)] for i,j in it.combinations(sorted(V),2)])
    p=HERE/'data'/f'{tag}-core.cnf'
    with p.open('w') as f:
        f.write('c Private-polygon obstruction; subformula of the full one-blue CNF\n')
        f.write(f'p cnf {d["m"]} {len(clauses)}\n')
        for C in clauses:f.write(' '.join(map(str,C))+' 0\n')
    full=[]
    for line in (HERE/'data'/f'{tag}-one.cnf').read_text().splitlines():
        if line and line[0] not in 'cp':full.append(tuple(map(int,line.split()[:-1])))
    assert all(tuple(C) in full for C in clauses)
    meta=dict(tag=tag,T=sorted(T),blue=sorted(V),private=records,variables=d['m'],clauses=len(clauses),
              sha256=hashlib.sha256(p.read_bytes()).hexdigest(),subformula_checked=True)
    (HERE/'data'/f'{tag}-core.json').write_text(json.dumps(meta,indent=2)+'\n')
    out.extend(['',f'Core: `{p.name}`, {d["m"]} variables, {len(clauses)} clauses.',
                f'SHA-256: `{meta["sha256"]}`.',''])
    print(json.dumps({k:meta[k] for k in ('tag','variables','clauses','sha256')}))
out.extend(['## Direct contradiction','',
            'Any four-cap-free B omits some t from T. If at most one old-blue',
            'point q is selected, all private polygons listed for that t would',
            'need to contain q: their only possible selected vertices lie in',
            'their displayed blue supports. But the intersection of those',
            'supports is empty. With no selected blue point they are all missed.',
            'This covers either color of r and every deletion from A.',''])
(HERE/'PRIVATE_POLYGONS.md').write_text('\n'.join(out))
