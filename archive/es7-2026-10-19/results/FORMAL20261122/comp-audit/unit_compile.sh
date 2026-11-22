#!/bin/sh
# comp-audit: body of one esr-ag-lcmp-* unit (cwd = the flat source dir; LEAN_PATH comes from the unit's environment).
# Compiles SRC to OUT.tmp with the pinned v4.24.0 binary, renames it to OUT on success, and appends lean_rc and the
# unit's cgroup memory figures (memory.peak, a 0.2 s sample of the anon peak, memory.events) to LOG, as capped() in
# experiments/omission-compact-checker-2026-11-05/assemble_final310.sh does.
# Usage: unit_compile.sh LOG OUT.olean SRC.lean
log=$1 out=$2 src=$3
cg=/sys/fs/cgroup$(cut -d: -f3 /proc/self/cgroup)
rm -f "$log.stop" "$log.anon"
( m=0; while [ ! -e "$log.stop" ]; do
    a=$(awk '$1=="anon"{print $2}' "$cg/memory.stat"); [ "${a:-0}" -gt "$m" ] && m=$a
    echo "$m" > "$log.anon"; sleep 0.2; done ) &
/usr/bin/time -v /home/jay/.elan/toolchains/leanprover--lean4---v4.24.0/bin/lean -j1 -R . -o "$out.tmp" "$src" > "$log" 2>&1
rc=$?
touch "$log.stop"; wait
if [ $rc -eq 0 ] && [ -f "$out.tmp" ]; then mv "$out.tmp" "$out"; else rm -f "$out.tmp"; fi
{ echo "lean_rc=$rc"
  echo "cgroup memory.peak: $(cat "$cg/memory.peak")"
  echo "cgroup memory.swap.peak: $(cat "$cg/memory.swap.peak")"
  echo "cgroup anon peak (sampled every 0.2 s): $(cat "$log.anon")"
  echo "cgroup memory.events: $(tr '\n' ' ' < "$cg/memory.events")"; } >> "$log"
rm -f "$log.stop" "$log.anon"
exit $rc
