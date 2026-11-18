#!/usr/bin/env python3
"""Autonomous driver for one slice tree (track G2, phase 2, 13 Nov 2026).

  slicedrv.py T THREADS NCTX DEADLINE_EPOCH STATEDIR [fastbb2 options ...]

Slice t = the pair (84 - t, 37 + t): rows h(F) >= t, h(Lo) >= 33 - t on top of h0 = 0, the 2,650 Lean rows and the
cake_lpr-certified coupled rows (pool_v1.json, then rows appended by witness kills).  Loop:
  1. rows file from STATEDIR/extra.json (capacity rows first, certified rows in a stable order, appended rows last);
  2. fastbb2 solve --slice=1 --on-witness=continue (resumable: master.txt and closed ctx-N.json.gz are kept; rows may
     only be appended, which fastbb2 checks with a prefix hash);
  3. exit 3 (WITNESS), or WIT_BATCH witness contexts waiting: tools/witness_kill2.py (phase-1 witness_kill.py + persisted
     transported rows of new cores) certifies pooled transported rows violated by each witness (CaDiCaL LRAT
     + cake_lpr "s VERIFIED UNSAT"), or probes the occupied set for new coupled cores, and APPENDS the certified rows
     to extra.json; then go to 1.  If a witness cannot be killed: STUCK.json (the obstruction), stop;
  4. exit 0: exact piecewise replay (verify_slice.py: scripts/omission_tree.check_tree in unbounded integers, plus the
     semantic row checks) with THREADS processes, then DONE.json; stop;
  5. exit 5 (deadline) or anything else: status.json says so; stop (run the same command again to resume).
status.json is rewritten after every step.  Nothing outside STATEDIR is written except the private kill tools'
certified.jsonl/cert files (killtools/) and the transported-row pool there.
"""
import glob, hashlib, json, os, shutil, subprocess, sys, time

P2 = '/home/jay/research/data/fastbb-20261113/p2'
KILL = '/home/jay/research/data/fastbb-20261113/killtools'
REPO = '/home/jay/research/lean/erdos-szekeres-lean'
PY = '/home/jay/research/data/six10-linux-20261105/venv.disk/bin/python'
TOOLS = REPO + '/cloud/es7-2026-10-19/results/FASTBB20261113/tools'
SRC = REPO + '/experiments/omission-residual32-rank-global-2026-10-10/source-2650.json.gz'
FASTBB = P2 + '/bin/fastbb2'
POOL = P2 + '/pool/pool_v1.json'


def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()


def main():
    T, THR, NCTX, DL, SD = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), float(sys.argv[4]), os.path.abspath(sys.argv[5])
    fopts = sys.argv[6:] or ['--ktop=16', '--dtop=8', '--klow=4', '--sbiter=1000']
    os.makedirs(SD, exist_ok=True)
    BB = os.path.join(SD, 'bb')
    EXTRA = os.path.join(SD, 'extra.json')
    ROWS = os.path.join(SD, 'rows.txt')
    LOG = open(os.path.join(SD, 'driver.log'), 'a')
    st = {'slice_t': T, 'pair': [84 - T, 37 + T], 'threads': THR, 'contexts': NCTX, 'deadline': time.strftime('%F %T', time.localtime(DL)),
          'fastbb_options': fopts, 'iterations': 0, 'witnesses_killed': 0, 'rows_appended': 0, 'state': 'starting'}
    if os.path.exists(os.path.join(SD, 'status.json')):
        try:
            old = json.load(open(os.path.join(SD, 'status.json')))
            for k in ('iterations', 'witnesses_killed', 'rows_appended'):
                st[k] = old.get(k, 0)
        except Exception:
            pass

    def log(**kw):
        kw['t'] = time.strftime('%F %T')
        LOG.write(json.dumps(kw) + '\n'); LOG.flush()

    def status(**kw):
        st.update(kw); st['updated'] = time.strftime('%F %T')
        tmp = os.path.join(SD, 'status.json.tmp'); json.dump(st, open(tmp, 'w'), indent=1); os.replace(tmp, os.path.join(SD, 'status.json'))

    if not os.path.exists(EXTRA):
        r = subprocess.run([PY, P2 + '/tools/make_slice_extra.py', str(T), POOL, EXTRA], capture_output=True, text=True)
        log(event='extra_created', out=r.stdout.strip(), err=r.stderr[-500:])
        if r.returncode:
            status(state='ERROR', error='make_slice_extra failed'); return 2
    for k in ('DONE.json', 'STUCK.json'):
        if os.path.exists(os.path.join(SD, k)):
            log(event='already_finished', file=k); return 0
    while True:
        left = DL - time.time()
        if left < 300:
            status(state='DEADLINE', note='resume with the same command'); log(event='deadline'); return 5
        r = subprocess.run([PY, TOOLS + '/fastbb_prep.py', SRC, EXTRA, ROWS], capture_output=True, text=True)
        if r.returncode:
            status(state='ERROR', error='fastbb_prep failed: ' + r.stderr[-300:]); return 2
        nrows = len(json.load(open(EXTRA)))
        st['iterations'] += 1
        status(state='searching', extra_rows=nrows, extra_sha256=sha(EXTRA))
        log(event='solve', iteration=st['iterations'], extra_rows=nrows, time_limit=int(left - 240))
        split = []
        if os.path.exists(os.path.join(SD, 'SPLIT_NEXT')):
            split = ['--split-open=2']
            os.remove(os.path.join(SD, 'SPLIT_NEXT'))
            log(event='split_open', levels=2)
        out_before = os.path.getsize(os.path.join(SD, 'fastbb.out')) if os.path.exists(os.path.join(SD, 'fastbb.out')) else 0
        # Batch kills: when WIT_BATCH (default 4) witness contexts have accumulated, or the oldest one is older than
        # WIT_AGE seconds (default 900), fastbb2 is stopped (the contexts in progress are lost, closed ones are kept),
        # the witnesses are killed and the search resumes with the new rows, so that the remaining contexts profit.
        wbatch = int(os.environ.get('WIT_BATCH', '4')); wage = float(os.environ.get('WIT_AGE', '900'))
        early = False
        with open(os.path.join(SD, 'fastbb.out'), 'a') as fo:
            fo.write(f'# {time.strftime("%F %T")} iteration {st["iterations"]}, extra rows {nrows}\n'); fo.flush()
            proc = subprocess.Popen([FASTBB, 'solve', ROWS, '33', str(THR), str(NCTX), BB, '--slice=1', '--on-witness=continue',
                                     f'--time-limit={int(left - 240)}'] + fopts + split, stdout=fo, stderr=subprocess.STDOUT)
            while True:
                try:
                    rc = proc.wait(timeout=20)
                    break
                except subprocess.TimeoutExpired:
                    wf = glob.glob(os.path.join(BB, 'witness-ctx-*.json'))
                    oldest = min((os.path.getmtime(p) for p in wf), default=None)
                    if len(wf) >= wbatch or (oldest is not None and time.time() - oldest > wage):
                        proc.terminate()
                        try:
                            proc.wait(timeout=30)
                        except subprocess.TimeoutExpired:
                            proc.kill(); proc.wait()
                        early = True
                        rc = 3
                        fo.write(f'# {time.strftime("%F %T")} driver stopped fastbb2 for a batch kill ({len(wf)} witness contexts)\n'); fo.flush()
                        break
        if early:
            log(event='batch_kill_stop', witness_files=len(glob.glob(os.path.join(BB, 'witness-ctx-*.json'))))
        with open(os.path.join(SD, 'fastbb.out')) as fo:
            fo.seek(out_before)
            if '"context_too_big"' in fo.read():
                open(os.path.join(SD, 'SPLIT_NEXT'), 'w').write('a context exceeded --max-ctx-nodes\n')
        ndone = len(glob.glob(os.path.join(BB, 'ctx-*.json.gz')))
        log(event='fastbb_exit', rc=rc, contexts_closed=ndone)
        status(contexts_closed=ndone, last_fastbb_exit=rc)
        if rc == 3:
            status(state='killing_witnesses')
            wit = sorted(glob.glob(os.path.join(BB, 'WITNESS.json')) + glob.glob(os.path.join(BB, 'witness-ctx-*.json')))
            before = nrows
            with open(os.path.join(SD, 'kill.out'), 'a') as fk:
                fk.write(f'# {time.strftime("%F %T")} {len(wit)} witness files\n'); fk.flush()
                kr = subprocess.run([PY, P2 + '/tools/witness_kill2.py', KILL, EXTRA, BB], stdout=fk, stderr=subprocess.STDOUT, cwd=REPO).returncode
            after = len(json.load(open(EXTRA)))
            hs = []
            for w in wit:
                try:
                    hs.append(json.load(open(w))['holes'])
                except Exception:
                    pass
            with open(os.path.join(SD, 'witnesses.jsonl'), 'a') as fw:
                for H in hs:
                    fw.write(json.dumps({'t': time.strftime('%F %T'), 'holes': H, 'kill_exit': kr, 'rows_before': before, 'rows_after': after}) + '\n')
            log(event='kill', exit=kr, witnesses=len(wit), rows_before=before, rows_after=after)
            if kr != 0:
                json.dump({'slice_t': T, 'state': 'STUCK', 'witness_files': wit, 'holes': hs, 'extra_rows': after,
                           'note': 'a 33-hole vector of this slice satisfies every row and no certified coupled row was found that it violates',
                           't': time.strftime('%F %T')}, open(os.path.join(SD, 'STUCK.json'), 'w'), indent=1)
                status(state='STUCK'); return 1
            K = os.path.join(BB, 'witnesses_killed', time.strftime('%Y%m%d-%H%M%S'))
            os.makedirs(K, exist_ok=True)
            for w in wit:
                shutil.move(w, os.path.join(K, os.path.basename(w)))
            st['witnesses_killed'] += len(hs); st['rows_appended'] += after - before
            status(state='restarting')
            continue
        if rc == 0:
            status(state='replaying')
            certs = [POOL, KILL + '/certified.jsonl']
            vr = subprocess.run([PY, P2 + '/tools/verify_slice.py', BB, str(T), str(THR)] + certs, capture_output=True, text=True, cwd=REPO)
            log(event='replay', exit=vr.returncode, out=vr.stdout[-3000:], err=vr.stderr[-1500:])
            if vr.returncode == 0:
                res = json.loads(vr.stdout.strip().splitlines()[-1])
                stats = None
                for line in open(os.path.join(SD, 'fastbb.out')):
                    if line.startswith('{"event": "DONE"'):
                        stats = json.loads(line)
                done = {'slice_t': T, 'pair': [84 - T, 37 + T], 'verdict': 'CLOSED (EXACT TREE)', 'replay': res,
                        'search_last_run': stats, 'witnesses_killed': st['witnesses_killed'], 'rows_appended': st['rows_appended'],
                        'inputs_sha256': {'source_gz': sha(SRC), 'extra': sha(EXTRA), 'rows_txt': sha(ROWS), 'pool_v1': sha(POOL),
                                          'killtools_certified': sha(KILL + '/certified.jsonl'), 'fastbb2_binary': sha(FASTBB),
                                          'fastbb2_source': sha(P2 + '/src/fastbb2.cpp')},
                        'finished': time.strftime('%F %T')}
                json.dump(done, open(os.path.join(SD, 'DONE.json'), 'w'), indent=1)
                status(state='DONE'); return 0
            status(state='REPLAY_FAILED', replay_err=vr.stderr[-800:]); return 2
        if rc == 4 and os.path.exists(os.path.join(SD, 'SPLIT_NEXT')):
            status(state='restarting', note='contexts too big: splitting the open ones 2 levels deeper')
            continue
        status(state='STOPPED', note=f'fastbb2 exit {rc} (5 = time limit, 4 = context too big, 2 = error); resume with the same command')
        return rc


if __name__ == '__main__':
    sys.exit(main())
