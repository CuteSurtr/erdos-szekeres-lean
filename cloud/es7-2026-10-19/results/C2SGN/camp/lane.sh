#!/bin/bash
# Compact-encoding lane (check and delete). Claims the next unit of UNITS (a cube name of CUBES, or COVER), builds the
# CNF (BASE + cube literals as units; for COVER the file COVERCNF), runs CaDiCaL --lrat with a time cap, then lrat-check
# and cake_lpr (heap HEAP MB, one cake_lpr at a time across lanes via camp/cakelock), records size, SHA-256 and verdicts
# in camp/results.jsonl, and deletes the proof once both checkers accept it (otherwise moves it to camp/failed).
# Waits while c2c/p8/STOP exists (memory guard). No new claim when less than 900 s remain before END.
# usage: lane.sh END CAP HEAP UNITS CUBES BASE COVERCNF
S=${WORK:?set WORK to the work directory}
B=$S/local/bin; D=$S/sgn/camp; END=$1; CAP=$2; HEAP=$3; UNITS=$4; CUBES=$5; BASE=$6; COVER=$7
while :; do
  left=$((END - $(date +%s))); [ $left -lt 900 ] && exit 0
  if [ -e $S/c2c/p8/STOP ]; then sleep 30; continue; fi
  name=""
  while read -r u; do k=${u//\//_}; mkdir $D/claims/$k 2>/dev/null && { name=$u; break; }; done < $UNITS
  [ -z "$name" ] && exit 0
  k=${name//\//_}; lim=$CAP; [ $left -lt $lim ] && lim=$left
  P=$D/work/$k.lrat; O=$D/out/$k.out
  if [ "$name" = COVER ]; then F=$COVER; n=0; else
    F=$D/work/$k.cnf
    lits=$(grep -F "$name " $CUBES | awk -v nm="$name" '$1 == nm' | cut -d' ' -f2-); n=$(echo $lits | wc -w | tr -d ' ')
    awk -v n=$n '/^p cnf/ {print $1, $2, $3, $4 + n; next} {print}' $BASE > $F; for l in $lits; do echo "$l 0"; done >> $F
  fi
  cnfsha=$(shasum -a 256 $F | cut -d' ' -f1)
  t0=$(date +%s); nice -n 5 $B/cadical -t $lim --lrat --binary=false $F $P > $O 2>&1; t1=$(date +%s)
  st=$(grep -m1 '^s ' $O | cut -c3-); [ -z "$st" ] && st=UNKNOWN
  ts=$(grep 'total process time since initialization' $O | awk '{print $(NF-1)}')
  rec="\"unit\": \"$name\", \"status\": \"$st\", \"cap_s\": $lim, \"solve_s\": ${ts:-null}, \"solve_wall_s\": $((t1-t0)), \"cube_literals\": $n, \"cnf_sha256\": \"$cnfsha\""
  if [ "$st" = "UNSATISFIABLE" ]; then
    pb=$(stat -f %z $P); psha=$(shasum -a 256 $P | cut -d' ' -f1)
    t2=$(date +%s); lc=$(nice -n 5 $B/lrat-check $F $P 2>&1 | grep -m1 -E 'VERIFIED|FAIL|rror'); t3=$(date +%s)
    until mkdir $D/cakelock 2>/dev/null; do sleep 5; done
    t4=$(date +%s); ck=$(nice -n 5 $B/cake_lpr --CML_HEAP_SIZE=$HEAP --CML_STACK_SIZE=1000 $F $P 2>&1 | grep -m1 -E 's VERIFIED|exhausted|rror|FAIL'); t5=$(date +%s)
    rmdir $D/cakelock; [ -z "$ck" ] && ck="no verdict line"
    if [ "$lc" = "c VERIFIED" ] && [ "$ck" = "s VERIFIED UNSAT" ]; then rm -f $P; kept=false; else mv $P $D/failed/; kept=true; fi
    rec="$rec, \"proof_bytes\": $pb, \"proof_sha256\": \"$psha\", \"lrat_check\": \"$lc\", \"lrat_check_s\": $((t3-t2)), \"cake_lpr\": \"$ck\", \"cake_s\": $((t5-t4)), \"cake_heap_mb\": $HEAP, \"proof_kept\": $kept"
  else
    [ "$st" = "SATISFIABLE" ] && cp $O $D/SAT_$k.out
    rm -f $P
  fi
  [ "$name" = COVER ] || rm -f $F
  echo "{$rec, \"finished\": \"$(date -u +%H:%M:%SZ)\"}" >> $D/results.jsonl
done
