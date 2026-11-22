#!/usr/bin/env python3
"""Reviewer rv5: own E1 re-print of the row certificates with the worker's frozen exe r15rowprint.

Runs inside unit esr-ag-rv5-e1r. Reads only outside review/; writes review/e1r_*.

* exe hash (coreutils) checked at the start, before every exe run and at the end (freeze-manifest hash).
* index -> id from the docstrings of the exe's own source files N66R15Enc/DataT*.lean, DataC*.lean (own parse).
* for every template except T208 and every core: `r15rowprint t|c k` streamed and compared byte for byte with
  `zstd -dc` of VB's kept jobs/<key>.cnf.zst; printed SHA-256 (hashlib) = decompressed SHA-256 = VB's json
  cnf_sha256; VB's json: cake_lines == ["s VERIFIED UNSAT"], cake_exact == 1, certified true.
* T208: `r15rowprint st 208 <n66-rowsvalid data/trim208.idx>` compared byte for byte with zstd -dc of VB's
  T_849f8a5e23a1fc77.trimmed.cnf.zst; hashes vs VB's .trimmed.sha256; .trimmed.cake.out exact line.
* controls: T0's print vs T1's CNF; out-of-range template index; out-of-range sub-list index; T208 sub-list with
  the last index dropped.
Order: smallest VB CNF first, T208 st last (largest memory).
"""
import hashlib, json, os, re, subprocess, sys, time
from pathlib import Path

V = Path('/home/jay/research/data/formalize-20261122/n66-l15-rows/review')
EXE = '/home/jay/research/data/formalize-20261122/n66-l15-rows/build/bin/r15rowprint'
EXE_SHA = '6b9af2c60542adbb5a422d8f14a26a8ca6a149db21527480c1f1f9e6486e2f4a'
L = Path('/home/jay/research/data/formalize-20261122/n66-l15-rows/lean/N66R15Enc')
J = Path('/home/jay/research/data/n66-20261113/vfy15/rows/jobs')
IDX208 = Path('/home/jay/research/data/formalize-20261122/n66-rowsvalid/data/trim208.idx')
EXACT = 's VERIFIED UNSAT'
CH = 1 << 20


def sha_cu(p):
    return subprocess.run(['sha256sum', str(p)], capture_output=True, text=True, check=True).stdout.split()[0]


def exe_ok():
    h = sha_cu(EXE)
    if h != EXE_SHA:
        raise SystemExit(f'EXE CHANGED: {h}')


def run(args, zst=None):
    """Run the exe under /usr/bin/time; stream stdout; if zst, compare with `zstd -dc zst` byte for byte."""
    exe_ok()
    t0 = time.time()
    p = subprocess.Popen(['/usr/bin/time', '-f', 'MAXRSS_KB %M', EXE] + args, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    z = subprocess.Popen(['zstd', '-dc', str(zst)], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL) if zst else None
    h, hz, n, eq = hashlib.sha256(), hashlib.sha256(), 0, zst is not None
    while True:
        b = p.stdout.read(CH)
        if not b:
            break
        h.update(b)
        n += len(b)
        if z is not None:
            c = z.stdout.read(len(b))
            hz.update(c)
            if c != b:
                eq = False
    if z is not None:
        while True:  # rest of the reference (must be empty for equality)
            c = z.stdout.read(CH)
            if not c:
                break
            hz.update(c)
            eq = False
        z.wait()
    err = p.stderr.read().decode()
    rc = p.wait()
    m = re.search(r'MAXRSS_KB (\d+)', err)
    return {'rc': rc, 'sha': h.hexdigest(), 'n': n, 'equal': eq if zst else None,
            'ref_sha': hz.hexdigest() if zst else None, 'rss_kb': int(m.group(1)) if m else None,
            'err': re.sub(r'MAXRSS_KB \d+\n?', '', err).strip(), 'wall': round(time.time() - t0, 2)}


def ids(pattern, files, rx):
    out = {}
    for f in files:
        for m in re.finditer(rx, f.read_text()):
            out[int(m.group(2))] = m.group(1)
    return out


def main():
    log = open(V / 'e1r.log', 'a')
    def say(*a):
        print(*a, file=log, flush=True)
    say(f'== {time.strftime("%F %T")} own_e1r start; exe {sha_cu(EXE)}')
    tid = ids('T', sorted(L.glob('DataT[0-9].lean')), r'/-- template ([0-9a-f]{16}) -/\ndef tmpl(\d+) : Cert')
    cid = ids('C', sorted(L.glob('DataC[0-9].lean')), r'/-- core (C_[0-9a-f]{16}) -/\ndef core(\d+) : Cert')
    assert sorted(tid) == list(range(421)) and sorted(cid) == list(range(208))
    jobs = [('t', k, f'T_{tid[k]}') for k in range(421) if k != 208] + [('c', k, cid[k]) for k in range(208)]
    jobs.sort(key=lambda x: (J / f'{x[2]}.cnf.zst').stat().st_size)
    cols = ['kind', 'idx', 'key', 'rc', 'bytes', 'printed_sha', 'vb_decompressed_sha', 'cmp_equal', 'vb_json_cnf_sha256',
            'vb_cake_exact_line', 'vb_certified', 'rss_kb', 'wall_s', 'verdict']
    rows = []
    for kind, k, key in jobs:
        vj = json.load(open(J / f'{key}.json'))
        r = run([kind, str(k)], zst=J / f'{key}.cnf.zst')
        line_ok = vj.get('cake_lines') == [EXACT] and vj.get('cake_exact') == 1
        ok = r['rc'] == 0 and r['equal'] is True and r['sha'] == r['ref_sha'] == vj.get('cnf_sha256')
        row = {'kind': kind, 'idx': k, 'key': key, 'rc': r['rc'], 'bytes': r['n'], 'printed_sha': r['sha'],
               'vb_decompressed_sha': r['ref_sha'], 'cmp_equal': r['equal'], 'vb_json_cnf_sha256': vj.get('cnf_sha256'),
               'vb_cake_exact_line': line_ok, 'vb_certified': vj.get('certified'), 'rss_kb': r['rss_kb'],
               'wall_s': r['wall'],
               'verdict': ('MATCH' if ok else 'DIFFER') + ('/E2ok' if line_ok and vj.get('certified') is True else '/E2?')}
        rows.append(row)
        say(kind, k, key, row['verdict'], r['n'], r['rss_kb'], r['wall'])
    # controls (small)
    ctl = []
    r = run(['t', '0'], zst=J / f'T_{tid[1]}.cnf.zst')
    ctl.append(('a T0 print vs T1 CNF', r['rc'], r['equal'], 'PASS' if r['equal'] is False else 'FAIL'))
    r = run(['t', '421'])
    ctl.append(('b template index 421', r['rc'], r['n'], r['err'], 'PASS' if r['rc'] != 0 and r['n'] == 0 else 'FAIL'))
    (V / 'ctl_bad.idx').write_text('0\n99999999\n')
    r = run(['st', '0', str(V / 'ctl_bad.idx')])
    ctl.append(('c sub-list with an out-of-range index (template 0)', r['rc'], r['n'], r['err'],
                'PASS' if r['rc'] == 1 and r['n'] == 0 else 'FAIL'))
    # T208, the theorem route (sub-list), then the dropped-index control
    key = f'T_{tid[208]}'
    vj = json.load(open(J / f'{key}.json'))
    tsha = (J / f'{key}.trimmed.sha256').read_text().split()
    tco = [x for x in (J / f'{key}.trimmed.cake.out').read_text().splitlines() if x.strip()]
    r = run(['st', '208', str(IDX208)], zst=J / f'{key}.trimmed.cnf.zst')
    t208 = {'key': key, 'idx_file': str(IDX208), 'idx_file_sha256': sha_cu(IDX208), 'rc': r['rc'], 'bytes': r['n'],
            'printed_sha': r['sha'], 'vb_trimmed_decompressed_sha': r['ref_sha'], 'cmp_equal': r['equal'],
            'vb_trimmed_sha256_file': tsha, 'trimmed_cake_out_lines': tco, 'vb_full_json_certified': vj.get('certified'),
            'vb_full_json_cnf_sha256': vj.get('cnf_sha256'), 'rss_kb': r['rss_kb'], 'wall_s': r['wall']}
    t208['verdict'] = 'MATCH' if (r['rc'] == 0 and r['equal'] is True and r['sha'] == r['ref_sha'] and
                                   r['sha'] in tsha and tco == [EXACT]) else 'DIFFER'
    say('T208 st', t208['verdict'], r['n'], r['rss_kb'], r['wall'])
    lines = [x for x in IDX208.read_text().split('\n') if x.strip()]
    (V / 'ctl_t208_drop_last.idx').write_text('\n'.join(lines[:-1]) + '\n')
    r = run(['st', '208', str(V / 'ctl_t208_drop_last.idx')], zst=J / f'{key}.trimmed.cnf.zst')
    ctl.append(('d T208 sub-list with the last index dropped', r['rc'], r['equal'], r['sha'],
                'PASS' if r['equal'] is False and r['sha'] != t208['printed_sha'] else 'FAIL'))
    with open(V / 'e1r_runs.tsv', 'w') as f:
        f.write('\t'.join(cols) + '\n')
        for row in rows:
            f.write('\t'.join(str(row[c]) for c in cols) + '\n')
    with open(V / 'e1r_controls.txt', 'w') as f:
        for c in ctl:
            f.write('\t'.join(map(str, c)) + '\n')
    summ = {'exe_sha_expected': EXE_SHA, 'exe_sha_end': sha_cu(EXE), 'full_certs_printed': len(rows),
            'MATCH': sum(1 for x in rows if x['verdict'].startswith('MATCH')),
            'E2ok_vb_lines': sum(1 for x in rows if x['verdict'].endswith('E2ok')),
            'templates': sum(1 for x in rows if x['kind'] == 't'), 'cores': sum(1 for x in rows if x['kind'] == 'c'),
            'max_rss_kb_full': max(x['rss_kb'] or 0 for x in rows), 'T208': t208,
            'controls': [c[-1] for c in ctl]}
    (V / 'e1r_summary.json').write_text(json.dumps(summ, indent=1) + '\n')
    say(f'== {time.strftime("%F %T")} done: MATCH {summ["MATCH"]}/{len(rows)}, T208 {t208["verdict"]}, '
        f'controls {summ["controls"]}')


if __name__ == '__main__':
    main()
