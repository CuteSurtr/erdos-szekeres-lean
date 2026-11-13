#!/usr/bin/env python3
"""Consistent build of the geometric chain of the compact ES(8) <= 311 recheck (6 November 2026).

  build_chain311.py --closure-only     # write build/chain311/closure.json, compile nothing
  build_chain311.py --pin-library      # closure, then pin or verify the library (library.json), no compile
  build_chain311.py --dry-run [...]    # closure, library, and every check before the first compile; no compile
  build_chain311.py                    # closure, library, then build every module once into build/chain311/olean

The chain: the import closure, outside Mathlib and the ErdosSzekeres library, of
`BalancedBudgets` and `Residual32Bridge2650.Rows` (imported by assembly/Final311Compact.lean), plus
`BalancedCoverCutsV2`, which `CompactChecker.Bridge311Bal` imports and which is not in that closure.
Every module is compiled once, in one directory (build/chain311/olean), with one toolchain (the
repository's Lean 4.24.0 and its .lake Mathlib v4.24.0), from its pinned source:

* the source bytes come from the committed file or tarball that holds them (closure.json, "origin");
* their sha256 must equal the pin of the 11 October bridge record
  (omission-residual32-bridge2650-2026-10-11/kernel-check.json: "modules" for the modules it compiled
  fresh, "reused_objects" for those it linked after pinning them against global-cover-314-check.json),
  and every other record that pins the same file must agree (closure.json, "pins");
* the sha256 is checked when the source is written into build/chain311/src and again just before
  its compile.

Each compile is one `lean -j1` process in its own scope,
  systemd-run --user --scope --unit=chain311-<token> -p MemoryMax=<cap> -p MemorySwapMax=0
    -p CPUQuota=100% nice -n 5 ...
with cap 12G, or 24G for the modules listed in HEAVY. At most two compiles run at once and at most
one of them is heavy. A heavy compile starts only if MemAvailable >= cap + 8 GB and the latest
"start" line of the es311-full driver log is a chunk (not a Root or Final); otherwise it waits, and
once that driver has left its chunk phase, heavy modules not yet started are reported as blocked.
A light compile that is OOM-killed under 12G is moved to the heavy queue once; a heavy compile
that is OOM-killed is recorded and not retried, unless a later run is given --retry-oom (with a larger
--heavy-cap, a decision for the machine's owner); --ignore-driver drops the wait for the driver's chunk
phase when that driver is not running.

A module is ok when lean exits 0, the .olean was written, the log has no `error:` and no
`declaration uses 'sorry'`, and every `#print axioms` line in it lists only propext,
Classical.choice and Quot.sound. One row per attempt goes to build/chain311/build.tsv (wall
time, peak RSS, cgroup memory.peak, OOM kills, .olean sha256 and whether it equals the .olean
sha256 recorded by the original check). Restart-safe: a module whose last row is ok, for the same
source sha256, and whose .olean still has the recorded sha256, is not rebuilt.

Review fixes (6 November 2026, later):
* Memory (GiB throughout, as systemd's "24G" and /proc/meminfo's kB / 2**20): before anything starts,
  a pending heavy module makes the run refuse when --heavy-cap + 8 exceeds MemTotal (it could never
  start) or MemAvailable (it could not start now). When nothing runs and nothing can start, a
  "waiting" line is printed every 5 minutes, and after --max-wait minutes (default 30) the run stops
  and reports those modules as blocked, instead of waiting silently. --ignore-driver is refused
  while the unit es311-full is active.
* The library (build/chain311/library.json): Lean's own list of the modules in the environment of a
  file that imports the chain's direct library imports (lake's LEAN_PATH only), each with the one
  root that provides it and its .olean sha256, plus the toolchain and lake-manifest sha256. Written
  once; when modules were already compiled, only if every one of those files is older than the
  first compile in build.tsv. Every later run (and assemble_final311.sh) re-verifies it and refuses
  on any difference, since the chain's .olean files would then be stale.
* Provenance: closure.json is rewritten only when its content changes (not its "written" and
  "script_sha256"), and every invocation appends a start and an end record (script sha256, argv,
  caps, closure content sha256, library digest) to build/chain311/runs.jsonl. A hand-corrected
  build.tsv row is described in build/chain311/row-notes.json, never silently.
* The verdict of a compile (the scope's Result, read before the scope is reset, then the log) is one
  function, collect(), tested on a real OOM kill in a small scope by test_build_chain311.py.
"""
import argparse
import datetime
import fcntl
import gzip
import hashlib
import json
import os
import re
import secrets
import signal
import subprocess
import sys
import tarfile
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent
EXP = REPO / "experiments"
OUT = HERE / "build" / "chain311"
SRC, OLEAN, LOGS = OUT / "src", OUT / "olean", OUT / "logs"
TSV, CLOSURE = OUT / "build.tsv", OUT / "closure.json"
LIBRARY, RUNS, LIBPROBE = OUT / "library.json", OUT / "runs.jsonl", OUT / "libprobe"
DRIVER_OUT = Path("/home/jay/research/data/es311-full-20261106/driver.out")
DRIVER_UNIT = "es311-full"
HEADROOM_GB = 8  # a heavy compile starts only with MemAvailable >= cap + HEADROOM_GB (GiB)
WAIT_NOTE_S = 300
ROOTS = ["BalancedBudgets", "Residual32Bridge2650.Rows"]
EXTRAS = ["BalancedCoverCutsV2"]  # imported by CompactChecker.Bridge311Bal, outside the closure of ROOTS
ALLOWED = {"propext", "Classical.choice", "Quot.sound"}
LIGHT_CAP, HEAVY_CAP = 12, 24  # GB
# Peak RSS of these exceeded 12 GB when last compiled (bridge record, arm64) or, for the two cut modules,
# BalancedCoverCutsV2 was OOM-killed under a hard 12G here and ResidualCoverCutsV2 is 2.4 times its size.
# Order = start order: short ones first, the two long cut modules last.
HEAVY = ["RankCoreFour", "RankCoreTwo", "SixthRelaxedTemplate", "RankCoreThree",
         "BalancedCoverCutsV2", "ResidualCoverCutsV2"]
COLUMNS = ["utc_start", "utc_end", "module", "cap_gb", "heavy", "verdict", "exit", "wall_s", "user_s",
           "max_rss_kb", "cg_peak_bytes", "cg_swap_peak_bytes", "oom_kill", "olean_bytes", "olean_sha256",
           "recorded_olean_sha256", "olean_match", "src_sha256", "axioms", "warnings",
           "mem_avail_gb_at_start", "driver_phase_at_start", "load1", "log"]

R2650 = EXP / "omission-residual32-bridge2650-2026-10-11/kernel-check.json"
R314 = EXP / "omission-global-assembly-2026-10-10/global-cover-314-check.json"
GA = EXP / "omission-global-assembly-2026-10-10"
RG = EXP / "omission-residual-geometry-2026-10-09"
CC = EXP / "omission-cover-certificates-2026-10-10"


def sha_bytes(b):
    return hashlib.sha256(b).hexdigest()


def sha_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for blk in iter(lambda: f.read(1 << 22), b""):
            h.update(blk)
    return h.hexdigest()


def rel(p):
    p = Path(p)
    return str(p.relative_to(REPO)) if p.is_relative_to(REPO) else str(p)


def utc():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def meminfo_gb(key):
    """/proc/meminfo field in GiB (kB / 2**20), the unit of systemd's MemoryMax=<n>G."""
    for line in open("/proc/meminfo"):
        if line.startswith(key + ":"):
            return int(line.split()[1]) / 2 ** 20
    return 0.0


def mem_available_gb():
    return meminfo_gb("MemAvailable")


def mpath(m):
    return Path(*m.split(".")).with_suffix(".olean")


def anon(s):
    return str(s).replace(str(REPO), "<repo>").replace(str(Path.home()), "<home>")


def unanon(s):
    return s.replace("<repo>", str(REPO)).replace("<home>", str(Path.home()))


def append_run(rec):
    with open(RUNS, "a") as f:
        f.write(json.dumps(rec) + "\n")


def unit_active(unit):
    return subprocess.run(["systemctl", "--user", "is-active", "--quiet", unit]).returncode == 0


def driver_phase():
    """Phase of the latest 'start' line of the es311-full driver log (chunk, root, final) or None."""
    try:
        text = DRIVER_OUT.read_text(errors="replace")
    except OSError:
        return None
    m = re.findall(r"^\S+ start (\w+) ", text, re.M)
    return m[-1] if m else None


def imports_of(text):
    """Module names of the header's import lines (Lean 4 allows only comments before and between them)."""
    names, i, n = [], 0, len(text)
    while i < n:
        if text.startswith("/-", i):
            depth, i = 1, i + 2
            while i < n and depth:
                if text.startswith("/-", i):
                    depth, i = depth + 1, i + 2
                elif text.startswith("-/", i):
                    depth, i = depth - 1, i + 2
                else:
                    i += 1
            continue
        if text.startswith("--", i):
            j = text.find("\n", i)
            i = n if j < 0 else j + 1
            continue
        if text[i] in " \t\r\n":
            i += 1
            continue
        m = re.compile(r"import\s+((?:[A-Za-z0-9_.]+[ \t]*)+)").match(text, i)
        if not m:
            break
        names += m.group(1).split()
        i = m.end()
    return names


# ---------------------------------------------------------------- origins and pins

def origin_of(mod, fresh):
    """Where the source bytes of `mod` are committed: (kind, path, member)."""
    if mod in fresh:
        return ("file", REPO / fresh[mod]["source"], None)
    if mod == "BalancedRows" or re.fullmatch(r"Geometry\d{5}", mod):
        return ("tar", GA / "balanced-rows-sources.tar.gz", mod + ".lean")
    if mod == "BalancedProof.Catalog":
        return ("tar", EXP / "omission-balanced-lean-2026-10-09/sources.tar.gz", "Catalog.lean")
    if mod == "Catalog":
        return ("gz", RG / "Catalog.lean.gz", None)
    if mod in ("ResidualCycleIndex", "ResidualGeometry") or re.fullmatch(r"ResidualGeometry\d{5}", mod):
        return ("tar", RG / "cycles-sources.tar.gz", mod + ".lean")
    if mod == "ResidualAllGeometry" or re.fullmatch(r"ResidualBlock\d{5}", mod):
        return ("tar", RG / "blocks-sources.tar.gz", mod + ".lean")
    if mod in ("ResidualCoverCutsV2", "BalancedCoverCutsV2"):
        return ("file", CC / (mod + ".lean"), None)
    return None


_tar_cache = {}


def read_origin(origin):
    kind, path, member = origin
    if kind == "file":
        return path.read_bytes()
    if kind == "gz":
        return gzip.decompress(path.read_bytes())
    if path not in _tar_cache:
        with tarfile.open(path, "r:gz") as t:
            _tar_cache[path] = {m.name.lstrip("./"): t.extractfile(m).read() for m in t.getmembers() if m.isfile()}
    return _tar_cache[path][member]


def secondary_pins():
    """{module: [(record, source sha256, olean sha256 or None)]} from the other records that pin a file."""
    out = {}

    def add(mod, record, src, olean=None):
        out.setdefault(mod, []).append((rel(record), src, olean))

    for rec in (GA / "balanced-rows-kernel-check.json", RG / "cycles-kernel-check.json",
                RG / "blocks-kernel-check.json", CC / "residual-v2-cuts-kernel-check.json",
                CC / "balanced-v2-cuts-kernel-check.json"):
        for mod, v in json.loads(rec.read_text())["modules"].items():
            add(mod, rec, v["source_sha256"], v.get("olean_sha256"))
    exp = json.loads((GA / "balanced-rows-export.json").read_text())
    for fn, h in exp["files"].items():
        add(fn[:-5], GA / "balanced-rows-export.json", h)
    cat = json.loads((RG / "catalog-validation.json").read_text())["catalog"]
    add("Catalog", RG / "catalog-validation.json", cat["source_sha256"], cat["olean_sha256"])
    bl = json.loads((EXP / "omission-balanced-lean-2026-10-09/export.json").read_text())
    if "Catalog.lean" in bl.get("files", {}):
        add("BalancedProof.Catalog", EXP / "omission-balanced-lean-2026-10-09/export.json", bl["files"]["Catalog.lean"])
    r314 = json.loads(R314.read_text())
    for k, h in r314["inputs"].items():
        for name in ("BalancedCoverCutsV2", "ResidualCoverCutsV2"):
            if k.endswith("/" + name + ".lean"):
                add(name, R314, h)
    lm = (HERE / "lean_make.sh").read_text()
    for mod, h in re.findall(r"\[([A-Za-z0-9_.]+)\]=\"[^|]*\|[^|]*\|([0-9a-f]{64})\"", lm):
        add(mod, HERE / "lean_make.sh", h)
    return out


def json_pins(obj, name, out):
    """Every (key, sha256) in a JSON tree whose key is `name` or ends with '/' + name."""
    if isinstance(obj, dict):
        for k, v in obj.items():
            if isinstance(v, str) and re.fullmatch(r"[0-9a-f]{64}", v) and (k == name or k.endswith("/" + name)):
                out.append(v)
            json_pins(v, name, out)
    elif isinstance(obj, list):
        for v in obj:
            json_pins(v, name, out)
    return out


def data_files(mod, org, text):
    """Files a module reads at compile time (include_str), with their pins from the bundle's records."""
    names = re.findall(r'include_str\s+"([^"]+)"', text)
    if not names:
        return []
    if org[0] != "file":
        sys.exit(f"{mod} reads files but comes from an archive")
    bundle = org[1].parent
    while bundle.parent != EXP:
        bundle = bundle.parent
    out = []
    for n in names:
        f = org[1].parent / n
        pins = []
        for rec in ("manifest.json", "kernel-check.json"):
            if (bundle / rec).exists():
                pins += [(rel(bundle / rec), h) for h in json_pins(json.loads((bundle / rec).read_text()), n, [])]
        got = sha_file(f)
        if not pins:
            sys.exit(f"{mod}: data file {f} is not pinned by any record of {bundle.name}")
        if any(h != got for _, h in pins):
            sys.exit(f"{mod}: data file {f} has sha256 {got}, pinned {sorted(set(h for _, h in pins))}")
        out.append({"name": n, "path": rel(f), "sha256": got, "bytes": f.stat().st_size,
                    "pins": sorted(set(r for r, _ in pins))})
    return out


def library_roots(lean_path):
    return [Path(p) for p in lean_path.split(":") if p]


def is_library(mod, roots):
    rp = Path(*mod.split(".")).with_suffix(".olean")
    return any((r / rp).is_file() for r in roots)


def compute_closure(lean_path):
    rec = json.loads(R2650.read_text())
    if not rec.get("complete"):
        sys.exit("the bridge record is not complete")
    if sha_file(R314) != rec["reuse_pin_record_sha256"]:
        sys.exit("global-cover-314-check.json differs from the copy the bridge record pinned against")
    fresh, reused = rec["modules"], rec["reused_objects"]
    sec = secondary_pins()
    secs = {}  # recorded compile seconds (arm64, October) of the modules the bridge record reused
    for r in (GA / "balanced-rows-kernel-check.json", RG / "cycles-kernel-check.json",
              RG / "blocks-kernel-check.json", CC / "residual-v2-cuts-kernel-check.json",
              CC / "balanced-v2-cuts-kernel-check.json"):
        for mod, v in json.loads(r.read_text())["modules"].items():
            secs[mod] = v.get("seconds")
    secs["Catalog"] = json.loads((RG / "catalog-validation.json").read_text())["catalog"]["seconds"]
    roots = library_roots(lean_path)
    mods, lib_imports, todo = {}, {}, list(ROOTS) + list(EXTRAS)
    while todo:
        m = todo.pop()
        if m in mods:
            continue
        if is_library(m, roots):
            continue
        org = origin_of(m, fresh)
        if org is None:
            sys.exit(f"no committed source known for {m}")
        data = read_origin(org)
        got = sha_bytes(data)
        if m in fresh:
            pin, pin_olean, pin_rec = fresh[m]["source_sha256"], fresh[m].get("olean_sha256"), "modules"
        elif m in reused:
            pin, pin_olean, pin_rec = reused[m]["source_sha256"], reused[m]["olean_sha256"], "reused_objects"
        else:
            sys.exit(f"{m} is not pinned by {rel(R2650)}")
        if got != pin:
            sys.exit(f"{m}: committed source {org} has sha256 {got}, pinned {pin}")
        pins = [{"record": rel(R2650) + ":" + pin_rec, "source_sha256": pin, "olean_sha256": pin_olean}]
        for record, s, o in sec.get(m, []):
            if s != pin:
                sys.exit(f"{m}: {record} pins {s}, the bridge record {pin}")
            if o and pin_olean and o != pin_olean:
                sys.exit(f"{m}: {record} records .olean {o}, the bridge record {pin_olean}")
            pins.append({"record": record, "source_sha256": s, "olean_sha256": o})
        imps = imports_of(data.decode("utf-8"))
        dfiles = data_files(m, org, data.decode("utf-8"))
        chain = [i for i in imps if not is_library(i, roots)]
        lib_imports[m] = [i for i in imps if i not in chain]
        f = fresh.get(m, {})
        mods[m] = {"module": m, "origin": {"kind": org[0], "path": rel(org[1]), "member": org[2]},
                   "source_sha256": pin, "source_bytes": len(data), "pins": pins,
                   "imports": chain, "library_imports": lib_imports[m], "data_files": dfiles,
                   "recorded_olean_sha256": pin_olean,
                   "recorded_seconds": f.get("seconds") or secs.get(m),
                   "recorded_max_rss_bytes": f.get("max_rss_bytes"),
                   "heavy": m in HEAVY}
        todo += chain
    # library imports must resolve to exactly one LEAN_PATH root
    for m, libs in lib_imports.items():
        for i in libs:
            hits = [r for r in roots if (r / Path(*i.split(".")).with_suffix(".olean")).is_file()]
            if len(hits) != 1:
                sys.exit(f"library import {i} of {m} found in {len(hits)} LEAN_PATH roots")
    # topological order, deterministic
    order, done = [], set()
    pending = sorted(mods)
    while pending:
        ready = [m for m in pending if all(d in done for d in mods[m]["imports"])]
        if not ready:
            sys.exit(f"import cycle among {pending[:5]}")
        for m in ready:
            order.append(m)
            done.add(m)
        pending = [m for m in pending if m not in done]
    in_roots = set()
    stack = list(ROOTS)
    while stack:
        m = stack.pop()
        if m in in_roots or m not in mods:
            continue
        in_roots.add(m)
        stack += mods[m]["imports"]
    for m in mods:
        mods[m]["in_closure_of_roots"] = m in in_roots
    return mods, order


# ---------------------------------------------------------------- building

def scope_run(cmd, mem, unit, log, env):
    """Start cmd under /usr/bin/time -v in its own hard-capped scope; mem is a MemoryMax value ("24G")."""
    wrap = ('cg=/sys/fs/cgroup$(cut -d: -f3 /proc/self/cgroup); "$@"; rc=$?; '
            'echo "cgroup memory.peak: $(cat $cg/memory.peak 2>/dev/null)"; '
            'echo "cgroup memory.swap.peak: $(cat $cg/memory.swap.peak 2>/dev/null)"; '
            'echo "cgroup oom_kill: $(sed -n "s/^oom_kill //p" $cg/memory.events 2>/dev/null)"; exit $rc')
    full = ["systemd-run", "--user", "--scope", "--quiet", f"--unit={unit}", "-p", f"MemoryMax={mem}",
            "-p", "MemorySwapMax=0", "-p", "CPUQuota=100%", "nice", "-n", "5",
            "sh", "-c", wrap, "sh", "/usr/bin/time", "-v", *cmd]
    with open(log, "w") as lf:
        return subprocess.Popen(full, cwd=REPO, env=env, stdout=lf, stderr=subprocess.STDOUT,
                                start_new_session=True)


def get_lean_path():
    """lake's LEAN_PATH (Mathlib, its dependencies, the ErdosSzekeres library), through a capped scope."""
    r = subprocess.run(["systemd-run", "--user", "--scope", "--quiet", "-p", "MemoryMax=2G", "-p",
                        "MemorySwapMax=0", "nice", "-n", "5", "lake", "env", "printenv", "LEAN_PATH"],
                       cwd=REPO, capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit("lake env failed: " + r.stderr)
    return r.stdout.strip()


def scope_name(unit):
    """systemctl takes a bare name as NAME.service: the scope must be named with its suffix. (Before the
    review fixes the bare name was used, so `show -p Result` read a nonexistent service, always "success".)"""
    return unit if unit.endswith(".scope") else unit + ".scope"


def stop_scope(unit, timeout=120):
    u = scope_name(unit)
    subprocess.run(["systemctl", "--user", "kill", "--signal=SIGKILL", u], capture_output=True)
    t0 = time.time()
    while time.time() - t0 < timeout:
        st = subprocess.run(["systemctl", "--user", "is-active", u], capture_output=True, text=True).stdout.strip()
        if st in ("inactive", "failed", "unknown", ""):
            subprocess.run(["systemctl", "--user", "reset-failed", u], capture_output=True)
            return True
        time.sleep(0.5)
    return False


def parse_log(text):
    def tv(key):
        m = re.search(rf"{re.escape(key)}: (\S+)", text)
        return m.group(1) if m else None

    wall = tv("Elapsed (wall clock) time (h:mm:ss or m:ss)")
    wall_s = sum(float(p) * 60 ** i for i, p in enumerate(reversed(wall.split(":")))) if wall else float("nan")
    ax = re.findall(r"^'([^']+)' depends on axioms: \[([^\]]*)\]", text, re.M)
    ax += [(k, "") for k in re.findall(r"^'([^']+)' does not depend on any axioms", text, re.M)]
    cg = re.search(r"^cgroup memory\.peak: (\d+)", text, re.M)
    sw = re.search(r"^cgroup memory\.swap\.peak: (\d+)", text, re.M)
    oom = re.search(r"^cgroup oom_kill: (\d+)", text, re.M)
    return {"wall_s": wall_s, "user_s": float(tv("User time (seconds)") or "nan"),
            "max_rss_kb": int(tv("Maximum resident set size (kbytes)") or 0),
            "cg_peak": int(cg.group(1)) if cg else 0, "cg_swap_peak": int(sw.group(1)) if sw else 0,
            "oom_kill": int(oom.group(1)) if oom else 0, "axioms": ax,
            "warnings": len(re.findall(r"(^|\s)warning:", text, re.M)),
            "error": bool(re.search(r"(^|\s)error:|declaration uses 'sorry'", text, re.M)),
            "time_exit": int(tv("Exit status") or -1),
            "signalled": "Command terminated by signal" in text}  # time -v then says "Exit status: 0"


def collect(p, unit, log, tmp, cap_gb):
    """Verdict of a finished scope_run compile: (verdict, parsed log, scope Result).

    When the kernel OOM-kills the compile, systemd stops the whole scope (its OOMPolicy), so the
    wrapper may print nothing; the scope's Result ("oom-kill") is read before the scope is reset."""
    result = subprocess.run(["systemctl", "--user", "show", "-p", "Result", "--value", scope_name(unit)],
                            capture_output=True, text=True).stdout.strip()
    emptied = stop_scope(unit) if p.returncode is not None else False
    r = parse_log(Path(log).read_text(errors="replace"))
    bad_ax = [k for k, v in r["axioms"] if not {a.strip() for a in v.split(",") if a.strip()} <= ALLOWED]
    oom = (r["oom_kill"] > 0 or p.returncode in (137, -9) or r["time_exit"] == 137 or result == "oom-kill")
    if result == "oom-kill" and not r["oom_kill"]:
        r["oom_kill"] = 1
    ok = (p.returncode == 0 and emptied and Path(tmp).exists() and not r["error"] and not bad_ax
          and not r["signalled"])
    if ok:
        verdict = "ok"
    elif oom:
        verdict = "oom-heavy" if cap_gb > LIGHT_CAP else "oom-light"
    else:
        verdict = "fail"
    return verdict, r, result


# ---------------------------------------------------------------- the library

def library_closure(lean_path, lib_imports):
    """{module: root} for every module in the environment of a file importing `lib_imports`, as Lean lists
    it (header.moduleNames), under lake's LEAN_PATH only; each must be provided by exactly one root."""
    LIBPROBE.mkdir(parents=True, exist_ok=True)
    src, log = LIBPROBE / "LibProbe.lean", LIBPROBE / "LibProbe.log"
    src.write_text("".join(f"import {m}\n" for m in lib_imports)
                   + "open Lean in\n#eval show CoreM Unit from do\n"
                   + "  for m in (← getEnv).header.moduleNames do\n    IO.println s!\"module {m}\"\n")
    unit = f"chain311-{secrets.token_hex(5)}"
    env = dict(os.environ, LEAN_PATH=lean_path, LEAN_NUM_THREADS="1", OMP_NUM_THREADS="1")
    p = scope_run(["lean", "-j1", "-R", str(LIBPROBE), str(src)], f"{LIGHT_CAP}G", unit, log, env)
    p.wait()
    verdict, r, _ = collect(p, unit, log, src, LIGHT_CAP)
    names = re.findall(r"^module (\S+)$", log.read_text(errors="replace"), re.M)
    if verdict != "ok" or not set(lib_imports) <= set(names):
        sys.exit(f"the library probe failed ({verdict}; see {log})")
    roots = library_roots(lean_path)
    out = {}
    for m in names:
        hits = [rt for rt in roots if (rt / mpath(m)).is_file()]
        if len(hits) != 1:
            sys.exit(f"library module {m} is provided by {len(hits)} LEAN_PATH roots")
        out[m] = hits[0]
    return out


def pin_library(lean_path, lib_imports):
    """Write library.json once, or verify it. Returns its digest (sha256 over 'module<TAB>sha256' lines)."""
    roots = library_roots(lean_path)
    files = library_closure(lean_path, lib_imports)
    cur = {m: [roots.index(rt), sha_file(rt / mpath(m))] for m, rt in sorted(files.items())}
    digest = sha_bytes("".join(f"{m}\t{s}\n" for m, (_, s) in cur.items()).encode())
    tc, mf = sha_file(REPO / "lean-toolchain"), sha_file(REPO / "lake-manifest.json")
    if LIBRARY.exists():
        pin = json.loads(LIBRARY.read_text())
        probs = []
        if [unanon(r) for r in pin["roots"]] != [str(r) for r in roots]:
            probs.append("lake's LEAN_PATH roots differ")
        if pin["lean_toolchain_sha256"] != tc or pin["lake_manifest_sha256"] != mf:
            probs.append("lean-toolchain or lake-manifest.json differs")
        diff = sorted(m for m in set(pin["modules"]) | set(cur) if pin["modules"].get(m) != cur.get(m))
        if diff:
            probs.append(f"{len(diff)} library .olean files differ, e.g. {diff[:4]}")
        if probs:
            sys.exit(f"the library differs from {rel(LIBRARY)} ({'; '.join(probs)}): the chain's .olean files "
                     "may be stale; rebuild build/chain311 from scratch")
        print(json.dumps({"library": rel(LIBRARY), "verified": len(cur), "digest": digest}), flush=True)
        return digest
    first = None
    if TSV.exists():
        starts = [line.split("\t")[0] for line in TSV.read_text().splitlines()[1:] if line]
        first = min(starts) if starts else None
    newest = max((rt / mpath(m)).stat().st_mtime for m, rt in files.items())
    if first:
        t0 = datetime.datetime.strptime(first, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=datetime.timezone.utc).timestamp()
        newer = sorted(m for m, rt in files.items() if (rt / mpath(m)).stat().st_mtime >= t0)
        if newer:
            sys.exit(f"{len(newer)} library .olean files are newer than the first compile of the chain ({first}), "
                     f"e.g. {newer[:4]}: they cannot be pinned for the existing build; rebuild from scratch")
    head = {"written": utc(), "script_sha256": sha_file(Path(__file__)),
            "how": "header.moduleNames of a file importing closure.json's library_imports, lake's LEAN_PATH only; "
                   "modules: name -> [index into roots, .olean sha256]",
            "lean_toolchain_sha256": tc, "lake_manifest_sha256": mf,
            "roots": [anon(r) for r in roots], "library_imports": sorted(lib_imports),
            "first_chain_compile_utc": first,
            "newest_mtime_utc": datetime.datetime.fromtimestamp(newest, datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "all_older_than_first_compile": bool(first), "count": len(cur), "digest_sha256": digest}
    body = ",\n".join(f"  {json.dumps(m)}: {json.dumps(v)}" for m, v in cur.items())
    LIBRARY.write_text(json.dumps(head, indent=1)[:-2] + ',\n "modules": {\n' + body + "\n }\n}\n")
    print(json.dumps({"library": rel(LIBRARY), "pinned": len(cur), "digest": digest, "first_compile": first,
                      "newest_mtime": datetime.datetime.fromtimestamp(newest, datetime.timezone.utc).isoformat()}),
          flush=True)
    return digest


def take_lock():
    lock = open(OUT / ".build.lock", "w")
    try:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        sys.exit("another build_chain311.py is running")
    return lock


def heavy_start_problem(cap, pending):
    """Why a heavy compile under `cap` GiB could not start now (None if it could)."""
    if not pending:
        return None
    total, avail = meminfo_gb("MemTotal"), mem_available_gb()
    if cap + HEADROOM_GB > total:
        return (f"heavy cap {cap}G + {HEADROOM_GB} GiB exceeds MemTotal {total:.1f} GiB: {pending} could never "
                "start on this machine")
    if avail < cap + HEADROOM_GB:
        return (f"MemAvailable {avail:.1f} GiB < heavy cap {cap}G + {HEADROOM_GB} GiB: {pending} could not start "
                "now; free memory (other jobs) or choose another --heavy-cap")
    return None


def build(mods, order, lean_path, retry_failed=False, retry_oom=False, ignore_driver=False, dry_run=False,
          max_wait_min=30.0):
    OLEAN.mkdir(parents=True, exist_ok=True)
    LOGS.mkdir(parents=True, exist_ok=True)
    # sources, checked
    for m in order:
        p = SRC / Path(*m.split(".")).with_suffix(".lean")
        if not p.exists() or sha_file(p) != mods[m]["source_sha256"]:
            p.parent.mkdir(parents=True, exist_ok=True)
            data = read_origin((mods[m]["origin"]["kind"], REPO / mods[m]["origin"]["path"], mods[m]["origin"]["member"]))
            p.write_bytes(data)
        if sha_file(p) != mods[m]["source_sha256"]:
            sys.exit(f"{m}: written source does not have its pinned sha256")
        for d in mods[m]["data_files"]:  # include_str is relative to the source file
            q = p.parent / d["name"]
            if not q.exists() or sha_file(q) != d["sha256"]:
                q.write_bytes((REPO / d["path"]).read_bytes())
            if sha_file(q) != d["sha256"]:
                sys.exit(f"{m}: written data file {q} does not have its pinned sha256")
    # no module may be provided by two LEAN_PATH roots
    roots = library_roots(lean_path) + [OLEAN]
    seen, dup = {}, []
    for r in roots:
        if r.is_dir():
            for dp, _, fs in os.walk(r):
                for fn in fs:
                    if fn.endswith(".olean") and ".tmp" not in fn:
                        k = os.path.relpath(os.path.join(dp, fn), r)
                        if k in seen and seen[k] != r:
                            dup.append(k)
                        seen.setdefault(k, r)
    if dup:
        sys.exit(f"{len(dup)} modules provided by two LEAN_PATH roots, e.g. {dup[:3]}")
    if not TSV.exists():
        TSV.write_text("\t".join(COLUMNS) + "\n")
    last = {}
    for line in TSV.read_text().splitlines()[1:]:
        row = dict(zip(COLUMNS, line.split("\t")))
        last[row["module"]] = row

    def olean_of(m):
        return OLEAN / Path(*m.split(".")).with_suffix(".olean")

    def is_done(m):
        r = last.get(m)
        return bool(r and r["verdict"] == "ok" and r["src_sha256"] == mods[m]["source_sha256"]
                    and olean_of(m).exists() and sha_file(olean_of(m)) == r["olean_sha256"])

    done = {m for m in order if is_done(m)}
    failed = {m: last[m]["verdict"] for m in order if m not in done and m in last
              and last[m]["verdict"] in ("oom-heavy", "fail")}
    if retry_failed:  # e.g. after a setup error; an OOM-killed heavy compile is not retried by this flag
        failed = {m: v for m, v in failed.items() if v != "fail"}
    if retry_oom:  # a deliberate decision, with a larger --heavy-cap: OOM-killed heavy modules once more
        failed = {m: v for m, v in failed.items() if v != "oom-heavy"}
    heavy = [m for m in HEAVY if m in mods]
    promoted = [m for m in order if m in last and last[m]["verdict"] == "oom-light" and m not in done]
    heavy += [m for m in promoted if m not in heavy]
    # expected remaining path length (recorded seconds) for list scheduling
    users = {m: [u for u in order if m in mods[u]["imports"]] for m in order}
    tail = {}
    for m in reversed(order):
        tail[m] = (mods[m]["recorded_seconds"] or 30.0) + max((tail[u] for u in users[m]), default=0.0)
    anc_heavy = set()
    for h in heavy:
        st = list(mods[h]["imports"])
        while st:
            a = st.pop()
            if a not in anc_heavy:
                anc_heavy.add(a)
                st += mods[a]["imports"]
    env = dict(os.environ, LEAN_PATH=lean_path + ":" + str(OLEAN), LEAN_NUM_THREADS="1", OMP_NUM_THREADS="1")
    running = {}  # Popen -> (module, tmp, log, unit, row-start info)
    pending_heavy = [h for h in heavy if h not in done and h not in failed
                     and (retry_oom or h not in last or last[h]["verdict"] != "oom-heavy")]
    why = heavy_start_problem(HEAVY_CAP, pending_heavy)
    head = {"start": utc(), "modules": len(order), "done": len(done), "failed": failed, "heavy": heavy,
            "pending_heavy": pending_heavy, "heavy_cap_gb": HEAVY_CAP,
            "mem_total_gib": round(meminfo_gb("MemTotal"), 1), "mem_available_gib": round(mem_available_gb(), 1),
            "heavy_start_problem": why}
    print(json.dumps(head), flush=True)
    if why:
        sys.exit("refused: " + why)
    if dry_run:
        return {"dry_run": True, **head, "not_built": [m for m in order if m not in done]}

    def on_signal(signum, frame):
        for p, (m, tmp, log, unit, info) in list(running.items()):
            stop_scope(unit)
            try:
                os.killpg(p.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
            p.wait()
            if tmp.exists():
                tmp.unlink()
        print(f"{utc()} signal {signum}: stopped {len(running)} compiles; nothing recorded for them", flush=True)
        sys.exit(130)

    signal.signal(signal.SIGTERM, on_signal)
    signal.signal(signal.SIGINT, on_signal)

    def start(m, cap):
        token = secrets.token_hex(5)
        unit = f"chain311-{token}"
        tgt = olean_of(m)
        tgt.parent.mkdir(parents=True, exist_ok=True)
        tmp = tgt.with_name(f"{tgt.stem}.tmp{os.getpid()}-{token}.olean")
        src = SRC / Path(*m.split(".")).with_suffix(".lean")
        if sha_file(src) != mods[m]["source_sha256"] or any(
                sha_file(src.parent / d["name"]) != d["sha256"] for d in mods[m]["data_files"]):
            sys.exit(f"{m}: source or data file changed before its compile")
        log = LOGS / f"{m}.{int(time.time())}.log"
        info = {"utc_start": utc(), "cap": cap, "mem": f"{mem_available_gb():.1f}", "phase": driver_phase() or "none",
                "load1": open("/proc/loadavg").read().split()[0]}
        p = scope_run(["lean", "-j1", "-s", "32768", "-R", str(SRC), "-o", str(tmp), str(src)], f"{cap}G", unit, log,
                      env)
        running[p] = (m, tmp, log, unit, info)
        print(f"{info['utc_start']} start {m} cap={cap}G heavy={cap > LIGHT_CAP} memavail={info['mem']} "
              f"driver={info['phase']} running={len(running)}", flush=True)

    def finish(p):
        m, tmp, log, unit, info = running.pop(p)
        verdict, r, _ = collect(p, unit, log, tmp, info["cap"])
        ok = verdict == "ok"
        osha, obytes = "", 0
        if ok:
            osha, obytes = sha_file(tmp), tmp.stat().st_size
            os.replace(tmp, olean_of(m))
        elif tmp.exists():
            tmp.unlink()
        rec = mods[m]["recorded_olean_sha256"] or ""
        row = {"utc_start": info["utc_start"], "utc_end": utc(), "module": m, "cap_gb": info["cap"],
               "heavy": int(info["cap"] > LIGHT_CAP), "verdict": verdict, "exit": p.returncode,
               "wall_s": f"{r['wall_s']:.2f}", "user_s": f"{r['user_s']:.2f}", "max_rss_kb": r["max_rss_kb"],
               "cg_peak_bytes": r["cg_peak"], "cg_swap_peak_bytes": r["cg_swap_peak"], "oom_kill": r["oom_kill"],
               "olean_bytes": obytes, "olean_sha256": osha, "recorded_olean_sha256": rec,
               "olean_match": ("yes" if osha == rec else "no") if (osha and rec) else "",
               "src_sha256": mods[m]["source_sha256"],
               "axioms": ";".join(f"{k}=[{re.sub(r'\s+', ' ', v).strip()}]" for k, v in r["axioms"]) or "none",
               "warnings": r["warnings"],
               "mem_avail_gb_at_start": info["mem"], "driver_phase_at_start": info["phase"],
               "load1": info["load1"], "log": rel(log)}
        with open(TSV, "a") as fh:
            fh.write("\t".join(str(row[c]) for c in COLUMNS) + "\n")
        last[m] = {k: str(v) for k, v in row.items()}
        print(f"{row['utc_end']} {verdict} {m} wall={row['wall_s']} rss_kb={r['max_rss_kb']} "
              f"cg_peak={r['cg_peak'] / 2 ** 30:.2f}G match={row['olean_match']} running={len(running)}", flush=True)
        if verdict == "ok":
            done.add(m)
        elif verdict == "oom-light" and m not in heavy:
            heavy.append(m)  # once, under the heavy cap
        else:
            failed[m] = verdict

    blocked_heavy, blocked_wait, wait_since, last_note = set(), [], None, 0.0
    while True:
        for p in [p for p in running if p.poll() is not None]:
            finish(p)
        run_mods = {it[0] for it in running.values()}
        heavy_running = any(it[4]["cap"] > LIGHT_CAP for it in running.values())

        def ready(m):
            return (m not in done and m not in failed and m not in run_mods
                    and all(d in done for d in mods[m]["imports"]))

        phase = "chunk" if ignore_driver else driver_phase()
        if phase in ("root", "final"):
            blocked_heavy = {h for h in heavy if h not in done and h not in failed and h not in run_mods}
        while len(running) < 2:
            run_mods = {it[0] for it in running.values()}
            cand = None
            hq = [h for h in heavy if ready(h) and (retry_oom or h not in last or last[h]["verdict"] != "oom-heavy")]
            if hq and not heavy_running and phase == "chunk" and mem_available_gb() >= HEAVY_CAP + HEADROOM_GB:
                cand, cap = hq[0], HEAVY_CAP
            if cand is None:
                lq = sorted((m for m in order if ready(m) and m not in heavy),
                            key=lambda m: (m not in anc_heavy, -tail[m], m))
                if lq and mem_available_gb() >= LIGHT_CAP + 4:
                    cand, cap = lq[0], LIGHT_CAP
            if cand is None:
                break
            start(cand, cap)
            heavy_running = heavy_running or cap > LIGHT_CAP
        remaining = [m for m in order if m not in done and m not in failed]
        if running:
            wait_since = None
        else:
            if not remaining:
                break
            runnable = [m for m in remaining if all(d in done for d in mods[m]["imports"])]
            if all(m in blocked_heavy for m in runnable):
                break
            # Nothing runs and nothing could start (memory, or the driver's phase): say so, and stop after
            # max_wait_min instead of waiting silently.
            now = time.time()
            if wait_since is None:
                wait_since, last_note = now, 0.0
            if now - last_note >= WAIT_NOTE_S:
                print(f"{utc()} waiting: nothing runs; ready {runnable[:4]}; MemAvailable {mem_available_gb():.1f} GiB "
                      f"(heavy needs {HEAVY_CAP + HEADROOM_GB}, light {LIGHT_CAP + 4}); driver phase {phase}",
                      flush=True)
                last_note = now
            if now - wait_since >= 60 * max_wait_min:
                blocked_wait = sorted(set(runnable) - blocked_heavy)
                print(f"{utc()} gave up after {max_wait_min:g} min of waiting: {blocked_wait}", flush=True)
                break
        time.sleep(2)
    remaining = [m for m in order if m not in done]
    summary = {"finished": utc(), "modules": len(order), "ok": len(done), "failed": failed,
               "blocked_heavy": sorted(blocked_heavy - done), "blocked_wait": blocked_wait, "not_built": remaining}
    print(json.dumps(summary), flush=True)
    return summary


def closure_body(rec):
    """closure.json without the fields that say when and by which script it was written."""
    return json.loads(json.dumps({k: v for k, v in rec.items() if k not in ("written", "script", "script_sha256")},
                                 sort_keys=True))


def main():
    global HEAVY_CAP
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--closure-only", action="store_true")
    ap.add_argument("--pin-library", action="store_true", help="pin (first time) or verify library.json; no compile")
    ap.add_argument("--dry-run", action="store_true", help="every check before the first compile; no compile")
    ap.add_argument("--retry-failed", action="store_true", help="compile again modules whose last verdict is fail")
    ap.add_argument("--retry-oom", action="store_true",
                    help="compile again, once, heavy modules whose last verdict is oom-heavy (use with --heavy-cap)")
    ap.add_argument("--heavy-cap", type=int, default=HEAVY_CAP,
                    help="MemoryMax in GiB of a heavy compile (default 24); it starts only with MemAvailable >= cap + 8")
    ap.add_argument("--ignore-driver", action="store_true",
                    help="do not wait for the es311-full driver's chunk phase (refused while es311-full is active)")
    ap.add_argument("--max-wait", type=float, default=30.0,
                    help="minutes to wait while nothing runs and nothing can start, then stop (default 30)")
    args = ap.parse_args()
    if args.ignore_driver and unit_active(DRIVER_UNIT):
        sys.exit(f"--ignore-driver is refused while the unit {DRIVER_UNIT} is active")
    OUT.mkdir(parents=True, exist_ok=True)
    lock = take_lock()  # noqa: F841 (held until exit)
    script_sha = sha_file(Path(__file__))
    lean_path = get_lean_path()
    mods, order = compute_closure(lean_path)
    toolchain = (REPO / "lean-toolchain").read_text().strip()
    rec = {"written": utc(), "script": rel(Path(__file__)), "script_sha256": script_sha,
           "roots": ROOTS, "extras": {"BalancedCoverCutsV2": "imported by CompactChecker.Bridge311Bal; "
                                      "not in the closure of the roots"},
           "toolchain": toolchain, "lean_toolchain_sha256": sha_file(REPO / "lean-toolchain"),
           "lake_manifest_sha256": sha_file(REPO / "lake-manifest.json"),
           "pin_record": rel(R2650), "pin_record_sha256": sha_file(R2650),
           "pin_record_reuse_pins": rel(R314), "pin_record_reuse_pins_sha256": sha_file(R314),
           "counts": {"modules": len(order), "data_files": sum(len(m["data_files"]) for m in mods.values()), "in_closure_of_roots": sum(m["in_closure_of_roots"] for m in mods.values()),
                      "extras_only": sum(not m["in_closure_of_roots"] for m in mods.values()),
                      "source_bytes": sum(m["source_bytes"] for m in mods.values()),
                      "with_recorded_olean_sha256": sum(bool(m["recorded_olean_sha256"]) for m in mods.values())},
           "library_imports": sorted({i for m in mods.values() for i in m["library_imports"]}),
           "order": order, "modules": {m: mods[m] for m in order}}
    body = closure_body(rec)
    body_sha = sha_bytes(json.dumps(body, sort_keys=True).encode())
    old = json.loads(CLOSURE.read_text()) if CLOSURE.exists() else None
    if old is not None and closure_body(old) == body:
        state = f"unchanged (written {old['written']} by script {old['script_sha256'][:12]})"
    else:
        CLOSURE.write_text(json.dumps(rec, indent=1) + "\n")
        state = "written" if old is None else "rewritten: its content changed"
    print(json.dumps({"closure": rel(CLOSURE), "state": state, "content_sha256": body_sha, **rec["counts"]}),
          flush=True)
    mode = ("closure-only" if args.closure_only else "pin-library" if args.pin_library
            else "dry-run" if args.dry_run else "build")
    run = {"event": "start", "utc": utc(), "pid": os.getpid(), "mode": mode, "argv": sys.argv[1:],
           "script_sha256": script_sha, "closure": state, "closure_content_sha256": body_sha,
           "heavy_cap_gb": args.heavy_cap, "light_cap_gb": LIGHT_CAP}
    if args.closure_only:
        append_run({**run, "event": "closure-only"})
        return
    run["library_digest_sha256"] = pin_library(lean_path, rec["library_imports"])
    append_run(run)
    if args.pin_library:
        return
    HEAVY_CAP = args.heavy_cap
    try:
        s = build(mods, order, lean_path, args.retry_failed, args.retry_oom, args.ignore_driver, args.dry_run,
                  args.max_wait)
    except SystemExit as e:
        append_run({"event": "end", "utc": utc(), "pid": os.getpid(), "exit": str(e.code)})
        raise
    append_run({"event": "end", "utc": utc(), "pid": os.getpid(),
                **{k: s[k] for k in ("ok", "done", "failed", "blocked_heavy", "blocked_wait", "not_built", "dry_run",
                           "pending_heavy") if k in s}})
    sys.exit(0 if s.get("dry_run") or not s["not_built"] else 1)


if __name__ == "__main__":
    main()
