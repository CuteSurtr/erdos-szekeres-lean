#!/usr/bin/env python3
"""Full balanced budget-64 search (route to ES(8) <= 310): run run_context.py on every one of the 4,096 depth-12 contexts.

Restart-safe and duplicate-free: a context counts as done when runs/ctx-<k>-b64.result.json has status 'closed'; a
context whose run_context.py process is alive (any parent, cwd = this directory) is never started again.  Order:
the LOWEST_LP contexts with the smallest budget-64 root LP first (most likely to hold a witness), then the rest by
decreasing budget-63 subtree size (largest first, so the tail is short).
Every 30 s: health (pause the youngest worker on Tctl >= 95 C for 2 cycles or MemAvailable < 4 GiB; resume when clear;
no new job below 450 GB free disk), reap finished jobs, start new ones up to WORKERS, write campaign/STATUS.
  exit 0 closed -> done;  3 witness -> campaign/WITNESS-ALERT.txt, no new jobs (running ones finish);
  4 capped (12 h) -> requeued once with no cap;  other -> retried once, then recorded as failed.
At the cutoff (file campaign/cutoff, epoch seconds) running workers get SIGTERM and the campaign stops; finished
contexts are kept.  Nothing is ever deleted.
"""
import os, sys, json, time, signal, subprocess, glob
HERE = os.path.dirname(os.path.abspath(__file__))
C = os.path.join(HERE, 'campaign'); os.makedirs(C, exist_ok=True)
PY = '<venv>/bin/python'
WORKERS = int(os.environ.get('WORKERS', '28')); LOWEST_LP = 64; CAP = 12 * 3600
LOG = os.path.join(C, 'campaign.log')

def log(m):
    with open(LOG, 'a') as f: f.write(time.strftime('%Y-%m-%d %H:%M:%S ') + m + '\n')

def result(k):
    p = os.path.join(HERE, 'runs', 'ctx-%d-b64.result.json' % k)
    try: return json.load(open(p))
    except Exception: return None

def alive():
    """ctx -> pid for live run_context.py --budget 64 processes started in this directory"""
    out = {}
    for p in os.listdir('/proc'):
        if not p.isdigit(): continue
        try:
            argv = [a.decode() for a in open('/proc/%s/cmdline' % p, 'rb').read().split(b'\0') if a]
            if os.readlink('/proc/%s/cwd' % p) != HERE: continue
        except Exception: continue
        if any(a.endswith('run_context.py') for a in argv) and '--budget' in argv and argv[argv.index('--budget') + 1] == '64':
            out[int(argv[argv.index('--ctx') + 1])] = int(p)
    return out

def order():
    ctx = [json.loads(l) for l in open(os.path.join(HERE, 'contexts.jsonl'))]
    size = {c['ctx']: c.get('b63_leaves', c.get('leaves', 0)) for c in ctx}
    lp = {}
    for l in open(os.path.join(HERE, 'lp_screen.jsonl')):
        d = json.loads(l); lp[d['ctx']] = d['lp']
    low = sorted(lp, key=lambda k: lp[k])[:LOWEST_LP]
    rest = sorted((k for k in size if k not in set(low)), key=lambda k: -size[k])
    return low + rest, size

def health():
    t = None
    for h in glob.glob('/sys/class/hwmon/hwmon*/name'):
        try:
            if open(h).read().strip() == 'k10temp': t = int(open(os.path.join(os.path.dirname(h), 'temp1_input')).read()) / 1000
        except Exception: pass
    mi = {}
    for line in open('/proc/meminfo'):
        k, v = line.split(':'); mi[k] = int(v.split()[0]) * 1024
    st = os.statvfs(HERE)
    return t, mi['MemAvailable'], st.f_bavail * st.f_frsize

def pstate(pid):
    try: return open('/proc/%d/stat' % pid).read().rsplit(')', 1)[1].split()[0]
    except Exception: return None

def pstart(pid):
    try: return int(open('/proc/%d/stat' % pid).read().rsplit(')', 1)[1].split()[19])
    except Exception: return 0

def main():
    import fcntl
    lk = open(os.path.join(C, 'campaign.lock'), 'w')
    try: fcntl.flock(lk, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except OSError: print('another campaign holds the lock'); return
    seq, size = order(); attempts = {}; capped_once = set(); children = {}
    log('campaign start pid %d, workers %d, contexts %d' % (os.getpid(), WORKERS, len(seq)))
    hot = 0; stop_new = os.path.exists(os.path.join(C, 'WITNESS-ALERT.txt'))
    while True:
        cut = int(open(os.path.join(C, 'cutoff')).read().split()[0])
        live = alive()
        for k, pr in list(children.items()):          # reap our own children
            rc = pr.poll()
            if rc is None: continue
            del children[k]; r = result(k)
            if rc == 0 and r and r.get('status') == 'closed':
                log('closed ctx %d nodes %d leaves %d cpu %.0fs' % (k, r['nodes'], r['leaves'], r.get('cpu_seconds', r.get('seconds', 0))))
            elif rc == 3:
                stop_new = True
                with open(os.path.join(C, 'WITNESS-ALERT.txt'), 'a') as f:
                    f.write('%s ctx %d witness: %s\n' % (time.strftime('%Y-%m-%d %H:%M:%S'), k, json.dumps({x: (r or {}).get(x) for x in ('witness_holes', 'witness_exact_valid')})))
                log('WITNESS in ctx %d (exact_valid=%s); no new jobs' % (k, (r or {}).get('witness_exact_valid')))
            elif rc == 4:
                capped_once.add(k); log('capped ctx %d; requeue without cap' % k)
            else:
                attempts[k] = attempts.get(k, 0) + 1; log('ERROR ctx %d rc %s (attempt %d)' % (k, rc, attempts[k]))
        done = [k for k in seq if (result(k) or {}).get('status') == 'closed']
        if time.time() >= cut:
            for k, pid in alive().items():
                try: os.kill(pid, signal.SIGCONT); os.kill(pid, signal.SIGTERM)
                except ProcessLookupError: pass
            log('CUTOFF: stopped; closed %d of %d' % (len(done), len(seq))); write_status(seq, size, done, alive(), True); return
        if len(done) == len(seq):
            log('ALL %d CONTEXTS CLOSED' % len(seq)); write_status(seq, size, done, {}, True); return
        t, mem, disk = health()
        hot = hot + 1 if (t is not None and t >= 95) else 0
        running = {k: p for k, p in live.items() if pstate(p) not in ('T', 'Z', None)}
        paused = {k: p for k, p in live.items() if pstate(p) == 'T'}
        if (hot >= 2 or mem < 4 * 2**30) and running:
            k, p = max(running.items(), key=lambda kv: pstart(kv[1])); os.kill(p, signal.SIGSTOP); log('PAUSE ctx %d (tctl %s, mem %.1f GiB)' % (k, t, mem / 2**30))
        elif paused and hot == 0 and (t is None or t <= 85) and mem > 8 * 2**30:
            k, p = min(paused.items(), key=lambda kv: pstart(kv[1])); os.kill(p, signal.SIGCONT); log('RESUME ctx %d' % k)
        if not stop_new and not paused and disk > 450e9 and (t is None or t < 85):
            dset = set(done)
            for k in seq:
                if len(alive()) >= WORKERS: break
                if k in dset or k in live or k in children or attempts.get(k, 0) >= 2: continue
                maxs = 0 if k in capped_once else CAP
                os.makedirs(os.path.join(HERE, 'logs'), exist_ok=True)
                children[k] = subprocess.Popen([PY, 'run_context.py', '--budget', '64', '--ctx', str(k), '--out', 'runs', '--progress', '900',
                                                '--max-seconds', str(maxs)], cwd=HERE, start_new_session=True,
                                               stdout=open(os.path.join(HERE, 'logs', 'ctx-%d-b64.out' % k), 'w'),
                                               stderr=open(os.path.join(HERE, 'logs', 'ctx-%d-b64.err' % k), 'w'))
                live[k] = children[k].pid; log('start ctx %d (b63 leaves %d)' % (k, size.get(k, 0)))
        write_status(seq, size, done, live, False, (t, mem, disk))
        time.sleep(30)

def write_status(seq, size, done, live, final, h=None):
    tot63 = sum(size[k] for k in seq); d63 = sum(size[k] for k in done)
    nodes = sum((result(k) or {}).get('nodes', 0) for k in done)
    d63n = sum((result(k) or {}).get('b63_record_nodes', 2 * size[k]) for k in done)
    ratio = nodes / d63n if d63n else 0
    lines = ['STATUS %s%s' % (time.strftime('%Y-%m-%d %H:%M:%S'), ' (FINAL)' if final else ''),
             'closed %d of %d contexts (%.1f%% of budget-63 leaves); running %d' % (len(done), len(seq), 100 * d63 / tot63, len(live)),
             'budget-64 nodes so far %d; ratio to record budget-63 nodes over closed contexts %.2f' % (nodes, ratio)]
    if h: lines.append('health: Tctl %s C, MemAvailable %.1f GiB, disk free %.0f GB' % (h[0], h[1] / 2**30, h[2] / 1e9))
    if os.path.exists(os.path.join(C, 'WITNESS-ALERT.txt')): lines.append('WITNESS ALERT: see campaign/WITNESS-ALERT.txt')
    open(os.path.join(C, 'STATUS'), 'w').write('\n'.join(lines) + '\n')

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--dry':
        seq, size = order(); done = [k for k in seq if (result(k) or {}).get('status') == 'closed']
        print(json.dumps({'contexts': len(seq), 'closed_already': len(done), 'alive_b64': alive(), 'first10': seq[:10],
                          'first10_sizes': [size[k] for k in seq[:10]], 'health': health()}, indent=1))
    else:
        main()
