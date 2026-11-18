#!/usr/bin/env python3
"""Initial too-big record for run_tree_v6.py, rebuilt read-only from a packet's finder logs. Selection data only.

Usage: init_too_big_v1.py PACKET OUT [--log=TAG ...]
Every finder receipt <run>/<tag>.json whose 'bb' is PACKET contributes the context_too_big events of <tag>.log (and of
<tag>.x.log if present); --log=TAG adds the log of a finder without a receipt (e.g. one stopped with its loop).
OUT gets one line '<context> <nodes_so_far> <tag>' per event and must not exist yet.
"""
import json
from pathlib import Path
import sys

pk=Path(sys.argv[1]).resolve();out=Path(sys.argv[2]);extra=[x[6:] for x in sys.argv[3:] if x.startswith('--log=')]
assert pk.is_dir() and len(extra)==len(sys.argv)-3
tags=sorted(q.stem for q in pk.parent.glob('*.json') if json.loads(q.read_text()).get('bb')==str(pk))+extra
lines=[]
for t in tags:
    for lg in [pk.parent/f'{t}.log',pk.parent/f'{t}.x.log']:
        if not lg.exists():assert lg.name.endswith('.x.log'),lg;continue
        for s in lg.read_text().splitlines():
            try:e=json.loads(s)
            except ValueError:continue
            if isinstance(e,dict) and e.get('event')=='context_too_big':lines.append(f"{e['context']} {e['nodes_so_far']} {lg.name[:-4]}\n")
with out.open('x') as f:f.write(''.join(lines))
best={}
for s in lines:c,n=map(int,s.split()[:2]);best[c]=max(best.get(c,0),n)
opn={c for c in best if not (pk/f'ctx-{c}.json.gz').exists()}
print(json.dumps({'logs':len(tags),'events':len(lines),'contexts':len(best),'open':len(opn),
                  'open_above_150000':sorted(c for c in opn if best[c]>150000)}))
