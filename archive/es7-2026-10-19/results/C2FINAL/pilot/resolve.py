#!/usr/bin/env python3
"""Re-solve the P8 pilot units that have no recorded CNF hash, keeping archived proofs.

Per unit, one process at a time:
- build the CNF exactly as C2P/tools/lane.py does and require its SHA-256 to equal the expected hash;
- CaDiCaL --lrat --binary=false with a cap;
- UNSAT: lrat-check; zstd archive into ARCHIVE with a decompress-and-hash round trip; cake_lpr (heap 8000 MB,
  11000 MB if exhausted); the raw proof is deleted only when both checkers accept and the round trip matches;
- one JSON record per unit appended to OUT.
A memory guard waits while active + wired + compressed memory exceeds GUARD_GB before each heavy step.
usage: resolve.py WORK BIN RESULTS EXPECTED_JSON ARCHIVE OUT UNIT..."""
import hashlib, json, os, re, subprocess, sys, time

WORK, BIN, RES, EXP, ARCH, OUT = sys.argv[1:7]
UNITS = sys.argv[7:]
CAP, GUARD_GB = 3600, 40.0
BASE = os.path.join(WORK, "base.cnf")
expected = json.load(open(EXP))["computed_for_no_hash"]
LOG = open(os.path.join(WORK, "resolve.log"), "a", buffering=1)
log = lambda m: LOG.write(time.strftime("%H:%M:%SZ ", time.gmtime()) + m + "\n")


def used_gb():
    out = subprocess.run(["vm_stat"], capture_output=True, text=True).stdout
    g = lambda k: int(re.search(rf"{k}:\s+(\d+)", out).group(1))
    return (g("Pages active") + g("Pages wired down") + g("Pages occupied by compressor")) * 16384 / 1e9


def guard():
    while (u := used_gb()) > GUARD_GB:
        log(f"guard: {u:.1f} GB in use, waiting"); time.sleep(30)


hull = {l.split()[0]: [int(x) for x in l.split()[1:]] for l in open(os.path.join(RES, "C2C34", "cubes.txt")) if l.strip()}
cubes, order = {}, []
for l in open(os.path.join(RES, "C2P", "cubes", "P8_cubes.txt")):
    if l.strip():
        n, *lits = l.split(); cubes[n] = [int(x) for x in lits]; order.append(n)


def extra(unit):
    if unit == "P8_cover":
        hs = set(hull["P8"]); cls = [[l] for l in hull["P8"]]
        cls += [[-x for x in cubes[n] if x not in hs] for n in order]
        return cls
    return [[l] for l in cubes[unit]]


def build(path, cls):
    h = hashlib.sha256()
    with open(BASE, "rb") as f, open(path, "wb") as g:
        while True:
            line = f.readline()
            if line.startswith(b"p cnf"):
                _, _, nv, nc = line.split()
                line = f"p cnf {int(nv)} {int(nc) + len(cls)}\n".encode(); g.write(line); h.update(line); break
            g.write(line); h.update(line)
        while (b := f.read(1 << 24)):
            g.write(b); h.update(b)
        tail = "".join(" ".join(map(str, c)) + " 0\n" for c in cls).encode(); g.write(tail); h.update(tail)
    return h.hexdigest()


def sha_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while (b := f.read(1 << 24)):
            h.update(b)
    return h.hexdigest()


def run(cmd, outpath=None):
    t0 = time.time(); p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    s = p.stdout.decode(errors="replace")
    if outpath: open(outpath, "w").write(s)
    return p.returncode, s, round(time.time() - t0, 1)


first = lambda s, pat: (m.group(0).strip() if (m := re.search(pat, s, re.M)) else None)
os.makedirs(ARCH, exist_ok=True)
for unit in UNITS:
    F, P, O = (os.path.join(WORK, f"{unit}.{x}") for x in ("cnf", "lrat", "out"))
    cnfsha = build(F, extra(unit))
    rec = {"unit": unit, "case": "P8", "cnf_sha256": cnfsha, "cnf_sha256_expected": expected[unit]}
    if cnfsha != expected[unit]:
        rec["status"] = "ERROR cnf hash mismatch"; log(f"{unit}: CNF hash mismatch")
    else:
        guard(); log(f"=== {unit} solve (cap {CAP})")
        ec, out, wall = run([os.path.join(BIN, "cadical"), "-t", str(CAP), "--lrat", "--binary=false", F, P], O)
        st = first(out, r"^s [A-Z]+"); st = st[2:] if st else ("UNKNOWN" if ec == 0 else f"ERROR exit {ec}")
        ts = re.search(r"total process time since initialization:\s+([\d.]+)", out)
        mb = re.search(r"maximum resident set size[^\d]*([\d.]+)\s*MB", out)
        rec.update(status=st, cap_s=CAP, solve_s=float(ts.group(1)) if ts else None, solve_wall_s=wall,
                   solve_rss_mb=float(mb.group(1)) if mb else None)
        if st == "UNSATISFIABLE":
            rec["proof_bytes"] = os.path.getsize(P); rec["proof_sha256"] = sha_file(P)
            _, o, t = run([os.path.join(BIN, "lrat-check"), F, P])
            rec["lrat_check"] = first(o, r"^.*(VERIFIED|FAIL|rror).*$"); rec["lrat_check_s"] = t
            A = os.path.join(ARCH, f"{unit}.lrat.zst")
            _, _, t = run(["zstd", "-q", "-f", "-T4", "-9", P, "-o", A]); rec["zstd_s"] = t
            rec["archive"] = os.path.relpath(A, os.path.dirname(ARCH)); rec["archive_bytes"] = os.path.getsize(A)
            rec["archive_sha256"] = sha_file(A)
            d = subprocess.run(f"zstd -dc '{A}' | shasum -a 256", shell=True, capture_output=True, text=True)
            rec["roundtrip"] = "verified" if d.stdout.split()[0] == rec["proof_sha256"] else "MISMATCH"
            if rec["lrat_check"] == "c VERIFIED":
                for heap in (8000, 11000):
                    guard()
                    _, o, t = run([os.path.join(BIN, "cake_lpr"), f"--CML_HEAP_SIZE={heap}", "--CML_STACK_SIZE=4000", F, P])
                    rec["cake_lpr"] = first(o, r"^.*(s VERIFIED|exhausted|rror|FAIL).*$") or "no verdict line"
                    rec["cake_s"] = t; rec["cake_heap_mb"] = heap
                    if "exhausted" not in rec["cake_lpr"]: break
            else:
                rec["cake_lpr"] = "not run"
            rec["certified"] = rec["lrat_check"] == "c VERIFIED" and rec.get("cake_lpr") == "s VERIFIED UNSAT"
            if rec["certified"] and rec["roundtrip"] == "verified":
                os.remove(P)
            else:
                rec["proof_kept"] = P
        elif st == "SATISFIABLE":
            os.replace(O, os.path.join(WORK, f"SAT_{unit}.out"))
    if os.path.exists(F): os.remove(F)
    rec["finished"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    with open(OUT, "a") as f: f.write(json.dumps(rec) + "\n")
    log(f"=== {unit} end {rec.get('status')} certified {rec.get('certified')} roundtrip {rec.get('roundtrip')}")
log("done")
