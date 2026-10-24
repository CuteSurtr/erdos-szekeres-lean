#!/bin/bash
# Knuth-style random descent through march_cu cube trees.
# usage: probe.sh BIN CNF STEP_DEPTH MAXSTEPS TLIM SEED OUTDIR
# At each step: march_cu -d STEP on the current restricted CNF; record #cubes (= surviving
# leaves L_i); solve 3 random cubes with icube (TLIM s each, 3 parallel); then pick one
# random cube and apply it as units. Estimated #leaves at depth = prod L_i.
BIN=$1; CNF=$2; STEP=$3; MAX=$4; TL=$5; SEED=$6; D=$7
mkdir -p $D; cp $CNF $D/cur.cnf; RANDOM=$SEED; prod=1; depth=0
for ((s=1; s<=MAX; s++)); do
  t0=$(date +%s.%N)
  $BIN/march_cu $D/cur.cnf -d $STEP -o $D/c.icnf > $D/m.log 2>&1
  tm=$(echo "$(date +%s.%N)-$t0" | bc)
  if grep -q "UNSATISFIABLE" $D/m.log; then echo "step $s depth $depth march refuted node"; break; fi
  L=$(grep -c '^a' $D/c.icnf); [ "$L" = 0 ] && { echo "step $s no cubes"; tail -3 $D/m.log; break; }
  prod=$(echo "$prod*$L" | bc); depth=$((depth+STEP))
  grep '^a' $D/c.icnf | shuf -n 3 --random-source=<(yes $RANDOM) > $D/s.icnf
  rm -f $D/s_*.tsv
  for w in 0 1 2; do $BIN/icube $D/cur.cnf $D/s.icnf 3 $w $TL $D/s_$w.tsv & done; wait
  res=$(cut -f2,3 $D/s_*.tsv | tr '\t' ':' | tr '\n' ' ')
  echo "step $s depth~$depth L=$L est_nodes=$prod march_s=$tm cubes: $res"
  pick=$(grep '^a' $D/c.icnf | shuf -n 1 --random-source=<(yes $RANDOM$s))
  python3 $BIN/../applycube.py $D/cur.cnf "$pick" $D/nxt.cnf && mv $D/nxt.cnf $D/cur.cnf
  if ! grep -q T $D/s_*.tsv; then echo "all sampled cubes solved within $TL s"; fi
done
