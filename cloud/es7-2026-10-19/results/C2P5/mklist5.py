#!/usr/bin/env python3
"""Work lists of the fifth C2P wave (lists/C2P5A.tsv, lists/C2P5B.tsv) from the records of all earlier waves and the
P8 pilot.

For the cases given (in priority order), every orbit of C2P/orbits/P<a>.tsv with no certified member is open; the cover
P<a>_cover is open if it has no certified record. For an open orbit the representative is run; when it already timed
out with a cap of 5,000 s or more, both members of the orbit are run, on different machines (refuting either member
suffices). Caps: cover 3,600 s; H 2,400 s; Q 8,000 s, or 10,000 s after an earlier timeout at a cap of 5,000 s or more.
Units listed in an EXCLUDE file (one name per line, optional) are left out.

Machine j runs the rows with idx = j (mod N), in idx order. The units are placed greedily on the machine with the least
expected load (ties to the lowest j), in phases: the Q units and covers of the first two cases (largest load first),
then their H units; then for each further case its Q units and cover, then its H units. A case given as r<a> is placed
in reverse (its H units in reverse order, then its Q units in reverse order); two lists that take the same case, one
of them reversed, then start it from opposite ends. Expected loads (solve and both checks, seconds): H 650, cover
1,200, Q 3,400, Q after a short timeout 4,500, Q after a timeout at 5,000 s or more 9,000.
usage: mklist5.py RESULTS_DIR OUT N [--exclude FILE] CASE...   (for example: mklist5.py results lists/C2P5B.tsv 50 2 1 3)"""
import glob, json, sys
args = sys.argv[1:]
excl = set()
if "--exclude" in args:
    i = args.index("--exclude"); excl = {l.strip() for l in open(args[i + 1]) if l.strip()}; del args[i:i + 2]
R, out, N, specs = args[0], args[1], int(args[2]), args[3:]
cert, tmax = set(), {}
for l in list(open(f"{R}/C2C34/logs/p8_units.tsv"))[1:]:
    f = l.rstrip("\n").split("\t")
    if f[9] == "c VERIFIED" and f[11] == "s VERIFIED UNSAT": cert.add(f[0])
    else: tmax.setdefault(f[0], 0)
for p in glob.glob(f"{R}/C2P*/M*/out.jsonl") + glob.glob(f"{R}/C2P*/LOCAL*/out.jsonl"):
    for l in open(p):
        if l.strip():
            r = json.loads(l)
            if r.get("certified") is True: cert.add(r["unit"])
            elif r["status"] == "UNKNOWN": tmax[r["unit"]] = max(tmax.get(r["unit"], 0), r["cap_s"])
            else: tmax.setdefault(r["unit"], 0)
isq = lambda u: u.count("-") == 1
def qrow(u):
    t = tmax.get(u, 0)
    return (u, "Q", 10000, 9000) if t >= 5000 else (u, "Q", 8000, 4500) if t > 0 else (u, "Q", 8000, 3400)
units, both = {}, set()                      # case -> (Q-like units with loads, H units); orbits run with both members
cases = [int(s.lstrip("r")) for s in specs]
for a in cases:
    rows = [l.rstrip("\n").split("\t")[:2] for l in list(open(f"{R}/C2P/orbits/P{a}.tsv"))[1:]]
    mem = {}
    for s, r in rows: mem.setdefault(r, []).append(s)
    q, h = [], []
    if f"P{a}_cover" not in cert: q.append((f"P{a}_cover", "cover", 3600, 1200))
    for r, ms in mem.items():
        if any(m in cert for m in ms): continue
        part = next((m for m in ms if m != r), r)
        run = [r, part] if tmax.get(r, 0) >= 5000 and part != r else [r]
        if len(run) == 2: both.add(r)
        for u in run:
            if u in excl: continue
            if isq(u): q.append(qrow(u) if u == r or tmax.get(u, 0) > 0 else (u, "Q", 10000, 7000))
            else: h.append((u, "H", 2400, 650))
    units[a] = (q, h)
def phase(s):
    a = int(s.lstrip("r")); q, h = units[a]
    return [h[::-1], q[::-1]] if s.startswith("r") else [sorted(q, key=lambda x: -x[3]), h]
first = specs[:2]
phases = [sorted(sum((units[int(s.lstrip("r"))][0] for s in first), []), key=lambda x: -x[3]),
          sum((units[int(s.lstrip("r"))][1] for s in first), [])]
for s in specs[2:]: phases += phase(s)
load, queue = [0] * N, [[] for _ in range(N)]
for ph in phases:
    for u, kind, cap, ld in ph:
        j = min(range(N), key=lambda j: (load[j], j))
        queue[j].append((u, kind, cap, load[j])); load[j] += ld
with open(out, "w") as f:
    f.write("idx\tunit\tcase\tkind\tcap_s\n")
    for idx in sorted(j + N * k for j in range(N) for k in range(len(queue[j]))):
        u, kind, cap, _ = queue[idx % N][idx // N]
        f.write(f"{idx}\t{u}\t{u.split('_')[0]}\t{kind}\t{cap}\n")
for a in cases:
    q, h = units[a]
    print(f"P{a}: Q {sum(1 for x in q if x[1] == 'Q')} (cap 10,000: {sum(1 for x in q if x[2] == 10000)}, orbits with "
          f"both members: {sum(1 for x in q if x[0] in both)}), cover {sum(1 for x in q if x[1] == 'cover')}, H {len(h)}")
for w in (12900, 17400):
    print(f"window {w} s: expected to start {sum(1 for j in range(N) for x in queue[j] if x[3] <= w - 900)} of "
          f"{sum(map(len, queue))} rows")
print(f"machine load min {min(load)} max {max(load)} s")
