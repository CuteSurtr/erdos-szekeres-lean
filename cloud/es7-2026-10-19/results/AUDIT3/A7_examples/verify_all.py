#!/usr/bin/env python3
"""A7 audit driver: independent exact verification of every lower-bound example.
usage: python3 -I verify_all.py OUTDIR [name ...]"""
import json, os, random, struct, subprocess, sys, time
from decimal import Decimal
from functools import cmp_to_key
from itertools import combinations
from math import comb

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import a7lib as L

R = os.environ.get("ES7_RESULTS", ".")

# name, path, fmt, claimed maps, K, claimed size, claimed centre-in-set (None = not claimed), claimed axis count
EX = [
    ("c3_27", R + "/SYMMAX/c3_27points.txt", "EIS", ["C3E"], 7, 27, None, None),
    ("c3_30", R + "/SYMMAX/c3_30points.txt", "EIS", ["C3E"], 7, 30, False, None),
    ("c3_31", R + "/SYMMAX/c3_31points.txt", "EIS", ["C3E"], 7, 31, True, None),
    ("c4_28", R + "/SYMMAX/c4_28points.txt", "Z2", ["C4"], 7, 28, False, None),
    ("c5_30", R + "/SYMMAX/c5_30points.txt", "Z5", ["C5"], 7, 30, False, None),
    ("c5_31", R + "/SYMMAX/c5_31points.txt", "Z5", ["C5"], 7, 31, True, None),
    ("c6_30", R + "/SYMMAX/c6_30points.txt", "EIS", ["C6E", "C3E"], 7, 30, False, None),
    ("mirror_32", R + "/SYMMAX/mirror_32points.txt", "Z2", ["M"], 7, 32, None, 0),
    ("k6_c2_16", R + "/SYMMAX/k6/c2_16points.txt", "Z2", ["C2"], 6, 16, False, None),
    ("k6_c3_13", R + "/SYMMAX/k6/c3_13points.txt", "EIS", ["C3E"], 6, 13, True, None),
    ("k6_c4_16", R + "/SYMMAX/k6/c4_16points.txt", "Z2", ["C4"], 6, 16, False, None),
    ("k6_c5_16", R + "/SYMMAX/k6/c5_16points.txt", "Z5", ["C5"], 6, 16, True, None),
    ("k6_mirror_12", R + "/SYMMAX/k6/mirror_12points.txt", "Z2", ["M"], 6, 12, None, 2),
    ("sym2_32", R + "/SYM2/sym7_32points.txt", "Z2", ["C2"], 7, 32, False, None),
    ("c5_31minus_centre", R + "/SYM5/c5_31minus_centre.txt", "Z5", ["C5"], 7, 30, False, None),
]

# extra maps tested for information (other possible symmetries)
EXTRA = {
    "Z2": {"C2": L.MAPS["C2"], "C4": L.MAPS["C4"], "M_y-axis": L.MAPS["M"], "M_x-axis": lambda p: (p[0], -p[1]),
           "M_diag": lambda p: (p[1], p[0]), "M_antidiag": lambda p: (-p[1], -p[0])},
    "EIS": {"C3E": L.MAPS["C3E"], "C6E": L.MAPS["C6E"], "C2E": lambda p: (-p[0], -p[1]),
            "conj(real-axis mirror)": lambda p: (p[0] - p[1], -p[1])},
    "Z5": {"C5": L.MAPS["C5"], "neg(half-turn)": lambda p: tuple(-t for t in p),
           "conj(real-axis mirror)": lambda p: (p[0] - p[1], -p[1], p[3] - p[1], p[2] - p[1])},
}

def rot_numeric(xy, mapname):
    x, y = xy
    if mapname == "M":
        return (-x, y)
    th = L.ANGLE_DEG[mapname]
    half3 = Decimal(3).sqrt() / 2
    cs = {180: (Decimal(-1), Decimal(0)), 90: (Decimal(0), Decimal(1)), 120: (Decimal(-1) / 2, half3),
          60: (Decimal(1) / 2, half3), 72: (L.COS[1], L.SIN[1])}[th]
    c, s = cs
    return (x * c - y * s, x * s + y * c)

def check_example(name, path, fmt, maps, K, nclaim, centre_claim, axis_claim, outdir, rng):
    t0 = time.time()
    res = {"name": name, "path": path, "fmt": fmt, "K": K, "claimed_size": nclaim}
    pts, anomalies = L.parse(path, fmt)
    n = len(pts)
    res["parsed_points"] = n
    res["parse_anomalies"] = anomalies
    res["size_ok"] = (n == nclaim)
    res["distinct"] = len(set(pts)) == n
    aff = [L.affine_coords(p, fmt) for p in pts]
    res["distinct_affine"] = len(set(aff)) == n
    res["max_abs_native_coordinate"] = max(abs(c) for p in pts for c in p)
    # ---------------- symmetry
    origin = tuple([0] * len(pts[0]))
    res["origin_in_set"] = origin in set(pts)
    res["centre_claim_ok"] = (centre_claim is None) or (res["origin_in_set"] == centre_claim)
    sym = {}
    Sset = set(pts)
    for m in maps:
        g = L.MAPS[m]
        inv = all(g(p) in Sset for p in pts)
        orbs = L.orbits(pts, g)
        sizes = sorted(len(o) for o in orbs)
        # numeric confirmation that the exact integer map is the claimed Euclidean isometry
        maxerr = Decimal(0)
        for p in pts:
            a = rot_numeric(L.true_xy(p, fmt), m)
            b = L.true_xy(g(p), fmt)
            e = max(abs(a[0] - b[0]), abs(a[1] - b[1]))
            maxerr = max(maxerr, e)
        sym[m] = {"invariant": inv, "orbit_sizes": sizes, "num_orbits": len(orbs),
                  "fixed_points": sum(1 for p in pts if g(p) == p),
                  "numeric_isometry_max_error": "%.3e" % maxerr}
    res["symmetry"] = sym
    if axis_claim is not None:
        res["points_on_mirror_axis"] = sum(1 for p in pts if p[0] == 0)
        res["axis_claim_ok"] = res["points_on_mirror_axis"] == axis_claim
    extra = {}
    for en, g in EXTRA[fmt].items():
        extra[en] = all(g(p) in Sset for p in pts)
    res["other_symmetries_tested"] = extra
    # ---------------- orientations, three methods
    OA = L.orient_table(pts, fmt, L.orient_A)
    zeros = 0
    mism_B = 0
    mism_C = 0
    minrel = None
    for i, j, k in combinations(range(n), 3):
        a = OA[i][j][k]
        if a == 0:
            zeros += 1
        b = L.orient_B(pts[i], pts[j], pts[k], fmt)
        if b != a:
            mism_B += 1
        c = L.orient_C(pts[i], pts[j], pts[k], fmt)
        sc = (c > 0) - (c < 0)
        if sc != a:
            mism_C += 1
        if minrel is None or abs(c) < minrel:
            minrel = abs(c)
    res["collinear_triples"] = zeros
    res["orient_methodB_mismatches"] = mism_B
    res["orient_numeric_mismatches"] = mism_C
    res["min_abs_numeric_cross"] = "%.6e" % minrel
    # ---------------- DP with four different linear orders
    base_cmp = L.lex_key_cmp(fmt)
    if fmt in ("Z2", "EIS"):
        def swap_cmp(p, q):
            a, b = L.affine_coords(p, fmt), L.affine_coords(q, fmt)
            a, b = (a[1], a[0]), (b[1], b[0])
            return (a > b) - (a < b)
    else:
        def swap_cmp(p, q):
            A, B = L.affine_coords(p, fmt), L.affine_coords(q, fmt)
            c = L.r5_cmp(A[1], B[1])
            return c if c else L.r5_cmp(A[0], B[0])
    idx_sorted = sorted(range(n), key=cmp_to_key(lambda i, j: base_cmp(pts[i], pts[j])))
    idx_sorted2 = sorted(range(n), key=cmp_to_key(lambda i, j: swap_cmp(pts[i], pts[j])))
    # strictness of the orders (injective functional): no ties
    ties1 = sum(1 for a, b in zip(idx_sorted, idx_sorted[1:]) if base_cmp(pts[a], pts[b]) == 0)
    ties2 = sum(1 for a, b in zip(idx_sorted2, idx_sorted2[1:]) if swap_cmp(pts[a], pts[b]) == 0)
    dps = []
    wits = []
    for order in (idx_sorted, idx_sorted[::-1], idx_sorted2, idx_sorted2[::-1]):
        d, w = L.max_convex_dp(OA, order)
        dps.append(d)
        wits.append(w)
    res["order_ties"] = [ties1, ties2]
    res["dp_max_convex_four_orders"] = dps
    # witness verification by two independent criteria
    cmpA = base_cmp
    crossA = lambda o, a, b: L.orient_A(o, a, b, fmt)
    wit_ok = []
    for w in wits:
        coords = [pts[t] for t in w]
        h = L.hull_is_convex_position(coords, cmpA, crossA)
        hp = L.convex_position_halfplane(w, OA)
        wit_ok.append(bool(h and hp and len(set(w)) == len(w)))
    res["dp_witness"] = [pts[t] for t in wits[0]]
    res["dp_witnesses_verified"] = wit_ok
    # ---------------- exhaustive brute force (C), on the exact orientation table
    binp = os.path.join(outdir, name + ".orient.bin")
    with open(binp, "wb") as f:
        f.write(struct.pack("<i", n))
        f.write(bytes((OA[i][j][k] & 0xFF) for i in range(n) for j in range(n) for k in range(n)))
    out = subprocess.run([os.path.join(HERE, "brute_a7"), binp, str(K)], capture_output=True, text=True).stdout
    res["brute_output"] = out.strip().splitlines()
    # ---------------- random-subset cross-check: DP versus exhaustive hull test on the subset
    nsub = 40 if fmt == "Z5" else 60
    mism = 0
    hist = {}
    for _ in range(nsub):
        m = rng.randint(7, min(n, 13))
        sub = sorted(rng.sample(range(n), m))
        order = sorted(sub, key=cmp_to_key(lambda i, j: base_cmp(pts[i], pts[j])))
        d, w = L.max_convex_dp(OA, order)
        # brute force: a convex d-subset exists (search, by hull), and no convex (d+1)-subset (exhaustive, by hull)
        exists_d = any(L.hull_is_convex_position([pts[t] for t in c], cmpA, crossA) for c in combinations(sub, d))
        exists_d1 = (d + 1 <= m) and any(L.hull_is_convex_position([pts[t] for t in c], cmpA, crossA)
                                         for c in combinations(sub, d + 1))
        if not exists_d or exists_d1:
            mism += 1
        hist[d] = hist.get(d, 0) + 1
    res["random_subset_checks"] = {"count": nsub, "mismatches": mism, "dp_value_histogram": hist}
    # ---------------- convex layers (rotation-symmetric sets) and orbit structure of layers
    layers = L.convex_layers(list(range(n)), OA)
    lay = []
    rotmap = None
    for m in maps:
        if m != "M":
            rotmap = L.MAPS[m]
            break
    for layer in layers:
        info = {"size": len(layer)}
        if rotmap is not None:
            orbs = L.orbits(pts, rotmap)
            orb_of = {}
            for oi, o in enumerate(orbs):
                for p in o:
                    orb_of[p] = oi
            info["orbits"] = sorted(set(orb_of[pts[t]] for t in layer))
            info["is_single_orbit"] = len(info["orbits"]) == 1 and len(layer) == len(orbs[info["orbits"][0]])
        lay.append(info)
    res["convex_layers"] = lay
    res["seconds"] = round(time.time() - t0, 1)
    # ---------------- verdict
    brute_ok = False
    brute_k1 = None
    for line in res["brute_output"]:
        if line.startswith("k=%d " % K):
            parts = dict(kv.split("=") for kv in line.split())
            brute_ok = (parts["convex_TRI"] == "0" and parts["convex_WRAP"] == "0" and parts["disagreements"] == "0"
                        and int(parts["subsets"]) == comb(n, K))
        if line.startswith("k=%d " % (K - 1)):
            brute_k1 = dict(kv.split("=") for kv in line.split())
    table_ok = "zero_entries_on_distinct_triples=0 alternation_violations=0" in res["brute_output"][0]
    res["brute_K_minus_1_convex"] = brute_k1
    ok = (res["size_ok"] and res["distinct"] and res["distinct_affine"] and not anomalies
          and all(v["invariant"] for v in sym.values()) and res["centre_claim_ok"]
          and res.get("axis_claim_ok", True) and zeros == 0 and mism_B == 0 and mism_C == 0
          and all(d == K - 1 for d in dps) and all(wit_ok) and brute_ok and table_ok and mism == 0
          and ties1 == 0 and ties2 == 0)
    res["VERDICT"] = "PASS" if ok else "FAIL"
    return res

def main():
    outdir = sys.argv[1]
    names = set(sys.argv[2:])
    rng = random.Random(20261101)
    allres = []
    for ex in EX:
        if names and ex[0] not in names:
            continue
        r = check_example(*ex, outdir, rng)
        allres.append(r)
        print("%-20s n=%-3d K=%d sym=%s centre=%s collinear=%d mB=%d mC=%d dp=%s brute=%s rand_mism=%d layers=%s %s (%.1fs)" % (
            r["name"], r["parsed_points"], r["K"],
            ",".join("%s:%s%s" % (m, "inv" if v["invariant"] else "NOT", v["orbit_sizes"]) for m, v in r["symmetry"].items()),
            r["origin_in_set"], r["collinear_triples"], r["orient_methodB_mismatches"], r["orient_numeric_mismatches"],
            r["dp_max_convex_four_orders"], [l for l in r["brute_output"][1:]],
            r["random_subset_checks"]["mismatches"], [x["size"] for x in r["convex_layers"]], r["VERDICT"], r["seconds"]),
            flush=True)
        with open(os.path.join(outdir, r["name"] + ".json"), "w") as f:
            json.dump(r, f, indent=1, default=str)
    with open(os.path.join(outdir, "summary.json"), "w") as f:
        json.dump(allres, f, indent=1, default=str)

if __name__ == "__main__":
    main()
