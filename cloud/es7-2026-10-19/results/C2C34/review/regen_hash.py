#!/usr/bin/env python3
"""Regenerate zcnf.py rot T K --m 2 --no-sb in memory (hashing sink, nothing written) and print body sha256."""
import sys, os, hashlib, time
C = os.environ.get('C2C', os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.join(C, '..', 'SYMZ'))
sys.path.insert(0, C)
import zcnf
class HSink:
    def __init__(self, path):
        self.h = hashlib.sha256(); self.n = 0
    def add(self, cl):
        self.n += 1
        self.h.update((" ".join(map(str, cl)) + " 0\n").encode())
zcnf.Sink = HSink
t, K = int(sys.argv[1]), int(sys.argv[2])
t0 = time.time()
enc = zcnf.ZEncoding('rot', t, K, 2, body=None, axis=0)
enc.build(sb=False, hull=False)
print(f"c zcnf kind=rot m=2 t={t} axis=0 N={2*t} K={K} | p cnf {enc.nv} {enc.sink.n} | body {enc.sink.h.hexdigest()} | {time.time()-t0:.0f}s")
