#!/usr/bin/env python3
"""Canonical forms (results/F/realizer/chiro.canonical_form: relabelling + reflection) of every
32-point set in inputs/distinct_K7*.txt, written as sha1 digests, for comparison with new sets.
usage: pool_canon.py OUT.txt"""
import sys, os, glob, hashlib
B = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../../..")
sys.path.insert(0, os.path.join(B, "results/F/realizer"))
import chiro
out = open(sys.argv[1], "w")
for fn in sorted(glob.glob(os.path.join(B, "inputs/distinct_K7*.txt"))):
    for l in open(fn):
        L = l.split(); i = L.index("32"); v = list(map(int, L[i + 1:i + 65]))
        P = [(v[2 * k], v[2 * k + 1]) for k in range(32)]
        c = chiro.canonical_form(chiro.chirotope_of(P), 32)
        out.write(f"{os.path.basename(fn)} {L[1]} {hashlib.sha1(c.encode()).hexdigest()}\n")
