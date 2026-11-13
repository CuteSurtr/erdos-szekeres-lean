#!/usr/bin/env python3
"""Auditor A5: close the central-34 case split using ONLY my own semantic cubes and my own derivation of the maps.

For every run record (C2C34 hex table, C2C34 pilot table, C2P*/*/out.jsonl, C2FINAL/pilot re-solves) the CNF the lane
hashed is rebuilt from the streamed base plus my semantic cube (format of the lane scripts) and its SHA-256 compared
with the recorded one. A unit counts as refuted only through a record with status UNSATISFIABLE, lrat-check
'c VERIFIED', cake_lpr 's VERIFIED UNSAT', and a recorded CNF hash equal to my rebuild.
Then: all 120 hexagonal hull cases refuted? every P_a cover (a = 1..8) refuted? every orbit {V, (a - V) mod 17} of
every P_a (a = 1..8) has a refuted member?  (P_9..P_16 are reduced to P_8..P_1 by (A); hull cover hash checked too.)
usage: orbitclosure.py BASE_CNF BASE_JSON RESULTS_DIR"""
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


hull_names = [f"P{a}" for a in range(1, T)] + [f"H{a}-{b}" for a, b in itertools.combinations(range(1, T), 2)]
hc = {n: (semantic_cube({0, int(n[1:])}) if n[0] == "P" else semantic_cube({0} | {int(x) for x in n[1:].split("-")}))
      for n in hull_names}
sub = {}
order = {}
for a in range(1, 9):
    inner = [o for o in range(1, T) if o != a]
    order[a] = []
    for h in (2, 3):
        for V in itertools.combinations(inner, h):
            n = f"P{a}_" + "-".join(map(str, V))
            sub[n] = semantic_cube({0, a}, set(V))
            order[a].append(n)


def extra(unit):
    if unit in hc:
        return [[l] for l in hc[unit]]
    if unit.endswith("_cover"):
        a = int(unit[1:].split("_")[0])
        hs = set(hc[f"P{a}"])
        return [[l] for l in hc[f"P{a}"]] + [[-x for x in sub[n] if x not in hs] for n in order[a]]
    return [[l] for l in sub[unit]]


states = {}


def state(n, keep=True):
    if (n, keep) not in states:
        h = hashlib.sha256()
        with open(BASE, "rb") as f:
            first = f.readline()
            hdr = f.readline()
            _, _, nv, nc = hdr.split()
            if keep:
                h.update(first)
            h.update(f"p cnf {int(nv)} {int(nc) + n}\n".encode())
            while True:
                b = f.read(1 << 24)
                if not b:
                    break
                h.update(b)
        states[(n, keep)] = h
    return states[(n, keep)].copy()


def digest(cls, keep=True):
    g = state(len(cls), keep)
    g.update("".join(" ".join(map(str, c)) + " 0\n" for c in cls).encode())
    return g.hexdigest()


# records: (source, unit, status, lrat, cake, hash)
recs = []
for r in csv.DictReader(open(os.path.join(RES, "C2C34", "logs", "hex_cases.tsv")), delimiter="\t"):
    recs.append(("hex", r["case"], r["status"], r["lrat_check"], r["cake_lpr"], r["cnf_sha256"]))
for r in csv.DictReader(open(os.path.join(RES, "C2C34", "logs", "p8_units.tsv")), delimiter="\t"):
    recs.append(("pilot", r["unit"], r["status"], r["lrat_check"], r["cake_lpr"], r["cnf_sha256"]))
for f in sorted(glob.glob(os.path.join(RES, "C2P*", "*", "out.jsonl"))) + [os.path.join(RES, "C2FINAL", "pilot", "out.jsonl")]:
    src = "/".join(f.split("/")[-3:-1])
    for line in open(f):
        if line.strip():
            r = json.loads(line)
            recs.append((src, r["unit"], r.get("status"), r.get("lrat_check"), r.get("cake_lpr"), r.get("cnf_sha256", "")))

stats = dict(records=len(recs), third_layer=0, no_hash=0, hash_match=0, hash_mismatch=0, unknown_unit=0)
refuted = set()
mismatches = []
for src, unit, st, lc, ck, hsh in recs:
    if "/" in unit:
        stats["third_layer"] += 1
        continue
    if unit not in hc and unit not in sub and not unit.endswith("_cover"):
        stats["unknown_unit"] += 1
        continue
    if not hsh:
        stats["no_hash"] += 1
        continue
    d = digest(extra(unit))
    if d != hsh:
        stats["hash_mismatch"] += 1
        mismatches.append(f"{src} {unit} {st}")
        continue
    stats["hash_match"] += 1
    if st == "UNSATISFIABLE" and lc == "c VERIFIED" and ck == "s VERIFIED UNSAT":
        refuted.add(unit)
print("records:", stats)
print("hash mismatches (first 10):", mismatches[:10])
hull_cover = digest([[-l for l in hc[n]] for n in hull_names], keep=False)
print("hull cover rebuilt from my cubes:", hull_cover, "== CERTIFICATES.md bb60facb...:",
      hull_cover == "bb60facb223788fb57291c73abfacd6deaa1eccd82ad2be9f50d36292959a60f")
hexes = [n for n in hull_names if n[0] == "H"]
print("hexagonal hull cases refuted:", sum(n in refuted for n in hexes), "of", len(hexes))
ok = all(n in refuted for n in hexes)
for a in range(1, 9):
    cov = f"P{a}_cover" in refuted
    orbits = {}
    for n in order[a]:
        V = [int(x) for x in n.split("_")[1].split("-")]
        m = f"P{a}_" + "-".join(map(str, sorted((a - i) % T for i in V)))
        assert m in sub
        orbits[frozenset((n, m))] = None
    closed = sum(1 for o in orbits if any(x in refuted for x in o))
    fixed = sum(1 for o in orbits if len(o) == 1)
    print(f"P{a}: cover refuted {cov}; orbits {len(orbits)} (fixed {fixed}); closed {closed}; "
          f"both members refuted {sum(1 for o in orbits if len(o) == 2 and all(x in refuted for x in o))}")
    ok &= cov and closed == len(orbits) == 287
print("CASE SPLIT CLOSED (with my cubes and the records)" if ok else "NOT CLOSED")
