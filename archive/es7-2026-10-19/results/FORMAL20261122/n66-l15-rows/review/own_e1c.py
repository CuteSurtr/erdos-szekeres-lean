#!/usr/bin/env python3
"""Reviewer rv5: own E1 re-print of the 105 level-15 cube trims with the worker's frozen exe n66r15print.

Runs inside unit esr-ag-rv5-e1c. Reads only outside review/; writes review/e1c_*.

* exe hash checked (coreutils) at the start, before every exe run, and at the end; must equal the freeze-manifest hash.
* exe `stats`, `rows`, `leaves`: rows compared with rows_used15.txt and with the reviewer's #eval dump of R1_15;
  leaves compared with the reviewer's #eval dump of leaves105; own leaf map: exe leaf i -> the unique certified
  campaign cube with the same literals in the same order (bijection required).
* per leaf i: `n66r15print trim i <n66-level15 desc/i.txt>` streamed and compared byte for byte with that cube's
  certified trim.cnf; printed SHA-256 (own hashlib) = coreutils sha256sum of the file = campaign trim_cnf_sha256 =
  cert.json = verify.json = vfy15 summary trim_cnf_sha = vfy15/cake/<id>.sha256; stderr cube = campaign lits,
  stderr clause count = campaign trim_cnf_clauses.
* per leaf E2 record checks (read only): cake.out == "s VERIFIED UNSAT\\n"; cert.json/verify.json cake_lpr exact
  line and ALL_OK; vfy15 summary cake_line == ["s VERIFIED UNSAT"]; vfy15/cake/<id>.cake.out has exactly one
  nonempty line, the exact line; vfy15 status cake_rc=0; vfy15 stream hash = campaign trim_lrat_sha256.
* controls: tampered descriptor, leaf index 105, leaf 1's descriptors printed as leaf 0, tampered copy of a trim
  file, comparator self-test with a flipped recorded hash.
"""
import hashlib, json, re, subprocess, sys, time
from pathlib import Path

V = Path('/home/jay/research/data/formalize-20261122/n66-l15-rows/review')
EXE = '/home/jay/research/data/formalize-20261122/n66-l15-rows/build/bin/n66r15print'
EXE_SHA = '65865b1e8e57dfe204ac8bbe3fa31cedb0e0cb6f52d6d53e1c7e69cf40104884'
L15 = Path('/home/jay/research/data/formalize-20261122/n66-level15')
W = Path('/home/jay/research/data/n66-20261113')
ROWS15 = L15 / 'lean/N66E15/data/rows_used15.txt'
EXACT = 's VERIFIED UNSAT'
CH = 1 << 20


def sha_cu(p):
    return subprocess.run(['sha256sum', str(p)], capture_output=True, text=True, check=True).stdout.split()[0]


def exe_ok():
    h = sha_cu(EXE)
    if h != EXE_SHA:
        raise SystemExit(f'EXE CHANGED: {h}')
    return True


def run(args, ref=None, keep=False):
    """Run the exe (under /usr/bin/time), stream stdout; return dict(rc, sha, n, equal, err, rss, wall, out)."""
    exe_ok()
    t0 = time.time()
    p = subprocess.Popen(['/usr/bin/time', '-f', 'MAXRSS_KB %M', EXE] + args, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    h = hashlib.sha256()
    n = 0
    eq = ref is not None
    f = open(ref, 'rb') if ref is not None else None
    buf = [] if keep else None
    while True:
        b = p.stdout.read(CH)
        if not b:
            break
        h.update(b)
        n += len(b)
        if keep:
            buf.append(b)
        if f is not None and eq:
            if f.read(len(b)) != b:
                eq = False
    if f is not None:
        if eq and f.read(1) != b'':
            eq = False
        f.close()
    err = p.stderr.read().decode()
    rc = p.wait()
    m = re.search(r'MAXRSS_KB (\d+)', err)
    return {'rc': rc, 'sha': h.hexdigest(), 'n': n, 'equal': eq if ref is not None else None,
            'err': re.sub(r'MAXRSS_KB \d+\n?', '', err).strip(), 'rss_kb': int(m.group(1)) if m else None,
            'wall': round(time.time() - t0, 2), 'out': b''.join(buf) if keep else None}


def same(*hs):
    return all(x is not None for x in hs) and len(set(hs)) == 1


def main():
    log = open(V / 'e1c.log', 'a')
    def say(*a):
        print(*a, file=log, flush=True)
    say(f'== {time.strftime("%F %T")} own_e1c start; exe {sha_cu(EXE)}')
    summ = {'exe': EXE, 'exe_sha_expected': EXE_SHA}
    camp = json.load(open(W / 'p2/c15/campaign_status.json'))
    summ['campaign_status_sha256'] = sha_cu(W / 'p2/c15/campaign_status.json')
    summ['vfy15_summary_sha256'] = sha_cu(W / 'vfy15/summary.json')
    cubes = {k: v for k, v in camp['cubes'].items() if v['status'] == 'certified'}
    vfy = {e['id']: e for e in json.load(open(W / 'vfy15/summary.json'))}
    # stats / rows / leaves
    r = run(['stats'], keep=True)
    (V / 'e1c_exe_stats.txt').write_bytes(r['out'])
    summ['stats'] = r['out'].decode()
    r = run(['rows'], keep=True)
    (V / 'e1c_exe_rows.txt').write_bytes(r['out'])
    summ['rows_rc'] = r['rc']
    summ['rows_equal_rows_used15'] = r['out'] == ROWS15.read_bytes()
    summ['rows_equal_own_eval_dump'] = r['out'] == (V / 'dump_R1_15.txt').read_bytes()
    summ['rows_sha256'] = r['sha']
    r = run(['leaves'], keep=True)
    (V / 'e1c_exe_leaves.txt').write_bytes(r['out'])
    lines = r['out'].decode().splitlines()
    dump = (V / 'dump_leaves105.txt').read_text().splitlines()
    summ['leaves_count'] = len(lines)
    summ['leaves_equal_own_eval_dump'] = [l.split(' ', 1)[1] if ' ' in l else '' for l in lines] == dump and \
        [l.split(' ', 1)[0] for l in lines] == [str(i) for i in range(len(lines))]
    key = {}
    for cid, c in cubes.items():
        k = ' '.join(f'{s}:{b}' for s, b in c['lits'])
        key.setdefault(k, []).append(cid)
    lmap = {}
    for l in lines:
        i, k = l.split(' ', 1)
        lmap[int(i)] = key.get(k, [])
    summ['leafmap_bijection'] = (all(len(v) == 1 for v in lmap.values()) and
                                 len({v[0] for v in lmap.values()}) == len(cubes) == len(lmap) == 105)
    with open(V / 'e1c_leafmap.tsv', 'w') as f:
        for i in sorted(lmap):
            cid = lmap[i][0]
            f.write(f"{i}\t{cid}\t{cubes[cid]['certdir']}\t{' '.join(f'{s}:{b}' for s, b in cubes[cid]['lits'])}\n")
    say('stats/rows/leaves done', summ['rows_equal_rows_used15'], summ['leaves_equal_own_eval_dump'],
        summ['leafmap_bijection'])
    # per leaf
    cols = ['i', 'cube', 'rc', 'bytes', 'printed_sha', 'file_sha_coreutils', 'cmp_equal', 'rec_campaign',
            'rec_cert_json', 'rec_verify_json', 'rec_vfy15', 'rec_vfy15_file', 'stderr_cube_ok', 'clauses_ok',
            'cake_out_exact', 'cert_json_line_allok', 'verify_json_line_allok', 'vfy15_line', 'vfy15_raw_exact',
            'vfy15_rc0', 'vfy15_stream_eq_lrat', 'rss_kb', 'wall_s', 'verdict']
    rows = []
    for i in range(105):
        cid = lmap[i][0]
        c = cubes[cid]
        cd = W / c['certdir']
        trim = cd / 'trim.cnf'
        r = run(['trim', str(i), str(L15 / 'desc' / f'{i}.txt')], ref=trim)
        fsha = sha_cu(trim)
        cj = json.load(open(cd / 'cert.json'))
        vj = json.load(open(cd / 'verify.json'))
        ve = vfy.get(cid, {})
        vfile = (W / 'vfy15/cake' / f'{cid}.sha256')
        vfsha = vfile.read_text().split()[0] if vfile.exists() else None
        m = re.match(r'leaf (\d+) \[(.*)\] clauses (\d+)$', r['err'])
        cube_s = ' '.join(f'{s}:{b}' for s, b in c['lits'])
        st_cube = bool(m) and m.group(1) == str(i) and m.group(2) == cube_s
        st_cl = bool(m) and int(m.group(3)) == c['trim_cnf_clauses']
        cake_out = (cd / 'cake.out').read_bytes() if (cd / 'cake.out').exists() else None
        raw = W / 'vfy15/cake' / f'{cid}.cake.out'
        raw_lines = [x for x in raw.read_text().splitlines() if x.strip()] if raw.exists() else None
        stat = W / 'vfy15/cake' / f'{cid}.status'
        strm = W / 'vfy15/cake' / f'{cid}.stream'
        row = {
            'i': i, 'cube': cid, 'rc': r['rc'], 'bytes': r['n'], 'printed_sha': r['sha'], 'file_sha_coreutils': fsha,
            'cmp_equal': r['equal'], 'rec_campaign': c['trim_cnf_sha256'], 'rec_cert_json': cj.get('trim_cnf_sha256'),
            'rec_verify_json': vj.get('trim_cnf_sha256'), 'rec_vfy15': ve.get('trim_cnf_sha'), 'rec_vfy15_file': vfsha,
            'stderr_cube_ok': st_cube, 'clauses_ok': st_cl,
            'cake_out_exact': cake_out == (EXACT + '\n').encode(),
            'cert_json_line_allok': cj.get('cake_lpr') == EXACT and cj.get('ALL_OK') is True,
            'verify_json_line_allok': vj.get('cake_lpr') == EXACT and vj.get('ALL_OK') is True,
            'vfy15_line': ve.get('cake_line') == [EXACT] and ve.get('cake_ok') is True,
            'vfy15_raw_exact': raw_lines == [EXACT],
            'vfy15_rc0': stat.exists() and 'cake_rc=0' in stat.read_text(),
            'vfy15_stream_eq_lrat': strm.exists() and strm.read_text().split()[0] == c['trim_lrat_sha256'],
            'rss_kb': r['rss_kb'], 'wall_s': r['wall']}
        ok = (r['rc'] == 0 and r['equal'] is True and same(r['sha'], fsha, row['rec_campaign'], row['rec_cert_json'],
              row['rec_verify_json'], row['rec_vfy15'], row['rec_vfy15_file']) and st_cube and st_cl)
        e2 = all(row[k] for k in ['cake_out_exact', 'cert_json_line_allok', 'verify_json_line_allok', 'vfy15_line',
                                   'vfy15_raw_exact', 'vfy15_rc0', 'vfy15_stream_eq_lrat'])
        row['verdict'] = ('MATCH' if ok else 'DIFFER') + ('/E2ok' if e2 else '/E2?')
        rows.append(row)
        say(i, cid, row['verdict'], r['n'], r['rss_kb'], r['wall'])
    with open(V / 'e1c_runs.tsv', 'w') as f:
        f.write('\t'.join(cols) + '\n')
        for row in rows:
            f.write('\t'.join(str(row[k]) for k in cols) + '\n')
    summ['leaves_MATCH'] = sum(1 for x in rows if x['verdict'].startswith('MATCH'))
    summ['leaves_E2ok'] = sum(1 for x in rows if x['verdict'].endswith('E2ok'))
    summ['distinct_texts'] = len({x['printed_sha'] for x in rows})
    summ['total_bytes'] = sum(x['bytes'] for x in rows)
    summ['max_rss_kb'] = max(x['rss_kb'] or 0 for x in rows)
    summ['indices_covered'] = sorted(x['i'] for x in rows) == list(range(105))
    # controls
    ctl = []
    i0 = 0
    trim0 = W / cubes[lmap[0][0]]['certdir'] / 'trim.cnf'
    trim1 = W / cubes[lmap[1][0]]['certdir'] / 'trim.cnf'
    d0 = (L15 / 'desc/0.txt').read_text().split('\n')
    m = re.match(r'E (\d+)$', d0[0])
    d0t = d0[:]
    d0t[0] = f'E {int(m.group(1)) + 1}'
    (V / 'ctl_desc0_tampered.txt').write_text('\n'.join(d0t))
    r = run(['trim', '0', str(V / 'ctl_desc0_tampered.txt')], ref=trim0)
    ctl.append(('a tampered descriptor (leaf 0, first line E k -> E k+1)', r['rc'], r['sha'], r['equal'],
                'PASS' if r['equal'] is False and r['sha'] != rows[0]['printed_sha'] else 'FAIL'))
    r = run(['trim', '105', str(L15 / 'desc/0.txt')])
    ctl.append(('b leaf index 105', r['rc'], r['n'], r['err'], 'PASS' if r['rc'] == 1 and r['n'] == 0 else 'FAIL'))
    r0 = run(['trim', '0', str(L15 / 'desc/1.txt')], ref=trim0)
    eq1 = None
    if r0['rc'] == 0:
        r1 = run(['trim', '0', str(L15 / 'desc/1.txt')], ref=trim1)
        eq1 = r1['equal']
    ctl.append(('c leaf 1 descriptors printed as leaf 0', r0['rc'], r0['sha'], r0['equal'], eq1, r0['err'][:120],
                'PASS' if (r0['rc'] != 0 and r0['n'] == 0) or (r0['equal'] is False and eq1 is False) else 'FAIL'))
    # tampered copy of a trim file (an UP-refuted leaf: 6 clauses)
    up = [x for x in rows if x['bytes'] < 200][0]
    src = W / cubes[up['cube']]['certdir'] / 'trim.cnf'
    txt = src.read_text().split('\n')
    txt[1] = txt[1].replace('-', '', 1) if txt[1].startswith('-') else '-' + txt[1]
    (V / 'ctl_trim_tampered.cnf').write_text('\n'.join(txt))
    r = run(['trim', str(up['i']), str(L15 / 'desc' / f"{up['i']}.txt")], ref=V / 'ctl_trim_tampered.cnf')
    ctl.append((f"d tampered copy of leaf {up['i']}'s trim.cnf (first clause literal negated)", r['rc'], r['sha'],
                r['equal'], sha_cu(V / 'ctl_trim_tampered.cnf'),
                'PASS' if r['equal'] is False and r['sha'] != sha_cu(V / 'ctl_trim_tampered.cnf') else 'FAIL'))
    flip = rows[5]['rec_campaign']
    flip = flip[:-1] + ('0' if flip[-1] != '0' else '1')
    ctl.append(('e comparator self-test: leaf 5 with its recorded hash last digit changed',
                same(rows[5]['printed_sha'], rows[5]['file_sha_coreutils'], flip),
                'PASS' if not same(rows[5]['printed_sha'], rows[5]['file_sha_coreutils'], flip) else 'FAIL'))
    with open(V / 'e1c_controls.txt', 'w') as f:
        for c in ctl:
            f.write('\t'.join(map(str, c)) + '\n')
    summ['controls'] = [c[-1] for c in ctl]
    summ['exe_sha_end'] = sha_cu(EXE)
    (V / 'e1c_summary.json').write_text(json.dumps(summ, indent=1) + '\n')
    say(f'== {time.strftime("%F %T")} done: MATCH {summ["leaves_MATCH"]}/105, E2ok {summ["leaves_E2ok"]}/105, '
        f'controls {summ["controls"]}')


if __name__ == '__main__':
    main()
