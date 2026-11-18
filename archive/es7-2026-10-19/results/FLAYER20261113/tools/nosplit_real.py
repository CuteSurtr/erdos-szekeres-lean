"""Try to realize the abstract no-split FL(5,5) configuration by real points (annealing on wrong triples),
then verify everything exactly on the real set."""
import sys, json, random, itertools
import realize_small
from esgeo import Analysis
d = json.load(open(sys.argv[1])); n, sig = d['n'], d['sig']
tries = int(sys.argv[2]) if len(sys.argv) > 2 else 6; iters = int(sys.argv[3]) if len(sys.argv) > 3 else 400000
rng = random.Random(int(sys.argv[4]) if len(sys.argv) > 4 else 11)
for t in range(tries):
    P = realize_small.realize(n, sig, rng, iters)
    print('attempt', t, 'realized' if P else 'failed', flush=True)
    if P:
        A = Analysis(P); print('real set: maxcap', int(A.capB.max()), 'maxcup', int(A.cupB.max()), 'gon', A.gon())
        json.dump({'a': d['a'], 'b': d['b'], 'n': n, 'sig': sig, 'P': P}, open(sys.argv[1].replace('.json', '_points.json'), 'w'))
        break
