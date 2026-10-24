#!/usr/bin/env python3
"""Canonical order-type fingerprint (chiro.canonical_form: relabelling and reflection, then sha1) of
integer point sets given as .pts files (one 'x y' per line).  usage: fingerprint.py a.pts [b.pts ...]
prints 'sha1 file' per set."""
import hashlib, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "tools", "realizer"))
from chiro import canonical_form, chirotope_of  # noqa
for f in sys.argv[1:]:
    P = [tuple(map(int, l.split())) for l in open(f) if l.strip()]
    print(hashlib.sha1(canonical_form(chirotope_of(P), len(P)).encode()).hexdigest(), f, flush=True)
