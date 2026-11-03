#!/usr/bin/env python3
"""run.py LANES DEADLINE_EPOCH : solve cubes/*.cnf (inconsistent phase patterns first) on LANES workers,
each with LRAT; check every UNSAT proof with lrat-check in the same lane. Limits = time left to DEADLINE."""
import sys, os, subprocess, time, itertools, threading, queue
P = os.environ['P']; B = os.environ['S'] + '/resolve/bin'   # P: work dir with cubes/; S: dir with resolve/bin
lanes, deadline = int(sys.argv[1]), float(sys.argv[2])
def consistent(name):           # bits for Y13,Y14,Y23,Y24,Y34 with Y12 = 1
    b = dict(zip(('13', '14', '23', '24', '34'), map(int, name[1:6]))); b['12'] = 1
    less = lambda i, j: b['%d%d' % (i, j)] if i < j else 1 - b['%d%d' % (j, i)]
    return any(all(less(p[k], p[k + 1]) for k in range(3)) and all(less(p[a], p[c]) for a in range(4) for c in range(a + 1, 4))
               for p in itertools.permutations((1, 2, 3, 4)))
names = sorted(f[:-4] for f in os.listdir(P + '/cubes') if f.startswith('c') and f.endswith('.cnf'))
names.sort(key=consistent)
q = queue.Queue(); [q.put(n) for n in names]
lock = threading.Lock()
def log(s):
    with lock:
        with open(P + '/results.txt', 'a') as f: f.write(time.strftime('%H:%M:%S ') + s + '\n')
def worker():
    while True:
        try: n = q.get_nowait()
        except queue.Empty: return
        left = int(deadline - time.time())
        if left < 30: log('%s skipped (deadline)' % n); continue
        cnf, lrat = P + '/cubes/%s.cnf' % n, P + '/cubes/%s.lrat' % n
        t0 = time.time()
        with open(P + '/logs/cad_%s.out' % n, 'w') as o:
            ec = subprocess.call([B + '/cadical', '-t', str(left), '--lrat', '--binary=false', cnf, lrat], stdout=o, stderr=subprocess.STDOUT)
        dt = time.time() - t0
        res = {10: 'SAT', 20: 'UNSAT'}.get(ec, 'UNKNOWN(%d)' % ec)
        log('%s consistent=%s %s %.1fs' % (n, consistent(n), res, dt))
        if ec == 20:
            r = subprocess.run([B + '/lrat-check', cnf, lrat], capture_output=True, text=True)
            v = [l for l in (r.stdout + r.stderr).splitlines() if 'VERIFIED' in l or 'FAIL' in l]
            log('%s lrat-check: %s' % (n, v[:1]))
        elif ec != 10 and os.path.exists(lrat):
            os.remove(lrat)
ts = [threading.Thread(target=worker) for _ in range(lanes)]
[t.start() for t in ts]; [t.join() for t in ts]
log('runner done')
