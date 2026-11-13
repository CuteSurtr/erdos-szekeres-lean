"""F-capacity LP threshold with the main thread's CEGAR rows added (read-only use of
res33-20261113/newrows.json; rows assumed valid there, demand 1 each)."""
import sys, json
sys.argv = [sys.argv[0]]
from cap_lp import res, lp, fam
RS, RC = res['states'], res['constraints']
new = json.load(open('/home/jay/research/data/res33-20261113/newrows.json'))
extra = [{'support': r['support'], 'rhs': r.get('rhs', 1)} for r in new]
F = fam(RS, lambda s: s[0] >= 5)
base = lp(RS, list(RC) + extra, [], True)[0]
print('rows', len(RC) + len(extra), 'base LP with CEGAR rows', round(base, 4), flush=True)
for c in [56, 57, 58, 59, 60, 61]:
    v = lp(RS, list(RC) + extra, [{'support': F, 'rhs': 84 - c}], True)[0]
    print('c', c, 'LP', round(v, 4), flush=True)
