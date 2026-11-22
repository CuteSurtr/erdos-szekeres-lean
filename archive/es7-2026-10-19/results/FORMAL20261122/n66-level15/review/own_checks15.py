"""Reviewer's own checks for item n66-level15 (slot lrv3). Written fresh for this review; none of the worker's or the
level-14 reviewer's scripts are imported or copied. Read-only on every input; writes only review/own_checks15.json,
review/leafmap15.tsv and review/own_checks15.out (stdout).

A. Leaves: the 105 leaves dumped from the olean (N66E15.leaves105, ReviewL15.lean) against campaign_status.json
   (bijection with the certified cubes, literal lists equal in order), then per certdir: cert.json, verify.json,
   cake.out, cake.err, cake_attempts.json, mtimes, and the independent verifier's records (vfy15/summary.json and
   vfy15/cake/<id>.*). The leaf map written here (leaf index -> cube id -> certdir) drives the own E1 re-run.
B. Rows: R0_15 dumped from the olean = embedded rowsText = lean/N66E15/data/rows_used15.txt; structure; R0_15 = union
   of the 105 used_rows.json; every row has a demand-1 justification in some tcert/justification.json.
C. Positive controls on real point sets (exact integers): states computed from the Lean definitions (EndingPath ->
   rank -> labels -> column -> index in stateList); validated on the record's ETV 50-point set (etv668.json); class
   membership (no 6-cap, no 6-cup, no 5-cap and 5-cup with common endpoints); no R0_15 row fully occupied by the ETV
   set, its three reflections, or random subsets.
"""
import hashlib, itertools, json, os, random, re, sys

RV = '/home/jay/research/data/formalize-20261122/n66-level15/review/'
D = '/home/jay/research/data/formalize-20261122/n66-level15/'
W = '/home/jay/research/data/n66-20261113/'
out = {}
fails = []


def check(name, cond, detail=None):
    if not cond:
        fails.append(name if detail is None else f'{name}: {detail}')
    return cond


def sha(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


# ---------------------------------------------------------------- A. leaves and records
st_raw = open(W + 'p2/c15/campaign_status.json', 'rb').read()
out['campaign_status_sha256'] = hashlib.sha256(st_raw).hexdigest()
check('campaign pin', out['campaign_status_sha256'] == '4802dc9a946cefa3b855b8c495becc0fb33491a89e5472c9722ccb9d0c8138f5')
st = json.loads(st_raw)
cubes = st['cubes']
cert = {k: v for k, v in cubes.items() if v['status'] == 'certified'}
out['campaign'] = {'cubes': len(cubes), 'certified': len(cert),
                   'split': sum(v['status'] == 'split' for v in cubes.values()),
                   'other_status': sorted({v['status'] for v in cubes.values()} - {'certified', 'split'}),
                   'final': st.get('final'), 'cover': st.get('cover')}
check('campaign final', st.get('final') is True)
check('campaign 105 certified', len(cert) == 105)

leaves = []
for line in open(RV + 'dump_leaves105.txt').read().splitlines():
    if line.strip():
        leaves.append(tuple((int(a), int(b)) for a, b in (t.split(':') for t in line.split())))
out['dump_leaves'] = len(leaves)
check('105 leaves dumped', len(leaves) == 105)
check('leaves distinct', len(set(leaves)) == len(leaves))
by_lits = {}
for cid, v in cert.items():
    key = tuple((int(s), int(b)) for s, b in v['lits'])
    check('certified lits distinct', key not in by_lits, cid)
    by_lits[key] = cid
leafmap = []
for i, lv in enumerate(leaves):
    cid = by_lits.get(lv)
    check('leaf matches a certified cube', cid is not None, f'leaf {i} {lv}')
    leafmap.append((i, cid, cert[cid]['certdir'] if cid else None))
matched = [c for _, c, _ in leafmap if c]
check('bijection leaves <-> certified cubes', sorted(matched) == sorted(cert))
with open(RV + 'leafmap15.tsv', 'w') as f:
    for i, cid, cd in leafmap:
        f.write(f'{i}\t{cid}\t{cd}\n')
# the worker's map (untrusted; compared only)
wl = [l.split() for l in open(D + 'tools/leaf_order15.txt').read().splitlines() if l.strip()]
out['worker_leaf_order_equal'] = [x[-1] for x in wl] == [c for _, c, _ in leafmap]

sbdump = [[int(a), int(b)] for a, b in (l.split() for l in open(RV + 'dump_sbPairs.txt').read().splitlines() if l.strip())]
out['sbPairs_len'] = len(sbdump)

vfy_raw = open(W + 'vfy15/summary.json', 'rb').read()
out['vfy15_summary_sha256'] = hashlib.sha256(vfy_raw).hexdigest()
check('vfy15 pin', out['vfy15_summary_sha256'] == '87b82b7a0029496176bdffdeabb87d95bd7f03eba844e576f31b826084927181')
vfy = {e['id']: e for e in json.loads(vfy_raw)}
check('vfy15 has 105 entries', len(vfy) == 105 and set(vfy) == set(cert))

per = []
cmd_re = re.compile(r'Command being timed: "/home/jay/\.local/bin/cake_lpr [^"]*? (\S+/trim\.cnf) (\S+/trim\.lrat)"')
for i, cid, cdr in leafmap:
    if cid is None:
        continue
    v = cert[cid]
    cd = W + cdr
    r = {'i': i, 'id': cid}
    cj = json.load(open(cd + '/cert.json'))
    vj = json.load(open(cd + '/verify.json'))
    lits = [[int(s), int(b)] for s, b in v['lits']]
    r['cert_ok'] = (cj.get('cube') == lits and cj.get('budget') == 15 and cj.get('bound') == 54
                    and cj.get('holes_at_least') == 16 and cj.get('W_size') == 70
                    and cj.get('trim_cnf_sha256') == v['trim_cnf_sha256'] and cj.get('trim_lrat_sha256') == v['trim_lrat_sha256']
                    and cj.get('trim_cnf_clauses') == v['trim_cnf_clauses'] and cj.get('ALL_OK') is True
                    and cj.get('cake_lpr') == 's VERIFIED UNSAT' and cj.get('sb_pairs') == sbdump
                    and cj.get('certdir', '').endswith(cdr))
    fv = cj.get('final_verify66') or {}
    r['fv66'] = {'bad': fv.get('bad'), 'rows_match': fv.get('rows_match'),
                 'templates': [fv.get('templates_verified'), fv.get('templates')],
                 'cores': [fv.get('cores_verified'), fv.get('cores')]}
    r['verify_ok'] = (vj.get('trim_cnf_sha256') == v['trim_cnf_sha256'] and vj.get('trim_lrat_sha256') == v['trim_lrat_sha256']
                      and vj.get('clauses') == v['trim_cnf_clauses'] and vj.get('header_vars') == 1647847
                      and isinstance(vj.get('max_var'), int) and vj['max_var'] <= 1647847 and vj.get('vars_ok') is True
                      and vj.get('budget') == 15 and vj.get('cube') == lits and vj.get('sb_pairs') == sbdump
                      and vj.get('unclassified') == 0 and vj.get('ALL_OK') is True and vj.get('cake_lpr') == 's VERIFIED UNSAT')
    r['cake_out_exact'] = open(cd + '/cake.out', 'rb').read() == b's VERIFIED UNSAT\n'
    err = open(cd + '/cake.err').read()
    runs = cmd_re.findall(err)
    r['cake_cmd'] = (len(runs) == 1 and runs[0] == (cdr + '/trim.cnf', cdr + '/trim.lrat')
                     and err.count('Command being timed') == 1 and 'Exit status: 0' in err)
    att = json.load(open(cd + '/cake_attempts.json'))
    r['cake_attempts'] = [[a.get('heap'), a.get('verified')] for a in att]
    r['cake_attempt_ok'] = len(att) >= 1 and att[-1].get('verified') is True
    m_trim = os.stat(cd + '/trim.cnf').st_mtime
    m_cake = os.stat(cd + '/cake.out').st_mtime
    m_cert = os.stat(cd + '/cert.json').st_mtime
    r['mtime_order'] = m_trim <= m_cake <= m_cert
    e = vfy[cid]
    r['vfy15_ok'] = (e.get('certdir') == cdr and e.get('cake_line') == ['s VERIFIED UNSAT'] and e.get('cake_ok') is True
                     and e.get('trim_cnf_sha') == v['trim_cnf_sha256'] and e.get('trim_lrat_sha') == v['trim_lrat_sha256']
                     and e.get('sub_ok') is True and e.get('fpu_ok') is True and e.get('gen_ok') is True
                     and e.get('rows_ok') is True and e.get('kinds_match') is True)
    # the verifier's own raw cake records (not its summary)
    vc = W + 'vfy15/cake/' + cid
    try:
        vlines = open(vc + '.cake.out').read().splitlines()
        vsha = dict((os.path.basename(l.split()[1]), l.split()[0]) for l in open(vc + '.sha256') if l.strip())
        vstatus = open(vc + '.status').read().split()
        verr = open(vc + '.cake.err').read()
        r['vfy15_raw_ok'] = (vlines == ['s VERIFIED UNSAT'] and vsha.get('trim.cnf') == v['trim_cnf_sha256']
                             and vsha.get('trim.lrat') == v['trim_lrat_sha256'] and vstatus[0] == 'cake_rc=0'
                             and 'Exit status: 0' in verr and (cdr + '/trim.cnf') in verr)
        r['vfy15_lrat_from'] = vstatus[1] if len(vstatus) > 1 else None
    except Exception as ex:  # noqa: BLE001
        r['vfy15_raw_ok'] = False
        r['vfy15_raw_err'] = repr(ex)
    r['up_refuted'] = bool(v.get('up_refuted'))
    per.append(r)
    for k in ('cert_ok', 'verify_ok', 'cake_out_exact', 'cake_cmd', 'cake_attempt_ok', 'mtime_order', 'vfy15_ok', 'vfy15_raw_ok'):
        check(k, r[k] is True, cid)
out['per_leaf_counts'] = {k: sum(1 for r in per if r.get(k) is True) for k in
                          ('cert_ok', 'verify_ok', 'cake_out_exact', 'cake_cmd', 'cake_attempt_ok', 'mtime_order',
                           'vfy15_ok', 'vfy15_raw_ok')}
out['fv66_bad_nonzero'] = [r['id'] for r in per if r['fv66']['bad'] not in (0, None)]
out['cake_attempts_multi'] = [[r['id'], r['cake_attempts']] for r in per if len(r['cake_attempts']) > 1]
out['vfy15_lrat_from'] = sorted({str(r.get('vfy15_lrat_from')) for r in per})
out['up_refuted'] = [r['id'] for r in per if r['up_refuted']]
out['trim_sha_distinct'] = len({cert[r['id']]['trim_cnf_sha256'] for r in per})

# ---------------------------------------------------------------- B. rows
f_rows = open(D + 'lean/N66E15/data/rows_used15.txt', 'rb').read()
d_rows = open(RV + 'dump_R0_15.txt', 'rb').read()
d_text = open(RV + 'dump_rowsText.txt', 'rb').read()
out['rows_file_sha256'] = hashlib.sha256(f_rows).hexdigest()
out['rows_dump_eq_file'] = d_rows == f_rows
out['rowsText_eq_file'] = d_text == f_rows
check('R0_15 dump = rows_used15.txt', d_rows == f_rows)
check('rowsText = rows_used15.txt', d_text == f_rows)
R = [tuple(int(x) for x in l.split()) for l in d_rows.decode().splitlines() if l.strip()]
out['R0_15_rows'] = len(R)
check('10859 rows', len(R) == 10859)
check('rows distinct', len(set(R)) == len(R))
struct_bad = [T for T in R if not T or any(a >= b for a, b in zip(T, T[1:])) or not all(0 <= s < 70 for s in T)
              or max(T) < 2]
out['rows_structure_bad'] = len(struct_bad)
check('rows sorted, nonempty, in range, contain a state >= 2', not struct_bad)
out['row_len_min_max'] = [min(map(len, R)), max(map(len, R))]
used = set()
used_demands = set()
just = {}
just_missing = []
for i, cid, cdr in leafmap:
    if cid is None:
        continue
    cd = W + cdr
    for e in json.load(open(cd + '/used_rows.json')):
        used.add(tuple(e[0])); used_demands.add(e[1])
    jp = cd + '/tcert/justification.json'
    if not os.path.exists(jp):
        just_missing.append([cid, len(json.load(open(cd + '/used_rows.json')))])
        continue
    for e in json.load(open(jp))['justifications']:
        just.setdefault(tuple(e['support']), set()).add((e.get('kind'), e.get('demand')))
out['used_rows_union'] = len(used)
out['used_rows_demands'] = sorted(used_demands)
out['R0_15_eq_union_used_rows'] = set(R) == used
check('R0_15 = union of used_rows.json', set(R) == used)
check('used_rows demand 1 only', used_demands == {1})
out['no_justification_file'] = just_missing
check('leaves without justification file use no row', all(n == 0 for _, n in just_missing))
unjust = [T for T in R if not any(d == 1 for _, d in just.get(T, ()))]
out['rows_without_demand1_justification'] = len(unjust)
check('every row justified at demand 1', not unjust)
kinds = {}
for T in R:
    for k in sorted({k for k, d in just.get(T, ()) if d == 1}):
        kinds[k] = kinds.get(k, 0) + 1
out['justification_kinds_per_row'] = kinds

# ---------------------------------------------------------------- C. real-set controls
# own stateList: nonincreasing 4-tuples over 0..4 sorted by (sum, tuple)
own_states = sorted((p for p in itertools.product(range(5), repeat=4) if p[0] >= p[1] >= p[2] >= p[3]),
                    key=lambda p: (sum(p), p))
dump_states = [tuple(int(x) for x in l.split()) for l in open(RV + 'dump_stateList.txt').read().splitlines() if l.strip()]
check('stateList dump = own sort', dump_states == own_states)
out['stateList_eq_own'] = dump_states == own_states
SIDX = {p: k for k, p in enumerate(own_states)}


def orient(p, q, r):
    return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])


def analyse(pts):
    """pts sorted by strictly increasing x. Returns (states, max cap path, max cup path, octagon?)."""
    n = len(pts)
    assert all(pts[i][0] < pts[i + 1][0] for i in range(n - 1)), 'x not strictly increasing'
    cup = {}
    for i, j, k in itertools.combinations(range(n), 3):
        o = orient(pts[i], pts[j], pts[k])
        assert o != 0, 'collinear triple'
        cup[i, j, k] = o > 0
    return analyse_colors(n, cup)


def analyse_colors(n, cup):
    # rank[color][u][v]: longest EndingPath (strictly increasing, consecutive triples of that color) ending at (u, v)
    rank = {False: [[0] * n for _ in range(n)], True: [[0] * n for _ in range(n)]}
    for v in range(n):
        for u in range(v):
            for col in (False, True):
                best = 2
                for t in range(u):
                    if cup[t, u, v] == col and rank[col][t][u] + 1 > best:
                        best = rank[col][t][u] + 1
                rank[col][u][v] = best
    states = []
    for v in range(n):
        colh = []
        for i in range(4):
            m = 0
            for u in range(v):
                cap_l, cup_l = rank[False][u][v] - 1, rank[True][u][v] - 1
                val = cup_l if i + 1 <= cap_l else 0
                m = max(m, val)
            colh.append(m)
        states.append(SIDX.get(tuple(colh), 70))   # List.idxOf: length (70) when absent
    mcap = max((rank[False][u][v] for v in range(n) for u in range(v)), default=0)
    mcup = max((rank[True][u][v] for v in range(n) for u in range(v)), default=0)
    # 5-paths from each start p: ends reachable by a 5-cap / a 5-cup with consecutive triples of one color
    octo = False
    for p in range(n):
        ends = {}
        for col in (False, True):
            L = {}
            for v in range(p + 1, n):
                L[p, v] = {2}
            for v in range(p + 1, n):
                for u in range(p + 1, v):
                    s = set()
                    for t in range(p, u):
                        if (t, u) in L and cup[t, u, v] == col:
                            s |= {x + 1 for x in L[t, u] if x + 1 <= 5}
                    if s:
                        L[u, v] = s
            ends[col] = {v for (u, v), s in L.items() if 5 in s}
        if ends[False] & ends[True]:
            octo = True
            break
    return states, mcap, mcup, octo


etv = json.load(open(W + 'etv668.json'))
P0 = [tuple(p) for p in etv['points']]
variants = {'id': P0,
            'x_reflect': sorted((-x, y) for x, y in P0),
            'y_reflect': [(x, -y) for x, y in P0],
            'xy_reflect': sorted((-x, -y) for x, y in P0)}
masks = []
for T in R:
    m = 0
    for s in T:
        m |= 1 << s
    masks.append(m)


def occ_mask(states):
    m = 0
    for s in states:
        if s < 70:
            m |= 1 << s
    return m


def full_rows(om):
    return sum(1 for m in masks if m & ~om == 0)


def tight_rows(om):
    return sum(1 for m in masks if bin(m & ~om).count('1') == 1)


def conj(p):
    return tuple(sum(1 for a in p if a >= j) for j in range(1, 5))


TAU = [SIDX[conj(p)] for p in own_states]
ctl = {}
cups_full = {}
for name, pts in variants.items():
    states, mcap, mcup, octo = analyse(pts)
    om = occ_mask(states)
    ctl[name] = {'n': len(pts), 'max_cap_path': mcap, 'max_cup_path': mcup, 'capcup55_octagon': octo,
                 'in_class': mcap <= 5 and mcup <= 5 and not octo, 'distinct_states': len(set(states)),
                 'states_absent_from_list': sum(1 for s in states if s >= 70),
                 'rows_fully_occupied': full_rows(om), 'rows_tight': tight_rows(om)}
    if name == 'id':
        ctl[name]['states_eq_etv668'] = states == etv['states']
        ctl[name]['holes_eq_etv668'] = sorted(set(range(70)) - set(states)) == sorted(etv['holes'])
        id_states = states
    if name == 'y_reflect':
        ctl[name]['states_eq_tau_of_id'] = states == [TAU[s] for s in id_states]
    check(f'{name} in class', ctl[name]['in_class'])
    check(f'{name} no row fully occupied', ctl[name]['rows_fully_occupied'] == 0)
check('own states = etv668.json states', ctl['id'].get('states_eq_etv668') is True)
check('own holes = etv668.json holes', ctl['id'].get('holes_eq_etv668') is True)
check('y-mirror states = tau of states', ctl['y_reflect'].get('states_eq_tau_of_id') is True)
out['controls'] = ctl

# random subsets (orientations inherited from the parent set, so they are configurations of the class too)
rng = random.Random(20261122)
nsub = int(os.environ.get('NSUB', '3000'))
viol = 0
tight_max = 0
sizes = []
pre = {}
for name, pts in variants.items():
    n = len(pts)
    pre[name] = {(i, j, k): orient(pts[i], pts[j], pts[k]) > 0 for i, j, k in itertools.combinations(range(n), 3)}
names = list(variants)
for it in range(nsub):
    name = names[it % 4]
    n0 = len(variants[name])
    k = rng.randint(8, n0 - 1)
    idx = sorted(rng.sample(range(n0), k))
    cupsub = {(a, b, c): pre[name][idx[a], idx[b], idx[c]] for a, b, c in itertools.combinations(range(k), 3)}
    states, mcap, mcup, octo = analyse_colors(k, cupsub)
    check('subset in class', mcap <= 5 and mcup <= 5 and not octo, f'{name} {idx}')
    om = occ_mask(states)
    fr = full_rows(om)
    if fr:
        viol += 1
        fails.append(f'subset violates {fr} rows: {name} {idx}')
    sizes.append(k)
out['random_subsets'] = {'count': nsub, 'seed': 20261122, 'size_min_max': [min(sizes), max(sizes)] if sizes else None,
                         'subsets_with_full_row': viol}

# ---------------------------------------------------------------- self-tests of the occupancy code
# known answers: 6-cup (parabola), 6-cap, a convex octagon (5-cap + 5-cup on common endpoints), collinear points
# rejected, and the states of a cap triple (0, 1, 2) and of a cup triple (0, 1, 3) computed by hand from the definitions
selftests = {}
s, mcap, mcup, octo = analyse([(x, x * x) for x in range(6)])
selftests['6cup'] = mcup == 6 and mcap == 2
s, mcap, mcup, octo = analyse([(x, -x * x) for x in range(6)])
selftests['6cap'] = mcap == 6 and mcup == 2
s, mcap, mcup, octo = analyse(sorted([(0, 0), (20, 70), (50, 110), (90, 120), (120, 0), (30, -70), (60, -110), (100, -120)]))
selftests['octagon'] = octo is True and mcap <= 5 and mcup <= 5
s, mcap, mcup, octo = analyse(sorted([(0, 0), (20, 70), (50, 110), (90, 120), (120, 0), (30, -70), (60, -110)]))
selftests['heptagon_no_octagon'] = octo is False
try:
    analyse([(0, 0), (1, 1), (2, 2)])
    selftests['collinear_rejected'] = False
except AssertionError:
    selftests['collinear_rejected'] = True
s, _, _, _ = analyse([(0, 0), (1, 5), (2, 0)])
selftests['cap_triple_states'] = s == [0, 1, 2] and own_states[2] == (1, 1, 0, 0)
s, _, _, _ = analyse([(0, 0), (1, -5), (2, 0)])
selftests['cup_triple_states'] = s == [0, 1, 3] and own_states[3] == (2, 0, 0, 0)
out['selftests'] = selftests
check('selftests', all(selftests.values()), selftests)

out['fails'] = fails
out['verdict'] = 'PASS' if not fails else 'FAIL'
json.dump(out, open(RV + 'own_checks15.json', 'w'), indent=1)
print(json.dumps({k: v for k, v in out.items() if k != 'controls'}, indent=1))
print(json.dumps(out['controls'], indent=1))
