#!/usr/bin/env python3
"""Merge the top-hull leaf logs into one tree file: main run (top33_leaves.jsonl, with its own
SPLIT record for the hard root cube), plus the manual depth-4 re-split of the last open child
(last_children / last_leaves) recorded as a SPLIT of that child.  The depth-5 side split of the
hard root cube (hard_leaves.jsonl) is kept as a separate file and not used in the tree."""
import json, sys
R = sys.argv[1]; out = sys.argv[2]
L = [json.loads(l) for l in open(R + '/top33_leaves.jsonl')]
done = {tuple(d['cube']) for d in L}
try:
    last = [int(x) for x in open(R + '/last_cube.txt').read().split()]
    if tuple(last) not in done:
        ch = [[int(x) for x in l.split()[1:-1]][len(last):] for l in open(R + '/last_children.icnf') if l.startswith('a')]
        L.append(dict(key='cube:' + ' '.join(map(str, last)), cube=last, weight_log2=-len(last), status='SPLIT',
                      solve_s=0.0, children=ch,
                      note='original solve stopped at wrap-up / re-split by hand with march_cu -d 4'))
        L += [json.loads(l) for l in open(R + '/last_leaves.jsonl')]
except FileNotFoundError:
    pass
with open(out, 'w') as f:
    for d in L: f.write(json.dumps(d) + '\n')
