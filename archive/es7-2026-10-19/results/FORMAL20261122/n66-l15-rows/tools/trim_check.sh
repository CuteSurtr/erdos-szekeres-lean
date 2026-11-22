#!/bin/bash
# M1(c), coreutils only: print leaf I's certificate with this dir's exe (n66r15print trim I DESC/I.txt; descriptors
# are n66-level15's untrusted desc/, read-only), hash the bytes with sha256sum and compare with sha256sum of that
# leaf's certified trim.cnf and the recorded trim_cnf_sha256 (campaign_status.json).
# usage: trim_check.sh OUT.tsv [I ...]   (default 0..104)
D=/home/jay/research/data/formalize-20261122/n66-l15-rows
L15=/home/jay/research/data/formalize-20261122/n66-level15
W=/home/jay/research/data/n66-20261113
EXE=$D/build/bin/n66r15print
OUT=$1; shift
IDS=${@:-$(seq 0 104)}
EH=$(sha256sum $EXE | cut -d' ' -f1)
echo "# exe $EH" >> $OUT
for i in $IDS; do
  [ "$(sha256sum $EXE | cut -d' ' -f1)" = "$EH" ] || { echo "EXE CHANGED" >> $OUT; exit 3; }
  cid=$(sed -n "$((i+1))p" $L15/tools/leaf_order15.txt)
  read -r cdir rec <<< $(python3 -I -c "
import json
c=json.load(open('$W/p2/c15/campaign_status.json'))['cubes']['$cid']
print(c['certdir'], c['trim_cnf_sha256'])")
  file=$(sha256sum $W/$cdir/trim.cnf | cut -d' ' -f1)
  got=$($EXE trim $i $L15/desc/$i.txt 2>>$D/logs/trim_print.err | sha256sum | cut -d' ' -f1)
  v=MATCH; { [ "$got" = "$rec" ] && [ "$got" = "$file" ]; } || v=DIFFER
  printf "%s\t%s\t%s\t%s\t%s\t%s\n" "$i" "$cid" "$got" "$file" "$rec" "$v" >> $OUT
done
