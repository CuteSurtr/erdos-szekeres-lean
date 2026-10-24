#!/bin/bash
export PATH=/opt/bin:$PATH
D=/home/user/erdos-szekeres-lean/cloud/es7-2026-10-19/results/C3WAVE1/C00
END=$(date -u -d '2026-10-20 11:33:00' +%s)
cd /opt/c3s/cloud/es7-2026-10-19/results/C3-S/tools
tail -n +2 /opt/work/roots.tsv | cut -f2 | while read R; do
  NOW=$(date +%s); [ $NOW -ge $END ] && break
  H=$(python3 -c "print(round(($END-$NOW)/3600,3))")
  echo "=== ROOT $R start $(date -u +%T) hours $H"
  python3 close_tree.py /opt/work/base.cnf /opt/work/out.jsonl $R --jobs ${JOBS:-4} --caps 300,300,600 --cadopts=--sat --split-singles --hours $H 2>&1
  echo "=== ROOT $R end $(date -u +%T)"
  if tail -n 3 /opt/work/driver.log | grep -q "SAT FOUND\|PROOF NOT ACCEPTED"; then echo "=== STOP"; break; fi
done
echo "=== RUNNER DONE $(date -u +%T)"
