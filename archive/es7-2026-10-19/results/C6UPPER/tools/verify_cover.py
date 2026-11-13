#!/usr/bin/env python3
"""verify_cover.py BASE.cnf META.json CUBEDIR : stdlib-only check of the cube split.
(1) every cube file = header(nv, nc+k) + exact body of BASE + k unit clauses;
(2) every cube carries the unit Y(1,2) and one sign pattern on Y(1,3),Y(1,4),Y(2,3),Y(2,4),Y(3,4);
(3) the patterns are pairwise distinct and number 2^5, so they cover all assignments of those variables.
Then UNSAT of all cubes implies UNSAT of BASE + Y(1,2)."""
import sys, json, os, hashlib
def check(cond, msg):
    """explicit check (not `assert`), so that `python3 -O` cannot skip it"""
    if not cond:
        sys.exit('FAIL: %s' % msg)
base, meta, d = sys.argv[1:4]
Y = json.load(open(meta))['Y']
y12 = Y['1,2']; cv = [Y[k] for k in ('1,3', '1,4', '2,3', '2,4', '3,4')]
raw = open(base, 'rb').read()
hdr, body = raw.split(b'\n', 1)
_, _, nv, nc = hdr.split(); nc = int(nc)
print('base sha256', hashlib.sha256(raw).hexdigest(), 'nv', int(nv), 'nc', nc)
seen = set()
for f in sorted(os.listdir(d)):
    if not (f.startswith('c') and f.endswith('.cnf')):
        continue
    r = open(os.path.join(d, f), 'rb').read()
    h, rest = r.split(b'\n', 1)
    check(rest.startswith(body), f)
    tail = rest[len(body):].decode().split('\n')
    units = [int(l.split()[0]) for l in tail if l.strip()]
    check(all(l.split()[1:] == ['0'] and len(l.split()) == 2 for l in tail if l.strip()), f)
    check(h.split() == [b'p', b'cnf', nv, str(nc + len(units)).encode()], f)
    check(units[0] == y12 and len(units) == 6, f)
    pat = tuple(1 if u > 0 else 0 for u in units[1:])
    check([abs(u) for u in units[1:]] == cv, f)
    check(f == 'c' + ''.join(map(str, pat)) + '.cnf', f)
    seen.add(pat)
check(len(seen) == 32, len(seen))
print('OK: 32 distinct cubes, each = base + Y(1,2) + pattern; cover complete')
