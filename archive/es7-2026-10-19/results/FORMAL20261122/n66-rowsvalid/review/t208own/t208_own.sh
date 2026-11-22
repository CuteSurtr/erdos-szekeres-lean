#!/bin/bash
# Independent T208 reproduction (main session, 22 Nov 2026): print the trimmed sub-list and the full n = 29 text with
# the frozen exe, hash both, compare with VB's recorded trimmed/full hashes and the decompressed VB files.
D=/home/jay/research/data/formalize-20261122/n66-rowsvalid; J=/home/jay/research/data/n66-20261113/vfy15/rows/jobs
EXE=$D/build/bin/rowprint; K=T_849f8a5e23a1fc77; O=$D/review/t208own
echo "start $(date '+%F %T') exe $(sha256sum $EXE | cut -c1-64)"
p=$($EXE st 208 $D/data/trim208.idx | sha256sum | cut -c1-64); echo "printed_trimmed $p"
echo "vb_trimmed_recorded $(awk '/trimmed.cnf/{print $1}' $J/$K.trimmed.sha256)"
echo "vb_trimmed_file     $(zstd -dc $J/$K.trimmed.cnf.zst | sha256sum | cut -c1-64)"
echo "vb_trimmed_verdict_lines $(grep -cx 's VERIFIED UNSAT' $J/$K.trimmed.cake.out)"
f=$($EXE t 208 | sha256sum | cut -c1-64); echo "printed_full $f"
echo "vb_full_file        $(zstd -dc $J/$K.cnf.zst | sha256sum | cut -c1-64)"
echo "end $(date '+%F %T') exe $(sha256sum $EXE | cut -c1-64)"
