#!/usr/bin/env python3
"""Driver for the compact Lean check of ES(8) <= 310 (written 6 November 2026; NOT run for real).
ES(8) <= 310 is NOT proved: the budget-64 campaign is still running and nothing of it has been compiled.

  drive_es310.py EXPORT_DIR --reuse build/es311/full:E311R [--jobs 2] [--nice 10] [--no-final]
                 [--only E310B.C000101,...] [--bench R] [--dry-run] [--memory 12G] [--root-memory 24G]
                 [--max-tctl 80] [--campaign-log FILE] [--campaign-dir DIR] [--start-gap 60]
                 [--mem-wait-max 1800] [--tsv FILE]

A copy of drive_es311.py (cited below as d311:<line>) with the changes of the ES(8) <= 310 design
(section C) and of its two critiques. EXPORT_DIR holds manifest-E310B.json (written by merge_es310.py
in the 311 schema) and src/E310B/*.lean. The driver compiles, in order:
  1. every chunk module of every manifest in EXPORT_DIR, longest predicted first (--jobs at a time);
  2. the Root of each complete manifest, once all its chunks are ok;
  3. E310.Final (written here from a fixed template, FINAL_TEMPLATE), once E310B.Root is ok, if the run
     is "full": the only manifest is E310B, complete, at export_root 0 and base_path [], budget 64,
     catalog Fcat62, and --reuse has verified the residual side. E310.Final imports E310B.Root and
     E311R.Root (never E311.Final, which would pull in E311B) and prints the axioms of
     E310.balanced_excludes_64 and E310.residual_excludes_32.
Compiles run exactly as in d311:15-35 (one `lean -j1` per transient scope es310-<export tag>-<token>,
MemoryMax=--memory or --root-memory, MemorySwapMax=0, CPUQuota=100%, nice --nice, /usr/bin/time -v,
temporary .olean renamed only on verdict ok, one TSV row per attempt in EXPORT_DIR/run.tsv with the 311
columns), with the same restart safety (d311:37-44).

Changes against drive_es311.py:
 1. Unit names. Every systemctl call names '<unit>.scope' (scope_unit). drive_es311.py passed the bare
    name (d311:152, 163, 165, 174, 478), which systemctl reads as '<unit>.service' (README.md:1231-1235),
    so its scope-emptiness check never saw the scope's cgroup.
 2. FINAL_TEMPLATE is E310.Final (design section D); the expected theorems are
    E310.balanced_excludes_64 and E310.residual_excludes_32; the scope tag is es310-.
 3. --reuse DIR:E311R. The residual side of the 311 run is reused, never compiled. Read-only checks of
    DIR/manifest-E311R.json and DIR/run.tsv: the manifest is complete at export_root 1, base_path
    [[0, 2]], budget 32, catalog Fcat2650; for each of its modules (126 chunks and E311R.Root) the last
    TSV row is "ok" with the right phase, the manifest's source sha256, the dependency stamp
    deps_stamp_of(phase, 'Fcat2650', current stamps), standard axioms for every expected theorem; the
    source file has that sha256 and passes shapes_es311.check_text; the .olean has the recorded sha256.
    Also the 13 CompactChecker / build/ext .olean files of the verified 311 assembly
    (logs/es311/final311-compact.json, chain.inputs) must still have their recorded sha256, since Lean
    does not check that the reused .olean files match the ones they were compiled against. A shared
    flock on DIR/.driver.lock (opened read-only) keeps drive_es311.py off DIR while this driver runs.
    Then EXPORT_DIR/reuse/E311R/*.olean are made (also in --dry-run) as file symlinks to
    DIR/olean/E311R/*.olean, and EXPORT_DIR/reuse (the parent) goes on LEAN_PATH. The reused .olean files are hashed again right
    before E310.Final starts and after it ends; a change fails it. Anything stale is refused. A
    manifest of the reused prefix inside EXPORT_DIR is refused.
 4. prepare() always runs lean_make.sh with LM_NO_BUILD=1 on Path, Fcat62, Fcat2650, Bridge311Bal and
    Bridge311Res (STAMPED, as assemble_final311.sh:104 and :483): a module that is not current is
    refused, never rebuilt. So the E311R stamp check has its Fcat2650 stamp, and E310.Final's stamp is
    over the same 5 names that the assembly recomputes.
 5. Memory gate: a chunk needs --reserve-gb + --job-gb of MemAvailable, a Root or Final needs
    --reserve-gb + --root-memory (d311:505 used a fixed 12).
 6. Each start hashes every .olean once: the done() results are kept (d311:370 and :379 called it twice).
 7. At every start the library pins of build/chain311/library.json are re-checked as in
    assemble_final311.sh:214-237 (toolchain and lake-manifest sha256, lake's LEAN_PATH roots, every
    pinned library .olean's sha256).
 8. Temperature and campaign gates: a new Lean job starts only if `sensors` reports Tctl < --max-tctl
    (default 80 C, at most 85; no reading counts as too hot), no PAUSE line newer than 10 min is among
    the last 50 lines of --campaign-log (the budget-64 campaign's log, read only), and at least
    --start-gap seconds have passed since the last start. Running jobs are never stopped by a gate.
 9. Options as in drive_es311.py: --no-final, --only, --bench, --dry-run, --jobs, --nice, --memory,
    --root-memory, --reserve-gb, --job-gb, --tsv. Defaults changed for the shared machine: --jobs 2,
    --nice 10. EXPORT_DIR may not lie in build/es311, build/CompactChecker, build/ext, build/chain311,
    the campaign directory or the reused export.

Fixes of 6 November 2026 (after the soundness and operations reviews; each has a test in test_driver_es310.sh):
10. A Root or E310.Final counts as done only if every module it imports was compiled before it started (the
    assembly's rule, assemble_final310.sh check-run: an import's row must end at most 2 s after the importer's
    row started) and is itself done. So a chunk recompiled after its Root (by --bench, a re-export or a later
    merge) makes the Root, and then E310.Final, run again (soundness review item 3).
11. WITNESS gate: WITNESS-ALERT.txt in --campaign-dir/campaign or any runs/*WITNESS* file refuses the start
    (exit 5) and, once seen during a run, starts nothing more (running compiles finish; exit 5; ops review 4).
12. Exit codes: 0 everything selected is done; 1 some module's last verdict is not ok; 3 work was left undone
    (STOP file, or --mem-wait-max: nothing ran and the memory gate blocked for that long; ops reviews 3a, 5);
    5 a WITNESS file; 130 SIGTERM/SIGINT. Precedence: 5, then 1, then 3.
13. Defaults for the shared machine: --start-gap 60 (ops review 6), --root-memory 24G (ops review 5: 12G was
    the old fallback); --mem-wait-max 1800.
"""
import argparse
import datetime
import fcntl
import hashlib
import json
import os
import re
import secrets
import signal
import socket
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import shapes_es311  # noqa: E402  (strict line shapes of the generated sources)

REPO = HERE.parent.parent
BUILD = HERE / "build"
CHAIN = BUILD / "chain311"
ROUTE_RECORD = HERE / "logs/es311/final311-compact.json"  # the verified 311 assembly (route "same")
CAMPAIGN_DIR = Path("/home/jay/research/data/es8-b64-pilot-20261105")
CAMPAIGN_LOG = CAMPAIGN_DIR / "campaign" / "campaign.log"
PROTECTED = [BUILD / "es311", BUILD / "CompactChecker", BUILD / "ext", BUILD / "chain311", CAMPAIGN_DIR]
ALLOWED = {"propext", "Classical.choice", "Quot.sound"}
OLD_COLUMNS = ["utc", "phase", "module", "leaves", "src_sha256", "deps_stamp", "verdict", "exit",
               "kernel_s", "elab_s", "wall_s", "user_s", "peak_rss_kb", "olean_bytes", "olean_sha256",
               "axioms", "expected", "load1", "host", "log"]
COLUMNS = OLD_COLUMNS + ["cg_peak_kb"]  # as d311:68-71
# Predicted wall seconds per leaf (d311:73), only to start the longest chunks first.
MS_PER_LEAF = {"balanced": 27.4, "residual": 14.4}
# Every lean_make.sh stamp the driver uses (assemble_final311.sh:104 recomputes E310.Final's over these).
STAMPED = ["Path", "Fcat62", "Fcat2650", "Bridge311Bal", "Bridge311Res"]
MAIN_PREFIX, REUSE_PREFIX = "E310B", "E311R"
# What E310.Final consumes from each side (Bridge311Bal.lean:216-217, Bridge311Res.lean:164-166).
SIDES = {
    "E310B": {"side": "balanced", "catalog": "CompactChecker.Fcat62", "budget": 64, "export_root": 0,
              "base_path": []},
    "E311R": {"side": "residual", "catalog": "CompactChecker.Fcat2650", "budget": 32, "export_root": 1,
              "base_path": [[0, 2]]},
}
FINAL_MODULE = "E310.Final"
FINAL_EXPECTED = ["E310.balanced_excludes_64", "E310.residual_excludes_32"]
SCOPE_TAG = "es310-"
PAUSE_WINDOW_S, PAUSE_TAIL_LINES = 600, 50

FINAL_TEMPLATE = """import E310B.Root
import E311R.Root
import CompactChecker.Bridge311Bal
import CompactChecker.Bridge311Res

/-!
ES(8) <= 310, compact check: the two arithmetic facts that `assembly/Final310Compact.lean` consumes.

* `balanced_excludes_64` is the body of `OmissionBalanced.ExcludesHoleBudget 64` (BalancedBudgets.lean).
* `residual_excludes_32` is the body of `OmissionResidual32Bridge2650.Excludes2650Zero 32`
  (Residual32Bridge2650/Rows.lean), from the reused residual side of the 311 run (E311R.Root).
-/

open scoped BigOperators

namespace E310

theorem balanced_excludes_64 :
    ¬ ∃ holes : Fin 252 → ℕ, (∀ i, holes i ≤ 1) ∧
      (∀ r, OmissionBalanced.demand r ≤ ∑ i ∈ OmissionBalanced.support r, holes i) ∧
      (∑ i, holes i) ≤ 64 :=
  CompactChecker.Bridge311Bal.balanced_of_root E310B.root

theorem residual_excludes_32 :
    ¬ ∃ holes : Fin 154 → ℕ, (∀ i, holes i ≤ 1) ∧ holes 0 = 0 ∧
      (∀ r, OmissionResidual32Bridge2650.demand2650 r ≤
        ∑ i ∈ OmissionResidual32Bridge2650.support2650 r, holes i) ∧
      (∑ i, holes i) ≤ 32 :=
  CompactChecker.Bridge311Res.residual_of_root E311R.root

#print axioms balanced_excludes_64
#print axioms residual_excludes_32

end E310
"""


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(1 << 22), b""):
            h.update(b)
    return h.hexdigest()


def mem_available_gb():
    for line in open("/proc/meminfo"):
        if line.startswith("MemAvailable:"):
            return int(line.split()[1]) / 2 ** 20
    return 0.0


def mem_gb(spec):
    """GiB of a MemoryMax value '<number><K|M|G|T>' (a hard cap is required: no 'infinity', no %)."""
    m = re.fullmatch(r"(\d+(?:\.\d+)?)([KMGT])", spec or "")
    if not m:
        raise ValueError(f"memory cap {spec!r} is not <number><K|M|G|T>")
    return float(m.group(1)) * {"K": 2 ** -20, "M": 2 ** -10, "G": 1, "T": 2 ** 10}[m.group(2)]


def utc():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def systemctl(*args):
    return subprocess.run(["systemctl", "--user", *args], capture_output=True, text=True)


def scope_unit(unit):
    """The full unit name: systemd-run --scope --unit=X makes X.scope, and a bare X means X.service."""
    return unit if unit.endswith(".scope") else unit + ".scope"


def pgroup_alive(pgid):
    if not pgid:
        return False
    try:
        os.killpg(pgid, 0)
        return True
    except (ProcessLookupError, PermissionError):
        return False


def kill_scope(unit, pgid=None, timeout=300):
    """As d311:148-177, with the '.scope' name: SIGKILL whatever is left in the scope and in the process
    group `pgid`, and wait until both are empty. True when empty. The group leader must already be
    reaped (a zombie still counts as a member of its group)."""
    unit = scope_unit(unit)
    cg = systemctl("show", "-p", "ControlGroup", "--value", unit).stdout.strip()

    def procs():
        if not cg:
            return ""
        try:
            return Path("/sys/fs/cgroup" + cg, "cgroup.procs").read_text().strip()
        except (FileNotFoundError, OSError):
            return ""

    if not procs() and not pgroup_alive(pgid):  # the usual case: lean exited and time reaped it
        systemctl("reset-failed", unit)
        return True
    systemctl("kill", "--signal=SIGKILL", unit)
    if pgroup_alive(pgid):
        try:
            os.killpg(pgid, signal.SIGKILL)
        except ProcessLookupError:
            pass
    t0 = time.time()
    while time.time() - t0 < timeout:
        if not procs() and not pgroup_alive(pgid):
            systemctl("reset-failed", unit)
            return True
        time.sleep(0.2)
    return False


def shadowed_modules(roots):
    """As d311:180-196: {module path: [roots]} for every .olean that two LEAN_PATH roots provide."""
    seen, dup = {}, {}
    for r in roots:
        if not os.path.isdir(r):
            continue
        for dirpath, _, files in os.walk(r):
            for fn in files:
                if fn.endswith(".olean") and ".tmp" not in fn:
                    rel = os.path.relpath(os.path.join(dirpath, fn), r)
                    if rel in seen:
                        dup.setdefault(rel, [seen[rel]]).append(r)
                    else:
                        seen[rel] = r
    return dup


def lake_lean_path():
    """lake's LEAN_PATH (as d311:211-212), in a small capped scope as assemble_final311.sh:452-453."""
    r = subprocess.run(["systemd-run", "--user", "--scope", "--quiet", "-p", "MemoryMax=2G", "-p",
                        "MemorySwapMax=0", "nice", "-n", "5", "lake", "env", "printenv", "LEAN_PATH"],
                       cwd=REPO, capture_output=True, text=True)
    if r.returncode != 0 or not r.stdout.strip():
        sys.exit(f"lake env printenv LEAN_PATH failed: {r.stderr.strip()[:300]}")
    return r.stdout.strip()


def prepare(nice):
    """lean_make.sh with LM_NO_BUILD=1 on the 5 STAMPED modules: refuses (never rebuilds) when one is
    not current. Returns their stamps and lake's LEAN_PATH."""
    env = dict(os.environ, LM_NICE=str(nice), LM_NO_BUILD="1")
    r = subprocess.run([str(HERE / "lean_make.sh"), *STAMPED], env=env, capture_output=True, text=True)
    sys.stderr.write(r.stderr)
    if r.returncode != 0:
        sys.exit("lean_make.sh with LM_NO_BUILD=1 refused (a CompactChecker module is not current); "
                 "refusing to run rather than rebuild")
    # lean_make.sh stamps are transitive (source, imports' stamps, library .oleans, toolchain).
    stamps = {m: (BUILD / "CompactChecker" / f"{m}.stamp").read_text().strip() for m in STAMPED}
    return stamps, lake_lean_path()


def deps_stamp_of(phase, catalog, stamps):
    """As d311:216-222. Chunks and Roots depend on Path and their side's catalog; Final on all stamps
    (here always the 5 STAMPED names)."""
    if phase == "final":
        names = sorted(stamps)
    else:
        names = ["Path", catalog]
    return hashlib.sha256("\n".join(f"{n}={stamps[n]}" for n in names).encode()).hexdigest()


def unanon(s):
    return s.replace("<repo>", str(REPO)).replace("<home>", str(Path.home()))


def mpath(m):
    return Path(*m.split(".")).with_suffix(".olean")


def check_library(lake_lp):
    """As assemble_final311.sh:214-237: toolchain, lake manifest, lake's roots and every library .olean
    that build/chain311/library.json pins must be as when pinned. [] or the problems."""
    lib = json.loads((CHAIN / "library.json").read_text())
    clo = json.loads((CHAIN / "closure.json").read_text())
    tc, mf = sha256_file(REPO / "lean-toolchain"), sha256_file(REPO / "lake-manifest.json")
    probs = []
    for name, rec in (("closure.json", clo), ("library.json", lib)):
        if rec["lean_toolchain_sha256"] != tc:
            probs.append(f"lean-toolchain differs from {name}")
        if rec["lake_manifest_sha256"] != mf:
            probs.append(f"lake-manifest.json differs from {name}")
    roots = [unanon(r) for r in lib["roots"]]
    if roots != [r for r in lake_lp.split(":") if r]:
        probs.append("lake's LEAN_PATH roots differ from library.json's")
    if not set(clo["library_imports"]) <= set(lib["modules"]):
        probs.append("library.json does not cover closure.json's library imports")
    diff = [m for m, (i, h) in lib["modules"].items()
            if not (Path(roots[i]) / mpath(m)).is_file() or sha256_file(Path(roots[i]) / mpath(m)) != h]
    if diff:
        probs.append(f"{len(diff)} library .olean files differ from library.json, e.g. {diff[:4]}")
    info = {"library_pinned_verified": len(lib["modules"]) if not probs else 0,
            "library_digest_sha256": lib["digest_sha256"], "library_pinned_utc": lib["written"]}
    return info, probs


def check_route_inputs():
    """The CompactChecker and build/ext .olean files of the verified 311 assembly (route 'same'): the
    E311R .olean files were compiled against them. ({file: sha256}, problems)."""
    if not ROUTE_RECORD.is_file():
        return {}, [f"{ROUTE_RECORD} is missing"]
    rec = json.loads(ROUTE_RECORD.read_text())
    probs = []
    if rec.get("verified") is not True or rec.get("route") != "same":
        probs.append(f"{ROUTE_RECORD.name} is not a verified route-'same' record")
    inputs = rec.get("chain", {}).get("inputs", {})
    if not inputs:
        probs.append(f"{ROUTE_RECORD.name} lists no chain inputs")
    for u, v in sorted(inputs.items()):
        f = BUILD / (u + ".olean")
        if not f.is_file():
            probs.append(f"build/{u}.olean is missing")
        elif sha256_file(f) != v["sha256"]:
            probs.append(f"build/{u}.olean differs from the 311 assembly record")
    return {u: v["sha256"] for u, v in inputs.items()}, probs


def parse_reuse(spec):
    d, sep, prefix = (spec or "").rpartition(":")
    if not sep or not d or not prefix:
        sys.exit(f"--reuse wants DIR:PREFIX (got {spec!r})")
    if prefix != REUSE_PREFIX:
        sys.exit(f"--reuse: only the residual side {REUSE_PREFIX} can be reused (got {prefix})")
    return Path(d).resolve(), prefix


def row_axioms(row):
    return dict(re.findall(r"([A-Za-z0-9_.]+)=\[([^\]]*)\]", row.get("axioms", "")))


def check_reuse(rdir, prefix, stamps):
    """Read-only verification of a reused, already compiled side (rdir = an export of drive_es311.py).
    Returns (info, problems); info["oleans"] maps module -> (.olean path, recorded sha256)."""
    probs = []
    mf = rdir / f"manifest-{prefix}.json"
    tsv = rdir / "run.tsv"
    if not mf.is_file() or not tsv.is_file():
        return None, [f"{mf} or {tsv} is missing"]
    man = json.loads(mf.read_bytes())
    if man.get("prefix") != prefix:
        probs.append(f"manifest prefix {man.get('prefix')!r} is not {prefix}")
    if man.get("complete") is not True or not man.get("root"):
        probs.append("the reused manifest is not complete or has no Root")
    for k, v in SIDES[prefix].items():
        if man.get(k) != v:
            probs.append(f"reused manifest {k} = {man.get(k)!r}, E310.Final needs {v!r}")
    if probs:
        return None, probs
    lines = tsv.read_text().splitlines()
    if not lines or lines[0].split("\t") != COLUMNS:  # read only: never upgraded here
        return None, [f"{tsv} does not have the current header"]
    last = {}
    for line in lines[1:]:
        row = dict(zip(COLUMNS, line.split("\t")))
        last[row["module"]] = row
    cat = man["catalog"].split(".")[-1]
    sp = shapes_es311.side_params(man)
    mods = []
    for mm in man["modules"]:
        if mm.get("corrupted"):
            probs.append(f"{mm['module']} is a corrupted test module")
        if mm["file"] is None:
            continue
        mods.append(("chunk", mm["module"], mm["file"], mm["sha256"],
                     [f"{mm['module']}.ex{s}" for s, _ in mm["subtree_roots"]]))
    if isinstance(man.get("modules"), list) and any(mm["file"] is None for mm in man["modules"]):
        probs.append("the reused manifest has unwritten modules")
    mods.append(("root", man["root"]["module"], man["root"]["file"], man["root"]["sha256"], [f"{prefix}.root"]))
    oleans, root_row = {}, None
    for phase, mod, file, src_sha, exp in mods:
        if not mod.startswith(prefix + "."):
            probs.append(f"{mod} is not a module of {prefix}")
            continue
        row = last.get(mod)
        if row is None:
            probs.append(f"{mod}: no row in run.tsv")
            continue
        if row["verdict"] != "ok" or row["phase"] != phase:
            probs.append(f"{mod}: last row is {row['phase']} {row['verdict']}, not {phase} ok")
            continue
        if row["src_sha256"] != src_sha:
            probs.append(f"{mod}: row source sha256 {row['src_sha256'][:12]} is not the manifest's {src_sha[:12]}")
            continue
        if row["deps_stamp"] != deps_stamp_of(phase, cat, stamps):
            probs.append(f"{mod}: dependency stamp {row['deps_stamp'][:12]} is not the current Path+{cat} stamp")
            continue
        ax = row_axioms(row)
        if not all(e in ax and {a.strip() for a in ax[e].split(",") if a.strip()} <= ALLOWED for e in exp):
            probs.append(f"{mod}: the row does not show standard axioms for {exp}")
            continue
        f = rdir / file
        if not f.is_file():
            probs.append(f"{mod}: source {file} is missing")
            continue
        data = f.read_bytes()
        if hashlib.sha256(data).hexdigest() != src_sha:
            probs.append(f"{mod}: source {file} differs from the manifest's sha256")
            continue
        errs = shapes_es311.check_text(data.decode("utf-8"), phase, mod if phase == "chunk" else prefix, sp)
        if errs:
            probs.append(f"{mod}: line-shape check failed ({errs[0]})")
            continue
        o = rdir / "olean" / mpath(mod)
        if not o.is_file() or sha256_file(o) != row["olean_sha256"]:
            probs.append(f"{mod}: .olean {o.relative_to(rdir)} is missing or differs from its row")
            continue
        oleans[mod] = (o.resolve(), row["olean_sha256"])
        if phase == "root":
            root_row = row
    route, rprobs = check_route_inputs()
    probs += rprobs
    digest = hashlib.sha256("".join(f"{m}\t{s}\n" for m, (_, s) in sorted(oleans.items())).encode()).hexdigest()
    info = {"dir": str(rdir), "prefix": prefix, "modules": len(oleans), "expected_modules": len(mods),
            "chunks": sum(1 for m in mods if m[0] == "chunk"), "total_leaves": man["total_leaves"],
            "manifest_sha256": sha256_file(mf), "olean_digest_sha256": digest,
            "route_inputs_verified": len(route) if not rprobs else 0, "oleans": oleans,
            "root_module": man["root"]["module"], "root_row": root_row}
    if len(oleans) != len(mods) and not probs:
        probs.append("not every reused module verified")
    return info, probs


def recheck_reuse(reuse, link_root):
    """Problems if a reused .olean or its symlink (link_root/<module path>.olean) changed since check_reuse."""
    probs = []
    for mod, (o, s) in sorted(reuse["oleans"].items()):
        ln = link_root / mpath(mod)
        if not ln.is_symlink() or os.readlink(ln) != str(o):
            probs.append(f"{mod}: symlink {ln} changed")
        elif not o.is_file() or sha256_file(o) != s:
            probs.append(f"{mod}: reused .olean {o} changed")
    return probs


def make_reuse_links(link_root, reuse):
    """link_root/<prefix>/*.olean (link_root = EXPORT_DIR/reuse, the LEAN_PATH root): file symlinks to the
    verified .olean files, so that module E311R.X is link_root/E311R/X.olean. Rebuilt at each start; only
    symlinks and directories under link_root/<prefix> are ever removed."""
    sub = link_root / reuse["prefix"]
    if sub.exists():
        for dp, dns, fns in os.walk(sub, topdown=False):
            for n in fns + dns:
                p = os.path.join(dp, n)
                if os.path.islink(p):
                    os.unlink(p)
                elif os.path.isdir(p):
                    os.rmdir(p)
                else:
                    sys.exit(f"{p} is not a symlink; refusing to touch {sub}")
    for mod, (o, _) in reuse["oleans"].items():
        ln = link_root / mpath(mod)
        ln.parent.mkdir(parents=True, exist_ok=True)
        ln.symlink_to(o)


def parse_tctl(text):
    """The highest 'Tctl:' reading of `sensors` output, or None."""
    vals = [float(v) for v in re.findall(r"^Tctl:\s+\+?(-?\d+(?:\.\d+)?)", text, re.M)]
    return max(vals) if vals else None


def tctl_now():
    try:
        r = subprocess.run(["sensors"], capture_output=True, text=True, timeout=20)
    except (OSError, subprocess.TimeoutExpired):
        return None
    return parse_tctl(r.stdout)


PAUSE_RE = re.compile(r"^(\d{4}-\d\d-\d\d \d\d:\d\d:\d\d) PAUSE\b")


def campaign_pause(log, now=None, tail_lines=PAUSE_TAIL_LINES, window=PAUSE_WINDOW_S):
    """The newest PAUSE line among the last `tail_lines` lines of the campaign log that is less than
    `window` seconds old, or None (also when the log is missing). campaign.py:22-23 writes local times."""
    try:
        with open(log, "rb") as f:
            f.seek(0, os.SEEK_END)
            f.seek(max(0, f.tell() - 65536))
            tail = f.read().decode("utf-8", "replace").splitlines()[-tail_lines:]
    except OSError:
        return None
    now = time.time() if now is None else now
    hit = None
    for ln in tail:
        m = PAUSE_RE.match(ln)
        if not m:
            continue
        try:
            t = time.mktime(time.strptime(m.group(1), "%Y-%m-%d %H:%M:%S"))
        except ValueError:
            continue
        if now - t < window:
            hit = ln
    return hit


def witness_files(campaign_dir):
    """The campaign's WITNESS files (read only): campaign/WITNESS-ALERT.txt and runs/*WITNESS*."""
    if campaign_dir is None:
        return []
    c = Path(campaign_dir)
    found = [str(c / "campaign" / "WITNESS-ALERT.txt")] if (c / "campaign" / "WITNESS-ALERT.txt").exists() else []
    found += sorted(str(p) for p in (c / "runs").glob("*WITNESS*")) if (c / "runs").is_dir() else []
    return found


def parse_utc(s):
    return datetime.datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=datetime.timezone.utc).timestamp()


def row_span(row):
    """(start, end) of a TSV row in epoch seconds: utc is written when the compile ends (finish())."""
    end = parse_utc(row["utc"])
    return end - float(row["wall_s"]), end


def imports_before(import_rows, row, slack=2.0):
    """The modules among import_rows ({module: row}) whose row ended more than `slack` s after `row` started
    (the assembly's check-run rule)."""
    try:
        start = row_span(row)[0]
    except (KeyError, ValueError):
        return sorted(import_rows)
    late = []
    for m, r in import_rows.items():
        try:
            if r is None or row_span(r)[1] > start + slack:
                late.append(m)
        except (KeyError, ValueError):
            late.append(m)
    return sorted(late)


def full_status(manifests, reuse):
    """(True, None) when E310.Final can be added; else (False, reason)."""
    if set(manifests) != {MAIN_PREFIX}:
        return False, f"the manifests are {sorted(manifests)}, not exactly [{MAIN_PREFIX}]"
    d = manifests[MAIN_PREFIX]
    if d.get("complete") is not True or not d.get("root"):
        return False, f"manifest-{MAIN_PREFIX}.json is not complete"
    for k, v in SIDES[MAIN_PREFIX].items():
        if d.get(k) != v:
            return False, f"manifest-{MAIN_PREFIX}.json has {k} = {d.get(k)!r}, not {v!r}"
    if not reuse or reuse.get("prefix") != REUSE_PREFIX:
        return False, f"no verified --reuse of {REUSE_PREFIX}"
    return True, None


def parse_log(text):
    """As d311:225-247."""
    def cum(name):
        m = re.search(rf"^\s+{re.escape(name)} ([0-9.]+)(ms|s)$", text, re.M)
        return float(m.group(1)) / (1000 if m.group(2) == "ms" else 1) if m else float("nan")

    def tv(key):
        m = re.search(rf"{re.escape(key)}: (\S+)", text)
        return m.group(1) if m else None

    wall = tv("Elapsed (wall clock) time (h:mm:ss or m:ss)")
    wall_s = sum(float(p) * 60 ** i for i, p in enumerate(reversed(wall.split(":")))) if wall else float("nan")
    pairs = re.findall(r"^'([^']+)' depends on axioms: \[([^\]]*)\]", text, re.M)
    pairs += [(k, "") for k in re.findall(r"^'([^']+)' does not depend on any axioms", text, re.M)]
    ax = dict(pairs)
    names = [k for k, _ in pairs]
    cg = re.search(r"^cgroup memory\.peak: (\d+)$", text, re.M)
    return {"kernel_s": cum("type checking"), "elab_s": cum("elaboration"), "wall_s": wall_s,
            "user_s": float(tv("User time (seconds)") or "nan"),
            "peak_rss_kb": int(tv("Maximum resident set size (kbytes)") or 0),
            "cg_peak_kb": int(cg.group(1)) // 1024 if cg else 0,
            "exit": int(tv("Exit status") or -1), "axioms": ax,
            "repeated": {k for k in names if names.count(k) > 1},
            "error": bool(re.search(r"(^|\s)error:|declaration uses 'sorry'", text))}


def inside(p, q):
    p, q = Path(os.path.realpath(p)), Path(os.path.realpath(q))
    return p == q or q in p.parents


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("export", type=Path)
    ap.add_argument("--reuse", help="DIR:E311R, an export of drive_es311.py whose residual side is reused")
    ap.add_argument("--jobs", type=int, default=2)
    ap.add_argument("--memory", default="12G", help="MemoryMax of each chunk compile")
    ap.add_argument("--root-memory", default="24G", help="MemoryMax of the Root and Final compiles")
    ap.add_argument("--nice", type=int, default=10)
    ap.add_argument("--reserve-gb", type=float, default=10.0)
    ap.add_argument("--job-gb", type=float, default=5.0, help="expected peak per chunk job")
    ap.add_argument("--tsv", type=Path)
    ap.add_argument("--only", help="comma-separated module names")
    ap.add_argument("--bench", type=int, default=0, help="compile each selected module R times, ignoring done state")
    ap.add_argument("--no-final", action="store_true", help="stop after the chunks and Roots")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--max-tctl", type=float, default=80.0, help="start a job only below this Tctl (C, <= 85)")
    ap.add_argument("--campaign-log", type=Path, default=CAMPAIGN_LOG,
                    help="no job starts while its last 50 lines hold a PAUSE line newer than 10 min")
    ap.add_argument("--start-gap", type=float, default=60.0, help="seconds between two job starts")
    ap.add_argument("--campaign-dir", type=Path, default=CAMPAIGN_DIR,
                    help="the campaign whose WITNESS files stop the driver (read only)")
    ap.add_argument("--mem-wait-max", type=float, default=1800.0,
                    help="stop (exit 3) when nothing runs and the memory gate has blocked this many seconds")
    args = ap.parse_args()
    try:
        chunk_cap = mem_gb(args.memory)
        root_cap = mem_gb(args.root_memory or args.memory)
    except ValueError as e:
        sys.exit(str(e))
    if not 0 < args.max_tctl <= 85:
        sys.exit("--max-tctl must be in (0, 85]")
    if args.jobs < 1 or args.nice < 0 or args.start_gap < 0 or args.mem_wait_max <= 0:
        sys.exit("--jobs >= 1, --nice >= 0, --start-gap >= 0 and --mem-wait-max > 0 are required")
    ex = args.export.resolve()
    if not ex.is_dir():
        sys.exit(f"{ex} is not a directory")
    for p in PROTECTED:
        if inside(ex, p):
            sys.exit(f"{ex} lies in {p}; refusing to drive a compile there")
    src_root, olean_root, log_root = ex / "src", ex / "olean", ex / "logs"
    tsv = args.tsv or ex / "run.tsv"
    if any(inside(tsv, p) for p in PROTECTED):
        sys.exit(f"--tsv {tsv} lies in a protected directory")
    rdir = rprefix = None
    if args.reuse:
        rdir, rprefix = parse_reuse(args.reuse)
        if inside(ex, rdir) or inside(rdir, ex):
            sys.exit(f"the export {ex} and the reused export {rdir} overlap")
    # One driver per export: the startup clean-up below would otherwise hit another driver's jobs.
    lockf = open(ex / ".driver.lock", "w")
    try:
        fcntl.flock(lockf, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        sys.exit(f"another drive_es310.py holds {ex / '.driver.lock'}")
    rlock = None
    if rdir is not None and (rdir / ".driver.lock").is_file():
        rlock = open(rdir / ".driver.lock", "rb")  # read-only; a shared lock keeps drive_es311.py out
        try:
            fcntl.flock(rlock, fcntl.LOCK_SH | fcntl.LOCK_NB)
        except BlockingIOError:
            sys.exit(f"a driver holds {rdir / '.driver.lock'}; the reused export may be changing")
    wit = witness_files(args.campaign_dir)
    if wit:
        print(f"WITNESS files in the campaign: {wit[:3]}; refusing to start (keep every file; tell the user)",
              flush=True)
        sys.exit(5)
    tag = SCOPE_TAG + hashlib.sha256(str(ex).encode()).hexdigest()[:10]  # scope names of this export
    manifests = {}
    for mf in sorted(ex.glob("manifest-*.json")):
        d = json.loads(mf.read_text())
        manifests[d["prefix"]] = d
    if not manifests:
        sys.exit("no manifest in " + str(ex))
    if rprefix is not None and rprefix in manifests:
        sys.exit(f"{ex} holds a manifest of the reused prefix {rprefix}; it is never compiled here")
    # Stamps (LM_NO_BUILD=1), lake's LEAN_PATH and the library pins, then the reused side.
    stamps, base_lp = prepare(args.nice)
    lib, lprobs = check_library(base_lp)
    if lprobs:
        sys.exit("library: " + "; ".join(lprobs) + " (the build may be stale); refusing to run")
    reuse = None
    if rdir is not None:
        reuse, rprobs = check_reuse(rdir, rprefix, stamps)
        if rprobs:
            sys.exit(f"--reuse {args.reuse}: {len(rprobs)} problems, e.g. {rprobs[:4]}; refusing to run "
                     f"(the reused side is never compiled here)")
    # The work list, with the expected theorems of each module.
    work = []  # (phase, module, file, leaves, expected theorem names, manifest sha or None)
    for prefix, d in manifests.items():
        for mm in d["modules"]:
            if mm["file"] is None:
                continue
            if mm.get("corrupted") and not (args.bench or args.only):
                sys.exit(f"{mm['module']} is a corrupted test module (only with --only or --bench)")
            exp = [f"{mm['module']}.ex{s}" for s, _ in mm["subtree_roots"]]
            work.append(("chunk", mm["module"], ex / mm["file"], mm["leaves"], exp, mm["sha256"]))
        if d["complete"] and d["root"]:
            work.append(("root", d["root"]["module"], ex / d["root"]["file"], d["total_leaves"],
                         [f"{prefix}.root"], d["root"]["sha256"]))
    full, why_not = full_status(manifests, reuse)
    final_note = "added" if full and not args.no_final else ("--no-final" if full else f"not full: {why_not}")
    if full and not args.no_final:
        fpath = src_root / "E310" / "Final.lean"
        fpath.parent.mkdir(parents=True, exist_ok=True)
        if not fpath.exists() or fpath.read_text() != FINAL_TEMPLATE:
            fpath.write_text(FINAL_TEMPLATE)
        work.append(("final", FINAL_MODULE, fpath, manifests[MAIN_PREFIX]["total_leaves"] + reuse["total_leaves"],
                     list(FINAL_EXPECTED), hashlib.sha256(FINAL_TEMPLATE.encode()).hexdigest()))
    if args.only:
        sel = set(args.only.split(","))
        work = [w for w in work if w[1] in sel]
        missing = sel - {w[1] for w in work}
        if missing:
            sys.exit(f"unknown or unwritten modules: {sorted(missing)}")
    # Chunks first, longest predicted first; then the Roots; then Final (d311:311-315).
    side_of = {p: d["side"] for p, d in manifests.items()}
    work = (sorted((w for w in work if w[0] == "chunk"),
                   key=lambda w: -MS_PER_LEAF.get(side_of[w[1].split(".")[0]], 30.0) * w[3])
            + [w for w in work if w[0] == "root"] + [w for w in work if w[0] == "final"])
    # Source hashes must match the manifests, and every generated line must have one of the
    # exporter's shapes, before anything runs (d311:316-331).
    sp_of = {p: shapes_es311.side_params(d) for p, d in manifests.items()}
    for phase, mod, f, _, _, want in work:
        data = f.read_bytes()
        got = hashlib.sha256(data).hexdigest()
        if got != want:
            sys.exit(f"{mod}: source sha256 {got} differs from the manifest ({want}); refusing to run")
        if phase == "final":
            errs = [] if data.decode("utf-8") == FINAL_TEMPLATE else ["not the fixed Final template"]
        else:
            prefix = mod.split(".")[0]
            errs = shapes_es311.check_text(data.decode("utf-8"), phase, mod if phase == "chunk" else prefix,
                                           sp_of[prefix])
        if errs:
            sys.exit(f"{mod}: line-shape check failed ({'; '.join(errs[:3])}); refusing to run")
    catalog_of = {p: d["catalog"].split(".")[-1] for p, d in manifests.items()}
    dstamp = {w[1]: deps_stamp_of(w[0], catalog_of.get(w[1].split(".")[0]), stamps) for w in work}
    link_root = ex / "reuse"
    roots = [base_lp, str(BUILD), str(BUILD / "ext"), str(olean_root)]
    if reuse:
        make_reuse_links(link_root, reuse)
        roots.append(str(link_root))  # the parent: module E311R.X is reuse/E311R/X.olean
    lean_path = ":".join(roots)
    dup = shadowed_modules(lean_path.split(":"))
    if dup:
        sys.exit(f"{len(dup)} modules are provided by two LEAN_PATH roots, e.g. "
                 f"{sorted(dup.items())[:3]}; refusing to run")
    # State from the TSV (d311:340-356).
    last = {}
    if tsv.exists():
        lines = tsv.read_text().splitlines()
        if lines[0].split("\t") == OLD_COLUMNS:  # written before cg_peak_kb existed: add the column
            lines = ["\t".join(COLUMNS)] + [line + "\t" for line in lines[1:]]
            up = tsv.with_name(tsv.name + ".upgrade")
            up.write_text("\n".join(lines) + "\n")
            os.replace(up, tsv)
        if lines[0].split("\t") != COLUMNS:
            sys.exit(f"{tsv} has another header")
        for line in lines[1:]:
            row = dict(zip(COLUMNS, line.split("\t")))
            last[row["module"]] = row
    else:
        tsv.parent.mkdir(parents=True, exist_ok=True)
        tsv.write_text("\t".join(COLUMNS) + "\n")

    def olean_of(mod):
        return olean_root / (mod.replace(".", "/") + ".olean")

    def done(mod, src_sha, stamp=None):
        row = last.get(mod)
        stamp = dstamp[mod] if stamp is None else stamp
        if not row or row["verdict"] != "ok" or row["src_sha256"] != src_sha or row["deps_stamp"] != stamp:
            return False
        o = olean_of(mod)
        return o.exists() and sha256_file(o) == row["olean_sha256"]

    done_now = {w[1]: done(w[1], w[5]) for w in work}  # one pass: every .olean hashed once per start
    # A Root / E310.Final is done only if its imports are done and were compiled before it started (fix 10).
    stale_order, root_ok = {}, {}
    for prefix, d in manifests.items():  # every complete manifest's Root, selected by --only or not
        if not (d["complete"] and d["root"]):
            continue
        rmod = d["root"]["module"]
        ok_ = done_now[rmod] if rmod in done_now else done(rmod, d["root"]["sha256"],
                                                          deps_stamp_of("root", catalog_of[prefix], stamps))
        if ok_:
            chunks = [mm for mm in d["modules"] if mm["file"] is not None]
            cst = deps_stamp_of("chunk", catalog_of[prefix], stamps)
            not_done = [mm["module"] for mm in chunks if not (done_now[mm["module"]] if mm["module"] in done_now
                                                              else done(mm["module"], mm["sha256"], cst))]
            late = imports_before({mm["module"]: last.get(mm["module"]) for mm in chunks}, last[rmod])
            if not_done or late:
                ok_ = False
                stale_order[rmod] = {"imports_not_done": not_done[:5], "imports_compiled_after_it": late[:5],
                                     "n": len(set(not_done) | set(late))}
        root_ok[rmod] = ok_
        if rmod in done_now:
            done_now[rmod] = ok_
    for w in work:
        if w[0] != "final" or not done_now[w[1]]:
            continue
        mine = MAIN_PREFIX + ".Root"
        rdone = root_ok.get(mine, False)
        imps = {mine: last.get(mine)}
        if reuse:
            imps[reuse["root_module"]] = reuse["root_row"]
        late = imports_before(imps, last[w[1]])
        if not rdone or late:
            done_now[w[1]] = False
            stale_order[w[1]] = {"imports_not_done": [] if rdone else [mine], "imports_compiled_after_it": late,
                                 "n": len(late) + (0 if rdone else 1)}
    plan = []
    for w in work:
        reps = args.bench if args.bench else (0 if done_now[w[1]] else 1)
        plan += [w] * reps
    # Left over by an earlier driver on this export (d311:372-377).
    leftover = [t for line in systemctl("list-units", "--all", "--plain", "--no-legend", "--type=scope",
                                        f"{tag}-*").stdout.splitlines()
                for t in line.split()[:2] if t.startswith(tag + "-")]
    stray = sorted(olean_root.rglob("*.tmp*.olean")) if olean_root.exists() else []
    t_now = tctl_now()
    pause_now = campaign_pause(args.campaign_log) if args.campaign_log else None
    print(json.dumps({"export": str(ex), "modules": len(work), "to_run": len(plan),
                      "already_done": sum(done_now.values()),
                      "order": ([w[1] for w in plan] if len(plan) <= 6 else
                                [w[1] for w in plan[:3]] + ["..."] + [w[1] for w in plan[-3:]]),
                      "final": final_note,
                      "reuse": ({k: v for k, v in reuse.items() if k != "oleans"} if reuse else None),
                      "library": lib,
                      "gate": {"tctl": t_now, "max_tctl": args.max_tctl,
                               "campaign_log": str(args.campaign_log) if args.campaign_log else None,
                               "campaign_log_exists": bool(args.campaign_log and args.campaign_log.is_file()),
                               "campaign_pause": pause_now, "start_gap_s": args.start_gap},
                      "memory": {"chunk_cap": args.memory, "root_cap": args.root_memory or args.memory,
                                 "chunk_need_gb": args.reserve_gb + args.job_gb,
                                 "root_need_gb": args.reserve_gb + root_cap, "mem_wait_max_s": args.mem_wait_max},
                      "stale_after_imports": stale_order, "witness_files": [],
                      "leftover_scopes": leftover, "stray_tmp_oleans": len(stray),
                      "scope_tag": tag, "deps": stamps, "tsv": str(tsv)}), flush=True)
    if args.dry_run:
        return
    for unit in leftover:
        if not kill_scope(unit):
            sys.exit(f"cannot empty the leftover scope {unit}")
    for t in stray:
        t.unlink()
    if leftover or stray:
        print(f"cleaned up: {len(leftover)} leftover scopes stopped, {len(stray)} stray temporary .olean deleted",
              flush=True)
    log_root.mkdir(parents=True, exist_ok=True)
    running = {}  # Popen -> (work item, tmp olean, log, load1, scope unit)
    queue = list(plan)
    attempt = {}

    def phase_ready(phase, prefix=None):
        """As d311:399-413: Roots wait for every chunk of their side, Final for every Root."""
        if phase == "chunk":
            return True
        pend = [w for w in queue if w[0] == "chunk" and (prefix is None or w[1].startswith(prefix + "."))]
        run = [it[0] for it in running.values() if it[0][0] == "chunk"
               and (prefix is None or it[0][1].startswith(prefix + "."))]
        if phase == "root":
            return not pend and not run and all(
                last.get(w[1], {}).get("verdict") == "ok" for w in work
                if w[0] == "chunk" and w[1].startswith(prefix + "."))
        pend = [w for w in queue if w[0] != "final"]
        run = [it[0] for it in running.values() if it[0][0] != "final"]
        return not pend and not run and all(last.get(w[1], {}).get("verdict") == "ok"
                                            for w in work if w[0] != "final")

    def start(w):
        """As d311:415-440."""
        phase, mod, f, leaves, exp, src_sha = w
        if rprefix is not None and mod.startswith(rprefix + "."):
            sys.exit(f"{mod} belongs to the reused side; never compiled here")
        if phase == "final" and reuse:
            probs = recheck_reuse(reuse, link_root)
            if probs:
                sys.exit(f"the reused side changed since this start ({probs[:3]}); not compiling {mod}")
        attempt[mod] = attempt.get(mod, 0) + 1
        final = olean_of(mod)
        final.parent.mkdir(parents=True, exist_ok=True)
        token = secrets.token_hex(6)
        tmp = final.with_suffix(f".tmp{os.getpid()}-{attempt[mod]}-{token}.olean")
        log = log_root / f"{mod}.{attempt[mod]}.{int(time.time())}.log"
        unit = f"{tag}-{token}"
        mem = args.memory if phase == "chunk" else (args.root_memory or args.memory)
        # sh reports the scope's cgroup memory.peak after time -v; the exit status is lean's.
        wrap = ('cg=/sys/fs/cgroup$(cut -d: -f3 /proc/self/cgroup); "$@"; rc=$?; '
                'echo "cgroup memory.peak: $(cat $cg/memory.peak 2>/dev/null)"; exit $rc')
        cmd = ["systemd-run", "--user", "--scope", "--quiet", f"--unit={unit}", "-p", f"MemoryMax={mem}",
               "-p", "MemorySwapMax=0", "-p", "CPUQuota=100%", "nice", "-n", str(args.nice),
               "sh", "-c", wrap, "sh", "/usr/bin/time", "-v",
               "lean", "-j1", "-R", str(src_root), "-o", str(tmp), str(f)]
        env = dict(os.environ, LEAN_PATH=lean_path, LEAN_NUM_THREADS="1", OMP_NUM_THREADS="1")
        load1 = open("/proc/loadavg").read().split()[0]
        with open(log, "w") as lf:
            p = subprocess.Popen(cmd, cwd=REPO, env=env, stdout=lf, stderr=subprocess.STDOUT,
                                 start_new_session=True)  # own process group, so that it can be killed whole
        running[p] = (w, tmp, log, load1, unit)
        print(f"{utc()} start {phase} {mod} leaves={leaves} running={len(running)} queued={len(queue)}", flush=True)

    def finish(p):
        """As d311:442-472; E310.Final also needs the reused .olean files unchanged."""
        w, tmp, log, load1, unit = running.pop(p)
        phase, mod, f, leaves, exp, src_sha = w
        emptied = kill_scope(unit, p.pid)
        text = log.read_text(errors="replace")
        r = parse_log(text)
        ok_ax = all(e in r["axioms"] and e not in r["repeated"]
                    and {a.strip() for a in r["axioms"][e].split(",") if a.strip()} <= ALLOWED for e in exp)
        reuse_ok = True
        if phase == "final" and reuse:
            probs = recheck_reuse(reuse, link_root)
            reuse_ok = not probs
            if probs:
                print(f"{mod}: the reused side changed during the compile: {probs[:3]}", flush=True)
        verdict = "ok" if (p.returncode == 0 and r["exit"] == 0 and emptied and tmp.exists() and not r["error"]
                           and ok_ax and reuse_ok and sha256_file(f) == src_sha) else "fail"
        osha, obytes = "", 0
        if verdict == "ok":
            osha, obytes = sha256_file(tmp), tmp.stat().st_size
            os.replace(tmp, olean_of(mod))
        elif tmp.exists():
            tmp.unlink()
        row = {"utc": utc(), "phase": phase, "module": mod, "leaves": leaves, "src_sha256": src_sha,
               "deps_stamp": dstamp[mod], "verdict": verdict, "exit": p.returncode,
               "kernel_s": f"{r['kernel_s']:.3f}", "elab_s": f"{r['elab_s']:.3f}",
               "wall_s": f"{r['wall_s']:.2f}", "user_s": f"{r['user_s']:.2f}",
               "peak_rss_kb": r["peak_rss_kb"], "olean_bytes": obytes, "olean_sha256": osha,
               "axioms": ";".join(f"{k}=[{v}]" for k, v in sorted(r["axioms"].items()) if k in exp) or "none",
               "expected": len(exp), "load1": load1, "host": socket.gethostname(),
               "log": str(log.relative_to(ex)), "cg_peak_kb": r["cg_peak_kb"]}
        with open(tsv, "a") as fh:
            fh.write("\t".join(str(row[c]) for c in COLUMNS) + "\n")
        last[mod] = {k: str(v) for k, v in row.items()}
        print(f"{row['utc']} {verdict} {mod} leaves={leaves} kernel={row['kernel_s']} wall={row['wall_s']} "
              f"rss={r['peak_rss_kb']} cg_peak={r['cg_peak_kb']} running={len(running)} queued={len(queue)}",
              flush=True)

    def on_signal(signum, frame):
        """As d311:474-488, with the '.scope' name."""
        for p, (w, tmp, log, _, unit) in list(running.items()):
            systemctl("kill", "--signal=SIGKILL", scope_unit(unit))
            try:
                os.killpg(p.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
            p.wait()  # reap the group leader first: an unreaped zombie keeps its process group alive
            kill_scope(unit, p.pid)
            if tmp.exists():
                tmp.unlink()
        print(f"signal {signum}: killed {len(running)} running compiles; nothing recorded for them", flush=True)
        sys.exit(130)

    gate_cache = {"t": 0.0, "why": None}
    wit_cache = {"t": 0.0, "files": []}

    def witness_now():
        """The campaign's WITNESS files, read at most every 5 s (fix 11)."""
        if time.time() - wit_cache["t"] >= 5:
            wit_cache.update(t=time.time(), files=witness_files(args.campaign_dir))
        return wit_cache["files"]

    def gate():
        """None when a new Lean job may start (Tctl and campaign PAUSE); else the reason. Cached 5 s."""
        if time.time() - gate_cache["t"] < 5:
            return gate_cache["why"]
        t = tctl_now()
        if t is None:
            why = "no-Tctl reading from sensors"
        elif t >= args.max_tctl:
            why = f"Tctl {t:.1f} C >= {args.max_tctl:g} C"
        else:
            ln = campaign_pause(args.campaign_log) if args.campaign_log else None
            why = f"campaign PAUSE in the last 10 min: {ln}" if ln else None
        gate_cache.update(t=time.time(), why=why)
        return why

    note = {"key": None, "t": 0.0}

    def waiting(msg):
        """Print why no job starts: when the kind of reason changes, else at most every 5 min."""
        key = msg.split(" ")[0]
        if key != note["key"] or time.time() - note["t"] > 300:
            print(f"{utc()} waiting: {msg}", flush=True)
            note.update(key=key, t=time.time())

    signal.signal(signal.SIGTERM, on_signal)
    signal.signal(signal.SIGINT, on_signal)
    last_start = 0.0
    stopped, mem_since = None, None
    while queue or running:
        for p in [p for p in running if p.poll() is not None]:
            finish(p)
        if witness_now() and stopped != "witness":
            stopped = "witness"
            print(f"{utc()} WITNESS files in the campaign: {witness_now()[:3]}; starting nothing more "
                  f"({len(running)} running compiles finish; keep every file; tell the user)", flush=True)
        stop = (ex / "STOP").exists() or stopped is not None
        # A Root or Final runs alone (d311:496-509), and every start passes the gates.
        while (queue and not stop and len(running) < args.jobs
               and not any(it[0][0] != "chunk" for it in running.values())):
            w = next((w for w in queue if phase_ready(w[0], w[1].split(".")[0])), None)
            if w is None:
                break
            if w[0] != "chunk" and running:
                break
            if time.time() - last_start < args.start_gap:
                break
            need = args.reserve_gb + (args.job_gb if w[0] == "chunk" else root_cap)
            if mem_available_gb() < need:
                waiting(f"MemAvailable {mem_available_gb():.1f} GiB < {need:g} GiB")
                if running:
                    mem_since = None
                elif mem_since is None:
                    mem_since = time.time()
                elif time.time() - mem_since > args.mem_wait_max:  # fix 12: never wait forever with nothing running
                    stopped = "memory"
                    print(f"{utc()} nothing ran and the memory gate blocked {w[1]} for {args.mem_wait_max:g} s "
                          f"(needs {need:g} GiB of MemAvailable, have {mem_available_gb():.1f}); stopping", flush=True)
                break
            mem_since = None
            why = gate()
            if why:
                waiting(why)
                break
            queue.remove(w)
            start(w)
            last_start = time.time()
            gate_cache["t"] = 0.0  # read the temperature afresh before the next start
        if stop and not running:
            print("STOP file present; stopping" if stopped is None else f"stopping ({stopped})", flush=True)
            break
        if queue and not running and not any(phase_ready(w[0], w[1].split(".")[0]) for w in queue):
            print("blocked: a prerequisite failed; see the TSV", flush=True)
            break
        time.sleep(1)
    bad = [m for m, row in last.items() if row["verdict"] != "ok" and m in {w[1] for w in work}]
    print(json.dumps({"finished": utc(), "not_ok": sorted(bad), "not_started": len(queue),
                      "stopped": stopped or ("STOP" if queue and (ex / "STOP").exists() else None)}), flush=True)
    sys.exit(5 if stopped == "witness" else 1 if bad else 3 if queue else 0)  # fix 12


if __name__ == "__main__":
    main()
