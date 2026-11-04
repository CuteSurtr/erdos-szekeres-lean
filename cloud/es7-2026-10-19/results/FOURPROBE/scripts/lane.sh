#!/bin/bash
# lane.sh NAME CNF LRAT DEADLINE_EPOCH [MAXSEC] : one cadical run with LRAT, RAM-gated, ends before deadline
D="<repo>/.cache/es7/final-2026-11-04/four_probe"
B="<repo>/.cache/es7/bin"
name=$1; cnf=$2; lrat=$3; dl=$4; mx=${5:-100000}
ram=$(vm_stat | awk '/Pages active/{a=$3}/wired down/{w=$4}/occupied by compressor/{c=$5}END{printf "%.1f\n",(a+w+c)*16384/1e9}')
left=$(( dl - $(date +%s) )); [ $left -gt $mx ] && left=$mx
echo "$(date +%H:%M:%S) $name start ram=$ram limit=$left" >> "$D/logs/lanes.txt"
if awk -v r=$ram 'BEGIN{exit !(r>36)}'; then echo "$(date +%H:%M:%S) $name SKIP ram=$ram" >> "$D/logs/lanes.txt"; exit 0; fi
if [ $left -lt 60 ]; then echo "$(date +%H:%M:%S) $name SKIP time" >> "$D/logs/lanes.txt"; exit 0; fi
t0=$(date +%s)
"$B/cadical" -t $left --lrat --binary=false "$cnf" "$lrat" > "$D/logs/cad_$name.out" 2>&1; ec=$?
dt=$(( $(date +%s) - t0 ))
res=UNKNOWN; [ $ec = 10 ] && res=SAT; [ $ec = 20 ] && res=UNSAT
echo "$(date +%H:%M:%S) $name exit=$ec $res ${dt}s" >> "$D/logs/lanes.txt"
if [ $ec = 20 ]; then
  "$B/lrat-check" "$cnf" "$lrat" > "$D/logs/lratcheck_$name.out" 2>&1
  echo "$(date +%H:%M:%S) $name lrat-check exit=$? $(grep -m1 -E 'VERIFIED|FAIL|rror' "$D/logs/lratcheck_$name.out")" >> "$D/logs/lanes.txt"
else
  ls -la "$lrat" >> "$D/logs/lanes.txt" 2>/dev/null; rm -f "$lrat"
fi
