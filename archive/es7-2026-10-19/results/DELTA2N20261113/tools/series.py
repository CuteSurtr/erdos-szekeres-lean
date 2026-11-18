"""Run eager_cert.py for m = m0..m1 for fixed (a, n, form); stop at the first case that is not UNSAT (timeout or SAT)
or when the base formula alone is UNSAT (then no valid signotope exists for larger m either)."""
import sys, subprocess, json, os
a, n, form, m0, m1, tl = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3], int(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6])
out = sys.argv[7] if len(sys.argv) > 7 else 'eager'
PY = sys.executable
def last():
    return json.loads(open(os.path.join(out, 'results.jsonl')).read().splitlines()[-1])
for m in range(m0, m1 + 1):
    subprocess.run([PY, 'eager_cert.py', str(a), str(n), str(m), 'base', '--tl', str(tl), '--out', out])
    r = last()
    if r['status'] == 'UNSAT': print('base UNSAT at m =', m, flush=True); break
    subprocess.run([PY, 'eager_cert.py', str(a), str(n), str(m), form, '--tl', str(tl), '--out', out])
    r = last()
    if r['status'] != 'UNSAT': print('stop at m =', m, r['status'], flush=True); break
