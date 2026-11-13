#!/usr/bin/env python3
"""Generate -> dedupe by order type -> exact saturation (sat.c), sequentially.

usage: driver.py RUNNAME K N GENMODE INIT ITERS T0 T1 WALKMOVES EMITEVERY STARTS_PER_BATCH
                 SEED0 DEADLINE_EPOCH [NEG_CONTROLS]

Only one heavy process runs at a time: gen (batch) then sat per new order type.
Global dedupe state (order types up to reflection) per K lives in
data/seen_K{K}.txt and is shared by all runs; results are appended to
logs/results_K{K}.jsonl, distinct sets to data/distinct_K{K}.txt.
Any non-saturated set (bad faces > 0) or face-count mismatch is written to
ALERT_* and the driver stops.
"""
import hashlib, json, os, random, subprocess, sys, time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BIN = os.path.join(ROOT, "bin")
DATA = os.path.join(ROOT, "data")
LOGS = os.path.join(ROOT, "logs")

(run, K, N, gmode, init, iters, T0, T1, walk, every, spb, seed0, deadline) = sys.argv[1:14]
K, N, spb, seed0, deadline = int(K), int(N), int(spb), int(seed0), float(deadline)
negctl = int(sys.argv[14]) if len(sys.argv) > 14 else 0

SUF = os.environ.get("SUFFIX", "")
seen_path = os.path.join(DATA, f"seen_K{K}{SUF}.txt")
seen_or_path = os.path.join(DATA, f"seen_or_K{K}{SUF}.txt")
import glob
seen, seen_or = set(), set()
for fn in glob.glob(os.path.join(DATA, f"seen_K{K}*.txt")):
    seen |= set(open(fn).read().split())
for fn in glob.glob(os.path.join(DATA, f"seen_or_K{K}*.txt")):
    seen_or |= set(open(fn).read().split())
seen_f = open(seen_path, "a")
seen_or_f = open(seen_or_path, "a")
res_f = open(os.path.join(LOGS, f"results_K{K}{SUF}.jsonl"), "a")
dist_f = open(os.path.join(DATA, f"distinct_K{K}{SUF}.txt"), "a")
tmpdir = os.path.join(DATA, "tmp_" + run)
os.makedirs(tmpdir, exist_ok=True)


def orient(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def run_sat(pts, k, badfile="/dev/null"):
    fn = os.path.join(tmpdir, "S.txt")
    with open(fn, "w") as f:
        f.write("".join(f"{x} {y}\n" for x, y in pts))
    p = subprocess.run([os.path.join(BIN, "sat"), "sat", fn, str(k), badfile], capture_output=True, text=True)
    if p.returncode != 0:
        raise RuntimeError("sat failed: " + p.stderr[-500:])
    return json.loads(p.stdout)


def alert(kind, info):
    fn = os.path.join(ROOT, f"ALERT_{kind}_{run}_{int(time.time())}.json")
    with open(fn, "w") as f:
        json.dump(info, f)
    print("ALERT", kind, fn, flush=True)


stats = dict(batches=0, generated=0, new_or=0, new=0, saturated=0, sat_cpu=0.0, gen_wall=0.0, negctl_ok=0,
             negctl_fail=0, zero=0)
rng = random.Random(seed0 * 7919 + K)
batch = 0
t_start = time.time()
stop = False
while time.time() < deadline and not stop:
    seed = seed0 + batch
    batch += 1
    out = os.path.join(tmpdir, f"batch.txt")
    if os.path.exists(out):
        os.remove(out)
    tg = time.time()
    if gmode == "file":
        out = init
        stop = True
        g = subprocess.CompletedProcess([], 0, stdout="file " + init, stderr="")
    else:
        g = subprocess.run([os.environ.get("GENBIN", os.path.join(BIN, "gen")), gmode, str(K), str(N), str(seed), str(spb), init, iters, T0, T1,
                            walk, every, out], capture_output=True, text=True)
    stats["gen_wall"] += time.time() - tg
    if g.returncode != 0:
        print("gen failed", g.stderr[-1000:], flush=True)
        break
    stats["batches"] += 1
    lines = open(out).read().splitlines() if os.path.exists(out) else []
    for line in lines:
        f = line.split()
        tag, E, canon, canonm, n = f[0], int(f[1]), f[2], f[3], int(f[4])
        c = list(map(int, f[5:]))
        pts = list(zip(c[0::2], c[1::2]))
        assert len(pts) == n
        stats["generated"] += 1
        if E != 0 or tag.startswith("ZERO"):
            stats["zero"] += tag.startswith("ZERO")
            alert("ZERO" if tag.startswith("ZERO") else "BADLINE", dict(tag=tag, E=E, n=n, points=pts, seed=seed))
            if tag.startswith("ZERO"):
                stop = True
                break
            continue
        d_or = hashlib.sha256(canon.encode()).hexdigest()[:32]
        if d_or not in seen_or:
            seen_or.add(d_or)
            seen_or_f.write(d_or + "\n")
            stats["new_or"] += 1
        dm = hashlib.sha256(canonm.encode()).hexdigest()[:32]
        if dm in seen:
            continue
        seen.add(dm)
        seen_f.write(dm + "\n")
        stats["new"] += 1
        r = run_sat(pts, K)
        stats["sat_cpu"] += r["cpu_seconds"]
        ok = (r["bad_candidates"] == 0 and r["faces_euler"] == r["faces_hit_by_valid_candidates"] and r["N"] == n)
        rec = dict(run=run, seed=seed, tag=tag, n=n, canonm=dm, faces=r["faces_euler"], hit=r["faces_hit_by_valid_candidates"],
                   bad=r["bad_candidates"], cand=r["candidates"], cpu=r["cpu_seconds"], saturated=ok)
        res_f.write(json.dumps(rec) + "\n")
        dist_f.write(f"{run} {tag} {dm} {n} " + " ".join(f"{x} {y}" for x, y in pts) + "\n")
        if ok:
            stats["saturated"] += 1
        else:
            alert("NONSAT", dict(rec=rec, points=pts, sat=r))
            stop = True
            break
        # negative control: drop one point; the dropped point's face must be bad
        if stats["new"] <= negctl:
            i = rng.randrange(n)
            T = pts[:i] + pts[i + 1:]
            bf = os.path.join(tmpdir, "bad.txt")
            r2 = run_sat(T, K, bf)
            p = pts[i]
            sig = "".join("+" if orient(T[a], T[b], p) > 0 else "-" for a in range(len(T)) for b in range(a + 1, len(T)))
            badsigs = set(l.split()[-1] for l in open(bf) if l.strip())
            good = r2["bad_candidates"] > 0 and sig in badsigs and r2["faces_euler"] == r2["faces_hit_by_valid_candidates"]
            stats["negctl_ok" if good else "negctl_fail"] += 1
            if not good:
                alert("NEGCTL", dict(rec=rec, dropped=i, sat=r2))
    seen_f.flush(); seen_or_f.flush(); res_f.flush(); dist_f.flush()
    el = time.time() - t_start
    print(f"[{run}] batch {batch} seed {seed} t={el:.0f}s " + " ".join(f"{k}={v:.1f}" if isinstance(v, float) else f"{k}={v}"
          for k, v in stats.items()) + f" | {g.stdout.strip()}", flush=True)
print(f"[{run}] FINAL " + json.dumps(stats), flush=True)
