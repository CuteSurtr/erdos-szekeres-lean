#!/bin/bash
# S4 step (b)+(c): build the case CNF, check its sha256, try CaDiCaL 120 s on the whole case.
# usage: whole.sh CASE   (run from cloud/es7-2026-10-19); prints CLOSED / OPEN / SAT / SHAFAIL
set -u; c=$1; B=/opt/work/bin; W=$(mktemp -d /opt/work/tmp/whole_${c}_XXXX); S4=results/WAVE2/S4
read U L SHA < <(python3 -c "import json,sys
for l in open('results/Mii-S/cases.jsonl'):
    r=json.loads(l)
    if r['case']=='$c': print(','.join(map(str,r['U'])) or '-', ','.join(map(str,r['L'])) or '-', r['cnf_sha256'])")
[ "$U" = - ] && U=""; [ "$L" = - ] && L=""
python3 results/Mii-S/scripts/hullsplit.py case /opt/work/F.cnf "$U" "$L" /opt/work/cases/$c.cnf >/dev/null
got=$(sha256sum /opt/work/cases/$c.cnf | cut -d' ' -f1)
if [ "$got" != "$SHA" ]; then echo "{\"case\":\"$c\",\"sha_fail\":\"$got\"}" >> $S4/whole.jsonl; rm -f /opt/work/cases/$c.cnf; echo SHAFAIL; exit; fi
t0=$(date +%s.%N); $B/cadical --lrat --binary=false -q -t 120 /opt/work/cases/$c.cnf $W/p.lrat > $W/out; rc=$?
t1=$(date +%s.%N); v=""; ck=0
if [ $rc = 20 ]; then v=$($B/cake_lpr /opt/work/cases/$c.cnf $W/p.lrat | grep '^s ' | head -1); ck=$(echo "$(date +%s.%N) - $t1" | bc); fi
st=$(echo "$t1 - $t0" | bc)
echo "{\"case\":\"$c\",\"case_sha256\":\"$got\",\"rc\":$rc,\"solve_s\":$st,\"cake_lpr\":\"$v\",\"check_s\":$ck}" >> $S4/whole.jsonl
if [ $rc = 10 ]; then mkdir -p $S4/$c; cp $W/out $S4/$c/SAT_whole.out; echo SAT
elif [ $rc = 20 ] && [ "$v" = "s VERIFIED UNSAT" ]; then
  mkdir -p $S4/$c; echo "{\"case\":\"$c\",\"case_sha256\":\"$got\",\"method\":\"whole cadical 120s\",\"status\":\"UNSAT\",\"cube\":[],\"cake_lpr\":\"$v\",\"solve_s\":$st,\"check_s\":$ck}" > $S4/$c/leaves.jsonl
  printf 'a 0\n' > $S4/$c/.l && mv $S4/$c/.l $S4/$c/leaves.icnf; : > $S4/$c/open.icnf; echo CLOSED
else echo OPEN; fi
rm -rf $W
