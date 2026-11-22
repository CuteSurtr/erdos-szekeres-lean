#!/bin/bash
# usage: start_unit.sh JOB RUNTIME_MIN command...   (gates first; unit esr-ag-lrb-JOB; output to logs/JOB.log)
set -euo pipefail
D=/home/jay/research/data/formalize-20261122/res118-rowblocks
job=$1; mins=$2; shift 2
$D/tools/gate.sh
systemd-run --user --unit=esr-ag-lrb-$job -p CPUQuota=100% -p MemoryMax=3500M -p MemorySwapMax=0 \
  -p RuntimeMaxSec=$((mins*60)) --nice=10 --working-directory=$D \
  /bin/bash -c "exec \"\$@\" > $D/logs/$job.log 2>&1" bash "$@"
echo "started esr-ag-lrb-$job"
