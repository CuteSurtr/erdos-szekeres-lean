#!/bin/bash
# Reviewer's one compile: bare lean v4.24.0 -j1, read-only LEAN_PATH copied from s3520-gate/tools/compile.sh
# (= res-slices-fv's stores, then the gate's olean/ LAST); output only under review/. Samples anon+shmem of its own cgroup.
set -u
RV=/home/jay/research/data/formalize-20261122/s3520-gate/review
G=/home/jay/research/data/formalize-20261122/s3520-gate
F=/home/jay/research/data/formalize-20261122/res-slices-fv
R=/home/jay/research/lean/erdos-szekeres-lean
P=$R/.lake/packages
X=$R/experiments/omission-compact-checker-2026-11-05
export LEAN_PATH="$P/Cli/.lake/build/lib/lean:$P/batteries/.lake/build/lib/lean:$P/Qq/.lake/build/lib/lean:$P/aesop/.lake/build/lib/lean:$P/proofwidgets/.lake/build/lib/lean:$P/importGraph/.lake/build/lib/lean:$P/LeanSearchClient/.lake/build/lib/lean:$P/plausible/.lake/build/lib/lean:$P/mathlib/.lake/build/lib/lean:$R/.lake/build/lib/lean:/home/jay/.elan/toolchains/leanprover--lean4---v4.24.0/lib/lean:$X/build/chain311/olean:/home/jay/research/data/bal186-20261119/zrow/leanz/olean:$F/olean:/home/jay/research/data/formalize-20261122/res118/olean:$G/olean"
echo "$LEAN_PATH" > $RV/logs/rv_lean_path.txt
cg=/sys/fs/cgroup$(cut -d: -f3 /proc/self/cgroup)
/usr/bin/time -v /home/jay/.elan/toolchains/leanprover--lean4---v4.24.0/bin/lean -j1 -R $RV/lean -o $RV/olean/RV3520.olean.tmp $RV/lean/RV3520.lean > $RV/logs/RV3520.log 2>&1 &
pid=$!; mx=0
while kill -0 $pid 2>/dev/null; do
  a=$(awk '$1=="anon"||$1=="shmem"{s+=$2} END{printf "%d", s/1048576}' $cg/memory.stat 2>/dev/null); [ "${a:-0}" -gt $mx ] && mx=$a; sleep 0.5
done
wait $pid; rc=$?
if [ $rc -eq 0 ]; then mv $RV/olean/RV3520.olean.tmp $RV/olean/RV3520.olean; else rm -f $RV/olean/RV3520.olean.tmp; fi
echo "lean_rc=$rc" >> $RV/logs/RV3520.log
echo "anon_shmem_max_mb=$mx rc=$rc cgroup=$cg" > $RV/logs/RV3520.mem
exit $rc
