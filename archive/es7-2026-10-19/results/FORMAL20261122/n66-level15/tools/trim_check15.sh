#!/bin/bash
# M1(c), coreutils only: print leaf I's certificate from Lean (n66print15 trim I DESC/I.txt), hash the bytes with
# sha256sum and compare with sha256sum of that leaf's certified trim.cnf and the recorded trim_cnf_sha256
# (campaign_status.json). usage: trim_check15.sh DESCDIR OUT.tsv [I ...]   (default 0..104)
D=/home/jay/research/data/formalize-20261122/n66-level15
W=/home/jay/research/data/n66-20261113
DESC=$1; OUT=$2; shift 2
IDS=${@:-$(seq 0 104)}
echo "# exe $(sha256sum $D/build/bin/n66print15 | cut -d' ' -f1)" >> $OUT
for i in $IDS; do
  cid=$(sed -n "$((i+1))p" $D/tools/leaf_order15.txt)
  read -r cdir rec <<< $(python3 -I -c "
import json
c=json.load(open('$W/p2/c15/campaign_status.json'))['cubes']['$cid']
print(c['certdir'], c['trim_cnf_sha256'])")
  file=$(sha256sum $W/$cdir/trim.cnf | cut -d' ' -f1)
  got=$($D/build/bin/n66print15 trim $i $DESC/$i.txt 2>>$D/logs/trim_print.err | sha256sum | cut -d' ' -f1)
  v=MATCH; { [ "$got" = "$rec" ] && [ "$got" = "$file" ]; } || v=DIFFER
  printf "%s\t%s\t%s\t%s\t%s\t%s\n" "$i" "$cid" "$got" "$file" "$rec" "$v" >> $OUT
done
