#!/usr/bin/env python3
"""Cost probe for one hull case (or the unsplit CNF with U = L = '-').
  probe_case.py CNF U L DEPTH NSAMPLE TIMEOUT SEED WORKDIR [JOBS]
Writes the case CNF, runs `march_cu CASE -d DEPTH -o cubes`, then solves NSAMPLE cubes chosen
uniformly at random (seeded) with `cadical -t TIMEOUT` on CASE + cube units, JOBS at a time.
Prints one JSON line: march time, cube count, refuted count, per-sample times/results.
Estimate of the case cost (core-seconds, censored at TIMEOUT) = ncubes * mean(sample time).
"""
import json, os, random, re, subprocess, sys, time, hashlib
from concurrent.futures import ThreadPoolExecutor
HERE = os.path.dirname(os.path.abspath(__file__)); BIN = os.environ.get("BIN", "/tmp/claude-0/w/bin")
cnf, U, L, D, K, T, seed, W = sys.argv[1:9]; jobs = int(sys.argv[9]) if len(sys.argv) > 9 else 1
D, K, T, seed = int(D), int(K), int(T), int(seed)
name = "FULL" if U == "-" else f"U{U.replace(',', '-')}_L{L.replace(',', '-')}"
d = os.path.join(W, f"probe_{name}_{os.getpid()}"); os.makedirs(d, exist_ok=True)
case = os.path.join(d, "case.cnf")
if U == "-": os.symlink(os.path.abspath(cnf), case)
else: subprocess.run([sys.executable, os.path.join(HERE, "hullsplit.py"), "case", cnf, U, L, case], check=True)
sha = hashlib.sha256(open(case, "rb").read()).hexdigest()
t0 = time.time()
mo = subprocess.run([os.path.join(BIN, "march_cu"), case, "-d", str(D), "-o", os.path.join(d, "cubes")],
                    capture_output=True, text=True).stdout
mt = time.time() - t0
m = re.search(r"number of cubes (\d+), including (\d+) refuted", mo)
cubes = [l.split()[1:-1] for l in open(os.path.join(d, "cubes")) if l.startswith("a")]
body = open(case).read().split("\n", 1); hdr = body[0].split()
rng = random.Random(seed); pick = rng.sample(range(len(cubes)), min(K, len(cubes)))
def solve(i):
    f = os.path.join(d, f"c{i}.cnf")
    with open(f, "w") as o:
        o.write(f"p cnf {hdr[2]} {int(hdr[3]) + len(cubes[i])}\n"); o.write(body[1])
        o.write("".join(f"{l} 0\n" for l in cubes[i]))
    s = time.time(); r = subprocess.run([os.path.join(BIN, "cadical"), "-q", "-t", str(T), f], stdout=subprocess.DEVNULL).returncode
    os.remove(f); out = {"i": i, "rc": r, "s": round(time.time() - s, 2)}
    if r == 10: out["cube"] = cubes[i]   # SAT: keep the cube so the model can be reproduced
    return out
with ThreadPoolExecutor(jobs) as ex: res = list(ex.map(solve, pick))
mean = sum(r["s"] for r in res) / max(1, len(res))
print(json.dumps({"case": name, "cnf_sha256": sha, "depth": D, "march_s": round(mt, 1), "ncubes": len(cubes),
                  "march_line": m.group(0) if m else None, "timeout": T, "samples": res,
                  "closed": sum(r["rc"] == 20 for r in res), "sat": sum(r["rc"] == 10 for r in res),
                  "est_core_s_censored": round(len(cubes) * mean + mt, 1)}))
subprocess.run(["rm", "-rf", d])
