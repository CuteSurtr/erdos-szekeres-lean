#!/bin/bash
# E1 for all 132 leaves with the reviewer's own comparison (bash + coreutils): the frozen printer exe prints the text of
# leaf i from desc/i.txt; its SHA-256 is compared with the coreutils SHA-256 of that leaf's certified trim.cnf
# (trim_sha256_coreutils.tsv, column 3). Writes e1_all.tsv and e1_all.err only.
set -uo pipefail
D=/home/jay/research/data/formalize-20261122/n66enc
RV=$D/review
cd $RV
echo "exe $(sha256sum $D/build/bin/n66print | cut -d' ' -f1)"
: > $RV/e1_all.tsv; : > $RV/e1_all.err
while IFS=$'\t' read -r i cid fileh rech v; do
  h=$( { $D/build/bin/n66print trim $i $D/desc/$i.txt 2>> $RV/e1_all.err; } | sha256sum | cut -d' ' -f1)
  [ "$h" = "$fileh" ] && r=MATCH || r=FAIL
  printf '%s\t%s\t%s\t%s\t%s\n' "$i" "$cid" "$h" "$fileh" "$r" >> $RV/e1_all.tsv
done < $RV/trim_sha256_coreutils.tsv
echo "e1_all: $(cut -f5 $RV/e1_all.tsv | sort | uniq -c | tr '\n' ' ') rows=$(wc -l < $RV/e1_all.tsv)"
