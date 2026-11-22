#!/bin/bash
# Reviewer's own copy check: forward-rename every n66-rowsvalid source the worker says it copied and diff against
# the worker's file. Output: review/own_diff_copies.txt (one line per file: SAME / DIFF + the diff for DIFF).
S=/home/jay/research/data/formalize-20261122/n66-rowsvalid/lean
T=/home/jay/research/data/formalize-20261122/n66-l15-rows/lean
O=/home/jay/research/data/formalize-20261122/n66-l15-rows/review/own_diff_copies.txt
: > $O
fw() { sed -e 's/RowEnc/N66R15Enc/g; s/RowGeo/N66R15Geo/g; s/RowChk/N66R15Chk/g; s/N66Enc/N66E15/g; s/N66Geo/N66G15/g' "$1"; }
pairs=""
for f in Gen DataT0 DataT1 DataT2 DataT3 DataT DataC0 DataC1 DataC2 DataC3 DataC; do pairs="$pairs RowEnc/$f:N66R15Enc/$f"; done
pairs="$pairs RowEnc/Main:N66R15Enc/RowMain"
for f in Basic Sem Eight Oct Row Kinds Assembly End; do pairs="$pairs RowGeo/$f:N66R15Geo/$f"; done
for f in Tables Look TabPs TabTt TabDr0 TabDr1 TabDr TabCan Check CertsOk IsCore $(for i in $(seq 0 13); do echo TabTt$i; done) $(for i in 0 1 2 3; do echo certsOkTF$i certsOkCF$i; done); do pairs="$pairs RowChk/$f:N66R15Chk/$f"; done
same=0; diffn=0
for p in $pairs; do
  a=${p%%:*}; b=${p#*:}
  if diff -q <(fw $S/$a.lean) $T/$b.lean > /dev/null; then echo "SAME $a -> $b" >> $O; same=$((same+1));
  else echo "DIFF $a -> $b" >> $O; diff <(fw $S/$a.lean) $T/$b.lean >> $O; diffn=$((diffn+1)); fi
done
echo "total $(echo $pairs | wc -w): SAME $same DIFF $diffn" | tee -a $O
# files in the worker's chain dirs that are not copies
ls $T/N66R15Enc $T/N66R15Chk $T/N66R15Geo | grep -c lean
