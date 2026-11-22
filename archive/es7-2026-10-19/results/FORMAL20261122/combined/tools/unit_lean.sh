#!/bin/bash
# combined: body of one esr-ag-lcb-* compile unit (fv304-audit's unit_lean.sh with the stop level as an argument).
# LEAN_PATH comes from the unit's environment. Compiles SRC with the pinned v4.24.0 binary (-R ROOT); OUT "-" writes
# no olean, else OUT.tmp is renamed to OUT on rc 0. A sampler records the cgroup's anon+shmem peak every 0.2 s (what
# memguard.sh counts; swap is 0 by MemorySwapMax=0) and sends SIGTERM to lean at STOP_MB (80 % of MemoryMax,
# pre-registered in README). Appends lean_rc and the cgroup memory figures to LOG.
# Usage: unit_lean.sh LOG OUT ROOT SRC STOP_MB
log=$1 out=$2 root=$3 src=$4 stop_mb=$5
cg=/sys/fs/cgroup$(cut -d: -f3 /proc/self/cgroup)
LIMIT=$((stop_mb * 1048576))
rm -f "$log.stop" "$log.anon" "$log.killed"
o=(); [ "$out" != "-" ] && { mkdir -p "$(dirname "$out")"; o=(-o "$out.tmp"); }
/usr/bin/time -v /home/jay/.elan/toolchains/leanprover--lean4---v4.24.0/bin/lean -j1 -R "$root" "${o[@]}" "$src" > "$log" 2>&1 &
tp=$!
( m=0; while [ ! -e "$log.stop" ]; do
    a=$(awk '$1=="anon"||$1=="shmem"{s+=$2} END{printf "%d", s}' "$cg/memory.stat")
    [ "${a:-0}" -gt "$m" ] && m=$a
    echo "$m" > "$log.anon"
    if [ "${a:-0}" -ge "$LIMIT" ] && [ ! -e "$log.killed" ]; then
      echo "$a" > "$log.killed"; pkill -TERM -P "$tp"
    fi
    sleep 0.2; done ) &
sp=$!
wait "$tp"; rc=$?
touch "$log.stop"; wait "$sp"
if [ "$out" != "-" ]; then
  if [ $rc -eq 0 ] && [ -f "$out.tmp" ]; then mv "$out.tmp" "$out"; else rm -f "$out.tmp"; fi
fi
{ echo "lean_rc=$rc"
  echo "cgroup memory.peak: $(cat "$cg/memory.peak")"
  echo "cgroup memory.swap.peak: $(cat "$cg/memory.swap.peak")"
  echo "cgroup anon+shmem peak (sampled every 0.2 s): $(cat "$log.anon")"
  [ -e "$log.killed" ] && echo "KILLED by the 80 % rule at anon+shmem $(cat "$log.killed") bytes"
  echo "cgroup memory.events: $(tr '\n' ' ' < "$cg/memory.events")"; } >> "$log"
rm -f "$log.stop" "$log.anon" "$log.killed"
exit $rc
