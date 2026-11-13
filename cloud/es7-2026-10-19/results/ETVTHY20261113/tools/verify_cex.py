"""Independent (pure-Python, exact integer) verification of the counterexample files in cex/.
Recomputes every chain statistic from scratch with pyexact (no C library)."""
import sys, json, glob, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pyexact import chains, otable

def stats(P):
    n = len(P); O = otable(P)
    capE, cupE, capB, cupB = chains(P, O)
    cap_end = [max([1] + [capB[s, v] for s in range(v)]) for v in range(n)]
    cup_end = [max([1] + [cupB[s, v] for s in range(v)]) for v in range(n)]
    cap_start = [max([1] + [capB[v, t] for t in range(v+1, n)]) for v in range(n)]
    gon = max(capB[k] + cupB[k] - 2 for k in capB)
    return dict(cap_end=cap_end, cup_end=cup_end, cap_start=cap_start, gon=gon,
                maxcap=max(capB.values()), maxcup=max(cupB.values()), capB=capB, cupB=cupB)

def sub_types(P, idx):
    Q = [P[i] for i in idx]
    if len(Q) < 2: return set(), 1, 1
    _, _, capB, cupB = chains(Q)
    return {(capB[k], cupB[k]) for k in capB}, max(capB.values()), max(cupB.values())

def has(types, a, b): return any(x >= a and y >= b for x, y in types)

def check(name, P):
    P = sorted(tuple(p) for p in P); n = len(P)
    assert len({p[0] for p in P}) == n
    st = stats(P)
    ok_set = st['gon'] <= 7 and st['maxcap'] <= 4
    ce, be, cs = st['cap_end'], st['cup_end'], st['cap_start']
    piece = {
        'M': [i for i in range(n) if cs[i] == 4 and ce[i] == 4],
        'B4': [i for i in range(n) if cs[i] == 4 and ce[i] <= 3],
        'B6': [i for i in range(n) if be[i] == 6],
        'R7': [i for i in range(n) if be[i] == 7],
        'R6': [i for i in range(n) if be[i] >= 6],
    }
    if name == 'M_has_45_heptagon': t, mc, mu = sub_types(P, piece['M']); claim = has(t, 4, 5)
    elif name == 'M_has_5cup': t, mc, mu = sub_types(P, piece['M']); claim = mu >= 5
    elif name == 'B4_has_36_heptagon': t, mc, mu = sub_types(P, piece['B4']); claim = has(t, 3, 6)
    elif name == 'B6_has_36_heptagon': t, mc, mu = sub_types(P, piece['B6']); claim = has(t, 3, 6)
    elif name == 'R7_has_36_heptagon': t, mc, mu = sub_types(P, piece['R7']); claim = has(t, 3, 6)
    elif name == 'R6_has_4cap': t, mc, mu = sub_types(P, piece['R6']); claim = mc >= 4
    elif name == 'R7_size_18': claim = len(piece['R7']) >= 18
    elif name == 'R7_size_19': claim = len(piece['R7']) >= 19
    elif name == 'R7_size_20': claim = len(piece['R7']) >= 20
    elif name == 'L7_R7_interleave':
        L7 = [s for s in range(n) if any(st['cupB'][s, t] >= 7 for t in range(s+1, n))]
        claim = max(L7) > min(piece['R7'])
    else: claim = None
    return dict(n=n, valid_5capfree_octagonfree=ok_set, claim=claim,
                sizes={k: len(v) for k, v in piece.items()})

if __name__ == '__main__':
    d = sys.argv[1] if len(sys.argv) > 1 else 'cex'
    for fn in sorted(glob.glob(os.path.join(d, '*.json'))):
        name = os.path.basename(fn)[:-5]
        r = check(name, json.load(open(fn))['P'])
        print(name, json.dumps(r), flush=True)
