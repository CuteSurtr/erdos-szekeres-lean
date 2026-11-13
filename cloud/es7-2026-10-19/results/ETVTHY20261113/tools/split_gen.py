"""Generic split test: can a set with no convex (k+1)-gon be 2-coloured with no monochromatic convex k-gon?"""
import sys, json, time
sys.path.insert(0, '/home/jay/research/data/etvthy-20261113')
from split2 import split
from collections import Counter
if __name__ == '__main__':
    k = int(sys.argv[1]); st = Counter()
    for fn in sys.argv[2:]:
        for si, l in enumerate(open(fn)):
            P = [tuple(p) for p in json.loads(l)['P']]
            r = split(P, k, tmax=300)
            st[r[0]] += 1
            if r[0] != 'OK': print('NOT OK', fn, si, len(P), r, flush=True)
    print('k', k, dict(st), flush=True)
