#!/usr/bin/env python3
"""Extra satcount validation where m = 0 faces exist: heptagon-free 31-point
sets (inputs/starts_K7_a.txt) are not saturated.  For each set: the number of
faces with m = 0 must equal sat.c's count of distinct bad faces (sat.c writes
one line per bad candidate with the face sign vector), every lattice point
found in an m = 0 / m = 1 face is recounted with cgon, and random points are
compared (satcount test vs cgon recount).

usage: calib_m0.py OUTJSON NSETS
"""
import os, sys, json, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dlib
from dlib import b

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
WORK = os.environ.get("DWORK", "/tmp")
out = {}
lines = open(os.path.join(ROOT, "inputs", "starts_K7_a.txt")).read().splitlines()
rng = random.Random(11)
for li in rng.sample(range(len(lines)), int(sys.argv[2])):
    f = lines[li].split()
    P = dlib.parse_line_pts(f, 3)
    assert dlib.cgon_count(P, 7)[7] == 0
    p = os.path.join(WORK, f"m0_{li}.txt"); fp = p + ".faces"; bp = p + ".bad"
    dlib.write_pts(p, P)
    st = dlib.satcount_sweep(p, 7, fp, 1, 3)
    r = dlib.run([b("sat"), "sat", p, "7", bp])
    sj = json.loads(r.stdout.strip().splitlines()[-1])
    badfaces = set(l.split()[-1] for l in open(bp))
    F = dlib.read_faces(fp)
    pm = [(fc["px"], fc["py"], fc["m"]) for fc in F if fc["ok"]]
    rng.shuffle(pm)
    pm = pm[:200]
    mism = 0
    for x, y, m in pm:
        c = dlib.cgon_count(P + [(x, y)], 7)
        if c[7] != m:
            mism += 1
    rp = []
    xs = [x for x, _ in P]; ext = max(xs) - min(xs)
    while len(rp) < 200:
        q = rng.choice(P); s = 2 ** rng.uniform(0, ext.bit_length() + 1)
        rp.append((q[0] + int(rng.uniform(-s, s)), q[1] + int(rng.uniform(-s, s))))
    t = dlib.run([b("satcount"), "test", p, "7"], "".join(f"{x} {y}\n" for x, y in rp)).stdout.split()
    mism2 = 0; chk = 0; h = {}
    for (x, y), m in zip(rp, t):
        if m == "degenerate":
            continue
        c = dlib.cgon_count(P + [(x, y)], 7)
        if c is None:
            continue
        chk += 1
        h[min(c[7], 3)] = h.get(min(c[7], 3), 0) + 1
        if int(m) != c[7]:
            mism2 += 1
    out[f"starts_K7_a_line{li}"] = {"satcount_m0_faces": st["m0"], "sat_bad_distinct_faces": len(badfaces),
                                    "sat_bad_candidates": sj["bad_candidates"], "complete": st["complete"],
                                    "m1_faces": st["m1"], "face_points_checked": len(pm), "face_point_mismatches": mism,
                                    "random_points_checked": chk, "random_point_mismatches": mism2, "random_hist_min3": h}
    for q in (p, fp, bp):
        os.unlink(q)
    print(li, out[f"starts_K7_a_line{li}"], flush=True)
json.dump(out, open(sys.argv[1], "w"), indent=1)
