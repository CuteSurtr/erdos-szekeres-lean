#!/bin/bash
# Mirror instances at k = 6 below 17 points (side facts / positive-control search).
# usage: probe_k6.sh <cnfdir> <bindir>
CNF="$1"; BIN="$2"; HERE="$(cd "$(dirname "$0")" && pwd)"; G="$HERE/../../../tools/etv/gen_etv.py"
cd "$CNF"
for n in 12 13 14 15 16; do
  python3 "$G" $n 6 6 6 --mirror -o m${n}k6.cnf > /dev/null
  python3 "$G" $n 6 6 6 --mirror --hull -o hm${n}k6.cnf > /dev/null
  for f in m${n}k6 hm${n}k6; do
    t0=$(date +%s)
    st=$("$BIN/cadical" -q "$f.cnf" | grep '^s ')
    echo "$f: $st ($(( $(date +%s) - t0 )) s)"
  done
done
