#!/usr/bin/env python3
"""prep.py -- reviewer rv4, own code (22 Nov 2026). Expected values and inputs for the n66enc-recheck review.

Reads the campaign files (read-only) and the encoder's leaf_order.txt / desc paths; writes only under verify/:
  out/expected.json  per-leaf expected values from four independent hash records, layout and state files
  out/plan.tsv       one exe run per line: name, reference, cmp options ('-' = none), exe arguments
  ctl/...            FULL inputs re-derived here (act from the state file, rows from mono/rows_1832.json),
                     negative-control inputs
Must finish before the first exe start (it parses 11.5 MB state files)."""
import hashlib, json, os, re, sys

V = '/home/jay/research/data/formalize-20261122/n66enc-recheck/verify'
W = '/home/jay/research/data/n66-20261113'
C14 = W + '/p2/c14'
ENC = '/home/jay/research/data/formalize-20261122/n66enc'
WORKER = '/home/jay/research/data/formalize-20261122/n66enc-recheck'
STATUS_MD = ('/home/jay/research/lean/erdos-szekeres-lean/archive/es7-2026-10-19/results/N66N20261113/'
             'cubes20261115/STATUS_campaign.md')
HEX = re.compile(r'^[0-9a-f]{64}$')
EXT_FIRST = list(range(0, 27))          # leaves of the worker's partial extension claim, checked first


def sha_file(p, start=0, length=None):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        f.seek(start)
        left = length
        while left is None or left > 0:
            b = f.read(1 << 20 if left is None else min(1 << 20, left))
            if not b:
                break
            h.update(b)
            if left is not None:
                left -= len(b)
    return h.hexdigest()


def sha_text(s):
    return hashlib.sha256(s.encode()).hexdigest()


def act_text(act):
    return ''.join(f'{a} {b} {c} {d}\n' for a, b, c, d in act)


def rows_text(rows):
    return ''.join(' '.join(map(str, r)) + '\n' for r in rows)


def need_hex(x, what):
    assert isinstance(x, str) and HEX.match(x), (what, x)
    return x


def eager_segment(cnf, n_eager):
    """Byte range of clause lines 1..n_eager (file lines 2..n_eager+1) of a DIMACS file, found by reading it."""
    with open(cnf, 'rb') as f:
        header = f.readline()
        H = len(header)
        lines, S = 0, 0
        while lines < n_eager:
            ln = f.readline()
            assert ln.endswith(b'\n'), 'file ended inside the eager range'
            S += len(ln)
            lines += 1
    return header.decode(), H, S


def main():
    os.makedirs(V + '/out', exist_ok=True)
    os.makedirs(V + '/ctl', exist_ok=True)
    cs_path = C14 + '/campaign_status.json'
    lo_path = ENC + '/tools/leaf_order.txt'
    inputs = {p: sha_file(p) for p in (cs_path, lo_path, STATUS_MD)}
    cs = json.load(open(cs_path))
    cubes = cs['cubes']
    order = [ln.strip() for ln in open(lo_path) if ln.strip()]
    certified = sorted(k for k, v in cubes.items() if v.get('status') == 'certified')
    leafmap = {'leaf_order_len': len(order), 'leaf_order_distinct': len(set(order)), 'certified': len(certified),
               'leaf_order_is_perm_of_certified': sorted(order) == certified}

    md = {}                                        # STATUS_campaign.md table: id -> trim hashes on certified rows
    for line in open(STATUS_MD):
        cells = [c.strip() for c in line.strip().strip('|').split('|')]
        if len(cells) >= 8 and cells[3] == 'certified':
            m = re.search(r'trim\.cnf ([0-9a-f]{64})', cells[7])
            if m:
                md.setdefault(cells[0], []).append(m.group(1))

    ref = None                                     # hhhhhh (leaf 131) values, the FULL reference inputs
    leaves = []
    plan_full = {}
    for i, cid in enumerate(order):
        cu = cubes[cid]
        cd = W + '/' + cu['certdir']
        cj = json.load(open(cd + '/cert.json'))
        vj = json.load(open(cd + '/verify.json'))
        lj = json.load(open(cd + '/layout.json'))
        st_path = lj['state']
        st = json.load(open(st_path))
        act = st['activated']
        rows_layout = lj['row_list']
        rf = json.load(open(W + '/' + st['rows_file']))
        rows_rf = [sorted(s) for s, d in rf if d == 1 and all(0 <= x < 70 for x in s)]
        md_h = md.get(cid, [])
        rec = {
            'i': i, 'cid': cid, 'certdir': cd, 'status': cu.get('status'), 'up_refuted': cu.get('up_refuted'),
            'lits': cu['lits'],
            'trim_sha': {'campaign_status': need_hex(cu['trim_cnf_sha256'], 'cs'),
                         'cert_json': need_hex(cj['trim_cnf_sha256'], 'cj'),
                         'verify_json': need_hex(vj['trim_cnf_sha256'], 'vj'),
                         'STATUS_campaign_md': need_hex(md_h[0], 'md') if len(set(md_h)) == 1 else None},
            'md_entries': len(md_h),
            'trim_clauses': {'campaign_status': cu.get('trim_cnf_clauses'), 'cert_json': cj.get('trim_cnf_clauses'),
                             'verify_json': vj.get('clauses')},
            'trim_bytes_stat': os.stat(cd + '/trim.cnf').st_size,
            'full_sha': {'cert_json': need_hex(cj['full_cnf_sha256'], 'cj full'),
                         'campaign_status': need_hex(cu['full_cnf_sha256'], 'cs full'),
                         'layout_json': need_hex(lj['cnf_sha256'], 'layout')},
            'cert_cnf_bytes_stat': os.stat(cd + '/cert.cnf').st_size,
            'layout': {k: lj[k] for k in ('L', 'vars', 'clauses', 'cnf_bytes', 'activated_quadruples', 'eager',
                                           'quad', 'units', 'rows', 'card', 'sb')},
            'layout_cube_eq_lits': lj['cube'] == cu['lits'],
            'cert_json_cube_eq_lits': cj['cube'] == cu['lits'],
            'state_path': st_path, 'state_sha256': sha_file(st_path),
            'state_cube_eq_lits': st.get('cube') == cu['lits'],
            'state_L': st.get('L'), 'n_act': len(act), 'act_distinct': len(set(map(tuple, act))) == len(act),
            'act_sha256': sha_text(act_text(act)),
            'n_rows_layout': len(rows_layout), 'rows_layout_sha256': sha_text(rows_text(rows_layout)),
            'rows_file': st['rows_file'], 'rows_file_eq_layout': rows_rf == rows_layout,
            'cnf_bytes_eq_stat': lj['cnf_bytes'] == os.stat(cd + '/cert.cnf').st_size,
            'expected_full_stderr': f"leaf {i} clauses {lj['clauses']} act {len(act)} rows {len(rows_layout)} bad 0",
        }
        rec['_W'], rec['_sb'] = lj['W'], lj['sb_pairs']
        if cid == 'hhhhhh':
            ref = {'act': act, 'rows_rf': rows_rf, 'rec': rec}
        leaves.append(rec)
        del st, act, rf, rows_rf, rows_layout, lj

    assert ref is not None and ref['rec']['i'] == 131
    r131 = ref['rec']
    # FULL inputs for leaf 131, re-derived: act from the state file, rows from the rows file (checked = layout)
    os.makedirs(V + '/ctl/hhhhhh', exist_ok=True)
    act_p, rows_p = V + '/ctl/hhhhhh/act.txt', V + '/ctl/hhhhhh/rows.txt'
    open(act_p, 'w').write(act_text(ref['act']))
    open(rows_p, 'w').write(rows_text(ref['rows_rf']))
    neg_act = V + '/ctl/neg_act131.txt'
    open(neg_act, 'w').write(act_text(ref['act'][:-1]))
    desc131 = open(ENC + '/desc/131.txt').read()
    first = desc131.split('\n', 1)[0]
    m = re.fullmatch(r'E (\d+)', first)
    assert m, first
    neg_desc = V + '/ctl/neg_desc131.txt'
    open(neg_desc, 'w').write(f'E {int(m.group(1)) + 1}' + desc131[len(first):])
    ctl = {'act131': act_p, 'act131_sha256': sha_file(act_p), 'rows131': rows_p, 'rows131_sha256': sha_file(rows_p),
           'neg_act131_sha256': sha_file(neg_act), 'neg_desc131_sha256': sha_file(neg_desc),
           'neg_desc_first_line': [first, f'E {int(m.group(1)) + 1}'],
           'compare': {}}
    for name, p in (('worker_act', WORKER + '/ctl/hhhhhh/act.txt'), ('worker_rows', WORKER + '/ctl/hhhhhh/rows.txt'),
                    ('encoder_act', ENC + '/ctl/act_hhhhhh.txt'), ('encoder_rows', ENC + '/ctl/rows1832.txt'),
                    ('worker_neg_desc', WORKER + '/ctl/neg_desc131.txt')):
        ctl['compare'][name] = sha_file(p) if os.path.exists(p) else None

    # Scope of a FULL run of leaf i with the exe (it hard-wires L, nvHeader, W and the SB pairs of hhhhhh)
    for rec in leaves:
        sc = (rec['layout']['L'] == r131['layout']['L'] and rec['layout']['vars'] == r131['layout']['vars'] and
              rec['_W'] == list(range(70)) and rec['_sb'] == r131['_sb'] and rec['layout_cube_eq_lits'] and
              rec['state_cube_eq_lits'] and rec['n_act'] == rec['layout']['activated_quadruples'] and
              rec['act_distinct'] and rec['cnf_bytes_eq_stat'])
        rec['full_in_scope'] = sc
        rec['act_same_as_131'] = rec['act_sha256'] == r131['act_sha256']
        rec['rows_same_as_131'] = rec['rows_layout_sha256'] == r131['rows_layout_sha256']
        del rec['_W'], rec['_sb']
    # leaves whose inputs differ from hhhhhh's get their own files (none expected; written only if needed)
    for rec in leaves:
        if rec['i'] == 131 or not rec['full_in_scope']:
            continue
        a, r = act_p, rows_p
        if not (rec['act_same_as_131'] and rec['rows_same_as_131']):
            d = V + '/ctl/' + rec['cid']
            os.makedirs(d, exist_ok=True)
            st = json.load(open(rec['state_path']))
            lj = json.load(open(rec['certdir'] + '/layout.json'))
            a, r = d + '/act.txt', d + '/rows.txt'
            open(a, 'w').write(act_text(st['activated']))
            open(r, 'w').write(rows_text(lj['row_list']))
            del st, lj
        plan_full[rec['i']] = (a, r)

    # EAGER: layout eager = [1, E] means clause lines 2..E+1 of cert.cnf (line 1 = header)
    cnf131 = r131['certdir'] + '/cert.cnf'
    E0, E = r131['layout']['eager']
    assert E0 == 1
    header, H, S = eager_segment(cnf131, E)
    eager = {'cnf': cnf131, 'E': E, 'header': header, 'header_bytes': H, 'segment_bytes': S,
             'header_expected': f"p cnf {r131['layout']['vars']} {r131['layout']['clauses']}\n",
             'segment_sha256': sha_file(cnf131, H, S), 'cert_cnf_sha256_fresh_py': sha_file(cnf131)}
    inputs[cnf131] = eager['cert_cnf_sha256_fresh_py']
    for p in (r131['certdir'] + '/layout.json', r131['certdir'] + '/cert.json', r131['state_path'],
              W + '/' + 'mono/rows_1832.json'):
        inputs[p] = sha_file(p)

    json.dump({'inputs': inputs, 'leafmap': leafmap, 'ctl': ctl, 'eager': eager, 'leaves': leaves},
              open(V + '/out/expected.json', 'w'), indent=1)

    # plan: required pieces first, then controls, then the FULL extension (0..26 first, then the rest)
    P = []
    P.append(('leaves', '-', '-', 'leaves'))
    P.append(('eager', cnf131, f'--ignore-initial=0:{H} --bytes={S}', 'eager'))
    P.append(('full:131', cnf131, '-', f'full 131 {act_p} {rows_p}'))
    for rec in leaves:
        P.append((f"trim:{rec['i']}", rec['certdir'] + '/trim.cnf', '-', f"trim {rec['i']} {ENC}/desc/{rec['i']}.txt"))
    P.append(('negfull:131', cnf131, '-', f'full 131 {neg_act} {rows_p}'))
    P.append(('negtrim:131', r131['certdir'] + '/trim.cnf', '-', f'trim 131 {neg_desc}'))
    rest = [i for i in range(131) if i not in EXT_FIRST]
    for i in EXT_FIRST + rest:
        if i in plan_full:
            a, r = plan_full[i]
            # '--' = no fresh file hash for extension leaves (implied by cmp equality + printed hash)
            P.append((f'full:{i}', leaves[i]['certdir'] + '/cert.cnf', '--', f'full {i} {a} {r}'))
    with open(V + '/out/plan.tsv', 'w') as f:
        for row in P:
            assert all('\t' not in x for x in row)
            f.write('\t'.join(row) + '\n')
    print(json.dumps({'leaves': len(leaves), 'plan': len(P), 'leafmap': leafmap,
                      'full_in_scope': sum(r['full_in_scope'] for r in leaves),
                      'act_same_as_131': sum(r['act_same_as_131'] for r in leaves),
                      'rows_same_as_131': sum(r['rows_same_as_131'] for r in leaves),
                      'eager': {k: eager[k] for k in ('E', 'header_bytes', 'segment_bytes', 'segment_sha256')}}))


if __name__ == '__main__':
    main()
