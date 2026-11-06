#!/usr/bin/env bash
# audit.sh: static checks of the ENCBLEAN Lean sources. Exit 0 iff all pass.
#   1. no forbidden token in code (comments and docstrings stripped first): sorry, admit, native_decide,
#      implemented_by, extern, unsafe, partial, axiom, opaque, set_option (this covers debug.skipKernelTC),
#      ofReduceBool;
#   2. no Mathlib: no `import Mathlib` and no `[[require]]` in lakefile.toml;
#   3. toolchain is leanprover/lean4:v4.24.0 (the repository's);
#   4. no kernel evaluation of the (6,8,11) instance (DESIGN.md D9): every declaration (a column-0 command and its
#      continuation lines) that mentions encB/gen/genCoded/numVars/allCodes/allCodesOf/encode/diagCoded applied to
#      6 8 11 (any spacing), or CubesUnsat64, may not contain decide, rfl, simp, simp_all, dsimp, omega,
#      native_decide, of_decide_eq_true, #eval, #reduce, example or run_cmd anywhere in the declaration, so a tactic
#      on a following line is caught too.
# Check 4 is a text check and can be evaded by indirection (a local abbreviation for 6, say). The real protection
# is the build itself: Cover.lean, which states the (6,8,11) theorems, builds in under a second.
# The axiom check is done at build time by `#guard_msgs in #print axioms` in EncB/KernelCheck.lean (gen) and
# EncB/KernelCheckB.lean (the M2 theorems), and for every declaration of the package by the query recorded in
# logs/axioms.log.
set -u -o pipefail
cd "$(dirname "$0")/.."
fail=0
SRCS=$(ls EncB.lean EncB/*.lean)
# strip /- ... -/ blocks (non-nested is enough here) and -- line comments, keep line count
strip() { perl -0777 -pe 's{/-.*?-/}{ my $s=$&; $s =~ tr/\n//cd; $s }gse; s{--[^\n]*}{}g' "$1"; }
for f in $SRCS; do
  code=$(strip "$f")
  hits=$(printf '%s\n' "$code" | grep -nwE 'sorry|admit|native_decide|implemented_by|extern|unsafe|partial|axiom|opaque|set_option|skipKernelTC|ofReduceBool' || true)
  if [ -n "$hits" ]; then echo "FORBIDDEN in $f:"; echo "$hits"; fail=1; fi
  if grep -nE '^\s*import\s+Mathlib' "$f"; then echo "MATHLIB import in $f"; fail=1; fi
done
if grep -n '^\s*\[\[require\]\]' lakefile.toml; then echo "lakefile.toml has a [[require]]"; fail=1; fi
# 4. the kernel never evaluates the (6,8,11) instance (DESIGN.md D9)
PAT='\b(encB|gen|genCoded|numVars|allCodes|allCodesOf|encode|diagCoded)\s+6\s+8\s+11\b|\bCubesUnsat64\b'
RISK='(?<![\w#])(decide|rfl|simp|simp_all|dsimp|omega|native_decide|of_decide_eq_true|example|run_cmd)(?![\w])|#eval\b|#reduce\b'
echo "declarations mentioning the (6,8,11) instance (pattern: $PAT):"
for f in $SRCS; do
  out=$(strip "$f" | PAT="$PAT" RISK="$RISK" F="$f" perl -e '
    my ($pat, $risk, $f) = ($ENV{PAT}, $ENV{RISK}, $ENV{F});
    my @lines = <STDIN>; my @blocks; my ($start, $buf) = (1, "");
    my $kw = qr/^(?:@\[|#\w|theorem|lemma|def|abbrev|instance|example|structure|inductive|class|axiom|opaque|private|protected|noncomputable|partial|unsafe|namespace|end|section|open|set_option|attribute|variable|universe|import|mutual|macro|syntax|elab|deriving|initialize|run_cmd|run_tac|run_elab)\b/;
    for my $i (0 .. $#lines) {
      if ($lines[$i] =~ $kw && $buf =~ /\S/) { push @blocks, [$start, $buf]; ($start, $buf) = ($i + 1, ""); }
      elsif ($lines[$i] =~ $kw) { $start = $i + 1; }
      $buf .= $lines[$i];
    }
    push @blocks, [$start, $buf] if $buf =~ /\S/;
    my $bad = 0;
    for my $b (@blocks) {
      my ($s, $t) = @$b;
      next unless $t =~ /$pat/;
      my ($first) = grep { /$pat/ } split /\n/, $t; $first //= (grep { /\S/ } split /\n/, $t)[0]; $first =~ s/^\s+//;
      my $n = () = $t =~ /\n/g;
      if ($t =~ /$risk/) { print "  KERNEL EVALUATION RISK $f:$s (+$n lines, token \"$&\"): $first\n"; $bad = 1; }
      else { print "  $f:$s (+$n lines): $first\n"; }
    }
    exit $bad;'); rc=$?
  [ -n "$out" ] && printf '%s\n' "$out"
  [ $rc -eq 0 ] || fail=1
done
tc=$(cat lean-toolchain)
[ "$tc" = "leanprover/lean4:v4.24.0" ] || { echo "toolchain is '$tc'"; fail=1; }
echo "sources: $(echo $SRCS)"
echo "toolchain: $tc"
[ $fail -eq 0 ] && echo "AUDIT PASS (no sorry/admit/native_decide/implemented_by/extern/unsafe/partial/axiom/opaque/set_option/ofReduceBool in code; Std-only; no decide/rfl/simp/omega/#eval/#reduce in a declaration that mentions the (6,8,11) instance)" || echo "AUDIT FAIL"
exit $fail
