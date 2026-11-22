#!/bin/bash
# M1(b) control: the complete level-15 cert.cnf of leaf I printed by this dir's exe (eager + activated quads + units +
# all 15,648 rows of the row file + card + sb; n66-level15's control inputs ctl/act_I.txt, ctl/rows1832.txt,
# read-only) vs the recorded full_cnf_sha256 (campaign_status.json, cert.json). usage: full_check.sh LEAFINDEX
set -e
D=/home/jay/research/data/formalize-20261122/n66-l15-rows
L15=/home/jay/research/data/formalize-20261122/n66-level15
W=/home/jay/research/data/n66-20261113
I=$1
cid=$(sed -n "$((I+1))p" $L15/tools/leaf_order15.txt)
read -r exp1 exp2 <<< $(python3 -I -c "
import json
c=json.load(open('$W/p2/c15/campaign_status.json'))['cubes']['$cid']
cj=json.load(open('$W/'+c['certdir']+'/cert.json'))
print(c['full_cnf_sha256'], cj['full_cnf_sha256'])")
echo "exe $(sha256sum $D/build/bin/n66r15print | cut -d' ' -f1)"
echo "inputs $(sha256sum $L15/ctl/act_$I.txt $L15/ctl/rows1832.txt | awk '{print $1}' | tr '\n' ' ')"
got=$(/usr/bin/time -f "full wall=%e s maxrss=%M KB" $D/build/bin/n66r15print full $I $L15/ctl/act_$I.txt $L15/ctl/rows1832.txt | sha256sum | cut -d' ' -f1)
echo "leaf $I $cid"
echo "recorded full_cnf_sha256 (campaign, cert.json): $exp1 $exp2"
echo "lean full print:                               $got"
[ "$exp1" = "$got" ] && [ "$exp2" = "$got" ] && echo FULL_MATCH || echo FULL_DIFFER
