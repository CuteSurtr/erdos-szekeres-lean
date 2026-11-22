#!/bin/bash
# One measured build unit (after the gates): run_mod.sh JOB Path1 Path2 ... ; log in logs/JOB.log
D=/home/jay/research/data/formalize-20261122/v182-lean
J=$1; shift
$D/tools/gate.sh || exit 1
systemd-run --user --unit=esr-ag-l182-$J -p CPUQuota=100% -p MemoryMax=3500M -p MemorySwapMax=0 -p RuntimeMaxSec=7200 \
  --nice=10 --working-directory=$D /bin/bash -c "/usr/bin/time -v $D/tools/build_mod.sh $* > $D/logs/$J.log 2>&1; echo EXIT \$? >> $D/logs/$J.log"
