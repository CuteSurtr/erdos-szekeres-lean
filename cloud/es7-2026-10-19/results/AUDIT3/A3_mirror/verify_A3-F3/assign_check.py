#!/usr/bin/env python3
"""A3-F3 (a), (e), and item 1 with axis points: exact check that the satisfying assignment the written proof leaves
implicit really works on the CNF zcnf.py writes.

For random exact integer mirror configurations in the normal form (axis = y-axis, left point of pair o is element 2o,
pairs by strictly decreasing height, two axis points upper first), in general position (checked exactly):
  E1  the zero triples among all triples of the N points and Z are exactly {Z, L_i, R_i}          (item 1 / (e))
  E2  every union-find class is sign-consistent: chi(T) * sg(T) is the same for all T in the class, so
      X_class := chi(root) is well defined and lit(T) = chi(T) for every nonzero triple                 ((a))
  E3  with X as in E2 and every conv variable set to the TRUE convexity of its point set (independent monotone-chain
      hull test), every clause holds except the K-set clauses of point sets that really are in convex position, and
      each convex canonical K-set falsifies exactly its own clause                                         ((a))
Also: a deliberately wrong fast-path GP clause (sign of l24 flipped in the first family) must be caught by E3.

usage: assign_check.py [n_configs_per_instance] [seed]"""
import importlib.util, itertools, os, random, sys

V = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(V, "zcnf_copy.py")


def load(name, subs):
    src = open(SRC).read()
    for old, new in subs:
        assert src.count(old) == 1, (name, old)
        src = src.replace(old, new)
    path = os.path.join(V, f"variant_{name}.py")
    open(path, "w").write(src)
    spec = importlib.util.spec_from_file_location(f"variant_{name}", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    os.remove(path)
    return mod


def det3(a, b, c):
    return (a[0] * (b[1] * c[2] - b[2] * c[1]) - a[1] * (b[0] * c[2] - b[2] * c[0])
            + a[2] * (b[0] * c[1] - b[1] * c[0]))


def sgn(x):
    return (x > 0) - (x < 0)


def cross(o, a, b):
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def convex_position(pts):
    """monotone chain; True iff every point is a strict hull vertex (general position assumed and checked)"""
    P = sorted(pts)
    lower, upper = [], []
    for p in P:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    for p in reversed(P):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    return len(lower) + len(upper) - 2 == len(P)


def random_config(t, axis, rng, R):
    while True:
        b = rng.sample(range(-R, R + 1), t + axis)
        hb = sorted(b[:t], reverse=True)              # pair heights, decreasing (normal form)
        c = sorted(b[t:], reverse=True)               # axis heights, upper first; all heights distinct
        a = [rng.randint(1, R) for _ in range(t)]
        pts = []
        for o in range(t):
            pts.append((-a[o], hb[o]))
            pts.append((a[o], hb[o]))
        for cj in c:
            pts.append((0, cj))
        if all(cross(p, q, r) != 0 for p, q, r in itertools.combinations(pts, 3)):
            return pts


def run_instance(mod, t, K, axis, nconf, rng, tag, verbose=True):
    body = os.path.join(V, f"tmp_assign_{tag}_{t}_{K}_{axis}.body")
    enc = mod.ZEncoding("mirror", t, K, body=body, axis=axis)
    enc.build(sb=True, hull=False)
    enc.sink.f.close()
    clauses = [list(map(int, line.split()[:-1])) for line in open(body)]
    os.remove(body)
    N, Z, P = enc.N, enc.Z, enc.P
    conv_of = {v: S for S, v in enc.conv.items()}
    # the K-set clause of each canonical K-set, rebuilt exactly as the encoder words it (the (K-1)-subsets are replaced
    # by their canonical representatives, which need not be subsets of S)
    Kset_of_clause = {}
    for S in itertools.combinations(range(N), K):
        if enc.canon(S) == S:
            key = frozenset(-enc.conv[enc.canon(S[:i] + S[i + 1:])] for i in range(K))
            Kset_of_clause.setdefault(key, []).append(S)
    stats = dict(configs=0, e1_bad=0, e2_bad=0, e3_unexplained=0, e3_missing=0, convex_K=0)
    for _ in range(nconf):
        pts = random_config(t, axis, rng, 40)
        vec = [(1, x, y) for x, y in pts] + [(0, 1, 0)]
        chi = {}
        for T in itertools.combinations(range(P), 3):
            chi[T] = sgn(det3(*(vec[i] for i in T)))
        # E1
        for T, s in chi.items():
            expected_zero = (Z in T and (lambda u: u[0] < enc.NP and u[1] < enc.NP and u[0] // 2 == u[1] // 2)(
                [i for i in T if i != Z]))
            if (s == 0) != expected_zero:
                stats["e1_bad"] += 1
        # E2
        X = {}
        for T, (v, sg) in enc.tv.items():
            val = chi[T] * sg
            if val == 0 or X.setdefault(v, val) != val:
                stats["e2_bad"] += 1
        # E3
        assign = {v: (X[v] == 1) for v in X}
        for v, S in conv_of.items():
            assign[v] = convex_position([pts[i] for i in S])
        convex_canon_K = set()
        for S in itertools.combinations(range(N), K):
            if enc.canon(S) == S and convex_position([pts[i] for i in S]):
                convex_canon_K.add(S)
        explained = set()
        for cl in clauses:
            if any(assign[abs(l)] == (l > 0) for l in cl):
                continue
            owners = [S for S in Kset_of_clause.get(frozenset(cl), []) if S in convex_canon_K]
            if owners:
                explained.update(owners)
            else:
                stats["e3_unexplained"] += 1
        stats["e3_missing"] += len(convex_canon_K - explained)
        stats["convex_K"] += len(convex_canon_K)
        stats["configs"] += 1
    if verbose:
        print(f"[{tag}] mirror t={t} K={K} axis={axis} clauses={len(clauses)}: {stats}")
    return stats


def main():
    nconf = int(sys.argv[1]) if len(sys.argv) > 1 else 30
    seed = int(sys.argv[2]) if len(sys.argv) > 2 else 20261101
    rng = random.Random(seed)
    orig = load("orig_assign", [])
    allok = True
    for t, K, axis in ((4, 5, 0), (4, 5, 1), (4, 5, 2), (5, 6, 0), (5, 6, 1), (5, 6, 2), (6, 7, 0), (6, 7, 1),
                       (6, 6, 2), (7, 7, 1)):
        st = run_instance(orig, t, K, axis, nconf, rng, "orig")
        allok &= st["e1_bad"] == 0 and st["e2_bad"] == 0 and st["e3_unexplained"] == 0 and st["e3_missing"] == 0
    # sensitivity: a wrong fast-path clause must be caught
    bad = load("fastmut", [("self.sink.add([-s1 * l12, -s1 * l34, -s2 * l13, s2 * l24, -s3 * l14, -s3 * l23])",
                            "self.sink.add([-s1 * l12, -s1 * l34, -s2 * l13, -s2 * l24, -s3 * l14, -s3 * l23])")])
    caught = 0
    for t, K, axis in ((5, 6, 1), (6, 7, 0)):
        st = run_instance(bad, t, K, axis, 10, rng, "fast-path mutant")
        caught += st["e3_unexplained"] > 0
    allok &= caught == 2
    print("RESULT", "PASS" if allok else "FAIL")


if __name__ == "__main__":
    main()
