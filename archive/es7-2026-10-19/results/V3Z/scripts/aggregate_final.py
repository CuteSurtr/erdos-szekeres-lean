#!/usr/bin/env python3
"""Acceptance table for V3Z (copy of results/V3T/scripts/aggregate.py, changed only as V3Z/TASK.md
step 4 allows: (a) a leaf counts as verified if any record for it is VERIFIED and no record for it
is SAT; a SAT record anywhere is printed first, prefixed SAT; TIMEOUT or REJECTED records next to a
VERIFIED one are only listed, prefixed NOTE; (b) the per-leaf cnf_sha256 is computed from a hash
object of the header and F's body cached per unit count; the bytes hashed are the same).

Original description: join v3_check.py outputs to the manifest by (case, lits).

usage: aggregate.py ROOT F.cnf MANIFEST.jsonl OUT.tsv CHECK.jsonl [CHECK.jsonl ...]

A case is ACCEPTED only if its cover record is VERIFIED for exactly the manifest's leaf list of
that case (leaves_sha256 recomputed here) and every leaf of the case has a VERIFIED record whose
lits match and whose cnf_sha256 equals the CNF rebuilt here (F + case cube + extra leaf literals),
unless the leaf contradicts the cube. Problems (SAT, REJECTED, TIMEOUT, NOT_COVERED, missing,
sha mismatch) are printed one per line, prefixed PROBLEM.
"""
import sys, os, json, hashlib, collections, statistics

root, fpath, man, out = sys.argv[1:5]
checks = sys.argv[5:]
raw = open(fpath, "rb").read()
hdr, body = raw.split(b"\n", 1)
nv, nc = int(hdr.split()[2]), int(hdr.split()[3])
cases = [json.loads(l) for l in open(os.path.join(root, "results/Mii-S/cases.jsonl"))]
cubes = [l for l in open(os.path.join(root, "results/Mii-S/cases.icnf")) if l.startswith("a ")]
cube_of = {c["case"]: sorted((int(x) for x in l.split()[1:-1]), key=abs) for c, l in zip(cases, cubes)}

recs = [json.loads(l) for l in open(man)]
by_case = collections.defaultdict(list)
for r in recs:
    by_case[r["case"]].append(r)

leafrec, coverrec = {}, {}
for cf in checks:
    for l in open(cf):
        try:
            o = json.loads(l)
        except ValueError:
            continue
        if o["kind"] == "leaf" and "lits" in o:
            k = (o["case"], json.dumps(o["lits"]))
            # (a) every record is kept; the verdict is decided per leaf below
            leafrec.setdefault(k, []).append((cf, o))
        elif o["kind"] == "cover" and "leaves_sha256" in o:
            coverrec.setdefault((o["key"], o["leaves_sha256"]), []).append(o)

# (b) hash object of header + body, cached per unit count; copied before adding the units
hcache = {}
def cnf_sha(units):
    n = len(units)
    if n not in hcache:
        h = hashlib.sha256(f"p cnf {nv} {nc + n}\n".encode())
        h.update(body)
        hcache[n] = h
    h = hcache[n].copy()
    h.update("".join(f"{x} 0\n" for x in units).encode())
    return h.hexdigest()

sats, notes = [], []
for (case, lt), lst in leafrec.items():
    for cf, o in lst:
        if o["verdict"] == "SAT":
            sats.append(f"SAT leaf {case} {lt} in {cf}: rc={o.get('rc')}")

rows, problems, times = [], [], []
for case in sorted(by_case):
    rs = by_case[case]
    lv = [r["lits"] for r in rs]
    lsha = hashlib.sha256(json.dumps(lv).encode()).hexdigest()
    cv = coverrec.get((case, lsha), [])
    cverd = "MISSING" if not cv else ("VERIFIED" if all(o["verdict"] == "VERIFIED" for o in cv)
                                      else [o["verdict"] for o in cv if o["verdict"] != "VERIFIED"][0])
    if cverd != "VERIFIED":
        problems.append(f"PROBLEM cover {case}: {cverd} (nleaves {len(lv)})")
    cube = cube_of[case]
    cs = set(cube)
    nver, st, ct, dirs = 0, 0.0, 0.0, set()
    for r in rs:
        dirs.update(os.path.dirname(s) if s.endswith(".icnf") else s for s in r["sources"])
        lst = leafrec.get((case, json.dumps(r["lits"])))
        if lst is None:
            problems.append(f"PROBLEM leaf {case} {r['lits']}: MISSING sources {r['sources']}")
            continue
        if any(o["verdict"] == "SAT" for cf, o in lst):
            problems.append(f"PROBLEM leaf {case} {r['lits']}: SAT sources {r['sources']}")
            continue
        ver = [(cf, o) for cf, o in lst if o["verdict"] == "VERIFIED"]
        if not ver:
            o = lst[-1][1]
            problems.append(f"PROBLEM leaf {case} {r['lits']}: {'/'.join(o['verdict'] for cf, o in lst)} rc={o.get('rc')} "
                            f"cake={o.get('cake_lpr')!r} sources {r['sources']}")
            continue
        for cf, o in lst:
            if o["verdict"] != "VERIFIED":
                notes.append(f"NOTE leaf {case} {r['lits']}: {o['verdict']} in {cf} next to VERIFIED")
        o = ver[0][1]
        if not any(-x in cs for x in r["lits"]):
            extra = sorted((x for x in r["lits"] if x not in cs), key=abs)
            units = cube + extra
            sha = cnf_sha(units)
            good = [o for cf, o in ver if o.get("cnf_sha256") == sha]
            if not good:
                problems.append(f"PROBLEM leaf {case} {r['lits']}: cnf_sha256 mismatch")
                continue
            for cf, x in ver:
                if x.get("cnf_sha256") != sha:
                    notes.append(f"NOTE leaf {case} {r['lits']}: VERIFIED record in {cf} with cnf_sha256 mismatch")
            o = good[0]
            times.append((o["solve_s"], o["check_s"]))
        nver += 1
        st += o.get("solve_s", 0.0)
        ct += o.get("check_s", 0.0)
    for o in cv:
        st += o.get("solve_s", 0.0)
        ct += o.get("check_s", 0.0)
    acc = cverd == "VERIFIED" and nver == len(rs)
    rows.append((case, len(rs), nver, cverd, round(st, 2), round(ct, 2), ",".join(sorted(dirs)), "ACCEPTED" if acc else "NOT_ACCEPTED"))

with open(out, "w") as f:
    f.write("case\tnleaves\tnverified\tcover\tsolve_s\tcheck_s\twave1_dirs\tresult\n")
    for r in rows:
        f.write("\t".join(map(str, r)) + "\n")
for p in sats + problems + notes:
    print(p)
print(f"SAT records {len(sats)}")
acc = [r for r in rows if r[-1] == "ACCEPTED"]
print(f"cases {len(rows)} accepted {len(acc)} leaves verified {sum(r[2] for r in rows)} of {sum(r[1] for r in rows)}")
if times:
    s = [a for a, b in times]; c = [b for a, b in times]; t = [a + b for a, b in times]
    print(f"per solved leaf (n={len(times)}): solve median {statistics.median(s):.1f}s max {max(s):.1f}s; "
          f"check median {statistics.median(c):.1f}s max {max(c):.1f}s; solve+check median {statistics.median(t):.1f}s max {max(t):.1f}s")
