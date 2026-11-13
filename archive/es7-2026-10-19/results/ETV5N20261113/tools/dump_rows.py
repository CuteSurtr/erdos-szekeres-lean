"""Write the current full row set (cycle + coupled) as [[support, demand], ...]."""
import json, sys, os
rows = {}
for s, d in json.load(open('rows_cycle.json')): rows[tuple(sorted(s))] = max(d, rows.get(tuple(sorted(s)), 0))
for fn in ('cores.jsonl', 'trows.jsonl'):
    if os.path.exists(fn):
        for line in open(fn):
            s = tuple(sorted(json.loads(line)['support'])); rows[s] = max(1, rows.get(s, 0))
json.dump([[list(k), v] for k, v in rows.items()], open(sys.argv[1], 'w'))
print(len(rows))
