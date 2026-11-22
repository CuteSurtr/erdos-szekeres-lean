#!/bin/bash
# build_all.sh: from an empty olean/ store, build every module from source (Std part, then the Mathlib part),
# then run the static audit. Log: logs/build.log (appended), logs/build_all.log (this run's summary).
set -u
W=/home/jay/research/data/formalize-20261122/sevenfold
rm -rf "$W/olean"; mkdir -p "$W/olean"
echo "=== build_all $(date -Is)" >> "$W/logs/build.log"
"$W/tools/build_std.sh" || { echo "build_std FAILED"; exit 1; }
"$W/tools/build_self.sh" || { echo "build_self FAILED"; exit 1; }
python3 -I "$W/tools/audit.py" > "$W/logs/audit.log" 2>&1; a=$?
(cd "$W/olean" && sha256sum EncBO/*.olean Geo7/*.olean) > "$W/logs/own_oleans.sha256"
echo "build_all done $(date -Is); audit exit $a"
exit $a
