#!/usr/bin/env python3
"""Calibrate n2's in-memory sweep against results/D satcount on every deletion of a
33-point set: complete face count, H(S-i) (n2 DFS) vs cgon, lowest m level (n2 keeps
only faces with a verified integer point; satcount counts all faces, so n2's lowest
level must be >= satcount's and equal whenever satcount's level has a realizable face).
usage: calib_vs_satcount.py points.txt out.json"""
import sys, json, subprocess, tempfile, os
H = os.path.dirname(os.path.abspath(__file__))
D = os.path.join(H, '..', '..', 'D', 'bin')
pts, out = sys.argv[1], sys.argv[2]
P = [tuple(map(int, l.split())) for l in open(pts)]
# n2 rescales; pass a pre-rescaled copy so both tools see identical coordinates
mx = max(max(abs(x), abs(y)) for x, y in P); f = (1 << 28) // mx
if f >= 2: P = [(x * f, y * f) for x, y in P]
tmp = tempfile.mkdtemp()
fn = os.path.join(tmp, 'p.txt'); open(fn, 'w').write(''.join(f'{x} {y}\n' for x, y in P))
n2 = subprocess.run([os.path.join(H, '..', 'bin_n2'), 'calib', fn, '0', '1', os.path.join(tmp, 'c')], capture_output=True, text=True).stdout.split('\n')
rows, bad = [], 0
for i, l in enumerate([l for l in n2 if l.startswith('del')]):
    t = l.split()
    q = os.path.join(tmp, 'd.txt'); open(q, 'w').write(''.join(f'{x} {y}\n' for j, (x, y) in enumerate(P) if j != i))
    r = json.loads(subprocess.run([os.path.join(D, 'satcount'), 'sweep', q, '7', '-', '1', '3'], capture_output=True, text=True).stdout)
    cg = subprocess.run([os.path.join(D, 'cgon'), 'count', '8'], stdin=open(q), capture_output=True, text=True).stdout
    c7 = int(cg.split('c7=')[1].split()[0])
    sat_min = next(m for m in range(4) if m == 3 or r[['m0', 'm1', 'm2'][m]] > 0)
    row = dict(i=i, deg=int(t[3]), H_del_n2=int(t[5]), H_del_cgon=c7, faces_n2=int(t[9]), faces_satcount=r['faces_hit'],
               complete=r['complete'], minm_n2=int(t[11]), minm_satcount=sat_min, satcount_hist=[r['m0'], r['m1'], r['m2'], r['m3plus']])
    ok = row['H_del_n2'] == c7 and row['faces_n2'] == r['faces_hit'] and r['complete'] and row['minm_n2'] >= sat_min
    row['minm_equal'] = row['minm_n2'] == sat_min
    bad += not ok; rows.append(row)
json.dump(dict(points=pts, rows=rows, failures=bad, minm_equal=sum(r['minm_equal'] for r in rows)), open(out, 'w'), indent=1)
print('failures', bad, 'minm equal', sum(r['minm_equal'] for r in rows), 'of', len(rows))
