#!/usr/bin/env python3
"""Independent re-check of saturation on a random sample of distinct sets:
sat.c (with certificate output) then verify.c (different face representatives,
face count F = E - V + 1, certificate-polygon convexity test), plus `cgon
count` confirming the base set has no convex K-gon.

usage: crosscheck.py K samplesize seed [runprefix]
"""
import glob, json, os, random, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
K, m, seed = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
pref = sys.argv[4] if len(sys.argv) > 4 else ""
rows = []
for fn in glob.glob(os.path.join(ROOT, "data", f"distinct_K{K}*.txt")):
    for l in open(fn):
        f = l.split()
        if f[0].startswith(pref):
            rows.append(f)
rng = random.Random(seed)
sample = rng.sample(rows, min(m, len(rows)))
tmp = os.path.join(ROOT, "data", f"tmp_xcheck_{K}_{seed}")
os.makedirs(tmp, exist_ok=True)
ok = bad = 0
for f in sample:
    n = int(f[3]); c = list(map(int, f[4:]))
    pts = list(zip(c[0::2], c[1::2]))
    pf = os.path.join(tmp, "S.txt")
    open(pf, "w").write("".join(f"{x} {y}\n" for x, y in pts))
    cert = os.path.join(tmp, "cert.txt")
    s = json.loads(subprocess.run([os.path.join(ROOT, "bin", "sat"), "sat", pf, str(K), "/dev/null", cert],
                                  capture_output=True, text=True, check=True).stdout)
    v = json.loads(subprocess.run([os.path.join(ROOT, "bin", "verify"), pf, str(K), cert],
                                  capture_output=True, text=True, check=True).stdout)
    cg = subprocess.run([os.path.join(ROOT, "bin", "cgon"), "count", str(K)], input=open(pf).read(),
                        capture_output=True, text=True).stdout
    good = (s["bad_candidates"] == 0 and s["faces_euler"] == s["faces_hit_by_valid_candidates"]
            and v["uncovered_distinct_faces"] == 0 and v["uncovered_candidates"] == 0
            and v["faces_E_minus_V_plus_1"] == v["distinct_faces_hit"] == s["faces_euler"]
            and f" c{K}=0 " in cg)
    ok += good; bad += not good
    if not good:
        print("MISMATCH", f[0], f[1], f[2], s, v, cg.strip(), flush=True)
print(json.dumps(dict(K=K, sampled=len(sample), pool=len(rows), prefix=pref, all_checks_pass=ok, failures=bad)))
