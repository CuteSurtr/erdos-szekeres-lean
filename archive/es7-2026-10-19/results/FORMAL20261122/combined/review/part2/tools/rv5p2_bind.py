#!/usr/bin/env python3
"""rv5 part 2 (reviewer's own code): sample re-print of the three CNF-verdict hypotheses with the frozen exes, plus
fresh cake_lpr runs on a few printed texts. Runs inside unit esr-ag-rv5-p2bind. Writes only under part2/.

* exes: n66r15print (65865b1e...), r15rowprint (6b9af2c6...) - both in n66-l15-rows logs/freeze_manifest.sha256 -
  and rowprint (eabe3791..., res118-rowblocks data/manifest.sha256). sha256 checked at the start, before every run
  and at the end.
* H-N66C (CubesUnsat105R): own leaf map (`n66r15print leaves` vs campaign_status certified cubes, by literal list);
  seeded sample (random.Random(20261123), 3 leaves) + hhhohh (UP-refuted) + oooooo_40o_52o_46o_44o_45o_39h; per leaf
  `n66r15print trim i <n66-level15 desc/i.txt>` streamed: byte-equal to the certified trim.cnf, sha256 = campaign
  trim_cnf_sha256 = fresh sha256 of the file; cake.out has the exact line.
* H-N66R (RowCertsUnsat): own index->id map from the DataT*/DataC* docstrings; seeded sample of 3 templates (not
  T208) + 1 core: `r15rowprint t|c k` byte-equal to zstd -dc of VB's jobs/<key>.cnf.zst, sha256 = VB json cnf_sha256,
  json exact line; T208: `r15rowprint st 208 <n66-rowsvalid data/trim208.idx>` byte-equal to VB's trimmed CNF,
  sha256 = .trimmed.sha256, .trimmed.cake.out exact line.
* H-ROWS (RowsTextUnsat): seeded 1 row per block: `rowprint row B I` sha256 = every T4 job of that support
  (ACCEPTED, recorded = actual CNF hash, exact line in its cake output, fresh sha256 of the retained CNF).
* fresh cake_lpr (--CML_HEAP_SIZE=2000) on the PRINTED bytes with the recorded LRAT (decompressed into data/tmp,
  stream hash = recorded LRAT hash): hhhohh, oooooo_40o_52o_46o_44o_45o_39h, the smallest sampled template, the
  sampled core, the smallest-LRAT sampled row; negative control: the sampled template's CNF with the core's LRAT.
  Evidence is the exact line `s VERIFIED UNSAT` (grep -x); the exit code is not used.
Writes data/bind_rv5p2.json and data/bind_rv5p2.tsv; exit 1 on any problem."""
import csv, hashlib, json, os, random, re, subprocess, sys, time
from pathlib import Path

P = Path('/home/jay/research/data/formalize-20261122/combined/review/part2')
F = Path('/home/jay/research/data/formalize-20261122')
TMP = P / 'data/tmp'
N66 = Path('/home/jay/research/data/n66-20261113')
J = N66 / 'vfy15/rows/jobs'
EXES = {'n66r15print': (F / 'n66-l15-rows/build/bin/n66r15print',
                        '65865b1e8e57dfe204ac8bbe3fa31cedb0e0cb6f52d6d53e1c7e69cf40104884'),
        'r15rowprint': (F / 'n66-l15-rows/build/bin/r15rowprint',
                        '6b9af2c60542adbb5a422d8f14a26a8ca6a149db21527480c1f1f9e6486e2f4a'),
        'rowprint': (F / 'res118-rowblocks/build/bin/rowprint',
                     'eabe37912b332a844e8731d21f3bf4612a6ad2348a54a8d576c90c13476bd496')}
CAKE = os.path.realpath('/home/jay/.local/bin/cake_lpr')
EXACT = 's VERIFIED UNSAT'
P307 = Path('/home/jay/research/data/roadmap-20261115/pm1115/p307v')
CH = 1 << 20
probs, log = [], []


def say(*a):
    s = ' '.join(str(x) for x in a)
    log.append(s)
    print(s, flush=True)


def sha_file(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(CH), b''):
            h.update(b)
    return h.hexdigest()


def exe_check(name):
    path, pin = EXES[name]
    h = sha_file(path)
    if h != pin:
        probs.append(f'{name} sha256 {h} != {pin}')
        raise SystemExit(f'EXE CHANGED {name}')


def run_print(name, args, ref_file=None, ref_cmd=None, keep=None):
    """Stream the exe's stdout: sha256, byte compare with a reference file or a reference command's stdout,
    optionally write to `keep`. Returns dict."""
    exe_check(name)
    t0 = time.time()
    p = subprocess.Popen(['/usr/bin/time', '-f', 'MAXRSS_KB %M', str(EXES[name][0])] + args,
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    ref = open(ref_file, 'rb') if ref_file else (
        subprocess.Popen(ref_cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL).stdout if ref_cmd else None)
    out = open(keep, 'wb') if keep else None
    h, hr, n, eq = hashlib.sha256(), hashlib.sha256(), 0, ref is not None
    while True:
        b = p.stdout.read(CH)
        if not b:
            break
        h.update(b)
        n += len(b)
        if out:
            out.write(b)
        if ref is not None:
            r = ref.read(len(b))
            hr.update(r)
            if r != b:
                eq = False
    if ref is not None:
        rest = ref.read()
        if rest:
            eq = False
            hr.update(rest)
            for b in iter(lambda: ref.read(CH), b''):
                hr.update(b)
        ref.close()
    if out:
        out.close()
    err = p.stderr.read().decode(errors='replace')
    rc = p.wait()
    m = re.search(r'MAXRSS_KB (\d+)', err)
    return {'rc': rc, 'sha': h.hexdigest(), 'bytes': n, 'equal': eq if ref is not None else None,
            'ref_sha': hr.hexdigest() if ref is not None else None, 'rss_kb': int(m.group(1)) if m else None,
            'stderr': re.sub(r'MAXRSS_KB \d+\n?', '', err).strip()[:300], 'wall_s': round(time.time() - t0, 2)}


def has_exact(path):
    try:
        return EXACT in Path(path).read_text(errors='replace').splitlines()
    except OSError:
        return False


def cake(label, cnf, lrat_src, lrat_ref, expect):
    """Fresh cake_lpr on `cnf` with the LRAT decompressed (or copied) from lrat_src into data/tmp."""
    lrat = TMP / f'{label}.lrat'
    with open(lrat, 'wb') as f:
        cmd = ['zstd', '-dc', '-q', str(lrat_src)] if str(lrat_src).endswith('.zst') else ['cat', str(lrat_src)]
        subprocess.run(cmd, stdout=f, check=True)
    lh = sha_file(lrat)
    outp = P / f'logs/cake/{label}.out'
    t0 = time.time()
    with open(outp, 'w') as f:
        r = subprocess.run(['/usr/bin/time', '-f', 'MAXRSS_KB %M', CAKE, '--CML_HEAP_SIZE=2000', str(cnf), str(lrat)],
                           stdout=f, stderr=subprocess.PIPE)
    err = r.stderr.decode(errors='replace')
    m = re.search(r'MAXRSS_KB (\d+)', err)
    lines = [l for l in outp.read_text(errors='replace').splitlines() if l.strip() == EXACT]
    lrat.unlink()
    res = {'label': label, 'cnf_sha': sha_file(cnf), 'lrat_sha': lh, 'lrat_ref': lrat_ref, 'exact_lines': len(lines),
           'cake_rc': r.returncode, 'rss_kb': int(m.group(1)) if m else None, 'wall_s': round(time.time() - t0, 2),
           'expected': expect}
    if expect == 'ACCEPT':
        res['result'] = 'ACCEPT_OK' if len(lines) == 1 and (lrat_ref is None or lh == lrat_ref) else 'FAIL'
    else:
        res['result'] = 'REJECT_OK' if len(lines) == 0 else 'FAIL'
    if res['result'] == 'FAIL':
        probs.append(f'cake {label}: {res}')
    say('CAKE', json.dumps(res))
    return res


def main():
    t0 = time.time()
    TMP.mkdir(exist_ok=True)
    (P / 'logs/cake').mkdir(exist_ok=True)
    info = {'cake_lpr_sha256': sha_file(CAKE)}
    for name in EXES:
        exe_check(name)
    # freeze manifests name the same hashes
    fm = (F / 'n66-l15-rows/logs/freeze_manifest.sha256').read_text()
    rm = (F / 'res118-rowblocks/data/manifest.sha256').read_text()
    info['exe_pins_in_manifests'] = {
        'n66r15print': f"{EXES['n66r15print'][1]}  {EXES['n66r15print'][0]}" in fm,
        'r15rowprint': f"{EXES['r15rowprint'][1]}  {EXES['r15rowprint'][0]}" in fm,
        'rowprint': f"{EXES['rowprint'][1]}  build/bin/rowprint" in rm}
    if not all(info['exe_pins_in_manifests'].values()):
        probs.append(f"exe pins not in manifests: {info['exe_pins_in_manifests']}")
    rng = random.Random(20261123)
    rows_out = []
    # ---- H-N66C
    camp = json.load(open(N66 / 'p2/c15/campaign_status.json'))
    info['campaign_status_sha256'] = sha_file(N66 / 'p2/c15/campaign_status.json')
    cubes = {k: v for k, v in camp['cubes'].items() if v['status'] == 'certified'}
    r = subprocess.run([str(EXES['n66r15print'][0]), 'leaves'], capture_output=True, check=True)
    leaves = {}
    for l in r.stdout.decode().splitlines():
        i, k = l.split(' ', 1)
        leaves[int(i)] = k
    bykey = {}
    for cid, c in cubes.items():
        bykey.setdefault(' '.join(f'{s}:{b}' for s, b in c['lits']), []).append(cid)
    lmap = {i: bykey.get(k, []) for i, k in leaves.items()}
    info['leafmap_bijection'] = (len(lmap) == 105 == len(cubes) and all(len(v) == 1 for v in lmap.values())
                                 and len({v[0] for v in lmap.values()}) == 105)
    if not info['leafmap_bijection']:
        probs.append('leaf map is not a bijection with the 105 certified cubes')
    inv = {v[0]: i for i, v in lmap.items() if len(v) == 1}
    sample_leaves = sorted(set(rng.sample(range(105), 3)) | {inv['hhhohh'], inv['oooooo_40o_52o_46o_44o_45o_39h']})
    keep_cube = {}
    for i in sample_leaves:
        cid = lmap[i][0]
        c = cubes[cid]
        trim = N66 / c['certdir'] / 'trim.cnf'
        keep = TMP / f'cube_{cid}.cnf' if cid in ('hhhohh', 'oooooo_40o_52o_46o_44o_45o_39h') else None
        pr = run_print('n66r15print', ['trim', str(i), str(F / 'n66-level15/desc' / f'{i}.txt')], ref_file=trim,
                       keep=keep)
        fsha = sha_file(trim)
        e2 = has_exact(N66 / c['certdir'] / 'cake.out')
        ok = pr['rc'] == 0 and pr['equal'] and pr['sha'] == fsha == c['trim_cnf_sha256'] and e2
        rows_out.append(['H-N66C', f'leaf {i}', cid, pr['sha'], c['trim_cnf_sha256'], fsha, str(pr['equal']),
                         str(e2), str(pr['bytes']), str(pr['rss_kb']), 'BOUND' if ok else 'FAIL'])
        if not ok:
            probs.append(f'leaf {i} {cid}: {pr}')
        if keep:
            keep_cube[cid] = (keep, N66 / c['certdir'] / 'trim.lrat.zst', c['trim_lrat_sha256'])
        say('LEAF', i, cid, 'BOUND' if ok else 'FAIL', pr['bytes'], pr['rss_kb'])
    # ---- H-N66R
    L = F / 'n66-l15-rows/lean/N66R15Enc'
    tid, cid_ = {}, {}
    for f in sorted(L.glob('DataT[0-9]*.lean')):
        for m in re.finditer(r'/-- template ([0-9a-f]{16}) -/\ndef tmpl(\d+) : Cert', f.read_text()):
            tid[int(m.group(2))] = 'T_' + m.group(1)
    for f in sorted(L.glob('DataC[0-9]*.lean')):
        for m in re.finditer(r'/-- core (C_[0-9a-f]{16}) -/\ndef core(\d+) : Cert', f.read_text()):
            cid_[int(m.group(2))] = m.group(1)
    info['cert_ids'] = {'templates': len(tid), 'cores': len(cid_)}
    if sorted(tid) != list(range(421)) or sorted(cid_) != list(range(208)):
        probs.append(f"certificate id parse: {info['cert_ids']}")
    ts = sorted(rng.sample([k for k in range(421) if k != 208], 3))
    cs = sorted(rng.sample(range(208), 1))
    certs = []
    for kind, k, key in [('t', k, tid[k]) for k in ts] + [('c', k, cid_[k]) for k in cs]:
        vj = json.load(open(J / f'{key}.json'))
        keep = TMP / f'cert_{key}.cnf'
        pr = run_print('r15rowprint', [kind, str(k)], ref_cmd=['zstd', '-dc', '-q', str(J / f'{key}.cnf.zst')],
                       keep=keep)
        e2 = vj.get('cake_lines') == [EXACT] and vj.get('cake_exact') == 1
        ok = pr['rc'] == 0 and pr['equal'] and pr['sha'] == pr['ref_sha'] == vj.get('cnf_sha256') and e2
        rows_out.append(['H-N66R', f'{kind} {k}', key, pr['sha'], vj.get('cnf_sha256'), pr['ref_sha'], str(pr['equal']),
                         str(e2), str(pr['bytes']), str(pr['rss_kb']), 'BOUND' if ok else 'FAIL'])
        if not ok:
            probs.append(f'cert {kind} {k} {key}: {pr} json {vj.get("cake_lines")} {vj.get("cake_exact")}')
        certs.append((kind, k, key, keep, J / f'{key}.lrat.zst', vj.get('lrat_sha256'),
                      (J / f'{key}.cnf.zst').stat().st_size))
        say('CERT', kind, k, key, 'BOUND' if ok else 'FAIL', pr['bytes'], pr['rss_kb'])
    K = 'T_849f8a5e23a1fc77'
    tsha = [l.split()[0] for l in (J / f'{K}.trimmed.sha256').read_text().splitlines() if l.strip().endswith('.cnf')]
    pr = run_print('r15rowprint', ['st', '208', str(F / 'n66-rowsvalid/data/trim208.idx')],
                   ref_cmd=['zstd', '-dc', '-q', str(J / f'{K}.trimmed.cnf.zst')])
    e2 = has_exact(J / f'{K}.trimmed.cake.out')
    ok = tid.get(208) == K and pr['rc'] == 0 and pr['equal'] and tsha and pr['sha'] == pr['ref_sha'] == tsha[0] and e2
    rows_out.append(['H-N66R', 'st 208', K, pr['sha'], tsha[0] if tsha else '', pr['ref_sha'], str(pr['equal']), str(e2),
                     str(pr['bytes']), str(pr['rss_kb']), 'BOUND' if ok else 'FAIL'])
    if not ok:
        probs.append(f'T208 sub-list: {pr} trimmed.sha256 {tsha} exact {e2}')
    say('T208', 'BOUND' if ok else 'FAIL', pr['bytes'], pr['rss_kb'])
    # ---- H-ROWS
    jobs = {}
    for d in ('lrat-b35s20-v169', 'lrat-b35s19-v16'):
        for row in csv.DictReader(open(P307 / d / 'lrat-results.tsv'), delimiter='\t'):
            row['_cake'] = str(P307 / d / 'cake' / (row['job'] + '.out'))
            jobs.setdefault(row['support'], []).append(row)
    rsel = []
    for b in 'PQUA':
        lst = subprocess.run([str(EXES['rowprint'][0]), 'list', b], capture_output=True, check=True).stdout.decode()
        idx = {int(l.split(' ')[0]): l.split(' ')[1] for l in lst.splitlines() if l.strip()}
        i = rng.choice(sorted(idx))
        supp = idx[i]
        keep = TMP / f'row_{b}{i}.cnf'
        pr = run_print('rowprint', ['row', b, str(i)], keep=keep)
        js = jobs.get(supp, [])
        bad = []
        if not js:
            bad.append('no T4 job')
        for j in js:
            cpath = j['cnf'] if os.path.exists(j['cnf']) else j['cnf'] + '.zst'
            fresh = (sha_file(cpath) if not cpath.endswith('.zst') else hashlib.sha256(
                subprocess.run(['zstd', '-dc', '-q', cpath], capture_output=True, check=True).stdout).hexdigest())
            if not (j['status'] == 'ACCEPTED' and j['cnf_sha_recorded'] == j['cnf_sha_actual'] == pr['sha'] == fresh
                    and has_exact(j['_cake'])):
                bad.append(f"job {j['job']}")
        ok = pr['rc'] == 0 and not bad
        rows_out.append(['H-ROWS', f'{b} {i}', supp, pr['sha'], js[0]['cnf_sha_recorded'] if js else '',
                         str(len(js)) + ' jobs', '', str(not bad), str(pr['bytes']), str(pr['rss_kb']),
                         'BOUND' if ok else 'FAIL'])
        if not ok:
            probs.append(f'row {b} {i}: {bad}')
        if js:
            lsrc = js[0]['lrat'] if os.path.exists(js[0]['lrat']) else js[0]['lrat'] + '.zst'
            rsel.append((os.stat(lsrc).st_size, b, i, keep, lsrc, js[0]['lrat_sha_actual']))
        say('ROW', b, i, 'BOUND' if ok else 'FAIL', pr['bytes'])
    for name in EXES:
        exe_check(name)
    # ---- fresh cake_lpr on printed bytes
    cakes = []
    for cid in ('hhhohh', 'oooooo_40o_52o_46o_44o_45o_39h'):
        keep, lz, lref = keep_cube[cid]
        cakes.append(cake(f'cube_{cid}', keep, lz, lref, 'ACCEPT'))
    tsel = min((c for c in certs if c[0] == 't'), key=lambda c: c[6])
    csel = next(c for c in certs if c[0] == 'c')
    cakes.append(cake(f'cert_{tsel[2]}', tsel[3], tsel[4], tsel[5], 'ACCEPT'))
    cakes.append(cake(f'cert_{csel[2]}', csel[3], csel[4], csel[5], 'ACCEPT'))
    cakes.append(cake(f'NEG_{tsel[2]}_cnf_with_{csel[2]}_lrat', tsel[3], csel[4], None, 'REJECT'))
    rs = min(rsel)
    cakes.append(cake(f'row_{rs[1]}{rs[2]}', rs[3], rs[4], rs[5], 'ACCEPT'))
    for x in TMP.iterdir():
        x.unlink()
    info.update({'sample_leaves': sample_leaves, 'sample_templates': ts, 'sample_cores': cs,
                 'bound': sum(1 for r in rows_out if r[-1] == 'BOUND'), 'items': len(rows_out), 'cakes': cakes,
                 'seconds': round(time.time() - t0, 1), 'problems': probs})
    (P / 'data/bind_rv5p2.tsv').write_text('hyp\titem\tid\tprinted_sha256\trecorded_sha256\treference_sha256\t'
                                           'byte_equal\tE2_record\tbytes\tmaxrss_kb\tstatus\n' +
                                           ''.join('\t'.join(r) + '\n' for r in rows_out))
    (P / 'data/bind_rv5p2.json').write_text(json.dumps(info, indent=1) + '\n')
    print(json.dumps(info, indent=1))
    return 1 if probs else 0


if __name__ == '__main__':
    sys.exit(main())
