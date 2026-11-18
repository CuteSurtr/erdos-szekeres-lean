"""Markdown table of refuted rules/localizations from restr/, must/, thr/ results and cex/ realizations."""
import json, os, glob
def load(d):
    fn = os.path.join(d, 'results.jsonl')
    return [json.loads(l) for l in open(fn)] if os.path.exists(fn) else []
def rng(ms):
    ms = sorted(set(ms))
    if not ms: return '–'
    out = []; s = p = ms[0]
    for x in ms[1:] + [None]:
        if x is None or x != p + 1:
            out.append('%d' % s if s == p else '%d–%d' % (s, p)); s = x
        p = x
    return ', '.join(out)
cert = lambda r: r['status'] == 'UNSAT' and r.get('cake_lpr') == 's VERIFIED UNSAT'
cex = {}
for fn in glob.glob('cex/*.json'):
    r = json.load(open(fn)); cex[os.path.basename(fn)] = r
ver = {}
if os.path.exists('verify_cex.log'):
    for l in open('verify_cex.log'):
        ver[l.split()[0]] = 'VERIFIED' in l
def real(prefix, a, n, ms):
    """smallest m among ms with a realized + verified point set"""
    out = []
    for m in ms:
        for suffix in ('', '_real'):
            fn = '%s_a%d_n%d_m%d%s.json' % (prefix, a, n, m, suffix)
            if fn in cex and cex[fn].get('realized') and ver.get(fn): out.append((m, fn))
    return out
names = {'QQ': 'Δ ⊆ Q ∪ Q′ (points that start no (a−1)-cap or end none)', 'ends': 'Δ ⊆ E_L ∪ E_R (ends of convex (n−1)-gons)',
         'rank': 'Δ ⊆ Δ_R ∪ Δ_L (rank-defined, ETVTHY §3.2)', 'Q': 'Δ ⊆ Q (negative control)', 'cupint': 'Δ ⊆ interior vertices of cup parts of gons', 'capint': 'Δ ⊆ interior vertices of cap parts of gons', 'cupint+ends': 'Δ ⊆ ends ∪ interior cup vertices of gons', 'capint+ends': 'Δ ⊆ ends ∪ interior cap vertices of gons', 'int': 'Δ ⊆ non-end vertices of gons',
         'cupR': 'Δ ⊇ all right ends of (n−1)-cups', 'cupRL': 'Δ ⊇ all left and right ends of (n−1)-cups',
         'gonRQ': 'Δ ⊇ all right ends of gons that start no (a−1)-cap', 'Qall': 'Δ ⊇ Q (all points that start no (a−1)-cap)'}
print('| statement tested | (a, n), form | CERTIFIED true for m = | fails (SAT + exact re-check) at m = | real point set (verified from coordinates) |')
print('|---|---|---|---|---|')
T = load('thr')
for key in sorted({(r['a'], r['n']) for r in T}):
    X = [r for r in T if (r['a'], r['n']) == key]; sat = sorted({r['m'] for r in X if r['status'] == 'SAT'})
    rl = real('threshold1', key[0], key[1], sat)
    print('| threshold rule: some Δ_x = (Q′ left of x) ∪ (Q from x on) works | (%d, %d), weak | %s | %s | %s |' % (key[0], key[1], rng([r['m'] for r in X if cert(r)]), rng(sat), (', '.join('m = %d: `%s`' % x for x in rl) or 'none found (signotopes only)') if sat else '–'))
U = load('upper')
unames = {'upper-chain': 'Δ meets the cap part (upper chain with both ends) of every gon', 'lower-chain': 'Δ meets the cup part (lower chain with both ends) of every gon', 'end-pair': 'Δ contains an end of every gon'}
for key in sorted({(r['rule'], r['a'], r['n'], r['form']) for r in U}, key=lambda k: (['end-pair', 'upper-chain', 'lower-chain'].index(k[0]), k[1:])):
    X = [r for r in U if (r['rule'], r['a'], r['n'], r['form']) == key]
    sat = sorted({r['m'] for r in X if r['status'] == 'SAT'}); unk = sorted({r['m'] for r in X if r['status'] == 'UNKNOWN'})
    rl = real(('%s_%s' % (key[0], key[3])).replace('-', ''), key[1], key[2], sat)
    print('| %s | (%d, %d), %s | %s | %s%s | %s |' % (unames[key[0]], key[1], key[2], key[3], rng([r['m'] for r in X if cert(r)]), rng(sat), (' (time-out at %s)' % rng(unk)) if unk else '',
          (', '.join('m = %d: `%s`' % x for x in rl) or 'none found (signotopes only)') if sat else '–'))
for d, field, pre in (('restr', 'allow', 'restr'), ('must', 'must', 'must')):
    R = load(d) + (load('restr2') if d == 'restr' else [])
    for key in sorted({(r[field], r['a'], r['n'], r['form']) for r in R}, key=lambda k: (['QQ', 'ends', 'cupint', 'capint', 'cupint+ends', 'capint+ends', 'int', 'rank', 'Q', 'cupR', 'cupRL', 'gonRQ', 'Qall'].index(k[0]), k[1:])):
        X = [r for r in R if (r[field], r['a'], r['n'], r['form']) == key]
        sat = sorted({r['m'] for r in X if r['status'] == 'SAT'}); unk = sorted({r['m'] for r in X if r['status'] == 'UNKNOWN'})
        rl = real('%s_%s_%s' % (pre, key[0], key[3]), key[1], key[2], sat)
        print('| %s | (%d, %d), %s | %s | %s%s | %s |' % (names[key[0]], key[1], key[2], key[3], rng([r['m'] for r in X if cert(r)]), rng(sat), (' (time-out at %s)' % rng(unk)) if unk else '',
              (', '.join('m = %d: `%s`' % x for x in rl) or 'none found (signotopes only)') if sat else '–'))
