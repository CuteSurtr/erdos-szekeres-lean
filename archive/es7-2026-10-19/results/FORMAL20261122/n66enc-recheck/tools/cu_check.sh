#!/bin/bash
# Coreutils cross-check of EAGER and FULL 131 (independent of recheck.py's Python comparator): sha256sum + cmp.
# Runs the frozen exe four times, one at a time. Output: logs/cu_check.log
D=/home/jay/research/data/formalize-20261122/n66enc-recheck
C=/home/jay/research/data/n66-20261113/p2/c14/hhhhhh/it1/cert.cnf
X=$D/bin/n66print
A=$D/ctl/hhhhhh/act.txt; R=$D/ctl/hhhhhh/rows.txt
exec >> $D/logs/cu_check.log 2>&1
echo "== $(date '+%F %T') exe $(sha256sum < $X | cut -c1-64)"
[ "$(sha256sum < $X | cut -c1-64)" = 98d121bad04264221de66e583db0df08f4431d1093b4b7a05114316accccaa46 ] || { echo ABORT_NOT_FROZEN; exit 1; }
echo "eager printed: $($X eager | sha256sum | cut -c1-64) rc=${PIPESTATUS[0]}"
echo "eager segment: $(tail -n +2 $C | head -n 1489581 | sha256sum | cut -c1-64)"
$X eager | cmp - <(tail -n +2 $C | head -n 1489581) && echo "eager cmp: EQUAL" || echo "eager cmp: DIFFER"
echo "full printed:  $($X full 131 $A $R 2>/dev/null | sha256sum | cut -c1-64) rc=${PIPESTATUS[0]}"
echo "cert.cnf file: $(sha256sum < $C | cut -c1-64)"
$X full 131 $A $R 2>/dev/null | cmp - $C && echo "full cmp: EQUAL" || echo "full cmp: DIFFER"
echo "== $(date '+%F %T') end"
