#!/bin/bash
# One cover certificate for the compact encoding: CaDiCaL --lrat on a cover CNF (time cap CAP), lrat-check, then
# cake_lpr (heap HEAP MB) while holding camp/cakelock, a JSON record in camp/results.jsonl, and deletion of the proof
# once both checkers accept it (otherwise it is moved to camp/failed). The cover CNF itself is kept.
# usage: covercheck.sh NAME COVERCNF CAP HEAP
D=${WORK:?set WORK to the work directory}/sgn/camp
B=${WORK:?set WORK to the work directory}/local/bin
NAME=$1; F=$2; CAP=$3; HEAP=$4
PROOF="$D/work/cover_$NAME.lrat"; OUT="$D/out/cover_$NAME.out"
cnfsha=$(shasum -a 256 "$F" | cut -d' ' -f1)
t0=$(date +%s); nice -n 5 "$B/cadical" -t "$CAP" --lrat --binary=false "$F" "$PROOF" > "$OUT" 2>&1; t1=$(date +%s)
st=$(grep -m1 '^s ' "$OUT" | cut -c3-); [ -z "$st" ] && st=UNKNOWN
ts=$(grep 'total process time since initialization' "$OUT" | awk '{print $(NF-1)}')
rec="\"unit\": \"$NAME\", \"status\": \"$st\", \"cap_s\": $CAP, \"solve_s\": ${ts:-null}, \"solve_wall_s\": $((t1-t0)), \"cnf_sha256\": \"$cnfsha\""
if [ "$st" = "UNSATISFIABLE" ]; then
  pb=$(stat -f %z "$PROOF"); psha=$(shasum -a 256 "$PROOF" | cut -d' ' -f1)
  t2=$(date +%s); lc=$(nice -n 5 "$B/lrat-check" "$F" "$PROOF" 2>&1 | grep -m1 -E 'VERIFIED|FAIL|rror'); t3=$(date +%s)
  until mkdir "$D/cakelock" 2>/dev/null; do sleep 5; done
  t4=$(date +%s); ck=$(nice -n 5 "$B/cake_lpr" --CML_HEAP_SIZE="$HEAP" --CML_STACK_SIZE=1000 "$F" "$PROOF" 2>&1 | grep -m1 -E 's VERIFIED|exhausted|rror|FAIL'); t5=$(date +%s)
  rmdir "$D/cakelock"; [ -z "$ck" ] && ck="no verdict line"
  if [ "$lc" = "c VERIFIED" ] && [ "$ck" = "s VERIFIED UNSAT" ]; then rm -f "$D/work/cover_$NAME.lrat"; kept=false
  else mv "$PROOF" "$D/failed/"; kept=true; fi
  rec="$rec, \"proof_bytes\": $pb, \"proof_sha256\": \"$psha\", \"lrat_check\": \"$lc\", \"lrat_check_s\": $((t3-t2)), \"cake_lpr\": \"$ck\", \"cake_s\": $((t5-t4)), \"cake_heap_mb\": $HEAP, \"proof_kept\": $kept"
else
  rm -f "$D/work/cover_$NAME.lrat"
fi
echo "{$rec, \"finished\": \"$(date -u +%H:%M:%SZ)\"}" >> "$D/results.jsonl"
