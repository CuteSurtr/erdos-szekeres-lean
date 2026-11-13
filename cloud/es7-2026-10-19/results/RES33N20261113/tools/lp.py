import sys, json
sys.path.insert(0, '.')
import highspy, numpy as np
from common import N, ROWS
import os
def load_rows():
    rows = list(ROWS); seen = {s for s, d in rows if d >= 1}
    tpl = json.load(open('templates.json')); ntpl = 0
    for name, v in tpl.items():
        for s in v['supports']:
            s = tuple(sorted(s))
            if s not in seen: seen.add(s); rows.append((s, 1)); ntpl += 1
    nnew = 0
    if os.path.exists('newrows.json'):
        for r in json.load(open('newrows.json')):
            s = tuple(sorted(r['support']))
            if s not in seen: seen.add(s); rows.append((s, 1)); nnew += 1
    return rows, ntpl, nnew
def lp(rows):
    h = highspy.Highs(); h.setOptionValue('output_flag', False)
    v = [h.addVariable(lb=0, ub=1, obj=1) for _ in range(N)]
    h.changeColBounds(0, 0, 0)
    for s, d in rows: h.addConstr(h.qsum(v[i] for i in s) >= d)
    h.run(); return h.getObjectiveValue()
base = [(s, d) for s, d in ROWS]
rows, ntpl, nnew = load_rows()
print('LP catalog 2650:', round(lp(base), 4))
print('LP + templates + newrows (%d,%d):' % (ntpl, nnew), round(lp(rows), 4))
