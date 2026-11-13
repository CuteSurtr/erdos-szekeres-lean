#!/usr/bin/env python3
"""up.py CNF[+CLAUSEFILE...]... (a "+"-joined argument is one formula): root-level unit propagation (two watched literals); prints #assigned variables or CONFLICT.
Solver-independent count of the literals implied at root by each formula."""
import sys, time

def up(path):
    clauses = []
    for part in path.split("+"):
      with open(part) as f:
        for line in f:
            if line[0] in 'pc':
                continue
            v = list(map(int, line.split()))
            assert v[-1] == 0
            clauses.append(v[:-1])
    nv = max(max(abs(l) for l in c) for c in clauses if c)
    val = [0] * (nv + 1)
    watch = {}
    trail = []
    for i, c in enumerate(clauses):
        if len(c) == 1:
            trail.append(c[0])
        else:
            watch.setdefault(c[0], []).append(i)
            watch.setdefault(c[1], []).append(i)
    def setlit(l):
        a = val[abs(l)]
        if a == 0:
            val[abs(l)] = 1 if l > 0 else -1
            return True
        return (a > 0) == (l > 0)
    q = []
    for l in trail:
        if not setlit(l):
            return 'CONFLICT'
        q.append(l)
    def is_true(l):
        a = val[abs(l)]
        return a != 0 and (a > 0) == (l > 0)
    def is_false(l):
        a = val[abs(l)]
        return a != 0 and (a > 0) != (l > 0)
    head = 0
    while head < len(q):
        l = q[head]; head += 1
        fl = -l
        ws = watch.get(fl, [])
        keep = []
        conflict = False
        for idx, ci in enumerate(ws):
            if conflict:
                keep.append(ci); continue
            c = clauses[ci]
            if c[0] == fl:
                c[0], c[1] = c[1], c[0]
            if is_true(c[0]):
                keep.append(ci); continue
            for k in range(2, len(c)):
                if not is_false(c[k]):
                    c[1], c[k] = c[k], c[1]
                    watch.setdefault(c[1], []).append(ci)
                    break
            else:
                keep.append(ci)
                if is_false(c[0]):
                    conflict = True
                else:
                    setlit(c[0]); q.append(c[0])
        watch[fl] = keep
        if conflict:
            return 'CONFLICT'
    return sum(1 for x in val[1:] if x)

for p in sys.argv[1:]:
    t = time.time()
    print(p, up(p), f'{time.time() - t:.1f}s', flush=True)
