#!/usr/bin/env bash
# audit.sh: static checks of the ENCBLEAN Lean sources. Exit 0 iff all pass.
#   1. no forbidden token in code (comments and docstrings stripped first): sorry, admit, native_decide,
#      implemented_by, extern, unsafe, partial, axiom, opaque;
#   2. no Mathlib: no `import Mathlib` and no `[[require]]` in lakefile.toml;
#   3. toolchain is leanprover/lean4:v4.24.0 (the repository's).
# The axiom check itself is done at build time by `#guard_msgs in #print axioms` in EncB/KernelCheck.lean.
set -u -o pipefail
cd "$(dirname "$0")/.."
fail=0
SRCS=$(ls EncB.lean EncB/*.lean)
for f in $SRCS; do
  # strip /- ... -/ blocks (non-nested is enough here) and -- line comments, keep line count
  code=$(perl -0777 -pe 's{/-.*?-/}{ my $s=$&; $s =~ tr/\n//cd; $s }gse; s{--[^\n]*}{}g' "$f")
  hits=$(printf '%s\n' "$code" | grep -nwE 'sorry|admit|native_decide|implemented_by|extern|unsafe|partial|axiom|opaque' || true)
  if [ -n "$hits" ]; then echo "FORBIDDEN in $f:"; echo "$hits"; fail=1; fi
  if grep -nE '^\s*import\s+Mathlib' "$f"; then echo "MATHLIB import in $f"; fail=1; fi
done
if grep -n '^\s*\[\[require\]\]' lakefile.toml; then echo "lakefile.toml has a [[require]]"; fail=1; fi
tc=$(cat lean-toolchain)
[ "$tc" = "leanprover/lean4:v4.24.0" ] || { echo "toolchain is '$tc'"; fail=1; }
echo "sources: $(echo $SRCS)"
echo "toolchain: $tc"
[ $fail -eq 0 ] && echo "AUDIT PASS (no sorry/admit/native_decide/implemented_by/extern/unsafe/partial/axiom/opaque in code; Std-only)" || echo "AUDIT FAIL"
exit $fail
