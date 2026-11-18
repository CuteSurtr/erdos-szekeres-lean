"""Markdown tables + hash list from the results.jsonl files of W."""
import json, os, sys, glob
def load(d):
    fn = os.path.join(d, 'results.jsonl')
    return [json.loads(l) for l in open(fn)] if os.path.exists(fn) else []
def rng(ms):
    ms = sorted(ms)
    if not ms: return '–'
    out = []; s = ms[0]; p = ms[0]
    for x in ms[1:] + [None]:
        if x is None or x != p + 1:
            out.append('%d' % s if s == p else '%d–%d' % (s, p))
            s = x
        p = x
    return ', '.join(out)
rows = load('eager') + load('grid') + load('late') + load('manual')
cert = lambda r: r['status'] == 'UNSAT' and r.get('cake_lpr') == 's VERIFIED UNSAT'
plain = [r for r in rows if not r.get('allow') and not r.get('reduced') and r['b'] == r['a'] - 1 and r.get('lo', 0) == 0 and r.get('hi', r['m']) == r['m']]
keys = sorted({(r['a'], r['n'], r['form']) for r in plain if r['form'] != 'base'})
print('| (a, n) | form | CERTIFIED for m = | COMPUTED only (proof not checked) | largest certified case: clauses, CaDiCaL s, LRAT bytes, cake_lpr s | base UNSAT (no valid signotope) at m = | status |')
print('|---|---|---|---|---|---|---|')
for a, n, form in keys:
    R = [r for r in plain if (r['a'], r['n'], r['form']) == (a, n, form)]
    ms = sorted({r['m'] for r in R if cert(r)})
    comp = sorted({r['m'] for r in R if r['status'] == 'UNSAT'} - set(ms))
    unk = sorted({r['m'] for r in R if r['status'] == 'UNKNOWN'} - set(ms) - set(comp))
    sat = sorted({r['m'] for r in R if r['status'] == 'SAT'})
    hard = max([r for r in R if cert(r)], key=lambda r: (r['m'], r['cadical_s']))
    B = [r for r in plain if (r['a'], r['n'], r['form']) == (a, n, 'base') and cert(r)]
    m0 = min([r['m'] for r in B]) if B else None
    complete = m0 is not None and all(x in ms for x in range(n - 1, m0))
    status = '**complete** (all m)' if complete else ('open from m = %d' % (max(ms + comp) + 1)) + (' (time-out at %s)' % rng(unk) if unk else '')
    if sat: status = 'SAT at m = ' + rng(sat)
    print('| (%d, %d) | %s | %s | %s | m = %d: %d, %.1f, %d, %.1f | %s | %s |' % (a, n, form, rng(ms), rng(comp), hard['m'], hard['clauses'], hard['cadical_s'], hard.get('lrat_bytes', 0), hard.get('cake_s', 0), m0 if m0 else '–', status))
print()
R = load('restr') + load('restr2')
print('| restriction on Δ | (a, n) | form | CERTIFIED true for m = | first failure (SAT, exact re-check) | time-out |')
print('|---|---|---|---|---|---|')
for key in sorted({(r['allow'], r['a'], r['n'], r['form']) for r in R}):
    X = [r for r in R if (r['allow'], r['a'], r['n'], r['form']) == key]
    ms = sorted({r['m'] for r in X if cert(r)}); sat = sorted({r['m'] for r in X if r['status'] == 'SAT'}); unk = sorted({r['m'] for r in X if r['status'] == 'UNKNOWN'})
    print('| %s | (%d, %d) | %s | %s | %s | %s |' % (key[0], key[1], key[2], key[3], rng(ms), ('m = %d' % sat[0]) if sat else '–', rng(unk)))
print()
T = load('thr')
print('| threshold rule | CERTIFIED true for m = | fails (SAT) at m = |')
print('|---|---|---|')
for key in sorted({(r['a'], r['n']) for r in T}):
    X = [r for r in T if (r['a'], r['n']) == key]
    print('| (a, n) = (%d, %d) | %s | %s |' % (key[0], key[1], rng({r['m'] for r in X if cert(r)}), rng({r['m'] for r in X if r['status'] == 'SAT'})))
# hash list
with open('cnf_hashes.tsv', 'w') as f:
    f.write('dir\ta\tn\tm\tform\tb\tallow\tmust\treduced\tvars\tclauses\tstatus\tcnf_sha256\tlrat_bytes\tlrat_sha256\tcake_lpr\tcadical_s\tcake_s\n')
    for d in ('eager', 'grid', 'late', 'manual', 'restr', 'restr2', 'must', 'red', 'control', 'thr', 'upper'):
        for r in load(d):
            f.write('\t'.join(str(x) for x in [d, r['a'], r['n'], r['m'], r.get('form', r.get('rule')), r.get('b', r['a'] - 1), r.get('allow'), r.get('must'), r.get('reduced'), r['vars'], r['clauses'], r['status'],
                                                r['cnf_sha256'], r.get('lrat_bytes', ''), r.get('lrat_sha256', ''), r.get('cake_lpr', ''), r['cadical_s'], r.get('cake_s', '')]) + '\n')
