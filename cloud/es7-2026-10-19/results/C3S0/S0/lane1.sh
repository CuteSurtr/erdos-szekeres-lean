#!/bin/bash
export PATH=/opt/bin:$PATH
END=1792549723
K=1
cd /opt/c3s/cloud/es7-2026-10-19/results/C3-S/tools
tail -n +2 /home/user/erdos-szekeres-lean/cloud/es7-2026-10-19/results/C3S0/S0/roots.tsv | awk -v k=$K '(NR-1)%3==k' | cut -f3 | while read R; do
  NOW=$(date +%s); [ $NOW -ge $END ] && break
  if grep -q "SAT FOUND\|PROOF NOT ACCEPTED" /opt/work/driver0.log /opt/work/driver1.log /opt/work/driver2.log 2>/dev/null; then echo "=== STOP"; break; fi
  S=$(python3 -c "print(round(min(0.17,($END-$NOW)/3600),3))")
  echo "=== ROOT $R start $(date -u +%T) hours $S"
  python3 close_tree.py /opt/work/base.cnf /opt/work/out$K.jsonl $R --jobs 1 --caps 300,300,600 --cadopts=--sat --split-singles --hours $S 2>&1
  echo "=== ROOT $R end $(date -u +%T)"
done
echo "=== RUNNER DONE $(date -u +%T)"
