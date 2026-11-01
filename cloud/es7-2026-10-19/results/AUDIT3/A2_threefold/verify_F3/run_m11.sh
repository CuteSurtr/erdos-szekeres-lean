#!/bin/bash
# m = 11, k = 7: the real base CNF (sha bf0e502e..., reproduced by ties.py basesha), in chunks of 8 sets
PY=${PY:-python3}
D=$(cd "$(dirname "$0")" && pwd)
for s in 1201 1202 1203 1204 1205 1206; do
  $PY -B $D/ties.py random $s 8 11 7 >> $D/logs/m11.jsonl
done
echo done-m11
