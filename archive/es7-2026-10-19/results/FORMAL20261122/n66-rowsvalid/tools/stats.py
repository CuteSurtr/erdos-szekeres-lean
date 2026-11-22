"""Statistics of the row justifications behind R0 (own code, read-only on the record's files).
For every row of n66enc's R0 (rows_used.txt, in order) take the first justification found over the 132 certified
leaves (campaign seq order), and collect the templates / cores it needs.  Writes data/just_R0.json and prints counts.
usage: python3 -I stats.py"""
import json, collections, os, sys, hashlib
W = '/home/jay/research/data/n66-20261113/'
R0F = '/home/jay/research/data/formalize-20261122/n66enc/lean/N66Enc/data/rows_used.txt'
OUT = '/home/jay/research/data/formalize-20261122/n66-rowsvalid/data/'
st = json.load(open(W + 'p2/c14/campaign_status.json'))['cubes']
leaves = sorted([c for c in st.values() if c['status'] == 'certified'], key=lambda c: c['seq'])
assert len(leaves) == 132, len(leaves)
R0 = [tuple(map(int, l.split())) for l in open(R0F) if l.strip()]
assert len(R0) == 11884
R0set = set(R0)
just = {}      # row -> (justification, cube id)
tmpl = {}      # id -> record
cores = {}     # support -> record (per content)
tmpl_src = collections.defaultdict(set)
for c in leaves:
    td = W + c['certdir'] + '/tcert/'
    if not os.path.exists(td + 'justification.json'):
        continue
    J = json.load(open(td + 'justification.json'))
    for l in open(td + 'template_certs.jsonl'):
        d = json.loads(l)
        key = json.dumps([d['core'], d['tests'], d.get('octs')])
        if d['id'] in tmpl:
            assert json.dumps([tmpl[d['id']]['core'], tmpl[d['id']]['tests'], tmpl[d['id']].get('octs')]) == key
            if tmpl[d['id']]['cnf_sha256'] != d['cnf_sha256']: print('WARN tmpl cnf hash differs', d['id'])
        else:
            tmpl[d['id']] = d
        tmpl_src[d['id']].add(c['id'])
    for l in open(td + 'core_certs.jsonl'):
        d = json.loads(l)
        k = tuple(d['support'])
        if k in cores and cores[k].get('cnf_sha256') != d.get('cnf_sha256'):
            print('WARN core content differs', k, cores[k].get('octs') is None, d.get('octs') is None)
        cores.setdefault(k, d)
    for j in J['justifications']:
        T = tuple(sorted(j['support']))
        if T in R0set and T not in just:
            just[T] = (j, c['id'])
missing = [T for T in R0 if T not in just]
print('rows', len(R0), 'justified', len(just), 'missing', len(missing))
kinds = collections.Counter(just[T][0]['kind'] for T in R0 if T in just)
print('kinds', dict(kinds))
need_t = collections.Counter(); need_c = set(); ntests = 0; npos = 0; ndom = 0; nemp = 0
for T in R0:
    j = just[T][0]
    jj = j['of'] if j['kind'] == 'mirror' else j
    if jj['kind'] == 'transported':
        t = tmpl[jj['template']]; need_t[jj['template']] += 1
        for x in t['tests']:
            ntests += 1
            if x[0] == 'positive': npos += 1
            elif x[0] == 'domain': ndom += 1
            else: nemp += 1
    elif jj['kind'] == 'core':
        need_c.add(tuple(jj['support']))
print('templates needed', len(need_t), 'cores needed', len(need_c))
print('test evaluations', ntests, 'positive', npos, 'domain', ndom, 'empty', nemp)
sz = collections.Counter(len(tmpl[t]['core']) for t in need_t)
print('template sizes', sorted(sz.items()))
print('template styles', collections.Counter('big' if 'octs' in tmpl[t] else 'old' for t in need_t))
print('tests per template: max', max(len(tmpl[t]['tests']) for t in need_t), 'sum', sum(len(tmpl[t]['tests']) for t in need_t))
print('octs per big template: max', max((len(tmpl[t]['octs']) for t in need_t if 'octs' in tmpl[t]), default=0))
cs = collections.Counter(len(c) for c in need_c)
print('core sizes', sorted(cs.items()))
print('core styles', collections.Counter('big' if 'octs' in cores[c] else 'old' for c in need_c))
print('core verdicts', collections.Counter(cores[c]['verdict'] for c in need_c))
print('template verdicts', collections.Counter(tmpl[t]['verdict'] for t in need_t))
cyc = [T for T in R0 if just[T][0]['kind'] == 'cycle']
print('cycle lens', collections.Counter(len(T) for T in cyc))
json.dump({'rows': [[list(T), just[T][0], just[T][1]] for T in R0],
           'templates': {t: tmpl[t] for t in need_t}, 'cores': [cores[c] for c in sorted(need_c)]},
          open(OUT + 'just_R0.json', 'w'))
print('wrote', OUT + 'just_R0.json')
