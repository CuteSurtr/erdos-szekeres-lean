#!/bin/bash
# M1(b) control: the complete cert.cnf of one leaf printed by Lean (eager + activated quads + units + rows + card + sb)
# vs the recorded full_cnf_sha256 (cert.json). usage: full_check.sh LEAFINDEX CUBEID
set -e
D=/home/jay/research/data/formalize-20261122/n66enc
W=/home/jay/research/data/n66-20261113
exp=$(python3 -c "import json;print(json.load(open('$W/p2/c14/$2/it1/cert.json'))['full_cnf_sha256'])")
got=$($D/build/bin/n66print full $1 $D/ctl/act_$2.txt $D/ctl/rows1832.txt | sha256sum | cut -d' ' -f1)
echo "recorded full_cnf_sha256: $exp"
echo "lean full print:          $got"
[ "$exp" = "$got" ] && echo FULL_MATCH || echo FULL_DIFFER
