"""Try to realize abstract samples (jsonl of sample_fl.py) by integer points; verify with the exact checker."""
import sys, json
import realize, fl
from fl import *
fn = sys.argv[1]; tries = int(sys.argv[2]) if len(sys.argv) > 2 else 3; rounds = int(sys.argv[3]) if len(sys.argv) > 3 else 30
seen = set()
for line in open(fn):
    d = json.loads(line)
    if d['sig'] in seen: continue
    seen.add(d['sig'])
    for seed in range(tries):
        P, info = realize.realize(d['n'], d['sig'], rounds=rounds, seed=seed)
        if P:
            S = Set66(P); assert S.ok and S.in_state == d['in_states'], 'states differ'
            E = sum(1 for f in S.in_f if f[0] == 4); A = sum(1 for f in S.in_f if f[3] >= 1); X = sum(1 for f in S.in_f if f[0] == 4 and f[3] >= 1)
            print('REALIZED sample seed', d['seed'], 'n', S.n, 'E', E, 'A', A, 'X', X, 'lp seed', seed, 'round', info, flush=True)
            with open(fn.replace('.jsonl', '_real.jsonl'), 'a') as f: f.write(json.dumps({'src': fn, 'sample_seed': d['seed'], 'E': E, 'A': A, 'X': X, 'P': P}) + '\n')
            break
        else: print('failed sample seed', d['seed'], 'lp seed', seed, 'best margin', info, flush=True)
