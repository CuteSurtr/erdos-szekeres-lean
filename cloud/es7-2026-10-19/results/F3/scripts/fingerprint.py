#!/usr/bin/env python3
"""Canonical order-type fingerprints (chiro.canonical_form, relabelling + reflection; also the
oriented form without reflection) of integer point sets, for deduplication of realized 26-sets.
Inputs: .pts files (one 'x y' per line) or .jsonl files with "id" and "points".
usage: fingerprint.py OUT.jsonl IN...   (one JSON line per set)"""
import sys, os, json, hashlib
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../F/realizer"))
from chiro import canonical_form, chirotope_of
def sets(path):
    if path.endswith(".pts"):
        yield os.path.basename(path)[:-4], [tuple(map(int, l.split())) for l in open(path) if l.strip()]
    else:
        for l in open(path):
            r = json.loads(l)
            if "points" in r: yield r.get("id", "?"), [tuple(p) for p in r["points"]]
out = open(sys.argv[1], "w")
for path in sys.argv[2:]:
    for name, P in sets(path):
        chi = chirotope_of(P); n = len(P)
        h = hashlib.sha1(canonical_form(chi, n).encode()).hexdigest()[:20]
        ho = hashlib.sha1(canonical_form(chi, n, mirror=False).encode()).hexdigest()[:20]
        rec = {"source": os.path.relpath(path), "id": name, "n": n, "fp": h, "fp_oriented": ho}
        out.write(json.dumps(rec) + "\n"); print(json.dumps(rec), flush=True)
