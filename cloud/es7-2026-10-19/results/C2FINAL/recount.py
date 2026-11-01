#!/usr/bin/env python3
"""Independent recount of the central 34-point parallelogram cases P1..P8.

Derives the 560 second-layer subcases of each case and their reflection orbits (i -> (a - i) mod 17) from scratch,
reads every run record (pilot TSV + all C2P* out.jsonl), and counts an orbit as closed only if some member has a
record with status UNSATISFIABLE, lrat_check "c VERIFIED" and cake_lpr "s VERIFIED UNSAT". Does not use the
'certified' field (only cross-checks it) and does not use C2P3/check_case.py.
usage: recount.py RESULTS_DIR [OUT_JSON]"""
import collections, csv, glob, itertools, json, os, sys

RES = sys.argv[1]
OUT = sys.argv[2] if len(sys.argv) > 2 else None


def ok(r):
    return (r.get("status") == "UNSATISFIABLE" and r.get("lrat_check") == "c VERIFIED"
            and r.get("cake_lpr") == "s VERIFIED UNSAT")


recs = []
for f in sorted(glob.glob(os.path.join(RES, "C2P*", "*", "out.jsonl"))):
    src = "/".join(f.split("/")[-3:-1])
    for i, line in enumerate(open(f)):
        if line.strip():
            r = json.loads(line); r["_src"] = f"{src}:{i + 1}"; recs.append(r)
with open(os.path.join(RES, "C2C34", "logs", "p8_units.tsv")) as fh:
    for i, r in enumerate(csv.DictReader(fh, delimiter="\t")):
        r["case"] = "P8"; r["_src"] = f"C2C34/pilot:{i + 2}"; r["_pilot"] = True; recs.append(r)

problems = []
status = collections.Counter(r.get("status") for r in recs)
bad = [r for r in recs if r.get("status") not in ("UNSATISFIABLE", "UNKNOWN")]
for r in bad:
    problems.append(f"non-UNSAT/UNKNOWN status {r.get('status')!r}: {r['unit']} {r['_src']}")
for r in recs:
    if r.get("status") == "UNSATISFIABLE" and not ok(r):
        problems.append(f"UNSAT but not accepted by both checkers: {r['unit']} {r['_src']} "
                        f"lrat={r.get('lrat_check')!r} cake={r.get('cake_lpr')!r}")
    if "certified" in r and bool(r["certified"]) != ok(r):
        problems.append(f"'certified' field disagrees with verdict strings: {r['unit']} {r['_src']}")

# CNF hash consistency per unit name (same unit built twice must give the same CNF)
hashes = collections.defaultdict(set)
for r in recs:
    if r.get("cnf_sha256"):
        hashes[r["unit"]].add(r["cnf_sha256"])
for u, hs in hashes.items():
    if len(hs) > 1:
        problems.append(f"unit {u} has {len(hs)} different cnf_sha256 values")

by_unit = collections.defaultdict(list)
for r in recs:
    by_unit[r["unit"]].append(r)

report = {"records": len(recs), "status_counts": dict(status), "cases": {}}
for a in range(1, 9):
    case = f"P{a}"
    inner = [i for i in range(1, 17) if i != a]
    subs = [tuple(c) for k in (2, 3) for c in itertools.combinations(inner, k)]
    name = lambda V: f"{case}_" + "-".join(map(str, sorted(V)))
    f = lambda V: tuple(sorted((a - i) % 17 for i in V))
    assert all(set(f(V)) <= set(inner) for V in subs)
    assert all(f(f(V)) == tuple(sorted(V)) for V in subs)
    # the subcase names must be exactly the cube file's names
    cube_names = [l.split(" ", 1)[0] for l in open(os.path.join(RES, "C2P", "cubes", f"{case}_cubes.txt")) if l.strip()]
    if sorted(cube_names) != sorted(name(V) for V in subs) or len(cube_names) != 560:
        problems.append(f"{case}: cube file names differ from the derived 560 subcases")
    orbits = {}
    for V in subs:
        key = min(name(V), name(f(V)))
        orbits.setdefault(key, set()).update({name(V), name(f(V))})
    fixed = sum(1 for V in subs if f(V) == tuple(sorted(V)))
    closed, open_, closers = 0, [], collections.Counter()
    for key, mem in orbits.items():
        good = [r for m in mem for r in by_unit.get(m, []) if ok(r)]
        if good:
            closed += 1
            closers["pilot" if all(r.get("_pilot") for r in good) else "wave"] += 1
        else:
            open_.append(key)
    cover = [r for r in by_unit.get(f"{case}_cover", []) if ok(r)]
    # sub-unit records (e.g. third-layer pieces "P8_3-11/...") never close an orbit here
    sub_units = sum(1 for u in by_unit if u.startswith(case + "_") and "/" in u)
    report["cases"][case] = {"subcases": len(subs), "orbits": len(orbits), "fixed": fixed, "closed": closed,
                             "open": sorted(open_), "cover_certified": len(cover),
                             "cover_srcs": [r["_src"] for r in cover],
                             "orbits_closed_only_by_pilot_records": closers["pilot"],
                             "subunit_names_ignored": sub_units}
    if not cover:
        problems.append(f"{case}: no certified cover record")
    if open_:
        problems.append(f"{case}: {len(open_)} open orbits")

used = {r["unit"] for r in recs if ok(r)}
no_hash = sorted(u for u in used if not any(r.get("cnf_sha256") for r in by_unit[u] if ok(r)))
report["certified_units_without_any_cnf_hash"] = no_hash
report["problems"] = problems
print(json.dumps({k: v for k, v in report.items() if k != "certified_units_without_any_cnf_hash"}, indent=1))
print("certified units whose every certified record lacks a cnf_sha256:", len(no_hash), no_hash[:12])
if OUT:
    json.dump(report, open(OUT, "w"), indent=1)
