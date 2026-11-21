"""Own implementation (verify-residual-row) of the residual state map, written from the Lean
definitions in ErdosSzekeres/Omission/ResidualRanks.lean and ResidualStates.lean:
  cup(i,j,k)  = orient(p_i,p_j,p_k) > 0   (Realization.lean, Configuration.cup)
  Eplus(u,v)  = longest cup ending with the exact pair (u,v)    (ActualRanks.rank cup true)
  Fminus(u,v) = longest cap starting with the exact pair (u,v)  (ResidualRanks.rank n cup false)
  label(u,v)  = (6 - Fminus(u,v), Eplus(u,v) - 1)
  column(v,i) = max_{u<v} (label.2 if i+1 <= label.1 else 0), i = 0..3
  state(v)    = [column(v,0..3)] + [0]
Exact arithmetic only (int or Fraction)."""
from fractions import Fraction


def orient(p, q, r):
    return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])


def cup_table(P):
    n = len(P)
    C = {}
    for i in range(n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                o = orient(P[i], P[j], P[k])
                if o == 0:
                    raise ValueError("collinear triple")
                C[i, j, k] = o > 0
    return C


def ranks_from_cup(n, cup):
    """cup: dict (i,j,k)->bool for i<j<k. Returns Eplus, Eminus (ending), Fminus, Fplus (starting)."""
    Eplus, Eminus = {}, {}
    for v in range(n):
        for u in range(v):
            bp, bm = 2, 2
            for t in range(u):
                if cup[t, u, v]:
                    bp = max(bp, Eplus[t, u] + 1)
                else:
                    bm = max(bm, Eminus[t, u] + 1)
            Eplus[u, v], Eminus[u, v] = bp, bm
    Fminus, Fplus = {}, {}
    for u in range(n - 1, -1, -1):
        for v in range(n - 1, u, -1):
            bm, bp = 2, 2
            for w in range(v + 1, n):
                if not cup[u, v, w]:
                    bm = max(bm, Fminus[v, w] + 1)
                else:
                    bp = max(bp, Fplus[v, w] + 1)
            Fminus[u, v], Fplus[u, v] = bm, bp
    return Eplus, Eminus, Fminus, Fplus


def residual_states(n, cup):
    Eplus, Eminus, Fminus, Fplus = ranks_from_cup(n, cup)
    states = []
    for v in range(n):
        cols = []
        for i in range(4):
            best = 0
            for u in range(v):
                a, b = 6 - Fminus[u, v], Eplus[u, v] - 1
                if i + 1 <= a:
                    best = max(best, b)
            cols.append(best)
        states.append(tuple(cols) + (0,))
    return states, (Eplus, Eminus, Fminus, Fplus)


def residual_conditions(n, cup, ranks):
    """no 6-cap, no 8-cup, no junction (6-cup ending at (t,u) and 5-cap starting at (u,v))."""
    Eplus, Eminus, Fminus, Fplus = ranks
    if any(x >= 6 for x in Fminus.values()):
        return False, "6-cap"
    if any(x >= 8 for x in Eplus.values()):
        return False, "8-cup"
    for u in range(n):
        ends6 = any(Eplus[t, u] >= 6 for t in range(u))
        starts5 = any(Fminus[u, v] >= 5 for v in range(u + 1, n))
        if ends6 and starts5:
            return False, "junction"
    return True, "ok"


def largest_convex(P, cup):
    """Largest convex polygon via max over endpoint pairs (s,t) of longest cap s..t + longest cup s..t - 2."""
    n = len(P)
    if n <= 2:
        return n
    best = 2
    for s in range(n):
        # Dcup[(j,t)] longest cup from s ending with pair (j,t); same for cap
        Dcup, Dcap = {}, {}
        for t in range(s + 1, n):
            Dcup[s, t] = 2
            Dcap[s, t] = 2
        for j in range(s + 1, n):
            for t in range(j + 1, n):
                bc, ba = None, None
                for i in range(s, j):
                    if (i, j) in Dcup and cup[i, j, t]:
                        bc = max(bc or 0, Dcup[i, j] + 1)
                    if (i, j) in Dcap and not cup[i, j, t]:
                        ba = max(ba or 0, Dcap[i, j] + 1)
                if bc:
                    Dcup[j, t] = max(Dcup.get((j, t), 0), bc)
                if ba:
                    Dcap[j, t] = max(Dcap.get((j, t), 0), ba)
        lc, la = {}, {}
        for (j, t), val in Dcup.items():
            lc[t] = max(lc.get(t, 0), val)
        for (j, t), val in Dcap.items():
            la[t] = max(la.get(t, 0), val)
        for t in range(s + 1, n):
            best = max(best, lc.get(t, 0) + la.get(t, 0) - 2)
    return best


def lower_hull_indices(P):
    """Indices of the vertices of the lower convex hull of x-sorted points (exact)."""
    H = []
    for i in range(len(P)):
        while len(H) >= 2 and orient(P[H[-2]], P[H[-1]], P[i]) <= 0:
            H.pop()
        H.append(i)
    return H
