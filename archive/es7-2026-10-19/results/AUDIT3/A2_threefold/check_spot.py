#!/usr/bin/env python3
"""A2 audit: check the C3SPOT records independently: verdict fields, that the solved rows are a
prefix of the shuffled sample, and that every re-solved CNF sha256 equals this audit's own
re-derivation (own unit generator of a2compose.py + the regenerated base body)."""
import hashlib, json, os, sys
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import a2compose as A  # noqa: E402
body, rdir = sys.argv[1], sys.argv[2]
rows = [l.rstrip("\n").split("\t") for l in open(os.path.join(rdir, "C3SPOT/units6.tsv")) if l.strip()]
recs = [json.loads(l) for l in open(os.path.join(rdir, "C3SPOT/out.jsonl")) if l.strip()]
solved = {r["node"]: r for r in recs}
pos = {row[1]: i for i, row in enumerate(rows)}
idx = sorted(pos[n] for n in solved)
ok = [r for r in recs if r.get("status") == "UNSATISFIABLE" and r.get("certified") is True and r.get("lrat_check") == "c VERIFIED"
      and r.get("cake_lpr") == "s VERIFIED UNSAT" and r.get("cnf_sha256") == rows[pos[r["node"]]][3]]
print("sample rows", len(rows), "distinct", len(pos), "re-solved", len(recs), "distinct", len(solved), "pass", len(ok))
print("solved row indices: min", idx[0], "max", idx[-1], "prefix of the shuffled list:", idx == list(range(len(idx))),
      "gaps below max:", len(set(range(idx[-1] + 1)) - set(idx)))
need = sorted({A.my_units(*A.parse(n)).__len__() for n in solved})
hs = {k: hashlib.sha256(f"p cnf {A.BASE_V} {A.BASE_C + k}\n".encode()) for k in need}
with open(body, "rb") as f:
    for b in iter(lambda: f.read(1 << 22), b""):
        for h in hs.values():
            h.update(b)
mism = 0
for n, r in solved.items():
    us = A.my_units(*A.parse(n))
    h = hs[len(us)].copy(); h.update("".join(f"{u} 0\n" for u in us).encode())
    mism += h.hexdigest() != r["cnf_sha256"]
print("re-solved CNF sha256 vs own re-derivation: mismatches", mism, "of", len(solved))
print("cube-node rows among re-solved:", sum("__" in n for n in solved))
