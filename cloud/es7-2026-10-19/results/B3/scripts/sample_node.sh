#!/bin/bash
# usage: sample_node.sh BIN CNF DEPTH_STEPS SEED TLIM WORK -> one line: seed steps L-product result secs
# random descent (march_cu -d 6 per step, python random choice), then plain CaDiCaL on the node
BIN=$1; CNF=$2; N=$3; SEED=$4; TL=$5; D=$6/n_${N}_$SEED
R=$(dirname $0); $R/descend.sh $BIN $CNF 6 $N $SEED $D
Ls=$(awk '{printf "%s*", $1}' $D/path.txt); prod=$(echo "${Ls}1" | bc)
s=$(date +%s.%N); timeout $TL $BIN/cadical -q $D/node.cnf > /dev/null 2>&1; rc=$?
dt=$(echo "$(date +%s.%N)-$s" | bc)
res=$([ $rc = 20 ] && echo U || ([ $rc = 10 ] && echo S || echo T))
echo "$SEED $N $prod $res $dt"
[ $rc = 10 ] && cp $D/node.cnf $6/SAT_node_${N}_$SEED.cnf
rm -f $D/node.cnf $D/nxt.cnf
