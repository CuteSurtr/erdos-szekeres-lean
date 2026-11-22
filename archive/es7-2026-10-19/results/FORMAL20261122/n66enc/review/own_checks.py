"""Reviewer's own checks for item n66-encoder (slot lrv2). Read-only on every input; writes review/own_checks.json.

A. state list: own sort of the nonincreasing 4-tuples over 0..4 by (sum, tuple) vs the list dumped from the olean.
B. leaves: the 132 leaves dumped from the olean (N66Enc.leaves132) vs campaign_status.json (lits, status), the
   leaf_order map used by M9, and per certdir: cert.json cube, cake.out exact content, cake command and exit status.
C. rows: R0 dumped from the olean vs the union of the 132 used_rows.json and the 132 tcert/justification.json
   (demand 1, kind) of the record.
D. positive controls (exact integers): the record's ETV 50-point set and its three reflections are checked for class
   membership (distinct x, general position, no 6-cap, no 6-cup, no 5-cap + 5-cup on common endpoints = no convex
   octagon in this class); the state of each point is computed exactly as the Lean definition N66Geo.idxOf does
   (labels = longest cap/cup ending with (u,v) minus 1; f_a = max cup label over incoming labels with cap label >= a;
   index in the sorted list); then no R0 row may be fully occupied, for the four sets and random subsets of them.
usage: own_checks.py SEED N_SUBSETS"""
import itertools, json, os, random, sys
import numpy as np

D = '/home/jay/research/data/formalize-20261122/n66enc'
RV = D + '/review'
W = '/home/jay/research/data/n66-20261113'
seed, nsub = int(sys.argv[1]), int(sys.argv[2])
out = {}

# ---------- A. states
own = sorted([f for f in itertools.product(range(5), repeat=4) if all(f[i] >= f[i + 1] for i in range(3))],
             key=lambda f: (sum(f), f))
lean = [tuple(map(int, l.split())) for l in open(RV + '/dump_stateList.txt') if l.strip()]
out['A_stateList_equals_own_sort'] = own == lean
out['A_states'] = len(own)
SIDX = {s: i for i, s in enumerate(own)}
TAU = [SIDX[tuple(sum(1 for a in range(4) if f[a] >= x) for x in range(1, 5))] for f in own]  # conjugate partition

# ---------- B. leaves and certdirs
st = json.load(open(W + '/p2/c14/campaign_status.json'))['cubes']
leaves = {cid: c for cid, c in st.items() if c['status'] != 'split'}
lean_leaves = [[[int(z.split(':')[0]), int(z.split(':')[1])] for z in l.split()]
               for l in open(RV + '/dump_leaves132.txt') if l.strip()]
order = [l.strip() for l in open(D + '/tools/leaf_order.txt') if l.strip()]
key = lambda lits: tuple(tuple(x) for x in lits)
out['B_lean_leaves'] = len(lean_leaves)
out['B_lean_leaves_distinct'] = len({key(x) for x in lean_leaves})
out['B_campaign_leaves'] = len(leaves)
out['B_campaign_leaves_all_certified'] = all(c['status'] == 'certified' for c in leaves.values())
out['B_leaf_multiset_equal'] = sorted(map(key, lean_leaves)) == sorted(key(c['lits']) for c in leaves.values())
out['B_leaf_order_map_ok'] = len(order) == 132 and len(set(order)) == 132 and \
    all(lean_leaves[i] == st[order[i]]['lits'] for i in range(132))
bad = []
for i, cid in enumerate(order):
    c = st[cid]; cd = f"{W}/{c['certdir']}"
    cj = json.load(open(cd + '/cert.json')); vj = json.load(open(cd + '/verify.json'))
    cake = open(cd + '/cake.out', 'rb').read()
    err = open(cd + '/cake.err').read()
    cmd_ok = f'"/home/jay/.local/bin/cake_lpr ' in err and f"{c['certdir']}/trim.cnf {c['certdir']}/trim.lrat\"" in err \
        and err.count('Command being timed') == 1 and 'Exit status: 0' in err
    hashes = {c['trim_cnf_sha256'], cj['trim_cnf_sha256'], vj['trim_cnf_sha256']}
    ok = (cj['cube'] == c['lits'] and cake == b's VERIFIED UNSAT\n' and cmd_ok and len(hashes) == 1
          and cj.get('ALL_OK') and vj.get('ALL_OK') and c.get('accept') == 'ok')
    if not ok:
        bad.append([i, cid, cj['cube'] == c['lits'], cake[:40].decode(errors='replace'), cmd_ok, len(hashes)])
out['B_certdir_checks_failed'] = bad
out['B_certdir_checks_ok'] = 132 - len(bad)

# ---------- C. rows
R0 = [tuple(map(int, l.split())) for l in open(RV + '/dump_R0.txt') if l.strip()]
out['C_R0_rows'] = len(R0)
out['C_R0_sorted_distinct'] = all(list(T) == sorted(set(T)) and all(0 <= s < 70 for s in T) for T in R0)
out['C_R0_all_have_state_outside_01'] = all(any(s >= 2 for s in T) for T in R0)
used, just, used_demands, no_just = set(), {}, set(), []
for c in leaves.values():
    cd = f"{W}/{c['certdir']}"
    for r in json.load(open(cd + '/used_rows.json')):
        used.add(tuple(sorted(r[0])))
        used_demands.add(r[1])
    jp = cd + '/tcert/justification.json'
    if not os.path.exists(jp):   # cubes whose trim uses no row (the UP-refuted ones) have no justification file
        no_just.append([c['id'], len(json.load(open(cd + '/used_rows.json')))])
        continue
    for e in json.load(open(jp))['justifications']:
        just.setdefault(tuple(sorted(e['support'])), set()).add((e['kind'], e['demand']))
R0set = set(R0)
out['C_R0_equals_union_of_used_rows'] = R0set == used
out['C_R0_rows_without_justification'] = sum(1 for T in R0 if T not in just)
out['C_used_row_demands'] = sorted(used_demands)
out['C_cubes_without_justification_file_[id,used_rows]'] = no_just
out['C_justified_demands'] = sorted({d for v in just.values() for _, d in v})
kinds = {}
for T in R0:
    for k in {k for k, _ in just.get(T, ())}:
        kinds[k] = kinds.get(k, 0) + 1
out['C_R0_rows_by_kind_any_cube'] = kinds

# ---------- D. positive controls
def orient(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])

def analyse(P, full=True):
    """P sorted by x. Returns (class_ok, reason, states). full=False skips the octagon test (subsets of a set of
    the class are in the class)."""
    n = len(P)
    if any(P[i][0] >= P[i + 1][0] for i in range(n - 1)):
        return False, 'x not strictly increasing', None
    O = {}
    for i, j, k in itertools.combinations(range(n), 3):
        o = orient(P[i], P[j], P[k])
        if o == 0:
            return False, 'collinear', None
        O[i, j, k] = o > 0
    cap = [[2 if u < v else 0 for v in range(n)] for u in range(n)]   # longest cap ending with (u, v)
    cup = [[2 if u < v else 0 for v in range(n)] for u in range(n)]
    for v in range(n):
        for u in range(v):
            for t in range(u):
                if O[t, u, v]:
                    cup[u][v] = max(cup[u][v], cup[t][u] + 1)
                else:
                    cap[u][v] = max(cap[u][v], cap[t][u] + 1)
    if max((cap[u][v] for v in range(n) for u in range(v)), default=0) >= 6:
        return False, '6-cap', None
    if max((cup[u][v] for v in range(n) for u in range(v)), default=0) >= 6:
        return False, '6-cup', None
    for p in (range(n) if full else ()):   # paths starting exactly at p
        lc = {}; lu = {}
        for v in range(p + 1, n):
            lc[p, v] = 2; lu[p, v] = 2
        for v in range(p + 1, n):
            for u in range(p + 1, v):
                bc = bu = 0
                for t in range(p, u):
                    if (t, u) in lc and not O[t, u, v]:
                        bc = max(bc, lc[t, u] + 1)
                    if (t, u) in lu and O[t, u, v]:
                        bu = max(bu, lu[t, u] + 1)
                if bc: lc[u, v] = bc
                if bu: lu[u, v] = bu
        endc = {v for (u, v), L in lc.items() if L >= 5}
        endu = {v for (u, v), L in lu.items() if L >= 5}
        if endc & endu:
            return False, 'convex octagon (5-cap and 5-cup on common endpoints)', None
    states = []
    for v in range(n):
        f = tuple(max([cup[u][v] - 1 for u in range(v) if cap[u][v] - 1 >= a] + [0]) for a in range(1, 5))
        if f not in SIDX:
            return False, f'profile {f} outside the 70 states', None
        states.append(SIDX[f])
    return True, 'ok', states

# self-tests of analyse (known answers)
assert analyse([(i, i * i) for i in range(6)])[1] == '6-cup'
assert analyse([(i, -i * i) for i in range(6)])[1] == '6-cap'
_oct = sorted([(0, 0), (2, 6), (5, 8), (8, 6), (10, 0), (1, -3), (4, -7), (7, -6)])
assert analyse(_oct)[1].startswith('convex octagon'), analyse(_oct)
assert analyse([(0, 0), (1, 1), (2, 4)])[2] == [0, 1, 3]      # cup triple: third point (2,0,0,0)
assert analyse([(0, 0), (1, -1), (2, -4)])[2] == [0, 1, 2]    # cap triple: third point (1,1,0,0)
assert analyse([(0, 0), (1, 1), (2, 2)])[1] == 'collinear'
out['D_selftests'] = 'pass'

M = np.zeros((len(R0), 70), bool)
for r, T in enumerate(R0):
    M[r, list(T)] = True

def violations(states):
    occ = np.zeros(70, bool); occ[states] = True
    return int((~(M & ~occ).any(axis=1)).sum()), int((M & ~occ).sum(axis=1).min())

etv = json.load(open(W + '/etv668.json'))
E0 = sorted(tuple(p) for p in etv['points'])
variants = {'etv': E0, 'refl_y': sorted((x, -y) for x, y in E0), 'refl_x': sorted((-x, y) for x, y in E0),
            'rot180': sorted((-x, -y) for x, y in E0)}
ctrl = {}
full_states = {}
for name, V in variants.items():
    ok, why, s = analyse(V)
    ctrl[name] = {'points': len(V), 'class_ok': ok, 'why': why}
    if ok:
        full_states[name] = s
        v, mm = violations(s)
        ctrl[name].update({'occupied': len(set(s)), 'distinct_states': len(set(s)) == len(s), 'violated_rows': v,
                           'min_missing_over_rows': mm})
out['D_full_sets'] = ctrl
if 'etv' in full_states:
    out['D_etv_states_equal_record'] = full_states['etv'] == etv['states']
    out['D_etv_holes_equal_record'] = sorted(set(range(70)) - set(full_states['etv'])) == sorted(etv['holes'])
if 'etv' in full_states and 'refl_y' in full_states:
    out['D_mirror_states_are_tau'] = full_states['refl_y'] == [TAU[s] for s in full_states['etv']]
rng = random.Random(seed)
tot_v, tested, min_missing, notok = 0, 0, 99, 0
names = list(variants)
for it in range(nsub):
    V = variants[names[it % 4]]
    k = rng.randrange(8, 50)
    P = sorted(rng.sample(V, k))
    ok, why, s = analyse(P, full=False)
    if not ok:
        notok += 1
        continue
    v, mm = violations(s)
    tested += 1; tot_v += v; min_missing = min(min_missing, mm)
out['D_subsets'] = {'seed': seed, 'requested': nsub, 'tested': tested, 'not_in_class': notok, 'violated_rows_total': tot_v,
                    'min_missing_over_all_rows_and_sets': min_missing}
json.dump(out, open(RV + '/own_checks.json', 'w'), indent=1)
print(json.dumps(out, indent=1))
