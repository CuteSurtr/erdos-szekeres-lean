#!/bin/bash
# Task 3: regenerate each cover obligation with cover.py, solve with CaDiCaL --lrat, check with cake_lpr.
# usage: t3_cover.sh OBLIGATION  -> one JSON line on stdout
S=/home/user/erdos-szekeres-lean/cloud/es7-2026-10-19/results/Mii-S/scripts
ob="$1"; W=/opt/work/t3/$(echo "$ob" | tr ':,' '__'); mkdir -p $W
python3 $S/cover.py cnf /opt/work/F/m33k7int.sub.cnf "$ob" $W/f.cnf
sha=$(sha256sum $W/f.cnf | cut -d' ' -f1)
t0=$(date +%s.%N); /opt/bin/cadical -q --lrat --binary=false -t 3000 $W/f.cnf $W/p.lrat > $W/out.txt; rc=$?; t1=$(date +%s.%N)
pb=$(stat -c %s $W/p.lrat 2>/dev/null || echo 0)
if [ $rc = 20 ]; then v=$(/opt/bin/cake_lpr $W/f.cnf $W/p.lrat | grep '^s ' | head -1); else v="not-run"; fi; t2=$(date +%s.%N)
printf '{"obligation":"%s","cnf_sha256":"%s","rc":%s,"solve_s":%.2f,"proof_bytes":%s,"cake_lpr":"%s","check_s":%.2f}\n' "$ob" $sha $rc $(echo "$t1-$t0"|bc) $pb "$v" $(echo "$t2-$t1"|bc)
rm -rf $W
