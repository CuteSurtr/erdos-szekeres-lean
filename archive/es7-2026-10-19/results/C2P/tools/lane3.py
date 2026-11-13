#!/usr/bin/env python3
"""One C2P lane (lane3.py: also third-layer units SUBCASE/W and SUBCASE/cover from cubes3/SUBCASE.txt): solve and certify units of the central 34-point parallelogram cases, one at a time.

For each row of UNITS (columns idx, unit, case, kind, cap_s), in order, while time remains before END:
- build WORK/unit.cnf: the base CNF plus the unit's cube literals as unit clauses (cubes/<case>_cubes.txt). For
  <case>_cover: the base plus the hull cube of the case (results/C2C34/cubes.txt) as units and one clause per subcase
  forbidding its second-layer literals (as results/C2C34/p8/mkunits.py does for P8);
- run CaDiCaL --lrat --binary=false with cap min(cap_s, time left - RESERVE);
- UNSAT: lrat-check, then cake_lpr (heap 8000 MB; heap 11000 MB again if the heap is exhausted); the proof is
  deleted afterwards in every case (its size and sha256 are recorded);
- SAT: the solver output (with the model) is kept as WORK/SAT_<unit>.out and the file WORK/SAT_FOUND is written;
  the lane continues with the next unit.
One JSON record per unit is appended to OUT. No unit is started with less than MIN_START s left.
usage: lane.py WORK RESULTS UNITS OUT END_EPOCH
  WORK: base.cnf and bin/{cadical,lrat-check,cake_lpr};  RESULTS: the results directory of the repository."""
import hashlib, json, os, re, subprocess, sys, time
WORK, RES, UNITS, OUT, END = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], int(sys.argv[5])
RESERVE, MIN_START = 600, 900
BIN = os.path.join(WORK, "bin"); BASE = os.path.join(WORK, "base.cnf")
LOG = open(os.path.join(WORK, "lane.log"), "a", buffering=1)
log = lambda m: LOG.write(time.strftime("%H:%M:%SZ ", time.gmtime()) + m + "\n")


def cube(case, unit):
    for l in open(os.path.join(RES, "C2P", "cubes", f"{case}_cubes.txt")):
        if l.split(" ", 1)[0] == unit:
            return [int(x) for x in l.split()[1:]]
    raise KeyError(unit)


def extra_clauses(case, unit):
    if "/" in unit:                                  # third-layer unit SUBCASE/W or SUBCASE/cover (cubes3/SUBCASE.txt)
        sub, w = unit.split("/")
        l3 = os.path.join(RES, "C2P", "cubes3", f"{sub}.txt")
        if w == "cover":
            l2 = cube(case, sub); hs = set(l2); cls = [[l] for l in l2]
            for l in open(l3):
                if l.strip():
                    lits = [int(x) for x in l.split()[1:]]; assert hs <= set(lits)
                    cls.append([-x for x in lits if x not in hs])
            return cls
        for l in open(l3):
            if l.split(" ", 1)[0] == unit:
                return [[int(x)] for x in l.split()[1:]]
        raise KeyError(unit)
    if unit.endswith("_cover"):
        hull = next([int(x) for x in l.split()[1:]] for l in open(os.path.join(RES, "C2C34", "cubes.txt"))
                    if l.split(" ", 1)[0] == case)
        hs = set(hull); cls = [[l] for l in hull]
        for l in open(os.path.join(RES, "C2P", "cubes", f"{case}_cubes.txt")):
            if l.strip():
                lits = [int(x) for x in l.split()[1:]]; assert hs <= set(lits)
                cls.append([-x for x in lits if x not in hs])
        return cls
    return [[l] for l in cube(case, unit)]


def build(path, cls):
    """base + extra clauses; returns the sha256 of the written file"""
    h = hashlib.sha256()
    with open(BASE, "rb") as f, open(path, "wb") as g:
        while True:
            line = f.readline()
            if line.startswith(b"p cnf"):
                _, _, nv, nc = line.split()
                line = f"p cnf {int(nv)} {int(nc) + len(cls)}\n".encode()
                g.write(line); h.update(line); break
            g.write(line); h.update(line)
        while True:
            b = f.read(1 << 24)
            if not b: break
            g.write(b); h.update(b)
        tail = "".join(" ".join(map(str, c)) + " 0\n" for c in cls).encode()
        g.write(tail); h.update(tail)
    return h.hexdigest()


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            b = f.read(1 << 24)
            if not b: return h.hexdigest()
            h.update(b)


def first(out, pat):
    m = re.search(pat, out, re.M)
    return m.group(0).strip() if m else None


def run(cmd, outpath=None):
    t0 = time.time()
    p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    s = p.stdout.decode(errors="replace")
    if outpath: open(outpath, "w").write(s)
    return p.returncode, s, round(time.time() - t0, 1)


rows = [l.rstrip("\n").split("\t") for l in open(UNITS) if l.strip() and not l.startswith("idx")]
for idx, unit, case, kind, cap in rows:
    left = END - time.time()
    if left < MIN_START:
        log(f"stop: {int(left)} s left"); break
    lim = int(min(int(cap), left - RESERVE))
    cls = extra_clauses(case, unit)
    F = os.path.join(WORK, "unit.cnf"); P = os.path.join(WORK, "unit.lrat"); O = os.path.join(WORK, "unit.out")
    log(f"=== UNIT {unit} start (cap {lim})")
    cnfsha = build(F, cls)
    ec, out, wall = run([os.path.join(BIN, "cadical"), "-t", str(lim), "--lrat", "--binary=false", F, P], O)
    st = first(out, r"^s [A-Z]+")
    st = st[2:] if st else ("UNKNOWN" if ec == 0 else f"ERROR exit {ec}")
    ts = re.search(r"total process time since initialization:\s+([\d.]+)", out)
    mb = re.search(r"maximum resident set size[^\d]*([\d.]+)\s*MB", out)
    rec = {"unit": unit, "case": case, "kind": kind, "status": st, "cap_s": lim,
           "solve_s": float(ts.group(1)) if ts else None, "solve_wall_s": wall,
           "solve_rss_mb": float(mb.group(1)) if mb else None, "extra_clauses": len(cls), "cnf_sha256": cnfsha}
    if st == "UNSATISFIABLE":
        rec["proof_bytes"] = os.path.getsize(P); rec["proof_sha256"] = sha(P)
        _, o, t = run([os.path.join(BIN, "lrat-check"), F, P])
        rec["lrat_check"] = first(o, r"^.*(VERIFIED|FAIL|rror).*$"); rec["lrat_check_s"] = t
        if rec["lrat_check"] == "c VERIFIED":
            for heap in (8000, 11000):
                _, o, t = run([os.path.join(BIN, "cake_lpr"), f"--CML_HEAP_SIZE={heap}", "--CML_STACK_SIZE=4000", F, P])
                rec["cake_lpr"] = first(o, r"^.*(s VERIFIED|exhausted|rror|FAIL).*$") or "no verdict line"
                rec["cake_s"] = t; rec["cake_heap_mb"] = heap
                if "exhausted" not in rec["cake_lpr"]: break
        else:
            rec["cake_lpr"] = "not run"
        rec["certified"] = rec["lrat_check"] == "c VERIFIED" and rec.get("cake_lpr") == "s VERIFIED UNSAT"
    elif st == "SATISFIABLE":
        os.replace(O, os.path.join(WORK, f"SAT_{unit}.out")); open(os.path.join(WORK, "SAT_FOUND"), "a").write(unit + "\n")
    for x in (P, F):
        if os.path.exists(x): os.remove(x)
    rec["finished"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    with open(OUT, "a") as f: f.write(json.dumps(rec) + "\n")
    log(f"=== UNIT {unit} end {st} solve {rec['solve_s']} certified {rec.get('certified')}")
log("lane done")
