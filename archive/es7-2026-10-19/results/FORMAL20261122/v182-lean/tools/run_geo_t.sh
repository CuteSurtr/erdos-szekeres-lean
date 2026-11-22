#!/bin/bash
# Like run_geo.sh but measured with /usr/bin/time -v: run_geo_t.sh JOB Mod1 ... ; log in logs/JOB.log
D=/home/jay/research/data/formalize-20261122/v182-lean
J=$1; shift
$D/tools/gate.sh || exit 1
systemd-run --user --unit=esr-ag-l182-$J -p CPUQuota=100% -p MemoryMax=3500M -p MemorySwapMax=0 -p RuntimeMaxSec=7200 \
  --nice=10 --working-directory=$D /bin/bash -c "/usr/bin/time -v $D/tools/build_geo.sh $* > $D/logs/$J.log 2>&1; echo EXIT \$? >> $D/logs/$J.log"
