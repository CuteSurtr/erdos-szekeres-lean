#!/usr/bin/env python3
"""Evaluate EVERY clause of an sgn.py CNF on a real labelled configuration, with auxiliary variables set by their
documented (intended) meaning, computed independently from the coordinates.

Variable layout reconstructed from the creation order in sgn.py (o-vars from the map; then, with --rs, y_i for
i=3..n/2 and the counter R[j,c]; then U[k,a,j,l], EU[k,a,b]; without --sym also V, EC). The layout is checked against
the header's variable count; a wrong layout would show up as mass clause failures.
"""
import itertools, json, os, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rv import det, cross, orient_table, exact_cups

HERE = os.path.dirname(os.path.abspath(__file__))
SGN = os.path.join(HERE, "..", "sgn", "sgn.py")
CAD = os.path.join(HERE, "..", "local", "bin", "cadical")
WORK = os.path.join(HERE, "work")


def build(n, K, sym=True, par=False, centre=False, rs=False, mirror=None, hexk=None, tag=""):
    name = f"f_{n}_{K}_{int(sym)}{int(par)}{int(centre)}{int(rs)}" + (f"_m{'-'.join(map(str, mirror))}" if mirror else "") \
        + (f"_h{hexk}" if hexk else "") + tag
    f = os.path.join(WORK, name + ".cnf"); mp = f + ".json"
    if not os.path.exists(f) or not os.path.exists(mp):
        cmd = [sys.executable, SGN, str(n), str(K), "-o", f, "--map", mp]
        if sym: cmd.append("--sym")
        if par: cmd.append("--par")
        if centre: cmd.append("--centre")
        if rs: cmd.append("--rs")
        if mirror: cmd += ["--mirror"] + [str(x) for x in mirror]
        if hexk: cmd += ["--hexk", str(hexk)]
        r = subprocess.run(cmd, capture_output=True, text=True, check=True)
        open(f + ".stats", "w").write(r.stdout)
    return Formula(f, mp, n, K, sym, par, centre, rs, mirror, hexk)


class Formula:
    def __init__(s, f, mp, n, K, sym, par, centre, rs, mirror, hexk):
        s.path, s.n, s.K, s.sym, s.par, s.centre, s.rs, s.mirror, s.hexk = f, n, K, sym, par, centre, rs, mirror, hexk
        s.clauses = []
        with open(f) as fh:
            for line in fh:
                if line[0] == 'c':
                    continue
                if line[0] == 'p':
                    _, _, nv, nc = line.split(); s.nv, s.nc = int(nv), int(nc); continue
                lits = [int(x) for x in line.split()]
                assert lits[-1] == 0
                s.clauses.append(tuple(lits[:-1]))
        assert len(s.clauses) == s.nc
        m = json.load(open(mp))
        s.ov = {(i, j, k): v for i, j, k, v in m["triples"]}
        s.no = m["o_vars"]
        # my own canonical form check: every sorted triple t has exactly one of t / mirror(t) in the map (sym)
        for t in itertools.combinations(range(1, n + 1), 3):
            mt = (n + 1 - t[2], n + 1 - t[1], n + 1 - t[0])
            if sym:
                assert (t in s.ov) != (mt in s.ov) or t == mt, t
            else:
                assert t in s.ov
        assert sorted(s.ov.values()) == list(range(1, s.no + 1))
        s.layout()

    def layout(s):
        n, K = s.n, s.K
        mean = {}
        nxt = s.no + 1
        if s.rs:
            mm = n // 2 - 2; need = (mm + 1) // 2
            s.need = need
            for i in range(3, n // 2 + 1):
                mean[nxt] = ('y', i); nxt += 1
            for j in range(mm):
                for c in range(1, need + 1):
                    mean[nxt] = ('R', j, c); nxt += 1
        for k in range(3, K + 1):
            for a, j, l in itertools.combinations(range(1, n + 1), 3):
                if j - a >= k - 2:
                    mean[nxt] = ('U', k, a, j, l); nxt += 1
        for k in range(3, K + 1):
            for a, b in itertools.combinations(range(1, n + 1), 2):
                if b - a >= k - 1:
                    mean[nxt] = ('EU', k, a, b); nxt += 1
        if not s.sym:
            for k in range(3, K + 1):
                for a, j, l in itertools.combinations(range(1, n + 1), 3):
                    if j - a >= k - 2:
                        mean[nxt] = ('V', k, a, j, l); nxt += 1
            for k in range(3, K + 1):
                for a, b in itertools.combinations(range(1, n + 1), 2):
                    if b - a >= k - 1:
                        mean[nxt] = ('EC', k, a, b); nxt += 1
        assert nxt - 1 == s.nv, (nxt - 1, s.nv)
        s.mean = mean

    def assignment(s, S):
        """intended values of every variable for labelled configuration S (S[i-1] = p_i)."""
        n, K = s.n, s.K
        assert len(S) == n
        o = orient_table(S)
        val = [None] * (s.nv + 1)
        for t, v in s.ov.items():
            val[v] = o[t]
        cup = exact_cups(o, n, K)
        cap = exact_cups({t: not b for t, b in o.items()}, n, K)
        ys = {}
        if s.rs:
            V1, V2 = S[n - 2], S[n - 1]
            for i in range(3, n // 2 + 1):
                q = S[i - 1]
                ys[i] = (cross(V1, q) > 0) == (cross(q, V2) > 0)    # c = origin; geometric sector test
        ylist = [ys[i] for i in range(3, n // 2 + 1)] if s.rs else []
        EUv = {}
        for v, mn in s.mean.items():
            typ = mn[0]
            if typ == 'y':
                val[v] = ys[mn[1]]
            elif typ == 'R':
                _, j, c = mn; val[v] = sum(ylist[:j + 1]) >= c
            elif typ == 'U':
                val[v] = bool(cup.get(mn[1:]))
            elif typ == 'V':
                val[v] = bool(cap.get(mn[1:]))
            elif typ == 'EU':
                _, k, a, b = mn; val[v] = any(cup.get((k, a, j, b)) for j in range(a + 1, b))
            elif typ == 'EC':
                _, k, a, b = mn; val[v] = any(cap.get((k, a, j, b)) for j in range(a + 1, b))
        assert all(x is not None for x in val[1:])
        return val, o, cup, cap

    def evaluate(s, S):
        val, o, cup, cap = s.assignment(S)
        bad = []
        for c in s.clauses:
            if not any(val[l] if l > 0 else not val[-l] for l in c):
                bad.append(c)
        return bad, val

    def describe(s, lit):
        v = abs(lit); sg = '' if lit > 0 else '-'
        if v <= s.no:
            t = [t for t, x in s.ov.items() if x == v][0]
            return f"{sg}o{t}"
        return f"{sg}{s.mean[v]}"


def cadical_with_units(F, units, extra=()):
    g = F.path + ".units.cnf"
    with open(g, "w") as h:
        h.write(f"p cnf {F.nv} {len(F.clauses) + len(units) + len(extra)}\n")
        for c in F.clauses:
            h.write(" ".join(map(str, c)) + " 0\n")
        for u in units:
            h.write(f"{u} 0\n")
        for c in extra:
            h.write(" ".join(map(str, c)) + " 0\n")
    r = subprocess.run([CAD, "-q", g], capture_output=True, text=True)
    os.remove(g)
    assert r.returncode in (10, 20), r.stdout[-300:]
    return r.returncode == 10
