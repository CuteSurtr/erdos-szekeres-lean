#!/bin/sh
# Pause the ES(8) <= 313 certificate check.
#   research-pause.sh          STOP: the coordinator and its Lean workers exit. Progress already
#                              recorded in .cache/es313/lean-export/kernel-check.json is kept
#                              (atomic per-module records); modules in flight are redone on resume.
#                              Releases all CPU and memory.
#   research-pause.sh --freeze FREEZE: SIGSTOP the coordinator and workers. Keeps their memory
#                              (several GB) resident; no work is lost. Undo with research-resume.sh.
. "$(dirname "$0")/research-common.sh"
C=$(coordinator_pids); W=$(worker_pids); L=$(wrapper_pids)
if [ -z "$C$W" ]; then echo "No certificate checker is running."; exit 0; fi
if [ "$1" = "--freeze" ]; then
  kill -STOP $C $W 2>/dev/null; echo frozen > "$RT/scheduler.mode"
  echo "Frozen coordinator [$C] and workers [$W]. Memory stays allocated."; exit 0
fi
kill -CONT $C $W 2>/dev/null
kill -INT $C 2>/dev/null          # coordinator stops dispatching; recorded progress is final
kill -TERM $W 2>/dev/null         # in-flight modules are not recorded and will be redone
for i in $(seq 1 60); do [ -z "$(coordinator_pids)$(worker_pids)" ] && break; sleep 1; done
[ -n "$(worker_pids)" ] && kill -KILL $(worker_pids) 2>/dev/null
[ -n "$(wrapper_pids)" ] && kill -TERM $(wrapper_pids) 2>/dev/null
echo stopped > "$RT/scheduler.mode"
python3 "$RT/state.py" --json "$RT/verification-state.json" >/dev/null 2>&1
echo "Stopped. $(python3 "$RT/state.py" | python3 -c 'import json,sys; s=json.load(sys.stdin); print(s["verified"], "verified,", s["remaining"], "remaining,", len(s["failed"]), "failed")')"
