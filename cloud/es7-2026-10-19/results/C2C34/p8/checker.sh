#!/bin/bash
# P8 checker lane: the only cake_lpr process. Takes the oldest proof in p8/queue, rebuilds its CNF, runs lrat-check
# first if the record has no verdict yet, then cake_lpr with heap HEAP MB; appends the final record to
# p8/results.jsonl and deletes the proof once both checkers accept it (otherwise moves it to p8/failed).
# No new check after END.  usage: checker.sh END HEAP
S=${WORK:?set WORK to the work directory}
C=$S/c2c; B=$S/local/bin; P8=$C/p8; END=$1; HEAP=$2; BASE=$C/c34h_final.cnf
while [ "$(date +%s)" -lt $END ]; do
  J=$(ls -tr $P8/queue/*.json 2>/dev/null | head -1)
  if [ -z "$J" ]; then sleep 20; continue; fi
  name=$(basename $J .json); P=$P8/queue/$name.lrat
  if [ "$name" = P8_cover ]; then F=$P8/cover.cnf; else
    F=$P8/work/chk_$name.cnf
    lits=$(grep "^$name " $C/l2/P8_cubes.txt | cut -d' ' -f2-); n=$(echo $lits | wc -w | tr -d ' ')
    awk -v n=$n '/^p cnf/ {print $1, $2, $3, $4 + n; next} {print}' $BASE > $F; for l in $lits; do echo "$l 0"; done >> $F
  fi
  rec=$(sed -e 's/^{//' -e 's/}$//' $J)
  if ! grep -q '"lrat_check"' $J; then
    pb=$(stat -f %z $P); psha=$(shasum -a 256 $P | cut -d' ' -f1)
    t2=$(date +%s); lc=$(nice -n 5 $B/lrat-check $F $P 2>&1 | grep -m1 -E 'VERIFIED|FAIL|rror'); t3=$(date +%s)
    rec="$rec, \"proof_bytes\": $pb, \"proof_sha256\": \"$psha\", \"lrat_check\": \"$lc\", \"lrat_check_s\": $((t3-t2))"
  else lc="c VERIFIED"; fi
  ck="not run"; t4=$(date +%s)
  if [ "$lc" = "c VERIFIED" ]; then
    ck=$(nice -n 5 $B/cake_lpr --CML_HEAP_SIZE=$HEAP --CML_STACK_SIZE=4000 $F $P 2>&1 | grep -m1 -E 's VERIFIED|exhausted|rror|FAIL'); [ -z "$ck" ] && ck="no verdict line"
  fi
  t5=$(date +%s)
  if [ "$lc" = "c VERIFIED" ] && [ "$ck" = "s VERIFIED UNSAT" ]; then rm -f $P; kept=false; else mv $P $P8/failed/; kept=true; fi
  echo "{$rec, \"cake_lpr\": \"$ck\", \"cake_s\": $((t5-t4)), \"cake_heap_mb\": $HEAP, \"proof_kept\": $kept, \"finished\": \"$(date -u +%H:%M:%SZ)\"}" >> $P8/results.jsonl
  rm -f $J; [ "$name" = P8_cover ] || rm -f $F
done
