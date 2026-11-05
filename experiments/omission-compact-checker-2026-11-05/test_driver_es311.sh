#!/bin/bash
# Kill and restart tests of drive_es311.py (6 November 2026, review fixes). Usage: test_driver_es311.sh WORKDIR
# WORKDIR gets copies of two trial exports (build/es311/trial/R-L1000-B64: three residual modules of
# 935-1,000 leaves; BX-L1000-B64: the corrupted balanced chunk). Every compile is the driver's own (one
# lean -j1 per scope, MemoryMax=12G, MemorySwapMax=0, nice 5); at most 2 run at once.
#   A. kill -9 of /usr/bin/time mid-compile (lean would be orphaned): verdict fail, no lean left, no .olean
#   B. kill -9 of the scope's top process (sh) mid-compile: the same
#   C. kill -9 of the driver itself with two compiles running: they survive as orphans; the next start
#      stops their scopes, deletes their temporary .olean files and compiles all three modules: ok
#   D. a further start runs nothing
#   E. SIGTERM to the driver mid-compile (--bench 1): no process, no .olean, no row
#   F. the corrupted chunk: verdict fail
#   G. a TSV with the old header and three ok rows (the trial's): upgraded in place, all three still done
set -u -o pipefail
D=$(cd "$(dirname "$0")" && pwd)
W=$(mkdir -p "$1" && cd "$1" && pwd)
T=$D/build/es311/trial
say() { echo "== $(date -u +%FT%TZ) $*"; }
fresh() {  # fresh copy of a trial export without its build state
  rm -rf "$W/$1"; mkdir -p "$W/$1/src"
  cp "$T/$2"/manifest-*.json "$W/$1/"; cp -r "$T/$2"/src/* "$W/$1/src/"
}
procs() { pgrep -af "lean -j1 .*$1" | grep -v pgrep || true; }
drive() { python3 "$D/drive_es311.py" "$@" 2>&1 | grep -v '^lean_make'; }
wait_lean() {  # until the lean process of module file $1 runs, then $2 more seconds
  # lean runs through the elan proxy, so its argv[0] is the toolchain's full path
  until pgrep -f "(^|/)lean -j1 .*$1" > /dev/null; do sleep 0.5; done; sleep "$2"
}
last_row() { tail -1 "$1/run.tsv" | cut -f3,7,8,11,21; }

fresh R R-L1000-B64
M=E311R/C00380.lean
for victim in time sh; do
  say "${victim}: kill -9 of the '$victim' process of the compile of $M"
  python3 "$D/drive_es311.py" "$W/R" --jobs 1 --only E311R.C00380 > "$W/$victim.out" 2>&1 &
  DRV=$!
  wait_lean "$W/R/src/$M" 4
  if [ $victim = time ]; then V=$(pgrep -f "^/usr/bin/time -v lean -j1 .*$W/R/src/$M"); else
    V=$(pgrep -f "^sh -c cg=.*$W/R/src/$M"); fi
  echo "killing $victim pid $V"; kill -9 $V
  wait $DRV; echo "driver exit $?"; grep -v '^{\|^lean_make' "$W/$victim.out"
  echo "row (module verdict exit wall cg_peak_kb): $(last_row "$W/R")"
  echo "lean processes left right after: [$(procs "$W/R/src/$M")]"
  sleep 25
  echo "25 s later: processes [$(procs "$W/R/src/$M")]; files in olean/E311R: [$(ls "$W/R/olean/E311R" 2>/dev/null | tr '\n' ' ')]"
done

say "C: kill -9 of the driver with two compiles running"
python3 "$D/drive_es311.py" "$W/R" --jobs 2 > "$W/C1.out" 2>&1 &
DRV=$!
wait_lean "$W/R/src/E311R" 4
kill -9 $DRV; wait $DRV 2>/dev/null
echo "orphans after the driver died: $(procs "$W/R/src" | wc -l) lean processes"
echo "scopes: $(systemctl --user list-units --all --plain --no-legend --type=scope 'es311-*' | awk '{print $1}' | tr '\n' ' ')"
drive "$W/R" --jobs 2 | grep -v '^{"export'
echo "after the restart: lean processes [$(procs "$W/R/src")]; stray tmp: $(find "$W/R/olean" -name '*.tmp*' | wc -l)"
cut -f3,7,8 "$W/R/run.tsv" | tail -4

say "D: restart of a finished export"
drive "$W/R" --jobs 2 | head -1 | python3 -c "import json,sys; d=json.load(sys.stdin); print('to_run', d['to_run'], 'already_done', d['already_done'])"

say "E: SIGTERM to the driver mid-compile"
rows=$(wc -l < "$W/R/run.tsv")
python3 "$D/drive_es311.py" "$W/R" --jobs 1 --bench 1 --only E311R.C00001 > "$W/E.out" 2>&1 &
DRV=$!
wait_lean "$W/R/src/E311R/C00001.lean" 3
kill -TERM $DRV
wait $DRV; echo "driver exit $?"; grep -v '^{\|^lean_make' "$W/E.out"
sleep 2
echo "processes [$(procs "$W/R/src")]; stray tmp: $(find "$W/R/olean" -name '*.tmp*' | wc -l); rows before $rows, after $(wc -l < "$W/R/run.tsv")"

say "F: the corrupted chunk"
fresh X BX-L1000-B64
drive "$W/X" --jobs 1 --only E311BX.C00001 | grep -v '^{'
echo "row: $(last_row "$W/X"); .olean files: $(find "$W/X/olean" -name '*.olean' 2>/dev/null | wc -l)"
grep -m1 "proved that the proposition" "$W"/X/logs/*.log | cut -c1-160

say "G: an old-header TSV with three ok rows"
rm -rf "$W/G"; cp -r "$T/R-L1000-B64" "$W/G"
head -1 "$W/G/run.tsv" | tr '\t' ' '
drive "$W/G" --jobs 1 --dry-run | head -1 | python3 -c "import json,sys; d=json.load(sys.stdin); print('to_run', d['to_run'], 'already_done', d['already_done'])"
head -1 "$W/G/run.tsv" | tr '\t' ' '; echo "rows: $(($(wc -l < "$W/G/run.tsv") - 1)), fields per row: $(tail -1 "$W/G/run.tsv" | awk -F'\t' '{print NF}')"
say "done"
