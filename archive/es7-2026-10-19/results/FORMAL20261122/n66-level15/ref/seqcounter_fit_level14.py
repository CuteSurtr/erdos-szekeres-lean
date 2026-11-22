"""Fit pysat's CardEnc.atmost(seqcounter) clause and aux-numbering order (no source on disk).
Reconstruction (diagonal walk, aux allocated on first reference):
  k >= n: no clauses; k == n-1: the single clause [-l for l in lits] (no aux).
  aux s(a,j) (a = 1..n-1 position of the prefix, j = 1..k) is needed iff j <= a and k - j <= (n-1) - a.
  for i in 1..n-1:
    if s(i,1) needed: emit [-x_i, s(i,1)]
    a, j = i, 1
    while a <= n-1 and j <= k and s(a,j) needed:
      if a+1 <= n-1 and s(a+1,j) needed: emit [-s(a,j), s(a+1,j)]
      if j < k: if a+1 <= n-1 and s(a+1,j+1) needed: emit [-x_{a+1}, -s(a,j), s(a+1,j+1)]
      else: emit [-x_{a+1}, -s(a,j)]
      a, j = a+1, j+1
Usage: python -I seqcounter_fit.py  (grid test against pysat; exits nonzero on the first mismatch)."""
import sys, itertools
from pysat.card import CardEnc, EncType

def recon(lits, k, top):
    n = len(lits)
    if k >= n: return [], top
    if k == n - 1: return [[-l for l in lits]], top      # pysat: "not all" as one clause
    assert k >= 1
    ids = {}
    def s(a, j):
        nonlocal top
        if (a, j) not in ids:
            top += 1; ids[(a, j)] = top
        return ids[(a, j)]
    need = lambda a, j: 1 <= a <= n - 1 and 1 <= j <= k and j <= a and k - j <= (n - 1) - a
    x = lambda i: lits[i - 1]
    out = []
    for i in range(1, n):
        if need(i, 1): out.append([-x(i), s(i, 1)])
        a, j = i, 1
        while a <= n - 1 and j <= k and need(a, j):
            if need(a + 1, j): out.append([-s(a, j), s(a + 1, j)])
            if j < k:
                if need(a + 1, j + 1): out.append([-x(a + 1), -s(a, j), s(a + 1, j + 1)])
            else:
                out.append([-x(a + 1), -s(a, j)])
            a, j = a + 1, j + 1
    return out, top

bad = 0; tests = 0
cases = [(n, k) for n in range(1, 40) for k in range(1, n + 2)] + [(68, 14), (68, 13), (68, 15), (70, 14)]
for n, k in cases:
    for sign in (1, -1):
        lits = [sign * (100 + 3 * i) for i in range(n)]
        top = 5000
        e = CardEnc.atmost(lits=lits, bound=k, top_id=top, encoding=EncType.seqcounter)
        mine, mtop = recon(lits, k, top)
        tests += 1
        if [list(c) for c in e.clauses] != mine or (mine and e.nv != mtop):
            bad += 1
            if bad <= 3: print('MISMATCH', n, k, sign, e.clauses[:12], mine[:12], e.nv, mtop)
# the production instance: 68 hole literals -sel_s (s = 2..69), sel_s = 988541 + s, bound 14, top 1647026
lits = [-(988541 + s) for s in range(2, 70)]
e = CardEnc.atmost(lits=lits, bound=14, top_id=1647026, encoding=EncType.seqcounter)
mine, mtop = recon(lits, 14, 1647026)
prod_ok = [list(c) for c in e.clauses] == mine and e.nv == mtop
print({'tests': tests, 'mismatches': bad, 'production_ok': prod_ok, 'production_clauses': len(mine), 'production_top': mtop})
sys.exit(0 if bad == 0 and prod_ok else 1)
