#!/usr/bin/env python3
"""Exact (Fraction) tools for Task C, independent of mirann's integer arithmetic.

  exact_tools.py scan K <mirann2> <brute_kgon|-> < set      exact axis scan of a mirror set with no axis point
  exact_tools.py verify K <brute_kgon> < set                general position, mirror symmetry, convex K-gon
                                                            count by exhaustive enumeration (brute_kgon)
  exact_tools.py model N K <brute_kgon> model.txt [--hull]  abstract SAT model: signotope axioms, mirror
                                                            identities, no convex K-gon (brute force)
A "set" is whitespace-separated coordinates x1 y1 x2 y2 ... (integers or p/q rationals); a line
"tag n x1 y1 ..." as written by mirann (.best/.zero) is also accepted.
"""
import sys, os, itertools, subprocess, tempfile, json
from fractions import Fraction as F
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mirlib import orient, general_position


def read_set(text):
    tok = text.split()
    if tok and not tok[0].lstrip('-').replace('/', '').isdigit():
        n = int(tok[1]); tok = tok[2:2 + 2 * n]
    v = [F(t) for t in tok]
    return [(v[i], v[i + 1]) for i in range(0, len(v), 2)]


def is_mirror(P):
    S = set(P)
    return all((-x, y) in S for x, y in P)


def sig_lines(P):
    """orientation signs of the points in their given order (1-based i<j<k)."""
    out = []
    for i, j, k in itertools.combinations(range(len(P)), 3):
        o = orient(P[i], P[j], P[k]); assert o != 0
        out.append(f"{i+1} {j+1} {k+1} {1 if o > 0 else -1}")
    return out


def brute(bk, n, K, lines):
    with tempfile.NamedTemporaryFile("w", suffix=".sig", delete=False) as f:
        f.write("\n".join(lines) + "\n"); path = f.name
    r = subprocess.run([bk, str(n), str(K), path], capture_output=True, text=True, check=True)
    os.unlink(path)
    last = r.stdout.strip().split("\n")[-1]
    d = dict(t.split("=") for t in last.split() if "=" in t)
    return int(d["signotope_violations"]), int(d["convex_K_subsets"])


def scan(K, ot, bk, P):
    assert is_mirror(P) and general_position(P) and all(x != 0 for x, _ in P)
    n0 = len(P)
    ts = set()
    for a, b in itertools.combinations(P, 2):
        if a[0] != b[0]:
            ts.add((a[1] * b[0] - b[1] * a[0]) / (b[0] - a[0]))
    ts = sorted(ts)
    cands = [ts[0] - 1] + [(ts[i] + ts[i + 1]) / 2 for i in range(len(ts) - 1)] + [ts[-1] + 1]
    base = {}
    for i, j, k in itertools.combinations(range(n0), 3):
        base[(i, j, k)] = 1 if orient(P[i], P[j], P[k]) > 0 else -1
    tables = []
    for t in cands:
        Q = P + [(F(0), t)]
        order = sorted(range(n0 + 1), key=lambda i: (Q[i][1], Q[i][0]))
        rank = [0] * (n0 + 1)
        for r, i in enumerate(order): rank[i] = r
        s = []
        for i, j, k in itertools.combinations(range(n0 + 1), 3):
            if k == n0:
                o = orient(Q[i], Q[j], Q[k]); assert o != 0, "collinear candidate"
                s.append(1 if o > 0 else -1)
            else:
                s.append(base[(i, j, k)])
        tables.append(f"{n0 + 1} " + " ".join(map(str, rank)) + " " + " ".join(map(str, s)))
    r = subprocess.run([ot, "otcount", str(K)], input="\n".join(tables) + "\n", capture_output=True, text=True, check=True)
    counts = [int(dict(t.split("=") for t in ln.split()[1:-1])[f"c{K}"]) for ln in r.stdout.strip().split("\n")]
    assert len(counts) == len(cands)
    best = min(counts); bi = counts.index(best)
    res = {"n": n0, "intervals": len(cands), "min_axis_E": best, "zero_intervals": counts.count(0), "t_best": str(cands[bi])}
    if bk != "-":
        # independent recount of the best candidate by exhaustive enumeration
        Q = sorted(P + [(F(0), cands[bi])])
        res["brute_check_best"] = brute(bk, len(Q), K, sig_lines(Q))[1]
    return res


if __name__ == "__main__":
    mode = sys.argv[1]
    if mode == "scan":
        K, ot, bk = int(sys.argv[2]), sys.argv[3], sys.argv[4]
        for line in sys.stdin:
            if line.strip():
                print(json.dumps(scan(K, ot, bk, read_set(line))), flush=True)
    elif mode == "verify":
        K, bk = int(sys.argv[2]), sys.argv[3]
        for line in sys.stdin:
            if not line.strip(): continue
            P = read_set(line)
            Q = sorted(P)
            gp = general_position(P)
            viol, conv = brute(bk, len(Q), K, sig_lines(Q)) if gp else (None, None)
            print(json.dumps({"n": len(P), "general_position": gp, "mirror_symmetric": is_mirror(P),
                              "axis_points": sum(1 for x, _ in P if x == 0), f"convex_{K}gons": conv}), flush=True)
    elif mode == "model":
        N, K, bk, path = int(sys.argv[2]), int(sys.argv[3]), sys.argv[4], sys.argv[5]
        hull = "--hull" in sys.argv
        lits = [int(t) for t in open(path).read().split() if t != "0"]
        val = {abs(l): l > 0 for l in lits}
        idx = {t: n + 1 for n, t in enumerate(itertools.combinations(range(1, N + 1), 3))}
        X = {t: val[v] for t, v in idx.items()}
        lo = 2 if hull else 1; m = N + lo
        mir_bad = sum(1 for (i, j, k), v in X.items() if i >= lo and X[tuple(sorted((m - k, m - j, m - i)))] != v)
        hull_bad = sum(1 for (i, j, k), v in X.items() if hull and i == 1 and not v)
        lines = [f"{i} {j} {k} {1 if v else -1}" for (i, j, k), v in X.items()]
        viol, conv = brute(bk, N, K, lines)
        print(json.dumps({"N": N, "K": K, "hull": hull, "signotope_violations": viol, "mirror_violations": mir_bad,
                          "hull_unit_violations": hull_bad, f"convex_{K}gons": conv}))
