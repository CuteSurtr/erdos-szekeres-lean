#!/bin/bash
# usage: launch.sh JOB  — gates (tools/gate.sh), then the one unit esr-ag-lrv3-JOB running tools/review_unit.sh; waits.
RV=/home/jay/research/data/formalize-20261122/v182-lean/review
J=$1
$RV/tools/gate.sh >> $RV/logs/gate_$J.log 2>&1 || { echo "GATE_GAVE_UP"; exit 1; }
tail -1 $RV/logs/gate_$J.log
systemd-run --user --wait --unit=esr-ag-lrv3-$J -p CPUQuota=100% -p MemoryMax=3500M -p MemorySwapMax=0 \
  -p RuntimeMaxSec=7200 --nice=10 --working-directory=$RV /bin/bash $RV/tools/review_unit.sh
echo "UNIT_DONE rc=$?"
