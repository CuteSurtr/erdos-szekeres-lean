#!/usr/bin/env python3
"""HEURISTIC: deterministic, balanced sampling of nearby nine-owner cuts."""
import argparse
import collections
import hashlib
import json
from pathlib import Path
import resource

resource.setrlimit(resource.RLIMIT_AS,(150<<20,150<<20))
p=argparse.ArgumentParser()
p.add_argument('witness',type=Path);p.add_argument('extra',type=Path)
p.add_argument('out',type=Path);p.add_argument('--count',type=int,default=128)
a=p.parse_args()
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
H=set(json.loads(a.witness.read_text())['holes'])
assert len(H)==34 and 0 not in H
have={tuple(sorted(r['support'])) for r in json.loads(a.extra.read_text()) if r['rhs']==1}
old=Path('/home/jay/research/data/fastbb-20261113/killtools')
provenance={};sources={}
for name in ['newrows.json','fnewrows.json','newrows_g2.json']:
    path=old/name;sources[str(path)]=sha(path)
    for k,r in enumerate(json.loads(path.read_text())):
        s=tuple(sorted(r['support']))
        if len(s)!=9 or len(set(s))!=9 or s in have or len(set(s)&H)!=1:continue
        assert all(type(i) is int and 0<=i<154 for i in s)
        provenance.setdefault(s,[]).append({'path':str(path),'index':k})
buckets=collections.defaultdict(list)
for s in provenance:buckets[next(iter(set(s)&H))].append(s)
for q in buckets.values():q.sort(key=lambda s:hashlib.sha256(bytes(s)).digest())
selected=[];count=collections.Counter()
while len(selected)<a.count and any(buckets.values()):
    for j in sorted(buckets):
        if not buckets[j]:continue
        s=buckets[j].pop();selected.append(s);count[j]+=1
        if len(selected)>=a.count:break
assert not a.out.exists()
r={'label':'HEURISTIC nearby candidates; no row accepted before a fresh certificate',
   'rationale':'Nine-owner supports meeting the previous witness in exactly one hole, sampled across that hole index; this does not assert that the current witness violates them.',
   'witness_sha256':sha(a.witness),'previous_extra_sha256':sha(a.extra),
   'candidate_sources':sources,'available_candidates':len(provenance),'selected_by_single_hole':dict(count),
   'candidates':[{'support':list(s),'rhs':1,'discovery_references':provenance[s]} for s in selected]}
a.out.write_text(json.dumps(r,indent=2)+'\n')
print(json.dumps({'available':len(provenance),'selected':len(selected),'buckets':len(buckets)}))
