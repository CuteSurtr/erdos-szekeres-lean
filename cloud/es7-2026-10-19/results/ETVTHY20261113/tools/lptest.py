"""Evaluate hypothetical rows on the 84-state omission model (cap5_omission rows + lazy cycle rows).
Exploratory only: HiGHS MIP values are not certificates."""
import sys, json, itertools, time
sys.path.insert(0, '/home/jay/research/data/theory310-20261113')
import numpy as np
import cap5_omission as C
base = json.load(open('/home/jay/research/data/theory310-20261113/cap5_omission_out.json'))
ST = [tuple(s) for s in base['states']]
idx = {s: i for i, s in enumerate(ST)}
rows0 = [(list(r[0]), r[1]) for r in base['rows']]
fixed = {0, idx[(1, 0, 0)]}

def capacity_row(pred, cap):
    sup = [i for i, s in enumerate(ST) if pred(s)]
    return (sup, len(sup) - cap)

def solve_lazy(extra, tl=60, lp=False):
    rows = rows0 + extra
    t0 = time.time()
    for it in range(30):
        if lp:
            h = C.highspy.Highs(); h.silent()
            inf = C.highspy.kHighsInf
            for i in range(C.N):
                h.addVar(0.0, 0.0 if i in fixed else 1.0); h.changeColCost(i, 1.0)
            for sup, d in rows:
                h.addRow(float(d), inf, len(sup), np.array(sup, dtype=np.int32), np.ones(len(sup)))
            h.run(); sol = h.getSolution().col_value
            return sum(sol), None
        holes, bound, status = C.solve(rows, fixed, time_limit=tl)
        occ = [i for i in range(C.N) if i not in holes]
        cyc = C.find_cycle(occ, 8, limit=40)
        if not cyc:
            return len(holes), holes
        rows = rows + [(list(c), 1) for c in cyc]
    return len(holes), holes

if __name__ == '__main__':
    assert ST == C.ST
    tests = {
        'base': [],
        'R7<=16': [capacity_row(lambda s: s[0] == 6, 16)],
        'R7<=10': [capacity_row(lambda s: s[0] == 6, 10)],
        'R6<=35': [capacity_row(lambda s: s[0] >= 5, 35)],
        'R6<=30': [capacity_row(lambda s: s[0] >= 5, 30)],
        'B6<=16': [capacity_row(lambda s: s[0] == 5, 16)],
        'T<=48': [capacity_row(lambda s: s[0] <= 5, 48)],
        'R4<=48': [capacity_row(lambda s: s[2] >= 1, 48)],
        'R4<=40': [capacity_row(lambda s: s[2] >= 1, 40)],
        'R4<=30': [capacity_row(lambda s: s[2] >= 1, 30)],
        'R7<=18': [capacity_row(lambda s: s[0] == 6, 18)],
        'R7<=21': [capacity_row(lambda s: s[0] == 6, 21)],
        'R7<=19': [capacity_row(lambda s: s[0] == 6, 19)],
        'Q7joint': [capacity_row(lambda s: s[0] == 6, 20), capacity_row(lambda s: s[2] == 0, 21)],
        'R7<=20': [capacity_row(lambda s: s[0] == 6, 20)],
        'DR<=44': [capacity_row(lambda s: s[0] + (s[1] >= 1) + (s[2] >= 1) >= 6, 44)],
        'DR<=35': [capacity_row(lambda s: s[0] + (s[1] >= 1) + (s[2] >= 1) >= 6, 35)],
        'DR<=29': [capacity_row(lambda s: s[0] + (s[1] >= 1) + (s[2] >= 1) >= 6, 29)],
        'R5<=50': [capacity_row(lambda s: s[0] >= 4, 50)],
        'M57<=41': [capacity_row(lambda s: s[0] <= 5, 41)],
    }
    which = sys.argv[1:] or list(tests)
    for name in which:
        h, holes = solve_lazy(tests[name])
        print(name, 'holes', h, 'occupied <=', 84 - h, flush=True)
