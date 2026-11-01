#!/bin/bash
# usage: descend.sh BIN CNF STEP NSTEPS SEED OUTDIR  -> OUTDIR/node.cnf, OUTDIR/path.txt
# random descent through march_cu -d STEP cube trees, choosing cubes with python random(SEED)
BIN=$1; CNF=$2; STEP=$3; N=$4; SEED=$5; D=$6; mkdir -p $D; cp $CNF $D/node.cnf; : > $D/path.txt
for ((s=1; s<=N; s++)); do
  $BIN/march_cu $D/node.cnf -d $STEP -o $D/c.icnf > $D/m.log 2>&1
  pick=$(python3 -c "import random,sys; random.seed($SEED*1000+$s); L=[l for l in open('$D/c.icnf') if l.startswith('a')]; print(len(L), random.choice(L).strip())")
  echo "$pick" >> $D/path.txt
  python3 $BIN/../applycube.py $D/node.cnf "${pick#* }" $D/nxt.cnf && mv $D/nxt.cnf $D/node.cnf
done
