#!/bin/bash
# Tests of drive_es310.py (6 November 2026). They test the driver only; ES(8) <= 310 is NOT proved.
#
#   test_driver_es310.sh WORKDIR [CASE...]     (e.g. build/es310/test-driver; default: every case, in order)
#
# Fixtures, made fresh under WORKDIR from the 311 trial exports in build/es311/trial (only read): a copy whose
# prefix and module names are rewritten (namespace/end lines only; C<5 digits> -> C<kkkk><mm>, e.g.
# E311R.C00380 -> E310BK.C038001) with the sha256 recomputed:
#   R  = trial R-L1000-B64 as E310BK (3 residual chunks of 935-1,000 leaves)
#   X  = trial BX-L1000-B64 as E310BX (the corrupted 721-leaf balanced chunk)
#   G  = R with the trial's old-header run.tsv and .olean files, renamed the same way
#   T  = block b113 (29 leaves, not corrupted) of the BX chunk alone, as E310BT.C000101: a tiny ok compile
#   TX = block b12 (51 leaves) of the BX chunk, which holds the corrupted leaf, alone, as E310BX.C000101: a tiny failing compile
# Cases without any Lean compile:
#   G  an old-header TSV with three ok rows: upgraded in place, all three still done (--dry-run)
#   H  --reuse: the real build/es311/full:E311R verifies 127 modules read-only (build/es311/full unchanged: a
#      fingerprint of every path, size, mtime, ctime and inode before and after); on a scratch COPY made with
#      cp --reflink=never, a changed .olean byte, a changed source, a later fail row, a changed dependency
#      stamp and an incomplete manifest each refuse; an E311R manifest in the export and another prefix refuse;
#      `lean --deps` (import resolution only) finds E311R.Root under the reuse root; while the driver runs,
#      an exclusive flock on build/es311/full/.driver.lock (drive_es311.py's) is refused
#   I  unit names: drive_es311.kill_scope with the bare name leaves a running transient scope (a `sleep`) alive;
#      drive_es310.kill_scope with the same bare name empties it
#   J  gates: parse_tctl / campaign_pause unit tests; a driver with --max-tctl 1, or with a fresh PAUSE line in
#      a fake campaign log, starts nothing and stops on STOP (safety net: --memory 1M); a second driver on the
#      same export is refused; --max-tctl 90 is refused
#   K  E310.Final: full_status on synthetic manifests; FINAL_TEMPLATE equals the verified 311 template with
#      only E311B->E310B, 63->64, E311->E310 changed (docstrings aside); expected names; scope tag
#   L  refusals: unknown --only, a corrupted module without --only, a source sha256 mismatch, a shape failure,
#      memory caps without a unit, an export in build/es311 or in the campaign directory (refused before the
#      lock file is opened), overlapping --reuse
#   M  prepare() passes LM_NO_BUILD=1 and the 5 module names; deps_stamp_of equals all 127 E311R rows and the
#      E311.Final row; library pins verified (4952); memory needs; each .olean hashed once per start (on G)
#   N  (fixer, 6 Nov) WITNESS gate: a WITNESS-ALERT.txt or a runs/*WITNESS* file in --campaign-dir refuses the
#      start (exit 5); one that appears while the driver waits stops it (exit 5, no row); --mem-wait-max: a job
#      the memory gate blocks while nothing runs stops the driver (exit 3, no row); imports_before unit tests
#   S  (fixer, 6 Nov) Root staleness, no Lean: a real sub-Root export of ctx 2406/2407 (export_es310 + merge
#      --subtree 11:1203, Python) with fake .olean files and synthetic ok rows: chunks before the Root ->
#      nothing to run; a later ok row of one chunk -> the Root runs again; a later fail row of a chunk -> that
#      chunk and the Root run
# Cases with tiny compiles (2 compiles of one block of <= 64 leaves each):
#   T  E310BT.C000101 ok (with --reuse build/es311/full:E311R, so the reuse root is on LEAN_PATH) and its .olean
#      written, a restart runs nothing; E310BX.C000101 (corrupted) fails,
#      no .olean, "decide proved that the proposition ... is false"
# Cases with compiles of 700-1,000-leaf modules (test_driver_es311.sh A-F ported; A-E share R, run in order; A makes R afresh):
#   A  kill -9 of /usr/bin/time mid-compile: verdict fail, no lean left, no .olean
#   B  kill -9 of the scope's top process (sh) mid-compile: the same
#   C  kill -9 of the driver with two compiles running: the next start stops their scopes, deletes their
#      temporary .olean files and compiles all three modules: ok
#   D  a further start runs nothing
#   E  SIGTERM to the driver mid-compile (--bench 1): no process, no .olean, no row
#   F  the corrupted chunk: verdict fail
# Every compile is the driver's own (one lean -j1 per scope, MemoryMax=12G, MemorySwapMax=0, nice 10, behind its
# Tctl < 80 C and campaign-PAUSE gates). Before each compiling step the script waits until the machine runs
# few enough Lean compiles that at most 2 run in all. Every check prints PASS or FAIL; exit 1 if any FAIL.
set -u -o pipefail
D=$(cd "$(dirname "$0")" && pwd)
[ $# -ge 1 ] || { echo "usage: $0 WORKDIR [CASE...]" >&2; exit 2; }
W=$(mkdir -p "$1" && cd "$1" && pwd); shift
case "$W/" in
  "$D/build/es311/"*|"$D/build/CompactChecker/"*|"$D/build/ext/"*|"$D/build/chain311/"*|/home/jay/research/data/*)
    echo "refusing WORKDIR $W" >&2; exit 2 ;;
esac
CASES=${*:-G H I J K L M N S T A B C D E F}
TR=$D/build/es311/trial
E311=$D/build/es311/full
PASSN=0 FAILN=0
ok() { echo "PASS: $*"; PASSN=$((PASSN + 1)); }
no() { echo "FAIL: $*"; FAILN=$((FAILN + 1)); }
check() { local n=$1; shift; if "$@"; then ok "$n"; else no "$n"; fi; }
say() { echo "== $(date -u +%FT%TZ) $*"; }
run_drv() {  # run_drv OUT ARGS...: runs the driver; OUT gets its output without lean_make lines; returns its exit
  local out=$1; shift
  python3 "$D/drive_es310.py" "$@" > "$out.raw" 2>&1; local rc=$?
  grep -v '^lean_make' "$out.raw" > "$out"; rm -f "$out.raw"; return $rc
}
jf() {  # jf OUT EXPR: EXPR over d = the first JSON line of OUT
  python3 -c 'import json,sys
d = next(json.loads(l) for l in open(sys.argv[1]) if l.startswith("{"))
print(eval(sys.argv[2], {}, {"d": d}))' "$1" "$2" 2>/dev/null
}
has() { grep -q -- "$2" "$1"; }
refused() { [ "$1" -ne 0 ] && grep -q -- "$3" "$2"; }  # refused RC OUT PATTERN
exited0() { [ "$1" -eq 0 ] && grep -q -- "$3" "$2"; }  # exited0 RC OUT PATTERN
procs() { pgrep -af "lean -j1 .*$1" | grep -v pgrep || true; }
compiles() { pgrep -fc '(^|/)lean (-j1 )?-R .* -o ' || true; }
wait_slots() {  # wait_slots N: until at most 2-N Lean compiles run on the machine
  local n=0
  until [ "$(compiles)" -le $((2 - $1)) ]; do
    [ $n -eq 0 ] && echo "waiting for Lean slots ($(compiles) compiles running)"; n=1; sleep 5
  done
}
wait_lean() {  # wait_lean FILE SECONDS DRIVER_PID: until the lean process of module file FILE runs, then SECONDS
  # more; returns 1 (instead of hanging) if the driver exits first or after 60 min (integration fix, 6 Nov)
  local n=0
  until pgrep -f "(^|/)lean -j1 .*$1" > /dev/null; do
    if ! kill -0 "$3" 2>/dev/null || [ $n -ge 7200 ]; then echo "wait_lean: no lean for $1 (driver gone or 60 min)"; return 1; fi
    sleep 0.5; n=$((n + 1))
  done
  sleep "$2"
}
wait_for() {  # wait_for FILE PATTERN SECONDS
  local t=0
  until grep -q -- "$2" "$1" 2>/dev/null; do sleep 1; t=$((t + 1)); [ $t -ge "$3" ] && return 1; done
  return 0  # (an until loop returns the status of its last body command)
}
last_row() { tail -1 "$1/run.tsv" | cut -f3,7,8,11,21; }

read -r -d '' FIX <<'PYEOF'
import hashlib, json, shutil, sys
from pathlib import Path
cmd = sys.argv[1]
sha = lambda b: hashlib.sha256(b).hexdigest()
newname = lambda mod, newp: f"{newp}.C{int(mod.split('.C')[1]):04d}01"

def write_src(dst, newp, nm, text):
    f = f"src/{newp}/{nm.split('.')[1]}.lean"
    (dst / f).parent.mkdir(parents=True, exist_ok=True)
    (dst / f).write_text(text)
    b = (dst / f).read_bytes()
    return f, sha(b), len(b)

if cmd == "rename":  # rename SRC DST OLDP NEWP [state]
    src, dst, oldp, newp = Path(sys.argv[2]), Path(sys.argv[3]), sys.argv[4], sys.argv[5]
    state = sys.argv[6:] == ["state"]
    man = json.loads((src / f"manifest-{oldp}.json").read_text())
    mods, shamap, names = [], {}, {}
    for mm in man["modules"]:
        if mm["file"] is None:
            continue
        nm = newname(mm["module"], newp)
        text = (src / mm["file"]).read_text()
        text = text.replace(f"namespace {mm['module']}\n", f"namespace {nm}\n").replace(f"end {mm['module']}\n", f"end {nm}\n")
        assert mm["module"] not in text and oldp + "." not in text
        f, s, n = write_src(dst, newp, nm, text)
        shamap[mm["sha256"]], names[mm["module"]] = s, nm
        mods.append(dict(mm, module=nm, file=f, sha256=s, source_bytes=n))
    man.update(prefix=newp, modules=mods, complete=False, root=None)
    (dst / f"manifest-{newp}.json").write_text(json.dumps(man, indent=1) + "\n")
    if state:  # the old-header TSV and the .olean files, renamed the same way
        lines = (src / "run.tsv").read_text().splitlines()
        cols = lines[0].split("\t")
        out = [lines[0]]
        for line in lines[1:]:
            r = dict(zip(cols, line.split("\t")))
            r["module"], r["src_sha256"] = names[r["module"]], shamap[r["src_sha256"]]
            out.append("\t".join(r[c] for c in cols))
        (dst / "run.tsv").write_text("\n".join(out) + "\n")
        for old, nm in names.items():
            o = src / "olean" / (old.replace(".", "/") + ".olean")
            t = dst / "olean" / (nm.replace(".", "/") + ".olean")
            t.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(o, t)
elif cmd == "tiny":  # tiny SRC OLDP MODULE BLOCK DST NEWP NEWMOD ok|corrupted
    src, oldp, mod, k, dst, newp, nm, kind = sys.argv[2:10]
    src, dst = Path(src), Path(dst)
    man = json.loads((src / f"manifest-{oldp}.json").read_text())
    mm = next(m for m in man["modules"] if m["module"] == mod)
    lines = (src / mm["file"]).read_text().split("\n")
    i = next(j for j, l in enumerate(lines) if l.startswith("noncomputable def "))
    j = next(j for j, l in enumerate(lines) if l.startswith(f"noncomputable def b{k} : "))
    blk = lines[j:j + 4]
    assert blk[1].startswith(f"theorem chk{k} : ") and blk[2].startswith(f"theorem ex{k} : ") and "checkF2_feas" in blk[3]
    leaves = blk[0].count("(.leaf ") + blk[0].count(".overBudget")
    head = [l for l in lines[:i] if not l.startswith("--")]
    head = [f"namespace {nm}" if l == f"namespace {mod}" else l for l in head]
    head.append(f"-- drive_es310 test fixture: block b{k} of {mod} ({src.name}), {leaves} leaves, budget {man['budget']}")
    text = "\n".join(head + blk + [f"#print axioms ex{k}", f"end {nm}"]) + "\n"
    f, s, n = write_src(dst, newp, nm, text)
    man.update(prefix=newp, complete=False, root=None, total_leaves=leaves, corruption=None,
               modules=[{"index": 1, "module": nm, "leaves": leaves, "subtree_roots": [[int(k), leaves]],
                         "file": f, "sha256": s, "source_bytes": n, "blocks": 1, "corrupted": kind == "corrupted"}])
    (dst / f"manifest-{newp}.json").write_text(json.dumps(man, indent=1) + "\n")
elif cmd == "resha":  # resha EXPORT PREFIX: recompute the manifest sha256 of every module file
    ex, p = Path(sys.argv[2]), sys.argv[3]
    mf = ex / f"manifest-{p}.json"
    man = json.loads(mf.read_text())
    for mm in man["modules"]:
        mm["sha256"] = sha((ex / mm["file"]).read_bytes())
    mf.write_text(json.dumps(man, indent=1) + "\n")
PYEOF
fix() { python3 -I -c "$FIX" "$@"; }
mk_R() { rm -rf "$W/R"; fix rename "$TR/R-L1000-B64" "$W/R" E311R E310BK; }
mk_X() { rm -rf "$W/X"; fix rename "$TR/BX-L1000-B64" "$W/X" E311BX E310BX; }
mk_G() { rm -rf "$W/G"; fix rename "$TR/R-L1000-B64" "$W/G" E311R E310BK state; }
mk_T() { rm -rf "$W/$1"; fix tiny "$TR/BX-L1000-B64" E311BX E311BX.C00001 113 "$W/$1" E310BT E310BT.C000101 ok; }
mk_TX() { rm -rf "$W/$1"; fix tiny "$TR/BX-L1000-B64" E311BX E311BX.C00001 12 "$W/$1" E310BX E310BX.C000101 corrupted; }
pyt() { python3 -c "$1" "$D" "${@:2}"; }  # python unit test: sys.argv[1] = D

case_G() {
  say "G: an old-header TSV with three ok rows"
  mk_G
  local nf0; nf0=$(head -1 "$W/G/run.tsv" | awk -F'\t' '{print NF}')
  run_drv "$W/G.out" "$W/G" --jobs 1 --dry-run; local rc=$?
  check "G: driver exit 0 (got $rc)" [ $rc -eq 0 ]
  check "G: the old header has 20 columns" [ "$nf0" = 20 ]
  check "G: to_run 0, already_done 3" [ "$(jf "$W/G.out" "(d['to_run'], d['already_done'])")" = "(0, 3)" ]
  check "G: header upgraded to 21 columns" [ "$(head -1 "$W/G/run.tsv" | awk -F'\t' '{print NF}')" = 21 ]
  check "G: all $(($(wc -l < "$W/G/run.tsv") - 1)) rows have 21 fields" \
    [ "$(awk -F'\t' 'NR > 1 {print NF}' "$W/G/run.tsv" | sort -u)" = 21 ]
  check "G: no reuse links without --reuse" [ ! -e "$W/G/reuse" ]
}

case_H() {
  say "H: --reuse of the residual side"
  mk_T H/out
  fp() { find "$E311" -printf '%P %s %T@ %C@ %i\n' | sort | sha256sum | cut -c1-64; }
  local fp0 rc CP=$W/H/es311copy; fp0=$(fp)
  run_drv "$W/H.real.out" "$W/H/out" --reuse "$E311:E311R" --dry-run; rc=$?
  check "H: real build/es311/full:E311R accepted (exit $rc)" [ $rc -eq 0 ]
  check "H: 127 modules (126 chunks + Root), 13 route inputs verified" \
    [ "$(jf "$W/H.real.out" "(d['reuse']['modules'], d['reuse']['chunks'], d['reuse']['route_inputs_verified'])")" = "(127, 126, 13)" ]
  check "H: 127 file symlinks out/reuse/E311R/<X>.olean -> build/es311/full/olean/E311R/<X>.olean, nothing else" \
    [ "$(find "$W/H/out/reuse" -mindepth 2 -maxdepth 2 -type l -lname "$E311/olean/E311R/*.olean" | wc -l)" = 127 \
      -a "$(find "$W/H/out/reuse" ! -type l | wc -l)" = 2 -a "$(find "$W/H/out/reuse" -mindepth 3 | wc -l)" = 0 ]
  pyt 'import json, os, sys; sys.path.insert(0, sys.argv[1]); import drive_es310 as d
from pathlib import Path
out, e = Path(sys.argv[2]), Path(sys.argv[3])
m = json.load(open(e / "manifest-E311R.json"))
mods = [x["module"] for x in m["modules"]] + [m["root"]["module"]]
bad = [x for x in mods if os.readlink(out / "reuse" / d.mpath(x)) != str((e / "olean" / d.mpath(x)).resolve())]
print("module resolution under the reuse root:", len(mods) - len(bad), "of", len(mods))' "$W/H/out" "$E311" > "$W/H.res.out" 2>&1
  check "H: every E311R module X resolves as <reuse root>/E311R/X.olean to its own .olean" has "$W/H.res.out" "root: 127 of 127"
  check "H: final not added for a test export" has "$W/H.real.out" '"final": "not full'
  printf 'import E311R.Root\nimport CompactChecker.Bridge311Res\n' > "$W/H/probe.lean"
  local LP; LP=$(cd "$D/../.." && systemd-run --user --scope --quiet -p MemoryMax=2G -p MemorySwapMax=0 nice -n 10 \
    lake env printenv LEAN_PATH)
  (cd "$D/../.." && LEAN_PATH="$LP:$D/build:$D/build/ext:$W/H/out/olean:$W/H/out/reuse" timeout 120 systemd-run --user \
    --scope --quiet -p MemoryMax=2G -p MemorySwapMax=0 nice -n 10 lean --deps "$W/H/probe.lean") > "$W/H.deps.out" 2>&1
  check "H: on the driver's LEAN_PATH, lean --deps (import resolution only, no elaboration) finds E311R.Root at out/reuse/E311R/Root.olean" \
    grep -qx "$W/H/out/reuse/E311R/Root.olean" "$W/H.deps.out"
  # Remove the outputs of an earlier run first: the background job truncates its output file only when it
  # starts, so wait_for could otherwise match a stale "waiting:" line (integration fix, 6 Nov).
  rm -f "$W/H.lock.out" "$W/H.lock2.out"
  python3 "$D/drive_es310.py" "$W/H/out" --reuse "$E311:E311R" --jobs 1 --max-tctl 1 --memory 1M > "$W/H.lock.out" 2>&1 &
  local DRV=$!
  if wait_for "$W/H.lock.out" "waiting: Tctl" 240; then
    python3 -I -c 'import fcntl, sys
f = open(sys.argv[1], "rb")
try:
    fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB); print("exclusive lock GRANTED")
except BlockingIOError:
    print("exclusive lock refused")' "$E311/.driver.lock" > "$W/H.lock2.out" 2>&1
  fi
  touch "$W/H/out/STOP"; wait $DRV; rm -f "$W/H/out/STOP"
  check "H: while drive_es310 runs with --reuse, drive_es311.py's exclusive lock on build/es311/full is refused" \
    has "$W/H.lock2.out" "exclusive lock refused"
  check "H: build/es311/full unchanged (fingerprint of every path, size, mtime, ctime, inode)" [ "$(fp)" = "$fp0" ]
  say "H: scratch copy of the E311R side (cp --reflink=never)"
  rm -rf "$CP"; mkdir -p "$CP/src" "$CP/olean"
  cp --reflink=never "$E311/manifest-E311R.json" "$E311/run.tsv" "$CP/"
  cp -r --reflink=never "$E311/src/E311R" "$CP/src/"; cp -r --reflink=never "$E311/olean/E311R" "$CP/olean/"
  check "H: the copy shares no inode with build/es311/full (C00064.olean)" \
    [ "$(stat -c %i "$CP/olean/E311R/C00064.olean")" != "$(stat -c %i "$E311/olean/E311R/C00064.olean")" ]
  run_drv "$W/H.c0.out" "$W/H/out" --reuse "$CP:E311R" --dry-run; rc=$?
  check "H: the unchanged copy is accepted (exit $rc), 127 modules" [ $rc -eq 0 -a "$(jf "$W/H.c0.out" "d['reuse']['modules']")" = 127 ]
  flip() { python3 -I -c 'import sys
p = sys.argv[1]; b = bytearray(open(p, "rb").read()); b[len(b) // 2] ^= 1; open(p, "wb").write(b)' "$1"; }
  flip "$CP/olean/E311R/C00064.olean"
  run_drv "$W/H.c1.out" "$W/H/out" --reuse "$CP:E311R" --dry-run; rc=$?
  check "H: one changed byte in a reused .olean refuses (exit $rc)" [ $rc -ne 0 ]
  check "H:   ... naming E311R.C00064's .olean" has "$W/H.c1.out" "E311R.C00064: .olean"
  sed -n 's/^.*refusing/refusing/p' "$W/H.c1.out" | head -1 | cut -c1-200
  flip "$CP/olean/E311R/C00064.olean"
  run_drv "$W/H.c2.out" "$W/H/out" --reuse "$CP:E311R" --dry-run; rc=$?
  check "H: restored byte accepted again (exit $rc)" [ $rc -eq 0 ]
  sed -i '0,/^-- /s/^-- /-- X/' "$CP/src/E311R/C00002.lean"
  run_drv "$W/H.c3.out" "$W/H/out" --reuse "$CP:E311R" --dry-run; rc=$?
  check "H: a changed reused source refuses (exit $rc)" refused $rc "$W/H.c3.out" "E311R.C00002: source"
  cp --reflink=never "$E311/src/E311R/C00002.lean" "$CP/src/E311R/C00002.lean"
  grep -P '\tE311R\.C00003\t' "$E311/run.tsv" | tail -1 | awk -F'\t' 'BEGIN{OFS="\t"} {$7 = "fail"; print}' >> "$CP/run.tsv"
  run_drv "$W/H.c4.out" "$W/H/out" --reuse "$CP:E311R" --dry-run; rc=$?
  check "H: a later fail row refuses (exit $rc)" refused $rc "$W/H.c4.out" "E311R.C00003: last row is chunk fail"
  cp --reflink=never "$E311/run.tsv" "$CP/run.tsv"
  python3 -I -c 'import sys
p = sys.argv[1]; L = open(p).read().splitlines()
i = max(j for j, l in enumerate(L) if l.split("\t")[2] == "E311R.Root")
c = L[i].split("\t"); c[5] = "0" * 64; L[i] = "\t".join(c); open(p, "w").write("\n".join(L) + "\n")' "$CP/run.tsv"
  run_drv "$W/H.c5.out" "$W/H/out" --reuse "$CP:E311R" --dry-run; rc=$?
  check "H: a changed dependency stamp refuses (exit $rc)" refused $rc "$W/H.c5.out" "E311R.Root: dependency stamp"
  cp --reflink=never "$E311/run.tsv" "$CP/run.tsv"
  python3 -I -c 'import json,sys
p = sys.argv[1]; d = json.load(open(p)); d["complete"] = False; open(p, "w").write(json.dumps(d))' "$CP/manifest-E311R.json"
  run_drv "$W/H.c6.out" "$W/H/out" --reuse "$CP:E311R" --dry-run; rc=$?
  check "H: an incomplete reused manifest refuses (exit $rc)" refused $rc "$W/H.c6.out" "not complete"
  cp --reflink=never "$E311/manifest-E311R.json" "$CP/manifest-E311R.json"
  cp "$TR/R-L1000-B64/manifest-E311R.json" "$W/H/out/"
  run_drv "$W/H.c7.out" "$W/H/out" --reuse "$CP:E311R" --dry-run; rc=$?
  check "H: an E311R manifest in the export refuses (exit $rc)" refused $rc "$W/H.c7.out" "never compiled here"
  rm -f "$W/H/out/manifest-E311R.json"
  run_drv "$W/H.c8.out" "$W/H/out" --reuse "$CP:E311B" --dry-run; rc=$?
  check "H: --reuse of another prefix refuses (exit $rc)" refused $rc "$W/H.c8.out" "only the residual side"
  run_drv "$W/H.c9.out" "$W/H/out" --reuse "$E311:E311R" --dry-run; rc=$?
  check "H: the real side accepted again at the end (exit $rc)" [ $rc -eq 0 ]
  check "H: build/es311/full still unchanged" [ "$(fp)" = "$fp0" ]
  rm -rf "$CP"
}

case_I() {
  say "I: unit names (a transient scope running sleep, no Lean)"
  local u rc bare full
  u=es310-unittest-$(head -c4 /dev/urandom | od -An -tx1 | tr -d ' \n')
  systemd-run --user --scope --quiet --unit="$u" sleep 600 &
  local SP=$!
  until systemctl --user is-active --quiet "$u.scope"; do sleep 0.2; done
  bare=$(systemctl --user show -p ControlGroup --value "$u"); full=$(systemctl --user show -p ControlGroup --value "$u.scope")
  check "I: the bare name resolves to no cgroup (what drive_es311.py asked for)" [ -z "$bare" ]
  check "I: '$u.scope' resolves to the scope's cgroup ($full)" [ -n "$full" ]
  pyt 'import sys; sys.path.insert(0, sys.argv[1]); import drive_es311 as e; print("drive_es311.kill_scope(bare):", e.kill_scope(sys.argv[2], None, 5))' "$u"
  check "I: drive_es311.kill_scope with the bare name leaves the sleep running" kill -0 $SP
  pyt 'import sys; sys.path.insert(0, sys.argv[1]); import drive_es310 as d
assert d.scope_unit("x") == "x.scope" and d.scope_unit("x.scope") == "x.scope"
print("drive_es310.kill_scope(bare):", d.kill_scope(sys.argv[2], None, 30))' "$u" > "$W/I.out" 2>&1
  cat "$W/I.out"
  wait $SP 2>/dev/null
  check "I: drive_es310.kill_scope with the bare name returns True" has "$W/I.out" "kill_scope(bare): True"
  check "I: the sleep is gone and the scope is not active" bash -c "! kill -0 $SP 2>/dev/null && ! systemctl --user is-active --quiet '$u.scope'"
  check "I: every systemctl call in drive_es310.py names the scope (kill_scope converts first)" \
    [ "$(grep -c 'unit = scope_unit(unit)' "$D/drive_es310.py")" = 1 -a "$(grep -c 'scope_unit(unit))' "$D/drive_es310.py")" = 1 ]
}

case_J() {
  say "J: temperature and campaign gates"
  mkdir -p "$W/J"
  pyt 'import os, sys, time; sys.path.insert(0, sys.argv[1]); import drive_es310 as d
w = sys.argv[2]
assert d.parse_tctl("k10temp-pci-00c3\nAdapter: PCI adapter\nTctl:         +73.4°C  \nTccd1: +60.0°C\n") == 73.4
assert d.parse_tctl("Tctl: +70.0°C\nTctl: +81.5°C\n") == 81.5
assert d.parse_tctl("Tccd1: +60.0°C\n") is None and d.parse_tctl("") is None
now = time.time()
ts = lambda dt: time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(now - dt))
def log(name, lines):
    p = os.path.join(w, name); open(p, "w").write("".join(l + "\n" for l in lines)); return p
start = lambda n: [f"{ts(30)} start ctx {i} (b63 leaves 300)" for i in range(n)]
P = f"{ts(120)} PAUSE ctx 858 (tctl 95.625, mem 36.6 GiB)"
assert d.campaign_pause(log("a", start(5) + [P] + start(3)), now) == P
assert d.campaign_pause(log("b", [f"{ts(660)} PAUSE ctx 1 (tctl 95.1, mem 30.0 GiB)"] + start(3)), now) is None
assert d.campaign_pause(log("c", [P] + start(50)), now) is None
assert d.campaign_pause(log("f", [P] + start(49)), now) == P
assert d.campaign_pause(os.path.join(w, "missing.log"), now) is None
assert d.campaign_pause(log("e", [f"{ts(60)} RESUME ctx 858"]), now) is None
print("gate unit tests ok")' "$W/J" > "$W/J.unit.out" 2>&1
  check "J: parse_tctl and campaign_pause unit tests" has "$W/J.unit.out" "gate unit tests ok"
  cat "$W/J.unit.out" | tail -3
  mk_T J/T
  rm -f "$W/J.t.out" "$W/J.p.out"  # no stale "waiting:" line for wait_for (see case H)
  python3 "$D/drive_es310.py" "$W/J/T" --jobs 1 --max-tctl 1 --memory 1M > "$W/J.t.out" 2>&1 &
  local DRV=$! rc
  if wait_for "$W/J.t.out" "waiting: Tctl" 240; then ok "J: --max-tctl 1: the driver waits ($(grep -m1 'waiting:' "$W/J.t.out" | cut -c1-80))"
  else no "J: --max-tctl 1: no 'waiting: Tctl' line"; fi
  run_drv "$W/J.second.out" "$W/J/T" --dry-run; rc=$?
  check "J: a second driver on the same export is refused (exit $rc)" refused $rc "$W/J.second.out" "another drive_es310.py holds"
  check "J: no lean started for the export" [ -z "$(procs "$W/J/T/src")" ]
  touch "$W/J/T/STOP"; wait $DRV; rc=$?
  check "J: STOP ends the waiting driver with exit 3 = work left undone (got $rc)" \
    bash -c "[ $rc -eq 3 ] && grep -q 'STOP file present' '$W/J.t.out' && grep -q '\"not_started\": 1' '$W/J.t.out'"
  check "J: no row was written" [ "$(wc -l < "$W/J/T/run.tsv")" = 1 ]
  rm -f "$W/J/T/STOP"
  printf '%s PAUSE ctx 1 (tctl 95.5, mem 30.0 GiB)\n%s start ctx 2 (b63 leaves 300)\n' "$(date '+%F %T')" "$(date '+%F %T')" > "$W/J/campaign.log"
  rm -f "$W/J.p.out"
  python3 "$D/drive_es310.py" "$W/J/T" --jobs 1 --max-tctl 85 --memory 1M --campaign-log "$W/J/campaign.log" > "$W/J.p.out" 2>&1 &
  DRV=$!
  if wait_for "$W/J.p.out" "waiting: campaign PAUSE" 240; then ok "J: a fresh PAUSE line: the driver waits"
  else no "J: a fresh PAUSE line: no 'waiting: campaign PAUSE' line ($(grep -m1 'waiting:' "$W/J.p.out"))"; fi
  check "J: the start JSON reports the PAUSE line" [ "$(jf "$W/J.p.out" "bool(d['gate']['campaign_pause'])")" = True ]
  touch "$W/J/T/STOP"; wait $DRV; rc=$?
  check "J: STOP ends it (exit $rc, 3 expected), no row, no lean" [ $rc -eq 3 -a "$(wc -l < "$W/J/T/run.tsv")" = 1 -a -z "$(procs "$W/J/T/src")" ]
  rm -f "$W/J/T/STOP"
  run_drv "$W/J.hot.out" "$W/J/T" --max-tctl 90 --dry-run; rc=$?
  check "J: --max-tctl 90 refused (exit $rc)" refused $rc "$W/J.hot.out" "must be in (0, 85]"
}

case_K() {
  say "K: E310.Final"
  pyt 'import re, sys; sys.path.insert(0, sys.argv[1]); import drive_es310 as d, drive_es311 as e
good = {"prefix": "E310B", "side": "balanced", "catalog": "CompactChecker.Fcat62", "budget": 64, "export_root": 0,
        "base_path": [], "complete": True, "root": {"module": "E310B.Root"}}
R = {"prefix": "E311R"}
assert d.full_status({"E310B": good}, R) == (True, None)
assert not d.full_status({"E310B": good}, None)[0]
assert not d.full_status({"E310B": good}, {"prefix": "E311B"})[0]
for k, v in [("complete", False), ("root", None), ("base_path", [[5, 2]]), ("budget", 63), ("export_root", 3),
             ("catalog", "CompactChecker.Fcat2650"), ("side", "residual")]:
    assert not d.full_status({"E310B": dict(good, **{k: v})}, R)[0], k
assert not d.full_status({"E310B": good, "E310BT": dict(good, prefix="E310BT")}, R)[0]
assert not d.full_status({"E311B": dict(good, prefix="E311B")}, R)[0]
T = d.FINAL_TEMPLATE
assert [l for l in T.splitlines() if l.startswith("import ")] == ["import E310B.Root", "import E311R.Root",
    "import CompactChecker.Bridge311Bal", "import CompactChecker.Bridge311Res"]
assert "E311.Final" not in T and "E311B" not in T
nodoc = lambda s: [l for l in re.sub(r"/-!.*?-/\n", "", s, flags=re.S).splitlines() if l.strip()]
old = e.FINAL_TEMPLATE
for a, b in [("E311B.Root", "E310B.Root"), ("E311B.root", "E310B.root"), ("balanced_excludes_63", "balanced_excludes_64"),
             ("holes i) ≤ 63", "holes i) ≤ 64"), ("namespace E311\n", "namespace E310\n"), ("end E311\n", "end E310\n")]:
    assert old.count(a) >= 1, a
    old = old.replace(a, b)
assert nodoc(old) == nodoc(T), "FINAL_TEMPLATE differs from the 311 template beyond the budget and the names"
assert d.FINAL_EXPECTED == ["E310.balanced_excludes_64", "E310.residual_excludes_32"] and d.FINAL_MODULE == "E310.Final"
assert d.SCOPE_TAG == "es310-" and d.STAMPED == ["Path", "Fcat62", "Fcat2650", "Bridge311Bal", "Bridge311Res"]
print("K ok")' > "$W/K.out" 2>&1
  check "K: full_status, FINAL_TEMPLATE = 311 template with only names and 63->64 changed, expected names, tag" has "$W/K.out" "K ok"
  tail -3 "$W/K.out"
}

case_L() {
  say "L: refusals"
  local rc lk0
  mk_T L/T; mk_TX L/TX
  run_drv "$W/L1.out" "$W/L/T" --only E310BT.C999901 --dry-run; rc=$?
  check "L: unknown --only refused (exit $rc)" refused $rc "$W/L1.out" "unknown or unwritten modules"
  run_drv "$W/L2.out" "$W/L/TX" --dry-run; rc=$?
  check "L: a corrupted module without --only refused (exit $rc)" refused $rc "$W/L2.out" "corrupted test module"
  sed -i 's/^-- drive_es310 test fixture/-- drive_es310 test fixturE/' "$W/L/T/src/E310BT/C000101.lean"
  run_drv "$W/L3.out" "$W/L/T" --dry-run; rc=$?
  check "L: a source sha256 mismatch refused (exit $rc)" refused $rc "$W/L3.out" "differs from the manifest"
  sed -i 's/^end E310BT.C000101$/#eval 1\nend E310BT.C000101/' "$W/L/T/src/E310BT/C000101.lean"; fix resha "$W/L/T" E310BT
  run_drv "$W/L4.out" "$W/L/T" --dry-run; rc=$?
  check "L: a '#eval' line refused by the shape check (exit $rc)" refused $rc "$W/L4.out" "line-shape check failed"
  mk_T L/T
  run_drv "$W/L5.out" "$W/L/T" --memory 12 --dry-run; rc=$?
  check "L: --memory 12 (no unit) refused (exit $rc)" refused $rc "$W/L5.out" "is not <number>"
  run_drv "$W/L6.out" "$W/L/T" --root-memory infinity --dry-run; rc=$?
  check "L: --root-memory infinity refused (exit $rc)" [ $rc -ne 0 ]
  lk0=$(stat -c '%s %Y' "$E311/.driver.lock")
  run_drv "$W/L7.out" "$E311" --dry-run; rc=$?
  check "L: an export in build/es311 refused (exit $rc)" refused $rc "$W/L7.out" "lies in"
  check "L:   ... before its .driver.lock was opened (size and mtime unchanged)" [ "$(stat -c '%s %Y' "$E311/.driver.lock")" = "$lk0" ]
  run_drv "$W/L8.out" /home/jay/research/data/es8-b64-pilot-20261105/campaign --dry-run; rc=$?
  check "L: an export in the campaign directory refused (exit $rc)" refused $rc "$W/L8.out" "lies in"
  run_drv "$W/L9.out" "$W/L/T" --reuse "$W/L/T:E311R" --dry-run; rc=$?
  check "L: an overlapping --reuse refused (exit $rc)" refused $rc "$W/L9.out" "overlap"
}

case_M() {
  say "M: prepare(), stamps, library pins, memory gate, one hash per .olean"
  [ -d "$W/G" ] || mk_G
  pyt 'import hashlib, subprocess, sys; sys.path.insert(0, sys.argv[1]); import drive_es310 as d
calls, real = [], subprocess.run
def fake(cmd, *a, **k):
    calls.append((cmd, k.get("env")))
    return subprocess.CompletedProcess(cmd, 0, "", "") if cmd[0].endswith("lean_make.sh") else real(cmd, *a, **k)
d.subprocess.run = fake
stamps, lp = d.prepare(10)
d.subprocess.run = real
lm = [c for c in calls if c[0][0].endswith("lean_make.sh")]
assert len(lm) == 1 and lm[0][1]["LM_NO_BUILD"] == "1" and lm[0][0][1:] == d.STAMPED, lm
assert sorted(stamps) == sorted(d.STAMPED) and lp
L = open(sys.argv[2]).read().splitlines(); cols = L[0].split("\t"); last = {}
for l in L[1:]:
    r = dict(zip(cols, l.split("\t"))); last[r["module"]] = r
rr = [r for m, r in last.items() if m.startswith("E311R.")]
assert len(rr) == 127 and all(r["deps_stamp"] == d.deps_stamp_of(r["phase"], "Fcat2650", stamps) for r in rr)
assert last["E311.Final"]["deps_stamp"] == d.deps_stamp_of("final", None, stamps)
assert d.mem_gb("24G") == 24 and d.mem_gb("512M") == 0.5 and d.mem_gb("1T") == 1024
for bad in ("12", "infinity", "50%", "", "G"):
    try:
        d.mem_gb(bad); raise SystemExit("accepted " + bad)
    except ValueError:
        pass
print("M unit ok:", {k: v[:12] for k, v in stamps.items()})' "$E311/run.tsv" > "$W/M.unit.out" 2>&1
  check "M: prepare passes LM_NO_BUILD=1 and the 5 names; stamps equal all 127 E311R rows and the E311.Final row; mem_gb" \
    has "$W/M.unit.out" "M unit ok"
  tail -2 "$W/M.unit.out" | cut -c1-200
  run_drv "$W/M.out" "$W/G" --dry-run --root-memory 24G --reserve-gb 10 --job-gb 5; local rc=$?
  check "M: dry-run exit 0 (got $rc)" [ $rc -eq 0 ]
  check "M: JSON deps has exactly the 5 STAMPED names" [ "$(jf "$W/M.out" "sorted(d['deps'])")" = "['Bridge311Bal', 'Bridge311Res', 'Fcat2650', 'Fcat62', 'Path']" ]
  check "M: library pins verified (4952 .olean files)" [ "$(jf "$W/M.out" "d['library']['library_pinned_verified']")" = 4952 ]
  check "M: memory needs: chunk 10+5, Root/Final 10+24" [ "$(jf "$W/M.out" "(d['memory']['chunk_need_gb'], d['memory']['root_need_gb'])")" = "(15.0, 34.0)" ]
  pyt 'import collections, sys; sys.path.insert(0, sys.argv[1]); import drive_es310 as d
n, real = collections.Counter(), d.sha256_file
def counted(p):
    n[str(p)] += 1; return real(p)
d.sha256_file = counted
sys.argv = ["drive_es310.py", sys.argv[2], "--dry-run"]
d.main()
ol = {p: c for p, c in n.items() if "/olean/E310BK/" in p}
print("olean hashes per start:", sorted(ol.values()), len(ol))' "$W/G" > "$W/M.hash.out" 2>&1
  check "M: each of the 3 .olean files hashed exactly once per start" has "$W/M.hash.out" "olean hashes per start: \[1, 1, 1\] 3"
  grep "olean hashes" "$W/M.hash.out"
}

case_N() {
  say "N: WITNESS gate, memory-wait limit (no Lean)"
  local rc DRV CD=$W/N/camp
  mk_T N/T
  rm -rf "$CD"; mkdir -p "$CD/campaign" "$CD/runs"
  local G=(--campaign-dir "$CD" --campaign-log "$CD/campaign/campaign.log")
  run_drv "$W/N0.out" "$W/N/T" --dry-run "${G[@]}"; rc=$?
  check "N: no WITNESS file: dry run exit 0 (got $rc)" [ $rc -eq 0 ]
  touch "$CD/campaign/WITNESS-ALERT.txt"
  run_drv "$W/N1.out" "$W/N/T" --dry-run "${G[@]}"; rc=$?
  check "N: campaign/WITNESS-ALERT.txt refuses the start (exit $rc, 5 expected)" bash -c "[ $rc -eq 5 ] && grep -q 'WITNESS files in the campaign' '$W/N1.out'"
  rm "$CD/campaign/WITNESS-ALERT.txt"; touch "$CD/runs/ctx-17-b64.WITNESS.json"
  run_drv "$W/N2.out" "$W/N/T" "${G[@]}"; rc=$?
  check "N: runs/ctx-17-b64.WITNESS.json refuses the start (exit $rc, 5 expected), no row" \
    bash -c "[ $rc -eq 5 ] && { [ ! -e '$W/N/T/run.tsv' ] || [ \$(wc -l < '$W/N/T/run.tsv') = 1 ]; }"
  rm "$CD/runs/ctx-17-b64.WITNESS.json"
  rm -f "$W/N.w.out"
  python3 "$D/drive_es310.py" "$W/N/T" --jobs 1 --max-tctl 1 --memory 1M "${G[@]}" > "$W/N.w.out" 2>&1 &
  DRV=$!
  if wait_for "$W/N.w.out" "waiting: Tctl" 240; then ok "N: the driver waits at the Tctl gate"; else no "N: no waiting line"; fi
  touch "$CD/campaign/WITNESS-ALERT.txt"
  if wait_for "$W/N.w.out" "WITNESS files in the campaign" 60; then ok "N: a WITNESS file that appears is seen within 60 s"
  else no "N: the appearing WITNESS file was not seen"; kill $DRV 2>/dev/null; fi
  wait $DRV; rc=$?
  check "N: ... and the driver stops with exit 5 (got $rc), no row, no lean" \
    [ $rc -eq 5 -a "$(wc -l < "$W/N/T/run.tsv")" = 1 -a -z "$(procs "$W/N/T/src")" ]
  rm "$CD/campaign/WITNESS-ALERT.txt"
  run_drv "$W/N.m.out" "$W/N/T" --jobs 1 --job-gb 100000 --mem-wait-max 3 "${G[@]}"; rc=$?
  check "N: --mem-wait-max 3 with a job that needs 100,010 GiB: exit 3 (got $rc), no row" \
    bash -c "[ $rc -eq 3 ] && grep -q 'memory gate blocked E310BT.C000101' '$W/N.m.out' && [ \$(wc -l < '$W/N/T/run.tsv') = 1 ]"
  pyt 'import sys; sys.path.insert(0, sys.argv[1]); import drive_es310 as d
r = lambda utc, wall: {"utc": utc, "wall_s": wall}
root = r("2026-11-06T00:01:40Z", "10.00")                      # started 00:01:30
assert d.imports_before({"a": r("2026-11-06T00:01:31Z", "5"), "b": r("2026-11-06T00:01:32Z", "5")}, root) == []
assert d.imports_before({"a": r("2026-11-06T00:01:33Z", "5")}, root) == ["a"]   # ended 3 s after the start
assert d.imports_before({"a": None, "b": r("2026-11-06T00:00:00Z", "1")}, root) == ["a"]
assert d.imports_before({"a": r("2026-11-06T00:00:00Z", "1")}, {"utc": "x", "wall_s": "1"}) == ["a"]
assert d.witness_files(None) == [] and d.witness_files("/nonexistent") == []
print("N unit ok")' > "$W/N.unit.out" 2>&1
  check "N: imports_before / witness_files unit tests" has "$W/N.unit.out" "N unit ok"
}

case_S() {
  say "S: Root staleness against its chunks (no Lean: fake .olean files, synthetic rows)"
  local rc S=$W/S
  rm -rf "$S"
  nice -n 10 python3 "$D/export_es310.py" --campaign /home/jay/research/data/es8-b64-pilot-20261105 \
    --source "$D/../omission-cover-certificates-2026-10-10/balanced-v2-source.json" --ctx 2406,2407 \
    --chunk-leaves 500 --block-leaves 64 --per-word 16 --prefix E310BT --out "$S" > "$W/S.export.json" 2> "$W/S.export.err"; rc=$?
  check "S: export of ctx 2406/2407 (exit $rc)" [ $rc -eq 0 ]
  python3 "$D/merge_es310.py" "$S" --subtree 11:1203 --prefix E310BT > "$W/S.merge.json" 2>&1; rc=$?
  check "S: merge --subtree 11:1203 (exit $rc)" [ $rc -eq 0 ]
  pyt 'import json, sys
from pathlib import Path
sys.path.insert(0, sys.argv[1]); import drive_es310 as d
D, S = Path(sys.argv[1]), Path(sys.argv[2])
man = json.loads((S / "manifest-E310BT.json").read_text())
st = {n: (D / "build/CompactChecker" / f"{n}.stamp").read_text().strip() for n in d.STAMPED}
import hashlib
rows = []
def row(utc, phase, mod, src, wall, verdict="ok"):
    o = S / "olean" / (mod.replace(".", "/") + ".olean"); o.parent.mkdir(parents=True, exist_ok=True)
    b = f"fake olean of {mod}".encode(); o.write_bytes(b)
    r = {"utc": utc, "phase": phase, "module": mod, "leaves": 1, "src_sha256": src,
         "deps_stamp": d.deps_stamp_of(phase, "Fcat62", st), "verdict": verdict, "exit": 0, "kernel_s": "1",
         "elab_s": "1", "wall_s": wall, "user_s": wall, "peak_rss_kb": 1, "olean_bytes": len(b),
         "olean_sha256": hashlib.sha256(b).hexdigest() if verdict == "ok" else "", "axioms": "x", "expected": 1,
         "load1": "1", "host": "synthetic", "log": "logs/none", "cg_peak_kb": 1}
    rows.append("\t".join(str(r[c]) for c in d.COLUMNS))
for mm in man["modules"]:
    row("2026-11-06T00:00:10Z", "chunk", mm["module"], mm["sha256"], "5.00")
row("2026-11-06T00:01:40Z", "root", "E310BT.Root", man["root"]["sha256"], "10.00")
(S / "run.tsv").write_text("\t".join(d.COLUMNS) + "\n" + "\n".join(rows) + "\n")
print("S rows", len(rows))' "$S" > "$W/S.rows.out" 2>&1
  check "S: synthetic rows written ($(cat "$W/S.rows.out"))" grep -q "S rows 9" "$W/S.rows.out"
  run_drv "$W/S1.out" "$S" --dry-run; rc=$?
  check "S: every chunk ended before the Root started: to_run 0, already_done 9 (exit $rc)" \
    [ "$(jf "$W/S1.out" "(d['to_run'], d['already_done'], d['stale_after_imports'])")" = "(0, 9, {})" ]
  awk -F'\t' 'BEGIN { OFS = "\t" } $3 == "E310BT.C240702" { $1 = "2026-11-06T00:05:00Z"; print }' "$S/run.tsv" > "$S/later.row"
  cat "$S/later.row" >> "$S/run.tsv"
  run_drv "$W/S2.out" "$S" --dry-run; rc=$?
  check "S: a later ok row of E310BT.C240702: the Root runs again (to_run 1, order [Root])" \
    [ "$(jf "$W/S2.out" "(d['to_run'], d['order'], d['stale_after_imports']['E310BT.Root']['imports_compiled_after_it'])")" = \
      "(1, ['E310BT.Root'], ['E310BT.C240702'])" ]
  awk -F'\t' 'BEGIN { OFS = "\t" } $3 == "E310BT.C240601" { $1 = "2026-11-06T00:06:00Z"; $7 = "fail"; $15 = ""; print; exit }' "$S/run.tsv" >> "$S/run.tsv"
  run_drv "$W/S3.out" "$S" --dry-run; rc=$?
  check "S: a later fail row of E310BT.C240601: that chunk and the Root run (to_run 2)" \
    [ "$(jf "$W/S3.out" "(d['to_run'], d['order'], 'E310BT.C240601' in d['stale_after_imports']['E310BT.Root']['imports_not_done'])")" = \
      "(2, ['E310BT.C240601', 'E310BT.Root'], True)" ]
}

case_T() {
  say "T: two tiny compiles (one block of <= 64 leaves each)"
  local rc
  mk_T T; mk_TX TX
  wait_slots 1
  run_drv "$W/T1.out" "$W/T" --jobs 1 --reuse "$E311:E311R"; rc=$?  # the reuse root on LEAN_PATH, as in the real run
  grep -v '^{' "$W/T1.out"
  check "T: E310BT.C000101 driver exit 0 (got $rc)" [ $rc -eq 0 ]
  check "T: its row is ok" [ "$(last_row "$W/T" | cut -f1,2)" = "$(printf 'E310BT.C000101\tok')" ]
  check "T: its .olean is written with the recorded sha256" \
    [ "$(sha256sum < "$W/T/olean/E310BT/C000101.olean" | cut -c1-64)" = "$(tail -1 "$W/T/run.tsv" | cut -f15)" ]
  run_drv "$W/T2.out" "$W/T" --jobs 1 --dry-run
  check "T: a restart runs nothing (to_run 0, already_done 1)" [ "$(jf "$W/T2.out" "(d['to_run'], d['already_done'])")" = "(0, 1)" ]
  wait_slots 1
  run_drv "$W/TX.out" "$W/TX" --jobs 1 --only E310BX.C000101; rc=$?
  grep -v '^{' "$W/TX.out"
  check "TX: the corrupted block: driver exit 1 (got $rc), verdict fail" [ $rc -eq 1 -a "$(last_row "$W/TX" | cut -f2)" = fail ]
  check "TX: no .olean" [ "$(find "$W/TX/olean" -name '*.olean' 2>/dev/null | wc -l)" = 0 ]
  check "TX: the log says decide proved the proposition false" grep -q "decide. proved that the proposition" "$W"/TX/logs/*.log
  grep -h -m1 "proved that the proposition" "$W"/TX/logs/*.log | cut -c1-160
}

case_A() {  # A starts the A-E chain on a FRESH R (a finished R left by an earlier run has nothing to compile)
  mk_R; kill_case time
}
case_B() { kill_case sh; }
kill_case() {  # test_driver_es311.sh:31-46
  local victim=$1 M=E310BK/C038001.lean V DRV rc
  [ -d "$W/R" ] || mk_R
  say "$victim: kill -9 of the '$victim' process of the compile of $M"
  wait_slots 1
  python3 "$D/drive_es310.py" "$W/R" --jobs 1 --only E310BK.C038001 > "$W/$victim.out" 2>&1 &
  DRV=$!
  wait_lean "$W/R/src/$M" 4 $DRV
  if [ "$victim" = time ]; then V=$(pgrep -f "^/usr/bin/time -v lean -j1 .*$W/R/src/$M"); else
    V=$(pgrep -f "^sh -c cg=.*$W/R/src/$M"); fi
  echo "killing $victim pid $V"; kill -9 $V
  wait $DRV; rc=$?
  grep -v '^{\|^lean_make' "$W/$victim.out"
  check "$victim: driver exit 1 (got $rc), verdict fail" [ $rc -eq 1 -a "$(last_row "$W/R" | cut -f1,2)" = "$(printf 'E310BK.C038001\tfail')" ]
  check "$victim: no lean left right after" [ -z "$(procs "$W/R/src/$M")" ]
  sleep 25
  check "$victim: 25 s later no lean and no .olean" [ -z "$(procs "$W/R/src/$M")" -a -z "$(ls "$W/R/olean/E310BK" 2>/dev/null)" ]
}

case_C() {  # test_driver_es311.sh:48-57
  say "C: kill -9 of the driver with two compiles running"
  [ -d "$W/R" ] || mk_R
  wait_slots 2
  python3 "$D/drive_es310.py" "$W/R" --jobs 2 --start-gap 0 > "$W/C1.out" 2>&1 &
  local DRV=$!
  wait_lean "$W/R/src/E310BK" 4 $DRV
  until [ "$(pgrep -f "(^|/)lean -j1 .*$W/R/src" | wc -l)" -ge 2 ] || ! kill -0 $DRV 2>/dev/null; do sleep 0.5; done
  kill -9 $DRV; wait $DRV 2>/dev/null
  echo "orphans after the driver died: $(procs "$W/R/src" | wc -l) lean processes"
  echo "scopes: $(systemctl --user list-units --all --plain --no-legend --type=scope 'es310-*' | awk '{print $1}' | tr '\n' ' ')"
  run_drv "$W/C2.out" "$W/R" --jobs 2 --start-gap 0
  grep -v '^{"export' "$W/C2.out"
  check "C: the restart cleaned up the leftover scopes" has "$W/C2.out" "leftover scopes stopped"
  check "C: no lean left, no stray tmp" [ -z "$(procs "$W/R/src")" -a "$(find "$W/R/olean" -name '*.tmp*' | wc -l)" = 0 ]
  check "C: all three modules ok" [ "$(tail -3 "$W/R/run.tsv" | cut -f7 | sort -u)" = ok ]
}

case_D() {  # test_driver_es311.sh:59-60
  say "D: restart of a finished export"
  run_drv "$W/D.out" "$W/R" --jobs 2 --dry-run
  check "D: to_run 0, already_done 3" [ "$(jf "$W/D.out" "(d['to_run'], d['already_done'])")" = "(0, 3)" ]
}

case_E() {  # test_driver_es311.sh:62-70
  say "E: SIGTERM to the driver mid-compile"
  local rows DRV rc
  rows=$(wc -l < "$W/R/run.tsv")
  wait_slots 1
  python3 "$D/drive_es310.py" "$W/R" --jobs 1 --bench 1 --only E310BK.C000101 > "$W/E.out" 2>&1 &
  DRV=$!
  wait_lean "$W/R/src/E310BK/C000101.lean" 3 $DRV
  kill -TERM $DRV
  wait $DRV; rc=$?
  grep -v '^{\|^lean_make' "$W/E.out"
  sleep 2
  check "E: driver exit 130 (got $rc), no process, no stray tmp, no new row" [ $rc -eq 130 -a -z "$(procs "$W/R/src")" \
    -a "$(find "$W/R/olean" -name '*.tmp*' | wc -l)" = 0 -a "$(wc -l < "$W/R/run.tsv")" = "$rows" ]
}

case_F() {  # test_driver_es311.sh:72-76
  say "F: the corrupted chunk"
  mk_X
  wait_slots 1
  run_drv "$W/F.out" "$W/X" --jobs 1 --only E310BX.C000101
  grep -v '^{' "$W/F.out"
  check "F: verdict fail, no .olean" [ "$(last_row "$W/X" | cut -f2)" = fail -a "$(find "$W/X/olean" -name '*.olean' 2>/dev/null | wc -l)" = 0 ]
  check "F: decide proved the proposition false" grep -q "proved that the proposition" "$W"/X/logs/*.log
}

say "test_driver_es310.sh: WORKDIR $W, cases: $CASES; drive_es310.py sha256 $(sha256sum < "$D/drive_es310.py" | cut -c1-16)"
for c in $CASES; do
  case $c in G|H|I|J|K|L|M|N|S|T|A|B|C|D|E|F) "case_$c" ;; *) no "unknown case $c" ;; esac
done
say "summary: $PASSN passed, $FAILN failed"
[ $FAILN -eq 0 ]
