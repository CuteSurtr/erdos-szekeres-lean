#!/usr/bin/env python3
"""Re-verify mirror sub-case (ii) wave results from scratch, one leaf at a time.

For every manifest record whose idx is congruent to SHARD modulo NSHARDS:
  CNF = F + the case cube as unit clauses + the leaf literals not already in the case cube,
  written as: header "p cnf NV NC+k", F's clause body unchanged, then one unit clause per
  literal (case cube sorted by abs, then the extra leaf literals sorted by abs).
  The case part alone (F + case units) must hash to the case's cnf_sha256 in cases.jsonl,
  which pins the case cube; the script stops if it does not.
  CaDiCaL writes a text LRAT proof; the leaf counts as verified only if cake_lpr prints the
  exact line "s VERIFIED UNSAT". Proof and CNF files are deleted after the check.
For every case whose position in the sorted list of manifest cases is congruent to SHARD
modulo NSHARDS, it also checks the cover: the CNF {case cube units} + {not leaf : leaf}
must be UNSAT (cake_lpr verified), i.e. every assignment satisfying the case cube satisfies
some leaf.

Every job uses its own directory WORK/<kind>-<idx>, so concurrent jobs never share files.
Output records are appended to OUT (JSON lines); a rerun skips records already present.

usage: v3_check.py --root ROOT --base F.cnf --manifest M.jsonl --shard I --nshards N
                   --out OUT.jsonl [--work DIR] [--jobs 4] [--cap 3600]
                   [--cadical /opt/bin/cadical] [--cake /opt/bin/cake_lpr]
"""
import argparse, hashlib, json, os, shutil, subprocess, sys, tempfile, threading, time
from concurrent.futures import ThreadPoolExecutor

F_SHA = "69c1dc8f7818cbef615c1c6f65db66463294ea8054f0cec602846f27ffff932d"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--base", required=True)
    ap.add_argument("--manifest", required=True)
    ap.add_argument("--shard", type=int, required=True)
    ap.add_argument("--nshards", type=int, required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--work", default="/opt/work/v3")
    ap.add_argument("--jobs", type=int, default=4)
    ap.add_argument("--cap", type=int, default=3600)
    ap.add_argument("--cadical", default="/opt/bin/cadical")
    ap.add_argument("--cake", default="/opt/bin/cake_lpr")
    ap.add_argument("--skip-leaves", action="store_true", help="check only the covers of this shard's cases")
    ap.add_argument("--skip-covers", action="store_true", help="check only this shard's leaves")
    a = ap.parse_args()

    raw = open(a.base, "rb").read()
    if hashlib.sha256(raw).hexdigest() != F_SHA:
        sys.exit("base CNF sha256 mismatch")
    hdr, body = raw.split(b"\n", 1)
    t = hdr.split()
    if t[:2] != [b"p", b"cnf"] or not body.endswith(b"\n"):
        sys.exit("unexpected base CNF layout")
    nv, nc = int(t[2]), int(t[3])

    cases = [json.loads(l) for l in open(os.path.join(a.root, "results/Mii-S/cases.jsonl"))]
    cubes = [l for l in open(os.path.join(a.root, "results/Mii-S/cases.icnf")) if l.startswith("a ")]
    if len(cases) != 450 or len(cubes) != 450:
        sys.exit("expected 450 cases and 450 cubes")
    cube_of = {}
    for c, line in zip(cases, cubes):
        tok = line.split()
        if tok[-1] != "0":
            sys.exit("malformed cube line")
        cube = sorted((int(x) for x in tok[1:-1]), key=abs)
        data = f"p cnf {nv} {nc + len(cube)}\n".encode() + body + "".join(f"{x} 0\n" for x in cube).encode()
        if hashlib.sha256(data).hexdigest() != c["cnf_sha256"]:
            sys.exit(f"case CNF sha256 mismatch for {c['case']}")
        cube_of[c["case"]] = cube

    recs = [json.loads(l) for l in open(a.manifest)]
    for i, r in enumerate(recs):
        if r["idx"] != i:
            sys.exit("manifest indices are not 0..n-1 in order")
    mine = [r for r in recs if r["idx"] % a.nshards == a.shard]
    case_list = sorted({r["case"] for r in recs})
    my_cases = [c for i, c in enumerate(case_list) if i % a.nshards == a.shard]

    done = set()
    if os.path.exists(a.out):
        for l in open(a.out):
            try:
                o = json.loads(l)
            except ValueError:
                continue
            if o.get("verdict") in ("VERIFIED", "REJECTED", "SAT", "NOT_COVERED"):
                done.add((o["kind"], o["key"], o.get("case"), json.dumps(o.get("lits")), o.get("leaves_sha256")))
    lock = threading.Lock()
    outf = open(a.out, "a")

    def emit(o):
        with lock:
            outf.write(json.dumps(o) + "\n")
            outf.flush()

    def solve_check(w, data):
        os.makedirs(a.work, exist_ok=True)
        w = tempfile.mkdtemp(prefix=os.path.basename(w) + ".", dir=a.work)
        cnf, prf = os.path.join(w, "f.cnf"), os.path.join(w, "p.lrat")
        open(cnf, "wb").write(data)
        t0 = time.time()
        try:
            rc = subprocess.run([a.cadical, "-q", "--lrat", "--binary=false", cnf, prf],
                                stdout=subprocess.DEVNULL, timeout=a.cap).returncode
        except subprocess.TimeoutExpired:
            rc = "TIMEOUT"
        st = time.time() - t0
        pb = os.path.getsize(prf) if os.path.exists(prf) else 0
        line, ct = "", 0.0
        if rc == 20:
            t0 = time.time()
            o = subprocess.run([a.cake, cnf, prf], capture_output=True, text=True).stdout
            ct = time.time() - t0
            line = next((x.strip() for x in o.splitlines() if x.startswith("s ")), o[-120:])
        shutil.rmtree(w, ignore_errors=True)
        return rc, round(st, 2), pb, line, round(ct, 2)

    def leaf_job(r):
        key = r["idx"]
        if ("leaf", key, r["case"], json.dumps(r["lits"]), None) in done:
            return
        cube = cube_of[r["case"]]
        cs = set(cube)
        lits = r["lits"]
        if any(-x in cs for x in lits):
            emit({"kind": "leaf", "key": key, "case": r["case"], "lits": lits, "verdict": "VERIFIED",
                  "note": "leaf contradicts the case cube, so its CNF is trivially UNSAT"})
            return
        if any(abs(x) > nv for x in lits):
            emit({"kind": "leaf", "key": key, "case": r["case"], "lits": lits, "verdict": "REJECTED",
                  "note": "literal outside the variable range"})
            return
        extra = sorted((x for x in lits if x not in cs), key=abs)
        units = cube + extra
        data = f"p cnf {nv} {nc + len(units)}\n".encode() + body + "".join(f"{x} 0\n" for x in units).encode()
        sha = hashlib.sha256(data).hexdigest()
        rc, st, pb, line, ct = solve_check(os.path.join(a.work, f"leaf-{key}"), data)
        verdict = ("VERIFIED" if line == "s VERIFIED UNSAT" else
                   "SAT" if rc == 10 else "TIMEOUT" if rc == "TIMEOUT" else "REJECTED")
        emit({"kind": "leaf", "key": key, "case": r["case"], "lits": lits, "cnf_sha256": sha, "rc": rc,
              "solve_s": st, "proof_bytes": pb, "cake_lpr": line, "check_s": ct, "verdict": verdict})

    def cover_job(case):
        lv = [r["lits"] for r in recs if r["case"] == case]
        lsha = hashlib.sha256(json.dumps(lv).encode()).hexdigest()
        if ("cover", case, None, "null", lsha) in done:
            return
        cube = cube_of[case]
        if any(len(x) == 0 for x in lv):
            emit({"kind": "cover", "key": case, "nleaves": len(lv), "leaves_sha256": lsha, "verdict": "VERIFIED",
                  "note": "the empty cube is a leaf"})
            return
        clauses = [[x] for x in cube] + [[-x for x in l] for l in lv]
        mv = max([nv] + [abs(x) for c in clauses for x in c])
        data = (f"p cnf {mv} {len(clauses)}\n" + "".join(" ".join(map(str, c)) + " 0\n" for c in clauses)).encode()
        rc, st, pb, line, ct = solve_check(os.path.join(a.work, f"cover-{case}"), data)
        verdict = ("VERIFIED" if line == "s VERIFIED UNSAT" else
                   "NOT_COVERED" if rc == 10 else "TIMEOUT" if rc == "TIMEOUT" else "REJECTED")
        emit({"kind": "cover", "key": case, "nleaves": len(lv), "leaves_sha256": lsha, "cnf_sha256": hashlib.sha256(data).hexdigest(),
              "rc": rc, "solve_s": st, "cake_lpr": line, "check_s": ct, "verdict": verdict})

    with ThreadPoolExecutor(a.jobs) as ex:
        jobs = [] if a.skip_covers else [ex.submit(cover_job, c) for c in my_cases]
        jobs += [] if a.skip_leaves else [ex.submit(leaf_job, r) for r in mine]
        for f in jobs:
            f.result()
    outf.close()
    print("shard", a.shard, "of", a.nshards, "leaves", len(mine), "covers", len(my_cases))


if __name__ == "__main__":
    main()
