#!/usr/bin/env python3
"""Driver for the compact ES(8) <= 311 recheck (6 November 2026). Written and tested on trial
exports; the full run has NOT been launched.

  drive_es311.py EXPORT_DIR [--jobs 16] [--only E311B.C00001,...] [--bench R] [--tsv FILE]

EXPORT_DIR holds what export_es311.py wrote (manifest-<Prefix>.json, src/<Prefix>/*.lean). The
driver compiles, in order:
  1. every chunk module of every manifest in EXPORT_DIR, of both sides, longest predicted first
     (parallel, --jobs at a time);
  2. each side's Root module, once all its chunks are done (complete manifests only);
  3. E311.Final (written here from a fixed template), once both Roots are done; it applies
     Bridge311Bal.balanced_of_root and Bridge311Res.residual_of_root and prints the axioms of
     the two statements that Final311 consumes.
A Root or Final starts only when nothing else runs, and nothing starts while it runs. Every
compile is one `lean -j1` process in its own named scope,
  systemd-run --user --scope --unit=es311-<export tag>-<token> -p MemoryMax=<--memory>
    -p MemorySwapMax=0 -p CPUQuota=100% nice -n <--nice>
(MemorySwapMax=0 makes MemoryMax a hard cap: without it a scope may swap past MemoryMax), with
/usr/bin/time -v, writing the .olean to a temporary name first. The log ends with the scope's cgroup
memory.peak (charged memory; the RSS of `time` also counts .olean pages mapped from the page cache).

Before anything runs (6 November 2026 review fixes): every source must have its manifest sha256 and
pass the strict line-shape check of shapes_es311.py (only the exporter's lines: no axiom, #eval,
option, macro or other command could fake a log line or weaken the kernel), E311.Final must be the
fixed template, and no module may be provided by two LEAN_PATH roots.

A module is marked done (verdict "ok") only if Lean exits 0, its scope could be emptied, the
.olean was written, the log has no error and no sorry, and for every theorem the module must
export (each subtree root `ex<k>` of a chunk, `root` of a Root, the two statements of Final) the
log has exactly one `#print axioms` line, starting a line, with axioms within {propext,
Classical.choice, Quot.sound}. Only then is the .olean renamed into place. Every attempt appends
one row to the TSV (default EXPORT_DIR/run.tsv): source sha256, dependency stamp, verdict,
kernel/elaboration/wall/user seconds, peak RSS, .olean size and sha256, axioms, log path and
the scope's cgroup memory.peak.

Restart safety: one driver per export (EXPORT_DIR/.driver.lock). On start it stops any scope
left by an earlier driver on this export (an orphaned lean), deletes stray temporary .olean files,
and reads the TSV; a module counts as done only if its last row is "ok", for the same source
sha256 (which must also equal the manifest's) and dependency stamp, and its .olean still has the
recorded sha256. Anything else is redone. When a compile ends, its scope is killed if anything is
left in it, and waited for, before the temporary .olean is renamed or deleted. Kill it at any time
(or touch EXPORT_DIR/STOP to let running jobs finish and stop). A job is started only while
MemAvailable is above --reserve-gb plus --job-gb.
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
ALLOWED = {"propext", "Classical.choice", "Quot.sound"}
OLD_COLUMNS = ["utc", "phase", "module", "leaves", "src_sha256", "deps_stamp", "verdict", "exit",
               "kernel_s", "elab_s", "wall_s", "user_s", "peak_rss_kb", "olean_bytes", "olean_sha256",
               "axioms", "expected", "load1", "host", "log"]
COLUMNS = OLD_COLUMNS + ["cg_peak_kb"]  # 6 November 2026 review fixes: the scope's cgroup memory.peak
# Predicted wall seconds per leaf (logs/es311/trial-fit.json), only to start the longest chunks first.
MS_PER_LEAF = {"balanced": 27.4, "residual": 14.4}

FINAL_TEMPLATE = """import E311B.Root
import E311R.Root
import CompactChecker.Bridge311Bal
import CompactChecker.Bridge311Res

/-!
ES(8) ≤ 311, compact recheck: the two arithmetic facts that `Final311/Final.lean` consumes.

* `balanced_excludes_63` is the body of `OmissionBalanced.ExcludesHoleBudget 63`
  (BalancedBudgets.lean), which Final311 obtains as
  `OmissionBalancedCover63.exclusion_transfer OmissionBalancedCover63.excludes_budget`.
* `residual_excludes_32` is the body of `OmissionResidual32Bridge2650.Excludes2650Zero 32`
  (Residual32Bridge2650/Rows.lean), which Final311 uses as `residual_excludes_2650_zero`.
-/

open scoped BigOperators

namespace E311

theorem balanced_excludes_63 :
    ¬ ∃ holes : Fin 252 → ℕ, (∀ i, holes i ≤ 1) ∧
      (∀ r, OmissionBalanced.demand r ≤ ∑ i ∈ OmissionBalanced.support r, holes i) ∧
      (∑ i, holes i) ≤ 63 :=
  CompactChecker.Bridge311Bal.balanced_of_root E311B.root

theorem residual_excludes_32 :
    ¬ ∃ holes : Fin 154 → ℕ, (∀ i, holes i ≤ 1) ∧ holes 0 = 0 ∧
      (∀ r, OmissionResidual32Bridge2650.demand2650 r ≤
        ∑ i ∈ OmissionResidual32Bridge2650.support2650 r, holes i) ∧
      (∑ i, holes i) ≤ 32 :=
  CompactChecker.Bridge311Res.residual_of_root E311R.root

#print axioms balanced_excludes_63
#print axioms residual_excludes_32

end E311
"""
DEFAULT_ROOTS = {"E311B": (0, []), "E311R": (1, [[0, 2]])}


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


def utc():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def systemctl(*args):
    return subprocess.run(["systemctl", "--user", *args], capture_output=True, text=True)


def pgroup_alive(pgid):
    if not pgid:
        return False
    try:
        os.killpg(pgid, 0)
        return True
    except (ProcessLookupError, PermissionError):
        return False


def kill_scope(unit, pgid=None, timeout=300):
    """SIGKILL whatever is left in the scope `unit` and in the process group `pgid`, and wait until
    both are empty, so that no orphaned lean can write a file afterwards. True when empty. The
    group leader must already be reaped (a zombie still counts as a member of its group)."""
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
    """{module path: [roots]} for every .olean that two LEAN_PATH roots provide. Lean loads the first
    one found and does not check it against the .olean files compiled against the other, so the
    driver refuses to run when any module is shadowed."""
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


def prepare(catalogs, final, nice):
    """Make the CompactChecker imports current (lean_make.sh); return their stamps and LEAN_PATH."""
    mods = ["Path"] + sorted(set(catalogs))
    if final:
        mods += ["Bridge311Bal", "Bridge311Res"]
    env = dict(os.environ, LM_NICE=str(nice))
    r = subprocess.run([str(HERE / "lean_make.sh"), *mods], env=env, capture_output=True, text=True)
    sys.stderr.write(r.stderr)
    if r.returncode != 0:
        sys.exit("lean_make.sh failed")
    # lean_make.sh stamps are transitive (source, imports' stamps, library .oleans, toolchain).
    stamps = {m: (BUILD / "CompactChecker" / f"{m}.stamp").read_text().strip() for m in mods}
    lp = subprocess.run(["lake", "env", "printenv", "LEAN_PATH"], cwd=REPO, capture_output=True,
                        text=True, check=True).stdout.strip()
    return stamps, lp


def deps_stamp_of(phase, catalog, stamps):
    """Chunks and Roots depend on Path and their side's catalog; Final also on the bridges."""
    if phase == "final":
        names = sorted(stamps)
    else:
        names = ["Path", catalog]
    return hashlib.sha256("\n".join(f"{n}={stamps[n]}" for n in names).encode()).hexdigest()


def parse_log(text):
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


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("export", type=Path)
    ap.add_argument("--jobs", type=int, default=4)
    ap.add_argument("--memory", default="12G", help="MemoryMax of each chunk compile")
    ap.add_argument("--root-memory", help="MemoryMax of the Root and Final compiles (default: --memory)")
    ap.add_argument("--nice", type=int, default=5)
    ap.add_argument("--reserve-gb", type=float, default=10.0)
    ap.add_argument("--job-gb", type=float, default=5.0, help="expected peak per chunk job")
    ap.add_argument("--tsv", type=Path)
    ap.add_argument("--only", help="comma-separated module names (chunks only)")
    ap.add_argument("--bench", type=int, default=0, help="compile each selected module R times, ignoring done state")
    ap.add_argument("--no-final", action="store_true", help="stop after the chunks and Roots")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    ex = args.export.resolve()
    src_root, olean_root, log_root = ex / "src", ex / "olean", ex / "logs"
    tsv = args.tsv or ex / "run.tsv"
    # One driver per export: the startup clean-up below would otherwise hit another driver's jobs.
    lockf = open(ex / ".driver.lock", "w")
    try:
        fcntl.flock(lockf, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        sys.exit(f"another drive_es311.py holds {ex / '.driver.lock'}")
    tag = "es311-" + hashlib.sha256(str(ex).encode()).hexdigest()[:10]  # scope names of this export
    manifests = {}
    for mf in sorted(ex.glob("manifest-*.json")):
        d = json.loads(mf.read_text())
        manifests[d["prefix"]] = d
    if not manifests:
        sys.exit("no manifest in " + str(ex))
    # The work list, with the expected theorems of each module.
    work = []  # (phase, module, file, leaves, expected theorem names, manifest sha or None)
    for prefix, d in manifests.items():
        for mm in d["modules"]:
            if mm["file"] is None:
                continue
            assert not mm.get("corrupted") or args.bench or args.only, \
                f"{mm['module']} is a corrupted test module"
            exp = [f"{mm['module']}.ex{s}" for s, _ in mm["subtree_roots"]]
            work.append(("chunk", mm["module"], ex / mm["file"], mm["leaves"], exp, mm["sha256"]))
        if d["complete"] and d["root"]:
            work.append(("root", d["root"]["module"], ex / d["root"]["file"], d["total_leaves"],
                         [f"{prefix}.root"], d["root"]["sha256"]))
    full = (set(manifests) == {"E311B", "E311R"} and all(
        manifests[p]["complete"] and manifests[p]["export_root"] == DEFAULT_ROOTS[p][0]
        and manifests[p]["base_path"] == DEFAULT_ROOTS[p][1] for p in manifests))
    if full and not args.no_final:
        fpath = src_root / "E311" / "Final.lean"
        fpath.parent.mkdir(parents=True, exist_ok=True)
        if not fpath.exists() or fpath.read_text() != FINAL_TEMPLATE:
            fpath.write_text(FINAL_TEMPLATE)
        work.append(("final", "E311.Final", fpath, sum(manifests[p]["total_leaves"] for p in manifests),
                     ["E311.balanced_excludes_63", "E311.residual_excludes_32"],
                     hashlib.sha256(FINAL_TEMPLATE.encode()).hexdigest()))
    if args.only:
        sel = set(args.only.split(","))
        work = [w for w in work if w[1] in sel]
        missing = sel - {w[1] for w in work}
        if missing:
            sys.exit(f"unknown or unwritten modules: {sorted(missing)}")
    # Chunks of both sides first, longest predicted first; then the Roots; then Final.
    side_of = {p: d["side"] for p, d in manifests.items()}
    work = (sorted((w for w in work if w[0] == "chunk"),
                   key=lambda w: -MS_PER_LEAF.get(side_of[w[1].split(".")[0]], 30.0) * w[3])
            + [w for w in work if w[0] == "root"] + [w for w in work if w[0] == "final"])
    # Source hashes must match the manifests, and every generated line must have one of the
    # exporter's shapes, before anything runs.
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
    stamps, base_lp = prepare(catalog_of.values(), any(w[0] == "final" for w in work), args.nice)
    dstamp = {w[1]: deps_stamp_of(w[0], catalog_of.get(w[1].split(".")[0]), stamps) for w in work}
    lean_path = ":".join([base_lp, str(BUILD), str(BUILD / "ext"), str(olean_root)])
    dup = shadowed_modules(lean_path.split(":"))
    if dup:
        sys.exit(f"{len(dup)} modules are provided by two LEAN_PATH roots, e.g. "
                 f"{sorted(dup.items())[:3]}; refusing to run")
    # State from the TSV.
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

    def done(mod, src_sha):
        row = last.get(mod)
        if not row or row["verdict"] != "ok" or row["src_sha256"] != src_sha or row["deps_stamp"] != dstamp[mod]:
            return False
        o = olean_of(mod)
        return o.exists() and sha256_file(o) == row["olean_sha256"]

    plan = []
    for w in work:
        reps = args.bench if args.bench else (0 if done(w[1], w[5]) else 1)
        plan += [w] * reps
    # Left over by an earlier driver on this export (killed with SIGKILL, or its compile's wrapper
    # killed): scopes with an orphaned lean, and temporary .olean files. Never renamed into place.
    leftover = [t for line in systemctl("list-units", "--all", "--plain", "--no-legend", "--type=scope",
                                        f"{tag}-*").stdout.splitlines()
                for t in line.split()[:2] if t.startswith(tag + "-")]
    stray = sorted(olean_root.rglob("*.tmp*.olean")) if olean_root.exists() else []
    print(json.dumps({"export": str(ex), "modules": len(work), "to_run": len(plan),
                      "already_done": sum(1 for w in work if done(w[1], w[5])),
                      "order": ([w[1] for w in plan] if len(plan) <= 6 else
                                [w[1] for w in plan[:3]] + ["..."] + [w[1] for w in plan[-3:]]),
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
        """Roots wait for every chunk of their side, Final for every Root."""
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
        phase, mod, f, leaves, exp, src_sha = w
        attempt[mod] = attempt.get(mod, 0) + 1
        final = olean_of(mod)
        final.parent.mkdir(parents=True, exist_ok=True)
        # unique per attempt (in --bench mode the same module may run twice at once) and per driver
        token = secrets.token_hex(6)
        tmp = final.with_suffix(f".tmp{os.getpid()}-{attempt[mod]}-{token}.olean")
        log = log_root / f"{mod}.{attempt[mod]}.{int(time.time())}.log"
        unit = f"{tag}-{token}"
        root = src_root
        mem = args.memory if phase == "chunk" else (args.root_memory or args.memory)
        # sh reports the scope's cgroup memory.peak after time -v; the exit status is lean's.
        wrap = ('cg=/sys/fs/cgroup$(cut -d: -f3 /proc/self/cgroup); "$@"; rc=$?; '
                'echo "cgroup memory.peak: $(cat $cg/memory.peak 2>/dev/null)"; exit $rc')
        cmd = ["systemd-run", "--user", "--scope", "--quiet", f"--unit={unit}", "-p", f"MemoryMax={mem}",
               "-p", "MemorySwapMax=0", "-p", "CPUQuota=100%", "nice", "-n", str(args.nice),
               "sh", "-c", wrap, "sh", "/usr/bin/time", "-v",
               "lean", "-j1", "-R", str(root), "-o", str(tmp), str(f)]
        env = dict(os.environ, LEAN_PATH=lean_path, LEAN_NUM_THREADS="1", OMP_NUM_THREADS="1")
        load1 = open("/proc/loadavg").read().split()[0]
        with open(log, "w") as lf:
            p = subprocess.Popen(cmd, cwd=REPO, env=env, stdout=lf, stderr=subprocess.STDOUT,
                                 start_new_session=True)  # own process group, so that it can be killed whole
        running[p] = (w, tmp, log, load1, unit)
        print(f"{utc()} start {phase} {mod} leaves={leaves} running={len(running)} queued={len(queue)}", flush=True)

    def finish(p):
        w, tmp, log, load1, unit = running.pop(p)
        phase, mod, f, leaves, exp, src_sha = w
        # Nothing of this compile may outlive it (e.g. a lean orphaned when only the wrapper was killed).
        emptied = kill_scope(unit, p.pid)
        text = log.read_text(errors="replace")
        r = parse_log(text)
        ok_ax = all(e in r["axioms"] and e not in r["repeated"]
                    and {a.strip() for a in r["axioms"][e].split(",") if a.strip()} <= ALLOWED for e in exp)
        verdict = "ok" if (p.returncode == 0 and r["exit"] == 0 and emptied and tmp.exists() and not r["error"]
                           and ok_ax and sha256_file(f) == src_sha) else "fail"
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
        """Kill the running compiles (whole process groups), drop their temporary .oleans, exit.
        Nothing is recorded for them, so they are redone on the next start."""
        for p, (w, tmp, log, _, unit) in list(running.items()):
            systemctl("kill", "--signal=SIGKILL", unit)
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

    signal.signal(signal.SIGTERM, on_signal)
    signal.signal(signal.SIGINT, on_signal)
    while queue or running:
        for p in [p for p in running if p.poll() is not None]:
            finish(p)
        stop = (ex / "STOP").exists()
        # A Root or Final runs alone: nothing starts while one runs, and one starts only when
        # nothing runs. The queue holds every chunk before any Root, so the Roots and Final come last.
        while (queue and not stop and len(running) < args.jobs
               and not any(it[0][0] != "chunk" for it in running.values())):
            w = next((w for w in queue if phase_ready(w[0], w[1].split(".")[0])), None)
            if w is None:
                break
            if w[0] != "chunk" and running:
                break
            need = args.reserve_gb + (args.job_gb if w[0] == "chunk" else 12)
            if mem_available_gb() < need:
                break
            queue.remove(w)
            start(w)
        if stop and not running:
            print("STOP file present; stopping", flush=True)
            break
        if queue and not running and not any(phase_ready(w[0], w[1].split(".")[0]) for w in queue):
            print("blocked: a prerequisite failed; see the TSV", flush=True)
            break
        time.sleep(1)
    bad = [m for m, row in last.items() if row["verdict"] != "ok" and m in {w[1] for w in work}]
    print(json.dumps({"finished": utc(), "not_ok": sorted(bad)}), flush=True)
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
