#!/usr/bin/env python3
"""Extract the depth-D contexts of the budget-63 balanced omission tree (ES(8) <= 311 record).

Read-only. Streams the xz parts (concatenated in the given order), parses node headers with the
same regex as the scratch script tree_ctx.py, and writes one JSON line per depth-D node:

  {"ctx": k, "preorder": node index, "depth": D, "missing": [...], "occupied": [...],
   "path": [[vertex, 0|1], ...], "nodes": subtree nodes, "leaves": subtree leaves,
   "weighted": weighted leaves, "over_budget": over-budget leaves, "max_depth": deepest leaf (absolute)}

path[j] = [v, 1] means state v is MISSING (hole, the 'one' child), [v, 0] means OCCUPIED ('zero' child).
Context numbering k follows the preorder of the tree (zero child before one child, as assemble.py writes it).

usage: extract_contexts.py OUT.jsonl SUMMARY.json DEPTH part-aa part-ab ...
"""
import json, lzma, re, sys, time, hashlib

out_path, summary_path, D = sys.argv[1], sys.argv[2], int(sys.argv[3])
parts = sys.argv[4:]
t0 = time.time()
dec = lzma.LZMADecompressor()
sha = hashlib.sha256()
rx = re.compile(r'\{"type":"(branch|weighted|over_budget|pending|context)"(?:,"vertex":(\d+),"zero":(\d+),"one":(\d+))?')
KIND = {'branch': 0, 'weighted': 1, 'over_budget': 2, 'pending': 3, 'context': 4}
kz, ko, kind, vx = [], [], [], []
tail = ''
started = False
header = ''
raw_bytes = 0


def eat(body):
    for m in rx.finditer(body):
        k = KIND[m.group(1)]
        kind.append(k)
        if k == 0:
            kz.append(int(m.group(3))); ko.append(int(m.group(4))); vx.append(int(m.group(2)))
        else:
            kz.append(-1); ko.append(-1); vx.append(-1)


for p in parts:
    with open(p, 'rb') as f:
        while True:
            ch = f.read(1 << 22)
            if not ch:
                break
            sha.update(ch)
            raw = dec.decompress(ch).decode()
            raw_bytes += len(raw)
            s = tail + raw
            if not started:
                k = s.find('"nodes":[')
                if k < 0:
                    tail = s
                    continue
                header = s[:k]
                s = s[k + 9:]
                started = True
            cut = s.rfind('{"type"')
            if cut <= 0:
                tail = s
                continue
            body, tail = s[:cut], s[cut:]
            eat(body)
eat(tail)
assert dec.eof, 'xz stream not complete'
n = len(kind)
t1 = time.time()
print(json.dumps({'event': 'parsed', 'nodes': n, 'decompressed_chars': raw_bytes, 'seconds': round(t1 - t0, 1),
                  'header': header[:300]}), flush=True)
# subtree sizes (children have larger indices than parents in the assembled preorder)
leaves = [0] * n; size = [0] * n; wl = [0] * n; ob = [0] * n; md = [0] * n
depth = [0] * n
for i in range(n):
    if kind[i] == 0:
        assert kz[i] > i and ko[i] > i
        depth[kz[i]] = depth[ko[i]] = depth[i] + 1
for i in range(n - 1, -1, -1):
    if kind[i] == 0:
        a, b = kz[i], ko[i]
        leaves[i] = leaves[a] + leaves[b]; size[i] = 1 + size[a] + size[b]
        wl[i] = wl[a] + wl[b]; ob[i] = ob[a] + ob[b]; md[i] = max(md[a], md[b])
    else:
        leaves[i] = 1; size[i] = 1; md[i] = depth[i]
        wl[i] = int(kind[i] == 1); ob[i] = int(kind[i] == 2)
assert size[0] == n, (size[0], n)
pend = sum(1 for k in kind if k in (3, 4))
# walk to depth D, recording paths
ctxs = []
stack = [(0, ())]
shallow_leaves = []
while stack:
    i, path = stack.pop()
    if depth[i] == D:
        ctxs.append((i, path)); continue
    if kind[i] != 0:
        shallow_leaves.append({'preorder': i, 'depth': depth[i], 'kind': kind[i]}); continue
    stack.append((ko[i], path + ((i, 1),)))
    stack.append((kz[i], path + ((i, 0),)))
ctxs.sort()
print(json.dumps({'event': 'contexts', 'count': len(ctxs), 'shallow_leaves': len(shallow_leaves)}), flush=True)
VERT = vx
with open(out_path, 'w') as f:
    for k, (i, path) in enumerate(ctxs):
        lits = [[VERT[j], b] for j, b in path]
        f.write(json.dumps({'ctx': k, 'preorder': i, 'depth': depth[i],
                            'missing': sorted(v for v, b in lits if b == 1),
                            'occupied': sorted(v for v, b in lits if b == 0),
                            'path': lits, 'nodes': size[i], 'leaves': leaves[i], 'weighted': wl[i],
                            'over_budget': ob[i], 'max_depth': md[i]}, separators=(',', ':')) + '\n')
xs = sorted(leaves[i] for i, _ in ctxs)
tot = sum(xs)
top = sum(xs[-max(1, len(xs) // 10):])
summ = {'parts': parts, 'parts_concat_sha256': sha.hexdigest(), 'tree_nodes': n, 'tree_leaves': leaves[0],
        'pending_nodes': pend, 'depth': D, 'contexts': len(ctxs), 'shallow_leaves': shallow_leaves,
        'context_leaves_sum': tot, 'context_nodes_sum': sum(size[i] for i, _ in ctxs),
        'min': xs[0], 'median': xs[len(xs) // 2], 'max': xs[-1], 'top10pct_share': round(top / tot, 4),
        'seconds': round(time.time() - t0, 1)}
json.dump(summ, open(summary_path, 'w'), indent=1)
print(json.dumps({k: v for k, v in summ.items() if k != 'shallow_leaves'}), flush=True)
