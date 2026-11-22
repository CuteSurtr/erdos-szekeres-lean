#!/bin/bash
# mutant.sh NAME FILE PYEXPR MODULE...: copy src/ and olean/ to mut/NAME, apply a one-line Python replacement
# PYEXPR (old|||new) to FILE, compile MODULE... in order against the copy (LP_SELF with the copy first) and
# report the first failing module. A mutant is KILLED iff some module fails.
set -u
. /home/jay/research/data/formalize-20261122/sevenfold/tools/env.sh
name=$1; file=$2; expr=$3; shift 3
M=$W/mut/$name
rm -rf "$M"; mkdir -p "$M"; cp -r "$W/src" "$M/src"; cp -r "$W/olean" "$M/olean"
python3 -I -c "
import sys
p, e = sys.argv[1], sys.argv[2]
old, new = e.split('|||')
s = open(p).read()
assert s.count(old) == 1, ('pattern count', s.count(old))
open(p, 'w').write(s.replace(old, new))
" "$M/src/$file" "$expr" || { echo "MUTANT $name: pattern not found"; exit 2; }
export LEAN_PATH="$TC/lib/lean"
for p in aesop batteries importGraph LeanSearchClient mathlib plausible proofwidgets Qq; do LEAN_PATH="$LEAN_PATH:$G/.lake/packages/$p/.lake/build/lib/lean"; done
export LEAN_PATH="$LEAN_PATH:$M/olean"
cd "$M/src"
for mod in "$@"; do
  f="${mod//.//}.lean"; o="$M/olean/${mod//.//}.olean"
  if ! "$LEAN" -j1 -R "$M/src" -o "$o" "$f" > "$M/$mod.out" 2>&1; then
    echo "MUTANT $name: KILLED at $mod: $(grep -m1 'error' "$M/$mod.out" | cut -c1-160)"; rm -rf "$M"; exit 0
  fi
done
echo "MUTANT $name: SURVIVED (all of $* compiled)"; rm -rf "$M"; exit 1
