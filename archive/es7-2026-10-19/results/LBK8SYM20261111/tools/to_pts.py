#!/usr/bin/env python3
"""Float m-fold configuration (JSON with lr, th [, centre]) -> exact .pts in the ES8SYM format
(point = sum_j w_j zeta^j, zeta = e^{2 pi i/m}).  Each orbit representative r e^{i th} is rounded to a + b*zeta with
integers a, b at scale 2^S; point (i,k) = zeta^k (a + b zeta) has w_k = a, w_{k+1 mod m} = b.  The centre (all zeros)
is appended when the JSON says centre = 1 or 'centre' is given.  Adapted from <six10-work-dir>/realize/p2/mfold/tools/to_pts.py.
usage: to_pts.py M CFG.json S OUT.pts [centre|nocentre]"""
import sys, json, math
m, src, S, out = int(sys.argv[1]), sys.argv[2], int(sys.argv[3]), sys.argv[4]
d = json.load(open(src))
centre = int(d.get('centre', 0))
if len(sys.argv) > 5:
    centre = 1 if sys.argv[5] == 'centre' else 0
zs = [math.exp(a) * complex(math.cos(b), math.sin(b)) for a, b in zip(d['lr'], d['th'])]
zs.sort(key=lambda z: -abs(z))
c, s = math.cos(2 * math.pi / m), math.sin(2 * math.pi / m)
rows = []
for z in zs:
    b = z.imag / s; a = z.real - b * c
    A, B = round(a * 2 ** S), round(b * 2 ** S)
    for k in range(m):
        w = [0] * m; w[k] += A; w[(k + 1) % m] += B; rows.append(w)
if centre:
    rows.append([0] * m)
with open(out, 'w') as f:
    f.write('# m=%d C=%d n=%d layers=%d scale=2^%d  point = sum_j w_j zeta^j, zeta=e^(2 pi i/%d)\n'
            % (m, centre, len(rows), len(zs), S, m))
    for w in rows:
        f.write(' '.join(map(str, w)) + '\n')
print('wrote', out, len(rows), 'points')
