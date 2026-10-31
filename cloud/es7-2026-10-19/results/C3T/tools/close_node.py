#!/usr/bin/env python3
"""Close layer-tree nodes with checked proofs.
Node CNF = BASE (gen_case.py 11 7 none, C3a chain) + the node's layer units (hullcase.layer_clauses)
appended as unit clauses; CaDiCaL --lrat (ASCII); counts as closed only if lrat-check (E2 patch)
AND cake_lpr both accept.  CNF and proof are deleted afterwards (the CNF is reproducible from the
node name; its sha256 is recorded).
C3T (FIX1) additions, all other fields unchanged: "cadical_args" (the full CaDiCaL argument list
without the CNF and proof paths) on every record, and "proof_sha256" (sha256 of the LRAT file that
both checkers read, computed before they run and before the proof is deleted; null when CaDiCaL
did not answer UNSATISFIABLE).
usage: close_node.py BASE OUT.jsonl CAP NODE [NODE ...]"""
import hashlib
import json
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "C3a"))
sys.path.insert(0, HERE)
from c3cnf import C3Enc  # noqa: E402
from hullcase import layer_clauses, parse_layers  # noqa: E402
from controls import dual  # noqa: E402


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 22), b""):
            h.update(b)
    return h.hexdigest()


def main():
    base, out, cap = sys.argv[1], sys.argv[2], int(sys.argv[3])
    E = C3Enc(11, 7)
    work = "/opt/work/close"
    os.makedirs(work, exist_ok=True)
    for node in sys.argv[4:]:
        us = [c[0] for c in layer_clauses(11, parse_layers(node), E.ccw, E.sig)]
        cnf, prf = os.path.join(work, node + ".cnf"), os.path.join(work, node + ".lrat")
        with open(base) as f, open(cnf, "w") as g:
            h = f.readline().split()
            g.write(f"p cnf {h[2]} {int(h[3]) + len(us)}\n")
            while True:
                b = f.read(1 << 24)
                if not b:
                    break
                g.write(b)
            g.write("".join(f"{u} 0\n" for u in us))
        rec = {"node": node, "base_sha256": sha(base), "units": len(us), "cnf_sha256": sha(cnf)}
        cargs = ["-q", "-t", str(cap), "--lrat", "--binary=false"]
        rec["cadical_args"] = cargs
        t = time.time()
        r = subprocess.run(["cadical"] + cargs + [cnf, prf], capture_output=True, text=True).stdout
        rec["status"] = next((l[2:] for l in r.splitlines() if l.startswith("s ")), "UNKNOWN")
        rec["solve_s"] = round(time.time() - t, 1)
        rec["proof_sha256"] = None
        if rec["status"] == "UNSATISFIABLE":
            rec["proof_bytes"] = os.path.getsize(prf)
            rec["proof_sha256"] = sha(prf)
            t = time.time()
            a, b, ok = dual(cnf, prf)
            rec.update({"lrat_check": a, "cake_lpr": b, "certified": ok, "check_s": round(time.time() - t, 1)})
        for x in (cnf, prf):
            if os.path.exists(x):
                os.remove(x)
        with open(out, "a") as fo:
            fo.write(json.dumps(rec) + "\n")
        print(json.dumps(rec), flush=True)


if __name__ == "__main__":
    main()
