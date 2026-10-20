#!/usr/bin/env python3
"""Canonical order-type fingerprint (chiro.canonical_form: relabelling and reflection, sha1) of
point sets given as .pts files (one 'x y' per line) or JSON-lines files with "id"/"points".
usage: fingerprint.py FILE...   -> lines: name fingerprint"""
import hashlib, json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../../tools/realizer"))
from chiro import canonical_form, chirotope_of
def fp(P): return hashlib.sha1(canonical_form(chirotope_of(P), len(P)).encode()).hexdigest()
for f in sys.argv[1:]:
    if f.endswith(".pts"):
        print(os.path.basename(f)[:-4], fp([tuple(map(int, l.split())) for l in open(f) if l.strip()]), flush=True)
    else:
        for l in open(f):
            r = json.loads(l)
            if "points" in r: print(r["id"], fp([tuple(p) for p in r["points"]]), flush=True)
