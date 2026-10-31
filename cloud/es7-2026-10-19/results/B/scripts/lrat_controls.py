#!/usr/bin/env python3
"""LRAT certificates for whole UNSAT control instances, plus a negative test of the checker.

For each instance: gen_etv.py CNF (+ x-reflection lex-leader if requested), solve with
`cadical --lrat=true --binary=false`, check with drat-trim's lrat-check, require "c VERIFIED".
Negative test: a proof for CNF+units of a cube must NOT verify against the CNF without the
units (lrat-check must not print "c VERIFIED").
usage: lrat_controls.py CACHE_DIR OUT.json
"""
import json, subprocess, sys, time
from pathlib import Path

HERE = Path(__file__).resolve().parent
TOOLS = HERE.parents[2] / "tools"
C = Path(sys.argv[1]).resolve()
W = C / "lratctl"; W.mkdir(exist_ok=True)
cad = str(C / "ext/cadical/build/cadical"); chk = str(C / "ext/drat-trim/lrat-check")
INST = [(6, 5, 5, 15, False), (6, 5, 5, 15, True), (7, 4, 7, 17, False), (7, 4, 7, 17, True),
        (7, 5, 5, 21, True), (6, 5, 6, 16, True)]


def verified(out):
    return any(l.strip() == "c VERIFIED" for l in out.splitlines())


rows = []
for k, a, u, N, sb in INST:
    cnf = W / f"k{k}a{a}u{u}N{N}{'_lexx' if sb else ''}.cnf"; prf = W / "p.lrat"
    subprocess.run([sys.executable, str(TOOLS / "etv/gen_etv.py"), str(N), str(a), str(u), str(k), "-o", str(cnf)], check=True, capture_output=True)
    if sb:
        subprocess.run([sys.executable, str(HERE / "lexx.py"), str(cnf), str(N), str(cnf)], check=True, capture_output=True)
    t = time.time(); r = subprocess.run([cad, "-q", "-n", "--lrat=true", "--binary=false", str(cnf), str(prf)]); ts = time.time() - t
    row = {"k": k, "a": a, "u": u, "N": N, "lexx": sb, "solve_rc": r.returncode, "solve_s": round(ts, 1)}
    if r.returncode == 20:
        row["proof_MB"] = round(prf.stat().st_size / 1e6, 1)
        t = time.time(); pc = subprocess.run([chk, str(cnf), str(prf)], capture_output=True, text=True)
        row["check_s"] = round(time.time() - t, 1); row["lrat"] = "VERIFIED" if verified(pc.stdout) else "FAILED"
    prf.unlink(missing_ok=True); cnf.unlink(missing_ok=True)
    print(json.dumps(row), flush=True); rows.append(row)
# negative tests on (6,5,5)@15: (i) the proof with its last 10% of lines removed (so the
# empty clause is gone) must not verify; (ii) the intact proof checked against a CNF with one
# clause deleted must not verify unless that clause is unused (we delete the first clause of
# the 4-point signotope block, which every refutation of this formula is expected to need,
# and report the outcome either way).
k, a, u, N = 6, 5, 5, 15
base = W / "neg_base.cnf"; prf = W / "neg.lrat"; trunc = W / "neg_trunc.lrat"; weak = W / "neg_weak.cnf"
subprocess.run([sys.executable, str(TOOLS / "etv/gen_etv.py"), str(N), str(a), str(u), str(k), "-o", str(base)], check=True, capture_output=True)
r = subprocess.run([cad, "-q", "-n", "--lrat=true", "--binary=false", str(base), str(prf)])
neg = {"negative_test_solve_rc": r.returncode}
if r.returncode == 20:
    pl = prf.read_text().splitlines()
    trunc.write_text("\n".join(pl[: int(len(pl) * 0.9)]) + "\n")
    bl = base.read_text().splitlines()
    h = bl[0].split()
    weak.write_text(f"p cnf {h[2]} {int(h[3]) - 1}\n" + "\n".join(bl[2:]) + "\n")
    good = subprocess.run([chk, str(base), str(prf)], capture_output=True, text=True)
    t1 = subprocess.run([chk, str(base), str(trunc)], capture_output=True, text=True)
    t2 = subprocess.run([chk, str(weak), str(prf)], capture_output=True, text=True)
    neg["intact_verified"] = verified(good.stdout)
    neg["truncated_verified"] = verified(t1.stdout)
    neg["clause_deleted_verified"] = verified(t2.stdout)
    neg["pass"] = neg["intact_verified"] and not neg["truncated_verified"]
for p in (base, prf, trunc, weak):
    p.unlink(missing_ok=True)
print(json.dumps(neg))
Path(sys.argv[2]).write_text(json.dumps({"instances": rows, "negative_test": neg,
                                         "all_verified": all(r.get("lrat") == "VERIFIED" for r in rows)}, indent=1))
