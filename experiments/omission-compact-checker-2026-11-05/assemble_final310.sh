#!/bin/bash
# Last step of the compact ES(8) <= 310 check (written 6 November 2026; NOT run for real: there is no E310 build
# yet, and ES(8) <= 310 is NOT proved): compile assembly/Final310Compact.lean in ONE consistent build and record
# its axioms. A copy of assemble_final311.sh (commit 418c9f273) with the changes of the es310 design, section D,
# and of its two critiques; every reused piece cites its line in assemble_final311.sh.
#
#   assemble_final310.sh                 # the real assembly; refuses unless everything below holds
#   assemble_final310.sh --dry-run       # every check (including the shapes and coverage gates), no compile
#   assemble_final310.sh --test-stub DIR # TEST ONLY: DIR/E310/Final.olean is a stub E310.Final (no Roots);
#                                        # skips the run checks and gates; writes into DIR/out, never into logs/
#   env: A310_MEM (cap of the two final compiles, default 24G, at most 44G; MemAvailable must be >= cap + 8 GiB),
#        A310_EXTRA_ROOT (TEST ONLY, refused unless --test-stub or A310_EXPORT: one more LEAN_PATH root, to
#                         test the shadowing refusal),
#        A310_EXPORT (TEST ONLY: another E310B export directory; then nothing is written to logs/es310, only to
#                     A310_EXPORT/assemble-out),
#        A310_E311 (TEST ONLY, refused unless A310_EXPORT: another es311 export directory for the reused E311R
#                   side, e.g. a copy with a changed run.tsv)
#
# Steps (each failure stops with "refused" or "FAILED" and exit 1):
#  0. assembly/Final310Compact.lean must have the sha256 pinned below (checked first, before anything else).
#  1. Everything is finished: the campaign's log says "ALL 4096 CONTEXTS CLOSED", its unit es8-b64-campaign is
#     not active (read-only query) and there is no WITNESS file; es310-full, es310-incr and es311-full are not
#     active; no drive_es310.py / export_es310.py / merge_es310.py runs on build/es310/full, no drive_es311.py on
#     build/es311/full, and no scope of either driver is left; no ALERT-changed-inputs.txt in the export.
#     The run (check-run): build/es310/full holds exactly manifest-E310B.json, complete, at the root ([], budget
#     64, Fcat62, 3131 rows, 252 states, catalog base 4194304), and ctx/ctx-0000.json .. ctx-4095.json (each
#     context once, prefix E310B, the pinned exporter sha256 EXPORTER_SHA256 / EXPORTER311_SHA256 and one set
#     of parameters for all, K a power of 2 >= 2^17 and J = K << 12, min margin >= 1, no corrupted module;
#     refused while EXPORTER_SHA256 is empty); the manifest's chunk modules are exactly the union of the
#     context manifests' modules (same names, files, sha256 and leaves), at least 4,096 of them.
#     build/es310/full/run.tsv has, for every
#     E310B chunk, E310B.Root and E310.Final, and build/es311/full/run.tsv for the 126 E311R chunks and
#     E311R.Root, a last row with verdict ok, the manifest's (or the fixed template's) source sha256, the
#     dependency stamp that drive_es310/drive_es311.deps_stamp_of computes from the current lean_make stamps,
#     and an .olean that still has the recorded sha256. Every import was compiled before its importer started
#     (chunks before their Root, both Roots before E310.Final). E310.Final's row shows standard axioms for
#     E310.balanced_excludes_64 and E310.residual_excludes_32. drive_es310.FINAL_TEMPLATE equals design
#     section D's E310.Final outside comments (it imports E310B.Root and E311R.Root, never E311.Final).
#     If drive_es310's reuse directory build/es310/full/reuse/E311R exists, its .oleans are the checked ones.
#     Gates (only when all of the above holds): `python3 shapes_es311.py build/es310/full` PASS on exactly
#     manifest-E310B.json, and `coverage_es310.py build/es310/full --complete --exporter-sha256 <pin>` PASS
#     (exit 0, mode complete, 4,096 contexts checked, the pinned exporter), with the manifest's sha256 equal
#     at check-run, before coverage, in coverage's merged_manifest_sha256 and after it.
#  2. The chain: build/chain311/build.tsv has an ok last row for every module of build/chain311/closure.json,
#     and each .olean still has its recorded sha256 (refused after step 4, as in 311). The toolchain and
#     lake-manifest sha256 of closure.json and library.json are today's; lake's LEAN_PATH roots are
#     library.json's, and every library .olean that library.json pins still has its sha256. No .olean under
#     .lake/build/lib or .lake/packages/*/.lake/build/lib is newer than the library freeze (LAKE_FREEZE_UTC:
#     the newest was written 2026-11-04T14:45:15Z). lean_make.sh (with LM_NO_BUILD, which runs no Lean)
#     confirms that Path, Fcat62, Fcat2650 and the bridges are current.
#  3. The three catalogs that the bridges import are compared by sha256 between build/ext, build/chain311/olean
#     and the October record; route "same" is required (the 310 assembly has no "rebuilt" route). The 13
#     inputs of that route (10 CompactChecker and 3 build/ext .olean files) must have exactly the sha256 that
#     the verified 311 assembly recorded (logs/es311/final311-compact.json, chain.inputs; pinned below), and
#     must be older than the first compile of the run (the minimum over both run.tsv files).
#  4. LEAN_PATH = lake's roots : build/chain311/olean : WORK/path, where WORK/path holds symlinks to the
#     CompactChecker .oleans, the E310B chunk and Root .oleans and E310/Final.olean (build/es310/full/olean),
#     and the E311R chunk and Root .oleans (build/es311/full/olean, read only). build/ext and build/ are NOT on
#     it. A module provided by two roots stops the script.
#  5. Final310Compact.lean is copied to WORK/final-src, the COPY's sha256 is checked against the pin right
#     before the compile, and the copy is compiled (so an edit of assembly/Final310Compact.lean after step 0
#     cannot reach the compile; fixer 6 Nov, soundness review item 1; assemble_final311.sh:523 checked the pin
#     just before its compile), in one hard-capped scope (MemoryMax=A310_MEM, MemorySwapMax=0, nice 10),
#     started only when Tctl < 85 C and fewer than 2 Lean compiles run (lean processes started with --server or
#     --worker, i.e. editor and lean-lsp servers, are not counted; ops review 7). Required: scope exit 0, the .olean
#     written, "Exit status: 0" and no "Command terminated by signal", no cgroup OOM kill, no error, no sorry,
#     and exactly one axiom line in the whole log: forces_convex_octagon_310's, within {propext,
#     Classical.choice, Quot.sound}.
#  6. Audit310.lean imports the result, prints the statement (`#check`: exactly one line, exactly
#     `... : ErdosSzekeres.ForcesConvexNGon 310 8`), the axioms again (exactly one axiom line, standard) and
#     the names of all modules in its environment (same exit, signal and OOM requirements). Every module is
#     mapped to the one LEAN_PATH root that provides it and hashed; a library module pinned by library.json
#     must have its pinned sha256; no E311B module and no E311.Final may be in the environment; in real mode
#     every expected E310B/E311R/E310 module must be. The manifest and both run.tsv files must not have
#     changed since step 1. Every non-library .olean in the environment must have its recorded sha256
#     (fixer 6 Nov, soundness review item 2): E310B/E311R/E310.Final the last run.tsv row, CompactChecker the
#     13 route pins, build/chain311 its build.tsv row, Final310Compact the .olean just written (only in the
#     test modes may E310.Final, the stub, have no record). The compiled source must have the pinned sha256.
#  7. logs/es310/final310-compact.log (both Lean logs), logs/es310/final310-compact.json (verdict, checks,
#     costs, gates, catalog comparison, inputs, hashes of every non-library .olean imported, a digest of the
#     library ones) and logs/es310/final310-compact-imports.tsv.gz. "verified": true and the line "VERIFIED"
#     only in the real mode; --test-stub and A310_EXPORT runs print "TEST ONLY" and record verified false,
#     checks_passed true/false (fixer 6 Nov, soundness review item 5).
#  Script pins (fixer 6 Nov, soundness review item 6; design gate 6): MERGE_SHA256, DRIVER_SHA256 and
#  COVERAGE_SHA256 (empty until freeze_es310.sh fills them, together with EXPORTER_SHA256) and SHAPES_SHA256
#  (shapes_es311.py, a committed 311 file): check-run refuses unless merge_es310.py, drive_es310.py,
#  coverage_es310.py and shapes_es311.py have these sha256, the merged manifest's merger_sha256 is the merge
#  pin and the coverage gate's checker_sha256 is the coverage pin.
#
# Every lean or lake process runs as  systemd-run --user --scope -p MemoryMax=.. -p MemorySwapMax=0 nice -n 10 ...
set -u -o pipefail
HERE=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
FINAL_SRC=$HERE/assembly/Final310Compact.lean
# sha256 of assembly/Final310Compact.lean as written on 6 November 2026 (design section D, byte for byte);
# NOT yet committed: re-pin here to the committed file's sha256.
FINAL_SRC_SHA=7a91d397b7020867d29093bef6aaf41cf85644c9369fad0197ff0ea742416f9e
# The exporter pins (design F, gate 2, and G.3): every context manifest must record exactly these sha256 of
# export_es310.py and export_es311.py, and coverage_es310.py gets the first as --exporter-sha256.
# EXPORTER_SHA256 is EMPTY until export_es310.py is frozen before the real export; while it is empty, the run
# check refuses. EXPORTER311_SHA256 is export_es311.py as it wrote the verified 311 export (manifest-E311B.json).
EXPORTER_SHA256=29854a3799db7ebdb29311255c2a089a0f2c9957beaa2d839583d50033920b1f
EXPORTER311_SHA256=334d2d75cff1effdb4a7420501c0e3247f0dbbe645ae86bf8f8dc03887edbbfb
# The other pipeline scripts (soundness review item 6): EMPTY until freeze_es310.sh fills them with
# EXPORTER_SHA256; while one is empty, the run check refuses. shapes_es311.py is the committed 311 file.
MERGE_SHA256=3cbf428b130f6dc2a01893a8dd387d24717b97625bc713a0b801b2fa8a797940
DRIVER_SHA256=7992026f1e94a98cdd1412e8272a30b3559120ce8364ab9c943d75e6534bdd5f
COVERAGE_SHA256=fff949b9d6a0cadc49184c7c7afa35d97775b769f90a3116360dfcdf23254be5
SHAPES_SHA256=9906b781d02cf54dc1af24b501f3306261a927432cc1f2af05fbe8ae91f33837
refuse() { echo "assemble_final310: refused: $*" >&2; exit 1; }
fail() { echo "assemble_final310: FAILED: $*" >&2; exit 1; }
say() { echo "assemble_final310: $(date -u +%FT%TZ) $*" >&2; }
# 0. The pinned source, before anything else (moved up from assemble_final311.sh:523).
[ -f "$FINAL_SRC" ] && [ "$(sha256sum < "$FINAL_SRC" | cut -c1-64)" = "$FINAL_SRC_SHA" ] \
  || refuse "$FINAL_SRC is not the pinned version (sha256 $FINAL_SRC_SHA)"
REPO=$(cd "$HERE/../.." && pwd)
EXPORT=${A310_EXPORT:-$HERE/build/es310/full}
E311=${A310_E311:-$HERE/build/es311/full}
CAMPAIGN=/home/jay/research/data/es8-b64-pilot-20261105
CHAIN=$HERE/build/chain311
THEOREM=ErdosSzekeres.Omission.Compact310.forces_convex_octagon_310
MEM=${A310_MEM:-24G}
TCTL_MAX=85 LEAN_SLOTS=2
MODE=real STUB=""
case "${1:-}" in
  "") ;;
  --dry-run) MODE=dry ;;
  --test-stub) MODE=stub; STUB=$(cd "${2:?--test-stub DIR}" && pwd) ;;
  *) echo "usage: $0 [--dry-run | --test-stub DIR]" >&2; exit 2 ;;
esac
if [ "$MODE" = stub ]; then WORK=$STUB/out; LOGDIR=$STUB/out
elif [ -n "${A310_EXPORT:-}" ]; then WORK=$EXPORT/assemble-out; LOGDIR=$EXPORT/assemble-out
else WORK=$HERE/build/es310/assembly; LOGDIR=$HERE/logs/es310; fi
if [ -n "${A310_EXTRA_ROOT:-}" ] && [ "$MODE" != stub ] && [ -z "${A310_EXPORT:-}" ]; then
  refuse "A310_EXTRA_ROOT is a test switch (only with --test-stub or A310_EXPORT)"
fi
if [ -n "${A310_E311:-}" ] && [ -z "${A310_EXPORT:-}" ]; then
  refuse "A310_E311 is a test switch (only with A310_EXPORT)"
fi
capped() {  # capped CAP LOG CMD...: one scope, hard cap; LOG gets time -v and the cgroup peaks (assemble_final311.sh:81-91)
  local cap=$1 log=$2; shift 2
  (cd "$REPO" && LEAN_NUM_THREADS=1 OMP_NUM_THREADS=1 systemd-run --user --scope --quiet \
    --unit="assemble310-$(head -c5 /dev/urandom | od -An -tx1 | tr -d ' \n')" \
    -p MemoryMax="$cap" -p MemorySwapMax=0 -p CPUQuota=100% nice -n 10 \
    sh -c 'cg=/sys/fs/cgroup$(cut -d: -f3 /proc/self/cgroup); "$@"; rc=$?
      echo "cgroup memory.peak: $(cat $cg/memory.peak 2>/dev/null)"
      echo "cgroup memory.swap.peak: $(cat $cg/memory.swap.peak 2>/dev/null)"
      echo "cgroup oom_kill: $(sed -n "s/^oom_kill //p" $cg/memory.events 2>/dev/null)"; exit $rc' \
    sh /usr/bin/time -v "$@") > "$log" 2>&1
}
cool() {  # wait (at most 30 min) until Tctl < TCTL_MAX C and fewer than LEAN_SLOTS Lean compiles run
  local i t="" n=""
  for i in $(seq 180); do
    t=$(sensors 2>/dev/null | awk '/^Tctl:/ {gsub(/[^0-9.]/, "", $2); print $2; exit}')
    n=$(py lean-jobs 2>/dev/null || echo 99)  # lean processes without --server / --worker (ops review 7)
    if [ -n "$t" ] && awk -v t="$t" -v m="$TCTL_MAX" 'BEGIN { exit !(t < m) }' && [ "$n" -lt "$LEAN_SLOTS" ]; then
      return 0
    fi
    [ "$i" -eq 1 ] && say "waiting: Tctl ${t:-unknown} C, $n lean processes (need < $TCTL_MAX C and < $LEAN_SLOTS)"
    sleep 10
  done
  refuse "for 30 min: Tctl ${t:-unknown} C, $n lean processes (need Tctl < $TCTL_MAX C and < $LEAN_SLOTS lean)"
}
cap_gb=$(echo "$MEM" | sed -n 's/^\([0-9]\+\)G$/\1/p')
[ -n "$cap_gb" ] && [ "$cap_gb" -le 44 ] || refuse "A310_MEM must be <N>G with N <= 44 (got $MEM)"

# The Python helper (run with -I; reads only, except where it writes WORK/path and the outputs).
read -r -d '' PY <<'PYEOF'
import gzip, hashlib, json, os, re, subprocess, sys, datetime
from pathlib import Path
cmd, HERE = sys.argv[1], Path(sys.argv[2])
REPO, CHAIN = HERE.parent.parent, HERE / "build/chain311"
EXPORT = Path(os.environ.get("A310_EXPORT") or HERE / "build/es310/full")
E311 = Path(os.environ.get("A310_E311") or HERE / "build/es311/full")
ALLOWED = {"propext", "Classical.choice", "Quot.sound"}
CATS = ["BalancedProof.Catalog", "BalancedCoverCutsV2", "Residual32Bridge2650.Catalog"]
STAMPED = ["Bridge311Bal", "Bridge311Res", "Fcat2650", "Fcat62", "Path"]  # drive_es310.prepare's final set
THM = "ErdosSzekeres.Omission.Compact310.forces_convex_octagon_310"
STATEMENT = "ErdosSzekeres.ForcesConvexNGon 310 8"
PREFIX, NCTX, E311R_CHUNKS = "E310B", 4096, 126
# Set by the bash part from its constants: export_es310, export_es311, merge_es310, drive_es310, coverage_es310,
# shapes_es311 (the last four: soundness review item 6).
PIN310, PIN311, PINMERGE, PINDRIVER, PINCOV, PINSHAPES = (os.environ.get("A310_PINS", "") + ":" * 6).split(":")[:6]
FINAL_PIN = os.environ.get("A310_FINAL_PIN", "")  # sha256 of assembly/Final310Compact.lean (FINAL_SRC_SHA)
FINAL_THMS = ("E310.balanced_excludes_64", "E310.residual_excludes_32")
# The 13 inputs of route "same", as the verified 311 assembly recorded them (logs/es311/final311-compact.json,
# chain.inputs, 2026-11-06T01:15Z): required by sha256, not only by mtime.
PINNED_INPUTS = {
    "CompactChecker/Bridge311Bal": "08e7fc1b807459a82408fd6bcd810d87757c48958db7e80f53056b598871c4b7",
    "CompactChecker/Bridge311Res": "21dc7075517ff3cf6ba468a93bfdf718fd66986a41b906c6e775547825f84d71",
    "CompactChecker/Fast": "1e55d4aa6a683f34148ec7b1e4ef9f8c1da0186059aac21185ef426ef98dfe35",
    "CompactChecker/Fast2": "14ce7ba1c6515c419fc3a1a2ad12946f606076df83595679b9eb0132bda8e51e",
    "CompactChecker/Fcat2650": "2b6c9f27f46837077b0bf390daba860c03d330cb84f145e6d091201787acde2c",
    "CompactChecker/Fcat62": "a532a3ce3968a5f96c5254fb741749aebf59c6fa8c76dc2122d5629e36fa55b0",
    "CompactChecker/Packed": "d0186d8387cd9e924511fb588a03d6d6d1e2b2c19c1dd06f533151ba523a7cd9",
    "CompactChecker/Path": "c0e64d18168c9f9fa2bf8bd01ffeb7967e92e80ca815f67804aa2d9cfaec4fd1",
    "CompactChecker/Split": "9d6e752b82da2425f9bde5ca7e27b5a8efddb49ea109df6f780078121668e8e9",
    "CompactChecker/WordPack": "bbd6dbe5ab9ae50e449d48c49dc2b929aadca1a3481d2d718de68ad9bed2552f",
    "ext/BalancedProof/Catalog": "d650caa857c8351dfd842004c11dedd326433a84e219f630211e980a21251c64",
    "ext/BalancedCoverCutsV2": "6f7f0ba1fa02149418c24b2d137341a2b556440352d2de7e6dd740b8fd9b0aa0",
    "ext/Residual32Bridge2650/Catalog": "4fe35a09c81e5c1ed530d3f2b7daa7ec93f65ecca286d2beab66fc6feb369df8",
}
# No library .olean may be written at or after this time (the newest under .lake/build/lib was written
# 2026-11-04T14:45:15Z, under .lake/packages 2026-11-04T14:40:30Z; checked 6 November 2026).
LAKE_FREEZE_UTC = "2026-11-04T14:46:00Z"
# Design section D's src/E310/Final.lean. drive_es310.FINAL_TEMPLATE must equal it outside comments.
DESIGN_FINAL = """import E310B.Root
import E311R.Root
import CompactChecker.Bridge311Bal
import CompactChecker.Bridge311Res
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

def driver(name):
    sys.path.insert(0, str(HERE))
    try:
        return __import__(name)
    except ImportError as e:
        sys.exit(f"cannot import {name} from {HERE}: {e}")

def code_lines(s):
    """The non-blank lines of a Lean text without its comments (nested /- -/ blocks and -- lines); a string
    literal is refused. Used to compare the driver's E310.Final template with design section D."""
    out, i, depth, n = [], 0, 0, len(s)
    while i < n:
        if depth:
            if s.startswith("/-", i):
                depth, i = depth + 1, i + 2
            elif s.startswith("-/", i):
                depth, i = depth - 1, i + 2
            else:
                i += 1
        elif s.startswith("/-", i):
            depth, i = 1, i + 2
        elif s.startswith("--", i):
            j = s.find("\n", i)
            i = n if j < 0 else j
        elif s[i] == '"':
            raise ValueError("a string literal")
        else:
            out.append(s[i]); i += 1
    if depth:
        raise ValueError("an unterminated comment")
    return [l.rstrip() for l in "".join(out).splitlines() if l.strip()]

def template_errors(t):
    try:
        got, want = code_lines(t), code_lines(DESIGN_FINAL)
    except ValueError as e:
        return [str(e)]
    if got != want:
        d = next((i for i, (a, b) in enumerate(zip(got, want)) if a != b), min(len(got), len(want)))
        return [f"differs from design section D outside comments at code line {d + 1}: "
                f"{got[d] if d < len(got) else '<end>'!r} vs {want[d] if d < len(want) else '<end>'!r}"]
    return []

def template():
    """drive_es310.FINAL_TEMPLATE, which must be design section D's E310.Final outside comments."""
    t = driver("drive_es310").FINAL_TEMPLATE
    errs = template_errors(t)
    if errs:
        sys.exit("drive_es310.FINAL_TEMPLATE: " + "; ".join(errs))
    return t

def last_rows(tsv):
    lines = Path(tsv).read_text().splitlines()
    cols = lines[0].split("\t")
    last = {}
    for line in lines[1:]:
        row = dict(zip(cols, line.split("\t")))
        last[row["module"]] = row
    return last

def axioms_of(row):
    return {k: {a.strip() for a in v.split(",") if a.strip()}
            for k, v in re.findall(r"([A-Za-z0-9_.]+)=\[([^\]]*)\]", row.get("axioms", ""))}

def contexts():
    """The 4,096 context manifests (written last by export_es310.py): checks and their union of modules."""
    files = sorted((EXPORT / "ctx").glob("ctx-*.json"))
    names = [f.name for f in files]
    want = [f"ctx-{k:04d}.json" for k in range(NCTX)]
    if names != want:
        miss, extra = sorted(set(want) - set(names)), sorted(set(names) - set(want))
        sys.exit(f"ctx/: {len(names)} context manifests, not ctx-0000..ctx-{NCTX - 1:04d}.json "
                 f"(missing {len(miss)}, e.g. {miss[:3]}; unexpected {extra[:3]})")
    if not re.fullmatch(r"[0-9a-f]{64}", PIN310) or not re.fullmatch(r"[0-9a-f]{64}", PIN311):
        sys.exit("the exporter sha256 pins are not set in assemble_final310.sh (EXPORTER_SHA256 is filled in when "
                 "export_es310.py is frozen, design G.3)")
    mods, exporters, params, leaves, probs = [], set(), set(), 0, []
    for k, f in enumerate(files):
        c = json.loads(f.read_text())
        p = c.get("params") or {}
        ex = c.get("exporter_sha256")
        if c.get("ctx") != k or c.get("prefix") != PREFIX:
            probs.append(f"{f.name}: ctx {c.get('ctx')!r}, prefix {c.get('prefix')!r}")
        if not isinstance(ex, dict) or ex.get("export_es310") != PIN310 or ex.get("export_es311") != PIN311:
            probs.append(f"{f.name}: exporter sha256 {ex!r} is not the pinned export_es310 {PIN310[:12]} / "
                         f"export_es311 {PIN311[:12]}")
        exporters.add(json.dumps(ex, sort_keys=True))
        K, J = p.get("K"), p.get("J")
        if p.get("budget") != 64 or p.get("catalog_base") != 4194304 or not isinstance(K, int) or K < 2 ** 17 \
                or K & (K - 1) or J != K << 12:
            probs.append(f"{f.name}: params {p}")
        params.add(json.dumps({x: p.get(x) for x in ("budget", "per_word", "chunk_leaves", "block_leaves",
                                                     "catalog_base")}, sort_keys=True))
        st = c.get("stats") or {}
        if not isinstance(st.get("min_margin"), int) or st["min_margin"] < 1:
            probs.append(f"{f.name}: min margin {st.get('min_margin')!r}")
        leaves += st.get("leaves") or 0
        cm = c.get("modules") or []
        if not cm:
            probs.append(f"{f.name}: no modules")
        for j, m in enumerate(cm, 1):
            name = f"{PREFIX}.C{k:04d}{j:02d}"
            if m.get("module") != name or m.get("file") != f"src/{PREFIX}/C{k:04d}{j:02d}.lean" or m.get("corrupted") \
                    or not isinstance(m.get("min_margin"), int) or m["min_margin"] < 1:
                probs.append(f"{f.name}: module {j} is {m.get('module')!r} ({m.get('file')!r}, corrupted "
                             f"{m.get('corrupted')!r}, min margin {m.get('min_margin')!r}), expected {name}")
            mods.append((m.get("module"), m.get("file"), m.get("sha256"), m.get("leaves")))
    if len(exporters) != 1:
        probs.append(f"{len(exporters)} different exporter sha256 records among the context manifests")
    if len(params) != 1:
        probs.append(f"{len(params)} different parameter sets among the context manifests")
    if probs:
        sys.exit(f"ctx/: {len(probs)} problems, e.g. {probs[:4]}")
    return mods, leaves, json.loads(exporters.pop()), json.loads(params.pop())

def script_pins():
    """The four pipeline scripts must have their pinned sha256 (soundness review item 6). {name: sha256}."""
    pins = {"merge_es310.py": PINMERGE, "drive_es310.py": PINDRIVER, "coverage_es310.py": PINCOV,
            "shapes_es311.py": PINSHAPES}
    unset = [n for n, p in pins.items() if not re.fullmatch(r"[0-9a-f]{64}", p)]
    if unset:
        sys.exit(f"the script sha256 pins are not set in assemble_final310.sh for {unset} (freeze_es310.sh fills "
                 "them when the pipeline is frozen)")
    now = {n: sha(HERE / n) for n in pins}
    off = [f"{n} ({now[n][:12]}, pinned {p[:12]})" for n, p in pins.items() if now[n] != p]
    if off:
        sys.exit(f"pipeline scripts differ from their pins: {off}")
    return now

def expected_run():
    """[(export, phase, module, source sha256, catalog)] of the full run: the E310B chunks, E310B.Root, the 126
    E311R chunks and E311R.Root (reused from build/es311/full), and E310.Final; plus a summary."""
    scripts = script_pins()
    mfs = sorted(p.name for p in EXPORT.glob("manifest-*.json"))
    if mfs != ["manifest-E310B.json"]:
        sys.exit(f"{EXPORT} must hold exactly manifest-E310B.json (found {mfs})")
    d = json.loads((EXPORT / "manifest-E310B.json").read_text())
    want = {"side": "balanced", "prefix": PREFIX, "catalog": "CompactChecker.Fcat62", "rows": 3131, "states": 252,
            "budget": 64, "catalog_base": 4194304, "complete": True, "export_root": 0, "base_path": []}
    bad = [f"{k}={d.get(k)!r} (not {v!r})" for k, v in want.items() if d.get(k) != v]
    root = d.get("root") or {}
    if root.get("module") != "E310B.Root" or root.get("file") != "src/E310B/Root.lean":
        bad.append(f"root {root!r}")
    if any(m.get("corrupted") for m in d["modules"]):
        bad.append("a corrupted test module")
    if d.get("merger_sha256") != PINMERGE:
        bad.append(f"merger_sha256 {str(d.get('merger_sha256'))[:12]} is not the pinned merge_es310.py {PINMERGE[:12]}")
    if bad:
        sys.exit("manifest-E310B.json: " + "; ".join(bad))
    ch = [m for m in d["modules"] if m["file"] is not None]
    cmods, cleaves, exporter, params = contexts()
    mine = sorted((m["module"], m["file"], m["sha256"], m["leaves"]) for m in ch)
    if len(ch) < NCTX or len(ch) != len(cmods) or mine != sorted(cmods) or len(set(mine)) != len(mine):
        sys.exit(f"manifest-E310B.json has {len(ch)} chunk modules; the context manifests list {len(cmods)}; "
                 f"they must be the same modules (names, files, sha256, leaves), at least {NCTX}")
    total = sum(m["leaves"] for m in ch)
    if d.get("total_leaves") != total or cleaves != total:
        sys.exit(f"leaves: manifest total {d.get('total_leaves')}, its modules {total}, context stats {cleaves}")
    out = [("es310", "chunk", m["module"], m["sha256"], "Fcat62") for m in ch]
    out.append(("es310", "root", "E310B.Root", root["sha256"], "Fcat62"))
    r = json.loads((E311 / "manifest-E311R.json").read_text())
    if not (r["complete"] and r["prefix"] == "E311R" and r["catalog"] == "CompactChecker.Fcat2650"
            and r["budget"] == 32 and r["export_root"] == 1 and r["base_path"] == [[0, 2]]
            and (r.get("root") or {}).get("module") == "E311R.Root"):
        sys.exit("manifest-E311R.json is not the complete residual export at [(0, 2)], budget 32")
    rch = [m for m in r["modules"] if m["file"] is not None]
    if len(rch) != E311R_CHUNKS or any(m.get("corrupted") for m in r["modules"]):
        sys.exit(f"manifest-E311R.json has {len(rch)} chunk modules, expected {E311R_CHUNKS}")
    out += [("es311", "chunk", m["module"], m["sha256"], "Fcat2650") for m in rch]
    out.append(("es311", "root", "E311R.Root", r["root"]["sha256"], "Fcat2650"))
    out.append(("es310", "final", "E310.Final", hashlib.sha256(template().encode()).hexdigest(), None))
    return out, {"chunks_e310b": len(ch), "leaves_e310b": total, "exporter": exporter, "params": params,
                 "scripts": scripts}

def current_stamps():
    return {n: (HERE / "build/CompactChecker" / f"{n}.stamp").read_text().strip() for n in STAMPED}

def export_of(where):
    return EXPORT if where == "es310" else E311

def check_run():
    exp, summ = expected_run()
    n = len(exp)
    tsvs = {w: export_of(w) / "run.tsv" for w in ("es310", "es311")}
    for w, t in tsvs.items():
        if not t.exists():
            sys.exit(f"no {t}")
    last = {w: last_rows(t) for w, t in tsvs.items()}
    st = current_stamps()
    drv = {"es310": driver("drive_es310"), "es311": driver("drive_es311")}
    bad, starts, span = [], [], {}
    for where, phase, m, s, cat in exp:
        r = last[where].get(m)
        if r is None:
            bad.append(f"{m}: no row in {where} run.tsv"); continue
        if r["verdict"] != "ok":
            bad.append(f"{m}: last verdict {r['verdict']}"); continue
        if r["src_sha256"] != s:
            bad.append(f"{m}: source sha256 {r['src_sha256'][:12]} is not {s[:12]}"); continue
        if r["deps_stamp"] != drv[where].deps_stamp_of(phase, cat, st):
            bad.append(f"{m}: dependency stamp {r['deps_stamp'][:12]} is not the current one"); continue
        o = export_of(where) / "olean" / mpath(m)
        if not o.is_file() or sha(o) != r["olean_sha256"]:
            bad.append(f"{m}: .olean missing or changed since its row"); continue
        end = parse_iso(r["utc"])  # utc is written when the compile ends
        span[m] = (end - float(r["wall_s"]), end)
        starts.append(span[m][0])
    if bad:
        sys.exit(f"{len(bad)} of {n} modules are not ok, e.g. {bad[:4]}")
    # Every import compiled before its importer started (2 s for the whole-second utc column).
    order = [(m, "E310B.Root") for w, ph, m, _, _ in exp if w == "es310" and ph == "chunk"]
    order += [(m, "E311R.Root") for w, ph, m, _, _ in exp if w == "es311" and ph == "chunk"]
    order += [("E310B.Root", "E310.Final"), ("E311R.Root", "E310.Final")]
    late = [f"{a} ended {iso(span[a][1])}, after {b} started {iso(span[b][0])}" for a, b in order
            if span[a][1] > span[b][0] + 2]
    if late:
        sys.exit(f"{len(late)} modules were compiled after a module that imports them, e.g. {late[:3]}")
    for m in ("E310B.Root", "E311R.Root"):
        w = "es310" if m.startswith("E310") else "es311"
        ax = axioms_of(last[w][m])
        if f"{m.split('.')[0]}.root" not in ax or not ax[f"{m.split('.')[0]}.root"] <= ALLOWED:
            sys.exit(f"{m} row does not show standard axioms for {m.split('.')[0]}.root")
    fr = last["es310"]["E310.Final"]
    ax = axioms_of(fr)
    for t in FINAL_THMS:
        if t not in ax or not ax[t] <= ALLOWED:
            sys.exit(f"E310.Final row does not show standard axioms for {t}")
    stray = [str(p) for p in (EXPORT / "olean").rglob("*.tmp*.olean")]
    stray += [str(p) for p in (E311 / "olean" / "E311R").rglob("*.tmp*.olean")]
    if stray:
        sys.exit(f"stray temporary .olean files in the exports: {stray[:3]}")
    # drive_es310's reuse directory (if any) must hold the very E311R .oleans checked above.
    reuse = EXPORT / "reuse" / "E311R"
    if reuse.exists():
        rows = {m: last["es311"][m]["olean_sha256"] for w, _, m, _, _ in exp if w == "es311"}
        off = [p.name for p in reuse.glob("*.olean")
               if rows.get("E311R." + p.stem) is None or sha(p) != rows["E311R." + p.stem]]
        if off:
            sys.exit(f"{reuse}: {len(off)} .olean files are not the checked E311R ones, e.g. {off[:3]}")
    print(json.dumps({"modules_in_es310_tsv": len(last["es310"]), "modules_ok": n, "deps_stamps_ok": n,
                      "chunks_e310b": summ["chunks_e310b"], "leaves_e310b": summ["leaves_e310b"],
                      "contexts": NCTX, "exporter": summ["exporter"], "params": summ["params"],
                      "scripts": summ["scripts"],
                      "e311r_modules_ok": E311R_CHUNKS + 1, "import_order_ok": len(order),
                      "first_compile_start_utc": iso(min(starts) - 1),
                      "final_row_utc": fr["utc"], "final_olean_sha256": fr["olean_sha256"],
                      "final_deps_stamp": fr["deps_stamp"],
                      "manifest_sha256": sha(EXPORT / "manifest-E310B.json"),
                      "run_tsv_sha256": sha(tsvs["es310"]), "e311_run_tsv_sha256": sha(tsvs["es311"]),
                      "e311r_manifest_sha256": sha(E311 / "manifest-E311R.json")}))

def gates(shapes_out, cov_out, cov_rc, msha_before, runj):
    """The shapes and coverage gates (their outputs were written by the bash part)."""
    probs = []
    try:
        s = json.loads(Path(shapes_out).read_text())
    except (OSError, ValueError) as e:
        s = {}
        probs.append(f"shapes_es311.py output is not JSON ({e})")
    if s.get("PASS") is not True or list(s.get("manifests", {})) != ["manifest-E310B.json"]:
        probs.append(f"shapes_es311.py did not PASS on exactly manifest-E310B.json: "
                     f"{ {k: v for k, v in s.items() if k != 'manifests'} } {list(s.get('manifests', {}))}")
    try:
        c = json.loads(Path(cov_out).read_text())
    except (OSError, ValueError) as e:
        c = {}
        probs.append(f"coverage_es310.py output is not JSON ({e})")
    if c.get("checker_sha256") != PINCOV:
        probs.append(f"coverage_es310.py checker_sha256 {str(c.get('checker_sha256'))[:12]} is not the pin {PINCOV[:12]}")
    if cov_rc != "0" or c.get("PASS") is not True or c.get("mode") != "complete" \
            or c.get("contexts_checked") != NCTX or (c.get("exporter_sha256") or {}).get("export_es310") != PIN310:
        probs.append(f"coverage_es310.py --complete did not PASS on all {NCTX} contexts with the pinned exporter "
                     f"(exit {cov_rc}, PASS {c.get('PASS')!r}, mode {c.get('mode')!r}, contexts "
                     f"{c.get('contexts_checked')!r}, exporter {c.get('exporter_sha256')!r})")
    now = sha(EXPORT / "manifest-E310B.json")
    want = json.loads(runj)["manifest_sha256"]
    if not (msha_before == now == want == c.get("merged_manifest_sha256")):
        probs.append(f"manifest-E310B.json sha256: check-run {want[:12]}, before coverage {msha_before[:12]}, "
                     f"checked by coverage {str(c.get('merged_manifest_sha256'))[:12]}, now {now[:12]}")
    if probs:
        sys.exit("gates: " + "; ".join(probs))
    print(json.dumps({"shapes_es311": {"PASS": True, "files": s["manifests"]["manifest-E310B.json"].get("files")},
                      "coverage_es310": {"PASS": True, "mode": "complete", "merged_manifest_sha256": now,
                                         "contexts_checked": c.get("contexts_checked"), "leaves": c.get("leaves"),
                                         "checker_sha256": c.get("checker_sha256"),
                                         "contexts_sha256": c.get("contexts_sha256"),
                                         "exporter_sha256": c.get("exporter_sha256")}}))

def cc_closure(start):
    """CompactChecker modules needed by `start` (from the source import lines; assemble_final311.sh:200-212)."""
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

def check_lake(roots=None):
    """No library .olean (repository and packages) written at or after LAKE_FREEZE_UTC."""
    roots = roots or [REPO / ".lake/build/lib"] + sorted(REPO.glob(".lake/packages/*/.lake/build/lib"))
    freeze, n, newest, newer = parse_iso(LAKE_FREEZE_UTC), 0, 0.0, []
    for r in roots:
        for dp, _, fs in os.walk(r):
            for fn in fs:
                if fn.endswith(".olean"):
                    t = os.stat(os.path.join(dp, fn)).st_mtime
                    n, newest = n + 1, max(newest, t)
                    if t >= freeze:
                        newer.append(os.path.relpath(os.path.join(dp, fn), REPO))
    if newer or n == 0:
        sys.exit(f"library freeze: {len(newer)} of {n} library .olean files are newer than {LAKE_FREEZE_UTC} "
                 f"(a lake build since?), e.g. {newer[:3]}")
    return {"lake_oleans_checked": n, "lake_newest_utc": iso(newest), "lake_freeze_utc": LAKE_FREEZE_UTC}

def check_library(lake_roots):
    """library.json: toolchain, manifest, lake's roots and every pinned library .olean (assemble_final311.sh:214-237)."""
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
    """Completeness of build/chain311 (reported, refused later), the library and its freeze, the catalogs (route
    "same" required) and the 13 pinned inputs of that route (assemble_final311.sh:239-295)."""
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
    lakej = check_lake()
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
    if route != "same":
        sys.exit(f"route {route}: the catalogs differ between build/ext, build/chain311 and the October record "
                 f"({ {k: (v['identical'], v['chain311_is_october']) for k, v in cats.items()} }); the 310 "
                 "assembly uses only route same (the existing bridges and the 13 pinned inputs)")
    used = [f"CompactChecker/{m}" for m in cc_closure(["Path", "Fcat62", "Fcat2650", "Bridge311Bal",
                                                         "Bridge311Res"])] + [f"ext/{mpath(m)}"[:-6] for m in CATS]
    hard = {}
    hc = HERE / "logs/es311/hardcap-rebuild.tsv"
    if hc.exists():
        for row in last_rows(hc).values():
            if re.fullmatch(r"[0-9a-f]{64}", row.get("olean_sha256", "")):
                hard[row["module"]] = row["olean_sha256"]
    inputs, newer, off = {}, [], []
    for u in used:
        f = HERE / "build" / (u + ".olean")
        if not f.is_file():
            sys.exit(f"input build/{u}.olean is missing")
        mod = u.split("/", 1)[1].replace("/", ".")
        inputs[u] = {"sha256": sha(f), "mtime_utc": iso(f.stat().st_mtime)}
        if mod in hard:
            inputs[u]["equals_hardcap_record"] = inputs[u]["sha256"] == hard[mod]
        if PINNED_INPUTS.get(u) != inputs[u]["sha256"]:
            off.append(f"{u} ({inputs[u]['sha256'][:12]}, pinned {(PINNED_INPUTS.get(u) or 'none')[:12]})")
        if run_start and f.stat().st_mtime >= parse_iso(run_start):
            newer.append(u)
    off += [f"{u} (pinned, not an input of the route)" for u in sorted(set(PINNED_INPUTS) - set(inputs))]
    if off:
        sys.exit(f"route same: {len(off)} inputs differ from the 13 sha256 the verified 311 assembly recorded: {off}")
    if newer:
        sys.exit(f"route same: {newer} changed after the run's first compile ({run_start}); the run was not "
                 "compiled against them")
    print(json.dumps({"modules": len(clo["order"]), "complete": not bad, "not_ok": bad,
                      "closure_sha256": sha(CHAIN / "closure.json"),
                      "olean_equal_to_recorded": match, **libj, **lakej, "catalogs": cats,
                      "catalogs_identical": all(c["identical"] for c in cats.values()),
                      "route": route, "inputs_equal_to_311_pins": len(inputs),
                      "run_first_compile_utc": run_start or None,
                      "inputs_older_than_run": bool(run_start), "inputs": inputs}))

def make_path(work, stub):
    """WORK/path: symlinks to the CompactChecker closure, and to the E310B, E311R and E310.Final .oleans
    (assemble_final311.sh:297-320)."""
    import shutil
    p = Path(work) / "path"
    if p.exists():
        shutil.rmtree(p)
    for m in cc_closure(["Path", "Fcat62", "Fcat2650", "Bridge311Bal", "Bridge311Res"]):
        t = p / "CompactChecker" / f"{m}.olean"
        t.parent.mkdir(parents=True, exist_ok=True)
        t.symlink_to(HERE / "build/CompactChecker" / f"{m}.olean")
    if stub:
        t = p / "E310/Final.olean"
        t.parent.mkdir(parents=True, exist_ok=True)
        t.symlink_to(Path(stub) / "E310/Final.olean")
        return
    exp, _ = expected_run()
    for where, _, m, _, _ in exp:
        t = p / mpath(m)
        t.parent.mkdir(parents=True, exist_ok=True)
        t.symlink_to(export_of(where) / "olean" / mpath(m))

def shadow(roots):
    """Refuse when a module is provided by two LEAN_PATH roots, or build/ext or build/ is a root
    (assemble_final311.sh:322-342)."""
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

AXLINE = re.compile(r"^'(.+?)' (?:depends on axioms: \[([^\]]*)\]|does not depend on any axioms)", re.M)

def lean_ok(log, rc, expect, olean=None):
    """Scope exit rc 0, "Exit status: 0" and no "Command terminated by signal", no cgroup OOM kill, the .olean
    (if given) written, no error, no sorry; the log's axiom lines are exactly one for each name in `expect`
    and no others, each with standard axioms (assemble_final311.sh:344-375, made exclusive)."""
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
    pairs = [(k, re.sub(r"\s+", " ", v or "").strip()) for k, v in AXLINE.findall(t)]
    if len(pairs) != len(expect):
        errs.append(f"{len(pairs)} axiom lines in the log, expected exactly {len(expect)}: {[k for k, _ in pairs][:4]}")
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

def lean_jobs():
    """Running lean processes that are not editor / lean-lsp servers (no --server or --worker argument)."""
    n = 0
    for p in os.listdir("/proc"):
        if not p.isdigit():
            continue
        try:
            if open(f"/proc/{p}/comm").read().strip() != "lean":
                continue
            argv = open(f"/proc/{p}/cmdline", "rb").read().split(b"\0")
        except OSError:
            continue
        if not any(a in (b"--server", b"--worker") for a in argv):
            n += 1
    return n

if cmd == "check-run":
    check_run()
elif cmd == "lean-jobs":
    print(lean_jobs())
elif cmd == "check-chain":
    check_chain(sys.argv[3], sys.argv[4] if len(sys.argv) > 4 else "")
elif cmd == "cc-closure":
    print(" ".join(cc_closure(sys.argv[3:])))
elif cmd == "check-lake":  # check-lake [ROOT...] (default: the repository's and the packages' build/lib)
    print(json.dumps(check_lake([Path(r) for r in sys.argv[3:]] or None)))
elif cmd == "gates":
    gates(*sys.argv[3:8])
elif cmd == "template":
    sys.stdout.write(template())
elif cmd == "design-template":
    sys.stdout.write(DESIGN_FINAL)
elif cmd == "template-errors":  # template-errors FILE
    e = template_errors(Path(sys.argv[3]).read_text())
    print("; ".join(e) or "ok")
    sys.exit(1 if e else 0)
elif cmd == "make-path":
    make_path(sys.argv[3], sys.argv[4] if len(sys.argv) > 4 else "")
elif cmd == "shadow":
    shadow(sys.argv[3].split(":"))
elif cmd == "report":
    # report MAINLOG MAINRC AUDITLOG AUDITRC LEAN_PATH OUTJSON OUTTSVGZ MODE ROUTE RUNJSON CHAINJSON MEM SRC LAKE_LP
    #        OLEAN GATESJSON
    (mainlog, mainrc, auditlog, auditrc, lp, outj, outt, mode, route, runj, chainj, mem, src, lake_lp,
     olean, gatesj) = sys.argv[3:19]
    errs, axioms = lean_ok(mainlog, mainrc, [THM], olean)
    at = Path(auditlog).read_text(errors="replace")
    aerrs, aaxioms = lean_ok(auditlog, auditrc, [THM])
    errs += ["audit: " + e for e in aerrs]
    stmts = re.findall(r"^@?" + re.escape(THM) + r" : (.*)$", at, re.M)  # `#check @c` may print the @
    if len(stmts) != 1 or stmts[0].strip() != STATEMENT:
        errs.append(f"statement is not exactly {STATEMENT} ({len(stmts)} statement lines: {stmts[:2]})")
    mods = re.findall(r"^module (\S+)$", at, re.M)
    if "Final310Compact" not in mods or len(mods) < 1000:
        errs.append(f"audit listed {len(mods)} modules")
    forbidden = [m for m in mods if m.startswith("E311B.") or m in ("E311.Final", "E311B")]
    if forbidden:
        errs.append(f"{len(forbidden)} E311B / E311.Final modules are in the environment, e.g. {forbidden[:3]}")
    if runj:  # real (or test-export) mode: every expected module is imported; nothing changed since step 1
        exp, _ = expected_run()
        miss = sorted({m for _, _, m, _, _ in exp} - set(mods))
        if miss:
            errs.append(f"{len(miss)} expected modules are not in the environment, e.g. {miss[:3]}")
        rj = json.loads(runj)
        for key, f in (("manifest_sha256", EXPORT / "manifest-E310B.json"), ("run_tsv_sha256", EXPORT / "run.tsv"),
                       ("e311_run_tsv_sha256", E311 / "run.tsv"), ("e311r_manifest_sha256", E311 / "manifest-E311R.json")):
            if sha(f) != rj[key]:
                errs.append(f"{f} changed since the run check")
    roots = [r for r in lp.split(":") if r]
    lib_roots = [r for r in lake_lp.split(":") if r]
    rows, missing = [], []
    for m in sorted(set(mods)):
        hits = [r for r in roots if (Path(r) / mpath(m)).is_file()]
        if len(hits) != 1:
            missing.append(m); continue
        f = Path(hits[0]) / mpath(m)
        kind = "library" if hits[0] in lib_roots else ("chain311" if hits[0].endswith("chain311/olean") else
               ("result" if m == "Final310Compact" else "path"))
        rows.append((m, kind, hits[0], str(f.resolve()), sha(f)))
    if missing:
        errs.append(f"{len(missing)} imported modules not found exactly once on LEAN_PATH, e.g. {missing[:3]}")
    pinned = json.loads((CHAIN / "library.json").read_text())["modules"]
    off = [m for m, k, _, _, s in rows if k == "library" and m in pinned and pinned[m][1] != s]
    if off:
        errs.append(f"{len(off)} imported library modules differ from library.json, e.g. {off[:3]}")
    # Every non-library .olean against its record (soundness review item 2).
    rec = {"CompactChecker." + u.split("/", 1)[1].replace("/", "."): h for u, h in PINNED_INPUTS.items()
           if u.startswith("CompactChecker/")}
    chain_rec = {m: r["olean_sha256"] for m, r in last_rows(CHAIN / "build.tsv").items() if r["verdict"] == "ok"}
    if runj:
        for t in (EXPORT / "run.tsv", E311 / "run.tsv"):
            for m, r in last_rows(t).items():
                if r["verdict"] == "ok" and (m.startswith(("E310B.", "E311R.")) or m == "E310.Final"):
                    rec[m] = r["olean_sha256"]
    unrec, diff_ = [], []
    for m, k, _, _, s in rows:
        if k == "library":
            continue
        want = (sha(olean) if m == "Final310Compact" and Path(olean).is_file() else None) if k == "result" else \
            chain_rec.get(m) if k == "chain311" else rec.get(m)
        if want is None:
            if not runj and m == "E310.Final":   # test modes: the stub E310.Final has no record
                continue
            unrec.append(f"{m} ({k})")
        elif want != s:
            diff_.append(f"{m} ({k}: {s[:12]}, recorded {want[:12]})")
    if unrec:
        errs.append(f"{len(unrec)} non-library .olean files have no recorded sha256, e.g. {unrec[:3]}")
    if diff_:
        errs.append(f"{len(diff_)} non-library .olean files differ from their records, e.g. {diff_[:3]}")
    if not re.fullmatch(r"[0-9a-f]{64}", FINAL_PIN) or sha(src) != FINAL_PIN:
        errs.append(f"the compiled source {src} (sha256 {sha(src)[:12]}) is not the pinned Final310Compact.lean "
                    f"({FINAL_PIN[:12] or 'no pin given'})")
    def anon(s):
        return s.replace(str(REPO), "<repo>").replace(str(Path.home()), "<home>")
    with gzip.open(outt, "wt") as f:
        f.write("module\tkind\troot\tfile\tsha256\n")
        for r in rows:
            f.write("\t".join(anon(x) for x in r) + "\n")
    lib = [r for r in rows if r[1] == "library"]
    digest = hashlib.sha256("".join(f"{m}\t{s}\n" for m, _, _, _, s in lib).encode()).hexdigest()
    top = {m: s for m, _, _, _, s in rows if m in ("BalancedBudgets", "Residual32Bridge2650.Rows", "E310.Final",
                                                    "CompactChecker.Bridge311Bal", "CompactChecker.Bridge311Res",
                                                    "E310B.Root", "E311R.Root", "Final310Compact")}
    rep = {"verified": not errs and mode == "real", "checks_passed": not errs, "test_only": mode != "real",
           "mode": mode, "route": route, "problems": errs,
           "theorem": THM, "statement": f"{THM} : {stmts[0].strip()}" if len(stmts) == 1 else None,
           "axioms": axioms.get(THM), "audit_axioms": aaxioms.get(THM),
           "final_source": anon(src), "final_source_sha256": sha(src), "final_source_pin": FINAL_PIN,
           "cap": mem, "main_compile": {"scope_exit": mainrc, **costs(mainlog)},
           "audit_compile": {"scope_exit": auditrc, **costs(auditlog)},
           "lean_path_roots": [anon(r) for r in roots], "run": json.loads(runj) if runj else None,
           "gates": json.loads(gatesj) if gatesj else None,
           "chain": json.loads(chainj), "top_level_oleans": top,
           "imported_modules": len(rows), "library_modules": len(lib), "library_digest_sha256": digest,
           "library_modules_checked_against_library_json": sum(1 for m, k, _, _, _ in rows if k == "library" and m in pinned),
           "non_library_oleans": {m: {"kind": k, "sha256": s} for m, k, _, _, s in rows if k != "library"},
           "imports_tsv": anon(outt), "imports_tsv_sha256": sha(outt)}
    Path(outj).write_text(json.dumps(rep, indent=1) + "\n")
    print(json.dumps({"verified": rep["verified"], "checks_passed": not errs, "test_only": rep["test_only"],
                      "problems": errs, "axioms": rep["axioms"]}))
    sys.exit(0 if not errs else 1)
else:
    sys.exit(f"unknown helper command {cmd}")
PYEOF
py() { local c=$1; shift; A310_PINS="$EXPORTER_SHA256:$EXPORTER311_SHA256:$MERGE_SHA256:$DRIVER_SHA256:$COVERAGE_SHA256:$SHAPES_SHA256" \
  A310_FINAL_PIN="$FINAL_SRC_SHA" python3 -I -c "$PY" "$c" "$HERE" "$@"; }

# 1. Everything finished, the run, and the two gates (assemble_final311.sh:463-475, extended).
RUNJ="" GATESJ=""
if [ "$MODE" != stub ]; then
  why=()  # every reason is reported
  # The campaign (read only: one status query of its unit, its log and its directory).
  grep -q ' ALL 4096 CONTEXTS CLOSED$' "$CAMPAIGN/campaign/campaign.log" 2>/dev/null \
    || why+=("the campaign log has no 'ALL 4096 CONTEXTS CLOSED' line")
  systemctl --user is-active --quiet es8-b64-campaign && why+=("the campaign unit es8-b64-campaign is still active")
  { [ -e "$CAMPAIGN/campaign/WITNESS-ALERT.txt" ] || compgen -G "$CAMPAIGN/runs/*WITNESS*" >/dev/null; } \
    && why+=("a WITNESS file exists in the campaign")
  for u in es310-full es310-incr es311-full; do
    systemctl --user is-active --quiet "$u" && why+=("unit $u is still active")
  done
  for p in drive_es310 export_es310 merge_es310; do
    pgrep -f "$p\\.py.*es310/full" >/dev/null && why+=("a $p.py runs on build/es310/full")
  done
  pgrep -f 'drive_es311\.py.*es311/full' >/dev/null && why+=("a drive_es311.py runs on build/es311/full (the reused side)")
  for pair in "es310:$EXPORT" "es311:$E311"; do  # drive_es31x.py's scope tags (drive_es311.py:259)
    TAG=${pair%%:*}-$(printf '%s' "$(cd "${pair#*:}" 2>/dev/null && pwd -P)" | sha256sum | cut -c1-10)
    [ -z "$(systemctl --user list-units --all --no-legend --plain "$TAG-*" 2>/dev/null)" ] \
      || why+=("scopes of the ${pair%%:*} driver ($TAG-*) are still present")
  done
  [ -e "$EXPORT/ALERT-changed-inputs.txt" ] && why+=("$EXPORT/ALERT-changed-inputs.txt exists")
  RUNJ=$(py check-run 2>&1) || { why+=("run: $RUNJ"); RUNJ=""; }
  if [ ${#why[@]} -eq 0 ]; then
    mkdir -p "$WORK"
    say "run complete: $RUNJ"
    say "gate: shapes_es311.py on $EXPORT"
    (cd "$HERE" && nice -n 10 python3 -I "$HERE/shapes_es311.py" "$EXPORT") > "$WORK/shapes-es310.json" 2> "$WORK/shapes-es310.err"
    MSHA0=$(sha256sum < "$EXPORT/manifest-E310B.json" | cut -c1-64)
    say "gate: coverage_es310.py --complete on $EXPORT (manifest sha256 $MSHA0)"
    (cd "$HERE" && nice -n 10 python3 -I "$HERE/coverage_es310.py" "$EXPORT" --complete --campaign "$CAMPAIGN" \
      --exporter-sha256 "$EXPORTER_SHA256" --jobs 8) > "$WORK/coverage-es310.json" 2> "$WORK/coverage-es310.err"
    crc=$?
    GATESJ=$(py gates "$WORK/shapes-es310.json" "$WORK/coverage-es310.json" "$crc" "$MSHA0" "$RUNJ" 2>&1) \
      || { why+=("$GATESJ (see $WORK/shapes-es310.json, $WORK/coverage-es310.json)"); GATESJ=""; }
  fi
  [ ${#why[@]} -eq 0 ] || refuse "$(printf '%s; ' "${why[@]}")"
  say "gates passed: $GATESJ"
fi

# 2. The chain, the library and its freeze, and 3. the catalogs and the 13 pinned inputs (assemble_final311.sh:477-489).
LAKE_LP=$(cd "$REPO" && systemd-run --user --scope --quiet -p MemoryMax=2G -p MemorySwapMax=0 nice -n 10 \
  lake env printenv LEAN_PATH) || fail "lake env"
RUN_START=""
[ -n "$RUNJ" ] && RUN_START=$(echo "$RUNJ" | python3 -I -c 'import json,sys; print(json.load(sys.stdin)["first_compile_start_utc"])')
CHAINJ=$(py check-chain "$LAKE_LP" "$RUN_START" 2>&1) || refuse "$CHAINJ"
(cd "$HERE" && LM_NO_BUILD=1 ./lean_make.sh Path Fcat62 Fcat2650 Bridge311Bal Bridge311Res) 2>/dev/null \
  || refuse "the CompactChecker modules are not current (LM_NO_BUILD=1 lean_make.sh fails)"
ROUTE=$(echo "$CHAINJ" | python3 -I -c 'import json,sys; print(json.load(sys.stdin)["route"])')
say "library: $(echo "$CHAINJ" | python3 -I -c 'import json,sys; d=json.load(sys.stdin); print(d["library_pinned_verified"], "pinned .olean files as in library.json (" + d["library_pinned_utc"] + "); " + str(d["lake_oleans_checked"]) + " .lake .olean files older than the freeze " + d["lake_freeze_utc"] + " (newest " + d["lake_newest_utc"] + ")")')"
say "catalogs (build/ext = build/chain311 = October record): route $ROUTE"
say "inputs of route $ROUTE: $(echo "$CHAINJ" | python3 -I -c 'import json,sys; d=json.load(sys.stdin); print(d["inputs_equal_to_311_pins"], "files with the 311 pins" + (", all older than the first compile of the run, " + d["run_first_compile_utc"] if d["inputs_older_than_run"] else " (no run: mtimes not checked)"))')"

# 4. LEAN_PATH.
mkdir -p "$WORK" "$LOGDIR"
py make-path "$WORK" "$STUB" || fail "make-path"
LP="$LAKE_LP:$CHAIN/olean:$WORK/path"
[ -n "${A310_EXTRA_ROOT:-}" ] && LP="$LP:$A310_EXTRA_ROOT"
NOLEAN=$(py shadow "$LP" 2>&1) || refuse "LEAN_PATH: $NOLEAN"
say "LEAN_PATH: $(echo "$LP" | tr ':' '\n' | wc -l) roots, $NOLEAN .olean files, no module provided twice"
echo "$CHAINJ" | grep -q '"complete": true' || refuse "the chain in build/chain311 is not complete: $(echo "$CHAINJ" \
  | python3 -I -c 'import json,sys; d=json.load(sys.stdin); print(len(d["not_ok"]), "of", d["modules"], "modules not ok:", ", ".join(d["not_ok"][:6]))')"
if [ "$MODE" = dry ]; then say "dry run: all checks passed; nothing compiled"; exit 0; fi

# 5. The assembly, and 6. the audit (assemble_final311.sh:526-552).
avail=$(awk '/^MemAvailable:/ {print int($2 / 1048576)}' /proc/meminfo)
[ "$avail" -ge $((cap_gb + 8)) ] || refuse "MemAvailable ${avail} GB < cap ${cap_gb} GB + 8 GB"
OUTD=$WORK/out-olean; rm -rf "$OUTD"; mkdir -p "$OUTD"
MAINLOG=$WORK/final310-compact.main.log AUDITLOG=$WORK/final310-compact.audit.log
cool
# The pinned source, copied and checked right before the compile; the copy is what Lean compiles.
FSRCD=$WORK/final-src; rm -rf "$FSRCD"; mkdir -p "$FSRCD"; FSRC=$FSRCD/Final310Compact.lean
cp "$FINAL_SRC" "$FSRC" && chmod a-w "$FSRC" || fail "copy of $FINAL_SRC"
[ "$(sha256sum < "$FSRC" | cut -c1-64)" = "$FINAL_SRC_SHA" ] || refuse "$FINAL_SRC is not the pinned version (sha256 $FINAL_SRC_SHA) at compile time"
say "compiling Final310Compact.lean (pinned copy $FSRC, sha256 $FINAL_SRC_SHA; cap $MEM)"
LEAN_PATH="$LP" capped "$MEM" "$MAINLOG" lean -j1 -R "$FSRCD" -o "$OUTD/Final310Compact.olean" "$FSRC"
rc=$?
say "lean exited $rc"
AUD=$WORK/audit; rm -rf "$AUD"; mkdir -p "$AUD"
cat > "$AUD/Audit310.lean" <<EOF
import Final310Compact
#check @$THEOREM
#print axioms $THEOREM
open Lean in
#eval show CoreM Unit from do
  for m in (← getEnv).header.moduleNames do
    IO.println s!"module {m}"
EOF
arc=none
if [ $rc -eq 0 ] && [ -f "$OUTD/Final310Compact.olean" ]; then
  msg=$(py shadow "$LP:$OUTD" 2>&1) || refuse "LEAN_PATH with the result: $msg"
  cool
  LEAN_PATH="$LP:$OUTD" capped "$MEM" "$AUDITLOG" lean -j1 -R "$AUD" "$AUD/Audit310.lean"
  arc=$?
  [ $arc -eq 0 ] || say "audit compile exited $arc"
else
  echo "(no audit: the main compile failed)" > "$AUDITLOG"
fi

# 7. Records (assemble_final311.sh:554-565).
M=real; [ "$MODE" = stub ] && M=stub; [ "$MODE" = real ] && [ -n "${A310_EXPORT:-}" ] && M=test-export
{ echo "===== Final310Compact.lean ($(date -u +%FT%TZ), cap $MEM, route $ROUTE)"; cat "$MAINLOG"
  echo "===== Audit310.lean"; grep -v '^module ' "$AUDITLOG"; echo "($(grep -c '^module ' "$AUDITLOG") module lines omitted; see the imports TSV)"
} | sed "s#$REPO#<repo>#g; s#$HOME#<home>#g" > "$LOGDIR/final310-compact.log"
py report "$MAINLOG" "$rc" "$AUDITLOG" "$arc" "$LP:$OUTD" "$LOGDIR/final310-compact.json" \
  "$LOGDIR/final310-compact-imports.tsv.gz" "$M" "$ROUTE" "$RUNJ" "$CHAINJ" "$MEM" "$FSRC" "$LAKE_LP" \
  "$OUTD/Final310Compact.olean" "$GATESJ"
v=$?
say "records: $LOGDIR/final310-compact.{log,json}, final310-compact-imports.tsv.gz"
[ $v -eq 0 ] || fail "not verified (see $LOGDIR/final310-compact.json)"
if [ "$M" = real ]; then
  say "VERIFIED $THEOREM : ErdosSzekeres.ForcesConvexNGon 310 8 (standard axioms only)"
else  # soundness review item 5: a test mode never prints VERIFIED
  say "TEST ONLY (mode $M): every check passed, but this is NOT a verification of ES(8) <= 310"
fi
