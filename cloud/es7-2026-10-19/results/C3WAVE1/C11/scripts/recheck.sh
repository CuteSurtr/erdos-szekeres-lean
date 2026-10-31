#!/bin/bash
# recheck.sh NODE -> one json line on stdout
N=$1; W=/opt/work/recheck; mkdir -p $W; cd /opt/c3s/cloud/es7-2026-10-19/results/C3-S/tools
python3 gen_case.py 11 7 $N -o $W/n.cnf >/dev/null; S=$(sha256sum $W/n.cnf | cut -c1-64)
t=$(date +%s); st=$(cadical -q -t 900 --sat --lrat --binary=false $W/n.cnf $W/n.lrat | grep "^s " ); ts=$(( $(date +%s)-t ))
a=$(lrat-check $W/n.cnf $W/n.lrat | grep -m1 "VERIFIED"); b=$(cake_lpr $W/n.cnf $W/n.lrat | head -1)
echo "{\"node\": \"$N\", \"cnf_sha256\": \"$S\", \"status\": \"$st\", \"solve_s\": $ts, \"lrat_check\": \"$a\", \"cake_lpr\": \"$b\", \"time\": \"$(date -u +%T)\"}"
rm -f $W/n.cnf $W/n.lrat
