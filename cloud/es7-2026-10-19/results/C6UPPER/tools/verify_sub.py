#!/usr/bin/env python3
"""verify_sub.py PARENT.cnf META.json SUBDIR : stdlib check that the 16 files s11111_<b>.cnf in SUBDIR are each
PARENT byte for byte plus the 4 units of pattern b on Y(1,5),Y(2,5),Y(3,5),Y(4,5), and that all 16 patterns occur.
Then UNSAT of the 16 sub-cubes implies UNSAT of PARENT."""
import sys, json, os, hashlib, itertools
parent, meta, d = sys.argv[1:4]
Y = json.load(open(meta))['Y']; v5 = [Y[k] for k in ('1,5', '2,5', '3,5', '4,5')]
raw = open(parent, 'rb').read(); hdr, body = raw.split(b'\n', 1); _, _, nv, nc = hdr.split()
print('parent sha256', hashlib.sha256(raw).hexdigest())
seen = set()
for b in itertools.product((1, 0), repeat=4):
    f = os.path.join(d, 's11111_' + ''.join(map(str, b)) + '.cnf'); r = open(f, 'rb').read()
    h, rest = r.split(b'\n', 1)
    assert h.split() == [b'p', b'cnf', nv, str(int(nc) + 4).encode()] and rest.startswith(body), f
    tail = [l for l in rest[len(body):].decode().split('\n') if l.strip()]
    assert tail == ['%d 0' % (v if x else -v) for v, x in zip(v5, b)], f
    seen.add(b)
assert len(seen) == 16
print('OK: 16 sub-cubes, each = parent + its Y(i,5) pattern; cover of the parent complete')
