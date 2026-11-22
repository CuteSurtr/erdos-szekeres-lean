#!/bin/bash
# M1/M2 cube controls in one unit (exe hash logged first):
#  (a) `n66r15print stats`; `n66r15print rows` vs n66-level15's rows_used15.txt (R1_15 printed = R0_15's file bytes);
#  (b) full cert.cnf of leaf 0 (12 cube literals) and leaf 22 (largest trim) vs full_cnf_sha256;
#  (c) the 105 trims, coreutils only (tools/trim_check.sh); the largest leaf (22) timed with /usr/bin/time -v.
set -uo pipefail
D=/home/jay/research/data/formalize-20261122/n66-l15-rows
L15=/home/jay/research/data/formalize-20261122/n66-level15
EXE=$D/build/bin/n66r15print
cd $D
echo "== start $(date '+%F %T') exe $(sha256sum $EXE | cut -d' ' -f1)"
/usr/bin/time -f "stats wall=%e s maxrss=%M KB" $EXE stats
r=$($EXE rows | sha256sum | cut -d' ' -f1); f=$(sha256sum $L15/lean/N66E15/data/rows_used15.txt | cut -d' ' -f1)
echo "rows print $r  rows_used15.txt $f  $([ "$r" = "$f" ] && echo ROWS_MATCH || echo ROWS_DIFFER)"
for I in 0 22; do tools/full_check.sh $I; done
echo "== largest leaf (22) timed $(date '+%F %T')"
/usr/bin/time -v $EXE trim 22 $L15/desc/22.txt 2> logs/trim22_time.txt | sha256sum
grep -E "Maximum resident|Elapsed|Exit status" logs/trim22_time.txt
echo "== trims $(date '+%F %T')"
rm -f logs/trim_all.tsv logs/trim_print.err
tools/trim_check.sh logs/trim_all.tsv
echo "MATCH $(grep -c 'MATCH$' logs/trim_all.tsv) DIFFER $(grep -c 'DIFFER$' logs/trim_all.tsv)"
echo "distinct printed hashes $(grep -v '^#' logs/trim_all.tsv | cut -f3 | sort -u | wc -l)"
echo "== done $(date '+%F %T') exe $(sha256sum $EXE | cut -d' ' -f1)"
