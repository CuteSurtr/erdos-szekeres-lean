import json, random, sys, collections
sys.path.insert(0, '.')
import coupled
rows = json.load(open('newrows.json'))
tr = [r for r in rows if r.get('kind') == 'transport']
cores = [r for r in rows if r.get('kind') == 'core']
print('rows', len(rows), 'cores', len(cores), 'transport', len(tr), collections.Counter(len(r['support']) for r in rows).most_common(6))
print('9-state cores:', [r['support'] for r in cores if len(r['support']) <= 10])
rng = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 1)
sample = rng.sample(tr, min(60, len(tr)))
bad = 0; res = collections.Counter()
for r in sample:
    st = coupled.fast_solve(r['support'], seconds=60)
    res[st] += 1
    if st != 'unsat':
        bad += 1; print('NOT UNSAT', st, r['support'], r['core'])
print('spot check', dict(res), 'bad', bad)
