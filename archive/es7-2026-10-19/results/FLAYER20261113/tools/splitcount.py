"""Number of valid strong splits of abstract FL(5,5) configurations on 14 points (exact, numpy bitmasks)."""
import sys, json, itertools
import numpy as np
n = 14; a = b = 5
ALL = np.arange(1 << n, dtype=np.int64); FULL = (1 << n) - 1
T3 = list(itertools.combinations(range(n), 3)); T4 = list(itertools.combinations(range(n), 4))
def count(sig):
    sg = {t: (1 if c == '+' else -1) for t, c in zip(T3, sig)}
    caps4 = [t for t in T4 if sg[t[0], t[1], t[2]] < 0 and sg[t[1], t[2], t[3]] < 0]
    cups4 = [t for t in T4 if sg[t[0], t[1], t[2]] > 0 and sg[t[1], t[2], t[3]] > 0]
    caps3 = [t for t in T3 if sg[t] < 0]; cups3 = [t for t in T3 if sg[t] > 0]
    m = lambda s: sum(1 << p for p in s)
    def gons(caps, cups):
        by = {}
        for c in cups: by.setdefault((c[0], c[-1]), []).append(c)
        return [m(set(c) | set(u)) for c in caps for u in by.get((c[0], c[-1]), [])]
    bad1 = set(m(c) for c in caps4) | set(gons(caps3, cups4)); bad2 = set(m(c) for c in cups4) | set(gons(caps4, cups3))
    ok = np.ones(1 << n, dtype=bool)
    for x in bad1: ok &= (ALL & x) != x
    comp = FULL ^ ALL
    for x in bad2: ok &= (comp & x) != x
    return int(ok.sum())
if __name__ == '__main__':
    d = json.load(open(sys.argv[1])); cs = []
    for M, m_, sig in d['maximal']:
        if m_ == n: cs.append(count(sig))
    cs.sort()
    print('abstract FL(5,5) witnesses with 14 points:', len(cs), 'number of valid strong splits: min', cs[0], 'median', cs[len(cs)//2], 'max', cs[-1])
    print('smallest ten:', cs[:10])
