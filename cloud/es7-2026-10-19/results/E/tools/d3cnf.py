#!/usr/bin/env python3
"""CNF for N = 6*n6 + 3 points with dihedral D3 symmetry (rotations by 120 degrees and three
mirror axes), one orbit of 3 points on the mirror axes and n6 orbits of 6, and no K points in
convex position.  For N = 33: n6 = 5 (the only D3 class at 33 points, see README).

Built on symcnf.SymEncoding (m = 3, auxiliary centre, t = 2*n6 + 1 rotation orbits) and its
labelling normal form:
  orbit 0  = the 3-orbit, (0,0) = its point on the mirror axis M;
  orbits 1..t-1 = the rotation orbits of the 6-orbits, each represented by its point in the open
             120-degree sector measured at the centre from the ray to (0,0), sorted by angle.
Let S be the reflection in M.  A 6-orbit {R^r p, R^r S p} with p at angle th in (0, 60) degrees
contributes p (angle th) and R S p (angle 120 - th) to the sector, so with the sorted labels
  orbits 1..n6 have angles in (0,60), orbits n6+1..t-1 in (60,120), and R S (j,0) = (t-j, 0).
Hence the label permutation of S is
  S(0, r) = (0, -r mod 3),   S(j, r) = (t-j, -r-1 mod 3) for 1 <= j <= t-1,   S(centre) = centre,
and a reflection reverses orientation: chi(S a, S b, S c) = -chi(a, b, c).
The CNF has one variable per D3-orbit of triples (sign bookkeeping includes the reflection
sign), and axiom / convexity clauses per D3-orbit of 4-, 5-, r- and K-sets.  All other clauses
(centre facts, sector and order constraints) are those of symcnf.py.  Every D3-symmetric set
in general position has such a labelling: moving the representative p of a 6-orbit slightly
keeps the D3 symmetry and all orientations of the set, so the centre can be assumed to be in
general position with the set as well (needed for the sector constraints).

usage: d3cnf.py N K -o out.cnf --map out.json
"""
import argparse
import itertools
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "tools", "symmetric"))
from symcnf import SymEncoding, parity_sort  # noqa: E402


class D3Encoding(SymEncoding):
    def sigma(self, i):
        if i == self.c:
            return i
        o, r = divmod(i, 3)
        if o == 0:
            return (-r) % 3
        return (self.t - o) * 3 + (-r - 1) % 3

    def _build_group(self):
        P = self.P
        rot = [[self.pi(i, k) for i in range(P)] for k in range(3)]
        sig = [self.sigma(i) for i in range(P)]
        assert sorted(sig) == list(range(P))
        assert all(sig[sig[i]] == i for i in range(P)), "sigma not an involution"
        # sigma R sigma = R^-1
        for i in range(P):
            assert sig[rot[1][sig[i]]] == rot[2][i], "sigma R sigma != R^-1"
        self.G = [(rot[k], 1) for k in range(3)] + [([rot[k][sig[i]] for i in range(P)], -1) for k in range(3)]

    def canon(self, S):
        best = S
        for perm, _ in self.G[1:]:
            T = tuple(sorted(perm[x] for x in S))
            if T < best:
                best = T
        return best

    def _triples(self):
        assert self.m == 3 and self.has_center and not self.center_in_set
        assert self.t % 2 == 1
        self._build_group()
        for T in itertools.combinations(range(self.P), 3):
            if T in self.tv:
                continue
            v = self.new()
            seen = {}
            for perm, sg in self.G:
                S, s = parity_sort((perm[T[0]], perm[T[1]], perm[T[2]]))
                # chi(g T) = sg * chi(T) = sg * v ;  chi(g T) = s * chi(S)  =>  chi(S) = s * sg * v
                val = s * sg
                if S in seen:
                    assert seen[S] == val, ("triple orbit forces orientation 0", T, S)
                else:
                    seen[S] = val
            for S, s in seen.items():
                self.tv[S] = (v, s)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("N", type=int)
    ap.add_argument("K", type=int)
    ap.add_argument("--kgon", choices=["layered", "direct"], default="layered")
    ap.add_argument("-o", "--out", required=True)
    ap.add_argument("--map")
    args = ap.parse_args()
    assert (args.N - 3) % 6 == 0
    enc = D3Encoding(args.N, args.K, 3, center_in_set=False, sb=True, kgon=args.kgon, center=True,
                     body=args.out + ".body")
    enc.build()
    enc.stats["group"] = "D3"
    info = enc.write(args.out, args.map)
    if args.map:
        d = json.load(open(args.map))
        d["group"] = "D3"
        d["sigma"] = [enc.sigma(i) for i in range(enc.P)]
        json.dump(d, open(args.map, "w"))
    info.pop("triples", None)
    info["group"] = "D3"
    print(json.dumps(info))


if __name__ == "__main__":
    main()
