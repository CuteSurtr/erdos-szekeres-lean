#!/usr/bin/env python3
"""Re-certify, and this time KEEP the proofs of, every coupled row used by the slice trees (track G2, 13 Nov 2026).

House rule: keep the LRAT (zstd) until an independent check has re-run it.  The certification tools of RES33N /
LO33N / phase 1 deleted CNF and LRAT after cake_lpr's verdict.  For every demand-one row of the given extra-row files
this script
  1. regenerates the coupled CNF from the support with the unchanged encoder (killtools/coupled.py) and compares its
     SHA-256 with the recorded cnf_sha256 (pool_v1 / killtools certified.jsonl);
  2. solves it with CaDiCaL 2.1.3 (--lrat=true --binary=false, as certify.py) and compares the LRAT SHA-256 with the
     recorded lrat_sha256 (CaDiCaL is deterministic, so equality is expected);
  3. checks the proof with cake_lpr --CML_HEAP_SIZE=400 and requires the line 's VERIFIED UNSAT';
  4. keeps CNF and LRAT compressed with zstd in OUTDIR/<cnf sha256[:16]>.{cnf,lrat}.zst.
Rows whose proof files already exist in OUTDIR or in killtools/proofs/ are skipped (they were kept when certified).
Usage: recert_keep.py OUTDIR WORKERS EXTRA.json [EXTRA.json ...]      -> OUTDIR/recert.jsonl, OUTDIR/summary.json
"""
import hashlib, json, os, subprocess, sys, time, multiprocessing as mp

KILL = '/home/jay/research/data/fastbb-20261113/killtools'
POOL = '/home/jay/research/data/fastbb-20261113/p2/pool/pool_v1.json'
CAKE = os.path.expanduser('~/.local/bin/cake_lpr')
sys.path.insert(0, KILL)
G = {}


def init(outdir):
    import coupled
    G['coupled'] = coupled
    G['out'] = outdir


def zkeep(path):
    dst = os.path.join(G['out'], os.path.basename(path) + '.zst')
    r = subprocess.run(['zstd', '-q', '-f', path, '-o', dst], capture_output=True, text=True)
    if r.returncode == 0 and os.path.exists(dst) and os.path.getsize(dst) > 0:
        os.remove(path)
        return dst
    return path


def work(job):
    S, rec_cnf, rec_lrat = job
    t0 = time.time()
    txt = G['coupled'].CNF(list(S)).dimacs()
    h = hashlib.sha256(txt.encode()).hexdigest()
    tmpd = os.path.join(G['out'], 'tmp'); os.makedirs(tmpd, exist_ok=True)
    p = os.path.join(tmpd, h[:16] + '.cnf'); q = p[:-4] + '.lrat'
    open(p, 'w').write(txt)
    out = {'support': list(S), 'cnf_sha256': h, 'cnf_matches_record': h in rec_cnf}
    r = subprocess.run(['cadical', '-q', '--lrat=true', '--binary=false', p, q], capture_output=True, text=True)
    out['cadical_exit'] = r.returncode
    if r.returncode == 20:
        lh = hashlib.sha256(open(q, 'rb').read()).hexdigest()
        out['lrat_sha256'] = lh
        out['lrat_matches_record'] = lh in rec_lrat
        out['lrat_bytes'] = os.path.getsize(q)
        c = subprocess.run([CAKE, '--CML_HEAP_SIZE=400', p, q], capture_output=True, text=True)
        out['verdict'] = 's VERIFIED UNSAT' if 's VERIFIED UNSAT' in c.stdout else ('cake_lpr: ' + (c.stdout + c.stderr)[-200:])
    else:
        out['verdict'] = f'cadical exit {r.returncode}'
    files = [zkeep(p)]
    if os.path.exists(q):
        files.append(zkeep(q))
    out['files'] = files
    out['seconds'] = round(time.time() - t0, 2)
    return out


def main():
    outdir, workers, extras = os.path.abspath(sys.argv[1]), int(sys.argv[2]), sys.argv[3:]
    os.makedirs(outdir, exist_ok=True)
    rec = {}
    for r in json.load(open(POOL)):
        rec.setdefault(tuple(sorted(r['support'])), (set(), set()))
        rec[tuple(sorted(r['support']))][0].add(r['cnf_sha256']); rec[tuple(sorted(r['support']))][1].add(r['lrat_sha256'])
    for line in open(os.path.join(KILL, 'certified.jsonl')):
        r = json.loads(line)
        if r.get('verdict') != 's VERIFIED UNSAT':
            continue
        k = tuple(sorted(r['support']))
        rec.setdefault(k, (set(), set()))
        rec[k][0].add(r['cnf_sha256']); rec[k][1].add(r.get('lrat_sha256', ''))
    sups, seen = [], set()
    for e in extras:
        for r in json.load(open(e))[2:]:
            k = tuple(sorted(r['support']))
            if r['rhs'] == 1 and k not in seen:
                seen.add(k); sups.append(k)
    done = set()
    jl = os.path.join(outdir, 'recert.jsonl')
    if os.path.exists(jl):
        for line in open(jl):
            d = json.loads(line)
            if d.get('verdict') == 's VERIFIED UNSAT':
                done.add(tuple(d['support']))
    kept_before = {f[:16] for f in os.listdir(os.path.join(KILL, 'proofs'))} if os.path.isdir(os.path.join(KILL, 'proofs')) else set()
    jobs = []
    for k in sups:
        if k in done:
            continue
        rc, rl = rec.get(k, (set(), set()))
        if any(c[:16] in kept_before for c in rc):
            continue
        jobs.append((k, rc, rl))
    t0 = time.time()
    n = ok = cm = lm = 0
    with open(jl, 'a') as f, mp.Pool(workers, initializer=init, initargs=(outdir,)) as pool:
        for d in pool.imap_unordered(work, jobs, chunksize=1):
            f.write(json.dumps(d) + '\n'); f.flush()
            n += 1; ok += d['verdict'] == 's VERIFIED UNSAT'; cm += d['cnf_matches_record']; lm += d.get('lrat_matches_record', False)
    allrec = [json.loads(l) for l in open(jl)]
    summ = {'extras': extras, 'rows_in_extras': len(sups), 'skipped_proof_already_kept': len(sups) - len(jobs) - len(done),
            'done_this_run': n, 'records_total': len(allrec),
            'verified_total': sum(d['verdict'] == 's VERIFIED UNSAT' for d in allrec),
            'cnf_hash_matches_record_total': sum(bool(d['cnf_matches_record']) for d in allrec),
            'lrat_hash_matches_record_total': sum(bool(d.get('lrat_matches_record')) for d in allrec),
            'not_verified': [d['support'] for d in allrec if d['verdict'] != 's VERIFIED UNSAT'],
            'seconds': round(time.time() - t0, 1), 'finished': time.strftime('%F %T')}
    json.dump(summ, open(os.path.join(outdir, 'summary.json'), 'w'), indent=1)
    print(json.dumps(summ))
    sys.exit(0 if not summ['not_verified'] else 1)


if __name__ == '__main__':
    main()
