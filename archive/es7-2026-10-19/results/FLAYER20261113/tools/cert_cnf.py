"""Certify a given CNF file: CaDiCaL 2.1.3 LRAT + cake_lpr.  Appends to cert/certified_cnf.jsonl.
usage: cert_cnf.py <file.cnf> [timeout_s]"""
import sys, os, json, time, hashlib, subprocess
CAKE = os.path.expanduser('~/.local/bin/cake_lpr')
p = sys.argv[1]; to = int(sys.argv[2]) if len(sys.argv) > 2 else 0; q = p[:-4] + '.lrat'
def sha(fn):
    h = hashlib.sha256()
    with open(fn, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 24), b''): h.update(chunk)
    return h.hexdigest()
res = {'cnf': os.path.basename(p), 'cnf_sha256': sha(p)}
t0 = time.time()
r = subprocess.run(['/usr/bin/cadical', '-q', '--lrat=true', '--binary=false'] + (['-t', str(to)] if to else []) + [p, q], capture_output=True, text=True)
res['cadical_exit'] = r.returncode; res['cadical_s'] = round(time.time() - t0, 1)
if r.returncode == 20:
    res['lrat_bytes'] = os.path.getsize(q); res['lrat_sha256'] = sha(q)
    t0 = time.time(); c = subprocess.run([CAKE, p, q], capture_output=True, text=True); res['cake_s'] = round(time.time() - t0, 1)
    res['verdict'] = 's VERIFIED UNSAT' if 's VERIFIED UNSAT' in c.stdout else 'cake_lpr: ' + (c.stdout + c.stderr)[-200:]
else: res['verdict'] = 'SAT' if r.returncode == 10 else 'UNKNOWN'
if os.path.exists(q): os.remove(q)
with open(os.path.join(os.path.dirname(os.path.abspath(p)), 'certified_cnf.jsonl'), 'a') as f: f.write(json.dumps(res) + '\n')
print(res, flush=True)
