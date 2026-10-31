#!/usr/bin/env python3
"""Work list of the second C2P wave (lists/C2P2.tsv), made from the records of the first wave and the P8 pilot.
- Long units (cap 6000 s), one per machine 0..L-1: every quadrilateral representative that timed out at its full cap
  and is not certified, except MAC_UNITS (run on the Mac), plus PARTNERS: the reflection partner of a subcase run on
  the Mac (refuting either member of a pair suffices, by results/C2C34 README section 6 and the review in C2P/review).
- Dedicated machines L..N-1: the cover of P6, then the rest of P7 (cut short by the end of wave 1, or not reached),
  with the caps of lists/C2P.tsv.
- Then every machine continues, dealt round robin from machine L on: the covers of P5..P1, then the rest of P6.
Machine j runs the rows with idx = j (mod N), in file order. usage: mklist2.py RESULTS_DIR OUT N"""
import collections, glob, json, sys
R, out, N = sys.argv[1], sys.argv[2], int(sys.argv[3])
MAC_UNITS, PARTNERS, LONG_CAP = {"P8_1-9"}, ["P8_7-16"], 6000
rows1 = [l.rstrip("\n").split("\t") for l in list(open(f"{R}/C2P/lists/C2P.tsv"))[1:]]
cap1 = {r[1]: int(r[4]) for r in rows1}
kind1 = {r[1]: r[3] for r in rows1}
cert, full = set(), set()
for l in list(open(f"{R}/C2C34/logs/p8_units.tsv"))[1:]:
    f = l.rstrip("\n").split("\t")
    if f[9] == "c VERIFIED" and f[11] == "s VERIFIED UNSAT": cert.add(f[0])
    elif f[3] == "UNKNOWN": full.add(f[0])
for p in glob.glob(f"{R}/C2P/M*/out.jsonl") + glob.glob(f"{R}/C2P/LOCAL*/out.jsonl"):
    for l in open(p):
        if not l.strip(): continue
        r = json.loads(l)
        if r.get("certified"): cert.add(r["unit"])
        elif r["status"] == "UNKNOWN" and ("LOCAL" in p or r["cap_s"] >= cap1.get(r["unit"], 0)): full.add(r["unit"])
reps = {a: [l.split("\t")[1].strip() for l in list(open(f"{R}/C2P/orbits/P{a}.tsv"))[1:]] for a in range(1, 9)}
reps = {a: list(dict.fromkeys(v)) for a, v in reps.items()}
open_ = lambda a: [u for u in reps[a] if u not in cert]
longu = [u for a in (8, 7) for u in open_(a) if u in full and u not in MAC_UNITS] + PARTNERS
L = len(longu)
assert L < N, (L, N)
q = collections.defaultdict(list)
for j, u in enumerate(longu): q[j].append((u, "Q", LONG_CAP))
ded = [("P6_cover", "cover", 3600)] if "P6_cover" not in cert else []
ded += [(u, kind1[u], cap1[u]) for u in open_(7) if u not in full]
for i, x in enumerate(ded): q[L + i % (N - L)].append(x)
rest = [(f"P{a}_cover", "cover", 3600) for a in range(5, 0, -1) if f"P{a}_cover" not in cert]
rest += [(u, kind1[u], cap1[u]) for u in open_(6) if u not in full]
order = list(range(L, N)) + list(range(L))
for i, x in enumerate(rest): q[order[i % N]].append(x)
with open(out, "w") as f:
    f.write("idx\tunit\tcase\tkind\tcap_s\n")
    for idx in sorted(j + N * k for j in q for k in range(len(q[j]))):
        u, kd, c = q[idx % N][idx // N]
        f.write(f"{idx}\t{u}\t{u.split('_')[0]}\t{kd}\t{c}\n")
print(f"long {L} (mac: {sorted(MAC_UNITS)}), dedicated {len(ded)} on {N - L} machines, P6 rest {len(rest)}; rows {sum(map(len, q.values()))}")
print("long units:", " ".join(longu))
