#!/bin/bash
# rv5: body of THE ONE review compile (unit esr-ag-rv5-ax). LEAN_PATH comes from the unit environment. No -o.
# Records /usr/bin/time -v, a 0.2 s sampler of the cgroup's anon+shmem (SIGTERM to lean at STOP_MB), cgroup figures.
# Usage: unit_ax.sh STOP_MB
set -u
R=/home/jay/research/data/formalize-20261122/combined/review
log=$R/logs/RV5Review.log stop_mb=$1
cg=/sys/fs/cgroup$(cut -d: -f3 /proc/self/cgroup)
LIMIT=$((stop_mb * 1048576))
rm -f $R/logs/anon_peak.txt $R/logs/killed.txt
echo "start $(date '+%F %T') LEAN_PATH=$LEAN_PATH" > $R/logs/unit_ax.info
/usr/bin/time -v /home/jay/.elan/toolchains/leanprover--lean4---v4.24.0/bin/lean -j1 -R $R/lean $R/lean/RV5Review.lean > $log 2>&1 &
tp=$!
( m=0; while kill -0 $tp 2>/dev/null; do
    a=$(awk '$1=="anon"||$1=="shmem"{s+=$2} END{printf "%d", s}' $cg/memory.stat)
    [ "${a:-0}" -gt "$m" ] && m=$a && echo $m > $R/logs/anon_peak.txt
    if [ "${a:-0}" -ge "$LIMIT" ] && [ ! -e $R/logs/killed.txt ]; then echo $a > $R/logs/killed.txt; pkill -TERM -P $tp; fi
    sleep 0.2; done ) &
sp=$!
wait $tp; rc=$?
wait $sp
{ echo "lean_rc=$rc"; echo "end $(date '+%F %T')"
  echo "cgroup memory.peak: $(cat $cg/memory.peak)"; echo "cgroup memory.swap.peak: $(cat $cg/memory.swap.peak)"
  echo "cgroup anon+shmem peak (0.2 s sampler): $(cat $R/logs/anon_peak.txt 2>/dev/null)"
  [ -e $R/logs/killed.txt ] && echo "KILLED by the 80 % rule at $(cat $R/logs/killed.txt) bytes"
  echo "cgroup memory.events: $(tr '\n' ' ' < $cg/memory.events)"; } >> $log
exit $rc
