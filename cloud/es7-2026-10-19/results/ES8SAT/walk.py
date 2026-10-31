#!/usr/bin/env python3
"""Random walk through 64-point sets in general position with no convex octagon, starting from witness8, with an exact
saturation test (sat.c: every face of the line arrangement) every A accepted moves. A test with bad_candidates > 0 means
a point can be added without creating a convex octagon, i.e. a 65-point set with no convex octagon: it is saved and
reported at once. usage: walk.py SEED OUTDIR DEADLINE_EPOCH [A]"""
import json, math, os, random, subprocess, sys, time
seed, out, dl = int(sys.argv[1]), sys.argv[2], float(sys.argv[3]); A = int(sys.argv[4]) if len(sys.argv) > 4 else 10
rng = random.Random(seed); os.makedirs(out, exist_ok=True)
SAT = os.environ.get("SAT_BIN") or os.path.join(os.path.dirname(os.path.abspath(__file__)), "sat")
P = [tuple(map(int, l.split())) for l in open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "witness8.txt")) if l.strip()]
B = (1 << 26) - 1
log = open(os.path.join(out, "walk.log"), "a", buffering=1)
def write(pts, f):
    with open(f, "w") as g: g.write("".join(f"{x} {y}\n" for x, y in pts))
acc = tries = tests = 0
while time.time() < dl:
    i = rng.randrange(64); others = P[:i] + P[i + 1:]
    write(others, os.path.join(out, "others.txt"))
    cands = []
    for _ in range(64):
        s = 10 ** rng.uniform(0, 7.3)
        q = (P[i][0] + round(rng.uniform(-1, 1) * s), P[i][1] + round(rng.uniform(-1, 1) * s))
        if abs(q[0]) <= B and abs(q[1]) <= B and q not in others: cands.append(q)
    r = subprocess.run([SAT, "test", os.path.join(out, "others.txt"), "8"], input="".join(f"{x} {y}\n" for x, y in cands),
                       capture_output=True, text=True)
    res = r.stdout.split()
    ok = [q for q, s in zip(cands, res) if s != "degenerate" and int(s) <= 7]
    tries += 1
    if not ok: continue
    P[i] = rng.choice(ok); acc += 1
    if acc % A: continue
    f = os.path.join(out, "cur.txt"); write(P, f)
    r = subprocess.run([SAT, "sat", f, "8", os.path.join(out, "bad.txt")], capture_output=True, text=True)
    tests += 1
    try: j = json.loads(r.stdout.strip().splitlines()[-1])
    except Exception: log.write(f"ERROR {r.stdout[-300:]} {r.stderr[-300:]}\n"); continue
    log.write(json.dumps({"t": round(time.time()), "acc": acc, "tries": tries, "test": tests, "faces": j["faces_euler"],
                          "hit": j["faces_hit_by_valid_candidates"], "bad": j["bad_candidates"], "cpu": j["cpu_seconds"]}) + "\n")
    if j["bad_candidates"] > 0 or j["faces_hit_by_valid_candidates"] != j["faces_euler"]:
        write(P, os.path.join(out, f"FOUND_{tests}.txt")); log.write("ALARM\n")
        if j["bad_candidates"] > 0: break
print("done", acc, tries, tests)
