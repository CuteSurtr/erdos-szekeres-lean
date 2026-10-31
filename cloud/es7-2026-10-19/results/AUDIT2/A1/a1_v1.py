# A1: decode V1L/Leaves.lean independently; compare with verify/hull_leaves.icnf and with
# the cake_lpr records of V1-0..V1-3 and the V1-L backup (index and cube literal-for-literal).
import re, json, sys, hashlib
B = sys.argv[1]  # cloud/es7-2026-10-19
src = open(B + '/results/V1-L/V1L/Leaves.lean').read()
chunks = {}
for m in re.finditer(r'def leafChunk(\d+) : List \(List Nat\) := \[(.*?)\]\]', src, re.S):
    chunks[int(m.group(1))] = [[int(x) for x in c.split(',')] for c in re.findall(r'\[([0-9, ]+)\]', m.group(2) + ']')]
order = [int(x) for x in re.findall(r'leafChunk(\d+)', src[src.index('def hullLeaves'):])]
assert order == list(range(12)), order
dec = lambda d: d // 2 if d % 2 == 0 else -(d // 2)
leaves = [[dec(d) for d in c] for k in order for c in chunks[k]]
print('Lean hullLeaves decoded:', len(leaves))
raw = open(B + '/verify/hull_leaves.icnf', 'rb').read()
print('hull_leaves.icnf sha256', hashlib.sha256(raw).hexdigest())
icnf = [[int(x) for x in l.split()[1:]] for l in raw.decode().splitlines() if l.strip()]
assert all(c[-1] == 0 for c in icnf); icnf = [c[:-1] for c in icnf]
print('icnf cubes', len(icnf), 'equal to Lean:', icnf == leaves)
files = ['V1-0/leaves_cake.jsonl', 'V1-1/leaves_cake.jsonl', 'V1-2/leaves_cake.jsonl',
         'V1-3/leaves_cake.jsonl', 'V1-L/backup_v1-1/leaves_cake.snapshot.jsonl']
ok = {}
for f in files:
    for line in open(B + '/results/' + f):
        r = json.loads(line); i = r.get('i', r.get('line'))
        good = r['solver_exit'] == 20 and r['cake_lpr'] in ('s VERIFIED UNSAT', 'VERIFIED UNSAT') and r.get('cake_exit', 0) == 0
        if good and r['cube'] == leaves[i]: ok.setdefault(i, []).append(f)
        elif good: print('cube mismatch', f, i)
miss = [i for i in range(len(leaves)) if i not in ok]
print('leaves with a verified record of the same index and cube:', len(ok), 'missing:', miss[:20])
print('residues per file:', {f: sorted({i % 4 for i in ok if f in ok[i]}) for f in files})
