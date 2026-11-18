#!/usr/bin/env python3
"""Differential test of fastbb's LP against HiGHS (reference only; neither is evidence of anything).

Usage: lp_difftest.py SOURCE.json.gz EXTRA.json|- DUMP.txt [OUT.json]

DUMP.txt comes from `fastbb lptest ROWS BUDGET DIVES SEED DUMP.txt`: one line per LP,
  status value nM m_1..m_nM nO o_1..o_nO      (status 0 = optimal, 1 = infeasible)
The LP is  min sum h  s.t.  row sums >= rhs,  0 <= h <= 1,  h = 1 on missing, h = 0 on occupied.
fastbb's value is its unperturbed dual bound at the final basis; HiGHS' value is its objective.
"""
import gzip, json, sys
import numpy as np
import highspy


def main():
    src, extra, dump = sys.argv[1], sys.argv[2], sys.argv[3]
    d = json.load(gzip.open(src))
    n = len(d['states'])
    rows = [(r['support'], r['rhs']) for r in d['constraints']]
    if extra != '-':
        rows += [(r['support'], r['rhs']) for r in json.load(open(extra))]
    h = highspy.Highs()
    h.setOptionValue('output_flag', False)
    h.setOptionValue('threads', 1)
    h.setOptionValue('presolve', 'off')
    v = [h.addVariable(lb=0, ub=1, obj=1) for _ in range(n)]
    for s, dem in rows:
        h.addConstr(h.qsum(v[i] for i in s) >= dem)
    idx = np.arange(n, dtype=np.int32)
    OPT, INF = highspy.HighsModelStatus.kOptimal, highspy.HighsModelStatus.kInfeasible
    total = opt = inf = status_mismatch = other = 0
    maxdiff = 0.0
    worst = None
    diffs = []
    for line in open(dump):
        t = line.split()
        st, val, nm = int(t[0]), float(t[1]), int(t[2])
        miss = [int(x) for x in t[3:3 + nm]]
        no = int(t[3 + nm])
        occ = [int(x) for x in t[4 + nm:4 + nm + no]]
        lo = np.zeros(n); hi = np.ones(n)
        lo[miss] = 1.0; hi[occ] = 0.0
        h.changeColsBounds(n, idx, lo, hi)
        h.run()
        hst = h.getModelStatus()
        if hst != OPT and hst != INF:
            h.clearSolver(); h.run(); hst = h.getModelStatus()
        total += 1
        if st not in (0, 1) or hst not in (OPT, INF):
            other += 1
            continue
        if (st == 0) != (hst == OPT):
            status_mismatch += 1
            continue
        if st == 0:
            opt += 1
            diff = abs(val - h.getObjectiveValue())
            diffs.append(diff)
            if diff > maxdiff:
                maxdiff, worst = diff, {'fastbb': val, 'highs': h.getObjectiveValue(), 'missing': miss, 'occupied': occ}
        else:
            inf += 1
    diffs.sort()
    res = {'lps': total, 'both_optimal': opt, 'both_infeasible': inf, 'status_mismatch': status_mismatch,
           'other_status': other, 'max_abs_value_diff': maxdiff,
           'median_abs_value_diff': diffs[len(diffs) // 2] if diffs else None,
           'p99_abs_value_diff': diffs[int(len(diffs) * 0.99)] if diffs else None, 'worst': worst}
    print(json.dumps(res))
    if len(sys.argv) > 4:
        json.dump(res, open(sys.argv[4], 'w'), indent=1)


if __name__ == '__main__':
    main()
