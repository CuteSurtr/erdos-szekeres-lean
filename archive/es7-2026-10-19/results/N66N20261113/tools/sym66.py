"""Mirror symmetry of the (A,B) = (4,4) catalog: the reflection y -> -y keeps the x-order and swaps caps and
cups, so it maps a (6,6)-set to a (6,6)-set and every incoming state (a Young diagram in the 4x4 box, column
heights f_1 >= ... >= f_4) to its transpose (conjugate partition).  TAU[s] = index of the transposed state."""
import etv_common as ec
from etv_common import STATES, N, A, B, SINDEX
assert A == B
def transpose(f):
    return tuple(sum(1 for x in f if x >= r) for r in range(1, B + 1))
TAU = [SINDEX[transpose(f)] for f in STATES]
assert all(TAU[TAU[s]] == s for s in range(N))
def mirror(support):
    return tuple(sorted(TAU[s] for s in support))
def close(rows):
    """rows: dict support tuple -> demand.  Returns the tau-closure (max demand)."""
    out = dict(rows)
    for s, d in rows.items():
        m = mirror(s)
        if out.get(m, 0) < d: out[m] = d
    return out
if __name__ == '__main__':
    import numpy as np, json, itertools
    T = np.array(TAU)
    # (1) cells: CELLS[TAU[s]] is the transpose of CELLS[s]
    assert all(ec.CELLS[TAU[s]] == frozenset((b, a) for a, b in ec.CELLS[s]) for s in range(N))
    # (2) refined domains transpose
    assert all(ec.DREF[TAU[s]][TAU[t]] == frozenset((b, a) for a, b in ec.DREF[s][t]) for s in range(N) for t in range(N))
    assert all(ec.CAPH[TAU[s]] == ec.CUPH[s] for s in range(N))
    # (3) triple table: forced orientation flips: TT[tau a, tau b, tau c] == TT[a, c, b]
    TTm = ec.TT[np.ix_(T, T, T)]
    print('TT tau-antisymmetric:', bool((TTm == ec.TT.transpose(0, 2, 1)).all()), 'forced triples', int(ec.TT.sum()),
          'both orientations forced:', int((ec.TT & ec.TT.transpose(0, 2, 1)).sum()),
          'cyclic invariant:', bool((ec.TT == ec.TT.transpose(1, 2, 0)).all()))
    print('N', N, 'fixed', ec.FIXED_OCC, [STATES[i] for i in ec.FIXED_OCC], 'tau-fixed states', sum(1 for s in range(N) if TAU[s] == s))
    base = json.load(open('cyc_base_A4B4.json'))
    rows = {tuple(r[0]): r[1] for r in base['rows']}
    from cycle_order import order, check_list
    nclosed = sum(1 for s in rows if mirror(s) in rows)
    okm = 0
    for s, d in rows.items():
        m = mirror(s); L = order(list(m))
        okm += (L is not None and check_list(L))
    print('baseline rows', len(rows), 'mirror already present', nclosed, 'mirror is a valid cycle row', okm)
