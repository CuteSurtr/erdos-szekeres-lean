#!/bin/sh
# F6: rebuild the skip file from W30 and other WAVE2 helpers' U_L8 leaves (never F6's own)
R=/home/user/erdos-szekeres-lean/cloud/es7-2026-10-19/results
S=$(ls $R/WAVE2/*/U_L8/leaves.jsonl 2>/dev/null | grep -v /F6/)
python3 $R/WAVE2/F6/mkskip.py 6c05114f422e02810378941f606a0b34f9c2e943b042880a1a2f065dc7f1bfd5 \
  $R/WAVE2/F6/U_L8/share.icnf /opt/work/skip.icnf $R/WAVE1/W30/U_L8/leaves.jsonl $S
