#!/usr/bin/env python3
"""Replay retained ES(7) certificates from manifest.json with every input bound to its recorded SHA-256.

For each selected manifest entry, one at a time:
  1. hash the proof archive and require the recorded SHA-256 (and size, where recorded);
  2. decompress it (one pass: archive hash, decompression and proof hash together) and require the recorded proof
     SHA-256 and size;
  3. produce the CNF by the entry's first method (archived .zst, generator run, or base + clauses exactly as the
     original lane built it), hashing while writing, and require the recorded CNF SHA-256; the other methods are run
     as cross-checks and must give the same hash;
  4. run lrat-check, then cake_lpr (heap ladder from the manifest, stack 4000 MiB), on exactly those two files;
  5. re-hash both files after the checkers and require the same hashes; delete them;
  6. append one JSON line: observed and recorded hashes, command lines, exit codes, verdict lines, timings, max RSS
     (wait4), and the SHA-256 of each checker's full output (kept in LOGS).
Modes: hash (steps 1-3 by streaming, no checker), lrat (no cake_lpr), full (everything).
A header line records the tool hashes (required to equal the manifest's), host, python, zstd and this file's hash.
Controls (lrat/full): tiny good/bad LRAT proofs, a forged hintless empty clause, and the c3hex-15 proof with one hint
removed; every checker must accept exactly the good ones, else the run stops.

usage: replay.py --manifest M --res RESULTS --aroot ARCHIVE_ROOT --bin BIN --work WORK --out OUT.jsonl
                 [--mode hash|lrat|full] [--select ID_OR_GROUP,...] [--exclude ...] [--all] [--max-proof-bytes N]
                 [--central-base FILE] [--mem-cap-gb 44] [--guard-gb 34] [--max-heap-mb N] [--rss-kill-mb N]
                 [--claims DIR] [--resume] [--keep] [--no-controls] [--no-cross-check] [--nocache]
Selection: default = entries with "default": true; --all = every entry; --select = ids or group names (prefix
matching with a trailing *). Memory: before each cake_lpr attempt the run waits until active+wired+compressed memory
plus the heap footprint (heap MiB * 1.048576 GB + 0.4 GB) is at most --mem-cap-gb; before every other heavy step it
waits until memory in use is at most --guard-gb.
"""
import argparse, fcntl, hashlib, json, os, platform, re, shutil, signal, socket, subprocess, sys, threading, time

MIB_GB = 1048576 / 1e9
ap = argparse.ArgumentParser()
ap.add_argument("--manifest", required=True)
ap.add_argument("--res", required=True, help="repository results directory (cloud/es7-2026-10-19/results)")
ap.add_argument("--aroot", required=True, help="proof-archive root")
ap.add_argument("--bin", required=True, help="directory with lrat-check and cake_lpr")
ap.add_argument("--work", required=True)
ap.add_argument("--out", required=True)
ap.add_argument("--logs", default=None, help="directory for full checker outputs (default WORK/../logs)")
ap.add_argument("--mode", choices=["hash", "lrat", "full"], default="full")
ap.add_argument("--select", default="")
ap.add_argument("--exclude", default="")
ap.add_argument("--all", action="store_true")
ap.add_argument("--max-proof-bytes", type=float, default=0)
ap.add_argument("--central-base", default=None, help="use this base CNF (hash required) instead of regenerating it")
ap.add_argument("--mem-cap-gb", type=float, default=44.0)
ap.add_argument("--guard-gb", type=float, default=34.0, help="memory guard before generators and checkers")
ap.add_argument("--light-guard-gb", type=float, default=0,
                help="memory guard before pure streaming steps (archive/proof/CNF hashing, ~20 MB RSS); 0 = --guard-gb")
ap.add_argument("--guard-max-wait-s", type=float, default=0, help="0 = wait forever")
ap.add_argument("--max-heap-mb", type=int, default=0, help="skip cake_lpr heaps above this (0 = no limit)")
ap.add_argument("--rss-kill-mb", type=float, default=0, help="kill a child above this RSS (0 = no limit)")
ap.add_argument("--claims", default=None)
ap.add_argument("--resume", action="store_true")
ap.add_argument("--keep", action="store_true")
ap.add_argument("--no-controls", action="store_true")
ap.add_argument("--no-cross-check", action="store_true")
ap.add_argument("--nocache", action="store_true", help="read archives with F_NOCACHE (spares the page cache)")
ap.add_argument("--allow-tool-mismatch", action="store_true")
A = ap.parse_args()

for d in (A.work, os.path.dirname(os.path.abspath(A.out)), A.logs or os.path.join(A.work, "..", "logs")):
    rd = os.path.realpath(d)
    for ro in (A.aroot, A.res):
        if rd == os.path.realpath(ro) or rd.startswith(os.path.realpath(ro) + os.sep):
            sys.exit(f"refusing to write inside read-only tree {ro}")
LOGS = os.path.abspath(A.logs or os.path.join(A.work, "..", "logs"))
os.makedirs(A.work, exist_ok=True); os.makedirs(LOGS, exist_ok=True)
MAN = json.load(open(A.manifest))
RUNLOG = open(os.path.join(A.work, "replay.log"), "a", buffering=1)
now = lambda: time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def log(m):
    RUNLOG.write(f"{now()} [{os.getpid()}] {m}\n")


def emit(rec):
    with open(A.out, "a") as f:
        f.write(json.dumps(rec, sort_keys=False) + "\n")


# ------------------------------------------------------------------------------------------------ memory and disk
def used_gb():
    out = subprocess.run(["vm_stat"], capture_output=True, text=True).stdout
    g = lambda k: int(re.search(rf"{k}:\s+(\d+)", out).group(1))
    page = int(re.search(r"page size of (\d+) bytes", out).group(1))
    return (g("Pages active") + g("Pages wired down") + g("Pages occupied by compressor")) * page / 1e9


def wait_mem(need_gb=0.0, label="", light=False):
    """wait while used + need exceeds the cap (need > 0) or used exceeds the guard (need == 0); returns waited s"""
    t0, last = time.time(), 0
    guard = (A.light_guard_gb or A.guard_gb) if light else A.guard_gb
    while True:
        u = used_gb()
        if (need_gb > 0 and u + need_gb <= A.mem_cap_gb) or (need_gb == 0 and u <= guard):
            return round(time.time() - t0, 1)
        if A.guard_max_wait_s and time.time() - t0 > A.guard_max_wait_s:
            raise TimeoutError(f"memory guard: {u:.1f} GB in use, need {need_gb:.1f} GB ({label})")
        if time.time() - last > 300:
            log(f"guard {label}: {u:.1f} GB in use, need {need_gb:.1f} GB, cap {A.mem_cap_gb} / guard {guard}")
            last = time.time()
        time.sleep(20)


def free_gb(path):
    return shutil.disk_usage(path).free / 1e9


# ------------------------------------------------------------------------------------------------ hashing and I/O
def open_read(path):
    fd = os.open(path, os.O_RDONLY)
    if A.nocache:
        fcntl.fcntl(fd, fcntl.F_NOCACHE, 1)
    return os.fdopen(fd, "rb", buffering=0)


def sha_file(path):
    h, n, t0 = hashlib.sha256(), 0, time.time()
    with open_read(path) as f:
        while (b := f.read(1 << 22)):
            h.update(b); n += len(b)
    return {"sha256": h.hexdigest(), "bytes": n, "s": round(time.time() - t0, 1)}


def stream_zstd(src, dst=None):
    """one pass over a .zst archive: its sha256/bytes and the decompressed sha256/bytes; writes dst if given"""
    t0 = time.time()
    p = subprocess.Popen(["zstd", "-q", "-d", "-c"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    ha, hd, na, err = hashlib.sha256(), hashlib.sha256(), [0], []

    def feed():
        try:
            with open_read(src) as f:
                while (b := f.read(1 << 22)):
                    ha.update(b); na[0] += len(b); p.stdin.write(b)
        except BaseException as ex:
            err.append(repr(ex))
        finally:
            try:
                p.stdin.close()
            except Exception:
                pass

    th = threading.Thread(target=feed, daemon=True); th.start()
    nd, g = 0, (open(dst, "wb") if dst else None)
    try:
        while (b := p.stdout.read(1 << 22)):
            hd.update(b); nd += len(b)
            if g:
                g.write(b)
    finally:
        if g:
            g.close()
    th.join(); rc = p.wait()
    if rc != 0 or err:
        raise RuntimeError(f"zstd exit {rc} {err}")
    return {"archive_sha256": ha.hexdigest(), "archive_bytes": na[0], "sha256": hd.hexdigest(), "bytes": nd,
            "s": round(time.time() - t0, 1)}


class Sink:
    """hash (and optionally write) a byte stream"""
    def __init__(self, dst=None):
        self.h, self.n, self.g = hashlib.sha256(), 0, (open(dst, "wb") if dst else None)

    def write(self, b):
        self.h.update(b); self.n += len(b)
        if self.g:
            self.g.write(b)

    def close(self):
        if self.g:
            self.g.close()
        return {"sha256": self.h.hexdigest(), "bytes": self.n}


def build_from_base(base, clauses, sink):
    """lane.py build(): lines before 'p cnf' copied, header clause count raised by len(clauses), rest of the base
    copied verbatim, then one line 'lits 0' per extra clause"""
    with open(base, "rb") as f:
        while True:
            line = f.readline()
            if not line:
                raise ValueError("base has no header")
            if line.startswith(b"p cnf"):
                _, _, nv, nc = line.split()
                sink.write(f"p cnf {int(nv)} {int(nc) + len(clauses)}\n".encode()); break
            sink.write(line)
        while (b := f.read(1 << 22)):
            sink.write(b)
    sink.write("".join(" ".join(map(str, c)) + " 0\n" for c in clauses).encode())


def build_hull_cover(base, cubes, sink):
    """hullcubes.py cover.cnf: 'p cnf NV NC+len(cubes)', the base lines after the header that are not empty, a final
    newline, then the negation of each cube (file order)"""
    with open(base, "rb") as f:
        for line in f:
            if line.startswith(b"p cnf"):
                _, _, nv, nc = line.split()
                sink.write(f"p cnf {nv.decode()} {int(nc) + len(cubes)}\n".encode()); break
        else:
            raise ValueError("base has no header")
        buf = []
        for line in f:
            if line in (b"\n", b""):
                continue
            if not line.endswith(b"\n"):
                line += b"\n"
            buf.append(line)
            if len(buf) >= 200000:
                sink.write(b"".join(buf)); buf = []
        sink.write(b"".join(buf))
    sink.write("".join(" ".join(str(-x) for x in lits) + " 0\n" for lits in cubes).encode())


# ------------------------------------------------------------------------------------------------ child processes
def run_child(cmd, logpath, cwd=None, rss_kill_bytes=0):
    """run cmd with stdout+stderr to logpath; returns exit, wall s, max RSS (wait4) and whether it was killed"""
    t0 = time.time()
    with open(logpath, "wb") as lf:
        p = subprocess.Popen(cmd, stdout=lf, stderr=subprocess.STDOUT, cwd=cwd)
        stop, killed = threading.Event(), []

        def watch():
            while not stop.wait(0.5):
                o = subprocess.run(["ps", "-o", "rss=", "-p", str(p.pid)], capture_output=True, text=True).stdout.strip()
                if not o:
                    return
                if int(o) * 1024 > rss_kill_bytes and not stop.is_set():
                    killed.append(int(o) * 1024)
                    try:
                        os.kill(p.pid, signal.SIGKILL)
                    except ProcessLookupError:
                        pass
                    return

        th = None
        if rss_kill_bytes:
            th = threading.Thread(target=watch, daemon=True); th.start()
        _, status, ru = os.wait4(p.pid, 0)
        stop.set()
        p.returncode = os.waitstatus_to_exitcode(status)
    if th:
        th.join()
    return {"exit": p.returncode, "s": round(time.time() - t0, 1), "max_rss_bytes": ru.ru_maxrss,
            "killed_rss_bytes": killed[0] if killed else None}


def first_line(text, pat):
    m = re.search(pat, text, re.M)
    return m.group(0).strip() if m else None


def run_checker(name, cmd, logname):
    lp = os.path.join(LOGS, logname)
    kill = int(A.rss_kill_mb * 1e6) if (A.rss_kill_mb and name == "lrat-check") else 0  # never limit cake_lpr
    r = run_child(cmd, lp, rss_kill_bytes=kill)
    text = open(lp, errors="replace").read()
    r.update(cmd=cmd, log=lp, log_sha256=hashlib.sha256(open(lp, "rb").read()).hexdigest())
    if name == "lrat-check":
        r["verdict"] = first_line(text, r"^.*(VERIFIED|FAIL|rror).*$")
        r["parsed_line"] = first_line(text, r"^c parsed a formula with.*$")
        r["added_line"] = first_line(text, r"^c Added clauses.*$")
        r["ok"] = (r["exit"] == 0 and re.search(r"^c VERIFIED$", text, re.M) is not None
                   and "FAIL" not in text and not r["killed_rss_bytes"])
    else:
        r["verdict"] = first_line(text, r"^.*(s VERIFIED|exhausted|rror|FAIL).*$") or "no verdict line"
        r["ok"] = r["exit"] == 0 and re.search(r"^s VERIFIED UNSAT$", text, re.M) is not None and not r["killed_rss_bytes"]
        r["exhausted"] = "exhausted" in text
    r["tail"] = text.splitlines()[-3:]
    return r


def lrat_cmd(cnf, proof):
    return [os.path.join(A.bin, "lrat-check"), cnf, proof]


def cake_cmd(cnf, proof, heap):
    return [os.path.join(A.bin, "cake_lpr"), f"--CML_HEAP_SIZE={heap}", f"--CML_STACK_SIZE={MAN['cake_lpr_stack_mb']}",
            cnf, proof]


# ------------------------------------------------------------------------------------------------ CNF methods
GEN_CACHE = {}


def run_generator(spec, keep_as=None):
    """copy the hash-checked generator files into a fresh directory and run them there; returns the output hash"""
    key = (spec["gen"], tuple(spec["argv"]))
    if key in GEN_CACHE and not keep_as:
        return dict(GEN_CACHE[key], cached=True)
    d = os.path.join(A.work, "gen_" + re.sub(r"[^A-Za-z0-9_.-]", "_", spec["out"]) + f"_{os.getpid()}")
    shutil.rmtree(d, ignore_errors=True); os.makedirs(d)
    files = [(spec["gen"], spec["gen_sha256"])] + [(w["file"], w["sha256"]) for w in spec.get("with", [])]
    for rel, want in files:
        data = open(os.path.join(A.res, rel), "rb").read()
        got = hashlib.sha256(data).hexdigest()
        if want and got != want:
            raise RuntimeError(f"generator {rel} sha256 {got} != recorded {want}")
        open(os.path.join(d, os.path.basename(rel)), "wb").write(data)
    cmd = [sys.executable, "-I", "-B", os.path.basename(spec["gen"])] + spec["argv"]
    wait_mem(0, "generator")
    r = run_child(cmd, os.path.join(d, "gen.log"), cwd=d,
                  rss_kill_bytes=int(A.rss_kill_mb * 1e6) if A.rss_kill_mb else 0)
    out = os.path.join(d, spec["out"])
    if r["exit"] != 0 or not os.path.exists(out):
        raise RuntimeError(f"generator failed: {r} {open(os.path.join(d, 'gen.log'), errors='replace').read()[-500:]}")
    h = sha_file(out)
    res = {"cmd": cmd, "cwd": "fresh directory holding only the hash-checked generator files",
           "python": sys.version.split()[0], "exit": r["exit"],
           "gen_s": r["s"], "gen_max_rss_bytes": r["max_rss_bytes"], "sha256": h["sha256"], "bytes": h["bytes"]}
    if "--map" in spec["argv"]:
        mp = os.path.join(d, spec["argv"][spec["argv"].index("--map") + 1])
        if os.path.exists(mp):
            res["map_sha256"] = sha_file(mp)["sha256"]
    with open(out, "rb") as f:
        for line in f:
            if line.startswith(b"p cnf"):
                res["header"] = line.decode().strip(); break
    if keep_as:
        os.replace(out, keep_as)
    shutil.rmtree(d, ignore_errors=True)
    GEN_CACHE[key] = {k: v for k, v in res.items()}
    return res


BASES = {}


def central_base():
    if "central_base" in BASES:
        return BASES["central_base"]
    spec = MAN["inputs"]["central_base"]
    if A.central_base:
        h = sha_file(A.central_base)
        info = {"path": os.path.abspath(A.central_base), "how": "given", **h}
    else:
        path = os.path.join(A.work, f"central_base_{os.getpid()}.cnf")  # per process: lanes may share WORK
        g = run_generator(dict(spec, **{"with": []}), keep_as=path)
        info = {"path": path, "how": "regenerated", **g}
    info["recorded_sha256"] = spec["sha256"]
    info["match"] = info["sha256"] == spec["sha256"]
    if "map_sha256" in info:
        info["map_match"] = info["map_sha256"] == spec["map_sha256"]
    log(f"central base {info['how']}: {info['sha256']} match {info['match']}")
    if not info["match"]:
        raise RuntimeError(f"central base sha256 {info['sha256']} != recorded {spec['sha256']}")
    BASES["central_base"] = info
    return info


CUBEFILES = {}


def cube_lines(rel):
    if rel not in CUBEFILES:
        rows = []
        for l in open(os.path.join(A.res, rel)):
            if l.strip():
                n, *lits = l.split()
                rows.append((n, [int(x) for x in lits]))
        CUBEFILES[rel] = rows
    return CUBEFILES[rel]


def unit_clauses(c):
    """exactly lane.py extra_clauses() / hlane.sh"""
    if c["type"] == "cube":
        return [[l] for l in next(lits for n, lits in cube_lines(c["cubes"]) if n == c["unit"])]
    if c["type"] == "hull":
        return [[l] for l in next(lits for n, lits in cube_lines(c["cubes"]) if n == c["case"])]
    if c["type"] == "cover":
        hull = next(lits for n, lits in cube_lines(c["hull_cubes"]) if n == c["case"])
        hs = set(hull); cls = [[l] for l in hull]
        for n, lits in cube_lines(c["cubes"]):
            assert hs <= set(lits), n
            cls.append([-x for x in lits if x not in hs])
        return cls
    raise ValueError(c)


def produce_cnf(m, dst):
    """produce (dst given) or only hash (dst None) the CNF by method m"""
    k = m["kind"]
    if k == "archive":
        r = stream_zstd(os.path.join(A.aroot, m["archive"]), dst)
        r["archive_match"] = r["archive_sha256"] == m["archive_sha256"] and (
            m.get("archive_bytes") is None or r["archive_bytes"] == m["archive_bytes"])
        return r
    if k == "generator":
        return run_generator(m, keep_as=dst)
    if k == "central_unit":
        t0, b = time.time(), central_base()
        s = Sink(dst); build_from_base(b["path"], unit_clauses(m["clauses"]), s)
        return dict(s.close(), s=round(time.time() - t0, 1), base_sha256=b["sha256"])
    if k == "hull_cover":
        t0, b = time.time(), central_base()
        cubes = [lits for _, lits in cube_lines(m["cubes"])]
        s = Sink(dst); build_hull_cover(b["path"], cubes, s)
        return dict(s.close(), s=round(time.time() - t0, 1), base_sha256=b["sha256"], cubes=len(cubes))
    if k == "c4cuts":
        t0 = time.time(); bp = os.path.join(A.work, f"c4base_{os.getpid()}.cnf")
        g = run_generator(m["base"], keep_as=bp)
        try:
            if g["sha256"] != m["base_sha256"]:
                raise RuntimeError(f"c4 base sha256 {g['sha256']} != recorded {m['base_sha256']}")
            cj = os.path.join(A.res, m["cuts"])
            csha = sha_file(cj)["sha256"]
            if csha != m["cuts_sha256"]:
                raise RuntimeError(f"cuts.jsonl sha256 {csha} != recorded {m['cuts_sha256']}")
            cuts = [json.loads(l)["clause"] for l in open(cj) if l.strip()]
            s = Sink(dst); build_from_base(bp, cuts, s)
            return dict(s.close(), s=round(time.time() - t0, 1), base_sha256=g["sha256"], base_gen_s=g["gen_s"],
                        base_gen_max_rss_bytes=g["gen_max_rss_bytes"], cuts=len(cuts), cuts_sha256=csha)
        finally:
            if os.path.exists(bp):
                os.remove(bp)
    raise ValueError(k)


# ------------------------------------------------------------------------------------------------ tools and controls
def tool_header():
    tools = {}
    for name, want in MAN["tools"].items():
        p = os.path.join(A.bin, name)
        got = sha_file(p)["sha256"] if os.path.exists(p) else None
        tools[name] = {"path": p, "sha256": got, "recorded_sha256": want["sha256"], "match": got == want["sha256"]}
    return tools


def controls(c3entry):
    """checkers must accept exactly the good proofs"""
    d = os.path.join(A.work, f"controls_{os.getpid()}"); shutil.rmtree(d, ignore_errors=True); os.makedirs(d)
    w = lambda n, s: (open(os.path.join(d, n), "w").write(s), os.path.join(d, n))[1]
    t = w("t.cnf", "p cnf 2 4\n1 2 0\n-1 2 0\n1 -2 0\n-1 -2 0\n")
    cases = [("good", t, w("good.lrat", "5 2 0 1 2 0\n6 0 5 3 4 0\n"), True),
             ("bad_missing_hint", t, w("bad.lrat", "5 2 0 1 2 0\n6 0 5 3 0\n"), False),
             ("forged_hintless_empty_clause", w("sat.cnf", "p cnf 1 1\n1 0\n"), w("forged.lrat", "2 0 0\n"), False)]
    if c3entry:
        cnf, prf = os.path.join(d, "c3.cnf"), os.path.join(d, "c3.lrat")
        a = stream_zstd(os.path.join(A.aroot, c3entry["proof"]["archive"]), prf)
        c = produce_cnf(c3entry["cnf"]["methods"][0], cnf)
        if a["sha256"] == c3entry["proof"]["sha256"] and c["sha256"] == c3entry["cnf"]["sha256"]:
            lines = open(prf).read().splitlines(True)
            i = max(k for k, l in enumerate(lines) if l.split()[1:2] == ["0"])
            tk = lines[i].split()
            lines[i] = " ".join(tk[:-2] + ["0"]) + "\n"
            open(os.path.join(d, "c3mut.lrat"), "w").write("".join(lines[:i + 1]))
            cases += [("c3hex15_genuine", cnf, prf, True),
                      ("c3hex15_last_empty_clause_hint_dropped", cnf, os.path.join(d, "c3mut.lrat"), False)]
    out, ok = [], True
    for name, cnf, prf, expect in cases:
        r = {"control": name, "expect_accept": expect}
        lc = run_checker("lrat-check", lrat_cmd(cnf, prf), f"control_{name}.lrat-check.out")
        r["lrat_check"] = {k: lc[k] for k in ("exit", "verdict", "ok")}
        good = lc["ok"] == expect
        if A.mode == "full":
            ck = run_checker("cake_lpr", cake_cmd(cnf, prf, 2000), f"control_{name}.cake_lpr.out")
            r["cake_lpr"] = {k: ck[k] for k in ("exit", "verdict", "ok")}
            good = good and ck["ok"] == expect
        r["as_expected"] = good; ok = ok and good; out.append(r)
    shutil.rmtree(d, ignore_errors=True)
    return ok, out


# ------------------------------------------------------------------------------------------------ one entry
def process(e):
    rec = {"type": "entry", "id": e["id"], "group": e["group"], "mode": A.mode, "started": now(),
           "critical": e["critical"], "recorded": {k: v for k, v in e["recorded"].items() if not k.endswith("_log")}}
    P = os.path.join(A.work, re.sub(r"[^A-Za-z0-9_.-]", "_", e["id"]) + ".lrat")
    F = os.path.join(A.work, re.sub(r"[^A-Za-z0-9_.-]", "_", e["id"]) + ".cnf")
    fails = []
    try:
        rec["mem_wait_s"] = wait_mem(0, e["id"], light=(A.mode == "hash"))
        need_disk = (0 if A.mode == "hash" else (e["proof"]["bytes"] + (e["cnf"]["bytes"] or 7e8)) / 1e9 + 2)
        if need_disk and free_gb(A.work) < need_disk:
            raise RuntimeError(f"disk: {free_gb(A.work):.0f} GB free, need {need_disk:.0f} GB")
        # 1-2: proof archive and proof
        ap_ = os.path.join(A.aroot, e["proof"]["archive"])
        z = stream_zstd(ap_, None if A.mode == "hash" else P)
        rec["archive"] = {"path": ap_, "sha256": z["archive_sha256"], "bytes": z["archive_bytes"],
                          "recorded_sha256": e["proof"]["archive_sha256"], "recorded_bytes": e["proof"]["archive_bytes"]}
        rec["archive"]["match"] = (z["archive_sha256"] == e["proof"]["archive_sha256"]
                                   and (e["proof"]["archive_bytes"] is None or z["archive_bytes"] == e["proof"]["archive_bytes"]))
        rec["proof"] = {"path": None if A.mode == "hash" else P, "sha256": z["sha256"], "bytes": z["bytes"],
                        "recorded_sha256": e["proof"]["sha256"], "recorded_bytes": e["proof"]["bytes"], "s": z["s"]}
        rec["proof"]["match"] = z["sha256"] == e["proof"]["sha256"] and z["bytes"] == e["proof"]["bytes"]
        if not rec["archive"]["match"]:
            fails.append("archive hash")
        if not rec["proof"]["match"]:
            fails.append("proof hash")
        # 3: CNF (first method produces the file; the others are cross-checks)
        meths = e["cnf"]["methods"]
        c = produce_cnf(meths[0], None if A.mode == "hash" else F)
        rec["cnf"] = {"method": meths[0]["kind"], "path": None if A.mode == "hash" else F,
                      "recorded_sha256": e["cnf"]["sha256"], "recorded_bytes": e["cnf"]["bytes"], **c}
        rec["cnf"]["match"] = c["sha256"] == e["cnf"]["sha256"] and (
            e["cnf"]["bytes"] is None or c["bytes"] == e["cnf"]["bytes"]) and c.get("archive_match", True)
        if not rec["cnf"]["match"]:
            fails.append("cnf hash")
        if not A.no_cross_check:
            rec["cnf_cross_checks"] = []
            for m in meths[1:]:
                x = produce_cnf(m, None)
                x.update(method=m["kind"], match=x["sha256"] == e["cnf"]["sha256"])
                rec["cnf_cross_checks"].append(x)
                if not x["match"]:
                    fails.append(f"cnf cross-check {m['kind']}")
        if A.mode == "hash" or fails:
            rec["status"] = "hashes match" if not fails else "FAILED: " + ", ".join(fails)
            rec["certified"] = False
            return rec
        # 4: checkers on exactly F and P
        sid = re.sub(r"[^A-Za-z0-9_.-]", "_", e["id"])
        rec["mem_wait_s"] += wait_mem(0, e["id"] + " lrat-check")
        rec["lrat_check"] = run_checker("lrat-check", lrat_cmd(F, P), f"{sid}.lrat-check.out")
        rl = e["recorded"].get("lrat_check_log") or {}
        if rl.get("added_line"):  # counts printed by the solve-time lrat-check run (archived log)
            rec["lrat_check"]["recorded_added_line"] = rl["added_line"]
            rec["lrat_check"]["added_line_matches_record"] = rec["lrat_check"]["added_line"] == rl["added_line"]
            rec["lrat_check"]["recorded_parsed_line"] = rl.get("parsed_line")
            rec["lrat_check"]["parsed_line_matches_record"] = rec["lrat_check"]["parsed_line"] == rl.get("parsed_line")
        if rec["lrat_check"]["killed_rss_bytes"]:
            fails.append(f"lrat-check NOT CHECKED (killed at RSS {rec['lrat_check']['killed_rss_bytes']} B, "
                         f"--rss-kill-mb {A.rss_kill_mb})")
        elif not rec["lrat_check"]["ok"]:
            fails.append("lrat-check")
        if A.mode == "full":
            atts = []
            for heap in e["heap_ladder_mb"]:
                if A.max_heap_mb and heap > A.max_heap_mb:
                    atts.append({"heap_mb": heap, "verdict": f"not run: heap above --max-heap-mb {A.max_heap_mb}"})
                    break
                waited = wait_mem(heap * MIB_GB + 0.4, f"{e['id']} cake_lpr heap {heap}")
                ck = run_checker("cake_lpr", cake_cmd(F, P, heap), f"{sid}.cake_lpr.heap{heap}.out")
                ck.update(heap_mb=heap, mem_wait_s=waited); atts.append(ck)
                if not ck.get("exhausted"):
                    break
            rec["cake_lpr"] = {"attempts": atts, "ok": bool(atts) and atts[-1].get("ok", False)}
            if not rec["cake_lpr"]["ok"]:
                fails.append("cake_lpr")
        # 5: files unchanged after the checkers
        pp, pc = sha_file(P), sha_file(F)
        rec["post_check"] = {"proof_sha256": pp["sha256"], "cnf_sha256": pc["sha256"],
                             "match": pp["sha256"] == z["sha256"] and pc["sha256"] == c["sha256"]}
        if not rec["post_check"]["match"]:
            fails.append("files changed during check")
        rec["certified"] = not fails and A.mode == "full"
        rec["status"] = ("FAILED: " + ", ".join(fails)) if fails else (
            "certified (lrat-check and cake_lpr)" if A.mode == "full" else "lrat-check verified (cake_lpr not run)")
        return rec
    except Exception as ex:
        rec["status"] = f"ERROR: {type(ex).__name__}: {ex}"; rec["certified"] = False
        return rec
    finally:
        if not A.keep:
            for x in (P, F):
                if os.path.exists(x):
                    os.remove(x)
        rec["finished"] = now()


# ------------------------------------------------------------------------------------------------ main
def selected(e):
    if any(e["id"] == s or e["group"] == s or (s.endswith("*") and e["id"].startswith(s[:-1]))
           for s in filter(None, A.exclude.split(","))):
        return False
    if A.select:
        ok = any(e["id"] == s or e["group"] == s or (s.endswith("*") and e["id"].startswith(s[:-1]))
                 for s in A.select.split(","))
    else:
        ok = A.all or e.get("default", False)
    if ok and A.max_proof_bytes and e["proof"]["bytes"] >= A.max_proof_bytes:
        ok = False
    return ok


todo = [e for e in MAN["entries"] if selected(e)]
done = set()
if A.resume and os.path.exists(A.out):
    for l in open(A.out):
        if l.strip():
            r = json.loads(l)
            if r.get("type") == "entry" and r.get("mode") == A.mode and (
                    r.get("certified") or r.get("status", "").startswith(("hashes match", "lrat-check verified"))):
                done.add(r["id"])
hdr = {"type": "header", "started": now(), "mode": A.mode, "host": socket.gethostname(),
       "platform": platform.platform(), "python": sys.version.split()[0], "python_path": sys.executable,
       "zstd": subprocess.run(["zstd", "--version"], capture_output=True, text=True).stdout.strip(),
       "replay_py_sha256": sha_file(os.path.abspath(__file__))["sha256"],
       "manifest": os.path.abspath(A.manifest), "manifest_sha256": sha_file(A.manifest)["sha256"],
       "manifest_commit": MAN.get("commit"), "argv": sys.argv, "selected": [e["id"] for e in todo],
       "skipped_resume": sorted(done & {e["id"] for e in todo})}
if A.mode != "hash":
    hdr["tools"] = tool_header()
    if not all(t["match"] for n, t in hdr["tools"].items() if n != "cadical") and not A.allow_tool_mismatch:
        hdr["status"] = "ABORT: checker binary hash differs from the manifest"; emit(hdr); sys.exit(2)
    if not A.no_controls:
        c3 = next((e for e in MAN["entries"] if e["id"] == "c3hex-15"), None)
        ok, res = controls(c3)
        hdr["controls"] = res; hdr["controls_ok"] = ok
        if not ok:
            hdr["status"] = "ABORT: a checker control did not behave as expected"; emit(hdr); sys.exit(3)
emit(hdr)
log(f"start mode {A.mode}: {len(todo)} entries")
n_ok = 0
for e in todo:
    if e["id"] in done:
        continue
    if A.claims:
        os.makedirs(A.claims, exist_ok=True)
        try:
            os.mkdir(os.path.join(A.claims, re.sub(r"[^A-Za-z0-9_.-]", "_", e["id"])))
        except FileExistsError:
            continue
    log(f"=== {e['id']} start")
    r = process(e)
    emit(r)
    n_ok += r["status"].startswith(("certified", "hashes match", "lrat-check verified"))
    log(f"=== {e['id']} {r['status']}")
if BASES.get("central_base", {}).get("how") == "regenerated" and not A.keep:
    try:
        os.remove(BASES["central_base"]["path"])
    except OSError:
        pass
emit({"type": "footer", "finished": now(), "entries_run": len(todo) - len(done & {e['id'] for e in todo}),
      "ok": n_ok, "central_base": {k: v for k, v in BASES.get("central_base", {}).items()}})
log("done")
