"""Independent exact check of the one-leaf (W1) certificate (standard library only)."""
import gzip, json, sys
cat = json.load(gzip.open('/home/jay/research/lean/erdos-szekeres-lean/experiments/omission-residual32-rank-global-2026-10-10/source-2650.json.gz'))
S, C = cat['states'], cat['constraints']
F = [i for i, s in enumerate(S) if s[0] >= 5]
assert len(F) == 84 and len(C) == 2650
cert = json.load(open(sys.argv[1] if len(sys.argv) > 1 else 'w1_leaf_certificate.json'))
w = {int(k): v for k, v in cert['weights_times6'].items()}
rows = {k: (C[k]['support'], C[k]['rhs']) if k < 2650 else (F, 28) for k in w}
load = [0] * 154; D = 0
for k, wt in w.items():
    sup, rhs = rows[k]; D += wt * rhs
    for i in sup: load[i] += wt
Cmult = 6
assert all(load[i] <= Cmult for i in range(1, 154)), 'load exceeds C'
# For any 0/1 h with h_0 = 0 satisfying the rows: D <= sum_i load_i h_i <= C * sum_{i>=1} h_i
print('rows', len(w), 'D', D, 'max load (i>=1)', max(load[1:]), '=> sum h >=', -(-D // Cmult), '; budget 33 excluded:', Cmult * 33 < D)
