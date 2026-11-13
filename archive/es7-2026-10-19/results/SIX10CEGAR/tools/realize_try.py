#!/usr/bin/env python3
"""realize_try.py MODEL SDPDIR [TRIES] : numerical realizability probe (evidence only).
Project the multi-scale SDP lift onto one complex seed per layer, z = U v for random v, and count the orbit signs
of the model that the configuration p_{6i+k} = w^k z_i gets wrong (w = exp(i pi/3)); then hill-climb on the seeds
in log-polar coordinates to reduce the count.  Mismatch 0 would be a candidate realization, to be re-checked exactly."""
import sys, json, numpy as np, importlib.util
from pathlib import Path
RES = Path('<review-results>')
s = importlib.util.spec_from_file_location('enc', RES / 'C7UPPER/gen.py'); G = importlib.util.module_from_spec(s); s.loader.exec_module(G)
s = importlib.util.spec_from_file_location('se', str(Path(__file__).with_name('sdp_ext.py'))); se = importlib.util.module_from_spec(s); s.loader.exec_module(se)
E = G.Enc(6, 8, 10)
model, sdpdir = sys.argv[1], Path(sys.argv[2]); tries = int(sys.argv[3]) if len(sys.argv) > 3 else 200
pos = set(json.loads(open(model).read()))
C = sorted(E.tvar, key=E.tvar.get); T = np.array(C); want = np.array([1 if E.tvar[c] in pos else -1 for c in C])
w = np.exp(1j * np.pi / 3)


def mism(z, ret=False):
    P = (z[T // 6] * w ** (T % 6))          # shape (ntrip, 3)
    a, b, c = P[:, 0], P[:, 1], P[:, 2]
    o = ((b - a) * np.conj(c - a)).imag * -1   # orient(a,b,c) = Im(conj(b-a)(c-a))
    bad = np.sign(o) != want
    return (int(bad.sum()), o) if ret else int(bad.sum())


raw, posx, vs, ix, entries, order = se.build(model, list(range(10)), False, False)
x = np.load(sdpdir / 'lift.npy'); n = 10
Dm = np.array([[x[ix['D', min(i, j), max(i, j)]] for j in range(n)] for i in range(n)])
Em = np.array([[0.0 if i == j else x[ix['E', min(i, j), max(i, j)]] * (1 if i < j else -1) for j in range(n)] for i in range(n)])
rng = np.random.default_rng(0); best = (10 ** 9, None)
for c in (1.0, -1.0):
    H = Dm + 1j * c * Em; H = (H + H.conj().T) / 2
    ev, U = np.linalg.eigh(H); keep = ev > 1e-14 * ev.max(); U = U[:, keep] * np.sqrt(ev[keep])
    for _ in range(tries):
        v = rng.normal(size=U.shape[1]) + 1j * rng.normal(size=U.shape[1])
        for zz in (U @ v, np.conj(U @ v)):
            m = mism(zz)
            if m < best[0]: best = (m, zz)
print('best random projection: %d of %d orbit signs wrong' % (best[0], len(C)), flush=True)
# hill climb in log-polar coordinates
z = best[1]; m = best[0]; rho = np.log(np.abs(z) + 1e-300); th = np.angle(z); step = 0.3
for it in range(6000):
    if m == 0: break
    i = rng.integers(10); r2, t2 = rho.copy(), th.copy()
    if rng.random() < 0.5: r2[i] += rng.normal() * step
    else: t2[i] += rng.normal() * step * 0.5
    z2 = np.exp(r2 + 1j * t2); m2 = mism(z2)
    if m2 <= m:
        rho, th, m = r2, t2, m2
    if it % 1000 == 999:
        step *= 0.7; print('iter', it + 1, 'wrong', m, flush=True)
z = np.exp(rho + 1j * th)
print('final wrong %d; radii' % m, np.round(np.abs(z) / np.abs(z).max(), 8).tolist())
np.save(Path(sdpdir).parent / ('realize_%s.npy' % Path(model).stem), z)
