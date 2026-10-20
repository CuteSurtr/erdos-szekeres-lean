#!/bin/bash
# closes the roots one at a time, in order, until DEADLINE (epoch seconds)
export PATH=/opt/bin:$PATH
D=/home/user/erdos-szekeres-lean/cloud/es7-2026-10-19/results/C3WAVE1/C18
cd /opt/c3s/cloud/es7-2026-10-19/results/C3-S/tools
for R in $(grep -v ' ' -v $D/roots.txt >/dev/null; awk 'NF==2{print $2}' $D/roots.txt); do
  now=$(date +%s); left=$(( DEADLINE - now )); [ $left -le 60 ] && break
  H=$(python3 -c "print(round($left/3600,3))")
  echo "=== ROOT $R start $(date -u +%T) hours $H" 
  python3 close_tree.py /opt/work/base.cnf $D/out.jsonl $R --jobs 4 --caps 300,300,600 --cadopts=--sat --split-singles --hours $H
  rc=$?
  echo "=== ROOT $R end $(date -u +%T) rc $rc"
done
echo "=== ALL DONE $(date -u +%T)"
