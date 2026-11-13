#!/bin/bash
# Last step of the compact ES(8) <= 311 recheck (written 6 November 2026; NOT yet run for real):
# compile assembly/Final311Compact.lean in ONE consistent build and record its axioms.
#
#   assemble_final311.sh                 # the real assembly; refuses unless the full run is finished
#   assemble_final311.sh --dry-run       # every check, no compile
#   assemble_final311.sh --test-stub DIR # TEST ONLY: DIR/E311/Final.olean is a stub E311.Final (no Roots);
#                                        # skips the run checks; writes into DIR/out, never into logs/
#   env: A311_MEM (cap of the two final compiles, default 24G, at most 28G),
#        A311_EXTRA_ROOT (TEST ONLY, refused unless --test-stub or A311_EXPORT: one more LEAN_PATH root, to
#                         test the shadowing refusal),
#        A311_EXPORT (TEST ONLY: another export directory, e.g. a copy with an incomplete run.tsv;
#                     then nothing is written to logs/es311, only to A311_EXPORT/assemble-out)
#
# Steps (each failure stops with "refused" or "FAILED" and exit 1):
#  1. The full run must be finished: es311-full is not active, no drive_es311.py runs on the export and
#     no scope of its driver is left; build/es311/full/run.tsv has, for each of the 352 modules (349
#     chunks of the two manifests, E311B.Root, E311R.Root, E311.Final), a last row with verdict ok, the
#     manifest's (or the fixed template's) source sha256, the dependency stamp that drive_es311.deps_stamp_of
#     computes from the current lean_make stamps (every row, not only E311.Final's), and an .olean that
#     still has the recorded sha256.
#  2. The chain: build/chain311/build.tsv has an ok last row for every module of
#     build/chain311/closure.json, and each .olean still has its recorded sha256 (refused after step 4,
#     so that the LEAN_PATH check also runs on an incomplete chain). The toolchain and lake-manifest
#     sha256 of closure.json and library.json are today's; lake's LEAN_PATH roots are library.json's, and
#     every library .olean that library.json pins (Lean's list of the chain's library closure) still has
#     its sha256. lean_make.sh (with LM_NO_BUILD, which runs no Lean) confirms that Path, Fcat62,
#     Fcat2650 and the bridges are current.
#  3. The three catalogs that the bridges import (BalancedProof.Catalog, BalancedCoverCutsV2,
#     Residual32Bridge2650.Catalog) are compared by sha256 between build/ext, build/chain311/olean and the
#     October record (closure.json's recorded_olean_sha256). All equal: route "same", the existing
#     bridges and E311.Final are used, and every CompactChecker and build/ext .olean they rest on must be
#     older than the first chunk compile of the run (run.tsv), so that it is the file E311.Final and the
#     chunks were compiled against. Otherwise route "rebuilt": Bridge311Bal, Bridge311Res, Bridge311Defs and
#     E311.Final are first recompiled against build/chain311 into a separate directory (then only Path,
#     Fcat62, Fcat2650 and their imports must be older than the run). The sha256 and mtime of every one of
#     those inputs go into the report.
#  4. LEAN_PATH = lake's roots : build/chain311/olean : WORK/path, where WORK/path holds symlinks to the
#     CompactChecker .oleans E311.Final needs, the 351 chunk and Root .oleans and E311/Final.olean
#     (build/ext and build/ are NOT on it). Every .olean under every root is listed; a module provided
#     by two roots stops the script.
#  5. Final311Compact.lean (sha256 pinned below) is compiled in one hard-capped scope
#     (MemoryMax=A311_MEM, MemorySwapMax=0). Required: the scope's exit status 0, the .olean written, a
#     time -v report with "Exit status: 0" and no "Command terminated by signal", no cgroup OOM kill, no
#     error, no sorry, and exactly one `#print axioms` line for forces_convex_octagon_311, with axioms
#     within {propext, Classical.choice, Quot.sound}.
#  6. An audit file imports the result, prints the statement (`#check`, which must read
#     `... : ErdosSzekeres.ForcesConvexNGon 311 8`) and the names of all modules in its environment
#     (the same exit, signal and OOM requirements). Every one of them is mapped to the one LEAN_PATH root
#     that provides it and hashed; a library module that library.json pins must have its pinned sha256.
#  7. logs/es311/final311-compact.log (both Lean logs) and logs/es311/final311-compact.json (verdict,
#     checks, costs, catalog comparison, inputs, hashes of every non-library .olean imported, a digest of
#     the library ones), and logs/es311/final311-compact-imports.tsv.gz (every imported .olean and its hash).
#
# Every lean or lake process runs as  systemd-run --user --scope -p MemoryMax=.. -p MemorySwapMax=0 nice -n 5 ...
set -u -o pipefail
HERE=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
REPO=$(cd "$HERE/../.." && pwd)
EXPORT=${A311_EXPORT:-$HERE/build/es311/full}
CHAIN=$HERE/build/chain311
FINAL_SRC=$HERE/assembly/Final311Compact.lean
FINAL_SRC_SHA=b41a996aeff5fe34550317db03e0766fc26b11a904c124cde8a7322c13ff009a  # as committed in aeca8078e
THEOREM=ErdosSzekeres.Omission.Compact311.forces_convex_octagon_311
MEM=${A311_MEM:-24G}
MODE=real STUB=""
case "${1:-}" in
  "") ;;
  --dry-run) MODE=dry ;;
  --test-stub) MODE=stub; STUB=$(cd "${2:?--test-stub DIR}" && pwd) ;;
  *) echo "usage: $0 [--dry-run | --test-stub DIR]" >&2; exit 2 ;;
esac
if [ "$MODE" = stub ]; then WORK=$STUB/out; LOGDIR=$STUB/out
elif [ -n "${A311_EXPORT:-}" ]; then WORK=$EXPORT/assemble-out; LOGDIR=$EXPORT/assemble-out
else WORK=$CHAIN/assembly; LOGDIR=$HERE/logs/es311; fi
refuse() { echo "assemble_final311: refused: $*" >&2; exit 1; }
if [ -n "${A311_EXTRA_ROOT:-}" ] && [ "$MODE" != stub ] && [ -z "${A311_EXPORT:-}" ]; then
  echo "assemble_final311: refused: A311_EXTRA_ROOT is a test switch (only with --test-stub or A311_EXPORT)" >&2; exit 1
fi
fail() { echo "assemble_final311: FAILED: $*" >&2; exit 1; }
say() { echo "assemble_final311: $(date -u +%FT%TZ) $*" >&2; }
capped() {  # capped CAP LOG CMD...: one scope, hard cap; LOG gets time -v and the cgroup peaks
  local cap=$1 log=$2; shift 2
  (cd "$REPO" && LEAN_NUM_THREADS=1 OMP_NUM_THREADS=1 systemd-run --user --scope --quiet \
    --unit="assemble311-$(head -c5 /dev/urandom | od -An -tx1 | tr -d ' \n')" \
    -p MemoryMax="$cap" -p MemorySwapMax=0 -p CPUQuota=100% nice -n 5 \
    sh -c 'cg=/sys/fs/cgroup$(cut -d: -f3 /proc/self/cgroup); "$@"; rc=$?
      echo "cgroup memory.peak: $(cat $cg/memory.peak 2>/dev/null)"
      echo "cgroup memory.swap.peak: $(cat $cg/memory.swap.peak 2>/dev/null)"
      echo "cgroup oom_kill: $(sed -n "s/^oom_kill //p" $cg/memory.events 2>/dev/null)"; exit $rc' \
    sh /usr/bin/time -v "$@") > "$log" 2>&1
}
cap_gb=$(echo "$MEM" | sed -n 's/^\([0-9]\+\)G$/\1/p')
[ -n "$cap_gb" ] && [ "$cap_gb" -le 28 ] || refuse "A311_MEM must be <N>G with N <= 28 (got $MEM)"

# The Python helper (run with -I; reads only, except where it writes WORK/path and the outputs).
read -r -d '' PY <<'PYEOF'
import gzip, hashlib, json, os, re, subprocess, sys, datetime
from pathlib import Path
cmd, HERE = sys.argv[1], Path(sys.argv[2])
REPO, CHAIN = HERE.parent.parent, HERE / "build/chain311"
EXPORT = Path(os.environ.get("A311_EXPORT") or HERE / "build/es311/full")
ALLOWED = {"propext", "Classical.choice", "Quot.sound"}
CATS = ["BalancedProof.Catalog", "BalancedCoverCutsV2", "Residual32Bridge2650.Catalog"]
STAMPED = ["Bridge311Bal", "Bridge311Res", "Fcat2650", "Fcat62", "Path"]  # drive_es311.prepare's final set

def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 22), b""):
            h.update(b)
    return h.hexdigest()

def mpath(m):
    return Path(*m.split(".")).with_suffix(".olean")

def iso(t):
    return datetime.datetime.fromtimestamp(t, datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def parse_iso(s):
    return datetime.datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=datetime.timezone.utc).timestamp()

def unanon(s):
    return s.replace("<repo>", str(REPO)).replace("<home>", str(Path.home()))

def driver():
    sys.path.insert(0, str(HERE))
    import drive_es311
    return drive_es311

def template():
    return driver().FINAL_TEMPLATE

def last_rows(tsv):
    lines = Path(tsv).read_text().splitlines()
    cols = lines[0].split("\t")
    last = {}
    for line in lines[1:]:
        row = dict(zip(cols, line.split("\t")))
        last[row["module"]] = row
    return last

def expected_run():
    """[(phase, module, source sha256, catalog)] of the full run: 349 chunks, 2 Roots, E311.Final."""
    out = []
    for p, n in (("E311B", 223), ("E311R", 126)):
        d = json.loads((EXPORT / f"manifest-{p}.json").read_text())
        if not d["complete"]:
            sys.exit(f"manifest-{p}.json is not complete")
        cat = d["catalog"].split(".")[-1]  # as drive_es311.main's catalog_of
        ch = [m for m in d["modules"] if m["file"] is not None]
        if len(ch) != n:
            sys.exit(f"manifest-{p}.json has {len(ch)} chunk modules, expected {n}")
        out += [("chunk", m["module"], m["sha256"], cat) for m in ch]
        out.append(("root", d["root"]["module"], d["root"]["sha256"], cat))
    out.append(("final", "E311.Final", hashlib.sha256(template().encode()).hexdigest(), None))
    return out

def current_stamps():
    return {n: (HERE / "build/CompactChecker" / f"{n}.stamp").read_text().strip() for n in STAMPED}

def check_run():
    exp = expected_run()
    if len(exp) != 352:
        sys.exit(f"{len(exp)} expected modules, not 352")
    tsv = EXPORT / "run.tsv"
    if not tsv.exists():
        sys.exit("no run.tsv")
    last = last_rows(tsv)
    st, drv = current_stamps(), driver()
    bad, starts = [], []
    for phase, m, s, cat in exp:
        r = last.get(m)
        if r is None:
            bad.append(f"{m}: no row"); continue
        if r["verdict"] != "ok":
            bad.append(f"{m}: last verdict {r['verdict']}"); continue
        if r["src_sha256"] != s:
            bad.append(f"{m}: source sha256 {r['src_sha256'][:12]} is not {s[:12]}"); continue
        if r["deps_stamp"] != drv.deps_stamp_of(phase, cat, st):
            bad.append(f"{m}: dependency stamp {r['deps_stamp'][:12]} is not the current one"); continue
        o = EXPORT / "olean" / mpath(m)
        if not o.is_file() or sha(o) != r["olean_sha256"]:
            bad.append(f"{m}: .olean missing or changed since its row"); continue
        starts.append(parse_iso(r["utc"]) - float(r["wall_s"]))  # utc is written when the compile ends
    if bad:
        sys.exit(f"{len(bad)} of 352 modules are not ok, e.g. {bad[:4]}")
    fr = last["E311.Final"]
    ax = dict(re.findall(r"([A-Za-z0-9_.]+)=\[([^\]]*)\]", fr["axioms"]))
    for t in ("E311.balanced_excludes_63", "E311.residual_excludes_32"):
        if t not in ax or not {a.strip() for a in ax[t].split(",") if a.strip()} <= ALLOWED:
            sys.exit(f"E311.Final row does not show standard axioms for {t}")
    stray = [str(p) for p in (EXPORT / "olean").rglob("*.tmp*.olean")]
    if stray:
        sys.exit(f"stray temporary .olean files in the export: {stray[:3]}")
    print(json.dumps({"rows": sum(1 for _ in open(tsv)) - 1, "modules_ok": 352, "deps_stamps_ok": 352,
                      "first_compile_start_utc": iso(min(starts) - 1),
                      "final_row_utc": fr["utc"], "final_olean_sha256": fr["olean_sha256"],
                      "final_deps_stamp": fr["deps_stamp"]}))

def cc_closure(start):
    """CompactChecker modules needed by `start` (from the source import lines)."""
    seen, todo = set(), list(start)
    while todo:
        m = todo.pop()
        if m in seen:
            continue
        seen.add(m)
        for line in (HERE / "CompactChecker" / f"{m}.lean").read_text().splitlines():
            mm = re.match(r"import CompactChecker\.(\w+)\s*$", line)
            if mm:
                todo.append(mm.group(1))
    return sorted(seen)

def check_library(lake_roots):
    """library.json: toolchain, manifest, lake's roots and every pinned library .olean as when pinned."""
    lib = json.loads((CHAIN / "library.json").read_text())
    clo = json.loads((CHAIN / "closure.json").read_text())
    tc, mf = sha(REPO / "lean-toolchain"), sha(REPO / "lake-manifest.json")
    probs = []
    for name, rec in (("closure.json", clo), ("library.json", lib)):
        if rec["lean_toolchain_sha256"] != tc:
            probs.append(f"lean-toolchain differs from {name}")
        if rec["lake_manifest_sha256"] != mf:
            probs.append(f"lake-manifest.json differs from {name}")
    roots = [unanon(r) for r in lib["roots"]]
    if roots != [r for r in lake_roots if r]:
        probs.append("lake's LEAN_PATH roots differ from library.json's")
    if not set(clo["library_imports"]) <= set(lib["modules"]):
        probs.append("library.json does not cover closure.json's library imports")
    diff = [m for m, (i, h) in lib["modules"].items()
            if not (Path(roots[i]) / mpath(m)).is_file() or sha(Path(roots[i]) / mpath(m)) != h]
    if diff:
        probs.append(f"{len(diff)} library .olean files differ from library.json, e.g. {diff[:4]}")
    if probs:
        sys.exit("library: " + "; ".join(probs) + " (the chain's .olean files may be stale)")
    return {"library_pinned_verified": len(lib["modules"]), "library_digest_sha256": lib["digest_sha256"],
            "library_pinned_utc": lib["written"], "lean_toolchain_sha256": tc, "lake_manifest_sha256": mf}

def check_chain(lake_lp, run_start):
    """Completeness of build/chain311 (reported, refused later), the library, the catalogs (route) and
    the CompactChecker / build/ext inputs of that route."""
    clo = json.loads((CHAIN / "closure.json").read_text())
    last = last_rows(CHAIN / "build.tsv")
    bad, match = [], 0
    for m in clo["order"]:
        r = last.get(m)
        o = CHAIN / "olean" / mpath(m)
        if not r or r["verdict"] != "ok" or r["src_sha256"] != clo["modules"][m]["source_sha256"]:
            bad.append(f"{m} ({r['verdict'] if r else 'not built'})"); continue
        if not o.is_file() or sha(o) != r["olean_sha256"]:
            bad.append(m + " (.olean changed)"); continue
        match += r["olean_match"] == "yes"
    libj = check_library(lake_lp.split(":"))
    cats = {}
    for m in CATS:
        a, b = HERE / "build/ext" / mpath(m), CHAIN / "olean" / mpath(m)
        if not (a.is_file() and b.is_file()) or any(x.startswith(m + " ") for x in bad):
            sys.exit(f"catalog {m} is not built in both build/ext and build/chain311")
        oct_ = clo["modules"][m]["recorded_olean_sha256"]
        cats[m] = {"build_ext": sha(a), "chain311": sha(b), "october": oct_}
        cats[m]["identical"] = cats[m]["build_ext"] == cats[m]["chain311"]
        cats[m]["chain311_is_october"] = cats[m]["chain311"] == oct_
    route = "same" if all(c["identical"] and c["chain311_is_october"] for c in cats.values()) else "rebuilt"
    # The inputs the route uses from build/CompactChecker and build/ext, with sha256 and mtime.
    chunk_side = cc_closure(["Path", "Fcat62", "Fcat2650"])
    used = [f"CompactChecker/{m}" for m in chunk_side]
    if route == "same":
        used = [f"CompactChecker/{m}" for m in cc_closure(["Path", "Fcat62", "Fcat2650", "Bridge311Bal",
                                                             "Bridge311Res"])] + [f"ext/{mpath(m)}"[:-6] for m in CATS]
    hard = {}
    hc = HERE / "logs/es311/hardcap-rebuild.tsv"
    if hc.exists():
        for row in last_rows(hc).values():
            if re.fullmatch(r"[0-9a-f]{64}", row.get("olean_sha256", "")):
                hard[row["module"]] = row["olean_sha256"]
    inputs, newer = {}, []
    for u in used:
        f = HERE / "build" / (u + ".olean")
        if not f.is_file():
            sys.exit(f"input build/{u}.olean is missing")
        mod = u.split("/", 1)[1].replace("/", ".")
        inputs[u] = {"sha256": sha(f), "mtime_utc": iso(f.stat().st_mtime)}
        if mod in hard:
            inputs[u]["equals_hardcap_record"] = inputs[u]["sha256"] == hard[mod]
        if run_start and f.stat().st_mtime >= parse_iso(run_start):
            newer.append(u)
    if newer:
        sys.exit(f"route {route}: {newer} changed after the run's first compile ({run_start}); the run was not "
                 "compiled against them")
    print(json.dumps({"modules": len(clo["order"]), "complete": not bad, "not_ok": bad,
                      "closure_sha256": sha(CHAIN / "closure.json"),
                      "olean_equal_to_recorded": match, **libj, "catalogs": cats,
                      "catalogs_identical": all(c["identical"] for c in cats.values()),
                      "route": route, "run_first_compile_utc": run_start or None,
                      "inputs_older_than_run": bool(run_start), "inputs": inputs}))

def make_path(work, route, stub):
    """WORK/path: symlinks. route 'same' links the existing bridges; 'rebuilt' leaves them out."""
    import shutil
    p = Path(work) / "path"
    if p.exists():
        shutil.rmtree(p)
    need = cc_closure(["Path", "Fcat62", "Fcat2650", "Bridge311Bal", "Bridge311Res"])
    for m in need:
        if route == "rebuilt" and m in ("Bridge311Bal", "Bridge311Res"):
            continue
        t = p / "CompactChecker" / f"{m}.olean"
        t.parent.mkdir(parents=True, exist_ok=True)
        t.symlink_to(HERE / "build/CompactChecker" / f"{m}.olean")
    if stub:
        t = p / "E311/Final.olean"
        t.parent.mkdir(parents=True, exist_ok=True)
        t.symlink_to(Path(stub) / "E311/Final.olean")
        return
    for phase, m, _, _ in expected_run():
        if phase == "final" and route == "rebuilt":
            continue
        t = p / mpath(m)
        t.parent.mkdir(parents=True, exist_ok=True)
        t.symlink_to(EXPORT / "olean" / mpath(m))

def shadow(roots):
    """Refuse when a module is provided by two LEAN_PATH roots, or build/ext or build/ is a root."""
    bad_roots = {str((HERE / "build").resolve()), str((HERE / "build/ext").resolve())}
    for r in roots:
        if r and str(Path(r).resolve()) in bad_roots:
            sys.exit(f"{r} must not be on LEAN_PATH")
    seen, dup = {}, {}
    for r in roots:
        if not r or not os.path.isdir(r):
            continue
        for dp, _, fs in os.walk(r, followlinks=True):
            for fn in fs:
                if fn.endswith(".olean"):
                    k = os.path.relpath(os.path.join(dp, fn), r)
                    if k in seen:
                        dup.setdefault(k, [seen[k]]).append(r)
                    else:
                        seen[k] = r
    if dup:
        sys.exit(f"{len(dup)} modules are provided by two LEAN_PATH roots, e.g. {sorted(dup.items())[:3]}")
    print(len(seen))

def lean_ok(log, rc, expect, olean=None):
    """Scope exit rc 0, a time -v report with "Exit status: 0" and no "Command terminated by signal" (time -v
    then reports "Exit status: 0" while itself exiting 137), no cgroup OOM kill, the .olean (if given)
    written, no error, no sorry; each name in `expect` printed once, with standard axioms."""
    t = Path(log).read_text(errors="replace")
    ex = re.search(r"Exit status: (\d+)", t)
    errs = []
    if str(rc) != "0":
        errs.append(f"scope exit status {rc}")
    if not ex or ex.group(1) != "0":
        errs.append(f"exit status {ex.group(1) if ex else '?'}")
    if "Command terminated by signal" in t:
        errs.append("terminated by a signal")
    oom = re.search(r"^cgroup oom_kill: (\d+)", t, re.M)
    if not oom or oom.group(1) != "0":
        errs.append(f"cgroup oom_kill {oom.group(1) if oom else '?'}")
    if olean is not None and not Path(olean).is_file():
        errs.append("no .olean written")
    if re.search(r"(^|\s)error:", t, re.M):
        errs.append("error in log")
    if "declaration uses 'sorry'" in t:
        errs.append("sorry in log")
    pairs = [(k, re.sub(r"\s+", " ", v).strip()) for k, v in
             re.findall(r"^'([^']+)' depends on axioms: \[([^\]]*)\]", t, re.M)]
    pairs += [(k, "") for k in re.findall(r"^'([^']+)' does not depend on any axioms", t, re.M)]
    for e in expect:
        got = [v for k, v in pairs if k == e]
        if len(got) != 1:
            errs.append(f"{len(got)} axiom lines for {e}")
        elif not {a.strip() for a in got[0].split(",") if a.strip()} <= ALLOWED:
            errs.append(f"nonstandard axioms for {e}: [{got[0]}]")
    return errs, dict(pairs)

def costs(log):
    t = Path(log).read_text(errors="replace")
    g = lambda k: (re.search(k, t, re.M) or [None, None])[1]
    return {"wall": g(r"Elapsed \(wall clock\) time \(h:mm:ss or m:ss\): (\S+)"),
            "max_rss_kb": g(r"Maximum resident set size \(kbytes\): (\d+)"),
            "cgroup_memory_peak": g(r"^cgroup memory\.peak: (\d+)"),
            "cgroup_swap_peak": g(r"^cgroup memory\.swap\.peak: (\d+)"),
            "cgroup_oom_kill": g(r"^cgroup oom_kill: (\d+)")}

if cmd == "check-run":
    check_run()
elif cmd == "check-chain":
    check_chain(sys.argv[3], sys.argv[4] if len(sys.argv) > 4 else "")
elif cmd == "template":
    sys.stdout.write(template())
elif cmd == "cc-closure":
    print(" ".join(cc_closure(sys.argv[3:])))
elif cmd == "make-path":
    make_path(sys.argv[3], sys.argv[4], sys.argv[5] if len(sys.argv) > 5 else "")
elif cmd == "shadow":
    shadow(sys.argv[3].split(":"))
elif cmd == "lean-ok":
    # lean-ok LOG RC [NAME...]
    errs, _ = lean_ok(sys.argv[3], sys.argv[4], sys.argv[5:])
    print("; ".join(errs))
    sys.exit(1 if errs else 0)
elif cmd == "report":
    # report MAINLOG MAINRC AUDITLOG AUDITRC LEAN_PATH OUTJSON OUTTSVGZ MODE ROUTE RUNJSON CHAINJSON MEM SRC LAKE_LP OLEAN
    (mainlog, mainrc, auditlog, auditrc, lp, outj, outt, mode, route, runj, chainj, mem, src, lake_lp,
     olean) = sys.argv[3:18]
    thm = "ErdosSzekeres.Omission.Compact311.forces_convex_octagon_311"
    errs, axioms = lean_ok(mainlog, mainrc, [thm], olean)
    at = Path(auditlog).read_text(errors="replace")
    aerrs, _ = lean_ok(auditlog, auditrc, [])
    errs += ["audit: " + e for e in aerrs]
    stmt = re.search(r"^@?" + re.escape(thm) + r" : (.*)$", at, re.M)  # `#check @c` may print the @
    if not stmt or stmt.group(1).strip() != "ErdosSzekeres.ForcesConvexNGon 311 8":
        errs.append(f"statement is not ForcesConvexNGon 311 8: {stmt.group(0) if stmt else 'missing'}")
    mods = re.findall(r"^module (\S+)$", at, re.M)
    if "Final311Compact" not in mods or len(mods) < 1000:
        errs.append(f"audit listed {len(mods)} modules")
    roots = [r for r in lp.split(":") if r]
    lib_roots = [r for r in lake_lp.split(":") if r]
    rows, missing = [], []
    for m in sorted(set(mods)):
        hits = [r for r in roots if (Path(r) / mpath(m)).is_file()]
        if len(hits) != 1:
            missing.append(m); continue
        f = Path(hits[0]) / mpath(m)
        kind = "library" if hits[0] in lib_roots else ("chain311" if hits[0].endswith("chain311/olean") else
               ("result" if m == "Final311Compact" else "path"))
        rows.append((m, kind, hits[0], str(f.resolve()), sha(f)))
    if missing:
        errs.append(f"{len(missing)} imported modules not found exactly once on LEAN_PATH, e.g. {missing[:3]}")
    pinned = json.loads((CHAIN / "library.json").read_text())["modules"]
    off = [m for m, k, _, _, s in rows if k == "library" and m in pinned and pinned[m][1] != s]
    if off:
        errs.append(f"{len(off)} imported library modules differ from library.json, e.g. {off[:3]}")
    def anon(s):
        return s.replace(str(REPO), "<repo>").replace(str(Path.home()), "<home>")
    with gzip.open(outt, "wt") as f:
        f.write("module\tkind\troot\tfile\tsha256\n")
        for r in rows:
            f.write("\t".join(anon(x) for x in r) + "\n")
    lib = [r for r in rows if r[1] == "library"]
    digest = hashlib.sha256("".join(f"{m}\t{s}\n" for m, _, _, _, s in lib).encode()).hexdigest()
    top = {m: s for m, _, _, _, s in rows if m in ("BalancedBudgets", "Residual32Bridge2650.Rows", "E311.Final",
                                                    "CompactChecker.Bridge311Bal", "CompactChecker.Bridge311Res",
                                                    "E311B.Root", "E311R.Root", "Final311Compact")}
    rep = {"verified": not errs, "mode": mode, "route": route, "problems": errs,
           "theorem": thm, "statement": stmt.group(0) if stmt else None,
           "axioms": axioms.get(thm), "final_source": anon(src), "final_source_sha256": sha(src),
           "cap": mem, "main_compile": {"scope_exit": mainrc, **costs(mainlog)},
           "audit_compile": {"scope_exit": auditrc, **costs(auditlog)},
           "lean_path_roots": [anon(r) for r in roots], "run": json.loads(runj) if runj else None,
           "chain": json.loads(chainj), "top_level_oleans": top,
           "imported_modules": len(rows), "library_modules": len(lib), "library_digest_sha256": digest,
           "library_modules_checked_against_library_json": sum(1 for m, k, _, _, _ in rows if k == "library" and m in pinned),
           "non_library_oleans": {m: {"kind": k, "sha256": s} for m, k, _, _, s in rows if k != "library"},
           "imports_tsv": anon(outt), "imports_tsv_sha256": sha(outt)}
    Path(outj).write_text(json.dumps(rep, indent=1) + "\n")
    print(json.dumps({"verified": rep["verified"], "problems": errs, "axioms": rep["axioms"]}))
    sys.exit(0 if not errs else 1)
PYEOF
py() { local c=$1; shift; python3 -I -c "$PY" "$c" "$HERE" "$@"; }

# 1. The full run.
RUNJ=""
if [ "$MODE" != stub ]; then
  why=()  # every reason is reported
  systemctl --user is-active --quiet es311-full && why+=("unit es311-full is still active")
  pgrep -f 'drive_es311\.py.*build/es311/full' >/dev/null && why+=("a drive_es311.py runs on the export")
  TAG=es311-$(printf '%s' "$(cd "$EXPORT" && pwd -P)" | sha256sum | cut -c1-10)  # drive_es311.py's scope tag
  [ -z "$(systemctl --user list-units --all --no-legend --plain "$TAG-*" 2>/dev/null)" ] \
    || why+=("scopes of the es311-full driver ($TAG-*) are still present")
  RUNJ=$(py check-run 2>&1) || { why+=("run.tsv: $RUNJ"); RUNJ=""; }
  [ ${#why[@]} -eq 0 ] || refuse "$(printf '%s; ' "${why[@]}")"
  say "full run complete: $RUNJ"
fi

# 2. The chain and the library, and 3. the catalogs and the inputs of the route.
LAKE_LP=$(cd "$REPO" && systemd-run --user --scope --quiet -p MemoryMax=2G -p MemorySwapMax=0 nice -n 5 \
  lake env printenv LEAN_PATH) || fail "lake env"
RUN_START=""
[ -n "$RUNJ" ] && RUN_START=$(echo "$RUNJ" | python3 -I -c 'import json,sys; print(json.load(sys.stdin)["first_compile_start_utc"])')
CHAINJ=$(py check-chain "$LAKE_LP" "$RUN_START" 2>&1) || refuse "$CHAINJ"
(cd "$HERE" && LM_NO_BUILD=1 ./lean_make.sh Path Fcat62 Fcat2650 Bridge311Bal Bridge311Res) 2>/dev/null \
  || refuse "the CompactChecker modules are not current (LM_NO_BUILD=1 lean_make.sh fails)"
ROUTE=$(echo "$CHAINJ" | python3 -I -c 'import json,sys; print(json.load(sys.stdin)["route"])')
[ "$MODE" = stub ] && [ "$ROUTE" != same ] && refuse "stub test: the catalogs differ; it assumes the existing bridges"
say "library: $(echo "$CHAINJ" | python3 -I -c 'import json,sys; d=json.load(sys.stdin); print(d["library_pinned_verified"], "pinned .olean files as in library.json (" + d["library_pinned_utc"] + ")")')"
say "catalogs (build/ext = build/chain311 = October record?): $(echo "$CHAINJ" | python3 -I -c 'import json,sys; d=json.load(sys.stdin); print({k: v["identical"] and v["chain311_is_october"] for k, v in d["catalogs"].items()})'); route $ROUTE"
say "inputs of route $ROUTE: $(echo "$CHAINJ" | python3 -I -c 'import json,sys; d=json.load(sys.stdin); i=d["inputs"]; print(len(i), "files" + (", all older than the first compile of the run, " + d["run_first_compile_utc"] if d["inputs_older_than_run"] else " (no run: mtimes not checked)"))')"

# 4. LEAN_PATH.
mkdir -p "$WORK" "$LOGDIR"
py make-path "$WORK" "$ROUTE" "$STUB" || fail "make-path"
LP="$LAKE_LP:$CHAIN/olean:$WORK/path"
[ -n "${A311_EXTRA_ROOT:-}" ] && LP="$LP:$A311_EXTRA_ROOT"
NOLEAN=$(py shadow "$LP" 2>&1) || refuse "LEAN_PATH: $NOLEAN"
say "LEAN_PATH: $(echo "$LP" | tr ':' '\n' | wc -l) roots, $NOLEAN .olean files, no module provided twice"
echo "$CHAINJ" | grep -q '"complete": true' || refuse "the chain in build/chain311 is not complete: $(echo "$CHAINJ" \
  | python3 -I -c 'import json,sys; d=json.load(sys.stdin); print(len(d["not_ok"]), "of", d["modules"], "modules not ok:", ", ".join(d["not_ok"][:6]))')"

if [ "$ROUTE" = rebuilt ]; then
  say "catalogs differ: recompiling the bridges and E311.Final against build/chain311"
  RB=$WORK/rebuilt; rm -rf "$RB"; mkdir -p "$RB/src/E311" "$RB/defs"
  for m in Bridge311Bal Bridge311Res; do
    [ "$MODE" = dry ] && break
    LEAN_PATH="$LP" capped 12G "$RB/$m.log" lean -j1 -R "$HERE" -o "$WORK/path/CompactChecker/$m.olean" \
      "$HERE/CompactChecker/$m.lean" || fail "compile $m (see $RB/$m.log)"
    py lean-ok "$RB/$m.log" 0 || fail "$m log"
  done
  if [ "$MODE" != dry ]; then
    LEAN_PATH="$LP" capped 12G "$RB/Bridge311Defs.log" lean -j1 -R "$HERE" -o "$RB/defs/Bridge311Defs.olean" \
      "$HERE/CompactChecker/Bridge311Defs.lean" || fail "compile Bridge311Defs (see $RB/Bridge311Defs.log)"
    py lean-ok "$RB/Bridge311Defs.log" 0 || fail "Bridge311Defs log"
    py template > "$RB/src/E311/Final.lean"
    mkdir -p "$WORK/path/E311"
    LEAN_PATH="$LP" capped "$MEM" "$RB/E311.Final.log" lean -j1 -R "$RB/src" -o "$WORK/path/E311/Final.olean" \
      "$RB/src/E311/Final.lean" || fail "compile E311.Final (see $RB/E311.Final.log)"
    py lean-ok "$RB/E311.Final.log" 0 E311.balanced_excludes_63 E311.residual_excludes_32 || fail "E311.Final log"
    msg=$(py shadow "$LP" 2>&1) || refuse "LEAN_PATH after the rebuild: $msg"
  fi
fi

[ "$(sha256sum < "$FINAL_SRC" | cut -c1-64)" = "$FINAL_SRC_SHA" ] || refuse "$FINAL_SRC is not the pinned version"
if [ "$MODE" = dry ]; then say "dry run: all checks passed; nothing compiled"; exit 0; fi

# 5. The assembly, and 6. the audit.
avail=$(awk '/^MemAvailable:/ {print int($2 / 1048576)}' /proc/meminfo)
[ "$avail" -ge $((cap_gb + 8)) ] || refuse "MemAvailable ${avail} GB < cap ${cap_gb} GB + 8 GB"
OUTD=$WORK/out-olean; rm -rf "$OUTD"; mkdir -p "$OUTD"
MAINLOG=$WORK/final311-compact.main.log AUDITLOG=$WORK/final311-compact.audit.log
say "compiling Final311Compact.lean (cap $MEM)"
LEAN_PATH="$LP" capped "$MEM" "$MAINLOG" lean -j1 -R "$HERE/assembly" -o "$OUTD/Final311Compact.olean" "$FINAL_SRC"
rc=$?
say "lean exited $rc"
AUD=$WORK/audit; rm -rf "$AUD"; mkdir -p "$AUD"
cat > "$AUD/Audit311.lean" <<EOF
import Final311Compact
#check @$THEOREM
open Lean in
#eval show CoreM Unit from do
  for m in (← getEnv).header.moduleNames do
    IO.println s!"module {m}"
EOF
arc=none
if [ $rc -eq 0 ] && [ -f "$OUTD/Final311Compact.olean" ]; then
  msg=$(py shadow "$LP:$OUTD" 2>&1) || refuse "LEAN_PATH with the result: $msg"
  LEAN_PATH="$LP:$OUTD" capped "$MEM" "$AUDITLOG" lean -j1 -R "$AUD" "$AUD/Audit311.lean"
  arc=$?
  [ $arc -eq 0 ] || say "audit compile exited $arc"
else
  echo "(no audit: the main compile failed)" > "$AUDITLOG"
fi

# 7. Records.
M=real; [ "$MODE" = stub ] && M=stub; [ "$MODE" = real ] && [ -n "${A311_EXPORT:-}" ] && M=test-export
{ echo "===== Final311Compact.lean ($(date -u +%FT%TZ), cap $MEM, route $ROUTE)"; cat "$MAINLOG"
  echo "===== Audit311.lean"; grep -v '^module ' "$AUDITLOG"; echo "($(grep -c '^module ' "$AUDITLOG") module lines omitted; see the imports TSV)"
} | sed "s#$REPO#<repo>#g; s#$HOME#<home>#g" > "$LOGDIR/final311-compact.log"
py report "$MAINLOG" "$rc" "$AUDITLOG" "$arc" "$LP:$OUTD" "$LOGDIR/final311-compact.json" \
  "$LOGDIR/final311-compact-imports.tsv.gz" "$M" "$ROUTE" "$RUNJ" "$CHAINJ" "$MEM" "$FINAL_SRC" "$LAKE_LP" \
  "$OUTD/Final311Compact.olean"
v=$?
say "records: $LOGDIR/final311-compact.{log,json}, final311-compact-imports.tsv.gz"
[ $v -eq 0 ] || fail "not verified (see $LOGDIR/final311-compact.json)"
say "VERIFIED $THEOREM : ErdosSzekeres.ForcesConvexNGon 311 8 (standard axioms only)"
