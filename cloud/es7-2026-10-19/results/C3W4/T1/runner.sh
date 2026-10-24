#!/bin/bash
# C3W4 T1 runner: LIST=W4_two.tsv, j=1, N=4, SLICE=1.0, H=4.0
export PATH=/opt/bin:$PATH
START=1792841487
END=$((START + 4*3600 - 900))
cd /opt/c3u/cloud/es7-2026-10-19/results/C3U/tools
# watchdog: at END, kill any running close_tree, solver or checker
( while [ $(date +%s) -lt $END ]; do sleep 20; done; pkill -f close_tree.py; pkill -x cadical; pkill -x cake_lpr; pkill -x lrat-check; echo "=== END KILL $(date -u +%T)" ) &
tail -n +2 /opt/work/roots.tsv | cut -f2 | while read R; do
  NOW=$(date +%s); [ $NOW -ge $END ] && break
  if grep -q "SAT FOUND\|PROOF NOT ACCEPTED" /opt/work/driver.log; then echo "=== STOP"; break; fi
  S=$(python3 -c "print(round(min(1.0, ($END-$NOW)/3600),3))")
  echo "=== ROOT $R start $(date -u +%T) hours $S"
  python3 close_tree.py /opt/work/base.cnf /opt/work/out.jsonl $R --jobs 3 --sigma-split 3 --sigma-levels 2 --caps 300,300,600 --cadopts=--sat --split-singles --hours $S 2>&1
  echo "=== ROOT $R end $(date -u +%T)"
  if grep -q "SAT FOUND\|PROOF NOT ACCEPTED" /opt/work/driver.log; then echo "=== STOP"; break; fi
done
echo "=== RUNNER DONE $(date -u +%T)"
