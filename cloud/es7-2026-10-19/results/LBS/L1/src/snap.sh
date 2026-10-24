#!/bin/bash
# copy live run logs (possibly unlinked) and best sets into snap/
cd "$(dirname "$0")/.." && mkdir -p snap
for pid in $(pgrep -x 'lbs2?'); do
  pre=$(tr '\0' ' ' < /proc/$pid/cmdline | awk '{print $4}'); s=$(basename $pre)
  for fd in /proc/$pid/fd/*; do l=$(readlink $fd); case "$l" in *runs.txt*) cat $fd > snap/$s.runs.txt;; esac; done
done
for f in runs/*.best.txt; do cp $f snap/; done
