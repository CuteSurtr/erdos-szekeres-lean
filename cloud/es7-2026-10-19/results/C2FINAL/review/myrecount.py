#!/usr/bin/env python3
"""Independent recount (reviewer's own code). Reads raw records only.
usage: myrecount.py RESULTS_DIR OUT_JSON"""
import csv, glob, itertools, json, os, sys
from collections import defaultdict, Counter

RES, OUTJ = sys.argv[1], sys.argv[2]
T = 17

recs = []  # (source, record dict)
files = sorted(glob.glob(os.path.join(RES, "C2P*", "**", "out.jsonl"), recursive=True))
for f in files:
    src = os.path.relpath(f, RES)
    for i, line in enumerate(open(f)):
        if not line.strip():
            continue
        try:
            r = json.loads(line)
        except Exception as e:
            print("BAD JSON", src, i, e); continue
        recs.append((f"{src}:{i+1}", r))
with open(os.path.join(RES, "C2C34", "logs", "p8_units.tsv")) as fh:
    for i, r in enumerate(csv.DictReader(fh, delimiter="\t")):
        recs.append((f"C2C34/logs/p8_units.tsv:{i+2}", dict(r)))
pilot = [(f"C2FINAL/pilot/out.jsonl:{i+1}", json.loads(l)) for i, l in
         enumerate(open(os.path.join(RES, "C2FINAL", "pilot", "out.jsonl"))) if l.strip()]

print("record files:", len(files), "records:", len(recs), "pilot re-solve:", len(pilot))
print("files outside depth C2P*/X/out.jsonl:", [os.path.relpath(f, RES) for f in files if os.path.relpath(f, RES).count("/") != 2])

def accepted(r):
    return (r.get("status") == "UNSATISFIABLE" and r.get("lrat_check") == "c VERIFIED"
            and r.get("cake_lpr") == "s VERIFIED UNSAT")

issues = []
status_ct = Counter()
keysets = Counter()
by_unit = defaultdict(list)
for src, r in recs:
    u = r.get("unit"); st = r.get("status")
    status_ct[st] += 1
    keysets[tuple(sorted(r))] += 1
    case = r.get("case")
    if case is None and "p8_units" in src:
        case = "P8"
    prefix = u.split("_")[0]
    if case != prefix:
        issues.append(f"case/unit prefix mismatch {src} unit={u} case={case}")
    if st not in ("UNSATISFIABLE", "UNKNOWN"):
        issues.append(f"status {st!r} at {src} {u}")
    if st == "UNSATISFIABLE":
        if r.get("lrat_check") != "c VERIFIED" or r.get("cake_lpr") != "s VERIFIED UNSAT":
            issues.append(f"UNSAT not doubly accepted {src} {u} lrat={r.get('lrat_check')!r} cake={r.get('cake_lpr')!r}")
        if not r.get("proof_sha256") or not r.get("proof_bytes"):
            issues.append(f"UNSAT without proof hash/size {src} {u}")
    else:
        for k in ("lrat_check", "cake_lpr", "proof_sha256", "certified"):
            if k in r and r[k] not in ("", None):
                issues.append(f"non-UNSAT record with field {k}={r[k]!r} {src} {u}")
    if "certified" in r and r["certified"] not in ("", None):
        c = r["certified"] in (True, "True")
        if c != accepted(r):
            issues.append(f"certified field disagrees {src} {u} certified={r['certified']!r}")
    if not r.get("cnf_sha256"):
        issues.append(f"no cnf_sha256 {src} {u} {st}")
    if r.get("proof_kept") not in (None, "", "False", False):
        issues.append(f"proof_kept {src} {u} {r.get('proof_kept')}")
    by_unit[u].append((src, r))

# conflicting outcomes for the same unit (e.g. SAT and UNSAT) and differing cnf hashes for the same unit
for u, L in by_unit.items():
    sts = {r.get("status") for _, r in L}
    if "SATISFIABLE" in sts:
        issues.append(f"unit {u} has a SAT record")
    hs = {r.get("cnf_sha256") for _, r in L if r.get("cnf_sha256")}
    if len(hs) > 1:
        issues.append(f"unit {u}: {len(hs)} distinct cnf hashes over {len(L)} records: {[(s, r.get('cnf_sha256','')[:10]) for s, r in L]}")
    ps = {r.get("proof_sha256") for _, r in L if r.get("proof_sha256")}
    if len(ps) > 1:
        issues.append(f"unit {u}: {len(ps)} distinct proof hashes: {[(s, r.get('proof_sha256','')[:10]) for s, r in L if r.get('proof_sha256')]}")

# pilot re-solve consistency with original pilot rows
for src, r in pilot:
    u = r["unit"]
    if not accepted(r): issues.append(f"pilot re-solve not accepted {src} {u}")
    if r.get("cnf_sha256") != r.get("cnf_sha256_expected"): issues.append(f"pilot cnf hash != expected {src} {u}")
    orig = [x for s, x in by_unit.get(u, []) if "p8_units" in s]
    if not orig: issues.append(f"pilot re-solve {u} has no pilot row")
    for o in orig:
        if o.get("cnf_sha256"): issues.append(f"pilot row {u} already had a hash")
        if u != "P8_cover" and o.get("proof_sha256") != r.get("proof_sha256"):
            issues.append(f"pilot re-solve {u}: proof hash differs from pilot row")

# cube files
def subcases(a):
    inner = [i for i in range(1, T) if i != a]
    return [V for h in (2, 3) for V in itertools.combinations(inner, h)]

def name(a, V):
    return f"P{a}_" + "-".join(map(str, V))

def refl(a, V):
    return tuple(sorted((a - i) % T for i in V))

summary = {}
all_units_needed = set()
for a in range(1, 9):
    S = subcases(a)
    names = [name(a, V) for V in S]
    assert len(set(names)) == 560
    cf = os.path.join(RES, "C2P", "cubes", f"P{a}_cubes.txt")
    cnames = [l.split()[0] for l in open(cf) if l.strip()]
    if sorted(cnames) != sorted(names) or len(cnames) != 560:
        issues.append(f"cube file P{a}: names differ from subcases ({len(cnames)} lines, "
                      f"missing {sorted(set(names)-set(cnames))[:5]}, extra {sorted(set(cnames)-set(names))[:5]})")
    # reflection maps subcases to subcases, involution
    Sset = set(S)
    for V in S:
        W = refl(a, V)
        if W not in Sset or refl(a, W) != V:
            issues.append(f"reflection problem P{a} {V} -> {W}")
    orbits = {frozenset([V, refl(a, V)]) for V in S}
    fixed = sum(1 for o in orbits if len(o) == 1)
    closed_orbits = 0; open_orbits = []
    closing_src = Counter()
    for o in orbits:
        srcs = []
        for V in o:
            for s, r in by_unit.get(name(a, V), []) + [(s, r) for s, r in pilot if r["unit"] == name(a, V)]:
                if accepted(r) and r.get("cnf_sha256"):
                    srcs.append(s)
        if srcs:
            closed_orbits += 1
            for s in srcs: closing_src[s.split("/")[0]] += 1
        else:
            open_orbits.append(sorted(name(a, V) for V in o))
    cov = [(s, r) for s, r in by_unit.get(f"P{a}_cover", []) + [(s, r) for s, r in pilot if r["unit"] == f"P{a}_cover"]
           if accepted(r) and r.get("cnf_sha256")]
    cov_any = [(s, r.get("status")) for s, r in by_unit.get(f"P{a}_cover", [])]
    summary[f"P{a}"] = {"subcases": len(S), "orbits": len(orbits), "fixed": fixed, "closed": closed_orbits,
                        "open": open_orbits, "cover_accepted_hashed": [s for s, _ in cov], "cover_all": cov_any}
    print(f"P{a}: subcases {len(S)} orbits {len(orbits)} fixed {fixed} closed {closed_orbits} open {len(open_orbits)} "
          f"cover(acc+hash) {[s for s,_ in cov]}  all cover recs {cov_any}")
    if open_orbits: print("   OPEN:", open_orbits[:10])

# third-layer units
third = sorted({u for u in by_unit if "/" in u})
print("third-layer units:", len(third), third[:20])
print("status counts:", dict(status_ct))
print("distinct key sets:", len(keysets))
for k, v in keysets.items(): print("  ", v, k)
print("ISSUES:", len(issues))
for x in issues: print("  ", x)
json.dump({"summary": summary, "issues": issues, "status": dict(status_ct)}, open(OUTJ, "w"), indent=1)
