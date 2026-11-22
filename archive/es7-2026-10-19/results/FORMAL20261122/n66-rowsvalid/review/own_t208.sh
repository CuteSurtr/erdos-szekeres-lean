#!/bin/bash
# Own T208 sub-list print with the frozen exe (slot lrv3, unit esr-ag-lrv3-st), only if memory projects safely:
# 1. rowprint st 26 one.idx (one clause of T26) measures the sub-list path's RSS on the 138 MiB template;
# 2. projection for st 208 = RSS(st 26) * 3303824 / 2426008 (full-print RSS of T208 in M9 / of T26 in own E1);
# 3. only if the projection is <= 2,800,000 KB: rowprint st 208 data/trim208.idx, hash compared with VB's trimmed CNF.
D=/home/jay/research/data/formalize-20261122/n66-rowsvalid
R=$D/review
EXE=$D/build/bin/rowprint
EH0=7140a6ffffb0e34b3074673c858e5584b7f2f31e482cd6e57490fa1e86e46344
S=$R/t208_st_summary.txt
echo "start $(date '+%F %T') exe $(sha256sum $EXE | cut -c1-64)" > $S
[ "$(sha256sum $EXE | cut -c1-64)" = "$EH0" ] || { echo "EXE CHANGED" >> $S; exit 3; }
echo 0 > $R/one.idx
h26=$( { /usr/bin/time -f "%M %e" -o $R/.t26 $EXE st 26 $R/one.idx < /dev/null; } | sha256sum | cut -c1-64 )
read r26 s26 < $R/.t26
echo "st 26 one.idx: maxrss_kb=$r26 secs=$s26 sha=$h26" >> $S
proj=$(( r26 * 3303824 / 2426008 ))
echo "projected st 208: maxrss_kb=$proj" >> $S
if [ "$proj" -le 2800000 ]; then
  h=$( { /usr/bin/time -f "%M %e" -o $R/.t208 $EXE st 208 $D/data/trim208.idx < /dev/null; } | sha256sum | cut -c1-64 )
  read r s < $R/.t208
  want=$(zstd -dcq /home/jay/research/data/n66-20261113/vfy15/rows/jobs/T_849f8a5e23a1fc77.trimmed.cnf.zst | sha256sum | cut -c1-64)
  echo "st 208 trim208.idx: maxrss_kb=$r secs=$s printed=$h vb_trimmed=$want $([ "$h" = "$want" ] && echo MATCH || echo MISMATCH)" >> $S
else
  echo "st 208 not run (projection above 2,800,000 KB)" >> $S
fi
echo "end $(date '+%F %T') exe $(sha256sum $EXE | cut -c1-64)" >> $S
rm -f $R/.t26 $R/.t208
