#!/bin/bash
# usage: launch_run.sh RUNDIR CNF NX NWORKERS HOURS [extra cnc2 args]
# Runs cnc2.py in the foreground (start it in the background yourself) and appends its final
# JSON line to RUNDIR/final.json.
D="$(cd "$(dirname "$0")" && pwd)"
RUN="$1"; CNF="$2"; NX="$3"; NW="$4"; H="$5"; shift 5
mkdir -p "$RUN"
python3 "$D/cnc2.py" "$CNF" "$NX" "$RUN" "$NW" --hours "$H" "$@" > "$RUN/final.json" 2> "$RUN/driver.err"
