#!/usr/bin/env python3
"""LP bounds of the present catalogs plus capacity rows on level-set supports.

Level-set families (owners' forbidden chains are proved in the README):
  residual F   = {f1>=5}            owners: no 5-cap            (cup-cap 84, ETV 42)
  residual Lo  = {f1<=4}            owners: no 6-cup, no 6-cap  (cup-cap 70, ETV 50)
  balanced X56 = {f1=f2=5}          owners: no 5-cap, no 7-cup  (cup-cap 56, ETV 41)
  balanced X56m= {f5>=2}            owners: no 5-cup, no 7-cap  (56, 41)
  balanced X70 = {f1=5, f5>=1}      owners: no 6-cup, no 6-cap  (70, 50)
  balanced Hi  = {f1=5}             owners: no 6-cap, no 7-cup  (126, 56)
  balanced Him = {f5>=1}            owners: no 6-cup, no 7-cap  (126, 56)
  balanced Lo  = {f1<=4}            owners: no 6-cup, no 7-cap  (126, 56)
  balanced Lom = {f5=0}             owners: no 6-cap, no 7-cup  (126, 56)
Capacity c on support X adds the row h(X) >= |X| - c.
"""
import gzip, json, sys
import numpy as np
import highspy

ROOT = '/home/jay/research/lean/erdos-szekeres-lean/'
res = json.load(gzip.open(ROOT + 'experiments/omission-residual32-rank-global-2026-10-10/source-2650.json.gz'))
bal = json.load(open(ROOT + 'experiments/omission-cover-certificates-2026-10-10/balanced-v2-source.json'))

def lp(states, rows, extra, fixed0, integer=False, tl=60):
    h = highspy.Highs(); h.silent(); h.setOptionValue('threads', 1)
    h.setOptionValue('time_limit', float(tl))
    n = len(states); inf = highspy.kHighsInf
    for i in range(n):
        h.addVar(0.0, 0.0 if (fixed0 and i == 0) else 1.0)
        h.changeColCost(i, 1.0)
        if integer:
            h.changeColIntegrality(i, highspy.HighsVarType.kInteger)
    for r in list(rows) + list(extra):
        sup = r['support']
        h.addRow(float(r['rhs']), inf, len(sup), np.array(sup, dtype=np.int32), np.ones(len(sup)))
    h.run()
    info = h.getInfo()
    return info.objective_function_value, (info.mip_dual_bound if integer else None)

def fam(states, pred):
    return [i for i, s in enumerate(states) if pred(s)]

if __name__ == '__main__':
    RS, RC = res['states'], res['constraints']
    BS, BC = bal['states'], bal['constraints']
    out = {}
    rf = {'F': fam(RS, lambda s: s[0] >= 5), 'Lo': fam(RS, lambda s: s[0] <= 4)}
    print('residual base LP', lp(RS, RC, [], True)[0])
    for name, X in rf.items():
        for c in [60, 55, 50, 46, 42]:
            if c >= len(X):
                continue
            v = lp(RS, RC, [{'support': X, 'rhs': len(X) - c}], True)[0]
            print(f'residual {name} |X|={len(X)} c={c}: LP {v:.3f}', flush=True)
            out[f'res-{name}-{c}'] = v
    v = lp(RS, RC, [{'support': rf['F'], 'rhs': 84 - 42}, {'support': rf['Lo'], 'rhs': 70 - 50}], True)[0]
    print(f'residual both ETV: LP {v:.3f}'); out['res-both-etv'] = v
    bf = {'X56': fam(BS, lambda s: s[0] == 5 and s[1] == 5), 'X56m': fam(BS, lambda s: s[4] >= 2),
          'X70': fam(BS, lambda s: s[0] == 5 and s[4] >= 1), 'Hi': fam(BS, lambda s: s[0] == 5),
          'Him': fam(BS, lambda s: s[4] >= 1), 'Lo': fam(BS, lambda s: s[0] <= 4),
          'Lom': fam(BS, lambda s: s[4] == 0)}
    etv = {'X56': 41, 'X56m': 41, 'X70': 50, 'Hi': 56, 'Him': 56, 'Lo': 56, 'Lom': 56}
    print('balanced base LP', lp(BS, BC, [], False)[0])
    for name, X in bf.items():
        for c in sorted({etv[name], etv[name] + 5, etv[name] + 10, etv[name] + 15}):
            if c >= len(X):
                continue
            v = lp(BS, BC, [{'support': X, 'rhs': len(X) - c}], False)[0]
            print(f'balanced {name} |X|={len(X)} c={c}: LP {v:.3f}', flush=True)
            out[f'bal-{name}-{c}'] = v
    allrows = [{'support': X, 'rhs': len(X) - etv[k]} for k, X in bf.items()]
    v = lp(BS, BC, allrows, False)[0]
    print(f'balanced all ETV rows: LP {v:.3f}'); out['bal-all-etv'] = v
    json.dump(out, open('cap_lp_out.json', 'w'), indent=1)
