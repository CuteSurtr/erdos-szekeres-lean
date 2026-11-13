#!/bin/bash
export PATH=/opt/bin:$PATH
END=$(date -u -d '2026-10-21 02:06:20' +%s)
REPO=/home/user/erdos-szekeres-lean
W2=$REPO/cloud/es7-2026-10-19/results/C3WAVE2
cd /opt/c3s/cloud/es7-2026-10-19/results/C3-S/tools
tail -n +2 /opt/work/roots.tsv | cut -f2 | while read R; do
  NOW=$(date +%s); [ $NOW -ge $END ] && break
  ( flock 9; cd $REPO && git pull -q --rebase --autostash ) 9>/opt/work/git.lock
  if cat $W2/K*/out.jsonl 2>/dev/null | grep -q "\"node\": \"$R[\"_]"; then
    echo "=== ROOT $R skipped $(date -u +%T) (already in another machine's out.jsonl)"; echo "$R" >> /opt/work/skipped.txt; continue
  fi
  S=$(python3 -c "print(round(min(0.17,($END-$NOW)/3600),3))")
  echo "=== ROOT $R start $(date -u +%T) hours $S"
  python3 close_tree.py /opt/work/base.cnf /opt/work/out.jsonl $R --jobs 3 --caps 300,300,600 --cadopts=--sat --split-singles --hours $S 2>&1
  echo "=== ROOT $R end $(date -u +%T)"
  if tail -n 3 /opt/work/driver.log | grep -q "SAT FOUND\|PROOF NOT ACCEPTED"; then echo "=== STOP"; break; fi
done
echo "=== RUNNER DONE $(date -u +%T)"
