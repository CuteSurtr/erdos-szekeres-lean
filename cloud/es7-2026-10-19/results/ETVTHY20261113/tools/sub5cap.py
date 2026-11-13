"""5-cap-free subsets of the 64-point octagon-free family (greedy, random orders), saved as a test pool."""
import sys, json, random, glob
sys.path.insert(0, '/home/jay/research/data/etvthy-20261113')
from esgeo import quick
D = '/home/jay/research/lean/erdos-szekeres-lean/experiments/es8-lower-bound-search-2026-10-11/family/sets/'
files = sorted(glob.glob(D + '*.txt'))
random.seed(7); out = open('pool_sub64.jsonl', 'w')
for fn in random.sample(files, 120):
    P = [tuple(map(int, l.split())) for l in open(fn) if l.strip()]
    best = []
    for rep in range(6):
        order = P[:]; random.shuffle(order); S = []
        for p in order:
            T = S + [p]
            if len(T) < 5 or quick(T)[1] <= 4: S = T
        if len(S) > len(best): best = S
    out.write(json.dumps({'src': fn.split('/')[-1], 'P': sorted(best)}) + '\n'); out.flush()
