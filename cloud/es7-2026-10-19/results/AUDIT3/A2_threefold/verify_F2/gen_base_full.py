#!/usr/bin/env python3
"""verify_F2: write the C3a chain base CNF for (m, k) = (11, 7) (gen_case.py 11 7 none) as ONE file
(header + body) without holding the clause list in memory, using the repository's c3cnf.py
unchanged (imported read-only from results/C3a; run with -B so no bytecode is written there).
The header must be known in advance: 'p cnf 168399 4154921' (documented); the script checks the
variable and clause counts after the build and prints the sha256 of the whole file, which must be
bf0e502ee78599400d36e0fc402a8ce79b4c41443327b4e0186902fab0cdd6da.
usage: python -I -B gen_base_full.py RESULTS_DIR OUT.cnf"""
import hashlib
import json
import os
import sys

sys.dont_write_bytecode = True
RD, OUT = sys.argv[1:3]
sys.path.insert(0, os.path.join(RD, "C3a"))
from c3cnf import C3Enc  # noqa: E402

NV, NC = 168399, 4154921


class Sink:
    def __init__(self, f):
        self.f, self.n = f, 0

    def append(self, c):
        self.f.write(" ".join(map(str, c)) + " 0\n")
        self.n += 1

    def __len__(self):
        return self.n


e = C3Enc(11, 7)
with open(OUT, "w", buffering=1 << 22) as f:
    f.write(f"p cnf {NV} {NC}\n")
    e.clauses = Sink(f)
    e.build()
ok_counts = (e.nv == NV and len(e.clauses) == NC)
h = hashlib.sha256()
with open(OUT, "rb") as f:
    for b in iter(lambda: f.read(1 << 22), b""):
        h.update(b)
print(json.dumps({"nv": e.nv, "clauses": len(e.clauses), "counts_match_header": ok_counts,
                  "sha256": h.hexdigest(), "bytes": os.path.getsize(OUT),
                  "sha_ok": h.hexdigest() == "bf0e502ee78599400d36e0fc402a8ce79b4c41443327b4e0186902fab0cdd6da"}))
