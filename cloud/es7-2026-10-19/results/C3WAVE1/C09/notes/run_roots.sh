#!/bin/bash
export PATH=/opt/bin:$PATH
D=/home/user/erdos-szekeres-lean/cloud/es7-2026-10-19/results/C3WAVE1/C09
STOP=$(date -u -d '2026-10-20 11:15:00' +%s)
JOBS=${JOBS:-4}
cd /opt/c3s/cloud/es7-2026-10-19/results/C3-S/tools
awk '{print $2}' $D/roots.txt | while read R; do
  if [ -n "$START_AT" ] && [ "$R" != "$START_AT" ] && [ -z "$STARTED" ]; then continue; fi; STARTED=1
  NOW=$(date +%s); [ $NOW -ge $STOP ] && { echo "TIME UP before $R"; break; }
  H=$(python3 -c "print(round(($STOP-$NOW)/3600,3))")
  echo "=== ROOT $R start $(date -u +%T) hours=$H jobs=$JOBS"
  timeout $((STOP-NOW)) python3 close_tree.py /opt/work/base.cnf /opt/work/out.jsonl $R --jobs $JOBS --caps 300,300,600 --cadopts=--sat --split-singles --hours $H 2>&1 | tee /opt/work/last.log
  echo "=== ROOT $R end $(date -u +%T) rc=${PIPESTATUS[0]}"
  if grep -q "SAT FOUND\|PROOF NOT ACCEPTED\|Traceback" /opt/work/last.log; then echo "=== STOPPED: needs attention"; break; fi
done
echo "=== RUNNER DONE $(date -u +%T)"
