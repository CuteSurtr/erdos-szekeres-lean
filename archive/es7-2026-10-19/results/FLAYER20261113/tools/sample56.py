"""Sampling test of the Pascal split for FL(5,6) (the class of Schroeder's M7(5,6) = 25): abstract 25-point
configurations from CaDiCaL with random seeds, each tested with split.split (and re-checked)."""
import sys, os, itertools, subprocess, json, time
import fls, split
n = int(sys.argv[1]); seeds = range(int(sys.argv[2]), int(sys.argv[3]))
HERE = os.path.dirname(os.path.abspath(__file__))
w = fls.FL(5, 6, n); cnf = os.path.join(HERE, 'tmp', f'fl56_{n}.cnf'); open(cnf, 'w').write(w.dimacs())
T = list(itertools.combinations(range(n), 3)); seen = set(); nosplit = 0; t0 = time.time()
for seed in seeds:
    import random
    rr = random.Random(seed); units = [(w.o[t] if rr.random() < 0.5 else -w.o[t]) for t in rr.sample(T, 10)]
    cnf2 = cnf + '.%d' % seed
    with open(cnf2, 'w') as f2:
        f2.write('p cnf %d %d\n' % (w.nv, len(w.cl) + len(units)))
        for c in w.cl: f2.write(' '.join(map(str, c)) + ' 0\n')
        for u in units: f2.write('%d 0\n' % u)
    r = subprocess.run(['/usr/bin/cadical', '-q', '-t', '20', f'--seed={seed}', cnf2], capture_output=True, text=True)
    os.remove(cnf2)
    if r.returncode != 10: continue
    model = set()
    for line in r.stdout.splitlines():
        if line.startswith('v '):
            for tok in line.split()[1:]:
                x = int(tok)
                if x > 0: model.add(x)
    info = fls.check_model(5, 6, n, w.o, model); assert info[0] <= 4 and info[1] <= 5 and not info[2]
    sig = ''.join('+' if w.o[t] in model else '-' for t in T)
    if sig in seen: continue
    seen.add(sig); f = split.sig_fn(n, sig)
    ok, S1, ncl = split.split(n, f, 5, 6)
    if ok: assert split.check_split(n, f, 5, 6, S1)
    else:
        nosplit += 1; json.dump({'a': 5, 'b': 6, 'n': n, 'sig': sig}, open(f'split_counterexample_5_6_{n}_{seed}.json', 'w'))
        print('NO SPLIT: seed', seed, flush=True)
print(f'FL(5,6) n={n}: {len(seen)} distinct abstract configurations, {nosplit} without strong split, {time.time()-t0:.0f}s', flush=True)
os.remove(cnf)
