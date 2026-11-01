#!/bin/bash
# Launch N lanes of c3resolve.py that share one unit list and one state directory.
# usage: launch_lanes.sh N [STATE_DIR] [ARCHIVE_DIR]
#   defaults: STATE_DIR = $C3P_STATE or ./c3pieces-state (never the committed run/), ARCHIVE_DIR = $C3P_ARCHIVE or
#   ./es7-c3-indispensable-2026-11-01
# Environment (all optional): GUARD_GB (default 34), C3P_CAP (3600), C3P_HEAP_MB (6000), C3P_HEAP_RETRY_MB (12000),
#   C3P_STACK_MB (2000), C3P_CAKE_SLOTS (2), C3P_MIN_FREE_GB (30), C3P_MAX_RSS_MB (0 = off), C3P_ZSTD_THREADS (1).
#   C3P_EXTRA_ARGS: extra runner arguments for every lane, e.g. "--retry-failed" after inspecting failures.
# Stop gracefully: touch STATE_DIR/STOP (each lane exits before its next claim).  Progress: --status (see below).
# After the run: python3 -I -B tools/verify_archive.py list/units.txt STATE_DIR/out.jsonl ARCHIVE_DIR
set -euo pipefail
N=${1:?usage: launch_lanes.sh N [STATE_DIR] [ARCHIVE_DIR]}
C=$(cd "$(dirname "$0")/.." && pwd)   # the directory holding tools/ and list/
STATE=${2:-${C3P_STATE:-$PWD/c3pieces-state}}
ARCHIVE=${3:-${C3P_ARCHIVE:-$PWD/es7-c3-indispensable-2026-11-01}}
export GUARD_GB=${GUARD_GB:-34}
mkdir -p "$STATE"
if [ -e "$STATE/STOP_SAT" ]; then echo "refusing: $STATE/STOP_SAT exists (a piece came out SAT; inspect first)"; exit 1; fi
rm -f "$STATE/STOP"
for i in $(seq 1 "$N"); do
  nohup python3 -I -B "$C/tools/c3resolve.py" --list "$C/list/units.txt" --state "$STATE" --lane "L$i" \
      --archive "$ARCHIVE" ${C3P_EXTRA_ARGS:-} >> "$STATE/lane$i.stdout" 2>&1 &
  echo "lane L$i pid $!"
  sleep 3
done
echo "status: python3 -I -B $C/tools/c3resolve.py --list $C/list/units.txt --state $STATE --status"
