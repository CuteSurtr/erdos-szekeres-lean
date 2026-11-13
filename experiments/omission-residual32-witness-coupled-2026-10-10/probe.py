#!/usr/bin/env python3
"""Bounded coupled-geometry search inside the exact case-four countermodel."""
import gc
import hashlib
import json
import random
import time
from pathlib import Path

import model

ROOT = Path('.cache/residual32-witness-coupled-2026-10-10')
SOURCE = Path('.cache/residual32-resume-2026-10-10-b/source.json')
SOURCE_SHA = 'f03eebb1d20eae3bd25dbb5024eaacdfdcc5bcd8ed964d190bdfa59c73aeb909'
HOLES = {7,12,33,39,44,47,50,51,52,54,55,56,69,71,73,75,76,77,78,90,97,99,101,109,115,117,118,119,124,127,132,133}
assert hashlib.sha256(SOURCE.read_bytes()).hexdigest() == SOURCE_SHA
data = json.loads(SOURCE.read_text())
occupied = set(range(154)) - HOLES
assert len(HOLES) == 32
assert all(len(HOLES.intersection(r['support'])) >= r['rhs'] for r in data['constraints'])
model.ROOT = ROOT
model.D = data
model.occupied = occupied
model.cells = [{(x+1,y) for x,h in enumerate(s[:4]) for y in range(1,h+1)} for s in data['states']]
# pair_boxes calls cells; keep its function binding while constructing the table.
state_sets = model.cells
model.cells = lambda s: {(i+1,y) for i,h in enumerate(s) for y in range(1,h+1)}
P, mn, mx = model.pair_boxes(data['states'])
model.TT = model.triple_table(P,mn,mx)
model.cells = state_sets

faces = sorted({frozenset(set(r['support']) & occupied) for r in data['constraints']
                if len(r['support']) - r['rhs'] == 7 and
                len(set(r['support']) & occupied) == 7}, key=lambda x: tuple(sorted(x)))
masks = [sum(1 << v for v in f) for f in faces]
rng = random.Random(2026101001)
pool = {}
for target in [12,13,14,16]:
    for face in faces:
        S = set(face)
        for _ in range(10):
            choices = []
            for f in faces:
                T = S | f
                if len(T) > target or T == S:
                    continue
                mask = sum(1 << v for v in T)
                score = sum(x & mask == x for x in masks)
                choices.append((score, -len(T), rng.random(), T))
            if not choices:
                break
            S = max(choices, key=lambda x:x[:3])[-1]
        if len(S) >= 8:
            mask = sum(1 << v for v in S)
            pool[tuple(sorted(S))] = sum(x & mask == x for x in masks)
ranked = sorted(pool, key=lambda s:(-pool[s],len(s),s))
entries = []
for target in [12,13,14,16]:
    group = [s for s in ranked if len(s) == target][:20]
    entries.extend({'support':list(s),'faces':pool[s],'size':len(s),'rank':i}
                   for i,s in enumerate(group))
entries.sort(key=lambda e:(e['rank'], e['size']))
ROOT.mkdir(parents=True,exist_ok=True)
(ROOT/'candidates.json').write_text(json.dumps(entries,indent=2)+'\n')
print('CANDIDATES',len(faces),len(pool),len(entries),flush=True)
started = time.monotonic()
deadline = started + 600
results = []
for entry in entries:
    if time.monotonic() >= deadline-10:
        break
    tick = time.monotonic()
    current = None
    print('BUILD',entry,flush=True)
    try:
        current = model.CompactModel(entry['support'],min(deadline,tick+45))
        result = current.probe(min(deadline,time.monotonic()+25))
    except (TimeoutError,model.z3.Z3Exception,MemoryError) as error:
        result = {'support':entry['support'],'status':'unknown','reason':str(error)}
    result['faces'] = entry['faces']
    result['total_seconds'] = time.monotonic()-tick
    results.append(result)
    print(json.dumps(result),flush=True)
    (ROOT/'results.json').write_text(json.dumps({'scope':'Discovery only; UNSAT requires Lean necessity and proof-term checks; SAT is not geometric realization.','source_sha256':SOURCE_SHA,'holes':sorted(HOLES),'results':results},indent=2)+'\n')
    if result['status'] == 'unsat':
        break
    del current
    gc.collect()
print('DONE',len(results),time.monotonic()-started,flush=True)
