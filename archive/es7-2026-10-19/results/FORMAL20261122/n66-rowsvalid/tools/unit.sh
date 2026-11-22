#!/bin/bash
# Run a command as a gated systemd user unit of slot lrv. usage: unit.sh <job> <command...>
# The job records its cgroup memory.peak in logs/peak_<job>.txt when it ends.
set -u
D=/home/jay/research/data/formalize-20261122/n66-rowsvalid
job=$1; shift
$D/tools/gate.sh > $D/logs/gate_$job.log 2>&1 || { echo "gate gave up"; exit 1; }
printf -v cmd '%q ' "$@"
systemd-run --user --unit=esr-ag-lrv-$job -p CPUQuota=100% -p MemoryMax=3500M -p MemorySwapMax=0 \
  -p RuntimeMaxSec=7200 --nice=10 --working-directory=$D --collect \
  bash -c "$cmd; rc=\$?; cg=\$(cut -d: -f3 /proc/self/cgroup); echo \"rc=\$rc peak=\$(cat /sys/fs/cgroup\$cg/memory.peak)\" > $D/logs/peak_$job.txt; exit \$rc"
