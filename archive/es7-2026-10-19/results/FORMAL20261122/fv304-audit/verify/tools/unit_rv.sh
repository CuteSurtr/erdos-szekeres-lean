#!/bin/bash
# rv4: body of unit esr-ag-rv4-fv304s. The ONE compile of this review: src/RV.lean, no -o (no olean written).
# LEAN_PATH = FV304's lean_path.txt + the audit's olean root, both read only. A sampler records the cgroup's
# anon+shmem peak every 0.5 s and sends SIGTERM to lean at 3,200 MB (80 % of MemoryMax=4000M; pre-registered).
# Page cache (memory.peak, `high` events) is reported, not a stop: about 25 GB of chunk oleans are mapped.
V=/home/jay/research/data/formalize-20261122/fv304-audit/verify
log=$V/logs/rv.log
export LEAN_PATH="$(cat /home/jay/research/data/fv304-20261120/lean_path.txt):/home/jay/research/data/formalize-20261122/fv304-audit/olean"
cg=/sys/fs/cgroup$(cut -d: -f3 /proc/self/cgroup)
LIMIT=$((3200 * 1048576))
echo "$LEAN_PATH" > $V/data/lean_path_rv.txt
/usr/bin/time -v /home/jay/.elan/toolchains/leanprover--lean4---v4.24.0/bin/lean -j1 -R $V/src $V/src/RV.lean > "$log" 2>&1 &
tp=$!
( m=0; while kill -0 $tp 2>/dev/null; do
    a=$(awk '$1=="anon"||$1=="shmem"{s+=$2} END{printf "%d", s}' "$cg/memory.stat")
    [ "${a:-0}" -gt "$m" ] && m=$a && echo "$m" > $V/logs/rv.anon
    if [ "${a:-0}" -ge "$LIMIT" ]; then echo "$a" > $V/logs/rv.killed; pkill -TERM -P $tp; fi
    sleep 0.5; done ) &
sp=$!
wait $tp; rc=$?
wait $sp
{ echo "lean_rc=$rc"
  echo "cgroup memory.peak: $(cat $cg/memory.peak)"
  echo "cgroup memory.swap.peak: $(cat $cg/memory.swap.peak)"
  echo "cgroup anon+shmem peak (sampled every 0.5 s): $(cat $V/logs/rv.anon 2>/dev/null)"
  [ -e $V/logs/rv.killed ] && echo "KILLED by the 80 % rule at anon+shmem $(cat $V/logs/rv.killed) bytes"
  echo "cgroup memory.events: $(tr '\n' ' ' < $cg/memory.events)"; } >> "$log"
exit $rc
