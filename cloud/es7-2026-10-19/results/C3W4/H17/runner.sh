#!/bin/bash
# C3W4 H17 runner: one close_tree.py run per root, in order, until END
export PATH=/opt/bin:$PATH
TOOLS=/opt/c3u/cloud/es7-2026-10-19/results/C3U/tools
END=1792858572
cd $TOOLS
tail -n +2 /opt/work/roots.tsv | cut -f2 | while read R; do
  NOW=$(date +%s); LEFT=$((END - NOW))
  [ $LEFT -le 0 ] && break
  S=$(python3 -c "print(round(min(2.0, $LEFT/3600), 4))")
  echo "=== ROOT $R start $(date -u +%FT%TZ) hours $S" >> /opt/work/driver.log
  python3 close_tree.py /opt/work/base.cnf /opt/work/out.jsonl $R --jobs 3 --sigma-split 3 --sigma-levels 2 --caps 1,1,300,600 --cadopts=--sat --hours $S >> /opt/work/driver.log 2>&1
  echo "=== ROOT $R end $(date -u +%FT%TZ) rc $?" >> /opt/work/driver.log
  if grep -q -e "SAT FOUND" -e "PROOF NOT ACCEPTED" /opt/work/driver.log; then echo "=== STOP" >> /opt/work/driver.log; break; fi
done
echo "=== RUNNER DONE $(date -u +%FT%TZ)" >> /opt/work/driver.log
