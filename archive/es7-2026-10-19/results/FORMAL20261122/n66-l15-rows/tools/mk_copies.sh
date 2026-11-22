#!/bin/bash
# Copy (not edit) n66-rowsvalid's row machinery into this work dir under non-clashing names, rebased on the level-15
# encoder: RowEnc -> N66R15Enc, RowGeo -> N66R15Geo, RowChk -> N66R15Chk, N66Enc -> N66E15, N66Geo -> N66G15.
# RowEnc/Main.lean becomes N66R15Enc/RowMain.lean. Assembly.lean and End.lean get hand edits afterwards
# (DESIGN.md §3); the generated row chunks are not copied (tools/gen_rows15.py writes the level-15 ones).
# Refuses to overwrite without --write.
set -eu
[ "${1:-}" = "--write" ] || { echo "refusing to overwrite copies without --write"; exit 2; }
S=/home/jay/research/data/formalize-20261122/n66-rowsvalid/lean
T=/home/jay/research/data/formalize-20261122/n66-l15-rows/lean
mkdir -p $T/N66R15Enc $T/N66R15Geo $T/N66R15Chk
ren() { sed -e 's/RowEnc/N66R15Enc/g' -e 's/RowGeo/N66R15Geo/g' -e 's/RowChk/N66R15Chk/g' -e 's/N66Enc/N66E15/g' -e 's/N66Geo/N66G15/g' "$1" > "$2"; }
for f in Gen DataT0 DataT1 DataT2 DataT3 DataT DataC0 DataC1 DataC2 DataC3 DataC; do ren $S/RowEnc/$f.lean $T/N66R15Enc/$f.lean; done
ren $S/RowEnc/Main.lean $T/N66R15Enc/RowMain.lean
for f in Basic Sem Eight Oct Row Kinds Assembly End; do ren $S/RowGeo/$f.lean $T/N66R15Geo/$f.lean; done
CHK="Tables Look TabPs TabTt TabDr0 TabDr1 TabDr TabCan Check CertsOk IsCore"
for i in $(seq 0 13); do CHK="$CHK TabTt$i"; done
for i in 0 1 2 3; do CHK="$CHK certsOkTF$i certsOkCF$i"; done
for f in $CHK; do ren $S/RowChk/$f.lean $T/N66R15Chk/$f.lean; done
echo "copied $(ls $T/N66R15Enc | wc -l) + $(ls $T/N66R15Geo | wc -l) + $(ls $T/N66R15Chk | wc -l) files"
