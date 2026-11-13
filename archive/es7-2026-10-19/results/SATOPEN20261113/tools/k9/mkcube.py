#!/usr/bin/env python3
r"""Write cube unit files for the k=9, 8-fold, t=16 formula BASE0.cnf (= certified S14 base without window units).
Variables: Y(i,j) = [psi_i < psi_j], 1 <= i < j <= 15, from cnf/A_m8K9t16.cnf.json; Z_i = 497697 + i = [psi_i < 22.5 deg].
usage:
  mkcube.py ex J R OUTDIR      LIS family: psi increasing on {1..15}\{J} (91 Y units) + Z decision-list cube R
                               (R = 0..13: Z_{s_1..s_R} true, Z_{s_{R+1}} false; R = 14: all 14 true; R = -1: no Z units)
                               where s_1 < ... < s_14 lists {1..15}\{J}.
  mkcube.py perm SEED MODE OUTDIR   random phases (seeded): MODE=DZ: 14 consecutive Y units + 15 Z units;
                               MODE=YZ: all 105 Y units + 15 Z units
"""
import json, os, random, sys
J = json.load(open('/home/jay/research/data/lb-k9oct-20261111/cnf/A_m8K9t16.cnf.json'))
assert J['nv'] == 497697
Yv = {tuple(map(int, k.split(','))): v for k, v in J['Y'].items()}
assert len(Yv) == 105 and all(1 <= i < j <= 15 for i, j in Yv)
def Y(i, j):              # literal for psi_i < psi_j
    return Yv[i, j] if i < j else -Yv[j, i]
def Z(i): return 497697 + i
def write(out, lits, desc):
    os.makedirs(out, exist_ok=True)
    assert len(set(abs(l) for l in lits)) == len(lits)
    with open(os.path.join(out, 'cube.units'), 'w') as f:
        for l in lits: f.write('%d 0\n' % l)
    with open(os.path.join(out, 'cube.desc'), 'w') as f: f.write(desc + '\n')
kind = sys.argv[1]
if kind == 'ex':
    j, r, out = int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
    s = [i for i in range(1, 16) if i != j]
    lits = [Y(a, b) for a in s for b in s if a < b]
    assert len(lits) == 91
    if r >= 0:
        lits += [Z(s[k]) for k in range(r)]
        if r < 14: lits.append(-Z(s[r]))
    write(out, lits, 'ex j=%d r=%d: psi increasing on layers %s; Z decision-list cube r' % (j, r, s))
elif kind == 'ex2':
    # two displaced layers J < K: psi increasing on {1..15} minus {J, K} (78 Y units), no Z units
    j, k, out = int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
    s = [i for i in range(1, 16) if i not in (j, k)]
    lits = [Y(a, b) for a in s for b in s if a < b]
    assert len(lits) == 78
    write(out, lits, 'ex2 j=%d k=%d: psi increasing on layers %s' % (j, k, s))
elif kind == 'cycx':
    # layer 0 and layer K displaced: the 14 layers s = {1..15}-{K} in cyclic spiral order cut at layer 0 after
    # position P: psi_{s_{P+1}} < ... < psi_{s_14} < psi_{s_1} < ... < psi_{s_P}; psi_K free (91 Y units)
    k, P, out = int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
    sl = [i for i in range(1, 16) if i != k]
    order = sl[P:] + sl[:P]; rank = {x: r for r, x in enumerate(order)}
    lits = [Y(a, b) if rank[a] < rank[b] else -Y(a, b) for a in sl for b in sl if a < b]
    assert len(lits) == 91
    write(out, lits, 'cycx k=%d P=%d: order (by phase) of the other 14 layers %s, layer %d free' % (k, P, order, k))
elif kind == 'cyc':
    # cyclic spiral of layers 1..15 cut at layer 0: psi_{p+1} < ... < psi_15 < psi_1 < ... < psi_p (all 105 Y units)
    p, out = int(sys.argv[2]), sys.argv[3]
    rank = {i: (i - p if i > p else i + 15 - p) for i in range(1, 16)}   # position in increasing phase order
    assert sorted(rank.values()) == list(range(1, 16))
    lits = [Y(a, b) if rank[a] < rank[b] else -Y(a, b) for a in range(1, 16) for b in range(a + 1, 16)]
    order = sorted(range(1, 16), key=lambda i: rank[i])
    write(out, lits, 'cyc p=%d: full order (by phase) %s' % (p, order))
elif kind == 'perm':
    seed, mode, out = int(sys.argv[2]), sys.argv[3], sys.argv[4]
    rng = random.Random(seed)
    psi = [None] + [rng.uniform(0, 45) for _ in range(15)]
    lits = []
    if mode in ('DZ', 'D'): lits = [Y(i, i + 1) if psi[i] < psi[i + 1] else -Y(i, i + 1) for i in range(1, 15)]
    if mode in ('YZ', 'Y'): lits = [Y(i, j) if psi[i] < psi[j] else -Y(i, j) for i in range(1, 16) for j in range(i + 1, 16)]
    if mode.startswith('B'):      # band: B<w>Z = Y(i,j) for 1 <= j-i <= w, plus Z
        w = int(mode[1:].rstrip('Z'))
        lits = [Y(i, j) if psi[i] < psi[j] else -Y(i, j) for i in range(1, 16) for j in range(i + 1, min(i + w, 15) + 1)]
    if mode in ('DZ', 'YZ', 'Z') or (mode.startswith('B') and mode.endswith('Z')): lits += [Z(i) if psi[i] < 22.5 else -Z(i) for i in range(1, 16)]
    order = sorted(range(1, 16), key=lambda i: psi[i])
    write(out, lits, 'perm seed=%d mode=%s order(by phase)=%s Z=%s' % (seed, mode, order, ''.join('1' if psi[i] < 22.5 else '0' for i in range(1, 16))))
else:
    sys.exit('unknown kind')
