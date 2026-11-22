#!/usr/bin/env python3
"""post.py -- reviewer rv4, own code (22 Nov 2026). Verdicts from out/runs.tsv (run.sh) and out/expected.json
(prep.py). Writes out/summary.json. Reads no file of a running unit."""
import json, re, os, collections

V = '/home/jay/research/data/formalize-20261122/n66enc-recheck/verify'
FROZEN = '98d121bad04264221de66e583db0df08f4431d1093b4b7a05114316accccaa46'
CLAIMED = {'eager': '27b6b91009e6b782d051dba0bedfbdecd5e309acb79de9f2182dcd5f74007ff4',
           'full131': 'f9620834edd34b727d63d17ccf455629af64b78df49679b44c0f017df29bf82c',
           'negfull': 'b694e6a4d5d0cd822d18acadcbf4c9b8ffe2914121711d0faf1034356099de31',
           'negtrim': '7b4e6eb2f79acbd783b5bbc3396681a486fdde23f082b36ceef1b229a6d59dda'}
COLS = ['name', 'time', 'exe_sha', 'rc', 'rss_kb', 'wall', 'printed_sha', 'lines', 'bytes', 'cmprc', 'cmp',
        'ref_sha', 'stderr', 'anon_kb', 'pipestatus', 'gate']
MEMMAX_KIB = 3000 * 1024


def load_runs():
    R = {}
    if os.path.exists(V + '/out/runs.tsv'):
        for ln in open(V + '/out/runs.tsv'):
            f = ln.rstrip('\n').split('\t')
            assert len(f) == len(COLS), ln
            r = dict(zip(COLS, f))
            tf = V + '/tmp/' + r['name'].replace(':', '_') + '/time'
            r['signal'] = 'terminated by signal' in open(tf).read() if os.path.exists(tf) else None
            R[r['name']] = r
    return R


def ok_run(r):
    return r['rc'] == '0' and r['signal'] is False and r['exe_sha'] == FROZEN


def main():
    X = json.load(open(V + '/out/expected.json'))
    L = X['leaves']
    R = load_runs()
    S = {'runs': len(R), 'exe_sha_all_frozen': all(r['exe_sha'] == FROZEN for r in R.values())}
    if os.path.exists(V + '/out/exe_hashes.tsv'):
        S['exe_hashes'] = [ln.rstrip('\n').split('\t') for ln in open(V + '/out/exe_hashes.tsv')]

    # leaf map
    if 'leaves' in R:
        r = R['leaves']
        got = [ln.split() for ln in open(V + '/tmp/leaves/stdout') if ln.strip()]
        diffs = []
        for i, rec in enumerate(L):
            want = [str(i)] + [f'{s}:{b}' for s, b in rec['lits']]
            if i >= len(got) or got[i] != want:
                diffs.append(i)
        S['leaves'] = {'run_ok': ok_run(r), 'lines': len(got), 'leaves_differing': diffs,
                       'perm': X['leafmap'], 'stderr': r['stderr'],
                       'verdict': 'MATCH' if ok_run(r) and len(got) == 132 and not diffs and
                       X['leafmap']['leaf_order_is_perm_of_certified'] else 'NOT_MATCH'}

    # eager
    if 'eager' in R:
        r, e = R['eager'], X['eager']
        conds = {'run_ok': ok_run(r), 'cmp_equal': r['cmprc'] == '0', 'bytes': int(r['bytes']) == e['segment_bytes'],
                 'lines': int(r['lines']) == e['E'], 'printed_eq_segment': r['printed_sha'] == e['segment_sha256'],
                 'eq_claimed': r['printed_sha'] == CLAIMED['eager'], 'header_ok': e['header'] == e['header_expected'],
                 'stderr_empty': r['stderr'] == ''}
        S['eager'] = {'conds': conds, 'printed_sha': r['printed_sha'], 'bytes': r['bytes'], 'lines': r['lines'],
                      'rss_kb': r['rss_kb'], 'verdict': 'MATCH' if all(conds.values()) else 'NOT_MATCH'}

    def full_check(i, r):
        rec = L[i]
        rs = set(rec['full_sha'].values())
        fresh = r['printed_sha'] == r['ref_sha'] or (i != 131 and r['ref_sha'] == '-' and r['cmprc'] == '0')
        return {'run_ok': ok_run(r), 'cmp_equal': r['cmprc'] == '0', 'printed_eq_fresh': fresh,
                'recorded_agree': len(rs) == 1, 'printed_eq_recorded': r['printed_sha'] in rs and len(rs) == 1,
                'bytes': int(r['bytes']) == rec['layout']['cnf_bytes'] == rec['cert_cnf_bytes_stat'],
                'lines': int(r['lines']) == rec['layout']['clauses'] + 1,
                'stderr': r['stderr'] == rec['expected_full_stderr']}

    if 'full:131' in R:
        c = full_check(131, R['full:131'])
        c['eq_claimed'] = R['full:131']['printed_sha'] == CLAIMED['full131']
        c['py_fresh_eq'] = X['eager']['cert_cnf_sha256_fresh_py'] == R['full:131']['printed_sha']
        S['full131'] = {'conds': c, 'stderr': R['full:131']['stderr'], 'rss_kb': R['full:131']['rss_kb'],
                        'ctl': X['ctl'], 'verdict': 'MATCH' if all(c.values()) else 'NOT_MATCH'}

    # trims
    T = {}
    for rec in L:
        n = f"trim:{rec['i']}"
        if n not in R:
            continue
        r = R[n]
        rs = set(v for v in rec['trim_sha'].values())
        m = re.fullmatch(r'leaf (\d+) \[(.*)\] clauses (\d+)', r['stderr'])
        ncl = set(rec['trim_clauses'].values())
        conds = {'run_ok': ok_run(r), 'cmp_equal': r['cmprc'] == '0', 'printed_eq_fresh': r['printed_sha'] == r['ref_sha'],
                 'four_records_present': None not in rs and rec['md_entries'] >= 1,
                 'printed_eq_records': len(rs) == 1 and r['printed_sha'] in rs,
                 'bytes_eq_stat': int(r['bytes']) == rec['trim_bytes_stat'],
                 'stderr_leaf': bool(m) and int(m.group(1)) == rec['i'] and
                 m.group(2) == ' '.join(f'{s}:{b}' for s, b in rec['lits']),
                 'clauses_eq_campaign': bool(m) and len(ncl) == 1 and int(m.group(3)) in ncl,
                 'lines_eq_clauses_plus_1': bool(m) and int(r['lines']) == int(m.group(3)) + 1}
        T[rec['i']] = {'conds': conds, 'sha': r['printed_sha'], 'bytes': int(r['bytes']),
                       'verdict': 'MATCH' if all(conds.values()) else 'NOT_MATCH'}
    if T:
        groups = collections.defaultdict(list)
        for i, t in T.items():
            groups[t['sha']].append(i)
        shared = {s: sorted(v) for s, v in groups.items() if len(v) > 1}
        up = sorted(rec['i'] for rec in L if rec['up_refuted'])
        S['trims'] = {'done': len(T), 'match': sum(t['verdict'] == 'MATCH' for t in T.values()),
                      'not_match': sorted(i for i, t in T.items() if t['verdict'] != 'MATCH'),
                      'failed_conds': {i: [k for k, v in t['conds'].items() if not v] for i, t in T.items()
                                       if t['verdict'] != 'MATCH'},
                      'distinct': len(groups), 'shared_groups': {s: {'leaves': v, 'bytes': T[v[0]]['bytes']}
                                                                  for s, v in shared.items()},
                      'up_refuted_leaves_campaign': up, 'total_bytes': sum(t['bytes'] for t in T.values()),
                      'max_rss_kb': max(int(R[f'trim:{i}']['rss_kb']) for i in T)}

    # controls
    if 'negfull:131' in R:
        r = R['negfull:131']
        S['negfull'] = {'rc': r['rc'], 'stderr': r['stderr'], 'cmp': r['cmp'], 'cmprc': r['cmprc'],
                        'printed_sha': r['printed_sha'], 'bytes': r['bytes'], 'lines': r['lines'],
                        'eq_worker_sha': r['printed_sha'] == CLAIMED['negfull'],
                        'differs_from_recorded': r['printed_sha'] != CLAIMED['full131'],
                        'ok': r['rc'] == '0' and r['cmprc'] == '1' and r['printed_sha'] != CLAIMED['full131']}
    if 'negtrim:131' in R:
        r = R['negtrim:131']
        S['negtrim'] = {'rc': r['rc'], 'stderr': r['stderr'], 'cmp': r['cmp'], 'cmprc': r['cmprc'],
                        'printed_sha': r['printed_sha'], 'bytes': r['bytes'], 'lines': r['lines'],
                        'eq_worker_sha': r['printed_sha'] == CLAIMED['negtrim'],
                        'differs_from_recorded': r['printed_sha'] != L[131]['trim_sha']['campaign_status'],
                        'ok': r['rc'] == '0' and r['cmprc'] == '1' and
                        r['printed_sha'] != L[131]['trim_sha']['campaign_status']}

    # FULL extension
    F = {}
    for i in range(131):
        n = f'full:{i}'
        if n in R:
            c = full_check(i, R[n])
            F[i] = 'MATCH' if all(c.values()) else 'NOT_MATCH:' + ','.join(k for k, v in c.items() if not v)
    S['fullext'] = {'done': len(F), 'match': sum(v == 'MATCH' for v in F.values()),
                    'first27_done': sum(i in F for i in range(27)),
                    'first27_match': sum(F.get(i) == 'MATCH' for i in range(27)),
                    'not_match': {i: v for i, v in F.items() if v != 'MATCH'},
                    'out_of_scope': [rec['i'] for rec in L if not rec['full_in_scope']],
                    'inputs_same_as_131': sum(rec['act_same_as_131'] and rec['rows_same_as_131'] for rec in L)}

    # memory
    rss = {n: int(r['rss_kb']) for n, r in R.items() if r['rss_kb'].isdigit()}
    anon = {n: int(r['anon_kb']) for n, r in R.items() if r['anon_kb'].isdigit()}
    if rss:
        mr, ma = max(rss, key=rss.get), max(anon, key=anon.get)
        S['memory'] = {'max_exe_rss_kb': rss[mr], 'at': mr, 'pct_of_3000MiB': round(100 * rss[mr] / MEMMAX_KIB, 2),
                       'max_unit_anon_kb_sampled': anon[ma], 'anon_at': ma,
                       'anon_pct_of_3000MiB': round(100 * anon[ma] / MEMMAX_KIB, 2)}
    json.dump(S, open(V + '/out/summary.json', 'w'), indent=1)
    print(json.dumps({k: (v.get('verdict', v) if isinstance(v, dict) and 'verdict' in v else v)
                      for k, v in S.items() if k not in ('exe_hashes',)}, default=str)[:3000])


if __name__ == '__main__':
    main()
