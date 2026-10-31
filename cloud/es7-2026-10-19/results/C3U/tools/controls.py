#!/usr/bin/env python3
"""C3-S controls and C3a/C3b agreement on the per-case CNFs.
usage: controls.py OUT.jsonl WORKDIR MK [MK ...]     MK = m,k[,cert]   (cert: dual-check UNSAT proofs)
For every case of (m, k), both encodings: CaDiCaL answer; with cert, each UNSAT is proved with
--lrat and accepted only if lrat-check (E2 patch) AND cake_lpr accept."""
import hashlib
import json
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from hullcase import cases, case_name  # noqa: E402

CAD, LRAT, CAKE = "cadical", "lrat-check", "cake_lpr"
CAP = int(os.environ.get("C3S_CAP", "600"))


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def dual(cnf, prf):
    a = subprocess.run([LRAT, cnf, prf], capture_output=True, text=True).stdout
    a = next((l for l in a.splitlines() if l.startswith("c VERIFIED") or l.startswith("c NOT VERIFIED")), "none")
    env = dict(os.environ, CML_HEAP_SIZE="12000", CML_STACK_SIZE="2000")
    b = subprocess.run([CAKE, cnf, prf], capture_output=True, text=True, env=env).stdout.strip().splitlines()
    b = b[0] if b else "none"
    return a, b, a == "c VERIFIED" and b == "s VERIFIED UNSAT"


def main():
    out, work = sys.argv[1], sys.argv[2]
    os.makedirs(work, exist_ok=True)
    with open(out, "a") as fo:
        for mk in sys.argv[3:]:
            p = mk.split(",")
            m, k, cert = int(p[0]), int(p[1]), len(p) > 2
            for c in ["none"] + [case_name(x) for x in cases(m, k)]:
                rec = {"m": m, "k": k, "case": c}
                for enc in ("c3a", "c3b"):
                    cnf = os.path.join(work, f"{enc}_m{m}k{k}_{c}.cnf")
                    subprocess.run([sys.executable, os.path.join(HERE, "gen_case.py"), str(m), str(k), c, "-o", cnf, "--enc", enc],
                                   check=True, capture_output=True)
                    t = time.time()
                    prf = cnf + ".lrat"
                    args = [CAD, "-q", "-t", str(CAP), cnf] + (["--lrat", "--binary=false", prf] if cert and enc == "c3a" else [])
                    r = subprocess.run(args, capture_output=True, text=True).stdout
                    st = next((l[2:] for l in r.splitlines() if l.startswith("s ")), "UNKNOWN")
                    rec[enc] = {"status": st, "s": round(time.time() - t, 2), "sha256": sha(cnf)}
                    if cert and enc == "c3a" and st == "UNSATISFIABLE":
                        a, b, ok = dual(cnf, prf)
                        rec[enc].update({"lrat_check": a, "cake_lpr": b, "certified": ok})
                    for x in (cnf, prf):
                        if os.path.exists(x):
                            os.remove(x)
                rec["agree"] = rec["c3a"]["status"] == rec["c3b"]["status"]
                fo.write(json.dumps(rec) + "\n")
                fo.flush()
                print(json.dumps(rec), flush=True)


if __name__ == "__main__":
    main()
