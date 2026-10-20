#!/bin/sh
# Copy the live J2 run logs into logs/ (committed). Reads through /proc/<pid>/fd so that
# logs whose path was replaced in the working tree are still captured.  Run from results/J2.
mkdir -p logs/pb logs/base_random logs/base_seeds
for pid in $(pgrep -f "python3 src/(pb|baseline).py"); do
  for fd in /proc/$pid/fd/*; do
    t=$(readlink $fd) || continue
    case "$t" in
      *results/J2/runs/*.jsonl*|*results/J2/runs/*.log*)
        rel=${t#*results/J2/runs/}; rel=${rel% (deleted)}
        cat $fd > logs/$rel.tmp && mv logs/$rel.tmp logs/$rel ;;
    esac
  done
done
for f in runs/pb/best.txt runs/pb/pool_top.txt runs/base_random/best.txt runs/base_seeds/best.txt \
         runs/*/ZERO_CANDIDATES.txt runs/base_*/found_top.txt; do
  [ -f "$f" ] && cp "$f" "logs/${f#runs/}"
done
