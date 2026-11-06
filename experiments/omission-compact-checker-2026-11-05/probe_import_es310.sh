#!/bin/bash
# Import probe E6 of the ES(8) <= 310 compact check (6 Nov 2026). ES(8) <= 310 is NOT proved.
#   probe_import_es310.sh [CAP]        (default CAP 4G; log: logs/es310/probe_import_es310-<time>.log)
# Question: are the imported .olean pages file-backed and reclaimable under a hard cgroup cap? If so, the
# Root, E310.Final and the assembly (which import 20-48 GB of chunk .olean) can run under 24G.
# Steps (design es310-design.md E6):
#  1. posix_fadvise(POSIX_FADV_DONTNEED) on every build/es311/full/olean/**/*.olean, each opened read-only
#     ("rb"): it drops their clean page-cache pages and changes no file (sizes, mtimes and sha256 are checked
#     unchanged at the end on a sample, and the file list/sizes/mtimes on all of them).
#  2. A probe file build/es310/test-e6-probe/ProbeE311.lean: `import E311.Final` and `#print axioms` of
#     E311.balanced_excludes_63 and E311.residual_excludes_32. It is compiled WITHOUT -o (no .olean is written
#     anywhere) by `lean -j1` in a transient scope: MemoryMax=CAP, MemorySwapMax=0, nice 10, under
#     /usr/bin/time -v; the scope's memory.peak and memory.events (oom_kill) are printed.
#     LEAN_PATH = lake's (lake env printenv LEAN_PATH, in a 2G scope) : build : build/ext : build/es311/full/olean
#     (the same roots as drive_es311.py used for E311.Final).
#  Pass: lean exit 0, oom_kill 0, both axiom lines standard. Fail: anything else.
# Waits for Tctl < 85 C and fewer than 2 lean processes before the compile. Nothing in build/es311 is written.
set -u -o pipefail
D=$(cd "$(dirname "$0")" && pwd)
REPO=$(cd "$D/../.." && pwd)
CAP=${1:-4G}
case "$CAP" in *[0-9][KMG]) ;; *) echo "CAP must be <number><K|M|G>"; exit 2 ;; esac
E311=$D/build/es311/full
W=$D/build/es310/test-e6-probe
LOG=$D/logs/es310/probe_import_es310-$(date +%Y%m%d-%H%M%S).log
mkdir -p "$W" "$D/logs/es310"
exec > >(tee "$LOG") 2>&1
echo "== $(date -u +%FT%TZ) import probe, cap $CAP; probe sha256 $(sha256sum < "$0" | cut -c1-16)"
python3 - "$E311/olean" "$W/before.json" <<'EOF'
import json, os, sys
root = sys.argv[1]
files = sorted(os.path.join(dp, f) for dp, _, fs in os.walk(root) for f in fs if f.endswith(".olean"))
json.dump({f: [os.stat(f).st_size, os.stat(f).st_mtime_ns] for f in files}, open(sys.argv[2], "w"))
EOF
command -v fincore >/dev/null && echo "page cache of build/es311/full/olean before: $(find "$E311/olean" -name '*.olean' -print0 | xargs -0 fincore -b -n -o RES 2>/dev/null | awk '{s+=$1} END {printf "%.2f GB", s/1e9}')"
python3 - "$E311/olean" <<'EOF'
import os, sys
n = b = 0
for dp, _, fs in os.walk(sys.argv[1]):
    for f in fs:
        if f.endswith(".olean"):
            p = os.path.join(dp, f)
            fd = os.open(p, os.O_RDONLY)
            try:
                os.posix_fadvise(fd, 0, 0, os.POSIX_FADV_DONTNEED)
            finally:
                os.close(fd)
            n += 1
            b += os.path.getsize(p)
print(f"posix_fadvise(DONTNEED) on {n} .olean files, {b / 1e9:.2f} GB (opened O_RDONLY)")
EOF
command -v fincore >/dev/null && echo "page cache of build/es311/full/olean after: $(find "$E311/olean" -name '*.olean' -print0 | xargs -0 fincore -b -n -o RES 2>/dev/null | awk '{s+=$1} END {printf "%.2f GB", s/1e9}')"
cat > "$W/ProbeE311.lean" <<'EOF'
import E311.Final
#print axioms E311.balanced_excludes_63
#print axioms E311.residual_excludes_32
EOF
LP=$(cd "$REPO" && systemd-run --user --scope --quiet -p MemoryMax=2G -p MemorySwapMax=0 nice -n 10 lake env printenv LEAN_PATH)
[ -n "$LP" ] || { echo "lake env printenv LEAN_PATH failed"; exit 2; }
export LEAN_PATH="$LP:$D/build:$D/build/ext:$E311/olean" LEAN_NUM_THREADS=1
for i in $(seq 360); do
  t=$(sensors 2>/dev/null | awk '/^Tctl:/ {gsub(/[^0-9.]/, "", $2); print $2; exit}'); n=$(pgrep -xc lean)
  [ -n "$t" ] && awk -v t="$t" 'BEGIN { exit !(t < 85) }' && [ "$n" -lt 2 ] && break
  sleep 10
done
echo "start: Tctl $t C, $n lean processes, MemAvailable $(awk '/MemAvailable/ {printf "%.1f GiB", $2/2^20}' /proc/meminfo)"
UNIT=es310-e6probe-$(date +%s)
WRAP='cg=/sys/fs/cgroup$(cut -d: -f3 /proc/self/cgroup); "$@"; rc=$?; echo "cgroup memory.peak: $(cat $cg/memory.peak)"; echo "cgroup memory.events: $(tr "\n" " " < $cg/memory.events)"; exit $rc'
cd "$REPO" && systemd-run --user --scope --quiet --unit="$UNIT" -p MemoryMax="$CAP" -p MemorySwapMax=0 \
  nice -n 10 sh -c "$WRAP" sh /usr/bin/time -v lean -j1 "$W/ProbeE311.lean" > "$W/probe.log" 2>&1
RC=$?
grep -E "depends on axioms|error|Exit status|Maximum resident|Elapsed|cgroup memory" "$W/probe.log"
OOM=$(sed -n 's/.*oom_kill \([0-9]*\).*/\1/p' "$W/probe.log" | tail -1)
NAX=$(grep -c "depends on axioms: \[propext, Classical.choice, Quot.sound\]" "$W/probe.log")
python3 - "$E311/olean" "$W/before.json" <<'EOF'
import json, os, sys
root, before = sys.argv[1], json.load(open(sys.argv[2]))
files = sorted(os.path.join(dp, f) for dp, _, fs in os.walk(root) for f in fs if f.endswith(".olean"))
now = {f: [os.stat(f).st_size, os.stat(f).st_mtime_ns] for f in files}
print("build/es311/full/olean unchanged (paths, sizes, mtimes):", now == before, f"({len(now)} files)")
EOF
echo "lean exit $RC, oom_kill ${OOM:-?}, standard axiom lines $NAX of 2"
if [ "$RC" -eq 0 ] && [ "${OOM:-1}" -eq 0 ] && [ "$NAX" -eq 2 ]; then echo "PROBE PASS (cap $CAP)"; else echo "PROBE FAIL (cap $CAP)"; exit 1; fi
