#!/bin/sh
# Final stage of ES(8) <= 311, replacing the tail of pipeline2.sh with one fewer import of the whole chain.
# Waits for the running kernel check (Root) to finish, compiles Bridge63, then compiles Final311/Final.lean
# verbatim plus one appended `#check` (Final.lean already prints its axiom reports), audits, and writes the
# verdict. Never commits or pushes.
REPO="$(cd "$(dirname "$0")/../../.." && pwd)"; cd "$REPO" || exit 1
export ELAN_HOME="$REPO/.elan"; export PATH="$ELAN_HOME/bin:$PATH"
E=.cache/es311; ST="$E/final-status.txt"
say() { echo "$(date '+%F %T') $*" | tee -a "$E/pipeline.log"; }
fail() { say "FAILED: $*"; echo "FAILED $(date '+%F %T'): $*" > "$ST"; exit 1; }
say "finish.sh: waiting for the kernel check to finish"
while pgrep -f 'check_omission_lean.py .cache/es311/lean-export' >/dev/null; do sleep 60; done
tail -1 "$E/lean-check.log" | grep -q '"complete": true' || fail "kernel check incomplete (see $E/lean-check.log)"
say "kernel check complete"
F=experiments/omission-final311-2026-10-14/Final311; OUT="$REPO/$E/final-build"; mkdir -p "$OUT/Final311"
if grep -rnwE "sorry|admit|native_decide|sorryAx" "$F" >/dev/null || LC_ALL=C grep -rlF -e sorry -e admit -e native_decide "$E/lean-export/BalancedCover63Proof" --include='*.lean' | head -1 | grep -q .; then fail "placeholder found"; fi
LP="$OUT:$REPO/$E/lean-export:$REPO/.cache/runtime/final-build:$REPO/.cache/es313/lean-export:$REPO/.cache/omission-residual32-bridge2650-2026-10-11:$(lake env printenv LEAN_PATH)"
LEAN_PATH="$LP" lean -j1 -M 12000 "$F/Bridge63.lean" -o "$OUT/Final311/Bridge63.olean" > "$E/final-Bridge63.out" 2>&1 || fail "compile Bridge63 (see $E/final-Bridge63.out)"
say "Bridge63 compiled"
A="$OUT/FinalAudited.lean"
cp "$F/Final.lean" "$A"
printf '\n#check @ErdosSzekeres.Omission.forces_convex_octagon_311\n' >> "$A"
n=$(wc -c < "$F/Final.lean" | tr -d ' ')
head -c "$n" "$A" | cmp -s - "$F/Final.lean" || fail "audited copy differs from Final.lean"
LEAN_PATH="$LP" lean -j1 -M 12000 "$A" > "$E/final-audit.out" 2>&1 || fail "compile Final.lean (see $E/final-audit.out)"
# Final.lean opens ErdosSzekeres, so the appended #check prints namespace-relative names.
grep -qE "^(ErdosSzekeres\.)?Omission\.forces_convex_octagon_311 : (ErdosSzekeres\.)?ForcesConvexNGon 311 8$" "$E/final-audit.out" || fail "unexpected statement"
grep -qiE "error|declaration uses 'sorry'" "$E/final-audit.out" && fail "errors or sorry in $E/final-audit.out"
python3 - "$E/final-audit.out" <<'PY' || fail "unexpected axioms"
import re, sys
reps = dict(re.findall(r"'([^']+)' depends on axioms: \[([^]]*)\]", open(sys.argv[1]).read(), re.S))
need = ['ErdosSzekeres.Omission.forces_convex_octagon_311', 'ErdosSzekeres.Omission.convex_octagon_of_card_ge_311']
assert all(n in reps for n in need), reps.keys()
assert all({a.strip() for a in v.split(',') if a.strip()} <= {'propext', 'Classical.choice', 'Quot.sound'} for v in reps.values())
PY
say "VERIFIED forces_convex_octagon_311 : ForcesConvexNGon 311 8 (standard axioms only)"
echo "VERIFIED $(date '+%F %T'): forces_convex_octagon_311 : ForcesConvexNGon 311 8 (standard axioms only)" > "$ST"
