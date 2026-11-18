"""Phase 2: independent link check for a row justification directory (tcert): the CNF texts whose LRAT proofs cake_lpr
accepted (SHA-256 recorded in template_certs.jsonl / core_certs.jsonl) are regenerated here from their definitions and
hashed again.  The static parts that template_cert66 / bigcore read from the disk cache (static/static_A4_B4_<n>.txt,
static/staticnoct_A4_B4_<n>.txt) are first regenerated from coupled5.CNF without the cache and compared byte for byte.
usage: p2_recheck_rows.py <tcert dir>      output: <tcert dir>/recheck.json"""
import sys, os, json, hashlib, time
import etv_common as ec, coupled5, bigcore
assert ec.A == 4 and ec.B == 4 and ec.N == 70
d = sys.argv[1]; t0 = time.time()
T = [json.loads(l) for l in open(os.path.join(d, 'template_certs.jsonl'))]
C = [json.loads(l) for l in open(os.path.join(d, 'core_certs.jsonl'))]
need_noct = sorted({len(t['core']) for t in T if 'octs' in t} | {len(c['support']) for c in C if 'octs' in c})
need_oct = sorted({len(t['core']) for t in T if 'octs' not in t})
H = lambda txt: hashlib.sha256(txt.encode()).hexdigest()
static_ok = {}
for n, octagon in [(n, False) for n in need_noct] + [(n, True) for n in need_oct]:
    cnf = coupled5.CNF(list(range(n)), static=True, octagon=octagon)
    cls = [c for c, t in zip(cnf.clauses, cnf.tags) if t is None]
    fresh = f'{cnf.nv} {len(cls)}\n' + ''.join(' '.join(map(str, c)) + ' 0\n' for c in cls)
    del cnf, cls
    p = os.path.join('static', f'static{"" if octagon else "noct"}_A4_B4_{n}.txt')
    static_ok[f'{"oct" if octagon else "noct"}{n}'] = (open(p).read() == fresh)
    del fresh
    print(json.dumps({'static': p, 'equal': static_ok[f'{"oct" if octagon else "noct"}{n}'], 'secs': round(time.time() - t0, 1)}), flush=True)
def template_text(core, tests, octs):
    if octs is not None:
        return bigcore.template_text(list(core), [list(e) for e in octs], [tuple(t) for t in tests])
    nv, nc, body = coupled5._static(len(core))
    dyn = coupled5.CNF(list(core), static=False)
    keep = set(tuple(t) for t in tests)
    cls = [c for c, t in zip(dyn.clauses, dyn.tags) if t in keep]
    return f'p cnf {nv} {nc + len(cls)}\n' + body + ''.join(' '.join(map(str, c)) + ' 0\n' for c in cls)
tm = 0; tbad = []
for r in T:
    ok = r['verdict'] == 's VERIFIED UNSAT' and H(template_text(r['core'], r['tests'], r.get('octs'))) == r['cnf_sha256']
    tm += ok
    if not ok: tbad.append(r['id'])
cm = 0; cbad = []
for r in C:
    S = r['support']
    txt = bigcore.template_text(list(S), [list(e) for e in r['octs']], None) if 'octs' in r else coupled5.CNF(list(S)).dimacs()
    ok = r['verdict'] == 's VERIFIED UNSAT' and H(txt) == r['cnf_sha256']
    cm += ok
    if not ok: cbad.append(S)
res = {'tcert': d, 'static_files_equal_to_fresh': static_ok, 'all_static_equal': all(static_ok.values()),
       'templates': len(T), 'templates_hash_match': tm, 'templates_bad': tbad[:10], 'cores': len(C), 'cores_hash_match': cm, 'cores_bad': cbad[:10],
       'ALL_OK': all(static_ok.values()) and tm == len(T) and cm == len(C), 'seconds': round(time.time() - t0, 1)}
json.dump(res, open(os.path.join(d, 'recheck.json'), 'w'), indent=1); print(json.dumps(res), flush=True)
