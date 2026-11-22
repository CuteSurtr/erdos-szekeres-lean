#!/usr/bin/env python3
"""n66enc-recheck: byte identity of the FROZEN N66 printer exe (n66print, SHA-256 FROZEN below) with the certified
level-14 campaign files.  usage: recheck.py selftest | stage1 | trims | fullall

  stage1   selftest; leaf map (n66print leaves = campaign lits); EAGER (n66print eager = cert.cnf lines 2..1+E of
           leaf 131 = hhhhhh); FULL 131 (n66print full = whole hhhhhh cert.cnf); negative control (one quadruple dropped)
  trims    TRIM i for all 132 leaves (n66print trim i desc/i.txt = trim.cnf); negative control (one descriptor changed)
  fullall  FULL i for the other 131 leaves, after a layout pre-screen (extension; out-of-scope leaves are not mismatches)

The exe's stdout is streamed (never stored) and compared byte for byte with the reference file while both are hashed.
MATCH = exit 0, nonempty output, byte equality, and printed SHA-256 = fresh hash of the reference = every recorded hash
(15 Nov campaign files).  Results: out/<stage>.jsonl (one object per piece; finished pieces are skipped on restart),
out/status_<stage>.json, logs/<stage>.log.  Every exe start is gated: no YIELD file, Tctl < 86 C, ag anon + 2400 <= 8000 MB."""
import hashlib, json, os, re, shutil, subprocess, sys, time

FROZEN = '98d121bad04264221de66e583db0df08f4431d1093b4b7a05114316accccaa46'
D = '/home/jay/research/data/formalize-20261122/n66enc-recheck'
ENC = '/home/jay/research/data/formalize-20261122/n66enc'
W = '/home/jay/research/data/n66-20261113'
REC = ('/home/jay/research/lean/erdos-szekeres-lean/archive/es7-2026-10-19/results/N66N20261113/cubes20261115/'
       'STATUS_campaign.md')
EXE, ORIG = f'{D}/bin/n66print', f'{ENC}/build/bin/n66print'
YIELD = '/home/jay/research/data/agents-20261121/YIELD'
CG = '/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice'
HEX = re.compile(r'^[0-9a-f]{64}$')
CHUNK = 1 << 22
STAGE = sys.argv[1] if len(sys.argv) > 1 else 'selftest'
LOGF = f'{D}/logs/{STAGE}.log'


def log(msg):
    line = f'{time.strftime("%F %T")} {msg}'
    print(line, flush=True)
    with open(LOGF, 'a') as f: f.write(line + '\n')


def sha_file(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(CHUNK), b''): h.update(b)
    return h.hexdigest()


def exe_sha():
    h = sha_file(EXE)
    if h != FROZEN: raise SystemExit(f'ABORT: {EXE} has SHA-256 {h}, not the frozen {FROZEN}')
    return h


# ---------- gate (rule 3) ----------
def tctl():
    m = re.search(r'Tctl:\s*\+?([0-9.]+)', subprocess.run(['sensors'], capture_output=True, text=True).stdout)
    return float(m.group(1)) if m else None


def ag_anon_mb():
    s = 0
    for u in os.listdir(CG):
        if u.startswith('esr-ag-') and u.endswith('.service'):
            try:
                for l in open(f'{CG}/{u}/memory.stat'):
                    k, v = l.split()
                    if k in ('anon', 'shmem'): s += int(v)
            except OSError: pass
    return s // 1048576


def gate():
    t0 = time.time()
    while True:
        y, t, a = os.path.exists(YIELD), tctl(), ag_anon_mb()
        if not y and t is not None and t < 86 and a + 2400 <= 8000: return dict(tctl=t, ag_anon_mb=a)
        if y: t0 = time.time()          # YIELD pauses without limit; the 45 min bound is for heat/memory only
        elif time.time() - t0 > 45 * 60: raise SystemExit(f'gate gave up after 45 min: tctl={t} ag_anon={a} MB')
        log(f'gate wait: yield={y} tctl={t} ag_anon={a} MB')
        time.sleep(60)


# ---------- run the exe, stream its stdout ----------
def spawn(args, errpath, sink):
    t0 = time.time()
    with open(errpath, 'wb') as e:
        p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=e)
        try:
            for b in iter(lambda: p.stdout.read(CHUNK), b''): sink(b)
        finally:
            p.stdout.close()
            _, st, ru = os.wait4(p.pid, 0)
            p.returncode = os.waitstatus_to_exitcode(st)
    if p.returncode < 0: raise RuntimeError(f'{args[:3]} killed by signal {-p.returncode}; piece not recorded')
    return p.returncode, ru.ru_maxrss, round(time.time() - t0, 2), open(errpath, errors='replace').read()[-2000:].strip()


def run_cmp(args, ref, mode, errpath):
    """mode 'whole': stdout must equal the whole file ref.  mode 'body': ref minus its first line (the DIMACS header);
    stdout must be a byte prefix of it (the caller checks the line count).  ref_sha: fresh SHA-256 of the whole file
    (whole) or of the compared segment (body)."""
    hp, hr = hashlib.sha256(), hashlib.sha256()
    s = dict(n=0, lines=0, eq=True, last=b'', first_diff=None)
    with open(ref, 'rb') as r:
        if mode == 'body': r.readline()
        def sink(b):
            rb = r.read(len(b)); hr.update(rb)
            if rb != b and s['eq']:
                k = next((j for j in range(min(len(rb), len(b))) if rb[j] != b[j]), min(len(rb), len(b)))
                s['eq'] = False; s['first_diff'] = dict(byte=s['n'] + k, line=s['lines'] + b[:k].count(b'\n') + 1)
            hp.update(b); s['n'] += len(b); s['lines'] += b.count(b'\n'); s['last'] = b[-1:]
        rc, rss, wall, err = spawn(args, errpath, sink)
        rest = r.read(CHUNK) if mode == 'whole' else b''
        if rest and s['eq']: s['eq'] = False; s['first_diff'] = dict(byte=s['n'], line=s['lines'] + 1, why='output ended first')
        while rest: hr.update(rest); rest = r.read(CHUNK)
    return dict(rc=rc, printed_sha=hp.hexdigest(), printed_bytes=s['n'], printed_lines=s['lines'],
                ends_nl=s['last'] == b'\n', ref_sha=hr.hexdigest(), equal=s['eq'], first_diff=s['first_diff'],
                maxrss_kb=rss, wall_s=wall, stderr=err)


def verdict(r, recs, extra_ok=True):
    hs = [r['printed_sha'], r['ref_sha']] + list(recs)
    ok = (r['rc'] == 0 and r['printed_bytes'] > 0 and r['equal'] and extra_ok
          and all(isinstance(h, str) and HEX.match(h) for h in hs) and len(set(hs)) == 1)
    return 'MATCH' if ok else 'MISMATCH'


# ---------- bookkeeping ----------
def load_done(stage):
    p = f'{D}/out/{stage}.jsonl'
    return {json.loads(l)['piece']: json.loads(l) for l in open(p)} if os.path.exists(p) else {}


def record(stage, rec):
    rec['time'] = time.strftime('%F %T')
    with open(f'{D}/out/{stage}.jsonl', 'a') as f: f.write(json.dumps(rec) + '\n')
    log(f"{rec['piece']}: {rec['verdict']}" + (f" rss={rec['maxrss_kb']} KB wall={rec['wall_s']} s" if 'maxrss_kb' in rec else ''))


def status(stage, extra=None):
    done = load_done(stage)
    vs = [v['verdict'] for v in done.values()]
    st = dict(stage=stage, updated=time.strftime('%F %T'), exe=EXE, exe_sha256=sha_file(EXE), frozen=FROZEN,
              pieces=len(done), verdicts={v: vs.count(v) for v in sorted(set(vs))},
              max_exe_rss_kb=max([v.get('maxrss_kb', 0) for v in done.values()] or [0]))
    st.update(extra or {})
    json.dump(st, open(f'{D}/out/status_{stage}.json', 'w'), indent=1)
    return st


def cgroup_peak():
    try:
        cg = open('/proc/self/cgroup').read().strip().split('::', 1)[1]
        return int(open(f'/sys/fs/cgroup{cg}/memory.peak').read())
    except (OSError, IndexError, ValueError): return None


def campaign():
    order = [l.strip() for l in open(f'{ENC}/tools/leaf_order.txt') if l.strip()]
    st = json.load(open(f'{W}/p2/c14/campaign_status.json'))['cubes']
    return order, st


def certdir(c): return f"{W}/{c['certdir']}"


def mkctl_child(state, layout, outdir):
    """Own extraction (independent of ../n66enc/tools/ctl_inputs.py) of the runtime data p2_write.py used:
    the state file's activated quadruples in file order, and layout.json row_list (rows in clause order)."""
    st = json.load(open(state)); lay = json.load(open(layout))
    os.makedirs(outdir, exist_ok=True)
    with open(f'{outdir}/act.txt', 'w') as f: f.write(''.join('%d %d %d %d\n' % tuple(q) for q in st['activated']))
    with open(f'{outdir}/rows.txt', 'w') as f: f.write(''.join(' '.join(map(str, s)) + '\n' for s in lay['row_list']))
    print(json.dumps(dict(nact=len(st['activated']), cube=st.get('cube'), sb_pairs=st.get('sb_pairs'), L=st.get('L'))))


def mk_ctl(lay, layout_path, outdir):
    o = json.loads(subprocess.run([sys.executable, '-I', __file__, 'mkctl', lay['state'], layout_path, outdir],
                                  capture_output=True, text=True, check=True).stdout)
    return f'{outdir}/act.txt', f'{outdir}/rows.txt', o['nact'], o['cube'], o['sb_pairs'], o['L']


def full_piece(i, cid, c, lay, pa, pr, tag='full'):
    cd = certdir(c)
    cj = json.load(open(f'{cd}/cert.json'))
    recs = [cj.get('full_cnf_sha256'), c.get('full_cnf_sha256'), lay.get('cnf_sha256')]
    g = gate(); h = exe_sha()
    r = run_cmp([EXE, 'full', str(i), pa, pr], f'{cd}/cert.cnf', 'whole', f'{D}/logs/{tag}_{i}.err')
    want_err = f"leaf {i} clauses {lay['clauses']} act {lay['activated_quadruples']} rows {len(lay['row_list'])} bad 0"
    extra = r['stderr'] == want_err and r['printed_bytes'] == lay['cnf_bytes']
    return dict(piece=f'{tag}:{i}', leaf=i, cube=cid, exe_sha256=h, gate=g, args=['full', str(i), pa, pr],
                act_sha256=sha_file(pa), rows_sha256=sha_file(pr), ref=f'{cd}/cert.cnf',
                recorded={'cert_json': recs[0], 'campaign_status': recs[1], 'layout_json': recs[2]},
                cnf_bytes_layout=lay['cnf_bytes'], stderr_expected=want_err, **r, verdict=verdict(r, recs, extra))


# ---------- selftest of the comparison logic ----------
def selftest():
    t = f'{D}/logs/selftest'; os.makedirs(t, exist_ok=True)
    ref = f'{t}/ref.cnf'; open(ref, 'wb').write(b'p cnf 3 2\n1 2 0\n-3 0\n')
    big = f'{t}/big.bin'; open(big, 'wb').write(b'\0' * 9_000_000)
    big2 = f'{t}/big2.bin'; bb = bytearray(9_000_000); bb[8_500_000] = 1; open(big2, 'wb').write(bytes(bb))
    sh = lambda s: ['/bin/sh', '-c', s]
    err = f'{t}/err'
    cases = [  # (args, ref, mode, expect_equal, expect_lines)
        (sh(r'printf "p cnf 3 2\n1 2 0\n-3 0\n"'), ref, 'whole', True, 3),
        (sh(r'printf "p cnf 3 2\n1 2 0\n-4 0\n"'), ref, 'whole', False, 3),
        (sh(r'printf "p cnf 3 2\n1 2 0\n"'), ref, 'whole', False, 2),
        (sh(r'printf "p cnf 3 2\n1 2 0\n-3 0\n4 0\n"'), ref, 'whole', False, 4),
        (sh(r'printf "1 2 0\n"'), ref, 'body', True, 1),
        (sh(r'printf "1 2 0\n-3 0\n"'), ref, 'body', True, 2),
        (sh(r'printf "1 3 0\n"'), ref, 'body', False, 1),
        (sh(r'printf "1 2 0\n-3 0\n5 0\n"'), ref, 'body', False, 3),
        (['head', '-c', '9000000', '/dev/zero'], big, 'whole', True, 0),
        (['head', '-c', '9000000', '/dev/zero'], big2, 'whole', False, 0),
    ]
    for k, (a, rf, m, eq, ln) in enumerate(cases):
        r = run_cmp(a, rf, m, err)
        assert r['rc'] == 0 and r['equal'] == eq and r['printed_lines'] == ln, (k, r)
        if eq: assert r['printed_sha'] == r['ref_sha'] and verdict(r, [r['printed_sha']]) == 'MATCH', (k, r)
        else: assert verdict(r, [r['ref_sha']]) == 'MISMATCH', (k, r)
    r = run_cmp(sh(r'printf "1 2 0\n"'), ref, 'whole', err)
    assert r['ref_sha'] == hashlib.sha256(open(ref, 'rb').read()).hexdigest()       # whole: fresh hash of the whole file
    r = run_cmp(sh('true'), ref, 'body', err)                                         # empty output: never a MATCH
    assert r['equal'] and r['printed_bytes'] == 0 and verdict(r, [r['printed_sha']]) == 'MISMATCH'
    r = run_cmp(sh(r'printf "p cnf 3 2\n1 2 0\n-3 0\n"; exit 3'), ref, 'whole', err)  # nonzero exit: never a MATCH
    assert r['rc'] == 3 and r['equal'] and verdict(r, [r['printed_sha']]) == 'MISMATCH'
    r = run_cmp(sh(r'printf "p cnf 3 2\n1 2 0\n-3 0\n"'), ref, 'whole', err)
    assert verdict(r, [r['printed_sha'], None]) == 'MISMATCH' and verdict(r, ['']) == 'MISMATCH'   # missing record
    assert verdict(r, [r['printed_sha']], extra_ok=False) == 'MISMATCH'
    for f in (big, big2): os.remove(f)
    log('selftest PASS (14 cases)')


# ---------- stages ----------
def stage1():
    selftest()
    if not os.path.exists(EXE):
        assert sha_file(ORIG) == FROZEN, 'original exe is not the frozen one'
        shutil.copy2(ORIG, EXE)
    h0 = exe_sha(); log(f'exe {EXE} sha256 {h0} (frozen); original {ORIG} sha256 {sha_file(ORIG)}')
    done = load_done('stage1')
    order, st = campaign()
    cid = order[131]; c = st[cid]; cd = certdir(c)
    lay = json.load(open(f'{cd}/layout.json'))
    if 'leaves' not in done:
        g = gate(); out = []
        rc, rss, wall, err = spawn([EXE, 'leaves'], f'{D}/logs/leaves.err', out.append)
        lv = {}
        for line in b''.join(out).decode().splitlines():
            w = line.split(); lv[int(w[0])] = [[int(x.split(':')[0]), int(x.split(':')[1])] for x in w[1:]]
        certified = sorted(k for k, v in st.items() if v['status'] == 'certified')
        bad = [i for i, q in enumerate(order) if lv.get(i) != st[q]['lits']]
        perm = sorted(order) == certified and len(order) == 132 == len(lv)
        record('stage1', dict(piece='leaves', exe_sha256=h0, gate=g, rc=rc, maxrss_kb=rss, wall_s=wall, stderr=err,
                              leaf_order_sha256=sha_file(f'{ENC}/tools/leaf_order.txt'), certified=len(certified),
                              leaf_order_is_perm_of_certified=perm, leaves_differing=bad,
                              verdict='MATCH' if rc == 0 and perm and not bad else 'MISMATCH'))
    if 'eager' not in done:
        e0, e1 = lay['eager']; E = e1 - e0 + 1
        g = gate(); h = exe_sha()
        r = run_cmp([EXE, 'eager'], f'{cd}/cert.cnf', 'body', f'{D}/logs/eager.err')
        ok = r['printed_lines'] == E and r['ends_nl']
        record('stage1', dict(piece='eager', leaf=131, cube=cid, exe_sha256=h, gate=g, args=['eager'],
                              ref=f'{cd}/cert.cnf', ref_segment=f'lines 2..{E + 1}', eager_clauses_layout=E, **r,
                              verdict=verdict(r, [], ok)))
    pa, pr, nact, scube, ssb, sL = mk_ctl(lay, f'{cd}/layout.json', f'{D}/ctl/{cid}')
    same = dict(act=sha_file(pa) == sha_file(f'{ENC}/ctl/act_{cid}.txt'), rows=sha_file(pr) == sha_file(f'{ENC}/ctl/rows1832.txt'))
    if 'full:131' not in done:
        rec = full_piece(131, cid, c, lay, pa, pr)
        rec['own_ctl_equals_worker_ctl'] = same
        rec['state_file'] = lay['state']; rec['state_sha256'] = sha_file(lay['state'])
        record('stage1', rec)
    if 'negfull:131' not in done:
        neg = f'{D}/ctl/{cid}/act_minus_last.txt'
        with open(pa) as f, open(neg, 'w') as g:
            prev = None
            for line in f:
                if prev is not None: g.write(prev)
                prev = line
        g = gate(); h = exe_sha()
        r = run_cmp([EXE, 'full', '131', neg, pr], f'{cd}/cert.cnf', 'whole', f'{D}/logs/negfull_131.err')
        recd = json.load(open(f'{cd}/cert.json'))['full_cnf_sha256']
        okc = r['rc'] == 0 and not r['equal'] and r['printed_sha'] != recd and verdict(r, [recd]) == 'MISMATCH'
        record('stage1', dict(piece='negfull:131', exe_sha256=h, gate=g, control='last activated quadruple dropped',
                              act_sha256=sha_file(neg), **r, verdict='CONTROL_OK' if okc else 'CONTROL_FAIL'))
        os.remove(neg)
    s = status('stage1', dict(exe_sha256_end=exe_sha(), original_sha256_end=sha_file(ORIG), cgroup_memory_peak_bytes_incl_page_cache=cgroup_peak()))
    log(f'stage1 end: {json.dumps(s)}')


def trims():
    h0 = exe_sha(); log(f'trims start, exe sha256 {h0}')
    done = load_done('trims')
    order, st = campaign()
    md = open(REC).read()
    mdh = {m.group(1): m.group(2) for m in re.finditer(r'^\| (\S+) \|.*?trim\.cnf ([0-9a-f]{64})', md, re.M)}
    for i, cid in enumerate(order):
        if f'trim:{i}' in done: continue
        c = st[cid]; cd = certdir(c)
        cj = json.load(open(f'{cd}/cert.json')); vj = json.load(open(f'{cd}/verify.json'))
        recs = [c.get('trim_cnf_sha256'), cj.get('trim_cnf_sha256'), vj.get('trim_cnf_sha256'), mdh.get(cid)]
        desc = f'{ENC}/desc/{i}.txt'
        g = gate(); h = exe_sha()
        r = run_cmp([EXE, 'trim', str(i), desc], f'{cd}/trim.cnf', 'whole', f'{D}/logs/trim_{i}.err')
        m = re.search(r'clauses (\d+)$', r['stderr'])
        record('trims', dict(piece=f'trim:{i}', leaf=i, cube=cid, exe_sha256=h, gate=g, args=['trim', str(i), desc],
                             desc_sha256=sha_file(desc), ref=f'{cd}/trim.cnf',
                             recorded={'campaign_status': recs[0], 'cert_json': recs[1], 'verify_json': recs[2],
                                       'STATUS_campaign_md': recs[3]},
                             clauses_printed=int(m.group(1)) if m else None, clauses_recorded=c.get('trim_cnf_clauses'),
                             cake_line='s VERIFIED UNSAT' in open(f'{cd}/cake.out').read().splitlines(),
                             all_ok_flags=bool(cj.get('ALL_OK')) and bool(vj.get('ALL_OK')), **r, verdict=verdict(r, recs)))
    done = load_done('trims')
    if 'negtrim:131' not in done:
        ds = open(f'{ENC}/desc/131.txt').read().splitlines()
        k = next(j for j, l in enumerate(ds) if l.startswith('E '))
        ds[k] = 'E %d' % (int(ds[k].split()[1]) + 1)
        neg = f'{D}/ctl/neg_desc131.txt'; open(neg, 'w').write('\n'.join(ds) + '\n')
        cd = certdir(st[order[131]])
        recd = st[order[131]]['trim_cnf_sha256']
        g = gate(); h = exe_sha()
        r = run_cmp([EXE, 'trim', '131', neg], f'{cd}/trim.cnf', 'whole', f'{D}/logs/negtrim_131.err')
        okc = r['rc'] == 0 and not r['equal'] and r['printed_sha'] != recd
        record('trims', dict(piece='negtrim:131', exe_sha256=h, gate=g, control=f'descriptor line {k + 1} E index +1',
                             desc_sha256=sha_file(neg), **r, verdict='CONTROL_OK' if okc else 'CONTROL_FAIL'))
    done = load_done('trims')
    tr = [v for k, v in done.items() if k.startswith('trim:')]
    with open(f'{D}/out/trims.tsv', 'w') as f:
        f.write('leaf\tcube\tprinted_sha256\tverdict\n')
        for v in sorted(tr, key=lambda v: v['leaf']): f.write(f"{v['leaf']}\t{v['cube']}\t{v['printed_sha']}\t{v['verdict']}\n")
    s = status('trims', dict(distinct_printed=len({v['printed_sha'] for v in tr}), exe_sha256_end=exe_sha(),
                             cgroup_memory_peak_bytes_incl_page_cache=cgroup_peak()))
    log(f'trims end: {json.dumps(s)}')


def fullall():
    h0 = exe_sha(); log(f'fullall start, exe sha256 {h0}')
    done = load_done('fullall')
    order, st = campaign()
    ref = json.load(open(f'{certdir(st[order[131]])}/layout.json'))
    for i, cid in enumerate(order):
        if i == 131 or f'full:{i}' in done: continue
        c = st[cid]; lay = json.load(open(f'{certdir(c)}/layout.json'))
        why = [k for k in ('L', 'sb_pairs', 'vars', 'W') if lay.get(k) != ref.get(k)]
        if lay.get('cube') != c['lits']: why.append('cube')
        if why:
            record('fullall', dict(piece=f'full:{i}', leaf=i, cube=cid, prescreen_differs=why, verdict='OUT_OF_SCOPE'))
            continue
        pa, pr, nact, scube, ssb, sL = mk_ctl(lay, f'{certdir(c)}/layout.json', f'{D}/ctl/{cid}')
        why = [k for k, ok in (('activated_count', nact == lay['activated_quadruples']), ('state_cube', scube == lay['cube']),
                               ('state_sb_pairs', ssb == lay['sb_pairs']), ('state_L', sL == lay['L'])) if not ok]
        if why:
            record('fullall', dict(piece=f'full:{i}', leaf=i, cube=cid, prescreen_differs=why, verdict='OUT_OF_SCOPE'))
        else:
            rec = full_piece(i, cid, c, lay, pa, pr)
            rec['state_file'] = lay['state']; rec['state_sha256'] = sha_file(lay['state'])
            record('fullall', rec)
        shutil.rmtree(f'{D}/ctl/{cid}')   # regenerable by mk_ctl; hashes are in the record
        status('fullall')
    s = status('fullall', dict(exe_sha256_end=exe_sha(), cgroup_memory_peak_bytes_incl_page_cache=cgroup_peak()))
    log(f'fullall end: {json.dumps(s)}')


if __name__ == '__main__':
    if STAGE == 'mkctl': mkctl_child(*sys.argv[2:5])
    else: {'selftest': selftest, 'stage1': stage1, 'trims': trims, 'fullall': fullall}[STAGE]()
