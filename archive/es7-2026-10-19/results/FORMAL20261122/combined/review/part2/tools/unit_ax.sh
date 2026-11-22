#!/bin/bash
# rv5 part 2: body of THE ONE review compile (unit esr-ag-rv5-p2ax). LEAN_PATH from the unit environment. No -o.
# /usr/bin/time -v, a 0.2 s sampler of the cgroup's anon+shmem (SIGTERM to lean at STOP_MB), cgroup figures at the end.
# Usage: unit_ax.sh STOP_MB
set -u
P=/home/jay/research/data/formalize-20261122/combined/review/part2
log=$P/logs/RV5P2Review.log stop_mb=$1
cg=/sys/fs/cgroup$(cut -d: -f3 /proc/self/cgroup)
LIMIT=$((stop_mb * 1048576))
rm -f $P/logs/anon_peak.txt $P/logs/killed.txt
echo "start $(date '+%F %T') sha256(lean file)=$(sha256sum $P/lean/RV5P2Review.lean | cut -c1-64) LEAN_PATH=$LEAN_PATH" > $P/logs/unit_ax.info
/usr/bin/time -v /home/jay/.elan/toolchains/leanprover--lean4---v4.24.0/bin/lean -j1 -R $P/lean $P/lean/RV5P2Review.lean > $log 2>&1 &
tp=$!
( m=0; while kill -0 $tp 2>/dev/null; do
    a=$(awk '$1=="anon"||$1=="shmem"{s+=$2} END{printf "%d", s}' $cg/memory.stat)
    [ "${a:-0}" -gt "$m" ] && m=$a && echo $m > $P/logs/anon_peak.txt
    if [ "${a:-0}" -ge "$LIMIT" ] && [ ! -e $P/logs/killed.txt ]; then echo $a > $P/logs/killed.txt; pkill -TERM -P $tp; fi
    sleep 0.2; done ) &
sp=$!
wait $tp; rc=$?
wait $sp
{ echo "lean_rc=$rc"; echo "end $(date '+%F %T')"
  echo "cgroup memory.peak: $(cat $cg/memory.peak)"; echo "cgroup memory.swap.peak: $(cat $cg/memory.swap.peak)"
  echo "cgroup anon+shmem peak (0.2 s sampler): $(cat $P/logs/anon_peak.txt 2>/dev/null)"
  [ -e $P/logs/killed.txt ] && echo "KILLED by the 80 % rule at $(cat $P/logs/killed.txt) bytes"
  echo "cgroup memory.events: $(tr '\n' ' ' < $cg/memory.events)"; } >> $log
exit $rc
