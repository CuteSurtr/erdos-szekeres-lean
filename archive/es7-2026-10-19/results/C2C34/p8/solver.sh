#!/bin/bash
# P8 solver lane. Claims the next unit of p8/units.txt, builds its CNF (base c34h_final.cnf + subcase cube units, or
# p8/cover.cnf), runs CaDiCaL --lrat with a time cap and lrat-check on an UNSAT proof, and hands the proof to the
# checker lane through p8/queue (proof + JSON record). Waits while the queue holds QMAX proofs, while p8/STOP exists,
# or while free memory is below 35%. No new claim when less than 900 s remain before END.  usage: solver.sh END CAP QMAX
S=${WORK:?set WORK to the work directory}
C=$S/c2c; B=$S/local/bin; P8=$C/p8; END=$1; CAP=$2; QMAX=$3; BASE=$C/c34h_final.cnf
while :; do
  left=$((END - $(date +%s))); [ $left -lt 900 ] && exit 0
  q=$(ls $P8/queue/*.lrat 2>/dev/null | wc -l | tr -d ' ')
  free=$(memory_pressure 2>/dev/null | awk '/free percentage/ {gsub("%", "", $NF); print $NF}')
  if [ -e $P8/STOP ] || [ "$q" -ge "$QMAX" ] || [ "${free:-100}" -lt 35 ]; then sleep 30; continue; fi
  name=""
  while read -r u; do mkdir $P8/claims/$u 2>/dev/null && { name=$u; break; }; done < $P8/units.txt
  [ -z "$name" ] && exit 0
  lim=$CAP; [ $left -lt $lim ] && lim=$left
  P=$P8/work/$name.lrat; O=$P8/out/$name.out
  if [ "$name" = P8_cover ]; then F=$P8/cover.cnf; n=0; else
    F=$P8/work/$name.cnf
    lits=$(grep "^$name " $C/l2/P8_cubes.txt | cut -d' ' -f2-); n=$(echo $lits | wc -w | tr -d ' ')
    awk -v n=$n '/^p cnf/ {print $1, $2, $3, $4 + n; next} {print}' $BASE > $F; for l in $lits; do echo "$l 0"; done >> $F
  fi
  cnfsha=$(shasum -a 256 $F | cut -d' ' -f1)
  t0=$(date +%s); nice -n 5 $B/cadical -t $lim --lrat --binary=false $F $P > $O 2>&1; t1=$(date +%s)
  st=$(grep -m1 '^s ' $O | cut -c3-); [ -z "$st" ] && st=UNKNOWN
  ts=$(grep 'total process time since initialization' $O | awk '{print $(NF-1)}'); mb=$(grep 'maximum resident' $O | awk '{print $(NF-1)}')
  rec="\"unit\": \"$name\", \"status\": \"$st\", \"cap_s\": $lim, \"solve_s\": ${ts:-null}, \"solve_wall_s\": $((t1-t0)), \"solve_rss_mb\": ${mb:-null}, \"cube_literals\": $n, \"cnf_sha256\": \"$cnfsha\""
  if [ "$st" = "UNSATISFIABLE" ]; then
    pb=$(stat -f %z $P); psha=$(shasum -a 256 $P | cut -d' ' -f1)
    t2=$(date +%s); lc=$(nice -n 5 $B/lrat-check $F $P 2>&1 | grep -m1 -E 'VERIFIED|FAIL|rror'); t3=$(date +%s)
    rec="$rec, \"proof_bytes\": $pb, \"proof_sha256\": \"$psha\", \"lrat_check\": \"$lc\", \"lrat_check_s\": $((t3-t2))"
    if [ "$lc" = "c VERIFIED" ]; then echo "{$rec}" > $P8/queue/$name.json; mv $P $P8/queue/$name.lrat
    else mv $P $P8/failed/; echo "{$rec, \"proof_kept\": true, \"finished\": \"$(date -u +%H:%M:%SZ)\"}" >> $P8/results.jsonl; fi
  else
    [ "$st" = "SATISFIABLE" ] && cp $O $P8/SAT_$name.out
    rm -f $P; echo "{$rec, \"finished\": \"$(date -u +%H:%M:%SZ)\"}" >> $P8/results.jsonl
  fi
  [ "$name" = P8_cover ] || rm -f $F
done
