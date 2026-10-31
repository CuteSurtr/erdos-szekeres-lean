#!/usr/bin/env python3
"""Aggregate Task D runs into results/D/summary.json and the best-set files.

usage: summarize.py RUNSDIR RESULTSDIR [NSAMPLE_BASELINE_SWEEPS]
"""
import os, sys, json, glob, statistics, collections, random, time
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dlib
import walk
import verify_exact
from fractions import Fraction

RUNS, RES = sys.argv[1], sys.argv[2]
NSAMP = int(sys.argv[3]) if len(sys.argv) > 3 else 300
NPROC = int(os.environ.get("NPROC", "8"))


def jl(path):
    out = []
    for f in sorted(glob.glob(path)):
        for line in open(f):
            line = line.strip()
            if line:
                out.append(json.loads(line))
    return out


def dist(v):
    if not v:
        return None
    v = sorted(v)
    q = lambda p: v[min(len(v) - 1, int(p * len(v)))]
    return {"n": len(v), "min": v[0], "p10": q(0.1), "median": q(0.5), "mean": round(statistics.mean(v), 2),
            "p90": q(0.9), "p99": q(0.99), "max": v[-1]}


def hist(v, edges):
    """counts of v in [edges[i], edges[i+1])"""
    res = collections.OrderedDict()
    for i in range(len(edges)):
        lo = edges[i]; hi = edges[i + 1] if i + 1 < len(edges) else None
        key = f"{lo}-{hi - 1}" if hi is not None and hi - 1 != lo else (f"{lo}" if hi is not None else f">={lo}")
        res[key] = sum(1 for x in v if x >= lo and (hi is None or x < hi))
    return res


S = {"generated": time.strftime("%Y-%m-%d %H:%M:%S %Z")}
EDGES_M1 = [0, 1, 10, 50, 100, 200, 500, 1000, 2000, 5000, 10000]

# ---------- calibration ----------
cal = json.load(open(os.path.join(RES, "calib", "calib_summary.json")))
S["calibration"] = {
    "k6_classical": {k: {kk: v[kk] for kk in ("exact_counts", "c6", "sat_bad", "sat_complete", "satcount_m0", "satcount_complete", "satcount_m1", "faces")}
                     for k, v in cal["k6_classical"].items()},
    "k6_annealed_16pt_sets": {k: v for k, v in cal["k6_annealed"].items() if k != "m1_faces_per_set"},
    "k6_null_deletions_of_one_hexagon_17pt_sets": {k: v for k, v in cal["k6_null"].items() if k not in ("m1_faces",)},
    "k6_m1_faces_annealed": dist(cal["k6_annealed"]["m1_faces_per_set"]),
    "k6_m1_faces_null": dist(cal["k6_null"]["m1_faces"]),
    "k6_m1_faces_null_hist": hist(cal["k6_null"]["m1_faces"], EDGES_M1),
    "k7_alphaevolve": cal["k7_alphaevolve"],
    "satcount_validation_total": cal["satcount_validation_total"],
    "satcount_validation_sets": len(cal["satcount_validation"]),
}

# ---------- seed sweep ----------
ss = jl(os.path.join(RUNS, "seedsweep", "seedsweep.jsonl"))
if ss:
    ssum = json.load(open(os.path.join(RUNS, "seedsweep", "seedsweep_summary.json")))
    m1 = [r["m1"] for r in ss]
    S["seed_sweep"] = dict(ssum)
    S["seed_sweep"].update({
        "m1_faces": dist(m1), "m1_faces_hist": hist(m1, EDGES_M1),
        "m1_fraction_of_faces": dist([r["m1"] / r["faces"] for r in ss]),
        "m2_faces": dist([r["m2"] for r in ss]),
        "m1_lattice_realizable_fraction": round(sum(r["m1_lattice_ok"] for r in ss) / max(1, sum(r["m1"] for r in ss)), 4),
        "m1_distinct_blocking_hexagons": dist([r["m1_distinct_blocking_hexagons"] for r in ss]),
        "k6_null_m1_fraction_of_faces": dist([x / 5804.0 for x in cal["k6_null"]["m1_faces"]]),
    })

# ---------- walk ----------
W = jl(os.path.join(RUNS, "walk", "walk_w*.jsonl"))
wsum = {}
for f in sorted(glob.glob(os.path.join(RUNS, "walk", "walk_w*_summary.json"))):
    d = json.load(open(f)); wsum[d["w"]] = d
tabu_union = set()
for f in glob.glob(os.path.join(RUNS, "walk", "walk_w*_tabu.txt")):
    tabu_union |= set(l.strip() for l in open(f) if l.strip())
if W:
    by = collections.defaultdict(list)
    for r in W:
        by[r["w"]].append(r)
    per = {}
    for w, L in sorted(by.items()):
        vis = [r for r in L if r["kind"] == "visit"]
        sm = wsum.get(w, {})
        cpu = (sm.get("cpu_process", 0) + sm.get("cpu_children", 0)) if sm else None
        per[w] = {"strategy": sm.get("strategy"), "states_swept": len(L), "walk_steps": len(vis),
                  "starts_swept": sum(1 for r in L if r["kind"] == "start"), "deadend_jumps": sm.get("deadends"),
                  "wall_s": sm.get("wall"), "cpu_s_total": round(cpu, 1) if cpu else None,
                  "sweep_cpu_s": sm.get("sweep_cpu"),
                  "new_heptagon_free_32_sets_per_cpu_hour": round(len(L) / cpu * 3600, 1) if cpu else None,
                  "m1_faces_on_walk_states": dist([r["m1"] for r in vis]),
                  "m1_faces_first_vs_last_quarter": [statistics.mean([r["m1"] for r in vis[:max(1, len(vis) // 4)]]) if vis else None,
                                                     statistics.mean([r["m1"] for r in vis[-max(1, len(vis) // 4):]]) if vis else None],
                  "m0_faces_total": sum(r["m0"] for r in L)}
    allvis = [r for r in W if r["kind"] == "visit"]
    S["walk"] = {
        "walkers": per,
        "states_swept_total": len(W),
        "distinct_32pt_order_types_visited_union": len(tabu_union) if tabu_union else None,
        "m0_faces_total": sum(r["m0"] for r in W),
        "min_heptagons_at_33_reached": 0 if sum(r["m0"] for r in W) else 1,
        "m1_faces_walk_states": dist([r["m1"] for r in allvis]),
        "m1_faces_walk_states_hist": hist([r["m1"] for r in allvis], EDGES_M1),
        "m1_faces_random_walkers_nearfull_seeds": dist([r["m1"] for r in allvis if per[r["w"]]["strategy"] == "random" and r["w"] < 6]),
        "m1_faces_greedy_walkers_nearfull_seeds": dist([r["m1"] for r in allvis if per[r["w"]]["strategy"] == "greedy"]),
        "m1_faces_random_walkers_anneal_seeds (w6,w7)": dist([r["m1"] for r in allvis if r["w"] >= 6]),
        "m2_faces_walk_states": dist([r["m2"] for r in allvis]),
        "m1_lattice_realizable_fraction": round(sum(r["pt_ok"] for r in W) / max(1, sum(r["pt_ok"] + r["pt_fail"] for r in W)), 4),
        "states_with_no_lattice_m1_face": sum(1 for r in W if r["pt_ok"] == 0),
        "cpu_s_total": round(sum(p["cpu_s_total"] or 0 for p in per.values()), 1),
    }

# ---------- baseline ----------
B = jl(os.path.join(RUNS, "baseline", "baseline_b*.jsonl"))
if B:
    bcpu = sum(r["cpu"] or 0 for r in B)
    sets32 = {}; zero = 0; lines = 0
    for f in glob.glob(os.path.join(RUNS, "baseline", "baseline_b*.txt")):
        for line in open(f):
            fl = line.split()
            lines += 1
            if fl[0].startswith("ZERO"):
                zero += 1
                continue
            sets32.setdefault(walk.h(fl[3]), dlib.parse_line_pts(fl, 4))
    starts_reached = sum(1 for r in B if "no emission" not in (r.get("stderr") or ""))
    S["baseline_random_restarts"] = {
        "starts": len(B), "starts_reaching_E1": starts_reached, "cpu_s": round(bcpu, 1),
        "emitted_heptagon_free_32_sets": lines - zero, "distinct_32pt_order_types": len(sets32),
        "zero_heptagon_33_sets": zero,
        "distinct_32_sets_per_cpu_hour": round(len(sets32) / bcpu * 3600, 1) if bcpu else None,
        "overlap_with_walk_order_types": len(set(sets32) & tabu_union),
    }
    # sweep a random sample of baseline 32-sets: plateau width at random plateau points
    rng = random.Random(7)
    keys = sorted(sets32)
    rng.shuffle(keys)
    keys = keys[:NSAMP]
    tmp = os.path.join(RUNS, "tmp_summarize"); os.makedirs(tmp, exist_ok=True)

    def sw(i):
        P = walk.normalize(sets32[keys[i]])
        p = os.path.join(tmp, f"b{i}.txt")
        dlib.write_pts(p, P)
        st = dlib.satcount_sweep(p, 7, "-", 1, 3)
        os.unlink(p)
        return st
    with ThreadPoolExecutor(NPROC) as ex:
        sts = list(ex.map(sw, range(len(keys))))
    S["baseline_random_restarts"]["sampled_sweeps"] = {
        "n": len(sts), "m0_total": sum(s["m0"] for s in sts), "all_complete": all(s["complete"] for s in sts),
        "m1_faces": dist([s["m1"] for s in sts]), "m1_faces_hist": hist([s["m1"] for s in sts], EDGES_M1),
        "mean_sweep_cpu_s": round(statistics.mean(s["cpu_seconds"] for s in sts), 3) if sts else None}
    if "walk" in S:
        wr = S["walk"]["states_swept_total"] / max(1e-9, S["walk"]["cpu_s_total"]) * 3600
        br = S["baseline_random_restarts"]["distinct_32_sets_per_cpu_hour"] or 0
        msw = S["baseline_random_restarts"]["sampled_sweeps"]["mean_sweep_cpu_s"] or 0
        brc = 3600.0 / (bcpu / max(1, len(sets32)) + msw) if sets32 else 0
        S["walk_vs_baseline"] = {
            "walk_new_32_sets_per_cpu_hour (each fully swept)": round(wr, 1),
            "baseline_distinct_32_sets_per_cpu_hour (unswept)": br,
            "baseline_distinct_32_sets_per_cpu_hour_if_each_swept": round(brc, 1),
            "ratio_walk_over_baseline_swept": round(wr / brc, 3) if brc else None,
            "ratio_walk_over_baseline_unswept": round(wr / br, 3) if br else None}

# ---------- annealing ----------
A = [r for r in jl(os.path.join(RUNS, "anneal", "anneal_w*.jsonl")) if "best" in r]
if A:
    fams = collections.defaultdict(list)
    for r in A:
        fams[r["family"]].append(r)
    EDGES_E = [0, 1, 2, 3, 4, 5, 6, 8, 10, 15, 20, 30, 50, 100, 1000]
    S["anneal"] = {
        "runs": len(A), "cpu_s": round(sum(r["cpu"] or 0 for r in A), 1),
        "recount_mismatches": sum(1 for r in A if r["best"] != r["recount7"]),
        "zero_heptagon_runs": sum(1 for r in A if r["recount7"] == 0),
        "min_energy_hist": hist([r["recount7"] for r in A], EDGES_E),
        "min_energy": min(r["recount7"] for r in A),
        "by_family": {f: {"runs": len(L), "cpu_s": round(sum(r["cpu"] or 0 for r in L), 1),
                          "best": min(r["recount7"] for r in L), "min_energy": dist([r["recount7"] for r in L]),
                          "hist": hist([r["recount7"] for r in L], EDGES_E),
                          "initial_energy": dist([r["E0"] for r in L])} for f, L in sorted(fams.items())},
        "by_iters": {str(it): dist([r["recount7"] for r in A if r["iters"] == it]) for it in sorted(set(r["iters"] for r in A))},
    }
    # 50 best distinct order types: fewest heptagons, then fewest hexagons
    emin = min(r["recount7"] for r in A)
    lowA = [r for r in A if r["recount7"] <= emin + 1]
    with ThreadPoolExecutor(NPROC) as ex:
        c6s = list(ex.map(lambda r: dlib.cgon_count(r["pts"], 6)[6], lowA))
    for r, c6 in zip(lowA, c6s):
        r["c6"] = c6
    A.sort(key=lambda r: (r["recount7"], r.get("c6") or 0, r["cpu"] or 0))
    cand = A[:2000]
    sigs = dlib.canon([r["pts"] for r in cand])
    best, seen = [], set()
    for r, (c, cm) in zip(cand, sigs):
        k = walk.h(cm)
        if k in seen:
            continue
        seen.add(k)
        best.append((r, k))
        if len(best) >= 50:
            break

    def ver(item):
        r, k = item
        P = [(Fraction(x), Fraction(y)) for x, y in r["pts"]]
        gp, why = verify_exact.general_position(P)
        ex = verify_exact.count_convex(P, 8) if gp else {}
        c = dlib.cgon_count(r["pts"], 8)
        return {"canonm_sha1_16": k, "family": r["family"], "info": r["info"], "run": [r["w"], r["run"]],
                "heptagons_cgon": c[7], "heptagons_exact_py": ex.get(7), "octagons_exact_py": ex.get(8),
                "general_position_exact": gp, "counts_cgon": {str(kk): v for kk, v in c.items()},
                "pts": r["pts"]}
    with ThreadPoolExecutor(NPROC) as ex:
        vb = list(ex.map(ver, best))
    with open(os.path.join(RES, "anneal_best50.jsonl"), "w") as f:
        for v in vb:
            f.write(json.dumps(v) + "\n")
    S["anneal"]["best50"] = {"file": "anneal_best50.jsonl", "energies": [v["heptagons_cgon"] for v in vb],
                             "hexagon_counts": [v["counts_cgon"]["6"] for v in vb],
                             "exact_py_agrees": all(v["heptagons_cgon"] == v["heptagons_exact_py"] for v in vb),
                             "all_general_position": all(v["general_position_exact"] for v in vb)}
    # distinct one-heptagon order types found by annealing, and saturation of
    # the heptagon-free deletions of the best 50 (exhaustive face sweeps)
    one = [r for r in A if r["recount7"] == 1]
    S["anneal"]["one_heptagon_runs"] = len(one)
    if one:
        sg1 = dlib.canon([r["pts"] for r in one])
        S["anneal"]["one_heptagon_distinct_order_types"] = len(set(c[1] for c in sg1))
        S["anneal"]["one_heptagon_distinct_by_family"] = {
            f: len(set(c[1] for r, c in zip(one, sg1) if r["family"] == f)) for f in sorted(fams)}
    dl = []
    for v in vb:
        if v["heptagons_cgon"] == 1:
            dl += [(T, lab) for T, lab in walk.seed_deletions([(v["canonm_sha1_16"], v["pts"])])]
    tmp = os.path.join(RUNS, "tmp_summarize"); os.makedirs(tmp, exist_ok=True)

    def sw2(i):
        p = os.path.join(tmp, f"a{i}.txt")
        dlib.write_pts(p, dl[i][0])
        st = dlib.satcount_sweep(p, 7, "-", 1, 3)
        os.unlink(p)
        return st
    with ThreadPoolExecutor(NPROC) as ex:
        st2 = list(ex.map(sw2, range(len(dl))))
    S["anneal"]["best50_deletion_sweeps"] = {
        "n": len(st2), "m0_total": sum(s["m0"] for s in st2), "all_complete": all(s["complete"] for s in st2),
        "m1_faces": dist([s["m1"] for s in st2]), "m1_faces_hist": hist([s["m1"] for s in st2], EDGES_M1)}

# ---------- found ----------
S["found_files"] = sorted(os.path.relpath(f, RUNS) for f in glob.glob(os.path.join(RUNS, "*", "FOUND*")))
json.dump(S, open(os.path.join(RES, "summary.json"), "w"), indent=1)
print(json.dumps({k: (v if k in ("found_files", "walk_vs_baseline") else "...") for k, v in S.items()}, indent=1))
