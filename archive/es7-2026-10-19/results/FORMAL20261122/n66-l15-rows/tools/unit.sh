#!/bin/bash
# Run a command as a gated systemd user unit of slot l15r (track ag).
# usage: unit.sh <job> <MemoryMax> <RuntimeMaxSec> <expected peak MB> <command...>
# Writes logs/gate_<job>.log, and logs/peak_<job>.txt (exit code, cgroup memory.peak) when the job ends.
set -u
D=/home/jay/research/data/formalize-20261122/n66-l15-rows
job=$1; mm=$2; rt=$3; pk=$4; shift 4
$D/tools/gate.sh $pk > $D/logs/gate_$job.log 2>&1 || { echo "gate gave up (logs/gate_$job.log)"; exit 1; }
printf -v cmd '%q ' "$@"
systemd-run --user --unit=esr-ag-l15r-$job --collect -p CPUQuota=100% -p MemoryMax=$mm -p MemorySwapMax=0 \
  -p RuntimeMaxSec=$rt --nice=10 --working-directory=$D \
  bash -c "$cmd; rc=\$?; cg=\$(cut -d: -f3 /proc/self/cgroup); echo \"rc=\$rc peak=\$(cat /sys/fs/cgroup\$cg/memory.peak)\" > $D/logs/peak_$job.txt; exit \$rc"
