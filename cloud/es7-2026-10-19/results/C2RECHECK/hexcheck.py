#!/usr/bin/env python3
"""Re-check the 120 hexagonal-hull cases of the central 34-point search on hash-checked files.

For each case of C2C34/logs/hex_cases.tsv, one lane at a time per process:
1. rebuild the case CNF exactly as C2C34/hlane.sh does (base with the header clause count raised by n, then the n
   unit clauses of the hull cube) and require its SHA-256 to equal the recorded cnf_sha256;
2. require the archive's SHA-256 to equal the recorded archive_sha256, decompress it, and require the proof's size
   and SHA-256 to equal the recorded ones;
3. run lrat-check and cake_lpr on exactly these two files (cake heap 8000 MB, 16000 MB again if exhausted);
4. delete the rebuilt CNF and the decompressed proof, and append one JSON line to OUT.
Lanes claim cases through mkdir in CLAIMS, so several processes can share one OUT. A memory guard waits while
active + wired + compressed memory exceeds GUARD_GB before each claim and before each cake_lpr.
usage: hexcheck.py BASE CUBES TSV ARCHIVE BIN WORK OUT [CASE ...]"""
import csv, hashlib, json, os, re, subprocess, sys, time

BASE, CUBES, TSV, ARCH, BIN, WORK, OUT = sys.argv[1:8]
ONLY = set(sys.argv[8:])
GUARD_GB = float(os.environ.get("HEX_GUARD_GB", 36))
CLAIMS = os.path.join(WORK, "claims")
os.makedirs(CLAIMS, exist_ok=True)
LOG = open(os.path.join(WORK, "hexcheck.log"), "a", buffering=1)
log = lambda m: LOG.write(time.strftime("%H:%M:%SZ ", time.gmtime()) + f"[{os.getpid()}] " + m + "\n")


def used_gb():
    out = subprocess.run(["vm_stat"], capture_output=True, text=True).stdout
    g = lambda k: int(re.search(rf"{k}:\s+(\d+)", out).group(1))
    return (g("Pages active") + g("Pages wired down") + g("Pages occupied by compressor")) * 16384 / 1e9


def guard():
    while (u := used_gb()) > GUARD_GB:
        log(f"guard: {u:.1f} GB in use, waiting"); time.sleep(30)


def build(path, lits):
    h = hashlib.sha256()
    with open(BASE, "rb") as f, open(path, "wb") as g:
        while True:
            line = f.readline()
            if not line:
                raise ValueError("no header")
            if line.startswith(b"p cnf"):
                _, _, nv, nc = line.split()
                line = f"p cnf {int(nv)} {int(nc) + len(lits)}\n".encode(); g.write(line); h.update(line); break
            g.write(line); h.update(line)
        while (b := f.read(1 << 24)):
            g.write(b); h.update(b)
        tail = "".join(f"{l} 0\n" for l in lits).encode(); g.write(tail); h.update(tail)
    return h.hexdigest()


def sha_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while (b := f.read(1 << 24)):
            h.update(b)
    return h.hexdigest()


def decompress(src, dst):
    h, n = hashlib.sha256(), 0
    p = subprocess.Popen(["zstd", "-q", "-d", "-c", src], stdout=subprocess.PIPE)
    with open(dst, "wb") as g:
        while (b := p.stdout.read(1 << 24)):
            g.write(b); h.update(b); n += len(b)
    if p.wait() != 0:
        raise RuntimeError(f"zstd exit {p.returncode}")
    return h.hexdigest(), n


def run(cmd):
    t0 = time.time(); p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return p.returncode, p.stdout.decode(errors="replace"), round(time.time() - t0, 1)


first = lambda s, pat: (m.group(0).strip() if (m := re.search(pat, s, re.M)) else None)
cubes = {}
for l in open(CUBES):
    if l.strip():
        name, *lits = l.split()
        cubes[name] = [int(x) for x in lits]
rows = list(csv.DictReader(open(TSV), delimiter="\t"))
for row in rows:
    case = row["case"]
    if ONLY and case not in ONLY:
        continue
    guard()
    try:
        os.mkdir(os.path.join(CLAIMS, case))
    except FileExistsError:
        continue
    F, P = os.path.join(WORK, f"{case}.cnf"), os.path.join(WORK, f"{case}.lrat")
    A = os.path.join(ARCH, f"{case}.lrat.zst")
    rec = {"case": case, "record_cnf_sha256": row["cnf_sha256"], "record_proof_sha256": row["proof_sha256"]}
    log(f"=== {case} start")
    rec["cnf_sha256"] = build(F, cubes[case])
    rec["cnf_matches_record"] = rec["cnf_sha256"] == row["cnf_sha256"]
    rec["archive_sha256"] = sha_file(A)
    rec["archive_matches_record"] = rec["archive_sha256"] == row["archive_sha256"]
    psha, pbytes = decompress(A, P)
    rec.update(proof_sha256=psha, proof_bytes=pbytes,
               proof_matches_record=(psha == row["proof_sha256"] and pbytes == int(row["proof_bytes"])))
    if rec["cnf_matches_record"] and rec["archive_matches_record"] and rec["proof_matches_record"]:
        _, o, t = run([os.path.join(BIN, "lrat-check"), F, P])
        rec["lrat_check"] = first(o, r"^.*(VERIFIED|FAIL|rror).*$"); rec["lrat_check_s"] = t
        for heap in (8000, 16000):
            guard()
            _, o, t = run([os.path.join(BIN, "cake_lpr"), f"--CML_HEAP_SIZE={heap}", "--CML_STACK_SIZE=4000", F, P])
            rec["cake_lpr"] = first(o, r"^.*(s VERIFIED|exhausted|rror|FAIL).*$") or "no verdict line"
            rec["cake_s"] = t; rec["cake_heap_mb"] = heap
            if "exhausted" not in rec["cake_lpr"]:
                break
        rec["certified"] = rec["lrat_check"] == "c VERIFIED" and rec["cake_lpr"] == "s VERIFIED UNSAT"
    else:
        rec["certified"] = False
    for x in (F, P):
        if os.path.exists(x):
            os.remove(x)
    rec["finished"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    with open(OUT, "a") as f:
        f.write(json.dumps(rec) + "\n")
    log(f"=== {case} end certified {rec['certified']} cake {rec.get('cake_lpr')} {rec.get('cake_s')} s")
log("done")
