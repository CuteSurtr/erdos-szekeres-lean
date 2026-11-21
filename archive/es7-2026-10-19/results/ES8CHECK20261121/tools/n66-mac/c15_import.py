"""c15_import.py (n66-mac, 21 Nov 2026): move Mac-solved N66 level-15 cubes into the Linux campaign.
  check  <W> <ref_layout.json> <id>...   standalone copy of p2c15_driver.accept() (same checks, same order); runs on the Mac or
                                          on Linux; <ref_layout.json> = Linux W/p2/b14h2/it1/layout.json (source of SB_PAIRS)
  import <W> <mac_root> <id>... [--apply] Linux only, driver unit esr-n66-drv15 STOPPED. For each id: status 'queued' in
                                          W/p2/c15/campaign_status.json, unit esr-n66-c15-<id> inactive, nothing under W/p2/c15 for
                                          it; copy <mac_root>/p2/c15/<id>{/,.out,.json,_L15.json,.time} into W/p2/c15; run the driver's OWN
                                          accept() (import p2c15_driver); only if it passes, mark the cube 'running' with an
                                          inactive unit, so that the restarted driver's finalize() reads <id>.out, re-runs
                                          accept() and sets 'certified' (no other driver path imports leaves). Without --apply:
                                          dry run (copies to a scratch folder only, writes nothing in the state).
"""
import glob, hashlib, json, os, shutil, subprocess, sys, time
SEL0, LEVEL = 988541, 15
def sha256(p):
    h = hashlib.sha256()
    with open(p, 'rb') as g:
        for chunk in iter(lambda: g.read(1 << 24), b''): h.update(chunk)
    return h.hexdigest()
def lits_of(cid):
    head, *rest = cid.split('_'); assert len(head) == 6 and set(head) <= set('oh'), cid
    L = [[s, 1 if c == 'o' else 0] for s, c in zip((25, 12, 16, 29, 17, 37), head)]
    return L + [[int(r[:-1]), 1 if r[-1] == 'o' else 0] for r in rest]
def certdir_of(W, cid):
    ev = []
    for l in open(os.path.join(W, 'p2/c15', cid + '.out')):
        try: ev.append(json.loads(l))
        except ValueError: pass
    un = [e for e in ev if e.get('event') == 'UNSAT']
    pc = next((e.get('exit') for e in ev if e.get('event') == 'p2_cert.sh'), None)
    return (un[-1]['certdir'] if un else None), pc, ev
def accept_copy(W, certdir, lits, SB_PAIRS):          # = p2c15_driver.accept() with W, SB_PAIRS passed in
    d = os.path.join(W, certdir)
    try:
        cj = json.load(open(d + '/cert.json')); vj = json.load(open(d + '/verify.json')); lay = json.load(open(d + '/layout.json'))
        cake = [l.rstrip('\n') for l in open(d + '/cake.out')]
        chk = {'cert_ALL_OK': cj.get('ALL_OK') is True, 'verify_ALL_OK': vj.get('ALL_OK') is True, 'cake_line': 's VERIFIED UNSAT' in cake,
               'L': lay['L'] == vj['budget'] == cj['budget'] == LEVEL, 'W': lay['W'] == list(range(70)) and cj['W_size'] == 70,
               'sb_pairs': lay.get('sb_pairs') == vj.get('sb_pairs') == cj.get('sb_pairs') == SB_PAIRS,
               'cube': lay['cube'] == vj['cube'] == cj['cube'] == lits, 'unclassified_0': vj.get('unclassified') == 0,
               'sel': lay['sel'] == [SEL0, SEL0 + 69], 'trim_cnf_sha256': sha256(d + '/trim.cnf') == vj['trim_cnf_sha256'] == cj['trim_cnf_sha256']}
    except (OSError, ValueError, KeyError, TypeError) as e:
        return False, f'certificate files incomplete ({type(e).__name__}: {e})', {}
    bad = [k for k, v in chk.items() if not v]
    return not bad, ('ok' if not bad else 'failed checks: ' + ', '.join(bad)), chk
def check(W, ref, ids):
    SB = json.load(open(ref))['sb_pairs']; assert len(SB) == 27
    out = {}
    for cid in ids:
        cd, pc, _ = certdir_of(W, cid)
        if cd is None: out[cid] = {'ok': False, 'why': 'no UNSAT event in .out'}; continue
        ok, why, chk = accept_copy(W, cd, lits_of(cid), SB)
        cj = json.load(open(os.path.join(W, cd, 'cert.json'))) if ok else {}
        out[cid] = {'ok': ok, 'why': why, 'certdir': cd, 'p2_cert_exit': pc, 'trim_cnf_sha256': cj.get('trim_cnf_sha256'),
                    'full_cnf_sha256': cj.get('full_cnf_sha256'), 'activated_quadruples': cj.get('activated_quadruples')}
    print(json.dumps(out, indent=1)); return all(v['ok'] for v in out.values())
def do_import(W, mac, ids, apply):
    sys.path.insert(0, W); os.chdir(W)
    import p2c15_driver as D                           # the driver's own accept(), SB_PAIRS, SEL0, PREFIX, OUT
    if D.active('esr-n66-drv15'): sys.exit('driver unit esr-n66-drv15 is active: stop it first')
    st = json.load(open(D.STATUS)); stage = os.path.join(W, 'p2', 'mac15_stage_' + time.strftime('%Y%m%d_%H%M%S')); res = {}
    for cid in ids:
        c = st['cubes'].get(cid)
        if c is None or c['status'] != 'queued': res[cid] = f'skip: status {None if c is None else c["status"]}'; continue
        if D.active(D.PREFIX + cid) or any(os.path.exists(os.path.join(W, D.OUT, cid + x)) for x in ('', '.out', '.json', '_L15.json', '.time')): res[cid] = 'skip: Linux files or unit exist'; continue
        dst = os.path.join(W, D.OUT) if apply else stage; os.makedirs(dst, exist_ok=True)
        src = os.path.join(mac, 'p2/c15')
        shutil.copytree(os.path.join(src, cid), os.path.join(dst, cid))
        for ext in ('.out', '.json', '_L15.json', '.time'):     # _L15.json = saved UNSAT state (VERIFY sub15alt path)
            if os.path.exists(os.path.join(src, cid + ext)): shutil.copy2(os.path.join(src, cid + ext), os.path.join(dst, cid + ext))
        if apply:
            cd, pc, ev = certdir_of(W, cid)
            if cd is None: res[cid] = 'no UNSAT event'; cd = os.path.join(D.OUT, cid, 'missing')
        else:                                          # dry run: the same files, read from the stage folder
            evs = [json.loads(l) for l in open(os.path.join(stage, cid + '.out')) if l.startswith('{')]
            un = [e for e in evs if e.get('event') == 'UNSAT']
            if not un: res[cid] = 'dry run: no UNSAT event'; continue
            cd = os.path.relpath(os.path.join(stage, os.path.relpath(un[-1]['certdir'], 'p2/c15')), W)
        cc = dict(c); cc['certdir'] = cd
        ok, why, info = D.accept(cc)
        res[cid] = f'accept: {why}'
        if ok and apply:
            c.update({'status': 'running', 'unit': D.PREFIX + cid, 'out': f'{D.OUT}/{cid}.out', 't0': time.time(), 'started': 'mac import',
                      'imported_from': 'mac (CaDiCaL 3.0.1)'})
        elif apply:
            rej = os.path.join(W, 'p2', 'mac15_rejected'); os.makedirs(rej, exist_ok=True)
            for x in ('', '.out', '.json', '_L15.json', '.time'):
                p = os.path.join(W, D.OUT, cid + x)
                if os.path.exists(p): shutil.move(p, rej)
    if apply:
        shutil.copy2(D.STATUS, D.STATUS + '.bak-' + time.strftime('%Y%m%d_%H%M%S'))
        json.dump(st, open(D.STATUS + '.tmp', 'w'), indent=1); os.replace(D.STATUS + '.tmp', D.STATUS)
    print(json.dumps(res, indent=1))
if __name__ == '__main__':
    if sys.argv[1] == 'check': sys.exit(0 if check(sys.argv[2], sys.argv[3], sys.argv[4:]) else 1)
    if sys.argv[1] == 'import':
        args = [x for x in sys.argv[2:] if x != '--apply']; do_import(args[0], args[1], args[2:], '--apply' in sys.argv)
