#!/bin/bash
# batch B: m = 11 (the real base CNF, sha bf0e502e...), then the 7-gon-free SYMMAX sets and orbit-deleted subsets
PY=${PY:-python3}
D=$(cd "$(dirname "$0")" && pwd)
X=${ES7_RESULTS:-$(cd "$D/../../.." && pwd)}/SYMMAX
$PY -B $D/ties.py random 1111 200 11 7 >> $D/logs/big.jsonl
$PY -B $D/ties.py file $X/c3_27points.txt 9 7 >> $D/logs/big.jsonl
$PY -B $D/ties.py file $X/c3_30points.txt 10 7 >> $D/logs/big.jsonl
$PY -B $D/ties.py file $X/c3_31points.txt 10 7 --drop-centre >> $D/logs/big.jsonl
$PY -B $D/ties.py file $X/c3_27points.txt 9 7 --subsets 150 21 5 >> $D/logs/big.jsonl
$PY -B $D/ties.py file $X/c3_30points.txt 10 7 --subsets 150 22 5 >> $D/logs/big.jsonl
$PY -B $D/ties.py file $X/c3_31points.txt 10 7 --drop-centre --subsets 150 23 5 >> $D/logs/big.jsonl
echo done-big
