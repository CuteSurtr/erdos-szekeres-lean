#!/usr/bin/env python3
"""Rewrite lists/C2P5C.tsv with the orphaned orbits: open orbits of P1-P4 (no certified member) none of whose members
is queued, unrecorded, on a C2P5 machine still running (no README) or on the Mac lane file given. One member per orbit
(the representative unless only its partner was tried), quadrilateral units first (cap 8,000 s), hexagonal 2,400 s;
round-robin over residues J0..J0+K-1 modulo 13 (the prompts of M37-M49 say N = 13).
usage: relist_c.py RESULTS_DIR MAC_UNITS_TSV K J0"""
import collections, glob, json, os, sys
R, macq, K, J0 = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
cert, recd = set(), set()
for p in glob.glob(f"{R}/C2P*/M*/out.jsonl") + glob.glob(f"{R}/C2P*/LOCAL*/out.jsonl"):
    for l in open(p):
        if l.strip():
            r = json.loads(l); recd.add(r["unit"])
            if r.get("certified"): cert.add(r["unit"])
def own(p):                                  # units with a record in one machine's own out.jsonl
    return {json.loads(l)["unit"] for l in open(p) if l.strip()} if os.path.exists(p) else set()
queued = set()
for d in glob.glob(f"{R}/C2P5/M*"):
    if os.path.exists(f"{d}/README.md") or not os.path.exists(f"{d}/units.tsv"): continue
    done = own(f"{d}/out.jsonl")
    queued |= {l.split("\t")[1] for l in list(open(f"{d}/units.tsv"))[1:] if l.split("\t")[1] not in done}
if os.path.exists(macq):
    done = own(os.path.join(os.path.dirname(macq), "out.jsonl"))
    queued |= {l.split("\t")[1] for l in list(open(macq))[1:] if l.split("\t")[1] not in done or l.split("\t")[1] in queued}
units = []
for a in (1, 2, 3, 4):
    mem = collections.defaultdict(list)
    for l in list(open(f"{R}/C2P/orbits/P{a}.tsv"))[1:]:
        s_, r_ = l.rstrip("\n").split("\t")[:2]; mem[r_].append(s_)
    for r_, ms in mem.items():
        if any(m in cert for m in ms) or any(m in queued for m in ms): continue
        part = next((m for m in ms if m != r_), r_)
        u = part if r_ in recd and part not in recd else r_
        units.append((u, f"P{a}", "Q" if u.count("-") == 1 else "H", 8000 if u.count("-") == 1 else 2400))
units.sort(key=lambda x: x[2] != "Q")
with open(f"{R}/C2P5/lists/C2P5C.tsv", "w") as f:
    f.write("idx\tunit\tcase\tkind\tcap_s\n")
    for i, (u, c, k, cap) in enumerate(units):
        f.write(f"{J0 + i % K + 13 * (i // K)}\t{u}\t{c}\t{k}\t{cap}\n")
print(f"{len(units)} orphaned orbits -> C2P5C.tsv on residues {J0}..{J0 + K - 1}:", collections.Counter(f"{c}{k}" for _, c, k, _ in units))
