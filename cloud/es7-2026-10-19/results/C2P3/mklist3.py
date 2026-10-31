#!/usr/bin/env python3
"""Work list of the third C2P wave (lists/C2P3.tsv) from the records of all earlier waves and the P8 pilot.
Open orbit representatives of P7 and P6 (no certified member, by C2P/orbits). Machine j runs the rows with idx = j (mod N):
- slot 1 on every machine: a quadrilateral (Q) unit with cap 6000 s: all open P7 Q, then the open P6 Q that already have a
  record without an answer, then the other open P6 Q;
- slot 2 (cap 4800 s): the remaining open P6 Q, on machines whose slot-1 unit has no earlier record;
- then the open hexagonal (H) units of P7 and P6 (cap 1800 s), round robin;
- then the units of P5 in orbit order (caps of C2P/lists/C2P.tsv), round robin.
The covers of P5..P1 are run on the Mac (not in this list). usage: mklist3.py RESULTS_DIR OUT N"""
import collections, glob, json, sys
R, out, N = sys.argv[1], sys.argv[2], int(sys.argv[3])
cap1 = {l.split("\t")[1]: int(l.rstrip("\n").split("\t")[4]) for l in list(open(f"{R}/C2P/lists/C2P.tsv"))[1:]}
cert, tried = set(), set()
for l in list(open(f"{R}/C2C34/logs/p8_units.tsv"))[1:]:
    f = l.rstrip("\n").split("\t"); tried.add(f[0])
    if f[9] == "c VERIFIED" and f[11] == "s VERIFIED UNSAT": cert.add(f[0])
for p in glob.glob(f"{R}/C2P*/M*/out.jsonl") + glob.glob(f"{R}/C2P*/LOCAL*/out.jsonl"):
    for l in open(p):
        if l.strip():
            r = json.loads(l); tried.add(r["unit"])
            if r.get("certified"): cert.add(r["unit"])
rep, reps = {}, {}
for a in range(1, 9):
    rows = [l.rstrip("\n").split("\t")[:2] for l in list(open(f"{R}/C2P/orbits/P{a}.tsv"))[1:]]
    for s, r in rows: rep[s] = r
    reps[a] = list(dict.fromkeys(r for s, r in rows))
crep = {rep[u] for u in cert if u in rep}
openr = {a: [u for u in reps[a] if u not in crep] for a in reps}
isq = lambda u: u.count("-") == 1
q7 = [u for u in openr[7] if isq(u)]
q6 = [u for u in openr[6] if isq(u) and u in tried] + [u for u in openr[6] if isq(u) and u not in tried]
h = [u for u in openr[7] + openr[6] if not isq(u)]
q = collections.defaultdict(list)
slot1 = (q7 + q6)[:N]; rest_q = (q7 + q6)[N:]
for j, u in enumerate(slot1): q[j].append((u, "Q", 6000))
fresh = [j for j, u in enumerate(slot1) if u not in tried] or list(range(N))
for i, u in enumerate(rest_q): q[fresh[i % len(fresh)]].append((u, "Q", 4800))
for i, u in enumerate(h): q[i % N].append((u, "H", 1800))
p5 = [u for u in openr[5]]
for i, u in enumerate(p5): q[(len(h) + i) % N].append((u, "Q" if isq(u) else "H", cap1.get(u, 2400 if isq(u) else 1800)))
with open(out, "w") as f:
    f.write("idx\tunit\tcase\tkind\tcap_s\n")
    for idx in sorted(j + N * k for j in q for k in range(len(q[j]))):
        u, kd, c = q[idx % N][idx // N]
        f.write(f"{idx}\t{u}\t{u.split('_')[0]}\t{kd}\t{c}\n")
print(f"slot1 {len(slot1)} (P7 Q {len(q7)}, P6 Q {len(slot1) - len(q7)}), slot2 Q {len(rest_q)}, H {len(h)}, P5 filler {len(p5)}; rows {sum(map(len, q.values()))}")
