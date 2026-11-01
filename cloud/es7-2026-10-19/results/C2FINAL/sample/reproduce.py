#!/usr/bin/env python3
"""Re-solve recorded central-34 subcase units and compare with their records.

Per unit, one process at a time: rebuild the CNF exactly as C2P/tools/lane.py does and require its SHA-256 to equal the
record's cnf_sha256; run CaDiCaL --lrat --binary=false; record whether the proof's size and SHA-256 equal the
recorded ones; check the new proof with lrat-check and cake_lpr; delete the proof (it is regenerable when it
reproduces the record). A memory guard waits while active + wired + compressed memory exceeds GUARD_GB.
usage: reproduce.py WORK BIN RESULTS OUT UNIT[@SOURCE]...   (SOURCE like C2P/M02 picks that machine's record)"""
import glob, hashlib, json, os, re, subprocess, sys, time

WORK, BIN, RES, OUT = sys.argv[1:5]
CAP, GUARD_GB = 3600, 40.0
ARCH = os.environ.get("REPRO_ARCHIVE")  # if set: zstd-archive each proof there with a round-trip check
BASE = os.path.join(WORK, "base.cnf")
LOG = open(os.path.join(WORK, "reproduce.log"), "a", buffering=1)
log = lambda m: LOG.write(time.strftime("%H:%M:%SZ ", time.gmtime()) + m + "\n")

records = {}
for f in sorted(glob.glob(os.path.join(RES, "C2P*", "*", "out.jsonl"))):
    src = "/".join(f.split("/")[-3:-1])
    for l in open(f):
        if l.strip():
            r = json.loads(l)
            if r.get("certified"):
                records.setdefault(r["unit"], []).append((src, r))


def used_gb():
    out = subprocess.run(["vm_stat"], capture_output=True, text=True).stdout
    g = lambda k: int(re.search(rf"{k}:\s+(\d+)", out).group(1))
    return (g("Pages active") + g("Pages wired down") + g("Pages occupied by compressor")) * 16384 / 1e9


def guard():
    while (u := used_gb()) > GUARD_GB:
        log(f"guard: {u:.1f} GB in use, waiting"); time.sleep(30)


def cube(case, unit):
    for l in open(os.path.join(RES, "C2P", "cubes", f"{case}_cubes.txt")):
        if l.split(" ", 1)[0] == unit:
            return [int(x) for x in l.split()[1:]]
    raise KeyError(unit)


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
for arg in sys.argv[5:]:
    unit, _, want = arg.partition("@")
    src, ref = next((s, r) for s, r in records[unit] if not want or s == want)
    case = ref["case"]
    F, P, O = (os.path.join(WORK, f"rep_{unit}.{x}") for x in ("cnf", "lrat", "out"))
    cnfsha = build(F, [[l] for l in cube(case, unit)])
    rec = {"unit": unit, "case": case, "record_source": src, "cnf_sha256": cnfsha,
           "cnf_matches_record": cnfsha == ref["cnf_sha256"]}
    if rec["cnf_matches_record"]:
        guard(); log(f"=== {unit} ({src}) solve")
        ec, out, wall = run([os.path.join(BIN, "cadical"), "-t", str(CAP), "--lrat", "--binary=false", F, P], O)
        st = first(out, r"^s [A-Z]+"); st = st[2:] if st else ("UNKNOWN" if ec == 0 else f"ERROR exit {ec}")
        ts = re.search(r"total process time since initialization:\s+([\d.]+)", out)
        rec.update(status=st, solve_s=float(ts.group(1)) if ts else None, record_solve_s=ref["solve_s"])
        if st == "UNSATISFIABLE":
            rec["proof_bytes"] = os.path.getsize(P); rec["proof_sha256"] = sha_file(P)
            rec["proof_reproduces_record"] = (rec["proof_sha256"] == ref["proof_sha256"]
                                              and rec["proof_bytes"] == ref["proof_bytes"])
            _, o, t = run([os.path.join(BIN, "lrat-check"), F, P])
            rec["lrat_check"] = first(o, r"^.*(VERIFIED|FAIL|rror).*$"); rec["lrat_check_s"] = t
            guard()
            _, o, t = run([os.path.join(BIN, "cake_lpr"), "--CML_HEAP_SIZE=8000", "--CML_STACK_SIZE=4000", F, P])
            rec["cake_lpr"] = first(o, r"^.*(s VERIFIED|exhausted|rror|FAIL).*$") or "no verdict line"; rec["cake_s"] = t
            rec["certified"] = rec["lrat_check"] == "c VERIFIED" and rec["cake_lpr"] == "s VERIFIED UNSAT"
            if ARCH:
                os.makedirs(ARCH, exist_ok=True); A = os.path.join(ARCH, f"{unit}.lrat.zst")
                run(["zstd", "-q", "-f", "-T4", "-9", P, "-o", A])
                rec["archive"] = os.path.basename(A); rec["archive_bytes"] = os.path.getsize(A)
                rec["archive_sha256"] = sha_file(A)
                d = subprocess.run(f"zstd -dc '{A}' | shasum -a 256", shell=True, capture_output=True, text=True)
                rec["roundtrip"] = "verified" if d.stdout.split()[0] == rec["proof_sha256"] else "MISMATCH"
            if not rec["certified"] or rec.get("roundtrip") == "MISMATCH":
                rec["proof_kept"] = P; P = P + ".kept"; os.replace(rec["proof_kept"], P); rec["proof_kept"] = P
    for x in (F, os.path.join(WORK, f"rep_{unit}.lrat"), O):
        if os.path.exists(x): os.remove(x)
    rec["finished"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    with open(OUT, "a") as f: f.write(json.dumps(rec) + "\n")
    log(f"=== {unit} end {rec.get('status')} reproduces {rec.get('proof_reproduces_record')} certified {rec.get('certified')}")
log("done")
