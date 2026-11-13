#!/usr/bin/env bash
# audit.sh: static checks of the ENCBLEAN Lean sources. Exit 0 iff all pass.
#   1. no forbidden token in code (comments and docstrings stripped first): sorry, admit, native_decide,
#      implemented_by, extern, unsafe, partial, axiom, opaque, set_option (this covers debug.skipKernelTC),
#      ofReduceBool;
#   2. no Mathlib: no `import Mathlib` and no `[[require]]` in lakefile.toml;
#   3. toolchain is leanprover/lean4:v4.24.0 (the repository's);
#   4. no kernel evaluation of the (6,8,11) instance (DESIGN.md D9): every declaration (a column-0 command and its
#      continuation lines) that mentions encB/gen/genCoded/numVars/allCodes/allCodesOf/encode/diagCoded applied to
#      6 8 11 (any spacing), or CubesUnsat64, may not contain decide, rfl, simp, simp_all, simpa, dsimp, omega,
#      grind, trivial (core expands it to decide), Eq.refl, eq_self, Nat.decEq, decide_eq_true, native_decide,
#      of_decide_eq_true, #eval, #reduce, example or run_cmd anywhere in the declaration, so a tactic on a following
#      line is caught too;
#   5. time gate: `lake build --no-build` must report the build up to date, and every file with a declaration found
#      by check 4 (since M9: Cover.lean, Render.lean, Satisfiable.lean, Compose.lean) is elaborated again with
#      `timeout ${AUDIT_LEAN_TIMEOUT:-60} lake env lean FILE`; each takes about 0.3-2 s, while an evaluation of
#      `encB 6 8 11` takes 11 s compiled and far longer in the kernel. AUDIT_SKIP_TIMEGATE=1 skips check 5 (for
#      static tests on a scratch copy without a build); the run then ends AUDIT INCOMPLETE, exit 3, never AUDIT PASS.
# Check 4 is a text check and can be evaded by indirection (a local abbreviation for 6, say, or a tactic not in the
# list). The real protection is the build itself and check 5: the files that state (6,8,11) theorems must elaborate
# within the time limit. Run this script inside the capped scope (README, "How to build and run"), after `lake build`.
# The axiom check is done at build time by `#guard_msgs in #print axioms` in EncB/KernelCheck.lean (gen),
# EncB/KernelCheckB.lean (the M2 theorems), EncB/Satisfiable.lean (M3), EncB/Render.lean and EncB/Compose.lean (M9),
# and for the declarations of the package by the queries recorded in logs/axioms.log (M3) and logs/m9_axioms.log (M9).
set -u -o pipefail
cd "$(dirname "$0")/.." || exit 2
fail=0
GATE=()
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
RISK='(?<![\w#])(decide|rfl|simp|simp_all|simpa|dsimp|omega|grind|trivial|Eq\.refl|eq_self|Nat\.decEq|decide_eq_true|native_decide|of_decide_eq_true|example|run_cmd)(?![\w])|#eval\b|#reduce\b'
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
  [ -n "$out" ] && printf '%s\n' "$out" && GATE+=("$f")
  [ $rc -eq 0 ] || fail=1
done
# 5. time gate: the files that state (6,8,11) theorems elaborate within the limit, from an up-to-date build
TO=${AUDIT_LEAN_TIMEOUT:-60}
gate=ran
if [ "${AUDIT_SKIP_TIMEGATE:-0}" = 1 ]; then
  echo "time gate: SKIPPED (AUDIT_SKIP_TIMEGATE=1)"; gate=skipped
else
  export PATH="$HOME/.elan/bin:$PATH"
  if lake build --no-build > /dev/null 2>&1; then echo "time gate: lake build --no-build: up to date"
  else echo "time gate: lake build --no-build exit $? (build missing or stale; run lake build first)"; fail=1; fi
  [ ${#GATE[@]} -gt 0 ] || { echo "time gate: no file mentions the (6,8,11) instance (unexpected)"; fail=1; }
  for f in "${GATE[@]}"; do
    t0=$(date +%s.%N)
    timeout -k 5 "$TO" lake env lean "$f" > /dev/null 2>&1; rc=$?
    dt=$(echo "$(date +%s.%N) - $t0" | bc)
    if [ $rc -eq 0 ]; then printf 'time gate: %s elaborated in %.1f s (limit %s s)\n' "$f" "$dt" "$TO"
    else printf 'time gate: %s FAILED after %.1f s (limit %s s, exit %s%s)\n' "$f" "$dt" "$TO" "$rc" "$([ $rc -ge 124 ] && echo ', timeout')"; fail=1; fi
  done
fi
tc=$(cat lean-toolchain)
[ "$tc" = "leanprover/lean4:v4.24.0" ] || { echo "toolchain is '$tc'"; fail=1; }
echo "sources: $(echo $SRCS)"
echo "toolchain: $tc"
if [ $fail -ne 0 ]; then echo "AUDIT FAIL"; exit 1; fi
if [ $gate = skipped ]; then echo "AUDIT INCOMPLETE (static checks 1-4 pass; time gate 5 skipped)"; exit 3; fi
echo "AUDIT PASS (no sorry/admit/native_decide/implemented_by/extern/unsafe/partial/axiom/opaque/set_option/ofReduceBool in code; Std-only; no decide/rfl/simp/simpa/omega/grind/trivial/Eq.refl/#eval/#reduce in a declaration that mentions the (6,8,11) instance; the files stating (6,8,11) theorems elaborate within ${TO} s each)"
exit 0
