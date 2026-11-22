#!/bin/bash
# Own E1 re-run (reviewer slot lrv3; bash + coreutils only; none of the worker's scripts).
# For every leaf index i of review/leafmap15.tsv (the reviewer's own map: olean dump of leaves105 -> campaign cube
# with equal literal list -> its certdir), the frozen printer prints `trim i desc/i.txt`. The output is compared byte
# for byte (cmp) with the certified trim.cnf in that leaf's own certdir and hashed with coreutils sha256sum.
# One exe at a time; the exe hash is checked before every run and at the end. Then three negative controls and the
# exe's `leaves` mode (compiled code) for comparison with the olean dump (interpreter).
set -u
D=/home/jay/research/data/formalize-20261122/n66-level15
RV=$D/review
W=/home/jay/research/data/n66-20261113
EXE=$D/build/bin/n66print15
FROZEN=63d7fc9913fc1d80c423512470370644c62643c7ea785343ddb27426cb35a229
T=$RV/tmp/e1
mkdir -p $T
OUT=$RV/e1_runs.tsv
LOG=$RV/e1_exe_hashes.txt
printf 'i\tid\texe_sha\trc\tmaxrss_kb\twall_s\tprinted_sha\tprinted_bytes\tfile_sha\tfile_bytes\tcmp\tstderr\n' > $OUT
echo "start $(date '+%F %T')" > $LOG
require_frozen() {   # runs in the main shell (never inside $(...)), so exit 3 stops the script
  local h; h=$(sha256sum $EXE | cut -d' ' -f1)
  echo "exe $1 $h" >> $LOG
  [ "$h" = "$FROZEN" ] || { echo "EXE CHANGED ($1)" >> $LOG; exit 3; }
}
require_frozen start
run_one() {   # $1 = index, $2 = descriptor file; output in $T/out, $T/err, $T/time
  /usr/bin/time -f '%x %M %e' -o $T/time $EXE trim "$1" "$2" > $T/out 2> $T/err
}
while IFS=$'\t' read -r i cid cdr; do
  h=$(sha256sum $EXE | cut -d' ' -f1)
  [ "$h" = "$FROZEN" ] || { echo "EXE CHANGED (leaf $i): $h" >> $LOG; exit 3; }
  ref=$W/$cdr/trim.cnf
  run_one $i $D/desc/$i.txt
  read -r rc rss wall < <(tail -1 $T/time)
  ps=$(sha256sum < $T/out | cut -d' ' -f1); pb=$(stat -c %s $T/out)
  fs=$(sha256sum < $ref | cut -d' ' -f1); fb=$(stat -c %s $ref)
  cmp -s $T/out $ref; c=$?
  e=$(tr '\t\n' '  ' < $T/err)
  printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' "$i" "$cid" "$h" "$rc" "$rss" "$wall" "$ps" "$pb" "$fs" "$fb" "$c" "$e" >> $OUT
  rm -f $T/out
done < $RV/leafmap15.tsv
echo "loop end $(date '+%F %T')" >> $LOG
# negative controls
CTL=$RV/e1_controls.txt
: > $CTL
# (a) leaf 0 with its first `E k` descriptor changed to `E k+1`: must print a different text (or refuse)
awk 'BEGIN{d=0} $1=="E" && d==0 {print "E", $2+1; d=1; next} {print}' $D/desc/0.txt > $T/mut0.txt
require_frozen ctl-a; run_one 0 $T/mut0.txt; read -r rc rss wall < <(tail -1 $T/time)
ref0=$W/$(awk -F'\t' '$1==0{print $3}' $RV/leafmap15.tsv)/trim.cnf
echo "a mutated-E rc=$rc bytes=$(stat -c %s $T/out) sha=$(sha256sum < $T/out | cut -d' ' -f1) ref=$(sha256sum < $ref0 | cut -d' ' -f1) cmp=$(cmp -s $T/out $ref0; echo $?)" >> $CTL
# (b) leaf index 105 (out of range): must refuse with exit 1 and empty stdout
require_frozen ctl-b; run_one 105 $D/desc/0.txt; read -r rc rss wall < <(tail -1 $T/time)
echo "b index105 rc=$rc stdout_bytes=$(stat -c %s $T/out) stderr=$(tr '\n' ' ' < $T/err)" >> $CTL
# (c) an invalid quadruple descriptor appended (not okQuad: repeated state): must refuse with exit 1 and empty stdout
{ cat $D/desc/0.txt; echo "Q 3 3 4 5 0"; } > $T/badq.txt
require_frozen ctl-c; run_one 0 $T/badq.txt; read -r rc rss wall < <(tail -1 $T/time)
echo "c badquad rc=$rc stdout_bytes=$(stat -c %s $T/out) stderr=$(tr '\n' ' ' < $T/err)" >> $CTL
# (d) informational: leaf 1's descriptors printed as leaf 0 (cube units are taken from the Lean leaf 0, so the text
#     differs from leaf 1's file wherever a unit of the differing literal is used; no pass/fail expectation)
require_frozen ctl-d; run_one 0 $D/desc/1.txt; read -r rc rss wall < <(tail -1 $T/time)
ref1=$W/$(awk -F'\t' '$1==1{print $3}' $RV/leafmap15.tsv)/trim.cnf
echo "d swapped rc=$rc sha=$(sha256sum < $T/out | cut -d' ' -f1) ref0=$(sha256sum < $ref0 | cut -d' ' -f1) ref1=$(sha256sum < $ref1 | cut -d' ' -f1)" >> $CTL
rm -f $T/out $T/mut0.txt $T/badq.txt
# the exe's own leaves list (compiled code)
require_frozen leaves
/usr/bin/time -f '%x %M %e' -o $T/time_leaves $EXE leaves > $RV/e1_exe_leaves.txt 2> $T/err_leaves
echo "leaves rc/maxrss/wall $(tail -1 $T/time_leaves)" >> $LOG
require_frozen end
echo "end $(date '+%F %T')" >> $LOG
