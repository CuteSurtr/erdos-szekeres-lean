#!/usr/bin/env python3
"""Mutation tests of the sub-case (ii) acceptance (AUDIT2/A4 NOTES.md, plus extra ones).
usage: mutate_agg.py ROOT F.cnf M.jsonl WORKDIR CHECK.jsonl [...]
Writes the mutated manifests / forged record files under WORKDIR and prints, for each test, the
last 'cases ... accepted ...' line (or FATAL) of the old aggregate_final.py and of v2."""
import hashlib, json, os, subprocess, sys

root, fpath, man, work = sys.argv[1:5]
checks = sys.argv[5:]
OLD = os.path.join(root, "results/V3Z/scripts/aggregate_final.py")
NEW = os.path.join(root, "results/FIX1/aggregate_final_v2.py")
os.makedirs(work, exist_ok=True)
CASE = "U12_L4"
recs = [json.loads(l) for l in open(man) if json.loads(l)["case"] == CASE]
lv_full = [r["lits"] for r in recs]
cases = {json.loads(l)["case"]: i for i, l in enumerate(open(os.path.join(root, "results/Mii-S/cases.jsonl")))}
cubes = [l for l in open(os.path.join(root, "results/Mii-S/cases.icnf")) if l.startswith("a ")]
cube = sorted((int(x) for x in cubes[cases[CASE]].split()[1:-1]), key=abs)
raw = open(fpath, "rb").read()
nv = int(raw.split(b"\n", 1)[0].split()[2])


def lsha(lv):
    return hashlib.sha256(json.dumps(lv).encode()).hexdigest()


def cover_bytes(lv):
    clauses = [[x] for x in cube] + [[-x for x in l] for l in lv]
    mv = max([nv] + [abs(x) for c in clauses for x in c])
    return (f"p cnf {mv} {len(clauses)}\n" + "".join(" ".join(map(str, c)) + " 0\n" for c in clauses)).encode()


def wman(name, rs):
    p = os.path.join(work, name)
    with open(p, "w") as f:
        for r in rs:
            f.write(json.dumps(r) + "\n")
    return p


def run(script, mp, extra, fpath=fpath):
    o = subprocess.run([sys.executable, script, root, fpath, mp, os.path.join(work, "out.tsv")] + checks + extra,
                       capture_output=True, text=True)
    lines = o.stdout.splitlines()
    last = next((l for l in lines if l.startswith("cases ") or l.startswith("FATAL")), f"(no summary, rc {o.returncode}) {o.stderr[-200:]}")
    probs = [l for l in lines if l.startswith("PROBLEM")]
    return f"rc {o.returncode}: {last}" + (f" | {probs[0][:150]}" if probs else "")


drop = recs[:-1]
lv = [r["lits"] for r in drop]
open(os.path.join(work, "cover127.cnf"), "wb").write(cover_bytes(lv))
st = subprocess.run(["cadical", "-q", os.path.join(work, "cover127.cnf")], capture_output=True, text=True)
print(f"{CASE}: {len(lv_full)} leaves; cover CNF with the last leaf dropped: cadical rc {st.returncode} "
      f"({next((l for l in st.stdout.splitlines() if l.startswith('s ')), '?')})")
m_full = wman("M_full.jsonl", recs)
m_drop = wman("M_drop.jsonl", drop)
real_sha = hashlib.sha256(cover_bytes(lv)).hexdigest()
tests = {
    "control: real U12_L4 manifest, real records": (m_full, []),
    "A4 (a): leaf dropped + forged cover with the empty-cube note": (m_drop, [{"kind": "cover", "key": CASE, "nleaves": len(lv), "leaves_sha256": lsha(lv), "verdict": "VERIFIED", "note": "the empty cube is a leaf"}]),
    "A4 (b): leaf dropped + forged cover cnf_sha256 0...0, cake_lpr ''": (m_drop, [{"kind": "cover", "key": CASE, "nleaves": len(lv), "leaves_sha256": lsha(lv), "cnf_sha256": "0" * 64, "rc": 20, "solve_s": 1.0, "cake_lpr": "", "check_s": 1.0, "verdict": "VERIFIED"}]),
    "extra (c): leaf dropped + forged cover with the right cnf_sha256 but cake_lpr ''": (m_drop, [{"kind": "cover", "key": CASE, "nleaves": len(lv), "leaves_sha256": lsha(lv), "cnf_sha256": real_sha, "rc": 20, "solve_s": 1.0, "cake_lpr": "", "check_s": 1.0, "verdict": "VERIFIED"}]),
    "extra (d): leaf dropped + forged cover with right sha and line but rc 10": (m_drop, [{"kind": "cover", "key": CASE, "nleaves": len(lv), "leaves_sha256": lsha(lv), "cnf_sha256": real_sha, "rc": 10, "solve_s": 1.0, "cake_lpr": "s VERIFIED UNSAT", "check_s": 1.0, "verdict": "VERIFIED"}]),
}
for name, (mp, forged) in tests.items():
    extra = []
    if forged:
        fp = os.path.join(work, "forged.jsonl")
        with open(fp, "w") as f:
            for o in forged:
                f.write(json.dumps(o) + "\n")
        extra = [fp]
    print(f"{name}\n  old: {run(OLD, mp, extra)}\n  v2:  {run(NEW, mp, extra)}")

# (f) leaf records: replace every record of one leaf of U12_L4 by a copy with cake_lpr '' (or rc 10)
leaf0 = json.dumps(recs[0]["lits"])
for tag, field, val in (("cake_lpr ''", "cake_lpr", ""), ("rc 10", "rc", 10)):
    mod = []
    for cf in checks:
        p = os.path.join(work, "mod_" + cf.replace("/", "_"))
        with open(cf) as f, open(p, "w") as g:
            for l in f:
                try:
                    o = json.loads(l)
                except ValueError:
                    g.write(l); continue
                if o.get("kind") == "leaf" and o.get("case") == CASE and json.dumps(o.get("lits")) == leaf0:
                    o[field] = val
                    l = json.dumps(o) + "\n"
                g.write(l)
        mod.append(p)
    saved = checks[:]
    checks[:] = mod
    print(f"extra (f): every record of leaf 0 of {CASE} with {tag} (verdict still VERIFIED)\n  old: {run(OLD, m_full, [])}\n  v2:  {run(NEW, m_full, [])}")
    checks[:] = saved
# (g) wrong F: one clause appended to F's body (header adjusted)
hdr, body = raw.split(b"\n", 1)
t = hdr.split()
fb = os.path.join(work, "Fbad.cnf")
open(fb, "wb").write(b"p cnf %s %d\n" % (t[2], int(t[3]) + 1) + body + b"1 2 0\n")
print(f"extra (g): F with one extra clause\n  old: {run(OLD, m_full, [], fb)}\n  v2:  {run(NEW, m_full, [], fb)}")
