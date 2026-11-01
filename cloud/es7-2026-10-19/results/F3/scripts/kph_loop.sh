#!/bin/bash
# KPH-style arm: abstract (7,5,7)@26 models (F2/s2 gen_models.py, CaDiCaL random phases + random
# assumptions + blocking) in chunks of CHUNK, each chunk realized with the validated realizer
# (F2/s2 realize_models.py -> results/F realize.py, 5 CPU-s per model, exact re-check).
# Seeds 3200000+i, i = 1, 2, ... until END (epoch seconds).
# usage: kph_loop.sh BIN OUTDIR END [CHUNK]
BIN=$1; O=$2; END=$3; CHUNK=${4:-100}; P=/usr/bin/python3
D=$(cd "$(dirname "$0")/../../F2/s2/scripts" && pwd); mkdir -p $O; i=0
while [ $(date +%s) -lt $END ]; do
  i=$((i+1)); sd=$((3200000+i))
  $P $D/gen_models.py $BIN/etv26.cnf --count $CHUNK --seed $sd -o $O/models_$sd.txt 2>> $O/gen.log
  $P $D/realize_models.py $O/models_$sd.txt --time 5 --jobs 1 -o $O/real_$sd.jsonl >> $O/realize.log 2>&1
done
