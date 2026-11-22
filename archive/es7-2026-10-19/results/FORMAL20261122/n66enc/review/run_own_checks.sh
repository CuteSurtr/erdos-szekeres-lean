#!/bin/bash
# Reviewer's own checks (slot lrv2), one unit, sequential: own_checks.py; coreutils SHA-256 of the 132 trim.cnf;
# E1 spot check: the frozen printer exe re-run on three leaves, stdout hashed by coreutils (nothing written but logs).
set -uo pipefail
D=/home/jay/research/data/formalize-20261122/n66enc
RV=$D/review
cd $RV
echo "== own_checks.py $(date '+%T')"
/usr/bin/time -v /home/jay/research/data/six10-linux-20261105/venv.disk/bin/python -I $RV/own_checks.py 7 3000 > $RV/own_checks.out 2> $RV/own_checks.time
echo "own_checks rc=$?"
echo "== coreutils sha256sum of 132 trim.cnf $(date '+%T')"
: > $RV/trim_sha256_coreutils.tsv
while IFS=$'\t' read -r i cid path rec; do
  h=$(sha256sum "$path" | cut -d' ' -f1)
  [ "$h" = "$rec" ] && v=MATCH || v=FAIL
  printf '%s\t%s\t%s\t%s\t%s\n' "$i" "$cid" "$h" "$rec" "$v" >> $RV/trim_sha256_coreutils.tsv
done < $RV/leaf_paths.tsv
echo "trim sha256: $(cut -f5 $RV/trim_sha256_coreutils.tsv | sort | uniq -c | tr '\n' ' ')"
echo "== E1 spot check (printer exe $(sha256sum $D/build/bin/n66print | cut -c1-16)) $(date '+%T')"
for i in 93 131 0; do
  rec=$(awk -F'\t' -v i=$i '$1==i{print $4}' $RV/leaf_paths.tsv)
  h=$( { /usr/bin/time -f "exe leaf $i wall=%e s maxrss=%M KB rc=%x" $D/build/bin/n66print trim $i $D/desc/$i.txt 2>> $RV/e1_spot.err; } | sha256sum | cut -d' ' -f1)
  [ "$h" = "$rec" ] && v=MATCH || v=FAIL
  echo "leaf $i printed $h record $rec $v"
done
echo "done $(date '+%T')"
