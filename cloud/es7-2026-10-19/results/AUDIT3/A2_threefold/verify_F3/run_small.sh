#!/bin/bash
# batch A: random 3-fold sets, m = 3..10, several k, ties forced in every canonical gap
PY=${PY:-python3}
D=$(cd "$(dirname "$0")" && pwd)
for m in 3 4 5 6 7 8; do
  $PY -B $D/ties.py random $((100+m)) 150 $m 5 6 7 >> $D/logs/small.jsonl
done
for m in 9 10; do
  $PY -B $D/ties.py random $((100+m)) 80 $m 7 8 >> $D/logs/small.jsonl
done
echo done-small
