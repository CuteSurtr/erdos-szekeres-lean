#!/bin/bash
# C3W4 H02 runner: W4_H3.tsv, j=2, N=30, SLICE=2.0, H=5.0
export PATH=/opt/bin:$PATH
TOOLS=/opt/c3u/cloud/es7-2026-10-19/results/C3U/tools
START=1792841467                       # 2026-10-24 11:31:07 UTC
END=$((START + 5*3600 - 900))          # 16:16:07 UTC
LOG=/opt/work/driver.log
OUT=/opt/work/out.jsonl
# watchdog: close_tree checks its deadline only between batches, so stop the whole group at END
( while [ $(date +%s) -lt $END ]; do sleep 20; done; echo "=== END reached $(date -u +%T), killing" >> $LOG; kill -TERM -$$ ) &
tail -n +2 /opt/work/roots.tsv | cut -f2 | while read R; do
  LEFT=$((END - $(date +%s)))
  [ $LEFT -le 0 ] && break
  S=$(python3 -c "print(min(2.0, $LEFT/3600))")
  echo "=== ROOT $R start $(date -u +%FT%TZ) hours $S" >> $LOG
  (cd $TOOLS && python3 close_tree.py /opt/work/base.cnf $OUT $R --jobs 3 \
     --sigma-split 3 --sigma-levels 2 --caps 1,1,300,600 --cadopts=--sat --hours $S) >> $LOG 2>&1
  echo "=== ROOT $R end $(date -u +%FT%TZ)" >> $LOG
  if grep -q -E "SAT FOUND|PROOF NOT ACCEPTED" $LOG; then echo "=== STOP on SAT/PROOF" >> $LOG; break; fi
done
echo "=== RUNNER done $(date -u +%FT%TZ)" >> $LOG
kill -TERM -$$ 2>/dev/null
