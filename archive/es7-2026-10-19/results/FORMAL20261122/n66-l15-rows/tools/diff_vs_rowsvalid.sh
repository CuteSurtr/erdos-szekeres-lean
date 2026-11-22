#!/bin/bash
# Show the complete difference between this dir's copies and n66-rowsvalid's sources: apply the reverse renames
# (N66R15Enc -> RowEnc, N66R15Geo -> RowGeo, N66R15Chk -> RowChk, N66E15 -> N66Enc, N66G15 -> N66Geo) to each copy
# and diff it with its original. Output: logs/diff_vs_rowsvalid.txt (files with no difference are listed as SAME).
D=/home/jay/research/data/formalize-20261122/n66-l15-rows
S=/home/jay/research/data/formalize-20261122/n66-rowsvalid/lean
out=$D/logs/diff_vs_rowsvalid.txt; : > $out
unren() { sed -e 's/N66R15Enc/RowEnc/g' -e 's/N66R15Geo/RowGeo/g' -e 's/N66R15Chk/RowChk/g' -e 's/N66E15/N66Enc/g' -e 's/N66G15/N66Geo/g' "$1"; }
pair() { if diff -q <(unren $D/lean/$1) $S/$2 > /dev/null; then echo "SAME $1 = $2" >> $out; else echo "=== DIFF $1 vs $2" >> $out; diff <(unren $D/lean/$1) $S/$2 >> $out; fi; }
for f in Gen DataT0 DataT1 DataT2 DataT3 DataT DataC0 DataC1 DataC2 DataC3 DataC; do pair N66R15Enc/$f.lean RowEnc/$f.lean; done
pair N66R15Enc/RowMain.lean RowEnc/Main.lean
for f in Basic Sem Eight Oct Row Kinds Assembly End; do pair N66R15Geo/$f.lean RowGeo/$f.lean; done
CHK="Tables Look TabPs TabTt TabDr0 TabDr1 TabDr TabCan Check CertsOk IsCore"
for i in $(seq 0 13); do CHK="$CHK TabTt$i"; done
for i in 0 1 2 3; do CHK="$CHK certsOkTF$i certsOkCF$i"; done
for f in $CHK; do pair N66R15Chk/$f.lean RowChk/$f.lean; done
L15=/home/jay/research/data/formalize-20261122/n66-level15/lean
for p in "N66R15Enc/Print.lean N66E15/Print.lean" "N66R15Enc/Main.lean N66E15/Main.lean" "N66R15Enc/Bridge.lean N66E15/Bridge.lean"; do
  set -- $p; echo "=== DIFF $1 vs n66-level15 $2 (N66R15Enc -> N66E15)" >> $out
  diff <(sed -e 's/N66R15Enc/N66E15/g' $D/lean/$1) $L15/$2 >> $out
done
echo "SAME: $(grep -c '^SAME' $out)  DIFF: $(grep -c '^=== DIFF' $out)"
