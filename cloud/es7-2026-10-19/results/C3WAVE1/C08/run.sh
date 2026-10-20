#!/bin/bash
# Close the roots one at a time, in order; stop on SAT / rejection; hard stop at END (epoch s).
# usage: run.sh JOBS [first-root-line]
export PATH=/opt/bin:$PATH
R=/home/user/erdos-szekeres-lean/cloud/es7-2026-10-19/results/C3WAVE1/C08
T=/opt/c3s/cloud/es7-2026-10-19/results/C3-S/tools
END=$(cat /opt/work/END)
JOBS=${1:-4}
while IFS=$'\t' read -r idx root; do
  grep -qx "$root" /opt/work/roots_done.txt 2>/dev/null && continue
  now=$(date +%s); left=$((END-now)); [ $left -le 60 ] && { echo "TIME UP before $root"; break; }
  H=$(python3 -c "print(round($left/3600,3))")
  echo "=== $(date -u +%H:%M:%S) root $idx $root jobs $JOBS hours $H"
  python3 $T/close_tree.py /opt/work/base.cnf $R/out.jsonl "$root" --jobs $JOBS --caps 300,300,600 --cadopts=--sat --split-singles --hours $H 2>&1 | tee /opt/work/last.log
  if grep -q "SAT FOUND\|PROOF NOT ACCEPTED" /opt/work/last.log; then echo "STOP: $(grep 'SAT FOUND\|PROOF NOT ACCEPTED' /opt/work/last.log)"; break; fi
  if grep -q '"open_frontier": 0' /opt/work/last.log; then echo "$root" >> /opt/work/roots_done.txt; echo "$root" >> $R/roots_done.txt; else echo "root $root not finished"; break; fi
done < /opt/work/roots.txt
echo "=== driver loop exit $(date -u +%H:%M:%S)"
