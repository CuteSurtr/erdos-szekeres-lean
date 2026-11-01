#!/usr/bin/env python3
"""Provenance/equality side checks:
 (1) SYM2/build.py: does sym(7, X=50, Y=10000, K=3) reproduce sym7_32points.txt exactly? (and the k=9 file)
 (2) SYM5/c5_31minus_centre.txt == SYMMAX/c5_31points.txt minus (0,0,0,0)?"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "repo_copy"))
sys.path.insert(0, HERE)
import a7lib as L
import build_sym2 as B
R = os.environ.get("ES7_RESULTS", ".")
f7, _ = L.parse(R + "/SYM2/sym7_32points.txt", "Z2")
g7 = B.sym(7, X=50, Y=10000, K=3)
print("sym7: file n=%d, build n=%d, identical list: %s, identical set: %s" % (len(f7), len(g7), f7 == g7, set(f7) == set(g7)))
f9, _ = L.parse(R + "/SYM2/sym9_128points.txt", "Z2")
g9 = B.sym(9, X=10**15, Y=10**15, K=10**9)
print("sym9: file n=%d, build n=%d, identical list: %s, identical set: %s" % (len(f9), len(g9), f9 == g9, set(f9) == set(g9)))
a, _ = L.parse(R + "/SYMMAX/c5_31points.txt", "Z5")
b, _ = L.parse(R + "/SYM5/c5_31minus_centre.txt", "Z5")
print("c5_31minus_centre == c5_31 \\ {0}: %s (sizes %d, %d)" % (set(b) == set(a) - {(0, 0, 0, 0)}, len(a), len(b)))
