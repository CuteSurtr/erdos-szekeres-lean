#!/bin/bash
# Old-vs-new benchmark on the 64-leaf chunk (6 November 2026; revised the same day).
# Usage (from anywhere): run_bench_fast2.sh TAG RUNS MODULE...
#   e.g. run_bench_fast2.sh 2026-11-06-hashed 5 Chunk733F Chunk733W4 Chunk733G4
# Before any run, every CompactChecker import of every MODULE (Packed, Fast, WordPack,
# Split, Fcat62, Fast2, ...) is made current by lean_make.sh: an .olean whose recorded
# source/dependency stamp does not match is rebuilt, and a failed build stops the script.
# Each compile is single-threaded under a one-core cgroup cap, nice 19, idle I/O;
# runs are interleaved round-robin so that load drift hits every module alike.
# Per-run logs: logs/bench-TAG/<module>.<run>.log; summary: logs/bench-TAG.tsv, with the
# sha256 of the chunk source and of Fast2.lean, the import stamp, and the sha256 of the
# imported .olean files taken before the run and re-checked after it (deps_unchanged).
# The first 6 November benchmark (logs/bench-2026-11-06.tsv, logs/bench/) was made by an
# earlier version of this script that did none of this.
set -u -o pipefail
D=experiments/omission-compact-checker-2026-11-05
source "$(dirname "$0")/lean_make.sh"
cd "$LM_REPO"
[ $# -ge 3 ] || lm_die "usage: run_bench_fast2.sh TAG RUNS MODULE..."
TAG=$1 RUNS=$2; shift 2
OUT=$D/build/bench
LOGS=$D/logs/bench-$TAG
TSV=$D/logs/bench-$TAG.tsv
HEADER=$'module\trun\tleaves\tkernel_s\ts_per_leaf\twall_s\tpeak_rss_kb\tolean_bytes\tkb_per_leaf\taxioms\tload1\tchunk_sha256\tfast2_sha256\tdeps_stamp\tdeps_olean_sha256\tdeps_unchanged'
if [ -f $TSV ]; then
  [ "$(head -1 $TSV)" = "$HEADER" ] || lm_die "$TSV exists with another header; pick a new TAG"
else
  mkdir -p $(dirname $TSV); printf '%s\n' "$HEADER" > $TSV
fi
mkdir -p $OUT $LOGS
declare -A DSTAMP
for m in "$@"; do
  [ -f $D/CompactChecker/$m.lean ] || lm_die "no module $m"
  deps_of $PWD/$D/CompactChecker/$m.lean
  DSTAMP[$m]=$R_STAMP; LM_CLOSURE[$m]=$R_CLOSURE
done
export LEAN_NUM_THREADS=1 OMP_NUM_THREADS=1
for run in $(seq 1 $RUNS); do
  for m in "$@"; do
    log=$LOGS/$m.$run.log
    load=$(cut -d' ' -f1 /proc/loadavg)
    src_sha=$(lm_sha $D/CompactChecker/$m.lean)
    f2_sha=$(lm_sha $D/CompactChecker/Fast2.lean)
    before=$(closure_olean_sha $m)
    rm -f $OUT/$m.olean
    "${LM_CAP[@]}" lake env bash -c "LEAN_PATH=\$LEAN_PATH:$PWD/$D/build /usr/bin/time -v lean -R $D -o $OUT/$m.olean $D/CompactChecker/$m.lean" > $log 2>&1
    after=$(closure_olean_sha $m)
    [ "$before" = "$after" ] && same=yes || same=NO
    python3 - "$log" "$OUT/$m.olean" "$m" "$run" "$load" "$src_sha" "$f2_sha" "${DSTAMP[$m]}" "$before" "$same" >> $TSV <<'EOF'
import os, re, sys
log, olean, m, run, load, src_sha, f2_sha, dstamp, before, same = sys.argv[1:]
t = open(log).read()
def secs(x):
    return float(x[:-2]) / 1000 if x.endswith("ms") else float(x[:-1])
k = max((secs(x) for x in re.findall(r"type checking took (\S+)", t)), default=float("nan"))
leaves = int(re.search(r"subtree root node \d+: (\d+) leaves", open(re.search(r"Command being timed: .* (\S+\.lean)\"", t).group(1)).read()).group(1))
w = re.search(r"Elapsed \(wall clock\) time \(h:mm:ss or m:ss\): (\S+)", t).group(1).split(":")
wall = sum(float(p) * 60 ** i for i, p in enumerate(reversed(w)))
rss = int(re.search(r"Maximum resident set size \(kbytes\): (\d+)", t).group(1))
ax = re.search(r"depends on axioms: \[([^\]]*)\]", t)
size = os.path.getsize(olean) if "Exit status: 0" in t and os.path.exists(olean) else 0
print(f"{m}\t{run}\t{leaves}\t{k:.3f}\t{k / leaves:.4f}\t{wall:.2f}\t{rss}\t{size}\t{size / leaves / 1000:.2f}\t"
      f"{ax.group(1).replace(', ', '+') if ax else 'none'}\t{load}\t{src_sha}\t{f2_sha}\t{dstamp}\t{before}\t{same}")
EOF
    tail -1 $TSV | cut -f1-11,16
  done
done
