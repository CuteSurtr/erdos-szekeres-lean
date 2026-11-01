#!/usr/bin/env python3
"""A2 audit: regenerate the C3a chain base CNF (c3cnf.py m k, i.e. gen_case.py m k none) without
holding the clause list in memory.  The vendored c3cnf.py (byte-identical to results/C3a/c3cnf.py)
is used unchanged; only its clause list is replaced by a sink that streams each clause to disk in
exactly the format of C3Enc.write().  Writes BODY (all clause lines, no header) and prints the
header and the sha256 of header + body (which must equal the documented base sha for m=11, k=7).
usage: gen_base_stream.py m k BODY_OUT"""
import hashlib
import json
import os
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "vendor"))
from c3cnf import C3Enc  # noqa: E402


class Sink:
    def __init__(self, f):
        self.f, self.n = f, 0

    def append(self, c):
        self.f.write(" ".join(map(str, c)) + " 0\n")
        self.n += 1

    def __len__(self):
        return self.n


def main():
    m, k, body = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
    e = C3Enc(m, k)
    with open(body, "w", buffering=1 << 22) as f:
        e.clauses = Sink(f)
        e.build()
    header = f"p cnf {e.nv} {len(e.clauses)}\n"
    h = hashlib.sha256(header.encode())
    with open(body, "rb") as f:
        for b in iter(lambda: f.read(1 << 22), b""):
            h.update(b)
    print(json.dumps({"m": m, "k": k, "header": header.strip(), "sha256_header_plus_body": h.hexdigest(),
                      "body_bytes": os.path.getsize(body), "sections": e.sections}))


if __name__ == "__main__":
    main()
