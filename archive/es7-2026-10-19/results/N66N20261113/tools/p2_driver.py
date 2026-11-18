"""Phase 2 autonomous driver for track A2 (N66 levels), 13/14 Nov 2026.  Polls every 60 s until 06:00 KST.
  * level 11: when CaDiCaL in unit nov13c-n66-c11 has finished with exit 20, the rest of the certificate pipeline
    (p2_cert.sh p2/c11) runs in unit nov13c-n66-c11v.
  * level L >= 12: two search slots a, b (p2_lazymono.py, budget L; slot b uses the mirror-closed warm start and another
    seed).  A slot whose unit is not running is relaunched (new unit name s<L><x><k>, warm start from its own last state
    file, at most 4 launches per slot) while resources allow; slot b only while no certificate unit runs.  When a slot
    reports UNSAT (state file p2/s<L>/<x>*_L<L>.json) the level's other units are stopped, the certificate unit
    nov13c-n66-c<L> (p2_cert.sh p2/c<L> <state>) starts, and level L+1 opens (warm start from the UNSAT state).  A
    SAT_MODEL (a selection with L holes satisfying every activated clause and violating no quadruple) closes the level:
    the method cannot prove it.
  * memory: if a certificate step waits for room (p2/c*/need_room.json, written by p2_cake.py) or my units use more
    than 8.3 GB, one search unit is stopped (highest level first, slot b first); its slot is relaunched later.
  * whenever a certificate directory gets cert.json with ALL_OK (W = all 70 states, no cube),
    /home/jay/research/data/phase2-20261113/n66_certified.json is rewritten (best certified bound + history) and a line
    is appended to the record README (section 9).
Resources: at most 3 threads (sum of CPUQuota of my nov13c-n66-* units, the driver's 5% excluded) and the machine cap
(cpu_free.sh); a unit starts only if my summed anonymous memory plus its estimate stays <= 8.5 GB; every unit ends by
06:00 KST (RuntimeMaxSec); no launch after 05:15.  State: p2/driver_state.json; log: p2/driver.log."""
import json, os, subprocess, time, glob, datetime, re
W = '/home/jay/research/data/n66-20261113'
PY = '/home/jay/research/data/six10-linux-20261105/venv.disk/bin/python'
CERTJ = '/home/jay/research/data/phase2-20261113/n66_certified.json'
README = '/home/jay/research/lean/erdos-szekeres-lean/cloud/es7-2026-10-19/results/N66N20261113/README.md'
BASE = '/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice'
STATEF = os.path.join(W, 'p2/driver_state.json'); LOGF = os.path.join(W, 'p2/driver.log')
END = datetime.datetime(2026, 11, 14, 6, 0, 0)
STOP_LAUNCH = datetime.datetime(2026, 11, 14, 5, 15, 0)
MAXT = 3
os.chdir(W)
def now(): return datetime.datetime.now()
def log(msg):
    with open(LOGF, 'a') as f: f.write(f'{now():%Y-%m-%d %H:%M:%S} {msg}\n')
def sh(cmd): return subprocess.run(cmd, shell=True, capture_output=True, text=True).stdout.strip()
def active(u): return sh(f'systemctl --user is-active nov13c-n66-{u}') in ('active', 'activating', 'deactivating', 'reloading')
def my_units():
    out = sh("systemctl --user list-units 'nov13c-n66-*' --type=service --state=active --plain --no-legend | awk '{print $1}'")
    return [x for x in out.split() if x and not x.startswith('nov13c-n66-drv')]
def threads_used():
    t = 0.0
    for u in my_units():
        q = sh(f'systemctl --user show {u} -p CPUQuotaPerSecUSec --value')
        if q.endswith('ms'): t += int(q[:-2]) / 1000
        elif q.endswith('s') and q != 'infinity': t += float(q[:-1])
        else: t += 1
    return t
def anon_mb():
    tot = 0
    for p in glob.glob(BASE + '/nov13c-n66-*.service'):
        try:
            for line in open(p + '/memory.stat'):
                if line.startswith('anon '): tot += int(line.split()[1]) // 1048576; break
        except OSError: pass
    return tot
def cpu_free():
    try: return int(sh('/home/jay/research/data/phase2-20261113/cpu_free.sh'))
    except ValueError: return 0
CUR = {}
def cert_active():
    # a certificate unit, or a batch search unit that found UNSAT and now runs p2_cert.sh on its own directory
    if any(u.startswith('nov13c-n66-c') for u in my_units()): return True
    S = CUR.get('S') or {}
    for lv in S.get('levels', {}).values():
        if lv.get('status') == 'UNSAT' and lv.get('certdir') and lv.get('winner_unit') and active(lv['winner_unit']) \
           and not os.path.exists(os.path.join(lv['certdir'], 'cert.json')): return True
    return False
def cfg():
    try: return json.load(open(os.path.join(W, 'p2/driver_config.json')))
    except Exception: return {}
def launch(u, cmd, mem_gb, est_mb, quota=100, quiet=False):
    if now() > STOP_LAUNCH: return False
    if threads_used() + quota / 100 > MAXT + 1e-9 or cpu_free() < quota / 100:
        if not quiet: log(f'not launching {u}: threads (mine {threads_used()}, machine free {cpu_free()})')
        return False
    if anon_mb() + est_mb > 8500:
        if not quiet: log(f'not launching {u}: memory (mine {anon_mb()} MB + estimate {est_mb} MB > 8500)')
        return False
    secs = int((END - now()).total_seconds()) - 120
    if secs < 900: return False
    full = (f"systemd-run --user --unit=nov13c-n66-{u} -p CPUQuota={quota}% -p MemoryMax={mem_gb}G -p MemorySwapMax=0 -p RuntimeMaxSec={secs} "
            f"--nice=10 --working-directory={W} --setenv=ETV_A=4 --setenv=ETV_B=4 --setenv=P2_UNIT=nov13c-n66-{u} /bin/bash -c {json.dumps(cmd)}")
    r = subprocess.run(full, shell=True, capture_output=True, text=True)
    log(f'launch {u} (quota {quota}%, MemoryMax {mem_gb}G, {secs} s): rc {r.returncode} {r.stderr.strip()[-200:]} :: {cmd}')
    return r.returncode == 0
def stop(u):
    subprocess.run(f'systemctl --user stop nov13c-n66-{u}', shell=True); log(f'stopped {u}')
def load():
    try: return json.load(open(STATEF))
    except Exception: return None
def save(S):
    json.dump(S, open(STATEF + '.tmp', 'w'), indent=1); os.replace(STATEF + '.tmp', STATEF)
def readme_status(line):
    # insert a line at the top of the STATUS block (between the markers) of the record README
    try:
        txt = open(README).read(); m = '<!-- STATUS -->\n'
        if m in txt:
            txt = txt.replace(m, m + line.rstrip() + '\n', 1); tmp = README + '.drvtmp'
            open(tmp, 'w').write(txt); os.replace(tmp, README)
    except OSError as e: log(f'README status update failed: {e}')
def readme_append(line):
    try:
        with open(README, 'a') as f: f.write(line.rstrip() + '\n')
    except OSError as e: log(f'README append failed: {e}')
PHASE1 = {'bound': 59, 'holes_at_least': 11, 'label': 'CERTIFIED', 'time': '2026-11-13 18:11 KST',
          'cnf_sha256': '920489253e49d2b8527ff32771b08afa05cc2956f149d3c20711657b5b4f4ab0',
          'lrat_sha256': '9272dfbc3364eff199dd1713e054d1879931e6dab2f0b301a0bb4e79b472a244',
          'what': 'phase 1: PB CNF "<= 10 holes" over 3,052 justified rows (README data/cert59)'}
def write_certified(S):
    hist = [PHASE1] + [S['certified'][k] for k in sorted(S['certified'], key=int)]
    best = min(hist, key=lambda h: h['bound'])
    out = {'bound': best['bound'], 'holes_at_least': best['holes_at_least'], 'record': 'R/N66N20261113',
           'cnf_sha256': best['cnf_sha256'], 'lrat_sha256': best['lrat_sha256'], 'time': best['time'], 'label': 'CERTIFIED',
           'what': best['what'], 'certdir': best.get('certdir'), 'history': hist,
           'updated': f'{now():%Y-%m-%d %H:%M:%S} KST (p2_driver.py)'}
    tmp = CERTJ + '.tmp'; json.dump(out, open(tmp, 'w'), indent=1); os.replace(tmp, CERTJ)
def check_cert(S, L, d):
    p = os.path.join(d, 'cert.json')
    if str(L) in S['certified'] or not os.path.exists(p): return
    c = json.load(open(p))
    if not c.get('ALL_OK') or c.get('W_size', 70) != 70 or c['cube']:
        if not S.get(f'warned_{L}'): S[f'warned_{L}'] = True; log(f'cert {d} not usable: ALL_OK {c.get("ALL_OK")}')
        return
    S['certified'][str(L)] = {'bound': c['bound'], 'holes_at_least': c['holes_at_least'], 'label': 'CERTIFIED', 'time': c['time'],
        'cnf_sha256': c['trim_cnf_sha256'], 'lrat_sha256': c['trim_lrat_sha256'], 'certdir': c['certdir'],
        'what': f"phase 2: trimmed monolithic sub-CNF \"<= {L} holes\" ({c['trim_cnf_clauses']} clauses: {c['kinds']}), used rows justified "
                f"({(c.get('final_verify66') or {}).get('kinds')}), cake_lpr s VERIFIED UNSAT, p2_verify ALL_OK; untrimmed CNF {c['full_cnf_sha256']}",
        'trim_lrat_bytes': c['trim_lrat_bytes'], 'used_rows': c['used']['used_rows']}
    write_certified(S)
    log(f'CERTIFIED level {L}: N66 <= {c["bound"]} ({d})')
    if L >= 13: readme_status(f"- **Update {now():%H:%M} KST (driver): N66 ≤ {c['bound']} CERTIFIED** (level {L}, `W/{d}`; §9 and n66_certified.json). The items below were written at 21:55.")
    readme_append(f"- {now():%H:%M} (driver) **CERTIFIED: N66 ≤ {c['bound']}** (at least {L + 1} holes): `W/{d}`, trimmed CNF SHA-256 "
                  f"`{c['trim_cnf_sha256']}`, trimmed LRAT SHA-256 `{c['trim_lrat_sha256']}`, {c['trim_cnf_clauses']} clauses {c['kinds']}, "
                  f"{c['used']['used_rows']} used rows justified, p2_verify ALL_OK; n66_certified.json updated.")
def slot_prefix(L, x, k): return f'p2/s{L}/{x}' + (str(k) if k else '')
def slot_unit(L, x, k): return f's{L}{x}' + (str(k) if k else '')
def launch_slot(S, L, x, quiet=False):
    lv = S['levels'][str(L)]; sl = lv['slots'][x]
    k = sl['k'] + 1 if sl.get('launched') else sl['k']
    if k > 3: return False
    pre = slot_prefix(L, x, k); u = slot_unit(L, x, k)
    os.makedirs(os.path.join(W, f'p2/s{L}'), exist_ok=True)
    warm = sl['warm']
    if sl.get('launched'):            # resume from the slot's own last state (it contains every activated quadruple)
        last = slot_prefix(L, x, sl['k']) + '.json'
        if os.path.exists(last): warm = last
    secs = int((END - now()).total_seconds()) - 400
    if sl.get('type', 'lazy') == 'batch':
        bdir = f'p2/b{L}{x}' + (str(k) if k else '')   # one directory per slot and launch
        cmd = (f"{PY} -u p2_batch.py --out {pre}.json --dir {bdir} --L {L} --rows mono/rows_1832.json --warm {warm} --seed {sl['seed']} "
               f"{'--tauclose ' if sl['tauclose'] else ''}{'--sb ' if sl.get('sb') else ''}"
               f"{('--cadopts=' + json.dumps(sl['cadopts']) + ' ') if sl.get('cadopts') else ''}--secs {secs - 3600} > {pre}.out 2>&1")
    else:
        cmd = (f"{PY} -u p2_lazymono.py --out {pre}.json --L {L} --rows mono/rows_1832.json --warm {warm} --seed {sl['seed']} "
               f"{'--tauclose ' if sl['tauclose'] else ''}--secs {secs} > {pre}.out 2>&1")
    if time.time() - CUR.get('last_search_launch', 0) < 180: return False      # one search launch per 3 minutes (memory grows after start)
    if launch(u, cmd, 4.5 if sl.get('type') == 'batch' else 3.5, 3300 if sl.get('type') == 'batch' else 2600, quiet=quiet):
        sl['k'] = k; sl['launched'] = True; sl['unit'] = u; CUR['last_search_launch'] = time.time(); return True
    return False
def search_units_by_priority(S):
    out = []
    for Ls in sorted(S['levels'], key=int, reverse=True):
        lv = S['levels'][Ls]
        for x in ('b', 'd', 'a', 'g', 'c', 'e'):
            sl = lv['slots'].get(x)
            if sl and sl.get('unit') and active(sl['unit']) and not (lv['status'] == 'UNSAT' and lv.get('winner_unit') == sl['unit']): out.append(sl['unit'])
    return out
def step(S):
    CUR['S'] = S
    # memory: a certificate step waiting for room, or my units close to the budget -> give up one search unit
    need = [p for p in glob.glob('p2/c*/need_room.json') + glob.glob('p2/c*/tcert/need_room.json') + glob.glob('p2/b*/it*/need_room.json')
            + glob.glob('p2/b*/it*/tcert/need_room.json') if time.time() - os.path.getmtime(p) < 120]
    if need: S['need_room_time'] = time.time()
    if need or anon_mb() > 8300:
        cand = search_units_by_priority(S)
        if cand:
            u = cand[0]; stop(u)
            for lv in S['levels'].values():
                for sl in lv['slots'].values():
                    if sl.get('unit') == u: sl['parked'] = 'memory' if not need else ''; sl['resume_after_cert'] = bool(need)
            log(f'memory: stopped search unit {u} (need_room {need}, mine {anon_mb()} MB)')
            readme_append(f"- {now():%H:%M} (driver) memory: search unit {u} stopped " + ("to make room for a certificate step; its slot resumes from its saved state when no certificate unit runs." if need else "because the track was above 8.3 GB; its slot stays parked (not restarted unchanged)."))
            return
    # level 11
    if not active('c11') and not S.get('c11v_launched'):
        cl = open('p2/c11/cadical.log').read() if os.path.exists('p2/c11/cadical.log') else ''
        if re.search(r'^exit 20', cl, re.M):
            if launch('c11v', './p2_cert.sh p2/c11 > p2/c11/cert_run.out 2>&1', 7, 600): S['c11v_launched'] = True
        elif re.search(r'^exit ', cl, re.M) and not S.get('c11_failed'):
            S['c11_failed'] = True; log('c11: CaDiCaL ended without UNSAT: ' + cl.strip().splitlines()[-1])
    check_cert(S, 11, 'p2/c11')
    # levels >= 12
    for Ls in sorted(S['levels'], key=int):
        L = int(Ls); lv = S['levels'][Ls]
        if lv['status'] == 'running':
            hits = sorted(glob.glob(f'p2/s{L}/*_L{L}.json'))
            if hits:
                lv['status'] = 'UNSAT'; lv['state'] = hits[0]; log(f'level {L}: UNSAT ({hits[0]})')
                try: cd = json.load(open(hits[0])).get('certdir')
                except Exception: cd = None
                wx = os.path.basename(hits[0])[0]; wsl = lv['slots'].get(wx, {})
                if cd:                          # a p2_batch.py run: its own unit runs p2_cert.sh on that directory
                    lv['certdir'] = cd; lv['cert_launched'] = True; lv['winner_unit'] = wsl.get('unit')
                for x, sl in lv['slots'].items():
                    if sl.get('unit') and active(sl['unit']) and sl.get('unit') != lv.get('winner_unit'): stop(sl['unit'])
                readme_append(f"- {now():%H:%M} (driver) level {L}: search run `W/{hits[0]}` reports \"at most {L} holes\" UNSAT (COMPUTED); certificate: "
                              + (f"p2_cert.sh in the same unit on `W/{cd}`." if cd else f"unit c{L} (p2_cert.sh p2/c{L})."))
            else:
                for o in glob.glob(f'p2/s{L}/*.out'):
                    if '"SAT_MODEL"' in open(o).read():
                        lv['status'] = 'SAT_MODEL'; lv['sat_out'] = o; log(f'level {L}: SAT_MODEL in {o}')
                        for x, sl in lv['slots'].items():
                            if sl.get('unit') and active(sl['unit']): stop(sl['unit'])
                        readme_append(f"- {now():%H:%M} (driver) level {L}: `W/{o}` found a selection with {L} holes that satisfies every activated clause and violates no quadruple (COMPUTED): this method does not prove level {L}.")
                        break
        if lv['status'] == 'running':
            for x in cfg().get('slot_order', ['a', 'c', 'b']):
                sl = lv['slots'].get(x)
                if sl is None or sl.get('parked') or (sl.get('unit') and active(sl['unit'])): continue
                if sl.get('unit') and os.path.exists(f"MEMGUARD_STOPPED_nov13c-n66-{sl['unit']}.txt"):
                    sl['parked'] = 'memguard'; log(f"slot {x} of level {L} parked: unit {sl['unit']} was stopped by the memory guard"); continue
                if sl.get('resume_after_cert') and cert_active(): continue
                if x != "a" and cert_active() and anon_mb() + 3300 + 800 > 8500: continue   # keep room for a certificate step
                if x != "a" and cert_active() and time.time() - S.get('need_room_time', 0) < 3600: continue   # no thrashing
                if now() > STOP_LAUNCH: continue
                launch_slot(S, L, x, quiet=True)
        if lv['status'] == 'UNSAT':
            if not lv.get('cert_launched'):
                if launch(f'c{L}', f"./p2_cert.sh p2/c{L} {lv['state']} > p2/c{L}.run.out 2>&1", 7, 3000): lv['cert_launched'] = True; lv['cert_unit'] = f'c{L}'
            check_cert(S, L, lv.get('certdir', f'p2/c{L}'))
            # one retry of the certificate pipeline if its unit ended without cert.json (steps already done are skipped)
            cdir = lv.get('certdir', f'p2/c{L}'); cu = lv.get('cert_unit') or lv.get('winner_unit')
            if lv.get('cert_launched') and cu and not active(cu) and not os.path.exists(os.path.join(cdir, 'cert.json')) \
               and not lv.get('cert_retry') and os.path.exists(os.path.join(cdir, 'cadical.log')):
                if launch(f'c{L}r', f"./p2_cert.sh {cdir} > {cdir}/cert_retry.out 2>&1", 7, 3000):
                    lv['cert_retry'] = True; lv['cert_unit'] = f'c{L}r'; log(f'level {L}: certificate pipeline retried on {cdir}')
            nxt = str(L + 1)
            if nxt not in S['levels'] and now() < STOP_LAUNCH:
                allslots = {'a': {'warm': lv['state'], 'seed': 1, 'tauclose': False, 'k': 0, 'type': 'lazy'},
                            'b': {'warm': lv['state'], 'seed': 2, 'tauclose': True, 'k': 0, 'type': 'lazy'},
                            'c': {'warm': lv['state'], 'seed': 3, 'tauclose': False, 'k': 0, 'type': 'batch'},
                            'e': {'warm': lv['state'], 'seed': 5, 'tauclose': True, 'k': 0, 'type': 'batch', 'sb': True},
                            'g': {'warm': lv['state'], 'seed': 7, 'tauclose': True, 'k': 0, 'type': 'batch', 'sb': True, 'cadopts': '--unsat'}}
                S['levels'][nxt] = {'status': 'running', 'slots': {x: allslots[x] for x in cfg().get('next_level_slots', ['a', 'c', 'b'])}}
                log(f'level {nxt} opened (warm start {lv["state"]}, slots {list(S["levels"][nxt]["slots"])})')
def main():
    S = load()
    if S is None:
        S = {'certified': {}, 'levels': {'12': {'status': 'running', 'slots': {
            'a': {'warm': 'lm/full_L11.json', 'seed': 1, 'tauclose': False, 'k': 0, 'launched': True, 'unit': 's12a'},
            'b': {'warm': 'lm/full_L11.json', 'seed': 2, 'tauclose': True, 'k': 0, 'launched': True, 'unit': 's12b'}}}}}
    log('driver start'); save(S)
    while now() < END:
        try:
            step(S)
        except Exception:
            import traceback; log('driver exception: ' + traceback.format_exc()[-800:])
        save(S)
        time.sleep(60)
    log('driver end (06:00)')
if __name__ == '__main__':
    main()
