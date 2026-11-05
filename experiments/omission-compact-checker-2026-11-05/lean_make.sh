#!/bin/bash
# Make experiment modules current in build/ (6 November 2026).
#
# Usage: lean_make.sh MODULE...      (e.g. lean_make.sh Fast2 Chunk733G4Reject)
#    or: source lean_make.sh          (defines ensure / deps_of for run_bench_fast2.sh)
#
# A module CompactChecker.M is current when build/CompactChecker/M.olean exists and
# build/CompactChecker/M.stamp equals its stamp: the sha256 of
#   * the sha256 of CompactChecker/M.lean,
#   * the stamps of its CompactChecker imports (made current first, recursively),
#   * the sha256 of the library .olean of every other import (.lake/build/lib/lean/...),
#   * the repository's lean-toolchain.
# A module that is not current is rebuilt with `lean` on that one file, under the
# one-core cap, with its log in logs/make/M.log. A failed build stops everything.
# Lean itself does not check that an imported .olean matches its source, so this
# is what ties every benchmark run to a recorded source version.
#
# 6 November 2026 (ES(8) <= 311 recheck): three external prerequisites of the 311 bridges
# (Bridge311Bal.lean, Bridge311Res.lean) are made the same way, into build/ext/, from sources pinned by sha256
# (LM_EXT below; a source with another hash stops the script). Their imports are library
# modules or each other. BalancedProof/Catalog.lean is extracted from the committed
# sources.tar.gz of omission-balanced-lean-2026-10-09. LM_NICE (default 19) sets the nice
# level of every build; the 311 trial uses LM_NICE=5.
#
# 6 November 2026 (review fixes): every build runs through lm_compile, under the hard cap above, and its log
# ends with the scope's cgroup memory.peak and memory.swap.peak (charged memory, unlike the RSS that `time`
# reports, which also counts .olean pages mapped from the page cache).
set -u -o pipefail
LM_REPO=$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)
LM_D=experiments/omission-compact-checker-2026-11-05
LM_B=$LM_D/build
LM_LOG=$LM_D/logs/make
# MemoryMax alone does not limit swap: a scope may swap out past it and finish (tested 6 November 2026,
# logs/es311/review-fixes.txt). MemorySwapMax=0 makes the cap hard: past it the compile is OOM-killed.
# LM_MEM (default 12G) sets it. BalancedCoverCutsV2 does not fit in a hard 12G (OOM-killed with 12.4 GB of
# anonymous memory); its build/ext .olean was made on 6 November under the old, soft cap, with swap.
LM_CAP=(systemd-run --user --scope --quiet -p CPUQuota=100% -p MemoryMax="${LM_MEM:-12G}" -p MemorySwapMax=0 nice -n "${LM_NICE:-19}" ionice -c 3)
declare -A LM_STAMP LM_CLOSURE
# external module -> "root|source (relative to root)|sha256 of the source"
declare -A LM_EXT=(
  [BalancedProof.Catalog]="$LM_B/ext-src|BalancedProof/Catalog.lean|17080b3c93264fcffd6b5b075ec00c2e713a01914290e3d11e53e516b648583c"
  [BalancedCoverCutsV2]="experiments/omission-cover-certificates-2026-10-10|BalancedCoverCutsV2.lean|a79cf10030df67ae1cc2d5910a3bac5aedb69eb6e6284cb63b53873ac5bd64dc"
  [Residual32Bridge2650.Catalog]="experiments/omission-residual32-bridge2650-2026-10-11|Residual32Bridge2650/Catalog.lean|5b97f861a4bf4272d2d3d7bbadbb076261f5d7c3c9bd2e86fbf4b1a9e87a1c71"
)

lm_die() { echo "lean_make: $*" >&2; exit 1; }
lm_sha() { sha256sum < "$1" | cut -c1-64; }

# lm_compile ROOT SRC OLEAN LOG (paths relative to the repository, or absolute): one `lean` process under
# LM_CAP; LOG gets the `time -v` report and then the scope's cgroup memory.peak and memory.swap.peak (bytes).
lm_compile() {
  local log=$4
  case $log in /*) ;; *) log=$LM_REPO/$log ;; esac
  (cd "$LM_REPO" && LEAN_NUM_THREADS=1 OMP_NUM_THREADS=1 "${LM_CAP[@]}" \
    lake env bash -c "LEAN_PATH=\$LEAN_PATH:$LM_REPO/$LM_B:$LM_REPO/$LM_B/ext /usr/bin/time -v lean -R $1 -o $3 $2; rc=\$?
      cg=/sys/fs/cgroup\$(cut -d: -f3 /proc/self/cgroup)
      echo \"cgroup memory.peak: \$(cat \$cg/memory.peak 2>/dev/null)\"
      echo \"cgroup memory.swap.peak: \$(cat \$cg/memory.swap.peak 2>/dev/null)\"
      exit \$rc") > "$log" 2>&1
}

# ensure_ext M: make build/ext/<M as path>.olean current (external prerequisite, pinned source).
ensure_ext() {
  local m=$1 root rel pin src olean stampf stamp
  [ -n "${LM_STAMP[$m]+x}" ] && return 0
  IFS='|' read -r root rel pin <<< "${LM_EXT[$m]}"
  src=$root/$rel
  if [ "$m" = BalancedProof.Catalog ] && [ ! -f "$LM_REPO/$src" ]; then
    mkdir -p "$LM_REPO/$root/BalancedProof"
    tar xzf "$LM_REPO/experiments/omission-balanced-lean-2026-10-09/sources.tar.gz" -O Catalog.lean \
      > "$LM_REPO/$src" || lm_die "cannot extract $src"
  fi
  [ -f "$LM_REPO/$src" ] || lm_die "no source $src"
  [ "$(lm_sha "$LM_REPO/$src")" = "$pin" ] || lm_die "$src does not have the pinned sha256 $pin"
  deps_of "$LM_REPO/$src"
  LM_CLOSURE[$m]=$R_CLOSURE
  olean=$LM_B/ext/${m//.//}.olean
  stampf=$LM_B/ext/${m//.//}.stamp
  stamp=$(printf 'src=%s deps=%s' "$pin" "$R_STAMP" | sha256sum | cut -c1-64)
  if [ -f "$LM_REPO/$olean" ] && [ "$(cat "$LM_REPO/$stampf" 2>/dev/null)" = "$stamp" ]; then
    echo "lean_make: $m current (stamp ${stamp:0:16})" >&2
  else
    [ -z "${LM_NO_BUILD:-}" ] || lm_die "$m is not current and LM_NO_BUILD is set"
    echo "lean_make: $m rebuilding $(date +%T)" >&2
    mkdir -p "$(dirname "$LM_REPO/$olean")" "$LM_REPO/$LM_LOG"
    rm -f "$LM_REPO/$stampf"
    lm_compile "$root" "$src" "$olean" "$LM_LOG/$m.log" || lm_die "building $m failed; see $LM_LOG/$m.log"
    echo "$stamp" > "$LM_REPO/$stampf"
    echo "lean_make: $m built $(date +%T) (stamp ${stamp:0:16}; $(grep -E 'Elapsed|Maximum resident|cgroup memory.peak' "$LM_REPO/$LM_LOG/$m.log" | sed 's/.*: //' | tr '\n' ' '))" >&2
  fi
  LM_STAMP[$m]=$stamp
}

# deps_of FILE: make every CompactChecker import of FILE current; sets R_STAMP (hash of
# the imports' stamps and library .oleans) and R_CLOSURE (transitive CompactChecker modules).
deps_of() {
  local f=$1 imp y lib parts="" clo=""
  for imp in $(sed -n 's/^import \([A-Za-z0-9_.]*\).*/\1/p' "$f"); do
    case $imp in
      CompactChecker.*)
        y=${imp#CompactChecker.}
        ensure "$y"
        parts+=" $y=${LM_STAMP[$y]}"
        clo+=" ${LM_CLOSURE[$y]} $y" ;;
      *)
        if [ -n "${LM_EXT[$imp]+x}" ]; then
          ensure_ext "$imp"
          parts+=" $imp=${LM_STAMP[$imp]}"
          continue
        fi
        lib=$LM_REPO/.lake/build/lib/lean/${imp//.//}.olean
        [ -f "$lib" ] || lm_die "library module $imp is not built ($lib); not building the library here"
        parts+=" $imp=$(lm_sha "$lib")" ;;
    esac
  done
  parts+=" toolchain=$(lm_sha "$LM_REPO/lean-toolchain")"
  R_STAMP=$(printf '%s' "$parts" | sha256sum | cut -c1-64)
  R_CLOSURE=$(printf '%s\n' $clo | sort -u | tr '\n' ' ')
}

# ensure M: make build/CompactChecker/M.olean current; sets LM_STAMP[M] and LM_CLOSURE[M].
ensure() {
  local m=$1 src stamp olean
  [ -n "${LM_STAMP[$m]+x}" ] && return 0
  src=$LM_D/CompactChecker/$m.lean
  olean=$LM_B/CompactChecker/$m.olean
  [ -f "$LM_REPO/$src" ] || lm_die "no source $src"
  deps_of "$LM_REPO/$src"
  LM_CLOSURE[$m]=$R_CLOSURE
  stamp=$(printf 'src=%s deps=%s' "$(lm_sha "$LM_REPO/$src")" "$R_STAMP" | sha256sum | cut -c1-64)
  if [ -f "$LM_REPO/$olean" ] && [ "$(cat "$LM_REPO/$LM_B/CompactChecker/$m.stamp" 2>/dev/null)" = "$stamp" ]; then
    echo "lean_make: $m current (stamp ${stamp:0:16})" >&2
  else
    [ -z "${LM_NO_BUILD:-}" ] || lm_die "$m is not current and LM_NO_BUILD is set"
    echo "lean_make: $m rebuilding $(date +%T)" >&2
    mkdir -p "$LM_REPO/$LM_B/CompactChecker" "$LM_REPO/$LM_LOG"
    rm -f "$LM_REPO/$LM_B/CompactChecker/$m.stamp"
    lm_compile "$LM_D" "$src" "$olean" "$LM_LOG/$m.log" || lm_die "building $m failed; see $LM_LOG/$m.log"
    echo "$stamp" > "$LM_REPO/$LM_B/CompactChecker/$m.stamp"
    echo "lean_make: $m built $(date +%T) (stamp ${stamp:0:16}; $(grep -E 'Elapsed|Maximum resident|cgroup memory.peak' "$LM_REPO/$LM_LOG/$m.log" | sed 's/.*: //' | tr '\n' ' '))" >&2
  fi
  LM_STAMP[$m]=$stamp
}

# closure_olean_sha M: one sha256 over the .olean files of M's transitive CompactChecker imports.
closure_olean_sha() {
  local y
  for y in ${LM_CLOSURE[$1]}; do lm_sha "$LM_REPO/$LM_B/CompactChecker/$y.olean"; done | sha256sum | cut -c1-64
}

if [ "${BASH_SOURCE[0]}" = "$0" ]; then
  [ $# -ge 1 ] || lm_die "usage: lean_make.sh MODULE..."
  for m in "$@"; do if [ -n "${LM_EXT[$m]+x}" ]; then ensure_ext "$m"; else ensure "$m"; fi; done
fi
