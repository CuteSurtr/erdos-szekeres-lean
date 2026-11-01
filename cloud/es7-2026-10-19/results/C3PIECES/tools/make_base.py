#!/usr/bin/env python3
"""Write the threefold base CNF (C3-S gen_case.py 11 7 none = C3a chain encoding, m = 11, k = 7) to OUT,
streaming each clause to disk instead of holding the clause list in memory (about 280 MB RSS, 5 s).

The repository's C3a/c3cnf.py is imported read-only and used unchanged; only its clause list is replaced by
a sink that writes each clause in exactly the format of C3Enc.write() (" ".join(lits) + " 0\n").  The
header is fixed in advance ('p cnf 168399 4154921', documented in results/C3W3S/TASK.md); after the build
the variable and clause counts are compared with it, and the SHA-256 of the whole file must be
bf0e502ee78599400d36e0fc402a8ce79b4c41443327b4e0186902fab0cdd6da.  On any mismatch the file is deleted and
the exit code is 1.  Run with python3 -I -B (no bytecode is written into the repository).
usage: make_base.py RESULTS_DIR OUT.cnf"""
import hashlib
import json
import os
import sys

sys.dont_write_bytecode = True
RD, OUT = sys.argv[1:3]
sys.path.insert(0, os.path.join(RD, "C3a"))
from c3cnf import C3Enc  # noqa: E402

NV, NC = 168399, 4154921
BASE_SHA = "bf0e502ee78599400d36e0fc402a8ce79b4c41443327b4e0186902fab0cdd6da"


class Sink:
    def __init__(self, f):
        self.f, self.n = f, 0

    def append(self, c):
        self.f.write(" ".join(map(str, c)) + " 0\n")
        self.n += 1

    def __len__(self):
        return self.n


tmp = OUT + ".part"
e = C3Enc(11, 7)
with open(tmp, "w", buffering=1 << 22) as f:
    f.write(f"p cnf {NV} {NC}\n")
    e.clauses = Sink(f)
    e.build()
h = hashlib.sha256()
with open(tmp, "rb") as f:
    for b in iter(lambda: f.read(1 << 22), b""):
        h.update(b)
res = {"nv": e.nv, "clauses": len(e.clauses), "bytes": os.path.getsize(tmp), "sha256": h.hexdigest()}
res["ok"] = e.nv == NV and len(e.clauses) == NC and h.hexdigest() == BASE_SHA
if res["ok"]:
    os.replace(tmp, OUT)
else:
    os.remove(tmp)
print(json.dumps(res))
sys.exit(0 if res["ok"] else 1)
