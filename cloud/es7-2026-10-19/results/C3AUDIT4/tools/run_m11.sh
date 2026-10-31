#!/bin/bash
# usage: run_m11.sh FILELIST SNAPDIR OUTDIR COMMIT   (composes C3U2 compose.py and mycompose(+myh6), each with and
# without --mirror-h6, on the record files listed in FILELIST, taken from COMMIT via git archive)
set -e
FLIST=$1; SNAP=$2; OUT=$3; COMMIT=$4
T=$(cd "$(dirname "$0")" && pwd)
RES=$T/../..
BASE=/tmp/claude-0/-home-user-erdos-szekeres-lean/a2372e58-e319-59b7-94d3-805904fed989/scratchpad/base/b117.cnf
mkdir -p "$SNAP" "$OUT"
(cd "$RES" && git archive "$COMMIT" $(cat "$FLIST")) | tar -x -C "$SNAP"
cd "$SNAP"
FL=$(cat "$FLIST" | tr '\n' ' ')
for w in mine C3U2; do
  for h in "" "--mirror-h6"; do
    W=$w; [ $w = C3U2 ] && W=$RES/C3U2/tools
    ( start=$(date +%s); python3 "$T/runcomp.py" $W 11 7 "$BASE" $FL $h > "$OUT/${w}${h}.json" 2> "$OUT/${w}${h}.err"; echo "secs $(( $(date +%s) - start ))" >> "$OUT/${w}${h}.err" ) &
  done
done
wait
