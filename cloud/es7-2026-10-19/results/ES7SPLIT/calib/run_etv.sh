#!/bin/bash
# usage: run_etv.sh N n a b [timeout_seconds] [extra gen flags...]
# Generates ETV(n,a,b;N) CNF, solves with CaDiCaL (wall-clock limit), checks SAT models independently.
# Environment: WORK (output directory for cnf/ and logs/, default ./etv_work), PY (default python3),
# CADICAL (default cadical; CaDiCaL 3.0.1 was used).
set -u
HERE=$(cd "$(dirname "$0")" && pwd)
W=${WORK:-./etv_work}
PY=${PY:-python3}
CAD=${CADICAL:-cadical}
mkdir -p $W/cnf $W/logs
N=$1; n=$2; a=$3; b=$4; T=${5:-60}; shift 5 2>/dev/null || shift $#
tag=N${N}_n${n}_a${a}_b${b}
f=$W/cnf/etv_$tag.cnf
$PY $HERE/gen_etv.py $N $n $a $b --xrefl "$@" -o $f > $W/logs/gen_$tag.json
start=$(date +%s.%N 2>/dev/null || date +%s)
$CAD -q -t $T $f > $W/logs/out_$tag.txt 2>&1
end=$(date +%s.%N 2>/dev/null || date +%s)
st=$(grep "^s " $W/logs/out_$tag.txt || echo "s UNKNOWN")
chk=""
if [ "$st" = "s SATISFIABLE" ]; then chk=$($PY $HERE/check_model.py $N $W/logs/out_$tag.txt); fi
echo "$tag: $st wall=$(echo "$end - $start" | bc) gen=$(cat $W/logs/gen_$tag.json) $chk"
