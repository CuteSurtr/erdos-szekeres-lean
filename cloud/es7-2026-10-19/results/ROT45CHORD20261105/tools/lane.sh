#!/bin/bash
# lane.sh CUBE.cnf : solve with CaDiCaL (text LRAT), then lrat-check an UNSAT proof; append one line to results.tsv
f=$1; b=${f%.cnf}; dl=$(cat deadline); now=$(date +%s); left=$(( dl - now )); [ $left -lt 60 ] && exit 0
t0=$(date +%s)
timeout $left cadical --lrat --binary=false -q $f $b.lrat > $b.out 2>&1; rc=$?
t1=$(date +%s)
res=$(grep -m1 -E '^s ' $b.out | cut -c3-); [ -z "$res" ] && res="UNKNOWN(rc=$rc)"
chk="-"
if [ "$res" = "UNSATISFIABLE" ]; then
  left=$(( dl - $(date +%s) )); timeout $left lrat-check $f $b.lrat > $b.check 2>&1; chk=$(grep -o -m1 -E 's VERIFIED|c VERIFIED|VERIFIED|FAILED' $b.check || echo "check-rc=$?")
fi
printf "%s\t%s\t%ss\t%s\t%s\n" "$(basename $b)" "$res" "$((t1-t0))" "$(du -h $b.lrat 2>/dev/null | cut -f1)" "$chk" >> results.tsv
