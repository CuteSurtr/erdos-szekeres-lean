#!/bin/bash
# fivefold (25 Nov 2026): compile src/Geo5/Main5.lean against the sevenfold build (read-only: its LP_SELF = Mathlib
# from ENCBLEAN geo's checkout + sevenfold's own olean store); output olean/Geo5/Main5.olean. Appends to logs/build.log.
set -u
. /home/jay/research/data/formalize-20261122/sevenfold/tools/env.sh
F=/home/jay/research/data/formalize-20261122/fivefold
export LEAN_PATH="$LP_SELF:$F/olean"
cd "$F/src"
echo "=== $(date -Is) Geo5.Main5 ($(sha256sum Geo5/Main5.lean | cut -c1-16))" >> "$F/logs/build.log"
/usr/bin/time -v "$LEAN" -j1 -R "$F/src" -o "$F/olean/Geo5/Main5.olean.tmp" Geo5/Main5.lean > "$F/logs/last.out" 2> "$F/logs/last.time"
rc=$?
cat "$F/logs/last.out" >> "$F/logs/build.log"
grep -E "Elapsed|Maximum resident" "$F/logs/last.time" >> "$F/logs/build.log"
echo "rc=$rc" >> "$F/logs/build.log"
if [ $rc -eq 0 ]; then mv "$F/olean/Geo5/Main5.olean.tmp" "$F/olean/Geo5/Main5.olean"; else rm -f "$F/olean/Geo5/Main5.olean.tmp"; fi
exit $rc
