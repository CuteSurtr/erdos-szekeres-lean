#!/bin/bash
# Incremental cycles of logs/es310/OPERATOR.md section A2 while the budget-64 campaign runs (6 November 2026).
# ES(8) <= 310 is NOT proved by anything this script does. Each cycle, strictly in order:
#   1. export every closed context not yet exported (frozen exporter, --per-word 16)
#   2. merge --partial
#   3. coverage --partial with the exact frozen exporter pin
#   4. compile the new chunks with drive_es310.py (2 jobs, nice 10, Tctl < 80 C, start gap 60 s), no Root/Final
# then sleep CYCLE seconds. Fine exit codes per step are those of OPERATOR.md; 4 (lock held) means retry next
# cycle. Any other code stops the loop, writes $OUT/INCR-STOPPED.txt with the reason and exits with that code;
# nothing is deleted. The loop ends by itself (exit 0) when campaign.log says ALL 4096 CONTEXTS CLOSED (the
# final steps of OPERATOR.md section B are run by hand) or when $OUT/STOP-INCR exists.
set -u
D=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
C=/home/jay/research/data/es8-b64-pilot-20261105
SRC=/home/jay/research/lean/erdos-szekeres-lean/experiments/omission-cover-certificates-2026-10-10/balanced-v2-source.json
OUT=$D/build/es310/full
K=16
CYCLE=${CYCLE:-3600}
cd "$D" || exit 1
mkdir -p "$OUT" logs/es310
PIN=$(sed -n 's/^EXPORTER_SHA256=\([0-9a-f]\{64\}\)$/\1/p' assemble_final310.sh)
[ ${#PIN} -eq 64 ] || { echo "incr: no frozen exporter pin" >&2; exit 1; }
say() { echo "$(date '+%F %T') $*"; }
stop() { say "STOP: $1"; printf '%s %s\n' "$(date '+%F %T')" "$1" >> "$OUT/INCR-STOPPED.txt"; exit "$2"; }
n=0
while true; do
  n=$((n + 1))
  [ -e "$OUT/STOP-INCR" ] && { say "STOP-INCR present; loop ends"; exit 0; }
  done_campaign=0
  grep -q ' ALL 4096 CONTEXTS CLOSED$' "$C/campaign/campaign.log" && done_campaign=1
  if [ -e "$C/campaign/WITNESS-ALERT.txt" ] || compgen -G "$C/runs/*WITNESS*" > /dev/null; then
    touch "$OUT/STOP"; stop "WITNESS file in the campaign: nothing more is run; tell the user" 5
  fi
  say "cycle $n: export"
  systemd-run --user --scope --quiet -p MemoryMax=4G -p MemorySwapMax=0 nice -n 19 \
    python3 -I export_es310.py --campaign "$C" --source "$SRC" --out "$OUT" --all-closed \
    --per-word $K --chunk-leaves 12000 --block-leaves 64 >> "$OUT/export-runs.jsonl" 2>> logs/es310/export-full.err
  rc=$?; say "export exit $rc: $(tail -1 "$OUT/export-runs.jsonl" | cut -c1-300)"
  case $rc in 0) ;; 4) say "export lock held; next cycle"; sleep "$CYCLE"; continue ;;
    *) stop "export exit $rc (see $OUT/export-runs.jsonl and logs/es310/export-full.err)" "$rc" ;; esac
  say "cycle $n: merge --partial"
  nice -n 19 python3 -I merge_es310.py "$OUT" --partial >> "$OUT/merge-runs.jsonl" 2>> logs/es310/merge-full.err
  rc=$?; say "merge exit $rc"
  case $rc in 0) ;; 4) sleep "$CYCLE"; continue ;; *) stop "merge exit $rc" "$rc" ;; esac
  say "cycle $n: coverage --partial"
  nice -n 19 python3 -I coverage_es310.py "$OUT" --partial --campaign "$C" --jobs 2 --cache "$OUT/coverage-cache.json" \
    --exporter-sha256 "$PIN" --report logs/es310/coverage-partial-last.json > /dev/null 2>> logs/es310/coverage-full.err
  rc=$?; say "coverage exit $rc"
  case $rc in 0) ;; 4) sleep "$CYCLE"; continue ;; *) stop "coverage exit $rc (logs/es310/coverage-partial-last.json)" "$rc" ;; esac
  if pgrep -f 'drive_es310\.py.*es310/full' > /dev/null; then
    say "a driver is already running on $OUT; compile skipped this cycle"
  elif [ -e "$OUT/STOP" ]; then
    say "STOP file present: compile skipped"
  else
    say "cycle $n: compile (drive_es310.py, 2 jobs)"
    python3 -I drive_es310.py "$OUT" --reuse build/es311/full:E311R --no-final --jobs 2 --nice 10 \
      --max-tctl 80 --start-gap 60 --memory 12G --root-memory 24G --campaign-dir "$C" >> logs/es310/drive-full.log 2>&1
    rc=$?; say "driver exit $rc"
    case $rc in 0|3) ;; *) stop "driver exit $rc (logs/es310/drive-full.log)" "$rc" ;; esac
  fi
  if [ $done_campaign -eq 1 ]; then say "campaign says ALL 4096 CONTEXTS CLOSED; incremental loop ends (run OPERATOR.md B by hand)"; exit 0; fi
  say "cycle $n done; sleeping $CYCLE s"
  sleep "$CYCLE"
done
