"""Read-only re-check of the certified cubes of the N66 level-14 cube campaign (15 Nov 2026), input for PROGRESS.md.
Per certified cube (status 'certified' in campaign_status.json), all must hold for the cube to count:
  cake.out has the exact line 's VERIFIED UNSAT'; cake.err's timed command is ~/.local/bin/cake_lpr on this certdir's trim.cnf trim.lrat;
  sha256sum(trim.cnf), sha256sum(trim.lrat) recomputed = cert.json = verify.json = driver status; zstd -dc trim.lrat.zst | sha256sum = trim.lrat;
  cert.json and verify.json ALL_OK, cake_lpr fields = the exact line, unclassified 0, kinds sum = clauses = trim.cnf header count;
  budget 14, W_size 70, layout sel/W/L, cube (layout, verify, cert) = plan, sb_pairs = b14h2's; rows: used = fv66 = justified, fv66 bad 0,
  rows_match, template unjustified 0, link re-check ALL_OK (when rows > 0); CaDiCaL 'Version 2.1.3', 'exit 20', 's UNSATISFIABLE';
  pipeline.log has the cadical/trim/cake/verify/cert.json steps and ends with P2_CERT_DONE.
Also an exact cover check by brute force over all assignments of the states that occur in any cube (own code, not the driver's).
Results are cached in the output JSON per certdir (file sizes and mtimes).  usage: chk.py OUT.json"""
import json, os, subprocess, sys, itertools, glob

W = '/home/jay/research/data/n66-20261113'
STATUS = os.environ.get('N66_STATUS', W + '/p2/c14/campaign_status.json')   # a frozen copy may be given
CAKE = '/home/jay/.local/bin/cake_lpr'
REF = json.load(open(W + '/p2/b14h2/it1/layout.json'))
SEL0 = 988541
SPLIT = [25, 12, 16, 29, 17, 37]
out = sys.argv[1]
cache = json.load(open(out))['cubes'] if os.path.exists(out) else {}

def sh(cmd):
    r = subprocess.run(['bash', '-o', 'pipefail', '-c', cmd], capture_output=True, text=True)
    if r.returncode: raise RuntimeError(f'{cmd}: rc {r.returncode} {r.stderr[-200:]}')
    return r.stdout

def sha(p): return sh(f"nice -n 10 sha256sum '{p}'").split()[0]
def stamp(d): return {f: [os.path.getsize(f'{d}/{f}'), os.stat(f'{d}/{f}').st_mtime_ns] if os.path.exists(f'{d}/{f}') else None
                     for f in ('trim.cnf', 'trim.lrat', 'trim.lrat.zst', 'cake.out', 'cake.err', 'cert.json', 'verify.json', 'pipeline.log')}

def check(c, prev=None):
    d = os.path.join(W, c['certdir']); rel = c['certdir']
    chk, info = {}, {'certdir': d}
    cake_lines = [l.rstrip('\n') for l in open(d + '/cake.out')]
    chk['cake_exact_line'] = cake_lines.count('s VERIFIED UNSAT') == 1
    info['cake_line'] = 's VERIFIED UNSAT' if chk['cake_exact_line'] else repr(cake_lines[-3:])
    cmdl = [l for l in open(d + '/cake.err') if 'Command being timed' in l]
    chk['cake_cmd'] = len(cmdl) == 1 and f'{CAKE} ' in cmdl[0] and f'{rel}/trim.cnf {rel}/trim.lrat"' in cmdl[0]
    info['cake_cmd'] = cmdl[0].strip() if cmdl else None
    att = json.load(open(d + '/cake_attempts.json'))
    chk['cake_attempt_verified'] = bool(att) and att[-1].get('verified') is True
    info['cake_heap_mb'], info['cake_s'], info['cake_rss_kb'] = att[-1].get('heap'), att[-1].get('seconds'), att[-1].get('max_rss_kb')
    info['cake_attempts'] = len(att)
    cj = json.load(open(d + '/cert.json')); vj = json.load(open(d + '/verify.json')); lay = json.load(open(d + '/layout.json'))
    K = ('trim_cnf_sha256', 'trim_lrat_sha256', 'trim_lrat_zst_sha256_of_content')
    if prev and all((prev.get('info') or {}).get(k) for k in K):      # same files (sizes, mtimes): reuse the hashes computed earlier
        tc, tl, tz = (prev['info'][k] for k in K)
    else:
        tc, tl = sha(d + '/trim.cnf'), sha(d + '/trim.lrat')
        tz = sh(f"nice -n 10 zstd -dc -q '{d}/trim.lrat.zst' | nice -n 10 sha256sum").split()[0]
    info.update({'trim_cnf_sha256': tc, 'trim_lrat_sha256': tl, 'trim_lrat_zst_sha256_of_content': tz, 'full_cnf_sha256': cj.get('full_cnf_sha256'),
                 'trim_cnf_bytes': os.path.getsize(d + '/trim.cnf'), 'trim_lrat_bytes': os.path.getsize(d + '/trim.lrat'),
                 'trim_lrat_zst_bytes': os.path.getsize(d + '/trim.lrat.zst'), 'trim_cnf_clauses': vj.get('clauses'), 'kinds': vj.get('kinds'),
                 'cert_time': cj.get('time')})
    chk['trim_cnf_sha256'] = tc == cj['trim_cnf_sha256'] == vj['trim_cnf_sha256'] == c.get('trim_cnf_sha256')
    chk['trim_lrat_sha256'] = tl == cj['trim_lrat_sha256'] == vj['trim_lrat_sha256'] == c.get('trim_lrat_sha256')
    chk['zst_roundtrip'] = tz == tl
    chk['trim_lrat_bytes'] = info['trim_lrat_bytes'] == cj['trim_lrat_bytes']
    chk['cert_ALL_OK'] = cj.get('ALL_OK') is True and cj.get('cake_lpr') == 's VERIFIED UNSAT'
    chk['verify_ALL_OK'] = vj.get('ALL_OK') is True and vj.get('cake_lpr') == 's VERIFIED UNSAT' and vj.get('vars_ok') is True
    chk['unclassified_0'] = vj.get('unclassified') == 0 and not vj.get('unclassified_sample')
    hdr = sh(f"head -c 4096 '{d}/trim.cnf' | grep -m1 '^p cnf'").split()
    info['trim_cnf_header'] = ' '.join(hdr)
    # p2_verify classifies the distinct clauses (kinds sum = distinct_clauses); duplicates are repeated copies of classified clauses
    chk['clause_counts'] = sum(vj['kinds'].values()) == vj['distinct_clauses'] and vj['clauses'] == cj['trim_cnf_clauses'] == int(hdr[3])
    info['duplicate_clauses'] = vj['clauses'] - vj['distinct_clauses']
    lits = [list(x) for x in c['lits']]
    chk['budget_W_sel'] = (lay['L'] == vj['budget'] == cj['budget'] == 14 and cj['W_size'] == 70 and lay['W'] == list(range(70))
                           and lay['sel'] == [SEL0, SEL0 + 69] and cj.get('bound') == 55 and cj.get('holes_at_least') == 15)
    chk['cube_matches_plan'] = lay['cube'] == vj['cube'] == cj['cube'] == lits
    chk['sb_pairs_b14h2'] = lay.get('sb_pairs') == vj.get('sb_pairs') == cj.get('sb_pairs') == REF['sb_pairs']
    nrows = vj['kinds'].get('rows', 0)
    used = json.load(open(d + '/used_rows.json'))
    info['rows'] = nrows
    if nrows:
        fv = json.loads(open(d + '/fv66.out').read().strip().splitlines()[-1])
        tco = [json.loads(l) for l in open(d + '/tcert.out') if l.strip().startswith('{')]
        rc = json.load(open(d + '/tcert/recheck.json'))
        chk['rows_justified'] = (len(used) == nrows == fv['rows'] == vj['justification']['justified_rows'] == cj['used']['used_rows']
                                 and fv['bad'] == 0 and fv['rows_match'] is True and tco[-1].get('unjustified') == 0
                                 and fv['templates_verified'] == fv['templates'] and fv['cores_verified'] == fv['cores']
                                 and rc.get('ALL_OK') is True and cj.get('link_recheck_ALL_OK') is True)
        info['row_kinds'] = fv['kinds']; info['templates'] = fv['templates']; info['cores'] = fv['cores']
    else:
        chk['rows_justified'] = len(used) == 0 and cj['used']['used_rows'] == 0
    cad = open(d + '/cadical.log').read()
    chk['cadical_2.1.3_unsat'] = 'c Version 2.1.3\n' in cad and '\nexit 20\n' in cad and '\ns UNSATISFIABLE\n' in cad
    pl = open(d + '/pipeline.log').read().splitlines()
    need = ['cadical UNSAT', 'trimmed:', 'cake_lpr: s VERIFIED UNSAT', 'verify:', 'cert.json written: CERTIFIED holes >= 15']
    chk['pipeline_steps'] = all(any(n in l for l in pl) for n in need) and pl[-1] == 'P2_CERT_DONE'
    info['lrat_full_sha256'] = (open(d + '/cert.lrat.sha256').read().split() or [None])[0] if os.path.exists(d + '/cert.lrat.sha256') else None
    info['untrimmed_lrat_present'] = os.path.exists(d + '/cert.lrat')
    info['cert_cnf_present'] = os.path.exists(d + '/cert.cnf')
    bad = [k for k, v in chk.items() if v is not True]
    return {'ok': not bad, 'bad': bad, 'checks': chk, 'info': info}

def uncovered(cubes, vs):
    n = 0
    for bits in itertools.product((0, 1), repeat=len(vs)):
        a = dict(zip(vs, bits))
        if not any(all(a[s] == b for s, b in cb) for cb in cubes): n += 1
    return n

st = json.load(open(STATUS))
res = {}
for i, c in st['cubes'].items():
    if c['status'] != 'certified': continue
    d = os.path.join(W, c['certdir']); s = stamp(d)
    prev = cache.get(i) if (cache.get(i) or {}).get('stamp') == s and (cache.get(i) or {}).get('certdir') == c['certdir'] else None
    try:
        r = check(c, prev)
    except Exception as e:                                              # a missing or broken file means: not counted
        r = {'ok': False, 'bad': [f'exception {type(e).__name__}: {e}'], 'checks': {}, 'info': {}}
    r['stamp'] = s; r['certdir'] = c['certdir']; res[i] = r
    print(i, 'OK' if r['ok'] else f'NOT OK {r["bad"]}', flush=True)

leaves = [c for c in st['cubes'].values() if c['status'] != 'split']
vs = sorted({s for c in st['cubes'].values() for s, _ in c['lits']})
# certified cubes: literals as recorded in verify.json (equal to the plan by check 'cube_matches_plan')
cert = []
for i, r in res.items():
    if r['ok']:
        cert.append([tuple(x) for x in json.load(open(os.path.join(W, r['certdir'], 'verify.json')))['cube']])
base = list(itertools.product((1, 0), repeat=6))
tree_ok = all(c['status'] != 'split' or (len(c['children']) == 2 and all(ch in st['cubes'] for ch in c['children'])
              and {tuple(map(tuple, st['cubes'][ch]['lits'])) for ch in c['children']} == {tuple(map(tuple, c['lits'] + [[c['split_on'], b]])) for b in (1, 0)})
              for c in st['cubes'].values())
cover = {'states': vs, 'assignments': 2 ** len(vs), 'leaves': len(leaves),
         'leaf_uncovered': uncovered([[tuple(x) for x in c['lits']] for c in leaves], vs),
         'roots_are_64_patterns': sorted(tuple(b for _, b in c['lits']) for c in st['cubes'].values() if c['depth'] == 0) == sorted(base)
                                  and all([s for s, _ in c['lits'][:6]] == SPLIT for c in st['cubes'].values()),
         'split_children_ok': tree_ok,
         'certified_counted': len(cert), 'certified_uncovered': uncovered(cert, vs) if cert else 2 ** len(vs),
         'certified_measure_of_64': sum(2 ** (6 - len(cb)) for cb in cert)}    # a cube with k literals = 2^(6-k) of the 64 base cubes
print(json.dumps(cover))
json.dump({'status_updated': st.get('updated'), 'final': st.get('final'), 'cubes': res, 'cover': cover}, open(out + '.tmp', 'w'), indent=1)
os.replace(out + '.tmp', out)
print('CHK_DONE', sum(r['ok'] for r in res.values()), 'ok of', len(res))
