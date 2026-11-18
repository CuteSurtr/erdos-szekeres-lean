"""Top-level conjecture in small first-layer cases (abstract model): for every n up to the maximum size,
is 'at least K points of the class' satisfiable?  K = conjectured bound + 1."""
import sys, time, json
import fls
def N1(a, b):
    from math import comb
    return comb(a + b - 4, a - 2) - (comb(a + b - 6, a - 3) if a >= 3 and b >= 3 else 0)
def cupcap(a, b):
    from math import comb
    return comb(a + b - 4, a - 2)
if __name__ == '__main__':
    a, b = int(sys.argv[1]), int(sys.argv[2]); to = float(sys.argv[3]) if len(sys.argv) > 3 else 120
    out = sys.argv[4] if len(sys.argv) > 4 else 'toplevel.jsonl'
    nmax = N1(a, b)
    tests = [('E', N1(a - 1, b) + 1), ('A', N1(a, b - 1) + 1), ('EuA', nmax - cupcap(a - 1, b - 1) + 1)]
    for what, K in tests:
        res = {}
        for n in range(K, nmax + 1):
            t0 = time.time(); st, info, size = fls.run(a, b, n, what, K, to)
            res[n] = st
            print(f'FL({a},{b}) n={n} |{what}|>={K}: {st} {info} {time.time()-t0:.1f}s', flush=True)
            if st != 'UNSAT': break
        verdict = 'HOLDS (UNSAT for all n<=%d)' % nmax if all(v == 'UNSAT' for v in res.values()) else 'FAILS/UNKNOWN'
        print(f'== FL({a},{b}): |{what}| <= {K-1}: {verdict}', flush=True)
        with open(out, 'a') as f: f.write(json.dumps({'a': a, 'b': b, 'what': what, 'K': K, 'res': res, 'verdict': verdict}) + '\n')
