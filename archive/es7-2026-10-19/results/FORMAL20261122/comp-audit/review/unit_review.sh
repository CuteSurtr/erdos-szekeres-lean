#!/bin/sh
# lrev: body of the one review unit esr-ag-lrev-axioms (cwd = this review dir; LEAN_PATH from the unit environment).
# Compiles Review.lean with the pinned v4.24.0 binary into Review.olean here, under /usr/bin/time -v, and appends
# lean_rc and the unit's cgroup figures (memory.peak, a 0.2 s sample of the anon peak, memory.events) to LOG.
# usage: unit_review.sh LOG
log=$1
cg=/sys/fs/cgroup$(cut -d: -f3 /proc/self/cgroup)
rm -f "$log.stop" "$log.anon"
( m=0; while [ ! -e "$log.stop" ]; do
    a=$(awk '$1=="anon"{print $2}' "$cg/memory.stat"); [ "${a:-0}" -gt "$m" ] && m=$a
    echo "$m" > "$log.anon"; sleep 0.2; done ) &
/usr/bin/time -v /home/jay/.elan/toolchains/leanprover--lean4---v4.24.0/bin/lean -j1 -R . -o Review.olean Review.lean > "$log" 2>&1
rc=$?
touch "$log.stop"; wait
{ echo "lean_rc=$rc"
  echo "cgroup memory.peak: $(cat "$cg/memory.peak")"
  echo "cgroup memory.swap.peak: $(cat "$cg/memory.swap.peak")"
  echo "cgroup anon peak (sampled every 0.2 s): $(cat "$log.anon")"
  echo "cgroup memory.events: $(tr '\n' ' ' < "$cg/memory.events")"; } >> "$log"
rm -f "$log.stop" "$log.anon"
exit $rc
