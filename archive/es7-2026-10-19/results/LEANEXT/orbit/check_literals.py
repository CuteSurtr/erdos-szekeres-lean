"""Check that the encoder's orbit literals agree with real orientations (evidence only, floats).

Usage: python3 -I check_literals.py <path to gen.py> m t seed [m t seed ...]

(1) sortpar's parity equals the sign of the sorting permutation (all 6 orders).
(2) For a random configuration of t nested regular m-gons (radius decreasing, theta_0 = 0,
    theta_i in (0, 2pi/m)), set V(C) = [orient(P(C)) > 0] for each canonical triple C and check that
    the literal Enc.o(a, b, c) evaluates to [orient(P a, P b, P c) > 0] for every ordered triple of
    distinct points.  Also check the hypothesis of the Lean model: P(rot(x, 1)) = rho(P(x)).
"""
import importlib.util, itertools, math, random, sys


def load(path):
    spec = importlib.util.spec_from_file_location("gen_under_test", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def orient(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def perm_sign(p):
    s = 1
    for i in range(len(p)):
        for j in range(i + 1, len(p)):
            if p[i] > p[j]:
                s = -s
    return s


def main():
    gen = load(sys.argv[1])
    for p in itertools.permutations(range(3)):
        srt, par = gen.Enc.sortpar(p)
        assert srt == (0, 1, 2) and par == perm_sign(p), (p, par)
    print("sortpar parity = permutation sign on all 6 orders: OK")
    args = sys.argv[2:]
    for q in range(0, len(args), 3):
        m, t, seed = int(args[q]), int(args[q + 1]), int(args[q + 2])
        rnd = random.Random(seed)
        radii = sorted((rnd.uniform(0.2, 1.0) for _ in range(t)), reverse=True)
        radii[0] = 1.0
        theta = [0.0] + [rnd.uniform(0.0, 2 * math.pi / m) for _ in range(t - 1)]
        P = [(radii[i] * math.cos(theta[i] + 2 * math.pi * k / m),
              radii[i] * math.sin(theta[i] + 2 * math.pi * k / m)) for i in range(t) for k in range(m)]
        e = gen.Enc(m, 8, t)
        n = m * t
        a = 2 * math.pi / m
        for x in range(n):
            y = P[e.rot(x, 1)]
            rx = (math.cos(a) * P[x][0] - math.sin(a) * P[x][1], math.sin(a) * P[x][0] + math.cos(a) * P[x][1])
            assert abs(y[0] - rx[0]) < 1e-12 and abs(y[1] - rx[1]) < 1e-12
        V = {}
        for C, v in e.tvar.items():
            V[v] = orient(P[C[0]], P[C[1]], P[C[2]]) > 0
        bad = 0
        cnt = 0
        mn = float("inf")
        for x, y, z in itertools.permutations(range(n), 3):
            o = orient(P[x], P[y], P[z])
            mn = min(mn, abs(o))
            lit = e.o(x, y, z)
            val = V[abs(lit)] if lit > 0 else not V[abs(lit)]
            cnt += 1
            if val != (o > 0):
                bad += 1
        print(f"m={m} t={t} seed={seed}: orbit vars={e.ntriplevars} ordered triples={cnt} "
              f"mismatches={bad} min|orient|={mn:.3e}")
        assert bad == 0


if __name__ == "__main__":
    main()
