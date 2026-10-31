#!/bin/bash
# Close roots one at a time, in order, until END (epoch seconds).
D=/opt/work/live; R0=/home/user/erdos-szekeres-lean/cloud/es7-2026-10-19/results/C3WAVE1/C02
END=$1; JOBS=${2:-4}
cd /opt/c3s/cloud/es7-2026-10-19/results/C3-S
while read -r R; do
  grep -q "^$R " $D/roots_done.txt 2>/dev/null && continue
  H=$(python3 -c "print(max(0.001,($END-$(date +%s))/3600))")
  [ $(date +%s) -ge $END ] && break
  echo "=== $R start $(date -u +%T) hours=$H" >> $D/driver.log
  python3 tools/close_tree.py /opt/work/base.cnf $D/out.jsonl "$R" --jobs $JOBS --caps 300,300,600 --cadopts=--sat --split-singles --hours $H >> $D/driver.log 2>&1
  rc=$?
  last=$(tail -1 $D/driver.log)
  echo "=== $R end $(date -u +%T) rc=$rc" >> $D/driver.log
  if grep -q '"open_frontier": 0' <<<"$last"; then echo "$R done" >> $D/roots_done.txt; else break; fi
done < $R0/roots.txt
echo RUNNER_EXIT $(date -u +%T) >> $D/driver.log
