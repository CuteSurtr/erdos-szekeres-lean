#!/usr/bin/env python3
"""Mac share of the balanced budget-64 search (ES(8) <= 310 route): run tools/run_context.py (the byte-identical
copy of the Linux campaign's driver, sha256 1937e9dc...) on the contexts at positions FLOOR..4096 of the Linux
campaign order (64 lowest-LP contexts, then decreasing budget-63 subtree size), smallest first, skipping every context
listed in skip_closed.txt (closed on the Linux machine) or already closed here (runs/ctx-<k>-b64.result.json with
status 'closed'). The same file layout as the Linux campaign, so the two runs/ directories can be merged.

Control files in campaign/: max_running (workers, default 15), floor (lowest position to run, default 2040), STOP
(no new jobs; running ones finish), WITNESS-ALERT.txt (written on a witness; no new jobs).
Every 20 s: reap jobs, start new ones up to max_running (not below 15 GB free disk or with memory pressure high),
write campaign/STATUS. Exit 0 closed, 3 witness, 4 capped, other: retried once, then recorded as failed.
Nothing is ever deleted. Restart-safe: a context whose run_context.py is alive is never started again.
"""
import fcntl, json, os, subprocess, sys, time
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
C = os.path.join(HERE, 'campaign'); os.makedirs(C, exist_ok=True)
RUNS = os.path.join(HERE, 'runs'); LOGS = os.path.join(HERE, 'logs', 'ctx'); os.makedirs(LOGS, exist_ok=True)
PY = os.path.join(HERE, 'venv', 'bin', 'python')
REPO = os.environ['ES_REPO']
LOG = os.path.join(C, 'campaign.log')


def log(m):
    with open(LOG, 'a') as f:
        f.write(time.strftime('%Y-%m-%d %H:%M:%S ') + m + '\n')


def ctl(name, default):
    try:
        return int(open(os.path.join(C, name)).read().split()[0])
    except Exception:
        return default


def result(k):
    try:
        return json.load(open(os.path.join(RUNS, 'ctx-%d-b64.result.json' % k)))
    except Exception:
        return None


def alive():
    """ctx -> pid of live run_context.py --budget 64 processes (any parent)"""
    out = {}
    ps = subprocess.run(['ps', '-ww', '-axo', 'pid=,command='], capture_output=True, text=True).stdout
    for line in ps.splitlines():
        pid, _, cmd = line.strip().partition(' ')
        a = cmd.split()
        if any(x.endswith('tools/run_context.py') for x in a) and '--budget' in a and a[a.index('--budget') + 1] == '64' \
                and '--out' in a and a[a.index('--out') + 1] == RUNS:
            out[int(a[a.index('--ctx') + 1])] = int(pid)
    return out


def healthy():
    st = os.statvfs(HERE)
    free = st.f_bavail * st.f_frsize
    try:
        level = int(subprocess.run(['sysctl', '-n', 'kern.memorystatus_level'], capture_output=True, text=True).stdout)
    except Exception:
        level = 100
    return free > 15 * 2**30 and level >= 15, free, level


def main():
    lk = open(os.path.join(C, 'campaign.lock'), 'w')
    try:
        fcntl.flock(lk, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except OSError:
        print('another campaign holds the lock'); return
    seq = json.load(open(os.path.join(HERE, 'order.json')))['seq']
    ctx = {json.loads(l)['ctx']: json.loads(l) for l in open(os.path.join(HERE, 'contexts.jsonl'))}
    skip = {int(x) for x in open(os.path.join(HERE, 'skip_closed.txt')) if x.strip()}
    children, attempts, failed = {}, {}, set()
    log('campaign start pid %d, contexts %d, skip %d, floor %d' % (os.getpid(), len(seq), len(skip), ctl('floor', 2040)))
    stop_new = os.path.exists(os.path.join(C, 'WITNESS-ALERT.txt'))
    while True:
        floor = ctl('floor', 2040)
        mine = [seq[i] for i in range(len(seq) - 1, floor - 2, -1)]      # positions 4096 .. floor, smallest first
        for k, pr in list(children.items()):
            rc = pr.poll()
            if rc is None:
                continue
            del children[k]
            r = result(k)
            if rc == 0 and r and r.get('status') == 'closed':
                log('closed ctx %d nodes %d leaves %d cpu %.0fs replay %s' % (k, r['nodes'], r['leaves'], r['cpu_s'], (r.get('replay') or {}).get('ok')))
            elif rc == 3:
                stop_new = True
                with open(os.path.join(C, 'WITNESS-ALERT.txt'), 'a') as f:
                    f.write('%s ctx %d witness: %s\n' % (time.strftime('%F %T'), k, json.dumps({x: (r or {}).get(x) for x in ('witness_holes', 'witness_exact_valid')})))
                log('WITNESS in ctx %d (exact_valid=%s); no new jobs' % (k, (r or {}).get('witness_exact_valid')))
            else:
                attempts[k] = attempts.get(k, 0) + 1
                log('ERROR ctx %d rc %s (attempt %d)' % (k, rc, attempts[k]))
                if attempts[k] >= 2:
                    failed.add(k)
        live = alive()
        done = [k for k in mine if (result(k) or {}).get('status') == 'closed']
        todo = [k for k in mine if k not in skip and k not in failed and (result(k) or {}).get('status') != 'closed']
        ok, free, level = healthy()
        cap = ctl('max_running', 15)
        stop = stop_new or os.path.exists(os.path.join(C, 'STOP'))
        if not stop and ok:
            for k in todo:
                if len(live) + len([c for c in children if c not in live]) >= cap:
                    break
                if k in live or k in children:
                    continue
                out = open(os.path.join(LOGS, 'ctx-%d.out' % k), 'a'); err = open(os.path.join(LOGS, 'ctx-%d.err' % k), 'a')
                children[k] = subprocess.Popen(['nice', '-n', '10', PY, '-B', os.path.join(HERE, 'tools', 'run_context.py'),
                                                '--budget', '64', '--ctx', str(k), '--contexts', os.path.join(HERE, 'contexts.jsonl'),
                                                '--out', RUNS], cwd=HERE, stdout=out, stderr=err, env=dict(os.environ, ES_REPO=REPO))
                live[k] = children[k].pid
                log('start ctx %d (position %d, b63 nodes %d)' % (k, seq.index(k) + 1, ctx[k]['nodes']))
        nodes = sum((result(k) or {}).get('nodes', 0) for k in done)
        cpu = sum((result(k) or {}).get('cpu_s', 0) for k in done)
        b63_done = sum(ctx[k]['nodes'] for k in done); b63_all = sum(ctx[k]['nodes'] for k in mine if k not in skip)
        with open(os.path.join(C, 'STATUS'), 'w') as f:
            f.write(json.dumps({'time': time.strftime('%F %T'), 'floor': floor, 'mine': len(mine), 'skipped_linux': len([k for k in mine if k in skip]),
                                'closed_here': len(done), 'todo': len(todo), 'running': sorted(live), 'failed': sorted(failed),
                                'b64_nodes_closed': nodes, 'cpu_s_closed': round(cpu), 'b63_nodes_share_done': round(b63_done / max(b63_all, 1), 4),
                                'free_gb': round(free / 2**30), 'mem_level': level, 'stop': stop, 'witness': stop_new}, indent=1) + '\n')
        if not todo and not live and not children:
            log('campaign done: closed %d of %d positions >= %d (skipped %d closed on Linux; failed %s)' % (len(done), len(mine), floor, len([k for k in mine if k in skip]), sorted(failed)))
            return
        if stop and not live and not children:
            log('stopped (STOP or witness); closed %d' % len(done)); return
        time.sleep(20)


if __name__ == '__main__':
    main()
