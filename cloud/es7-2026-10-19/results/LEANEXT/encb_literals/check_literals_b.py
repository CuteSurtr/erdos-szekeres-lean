"""Test encoder B's orbit literals (gen_b2.py: canon, perm_sign, olit) against real orientations.
Evidence only (float64 with a guard).

Usage: python3 -I check_literals_b.py <path to gen_b2.py> m t seed [m t seed ...]

The encoder's code is NOT reimplemented.  gen_b2.py calls main() at import time, so it is parsed with `ast`; the
statements of main() before `cls = []` (minus the two that read sys.argv) are executed in a fresh namespace with
m, K, t given.  This runs the encoder's own `canon`, `orb` construction, `perm_sign` and `olit` unchanged.

(1) Literal test.  For a random nested m-fold configuration (layer 0 outermost, radius 1, theta_0 = 0,
    theta_i in (0, 2pi/m), each layer strictly inside the previous polygon), point (i,k) = rotation of layer i's
    representative by 2pi k/m.  Set V(C) = [orient(points of C in canonical order) > 0] for each canonical triple C
    in orb, and check olit(P,Q,R) evaluated under V equals [orient(P,Q,R) > 0] for every ordered triple of distinct
    points.  Configurations whose min |orient| over all ordered triples is < 1e-9 are rejected and resampled.
(2) Extra clause test.  The statements of main() before `nchain = 0` (phase transitivity, exact angular clauses,
    nesting units) are executed too, and every clause produced there is evaluated under the real assignment
    V, Y'(i,j) = [psi_i < psi_j], Hb(i) = [theta_i < pi/m] (odd m), with psi_i = theta_i mod pi/m (odd m) or
    theta_i mod 2pi/m (even m).  Chain clauses (F variables) are not tested.
(3) Also, unconstrained m-fold configurations (random radii in any order, no nesting) for test (1) only.
(4) Exact check: canon(tri) is a sorted rotation of tri, is constant on Z_m-orbits, and len(orb) equals the number of
    Z_m-orbits of 3-subsets (computed independently as the minimum over all m rotations).
"""
import ast, builtins, hashlib, itertools, math, random, sys

GUARD = 1e-9


def orient(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def extract(path):
    src = open(path).read()
    tree = ast.parse(src)
    mains = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "main"]
    assert len(mains) == 1
    body = mains[0].body

    def stop_at(name):
        for idx, st in enumerate(body):
            if isinstance(st, ast.Assign) and any(isinstance(tg, ast.Name) and tg.id == name for tg in st.targets):
                return idx
        raise RuntimeError(name)

    def keep(st):
        seg = ast.get_source_segment(src, st)
        return "sys.argv" not in seg

    dropped = [ast.get_source_segment(src, st) for st in body[:stop_at("cls")] if not keep(st)]
    part1 = [st for st in body[:stop_at("cls")] if keep(st)]
    part2 = [st for st in body[:stop_at("nchain")] if keep(st)]
    segs = {}
    for st in part1:
        if isinstance(st, ast.FunctionDef) and st.name in ("canon", "perm_sign", "olit"):
            segs[st.name] = ast.get_source_segment(src, st)
    assert set(segs) == {"canon", "perm_sign", "olit"}
    c1 = compile(ast.Module(body=part1, type_ignores=[]), path + "#main[:cls]", "exec")
    c2 = compile(ast.Module(body=part2, type_ignores=[]), path + "#main[:nchain]", "exec")
    return src, segs, dropped, c1, c2


def run_encoder(code, m, t):
    ns = {"__builtins__": builtins, "itertools": itertools, "m": m, "K": 8, "t": t}
    exec(code, ns)
    return ns


def sample(m, t, rnd, nested):
    a = 2 * math.pi / m
    while True:
        theta = [0.0] + [rnd.uniform(0.0, a) for _ in range(t - 1)]
        if nested:
            radii = [1.0]
            ok = True
            for i in range(1, t):
                for _ in range(1000):
                    r = radii[-1] * rnd.uniform(0.55, 1.0)
                    p0 = (radii[-1] * math.cos(theta[i - 1]), radii[-1] * math.sin(theta[i - 1]))
                    p1 = (radii[-1] * math.cos(theta[i - 1] + a), radii[-1] * math.sin(theta[i - 1] + a))
                    if all(orient(p0, p1, (r * math.cos(theta[i] + a * k), r * math.sin(theta[i] + a * k))) > GUARD
                           for k in range(m)):
                        break
                else:
                    ok = False
                    break
                radii.append(r)
            if not ok:
                continue
        else:
            radii = [rnd.uniform(0.2, 1.0) for _ in range(t)]
        P = {(i, k): (radii[i] * math.cos(theta[i] + a * k), radii[i] * math.sin(theta[i] + a * k))
             for i in range(t) for k in range(m)}
        return theta, radii, P


def check(code1, code2, m, t, seed, nested):
    rnd = random.Random(seed)
    rejected = 0
    while True:
        theta, radii, P = sample(m, t, rnd, nested)
        pts = list(P)
        trip = {}
        mn = float("inf")
        for x, y, z in itertools.permutations(pts, 3):
            o = orient(P[x], P[y], P[z])
            trip[(x, y, z)] = o
            mn = min(mn, abs(o))
        if mn >= GUARD:
            break
        rejected += 1
    # symmetry hypothesis: P(i, k+1) = rho(P(i, k))
    a = 2 * math.pi / m
    for (i, k), p in P.items():
        q = P[(i, (k + 1) % m)]
        rp = (math.cos(a) * p[0] - math.sin(a) * p[1], math.sin(a) * p[0] + math.cos(a) * p[1])
        assert abs(q[0] - rp[0]) < 1e-12 and abs(q[1] - rp[1]) < 1e-12
    ns = run_encoder(code1, m, t)
    orb, olit = ns["orb"], ns["olit"]
    # orbit count (independent): distinct Z_m-orbits of 3-subsets; canon must be one value per orbit
    seen = {}
    canon_bad = 0
    for tri in itertools.combinations(sorted(P), 3):
        key = min(tuple(sorted((i, (k + s) % m) for (i, k) in tri)) for s in range(m))
        c = ns["canon"](list(tri))
        assert sorted(c) == list(c) and any(tuple(sorted((i, (k + s) % m) for (i, k) in tri)) == c
                                           for s in range(m))
        if seen.setdefault(key, c) != c:
            canon_bad += 1
    norbits = len(seen)
    V = {}
    for C, v in orb.items():
        assert len(C) == 3 and all(c in P for c in C)
        V[v] = orient(P[C[0]], P[C[1]], P[C[2]]) > 0
    bad = cnt = 0
    for (x, y, z), o in trip.items():
        lit = olit(x, y, z)
        val = V[abs(lit)] if lit > 0 else not V[abs(lit)]
        cnt += 1
        if val != (o > 0):
            bad += 1
    line = (f"{'nested' if nested else 'free  '} m={m} t={t} seed={seed}: rejected={rejected} orbit vars={len(orb)} Z_m-orbits={norbits} canon-not-invariant={canon_bad} "
            f"ordered triples={cnt} mismatches={bad} min|orient|={mn:.3e}")
    cbad = ncl = None
    if nested:
        try:
            ns2 = run_encoder(code2, m, t)
        except Exception as ex:
            print(line + f" | encoder clause section raised {type(ex).__name__}: {ex}", flush=True)
            return bad, cnt, mn, 0, int(canon_bad > 0 or norbits != len(orb)), 1
        assert ns2["orb"] == orb
        odd = m % 2 == 1
        cell = math.pi / m if odd else 2 * math.pi / m
        psi = [th % cell for th in theta]
        assert all(psi[i] > GUARD and abs(psi[i] - cell) > GUARD for i in range(1, t))
        A = dict(V)
        for (i, j), v in ns2["Yv"].items():
            assert abs(psi[i] - psi[j]) > GUARD
            A[v] = psi[i] < psi[j]
        for i, v in ns2["Hv"].items():
            assert abs(theta[i] - math.pi / m) > GUARD
            A[v] = theta[i] < math.pi / m
        cls = ns2["cls"]
        ncl = len(cls)
        cbad = 0
        for cl in cls:
            if not any((A[abs(l)] if l > 0 else not A[abs(l)]) for l in cl):
                cbad += 1
        line += f" | non-chain clauses={ncl} violated={cbad}"
    print(line, flush=True)
    return bad, cnt, mn, cbad, int(canon_bad > 0 or norbits != len(orb)), 0


def main():
    path = sys.argv[1]
    src, segs, dropped, c1, c2 = extract(path)
    print("gen_b2.py sha256", hashlib.sha256(src.encode()).hexdigest())
    print("dropped statements (read sys.argv):", dropped)
    for name in ("canon", "perm_sign", "olit"):
        print(f"extracted {name}: sha256(source) = {hashlib.sha256(segs[name].encode()).hexdigest()}")
    tot_bad = tot_cnt = tot_cbad = tot_canon = tot_raised = 0
    gmin = float("inf")
    args = sys.argv[2:]
    for q in range(0, len(args), 3):
        m, t, seed = int(args[q]), int(args[q + 1]), int(args[q + 2])
        for nested in (True, False):
            try:
                bad, cnt, mn, cbad, cb, rz = check(c1, c2, m, t, seed, nested)
            except Exception as ex:
                print(f"m={m} t={t} seed={seed} nested={nested}: literal section raised {type(ex).__name__}: {ex}",
                      flush=True)
                tot_raised += 1
                continue
            tot_canon += cb
            tot_raised += rz
            tot_bad += bad; tot_cnt += cnt; gmin = min(gmin, mn)
            if cbad is not None:
                tot_cbad += cbad
    print(f"TOTAL ordered triples={tot_cnt} mismatches={tot_bad} min|orient|={gmin:.3e} "
          f"violated non-chain clauses={tot_cbad} configs with canon/orbit-count failure={tot_canon} "
          f"runs where encoder code raised={tot_raised}")


if __name__ == "__main__":
    main()
