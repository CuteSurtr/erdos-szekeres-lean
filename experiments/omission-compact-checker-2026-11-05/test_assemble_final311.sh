#!/bin/bash
# Tests of assemble_final311.sh (6 November 2026). Everything is written under build/chain311/stubtest;
# nothing touches build/es311/full (read only) or logs/es311 except the summary
# logs/es311/assemble-tests.txt. Needs build/chain311 (complete, or at least its balanced side and catalogs).
#
#  1. A stub E311.Final: the fixed template of drive_es311.py without the two Root imports, its two
#     theorems with the template's exact statements but proved by `sorry`. Compiled against the chain.
#  2. assemble_final311.sh --test-stub: Final311Compact.lean against the stub. Expected: Lean exits 0
#     (the composition elaborates against the real chain), the statement reads ForcesConvexNGon 311 8,
#     sorryAx is among the axioms, and the script reports "not verified". If the chain is incomplete
#     (Residual32Bridge2650.Rows not built), the script must refuse; then only the balanced half (its
#     declaration copied verbatim from Final311Compact.lean) is compiled against the stub.
#  3. Run checks: (a) a copy of the export with an incomplete run.tsv is refused; (b) a process named like
#     the driver is refused; (c) --dry-run on the real, finished export (every check, no compile).
#  4. --test-stub with an extra LEAN_PATH root holding a copy of BalancedBudgets.olean: refused (shadowing).
#  5. --test-stub with build/ext as an extra root: refused.
#  6. The audit file's `#check @` / `#eval` lines on a module that exists (BalancedBudgets).
#  7. The report step on synthetic logs (no Lean): (a) a clean main log; (b) a main log of a lean killed by a
#     signal (time -v says "Exit status: 0", the scope 137); (c) a main log with a cgroup OOM kill.
#  8. Run checks (review fixes): a copy of the export with the full run.tsv but one chunk row's dependency
#     stamp changed is refused; A311_EXTRA_ROOT outside --test-stub and A311_EXPORT is refused.
#  9. The pins of check-chain (python helper on a fake tree of symlinks and copies, no Lean): unchanged it
#     passes with route same; refused when one library.json hash, or closure.json's toolchain sha256,
#     differs, or when a CompactChecker input is newer than the run's first compile; route rebuilt when a
#     catalog's October record differs.
# Every lean or lake process runs in a scope with MemoryMax=12G and MemorySwapMax=0, one at a time.
set -u -o pipefail
HERE=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
REPO=$(cd "$HERE/../.." && pwd)
T=$HERE/build/chain311/stubtest
OUT=$HERE/logs/es311/assemble-tests.txt
rm -rf "$T"; mkdir -p "$T/src/E311" "$T/path/CompactChecker" "$T/E311" "$T/shadow"
exec 3>&1
log() { echo "$*" | sed "s#$REPO#<repo>#g; s#$HOME#<home>#g" | tee -a "$T/summary.txt" >&3; }
: > "$T/summary.txt"
log "assemble_final311.sh tests, $(date -u +%FT%TZ); assemble_final311.sh sha256 $(sha256sum < "$HERE/assemble_final311.sh" | cut -c1-64)"

# 1. The stub.
python3 -I - "$HERE" > "$T/src/E311/Final.lean" <<'PY' || { log "FAIL: stub generation"; exit 1; }
import re, sys
sys.path.insert(0, sys.argv[1])
import drive_es311
t = drive_es311.FINAL_TEMPLATE
s = t.replace("import E311B.Root\n", "").replace("import E311R.Root\n", "")
s = s.replace("  CompactChecker.Bridge311Bal.balanced_of_root E311B.root\n", "  sorry\n")
s = s.replace("  CompactChecker.Bridge311Res.residual_of_root E311R.root\n", "  sorry\n")
stm = lambda x: re.findall(r"(theorem \w+ :.*?):=", x, re.S)
assert len(stm(t)) == 2 and stm(s) == stm(t), "statements differ from the template"
assert s.count("sorry") == 2 and "E311B" not in s and "E311R" not in s
sys.stdout.write(s)
PY
log "stub source: $(sha256sum < "$T/src/E311/Final.lean" | cut -c1-64); statements byte-identical to the template's"
for m in $(python3 -I - "$HERE" <<'PY'
import re, sys
from pathlib import Path
here = Path(sys.argv[1]); seen, todo = set(), ["Bridge311Bal", "Bridge311Res"]
while todo:
    m = todo.pop()
    if m not in seen:
        seen.add(m)
        todo += re.findall(r"^import CompactChecker\.(\w+)\s*$", (here / "CompactChecker" / f"{m}.lean").read_text(), re.M)
print(" ".join(sorted(seen)))
PY
); do ln -s "$HERE/build/CompactChecker/$m.olean" "$T/path/CompactChecker/$m.olean"; done
LAKE_LP=$(cd "$REPO" && systemd-run --user --scope --quiet -p MemoryMax=2G -p MemorySwapMax=0 nice -n 5 \
  lake env printenv LEAN_PATH)
(cd "$REPO" && LEAN_PATH="$LAKE_LP:$HERE/build/chain311/olean:$T/path" LEAN_NUM_THREADS=1 \
  systemd-run --user --scope --quiet -p MemoryMax=12G -p MemorySwapMax=0 -p CPUQuota=100% nice -n 5 \
  /usr/bin/time -v lean -j1 -R "$T/src" -o "$T/E311/Final.olean" "$T/src/E311/Final.lean") > "$T/stub-final.log" 2>&1
rc=$?
log "1. stub E311.Final: lean exit $rc; $(grep -c "declaration uses 'sorry'" "$T/stub-final.log") sorry warnings;" \
  "$(grep -E "^'E311\." "$T/stub-final.log" | tr '\n' ' ')"
[ $rc -eq 0 ] || { log "FAIL: the stub does not compile"; exit 1; }

# 2. The composition against the stub.
if [ -f "$HERE/build/chain311/olean/Residual32Bridge2650/Rows.olean" ]; then
A311_MEM=12G "$HERE/assemble_final311.sh" --test-stub "$T" > "$T/assemble-stub.out" 2>&1
rc=$?
J=$T/out/final311-compact.json
log "2. --test-stub: exit $rc (1 expected); $(tail -1 "$T/assemble-stub.out")"
python3 -I - "$J" <<'PY' | while read -r l; do log "   $l"; done
import json, sys
d = json.load(open(sys.argv[1]))
print(f"lean main compile: wall {d['main_compile']['wall']}, cgroup peak {int(d['main_compile']['cgroup_memory_peak'] or 0) / 2**30:.2f} GB, "
      f"RSS {int(d['main_compile']['max_rss_kb'] or 0) / 2**20:.2f} GB")
print(f"statement: {d['statement']}")
print(f"axioms: [{d['axioms']}]")
print(f"verified: {d['verified']}; problems: {d['problems']}")
print(f"imported modules: {d['imported_modules']} (library {d['library_modules']}); top-level: "
      + ", ".join(f"{k} {v[:12]}" for k, v in sorted(d['top_level_oleans'].items())))
ok = (not d["verified"] and "sorryAx" in (d["axioms"] or "") and d["statement"]
      == "ErdosSzekeres.Omission.Compact311.forces_convex_octagon_311 : ErdosSzekeres.ForcesConvexNGon 311 8"
      and d["problems"] == ["nonstandard axioms for ErdosSzekeres.Omission.Compact311.forces_convex_octagon_311: ["
                            + d["axioms"] + "]"])
print("RESULT " + ("as expected: Lean exit 0, ForcesConvexNGon 311 8, sorryAx, rejected only for its axioms"
                   if ok else "UNEXPECTED"))
PY
grep -q 'Exit status: 0' "$T/out/final311-compact.main.log" && log "   main compile log: Exit status 0" \
  || log "   UNEXPECTED: main compile did not exit 0"
else
# The chain is incomplete (Residual32Bridge2650.Rows not built): the script must refuse, and only the
# balanced half of Final311Compact.lean can be composed. Its declaration is copied verbatim from the file.
A311_MEM=12G "$HERE/assemble_final311.sh" --test-stub "$T" > "$T/assemble-stub.out" 2>&1
log "2. --test-stub with the chain incomplete: exit $? (1 expected): $(tail -1 "$T/assemble-stub.out" | cut -c1-300)"
mkdir -p "$T/half" "$T/path/E311"; ln -sf "$T/E311/Final.olean" "$T/path/E311/Final.olean"
python3 -I - "$HERE/assembly/Final311Compact.lean" > "$T/half/Compose311Balanced.lean" <<'PY' || { log "FAIL: half"; exit 1; }
import re, sys
src = open(sys.argv[1]).read()
decl = re.search(r"^theorem balanced_population_188 :.*?\n\n", src, re.S | re.M).group(0)
sys.stdout.write("import BalancedBudgets\nimport E311.Final\n\nopen ErdosSzekeres\n\n"
                 "namespace ErdosSzekeres.Omission.Compact311\n\n" + decl
                 + "#print axioms balanced_population_188\n\nend ErdosSzekeres.Omission.Compact311\n")
PY
(cd "$REPO" && LEAN_PATH="$LAKE_LP:$HERE/build/chain311/olean:$T/path" LEAN_NUM_THREADS=1 \
  systemd-run --user --scope --quiet -p MemoryMax=12G -p MemorySwapMax=0 -p CPUQuota=100% nice -n 5 \
  sh -c 'cg=/sys/fs/cgroup$(cut -d: -f3 /proc/self/cgroup); "$@"; rc=$?; echo "cgroup memory.peak: $(cat $cg/memory.peak)"; exit $rc' \
  sh /usr/bin/time -v lean -j1 -R "$T/half" "$T/half/Compose311Balanced.lean") > "$T/half.log" 2>&1
rc=$?
log "2'. balanced half (BalancedBudgets + stub E311.Final; declaration verbatim from Final311Compact.lean): lean exit $rc;" \
  "$(grep -c '^error\|error:' "$T/half.log") errors; $(tr '\n' ' ' < "$T/half.log" | tr -s ' ' | grep -o "'ErdosSzekeres.Omission.Compact311.balanced_population_188' depends on axioms: \[[^]]*\]");" \
  "wall $(sed -n 's/.*Elapsed (wall clock) time (h:mm:ss or m:ss): //p' "$T/half.log"), cgroup peak $(sed -n 's/^cgroup memory.peak: //p' "$T/half.log") B"
fi

# 3. Refusals of the run checks, and the dry run on the real export.
#  a. A copy of the export whose run.tsv keeps only the rows written before 22:30 UTC (mid chunk phase):
#     manifests copied, olean/ a symlink to the real (read-only) directory.
I=$T/export-incomplete; mkdir -p "$I"
cp "$HERE/build/es311/full/manifest-E311B.json" "$HERE/build/es311/full/manifest-E311R.json" "$I/"
ln -s "$HERE/build/es311/full/olean" "$I/olean"
awk -F'\t' 'NR == 1 || $1 < "2026-11-05T22:30:00Z"' "$HERE/build/es311/full/run.tsv" > "$I/run.tsv"
A311_EXPORT="$I" "$HERE/assemble_final311.sh" --dry-run > "$T/assemble-incomplete.out" 2>&1
rc=$?
log "3a. run.tsv with $(($(wc -l < "$I/run.tsv") - 1)) of 352 rows: exit $rc (1 expected): $(tail -1 "$T/assemble-incomplete.out" | cut -c1-300)"
#  b. A process whose command line looks like the driver's.
bash -c 'exec -a "python3 drive_es311.py build/es311/full --jobs 8" sleep 120' &
dummy=$!; sleep 1
"$HERE/assemble_final311.sh" --dry-run > "$T/assemble-driver.out" 2>&1
log "3b. a process named like the driver: exit $? (1 expected): $(tail -1 "$T/assemble-driver.out" | cut -c1-300)"
kill $dummy 2>/dev/null; wait $dummy 2>/dev/null
#  c. The real export, finished: every check, no compile.
"$HERE/assemble_final311.sh" --dry-run > "$T/assemble-dry.out" 2>&1
rc=$?
if [ -f "$HERE/build/chain311/olean/Residual32Bridge2650/Rows.olean" ]; then e="0 expected"; else e="1 expected: the chain is incomplete"; fi
log "3c. --dry-run on the real export: exit $rc ($e):"
while read -r l; do log "    $l"; done < "$T/assemble-dry.out"

# 4. A shadowed module.
cp "$HERE/build/chain311/olean/BalancedBudgets.olean" "$T/shadow/BalancedBudgets.olean"
A311_MEM=12G A311_EXTRA_ROOT="$T/shadow" "$HERE/assemble_final311.sh" --test-stub "$T" > "$T/assemble-shadow.out" 2>&1
log "4. extra root with a copy of BalancedBudgets.olean: exit $? (1 expected): $(tail -1 "$T/assemble-shadow.out" | cut -c1-400)"

# 5. build/ext on LEAN_PATH.
A311_MEM=12G A311_EXTRA_ROOT="$HERE/build/ext" "$HERE/assemble_final311.sh" --test-stub "$T" > "$T/assemble-ext.out" 2>&1
log "5. build/ext as an extra root: exit $? (1 expected): $(tail -1 "$T/assemble-ext.out" | cut -c1-400)"
cp "$T/summary.txt" "$OUT"

# 6. The audit file's Lean (the same `#check @` and `#eval` lines as assemble_final311.sh writes, on a
#    module that exists now): it must elaborate and list the imported modules.
mkdir -p "$T/audit"
cat > "$T/audit/AuditProbe.lean" <<'LEAN'
import BalancedBudgets
#check @OmissionBalanced.balanced_bound_of_hole_budget
open Lean in
#eval show CoreM Unit from do
  for m in (← getEnv).header.moduleNames do
    IO.println s!"module {m}"
LEAN
(cd "$REPO" && LEAN_PATH="$LAKE_LP:$HERE/build/chain311/olean" LEAN_NUM_THREADS=1 \
  systemd-run --user --scope --quiet -p MemoryMax=12G -p MemorySwapMax=0 -p CPUQuota=100% nice -n 5 \
  lean -j1 -R "$T/audit" "$T/audit/AuditProbe.lean") > "$T/audit.log" 2>&1
rc=$?
log "6. audit probe: lean exit $rc; $(grep -c '^module ' "$T/audit.log") module lines (BalancedBudgets listed: $(grep -cx 'module BalancedBudgets' "$T/audit.log")); #check prints: $(grep -m1 '^@\?OmissionBalanced.balanced_bound_of_hole_budget' "$T/audit.log" | cut -c1-160)"

# 7. The report step of assemble_final311.sh on synthetic logs (no Lean): a main log with exit 0 and a
#    standard axiom line, and an audit log with the statement and the probe's module list plus
#    Final311Compact, which is on no LEAN_PATH root here. Expected: one problem, that module not found.
cg0=$(printf 'cgroup memory.peak: 1\ncgroup memory.swap.peak: 0\ncgroup oom_kill: 0')
printf "'%s' depends on axioms: [propext, Classical.choice, Quot.sound]\n\tExit status: 0\n%s\n" \
  ErdosSzekeres.Omission.Compact311.forces_convex_octagon_311 "$cg0" > "$T/synthetic-main.log"
{ echo "ErdosSzekeres.Omission.Compact311.forces_convex_octagon_311 : ErdosSzekeres.ForcesConvexNGon 311 8"
  grep '^module ' "$T/audit.log"; echo "module Final311Compact"; printf '\tExit status: 0\n%s\n' "$cg0"; } > "$T/synthetic-audit.log"
PYH=$(python3 -I -c "import sys; t = open(sys.argv[1]).read(); print(t.split(\"<<'PYEOF'\\n\", 1)[1].split('\\nPYEOF\\n', 1)[0])" "$HERE/assemble_final311.sh")
CJ=$(python3 -I -c "$PYH" check-chain "$HERE" "$LAKE_LP" "" 2>&1)
SOME_OLEAN=$T/E311/Final.olean  # stands for the written result
synth() {  # synth MAINLOG MAINRC TAG
  python3 -I -c "$PYH" report "$HERE" "$1" "$2" "$T/synthetic-audit.log" 0 "$LAKE_LP:$HERE/build/chain311/olean" \
    "$T/synthetic-$3.json" "$T/synthetic-$3-imports.tsv.gz" synthetic same "" "$CJ" 12G \
    "$HERE/assembly/Final311Compact.lean" "$LAKE_LP" "$SOME_OLEAN" > "$T/synthetic-$3.out" 2>&1
}
synth "$T/synthetic-main.log" 0 a
log "7a. report on synthetic logs: exit $? (1 expected): $(cut -c1-300 "$T/synthetic-a.out")"
log "   $(python3 -I -c "import json,sys; d=json.load(open(sys.argv[1])); print('statement:', d['statement'], '| imported', d['imported_modules'], 'library', d['library_modules'], '(checked against library.json:', d['library_modules_checked_against_library_json'], ') | non-library', sorted(d['non_library_oleans'])[:3], '...')" "$T/synthetic-a.json" | cut -c1-300)"
#  b. lean killed by a signal: time -v reports "Exit status: 0" and "Command terminated by signal 9"; the scope 137.
{ echo "Command terminated by signal 9"; cat "$T/synthetic-main.log"; } > "$T/synthetic-main-signal.log"
synth "$T/synthetic-main-signal.log" 137 b
log "7b. report, lean killed by signal 9 (time -v: Exit status 0; scope 137): exit $? (1 expected): $(cut -c1-300 "$T/synthetic-b.out")"
#  c. a cgroup OOM kill recorded by the wrapper.
sed 's/^cgroup oom_kill: 0$/cgroup oom_kill: 1/' "$T/synthetic-main.log" > "$T/synthetic-main-oom.log"
synth "$T/synthetic-main-oom.log" 0 c
log "7c. report, cgroup oom_kill 1: exit $? (1 expected): $(cut -c1-300 "$T/synthetic-c.out")"
cp "$T/summary.txt" "$OUT"

# 8. Run checks added by the review fixes.
#  a. A copy of the export with the full run.tsv, one chunk row's deps_stamp changed (the row of E311B.C00022).
I2=$T/export-stamp; mkdir -p "$I2"
cp "$HERE/build/es311/full/manifest-E311B.json" "$HERE/build/es311/full/manifest-E311R.json" "$I2/"
ln -s "$HERE/build/es311/full/olean" "$I2/olean"
awk -F'\t' 'BEGIN{OFS="\t"} NR > 1 && $3 == "E311B.C00022" {$6 = "0000" substr($6, 5)} {print}' \
  "$HERE/build/es311/full/run.tsv" > "$I2/run.tsv"
A311_EXPORT="$I2" "$HERE/assemble_final311.sh" --dry-run > "$T/assemble-stamp.out" 2>&1
log "8a. run.tsv with one chunk's dependency stamp changed: exit $? (1 expected): $(tail -1 "$T/assemble-stamp.out" | cut -c1-300)"
#  b. A311_EXTRA_ROOT in the real mode (here --dry-run, which the real mode shares).
A311_EXTRA_ROOT="$T/shadow" "$HERE/assemble_final311.sh" --dry-run > "$T/assemble-extra-real.out" 2>&1
log "8b. A311_EXTRA_ROOT without --test-stub or A311_EXPORT: exit $? (1 expected): $(tail -1 "$T/assemble-extra-real.out" | cut -c1-300)"

# 9. The pins of check-chain on a fake tree: FR/experiments/x stands for HERE, with symlinks to the real files
#    except the ones a case changes (copies). FR/.lake, lean-toolchain and lake-manifest.json are symlinks.
FR=$T/fake/repo; FH=$FR/experiments/x
mkdir -p "$FH/build/chain311" "$FH/build/CompactChecker" "$FH/logs/es311"
for f in .lake lean-toolchain lake-manifest.json; do ln -s "$REPO/$f" "$FR/$f"; done
ln -s "$HERE/CompactChecker" "$FH/CompactChecker"; ln -s "$HERE/build/ext" "$FH/build/ext"
ln -s "$HERE/logs/es311/hardcap-rebuild.tsv" "$FH/logs/es311/hardcap-rebuild.tsv"
for f in build.tsv olean; do ln -s "$HERE/build/chain311/$f" "$FH/build/chain311/$f"; done
for f in "$HERE"/build/CompactChecker/*.olean; do ln -s "$f" "$FH/build/CompactChecker/$(basename "$f")"; done
FLP=$(echo "$LAKE_LP" | sed "s#$REPO/#$FR/#g")
RS=$(python3 -I -c "$PYH" check-run "$HERE" | python3 -I -c 'import json,sys; print(json.load(sys.stdin)["first_compile_start_utc"])')
pins() { cp "$HERE/build/chain311/closure.json" "$HERE/build/chain311/library.json" "$FH/build/chain311/"; }
chk() { python3 -I -c "$PYH" check-chain "$FH" "$FLP" "$RS" > "$T/pins-$1.out" 2>&1; }
edit_json() {  # edit_json FILE PYTHON-EXPRESSION-STATEMENT (d is the loaded JSON)
  python3 -I -c 'import json, sys; f = sys.argv[1]; d = json.load(open(f)); exec(sys.argv[2]); json.dump(d, open(f, "w"))' "$1" "$2"; }
pins; chk 0; r=$?
log "9a. fake tree, unchanged: exit $r (0 expected); $(python3 -I -c 'import json,sys; d=json.load(open(sys.argv[1])); print("route", d["route"], "| library verified", d["library_pinned_verified"], "| inputs", len(d["inputs"]), "older than", d["run_first_compile_utc"], "| equal to the hard-cap record:", sorted(k for k, v in d["inputs"].items() if v.get("equals_hardcap_record")))' "$T/pins-0.out" 2>&1 | cut -c1-400)"
pins; edit_json "$FH/build/chain311/library.json" 'd["modules"]["ErdosSzekeres.Omission.PopulationBounds"][1] = "0" * 64'
chk 1; log "9b. library.json hash of PopulationBounds changed: exit $? (1 expected): $(tail -1 "$T/pins-1.out" | cut -c1-300)"
pins; edit_json "$FH/build/chain311/closure.json" 'd["lean_toolchain_sha256"] = "0" * 64'
chk 2; log "9c. closure.json toolchain sha256 changed: exit $? (1 expected): $(tail -1 "$T/pins-2.out" | cut -c1-300)"
pins; rm "$FH/build/CompactChecker/Fcat62.olean"; cp "$HERE/build/CompactChecker/Fcat62.olean" "$FH/build/CompactChecker/"
chk 3; log "9d. a copy of Fcat62.olean written now (same bytes, newer mtime): exit $? (1 expected): $(tail -1 "$T/pins-3.out" | cut -c1-300)"
rm "$FH/build/CompactChecker/Fcat62.olean"; ln -s "$HERE/build/CompactChecker/Fcat62.olean" "$FH/build/CompactChecker/Fcat62.olean"
pins; edit_json "$FH/build/chain311/closure.json" 'd["modules"]["BalancedCoverCutsV2"]["recorded_olean_sha256"] = "0" * 64'
chk 4; r=$?
log "9e. October record of BalancedCoverCutsV2 changed: exit $r (0 expected); route $(python3 -I -c 'import json,sys; print(json.load(open(sys.argv[1]))["route"])' "$T/pins-4.out" 2>&1 | cut -c1-200) (rebuilt expected)"
cp "$T/summary.txt" "$OUT"
