#!/usr/bin/env python3
"""walk32 worker: ES base (gen_es.py) -> random walk (walk) -> snapshots -> vfy4 (exact GP,
convex k-subset counts, order-type hash) -> tools/realizer/saturate.py --K 7 (exact checks
and sat.c).  One JSON line per distinct (per worker) order type into live/eE_wW.jsonl, the
points into live/eE_sets_wW.txt (live/ is not tracked by git; copies are committed under data/).
Stops at DEADLINE (unix time) or if live/STOP exists; any set with bad_candidates > 0 writes
live/ALERT_* and creates live/STOP.  EPOCH only changes the random seeds (restarts).
usage: driver.py WORKER DEADLINE EPOCH"""
import json, os, random, subprocess, sys, time
HERE = os.path.dirname(os.path.abspath(__file__))
TOOLS = os.path.join(HERE, "..", "..", "..", "tools")
SAT = os.path.join(HERE, "sat")
w, deadline, epoch = int(sys.argv[1]), float(sys.argv[2]), int(sys.argv[3])
out = os.path.join(HERE, "live"); os.makedirs(out, exist_ok=True)
tmp = os.path.join(out, f"tmp{w}"); os.makedirs(tmp, exist_ok=True)
rng = random.Random(1000 * epoch + w)
seen = set()
jl = open(os.path.join(out, f"e{epoch}_w{w}.jsonl"), "a")
sets = open(os.path.join(out, f"e{epoch}_sets_w{w}.txt"), "a")

def test(path, rec):
    t0 = time.time()
    v = json.loads(subprocess.run([os.path.join(HERE, "vfy4"), path], capture_output=True, text=True).stdout)
    rec.update(vfy4=v)
    if not v.get("general_position") or v["c7"] != 0 or v["c8plus"] != 0:
        rec["skipped"] = "not GP or has convex 7-gon"
    elif v["ot_hash"] in seen:
        return None
    else:
        seen.add(v["ot_hash"])
        r = subprocess.run([sys.executable, os.path.join(TOOLS, "realizer", "saturate.py"), "--sat", SAT, "--K", "7", path],
                           capture_output=True, text=True)
        s = json.loads(r.stdout.strip().splitlines()[-1])
        sat = s.get("sat", {})
        rec.update(ot_hash=v["ot_hash"], c6=v["c6"], c5=v["c5"], hull=v["hull"], max_abs_coord=v["max_abs_coord"],
                   py_general_position=s.get("general_position"), py_largest_convex_subset=s.get("largest_convex_subset"),
                   faces=sat.get("faces_euler") if isinstance(sat, dict) else None,
                   faces_hit=sat.get("faces_hit_by_valid_candidates") if isinstance(sat, dict) else None,
                   faces_covered=s.get("faces_covered"), bad_candidates=sat.get("bad_candidates") if isinstance(sat, dict) else None,
                   saturated=s.get("saturated"), sat_raw=sat if not isinstance(sat, dict) or "error" in sat else None)
        pts = open(path).read().split()
        sets.write(v["ot_hash"] + " " + " ".join(pts) + "\n"); sets.flush()
        if rec.get("bad_candidates") != 0 or not rec.get("faces_covered") or s.get("largest_convex_subset", 7) >= 7:
            tag = f"ALERT_e{epoch}_w{w}_{v['ot_hash']}"
            open(os.path.join(out, tag + ".pts"), "w").write(open(path).read())
            open(os.path.join(out, tag + ".json"), "w").write(json.dumps(s) + "\n")
            if rec.get("bad_candidates"):
                open(os.path.join(out, "STOP"), "w").write(tag + "\n")
    rec["seconds"] = round(time.time() - t0, 3)
    jl.write(json.dumps(rec) + "\n"); jl.flush()
    return rec

run = 0
while time.time() < deadline and not os.path.exists(os.path.join(out, "STOP")):
    run += 1
    mild = rng.choice([0, 1, 1, 1, 2, 2])
    bseed = rng.randrange(10 ** 9)
    base = os.path.join(tmp, "base.txt")
    subprocess.run([sys.executable, os.path.join(HERE, "gen_es.py"), str(bseed), base, str(mild)], check=True)
    wseed = rng.randrange(10 ** 9)
    steps = rng.choice([1, 2, 5, 10, 30, 100, 300, 1000, 3000])
    nsnap = rng.choice([5, 10, 20])
    rmin = rng.choice([1e-3, 1e-2, 1e-1])
    gen = dict(generator="walk32", worker=w, run=run, base_mild=mild, base_seed=bseed, walk_seed=wseed,
               steps=steps, nsnap=nsnap, rmin=rmin)
    pref = os.path.join(tmp, "s")
    r = subprocess.run([os.path.join(HERE, "walk"), base, str(wseed), str(nsnap), str(steps), str(rmin), pref],
                       capture_output=True, text=True)
    try:
        wstat = json.loads(r.stderr.strip().splitlines()[-1])
    except Exception:
        wstat = {"error": r.stderr[-300:]}
    for k in range(1, nsnap + 1):
        p = f"{pref}_{k}.txt"
        if not os.path.exists(p):
            continue
        test(p, dict(gen, snap=k, walk_len=k * steps, walk_stat=wstat if k == nsnap else None))
        os.remove(p)
        if os.path.exists(os.path.join(out, "STOP")):
            break
