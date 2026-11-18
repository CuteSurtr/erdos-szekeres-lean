"""Independent row rejustification; inheritance is by identical CNF definition/hash.
Adapted from ../.. /tools/rows66.py, with stronger format checks and an explicit
new-certificate inventory. Does not run SAT solvers or proof checkers.
"""
import collections
import hashlib
import itertools as it
import json
from model import D, OLD, HERE, tau, positive, valid

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def records(directory):
    out = []
    for kind, filename in [('tmpl','template_certs.jsonl'), ('core','core_certs.jsonl')]:
        for line in (directory/'tcert'/filename).read_text().splitlines():
            out.append((kind, json.loads(line)))
    return out

def definition(kind, record):
    keys = ['core','tests','octs'] if kind == 'tmpl' else ['support','octs']
    return {k: record[k] for k in keys if k in record}

def main():
    current = records(D)
    prior = {r['cnf_sha256']: (k,r) for k,r in records(OLD)}
    receipts = {x['full_sha256']: x for line in
                (HERE.parent/'logs/n66-row-certificates.jsonl').read_text().splitlines()
                if (x := json.loads(line))}
    T = {r['id']: r for k,r in current if k == 'tmpl'}
    K = {tuple(r['support']): r for k,r in current if k == 'core'}
    assert len(T)+len(K) == len(current)
    for kind, r in current:
        support = r['core'] if kind == 'tmpl' else r['support']
        assert support == sorted(set(support)) and all(0 <= i < 70 for i in support)
        assert r['verdict'] == 's VERIFIED UNSAT'
        if 'octs' in r:
            for q in r['octs']:
                assert q == sorted(set(q)) and len(q) == 8
                assert all(0 <= i < len(support) for i in q)
        if kind == 'tmpl':
            assert all(valid(t, support) for t in r['tests'])
            assert hashlib.sha256(json.dumps([r['core'],r['tests'],r.get('octs')]).encode()).hexdigest()[:16] == r['id']
    J = json.loads((D/'tcert/justification.json').read_text())
    rows = json.loads((D/'used_rows.json').read_text())
    assert sha(D/'used_rows.json') == J['rows_sha256']
    assert collections.Counter((tuple(s),d) for s,d in rows) == collections.Counter(
        (tuple(j['support']),j['demand']) for j in J['justifications'])
    used = set(); cycles = []; depth_counts = collections.Counter()
    def check(j, depth=0):
        assert depth < 10
        s = j['support']
        assert s == sorted(set(s)) and all(0 <= i < 70 for i in s)
        assert j['demand'] == 1
        depth_counts[j['kind']] += 1
        if j['kind'] == 'mirror':
            q = j['of']
            assert sorted(tau[i] for i in q['support']) == s
            assert j['demand'] == q['demand']
            check(q, depth+1)
        elif j['kind'] == 'cycle':
            order = j['order']
            assert sorted(order) == s and j['demand'] == len(s)-7
            assert all(positive(*q) for q in it.combinations(order, 3))
            cycles.append({'support':s, 'order':order, 'depth':depth,
                           'triples_checked':len(list(it.combinations(order,3)))})
        elif j['kind'] == 'core':
            used.add(K[tuple(s)]['cnf_sha256'])
        elif j['kind'] == 'transported':
            r = T[j['template']]; sig = j['sigma']
            assert len(sig) == len(r['core']) and sorted(sig) == s
            assert all(valid(t, sig) for t in r['tests'])
            used.add(r['cnf_sha256'])
        else:
            raise ValueError(j['kind'])
    for j in J['justifications']:
        check(j)
    obligations = []; inherited = []; required = []
    for kind,r in current:
        h = r['cnf_sha256']
        if h not in used:
            continue
        item = {'kind':kind, 'record':r}
        required.append(item)
        if h in prior:
            oldkind, old = prior[h]
            assert kind == oldkind and definition(kind,r) == definition(kind,old)
            receipt = receipts[h]
            assert receipt['result'] in ('CERTIFIED','INHERITED independently verified identical CNF')
            if receipt['result'] == 'CERTIFIED':
                p = HERE.parent
                log = __import__('pathlib').Path('/home/jay/research/data/verify309-codex-20261113/rows')/(h+'.cake.log')
                assert 's VERIFIED UNSAT' in log.read_text().splitlines()
            inherited.append({'kind':kind,'cnf_sha256':h,'prior_receipt':receipt})
        else:
            obligations.append(item)
    assert len(required) == len(used)
    out = HERE/'data'
    (out/'cycles.json').write_text(json.dumps(cycles,indent=2)+'\n')
    (out/'new_certificates.json').write_text(json.dumps(obligations,indent=2)+'\n')
    (out/'inherited_certificates.json').write_text(json.dumps(inherited,indent=2)+'\n')
    summary = {'label':'COMPUTED','result':'ALL ROW JUSTIFICATIONS PASS; new certificates pending',
        'rows':len(rows),'kinds':dict(collections.Counter(j['kind'] for j in J['justifications'])),
        'recursive_kinds':dict(depth_counts),'cycle_triples_checked':sum(c['triples_checked'] for c in cycles),
        'required_templates':sum(k == 'tmpl' and r['cnf_sha256'] in used for k,r in current),
        'required_cores':sum(k == 'core' and r['cnf_sha256'] in used for k,r in current),
        'inherited':len(inherited),'new_certificates_needed':len(obligations),
        'used_rows_sha256':sha(D/'used_rows.json'),
        'justification_sha256':sha(D/'tcert/justification.json')}
    (out/'rows.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary),flush=True)

if __name__ == '__main__':
    main()
