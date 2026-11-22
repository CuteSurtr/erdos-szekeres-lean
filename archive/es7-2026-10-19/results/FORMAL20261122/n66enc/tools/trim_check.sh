#!/bin/bash
# M1(c): print leaf I's certificate from Lean (n66print trim I DESC) and compare its SHA-256 with the recorded
# trim_cnf_sha256 of that leaf (campaign_status.json and cert.json). usage: trim_check.sh DESCDIR OUT.tsv [I ...]
D=/home/jay/research/data/formalize-20261122/n66enc
W=/home/jay/research/data/n66-20261113
DESC=$1; OUT=$2; shift 2
IDS=${@:-$(seq 0 131)}
for i in $IDS; do
  cid=$(sed -n "$((i+1))p" $D/tools/leaf_order.txt)
  read -r rec1 rec2 <<< $(python3 -c "
import json
st=json.load(open('$W/p2/c14/campaign_status.json'))['cubes']['$cid']
cj=json.load(open('$W/'+st['certdir']+'/cert.json'))
print(st['trim_cnf_sha256'], cj['trim_cnf_sha256'])")
  got=$($D/build/bin/n66print trim $i $DESC/$i.txt 2>>$D/logs/trim_print.err | sha256sum | cut -d' ' -f1)
  v=MATCH; { [ "$got" = "$rec1" ] && [ "$got" = "$rec2" ]; } || v=DIFFER
  printf "%s\t%s\t%s\t%s\t%s\n" "$i" "$cid" "$got" "$rec1" "$v" >> $OUT
done
