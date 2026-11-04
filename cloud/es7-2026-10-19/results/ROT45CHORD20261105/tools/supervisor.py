#!/usr/bin/env python3
"""Detached supervisor for the 5-fold / 4-fold chord-lemma threshold cubes (ROT45CHORD20261105).

Restart-safe: all state is derived from the filesystem and the process table each cycle; it never restarts or
duplicates a solver (a cube with a lock file is never started again).
Every 30 s it:
  * reads the cutoff (epoch seconds, file `cutoff_final`); at the cutoff it terminates every unfinished solver and
    every running check (SIGCONT+SIGTERM, then SIGKILL after 60 s), records them, writes the final report and exits;
  * health: CPU Tctl (k10temp), MemAvailable, swap, free disk.  Pauses (SIGSTOP) the youngest running solver when
    Tctl >= 95 C for 2 cycles or MemAvailable < 4 GiB; resumes (SIGCONT) when Tctl <= 85 C and MemAvailable > 8 GiB.
    Disk floor 400 GB: below 430 GB free it stops the youngest unfinished solver and deletes ONLY that solver's
    partial (unfinished, unverified) LRAT file.  Verified artifacts are never deleted.  No new solver starts below
    600 GB free.
  * finished solvers: reads `s UNSATISFIABLE` / `s SATISFIABLE` from the cube's .out; for UNSAT it launches
    check_wrapper.sh (lrat-check, then SHA-256 of CNF, LRAT, out and check log); verdict VERIFIED requires exit code 0
    and the line "c VERIFIED".
  * starts never-started cubes only while fewer than 30 solvers run, health is fine, disk > 600 GB, and more than 1 h
    remains before the cutoff.
Records: final/results_final.tsv (append-only), final/STATUS (refreshed), final/supervisor.log, final/final_report.md.
"""
import os, sys, time, json, signal, glob, subprocess, shutil
D = '<rot45-work-dir>'
OUT = os.path.join(D, 'final'); os.makedirs(OUT, exist_ok=True)
LOG = os.path.join(OUT, 'supervisor.log'); RES = os.path.join(OUT, 'results_final.tsv')
MAXLANES = 30; MAXCHECKS = 3
DISK_FLOOR = 400e9; DISK_STOP = 430e9; DISK_START = 600e9
T_PAUSE = 95.0; T_RESUME = 85.0; MEM_PAUSE = 4 * 2**30; MEM_RESUME = 8 * 2**30

def log(msg):
    with open(LOG, 'a') as f: f.write(time.strftime('%Y-%m-%d %H:%M:%S ') + msg + '\n')

def cubes():
    return sorted(glob.glob(os.path.join(D, 'cubes5', 'o*.cnf'))) + sorted(glob.glob(os.path.join(D, 'cubes4', 'o*.cnf')))

def base(c): return c[:-4]
def rel(c): return os.path.relpath(c, D)

def procs():
    """cube base (absolute) -> list of (pid, kind) for cadical solvers and lrat-check processes"""
    res = {}
    for p in os.listdir('/proc'):
        if not p.isdigit(): continue
        try:
            argv = open('/proc/%s/cmdline' % p, 'rb').read().split(b'\0')
            argv = [a.decode() for a in argv if a]
        except Exception: continue
        if not argv: continue
        prog = os.path.basename(argv[0])
        if prog == 'cadical' and len(argv) >= 2 and argv[-1].endswith('.lrat') and '/o' in argv[-1]:
            b = argv[-1][:-5]; b = b if b.startswith('/') else os.path.join(D, b)
            res.setdefault(b, []).append((int(p), 'solver'))
        elif prog == 'lrat-check' and len(argv) >= 3 and argv[1].endswith('.cnf') and '/o' in argv[1]:
            b = argv[1][:-4]; b = b if b.startswith('/') else os.path.join(D, b)
            res.setdefault(b, []).append((int(p), 'check'))
    return res

def pstate(pid):
    try: return open('/proc/%d/stat' % pid).read().rsplit(')', 1)[1].split()[0]
    except Exception: return None

def pstart(pid):
    try:
        st = open('/proc/%d/stat' % pid).read().rsplit(')', 1)[1].split()
        ticks = int(st[19]); hz = os.sysconf('SC_CLK_TCK')
        boot = float(open('/proc/stat').read().split('btime ')[1].split()[0])
        return boot + ticks / hz
    except Exception: return 0.0

def recorded():
    done = {}
    if os.path.exists(RES):
        for line in open(RES):
            f = line.rstrip('\n').split('\t')
            if len(f) >= 2: done[f[0]] = f[1]
    return done

def record(cube, status, extra=''):
    with open(RES, 'a') as f: f.write('%s\t%s\t%s\t%s\n' % (rel(cube), status, time.strftime('%Y-%m-%d %H:%M:%S'), extra))
    log('RECORD %s %s %s' % (rel(cube), status, extra))

def health():
    t = None
    for h in glob.glob('/sys/class/hwmon/hwmon*/name'):
        if open(h).read().strip() == 'k10temp':
            try: t = int(open(os.path.join(os.path.dirname(h), 'temp1_input')).read()) / 1000.0
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

def cutoff(): return int(open(os.path.join(D, 'cutoff_final')).read().split()[0])

def start_check(b, cut):
    subprocess.Popen([os.path.join(D, 'check_wrapper.sh'), b, str(cut)], cwd=D, start_new_session=True,
                     stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    log('CHECK started %s' % rel(b))

def start_solver(c):
    b = base(c); open(b + '.lock', 'w').write('started by supervisor %s\n' % time.strftime('%H:%M:%S'))
    out = open(b + '.out', 'w')
    subprocess.Popen(['cadical', '--lrat', '--binary=false', '-q', rel(c), rel(b) + '.lrat'], cwd=D,
                     start_new_session=True, stdout=out, stderr=subprocess.STDOUT)
    log('SOLVER started %s' % rel(c))

def finalize(reason):
    log('FINALIZE (%s)' % reason)
    pr = procs(); done = recorded()
    targets = [(b, pid, kind) for b, lst in pr.items() for pid, kind in lst]
    for b, pid, kind in targets:
        try: os.kill(pid, signal.SIGCONT); os.kill(pid, signal.SIGTERM)
        except ProcessLookupError: pass
    t0 = time.time()
    while time.time() - t0 < 60 and any(pstate(pid) not in (None, 'Z') for _, pid, _ in targets): time.sleep(2)
    for b, pid, kind in targets:
        if pstate(pid) not in (None, 'Z'):
            try: os.kill(pid, signal.SIGKILL)
            except ProcessLookupError: pass
    time.sleep(3)
    # clean up the original lane wrappers: lane.sh first (so it cannot run its own check), then the SIGSTOPped timeouts
    for p in os.listdir('/proc'):
        if not p.isdigit(): continue
        try: argv = [a.decode() for a in open('/proc/%s/cmdline' % p, 'rb').read().split(b'\0') if a]
        except Exception: continue
        if len(argv) >= 3 and argv[0] == '/bin/bash' and argv[1] == './lane.sh':
            try: os.kill(int(p), signal.SIGKILL); log('cleanup lane.sh %s' % p)
            except ProcessLookupError: pass
    time.sleep(1)
    for p in os.listdir('/proc'):
        if not p.isdigit(): continue
        try: argv = [a.decode() for a in open('/proc/%s/cmdline' % p, 'rb').read().split(b'\0') if a]
        except Exception: continue
        if len(argv) >= 3 and argv[0] == 'timeout' and 'cadical' in argv and '/o' in argv[-1]:
            try: os.kill(int(p), signal.SIGKILL); log('cleanup timeout %s' % p)
            except ProcessLookupError: pass
    for c in cubes():
        b = base(c); r = rel(c)
        if r in done: continue
        v = outverdict(b); kinds = [k for _, _, k in [(x, y, z) for x, y, z in targets if x == b]]
        if v == 'UNSATISFIABLE':
            m = checkmeta(b)
            if m.get('verdict') == 'VERIFIED' and m.get('rc') == '0': record(c, 'UNSAT-VERIFIED', 'check_s=%s' % m.get('seconds'))
            else: record(c, 'UNSAT-CHECK-INCOMPLETE', 'check stopped at cutoff; CNF, LRAT and out preserved')
        elif v == 'SATISFIABLE': record(c, 'SAT', 'model in .out')
        elif os.path.exists(b + '.lock'):
            record(c, 'UNRESOLVED-AT-CUTOFF' if 'solver' in kinds else 'ENDED-NO-ANSWER', 'logs preserved')
        else: record(c, 'NEVER-STARTED')
    write_report()

def write_report():
    done = recorded(); h = health()
    imp = [l.split('\t') for l in open(os.path.join(D, 'imp_results.tsv'))]
    impok = {'5': 0, '4': 0}
    for f in imp:
        if len(f) >= 3 and f[1] == 'UNSATISFIABLE' and f[2].strip() == 'VERIFIED': impok['5' if 'imp5/' in f[0] else '4'] += 1
    lines = ['# Final report: chord-lemma threshold cubes (generated %s by supervisor.py)' % time.strftime('%Y-%m-%d %H:%M:%S %Z'), '',
             'This report is generated automatically. It claims no bound.', '']
    for m, n, imp_n in (('5', 24, 40), ('4', 12, 20)):
        cs = [c for c in cubes() if '/cubes%s/' % m in c]
        st = {rel(c): done.get(rel(c), 'NOT-RECORDED') for c in cs}
        ver = sum(1 for v in st.values() if v == 'UNSAT-VERIFIED')
        lines += ['## %s-fold (%s cubes: total phase orders)' % (m, n), '',
                  '- phase-order cubes UNSAT with lrat-check VERIFIED: %d of %d' % (ver, len(cs)),
                  '- transitivity-violating patterns UNSAT with lrat-check VERIFIED: %d of %d' % (impok[m], imp_n),
                  '- cover complete with every proof verified: %s' % ('YES' if ver == len(cs) == n and impok[m] == imp_n else 'NO'), '',
                  '| cube | status |', '|---|---|'] + ['| %s | %s |' % (k, v) for k, v in sorted(st.items())] + ['']
    lines += ['## Remaining obligations before any theorem can be stated', '',
              '- Every phase-order cube and every transitivity pattern must be UNSAT with a checked proof (table above).',
              '- Soundness of encoder A for (m, K) = (5, 8) and (4, 8). This is a written proof, reviewed in ROT456 section 2, not Lean-checked.',
              '- Soundness of the reflection unit (H(1) for odd m, Y(1,2) for even m): C7UPPER / C6UPPER section 2, written.',
              '- The chord lemma: a written proof. Every added clause was proved by an independent exact verifier (CHORD20261105 section 6).',
              '- Optional second checker (cake_lpr) on every proof, as done for C6UPPER and C7UPPER.',
              '- Unresolved cubes need longer runs or a finer split (for example by the position of layer 5). Their partial LRAT files are',
              '  unfinished and unverified. They can be deleted to reclaim disk, but this script does not do so except to keep 400 GB free.', '',
              'Health at report time: Tctl %s C, MemAvailable %.1f GiB, swap used %.1f GiB, disk free %.0f GB.' % (
                  h['tctl'], h['memavail'] / 2**30, h['swapused'] / 2**30, h['diskfree'] / 1e9)]
    open(os.path.join(OUT, 'final_report.md'), 'w').write('\n'.join(lines) + '\n')
    log('REPORT written')

def main():
    log('supervisor start pid %d, cutoff %s' % (os.getpid(), time.strftime('%Y-%m-%d %H:%M', time.localtime(cutoff()))))
    hot = 0; swap_hist = []
    while True:
        cut = cutoff(); now = time.time()
        if now >= cut:
            finalize('cutoff'); return
        h = health(); pr = procs(); done = recorded()
        solvers = {b: pid for b, lst in pr.items() for pid, k in lst if k == 'solver'}
        checks = {b: pid for b, lst in pr.items() for pid, k in lst if k == 'check'}
        running = {b: pid for b, pid in solvers.items() if pstate(pid) not in ('T', 'Z', None)}
        paused = {b: pid for b, pid in solvers.items() if pstate(pid) == 'T'}
        # ---- health actions
        hot = hot + 1 if (h['tctl'] is not None and h['tctl'] >= T_PAUSE) else 0
        swap_hist = (swap_hist + [h['swapused']])[-10:]
        swap_growing = len(swap_hist) >= 10 and swap_hist[-1] - swap_hist[0] > 2**30 and h['memavail'] < MEM_RESUME
        if (hot >= 2 or h['memavail'] < MEM_PAUSE or swap_growing) and running:
            b, pid = max(running.items(), key=lambda kv: pstart(kv[1]))
            os.kill(pid, signal.SIGSTOP); log('PAUSE %s (tctl %s, memavail %.1f GiB, swap %.1f GiB)' % (rel(b), h['tctl'], h['memavail'] / 2**30, h['swapused'] / 2**30))
        elif paused and (h['tctl'] is None or h['tctl'] <= T_RESUME) and h['memavail'] > MEM_RESUME and not swap_growing:
            b, pid = min(paused.items(), key=lambda kv: pstart(kv[1]))
            os.kill(pid, signal.SIGCONT); log('RESUME %s' % rel(b))
        if h['diskfree'] < DISK_STOP and solvers:
            b, pid = max(solvers.items(), key=lambda kv: pstart(kv[1]))
            try: os.kill(pid, signal.SIGCONT); os.kill(pid, signal.SIGTERM)
            except ProcessLookupError: pass
            for _ in range(30):
                if pstate(pid) in (None, 'Z'): break
                time.sleep(2)
            if pstate(pid) not in (None, 'Z'): os.kill(pid, signal.SIGKILL); time.sleep(2)
            sz = os.path.getsize(b + '.lrat') if os.path.exists(b + '.lrat') else 0
            if outverdict(b) is None and os.path.exists(b + '.lrat'):
                os.remove(b + '.lrat'); log('DISK: deleted partial unverified %s.lrat (%.1f GB)' % (rel(b), sz / 1e9))
            record(b + '.cnf', 'STOPPED-DISK', 'free %.0f GB; partial LRAT deleted' % (h['diskfree'] / 1e9))
            continue
        # ---- finished solvers and checks
        nchecks = len(checks)
        for c in cubes():
            b = base(c); r = rel(c)
            if r in done or b in solvers: continue
            if not os.path.exists(b + '.lock'): continue
            v = outverdict(b)
            if v == 'UNSATISFIABLE':
                m = checkmeta(b)
                if m.get('done'):
                    if m.get('verdict') == 'VERIFIED' and m.get('rc') == '0':
                        record(c, 'UNSAT-VERIFIED', 'check_s=%s lrat_GB=%.1f' % (m.get('seconds'), os.path.getsize(b + '.lrat') / 1e9))
                    else:
                        record(c, 'UNSAT-CHECK-FAILED', 'rc=%s verdict=%s (artifacts preserved)' % (m.get('rc'), m.get('verdict')))
                elif b not in checks and not os.path.exists(b + '.check.meta') and nchecks < MAXCHECKS:
                    start_check(b, cut); nchecks += 1
            elif v == 'SATISFIABLE':
                record(c, 'SAT', 'model in %s.out' % rel(b))
            else:
                record(c, 'ENDED-NO-ANSWER', 'solver exited without s-line; logs preserved')
        # ---- start never-started cubes
        if len(running) < MAXLANES and not paused and h['diskfree'] > DISK_START and cut - now > 3600 \
                and (h['tctl'] is None or h['tctl'] < T_RESUME) and h['memavail'] > MEM_RESUME:
            for c in cubes():
                if not os.path.exists(base(c) + '.lock'):
                    start_solver(c); break
        # ---- status
        st = ['STATUS %s  (cutoff %s)' % (time.strftime('%Y-%m-%d %H:%M:%S'), time.strftime('%Y-%m-%d %H:%M', time.localtime(cut))),
              'health: Tctl %s C, MemAvailable %.1f GiB, swap used %.1f GiB, disk free %.0f GB' % (h['tctl'], h['memavail'] / 2**30, h['swapused'] / 2**30, h['diskfree'] / 1e9),
              'solvers running %d, paused %d, checks running %d, never started %d' % (len(running), len(paused), len(checks), sum(1 for c in cubes() if not os.path.exists(base(c) + '.lock'))),
              'recorded: %s' % json.dumps({k: v for k, v in sorted(recorded().items())})]
        open(os.path.join(OUT, 'STATUS'), 'w').write('\n'.join(st) + '\n')
        time.sleep(30)

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--dry':
        h = health(); pr = procs()
        print(json.dumps({'health': h, 'n_solvers': sum(1 for l in pr.values() for _, k in l if k == 'solver'),
                          'n_checks': sum(1 for l in pr.values() for _, k in l if k == 'check'), 'cutoff': cutoff(),
                          'recorded': recorded(), 'never_started': [rel(c) for c in cubes() if not os.path.exists(base(c) + '.lock')]}, indent=1))
    else:
        main()
