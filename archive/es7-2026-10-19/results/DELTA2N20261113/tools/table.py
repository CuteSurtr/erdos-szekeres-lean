import json, sys, os, collections
rows = []
for d in sys.argv[1:]:
    fn = os.path.join(d, 'results.jsonl')
    if os.path.exists(fn): rows += [json.loads(l) for l in open(fn)]
best = {}
for r in rows:
    if r.get('lo', 0) != 0 or r.get('hi', r['m']) != r['m']: continue
    if r['b'] != r['a'] - 1: continue
    key = (r['a'], r['n'], r['form'])
    best.setdefault(key, {})
    cur = best[key].get(r['m'])
    # prefer certified UNSAT
    rank = lambda x: (x['status'] == 'UNSAT' and x.get('cake_lpr') == 's VERIFIED UNSAT', x['status'] == 'UNSAT', x['status'] == 'SAT')
    if cur is None or rank(r) > rank(cur): best[key][r['m']] = r
for key in sorted(best):
    a, n, form = key
    ms = sorted(best[key])
    cert = [m for m in ms if best[key][m]['status'] == 'UNSAT' and best[key][m].get('cake_lpr') == 's VERIFIED UNSAT']
    sat = [m for m in ms if best[key][m]['status'] == 'SAT']
    unk = [m for m in ms if best[key][m]['status'] == 'UNKNOWN']
    last = best[key][max(cert)] if cert else None
    print('(a=%d,n=%d) %-6s certified UNSAT m=%s  SAT m=%s  timeout m=%s  last: cadical %ss cake %ss' % (a, n, form, cert, sat, unk, last and last['cadical_s'], last and last.get('cake_s')))
