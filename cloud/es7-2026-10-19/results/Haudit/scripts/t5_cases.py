#!/usr/bin/env python3
"""Task 5: re-check closed cases from scratch: own case CNF (F + own cube units), CaDiCaL --lrat, cake_lpr.
usage: t5_cases.py SEED NRANDOM NHARD OUT.jsonl"""
import sys, json, random, hashlib, subprocess, time, os
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, '/opt/audit'); import mycube as M
SEED, NR, NH, OUT = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
recs = [json.loads(l) for l in open('/home/user/erdos-szekeres-lean/cloud/es7-2026-10-19/results/Mii-S/cases.jsonl')]
closed = [r for r in recs if r['status'] == 'UNSAT_VERIFIED']
hard = sorted(closed, key=lambda r: -r['solve_s'])[:NH]
rest = [r for r in closed if r not in hard]
pick = hard + random.Random(SEED).sample(rest, NR)
raw = open('/opt/work/F/m33k7int.sub.cnf', 'rb').read(); hdr, body = raw.split(b"\n", 1)
nv, nc = map(int, hdr.split()[2:4])
def run(r):
    w = f"/opt/work/t5/{r['case']}"; os.makedirs(w, exist_ok=True)
    cube = sorted(M.cube(r['U'], r['L']), key=abs)
    data = f"p cnf {nv} {nc + len(cube)}\n".encode() + body + "".join(f"{l} 0\n" for l in cube).encode()
    sha = hashlib.sha256(data).hexdigest()
    open(f"{w}/f.cnf", 'wb').write(data)
    t = time.time(); rc = subprocess.run(['/opt/bin/cadical', '-q', '--lrat', '--binary=false', f"{w}/f.cnf", f"{w}/p.lrat"], stdout=subprocess.DEVNULL).returncode; st = time.time() - t
    pb = os.path.getsize(f"{w}/p.lrat") if os.path.exists(f"{w}/p.lrat") else 0
    t = time.time(); o = subprocess.run(['/opt/bin/cake_lpr', f"{w}/f.cnf", f"{w}/p.lrat"], capture_output=True, text=True).stdout if rc == 20 else ""
    v = next((l for l in o.splitlines() if l.startswith('s ')), o[-100:]); ct = time.time() - t
    subprocess.run(['rm', '-rf', w])
    return {"case": r['case'], "picked": "hardest" if r in hard else "random", "cnf_sha256": sha, "sha_match": sha == r['cnf_sha256'],
            "rc": rc, "solve_s": round(st, 2), "proof_bytes": pb, "cake_lpr": v, "check_s": round(ct, 2),
            "recorded_solve_s": r['solve_s'], "leaves": "single leaf = empty cube (method direct)"}
with ThreadPoolExecutor(3) as ex, open(OUT, 'w') as f:
    for res in ex.map(run, pick): f.write(json.dumps(res) + "\n"); f.flush()
