#!/usr/bin/env python3
"""Independent streaming replay of the 313 residual certificate tree (Excludes2650Zero 32).

Own implementation (does not import repository code).  The xz parts are decompressed through a
pipe and the flat "nodes" array is decoded object by object, so the 359 MB JSON is never held in
memory.  For every weighted leaf in the subtree of node 1 (root branch on state 0, value 0 =
state 0 occupied) it recomputes, with exact integers, the capacity margin

    lower - cap*(B - |M|) - sum_{i free} max(0, load_i - cap),
    lower  = sum_r w_r * max(0, d_r - |S_r & M|),  load_i = sum_r w_r [i in S_r],

where M / O are the states fixed missing / occupied on the path.  Soundness: for a Boolean h with
h|M = 1, h|O = 0, sum h <= B and every row satisfied,
    lower <= sum_{i free} load_i h_i <= cap*(sum h - |M|) + excess <= cap*(B-|M|) + excess,
so a positive margin is a contradiction.  Bitmask arithmetic on Python ints is used throughout.
Usage: python3 -I replay_313_tree.py
"""
import gzip, json, subprocess, sys, glob, hashlib, time

import os as _os  # paths are relative to this file; ES_REPO_ROOT overrides the repository root
HERE = _os.path.dirname(_os.path.abspath(__file__))
TOP = _os.path.dirname(_os.path.dirname(HERE))  # cloud/es7-2026-10-19/results/ES8SLACK
ROOT = _os.environ.get('ES_REPO_ROOT') or _os.path.normpath(_os.path.join(TOP, '..', '..', '..', '..'))
E = ROOT + '/experiments'
SRC = E + '/omission-residual32-rank-global-2026-10-10/source-2650.json.gz'
PARTS = sorted(glob.glob(E + '/omission-final313-2026-10-11/certificate/tree-2650-32.json.xz.part-*'))

raw = gzip.decompress(open(SRC, 'rb').read())
assert hashlib.sha256(raw).hexdigest() == 'e800d5f8a6c5cc45c73ddcc1e57488f2ca8f2ffb704a1515ff7444d589c682f6'
cat = json.loads(raw)
N = len(cat['states'])
rows = [(sum(1 << i for i in set(r['support'])), r['support'], int(r['rhs'])) for r in cat['constraints']]
R = len(rows)
del raw, cat

cmd = 'cat ' + ' '.join("'%s'" % p for p in PARTS) + ' | xz -dc'
proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, bufsize=1 << 20)
stream = proc.stdout
dec = json.JSONDecoder()

buf = ''
def fill():
    global buf
    chunk = stream.read(1 << 22)
    if chunk:
        buf += chunk.decode('ascii')
        return True
    return False

# header
while '"nodes":[' not in buf:
    if not fill():
        raise SystemExit('no nodes array')
head, buf = buf.split('"nodes":[', 1)
header = json.loads(head + '"nodes":[]}')
B = header['hole_budget']; root = header['root']
assert B == 32 and root == 0, header
assert header['source_sha256'] == 'e800d5f8a6c5cc45c73ddcc1e57488f2ca8f2ffb704a1515ff7444d589c682f6'

parent = {}          # child index -> (parent index, vertex, value)   (value 1 = missing)
assigned = set()
k = 0
pos = 0
stats = dict(branch=0, weighted=0, pending=0, other=0, leaves_in_zero_subtree=0,
             min_margin=None, bad=[], pending_nodes=[], max_depth=0, max_weight=0, max_cap=0)
t0 = time.time()

def path_of(idx):
    """Return (missing_mask, occupied_mask, list of path nodes from idx up to root)."""
    miss = 0; occ = 0; seen_vars = 0; chain = [idx]
    cur = idx
    while cur != root:
        p, v, val = parent[cur]
        bit = 1 << v
        assert not (seen_vars & bit), 'variable repeated on a path'
        seen_vars |= bit
        if val:
            miss |= bit
        else:
            occ |= bit
        cur = p
        chain.append(cur)
    return miss, occ, chain

def margin(miss, occ, node):
    cap = node['capacity']; W = node['weights']
    assert type(cap) is int and cap >= 0
    loads = [0] * N
    lower = 0
    used = set()
    for pair in W:
        r, w = pair
        assert type(r) is int and 0 <= r < R and r not in used and type(w) is int and w >= 0
        used.add(r)
        m, sup, dem = rows[r]
        lower += w * max(0, dem - (m & miss).bit_count())
        for i in sup:
            loads[i] += w
        if w > stats['max_weight']:
            stats['max_weight'] = w
    if cap > stats['max_cap']:
        stats['max_cap'] = cap
    fixed = miss | occ
    excess = 0
    for i in range(N):
        if not (fixed >> i) & 1:
            if loads[i] > cap:
                excess += loads[i] - cap
    return lower - cap * (B - miss.bit_count()) - excess

done = False
while not done:
    # decode next object
    while True:
        # skip separators/whitespace
        while pos < len(buf) and buf[pos] in ', \n\r\t':
            pos += 1
        if pos < len(buf) and buf[pos] == ']':
            done = True
            break
        try:
            node, end = dec.raw_decode(buf, pos)
            pos = end
            break
        except json.JSONDecodeError:
            buf = buf[pos:]; pos = 0
            if not fill():
                raise SystemExit('truncated stream')
    if done:
        break
    if pos > (1 << 23):
        buf = buf[pos:]; pos = 0
    t = node.get('type')
    if t == 'branch':
        stats['branch'] += 1
        v = node['vertex']; z = node['zero']; o = node['one']
        assert type(v) is int and 0 <= v < N
        for c, val in ((z, 0), (o, 1)):
            assert type(c) is int and c > k, 'child index not after parent (non-preorder)'
            assert c not in assigned, 'node with two parents'
            assigned.add(c)
            parent[c] = (k, v, val)
    elif t == 'weighted':
        stats['weighted'] += 1
        assert k in parent, 'leaf before its parent'
        miss, occ, chain = path_of(k)
        stats['max_depth'] = max(stats['max_depth'], len(chain) - 1)
        in_zero = (len(chain) >= 2 and chain[-2] == 1)
        if in_zero:
            assert occ & 1, 'zero subtree leaf without state 0 occupied'
            stats['leaves_in_zero_subtree'] += 1
            mg = margin(miss, occ, node)
            if stats['min_margin'] is None or mg < stats['min_margin']:
                stats['min_margin'] = mg
            if mg <= 0:
                stats['bad'].append(k)
    elif t == 'pending':
        stats['pending'] += 1
        miss, occ, chain = path_of(k)
        stats['pending_nodes'].append((k, chain[-2] if len(chain) >= 2 else None))
    else:
        stats['other'] += 1
    k += 1
    if k % 100000 == 0:
        print('nodes', k, 'elapsed %.1fs' % (time.time() - t0), file=sys.stderr, flush=True)

proc.wait()
stats['nodes'] = k
stats['all_children_assigned'] = (len(assigned) == k - 1) and all(0 < c < k for c in assigned)
stats['root_branch'] = None
stats['elapsed_s'] = round(time.time() - t0, 1)
ok = (stats['bad'] == [] and stats['other'] == 0 and stats['all_children_assigned']
      and all(top == 875158 or top != 1 for _, top in stats['pending_nodes'])
      and stats['min_margin'] is not None and stats['min_margin'] >= 1)
stats['ALL_ZERO_SUBTREE_LEAVES_CERTIFIED'] = ok
print(json.dumps(stats, indent=1))
json.dump(stats, open(HERE + '/replay_313_tree_out.json', 'w'), indent=1)
sys.exit(0 if ok else 1)
