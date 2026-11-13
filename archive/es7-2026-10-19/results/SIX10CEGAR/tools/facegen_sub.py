#!/usr/bin/env python3
"""facegen_sub.py MODEL SDPDIR SPEC_OUT LAYERS : as facegen.py, for a lift computed on the layer subset LAYERS (sdp_ext.py --layers);
layers outside LAYERS become free singleton groups (their coordinates lie in the face). From facegen.py: read the degenerate optimal lift of sdp_ext.py (lift.npy) and propose an exact face:
groups of layers z_i = R^{k_i} w_g (R = rotation by 60 degrees) plus zero layers z_i = 0. Numerical (evidence only);
the face is only a hypothesis that the exact face certificate then verifies."""
import sys, json, numpy as np, importlib.util
from pathlib import Path
s = importlib.util.spec_from_file_location('se', str(Path(__file__).with_name('sdp_ext.py'))); se = importlib.util.module_from_spec(s); s.loader.exec_module(se)
model, sdpdir, out = sys.argv[1], Path(sys.argv[2]), sys.argv[3]; LS = [int(v) for v in sys.argv[4].split(',')]
raw, pos, vs, ix, entries, order = se.build(model, list(range(10)), False, False)
x = np.load(sdpdir / 'lift.npy'); n = 10
Dm = np.array([[x[ix['D', min(i, j), max(i, j)]] for j in LS] for i in LS])
Em = np.array([[0.0 if i == j else x[ix['E', min(i, j), max(i, j)]] * (1 if i < j else -1) for j in LS] for i in LS])
n = len(LS)
best = None
for c in (1.0, -1.0, 3 ** .5, -(3 ** .5), 1 / 3 ** .5, -1 / 3 ** .5):
    H = Dm + 1j * c * Em; H = (H + H.conj().T) / 2
    ev, U = np.linalg.eigh(H); keep = ev > 1e-6 * ev.max()
    U = U[:, keep] * np.sqrt(ev[keep]); r = U.shape[1]
    norms = np.linalg.norm(U, axis=1); scale = norms.max()
    zero = [i for i in range(n) if norms[i] < 1e-4 * scale]
    groups = []; assigned = set(zero); ok = True
    for i in range(n):
        if i in assigned: continue
        g = [(i, 0)]; assigned.add(i)
        for j in range(i + 1, n):
            if j in assigned: continue
            for k in range(6):
                w = np.exp(1j * np.pi / 3 * k)
                if np.linalg.norm(U[j] - w * U[i]) < 1e-4 * scale:
                    g.append((j, k)); assigned.add(j); break
        groups.append([(LS[a], k) for a, k in g])
    zero = [LS[a] for a in zero]
    if len(groups) >= r:
        groups += [[(i, 0)] for i in range(10) if i not in LS]   # the face spanned by the groups contains the range of the lift
        best = {'c': c, 'rank': r, 'groups': groups, 'zero': zero}; break
if best is None:
    print('no clean face'); sys.exit(1)
json.dump(best, open(out, 'w')); print(json.dumps(best))
