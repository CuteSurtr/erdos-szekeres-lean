#!/bin/bash
# M1(b) control: the complete level-15 cert.cnf of leaf I printed by Lean (eager + activated quads + units + rows +
# card + sb) vs the recorded full_cnf_sha256 (cert.json, campaign_status.json; c15_post.sh checked it against the
# original file before packing). usage: full_check15.sh LEAFINDEX
set -e
D=/home/jay/research/data/formalize-20261122/n66-level15
W=/home/jay/research/data/n66-20261113
I=$1
cid=$(sed -n "$((I+1))p" $D/tools/leaf_order15.txt)
read -r exp1 exp2 <<< $(python3 -I -c "
import json
c=json.load(open('$W/p2/c15/campaign_status.json'))['cubes']['$cid']
cj=json.load(open('$W/'+c['certdir']+'/cert.json'))
print(c['full_cnf_sha256'], cj['full_cnf_sha256'])")
echo "exe $(sha256sum $D/build/bin/n66print15 | cut -d' ' -f1)"
got=$(/usr/bin/time -f "full wall=%e s maxrss=%M KB" $D/build/bin/n66print15 full $I $D/ctl/act_$I.txt $D/ctl/rows1832.txt | sha256sum | cut -d' ' -f1)
echo "leaf $I $cid"
echo "recorded full_cnf_sha256 (campaign, cert.json): $exp1 $exp2"
echo "lean full print:                               $got"
[ "$exp1" = "$got" ] && [ "$exp2" = "$got" ] && echo FULL_MATCH || echo FULL_DIFFER
