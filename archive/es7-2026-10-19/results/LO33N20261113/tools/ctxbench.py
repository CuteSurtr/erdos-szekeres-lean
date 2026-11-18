"""Benchmark engine variants on the SAME contexts (time to close them).  Usage: ctxbench.py outdir cid1,cid2,... [maxnodes]"""
import os, sys, json, time
for k in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS'): os.environ[k] = '1'
os.environ.setdefault('K_TOP', '16'); os.environ.setdefault('D_TOP', '8'); os.environ.setdefault('K_LOW', '4')
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
os.chdir('/home/jay/research/lean/erdos-szekeres-lean')
import pbb_fast as Q
out = sys.argv[1]; cids = [int(x) for x in sys.argv[2].split(',')]; MAXN = int(sys.argv[3]) if len(sys.argv) > 3 else 10**9
master = json.load(open(os.path.join(out, 'master.json')))
Q.init(master['extra'], 33); s = Q.G['s']
fr = {int(c): (int(m), int(o)) for c, m, o in master['frontier']}
tot_n = 0; tot_t = 0.0; res = []
for cid in cids:
    s.reset_lazy(); m, o = fr[cid]; stack = [(m, o)]; n = 0; t = time.time(); wit = 0
    while stack and n < MAXN:
        mm, oo = stack.pop(); kind, val = s.expand(mm, oo); n += 1
        if kind == 'witness': wit += 1; continue
        if kind == 'branch':
            stack.append((mm, oo | (1 << val))); stack.append((mm | (1 << val), oo))
    dt = time.time() - t; tot_n += n; tot_t += dt; res.append((cid, n, round(dt, 1), 'open' if stack else 'closed', wit))
print(json.dumps({'K_LOW': os.environ['K_LOW'], 'ITLIM': Q.ITLIM, 'HS_OPTS': os.environ.get('HS_OPTS'), 'nodes': tot_n, 'seconds': round(tot_t, 1),
                  'n_per_s': round(tot_n / tot_t, 1), 'per_ctx': res}), flush=True)
