"""Level-set families: forbidden chain lengths from label domains, ETV values,
witness occupancy, and LP capacity thresholds."""
import sys, itertools, json
from math import comb
sys.argv = [sys.argv[0]]
from cap_lp import res, bal, lp
def cells(s, A): return {(a+1, y) for a in range(A) for y in range(1, s[a]+1)}
def etv(a, b, n=8):
    # max size: no a-cap, no b-cup, no n-gon (conjectured ETV; cup-cap when n >= a+b-3)
    if n >= a + b - 3: return comb(a + b - 4, a - 2)
    return sum(comb(n - 2, i) for i in range(n - b, a - 1))
def analyse(kind, S, C, A, Bdim, fixed0, target):
    out = []
    Cs = [cells(s, A) for s in S]
    thr_ranges = [range(0, 7 if kind=='res' else 6)] * A
    seen = set()
    for th in itertools.product(*thr_ranges):
        if any(th[i] < th[i+1] for i in range(A-1)): continue
        X = [i for i, s in enumerate(S) if all(s[a] >= th[a] for a in range(A))]
        key = tuple(X)
        if len(X) < 10 or key in seen: continue
        seen.add(key)
        capset = set(); cupset = set()
        for s in X:
            for t in X:
                if s == t: continue
                d = Cs[t] - Cs[s]
                if kind == 'res': d.discard((1, 6))
                for (a, b) in d: capset.add(a); cupset.add(b)
        ca = len(capset) + 1; cu = len(cupset) + 1     # max cap / cup length among owners
        e = etv(ca + 1, cu + 1)
        if e >= len(X): continue
        # LP threshold: largest c with LP > target
        lo, hi = 0, len(X) - 1; best = None
        base = lp(S, C, [], fixed0)[0]
        while lo <= hi:
            mid = (lo + hi) // 2
            v = lp(S, C, [{'support': X, 'rhs': len(X) - mid}], fixed0)[0]
            if v > target + 1e-6: best = mid; lo = mid + 1
            else: hi = mid - 1
        out.append({'thr': th, 'size': len(X), 'maxcap': ca, 'maxcup': cu, 'etv': e, 'cstar': best,
                    'slack': (best - e) if best is not None else None})
    return out
if __name__ == '__main__':
    r = analyse('res', res['states'], res['constraints'], 4, 6, True, 33)
    b = analyse('bal', bal['states'], bal['constraints'], 5, 5, False, 65)
    for name, L in (('res', r), ('bal', b)):
        L = [x for x in L if x['cstar'] is not None]
        L.sort(key=lambda x: (-x['slack'], x['maxcap'] + x['maxcup']))
        print(name, 'families with a useful threshold:', len(L))
        for x in L[:25]: print('  ', x)
    json.dump({'res': r, 'bal': b}, open('families_out.json', 'w'), indent=1)
