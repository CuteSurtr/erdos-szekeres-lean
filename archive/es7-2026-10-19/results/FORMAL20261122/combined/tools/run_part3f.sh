#!/bin/bash
# combined part 3 chain, resume g (26 Nov 2026; PART3.md §7, 10:34): only §6 item 3, the import audit. Resume f
# (run_part3e.sh) stopped at audit3: audit3.py's default log list included logs/ES302Final.log, which has no module
# list; Audit3.log alone carries it. The N66 driver restart of run_part3e.sh is dropped (re-solve finished 06:13).
set -u
W=/home/jay/research/data/formalize-20261122/combined
LOG=$W/data/part3_run.log; SUM=$W/data/part3_summary.json
log() { echo "$(date '+%F %T') $*" >> "$LOG"; }
done_json() { printf '{"time": "%s", "stage": "%s", "status": "%s"}\n' "$(date '+%F %T')" "$1" "$2" > "$SUM"; }
fail() { log "STOP at $1: $2"; done_json "$1" "STOPPED: $2"; exit 1; }
cd "$W"
log "chain start (resume g: audit3 only, logs/Audit3.log as its one module list; ES302Final, Bad302, Audit3 done by f; PART3.md §7)"
grep -q 'lean_rc=0' logs/Audit3.log || fail audit3 "Audit3 lean_rc"
tools/start3.sh audit3 2048 10800 1 python3 -I -B tools/audit3.py logs/Audit3.log \
  || fail audit3 "audit3.py reported problems (data/audit3.json)"
log "audit3 ok"
done_json all "OK: finish recipe, links3, ES302Final, Bad302 control, Audit3, audit3 (acceptance needs the advisor)"
log "chain end"
