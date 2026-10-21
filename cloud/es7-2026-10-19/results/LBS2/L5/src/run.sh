#!/bin/bash
# LBS2 L5 driver. BIN = directory with the binaries built from src/ and tools/trackA/sat.c:
#   gcc -O2 -o $BIN/sat ../../../tools/trackA/sat.c; clang -O2 -o $BIN/sat_wide src/sat_wide.c
#   gcc -O2 -o $BIN/vfy7 src/vfy7.c; g++ -O2 -march=native -o $BIN/anneal32 src/anneal32.cpp
# usage (from results/LBS2/L5): src/run.sh BIN SECONDS
BIN=$1; SECS=$2; SATPY=../../../tools/realizer/saturate.py
for s in 11 12; do setsid nohup $BIN/anneal32 $s $SECS run/a$s.sets >/dev/null 2>&1 & done
setsid nohup $BIN/anneal32 21 $SECS run/a21.sets run/starts.txt >/dev/null 2>run/a21.err &
setsid nohup python3 src/pipeline.py run/cands_near.jsonl run/out_near.jsonl $BIN/sat $BIN/vfy7 $SATPY $BIN/sat_wide src/saturate_wide.py > run/pipeline_near.log 2>&1 &
# anneal outputs: convert and test every 2 minutes until the annealers stop, then once more
setsid nohup bash -c "
  while pgrep -x anneal32 >/dev/null; do
    python3 src/anneal2cands.py run/cands_anneal.jsonl run/a*.sets 2>/dev/null
    python3 src/pipeline.py run/cands_anneal.jsonl run/out_anneal.jsonl $BIN/sat $BIN/vfy7 $SATPY $BIN/sat_wide src/saturate_wide.py >> run/pipeline_anneal.log 2>&1
    sleep 120; done
  python3 src/anneal2cands.py run/cands_anneal.jsonl run/a*.sets 2>/dev/null
  python3 src/pipeline.py run/cands_anneal.jsonl run/out_anneal.jsonl $BIN/sat $BIN/vfy7 $SATPY $BIN/sat_wide src/saturate_wide.py >> run/pipeline_anneal.log 2>&1
  echo DONE >> run/pipeline_anneal.log" >/dev/null 2>&1 &
