#!/usr/bin/env python3
"""Job scheduler for the k=9 cubes inside one systemd unit (CPU and memory capped by the unit).
queue.txt: lines 'CUBENAME TLIMIT' in priority order (re-read every loop; '#' comments).
A cube is solved by tools/solve.sh, UNSAT cubes are checked by tools/check.sh (cake_lpr).
Resource model: at most MAXJOBS processes; solver MEM_S GB, checker MEM_C GB; budget MEMB GB.
While a check is pending, no new solver is started if it would block the checker.
Files STOP (no new jobs) and the deadlines in local time (no new jobs after SOFT, kill after HARD)."""
import os, subprocess, time, signal, datetime
K9 = '/home/jay/research/data/satopen-20261113/k9'
C = K9 + '/cubes'
MAXJOBS = int(os.environ.get('MAXJOBS', 4)); MEMB = float(os.environ.get('MEMB', 17.2))
MEM_S = float(os.environ.get('MEM_S', 4.1)); MEM_C = float(os.environ.get('MEM_C', 9.0)); MEM_C2 = 11.6
SOFT = os.environ.get('SOFT', '05:30'); HARD = os.environ.get('HARD', '05:37')
running = {}   # pid -> (kind, cube, Popen, t0)
def log(msg):
    with open(K9 + '/sched.log', 'a') as f: f.write(time.strftime('%F %T ') + msg + '\n')
def hm(): return time.strftime('%H:%M')
def queue():
    out = []
    try:
        for line in open(K9 + '/queue.txt'):
            line = line.split('#')[0].split()
            if len(line) >= 2: out.append((line[0], int(line[1])))
    except FileNotFoundError: pass
    return out
def busy(): return {c for (_, c, _, _) in running.values()}
def mem(): return sum(MEM_S if k == 's' else (MEM_C if k == 'c' else MEM_C2) for (k, _, _, _) in running.values())
log('start MAXJOBS=%d MEMB=%.1f MEM_C=%.1f SOFT=%s HARD=%s' % (MAXJOBS, MEMB, MEM_C, SOFT, HARD))
while True:
    for pid, (k, c, p, t0) in list(running.items()):
        if p.poll() is not None:
            del running[pid]
            info = ''
            try: info = open(os.path.join(C, c, 'solved' if k == 's' else 'result.txt')).read().strip().splitlines()[-1]
            except Exception: pass
            log('%s %s finished rc=%s after %ds: %s' % ('solve' if k == 's' else 'check', c, p.returncode, time.time() - t0, info))
    now = hm()
    if now >= HARD and now < '12:00':
        for pid, (k, c, p, t0) in running.items():
            log('HARD deadline: terminating %s %s' % (k, c)); p.send_signal(signal.SIGTERM)
        time.sleep(5)
        for pid, (k, c, p, t0) in running.items():
            if p.poll() is None: p.kill()
        log('exit at hard deadline'); break
    stop = os.path.exists(K9 + '/STOP') or (now >= SOFT and now < '12:00')
    if not stop:
        b = busy()
        pend = sorted(c for c in os.listdir(C) if os.path.exists(os.path.join(C, c, 'solved'))
                      and 'exit 20' in open(os.path.join(C, c, 'solved')).read()
                      and not os.path.exists(os.path.join(C, c, 'result.txt')) and c not in b
                      and not os.path.exists(os.path.join(C, c, 'noproof'))
                      and not (os.path.exists(os.path.join(C, c, 'heapfail')) and len(open(os.path.join(C, c, 'heapfail')).readlines()) >= 2))
        nchk = sum(1 for (k, _, _, _) in running.values() if k in 'cC')
        if pend and nchk == 0 and len(running) < MAXJOBS:
            c = pend[0]; big = os.path.exists(os.path.join(C, c, 'heapfail'))
            mc = MEM_C2 if big else MEM_C
            if mem() + mc <= MEMB:
                p = subprocess.Popen(['sh', K9 + '/tools/check.sh', os.path.join(C, c)], env=dict(os.environ, HEAP='11000' if big else '8500'))
                running[p.pid] = ('C' if big else 'c', c, p, time.time()); log('check %s heap %s' % (c, '11000' if big else '8500'))
        for c, tl in queue():
            if len(running) >= MAXJOBS: break
            d = os.path.join(C, c)
            if c in busy() or os.path.exists(os.path.join(d, 'solved')) or not os.path.exists(os.path.join(d, 'cube.units')): continue
            need = mem() + MEM_S
            if pend and nchk == 0: need += (MEM_C2 if os.path.exists(os.path.join(C, pend[0], 'heapfail')) else MEM_C)   # keep room for the pending check
            if need > MEMB: break
            p = subprocess.Popen(['sh', K9 + '/tools/solve.sh', d, str(tl)])
            running[p.pid] = ('s', c, p, time.time()); log('solve %s limit %d' % (c, tl))
    elif not running:
        log('stopped (STOP file or soft deadline), nothing running: exit'); break
    with open(K9 + '/STATUS', 'w') as f:
        f.write(time.strftime('%F %T') + ' running: ' + ', '.join('%s:%s(%ds)' % (k, c, time.time() - t0) for (k, c, p, t0) in running.values()) + '\n')
    time.sleep(10)
