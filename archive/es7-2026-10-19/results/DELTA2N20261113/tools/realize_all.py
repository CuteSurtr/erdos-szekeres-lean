"""Realize the SAT models (abstract signotopes refuting a restricted statement) of the given results files as point sets."""
import sys, json, os
from realize import realize
os.makedirs('cex', exist_ok=True)
for fn in sys.argv[1:]:
    for l in open(fn):
        r = json.loads(l)
        if r['status'] != 'SAT' or 'model' not in r: continue
        if r.get('must'): base = 'must_' + r['must'] + '_' + r.get('form', '')
        elif r.get('rule') in ('upper-chain', 'lower-chain', 'end-pair'): base = r['rule'] + '_' + r.get('form', '')
        elif r.get('rule'): base = r['rule']
        else: base = 'restr_' + str(r.get('allow')) + '_' + r.get('form', '')
        name = ('%s_a%d_n%d_m%d' % (base, r['a'], r['n'], r['m'])).replace('-', '')
        out = os.path.join('cex', name + '.json')
        if os.path.exists(out): continue
        P = realize(r['m'], r['model'], restarts=int(os.environ.get('RESTARTS', '60')), seed=7)
        rec = {'name': name, 'a': r['a'], 'n': r['n'], 'm': r['m'], 'kind': r.get('rule') or (('must=' + r['must']) if r.get('must') else ('allow=' + str(r.get('allow')))), 'form': r.get('form'),
               'signs': r['model'], 'realized': P is not None, 'P': P}
        json.dump(rec, open(out, 'w'))
        print(name, 'realized' if P else 'NOT realized (%s restarts)' % os.environ.get('RESTARTS', '60'), flush=True)
