"""Mutation tests for zcnf.py rot (m = 2) at small sizes.

Each mutant is a copy of the original encoder (zcnf_orig.py, sha256 13d6c162...) with one deliberate defect, applied as
exact text replacements (each old string must occur exactly once).  For each mutant and each instance (t, K, flags):
  1. generate the CNF with the mutant (generation may fail: the encoder's own contradiction check);
  2. map check against the hand-derived classes (classes.check_map);
  3. spec comparison family by family (spec.py) -- detects missing/extra/changed families;
  4. real-configuration evaluation: for real centrally symmetric sets with no convex K-gon, labelled in the normal form
     from every hull vertex, the real assignment (triple variables from point-only triples, conv = actual convexity)
     is evaluated clause by clause with evalcnf; the original must give 0 violated clauses;
  5. two-way SAT test (CaDiCaL): CNF + the real values of all point-only triples as units must be SAT for the
     original; UNSAT shows that the mutant excludes a real configuration (unsound);
  6. free solve of the known-UNSAT instance t = 9, K = 6 (18 points; ES(6) = 17) for the weakening mutants, with an
     independent axiom check of the model found.
"""
import itertools
import json
import os
import random
import shutil
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import classes  # noqa: E402
import geom     # noqa: E402
import spec     # noqa: E402

CADICAL = os.environ.get("CADICAL", "cadical")   # CaDiCaL 3.0.1 binary (path or name on the PATH)
ORIG = os.path.join(HERE, "zcnf_orig.py")

MUTANTS = {
    "original": ("control: the unmodified encoder", []),
    "identity_sign": ("centre identity with the wrong sign: chi(c,p,q) = -chi(-p,p,q)",
                      [("""                sp = 1
                base = (tp, p)            # chi(Z,p,q) = chi(tau p, p, q)""",
                        """                sp = -1
                base = (tp, p)            # chi(Z,p,q) = chi(tau p, p, q)""")]),
    "zero_missing": ("no zero triples: {c,p,-p} treated as a nonzero triple",
                     [("""        if self.Z not in T:
            return False
        a, b = [x for x in T if x != self.Z]
        return a < self.NP and b < self.NP and self.tau(a) == b""",
                       """        return False""")]),
    "zero_extra": ("extra zero triples {c,(0,0),(1,0)} and {c,(0,1),(1,1)} (identity loop skips zero triples)",
                   [("""        a, b = [x for x in T if x != self.Z]
        return a < self.NP and b < self.NP and self.tau(a) == b""",
                     """        a, b = sorted(x for x in T if x != self.Z)
        if (a, b) in ((0, 2), (1, 3)):
            return True
        return a < self.NP and b < self.NP and self.tau(a) == b"""),
                    ("""                if q in (p, tp):
                    continue""",
                     """                if q in (p, tp) or self.is_zero((Z, p, q)):
                    continue""")]),
    "angular_cycle": ("angular order made cyclic: chi(c,(1,0),(3,0)) = - while (1,0) < (2,0) < (3,0)",
                      [("""                for o2 in range(o + 1, t):
                    u.append(self.lit(Z, self.pt(o, 0), self.pt(o2, 0)))
        else:""",
                        """                for o2 in range(o + 1, t):
                    u.append((-1 if (o, o2) == (1, 3) else 1) * self.lit(Z, self.pt(o, 0), self.pt(o2, 0)))
        else:""")]),
    "hull_anchor": ("hull-vertex clauses anchored at (1,0) instead of (0,0)",
                    [("""        q = self.pt(0, 0)
        cnt = 0""", """        q = self.pt(1, 0)
        cnt = 0""")]),
    "a4_missing": ("interiority (A4) family not emitted",
                   [("""    def add_a4(self):
        cnt = 0""", """    def add_a4(self):
        self.stats["a4_4sets"] = 0
        return
        cnt = 0""")]),
    "a4_sign": ("interiority clause with the wrong sign on chi(p,q,r) (forbids t inside pqr)",
                [("""                    cl = [-s * self.lit(t, q, r), -s * self.lit(p, t, r), -s * self.lit(p, q, t), s * self.lit(p, q, r)]""",
                  """                    cl = [-s * self.lit(t, q, r), -s * self.lit(p, t, r), -s * self.lit(p, q, t), -s * self.lit(p, q, r)]""")]),
    "gp_sign": ("Grassmann-Pluecker with the middle coefficient +1",
                [("""((y[0], y[2]), (y[1], y[3]), -1)""", """((y[0], y[2]), (y[1], y[3]), 1)""")]),
    "gp_missing": ("Grassmann-Pluecker family not emitted",
                   [("""    def add_gp(self):
        cnt = 0""", """    def add_gp(self):
        self.stats["gp_5sets"] = 0
        return
        cnt = 0""")]),
    "group_sign": ("half-turn treated as orientation-reversing on point triples (det -1)",
                   [("""            self.gen = [self.rot(i) for i in range(self.P)]
            self.gsign = (1, 1)""", """            self.gen = [self.rot(i) for i in range(self.P)]
            self.gsign = (-1, 1)""")]),
    "k_off_by_one": ("forbids convex (K-1)-gons instead of K-gons",
                     [("""    def add_kgon(self):
        K = self.K""", """    def add_kgon(self):
        K = self.K - 1""")]),
    "conv4_pattern": ("a non-convex 4-point pattern (+,+,-,+) counted as convex",
                      [("""        if n_in == 0:
            convex.append(pat)
    assert len(convex) == 6""", """        if n_in == 0 or pat == (1, 1, -1, 1):
            convex.append(pat)
    assert len(convex) == 7""")]),
}

WEAKENING = {"a4_missing", "gp_missing"}


def make_mutant(name, outdir):
    src = open(ORIG).read()
    for old, new in MUTANTS[name][1]:
        assert src.count(old) == 1, (name, old[:60], src.count(old))
        src = src.replace(old, new)
    d = os.path.join(outdir, name)
    os.makedirs(d, exist_ok=True)
    p = os.path.join(d, "zcnf_mut.py")
    with open(p, "w") as f:
        f.write(src)
    return p


def generate(mod, t, K, flags, out):
    cmd = [sys.executable, "-I", mod, "rot", str(t), str(K), "--m", "2"] + flags + ["-o", out + ".cnf",
                                                                                  "--map", out + ".json"]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        last = (r.stderr.strip().splitlines() or ["?"])[-1]
        return False, last
    return True, ""


def assignment_for(info, X):
    """real assignment through the CNF's own map: each triple variable from a point-only triple of its class (if any);
    returns (bytearray, identities_consistent, zero_pattern_ok, conv levels)"""
    N, K, V, XV = info["N"], info["K"], info["vars"], info["X_vars"]
    tv = {(a, b, c): (v, s) for a, b, c, v, s in info["triples"]}
    byv = {}
    for T, (v, s) in tv.items():
        byv.setdefault(v, []).append((T, s))
    zero_ok = all((T in tv) == (geom.orient(X[T[0]], X[T[1]], X[T[2]]) != 0)
                  for T in itertools.combinations(range(N + 1), 3))
    val = bytearray(V + 1)
    consistent = True
    for v, lst in byv.items():
        vals = []
        for T, s in lst:
            o = geom.sgn(geom.orient(X[T[0]], X[T[1]], X[T[2]]))
            vals.append((N not in T, o * s))
        if len({x for _, x in vals}) != 1:
            consistent = False
        pts = [x for isp, x in vals if isp and x != 0] or [x for _, x in vals if x != 0] or [1]
        val[v] = 1 if pts[0] > 0 else 255
    # conv variables: numbering of the mutant's own add_kgon is the documented one, with its K
    Kc = info["Kc"]
    sets = classes.conv_numbering(N, Kc, XV)
    assert XV + len(sets) == V, ("conv numbering", XV + len(sets), V)
    for i, Q in enumerate(sets):
        val[XV + 1 + i] = 1 if geom.in_convex_position([X[j] for j in Q]) else 255
    return val, consistent, zero_ok


def evaluate(cnf, vals, workdir):
    files = []
    for i, v in enumerate(vals):
        fn = os.path.join(workdir, f"asg{i}.bin")
        with open(fn, "wb") as f:
            f.write(bytes(v))
        files.append(fn)
    pref = os.path.join(workdir, "ev")
    r = subprocess.run([os.path.join(HERE, "evalcnf"), cnf, pref] + files, capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    viol = []
    for i in range(len(vals)):
        with open(f"{pref}.{i}.viol") as f:
            viol.append([list(map(int, line.split()))[1:-1] for line in f])
        os.remove(f"{pref}.{i}.viol")
    for fn in files:
        os.remove(fn)
    return viol


def sat_with_units(cnf, units, workdir):
    """CNF + unit clauses -> 'SAT' / 'UNSAT' (CaDiCaL, small instances only)"""
    p = os.path.join(workdir, "units.cnf")
    with open(cnf) as f, open(p, "w") as g:
        for line in f:
            if line.startswith("p cnf"):
                _, _, nv, nc = line.split()
                g.write(f"p cnf {nv} {int(nc) + len(units)}\n")
            else:
                g.write(line)
        for u in units:
            g.write(f"{u} 0\n")
    r = subprocess.run([CADICAL, "-q", "-t", "120", p], capture_output=True, text=True)
    os.remove(p)
    return {10: "SAT", 20: "UNSAT"}.get(r.returncode, f"UNKNOWN({r.returncode})"), r.stdout


def classify(clause, info):
    XV = info["X_vars"]
    if len(clause) == 1:
        return "unit"
    if all(abs(l) <= XV for l in clause):
        return f"triple-only/{len(clause)}"
    if any(l > XV for l in clause):
        return "conv-definition"
    return "kgon"


def configs_for(t, K, rng, n=6):
    out = []
    tries = 0
    while len(out) < n and tries < 20000:
        tries += 1
        sh = rng.choice(["box", "radial", "ring", "nearline"])
        P = geom.random_central(t, rng, box=10 ** 5, shape=sh)
        if geom.max_convex_bruteforce(P, cap=K) < K:
            out.append(P)
    assert len(out) == n
    return out


def model_axiom_check(info, model_lits):
    """independent check of a SAT model: decode the chirotope of all triples and test interiority (A4) on every
    4-element set without zero triple and the 3-term GP relation on every 5-set; returns counts of violations"""
    N, Z = info["N"], info["Z"]
    tv = {(a, b, c): (v, s) for a, b, c, v, s in info["triples"]}
    pos = {abs(l): (l > 0) for l in model_lits}

    def chi(a, b, c):
        T = (a, b, c)
        S = tuple(sorted(T))
        if S not in tv:
            return 0
        v, s = tv[S]
        x = 1 if pos.get(v, False) else -1
        return classes.perm_sign(T) * s * x
    a4_bad = 0
    for S in itertools.combinations(range(N + 1), 4):
        if any(chi(*T) == 0 for T in itertools.combinations(S, 3)):
            continue
        for tt in S:
            p, q, r = [x for x in S if x != tt]
            v = (chi(tt, q, r), chi(p, tt, r), chi(p, q, tt))
            if v[0] == v[1] == v[2] == -chi(p, q, r):
                a4_bad += 1
    gp_bad = 0
    for F in itertools.combinations(range(N + 1), 5):
        for x in F:
            a, b, c, d = [y for y in F if y != x]
            terms = [chi(x, a, b) * chi(x, c, d), -chi(x, a, c) * chi(x, b, d), chi(x, a, d) * chi(x, b, c)]
            nz = [u for u in terms if u != 0]
            if nz and not (1 in nz and -1 in nz):
                gp_bad += 1
    return a4_bad, gp_bad


def main():
    outdir = os.path.join(HERE, "mut")
    rng = random.Random(20261101)
    instances = [(4, 5, ["--hull"]), (5, 6, ["--hull"]), (6, 6, ["--hull"]), (5, 6, ["--no-sb"]), (8, 7, ["--hull"])]
    R = os.path.join(HERE, "..", "..")   # cloud/es7-2026-10-19/results
    sym32 = geom.read_points(os.path.join(R, "SYM2", "sym7_32points.txt"))
    # configurations without a convex K-gon
    cfgs = {}
    for t, K, _ in instances:
        if (t, K) in cfgs:
            continue
        if (t, K) == (8, 7):
            S32 = set(sym32)
            pairs = sorted({tuple(sorted((p, (-p[0], -p[1])))) for p in sym32})
            assert len(pairs) == 16 and all(q in S32 for pr in pairs for q in pr)
            lst = []
            while len(lst) < 4:
                sel = rng.sample(pairs, 8)
                lst.append([x for pr in sel for x in pr])
            cfgs[(t, K)] = lst
        else:
            cfgs[(t, K)] = configs_for(t, K, rng)
        for P in cfgs[(t, K)]:
            assert geom.general_position(P) and geom.max_convex_bruteforce(P, cap=K) < K
    summary = {}
    log = []

    def say(s):
        print(s, flush=True)
        log.append(s)
    names = [n for n in MUTANTS if not sys.argv[1:] or n in sys.argv[1:]]
    for name in names:
        mod = make_mutant(name, outdir)
        say(f"=== {name}: {MUTANTS[name][0]}")
        res = {}
        for t, K, flags in instances:
            tag = f"t{t}k{K}{''.join(flags).replace('--', '_')}"
            base = os.path.join(outdir, name, tag)
            ok, err = generate(mod, t, K, flags, base)
            if not ok:
                say(f"  {tag}: GENERATION FAILED (caught by the encoder's own check): {err}")
                res[tag] = {"generation": "failed", "error": err}
                continue
            info = json.load(open(base + ".json"))
            info["Kc"] = K - 1 if name == "k_off_by_one" else K
            mapok, msgs, _ = classes.check_map(info)
            # spec comparison
            r = subprocess.run([sys.executable, "-I", os.path.join(HERE, "spec.py"), base + ".cnf", base + ".json"]
                               + [f for f in flags if f in ("--hull", "--no-sb")], capture_output=True, text=True)
            spec_line = [l for l in r.stdout.splitlines() if "SPEC COMPARISON" in l or "map check failed" in l]
            spec_out = (spec_line[-1] if spec_line else (r.stdout + r.stderr).strip().splitlines()[-1])
            differ = [l.split()[0] for l in r.stdout.splitlines() if "DIFFER" in l]
            # real configurations
            vals, meta = [], []
            for ci, P in enumerate(cfgs[(t, K)]):
                H = geom.hull_vertices(P)
                for p0 in H:
                    X = geom.normal_form(P, (0, 0), p0)
                    v, cons, zok = assignment_for(info, X)
                    vals.append(v)
                    meta.append((ci, p0, cons, zok, X))
            viol = evaluate(base + ".cnf", vals, os.path.join(outdir, name))
            nbad = sum(1 for vv in viol if vv)
            kinds = {}
            for vv in viol:
                for cl in vv:
                    k = classify(cl, info)
                    kinds[k] = kinds.get(k, 0) + 1
            incons = sum(1 for m in meta if not m[2])
            zbad = sum(1 for m in meta if not m[3])
            # two-way SAT test on the first labelling of each configuration
            sat = []
            done_cfg = set()
            tv = {(a, b, c): (vv_, s) for a, b, c, vv_, s in info["triples"]}
            for (ci, p0, cons, zok, X) in meta:
                if ci in done_cfg:
                    continue
                done_cfg.add(ci)
                units = set()
                for T, (var, s) in tv.items():
                    if info["N"] in T:
                        continue
                    o = geom.sgn(geom.orient(X[T[0]], X[T[1]], X[T[2]]))
                    units.add(var if o * s > 0 else -var)
                st, _ = sat_with_units(base + ".cnf", sorted(units, key=abs), os.path.join(outdir, name))
                sat.append(st)
            res[tag] = {"map_check": mapok, "spec": spec_out, "spec_differ": differ, "labellings": len(vals),
                        "labellings_with_violations": nbad, "violations_by_kind": kinds,
                        "identity_inconsistent_labellings": incons, "zero_pattern_bad_labellings": zbad,
                        "two_way": sat}
            say(f"  {tag}: map_check={'ok' if mapok else 'MISMATCH'}; spec: "
                f"{'PASS' if 'PASSED' in spec_out else 'FAIL ' + str(differ or spec_out)}; "
                f"real labellings {len(vals)}, with violated clauses {nbad} {kinds if kinds else ''}; "
                f"identity-inconsistent {incons}; zero-pattern-mismatch {zbad}; two-way SAT tests {sat}")
        # free solve of a known-UNSAT instance for weakening mutants (and the original)
        if name in WEAKENING or name == "original":
            base = os.path.join(outdir, name, "t9k6_free")
            ok, err = generate(mod, 9, 6, [], base)
            if ok:
                info = json.load(open(base + ".json"))
                r = subprocess.run([CADICAL, "-t", "600", base + ".cnf"], capture_output=True, text=True)
                st = {10: "SAT", 20: "UNSAT"}.get(r.returncode, f"UNKNOWN({r.returncode})")
                extra = ""
                if st == "SAT":
                    lits = [int(x) for line in r.stdout.splitlines() if line.startswith("v ")
                            for x in line.split()[1:] if x != "0"]
                    a4b, gpb = model_axiom_check(info, lits)
                    extra = f"; model violates interiority on {a4b} (4-set, t) instances and GP on {gpb} (5-set, x) instances"
                res["t9k6_free"] = st + extra
                say(f"  t9k6 free solve (18 points, no convex hexagon; ES(6) = 17 so no real set): {st}{extra}")
        summary[name] = res
    suffix = "" if not sys.argv[1:] else "_" + "_".join(sys.argv[1:])
    with open(os.path.join(outdir, f"summary{suffix}.json"), "w") as f:
        json.dump(summary, f, indent=1)
    with open(os.path.join(HERE, "logs", f"mutation{suffix}.log"), "w") as f:
        f.write("\n".join(log) + "\n")


if __name__ == "__main__":
    main()
