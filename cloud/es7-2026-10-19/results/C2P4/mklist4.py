#!/usr/bin/env python3
"""Work list of the fourth C2P wave (lists/C2P4.tsv) from the records of all earlier waves and the P8 pilot.

For the cases given (in priority order), every orbit of C2P/orbits/P<a>.tsv with no certified member is open; the cover
P<a>_cover is open if it has no certified record. For an open orbit the representative is run; when the representative
already timed out with a cap of 5,000 s or more and its reflection partner has no record, the partner is run as well,
on another machine (refuting either member suffices). Caps: cover 3,600 s; H 1,800 s; Q 6,000 s, or 7,000 s after an
earlier timeout of the unit itself.

Machine j runs the rows with idx = j (mod N), in idx order. The units are placed greedily on the machine with the least
expected load (ties to the lowest j), in phases: the Q units and covers of the first two cases (largest load first),
then their H units; then for each further case its Q units and cover, then its H units. Expected loads (solve and
both checks, seconds): H 650, cover 1,200, Q 3,400, Q after an earlier timeout 7,000. A machine has about 7,900 s
for its lane, so the tail of a heavily loaded queue may not be reached; such units stay open for a later wave.
usage: mklist4.py RESULTS_DIR OUT N CASE...   (for example: mklist4.py results lists/C2P4.tsv 50 7 6 5 4)"""
import glob, json, sys
R, out, N, cases = sys.argv[1], sys.argv[2], int(sys.argv[3]), [int(a) for a in sys.argv[4:]]
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
units, subst = {}, set()                     # case -> (Q-like units with loads, H units); partners run instead
for a in cases:
    rows = [l.rstrip("\n").split("\t")[:2] for l in list(open(f"{R}/C2P/orbits/P{a}.tsv"))[1:]]
    mem = {}
    for s, r in rows: mem.setdefault(r, []).append(s)
    q, h = [], []
    if f"P{a}_cover" not in cert: q.append((f"P{a}_cover", "cover", 3600, 1200))
    for r, ms in mem.items():
        if any(m in cert for m in ms): continue
        part = next((m for m in ms if m != r), r)
        u = part if tmax.get(r, 0) >= 5000 and part not in tmax else r
        if u != r:                           # the partner, and the representative again on another machine
            subst.add(u); q.append((r, "Q", 7000, 7000))
        if isq(u):
            hard = tmax.get(u, 0) > 0
            q.append((u, "Q", 7000 if hard else 6000, 7000 if hard else 3400))
        else:
            h.append((u, "H", 1800, 650))
    units[a] = (q, h)
phases = [sorted(units[cases[0]][0] + (units[cases[1]][0] if len(cases) > 1 else []), key=lambda x: -x[3]),
          units[cases[0]][1] + (units[cases[1]][1] if len(cases) > 1 else [])]
for a in cases[2:]: phases += [sorted(units[a][0], key=lambda x: -x[3]), units[a][1]]
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
reach = sum(1 for j in range(N) for x in queue[j] if x[3] <= 7000)
for a in cases:
    q, h = units[a]
    print(f"P{a}: Q {sum(1 for x in q if x[1] == 'Q')} (after a timeout: {sum(1 for x in q if x[2] == 7000)}, partners: "
          f"{sum(1 for x in q if x[0] in subst)}), cover {sum(1 for x in q if x[1] == 'cover')}, H {len(h)}")
print(f"rows {sum(map(len, queue))}; expected to start within the lane window: {reach}; "
      f"machine load min {min(load)} max {max(load)} s")
