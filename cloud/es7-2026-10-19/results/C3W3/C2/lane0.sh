#!/bin/bash
# C3W3 C2 lane 0: roots at positions = 0 (mod 1) of roots.tsv, in order
TOOLS=/opt/c3s/cloud/es7-2026-10-19/results/C3-S/tools
END=1792578437   # start 1792557737 (04:42:17 UTC) + 6 h - 15 min
LOG=/opt/work/driver0.log
OUT=/opt/work/out0.jsonl
export PATH=/opt/bin:$PATH
for R in $(awk -F'\t' 'NR>1{print $2}' /opt/work/roots.tsv); do
  if grep -qE 'SAT FOUND|PROOF NOT ACCEPTED' /opt/work/driver*.log 2>/dev/null; then echo "=== STOP (SAT FOUND or PROOF NOT ACCEPTED)" >> $LOG; break; fi
  NOW=$(date +%s); LEFT=$((END - NOW))
  [ $LEFT -le 0 ] && break
  S=$(python3 -c "print(round(min(2.0, $LEFT/3600), 4))")
  echo "=== ROOT $R start $(date -u +%FT%TZ) hours=$S" >> $LOG
  (cd $TOOLS && python3 close_tree.py /opt/work/base.cnf $OUT $R --jobs 3 --caps 300,300,600 --cadopts=--sat --split-singles --hours $S) >> $LOG 2>&1
  echo "=== ROOT $R end $(date -u +%FT%TZ) rc=$?" >> $LOG
done
echo "=== LANE DONE $(date -u +%FT%TZ)" >> $LOG
