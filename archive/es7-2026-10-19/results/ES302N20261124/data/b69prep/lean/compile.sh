#!/bin/sh
# compile.sh (b69-prep): elaborate BindN54.lean (expect rc 0) and two negative controls (expect rc 1: the Z-row demand
# 15 instead of 16; one Z index changed) with the pinned v4.24.0 binary and the comp-audit's read-only LEAN_PATH
# (library roots of chain311/lake-lean-path.txt : chain311/olean : comp-audit/out/olean). No -o: nothing is written
# except the .out files and compile.log here. Body of unit esr-ag-b69p-lean* (1 thread, MemoryMax 3000M).
C=/home/jay/research/lean/erdos-szekeres-lean/experiments/omission-compact-checker-2026-11-05/build/chain311
export LEAN_PATH="$(cat $C/lake-lean-path.txt):$C/olean:/home/jay/research/data/formalize-20261122/comp-audit/out/olean"
export LEAN_NUM_THREADS=1
cd /home/jay/research/data/bal186-20261119/b69prep/lean
: > compile.log
for f in BindN54 BindN54_neg15 BindN54_negZ; do
  timeout 600 /home/jay/.elan/toolchains/leanprover--lean4---v4.24.0/bin/lean -j1 $f.lean > $f.out 2>&1
  echo "$f lean_rc=$? sha256=$(sha256sum < $f.lean | cut -c1-64)" >> compile.log
done
cg=/sys/fs/cgroup$(cut -d: -f3 /proc/self/cgroup)
{ echo "cgroup memory.peak: $(cat $cg/memory.peak)"; echo "cgroup memory.events: $(tr '\n' ' ' < $cg/memory.events)"; } >> compile.log
