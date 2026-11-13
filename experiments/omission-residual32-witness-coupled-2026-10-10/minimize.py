#!/usr/bin/env python3
"""Delete owners from a discovered necessary-condition obstruction."""
from pathlib import Path
exec(Path(__file__).with_name('probe.py').read_text().split('\nfaces = ')[0])
initial = [17,25,43,53,65,68,74,79,85,89,91,96,107,110,111,125]
support = initial.copy()
started = time.monotonic()
deadline = started + 600
results = []
for removed in initial:
    if time.monotonic() >= deadline-10 or len(support) <= 8:
        break
    trial = [v for v in support if v != removed]
    tick = time.monotonic()
    current = None
    try:
        current = model.CompactModel(trial,min(deadline,tick+30))
        result = current.probe(min(deadline,time.monotonic()+25))
    except (TimeoutError,model.z3.Z3Exception,MemoryError) as error:
        result = {'support':trial,'status':'unknown','reason':str(error)}
    result['removed'] = removed
    result['total_seconds'] = time.monotonic()-tick
    if result['status'] == 'unsat':
        support = trial
    results.append(result)
    print(json.dumps(result),flush=True)
    (ROOT/'minimal-core.json').write_text(json.dumps({'scope':'Discovery only; not a Lean proof.','source_sha256':SOURCE_SHA,'holes':sorted(HOLES),'initial':initial,'support':support,'deletions':results},indent=2)+'\n')
    del current
    gc.collect()
print('FINAL',support,time.monotonic()-started,flush=True)
