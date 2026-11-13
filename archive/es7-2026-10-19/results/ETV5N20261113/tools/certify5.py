"""Certify rows: full coupled CNF (uncached builder) for each support, CaDiCaL 2.1.3 LRAT, cake_lpr.
A row counts as CERTIFIED only on cake_lpr's 's VERIFIED UNSAT'.  Appends to certified.jsonl
(support, cnf sha256, lrat sha256, verdict); CNF and LRAT are deleted after the hashes are recorded.
usage: certify5.py <supports.json | jsonl-with-'support'> [max]"""
import hashlib, json, os, subprocess, sys, time
HERE = os.path.dirname(os.path.abspath(__file__))
import coupled5
CAKE = os.path.expanduser('~/.local/bin/cake_lpr')
OUT = os.environ.get('CERT_OUT', os.path.join(HERE, 'certified.jsonl'))
WD = os.path.join(HERE, 'cert'); os.makedirs(WD, exist_ok=True)

def done():
    s = {}
    if os.path.exists(OUT):
        for line in open(OUT):
            r = json.loads(line); s[tuple(r['support'])] = r['verdict']
    return s

def certify(S):
    cnf = coupled5.CNF(S)
    txt = cnf.dimacs(); h = hashlib.sha256(txt.encode()).hexdigest()
    p = os.path.join(WD, h[:16] + '.cnf'); q = p[:-4] + '.lrat'
    open(p, 'w').write(txt)
    r = subprocess.run(['cadical', '-q', '--lrat=true', '--binary=false', p, q], capture_output=True, text=True)
    if r.returncode != 20:
        os.remove(p)
        if os.path.exists(q): os.remove(q)
        return {'support': S, 'cnf_sha256': h, 'verdict': f'cadical exit {r.returncode}'}
    lh = hashlib.sha256(open(q, 'rb').read()).hexdigest()
    c = subprocess.run([CAKE, p, q], capture_output=True, text=True)
    ok = 's VERIFIED UNSAT' in c.stdout
    os.remove(p); os.remove(q)
    return {'support': S, 'cnf_sha256': h, 'lrat_sha256': lh,
            'verdict': 's VERIFIED UNSAT' if ok else ('cake_lpr: ' + (c.stdout + c.stderr)[-200:])}

if __name__ == '__main__':
    src = sys.argv[1]; mx = int(sys.argv[2]) if len(sys.argv) > 2 else 10**9
    if src.endswith('.jsonl'):
        sups = [json.loads(l)['support'] for l in open(src)]
    else:
        sups = json.load(open(src))
        sups = [x[0] if isinstance(x[0], list) else x for x in sups]   # accept [[support, demand], ...]
    part = os.environ.get('CERT_PART')   # 'k/m': take every m-th support starting at k
    if part:
        k, m = map(int, part.split('/')); sups = sups[k::m]
    only1 = os.environ.get('CERT_DEMAND1')
    if only1:
        full = json.load(open(src)); sups = [x[0] for x in full if x[1] == 1]
        if part: sups = sups[k::m]
    have = done(); n = 0
    with open(OUT, 'a') as f:
        for S in sups:
            S = sorted(S)
            if tuple(S) in have: continue
            t = time.time(); res = certify(S); res['seconds'] = round(time.time() - t, 2)
            f.write(json.dumps(res) + '\n'); f.flush(); have[tuple(S)] = res['verdict']; n += 1
            print(res['verdict'], len(S), res['seconds'], flush=True)
            if n >= mx: break
    print('certified this run:', n)
