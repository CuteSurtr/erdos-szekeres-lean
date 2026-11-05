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
set -u -o pipefail
LM_REPO=$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)
LM_D=experiments/omission-compact-checker-2026-11-05
LM_B=$LM_D/build
LM_LOG=$LM_D/logs/make
LM_CAP=(systemd-run --user --scope --quiet -p CPUQuota=100% -p MemoryMax=12G nice -n 19 ionice -c 3)
declare -A LM_STAMP LM_CLOSURE

lm_die() { echo "lean_make: $*" >&2; exit 1; }
lm_sha() { sha256sum < "$1" | cut -c1-64; }

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
    echo "lean_make: $m rebuilding $(date +%T)" >&2
    mkdir -p "$LM_REPO/$LM_B/CompactChecker" "$LM_REPO/$LM_LOG"
    rm -f "$LM_REPO/$LM_B/CompactChecker/$m.stamp"
    (cd "$LM_REPO" && LEAN_NUM_THREADS=1 OMP_NUM_THREADS=1 "${LM_CAP[@]}" \
      lake env bash -c "LEAN_PATH=\$LEAN_PATH:$LM_REPO/$LM_B /usr/bin/time -v lean -R $LM_D -o $olean $src") \
      > "$LM_REPO/$LM_LOG/$m.log" 2>&1 || lm_die "building $m failed; see $LM_LOG/$m.log"
    echo "$stamp" > "$LM_REPO/$LM_B/CompactChecker/$m.stamp"
    echo "lean_make: $m built $(date +%T) (stamp ${stamp:0:16}; $(grep -E 'Elapsed|Maximum resident' "$LM_REPO/$LM_LOG/$m.log" | sed 's/.*: //' | tr '\n' ' '))" >&2
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
  for m in "$@"; do ensure "$m"; done
fi
