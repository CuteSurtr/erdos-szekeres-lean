"""Referee's independent evaluator for zcnf.py rot --m 2 [--hull] at small sizes.

Shares no code with ../../tests (own geometry, own labelling, own convexity test, own clause parser, own
expected-violation derivation).  For each real centrally symmetric configuration (exact integers) and each chosen first
point, it labels the set in the normal form, computes the real assignment through the encoder's map, evaluates every
clause, and compares the violated clauses (as literal multisets) with an expectation derived from geometry alone:
  * the KGON clause {-conv(canon(Q - x)) : x in Q} of every canonical K-set Q in convex position;
  * if the first point is not a hull vertex: the HULL clause of each triangle of other points containing it.
usage: refeval.py ENCODER.py t K [--hull] [--seed S] [--ncfg N] [--keep]
Exit status 0 iff every labelling gives exactly the expected violated clauses and every class is consistent.
"""
import itertools
import json
import os
import random
import subprocess
import sys
import tempfile


def cross(o, a, b):
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def sg(x):
    return 1 if x > 0 else (-1 if x < 0 else 0)


def strictly_inside(q, a, b, d):
    s = (sg(cross(a, b, q)), sg(cross(b, d, q)), sg(cross(d, a, q)))
    return s[0] != 0 and s[0] == s[1] == s[2]


def convex_position(Q):
    for i, q in enumerate(Q):
        others = Q[:i] + Q[i + 1:]
        for a, b, d in itertools.combinations(others, 3):
            if strictly_inside(q, a, b, d):
                return False
    return True


def is_hull_vertex(P, p):
    others = [q for q in P if q != p]
    return not any(strictly_inside(p, a, b, d) for a, b, d in itertools.combinations(others, 3))


def gen_config(t, rng, mode):
    """t antipodal pairs about c = (0, 0) (or a random integer centre), general position, exact integers"""
    while True:
        c = (0, 0) if mode != "offc" else (rng.randint(-9, 9), rng.randint(-9, 9))
        P = []
        for _ in range(t):
            if mode == "small":
                q = (rng.randint(-12, 12), rng.randint(-12, 12))
            else:
                q = (rng.randint(-10 ** 4, 10 ** 4), rng.randint(-10 ** 4, 10 ** 4))
            q = (q[0] + c[0], q[1] + c[1])
            P += [q, (2 * c[0] - q[0], 2 * c[1] - q[1])]
        if len(set(P)) != len(P) or c in P:
            continue
        if any(cross(a, b, d) == 0 for a, b, d in itertools.combinations(P, 3)):
            continue
        return P, c


def label(P, c, p0):
    """normal form: X0 = p0, X1 = h(p0); representatives strictly left of c -> p0, sorted counter-clockwise; X[2t] = c"""
    h = lambda q: (2 * c[0] - q[0], 2 * c[1] - q[1])
    reps = [q for q in P if q not in (p0, h(p0)) and cross(c, p0, q) > 0]
    assert len(reps) == len(P) // 2 - 1
    # selection sort with the angular comparator, then verify all pairs
    order = []
    rest = list(reps)
    while rest:
        first = [r for r in rest if all(r == s or cross(c, r, s) > 0 for s in rest)]
        assert len(first) == 1
        order.append(first[0])
        rest.remove(first[0])
    X = [p0, h(p0)]
    for r in order:
        X += [r, h(r)]
    X.append(c)
    for i in range(1, len(order) + 1):
        assert cross(c, X[0], X[2 * i]) > 0
        for j in range(i + 1, len(order) + 1):
            assert cross(c, X[2 * i], X[2 * j]) > 0
    return X


def main():
    enc, t, K = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
    hull = "--hull" in sys.argv
    seed = int(sys.argv[sys.argv.index("--seed") + 1]) if "--seed" in sys.argv else 1
    ncfg = int(sys.argv[sys.argv.index("--ncfg") + 1]) if "--ncfg" in sys.argv else 4
    rng = random.Random(seed)
    tmp = tempfile.mkdtemp(prefix="refeval_", dir=os.path.dirname(os.path.abspath(__file__)))
    cnf, mp = os.path.join(tmp, "f.cnf"), os.path.join(tmp, "f.json")
    r = subprocess.run([sys.executable, "-I", enc, "rot", str(t), str(K), "--m", "2"] + (["--hull"] if hull else [])
                       + ["-o", cnf, "--map", mp], capture_output=True, text=True)
    if r.returncode != 0:
        print(f"GENERATION FAILED: {(r.stderr.strip().splitlines() or ['?'])[-1]}")
        sys.exit(2)
    info = json.load(open(mp))
    N, Z, XV, V = info["N"], info["Z"], info["X_vars"], info["vars"]
    assert N == 2 * t and Z == N
    tv = {(a, b, d): (v, s) for a, b, d, v, s in info["triples"]}
    # conv numbering as documented: r = 4..K-1, lexicographic, canonical = S <= sorted(h S)
    h = lambda i: i ^ 1
    canon = lambda S: min(tuple(S), tuple(sorted(h(x) for x in S)))
    convsets = [S for r_ in range(4, K) for S in itertools.combinations(range(N), r_) if canon(S) == S]
    convvar = {S: XV + 1 + i for i, S in enumerate(convsets)}
    assert XV + len(convsets) == V, (XV, len(convsets), V)
    clauses = []
    with open(cnf) as f:
        for line in f:
            if line[0] in "cp":
                continue
            x = list(map(int, line.split()))
            assert x[-1] == 0 and 0 not in x[:-1]
            clauses.append(x[:-1])
    assert len(clauses) == info["clauses"]
    sign_of_perm = lambda T: (-1) ** sum(1 for i in range(3) for j in range(i + 1, 3) if T[i] > T[j])

    def lit_of(a, b, d):
        S = tuple(sorted((a, b, d)))
        v, s = tv[S]
        return sign_of_perm((a, b, d)) * s * v

    allok = True
    nlab = 0
    for ci in range(ncfg):
        P, c = gen_config(t, rng, ["small", "big", "offc", "big"][ci % 4])
        H = [p for p in P if is_hull_vertex(P, p)]
        inner = [p for p in P if p not in H]
        control = hull and "--nocontrol" not in sys.argv
        firsts = [(p, True) for p in H] + ([(inner[0], False)] if inner and control else [])
        for p0, onhull in firsts:
            nlab += 1
            X = label(P, c, p0)
            val = [0] * (V + 1)
            consistent = True
            for (a, b, d), (v, s) in tv.items():
                o = sg(cross(X[a], X[b], X[d]))
                if o == 0:
                    consistent = False
                x = o * s
                if val[v] == 0:
                    val[v] = x
                elif val[v] != x:
                    consistent = False
            zeros = {T for T in itertools.combinations(range(N + 1), 3) if cross(X[T[0]], X[T[1]], X[T[2]]) == 0}
            zero_ok = zeros == set(itertools.combinations(range(N + 1), 3)) - set(tv)
            for S in convsets:
                val[convvar[S]] = 1 if convex_position([X[i] for i in S]) else -1
            assert all(val[v] != 0 for v in range(1, V + 1))
            viol = sorted(tuple(sorted(set(cl))) for cl in clauses
                          if not any((l > 0 and val[l] == 1) or (l < 0 and val[-l] == -1) for l in cl))
            exp = []
            for Q in itertools.combinations(range(N), K):
                if canon(Q) == Q and convex_position([X[i] for i in Q]):
                    exp.append(tuple(sorted({-convvar[canon(Q[:i] + Q[i + 1:])] for i in range(K)})))
            if hull and not onhull:
                for a, b, d in itertools.combinations(range(1, N), 3):
                    if strictly_inside(X[0], X[a], X[b], X[d]):
                        s = sg(cross(X[a], X[b], X[0]))
                        exp.append(tuple(sorted({-s * lit_of(a, b, 0), -s * lit_of(b, d, 0), -s * lit_of(d, a, 0)})))
            exp.sort()
            ok = consistent and zero_ok and viol == exp
            allok &= ok
            if not ok:
                extra = len([x for x in viol if x not in set(exp)])
                missing = len([x for x in exp if x not in set(viol)])
                print(f"  cfg{ci} p0={p0} hull={onhull}: consistent={consistent} zero_ok={zero_ok} "
                      f"violated={len(viol)} expected={len(exp)} unexpected={extra} missing={missing}")
    print(f"refeval {os.path.basename(os.path.dirname(os.path.abspath(enc)))} t={t} K={K} hull={hull} seed={seed}: "
          f"{len(clauses)} clauses, {nlab} labellings -> {'PASS' if allok else 'FAIL'}")
    if "--keep" not in sys.argv:
        for fn in os.listdir(tmp):
            os.remove(os.path.join(tmp, fn))
        os.rmdir(tmp)
    sys.exit(0 if allok else 1)


if __name__ == "__main__":
    main()
