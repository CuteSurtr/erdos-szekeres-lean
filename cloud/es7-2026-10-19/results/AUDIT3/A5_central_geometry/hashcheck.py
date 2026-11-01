#!/usr/bin/env python3
"""Auditor A5: tie certified records to MY semantic cubes. For selected units, rebuild the exact CNF bytes the lanes
hashed -- base (streamed, never loaded) with the clause count raised, plus extra clauses written from my own cubes
(derived from the normal-form semantics in static_checks.py, literals sorted by |l| as the generators print them) --
and compare the SHA-256 with the recorded cnf_sha256.
Formats (read from the scripts): hullcubes.py drops the leading comment line; hlane.sh, p8/solver.sh and lane.py keep
it and replace only the 'p cnf' line.
usage: hashcheck.py BASE_CNF BASE_JSON RESULTS_DIR"""
import csv, glob, hashlib, itertools, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from a5lib import *

BASE, MAPF, RES = sys.argv[1:4]
mp = Map(MAPF)
pt = lambda o, r: 2 * o + r


def ccw_vertices(classes):
    cl = sorted(classes)
    return [pt(o, 0) for o in cl] + [pt(o, 1) for o in cl]


def semantic_cube(outer, inner=None):
    lits = set()
    H = ccw_vertices(outer)
    for k in range(len(H)):
        u, w = H[k], H[(k + 1) % len(H)]
        for q in range(N):
            if q not in (u, w):
                lits.add(mp.lit(u, w, q))
    if inner is not None:
        pts_in = [q for q in range(N) if q // 2 not in outer]
        H2 = ccw_vertices(inner)
        for k in range(len(H2)):
            u, w = H2[k], H2[(k + 1) % len(H2)]
            for q in pts_in:
                if q not in (u, w):
                    lits.add(mp.lit(u, w, q))
    return sorted(lits, key=abs)


def subcube(name):
    case, Vs = name.split("_")
    a = int(case[1:])
    return semantic_cube({0, a}, {int(x) for x in Vs.split("-")})


# ---- records
rec = {}
for r in csv.DictReader(open(os.path.join(RES, "C2C34", "logs", "hex_cases.tsv")), delimiter="\t"):
    rec.setdefault(r["case"], set()).add(r["cnf_sha256"])
for r in csv.DictReader(open(os.path.join(RES, "C2C34", "logs", "p8_units.tsv")), delimiter="\t"):
    if r.get("cnf_sha256"):
        rec.setdefault(r["unit"], set()).add(r["cnf_sha256"])
certified = {}
for f in sorted(glob.glob(os.path.join(RES, "C2P*", "*", "out.jsonl"))) + [os.path.join(RES, "C2FINAL", "pilot", "out.jsonl")]:
    for line in open(f):
        if line.strip():
            r = json.loads(line)
            if r.get("cnf_sha256"):
                rec.setdefault(r["unit"], set()).add(r["cnf_sha256"])
                if r.get("status") == "UNSATISFIABLE" and r.get("lrat_check") == "c VERIFIED" and r.get("cake_lpr") == "s VERIFIED UNSAT":
                    certified.setdefault(r["unit"], set()).add(r["cnf_sha256"])
hullcover_expected = "bb60facb223788fb57291c73abfacd6deaa1eccd82ad2be9f50d36292959a60f"

targets = []   # (label, keep_comment, extra clauses, expected hash set, certified-hash set or None)
hull_cases = [f"P{a}" for a in range(1, T)] + [f"H{a}-{b}" for a, b in itertools.combinations(range(1, T), 2)]
hc = {n: (semantic_cube({0, int(n[1:])}) if n[0] == "P" else semantic_cube({0} | {int(x) for x in n[1:].split("-")})) for n in hull_cases}
targets.append(("hull cover (136 cubes)", False, [[-l for l in hc[n]] for n in hull_cases], {hullcover_expected}, None))
for a in range(1, 9):
    hs = set(hc[f"P{a}"])
    cls = [[l] for l in hc[f"P{a}"]]
    inner = [o for o in range(1, T) if o != a]
    for h in (2, 3):
        for V in itertools.combinations(inner, h):
            c = semantic_cube({0, a}, set(V))
            cls.append([-x for x in c if x not in hs])
    u = f"P{a}_cover"
    targets.append((u, True, cls, rec.get(u, set()), certified.get(u, set())))
for n in ["H1-2", "H5-11", "H8-9", "H15-16", "H3-14"]:
    targets.append((n, True, [[l] for l in hc[n]], rec.get(n, set()), None))
for u in ["P8_1-14", "P8_7-11", "P1_9-10", "P1_9-10-15", "P3_6-14", "P5_2-3-10", "P7_12-14", "P2_1-3"]:
    targets.append((u, True, [[l] for l in subcube(u)], rec.get(u, set()), certified.get(u, set())))

groups = {}
for t in targets:
    groups.setdefault((t[1], len(t[2])), []).append(t)
ok_all = True
for (keep, n), ts in groups.items():
    h = hashlib.sha256()
    with open(BASE, "rb") as f:
        first = f.readline()
        assert first.startswith(b"c zcnf")
        hdr = f.readline()
        assert hdr.startswith(b"p cnf")
        _, _, nv, nc = hdr.split()
        if keep:
            h.update(first)
        h.update(f"p cnf {int(nv)} {int(nc) + n}\n".encode())
        while True:
            b = f.read(1 << 24)
            if not b:
                break
            h.update(b)
    for label_, _, cls, exp, cert in ts:
        g = h.copy()
        g.update("".join(" ".join(map(str, c)) + " 0\n" for c in cls).encode())
        d = g.hexdigest()
        match = d in exp
        ok_all &= match
        print(f"{label_:24s} extra {n:4d}  my hash {d[:16]}  recorded {sorted(x[:16] for x in exp)}  match {match}"
              + ("" if cert is None else f"  certified record with this hash: {d in cert}"))
print("ALL MATCH" if ok_all else "SOME MISMATCH")
