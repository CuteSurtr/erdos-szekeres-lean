#!/usr/bin/env python3
"""Acceptance table for V3T: join v3_check.py outputs to the manifest by (case, lits).

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
            # a non-VERIFIED record anywhere is kept and reported
            if k not in leafrec or o["verdict"] != "VERIFIED":
                leafrec[k] = o
        elif o["kind"] == "cover" and "leaves_sha256" in o:
            coverrec.setdefault((o["key"], o["leaves_sha256"]), []).append(o)

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
        o = leafrec.get((case, json.dumps(r["lits"])))
        if o is None:
            problems.append(f"PROBLEM leaf {case} {r['lits']}: MISSING sources {r['sources']}")
            continue
        if o["verdict"] != "VERIFIED":
            problems.append(f"PROBLEM leaf {case} {r['lits']}: {o['verdict']} rc={o.get('rc')} "
                            f"cake={o.get('cake_lpr')!r} sources {r['sources']}")
            continue
        if not any(-x in cs for x in r["lits"]):
            extra = sorted((x for x in r["lits"] if x not in cs), key=abs)
            units = cube + extra
            data = f"p cnf {nv} {nc + len(units)}\n".encode() + body + "".join(f"{x} 0\n" for x in units).encode()
            if hashlib.sha256(data).hexdigest() != o.get("cnf_sha256"):
                problems.append(f"PROBLEM leaf {case} {r['lits']}: cnf_sha256 mismatch")
                continue
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
for p in problems:
    print(p)
acc = [r for r in rows if r[-1] == "ACCEPTED"]
print(f"cases {len(rows)} accepted {len(acc)} leaves verified {sum(r[2] for r in rows)} of {sum(r[1] for r in rows)}")
if times:
    s = [a for a, b in times]; c = [b for a, b in times]; t = [a + b for a, b in times]
    print(f"per solved leaf (n={len(times)}): solve median {statistics.median(s):.1f}s max {max(s):.1f}s; "
          f"check median {statistics.median(c):.1f}s max {max(c):.1f}s; solve+check median {statistics.median(t):.1f}s max {max(t):.1f}s")
