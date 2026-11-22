#!/bin/bash
# s3520-gate (22 Nov 2026): run a command inside the current systemd unit and sample the unit's own cgroup every 0.5 s.
# Usage: sampled.sh OUT.mem COMMAND...      (OUT.mem gets: max anon+shmem MB, max anon MB, memory.peak MB, rc)
# anon + shmem is what the memory guard counts; memory.peak also counts page cache.
set -u
out=$1; shift
cg=/sys/fs/cgroup$(sed -n 's/^0:://p' /proc/self/cgroup)
"$@" &
pid=$!
maxas=0; maxa=0
while kill -0 $pid 2>/dev/null; do
  read -r a s < <(awk '$1=="anon"{a=$2} $1=="shmem"{s=$2} END{printf "%d %d", a/1048576, s/1048576}' "$cg/memory.stat")
  [ $((a + s)) -gt $maxas ] && maxas=$((a + s))
  [ $a -gt $maxa ] && maxa=$a
  sleep 0.5
done
wait $pid; rc=$?
pk=$(( $(cat "$cg/memory.peak" 2>/dev/null || echo 0) / 1048576 ))
echo "anon_shmem_max_mb=$maxas anon_max_mb=$maxa cgroup_peak_mb=$pk rc=$rc cgroup=$cg" > "$out"
exit $rc
