#!/bin/sh
# Resume the ES(8) <= 313 certificate check (only one coordinator is ever allowed).
# Thaws a frozen run, otherwise starts the checker with --resume: recorded modules whose
# .olean still matches its SHA-256 are skipped, everything else is (re)checked.
# Usage: research-resume.sh [WORKERS]   (default 5; lowered priority: nice 10)
. "$(dirname "$0")/research-common.sh"
WORKERS="${1:-5}"
C=$(coordinator_pids)
if [ -n "$C" ]; then
  if [ "$(cat "$RT/scheduler.mode" 2>/dev/null)" = frozen ]; then
    kill -CONT $C $(worker_pids) 2>/dev/null; echo running > "$RT/scheduler.mode"; echo "Thawed coordinator [$C]."
  else echo "Already running (coordinator [$C]); not starting a second one."; fi
  exit 0
fi
cd "$REPO"
[ -f "$RT/scheduler.log" ] && mv "$RT/scheduler.log" "$RT/scheduler-$(date +%Y%m%dT%H%M%S).log"
nohup nice -n 10 lake env python3 "$CHECKER" "$EXPORT" --resume --workers "$WORKERS" --memory 6000 \
  > "$RT/scheduler.log" 2>&1 &
echo "$WORKERS" > "$RT/scheduler.workers"; echo running > "$RT/scheduler.mode"; date +%s > "$RT/scheduler.started"
python3 "$RT/state.py" | python3 -c 'import json,sys; print(json.load(sys.stdin)["verified"])' > "$RT/scheduler.start_verified"
sleep 3; echo "Started checker with $WORKERS workers (nice 10); log: .cache/runtime/scheduler.log"
