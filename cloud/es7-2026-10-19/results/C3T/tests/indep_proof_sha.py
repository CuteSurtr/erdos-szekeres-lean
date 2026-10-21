#!/usr/bin/env python3
"""Independent check of proof_sha256: for the first N certified records of a small run, build the
node CNF here (BASE + layer units, the same bytes as close_node.py), check its sha256 against the
record, run CaDiCaL with the record's cadical_args, hash the LRAT file, compare with proof_sha256,
and check it with cake_lpr.
usage: indep_proof_sha.py TOOLSDIR m k BASE RECORDS.jsonl N WORK"""
import hashlib, json, os, subprocess, sys

tools, m, k, base, recf, N, work = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4], sys.argv[5], int(sys.argv[6]), sys.argv[7]
sys.path.insert(0, os.path.join(tools, "..", "..", "C3a"))
sys.path.insert(0, tools)
from c3cnf import C3Enc  # noqa: E402
from hullcase import layer_clauses, parse_layers  # noqa: E402

E = C3Enc(m, k)
os.makedirs(work, exist_ok=True)
raw = open(base, "rb").read()
hdr, body = raw.split(b"\n", 1)
h = hdr.split()
fails = n = 0
for l in open(recf):
    r = json.loads(l)
    if not r.get("certified") or n >= N:
        continue
    n += 1
    us = [c[0] for c in layer_clauses(m, parse_layers(r["node"]), E.ccw, E.sig)]
    data = b"p cnf %s %d\n" % (h[2], int(h[3]) + len(us)) + body + "".join(f"{u} 0\n" for u in us).encode()
    cnf, prf = os.path.join(work, "x.cnf"), os.path.join(work, "x.lrat")
    open(cnf, "wb").write(data)
    subprocess.run(["cadical"] + r["cadical_args"] + [cnf, prf], capture_output=True)
    ps = hashlib.sha256(open(prf, "rb").read()).hexdigest()
    cake = subprocess.run(["cake_lpr", cnf, prf], capture_output=True, text=True).stdout.strip()
    ok = hashlib.sha256(data).hexdigest() == r["cnf_sha256"] and ps == r["proof_sha256"] and cake == "s VERIFIED UNSAT"
    fails += not ok
    print(f"{r['node']}: cnf_sha256 {'=' if hashlib.sha256(data).hexdigest() == r['cnf_sha256'] else '!='} record, "
          f"proof_sha256 {'=' if ps == r['proof_sha256'] else '!='} record, cake_lpr {cake!r}")
    os.remove(cnf); os.remove(prf)
print("checked", n, "FAILURES", fails)
