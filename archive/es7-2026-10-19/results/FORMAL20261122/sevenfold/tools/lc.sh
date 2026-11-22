#!/bin/bash
# lc.sh std|geo MODULE [MODULE ...]: compile each module (src/<Mod path>.lean -> olean/<Mod path>.olean) in order,
# with /usr/bin/time -v; appends to logs/build.log. Stops at the first failure.
set -u
. /home/jay/research/data/formalize-20261122/sevenfold/tools/env.sh
kind=$1; shift
case "$kind" in geo) export LEAN_PATH="$LP_GEO";; self) export LEAN_PATH="$LP_SELF";; *) export LEAN_PATH="$LP_STD";; esac
cd "$W/src"
for mod in "$@"; do
  f="${mod//.//}.lean"; o="$W/olean/${mod//.//}.olean"; mkdir -p "$(dirname "$o")"
  echo "=== $(date -Is) $kind $mod ($(sha256sum "$f" | cut -c1-16))" >> "$W/logs/build.log"
  /usr/bin/time -v "$LEAN" -j1 -R "$W/src" -o "$o" "$f" > "$W/logs/last.out" 2> "$W/logs/last.time"
  rc=$?
  cat "$W/logs/last.out" >> "$W/logs/build.log"
  grep -E "Elapsed|Maximum resident" "$W/logs/last.time" >> "$W/logs/build.log"
  echo "rc=$rc" >> "$W/logs/build.log"
  [ $rc -ne 0 ] && { rm -f "$o"; exit $rc; }
done
exit 0
