#!/usr/bin/env python3
"""Hash-bound re-solve of the threefold (C3, m = 11, k = 7) sigma-cube pieces that the cover cannot do without.

For every piece of LIST (one canonical piece name per line, e.g. 0s0-3s1_1s1-8s1__2s0-4s0-5s0), one lane at a time:
 1. find its certified record(s) in the 280 record files of results/C3FINAL/compose_files.txt (certified exactly as
    compose.py counts it).  A results/C3PLAN/scripts/sigma_cubes.py record stores the PARENT node in "node" and the
    fixed sigma bits in "cube"; the piece is parent + '__' + cube (sorted by residue);
 2. rebuild its CNF exactly as sigma_cubes.run() did: the base header with the clause count raised by u, the base
    body byte for byte, then u unit lines "lit 0": the layer units of the parent (C3-S/tools/hullcase.layer_clauses,
    the module sigma_cubes.py imported) followed by one sigma unit per cube bit in the record's own bit order;
    REQUIRE its SHA-256 (streamed while writing) to equal the record's cnf_sha256 and u to equal its "units";
 3. run CaDiCaL with the record's exact command line: -q -t CAP <record cadical_opts> --lrat --binary=false
    (sigma_cubes.py ran 'cadical -q -t 300 --sat --lrat --binary=false').  -t only arms a wall-clock alarm and
    does not change the search, so CAP (default 3600, env C3P_CAP) may exceed the record's 300 s; the proof's
    size (and SHA-256, where a record has one) is compared with the record;
 4. check the proof with lrat-check (verdict: a line 'c VERIFIED', no 'NOT VERIFIED', exit 0) and with cake_lpr
    (verdict: a line exactly 's VERIFIED UNSAT'; heap C3P_HEAP_MB = 6000, retried with C3P_HEAP_RETRY_MB = 12000
    if the heap is exhausted; at most C3P_CAKE_SLOTS = 2 cake_lpr processes at once across lanes);
 5. if both accept: zstd -9 the proof into ARCHIVE as <piece>.lrat.zst.part, decompress it again and require the
    stream's SHA-256 and size to equal the proof's, then rename it to <piece>.lrat.zst and append a line to
    ARCHIVE/MANIFEST.jsonl; delete the CNF and the proof.  A proof that fails a check or the round trip is kept
    in the lane's work directory (with its CNF) for inspection;
 6. append one JSON line for the piece to OUT and write STATE/done/<piece>.json.
Claims: a lane takes a piece by holding an exclusive flock on STATE/claims/<piece>.lock (released by the kernel
if the lane dies) and skips pieces that are done or locked, so any number of lanes can share one LIST and STATE.
Memory guard: before each claim and before each solver/checker process the lane waits while active + wired +
compressed memory (vm_stat) exceeds GUARD_GB (env, default 34) GB; it also waits while the work or archive file
system has less than C3P_MIN_FREE_GB (default 30) GB free.  Optional C3P_MAX_RSS_MB kills a solver/checker whose
RSS exceeds it (recorded as such).  'touch STATE/STOP' makes every lane exit before its next claim; a SAT answer
writes STATE/STOP_SAT and STATE/STOP (all lanes stop) and keeps the solver output (abstract model only).
Start-up checks (abort on failure): base SHA-256, checker sanity (both checkers reject a forged empty-clause step
and accept a valid proof), every listed piece has a certified record with consistent CNF hashes.
Build-only mode (--build-only): steps 1-2 for every listed piece and every certified record of it, hashing the
rebuilt bytes as a stream (no CNF is written, no claim, no solver); one JSON line per piece.
usage: python3 -I -B c3resolve.py --list LIST --state STATE [--lane NAME] [--archive DIR] [--out OUT.jsonl]
           [--results R] [--base BASE.cnf] [--bin DIR] [--only PIECE ...] [--limit K] [--retry-failed]
           [--build-only] [--status]"""
import argparse
import fcntl
import hashlib
import importlib.util
import json
import os
import re
import shutil
import signal
import socket
import subprocess
import sys
import time

sys.dont_write_bytecode = True
# Default paths (the run used machine-specific absolute paths here; the options --results/--base/--bin/--archive or
# the variables C3P_RESULTS/C3P_BASE/C3P_BIN/C3P_ARCHIVE override them).
DEF_RESULTS = os.environ.get("C3P_RESULTS", os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
DEF_BASE = os.environ.get("C3P_BASE", "base_m11k7.cnf")
DEF_BIN = os.environ.get("C3P_BIN", "bin")
DEF_ARCHIVE = os.environ.get("C3P_ARCHIVE", "es7-c3-indispensable-2026-11-01")
BASE_SHA = "bf0e502ee78599400d36e0fc402a8ce79b4c41443327b4e0186902fab0cdd6da"
M, K = 11, 7
GB = 1e9


def env_num(name, default, typ=float):
    v = os.environ.get(name)
    return typ(v) if v not in (None, "") else default


GUARD_GB = env_num("GUARD_GB", 34.0)
CAP = env_num("C3P_CAP", 3600, int)
HEAP_MB = env_num("C3P_HEAP_MB", 6000, int)
HEAP_RETRY_MB = env_num("C3P_HEAP_RETRY_MB", 12000, int)
STACK_MB = env_num("C3P_STACK_MB", 2000, int)
CAKE_SLOTS = env_num("C3P_CAKE_SLOTS", 2, int)
MIN_FREE_GB = env_num("C3P_MIN_FREE_GB", 30.0)
MAX_RSS_MB = env_num("C3P_MAX_RSS_MB", 0, int)  # 0 = no limit
ZSTD_THREADS = env_num("C3P_ZSTD_THREADS", 1, int)
ZLEVEL = env_num("C3P_ZSTD_LEVEL", 9, int)


# ------------------------------------------------------------------------------------------------ small helpers
def now():
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


_BUF = bytearray(1 << 23)  # one reusable 8 MB read buffer (avoids allocator growth from repeated large reads)


def chunks(f):
    """yield successive chunks of binary stream f as memoryviews of _BUF (each valid until the next one)."""
    mv = memoryview(_BUF)
    while (n := f.readinto(mv)):
        yield mv[:n]


def sha_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in chunks(f):
            h.update(b)
    return h.hexdigest()


def used_gb():
    out = subprocess.run(["vm_stat"], capture_output=True, text=True).stdout
    page = int(re.search(r"page size of (\d+) bytes", out).group(1))
    g = lambda k: int(re.search(rf"{k}:\s+(\d+)", out).group(1))
    return (g("Pages active") + g("Pages wired down") + g("Pages occupied by compressor")) * page / GB


class StopRequested(Exception):
    pass


class Lane:
    def __init__(self, state, name, archive):
        self.state, self.name, self.archive = state, name, archive
        self.logf = open(os.path.join(state, "runner.log"), "a", buffering=1)

    def log(self, msg):
        self.logf.write(f"{now()} [{self.name} {os.getpid()}] {msg}\n")

    def stop_requested(self):
        return any(os.path.exists(os.path.join(self.state, f)) for f in ("STOP", "STOP_SAT"))

    def guard(self, what):
        waited = 0
        while True:
            if waited and self.stop_requested():
                raise StopRequested(f"STOP while waiting before {what}")
            u = used_gb()
            free = min(shutil.disk_usage(self.state).free, shutil.disk_usage(self.archive).free) / GB if self.archive \
                else shutil.disk_usage(self.state).free / GB
            if u <= GUARD_GB and free >= MIN_FREE_GB:
                return waited
            if waited % 300 == 0:
                self.log(f"guard before {what}: {u:.1f} GB in use (limit {GUARD_GB}), {free:.0f} GB free disk "
                         f"(min {MIN_FREE_GB}); waiting")
            time.sleep(30)
            waited += 30


CHILD = []  # the running solver/checker, killed if the lane receives SIGTERM/SIGINT


def on_signal(signum, _frame):
    for p in CHILD:
        try:
            p.kill()
        except Exception:  # noqa: BLE001
            pass
    raise SystemExit(f"signal {signum}")


def run_proc(cmd, logpath, header, rss_limit_mb=0):
    """run cmd with stdout+stderr to logpath (after the header lines); return (dict with exit, wall s, cpu s, max RSS,
    the process's own output without the header).  Verdicts are parsed from the process output only."""
    with open(logpath, "w") as lf:
        lf.write(header + "\n")
        lf.flush()
        start = lf.tell()
        t0 = time.time()
        p = subprocess.Popen(cmd, stdout=lf, stderr=subprocess.STDOUT)
        CHILD.append(p)
        killed, last_poll = None, 0.0
        try:
            while True:
                pid, status, ru = os.wait4(p.pid, os.WNOHANG)
                if pid:
                    break
                if rss_limit_mb and time.time() - last_poll >= 2:
                    last_poll = time.time()
                    q = subprocess.run(["ps", "-o", "rss=", "-p", str(p.pid)], capture_output=True, text=True).stdout.strip()
                    if q and int(q) / 1024 > rss_limit_mb:
                        killed = f"RSS {int(q) // 1024} MB > limit {rss_limit_mb} MB"
                        p.kill()
                time.sleep(0.5)
        finally:
            CHILD.remove(p)
        p.returncode = os.waitstatus_to_exitcode(status)
    res = {"exit": p.returncode, "wall_s": round(time.time() - t0, 1), "cpu_s": round(ru.ru_utime + ru.ru_stime, 1),
           "max_rss_mb": round(ru.ru_maxrss / 2 ** 20)}  # macOS: ru_maxrss in bytes
    if killed:
        res["killed"] = killed
    with open(logpath, "rb") as lf:
        lf.seek(start)
        return res, lf.read().decode(errors="replace")


def lrat_verdict(out, ec):
    lines = out.splitlines()
    if "c VERIFIED" in lines and not any("NOT VERIFIED" in l for l in lines) and ec == 0:
        return "c VERIFIED"
    bad = [l for l in lines if "NOT VERIFIED" in l or "FAIL" in l or "rror" in l]
    return bad[-1].strip() if bad else f"no verdict (exit {ec})"


def cake_verdict(out):
    lines = [l.strip() for l in out.splitlines()]
    if "s VERIFIED UNSAT" in lines:
        return "s VERIFIED UNSAT"
    bad = [l for l in lines if "exhausted" in l or "fail" in l.lower() or "rror" in l]
    return bad[0] if bad else "no verdict line"


# ------------------------------------------------------------------------------------------------ repository code
def load_module(name, path, pyc_prefix):
    sys.pycache_prefix = pyc_prefix  # never read or write the repository's __pycache__
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class Repo:
    def __init__(self, rd, pyc_prefix):
        self.rd = rd
        self.files = [l.strip() for l in open(os.path.join(rd, "C3FINAL", "compose_files.txt")) if l.strip()]
        c3cnf = load_module("c3cnf_repo", os.path.join(rd, "C3a", "c3cnf.py"), pyc_prefix)
        self.hc_s = load_module("hullcase_c3s", os.path.join(rd, "C3-S", "tools", "hullcase.py"), pyc_prefix)
        self.hc_u = load_module("hullcase_c3u2", os.path.join(rd, "C3U2", "tools", "hullcase.py"), pyc_prefix)
        self.E = c3cnf.C3Enc(M, K)  # literal maps only (no clause is built)
        self.src_sha = {p: sha_file(os.path.join(rd, p)) for p in
                        ("C3a/c3cnf.py", "C3-S/tools/hullcase.py", "C3U2/tools/hullcase.py",
                         "C3PLAN/scripts/sigma_cubes.py", "C3FINAL/compose_files.txt")}

    @staticmethod
    def certified(r):  # exactly compose.py's test
        return bool(r.get("certified")) and r.get("lrat_check") == "c VERIFIED" and r.get("cake_lpr") == "s VERIFIED UNSAT"

    def canon(self, r):
        hc = self.hc_u
        if "cube" in r:
            lay, c0 = hc.parse_node(r["node"])
            if c0:
                raise ValueError(f"sigma_cubes record on a cube node {r['node']}")
            return hc.node_name(lay, sorted((int(x), int(v)) for x, v in r["cube"].items()))
        return hc.node_name(*hc.parse_node(r["node"]))

    def records(self, wanted):
        """{piece: [entry]} for the wanted pieces; entry = {file, line, rec, certified}."""
        out = {p: [] for p in wanted}
        for f in self.files:
            for i, l in enumerate(open(os.path.join(self.rd, f))):
                if not l.strip():
                    continue
                r = json.loads(l)
                if "node" not in r:
                    continue
                n = self.canon(r)
                if n in out:
                    out[n].append({"file": f, "line": i + 1, "rec": r, "certified": self.certified(r)})
        return out

    def units(self, r):
        """unit literals exactly as sigma_cubes.run(): parent layer units, then the cube bits in the record's order."""
        hc, E = self.hc_s, self.E
        if "cube" in r:
            us = [c[0] for c in hc.layer_clauses(M, hc.parse_layers(r["node"]), E.ccw, E.sig)]
            us += [E.sig(int(b)) if v else -E.sig(int(b)) for b, v in r["cube"].items()]
        else:  # plain close_node/close_tree record (not expected in this list): C3U2 node units
            us = self.hc_u.node_units(M, r["node"], E.ccw, E.sig)
        return us

    def units_compose_way(self, piece):
        return self.hc_u.node_units(M, piece, self.E.ccw, self.E.sig)


def build_cnf(base, units, path=None):
    """header with clause count raised by len(units), base body byte for byte, unit lines; streamed SHA-256."""
    h, n = hashlib.sha256(), 0
    g = open(path + ".part", "wb") if path else None
    try:
        with open(base, "rb") as f:
            hd = f.readline().split()
            if hd[:2] != [b"p", b"cnf"] or len(hd) != 4:
                raise ValueError("base header is not 'p cnf V C'")
            line = f"p cnf {int(hd[2])} {int(hd[3]) + len(units)}\n".encode()
            h.update(line); n += len(line)
            if g:
                g.write(line)
            for b in chunks(f):
                h.update(b); n += len(b)
                if g:
                    g.write(b)
        tail = "".join(f"{u} 0\n" for u in units).encode()
        h.update(tail); n += len(tail)
        if g:
            g.write(tail)
    finally:
        if g:
            g.close()
    if path:
        os.replace(path + ".part", path)
    return h.hexdigest(), n


# ------------------------------------------------------------------------------------------------ start-up checks
def sanity(bin_dir, d):
    """both checkers must reject a forged empty-clause step (the E2 test) and accept a valid proof."""
    os.makedirs(d, exist_ok=True)

    def w(name, text):
        path = os.path.join(d, name)
        with open(path, "w") as f:
            f.write(text)
        return path

    cnf, bad, good = w("e2.cnf", "p cnf 1 2\n1 0\n-1 0\n"), w("e2_forged.lrat", "3 0 0\n"), w("e2_good.lrat", "3 0 1 2 0\n")
    res = {}
    for tag, prf in (("forged", bad), ("good", good)):
        a = subprocess.run([os.path.join(bin_dir, "lrat-check"), cnf, prf], capture_output=True, text=True)
        b = subprocess.run([os.path.join(bin_dir, "cake_lpr"), "--CML_HEAP_SIZE=64", "--CML_STACK_SIZE=16", cnf, prf],
                           capture_output=True, text=True)
        res[tag] = {"lrat_check": lrat_verdict(a.stdout + a.stderr, a.returncode), "cake_lpr": cake_verdict(b.stdout + b.stderr)}
    ok = (res["forged"]["lrat_check"] != "c VERIFIED" and res["forged"]["cake_lpr"] != "s VERIFIED UNSAT"
          and res["good"]["lrat_check"] == "c VERIFIED" and res["good"]["cake_lpr"] == "s VERIFIED UNSAT")
    return ok, res


def tool_ids(bin_dir):
    ids = {t: sha_file(os.path.join(bin_dir, t)) for t in ("cadical", "lrat-check", "cake_lpr")}
    ids["cadical_build"] = subprocess.run([os.path.join(bin_dir, "cadical"), "--build"], capture_output=True,
                                          text=True).stdout.strip().splitlines()[:1]
    ids["zstd"] = subprocess.run(["zstd", "--version"], capture_output=True, text=True).stdout.strip()
    return ids


def pick_record(entries):
    """the certified record(s); all must carry the same cnf_sha256 (else the piece is refused)."""
    cert = [e for e in entries if e["certified"]]
    if not cert:
        return None, "no certified record"
    shas = {e["rec"].get("cnf_sha256") for e in cert}
    if len(shas) != 1 or None in shas:
        return None, f"certified records disagree on cnf_sha256: {sorted(map(str, shas))}"
    return cert[0], None


def rec_summary(e):
    r = e["rec"]
    keep = ("node", "cube", "units", "cnf_sha256", "proof_sha256", "proof_bytes", "cap", "cadical_opts", "status",
            "solve_s", "check_s", "lrat_check", "cake_lpr", "certified", "base_sha256")
    return dict({"file": e["file"], "line": e["line"]}, **{k: r[k] for k in keep if k in r})


# ------------------------------------------------------------------------------------------------ one piece
def append_locked(path, obj):
    with open(path, "a") as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        f.write(json.dumps(obj) + "\n")
        f.flush()
        os.fsync(f.fileno())
        fcntl.flock(f, fcntl.LOCK_UN)


def acquire_cake_slot(state, lane):
    d = os.path.join(state, "slots")
    os.makedirs(d, exist_ok=True)
    t0 = time.time()
    while True:
        for i in range(max(1, CAKE_SLOTS)):
            fd = os.open(os.path.join(d, f"cake.{i}.lock"), os.O_CREAT | os.O_RDWR, 0o644)
            try:
                fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
                return fd, round(time.time() - t0, 1)
            except BlockingIOError:
                os.close(fd)
        time.sleep(10)


def process(piece, entries, a, lane, repo, tools, ctx):
    rec = {"piece": piece, "lane": lane.name, "host": socket.gethostname(), "pid": os.getpid(), "started": now(),
           "list_sha256": ctx["list_sha256"], "list_index": ctx["index"][piece], "base_sha256": BASE_SHA,
           "tools": tools, "repo_sources_sha256": repo.src_sha}
    ref, why = pick_record(entries)
    rec["n_records"], rec["n_certified_records"] = len(entries), sum(e["certified"] for e in entries)
    rec["other_records"] = [rec_summary(e) for e in entries if e is not ref]
    if ref is None:
        rec.update(outcome="NO_RECORD", error=why)
        return rec
    r = ref["rec"]
    rec["record"] = rec_summary(ref)
    W = ctx["work"]
    L = os.path.join(a.state, "logs")
    os.makedirs(W, exist_ok=True)
    os.makedirs(L, exist_ok=True)
    F, P = os.path.join(W, piece + ".cnf"), os.path.join(W, piece + ".lrat")
    us = repo.units(r)
    rec["units"] = len(us)
    rec["units_match_record"] = (len(us) == r.get("units"))
    rec["units_equal_compose_order"] = (us == repo.units_compose_way(piece))
    lane.log(f"=== {piece} build")
    rec["cnf_sha256"], rec["cnf_bytes"] = build_cnf(a.base, us, F)
    rec["cnf_matches_record"] = rec["cnf_sha256"] == r.get("cnf_sha256")
    if not (rec["cnf_matches_record"] and rec["units_match_record"]):
        os.remove(F)
        rec["outcome"] = "CNF_MISMATCH"
        return rec
    opts = r.get("cadical_opts")
    if not isinstance(opts, list) or not all(isinstance(x, str) for x in opts):
        os.remove(F)
        rec.update(outcome="ERROR", error="record has no cadical_opts list")
        return rec
    argv = [os.path.join(a.bin, "cadical"), "-q", "-t", str(CAP)] + opts + ["--lrat", "--binary=false", F, P]
    rec["cadical_args"] = argv[1:-2]
    rec["record_cap"], rec["cap"] = r.get("cap"), CAP
    rec["guard_wait_s"] = lane.guard("cadical")
    rec["mem_used_gb_at_solve"] = round(used_gb(), 1)
    lane.log(f"=== {piece} solve")
    hdr = f"c3resolve: {' '.join(argv)}\nc3resolve: cnf_sha256 {rec['cnf_sha256']}"
    rec["logs"] = {"cadical": os.path.join(L, piece + ".cadical.log")}
    res, out = run_proc(argv, rec["logs"]["cadical"], hdr, MAX_RSS_MB)
    st = next((l[2:].strip() for l in out.splitlines() if l.startswith("s ")), None)
    rec["status"] = st or ("KILLED" if res.get("killed") else f"UNKNOWN (exit {res['exit']})")
    rec["cadical"] = res
    rec["solve_s"] = res["wall_s"]
    if rec["status"] == "SATISFIABLE":
        open(os.path.join(a.state, "STOP_SAT"), "a").write(f"{now()} {piece} {lane.name}\n")
        open(os.path.join(a.state, "STOP"), "a").write(f"{now()} SAT on {piece}\n")
        rec.update(outcome="SAT", note="SAT: abstract model only (not a point set); solver output kept in logs/; "
                                       "all lanes stopped (STATE/STOP_SAT)")
        os.remove(F)
        if os.path.exists(P):
            os.remove(P)
        return rec
    if rec["status"] != "UNSATISFIABLE":
        for x in (F, P):
            if os.path.exists(x):
                os.remove(x)
        rec["outcome"] = "UNKNOWN"
        return rec
    rec["proof_bytes"] = os.path.getsize(P)
    rec["proof_sha256"] = sha_file(P)
    rec["proof_bytes_match_record"] = rec["proof_bytes"] == r.get("proof_bytes") if "proof_bytes" in r else None
    rec["proof_sha256_match_record"] = rec["proof_sha256"] == r.get("proof_sha256") if r.get("proof_sha256") else None
    hdr = f"c3resolve: cnf_sha256 {rec['cnf_sha256']} proof_sha256 {rec['proof_sha256']}"
    rec["guard_wait_lrat_s"] = lane.guard("lrat-check")
    lane.log(f"=== {piece} lrat-check")
    rec["logs"]["lrat-check"] = os.path.join(L, piece + ".lrat-check.log")
    res, out = run_proc([os.path.join(a.bin, "lrat-check"), F, P], rec["logs"]["lrat-check"],
                        hdr + f"\nc3resolve: lrat-check {F} {P}", MAX_RSS_MB)
    rec["lrat_check"], rec["lrat_check_run"] = lrat_verdict(out, res["exit"]), res
    m = re.search(r"Added clauses = (\d+)\.\s+Deleted clauses = (\d+)", out)
    if m:
        rec["lrat_added"], rec["lrat_deleted"] = int(m.group(1)), int(m.group(2))
    rec["cake_runs"], rec["guard_wait_cake_s"] = [], 0
    heap, stack = HEAP_MB, STACK_MB
    for attempt in (1, 2):  # second attempt only if the first one reports an exhausted heap or stack
        rec["guard_wait_cake_s"] += lane.guard("cake_lpr")
        fd, slot_wait = acquire_cake_slot(a.state, lane)
        try:
            rec["guard_wait_cake_s"] += lane.guard("cake_lpr (slot held)")
            lane.log(f"=== {piece} cake_lpr heap {heap} stack {stack}")
            argv_c = [os.path.join(a.bin, "cake_lpr"), f"--CML_HEAP_SIZE={heap}", f"--CML_STACK_SIZE={stack}", F, P]
            rec["logs"][f"cake_lpr.{attempt}"] = os.path.join(L, f"{piece}.cake_lpr.{attempt}.log")
            res, out = run_proc(argv_c, rec["logs"][f"cake_lpr.{attempt}"],
                                hdr + "\nc3resolve: " + " ".join(argv_c), MAX_RSS_MB)
        finally:
            os.close(fd)
        v = cake_verdict(out)
        rec["cake_runs"].append(dict(res, heap_mb=heap, stack_mb=stack, verdict=v, slot_wait_s=slot_wait))
        rec["cake_lpr"], rec["cake_heap_mb"], rec["cake_s"] = v, heap, res["wall_s"]
        if "exhausted" not in v or res.get("killed"):
            break
        if "stack" in v.lower():
            stack = max(2 * stack, 4000)
        else:
            heap = HEAP_RETRY_MB
    rec["certified"] = rec["lrat_check"] == "c VERIFIED" and rec["cake_lpr"] == "s VERIFIED UNSAT"
    if not rec["certified"]:
        os.replace(F, F + ".kept")
        os.replace(P, P + ".kept")
        rec.update(outcome="CHECK_FAIL", kept=[F + ".kept", P + ".kept"])
        return rec
    # archive with a decompress-and-hash round trip
    A = os.path.join(a.archive, piece + ".lrat.zst")
    part = A + ".part"
    rec["guard_wait_zstd_s"] = lane.guard("zstd")
    lane.log(f"=== {piece} archive")
    t0 = time.time()
    z = subprocess.run(["zstd", "-q", f"-{ZLEVEL}", f"-T{ZSTD_THREADS}", "-f", P, "-o", part], capture_output=True, text=True)
    rec["zstd_s"] = round(time.time() - t0, 1)
    rt_ok = False
    if z.returncode == 0:
        t0 = time.time()
        h, n = hashlib.sha256(), 0
        d = subprocess.Popen(["zstd", "-q", "-d", "-c", part], stdout=subprocess.PIPE)
        for b in chunks(d.stdout):
            h.update(b); n += len(b)
        rt_ok = d.wait() == 0 and h.hexdigest() == rec["proof_sha256"] and n == rec["proof_bytes"]
        rec["roundtrip_s"] = round(time.time() - t0, 1)
        rec["roundtrip_sha256"], rec["roundtrip_bytes"] = h.hexdigest(), n
    else:
        rec["zstd_error"] = z.stderr[-300:]
    rec["roundtrip"] = "verified" if rt_ok else "MISMATCH"
    if not rt_ok:
        if os.path.exists(part):
            os.remove(part)
        os.replace(F, F + ".kept")
        os.replace(P, P + ".kept")
        rec.update(outcome="ROUNDTRIP_FAIL", kept=[F + ".kept", P + ".kept"])
        return rec
    if os.path.exists(A):
        rec["replaced_archive_sha256"] = sha_file(A)
    os.replace(part, A)
    rec["archive"], rec["archive_bytes"], rec["archive_sha256"] = A, os.path.getsize(A), sha_file(A)
    rec["archive_zstd"] = f"zstd -{ZLEVEL} -T{ZSTD_THREADS}"
    append_locked(os.path.join(a.archive, "MANIFEST.jsonl"), {
        "piece": piece, "archive": os.path.basename(A), "archive_bytes": rec["archive_bytes"],
        "archive_sha256": rec["archive_sha256"], "proof_bytes": rec["proof_bytes"], "proof_sha256": rec["proof_sha256"],
        "cnf_sha256": rec["cnf_sha256"], "cnf_bytes": rec["cnf_bytes"], "units": rec["units"], "base_sha256": BASE_SHA,
        "record_file": ref["file"], "record_line": ref["line"], "record_node": r["node"], "record_cube": r["cube"],
        "cadical_args": rec["cadical_args"], "lrat_check": rec["lrat_check"], "cake_lpr": rec["cake_lpr"],
        "tools": tools, "lane": lane.name, "host": rec["host"], "finished": now()})
    os.remove(F)
    os.remove(P)
    rec["outcome"] = "certified"
    return rec


ARCHIVE_README = """Threefold (C3, m = 11, k = 7) sigma-cube pieces that the C3FINAL cover cannot do without, re-solved with
hash binding (audit finding F2).  One file <piece>.lrat.zst per piece: the ASCII LRAT proof (CaDiCaL 3.0.1
c6073042, the record's options '-q --sat' plus '--lrat --binary=false'), zstd -9.  MANIFEST.jsonl has one line
per archived proof: archive and proof SHA-256/size, the CNF SHA-256 (equal to the campaign record's cnf_sha256),
the record it reproduces, both checker verdicts (lrat-check E2 'c VERIFIED', cake_lpr 's VERIFIED UNSAT') and the
SHA-256 of the solver and checker binaries.  The CNF is not stored: it is the base CNF (C3-S gen_case.py 11 7 none,
'p cnf 168399 4154921', sha256 bf0e502e...6cdd6da) with the clause count raised by u and u unit lines appended
(the parent node's layer units from C3-S/tools/hullcase.py, then the sigma bits of the piece), exactly as
results/C3PLAN/scripts/sigma_cubes.py built it.  Runner: c3resolve.py (results/C3PIECES/tools), which also
writes the per-piece JSON lines and raw checker logs.
"""


# ------------------------------------------------------------------------------------------------ main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--list", required=True)
    ap.add_argument("--state", required=True)
    ap.add_argument("--lane", default=f"{socket.gethostname().split('.')[0]}-{os.getpid()}")
    ap.add_argument("--archive", default=DEF_ARCHIVE)
    ap.add_argument("--out")
    ap.add_argument("--results", default=DEF_RESULTS)
    ap.add_argument("--base", default=DEF_BASE)
    ap.add_argument("--bin", default=DEF_BIN)
    ap.add_argument("--only", nargs="*")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--retry-failed", action="store_true")
    ap.add_argument("--build-only", action="store_true")
    ap.add_argument("--status", action="store_true")
    a = ap.parse_args()
    a.state = os.path.abspath(a.state)
    for d in ("claims", "done", "logs", "work"):
        os.makedirs(os.path.join(a.state, d), exist_ok=True)
    pieces = [l.strip() for l in open(a.list) if l.strip() and not l.startswith("#")]
    if len(set(pieces)) != len(pieces):
        sys.exit("duplicate pieces in LIST")
    list_sha = sha_file(a.list)
    if a.status:
        return status(a, pieces)
    lane = Lane(a.state, a.lane, None if a.build_only else a.archive)
    out = a.out or os.path.join(a.state, "buildcheck.jsonl" if a.build_only else "out.jsonl")
    lane.log(f"start {'build-only' if a.build_only else 'resolve'} list {a.list} ({len(pieces)} pieces, sha {list_sha[:16]}) "
             f"GUARD_GB {GUARD_GB} CAP {CAP} heap {HEAP_MB}/{HEAP_RETRY_MB} stack {STACK_MB} slots {CAKE_SLOTS} "
             f"max_rss {MAX_RSS_MB} archive {a.archive}")
    # start-up checks
    bs = sha_file(a.base)
    if bs != BASE_SHA:
        sys.exit(f"base {a.base} has sha256 {bs}, not {BASE_SHA}")
    repo = Repo(a.results, os.path.join(a.state, "pycache_prefix_unused"))
    recs = repo.records(set(pieces))
    problems = {p: pick_record(recs[p])[1] for p in pieces if pick_record(recs[p])[0] is None}
    if problems and not a.build_only:
        sys.exit(f"pieces without a usable certified record: {json.dumps(problems)[:2000]}")
    ctx = {"list_sha256": list_sha, "index": {p: i for i, p in enumerate(pieces)}}
    if a.build_only:
        n_ok = 0
        for p in pieces:
            if a.only and p not in a.only:
                continue
            t0 = time.time()
            row = {"piece": p, "list_index": ctx["index"][p], "list_sha256": list_sha, "base_sha256": BASE_SHA,
                   "n_records": len(recs[p]), "n_certified_records": sum(e["certified"] for e in recs[p]),
                   "records": []}
            ref, why = pick_record(recs[p])
            row["reference_ok"] = ref is not None
            if why:
                row["error"] = why
            for e in recs[p]:
                if not e["certified"]:
                    row["records"].append(dict(rec_summary(e), checked=False))
                    continue
                us = repo.units(e["rec"])
                sha, nb = build_cnf(a.base, us)  # hash only, nothing written
                row["records"].append(dict(rec_summary(e), checked=True, rebuilt_units=len(us), rebuilt_sha256=sha,
                                           rebuilt_bytes=nb, sha_match=sha == e["rec"].get("cnf_sha256"),
                                           units_match=len(us) == e["rec"].get("units"),
                                           units_equal_compose_order=us == repo.units_compose_way(p)))
            chk = [x for x in row["records"] if x["checked"]]
            row["all_certified_records_match"] = bool(chk) and all(x["sha_match"] and x["units_match"] for x in chk)
            row["s"] = round(time.time() - t0, 2)
            n_ok += row["all_certified_records_match"]
            append_locked(out, row)
        lane.log(f"build-only done: {n_ok} pieces with every certified record's CNF hash reproduced")
        print(json.dumps({"build_only": True, "pieces": len(pieces), "all_match": n_ok, "out": out}))
        return
    ok, san = sanity(a.bin, os.path.join(a.state, "sanity"))
    if not ok:
        sys.exit(f"checker sanity test failed: {san}")
    tools = tool_ids(a.bin)
    tools["sanity"] = san
    for sig in (signal.SIGTERM, signal.SIGINT):
        signal.signal(sig, on_signal)
    clean_dead_work(a.state, lane)
    ctx["work"] = os.path.join(a.state, "work", f"{lane.name}.{os.getpid()}")  # per process: never shared
    os.makedirs(ctx["work"], exist_ok=True)
    os.makedirs(a.archive, exist_ok=True)
    rd = os.path.join(a.archive, "README.txt")
    if not os.path.exists(rd):
        try:
            fd = os.open(rd, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o644)
            os.write(fd, ARCHIVE_README.encode())
            os.close(fd)
        except FileExistsError:
            pass
    done_n = claim_loop(a, pieces, recs, lane, repo, tools, ctx, out)
    try:
        os.rmdir(ctx["work"])  # only if empty (kept proofs stay)
    except OSError:
        pass
    lane.log(f"lane exits after {done_n} pieces")


def pending_ok(a, dm):
    """True if the piece with done marker dm still needs work (no marker, or a failed one under --retry-failed)."""
    if not os.path.exists(dm):
        return True
    return bool(a.retry_failed) and json.load(open(dm)).get("outcome") != "certified"


def claim_loop(a, pieces, recs, lane, repo, tools, ctx, out):
    """repeated passes over LIST: claim (flock) and process every piece that is pending and not locked by a live
    lane; each piece at most once per lane process.  A pass that claims nothing ends the lane, so a surviving lane
    also takes over pieces whose lane died (the kernel drops a dead lane's locks)."""
    done_n, attempted = 0, set()
    while True:
        progressed = False
        for p in pieces:
            if (a.only and p not in a.only) or p in attempted:
                continue
            if a.limit and done_n >= a.limit:
                return done_n
            if lane.stop_requested():
                lane.log("STOP or STOP_SAT file present: exiting")
                return done_n
            dm = os.path.join(a.state, "done", p + ".json")
            if not pending_ok(a, dm):
                continue
            try:
                lane.guard("claim")
            except StopRequested as ex:
                lane.log(f"{ex}: exiting")
                return done_n
            fd = os.open(os.path.join(a.state, "claims", p + ".lock"), os.O_CREAT | os.O_RDWR, 0o644)
            try:
                fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except BlockingIOError:
                os.close(fd)
                continue
            try:
                if not pending_ok(a, dm):
                    continue  # finished by another lane between the check and the lock
                if lane.stop_requested():
                    return done_n
                attempted.add(p)
                progressed = True
                os.ftruncate(fd, 0)
                os.write(fd, json.dumps({"lane": lane.name, "pid": os.getpid(), "host": socket.gethostname(),
                                         "claimed": now()}).encode())
                try:
                    rec = process(p, recs[p], a, lane, repo, tools, ctx)
                except StopRequested as ex:  # waiting in the guard when STOP appeared: leave the piece pending
                    for x in (".cnf", ".cnf.part", ".lrat"):
                        if os.path.exists(os.path.join(ctx["work"], p + x)):
                            os.remove(os.path.join(ctx["work"], p + x))
                    lane.log(f"=== {p} left pending: {ex}")
                    return done_n
                except Exception as ex:  # noqa: BLE001  (record and go on; the lock is released below)
                    rec = {"piece": p, "lane": lane.name, "outcome": "ERROR", "error": repr(ex)[:1000]}
                    for x in (".cnf", ".cnf.part", ".lrat"):
                        if os.path.exists(os.path.join(ctx["work"], p + x)):
                            os.remove(os.path.join(ctx["work"], p + x))
                rec["finished"] = now()
                append_locked(out, rec)
                tmp = dm + f".tmp{os.getpid()}"
                with open(tmp, "w") as f:
                    json.dump(rec, f)
                os.replace(tmp, dm)
                done_n += 1
                lane.log(f"=== {p} end {rec.get('outcome')} solve {rec.get('solve_s')} s proof_bytes_match "
                         f"{rec.get('proof_bytes_match_record')} lrat {rec.get('lrat_check')} cake {rec.get('cake_lpr')}")
                if rec.get("outcome") == "SAT":
                    return done_n
            finally:
                os.close(fd)
        if not progressed:
            return done_n


def clean_dead_work(state, lane):
    """remove CNF and proof files (never *.kept) left in STATE/work/<lane>.<pid>/ by lanes of this host that died."""
    wd = os.path.join(state, "work")
    for d in os.listdir(wd):
        pid = d.rsplit(".", 1)[-1]
        if not pid.isdigit() or int(pid) == os.getpid():
            continue
        try:
            os.kill(int(pid), 0)
            continue  # alive (or PID reused): leave it
        except ProcessLookupError:
            pass
        except PermissionError:
            continue
        full = os.path.join(wd, d)
        gone = [f for f in os.listdir(full) if f.endswith((".cnf", ".cnf.part", ".lrat"))]
        for f in gone:
            os.remove(os.path.join(full, f))
        try:
            os.rmdir(full)
        except OSError:
            pass
        if gone:
            lane.log(f"removed {len(gone)} leftover files of dead lane process {d}: {gone}")


def status(a, pieces):
    cnt, active = {}, []
    for p in pieces:
        dm = os.path.join(a.state, "done", p + ".json")
        o = json.load(open(dm)).get("outcome") if os.path.exists(dm) else None
        lk = os.path.join(a.state, "claims", p + ".lock")
        if os.path.exists(lk):
            fd = os.open(lk, os.O_RDONLY)
            try:
                fcntl.flock(fd, fcntl.LOCK_SH | fcntl.LOCK_NB)
                fcntl.flock(fd, fcntl.LOCK_UN)
            except BlockingIOError:
                active.append((p, open(lk).read()))
            finally:
                os.close(fd)
        cnt[o or "pending"] = cnt.get(o or "pending", 0) + 1
    print(json.dumps({"pieces": len(pieces), "by_outcome": cnt, "in_progress": active,
                      "stop": os.path.exists(os.path.join(a.state, "STOP")),
                      "stop_sat": os.path.exists(os.path.join(a.state, "STOP_SAT"))}, indent=1))


if __name__ == "__main__":
    main()
