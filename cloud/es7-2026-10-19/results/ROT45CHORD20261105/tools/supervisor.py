#!/usr/bin/env python3
"""Detached supervisor (v2, after the 5 Nov 04:30 review) for the 5-fold / 4-fold chord-lemma threshold cubes.

Restart-safe: state comes from the filesystem and the process table.  A cube with a .lock file is never started again,
so no solver is ever restarted or duplicated.  Only processes whose cwd is this directory are touched.
Every 30 s:
  * cutoff (epoch seconds in `cutoff_final`, written atomically; the last good value is kept on a parse error; a
    value earlier than the one seen at start is ignored unless final/FINALIZE_EARLY exists; finalization needs
    now >= cutoff on two consecutive cycles).  At the cutoff, every unfinished SOLVER is terminated
    (SIGCONT+SIGTERM, SIGKILL after 60 s), then the SIGSTOPped lane wrappers are removed (lane.sh first).
    Verification of UNSAT proofs then continues for up to CHECK_GRACE seconds, every cube is recorded once, and
    final/final_report.md is written.
  * health: pause (SIGSTOP) the youngest running solver if Tctl >= 95 C on 2 cycles, MemAvailable < 4 GiB, or swap
    grows by > 1 GiB in 5 min with MemAvailable < 8 GiB; resume (SIGCONT) when all clear.
    Disk: below 430 GB free, pause the youngest running solver (no data lost).  Below the 400 GB floor, terminate the
    youngest solver and delete ONLY its partial, unfinished LRAT (never a finished or verified one), one per cycle.
    New solvers start only above 600 GB.
  * an UNSAT solver gets check_wrapper.sh (cake_lpr verdict; hashes of all artifacts).  VERIFIED and REJECTED are
    final; INTERRUPTED is retried up to 3 times.  A SAT answer's model is checked against the CNF.
  * never-started cubes start only while fewer than MAXLANES solvers run, health is fine, and > 1 h remains.
"""
import os, sys, time, json, signal, glob, subprocess, fcntl
D = '<rot45-work-dir>'
OUT = os.path.join(D, 'final'); os.makedirs(OUT, exist_ok=True)
LOG = os.path.join(OUT, 'supervisor.log'); RES = os.path.join(OUT, 'results_final.tsv')
MAXLANES = 30; MAXCHECKS = 2; CHECK_GRACE = 3 * 3600; MAX_ATTEMPTS = 3
DISK_FLOOR = 400e9; DISK_PAUSE = 430e9; DISK_START = 600e9
T_PAUSE = 95.0; T_RESUME = 85.0; MEM_PAUSE = 4 * 2**30; MEM_RESUME = 8 * 2**30
_last_cut = [None]

def log(msg):
    with open(LOG, 'a') as f: f.write(time.strftime('%Y-%m-%d %H:%M:%S ') + msg + '\n')

def cubes():
    return sorted(glob.glob(os.path.join(D, 'cubes5', 'o*.cnf'))) + sorted(glob.glob(os.path.join(D, 'cubes4', 'o*.cnf')))
CUBESET = None
def base(c): return c[:-4]
def rel(c): return os.path.relpath(c, D)

def proc_info(p):
    try:
        argv = [a.decode() for a in open('/proc/%s/cmdline' % p, 'rb').read().split(b'\0') if a]
        cwd = os.readlink('/proc/%s/cwd' % p)
        return argv, cwd
    except Exception: return None, None

def procs():
    """cube base (absolute) -> list of (pid, kind) for this run's solvers and checkers (cwd must be D)"""
    res = {}
    for p in os.listdir('/proc'):
        if not p.isdigit(): continue
        argv, cwd = proc_info(p)
        if not argv or cwd != D: continue
        prog = os.path.basename(argv[0])
        b = None; kind = None
        if prog == 'cadical' and argv[-1].endswith('.lrat'): b = argv[-1][:-5]; kind = 'solver'
        elif prog in ('cake_lpr', 'lrat-check') and len(argv) >= 3 and argv[1].endswith('.cnf'): b = argv[1][:-4]; kind = 'check'
        if b is None: continue
        b = b if b.startswith('/') else os.path.join(D, b)
        if b in CUBESET: res.setdefault(b, []).append((int(p), kind))
    return res

def pstate(pid):
    try: return open('/proc/%d/stat' % pid).read().rsplit(')', 1)[1].split()[0]
    except Exception: return None

def pstart(pid):
    try:
        st = open('/proc/%d/stat' % pid).read().rsplit(')', 1)[1].split()
        boot = float(open('/proc/stat').read().split('btime ')[1].split()[0])
        return boot + int(st[19]) / os.sysconf('SC_CLK_TCK')
    except Exception: return 0.0

def recorded():
    done = {}
    if os.path.exists(RES):
        for line in open(RES):
            f = line.rstrip('\n').split('\t')
            if len(f) >= 2: done[f[0]] = f[1]
    return done

def record(cube, status, extra=''):
    if rel(cube) in recorded(): return
    with open(RES, 'a') as f: f.write('%s\t%s\t%s\t%s\n' % (rel(cube), status, time.strftime('%Y-%m-%d %H:%M:%S'), extra))
    log('RECORD %s %s %s' % (rel(cube), status, extra))

def health():
    t = None
    for h in glob.glob('/sys/class/hwmon/hwmon*/name'):
        try:
            if open(h).read().strip() == 'k10temp':
                t = int(open(os.path.join(os.path.dirname(h), 'temp1_input')).read()) / 1000.0
        except Exception: pass
    mi = {}
    for line in open('/proc/meminfo'):
        k, v = line.split(':'); mi[k] = int(v.split()[0]) * 1024
    st = os.statvfs(D)
    return {'tctl': t, 'memavail': mi['MemAvailable'], 'swapused': mi['SwapTotal'] - mi['SwapFree'],
            'diskfree': st.f_bavail * st.f_frsize}

def outverdict(b):
    try:
        for line in open(b + '.out', errors='replace'):
            if line.startswith('s '): return line[2:].strip()
    except FileNotFoundError: pass
    return None

def checkmeta(b):
    m = {}
    try:
        for line in open(b + '.check.meta'):
            for tok in line.split():
                if '=' in tok: k, v = tok.split('=', 1); m[k] = v
            if line.strip() == 'done': m['done'] = '1'
    except FileNotFoundError: pass
    return m

def attempts(b): return len(glob.glob(b + '.check.meta.abort*'))

def cutoff():
    try:
        v = int(open(os.path.join(D, 'cutoff_final')).read().split()[0])
        if v > 1.7e9: _last_cut[0] = v
        else: log('cutoff_final: implausible value %r ignored' % v)
    except Exception as e:
        log('cutoff_final unreadable (%s); keeping %s' % (e, _last_cut[0]))
    return _last_cut[0]

def start_check(b):
    subprocess.Popen([os.path.join(D, 'check_wrapper.sh'), b], cwd=D, start_new_session=True,
                     stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    log('CHECK started %s (attempt %d)' % (rel(b), attempts(b) + 1))

def start_solver(c):
    b = base(c)
    try: fd = os.open(b + '.lock', os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    except FileExistsError: return
    os.write(fd, ('started by supervisor %s\n' % time.strftime('%H:%M:%S')).encode()); os.close(fd)
    out = open(b + '.out', 'x')
    subprocess.Popen(['cadical', '--lrat', '--binary=false', '-q', rel(c), rel(b) + '.lrat'], cwd=D,
                     start_new_session=True, stdout=out, stderr=subprocess.STDOUT)
    log('SOLVER started %s' % rel(c))

def verify_model(b):
    """check a SAT answer: every clause of the CNF has a true literal under the v-lines"""
    val = set()
    for line in open(b + '.out', errors='replace'):
        if line.startswith('v '): val.update(int(x) for x in line[2:].split() if x != '0')
    bad = 0
    with open(b + '.cnf') as f:
        for line in f:
            if not line or line[0] in 'cp': continue
            lits = [int(x) for x in line.split()[:-1]]
            if lits and not any(l in val for l in lits): bad += 1
    return bad

def manage_checks(checks, done, allow_new=True):
    """record finished checks; (re)start checks for UNSAT cubes; returns number of running checks"""
    n = len(checks)
    for c in cubes():
        b = base(c); r = rel(c)
        if r in done or b in checks: continue
        if outverdict(b) != 'UNSATISFIABLE': continue
        m = checkmeta(b)
        if m.get('done'):
            if m.get('verdict') == 'VERIFIED':
                record(c, 'UNSAT-VERIFIED', 'cake_lpr s VERIFIED UNSAT; check_s=%s; lrat_GB=%.1f; hashes in %s.hashes.txt' % (
                    m.get('seconds'), os.path.getsize(b + '.lrat') / 1e9, rel(b)))
            elif m.get('verdict') == 'REJECTED':
                record(c, 'UNSAT-PROOF-REJECTED', 'cake_lpr: Checking failed (artifacts preserved)')
            else:
                k = attempts(b)
                os.rename(b + '.check.meta', b + '.check.meta.abort%d' % k); log('CHECK interrupted %s rc=%s; kept as abort%d' % (r, m.get('rc'), k))
                if k + 1 >= MAX_ATTEMPTS: record(c, 'UNSAT-CHECK-INTERRUPTED', 'check interrupted %d times (artifacts preserved)' % (k + 1))
        elif os.path.exists(b + '.check.meta'):
            # meta without 'done' and no running checker: the wrapper died
            if time.time() - os.path.getmtime(b + '.check.meta') > 120:
                k = attempts(b); os.rename(b + '.check.meta', b + '.check.meta.abort%d' % k); log('CHECK wrapper died %s; kept as abort%d' % (r, k))
        elif allow_new and n < MAXCHECKS and attempts(b) < MAX_ATTEMPTS:
            start_check(b); n += 1
    return n

def finalize():
    log('FINALIZE begins')
    pr = procs()
    solvers = [(b, pid) for b, lst in pr.items() for pid, k in lst if k == 'solver']
    for b, pid in solvers:
        try: os.kill(pid, signal.SIGCONT); os.kill(pid, signal.SIGTERM)
        except ProcessLookupError: pass
    t0 = time.time()
    while time.time() - t0 < 60 and any(pstate(pid) not in (None, 'Z') for _, pid in solvers): time.sleep(2)
    for b, pid in solvers:
        if pstate(pid) not in (None, 'Z'):
            try: os.kill(pid, signal.SIGKILL)
            except ProcessLookupError: pass
    stopped = {b for b, _ in solvers}
    time.sleep(3)
    # remove the original lane wrappers (cwd D only): lane.sh first so it cannot run its own check, then the timeouts
    for want in ('lane', 'timeout'):
        for p in os.listdir('/proc'):
            if not p.isdigit(): continue
            argv, cwd = proc_info(p)
            if not argv or cwd != D: continue
            hit = (want == 'lane' and len(argv) >= 3 and argv[0] == '/bin/bash' and argv[1] == './lane.sh') or \
                  (want == 'timeout' and argv[0] == 'timeout' and 'cadical' in argv)
            if hit:
                try: os.kill(int(p), signal.SIGKILL); log('cleanup %s %s' % (want, p))
                except ProcessLookupError: pass
        time.sleep(1)
    # verification grace period
    tg = time.time()
    while time.time() - tg < CHECK_GRACE:
        pr = procs(); done = recorded()
        checks = {b: pid for b, lst in pr.items() for pid, k in lst if k == 'check'}
        manage_checks(checks, done)
        pending = [c for c in cubes() if rel(c) not in recorded() and outverdict(base(c)) == 'UNSATISFIABLE']
        if not pending and not checks: break
        time.sleep(30)
    pr = procs()
    for b, lst in pr.items():
        for pid, k in lst:
            if k == 'check':
                try: os.kill(pid, signal.SIGTERM)
                except ProcessLookupError: pass
    time.sleep(5)
    for c in cubes():
        b = base(c); r = rel(c)
        if r in recorded(): continue
        v = outverdict(b)
        if v == 'UNSATISFIABLE': record(c, 'UNSAT-UNCHECKED', 'verification did not finish in the grace period; CNF, LRAT, out preserved')
        elif v == 'SATISFIABLE':
            bad = verify_model(b); record(c, 'SAT-MODEL-VALID' if bad == 0 else 'SAT-MODEL-INVALID', 'falsified clauses %d' % bad)
        elif b in stopped: record(c, 'UNRESOLVED-AT-CUTOFF', 'solver terminated at the cutoff; out and partial LRAT preserved')
        elif os.path.exists(b + '.lock'): record(c, 'ENDED-NO-ANSWER', 'solver ended before the cutoff without an answer')
        else: record(c, 'NEVER-STARTED')
    write_report()
    log('FINALIZE done')

def write_report():
    done = recorded(); h = health()
    imp = {}
    p = os.path.join(D, 'imp2_results.tsv')
    if os.path.exists(p):
        for l in open(p):
            f = l.rstrip('\n').split('\t')
            if len(f) >= 3: imp[f[0]] = (f[1], f[2])
    lines = ['# Final report: chord-lemma threshold cubes (generated %s by supervisor.py v2)' % time.strftime('%Y-%m-%d %H:%M:%S %Z'), '',
             'This report is generated automatically. It claims no bound. Verdicts come from cake_lpr; lrat-check is not used.', '']
    for m, n, imp_n in (('5', 24, 40), ('4', 12, 20)):
        cs = [c for c in cubes() if '/cubes%s/' % m in c]
        st = {rel(c): done.get(rel(c), 'NOT-RECORDED') for c in cs}
        ver = sum(1 for v in st.values() if v == 'UNSAT-VERIFIED')
        impok = sum(1 for k, (s, v) in imp.items() if k.startswith('imp%s/' % m) and s == 'UNSATISFIABLE' and v == 'VERIFIED')
        lines += ['## %s-fold (%d phase-order cubes)' % (m, n), '',
                  '- phase-order cubes UNSAT, proof accepted by cake_lpr: %d of %d' % (ver, len(cs)),
                  '- transitivity-violating patterns UNSAT, proof accepted by cake_lpr (imp2_results.tsv): %d of %d' % (impok, imp_n),
                  '- cover complete with every proof accepted by cake_lpr: %s' % ('YES' if ver == len(cs) == n and impok == imp_n else 'NO'), '',
                  '| cube | status |', '|---|---|'] + ['| %s | %s |' % (k, v) for k, v in sorted(st.items())] + ['']
    lines += ['## Remaining obligations before any theorem can be stated', '',
              '- Every phase-order cube and every transitivity pattern UNSAT, with each proof accepted by cake_lpr (table above).',
              '- Soundness of encoder A for (m, K) = (5, 8) and (4, 8): written proof, reviewed in ROT456 section 2, not Lean-checked.',
              '- Soundness of the reflection unit (H(1) for odd m, Y(1,2) for even m): written, C7UPPER / C6UPPER section 2.',
              '- The chord lemma: written proof; every added clause is proved by an independent exact verifier (CHORD20261105 section 6).',
              '- Unresolved cubes need longer runs or a finer split, for example by the position of layer 5. Their partial LRAT files are',
              '  unfinished and unverified; this script deletes one only when that is needed to keep 400 GB of disk free.', '',
              'Health at report time: Tctl %s C, MemAvailable %.1f GiB, swap used %.1f GiB, disk free %.0f GB.' % (
                  h['tctl'], h['memavail'] / 2**30, h['swapused'] / 2**30, h['diskfree'] / 1e9)]
    open(os.path.join(OUT, 'final_report.md'), 'w').write('\n'.join(lines) + '\n')
    log('REPORT written')

def main():
    lockf = open(os.path.join(OUT, 'supervisor.lock'), 'w')
    try: fcntl.flock(lockf, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except OSError: print('another supervisor holds the lock'); return
    cut0 = cutoff()
    log('supervisor v2 start pid %d, cutoff %s' % (os.getpid(), time.strftime('%Y-%m-%d %H:%M', time.localtime(cut0))))
    hot = 0; swap_hist = []; due = 0
    while True:
        cut = cutoff()
        if cut < cut0 and not os.path.exists(os.path.join(OUT, 'FINALIZE_EARLY')):
            log('cutoff %d earlier than start value %d ignored (create final/FINALIZE_EARLY to allow)' % (cut, cut0)); cut = cut0
        now = time.time()
        due = due + 1 if now >= cut else 0
        if due >= 2:
            finalize(); return
        h = health(); pr = procs(); done = recorded()
        solvers = {b: pid for b, lst in pr.items() for pid, k in lst if k == 'solver'}
        checks = {b: pid for b, lst in pr.items() for pid, k in lst if k == 'check'}
        running = {b: pid for b, pid in solvers.items() if pstate(pid) not in ('T', 'Z', None)}
        paused = {b: pid for b, pid in solvers.items() if pstate(pid) == 'T'}
        hot = hot + 1 if (h['tctl'] is not None and h['tctl'] >= T_PAUSE) else 0
        swap_hist = (swap_hist + [h['swapused']])[-10:]
        swap_growing = len(swap_hist) >= 10 and swap_hist[-1] - swap_hist[0] > 2**30 and h['memavail'] < MEM_RESUME
        if h['diskfree'] < DISK_FLOOR and solvers:
            b, pid = max(solvers.items(), key=lambda kv: pstart(kv[1]))
            try: os.kill(pid, signal.SIGCONT); os.kill(pid, signal.SIGTERM)
            except ProcessLookupError: pass
            for _ in range(30):
                if pstate(pid) in (None, 'Z'): break
                time.sleep(2)
            if pstate(pid) not in (None, 'Z'):
                try: os.kill(pid, signal.SIGKILL)
                except ProcessLookupError: pass
                time.sleep(2)
            if outverdict(b) is None:
                sz = os.path.getsize(b + '.lrat') if os.path.exists(b + '.lrat') else 0
                record(b + '.cnf', 'STOPPED-DISK', 'free %.0f GB below the 400 GB floor; partial LRAT (%.1f GB) deleted' % (h['diskfree'] / 1e9, sz / 1e9))
                if os.path.exists(b + '.lrat'): os.remove(b + '.lrat')
            time.sleep(30); continue
        need_pause = hot >= 2 or h['memavail'] < MEM_PAUSE or swap_growing or h['diskfree'] < DISK_PAUSE
        if need_pause and running:
            b, pid = max(running.items(), key=lambda kv: pstart(kv[1]))
            os.kill(pid, signal.SIGSTOP); log('PAUSE %s (tctl %s, memavail %.1f GiB, swap %.1f GiB, disk %.0f GB)' % (
                rel(b), h['tctl'], h['memavail'] / 2**30, h['swapused'] / 2**30, h['diskfree'] / 1e9))
        elif paused and not need_pause and (h['tctl'] is None or h['tctl'] <= T_RESUME) and h['memavail'] > MEM_RESUME:
            b, pid = min(paused.items(), key=lambda kv: pstart(kv[1]))
            os.kill(pid, signal.SIGCONT); log('RESUME %s' % rel(b))
        manage_checks(checks, done)
        for c in cubes():
            b = base(c); r = rel(c)
            if r in done or b in solvers or not os.path.exists(b + '.lock'): continue
            v = outverdict(b)
            if v == 'SATISFIABLE':
                bad = verify_model(b); record(c, 'SAT-MODEL-VALID' if bad == 0 else 'SAT-MODEL-INVALID', 'falsified clauses %d; model in %s.out' % (bad, rel(b)))
            elif v is None:
                record(c, 'ENDED-NO-ANSWER', 'solver exited without an s-line; logs preserved')
        if len(running) < MAXLANES and not paused and not need_pause and h['diskfree'] > DISK_START and cut - now > 3600 \
                and (h['tctl'] is None or h['tctl'] < T_RESUME) and h['memavail'] > MEM_RESUME:
            for c in cubes():
                if not os.path.exists(base(c) + '.lock'):
                    start_solver(c); break
        st = ['STATUS %s  (cutoff %s; supervisor v2)' % (time.strftime('%Y-%m-%d %H:%M:%S'), time.strftime('%Y-%m-%d %H:%M', time.localtime(cut))),
              'health: Tctl %s C, MemAvailable %.1f GiB, swap used %.1f GiB, disk free %.0f GB' % (h['tctl'], h['memavail'] / 2**30, h['swapused'] / 2**30, h['diskfree'] / 1e9),
              'solvers running %d, paused %d, checks running %d, never started %d' % (len(running), len(paused), len(checks), sum(1 for c in cubes() if not os.path.exists(base(c) + '.lock'))),
              'recorded: %s' % json.dumps(dict(sorted(recorded().items())))]
        open(os.path.join(OUT, 'STATUS'), 'w').write('\n'.join(st) + '\n')
        time.sleep(30)

CUBESET = {base(c) for c in cubes()}
if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--dry':
        h = health(); pr = procs()
        print(json.dumps({'health': h, 'solvers': len([1 for l in pr.values() for _, k in l if k == 'solver']),
                          'checks': len([1 for l in pr.values() for _, k in l if k == 'check']), 'cutoff': cutoff(),
                          'recorded': recorded(), 'never_started': [rel(c) for c in cubes() if not os.path.exists(base(c) + '.lock')]}, indent=1))
    else:
        main()
