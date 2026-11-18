"""Certify each new row: full coupled CNF for its support, CaDiCaL LRAT proof, cake_lpr check.
A row counts as CERTIFIED only on cake_lpr's 's VERIFIED UNSAT' line (lrat-check is unsound).
Results append to certified.jsonl (support, cnf sha256, lrat sha256, verdict)."""
import hashlib, json, os, subprocess, sys, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import coupled

CAKE = os.path.expanduser('~/.local/bin/cake_lpr')
OUT = os.path.join(HERE, 'certified.jsonl')
WD = os.path.join(HERE, 'cert'); os.makedirs(WD, exist_ok=True)

def done():
    s = set()
    if os.path.exists(OUT):
        for line in open(OUT):
            r = json.loads(line); s.add(tuple(r['support']))
    return s

def certify(S):
    cnf = coupled.CNF(S)
    txt = cnf.dimacs()
    h = hashlib.sha256(txt.encode()).hexdigest()
    p = os.path.join(WD, h[:16] + '.cnf'); q = p[:-4] + '.lrat'
    open(p, 'w').write(txt)
    r = subprocess.run(['cadical', '-q', '--lrat=true', '--binary=false', p, q], capture_output=True, text=True)
    if r.returncode != 20:
        os.remove(p); return {'support': S, 'cnf_sha256': h, 'verdict': f'cadical exit {r.returncode}'}
    lh = hashlib.sha256(open(q, 'rb').read()).hexdigest()
    c = subprocess.run([CAKE, p, q], capture_output=True, text=True)
    ok = 's VERIFIED UNSAT' in c.stdout
    os.remove(p); os.remove(q)
    return {'support': S, 'cnf_sha256': h, 'lrat_sha256': lh,
            'verdict': 's VERIFIED UNSAT' if ok else ('cake_lpr: ' + (c.stdout + c.stderr)[-200:])}

if __name__ == '__main__':
    have = done()
    rows = json.load(open(os.path.join(HERE, 'newrows.json')))
    import random
    mode = sys.argv[1] if len(sys.argv) > 1 else 'cores'
    if mode == 'cores':
        rows = [r for r in rows if r.get('kind') in (None, 'core')]
    else:  # sample of transported rows
        tr = [r for r in rows if r.get('kind') == 'transport']
        rows = random.Random(int(mode)).sample(tr, min(150, len(tr)))
    n = 0
    with open(OUT, 'a') as f:
        for r in rows:
            S = sorted(r['support'])
            if tuple(S) in have: continue
            t = time.time(); res = certify(S); res['seconds'] = round(time.time() - t, 1)
            f.write(json.dumps(res) + '\n'); f.flush(); have.add(tuple(S)); n += 1
            print(res['verdict'], len(S), res['seconds'], flush=True)
    print('certified this run:', n)
