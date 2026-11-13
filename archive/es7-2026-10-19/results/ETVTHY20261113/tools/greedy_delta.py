"""Left-to-right greedy: blue stays free of convex k-gons; red = points that would close one. Is red 4-cap-free?"""
import sys, json
sys.path.insert(0, '/home/jay/research/data/etvthy-20261113')
from esgeo import quick
from collections import Counter
def greedy(P, k, rev=False):
    P = sorted(P)
    if rev: P = [(-x, y) for (x, y) in P][::-1]
    blue = []; red = []
    for p in P:
        g = quick(blue + [p])[0] if len(blue) >= 2 else 0
        (red if g >= k else blue).append(p)
    return blue, red
if __name__ == '__main__':
  st = Counter(); sizes = []
  k = int(sys.argv[1])
  for fn in sys.argv[2:]:
      sets = [json.load(open(fn))] if fn.endswith('.json') else [json.loads(l)['P'] for l in open(fn)]
      for P in sets:
          P = [tuple(p) for p in P]
          for rev in (False, True):
              b, r = greedy(P, k, rev)
              mc = quick(r)[1] if len(r) >= 3 else len(r)
              st[(rev, mc)] += 1; sizes.append((len(P), len(r), mc, rev))
  print(dict(st)); print('max red', max(s[1] for s in sizes))
  print([s for s in sizes if s[0] >= 40])
