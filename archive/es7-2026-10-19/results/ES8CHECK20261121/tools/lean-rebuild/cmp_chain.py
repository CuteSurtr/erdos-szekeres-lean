import json, csv, hashlib, os
A = '<scratch>/agents/lean-rebuild'
L = A + '/esb/experiments/omission-compact-checker-2026-11-05/logs/es311'
d = json.load(open(L + '/chain311-closure.json'))
tsv = {}
for r in csv.DictReader(open(L + '/chain311-build.tsv'), delimiter='\t'):
    if r['verdict'] == 'ok': tsv[r['module']] = r
st = {}
for k, v in d['modules'].items():
    p = os.path.join(A + '/olean', *k.split('.')) + '.olean'
    if not os.path.exists(p): continue
    h = hashlib.sha256(open(p, 'rb').read()).hexdigest()
    rec = v['recorded_olean_sha256']; built = tsv.get(k, {}).get('olean_sha256')
    s = ('match-recorded' if h == rec else 'differs-recorded') + '/' + ('match-chain311' if h == built else 'differs-chain311')
    st.setdefault(s, []).append(k)
for s, ks in st.items(): print(s, len(ks), ks if len(ks) < 6 else ks[:3] + ['...'])
