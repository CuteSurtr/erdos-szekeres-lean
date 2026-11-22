#!/bin/bash
# Run a command as a gated systemd user unit esr-ag-rv5-<job> (track ag), one at a time.
# usage: unit.sh <job> <MemoryMax> <RuntimeMaxSec> <expected peak MB> <command...>
# Writes review/gate_<job>.log and review/peak_<job>.txt (exit code, cgroup memory.peak, max anon sampled).
set -u
V=/home/jay/research/data/formalize-20261122/n66-l15-rows/review
job=$1; mm=$2; rt=$3; pk=$4; shift 4
$V/gate.sh $pk > $V/gate_$job.log 2>&1 || { echo "gate gave up ($V/gate_$job.log)"; exit 1; }
printf -v cmd '%q ' "$@"
systemd-run --user --unit=esr-ag-rv5-$job --collect -p CPUQuota=100% -p MemoryMax=$mm -p MemorySwapMax=0 \
  -p RuntimeMaxSec=$rt --nice=10 --working-directory=$V \
  bash -c "cg=\$(cut -d: -f3 /proc/self/cgroup); ( m=0; while :; do a=\$(awk '\$1==\"anon\"{print int(\$2/1048576)}' /sys/fs/cgroup\$cg/memory.stat 2>/dev/null); [ -n \"\$a\" ] && [ \"\$a\" -gt \"\$m\" ] && { m=\$a; echo \$m > $V/anonmax_$job.txt; }; sleep 1; done ) & s=\$!; $cmd; rc=\$?; kill \$s 2>/dev/null; echo \"rc=\$rc peak=\$(cat /sys/fs/cgroup\$cg/memory.peak) anon_max_MB=\$(cat $V/anonmax_$job.txt 2>/dev/null)\" > $V/peak_$job.txt; exit \$rc"
