"""Exact maxima of |E|, |A|, |EuA|, |EnA| over abstract first-layer (a,b)-signotopes, by n (SAT, COMPUTED)."""
import sys, time, json
import fls
from toplevel import N1, cupcap
a, b = int(sys.argv[1]), int(sys.argv[2]); to = float(sys.argv[3]) if len(sys.argv) > 3 else 60
nmax = N1(a, b); best = {}
for what in ('E', 'A', 'EuA', 'EnA'):
    K = 1; row = {}
    for n in range(2, nmax + 1):
        # largest K with SAT at this n (monotone in K); start from previous best
        k = max(1, row.get(n - 1, 1))
        while True:
            st, info, size = fls.run(a, b, n, what, k, to)
            if st == 'SAT': row[n] = k; k += 1
            else:
                if st != 'UNSAT': row[n] = -row.get(n, 0)   # unknown above
                row.setdefault(n, 0); break
    best[what] = row
    print(f'FL({a},{b}) max |{what}| by n:', row, flush=True)
json.dump(best, open(f'small_table_{a}_{b}.json', 'w'))
