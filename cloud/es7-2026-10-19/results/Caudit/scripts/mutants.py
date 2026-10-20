#!/usr/bin/env python3
"""Which controls distinguish the real mirror encodings from plausible wrong ones?

usage: mutants.py <bundle_root> <hornchk> <workdir> <r33prefix> <d31prefix> <classical32 assume dir>
Builds patched copies of gen_etv.py / mirgen.py (one mutation each), regenerates the CNFs,
and runs, with independent code:
  S:  the results/C solver controls (pysat Glucose4, not CaDiCaL): m8k5 SAT; m9k5, hm9k5,
      m9k5.sub, m17k6, hm17k6, m17k6.sub, hm17k6.sub UNSAT (time-capped);
  P32: classical mirror 32-point set (0 axis points) SAT in m32k7 and m32k7.sub;
  R33: 500 random interior + 500 hull-vertex 33-point sets: no violated orientation clause;
  SMALL: small-n equivalence (N=7 k=5, N=9 k=6, N=11 k=7; 600 sets each): no free set UNSAT;
  D31: the 15 heptagon-free 31-point sets with one axis point are SAT in their sub-case CNF.
A control "catches" a mutant if its expected outcome fails.
"""
import sys, os, subprocess, json, math, time, re
root, hk, wd, r33, d31, cl = sys.argv[1:7]
os.makedirs(wd, exist_ok=True)
G0 = open(f"{root}/tools/etv/gen_etv.py").read(); M0 = open(f"{root}/results/C/scripts/mirgen.py").read()
MUT = {
 "none": ([], []),
 "M1_sign_rule_negated": ([("cl.append([-v, w]); cl.append([v, -w])", "cl.append([v, w]); cl.append([-v, -w])")],
                          [("    rep[v] = min(v, w)", "    rep[v] = v if v <= w else -w")]),
 "M3_hull_pairing_unshifted": ([("lo = 2 if a.hull else 1; m = N + lo", "lo = 2 if a.hull else 1; m = N + 1")],
                               [("lo = 2 if a.hull else 1; m = N + lo", "lo = 2 if a.hull else 1; m = N + 1")]),
 "M4_interior_wrong_axis_label": ([], [("c = (N + 1) // 2\n", "c = (N + 1) // 2 + 1\n")]),
 "M5_interior_only_chords_from_1": ([], [("for i in range(1, c) for k in range(c + 1, N + 1)", "for i in range(1, 2) for k in range(c + 1, N + 1)")]),
 "M6_yflip_unit_in_hull_case": ([], [("    assert not a.hull\n    extra.append((sub(idx[(1, 2, 3)]),))", "    extra.append((sub(idx[(2, 3, 4)] if a.hull else idx[(1, 2, 3)]),))")]),
 "M7_hull_units_negated": ([("cl.append([X[(1, i, j)]])", "cl.append([-X[(1, i, j)]])")], []),
 "M8_gon_length_off_by_one": ([("s = K + 2 - r", "s = K + 1 - r")], []),
}
def patch(src, reps):
    for a, b in reps:
        assert src.count(a) == 1, a
        src = src.replace(a, b)
    return src
from pysat.formula import CNF
from pysat.solvers import Glucose4
def solve(path, tl=900):
    f = CNF(from_file=path); s = Glucose4(bootstrap_with=f.clauses)
    import threading
    t = threading.Timer(tl, s.interrupt); t.start()
    r = s.solve_limited(expect_interrupt=True); t.cancel(); s.delete()
    return {True: "SAT", False: "UNSAT", None: "TIMEOUT"}[r]
def hcheck(cnf, nX, lines):
    r = subprocess.run([hk, cnf, str(nX)], input=lines, capture_output=True, text=True, check=True)
    return [l for l in r.stdout.split("\n") if l.strip()]
def ok(l): return " xviol=0 " in l and " forbviol=0 " in l
def xok(l): return " xviol=0 " in l
head = lambda p, n: "".join(open(p).readlines()[:n])
res = {}
for name, (gp, mp) in MUT.items():
    d = f"{wd}/{name}"; os.makedirs(d, exist_ok=True)
    open(f"{d}/gen_etv.py", "w").write(patch(G0, gp)); open(f"{d}/mirgen.py", "w").write(patch(M0, mp))
    G, MG = f"{d}/gen_etv.py", f"{d}/mirgen.py"
    def gen(out, *args): subprocess.run(["python3", G, *map(str, args), "-o", f"{d}/{out}"], check=True, capture_output=True)
    def mg(inp, N, out, *opt): subprocess.run(["python3", MG, f"{d}/{inp}", str(N), *opt, "-o", f"{d}/{out}"], check=True, capture_output=True)
    for N, k in [(8, 5), (9, 5), (17, 6), (32, 7), (33, 7), (31, 7)]:
        gen(f"m{N}k{k}.cnf", N, k, k, k, "--mirror")
        if N % 2: gen(f"hm{N}k{k}.cnf", N, k, k, k, "--mirror", "--hull")
    mg("m9k5.cnf", 9, "m9k5.sub.cnf"); mg("m17k6.cnf", 17, "m17k6.sub.cnf"); mg("hm17k6.cnf", 17, "hm17k6.sub.cnf", "--hull")
    mg("m32k7.cnf", 32, "m32k7.sub.cnf")
    for N in (31, 33):
        mg(f"m{N}k7.cnf", N, f"m{N}k7int.sub.cnf", "--interior", "--yflip-unit")
        mg(f"hm{N}k7.cnf", N, f"hm{N}k7.sub.cnf", "--hull", *(["--yflip-unit"] if name.startswith("M6") else []))
    r = {}
    t0 = time.time()
    exp = {"m8k5": "SAT", "m9k5": "UNSAT", "hm9k5": "UNSAT", "m9k5.sub": "UNSAT", "m17k6": "UNSAT", "hm17k6": "UNSAT", "m17k6.sub": "UNSAT", "hm17k6.sub": "UNSAT"}
    S = {c: solve(f"{d}/{c}.cnf") for c in exp}
    r["S_solver_controls"] = {"pass": all(S[c] == exp[c] for c in exp), "got": S}
    a = open(f"{cl}/m32k7_assume.txt").read().split(); bits = "".join("1" if int(x) > 0 else "0" for x in sorted(a, key=lambda x: abs(int(x))))
    p32 = [ok(hcheck(f"{d}/{c}.cnf", 4960, f"c32 {bits}\n")[0]) for c in ("m32k7", "m32k7.sub")]
    r["P32_classical_SAT"] = {"pass": all(p32)}
    li = head(f"{r33}.ii.txt", 500); lv = head(f"{r33}.i.txt", 500)
    a1 = sum(xok(l) for l in hcheck(f"{d}/m33k7int.sub.cnf", 5456, li)); a2 = sum(xok(l) for l in hcheck(f"{d}/hm33k7.sub.cnf", 5456, lv))
    a3 = sum(xok(l) for l in hcheck(f"{d}/m33k7.cnf", 5456, li)); a4 = sum(xok(l) for l in hcheck(f"{d}/hm33k7.cnf", 5456, lv))
    r["R33_random_orientation_clauses"] = {"pass": a1 == a2 == a3 == a4 == 500, "int.sub": a1, "h.sub": a2, "m": a3, "hm": a4}
    sm = []
    env = dict(os.environ, GEN_ETV=G, MIRGEN=MG)
    for N, k in [(7, 5), (9, 6), (11, 7)]:
        o = subprocess.run(["python3", f"{root}/results/Caudit/scripts/small.py", root, hk, f"{d}/small", str(N), str(k), "600", str(N * 100 + k + 7)], env=env, capture_output=True, text=True, check=True).stdout
        j = json.loads(o); sm.append({kk: v["unsound(free but UNSAT)"] for kk, v in j.items() if isinstance(v, dict)} | {"N": N, "k": k})
    r["SMALL_equivalence"] = {"pass": all(v == 0 for s in sm for kk, v in s.items() if kk not in ("N", "k")), "detail": sm}
    # reference: heptagon-freeness decided by the unmutated plain m31k7.cnf (base clauses proved in results/H)
    xs = {l.split()[0]: l for l in hcheck(f"{wd}/none/m31k7.cnf", 4495, open(f"{d31}.xs.txt").read())}
    free = {i for i, l in xs.items() if ok(l)}
    fi = [l for l in open(f"{d31}.ii.txt") if l.split()[0] in free]; fv = [l for l in open(f"{d31}.i.txt") if l.split()[0] in free]
    b1 = sum(ok(l) for l in hcheck(f"{d}/m31k7int.sub.cnf", 4495, "".join(fi))); b2 = sum(ok(l) for l in hcheck(f"{d}/hm31k7.sub.cnf", 4495, "".join(fv)))
    r["D31_heptagon_free_31_SAT"] = {"pass": b1 == len(fi) and b2 == len(fv), "int.sub": f"{b1}/{len(fi)}", "h.sub": f"{b2}/{len(fv)}"}
    r["time_s"] = round(time.time() - t0)
    res[name] = r
    print(name, json.dumps(r), flush=True)
json.dump(res, open(f"{wd}/mutants.json", "w"), indent=1)
