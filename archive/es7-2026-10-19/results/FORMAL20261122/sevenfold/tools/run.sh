#!/bin/bash
# run.sh JOB CMD...: start the command as unit esr-ag-lenc7-JOB (caps of the task) after the gate, and wait for it.
W=/home/jay/research/data/formalize-20261122/sevenfold
job=$1; shift
"$W/tools/gate.sh" || exit 99
systemd-run --user --wait --collect --unit="esr-ag-lenc7-$job" -p CPUQuota=100% -p MemoryMax=3500M -p MemorySwapMax=0 \
  -p MemoryHigh=2800M -p RuntimeMaxSec=7200 --nice=10 --working-directory="$W" "$@"
