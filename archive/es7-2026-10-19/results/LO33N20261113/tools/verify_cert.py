"""Independent replay of a two-capacity certificate (LO33, 13 Nov 2026).
Usage (any cwd): verify_cert.py c c2 extra.json tree.json.gz [certified.jsonl]
Checks, in exact integer arithmetic:
 1. the base catalog is source-2650.json.gz with the pinned SHA-256 (common.py);
 2. the extra rows are exactly: the row (F, 84 - c) if 84 - c > 0, the row (Lo, 70 - c2) if 70 - c2 > 0, and
    demand-one rows whose supports all carry a cake_lpr 's VERIFIED UNSAT' verdict in certified.jsonl;
 3. the tree replays under scripts/omission_tree.check_tree at budget 33 with exactly one pending leaf,
    and that leaf is the root's 'state 0 missing' child (discharged by
    OmissionResidualZeroState.zero_mem_residualOccupied, as in the 313 tree)."""
import gzip, hashlib, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
REPO = '/home/jay/research/lean/erdos-szekeres-lean'; sys.path.insert(0, os.path.join(REPO, 'scripts'))
from lo_common import N, ROWS, F, LO, certified_supports
from omission_tree import check_tree
c, c2, xp, tp = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3], sys.argv[4]
cp = sys.argv[5] if len(sys.argv) > 5 else os.path.join(HERE, 'certified.jsonl')
extra = json.load(open(xp))
cert = {tuple(s) for s in certified_supports(cp)}
caps = [(sorted(r['support']), r['rhs']) for r in extra if r['rhs'] != 1]
want = [(sorted(F), 84 - c)] * (84 - c > 0) + [(sorted(LO), 70 - c2)] * (70 - c2 > 0)
assert sorted(caps) == sorted(want), 'capacity rows differ from the pair'
ones = [tuple(sorted(r['support'])) for r in extra if r['rhs'] == 1]
assert all(s in cert for s in ones), 'an extra row is not cake_lpr-certified'
rows = [(list(s), d) for s, d in ROWS] + [(list(r['support']), r['rhs']) for r in extra]
tree = json.load(gzip.open(tp))
BUD = int(os.environ.get('LO_BUDGET', '33'))
assert tree['hole_budget'] == BUD and tree['root'] == 0
nodes = tree['nodes']; root = nodes[0]
assert root['type'] == 'branch' and root['vertex'] == 0 and nodes[root['one']]['type'] == 'pending'
res = check_tree(N, rows, BUD, nodes, 0, allow_pending=True)
assert res['pending'] == 1 and res['minimum_margin'] >= 1
print(json.dumps({'pair': [c, c2], 'budget': BUD, 'extra_rows': len(extra), 'certified_rows_used': len(ones), 'capacity_rows': [(len(s), d) for s, d in caps],
                  'replay': res, 'extra_sha256': hashlib.sha256(open(xp, 'rb').read()).hexdigest(),
                  'tree_sha256': hashlib.sha256(open(tp, 'rb').read()).hexdigest(), 'verdict': 'CLOSED (exact replay)'}))
