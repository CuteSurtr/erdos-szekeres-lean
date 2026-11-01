#!/bin/bash
# C3W6 P28 lane 1: units at positions = 1 (mod 3) of units.tsv
export PATH=/opt/bin:$PATH
END=1792921585
K=1
LOG=/opt/work/driver$K.log
TOOLS=/opt/c3u2/cloud/es7-2026-10-19/results/C3U2/tools
cd $TOOLS
tail -n +2 /opt/work/units.tsv | cut -f2 | awk -v k=$K '(NR-1)%3==k' | while read U; do
  [ -e /opt/work/STOP ] && { echo "=== STOP"; break; }
  [ $(date +%s) -ge $END ] && break
  echo "=== UNIT $U start $(date -u +%FT%T)"
  OUTP=$(python3 close_tree.py /opt/work/base.cnf /opt/work/out$K.jsonl $U --jobs 1 --sigma-split 3 --sigma-levels 2 --caps 900,600 --cadopts=--sat --hours 0.02 2>&1)
  echo "$OUTP" > /opt/work/last$K.txt
  echo "$OUTP" | grep -v '^{' | grep -v '^$'
  echo "$OUTP" | grep '"status"'
  echo "$OUTP" | tail -1
  echo "=== UNIT $U end $(date -u +%FT%T)"
  if echo "$OUTP" | grep -q "SAT FOUND"; then echo "=== SAT FOUND, STOP"; touch /opt/work/STOP; break; fi
  if echo "$OUTP" | grep -q "PROOF NOT ACCEPTED"; then
    echo "=== RECHECK $U start $(date -u +%FT%T)"
    python3 close_tree.py /opt/work/base.cnf /opt/work/recheck.jsonl $U --jobs 1 --caps 900 --cadopts=--sat --hours 0.02 2>&1 | tail -3
    echo "=== RECHECK $U end $(date -u +%FT%T)"
    if ! grep -F "\"node\": \"$U\"" /opt/work/recheck.jsonl | grep -q '"certified": true'; then echo "=== RECHECK FAILED, STOP"; touch /opt/work/STOP; break; fi
  fi
done
echo "=== LANE DONE $(date -u +%FT%T)"
