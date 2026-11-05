#!/bin/bash
# Rebuild modules under the hard cap of lean_make.sh (MemoryMax=12G with MemorySwapMax=0; 6 November 2026,
# review fixes), into OUTDIR, without touching build/ or any stamp, and compare each new .olean byte for byte
# with the one in build/. Every import must already be current (LM_NO_BUILD); nothing in build/ is rebuilt.
# Usage: hardcap_rebuild_es311.sh OUTDIR MODULE...   (a CompactChecker module, or an external one of LM_EXT)
# Prints one TSV row per module: module, exit, wall, peak RSS (time -v), cgroup memory.peak and
# memory.swap.peak (bytes), identical (yes/no), sha256 of the new .olean.
set -u -o pipefail
source "$(dirname "$0")/lean_make.sh"
export LM_NO_BUILD=1
[ $# -ge 2 ] || lm_die "usage: hardcap_rebuild_es311.sh OUTDIR MODULE..."
mkdir -p "$1" || exit 1
OUT=$(cd "$1" && pwd); shift
printf 'module\texit\twall\tpeak_rss_kb\tcg_memory_peak\tcg_swap_peak\tidentical\tolean_sha256\n'
for m in "$@"; do
  if [ -n "${LM_EXT[$m]+x}" ]; then
    IFS='|' read -r root rel pin <<< "${LM_EXT[$m]}"
    src=$root/$rel ref=$LM_B/ext/${m//.//}.olean
    ensure_ext "$m"
  else
    root=$LM_D src=$LM_D/CompactChecker/$m.lean ref=$LM_B/CompactChecker/$m.olean
    ensure "$m"
  fi
  o=$OUT/${m//.//}.olean log=$OUT/$m.log
  mkdir -p "$(dirname "$o")"; rm -f "$o"
  lm_compile "$root" "$src" "$o" "$log"; rc=$?
  osha=-; same=no
  if [ -f "$o" ]; then osha=$(lm_sha "$o"); [ "$osha" = "$(lm_sha "$LM_REPO/$ref")" ] && same=yes; fi
  v() { grep -m1 "$1" "$log" | sed 's/.*: //'; }
  printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' "$m" "$rc" "$(v 'Elapsed (wall')" "$(v 'Maximum resident')" \
    "$(v 'cgroup memory.peak')" "$(v 'cgroup memory.swap.peak')" "$same" "$osha"
done
