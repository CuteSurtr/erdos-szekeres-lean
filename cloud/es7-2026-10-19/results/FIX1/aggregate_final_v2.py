#!/usr/bin/env python3
"""FIX1 v2 of results/V3Z/scripts/aggregate_final.py (AUDIT2/A4 findings 1 and 2). Changes, all
of them additional checks; everything else is unchanged:
 (v2-1) F must have sha256 F_SHA; cases.jsonl and cases.icnf must have the pinned sha256s, 450
        lines each, and every case CNF (F + cube units, as verify/v3/v3_check.py at 92746ac builds
        it) must hash to that case's cnf_sha256 in cases.jsonl.  Otherwise the script exits 2.
 (v2-2) a leaf record is used only if verdict VERIFIED, rc == 20, cake_lpr == "s VERIFIED UNSAT"
        exactly, and cnf_sha256 equal to the leaf CNF rebuilt here.  A leaf that contradicts its
        case cube needs no record (its CNF has x and -x as units); such leaves are counted.
 (v2-3) a cover record is used only if verdict VERIFIED, rc == 20, cake_lpr exactly
        "s VERIFIED UNSAT", nleaves equal, and cnf_sha256 equal to the cover CNF rebuilt here
        (case-cube units, then one clause -leaf per manifest leaf, header "p cnf MV NCL" with
        MV = max(nv, |lit|), as v3_check.py cover_job writes it), OR it carries exactly the note
        "the empty cube is a leaf" and the manifest's leaf list for the case is exactly [[]].
        As before, every cover record for (case, leaves_sha256) must be VERIFIED; in v2 every one
        of them must also pass this test, else the cover is a PROBLEM.

V3Z description: Acceptance table for V3Z (copy of results/V3T/scripts/aggregate.py, changed only as V3Z/TASK.md
step 4 allows: (a) a leaf counts as verified if any record for it is VERIFIED and no record for it
is SAT; a SAT record anywhere is printed first, prefixed SAT; TIMEOUT or REJECTED records next to a
VERIFIED one are only listed, prefixed NOTE; (b) the per-leaf cnf_sha256 is computed from a hash
object of the header and F's body cached per unit count; the bytes hashed are the same).

Original description: join v3_check.py outputs to the manifest by (case, lits).

usage: aggregate_final_v2.py ROOT F.cnf MANIFEST.jsonl OUT.tsv CHECK.jsonl [CHECK.jsonl ...]

A case is ACCEPTED only if its cover record is VERIFIED for exactly the manifest's leaf list of
that case (leaves_sha256 recomputed here) and every leaf of the case has a VERIFIED record whose
lits match and whose cnf_sha256 equals the CNF rebuilt here (F + case cube + extra leaf literals),
unless the leaf contradicts the cube. Problems (SAT, REJECTED, TIMEOUT, NOT_COVERED, missing,
sha mismatch) are printed one per line, prefixed PROBLEM.
"""
import sys, os, json, hashlib, collections, statistics

F_SHA = "69c1dc8f7818cbef615c1c6f65db66463294ea8054f0cec602846f27ffff932d"
CASES_JSONL_SHA = "5b58b4c62e4e01f4231a6847a695f11df44ff7fd81ab971fe3d6ec8225365225"
CASES_ICNF_SHA = "6b6f0946245da5cb33f287a0484c5ce7ef022bc26452a949848704018e6db742"
EXACT = "s VERIFIED UNSAT"
EMPTY_NOTE = "the empty cube is a leaf"


def die(msg):
    print("FATAL " + msg)
    sys.exit(2)


root, fpath, man, out = sys.argv[1:5]
checks = sys.argv[5:]
raw = open(fpath, "rb").read()
# (v2-1) pin F, cases.jsonl, cases.icnf and every case CNF
if hashlib.sha256(raw).hexdigest() != F_SHA:
    die(f"F sha256 {hashlib.sha256(raw).hexdigest()} is not {F_SHA}")
hdr, body = raw.split(b"\n", 1)
if hdr.split()[:2] != [b"p", b"cnf"] or not body.endswith(b"\n"):
    die("unexpected F layout")
nv, nc = int(hdr.split()[2]), int(hdr.split()[3])
cj = open(os.path.join(root, "results/Mii-S/cases.jsonl"), "rb").read()
ci = open(os.path.join(root, "results/Mii-S/cases.icnf"), "rb").read()
if hashlib.sha256(cj).hexdigest() != CASES_JSONL_SHA:
    die("cases.jsonl sha256 mismatch")
if hashlib.sha256(ci).hexdigest() != CASES_ICNF_SHA:
    die("cases.icnf sha256 mismatch")
cases = [json.loads(l) for l in cj.decode().splitlines()]
cubes = [l for l in ci.decode().splitlines() if l.startswith("a ")]
if len(cases) != 450 or len(cubes) != 450 or len({c["case"] for c in cases}) != 450:
    die("expected 450 distinct cases and 450 cubes")
cube_of = {}
for c, l in zip(cases, cubes):
    tok = l.split()
    if tok[-1] != "0":
        die(f"malformed cube line for {c['case']}")
    cube = sorted((int(x) for x in tok[1:-1]), key=abs)
    data = f"p cnf {nv} {nc + len(cube)}\n".encode() + body + "".join(f"{x} 0\n" for x in cube).encode()
    if hashlib.sha256(data).hexdigest() != c["cnf_sha256"]:
        die(f"case CNF sha256 mismatch for {c['case']}")
    cube_of[c["case"]] = cube

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

def cover_sha(cube, lv):
    # exactly the bytes of verify/v3/v3_check.py (92746ac) cover_job
    clauses = [[x] for x in cube] + [[-x for x in l] for l in lv]
    mv = max([nv] + [abs(x) for c in clauses for x in c])
    data = (f"p cnf {mv} {len(clauses)}\n" + "".join(" ".join(map(str, c)) + " 0\n" for c in clauses)).encode()
    return hashlib.sha256(data).hexdigest()


def cover_ok(o, case, lv):
    """(v2-3) None if the VERIFIED cover record o is valid for leaf list lv, else the reason."""
    if o.get("nleaves") != len(lv):
        return "nleaves mismatch"
    if "note" in o:
        if o["note"] == EMPTY_NOTE and lv == [[]]:
            return None
        return f"note {o['note']!r} but the leaf list is not exactly [[]] ({len(lv)} leaves)"
    if o.get("rc") != 20:
        return f"rc {o.get('rc')!r}"
    if o.get("cake_lpr") != EXACT:
        return f"cake_lpr {o.get('cake_lpr')!r}"
    if o.get("cnf_sha256") != cover_sha(cube_of[case], lv):
        return "cover cnf_sha256 mismatch"
    return None


sats, notes = [], []
ncontra = 0
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
    if cverd == "VERIFIED":
        bad = [x for x in (cover_ok(o, case, lv) for o in cv) if x]
        if bad:
            cverd = "INVALID"
            problems.append(f"PROBLEM cover {case}: VERIFIED record rejected by v2: {bad[0]} (nleaves {len(lv)})")
    else:
        problems.append(f"PROBLEM cover {case}: {cverd} (nleaves {len(lv)})")
    cube = cube_of[case]
    cs = set(cube)
    nver, st, ct, dirs = 0, 0.0, 0.0, set()
    for r in rs:
        dirs.update(os.path.dirname(s) if s.endswith(".icnf") else s for s in r["sources"])
        lst = leafrec.get((case, json.dumps(r["lits"])))
        if any(-x in cs for x in r["lits"]):
            # (v2-2) the leaf CNF contains x and -x as unit clauses: UNSAT without a record
            if lst and any(o["verdict"] == "SAT" for cf, o in lst):
                problems.append(f"PROBLEM leaf {case} {r['lits']}: SAT record for a leaf contradicting the cube")
                continue
            ncontra += 1
            nver += 1
            continue
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
        extra = sorted((x for x in r["lits"] if x not in cs), key=abs)
        units = cube + extra
        sha = cnf_sha(units)
        # (v2-2) a record is used only with the right CNF, solver exit 20 and the exact line
        good = [o for cf, o in ver if o.get("cnf_sha256") == sha and o.get("rc") == 20 and o.get("cake_lpr") == EXACT]
        if not good:
            problems.append(f"PROBLEM leaf {case} {r['lits']}: no VERIFIED record with matching cnf_sha256, rc 20 and the exact line")
            continue
        for cf, x in ver:
            if x.get("cnf_sha256") != sha:
                notes.append(f"NOTE leaf {case} {r['lits']}: VERIFIED record in {cf} with cnf_sha256 mismatch")
            elif x.get("rc") != 20 or x.get("cake_lpr") != EXACT:
                notes.append(f"NOTE leaf {case} {r['lits']}: VERIFIED record in {cf} without rc 20 and the exact line")
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
print(f"pinned: F {F_SHA}, cases.jsonl {CASES_JSONL_SHA}, cases.icnf {CASES_ICNF_SHA}, 450 case CNFs")
print(f"leaves accepted because they contradict the case cube (no record needed): {ncontra}")
acc = [r for r in rows if r[-1] == "ACCEPTED"]
print(f"cases {len(rows)} accepted {len(acc)} leaves verified {sum(r[2] for r in rows)} of {sum(r[1] for r in rows)}")
if times:
    s = [a for a, b in times]; c = [b for a, b in times]; t = [a + b for a, b in times]
    print(f"per solved leaf (n={len(times)}): solve median {statistics.median(s):.1f}s max {max(s):.1f}s; "
          f"check median {statistics.median(c):.1f}s max {max(c):.1f}s; solve+check median {statistics.median(t):.1f}s max {max(t):.1f}s")
