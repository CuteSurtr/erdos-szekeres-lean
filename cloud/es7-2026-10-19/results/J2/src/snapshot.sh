#!/bin/sh
# Copy the live J2 run logs (runs/, not committed) into logs/ (committed). Reads through
# /proc/<pid>/fd so a log whose path was replaced in the working tree is still captured.
# Run from results/J2.
for pid in $(pgrep -f "python3 src/(pb|baseline).py"); do
  for fd in /proc/$pid/fd/*; do
    t=$(readlink $fd) || continue
    case "$t" in
      *results/J2/runs/*.jsonl*|*results/J2/runs/*.log*)
        rel=${t#*results/J2/runs/}; rel=${rel% (deleted)}
        mkdir -p "$(dirname logs/$rel)"
        cat $fd > logs/$rel.tmp && mv logs/$rel.tmp logs/$rel ;;
    esac
  done
done
for d in runs/*/; do
  a=$(basename $d)
  for f in best.txt pool_top.txt found_top.txt ZERO_CANDIDATES.txt; do
    [ -f "$d$f" ] && mkdir -p logs/$a && cp "$d$f" logs/$a/$f
  done
done
