#!/bin/sh
# Local monitor for the ES(8) <= 313 certificate check. Single instance; no model or network use.
# Every INTERVAL seconds (default 600): refresh .cache/runtime/verification-state.json, append one
# line to monitor.log, log genuine failures and resource-budget violations to failure-summary.log,
# restart a scheduler that died unexpectedly (at most 3 times; never after a genuine failure or a
# user pause), and run research-finalize.sh once when every module is verified.
. "$(dirname "$0")/research-common.sh"
INTERVAL="${INTERVAL:-600}"
# Single instance: an atomic lock directory holding the owner PID; a stale lock (dead owner) is taken over.
LOCK="$RT/monitor.lock"
if ! mkdir "$LOCK" 2>/dev/null; then
  OLD=$(cat "$LOCK/pid" 2>/dev/null)
  if [ -n "$OLD" ] && ps -p "$OLD" -o command= | grep -q research-monitor.sh; then echo "Monitor already running ($OLD)."; exit 0; fi
  rm -rf "$LOCK"; mkdir "$LOCK" || exit 1
fi
echo $$ > "$LOCK/pid"; echo $$ > "$RT/monitor.pid"
trap 'rm -rf "$LOCK"' EXIT
SWAP0=$(sysctl -n vm.swapusage | awk '{print $6}' | tr -d M)
restarts=0
while :; do
  python3 "$RT/state.py" --json "$RT/verification-state.json" > "$RT/.state.out" 2>&1
  V=$(python3 -c 'import json;s=json.load(open("'"$RT"'/verification-state.json"));print(s["verified"],s["expected_modules"],len(s["failed"]))' 2>/dev/null)
  set -- $V; VER=${1:-?}; EXP=${2:-?}; FAIL=${3:-?}
  C=$(coordinator_pids); W=$(worker_pids)
  RSS=$( [ -n "$W" ] && ps -o rss= -p $(echo $W | tr ' ' ',') | awk '{r+=$1} END {printf "%.1f", r/1048576}' || echo 0)
  FREE=$(memory_pressure | tail -1 | grep -o '[0-9]*%')
  SWAP=$(sysctl -n vm.swapusage | awk '{print $6}' | tr -d M)
  MODE=$(cat "$RT/scheduler.mode" 2>/dev/null)
  echo "$(date '+%F %T') verified=$VER/$EXP failed=$FAIL coordinator=$( [ -n "$C" ] && echo up || echo down) workers=$(echo $W | wc -w | tr -d ' ') leanRSS=${RSS}GB memfree=$FREE swapMB=$SWAP mode=$MODE" >> "$RT/monitor.log"
  [ "$FAIL" != "0" ] && [ "$FAIL" != "?" ] && echo "$(date '+%F %T') GENUINE FAILURE recorded: see verification-state.json" >> "$RT/failure-summary.log"
  awk -v s="$SWAP" -v s0="$SWAP0" 'BEGIN {exit !(s - s0 > 2048)}' && echo "$(date '+%F %T') BUDGET: swap grew by >2 GB (now ${SWAP} MB)" >> "$RT/failure-summary.log"
  [ "${FREE%\%}" -lt 15 ] 2>/dev/null && echo "$(date '+%F %T') BUDGET: memory free ${FREE}" >> "$RT/failure-summary.log"
  if [ -z "$C" ]; then
    if [ "$VER" = "$EXP" ] && [ "$FAIL" = "0" ]; then
      if [ ! -f "$RT/final-status.txt" ]; then
        echo "$(date '+%F %T') all modules verified; running research-finalize.sh" >> "$RT/monitor.log"
        "$REPO/scripts/research-finalize.sh" >> "$RT/finalize.log" 2>&1
      fi
      echo "$(date '+%F %T') monitor exiting: verification complete" >> "$RT/monitor.log"; exit 0
    elif [ "$MODE" = running ] && [ "$FAIL" = "0" ] && [ $restarts -lt 3 ]; then
      restarts=$((restarts + 1))
      echo "$(date '+%F %T') scheduler down unexpectedly; restart $restarts/3" >> "$RT/failure-summary.log"
      "$REPO/scripts/research-resume.sh" "$(cat "$RT/scheduler.workers" 2>/dev/null || echo 5)" >> "$RT/monitor.log" 2>&1
    fi
  fi
  sleep "$INTERVAL"
done
