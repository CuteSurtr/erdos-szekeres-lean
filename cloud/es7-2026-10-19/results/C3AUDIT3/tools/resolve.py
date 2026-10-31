"""re-solve cube nodes at m = 11 with my own CNF (mycompose.units): CaDiCaL --sat --lrat --binary=false,
lrat-check (E2) + cake_lpr; print cnf_sha256 / verdict next to the record's.
usage: resolve.py BASE CAP OUT.jsonl NAME=SHA [...]"""
import json, os, subprocess, sys, time, concurrent.futures as cf
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mycompose as Y, mydriver as D
from c3cnf import C3Enc
base, cap, out = sys.argv[1], sys.argv[2], sys.argv[3]
W = "/opt/work/resolve"; os.makedirs(W, exist_ok=True)

def one(arg):
    name, want = arg.split("=")
    kk = Y.parse(name)
    us = Y.units(11, C3Enc(11, 7), *kk)
    cnf, prf = f"{W}/{name}.cnf", f"{W}/{name}.lrat"
    with open(base) as f, open(cnf, "w") as g:
        h = f.readline().split(); g.write(f"p cnf {h[2]} {int(h[3]) + len(us)}\n")
        while True:
            b = f.read(1 << 24)
            if not b: break
            g.write(b)
        g.write("".join(f"{u} 0\n" for u in us))
    rec = {"node": name, "units": len(us), "cnf_sha256": Y.fsha(cnf), "record_sha256": want}
    rec["sha_equal"] = rec["cnf_sha256"] == want
    t = time.time()
    r = subprocess.run(["/opt/bin/cadical", "-q", "-t", cap, "--sat", "--lrat", "--binary=false", cnf, prf], capture_output=True, text=True).stdout
    rec["status"] = next((l[2:] for l in r.splitlines() if l.startswith("s ")), "UNKNOWN"); rec["solve_s"] = round(time.time() - t, 1)
    if rec["status"] == "UNSATISFIABLE":
        rec["proof_bytes"] = os.path.getsize(prf); rec["proof_sha256"] = Y.fsha(prf)
        t = time.time(); a, b, ok = D.dual(cnf, prf)
        rec.update({"lrat_check": a, "cake_lpr": b, "certified": ok, "check_s": round(time.time() - t, 1)})
    for x in (cnf, prf):
        if os.path.exists(x): os.remove(x)
    return rec

with cf.ProcessPoolExecutor(2) as ex, open(out, "a") as fo:
    for rec in ex.map(one, sys.argv[4:]):
        fo.write(json.dumps(rec) + "\n"); fo.flush(); print(json.dumps(rec), flush=True)
