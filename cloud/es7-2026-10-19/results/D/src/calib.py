#!/usr/bin/env python3
"""Task D calibration.

1. k = 6: every hexagon-free 16-point set must be saturated (ES(6) = 17).
   Sets: classical ES(6) construction and two symmetric 16-point sets from
   tools/decomp/sets.py, plus annealed hexagon-free sets from gen walk.
   Each set is checked with sat.c (K=6: bad_candidates must be 0) and with
   satcount.c (m0 must be 0), both with Euler-complete face enumeration.
2. k = 6 null: m=1 face counts for deletions of one-hexagon 17-point sets.
3. k = 7: AlphaEvolve's 33-point set, exact counts (verify_exact.py on the
   exact binary fractions of the floats; cgon.c on an integer realization with
   the same orientation signs).
4. satcount validation: m at sampled points vs cgon recounts of S + {p}.
"""
import os, sys, json, random, time, subprocess, tempfile
from fractions import Fraction
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dlib
from dlib import b
import verify_exact

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
OUT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "calib"))
WORK = os.environ.get("DWORK", "/tmp")
os.makedirs(OUT, exist_ok=True)
NPROC = int(os.environ.get("NPROC", "14"))
T0 = time.time()
summary = {}


def tmpfile(tag):
    fd, p = tempfile.mkstemp(prefix=tag, suffix=".txt", dir=WORK)
    os.close(fd)
    return p


def sat_json(path, K):
    r = dlib.run([b("sat"), "sat", path, str(K)])
    return json.loads(r.stdout.strip().splitlines()[-1])


def check_k6(P):
    p = tmpfile("k6_")
    dlib.write_pts(p, P)
    c = dlib.cgon_count(P, 6)
    s = sat_json(p, 6)
    sc = dlib.satcount_sweep(p, 6)
    os.unlink(p)
    return {"c6": c[6], "sat_bad": s["bad_candidates"], "sat_complete": s["faces_euler"] == s["faces_hit_by_valid_candidates"],
            "satcount_m0": sc["m0"], "satcount_m1": sc["m1"], "satcount_m2": sc["m2"], "satcount_complete": sc["complete"],
            "faces": sc["faces_euler"]}


# ---------------- 1. k = 6 saturation ----------------
sys.path.insert(0, os.path.join(ROOT, "tools", "decomp"))
import sets as decomp_sets  # noqa: E402

classical = {}
es6 = decomp_sets.ES(6)
classical["ES6_classical"] = [(Fraction(x), Fraction(y)) for x, y in es6]
classical["four_fold_16"] = [(Fraction(str(x)), Fraction(str(y))) for x, y in decomp_sets.four]
classical["five_fold_16"] = [(Fraction(x), Fraction(y)) for x, y in decomp_sets.five]
cl_res = {}
for name, P in classical.items():
    gp, why = verify_exact.general_position(P)
    ex = verify_exact.count_convex(P, 6) if gp else None
    Q, bits = dlib.integerize(P, 24, 29)
    r = {"n": len(P), "general_position_exact": gp, "exact_counts": ex and {str(k): v for k, v in ex.items()},
         "integer_realization_bits": bits}
    if Q is not None:
        r.update(check_k6(Q))
    cl_res[name] = r
summary["k6_classical"] = cl_res
print("classical", json.dumps(cl_res), flush=True)

# annealed hexagon-free 16-point sets
k6file = os.path.join(WORK, "k6walk.txt")
if os.path.exists(k6file):
    os.unlink(k6file)
def genwalk(seed):
    out = os.path.join(WORK, f"k6walk_{seed}.txt")
    if os.path.exists(out):
        os.unlink(out)
    dlib.run([b("gen"), "walk", "6", "16", str(seed), "12", "random:1000000", "200000", "1.0", "0.01", "500", "100", out])
    return out
with ThreadPoolExecutor(NPROC) as ex:
    outs = list(ex.map(genwalk, range(1, NPROC + 1)))
sets16 = {}
for o in outs:
    for line in open(o):
        f = line.split()
        if int(f[1]) != 0:
            continue
        sets16.setdefault(f[3], dlib.parse_line_pts(f, 4))
print("k6 annealed distinct order types:", len(sets16), flush=True)
with ThreadPoolExecutor(NPROC) as ex:
    res = list(ex.map(check_k6, list(sets16.values())))
agg = {"sets": len(res), "all_hexagon_free": all(r["c6"] == 0 for r in res),
       "sat_bad_total": sum(r["sat_bad"] for r in res), "sat_all_complete": all(r["sat_complete"] for r in res),
       "satcount_m0_total": sum(r["satcount_m0"] for r in res), "satcount_all_complete": all(r["satcount_complete"] for r in res),
       "m1_faces_per_set": sorted(r["satcount_m1"] for r in res)}
summary["k6_annealed"] = agg
print("k6 annealed", {k: v for k, v in agg.items() if k != "m1_faces_per_set"}, flush=True)

# ---------------- 2. k = 6 null: deletions of one-hexagon 17-point sets ----------------
def gennear(seed):
    out = os.path.join(WORK, f"k6near_{seed}.txt")
    if os.path.exists(out):
        os.unlink(out)
    dlib.run([b("gen"), "near", "6", "17", str(seed), "6", "random:1000000", "200000", "1.0", "0.01", "300", "100", out])
    return out
with ThreadPoolExecutor(NPROC) as ex:
    outs = list(ex.map(gennear, range(101, 101 + NPROC)))
near16 = {}
zero17 = 0
for o in outs:
    for line in open(o):
        f = line.split()
        if f[0].startswith("ZERO"):
            zero17 += 1
            continue
        near16.setdefault(f[3], dlib.parse_line_pts(f, 4))
with ThreadPoolExecutor(NPROC) as ex:
    resn = list(ex.map(check_k6, list(near16.values())))
summary["k6_null"] = {"deletions": len(resn), "zero_17_point_sets (must be 0)": zero17,
                      "sat_bad_total": sum(r["sat_bad"] for r in resn),
                      "satcount_m0_total": sum(r["satcount_m0"] for r in resn),
                      "m1_faces": sorted(r["satcount_m1"] for r in resn),
                      "faces": sorted(set(r["faces"] for r in resn))}
print("k6 null", len(resn), "m0 total", summary["k6_null"]["satcount_m0_total"], flush=True)

# ---------------- 3. k = 7 AlphaEvolve ----------------
ae = json.load(open(os.path.join(ROOT, "inputs", "alphaevolve_pts.json")))
P = [(Fraction(x), Fraction(y)) for x, y in ae["points_7"]]
gp, why = verify_exact.general_position(P)
exc = verify_exact.count_convex(P, 8)
hepts = verify_exact.list_kgons(P, 7)
Q, bits = dlib.integerize(P, 26, 29)
aer = {"n": len(P), "general_position_exact": gp, "exact_counts_fraction": {str(k): v for k, v in exc.items()},
       "heptagons_exact": hepts, "integer_realization_bits": bits}
if Q is not None:
    c = dlib.cgon_count(Q, 8)
    aer["cgon_counts_integer"] = {str(k): v for k, v in c.items()}
    exq = verify_exact.count_convex(Q, 8)
    aer["exact_counts_integer"] = {str(k): v for k, v in exq.items()}
    dlib.write_pts(os.path.join(OUT, "alphaevolve_int.txt"), Q)
    aer["integer_points_file"] = "calib/alphaevolve_int.txt"
summary["k7_alphaevolve"] = aer
print("alphaevolve", json.dumps(aer), flush=True)

# ---------------- 4. satcount validation at sampled points ----------------
def validate(P, K, nsamp, seed):
    rng = random.Random(seed)
    base = dlib.cgon_count(P, K)[K]
    p = tmpfile("val_")
    dlib.write_pts(p, P)
    fp = p + ".faces"
    sw = dlib.satcount_sweep(p, K, fp, 1, 3)
    faces = dlib.read_faces(fp)
    pts = []
    xs = [x for x, _ in P]; ys = [y for _, y in P]
    ext = max(max(xs) - min(xs), max(ys) - min(ys))
    while len(pts) < nsamp:
        q = rng.choice(P)
        sc = 2 ** rng.uniform(0, max(1, ext.bit_length() + 1))
        pts.append((q[0] + int(rng.uniform(-sc, sc)), q[1] + int(rng.uniform(-sc, sc))))
    face_pts = [(f["px"], f["py"], f["m"]) for f in faces if f["ok"]]
    rng.shuffle(face_pts)
    face_pts = face_pts[:nsamp]
    allp = pts + [(x, y) for x, y, _ in face_pts]
    r = dlib.run([b("satcount"), "test", p, str(K)], "".join(f"{x} {y}\n" for x, y in allp))
    ms = r.stdout.split()
    mism = 0; checked = 0; facemism = 0; hist = {}
    for i, (x, y) in enumerate(allp):
        if ms[i] == "degenerate":
            continue
        c = dlib.cgon_count(P + [(x, y)], K)
        if c is None:
            continue
        checked += 1
        mm = c[K] - base
        hist[min(mm, 3)] = hist.get(min(mm, 3), 0) + 1
        if int(ms[i]) != mm:
            mism += 1
        if i >= len(pts):
            fm = face_pts[i - len(pts)][2]
            if fm != min(mm, 3):
                facemism += 1
    os.unlink(p); os.unlink(fp)
    return {"K": K, "base_count": base, "checked": checked, "mismatch_test_vs_cgon": mism,
            "face_points_checked": len(face_pts), "mismatch_face_m_vs_cgon": facemism, "hist_min3": hist,
            "sweep": {k: sw[k] for k in ("m0", "m1", "m2", "m3plus", "complete")}}

val = {}
jobs = []
for i, P in enumerate(list(sets16.values())[:6]):
    jobs.append((f"k6_set{i}", P, 6))
for i, P in enumerate(list(near16.values())[:6]):
    jobs.append((f"k6_null{i}", P, 6))
# k = 7: deletions of the first nearfull seed and a non-heptagon-free 32-set
nf = open(os.path.join(ROOT, "inputs", "nearfull_p2c.txt")).readline().split()
S33 = dlib.parse_line_pts(nf, 2)
for v in range(33):
    S = S33[:v] + S33[v + 1:]
    if dlib.cgon_count(S, 7)[7] == 0:
        jobs.append((f"k7_p2c0_drop{v}", S, 7))
pool = open(os.path.join(ROOT, "inputs", "distinct_K7.txt")).readline().split()
jobs.append(("k7_pool0_with_heptagons", dlib.parse_line_pts(pool, 3), 7))
if Q is not None:
    jobs.append(("k7_alphaevolve33_with_one_heptagon", Q, 7))
with ThreadPoolExecutor(NPROC) as ex:
    futs = {name: ex.submit(validate, P, K, 150, hash(name) & 0xffff) for name, P, K in jobs}
    for name, f in futs.items():
        val[name] = f.result()
summary["satcount_validation"] = val
tot = sum(v["checked"] for v in val.values()); mm = sum(v["mismatch_test_vs_cgon"] + v["mismatch_face_m_vs_cgon"] for v in val.values())
summary["satcount_validation_total"] = {"points_checked": tot, "mismatches": mm}
print("validation points", tot, "mismatches", mm, flush=True)
summary["wall_seconds"] = round(time.time() - T0, 1)
json.dump(summary, open(os.path.join(OUT, "calib_summary.json"), "w"), indent=1)
print("done", summary["wall_seconds"])
