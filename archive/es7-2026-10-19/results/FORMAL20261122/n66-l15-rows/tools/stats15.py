"""Row justifications behind R0_15 (own code, read-only on the record's files; untrusted: every certificate it
selects is checked by the kernel, and every certificate CNF by hash, M3/M9).
For every row of n66-level15's R0_15 (rows_used15.txt, in order) take the first justification over the 105
certified level-15 leaves (campaign seq order; c15 justification.json lists exactly the trim's rows, so every pick is
a (row, cube) pair VB's rowchk.py checked), collect the templates / cores it needs, and compare them with the 629
certificates of n66-rowsvalid (data/certs_manifest.tsv, VB job ids). Also compares with the level-14 certificate of
the 10,264 shared rows (n66-rowsvalid data/just_R0.json).
Writes data/just_R15.json; prints counts. usage: python3 -I stats15.py"""
import json, collections, os, hashlib
W = '/home/jay/research/data/n66-20261113/'
R15F = '/home/jay/research/data/formalize-20261122/n66-level15/lean/N66E15/data/rows_used15.txt'
RV = '/home/jay/research/data/formalize-20261122/n66-rowsvalid/'
OUT = '/home/jay/research/data/formalize-20261122/n66-l15-rows/data/'
CS = W + 'p2/c15/campaign_status.json'
assert hashlib.sha256(open(CS, 'rb').read()).hexdigest() == '4802dc9a946cefa3b855b8c495becc0fb33491a89e5472c9722ccb9d0c8138f5'
assert hashlib.sha256(open(R15F, 'rb').read()).hexdigest().startswith('f45e25f1')
st = json.load(open(CS))['cubes']
leaves = sorted([c for c in st.values() if c['status'] == 'certified'], key=lambda c: c['seq'])
assert len(leaves) == 105, len(leaves)
R15 = [tuple(map(int, l.split())) for l in open(R15F) if l.strip()]
assert len(R15) == 10859 and len(set(R15)) == 10859
R15set = set(R15)


def job_key_core(support, octs):
    return 'C_' + hashlib.sha256(json.dumps([list(sorted(support)), octs]).encode()).hexdigest()[:16]


just = {}
tmpl = {}
cores = {}
nojust = []
for c in leaves:
    td = W + c['certdir'] + '/tcert/'
    if not os.path.exists(td + 'justification.json'):
        nojust.append(c['id'])
        continue
    J = json.load(open(td + 'justification.json'))
    for l in open(td + 'template_certs.jsonl'):
        d = json.loads(l)
        key = json.dumps([d['core'], d['tests'], d.get('octs')])
        if d['id'] in tmpl:
            assert json.dumps([tmpl[d['id']]['core'], tmpl[d['id']]['tests'], tmpl[d['id']].get('octs')]) == key, d['id']
        else:
            tmpl[d['id']] = d
    for l in open(td + 'core_certs.jsonl'):
        d = json.loads(l)
        k = job_key_core(d['support'], d.get('octs'))
        cores.setdefault(k, d)
    seen = set()
    for j in J['justifications']:
        T = tuple(sorted(j['support']))
        assert T not in seen, (c['id'], T)          # one entry per row per cube
        seen.add(T)
        if T in R15set and T not in just:
            just[T] = (j, c['id'])
missing = [T for T in R15 if T not in just]
print('leaves without justification.json', len(nojust), nojust[:10])
print('rows', len(R15), 'justified', len(just), 'missing', len(missing))
kinds = collections.Counter(just[T][0]['kind'] + ('/' + just[T][0]['of']['kind'] if just[T][0]['kind'] == 'mirror' else '')
                            for T in R15 if T in just)
print('kinds', dict(kinds))

need_t, need_c = set(), set()
for T in R15:
    j = just[T][0]
    assert j['demand'] == 1
    jj = j['of'] if j['kind'] == 'mirror' else j
    if jj['kind'] == 'transported':
        assert tmpl[jj['template']]['verdict'] == 's VERIFIED UNSAT'
        need_t.add(jj['template'])
    elif jj['kind'] == 'core':
        k = job_key_core(jj['support'], None)
        # the core entry of the cube that justified the row (support -> record core cert)
        need_c.add(tuple(sorted(jj['support'])))
print('templates needed', len(need_t), 'core supports needed', len(need_c))

man = [l.rstrip('\n').split('\t') for l in open(RV + 'data/certs_manifest.tsv')][1:]
have_t = {r[2] for r in man if r[1] == 'T'}
have_c = {r[2] for r in man if r[1] == 'C'}
print('n66-rowsvalid certificates: templates', len(have_t), 'cores', len(have_c))
new_t = sorted(need_t - have_t)
# cores: VB key = hash(support, octs of the record core cert used by that cube)
core_keys = {}
for T in R15:
    j = just[T][0]
    jj = j['of'] if j['kind'] == 'mirror' else j
    if jj['kind'] == 'core':
        cid = just[T][1]
        td = W + st[cid]['certdir'] + '/tcert/'
        cc = {}
        for l in open(td + 'core_certs.jsonl'):
            d = json.loads(l); cc[tuple(sorted(d['support']))] = d
        d = cc[tuple(sorted(jj['support']))]
        assert d['verdict'] == 's VERIFIED UNSAT'
        core_keys[tuple(sorted(jj['support']))] = job_key_core(d['support'], d.get('octs'))
new_c = sorted(set(core_keys.values()) - have_c)
print('templates not among the 629:', len(new_t), new_t[:20])
print('cores not among the 629:', len(new_c), new_c[:20])

# level-14 comparison
L14 = json.load(open(RV + 'data/just_R0.json'))
j14 = {tuple(r[0]): r[1] for r in L14['rows']}
shared = [T for T in R15 if T in j14]
print('shared with level 14', len(shared), 'new', len(R15) - len(shared))
same = sum(1 for T in shared if json.dumps(j14[T], sort_keys=True) == json.dumps(just[T][0], sort_keys=True))
print('shared rows with an identical justification', same)
newrows = [T for T in R15 if T not in j14]
print('kinds of the new rows', dict(collections.Counter(just[T][0]['kind'] for T in newrows)))
json.dump({'rows': [[list(T), just[T][0], just[T][1]] for T in R15],
           'templates': {t: tmpl[t] for t in sorted(need_t)},
           'core_keys': {' '.join(map(str, k)): v for k, v in core_keys.items()},
           'new_templates': new_t, 'new_cores': new_c},
          open(OUT + 'just_R15.json', 'w'))
print('wrote', OUT + 'just_R15.json')
