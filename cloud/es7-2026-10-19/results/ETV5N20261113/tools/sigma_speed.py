import json, time, random, sys
sys.argv = ['x', 'final18/subset18_rows.json', '/tmp/none', '1']
import importlib.util
spec = importlib.util.spec_from_file_location('tc', 'template_cert.py'); tc = importlib.util.module_from_spec(spec); spec.loader.exec_module(tc)
import transport5
def find_sigma2(core, tests, image):
    k = len(core); img = sorted(image)
    sc = [transport5.scope(t) for t in tests]
    checks = [[(t, s) for t, s in zip(tests, sc) if i in s] for i in range(k)]
    sig = [None] * k
    def dfs(assigned, used):
        if len(assigned) == k: return True
        best = None
        for i in range(k):
            if i in assigned: continue
            ready = [t for t, s in checks[i] if s - {i} <= assigned]
            opts = []
            for v in img:
                if v in used: continue
                sig[i] = v
                if all(transport5.good(t, sig) for t in ready): opts.append(v)
            sig[i] = None
            if not opts: return False
            if best is None or (len(opts), -len(ready)) < best[0]: best = ((len(opts), -len(ready)), i, opts)
        _, i, opts = best
        for v in opts:
            sig[i] = v
            if dfs(assigned | {i}, used | {v}): return True
        sig[i] = None
        return False
    return list(sig) if dfs(frozenset(), frozenset()) else None
rows = json.load(open('final18/subset18_rows.json'))
rng = random.Random(3); sample = rng.sample(rows, 300)
t1 = t2 = 0; agree = 0; n = 0; slow = []
for s, d in sample:
    S = tuple(sorted(s)); core = tc.tr.get(S)
    if core is None: continue
    for tests in tc.tmpls.get(tuple(core), []):
        a = time.time(); g2 = find_sigma2(core, tests, S); t2 += time.time() - a
        a = time.time(); g1 = tc.find_sigma(core, tests, S) if True else None; dt = time.time() - a; t1 += dt
        if dt > 1: slow.append(round(dt, 1))
        agree += (g1 is None) == (g2 is None); n += 1
        if g2 is not None: break
print('pairs', n, 'agree', agree, 'old total s', round(t1, 1), 'new total s', round(t2, 1), 'slow old', slow[:10])
