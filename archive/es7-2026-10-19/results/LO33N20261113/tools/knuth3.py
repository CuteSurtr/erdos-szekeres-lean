"""Knuth random-dive estimate using the production slice engine itself (pbb_fast.FastSlice.expand), so the
estimate refers to exactly the rule that is run.  HEURISTIC.
Usage: knuth3.py extra.json dives seed out.json   (env: K_TOP, D_TOP, K_LOW, LO_PC)"""
import os, sys, json, math, random, time
for k in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS'): os.environ[k] = '1'
os.environ.setdefault('K_TOP', '16'); os.environ.setdefault('D_TOP', '8'); os.environ.setdefault('K_LOW', '4')
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
extra, dives, seed, out = os.path.abspath(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), os.path.abspath(sys.argv[4])
os.chdir('/home/jay/research/lean/erdos-szekeres-lean')
import pbb_fast as Q
BUD = int(os.environ.get('LO_BUDGET', '33'))
Q.init(extra, BUD); s = Q.G['s']; rng = random.Random(seed)
ests, depths, wit = [], [], []; t0 = time.time()
for dv in range(dives):
    m, o, d, tot, w = 0, 1, 0, 1.0, 1.0
    while True:
        kind, val = s.expand(m, o)
        if kind == 'witness': wit.append(val); break
        if kind == 'leaf': break
        if rng.random() < 0.5: o |= 1 << val
        else: m |= 1 << val
        d += 1; w *= 2; tot += w
    ests.append(tot); depths.append(d); mu = sum(ests) / len(ests)
    rec = {'extra': os.path.basename(extra), 'pc': Q.PC, 'K': [os.environ['K_TOP'], os.environ['D_TOP'], os.environ['K_LOW']], 'dives': dv + 1,
           'log10_mean_nodes': round(math.log10(mu), 3), 'median_depth': sorted(depths)[len(depths) // 2], 'max_depth': max(depths),
           'witnesses': len(wit), 't': round(time.time() - t0)}
    print(json.dumps(rec), flush=True)
    json.dump({**rec, 'ests': ests, 'depths': depths, 'witness_vectors': wit}, open(out, 'w'))
