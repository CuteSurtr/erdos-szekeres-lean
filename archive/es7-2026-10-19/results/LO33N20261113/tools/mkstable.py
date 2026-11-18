"""Stable-order extra file for a pair: capacity rows first, then certified rows in certified.jsonl order."""
import json, sys, os
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from lo_common import cap_rows
c, c2, out = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
seen, cert = set(), []
for line in open(os.path.join(HERE, 'certified.jsonl')):
    r = json.loads(line)
    if r.get('verdict') == 's VERIFIED UNSAT':
        s = tuple(sorted(r['support']))
        if s not in seen: seen.add(s); cert.append(list(s))
json.dump(cap_rows(c, c2) + [{'support': s, 'rhs': 1} for s in cert], open(out, 'w')); print(out, len(cert))
