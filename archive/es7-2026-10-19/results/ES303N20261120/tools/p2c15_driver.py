"""N66 level 15 (N66 <= 54) cube-and-conquer driver p2c15_driver.py = copy of p2c14_driver_r7.py (20 Nov 2026) with: L 15,
warm p2/s15/q.json, OUT p2/c15, units esr-n66-c15-<id>, limits/memory scaled from the cal15 calibration, cal15 leaves adopted
through the same accept(), optional deletion of partial files of timed-out runs (DELETE_PARTIALS, owner decision).
(r7 text:) N66 level 14 (N66 <= 55) cube-and-conquer driver, r7 = copy of r6 for the session of 18 Nov 2026 (KST): deadline 18 Nov 18:00;
partial files of timed-out runs are kept uncompressed (1.1 TB free; no zpart unit).  (r6 text:) r6 = copy of r5 for the night 16-17 Nov 2026 (KST): deadline 17 Nov 09:30,
free-disk floor for new starts (DISK_FLOOR); everything else unchanged from r5.
(r5 text:) N66 level 14 cube-and-conquer driver, 15 Nov 2026 (KST).  Plan: archive/.../N66N20261113/cubes20261115/README.md.
Each cube runs as its own systemd user unit esr-n66-cube-<id> (CPUQuota 98 %, MemoryMax 3.6G, MemorySwapMax 0, nice 10,
RuntimeMaxSec ending before the deadline) through p2_batch_cube.py (copy of p2_batch.py with --cube), whose UNSAT branch runs
the record's p2_cert.sh unchanged in the same unit (trim, p2_cake.py/cake_lpr, rows, template_cert66, final_verify66,
p2_recheck_rows, p2_verify, cert.json).  A cube counts only if accept() passes (the acceptance rules of README section 6).
A cube whose CaDiCaL run hits the time limit is replaced by its two children on the next state of RESPLIT.
Slots: 2 cube units until 06:45 KST, then 3, each start gated on room in the n66 memory track and in the 24 GB total
(budgets read from the running memguard).  Status: p2/c14/campaign_status.json and the record's STATUS_campaign.md.
usage: p2c14_driver.py [--selftest]"""
import datetime, glob, hashlib, itertools, json, os, shutil, subprocess, sys, time

W = '/home/jay/research/data/n66-20261113'
PY = '/home/jay/research/data/six10-linux-20261105/venv.disk/bin/python'
SBFILE = '/home/jay/research/data/roadmap-20261115/n66cubes/sb_clauses.cnf'     # = last 79 lines of b14h2 cert.cnf (critic)
REC = '/home/jay/research/lean/erdos-szekeres-lean/archive/es7-2026-10-19/results/N66N20261113/cubes20261120/STATUS_campaign.md'
CG = '/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice'
OUT, PREFIX = 'p2/c15', 'esr-n66-c15-'
LEVEL, WARM = 15, 'p2/s15/q.json'
DELETE_PARTIALS = True                                        # owner OK 20 Nov 2026 ~11:00 KST: delete cert.lrat/cert.cnf of timed-out runs
ADOPT_DIR = 'p2/cal15'                                        # calibration leaves (same options, same warm file) adopted via accept()
STATUS = os.path.join(W, OUT, 'campaign_status.json')
KST = datetime.timezone(datetime.timedelta(hours=9))
def at(hm, day=18):   # r6: explicit day of November 2026 (r7: default 18)
    h, m = map(int, hm.split(':')); return datetime.datetime(2026, 11, day, h, m, tzinfo=KST).timestamp()
DEADLINE, SLOT3 = at(os.environ.get('C15_DEADLINE_HM', '18:00'), int(os.environ.get('C15_DEADLINE_DAY', '22'))), 0   # c15: from the environment
DISK_FLOOR = 120 * 10**9                                      # r6: no new cube while the data disk has less than 120 GB free
NSLOTS = int(os.environ.get('C15_SLOTS', '5'))                                                    # resume r3 (15 Nov pm, 13:5x): 5 slots after L1 freed a thread
SPLIT = [25, 12, 16, 29, 17, 37]                              # README section 3
RESPLIT = [40, 52, 46, 44, 45, 39, 32, 30, 20, 57, 14, 53, 38, 47, 33, 19, 50, 58, 62, 35, 23, 49]   # r4: A1's P3+P5 order (core usage), 23/49 last
def band(lits):
    """r4: A1's cost band (ANALYSIS_1115PM.md main finding 1); used only for the time limit, memory and pre-split choice"""
    d = {s: b for s, b in lits}
    b = sum(1 for s in SPLIT if d.get(s) == 1) + (1 if d.get(37) == 1 else 0)
    if d.get(25) == 0 and d.get(29) == 1 and d.get(37) == 1: b -= 1
    return b - sum(1 for s, v in lits[6:] if v == 0)
def k_o(lits): return sum(1 for s, v in lits[6:] if v == 1)
def presplit_due(lits):   # r4: A1's P2 (P(cert within 2,400 s) < 0.2): band 6 with k <= 2, band >= 7 with k <= 5
    b, k = band(lits), k_o(lits); return (b == 6 and k <= 2) or (b >= 7 and k <= 5)
def limit_for(lits): return 7200 if band(lits) >= 4 else 3600   # c15: r4's 2400/1200 x 3 (cal15: L15/L14 CPU ratio 2.3 on hhhhhh, conflicts 4.4)
def memmax_for(lits): return '6500M'                          # c15: cake_lpr heap tier 5500 MB + p2_batch fits under 95 %
LIMIT, CERT_ALLOW, MIN_T = 3600, 1800, 900                     # CaDiCaL s per cube (HEURISTIC); s kept for p2_cert.sh; shortest run
RES_MB = int(os.environ.get('C15_RES_MB', '3800'))   # c15: per running cube; env since 20 Nov 12:30 (observed peaks <= 2.7 GB)
QUOTA = 98                                                    # CPUQuota % of a cube unit: 3 x 98 % + the driver's 6 % = 3 threads
MAXMIB = 6500                                           # MemoryMax of a cube unit in MiB (80 % = 2,949)
SEL0 = 988541                                                 # sel_s = SEL0 + s (b14h2 layout 'sel' = [988541, 988610])
REF = json.load(open(os.path.join(W, 'p2/b14h2/it1/layout.json')))
SB_PAIRS = REF['sb_pairs']
assert len(SB_PAIRS) == 27 and REF['sel'] == [SEL0, SEL0 + 69] and REF['W'] == list(range(70)) and REF['L'] == 14
SBC = [[int(x) for x in l.split()[:-1]] for l in open(SBFILE) if l.strip()]
assert len(SBC) == 79

def now_s(): return time.strftime('%H:%M:%S')
def lit(s, b): return SEL0 + s if b else -(SEL0 + s)
def cid(lits): return ''.join('o' if b else 'h' for _, b in lits[:6]) + ''.join(f'_{s}{"o" if b else "h"}' for s, b in lits[6:])

def up_refuted(lits):
    """unit propagation over the 79 SB clauses with the fixed units (states 0, 1 occupied) and the cube units (planning only)"""
    a = {lit(0, 1), lit(1, 1)} | {lit(s, b) for s, b in lits}
    if any(-x in a for x in a): return True
    ch = True
    while ch:
        ch = False
        for c in SBC:
            if any(l in a for l in c): continue
            free = [l for l in c if -l not in a]
            if not free: return True
            if len(free) == 1: a.add(free[0]); ch = True
    return False

def covered(cubes):
    """exact: True iff the disjunction of the cubes (sets of DIMACS literals) is a tautology"""
    if any(not c for c in cubes): return True
    if not cubes: return False
    v = abs(next(iter(cubes[0])))
    return covered([c - {v} for c in cubes if -v not in c]) and covered([c - {-v} for c in cubes if v not in c])

def selftest():
    assert covered([frozenset([1]), frozenset([-1, 2]), frozenset([-1, -2])]) and not covered([frozenset([1]), frozenset([-1, 2])])
    assert not covered([]) and covered([frozenset()])
    full = [[[s, b] for s, b in zip(SPLIT, bits)] for bits in itertools.product((1, 0), repeat=6)]
    up = [c for c in full if up_refuted(c)]
    assert len(up) == 8 and all(dict(map(tuple, c))[25] == 0 and dict(map(tuple, c))[29] == 1 and dict(map(tuple, c))[37] == 0 for c in up), up
    assert covered([frozenset(lit(s, b) for s, b in c) for c in full])
    assert not covered([frozenset(lit(s, b) for s, b in c) for c in full[1:]])
    assert not up_refuted([[25, 0], [12, 0], [16, 0], [29, 0], [17, 0], [37, 0]])
    return up

def add(st, lits, parent):
    i = cid(lits)
    if i in st['cubes']: return
    st['seq'] += 1
    st['cubes'][i] = {'id': i, 'lits': lits, 'holes': sum(1 for _, b in lits if b == 0), 'up_refuted': up_refuted(lits), 'parent': parent,
                      'depth': len(lits) - 6, 'seq': st['seq'], 'status': 'queued', 'unit': PREFIX + i, 'out': f'{OUT}/{i}.out'}

def prio(c): return (0 if c['id'] == 'hhhhhh' else 1 if c['up_refuted'] else 2, -c['holes'], c['depth'], c['seq'])

def active(unit): return subprocess.run(['systemctl', '--user', 'is-active', '--quiet', unit]).returncode == 0
def active_cubes():
    r = subprocess.run(['systemctl', '--user', 'list-units', PREFIX + '*', '--type=service', '--state=active', '--plain', '--no-legend'],
                       capture_output=True, text=True).stdout
    return [l.split()[0][:-len('.service')] for l in r.splitlines() if l.strip()]

def anon_mb(unit):
    try:
        return sum(int(l.split()[1]) for l in open(f'{CG}/{unit}.service/memory.stat') if l.split()[0] in ('anon', 'shmem')) // 1048576
    except (OSError, ValueError, IndexError):
        return 0

def guard():
    """(n66 budget, total budget) in MB of the running memguard (argv: bash .../memguard.sh esr TOTAL track=MB ...), or None"""
    best = None
    for pid in subprocess.run(['pgrep', '-f', 'memguard.sh'], capture_output=True, text=True).stdout.split():
        try: argv = open(f'/proc/{pid}/cmdline').read().split('\0')
        except OSError: continue
        for i in (0, 1):
            if len(argv) > i + 2 and argv[i].endswith('/memguard.sh') and argv[i + 1] == 'esr' and argv[i + 2].isdigit():
                kv = dict(x.split('=', 1) for x in argv[i + 3:] if '=' in x)
                g = (int(kv.get('n66', 3000)), int(argv[i + 2]))
                best = g if best is None else (min(best[0], g[0]), min(best[1], g[1]))
    return best

def room():
    g = guard()
    if not g: return False, 'no memory guard running'
    n66 = tot = 0
    for p in glob.glob(CG + '/esr-*.service'):
        u = os.path.basename(p)[:-len('.service')]; a = anon_mb(u)
        r = max(a, RES_MB) if u.startswith(PREFIX) else a           # a running cube is reserved at its expected peak
        tot += r; n66 += r if u.startswith('esr-n66-') else 0
    fr = shutil.disk_usage(W).free
    if fr < DISK_FLOOR: return False, f'disk floor: {fr // 10**9} GB free < {DISK_FLOOR // 10**9} GB'
    if n66 + RES_MB > g[0] - 200: return False, f'n66 track: {n66} + {RES_MB} MB > {g[0]} - 200'
    if tot + RES_MB > g[1] - 500: return False, f'all research units: {tot} + {RES_MB} MB > {g[1]} - 500'
    return True, f'n66 {n66} MB of {g[0]}, all {tot} MB of {g[1]}'

CPU_CAP_MILLI = int(os.environ.get('C15_CPU_CAP_MILLI', '16000'))   # 20 Nov 17:45: owner allowed 80-90 % of the 32 logical CPUs; the cap is set at launch

def cpu_free_milli():
    """16-thread cap minus the summed CPUQuota of the active esr-* units, in thousandths of a thread (cpu_free.sh's rule, unrounded)"""
    used = 0
    for l in subprocess.run(['systemctl', '--user', 'list-units', 'esr-*', '--type=service', '--state=active', '--plain', '--no-legend'], capture_output=True, text=True).stdout.splitlines():
        q = subprocess.run(['systemctl', '--user', 'show', l.split()[0], '-p', 'CPUQuotaPerSecUSec', '--value'], capture_output=True, text=True).stdout.strip()
        used += int(q[:-2]) if q.endswith('ms') else int(float(q[:-1]) * 1000) if q.endswith('s') and q[:-1].replace('.', '').isdigit() else 1000
    return CPU_CAP_MILLI - used

def max_slots(st, t): return max(1, NSLOTS - st.get('slot_penalty', 0))

def launch(st, c):
    t = time.time(); remain = int(DEADLINE - t - 60); T = min(limit_for(c['lits']), remain - CERT_ALLOW)
    if T < MIN_T: return False
    o = f'{OUT}/{c["id"]}'
    cmd = (f"{PY} -u p2_batch_cube.py --out {o}.json --dir {o} --L {LEVEL} --rows mono/rows_1832.json --warm {WARM} --seed 11 "
           f"--tauclose --sb --cube {','.join(f'{s}:{b}' for s, b in c['lits'])} '--cadopts=--unsat -t {T}' --secs {T} > {o}.out 2>&1; "
           f"for d in {o}/it*; do [ -f $d/cert.json ] && ./c15_post.sh $d; done; true")   # c15: zstd trim.lrat + cert.cnf of a certified leaf (owner OK)
    r = subprocess.run(['systemd-run', '--user', f'--unit={c["unit"]}', '-p', f'CPUQuota={QUOTA}%', '-p', f'MemoryMax={memmax_for(c["lits"])}', '-p', 'MemorySwapMax=0',
                        '-p', f'RuntimeMaxSec={remain}', '--nice=10', f'--working-directory={W}', '-E', 'ETV_A=4', '-E', 'ETV_B=4',
                        '-E', f'P2_UNIT={c["unit"]}', '/bin/bash', '-c', cmd], capture_output=True, text=True)
    c.update({'started': now_s(), 't0': t, 'limit_s': T, 'runtime_max_s': remain, 'launch_rc': r.returncode})
    if r.returncode:
        c['status'] = 'failed'; c['why'] = 'systemd-run: ' + (r.stderr or r.stdout)[-300:]; log(st, f'launch failed {c["id"]}: {c["why"]}')
        return True
    c['status'] = 'running'; c['band'] = band(c['lits']); log(st, f'start {c["id"]} (holes {c["holes"]}, band {c["band"]}, UP {c["up_refuted"]}, limit {T} s, MemoryMax {memmax_for(c["lits"])})')
    return True

def sha256(p):
    h = hashlib.sha256()
    with open(p, 'rb') as g:
        for chunk in iter(lambda: g.read(1 << 24), b''): h.update(chunk)
    return h.hexdigest()

def accept(c):
    """README section 6: cert.json and verify.json ALL_OK; the exact cake_lpr line; L 14; W = range(70); the b14h2 SB pair list;
    cube = the cube's literals in layout, verify and cert; no unclassified clause; trim.cnf hash recomputed here."""
    d = os.path.join(W, c['certdir'])
    try:
        cj = json.load(open(d + '/cert.json')); vj = json.load(open(d + '/verify.json')); lay = json.load(open(d + '/layout.json'))
        cake = [l.rstrip('\n') for l in open(d + '/cake.out')]
        lits = [list(x) for x in c['lits']]
        chk = {'cert_ALL_OK': cj.get('ALL_OK') is True, 'verify_ALL_OK': vj.get('ALL_OK') is True, 'cake_line': 's VERIFIED UNSAT' in cake,
               'L': lay['L'] == vj['budget'] == cj['budget'] == LEVEL, 'W': lay['W'] == list(range(70)) and cj['W_size'] == 70,
               'sb_pairs': lay.get('sb_pairs') == vj.get('sb_pairs') == cj.get('sb_pairs') == SB_PAIRS,
               'cube': lay['cube'] == vj['cube'] == cj['cube'] == lits, 'unclassified_0': vj.get('unclassified') == 0,
               'sel': lay['sel'] == [SEL0, SEL0 + 69], 'trim_cnf_sha256': sha256(d + '/trim.cnf') == vj['trim_cnf_sha256'] == cj['trim_cnf_sha256']}
    except (OSError, ValueError, KeyError, TypeError) as e:
        return False, f'certificate files incomplete ({type(e).__name__}: {e})', {}
    bad = [k for k, v in chk.items() if not v]
    info = {'trim_cnf_sha256': cj.get('trim_cnf_sha256'), 'trim_lrat_sha256': cj.get('trim_lrat_sha256'), 'full_cnf_sha256': cj.get('full_cnf_sha256'),
            'trim_cnf_clauses': cj.get('trim_cnf_clauses'), 'trim_lrat_bytes': cj.get('trim_lrat_bytes'), 'used_rows': (cj.get('used') or {}).get('used_rows'),
            'kinds': cj.get('kinds')}
    return not bad, ('ok' if not bad else 'failed checks: ' + ', '.join(bad)), info

def cad_stats(c):
    """conflicts and wall of the last CaDiCaL run of the cube (from cadical.log)"""
    its = sorted(glob.glob(os.path.join(W, OUT, c['id'], 'it*', 'cadical.log')), key=lambda p: int(p.split('/it')[-1].split('/')[0]))
    s = {}
    if its:
        try:
            for l in open(its[-1]):
                if l.startswith('c conflicts:'): s['conflicts'] = int(l.split()[2])
                if l.startswith('c total process time'): s['process_s'] = float(l.split()[-2])
                if l.startswith('c maximum resident'): s['cadical_rss_mb'] = float(l.split()[-2])
        except (OSError, ValueError, IndexError) as e:           # r2: guarded (critic issue 5)
            s['cad_stats_error'] = f'{type(e).__name__}: {e}'
    return s

def finalize(st, c):
    ev = []
    try:
        for l in open(os.path.join(W, c['out'])):
            try: ev.append(json.loads(l))
            except ValueError: pass
    except OSError: pass
    c['ended'] = now_s(); c.update(cad_stats(c))
    c['wall_s'] = max([e['secs'] for e in ev if isinstance(e.get('secs'), (int, float))] or [round(time.time() - c.get('t0', time.time()), 1)])
    kinds = [e.get('event') for e in ev]
    unsat = [e for e in ev if e.get('event') == 'UNSAT']
    if unsat:
        c['certdir'] = unsat[-1]['certdir']; c['solve_secs'] = unsat[-1].get('solve_secs')
        c['p2_cert_exit'] = next((e.get('exit') for e in ev if e.get('event') == 'p2_cert.sh'), None)
        ok, why, info = accept(c); c['accept'] = why; c.update(info)
        if ok:
            c['status'] = 'certified'
            d = os.path.join(W, c['certdir'])
            if not os.path.exists(d + '/trim.lrat.zst'):                # keep the LRAT the certificate relies on, also as zstd
                z = subprocess.run(['nice', '-n', '10', 'zstd', '-q', '-k', '-3', '-T1', d + '/trim.lrat', '-o', d + '/trim.lrat.zst'], capture_output=True, text=True)
                c['zstd_rc'] = z.returncode
        else:
            c['status'] = 'unsat_not_accepted'
            if time.time() > DEADLINE - 180: c['why'] = 'cut at the deadline during p2_cert.sh; resume: ./p2_cert.sh ' + c['certdir']
    elif any(e.get('event') == 'SAT_MODEL' for e in ev):
        c['status'] = 'SAT'; c['sat'] = [e for e in ev if e.get('event') == 'SAT_MODEL'][-1]
    elif any(e.get('event') == 'cadical ended without verdict' and e.get('exit') == 0 for e in ev):   # r2: time-limit ends only (critic issue 4)
        used = {s for s, _ in c['lits']}; nxt = next((s for s in RESPLIT if s not in used), None)
        freed = 0
        for p in glob.glob(os.path.join(W, OUT, c['id'], 'it*', 'cert.lrat')) + glob.glob(os.path.join(W, OUT, c['id'], 'it*', 'cert.cnf')):
            freed += os.path.getsize(p)                               # r2: partial files are KEPT (deletion is an owner question)
            if DELETE_PARTIALS: os.remove(p)                          # c15: only with the owner's OK (a timed-out run certifies nothing)
        c['deleted_partial_bytes' if DELETE_PARTIALS else 'kept_partial_bytes'] = freed
        if nxt is None:
            c['status'] = 'timeout_no_split_state'
        else:
            c['status'] = 'split'; c['split_on'] = nxt; c['children'] = [cid(c['lits'] + [[nxt, 1]]), cid(c['lits'] + [[nxt, 0]])]
            for b in (1, 0): add(st, c['lits'] + [[nxt, b]], c['id'])
    else:
        stopped = os.path.exists(os.path.join(W, f'MEMGUARD_STOPPED_{c["unit"]}.txt'))
        c['status'] = 'failed'
        c['why'] = ('stopped by the memory guard' if stopped else 'cut at the deadline' if time.time() > DEADLINE - 180
                    else f'no verdict; last events {[e.get("event") for e in ev][-3:]}')
        if stopped:
            st['slot_penalty'] = st.get('slot_penalty', 0) + 1    # never restart unchanged: one slot fewer from now on
    log(st, f'end {c["id"]}: {c["status"]} {c.get("accept", c.get("why", ""))} (wall {c["wall_s"]} s, conflicts {c.get("conflicts")})')

def adopt(st):
    """c15: a depth-0 cube solved by cal15.sh (same p2_batch_cube options, same warm file) counts as certified only if accept() passes"""
    for c in st['cubes'].values():
        o = os.path.join(W, ADOPT_DIR, c['id'] + '.out')
        if c['depth'] != 0 or not os.path.exists(o): continue
        ev = []
        for l in open(o):
            try: ev.append(json.loads(l))
            except ValueError: pass
        un = [e for e in ev if e.get('event') == 'UNSAT']
        if not un: continue
        c.update({'certdir': un[-1]['certdir'], 'solve_secs': un[-1].get('solve_secs'), 'out': os.path.relpath(o, W), 'adopted_from': ADOPT_DIR,
                  'p2_cert_exit': next((e.get('exit') for e in ev if e.get('event') == 'p2_cert.sh'), None)})
        ok, why, info = accept(c); c['accept'] = why; c.update(info)
        if ok:
            c['status'] = 'certified'; d = os.path.join(W, c['certdir'])
            if not os.path.exists(d + '/trim.lrat.zst'):
                z = subprocess.run(['nice', '-n', '10', 'zstd', '-q', '-k', '-3', '-T1', d + '/trim.lrat', '-o', d + '/trim.lrat.zst'], capture_output=True, text=True)
                c['zstd_rc'] = z.returncode
        log(st, f'adopt {c["id"]} from {ADOPT_DIR}: {"certified" if ok else "NOT accepted"} ({why})')

def log(st, msg):
    st['log'].append(f'{now_s()} {msg}'); st['log'] = st['log'][-300:]; print(f'{now_s()} {msg}', flush=True)

def cover(st):
    leaves = [c for c in st['cubes'].values() if c['status'] != 'split']
    sets = lambda cs: [frozenset(lit(s, b) for s, b in c['lits']) for c in cs]
    cert = [c for c in leaves if c['status'] == 'certified']
    certsets = []
    for c in cert:                                                    # cube literals from verify.json, not from the plan (README section 6)
        v = json.load(open(os.path.join(W, c['certdir'], 'verify.json')))
        certsets.append(frozenset(lit(s, b) for s, b in v['cube']))
    return {'leaves': len(leaves), 'leaf_cover_ok': covered(sets(leaves)), 'certified_leaves': len(cert),
            'certified_cover_ok': covered(certsets) if certsets else False}

def write_status(st, final=False):
    t = time.time()
    counts = {}
    for c in st['cubes'].values(): counts[c['status']] = counts.get(c['status'], 0) + 1
    st['cover'] = cover(st); st['counts'] = counts; st['updated'] = now_s(); st['final'] = final
    st['slots_now'] = max_slots(st, t); st['guard'] = guard()
    json.dump(st, open(STATUS + '.tmp', 'w'), indent=1); os.replace(STATUS + '.tmp', STATUS)
    cv = st['cover']
    head = ('**Every leaf has an accepted certificate (cover complete): N66 <= 54 follows (as N66 <= 55 did at level 14); needs an independent check before it is stated.**' if cv['certified_cover_ok'] else
            '**N66 <= 54 is NOT decided.** N66 <= 55 (level 14 cube campaign, CERTIFIED) remains the bound.')
    L = [f'# N66 level-15 cube campaign: status {"(final)" if final else "(live)"}', '',
         f'{head} Written by `W/p2c15_driver.py` at {st["updated"]} KST, {time.strftime("%d")} November 2026{" (final)" if final else ""}; '
         f'plan and labels in `README.md` of this folder. W = `{W}`; per-cube files in `W/{OUT}/<id>/it<k>/`; machine status '
         f'`W/{OUT}/campaign_status.json`.', '',
         '## Allocation', '',
         f'- Driver p2c15_driver.py (copy of p2c14_driver_r7.py; r4/r5 rules A1 P1-P3 with the time limits x 3: band >= 4 gets 7,200 s, else 3,600 s; MemoryMax 6500M; pre-split of band-6/7 cubes; A1 split order): cube units `esr-n66-c15-<id>`: 1 thread each (CPUQuota 98 %), MemorySwapMax 0, nice 10, RuntimeMaxSec ending '
         f'by {st["deadline"]}. At most {NSLOTS} at a time (now {st["slots_now"]}; memguard slot penalty {st.get("slot_penalty", 0)}). No new cube while the disk has less than {DISK_FLOOR // 10**9} GB free. Partial files of timed-out runs: {"deleted (owner OK)" if DELETE_PARTIALS else "kept"}.',
         f'- Each start also needs room: running cubes reserved at {RES_MB:,} MB each, n66 track + {RES_MB:,} <= n66 budget - 200 MB and all research '
         f'units + {RES_MB:,} <= total - 500 MB (budgets from the running memguard: {st["guard"]}), and 0.98 free thread under the 16-thread cap (summed CPUQuota of active esr-* units).',
         '- The cake_lpr step runs inside the cube unit after CaDiCaL exits (p2_cert.sh -> p2_cake.py, unchanged; heap tiers 2000/3200/4500/5500 MB).',
         f'- Driver unit `esr-n66-drv15`: CPUQuota 6 %, MemoryMax 300M. Calibration leaves from `W/{ADOPT_DIR}` are adopted only through accept().', '',
         '## Cover argument', '',
         '- Split states 25 12 16 29 17 37, sel_s = 988541 + s; o = occupied = +sel_s, h = hole = -sel_s; cube ids list the six signs in '
         'that order, then `_<s><o|h>` for every re-split state. The 64 sign patterns are all assignments of the six variables, so their '
         'disjunction is a tautology.',
         '- Unit propagation on the 79 SB clauses refutes 8 of the 64 (all with 25 h, 29 o, 37 h): ' +
         ', '.join(sorted(c['id'] for c in st['cubes'].values() if c['depth'] == 0 and c['up_refuted'])) +
         '. They run through the same pipeline; like every cube they count only with their own accepted certificate.',
         '- A cube whose CaDiCaL run reaches its time limit is replaced by its children c AND s occupied, c AND s hole, s = the first state of '
         + ' '.join(map(str, RESPLIT)) + ' not in c (A1 order since r4; corrected 16 Nov after CN issue 6). The two children cover the parent, so the leaves always cover the 2^6 split.',
         f'- Leaves now: {cv["leaves"]}; exact leaf cover check: {"COVER_OK" if cv["leaf_cover_ok"] else "NOT COVERED (bug)"}.',
         f'- Accepted certificates: {cv["certified_leaves"]} of {cv["leaves"]} leaves. Cover by accepted certificates (cube literals read '
         f'from each verify.json): {"COVER_OK" if cv["certified_cover_ok"] else "not complete"}.',
         '- Acceptance (level-14 README section 6, with L = 15): cert.json and verify.json ALL_OK; cake.out has the exact line `s VERIFIED UNSAT`; L = 15; '
         'W = range(70); the 27-pair SB list of b14h2; the cube field of layout, verify and cert equals the cube; 0 unclassified clauses; '
         'trim.cnf SHA-256 recomputed by the driver. Rows are justified by template_cert66 without cube assumptions.', '',
         '## Counts', '', ', '.join(f'{k}: {v}' for k, v in sorted(counts.items())), '',
         '## Cubes (priority order)', '',
         '| id | holes | UP | status | started | wall s | conflicts | note |', '|---|---|---|---|---|---|---|---|']
    for c in sorted(st['cubes'].values(), key=prio):
        note = c.get('accept') if c['status'] in ('certified', 'unsat_not_accepted') else c.get('why', '')
        if c['status'] == 'certified': note = f'trim.cnf {c.get("trim_cnf_sha256", "")}; rows {c.get("used_rows")}'
        if c['status'] == 'split': note = f'split on {c["split_on"]}'
        if c.get('peak_anon_mb'): note = f'{note}; peak {c["peak_anon_mb"]} MB'.lstrip('; ')
        L.append(f'| {c["id"]} | {c["holes"]} | {"yes" if c["up_refuted"] else ""} | {c["status"]} | {c.get("started", "")} | '
                 f'{c.get("wall_s", "")} | {c.get("conflicts", "")} | {note} |')
    L += ['', '## Log (last 40)', '', '```'] + st['log'][-40:] + ['```', '',
          '## Monitor', '', '```bash', f'cat {STATUS} | head -c 2000', 'systemctl --user list-units "esr-n66-*"',
          'journalctl --user -u esr-n66-drv15 -n 30 --no-pager', '```', '']
    open(REC + '.tmp', 'w').write('\n'.join(L)); os.replace(REC + '.tmp', REC)

def main():
    os.chdir(W)
    os.makedirs(os.path.join(W, OUT), exist_ok=True)              # c15: the output folder did not exist on the first start (crash 11:05)
    up = selftest()
    if '--selftest' in sys.argv:
        st = {'cubes': {}, 'seq': 0}
        for bits in itertools.product((1, 0), repeat=6): add(st, [[s, b] for s, b in zip(SPLIT, bits)], None)
        q = sorted(st['cubes'].values(), key=prio)
        print('SELFTEST_OK; UP-refuted:', [cid(c) for c in up]); print('order:', ' '.join(c['id'] for c in q)); print('guard', guard(), 'room', room(), 'cpu_free_milli', cpu_free_milli())
        return
    if os.path.exists(STATUS):
        st = json.load(open(STATUS)); st['deadline'] = time.strftime('%H:%M KST %d Nov', time.localtime(DEADLINE)); st['final'] = False
        log(st, f'driver c15 restarted; state loaded; {NSLOTS} slots, band limits 3600/7200 s, presplit, A1 order, disk floor {DISK_FLOOR // 10**9} GB, delete partials {DELETE_PARTIALS}')
    else:
        st = {'cubes': {}, 'seq': 0, 'log': [], 'started': now_s(), 'deadline': time.strftime('%H:%M KST %d Nov', time.localtime(DEADLINE))}
        for bits in itertools.product((1, 0), repeat=6): add(st, [[s, b] for s, b in zip(SPLIT, bits)], None)
        log(st, f'driver started; 64 cubes; L {LEVEL}; warm {WARM}')
        adopt(st)
    stop, lastmd = False, 0
    while True:
        t = time.time(); changed = False
        for c in list(st['cubes'].values()):
            if c['status'] == 'running':
                if active(c['unit']):
                    c['peak_anon_mb'] = max(c.get('peak_anon_mb', 0), anon_mb(c['unit']))
                    if c['peak_anon_mb'] > 0.8 * MAXMIB and not c.get('over80'): c['over80'] = True; log(st, f'{c["id"]} above 80 % of MemoryMax ({c["peak_anon_mb"]} MB)')
                else:
                    finalize(st, c); changed = True
                    if c['status'] == 'SAT': stop = True
        if stop and not st.get('stopped'):
            st['stopped'] = True; log(st, 'SAT cube: level 14 relaxation satisfiable in a cube; stopping the campaign')
            for c in st['cubes'].values():
                if c['status'] == 'running': subprocess.run(['systemctl', '--user', 'stop', c['unit']]); c['status'] = 'stopped_after_SAT'
        if not stop:   # r4: A1's P2 staircase pre-split (no run): split queued hopeless cubes down the 'o' side
            for c in list(st['cubes'].values()):
                if c['status'] == 'queued' and presplit_due(c['lits']):
                    used = {s for s, _ in c['lits']}; nxt = next((s for s in RESPLIT if s not in used), None)
                    if nxt is None: continue
                    c.update({'status': 'split', 'split_on': nxt, 'presplit': True, 'band': band(c['lits']),
                              'children': [cid(c['lits'] + [[nxt, 1]]), cid(c['lits'] + [[nxt, 0]])]})
                    for bb in (1, 0): add(st, c['lits'] + [[nxt, bb]], c['id'])
                    log(st, f'presplit {c["id"]} (band {c["band"]}) on {nxt}'); changed = True
        if not stop and t < DEADLINE - 60 - CERT_ALLOW - MIN_T:
            n = len(active_cubes())
            while n < max_slots(st, t):
                q = [c for c in st['cubes'].values() if c['status'] == 'queued']
                if not q: break
                ok, why = room(); st['gate'] = why
                if not ok: break
                if cpu_free_milli() < QUOTA * 10: st['gate'] = f'no free thread under the {CPU_CAP_MILLI / 1000:g}-thread cap'; break
                if not launch(st, min(q, key=prio)): break
                n += 1; changed = True; time.sleep(3)
        running = [c for c in st['cubes'].values() if c['status'] == 'running']
        queued = [c for c in st['cubes'].values() if c['status'] == 'queued']
        done = not running and (not queued or stop or t >= DEADLINE - 60 - CERT_ALLOW - MIN_T)
        if done or t >= DEADLINE - 40:
            if not done: log(st, f'deadline: {len(running)} cube units still running (their RuntimeMaxSec ends them by the deadline)')
            write_status(st, final=True); log(st, 'driver end'); write_status(st, final=True); return
        if changed or t - lastmd > 300:
            write_status(st); lastmd = t
        else:
            st['updated'] = now_s(); json.dump(st, open(STATUS + '.tmp', 'w'), indent=1); os.replace(STATUS + '.tmp', STATUS)
        time.sleep(15)

if __name__ == '__main__':
    main()
