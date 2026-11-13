#!/usr/bin/env python3
"""Check the (2 => 1) gluing recipe of Theorem 6 on the largest available input:
a 26-point set A0 with distinct x, general position, no 5-cap and gon <= 6
(27 points would be needed for the theorem; such a set is not known).
B0 = {(t_j, -M - eps t_j^2)} with t_j in [-1,1].  Verify exactly:
 general position of A0 u B0, (S1) and (S2) for z = (0,-1), and gon(A0 u B0) = 6.
Also report the smallest M (on a grid) for which the recipe works, to see that
'M large' is really needed and sufficient."""
import os, sys, itertools
from fractions import Fraction as Fr
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from geomdp import orient, general_position, distinct_x, analyse

def load(path):
    P = []
    for line in open(path):
        s = line.split()
        if len(s) >= 2:
            P.append((int(s[0]), int(s[1])))
    return P

def split_ok_down(A, B):
    """z = (0,-1): B strictly below all lines through 2 points of A; A strictly above all lines of B."""
    for a, a2 in itertools.combinations(sorted(A), 2):     # a.x < a2.x
        for b in B:
            if not orient(a, a2, b) < 0:
                return False
    for b, b2 in itertools.combinations(sorted(B), 2):
        for a in A:
            if not orient(b, b2, a) > 0:
                return False
    return True

def main():
    P = load(sys.argv[1])
    print('classical set:', len(P), 'points; general position', general_position(P), '; distinct x', distinct_x(P))
    print('  analysis:', analyse(P))
    Ps = sorted(P)
    A0 = Ps[:26]; Btail = Ps[26:]
    print('A0 = 26 leftmost points:', analyse(A0), 'general position', general_position(A0))
    print('last 6 points:', analyse(Btail))
    a0 = analyse(A0)
    if a0['maxcap'] > 4 or a0['gon'] > 6:
        print('A0 not usable in the standard frame'); return
    ts = [Fr(-1), Fr(-3, 5), Fr(-1, 5), Fr(1, 5), Fr(3, 5), Fr(9, 10)]   # avoid A0's x = 0, 1
    eps = Fr(1)
    results = []
    for M in [10, 100, 1000, 3000, 10**4, 10**5, 10**6]:
        B0 = [(t, -M - eps*t*t) for t in ts]
        S = A0 + B0
        gp = general_position(S)
        sp = split_ok_down(A0, B0)
        res = {'M': M, 'general_position': gp, 'split_z_down': sp}
        if gp and len({p[0] for p in S}) == len(S):
            res.update(analyse(S))
        results.append(res)
        print(res)

if __name__ == '__main__':
    main()
